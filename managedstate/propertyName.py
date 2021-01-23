class PropertyName:
    __hash__ = None  # Hash for this class will need custom implementation, not currently implemented

    def __init__(self, property_name: str):
        self.__name = property_name

    @property
    def name(self) -> str:
        return self.__name
