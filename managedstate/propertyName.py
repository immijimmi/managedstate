class PropertyName:
    __hash__ = None
    """
    As this class is used indirectly to determine the method of access for the state object,
    it will never be used as a direct index. Thus, it should never be set as a key.
    """

    def __init__(self, property_name: str):
        self.__name = property_name

    @property
    def name(self) -> str:
        return self.__name
