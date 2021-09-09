class OpenShiftCLILibraryException(Exception):
    ROBOT_CONTINUE_ON_FAILURE = True


class ResourceNotFound(OpenShiftCLILibraryException):
    pass


class ResourceOperationFailed(OpenShiftCLILibraryException):
    pass
