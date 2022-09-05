class ErrorMessages:
    @staticmethod
    def invalid_method(method):
        raise ValueError("Unable to add listeners to the specified method: {}".format(method))
