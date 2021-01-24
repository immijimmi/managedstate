from objectextensions import Extension

from typing import Sequence, List, Any

from ...state import State
from .constants import Keys
from .dynamickeyquery import DynamicKeyQuery


class Registrar(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, State)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Registrar._wrap_init)

        Extension._set(target_cls, "register", Registrar._register)
        Extension._set(target_cls, "registered_get", Registrar._registered_get)
        Extension._set(target_cls, "registered_set", Registrar._registered_set)

    def _wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_paths", {})

    def _register(self, registered_path_label: str, path_keys: Sequence[Any], defaults: Sequence[Any] = ()) -> None:
        """
        Saves the provided path keys and defaults under the provided label, so that a custom get or set can be
        carried out at later times simply by providing the label again in a call to registered_get() or registered_set()
        """

        registered_path = {Keys.path_keys: path_keys, Keys.defaults: defaults}
        self._paths[registered_path_label] = registered_path

    def _registered_get(self, registered_path_label: str, custom_query_args: Sequence[Any] = ()) -> Any:
        """
        Calls get(), passing in the path keys and defaults previously provided in register().
        If any of these path keys are instances of DynamicPathKey, each will be called and passed one value from
        the custom query args list and is expected to return a valid path key
        """

        registered_path = self._paths[registered_path_label]
        path_keys = Registrar._process_registered_path_keys(
            registered_path[Keys.path_keys], custom_query_args
        )
        defaults = registered_path[Keys.defaults]

        self._extension_data[Keys.registered_path_label] = registered_path_label
        self._extension_data[Keys.custom_query_args] = custom_query_args

        result = self.get(path_keys, defaults)

        del self._extension_data[Keys.registered_path_label]
        del self._extension_data[Keys.custom_query_args]

        return result

    def _registered_set(self, value: Any, registered_path_label: str, custom_query_args: Sequence[Any] = ()) -> None:
        """
        Calls set(), passing in the path keys and defaults previously provided in register().
        If any of these path keys are instances of DynamicPathKey, each will be called and passed one value from
        the custom query args list and is expected to return a valid path key
        """

        registered_path = self._paths[registered_path_label]
        path_keys = Registrar._process_registered_path_keys(
            registered_path[Keys.path_keys], custom_query_args
        )
        defaults = registered_path[Keys.defaults]

        self._extension_data[Keys.registered_path_label] = registered_path_label
        self._extension_data[Keys.custom_query_args] = custom_query_args

        result = self.set(value, path_keys, defaults)

        del self._extension_data[Keys.registered_path_label]
        del self._extension_data[Keys.custom_query_args]

    @staticmethod
    def _process_registered_path_keys(path_keys: Sequence[Any], custom_query_args: Sequence[Any]) -> List[Any]:
        """
        Used internally to coalesce instances of DynamicKeyQuery before path keys are passed to set()/get()
        """

        working_args = list(custom_query_args)
        result = []

        for path_node in path_keys:
            if type(path_node) is DynamicKeyQuery:
                result.append(path_node(working_args.pop(0)))
            else:
                result.append(path_node)

        return result
