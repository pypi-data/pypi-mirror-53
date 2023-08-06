# Copyright (C) 2019 Catalyst Cloud Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import copy
from functools import WRAPPER_ASSIGNMENTS, wraps
import six
from unittest import TestCase

from confspirator import exceptions
from confspirator import base
from confspirator import utils


# NOTE(adriant): needed until we drop py2
def _available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This is required as a workaround for http://bugs.python.org/issue3445
    under Python 2.
    """
    if six.PY3:
        return WRAPPER_ASSIGNMENTS
    else:
        return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))


class modify_conf(object):
    """A test decorator to allow modifying the conf for tests

    Operations avaiable:
        value:
            - override
        list:
            - override
            - preprend
            - append
            - remove
        dict:
            - override
            - update
            - delete
            - overlay
        GroupNamespace:
            - override
            - overlay

    example usage:

    @modify_conf(
        conf=CONF,
        operations={
            "test_app.api_settings.item_list_options": [
                {"operation": "remove", "value": "option1"},
            ],
    })
    class MyTestClass(TestCase):

    :param conf: The root GroupNamespace
    :param operations: a dict of dot seperate paths to lists of operations
    """

    enable_exception = None

    def __init__(self, conf, operations):
        self.conf = conf
        self.operations = operations

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def decorate_class(self, cls):
        if issubclass(cls, TestCase):
            decorated_setUp = cls.setUp
            decorated_tearDown = cls.tearDown

            def setUp(inner_self):
                self.enable()
                decorated_setUp(inner_self)

            def tearDown(inner_self):
                decorated_tearDown(inner_self)
                self.disable()

            cls.setUp = setUp
            cls.tearDown = tearDown
            return cls
        raise TypeError("Can only decorate subclasses of unittest.TestCase")

    def decorate_callable(self, func):
        @wraps(func, assigned=_available_attrs(func))
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def __call__(self, decorated):
        if isinstance(decorated, type):
            return self.decorate_class(decorated)
        elif callable(decorated):
            return self.decorate_callable(decorated)
        raise TypeError("Cannot decorate object of type %s" % type(decorated))

    def _get_nested_value(self, conf, path):
        if len(path) == 1:
            return conf[path[0]]
        elif path:
            return self._get_nested_value(conf[path[0]], path[1:])
        return conf

    def _do_operation(self, root_key, path, operation):
        keys = path.split(".")
        if keys[0] != root_key:
            raise exceptions.NoSuchConfig(path)

        end_key = keys[-1]
        if operation["operation"] == "override":
            if len(keys) == 1:
                raise exceptions.InvalidTestOperation("Cannot override root conf")
            holder = self._get_nested_value(self.conf, keys[1:-1])
            if not isinstance(holder, base.BaseGroupNamespace):
                raise exceptions.InvalidTestOperation(
                    "Overridden key must have a conf group as parent."
                )
            holder._values[end_key] = operation["value"]
        elif operation["operation"] in ["prepend", "append", "remove"]:
            list_val = self._get_nested_value(self.conf, keys[1:])
            if not isinstance(list_val, list):
                raise exceptions.InvalidTestOperation(
                    "'%s' is a list only operation" % operation["operation"]
                )
            if operation["operation"] == "prepend":
                list_val.insert(0, operation["value"])
            if operation["operation"] == "append":
                list_val.append(operation["value"])
            if operation["operation"] == "remove":
                list_val.remove(operation["value"])
        elif operation["operation"] in ["update", "delete"]:
            dict_val = self._get_nested_value(self.conf, keys[1:])
            if not isinstance(dict_val, dict):
                raise exceptions.InvalidTestOperation(
                    "'%s' is a dict only operation" % operation["operation"]
                )
            if operation["operation"] == "update":
                dict_val.update(operation["value"])
            if operation["operation"] == "delete":
                del dict_val[operation["value"]]
        elif operation["operation"] == "overlay":
            dict_like_val = self._get_nested_value(self.conf, keys[1:])
            if not isinstance(dict_like_val, (dict, base.BaseGroupNamespace)):
                raise exceptions.InvalidTestOperation(
                    "'%s' is a dict only operation" % operation["operation"]
                )
            holder = self._get_nested_value(self.conf, keys[1:-1])
            if isinstance(holder, base.BaseGroupNamespace):
                holder._values[end_key] = utils.recursive_merge(
                    dict_like_val, operation["value"]
                )
            else:
                holder[end_key] = utils.recursive_merge(
                    dict_like_val, operation["value"]
                )

    def enable(self):
        self.wrapped = copy.deepcopy(self.conf._values)

        root_key = self.conf.name

        for path, operations in self.operations.items():
            try:
                for operation in operations:
                    self._do_operation(root_key, path, operation)
            except Exception as exc:
                self.enable_exception = exc
                self.disable()

    def disable(self):
        self.conf._values = self.wrapped
        del self.wrapped
        if self.enable_exception is not None:
            exc = self.enable_exception
            self.enable_exception = None
            raise exc
