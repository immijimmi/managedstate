class AttributeName:
    """
    An instance of this class should be provided as a path key when getting or setting the state,
    to indicate that the next nesting level of the state should be accessed via an object attribute
    """

    # As this class is used indirectly to determine the method of access into the state,
    # it should never be stored directly as a key within that state
    __hash__ = None

    def __init__(self, attribute_name: str):
        self.__name = attribute_name

    @property
    def name(self) -> str:
        return self.__name
