class NoConfig(Exception):
    """Raisen when config file is not found"""
    pass

class NoImplementation(Exception):
    """Raisen when some funtionality has not been implemented yet."""

class BadConfig(Exception):
    """Raisen when config file is not found or has wrong fields"""
    pass