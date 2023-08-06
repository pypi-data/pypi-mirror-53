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

import os

from confspirator import constants
from confspirator import exceptions
from confspirator import base
from confspirator import groups


def _get_nested_value(conf, path):
    """Simple recursive function to get a value down a path in a dict"""
    if conf is None:
        raise KeyError("No value in config dict.")
    if len(path) == 1:
        return conf[path[0]]
    else:
        return _get_nested_value(conf[path[0]], path[1:])


def _get_value(conf, field):
    """Get the given config field value from the conf dict

    Will attempt to get the key at the given path, or fallback
    to a deprecated path if specified.
    """
    path = field.path()
    try:
        return _get_nested_value(conf, path)
    except KeyError:
        envvar_name = field.envvar_name()
        result = os.environ.get(envvar_name, constants.DEFAULT_NONE_VALUE)

    if result == constants.DEFAULT_NONE_VALUE and field.deprecated_location:
        path = field.path(deprecated=True)
        try:
            return _get_nested_value(conf, path)
        except KeyError:
            envvar_name = field.envvar_name(deprecated=True)
            result = os.environ.get(envvar_name, constants.DEFAULT_NONE_VALUE)
    return result


def process_group(group, conf, test_mode, lazy_loading=False):
    """Process a given ConfigGroup against the conf dict into a GroupNamespace"""
    if not isinstance(group, base.BaseConfigGroup):
        raise exceptions.InvalidConfGroup("'%s' is not a valid ConfigGroup." % group)

    if group.lazy_load and not lazy_loading:
        return groups.LazyLoadedGroupNamespace(group.name, group, conf, test_mode)

    parsed_children = {}
    errors = {}
    for child in group:
        if isinstance(child, base.BaseConfigGroup):
            parsed_children[child.name] = process_group(child, conf, test_mode)
            continue

        conf_val = _get_value(conf, child)
        try:
            parsed_val = child.parse_value(conf_val, test_mode)
            parsed_children[child.name] = parsed_val
        except exceptions.InvalidConfValue as e:
            errors[child.path_str()] = e.errors

    if errors:
        raise exceptions.InvalidConfGroup(errors)

    if lazy_loading:
        return parsed_children
    return groups.GroupNamespace(group.name, parsed_children)


def load_config(config_groups, conf_dict, root_group_name="conf", test_mode=False):
    """Load the config groups

    :param config_groups: A single config group or a list of groups.
    :param conf_dict: The loaded dictionary of config values
    :param root_group_name: If config_groups is a list, the namespace of the
                            root wrapper group.
    :param test_mode: If test are running. Will ignore deprecation warnings
                      and ignore fields with 'required_for_tests=False'.
    """
    if not isinstance(config_groups, (list, tuple)):
        config_groups = [config_groups]

    parsed_groups = {}
    errors = {}
    for group in config_groups:
        try:
            parsed_groups[group.name] = process_group(group, conf_dict, test_mode)
        except exceptions.InvalidConfGroup as e:
            errors[group.name] = e.errors

    if errors:
        raise exceptions.InvalidConf(errors)

    if len(parsed_groups) != 1:
        return groups.GroupNamespace(root_group_name, values=parsed_groups)
    return list(parsed_groups.values())[0]
