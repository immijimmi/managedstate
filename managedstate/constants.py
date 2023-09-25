class NO_DEFAULT:
    """
    Used to signify that a path key provided when accessing data from a State object
    does not have an associated default value,
    to ensure that an exception is raised if the path key is not valid.

    This allows for defaults to still be provided for path keys *after* the current one,
    since a value must be provided at the current index of the defaults list
    """

    __init__ = None
