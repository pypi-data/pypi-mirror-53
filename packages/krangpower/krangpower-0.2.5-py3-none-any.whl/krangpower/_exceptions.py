# ,---------------------------------------------------------------------------,
# |  This module is part of the krangpower electrical distribution simulation |
# |  suit by Federico Rosato <federico.rosato@supsi.ch> et al.                |
# |  Please refer to the license file published together with this code.      |
# |  All rights not explicitly granted by the license are reserved.           |
# '---------------------------------------------------------------------------'


class AssociationError(Exception):
    def __init__(self, 
                 association_target_type, 
                 association_target_name, 
                 association_subject_type,
                 association_subject_name, 
                 msg=None):
        if msg is None:
            msg = 'krangpower does not know how to associate a {0}({1}) to a {2}({3})'\
                .format(association_target_type,
                        association_target_name,
                        association_subject_type,
                        association_subject_name)
            
        super().__init__(msg)
        self.association_target_type = association_target_type
        self.association_subject_type = association_subject_type
        self.association_target_name = association_target_name
        self.association_subject_name = association_subject_name


class TypeRecoveryError(Exception):
    pass


class TypeUnrecoverableError(TypeRecoveryError):
    def __init__(self, original_type, msg=None):
        if msg is None:
            msg = 'krangpower has no options to recover a type {}'.format(str(original_type))
        super().__init__(msg)
        self.unrecoverable_type =original_type


class RecoveryTargetError(TypeRecoveryError):
    def __init__(self, original_type, target_type, msg=None):
        if msg is None:
            msg = 'krangpower does not know how to convert type {}---->{}'\
                .format(str(original_type), str(target_type))
        super().__init__(msg)
        self.original_type = original_type
        self.invalid_target_type = target_type


class KrangInstancingError(Exception):
    def __init__(self, already_existing_krang_name, msg=None):

        if msg is None:
            msg = 'Cannot create a new Krang - A Krang ({0}) already exists.'\
                  'Delete every reference to it if you want to instantiate another.'\
                .format(already_existing_krang_name)
        super().__init__(msg)


class KrangObjAdditionError(Exception):
    def __init__(self, object, msg=None):
        if msg is None:
            msg = 'There was a problem in adding object {} to Krang'.format(str(object))
        super().__init__(msg)


class ClearingAttemptError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'A "clear" command was passed to the text command interface.' \
                  'If you wish a new circuit, delete the existing Krang.'
        super().__init__(msg)


class UnsolvedCircuitError(Exception):
    def __init__(self, property_stack: str, msg=None):
        if msg is None:
            msg = 'An attempt to access the calculated property {} was made before solving the circuit.'\
                .format(property_stack)
        super().__init__(msg)
