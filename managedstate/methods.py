from typing import Any
from copy import deepcopy


class Methods:
    @staticmethod
    def try_copy(item: Any) -> Any:
        """
        A failsafe deepcopy wrapper
        """

        try:
            return deepcopy(item)
        except:
            return item


class ErrorMessages:
    @staticmethod
    def no_default(path_index):
        raise ValueError("No value found and no default provided for the path key at index {0}".format(path_index))
