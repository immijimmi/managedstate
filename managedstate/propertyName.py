class PropertyName:
    __hash__ = None  # Hash for this class will need custom implementation, not currently implemented

    def __init__(self, property_name):
        self.__name = property_name

    @property
    def name(self):
        return self.__name
