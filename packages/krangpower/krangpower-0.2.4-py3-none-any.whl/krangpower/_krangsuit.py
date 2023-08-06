import copy
import gc
import hashlib
import io
import json
import os.path
import pickle
import re
import weakref
import xml.etree.ElementTree as ElementTree
import zipfile
from csv import reader as csvreader
from functools import wraps, singledispatch
from logging import INFO as LOGGING_INFO
from tokenize import tokenize, untokenize

import canonicaljson
import networkx as nx
import numpy as np
import pandas
from scipy.sparse import csc_matrix

from . import _busquery as bq
from . import _components as co
from . import enhancer
from ._aux_fcn import get_help_out, bus_resolve, diff_dicts
from ._config_loader import PINT_QTY_TYPE, ELK, DEFAULT_KRANG_NAME, UM, DSSHELP, COMMAND_LOGPATH, MAIN_LOGPATH, \
    TMP_PATH, GLOBAL_PRECISION, LSH_ZIP_NAME, DEFAULT_SETTINGS, BASE_FREQUENCY, TMK, BYPASS_REGEX, BCOMMAND_LOGPATH
from ._deptree import DepTree as _DepGraph
from ._exceptions import KrangInstancingError, KrangObjAdditionError, ClearingAttemptError
from ._logging_init import remove_filehandlers, add_rotfilehandler, mlog, clog, bclog, add_comfilehandler
from ._pbar import PBar as _PBar
from .enhancer.OpendssdirectEnhancer import pack
from ._krg2cdf import krg2cdf as _krg2cdf

# __all__ = ['Krang', 'from_json', 'CACHE_ENABLED', 'open_ckt']
_FQ_DM_NAME = 'dm.pkl'

CACHE_ENABLED = True
_INSTANCE = None  # krang singleton support variable

_CIRCUIT_INIT_RE = re.compile('(new *(object *=)? *circuit\.)' # beginning of declaration
                              '([^(\n| )]+)'  # circuit name
                              '([^!|\n]+)?' # first parameters
                              '( *(![^\n]+)?)'  # optional first comment
                              '(\n *(![^\n]+)*)*'  # optional sequence of newlines/comments
                              '((more|~ * [^\n]+\n)*)',  # optional continuation blocks

                              re.IGNORECASE)

_MORE_RE = re.compile('(more|~ *)', re.IGNORECASE)

_CLEAR_RE = re.compile('\n *clear', re.IGNORECASE)


# -----------------------------------------------------------------------------------------------------------------
# CONTEXT MANAGER FOR TEMPORARY VARIATION OF CWD
# -----------------------------------------------------------------------------------------------------------------
class _KrangCwdRedirector:
    # context manager for safe variation of krang cwd
    def __init__(self, target_krang, target_cwd: str):
        self.kr = target_krang
        self.t_cwd = target_cwd

    def __enter__(self):
        self.kr.brain.Basic.DataPath(self.t_cwd)
        return self.kr

    def __exit__(self, *args):
        self.kr.brain.Basic.DataPath(TMP_PATH)


# -----------------------------------------------------------------------------------------------------------------
# HELP DECORATOR
# -----------------------------------------------------------------------------------------------------------------
def _helpfun(config, section):
    """This decorator adds a 'help' submethod to a function or method, and is meant to read a series of help (
    property, desc) pairs from a config file. The help method is invoked by function.help(), just prints stuff to the
    console and returns nothing. """

    def _real_helpfun(f):
        @wraps(f)
        def ghelp():
            print('\nPARAMETERS HELP FOR FUNCTION {0} ({1})\n'.format(f.__name__, section))
            print(get_help_out(config, section))

        f.help = ghelp
        return f

    return _real_helpfun


# -----------------------------------------------------------------------------------------------------------------
# DECORATORS FOR VOLATILE METHOD CACHING
# -----------------------------------------------------------------------------------------------------------------
def _invalidate_cache(f):
    # this decorator is meant to be used with those Krang methods that alter the circuit described by the Krang,
    # thus invalidating the method cache accumulated till that moment
    @wraps(f)
    def cached_invalidator_f(self, *args, **kwargs):
        if hasattr(self, '_fncache'):
            self._fncache = {}
        elif hasattr(self.oek, '_fncache'):
            self.oek._fncache = {}
        else:
            raise AttributeError
        return f(self, *args, **kwargs)

    return cached_invalidator_f


def _is_bypassable(cmd_str):
    for rx in BYPASS_REGEX:
        if rx.search(cmd_str) is not None:
            return True

    return False


def _invalidate_graphcache_on_command(f_command):
    # this decorator is meant to be used with those Krang methods that alter the circuit described by the Krang,
    # thus invalidating the method cache accumulated till that moment

    @wraps(f_command)
    def cached_invalidator_f(self, cmd_str, echo=True):
        if not _is_bypassable(cmd_str):
            if hasattr(self, '_graphcache'):
                self._graphcache = None
            elif hasattr(self.oek, '_graphcache'):
                self.oek._graphcache = None
            else:
                raise AttributeError
        return f_command(self, cmd_str, echo)

    return cached_invalidator_f


def _invalidate_cache_outside(oek):
    # this decorator is meant to be used with functions outside Krang  that nevertheless alter the circuit described by
    # the currently instantiated Krang, thus invalidating the method cache
    def _direct_invalidate_cache(f):
        if hasattr(oek, '_fncache'):
            oek._fncache = {}
        else:
            raise AttributeError
        return f

    return _direct_invalidate_cache


def _cache(f):
    # this decorator is meant to be used with expensive Krang methods that can be cached and don't change value
    # until the Krang is actively modified
    @wraps(f)
    def cached_f(self, *args, **kwargs):
        if CACHE_ENABLED:
            try:
                return self._fncache[f.__name__]
            except KeyError:
                value = f(self, *args, **kwargs)
                self._fncache[f.__name__] = value
                return value
        else:
            return f(self, *args, **kwargs)

    cached_f.__name__ = f.__name__
    return cached_f


def _graph_cache(f):
    # this decorator is meant to be used with expensive Krang methods that can be cached and don't change value
    # until the Krang is actively modified
    @wraps(f)
    def cached_f(self, *args, **kwargs):
        if CACHE_ENABLED:
            if self._graphcache is not None:
                return self._graphcache
            else:
                value = f(self, *args, **kwargs)
                self._graphcache = value
                return value
        else:
            return f(self, *args, **kwargs)

    cached_f.__name__ = f.__name__
    return cached_f


# -----------------------------------------------------------------------------------------------------------------
# ------------------------------------------ _ --------------------------------------------------------------------
#                                           | | ___ __ __ _ _ __   __ _
#                                           | |/ | '__/ _` | '_ \ / _` |
#                                           |   <| | | (_| | | | | (_| |
#                                           |_|\_|_|  \__,_|_| |_|\__, |
# ----------------------------------------------------------------|___/--------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
class Krang(object):
    """The krang is an object capable of creating, editing, solving and retrieving information about an electrical
    distribution system."""
    def __new__(cls, *args, **kwargs):

        # For increased safety, we explicitly garbage-collect
        gc.collect()

        # Krang is a singleton; attempting to create a second one will raise an error
        if globals()['_INSTANCE'] is not None:
            raise KrangInstancingError(globals()['_INSTANCE'])

        return super().__new__(cls)

    def __init__(self,
                 name=DEFAULT_KRANG_NAME,
                 voltage_source=co.Vsource(),
                 source_bus_name='sourcebus',
                 working_frequency=BASE_FREQUENCY,
                 redirect_path=False):

        # first of all, we double-check that we arrived at initialization with _INSTANCE == None
        assert globals()['_INSTANCE'] is None
        # we immediately assign a weakref to self
        globals()['_INSTANCE'] = weakref.ref(self)

        # public attributes
        self.id = name
        """Krang.id is a string identifier for the krang that is used in the logs."""
        self.brain = enhancer
        """Krang.brain points to krangpower.enhancer It has the same interface as OpenDSSDirect.py, but
        can pack objects and returns enhanced data structures such as pint qtys and numpy arrays."""

        # private attributes
        self._flags = {'coords_preloaded': False}
        self._csvloadshapes = []
        self._ai_list = []
        self._fncache = {}
        self._graphcache = None
        self._coords_linked = {}

        # file output redirection to the temp folder
        # current_cwd = os.getcwd()
        # this function has the side effect of changing the cwd
        if redirect_path:
            self.brain.Basic.DataPath(TMP_PATH)
        # os.chdir(current_cwd)

        # binding the file formatters to the module-wide loggers
        add_rotfilehandler(mlog, MAIN_LOGPATH)
        add_rotfilehandler(clog, COMMAND_LOGPATH)
        add_comfilehandler(bclog, BCOMMAND_LOGPATH)

        # OpenDSS initialization commands
        self.command('clear')
        master_string = self._form_newcircuit_string(name, voltage_source, source_bus_name)
        self.command(master_string)
        self.set(mode='duty')
        self.set(basefreq=working_frequency * UM.Hz)
        self.set(defaultbasefrequency=working_frequency * UM.Hz)
        self.set(frequency=working_frequency * UM.Hz)

        # in order to make 'sourcebus' recognizable since the beginning
        self.command('makebuslist')

    # -----------------------------------------------------------------------------------------------------------------
    # CLASS UTILITY METHODS
    # -----------------------------------------------------------------------------------------------------------------

    @classmethod
    def open_ckt(cls, path):
        """Loads a ckt package saved through Krang.pack_ckt() and returns a Krang."""
        return _open_ckt(path)

    @classmethod
    def from_json(cls, path):
        """Loads circuit data from a json structured like the ones returned by Krang.save_json. Declaration precedence due
        to dependency between objects is automatically taken care of."""
        return _from_json(path)

    @classmethod
    def from_dss(cls, file_path, target_krang=None, frequency=BASE_FREQUENCY):
        """from_dss(file_path, target_krang, frequency) allows to create a krang from an existing dss script or to pass
        commands to a krang from an existing dss script. USE AT YOUR OWN RISK.

        :param file_path: The path of the dss file to utilize
        :param target_krang:

         - If None, a new krang will be created and initialized with the information from the file (must
           contain a 'new circuit' command).
         - If a Krang is passed, the commands in the script will be passed to that Krang.

        :param frequency: the general frequency to use for the krang, if a new one is created.
        """
        return _from_dss(file_path, target_krang, frequency)

    # -----------------------------------------------------------------------------------------------------------------
    # DUNDERS AND PRIMITIVE FUNCTIONALITY
    # -----------------------------------------------------------------------------------------------------------------

    def __del__(self):
        # clearing the circuit from the underlying OpenDSS
        self.brain.Basic.ClearAll()
        # removing the filehandlers from the module-wide loggers
        remove_filehandlers(mlog)
        remove_filehandlers(clog)
        remove_filehandlers(bclog)
        # resetting the global singleton-controlling variable
        globals()['_INSTANCE'] = None

    @property
    def name(self):
        """The name of the circuit.."""
        return self.brain.Circuit.Name()

    @property
    def com(self):
        """Krang.com is a list of all the commands sent to the text interface throughout the Krang's lifespan."""
        with open(BCOMMAND_LOGPATH, 'r') as bcfile:
            return bcfile.read()

    @staticmethod
    def get_unit_registry():
        """Retrieves krangpower's UnitRegistry."""
        return UM

    @property
    def _named_entities(self):
        nms = [x for x in self.brain.get_all_names()
               if x.split('.', 1)[0] in ('tsdata', 'cndata', 'linecode', 'wiredata', 'linegeometry')]
        return [self[n].unpack() for n in nms]

    @staticmethod
    def _form_newcircuit_string(name, vsource, source_bus_name):
        master_string = 'new object = circuit.' + name + ' '
        vsource.name = 'source'  # we force the name, so an already named vsource can be used as source.
        main_source_dec = vsource.fcs(buses=(source_bus_name, source_bus_name + '.0.0.0'))
        main_dec = re.sub('New vsource\.source ', '', main_source_dec)
        main_dec = re.sub('bus2=[^ ]+ ', '', main_dec)
        master_string += ' ' + main_dec + '\n'
        return master_string

    def __getitem__(self, item):
        """Krang['bus.nname'], Krang['load.load1'], Krang['load1'] gets the component or a list of components of the bus;
        Krang[('bus.nname',)], Krang['bus.b1','bus.b2'] gets a BusView to which you can add components with <<.
        Note that in order to get a BusView of a single bus, one needs to explicitly pack it in a tuple.
        """
        # implemented outside for rigid single dispatching between strings and tuples
        return _oe_getitem(item, self)

    def __getattr__(self, item):
        """Krang.item, aside from retrieving the builtin attributes, wraps by default the calls to opendssdirect's
        'class_to_dataframe' utility function. These are accessible via capital letter calls. Both singular and plural
        are accepted. (e.g., 'Line' or 'Lines', 'RegControl' , 'Regcontrol', 'RegControls', but not 'transformers')"""
        try:
            assert item[0].isupper()
            dep_item = re.sub('s$', '', item).lower()
            return self.brain.utils.class_to_dataframe(dep_item)
        except (AssertionError, NotImplementedError):
            raise AttributeError('{0} is neither a valid attribute nor a valid identifier for the class-views.'.format(
                item
            ))

    @_invalidate_cache
    def __lshift__(self, other):
        """The left-shift operator << adds components to the Krang. Components that can and have to be directly added
        to the krang are those that represent data (WireData, TSData, LineGeometry...) or those that are in the circuit
        but above the topology (such as Monitors and all the Controllers).
        The names of these elements must not be blank when they are added."""
        try:
            assert other.isnamed()
            if isinstance(other, co.CsvLoadshape):
                self._csvloadshapes.append(other)
        except AssertionError:
            try:
                assert other.isabove()
            except AssertionError:
                raise KrangObjAdditionError(other, msg='The object {} could not be directly added to the Krang.'
                                                       ' Is it a bus-bound object?'.format(str(other)))

        try:
            assert other.name != ''
        except AssertionError:
            raise KrangObjAdditionError(other, msg='Tried to add an object ({}) with a blank name'.format(str(other)))

        # we direct-declare possibly undeclared objects that were associated with other
        for ass_obj in other._multiplied_objs:
            if ass_obj.fullname not in self.brain.get_all_names():
                # notice that we can also associate _packedopendsselements, that would fail as arguments to <<
                # because they don't have an isnamed attribute, etc; but _packedopendsselements should already be
                # in brain.get_all_names!!!!!
                self << ass_obj

        self.command(other.fcs())
        self.brain._names_up2date = False
        return self

    # -----------------------------------------------------------------------------------------------------------------
    # OPENDSS COMMANDS AND OPTIONS
    # -----------------------------------------------------------------------------------------------------------------

    @_helpfun(DSSHELP, 'EXECUTIVE')
    @_invalidate_cache
    @_invalidate_graphcache_on_command
    def command(self, cmd_str: str, echo=True):
        """Performs an opendss textual command and adds the commands to the record Krang.com if echo is True."""

        # checks that you're not trying to clear after a circuit is brought into existence,
        # because that would wreak havoc with the existing krang.
        if self.brain.Basic.NumCircuits() != 0:
            if _CLEAR_RE.search(cmd_str):
                raise ClearingAttemptError

        rslt = self.brain.txt_command(cmd_str, echo)
        return rslt

    @_helpfun(DSSHELP, 'OPTIONS')
    @_invalidate_cache
    def set(self, **opts_vals):
        """Sets circuit options according to a dict. Option that have a physical dimensionality (such as stepsize) can
        be specified as pint quantities; otherwise, the default opendss units will be used."""
        for option, value in opts_vals.items():
            if hasattr(value, 'magnitude'):
                vl = value.to(UM.parse_units(DEFAULT_SETTINGS['units'][option])).magnitude
            else:
                vl = value

            _RETRY = 10
            for rt in range(_RETRY):

                self.command('set {0}={1}'.format(option, vl))
                revl = self.get(option)[option]
                if hasattr(revl, 'magnitude'):
                    revl = revl.magnitude

                # acknowledge
                try:
                    if isinstance(value, str):
                        assert revl.lower().startswith(vl.lower())
                    else:
                        assert np.allclose(revl, vl)

                    break
                except AssertionError:
                    mlog.warning('Option {0}={1} was not correctly acknowledged (value == {2}), retry #{3}/{4}'
                                 .format(option, vl, self.get(option)[option], rt, _RETRY))
                    continue
            else:
                raise IOError('OpenDSS could not acknowledge option {0}={1} (value == {2})'
                              .format(option, vl, self.get(option)[option]))

    @_helpfun(DSSHELP, 'OPTIONS')
    def get(self, *opts):
        """Takes a list of circuit options and returns them as dict of name, value."""
        assert all([x in list(DEFAULT_SETTINGS['values'].keys()) for x in opts])
        r_opts = {opt: self.command('get {0}'.format(opt), echo=False).split('!')[0] for opt in opts}

        for op in r_opts.keys():
            tt = type(DEFAULT_SETTINGS['values'][op])
            if tt is list:
                r_opts[op] = eval(r_opts[op])  # lists are literals like [13]
            else:
                r_opts[op] = tt(r_opts[op])
            if op in DEFAULT_SETTINGS['units'].keys():
                r_opts[op] *= UM.parse_units(DEFAULT_SETTINGS['units'][op])

        return r_opts

    def get1(self, opt):
        return self.get(opt)[opt]

    @_helpfun(DSSHELP, 'EXPORT')
    def export(self, object_descriptor):
        """Wraps the OpenDSS export command. Returns a DataFrame for csv exports, an ElementTree for xml exports.
        This method has a help attribute that prints to console the available options."""
        tmp_filename = self.command('export ' + object_descriptor)
        if tmp_filename.lower().endswith('csv'):
            return pandas.read_csv(tmp_filename)
        elif tmp_filename.lower().endswith('xml'):
            return ElementTree.parse(tmp_filename)
        else:
            raise ValueError('Unknown format for export file {0}, contact the developer'.format(tmp_filename))

    # -----------------------------------------------------------------------------------------------------------------
    # INTERNAL OPENDSS REPRESENTATION WRAPPERS
    # -----------------------------------------------------------------------------------------------------------------

    @_helpfun(DSSHELP, 'PLOT')
    def plot(self, object_descriptor):
        """Wraps the OpenDSS plot command. This method has a help attribute that prints to console the available
         options."""
        self.command('plot ' + object_descriptor)

    @_helpfun(DSSHELP, 'SHOW')
    def show(self, object_descriptor):
        """Wraps the OpenDSS show command. This method has a help attribute that prints to console the available
         options."""
        self.command('show ' + object_descriptor)

    # -----------------------------------------------------------------------------------------------------------------
    # SOLUTION METHODS
    # -----------------------------------------------------------------------------------------------------------------

    def drag_solve(self):
        """This command solves one step at a time and saves node currents
        and voltages in the two DataFrames returned."""
        nmbr = self.brain.Solution.Number()
        self.brain.Solution.Number(1)
        v = pandas.DataFrame(
            columns=[x.lower() for x in self.brain.Circuit.YNodeOrder()])
        i = pandas.DataFrame(
            columns=[x.lower() for x in self.brain.Circuit.YNodeOrder()])

        self.brain.log_line_on_debug_log('Commencing drag_solve of {0} points: the individual "solve" commands will be omitted.'
                            ' Wait for end message...'.format(nmbr))
        for _ in _PBar(range(nmbr), level=LOGGING_INFO):
            for ai_el in self._ai_list:
                self.command(ai_el.fus(self, ai_el.name))

            self.solve(echo=False)
            v = v.append(self.brain.Circuit.YNodeVArray(), ignore_index=True)
            i = i.append(self.brain.Circuit.YCurrents(), ignore_index=True)

        self.brain.log_line_on_debug_log('Drag_solve ended')
        self.brain.Solution.Number(nmbr)

        return v, i

    def snap(self):
        """Solves a circuit snapshot."""
        n = self.get('number', 'stepsize')
        self.set(mode='snap')
        self.solve()
        self.set(mode='duty')
        self.set(**n)  # a snap solve internally sets number to 1, so we have to reset it

    def custom_drag_solve(self, *qties, as_dict=False):
        """This command solves one step at a time and returns a list of values (of length equal to the number of steps
        solved) for each of the quantities indicated, as strings, in the arguments.
        For example:

        pwr, lss = myKrang.custom_drag_solve('myKrang["agent_1"].Powers()', 'myKrang.brain.Circuit.Losses()')

        (returns two lists with the values assumed by the expressions passed after each solution steps).

        DEPRECATED IN FAVOR OF Krang.evalsolve

        """

        # we tokenize qties in order to replace the name with self
        r_qties = []
        linq = {}
        for q in qties:
            rsq = []
            tkn = tokenize(io.BytesIO(q.encode('utf-8')).readline)
            for idx, (toknum, tokval, _, _, _) in enumerate(tkn):
                if idx == 1:  # the content of token number 1 is replaced with "self"
                    rsq.append((toknum, 'self'))
                else:  # everything else is left untouched
                    rsq.append((toknum, tokval))
            r_qty = untokenize(rsq).decode('utf-8').replace(' ', '')
            if r_qty not in r_qties:
                r_qties.append(r_qty)
                linq[r_qty] = q

        nmbr = self.brain.Solution.Number()
        self.brain.Solution.Number(1)
        rslt = {linq[q]: None for q in r_qties}

        for n in _PBar(range(nmbr), level=LOGGING_INFO):
            for ai_el in self._ai_list:
                if n == 0:  # it's possible that, at the first step, there's no solution for the ai_el to query.
                    try:    # So we just pass and the solution will use the default values
                        self.command(ai_el.fus(self, ai_el.name))
                    except OSError:
                        self.snap()
                        self.command(ai_el.fus(self, ai_el.name))
                else:  # from the 2nd step on, the command has to work correctly, so no try block.
                    self.command(ai_el.fus(self, ai_el.name))
            self.solve()
            for q in r_qties:
                rslt[linq[q]] = eval(q)

        self.brain.Solution.Number(nmbr)

        if as_dict:
            return rslt
        else:
            return list(rslt.values())

    def evalsolve(self, *fns, every_steps=1, always_rebuild_Y=False, as_df=True, detect_multindex=True):
        """Solves the circuit for the set number of steps, evaluating the function passed at each step and returning the
        results.
        Accepts as arguments a series of functions that take a Krang object as input.
        Returns a dictionary or a DF; each item/column contains the returned values of the corresponding function
        passed, indicized by simulation time.

        :param fns: the functions to evaluate, passed as sequence of *args. The functions have to accept one positional
         argument of type Krang, as they will be passed this instance.
        :param every_steps: Every how many steps to perform the evaluation. Default = 1.
        :param always_rebuild_Y: Whether to impart the 'BuildY' command before solving.
        :param as_df: Whether to return the results in a dict or in a pandas.DataFrame
        :param detect_multindex: (NOT YET IMPLEMENTED) if set to True, and so is as_df, evalsolve checks if all the
         individual results returned by the functions are dicts with the same keys. If so, those keys are used as a
         multi-index for the DataFrame.
        """

        nmbr = self.brain.Solution.Number()
        self.brain.Solution.Number(every_steps)
        rslt = {fname: [] for fname in [x.__name__ for x in fns]}
        timestamps = []

        for n in range(nmbr):  # _PBar(range(nmbr), level=LOGGING_INFO):
            for ai_el in self._ai_list:
                if n == 0:  # it's possible that, at the first step, there's no solution for the ai_el to query.
                    try:    # So we just pass and the solution will use the default values
                        self.command(ai_el.fus(self, ai_el.name))
                    except OSError:
                        self.snap()
                        self.command(ai_el.fus(self, ai_el.name))
                else:  # from the 2nd step on, the command HAS to work correctly, so no try block.
                    self.command(ai_el.fus(self, ai_el.name))

            if always_rebuild_Y:
                self.command('BuildY')

            self.solve()
            timestamps.append(self.brain.Solution.DblHour().to('hour').magnitude)
            for fn in fns:
                evaluation = fn(self)
                rslt[fn.__name__].append(evaluation)

        self.brain.Solution.Number(nmbr)

        if as_df:
            main_col_names = [x.__name__ for x in fns]

            if detect_multindex:
                complexive_dict = {}
                for fn_name in main_col_names:
                    for putative_dict in rslt[fn_name]:
                        complexive_dict.update({(fn_name, k): v for k, v in putative_dict.items()})

                rslt_df = pandas.DataFrame(complexive_dict)

            else:

                rslt_df = pandas.DataFrame(index=timestamps, columns=main_col_names)
                for fn in fns:
                    rslt_df[fn.__name__] = rslt[fn.__name__]

            return rslt_df
        else:
            return rslt

    @_cache
    def Ybus_noload(self):
        """Returns the Ybus matrix of the existing circuit with all loads, generators set to 0 kW and 0 kVAr.
        The Ybus computed in such a way can be used to compute the load/generator injection currents as Ybus_noload * V,
        where V is the node voltage vector computed in any other condition of load.
        The matrix is returned in Compressed Sparse Column representation.
        """

        target_elements = [x for x in self.brain.get_all_names() if x.split('.')[0] in ('load', 'generator')]
        if target_elements:
            # fp0 = self.fingerprint()
            for t in target_elements:
                self.command('disable {}'.format(t))

            self.command('BuildY')
            self.snap()  # otherwise it does not really trigger the build

            y0 = csc_matrix(self.brain.Circuit.SystemY().values)

            for t in target_elements:
                self.command('enable {}'.format(t))

            # assert self.fingerprint() == fp0
            # disable-enable is trustworthy. No need for lengthy fingerprint comparison
        else:
            y0 = csc_matrix(self.brain.Circuit.SystemY().values)

        return y0

    def solve(self, echo=True):
        """Imparts the solve command to OpenDSS."""
        if self._flags['coords_preloaded']:
            self._declare_buscoords()
        self.command('solve', echo)

    # -----------------------------------------------------------------------------------------------------------------
    # COORDINATES-RELATED METHODS
    # -----------------------------------------------------------------------------------------------------------------

    @_invalidate_cache
    def _preload_buscoords(self, path):
        """Loads in a local dict the buscoords from path."""
        with open(path, 'r') as bc_file:
            bcr = csvreader(bc_file)
            try:
                while True:
                    try:
                        row = next(bcr)
                        float(row[1])
                        float(row[2])
                        break
                    except ValueError:
                        continue
            except StopIteration:
                # this means that we hit stopiteration of bcr without finding a valid line
                # for which float(row[x]) did not raise ValueError, thus breaking the while
                raise ValueError('No valid coords found in file "{0}"'.format(path))

            while row:
                self._coords_linked[str(row[0])] = [float(row[1]), float(row[2])]
                try:
                    row = next(bcr)
                except StopIteration:
                    break
        self._flags['coords_preloaded'] = True
        return

    @_invalidate_cache
    def _declare_buscoords(self):
        """Meant to be called just before solve, so that all buses are already mentioned"""
        self.command('makebuslist')
        for busname, coords in self._coords_linked.items():
            if coords is not None:
                try:
                    self['bus.' + busname].X(coords[0])
                    self['bus.' + busname].Y(coords[1])
                except KeyError:
                    continue  # we ignore buses present in coords linked, but not generated
            else:
                continue
        self._flags['coords_preloaded'] = False

    @_invalidate_cache
    def link_coords(self, csv_path):
        """Notifies Krang of a csv file with bus coordinates to use."""
        # todo sanity check
        self._preload_buscoords(csv_path)

    @_cache
    def bus_coords(self):
        """Returns a dict with the bus coordinates already loaded in Opendss. Beware that coordinates loaded through
        a link_kml or link_csv are not immediately loaded in the Opendss, but they are just before a solution is
        launched. """

        # why not?
        if self._flags['coords_preloaded']:
            self._declare_buscoords()

        bp = {}
        for bn in self.brain.Circuit.AllBusNames():
            if self['bus.' + bn].Coorddefined():
                bp[bn] = (self['bus.' + bn].X(), self['bus.' + bn].Y())
            else:
                bp[bn] = None
        return bp

    # -----------------------------------------------------------------------------------------------------------------
    # PICKLING, PACKING, HASHING
    # -----------------------------------------------------------------------------------------------------------------

    @_cache
    def fingerprint(self):
        """Returns the md5 hash digest for Krang.make_json_dict() in canonical form. Its main use is to compare two
        circuits in order to confirm that they are equivalent."""
        return hashlib.md5(canonicaljson.encode_canonical_json(self.make_json_dict())).hexdigest()

    @_cache
    def _zip_csv(self):
        csvflo = io.BytesIO()
        with zipfile.ZipFile(csvflo, mode='w', compression=zipfile.ZIP_DEFLATED) as csvzip:
            for csvlsh in [x for x in self._csvloadshapes]:
                with open(csvlsh.csv_path, 'br') as cfile:
                    csvzip.writestr(os.path.basename(csvlsh.csv_path),
                                    cfile.read())
        return csvflo

    @_cache
    def _pickle_fourq(self):
        fqglo = io.BytesIO()
        pickle.dump(self._ai_list, fqglo, protocol=pickle.HIGHEST_PROTOCOL)

        return fqglo

    @_cache
    def make_json_dict(self):
        """Returns a complete description of the circuit and its objects as a json.dumpable-dict."""
        master_dict = {'cktname': self.name, 'elements': {}, 'settings': {}}

        # elements
        for Nm in self.brain.Circuit.AllElementNames(): # _PBar(self.brain.Circuit.AllElementNames(), level=LOGGING_INFO, desc='jsonizing elements...'):
            nm = Nm.lower()
            master_dict['elements'][nm] = self[nm].unpack().jsonize()
            master_dict['elements'][nm]['topological'] = self[nm].topological

        # named entities
        for ne in self._named_entities: # _PBar(self._named_entities, level=LOGGING_INFO, desc='jsonizing named entities...'):
            master_dict['elements'][ne.fullname] = ne.jsonize()

        # loadshapes
        for ls in self._csvloadshapes: # _PBar(self._csvloadshapes, level=LOGGING_INFO, desc='jsonizing loadshapes...'):
            master_dict['elements'][ls.fullname] = ls.jsonize()

        # options
        dumpable_settings = set(DEFAULT_SETTINGS['values'].keys()) - set(DEFAULT_SETTINGS['contingent'])
        opts = self.get(*dumpable_settings)
        for on, ov in _PBar(opts.items(), level=LOGGING_INFO, desc='jsonizing options...'):
            if isinstance(ov, PINT_QTY_TYPE):
                opts[on] = np.round(ov.to(UM.parse_units(DEFAULT_SETTINGS['units'][on])).magnitude,
                                    decimals=GLOBAL_PRECISION)
                if isinstance(opts[on], (np.ndarray, np.matrix)):
                    # settings are never matrices; this happens because when *ing a list for a unit, the content
                    # becomes an array.
                    opts[on] = opts[on].tolist()
                if isinstance(opts[on], (np.int32, np.int64)):
                    opts[on] = int(opts[on])
            elif isinstance(ov, float):
                opts[on] = np.round(opts[on], decimals=GLOBAL_PRECISION)
            elif isinstance(ov, (np.ndarray, np.matrix)):
                np.round(opts[on], decimals=GLOBAL_PRECISION).tolist()

        master_dict['settings']['values'] = opts
        master_dict['settings']['units'] = DEFAULT_SETTINGS['units']

        # coordinates
        master_dict['buscoords'] = self.bus_coords()

        return master_dict

    def save_json(self, path=None, indent=2):
        """Saves a complete JSON description of the circuit and its objects. If a valid path string is passed,
        a file will be created, and None will be returned; if None is passed as path, a Text buffered  Stream
        (io.StringIO) with the exact same information as the file will be returned instead."""

        if path is None:
            vfile = io.StringIO()
            json.dump(self.make_json_dict(), vfile, indent=indent)
            return vfile

        else:
            with open(path, 'w') as ofile:
                json.dump(self.make_json_dict(), ofile, indent=indent)
            return None

    def pack_ckt(self, path=None):
        """Packs a ckt archive with all the information needed to reproduce the Krang. If a valid path string is passed,
        a file will be created, and None will be returned; if None is passed as path, a Binary buffered I/O
        (io.BytesIO) with the exact same information as the file will be returned instead."""

        self._declare_buscoords()  # otherwise dangling coordinates would not be saved

        if path is None:
            spath = io.BytesIO()
        else:
            spath = path

        with zipfile.ZipFile(spath, mode='w', compression=zipfile.ZIP_DEFLATED) as packfile:
            packfile.writestr(LSH_ZIP_NAME, self._zip_csv().getvalue())
            packfile.writestr(_FQ_DM_NAME, self._pickle_fourq().getvalue())
            jsio = io.StringIO()
            json.dump(self.make_json_dict(), jsio, indent=2)
            packfile.writestr(self.name + '.json', jsio.getvalue())
            md5io = io.StringIO(self.fingerprint())
            packfile.writestr('krang_hash.md5', md5io.getvalue())

        if path is None:
            return spath
        else:
            return None

    def save_dss(self, path=None):
        """Saves a file with the text commands that were imparted by the Krang.command method aside from those for which
        echo was False. The file output should be loadable and runnable in traditional OpenDSS with no modifications.
        """

        if path is None:
            return self.com

        with open(path, 'w') as ofile:
            ofile.write(self.com)

    def to_cdf(self):
        raise NotImplemented
        # return _krg2cdf(self)

    # -----------------------------------------------------------------------------------------------------------------
    #  GRAPH
    # -----------------------------------------------------------------------------------------------------------------

    @_graph_cache
    def graph(self):
        """Krang.graph is a Networkx.Graph that contains a description of the circuit. The elements are stored as
        _PackedOpendssElement's in the edge/node property 'el'. More information about how to make use of the graph
        can be found in the dedicated page."""

        def _update_node(myself, graph, bus, terminal, myname):
            try:
                exel = graph.nodes[bus][ELK]

            except KeyError:
                graph.add_node(bus, **{ELK: [myself[myname]],
                                       TMK: {myname: terminal}})
                return
            exel.append(myself[myname])
            graph.nodes[bus][TMK].update({myname: terminal})
            return

        def _update_edge(myself, graph, ed, terminals, myname):
            try:
                exel = graph.edges[ed][ELK]
            except KeyError:
                graph.add_edge(*ed, **{ELK: [myself[myname]],
                                       TMK: {myname: dict(zip(ed, terminals))}})
                return
            exel.append(myself[myname])
            graph.edges[ed][TMK].update({myname: dict(zip(ed, terminals))})
            return

        gr = nx.Graph()
        ns = self.brain.Circuit.AllElementNames()
        for name in ns:
            try:
                buses = self[name].BusNames()
            except (TypeError, AttributeError):
                continue

            if len(buses) == 1:
                bs, t = bus_resolve(buses[0])

                _update_node(self, gr, bs, t, name)

                # gr.add_node(bs, **{_elk: self.oe[name]})
            elif len(buses) == 2:
                bs0, t0 = bus_resolve(buses[0])
                bs1, t1 = bus_resolve(buses[1])

                _update_edge(self, gr, (bs0, bs1), (t0, t1), name)

                # gr.add_edge(bs0, bs1, **{_elk: self.oe[name]})
            else:
                assert self[name].eltype == 'transformer'
                nw = self[name].NumWindings()
                bs0, t0 = bus_resolve(buses[0])

                # we ASSUME that there is one primary winding and it's the first
                for w in range(1, nw):
                    bsw, tw = bus_resolve(buses[w])
                    _update_edge(self, gr, (bs0, bsw), (t0, tw), name)

        # pack all the buses together with the elements
        for n in gr.nodes:
            gr.nodes[n]['bus'] = self['bus.' + str(n)]

        return gr

    def peek(self):
        import matplotlib
        matplotlib.use('Qt5Agg')
        import matplotlib.pyplot as plt

        self._declare_buscoords()

        stpos = {x: y for x, y in self.bus_coords().items() if y is not None}
        if stpos == {}:
            posi = nx.spring_layout(self.graph())
        else:
            posi = nx.spring_layout(self.graph(), pos=stpos, fixed=stpos)

        nx.draw_networkx(self.graph(), pos=posi)
        plt.show()

# -------------------------------------------------------------
# Single-dispatched __getitem__
# -------------------------------------------------------------

@singledispatch
def _oe_getitem(item, krg):
    # no default implementation
    raise TypeError('Invalid identificator passed. You can specify fully qualified element names as str, or bus/'
                    'couples of buses as tuples of str.')


@_oe_getitem.register(str)
def _(item, krg):

    pe = pack(item)
    # packedopendsselements returned through a krang have to invalidate
    # the whole cache when their setitem method is used to modify something
    pe.__setitem__ = _invalidate_cache_outside(weakref.proxy(krg))(pe.__setitem__)
    return pe


@_oe_getitem.register(tuple)
def _(item, krg):
    # assert len(item) <= 2
    bustermtuples = map(bus_resolve, item)
    return _BusView(krg, list(bustermtuples))


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------_---------------------_-------------------------------------------------
#                                   | |__  _   _ _____   _(_) _____      __
#                                   | '_ \| | | / __\ \ / / |/ _ \ \ /\ / /
#                                   | |_) | |_| \__ \\ V /| |  __/\ V  V /
# ----------------------------------|_.__/ \__,_|___/ \_/ |_|\___| \_/\_/ -----------------------------------
# -----------------------------------------------------------------------------------------------------------
class _BusView:
    def __init__(self, oek: Krang, bustermtuples):
        self.btt = bustermtuples
        self.tp = [b[1] for b in bustermtuples]
        self.buses = [b[0] for b in bustermtuples]
        self.nb = len(self.buses)
        self.oek = weakref.proxy(oek)
        self._content = None

        buskey = 'buses'
        tkey = 'terminals'

        self.fcs_kwargs = {buskey: self.buses, tkey: self.tp}

    @_invalidate_cache
    def __lshift__(self, other):
        """Adds a component to the BusView, binding the component added to the buses referenced by the BusView."""
        try:
            assert not other.isnamed()
        except (AssertionError, AttributeError):
            raise KrangObjAdditionError(other, msg='Tried to add an incompatible object.')

        try:
            assert other.name != ''
        except AssertionError:
            raise KrangObjAdditionError(other, 'Could not add object {}. Did you remember to'
                                               ' name the element before adding it?'
                                        .format(other))

        # we declare possibly undeclared objects that were associated with other (loadshapes...)
        for ass_obj in other._multiplied_objs:
            if ass_obj.fullname not in self.oek.brain.get_all_names():
                self.oek << ass_obj

        self.oek.command(other.fcs(**self.fcs_kwargs))

        # remember ai elements
        if other.isai():
            self.oek._ai_list.append(other)

        return self

    def __str__(self):
        return '<BusView' + str(self.buses) + '>'

    def __repr__(self):
        return self.__str__()

    @property
    def content(self):
        """A list containing the PackedOpendssElements bound to the BusView's buses."""
        # todo remove reliance on self.oek.graph (not very urgent)
        if self._content is None:
            # CONTENT IS NOT UPDATED AFTER FIRST EVAL
            if len(self.buses) == 1:
                try:
                    self._content = self.oek.graph().nodes[self.buses[0]][ELK]
                    # it's ok that a KeyError by both indexes is caught in the same way
                except KeyError:
                    self._content = []
            elif len(self.buses) == 2:
                self._content = list(nx.get_edge_attributes(self.oek.graph().subgraph(self.buses), ELK).values())
            else:
                # if more than two buses, we search among the transformers.
                self._content = []
                for trf_name in self.oek.brain.Transformers.AllNames():
                    buses_set = set(self.oek[trf_name].BusNames())
                    if buses_set == set(self.buses):
                        self._content.append(self.oek[trf_name])
        return self._content

    def __getattr__(self, item):
        """Calculates a quantity from the submodule busquery on the BusView."""

        try:
            # attributes requested via getattr are searched in busquery
            f = bq.get_fun(item)
        except KeyError:
            raise AttributeError('Attribute/query function {0} is not implemented'.format(item))

        if self.nb == 1:
            return f(self.oek, self, self.buses[0])
        elif self.nb == 2:
            return f(self.oek, self, self.buses)
        else:
            raise AttributeError


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------___-----_-----------------_---------------------------
#                               ___  __ ___   _____   ( _ )   | | ___   __ _  __| |
#                              / __|/ _` \ \ / / _ \  / _ \/\ | |/ _ \ / _` |/ _` |
#                              \__ \ (_| |\ V /  __/ | (_>  < | | (_) | (_| | (_| |
# -----------------------------|___/\__,_| \_/ \___|  \___/\/ |_|\___/ \__,_|\__,_|--------------------------
# -----------------------------------------------------------------------------------------------------------
def _from_json(path, redirect_path=False, final_snap=True):
    """Loads circuit data from a json structured like the ones returned by Krang.save_json. Declaration precedence due
    to dependency between object is automatically taken care of."""
    # load all entities
    if isinstance(path, str):
        with open(path, 'r') as ofile:
            master_dict = json.load(ofile)
    else:
        master_dict = json.load(path)

    # init the krang with the source, then remove it from the dict
    l_ckt = Krang(master_dict['cktname'], co.dejsonize(master_dict['elements']['vsource.source']), redirect_path=redirect_path)
    # todo see if it's sourcebus
    del master_dict['elements']['vsource.source']

    # load and declare options
    opt_dict = master_dict['settings']
    for on, ov in opt_dict['values'].items():

        # the purpose of the following block is to see if the value is the same as the default and, if so, we
        # don't bother setting it and instead continue the for loop

        if on in opt_dict['units'].keys():
            # we get the actual unit and the default unit
            actual_unit = ov * UM.parse_units(opt_dict['units'][on])
            default_unit = DEFAULT_SETTINGS['units'][on]
            try:
                # on is a physical qty, so we can compare it with numpy
                if np.isclose(np.asarray((ov * actual_unit).to(default_unit).magnitude),
                              np.asarray(DEFAULT_SETTINGS['values'][on])
                              ).all():
                    mlog.debug('option {0}={1} was skipped'.format(on, (ov * actual_unit).to(default_unit)))
                    continue
                else:
                    pass
            except ValueError:  # happens with arrays of variable dimensions, e.g. voltage bases
                pass

        else:  # on is, therefore, a measureless qty, but may be of many types
            try:  # we try to see if it quacks like a string...
                if ov.lower() == DEFAULT_SETTINGS['values'][on].lower():
                    mlog.debug('option {0}={1} was skipped'.format(on, ov))
                    continue
            except AttributeError:  # if it doesn't, we perform a flexible numeric comparison with numpy
                try:
                    if np.isclose(np.asarray(ov),
                                  np.asarray(DEFAULT_SETTINGS['values'][on])
                                  ).all():
                        mlog.debug('option {0}={1} was skipped'.format(on, ov))
                        continue
                except ValueError as ve:  # happens with arrays of variable dimensions, e.g. voltage bases
                    pass

        # ... if we're here, no continue command was reached, so we have to actually set the option.
        if on in opt_dict['units'].keys():
            d_ov = ov * UM.parse_units(opt_dict['units'][on])
        else:
            d_ov = ov
        l_ckt.set(**{on: d_ov})
        mlog.debug('option {0}={1} was DECLARED'.format(on, d_ov))

    # reconstruction of dependency graph and declarations
    dep_graph = construct_deptree(master_dict['elements'])
    l_ckt = declare_deptree(l_ckt, dep_graph, master_dict['elements'], logger=mlog)

    l_ckt._coords_linked = master_dict['buscoords']
    l_ckt._declare_buscoords()
    mlog.debug('coordinates just declared, exiting')

    # patch for curing the stepsize bug; this is probably due to stepsize overwriting by other settings
    l_ckt.set(stepsize=master_dict['settings']['values']['stepsize'])
    # patch for curing the stepsize bug

    if final_snap:
        # this often prevents segfaults when tampering with a krang's elements after loading, but before solving
        l_ckt.snap()

    return l_ckt


def construct_deptree(element_dict: dict):
    dep_graph = _DepGraph()
    for jobj in element_dict.values():
        vname = jobj['type'].split('_')[0] + '.' + jobj['name']
        # if the element has no dependencies, we just add a node with iths name
        if jobj['depends'] == {} or all([d == '' for d in jobj['depends'].values()]):
            dep_graph.add_node(vname)
        else:
            # if an element parameter depends on another name, or a list of other names, we create all the edges
            # necessary
            types_dict = {d['name'].lower(): d['type'].lower() for d in element_dict.values()}
            for dvalue in jobj['depends'].values():
                if isinstance(dvalue, list):
                    for dv in dvalue:
                        if dv != '':
                            lower_name = dv.lower().split('.', 1)[-1]
                            dep_graph.add_edge(vname, types_dict[lower_name] + '.' + lower_name)
                else:
                    if dvalue != '':
                        lower_name = dvalue.lower().split('.', 1)[-1]
                        dep_graph.add_edge(vname, types_dict[lower_name] + '.' + lower_name)
    
    return dep_graph


def declare_deptree(krg: Krang, dep_tree: _DepGraph, element_dict: dict, logger=None):
    # we cyclically consider all "leaves", add the objects at the leaves, then trim the leaves and go on with
    # the new leaves.
    # In this way we are sure that, whenever a name is mentioned in a fcs, its entity was already declared.

    class __logger_mocker:
        def debug(self, *args, **kwargs):
            pass

    if logger is None:
        mlog = __logger_mocker()
    else:
        mlog = logger

    for trimmed_leaves in dep_tree.recursive_prune():
        for nm in trimmed_leaves:
            try:
                jobj = copy.deepcopy(element_dict[nm.lower()])
            except KeyError:
                mdmod = {k.split('.')[1]: v for k, v in element_dict.items()}
                try:
                    jobj = copy.deepcopy(mdmod[nm.lower()])
                except KeyError:
                    jobj = copy.deepcopy(mdmod[nm.split('.')[1].lower()])
            dssobj = co.dejsonize(jobj)
            if dssobj.isnamed():
                krg << dssobj
                mlog.debug('element {0} was added as named'.format(nm))
            elif dssobj.isabove():
                krg << dssobj.aka(jobj['name'])
                mlog.debug('element {0} was added as above'.format(nm))
            else:
                krg[tuple(jobj['topological'])] << dssobj.aka(jobj['name'])
                mlog.debug('element {0} was added as regular'.format(nm))
                # l_ckt.command(dssobj.aka(jobj['name']).fcs(buses=jobj['topological']))
        
    return krg


# external implementation of loading methods
def _open_ckt(path):
    """Loads a ckt package saved through Krang.pack_ckt() and returns a Krang."""
    with zipfile.ZipFile(path, mode='r') as zf:
        with zf.open(LSH_ZIP_NAME) as lsh_file:
            # the loadshapes csv are extracted in the temp_path, where they will be looked for by their
            # csvloadshapes, since in the json no explicit path will be specified
            lsh_data = io.BytesIO(lsh_file.read())
            zipfile.ZipFile(lsh_data).extractall(TMP_PATH)

        # as of 0.2.0, only one json, the main one, is to be found in the pack. we get it and load it.
        fls = [x for x in zf.namelist() if x.lower().endswith('.json')]
        assert len(fls) == 1
        jso = zf.open(fls[0])
        krg = _from_json(jso, redirect_path=True, final_snap=True)

        # If any AI are present, they are loaded from their pickle file and put inside _ai_list.
        if _FQ_DM_NAME in zf.namelist():
            with zf.open(_FQ_DM_NAME) as fq_file:
                krg._ai_list = pickle.load(fq_file)

        # If present, we load the md5 checksum that was packed with the zip file when it was created.
        # If not (for example, in manually edited packs), we jump
        if 'krang_hash.md5' in zf.namelist():
            with zf.open('krang_hash.md5', 'r') as md5_file:
                kranghash = md5_file.read().decode('utf-8')

            # We check that the hashes match.
            if krg.fingerprint() != kranghash:
                # If not, we throw an IOError with a nice diff display of the jsons differences.
                raw_dict = json.load(zf.open(fls[0]))
                err = diff_dicts(raw_dict,
                                 krg.make_json_dict())
                raise IOError('JSONs not corresponding - see below:\n\n' + err)

    return krg


def _from_dss(file_path, target_krang=None, frequency=BASE_FREQUENCY):
    """from_dss(file_path, target_krang, frequency) allows to create a krang from an existing dss script or to pass
    commands to a krang from an existing dss script. USE AT YOUR OWN RISK.

    :param file_path: The path of the dss file to utilize
    :param target_krang:

     - If None, a new krang will be created and initialized with the information from the file (must
       contain a 'new circuit' command).
     - If a Krang is passed, the commands in the script will be passed to that Krang.

    :param frequency: the general frequency to use for the krang, if a new one is created.
    """

    with open(file_path, 'r') as dss_file:
        dss_script_content = dss_file.read()

    if target_krang is None:
        # we extract the initialization parameters from here
        spawn = _CIRCUIT_INIT_RE.search(dss_script_content)
        extr_name = spawn.group(3)

        if spawn.group(4) is not None:
            extr_vsource_p0 = {k.lower(): v for k, v in [x.split('=') for x in spawn.group(4).split()]}
        else:
            extr_vsource_p0 = {}

        if spawn.group(9) is not None:
            extr_vsource_p1 = {k.lower(): v for k, v in [x.split('=') for x in _MORE_RE.sub('', spawn.group(9)).split()]}
        else:
            extr_vsource_p1 = {}

        extr_vsource_params = {**extr_vsource_p0, **extr_vsource_p1}

        if 'bus1' in extr_vsource_params.keys():
            extr_basebus_name = extr_vsource_params['bus1']
            del extr_vsource_params['bus1']
        else:
            extr_basebus_name = 'sourcebus'
        if 'bus2' in extr_vsource_params.keys():
            raise ValueError('Direct specification of the slack vsource bus2 is bad practice and is not allowed.'
                             'Please check the script.')

        target_krang = Krang(extr_name,
                             co.Vsource(**extr_vsource_params),
                             extr_basebus_name,
                             frequency)

        # cutting off the header
        refined_commands = _CLEAR_RE.sub('', dss_script_content)  # matches only the first clear
        refined_commands = _CIRCUIT_INIT_RE.sub('', refined_commands)

    else:
        refined_commands = dss_script_content

    base_dir = os.path.dirname(file_path)

    with _KrangCwdRedirector(target_krang, base_dir) as diverted_krang:
        for line in refined_commands.splitlines():
            diverted_krang.command(line)

    return target_krang


def _main():
    pass


if __name__ == '__main__':
    _main()
