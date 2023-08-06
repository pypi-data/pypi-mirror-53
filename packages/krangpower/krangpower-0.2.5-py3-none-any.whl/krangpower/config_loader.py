import configparser as cfp
import json
import logging
import os.path
import re
import platform

import pint

from .aux_fcn import load_dictionary_json

__all__ = ['UM', 'krang_directory', 'TMP_PATH']
_THISDIR = os.path.dirname(os.path.realpath(__file__))
_WIN_ENV_VAR_REGEX = re.compile('(%)([^%]+)(%)')
_LINUX_ENV_VAR_REGEX = re.compile('(\$)([^(/|\\)]+)')

# -------------------------------------------------------------
# CONFIG LOAD
# -------------------------------------------------------------
CONFIG = cfp.ConfigParser()
CONFIG.read(os.path.join(_THISDIR, 'config/krang_config.cfg'))

# -------------------------------------------------------------
# HELP LOAD
# -------------------------------------------------------------
DSSHELP = cfp.RawConfigParser()
DSSHELP.read(os.path.join(_THISDIR, 'defaults/DSSHelp.cfg'))


# -------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------
_INTERFACE_METHODS_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'interfaces'))
_UNIT_MEASUREMENT_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'measurement_units'))
_MANDATORY_UNITS_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'mandatory_units'))
_TREATMENTS_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'treatments'))
_INTERF_SELECTORS_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'interface_selectors'))
_DEFAULT_SETTINGS_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'default_settings'))
_DEFAULT_ENTITIES_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'default_entities'))
_ASSOCIATION_TYPES_PATH = os.path.join(_THISDIR, CONFIG.get('data_files', 'association_types'))

_GLOBAL_LOG_LEVEL = getattr(logging, CONFIG.get('misc_settings', 'default_logging_level'))
_ELK = CONFIG.get('misc_settings', 'graph_element_tag')
_DEFAULT_KRANG_NAME = CONFIG.get('misc_settings', 'default_krang_name')
_CMD_LOG_NEWLINE_LEN = CONFIG.getint('misc_settings', 'newline_cmdlog_length')
_DEFAULT_NAME = CONFIG.get('misc_settings', 'default_enhancer_name')
_GLOBAL_PRECISION = CONFIG.getint('precision', 'global_precision')
_LSH_ZIP_NAME = CONFIG.get('misc_settings', 'inner_loadshape_zip_filename')
_PBAR_ISASCII = CONFIG.getboolean('misc_settings', 'ascii_pbar')


# -------------------------------------------------------------
#  LOG PATH
# -------------------------------------------------------------
def replace_env(match):
    return os.getenv(match.group(2))


# general log
if platform.system() == 'Windows':

    basepath = CONFIG.get('log_file', 'win_log_folder')
    basepath = _WIN_ENV_VAR_REGEX.sub(replace_env, basepath)
    # basepath = re.sub('(%)([^%]+)(%)', replace_env, basepath)

    _MAIN_LOGPATH = os.path.join(basepath,
                                 CONFIG.get('log_file', 'general_log_name'))
elif platform.system() == 'Linux':

    basepath = CONFIG.get('log_file', 'linux_log_folder')
    basepath = _LINUX_ENV_VAR_REGEX.sub(replace_env, basepath)
    # basepath = re.sub('(\$)([^(/|\\)]+)', replace_env, basepath)

    _MAIN_LOGPATH = os.path.join(basepath,
                                 CONFIG.get('log_file', 'general_log_name'))
else:
    raise OSError('Could not find a valid log path.')

# command_log
if platform.system() == 'Windows':

    basepath = CONFIG.get('log_file', 'win_log_folder')
    basepath = _WIN_ENV_VAR_REGEX.sub(replace_env, basepath)
    # basepath = re.sub('(%)([^%]+)(%)', replace_env, basepath)

    _COMMAND_LOGPATH = os.path.join(basepath,
                                    CONFIG.get('log_file', 'commands_log_name'))
elif platform.system() == 'Linux':

    basepath = CONFIG.get('log_file', 'linux_log_folder')
    basepath = _LINUX_ENV_VAR_REGEX.sub(replace_env, basepath)
    # basepath = re.sub('(\$)([^/|\\]+)', replace_env, basepath)

    _COMMAND_LOGPATH = os.path.join(basepath,
                                    CONFIG.get('log_file', 'commands_log_name'))
else:
    raise OSError('Could not find a valid log path.')


# -------------------------------------------------------------
#  TEMPORARY FILES PATH
# -------------------------------------------------------------
if platform.system() == 'Windows':
    TMP_PATH = os.path.join(os.getenv('TEMP'), CONFIG.get('temp_files', 'temp_subfolder'))
elif platform.system() == 'Linux':
    TMP_PATH = os.path.join('/var/tmp', CONFIG.get('temp_files', 'temp_subfolder'))
else:
    raise OSError('Could not find a valid temp path.')

_COORDS_FILE_PATH = os.path.join(TMP_PATH, 'bus_coords_fromkml.csv')

# -------------------------------------------------------------
#  UNIT MEASURE REGISTRY
# -------------------------------------------------------------
UM = pint.UnitRegistry()
UM.define('percent = 0.01 * dimensionless = pct')
UM.define('none = [generic_length] = unitlength')  # when lengths are set as none, this creates a common basis
UM.define('mt = meter')
_PINT_QTY_TYPE = type(1 * UM.m)


# -------------------------------------------------------------
#  DICTIONARY OF MANDATORY UNITS
# -------------------------------------------------------------
with open(_MANDATORY_UNITS_PATH, 'r') as mf:
    _MANDATORY_UNITS = json.load(mf)

# -------------------------------------------------------------
#  DEFAULTS DICTIONARIES
# -------------------------------------------------------------
DEFAULT_COMP = load_dictionary_json(_DEFAULT_ENTITIES_PATH)
with open(_DEFAULT_SETTINGS_PATH, 'r') as f:
    DEFAULT_SETTINGS = json.load(f)

krang_directory = _THISDIR  # we expose our path, because you could want to find the test cases, etc
