# -*- coding: utf-8 -*-
"""Decorator utils for project classes"""


def extend_class_option_spec(original_class, name, expected_type):
    if original_class is None:
        raise NotImplementedError("Cant set option_spec[%s] into None" % name)
    _spec = getattr(original_class, 'option_spec', {})
    _spec = isinstance(_spec, dict) and _spec or {}
    _spec[name] = expected_type
    setattr(original_class, 'option_spec', _spec)


def use_option(option_name: str, option_spec: type) -> callable:
    """Decorate class with option spec parameters

    Inserts option <option_name> with expected class
    into directive class definition. Defines option_spec class attribute if
    not defined in original class.

    :param option_name: directive option name
    :type option_name: str
    :param option_spec: directive option type, like six.text_type or int
    :type option_spec: type

    :returns: class decorator
    :rtype: callable
    """

    def use_option_internal(original_class):
        """Actual class decorator
        :param original_class: class to decorate
        :type original_class: type

        :return: Decorated class
        :rtype: type
        """
        return extend_class_option_spec(
            original_class, option_name, option_spec
        )

    return use_option_internal


def use_filter(filter_class: type) -> callable:
    """Decorate class with filter_class

        Inserts filter <filter_class> into filters class definition.

        :param filter_class: filter class
        :type filter_class: CommitsFilter

        :returns: class decorator
        :rtype: callable
        """

    def use_option_internal(original_class):
        """Actual class decorator
        :param original_class: class to decorate
        :type original_class: type

        :return: Decorated class
        :rtype: type
        """
        _filters = getattr(original_class, 'filters', [])
        _filters = isinstance(_filters, list) and _filters or []
        _filters.append(filter_class)
        original_class.filters = _filters
        filter_options = getattr(filter_class, 'option_spec', {})
        [
            extend_class_option_spec(original_class, k, v)
            for k, v in filter_options.items()
        ]

        return original_class

    return use_option_internal


def use_context_extender(filter_class: type) -> callable:
    """Extend class with context_extender

        Inserts filter <filter_class> into context_processors class definition.

        :param filter_class: filter class
        :type filter_class: CommitsFilter

        :returns: class decorator
        :rtype: callable
        """

    def use_option_internal(original_class):
        """Actual class decorator
        :param original_class: class to decorate
        :type original_class: type

        :return: Decorated class
        :rtype: type
        """
        _filters = getattr(original_class, 'context_processors', [])
        _filters = isinstance(_filters, list) and _filters or []
        _filters.append(filter_class)
        original_class.filters = _filters
        filter_options = getattr(filter_class, 'option_spec', {})

        [
            extend_class_option_spec(original_class, k, v)
            for k, v in filter_options.items()
        ]

        return original_class

    return use_option_internal
