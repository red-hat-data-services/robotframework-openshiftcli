class openshiftcliLibraryException(Exception):
    ROBOT_CONTINUE_ON_FAILURE = True


class ResourceNotFound(openshiftcliLibraryException):
    pass


class ResourceOperationFailed(openshiftcliLibraryException):
    pass
