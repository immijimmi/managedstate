from objectextensions import Extension

from typing import Callable, Generator, Any

from ...state import State
from .constants import Keys, ErrorMessages


class Listeners(Extension):
    @staticmethod
    def can_extend(target_cls):
        return issubclass(target_cls, State)

    @staticmethod
    def extend(target_cls):
        Extension._wrap(target_cls, "__init__", Listeners._wrap_init)

        Extension._set(target_cls, "add_listener", Listeners._add_listener)
        Extension._set(target_cls, "remove_listener", Listeners._remove_listener)

        Extension._wrap(target_cls, Keys.method_get, Listeners._get_listeners_caller(Keys.method_get))
        Extension._wrap(target_cls, Keys.method_set, Listeners._get_listeners_caller(Keys.method_set))

    def _wrap_init(self, *args, **kwargs):
        yield
        Extension._set(self, "_listeners", {
            Keys.method_get: set(),
            Keys.method_set: set()
        })

    def _add_listener(self, method: str, listener: Callable[[dict], None]) -> None:
        """
        Adds the provided listener to a set of callbacks for the specified method.
        These callbacks will receive a dict containing copies of the method arguments and its return value
        """

        if method not in [Keys.method_get, Keys.method_set]:
            ErrorMessages.invalid_method(method)

        self._listeners[method].add(listener)

    def _remove_listener(self, method: str, listener: Callable[[dict], None]) -> None:
        """
        Removes the provided listener from the set of callbacks for the specified method.
        """

        if method not in [Keys.method_get, Keys.method_set]:
            ErrorMessages.invalid_method(method)

        if listener in self._listeners[method]:
            self._listeners[method].remove(listener)

    @staticmethod
    def _get_listeners_caller(method: str) -> Callable[[State, Any, Any], Generator[None, Any, None]]:
        """
        Used internally as a generic way to get listener handlers that can wrap each relevant method
        """

        def call_listeners(self, *args, **kwargs):
            result = yield

            for listener in self._listeners[method]:
                listener(self, *args, **kwargs)

        return call_listeners
