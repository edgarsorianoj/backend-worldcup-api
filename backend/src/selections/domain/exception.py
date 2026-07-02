class DomainError(Exception):
    pass

class SelectionNotFound(DomainError):
    pass

class SelectionFlagNotValid(DomainError):
    pass