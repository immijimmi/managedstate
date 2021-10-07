from .partialquery import PartialQuery


class PartialQueries:
    """
    Helper class that exposes some pre-made PartialQuery objects to slot into a .register call
    """

    KEY = PartialQuery(lambda key: key)  # Simply provides the deferred key as-is


class Keys:
    registered_path_label = "registered_path_label"
    custom_query_args = "custom_query_args"

    path_keys = "path_keys"
    defaults = "defaults"
