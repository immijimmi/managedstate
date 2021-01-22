from objectextensions import Extendable

from .recursiveNode import RecursiveNode


class State(Extendable):
    def __init__(self, initial_state=None):
        self.__state = initial_state or {}

    def get(self, path_keys=(), defaults=()):
        return RecursiveNode(self.__state, path_keys, defaults).get()

    def set(self, value, path_keys=(), defaults=()):
        working_state = RecursiveNode(self.__state, path_keys, defaults)
        working_state.set(value)
        self.__state = working_state.value
