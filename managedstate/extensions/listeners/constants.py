class Keys:
    method_get = "get"
    method_set = "set"

    new_state = "new_state"


class ErrorMessages:
    @staticmethod
    def invalid_method(method):
        raise ValueError("Unable to add listeners to the specified method: {}".format(method))
