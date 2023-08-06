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
from collections import OrderedDict

from slugify import slugify

from confspirator import base
from confspirator import exceptions
from confspirator.fields import BaseConfigField
from confspirator import utils


class ConfigGroup(base.BaseConfigGroup):
    """Configuration group class

    Group which can onto it have registered fields or nested
    groups.

    :param name: the name of this group
    :param lazy_load: if true the group won't fully load until accessed
    :param children: children to register right away
    """

    def __init__(self, name, children=None, lazy_load=False, reformat_name=True):
        if reformat_name:
            name = slugify(name)
        # we still at the very least do some basic formatting
        name = name.replace("-", "_").replace(" ", "_")
        if name.startswith("_"):
            raise ValueError("illegal name %s with prefix _" % (name,))
        self.name = name
        self.lazy_load = lazy_load
        self._parent_group = None
        self._children = OrderedDict()
        if children:
            for child in children:
                self.register_child_config(child)

    def set_parent(self, parent):
        self._parent_group = parent

    def path(self):
        """Get the path down to this group"""
        path = []
        parent = self._parent_group
        while parent:
            path.append(parent.name)
            parent = parent._parent_group
        path.reverse()
        path.append(self.name)
        return path

    def register_child_config(self, child, override=False):
        """Register a child config

        :param child: a ConfigField or ConfigGroup instance
        :param override: replace if name already present
        """
        if not isinstance(child, (BaseConfigField, ConfigGroup)):
            raise exceptions.InvalidConfigClass(
                "'%s' is not a valid config class" % child
            )
        if not override and child.name in self._children:
            raise exceptions.ConfigGroupAlreadyRegistered(
                "'%s' is already registered in this group." % child
            )
        self._children[child.name] = child
        child.set_parent(self)

    def extend(self, children=None, remove_children=None):
        """Make a new group based on this group

        :param children: a list of configs to override or add
        :param remove_children: A list of names to remove
        """
        new_children = {}
        for name, child in self._children.items():
            if isinstance(child, ConfigGroup):
                new_children[name] = copy.deepcopy(child)
            else:
                new_children[name] = copy.copy(child)
        if remove_children:
            for name in remove_children:
                new_children.pop(name, None)

        new_group = ConfigGroup(
            self.name, children=new_children.values(), lazy_load=self.lazy_load
        )

        if children:
            for child in children:
                new_group.register_child_config(child, override=True)

        return new_group

    def copy(self):
        return copy.deepcopy(self)

    def __contains__(self, key):
        """Return True if key is the name of a registered config or group."""
        return key in self._children

    def __iter__(self):
        """Iterate over all registered config and groups."""
        for child in self._children.values():
            yield child

    def __str__(self):
        return self.name

    def __deepcopy__(self, memo):
        new_children = []
        for child in self._children.values():
            if isinstance(child, ConfigGroup):
                new_children.append(copy.deepcopy(child, memo=memo))
            else:
                new_children.append(copy.copy(child))

        new_group = ConfigGroup(
            self.name,
            lazy_load=self.lazy_load,
            children=new_children,
            reformat_name=False,
        )
        new_group.set_parent(self._parent_group)
        return new_group


class DynamicNameConfigGroup(ConfigGroup):
    """Configuration group class which must be named later

    Group which can onto it have registered fields or nested
    groups.

    :param lazy_load: if true the group won't fully load until accessed
    :param children: children to register right away
    """

    def __init__(self, children=None, lazy_load=False):
        self.lazy_load = lazy_load
        self._parent_group = None
        self._children = OrderedDict()
        if children:
            for child in children:
                self.register_child_config(child)

        self._name = None

    def set_name(self, name, reformat_name=True):
        if reformat_name:
            name = slugify(name)
        # we still at the very least do some basic formatting
        name = name.replace("-", "_").replace(" ", "_")
        if name.startswith("_"):
            raise ValueError("illegal name %s with prefix _" % (name,))
        self._name = name

    @property
    def name(self):
        if not self._name:
            raise exceptions.InvalidConfGroup("Must name the group before using it.")
        return self._name

    def extend(self, children=None, remove_children=None):
        new_children = {}
        for name, child in self._children.items():
            if isinstance(child, ConfigGroup):
                new_children[name] = copy.deepcopy(child)
            else:
                new_children[name] = copy.copy(child)
        if remove_children:
            for name in remove_children:
                new_children.pop(name, None)

        new_group = DynamicNameConfigGroup(
            children=new_children.values(), lazy_load=self.lazy_load
        )

        if children:
            for child in children:
                new_group.register_child_config(child, override=True)

        return new_group

    def __deepcopy__(self, memo):
        new_children = []
        for child in self._children.values():
            if isinstance(child, ConfigGroup):
                new_children.append(copy.deepcopy(child, memo=memo))
            else:
                new_children.append(copy.copy(child))

        new_group = DynamicNameConfigGroup(
            children=new_children,
            lazy_load=self.lazy_load,
        )
        new_group.set_parent(self._parent_group)
        try:
            new_group.set_name(self.name, reformat_name=False)
        except exceptions.InvalidConfGroup:
            pass
        return new_group


class GroupNamespace(base.BaseGroupNamespace):
    """A namespace in which to store parsed config data

    This is a parsed version of a config group.

    :param name: the name of the group
    :param values: a dict of the child values
    """

    def __init__(self, name, values):
        self.name = name
        self._parent = None

        new_values = {}
        for name, child in values.items():
            if isinstance(child, GroupNamespace):
                child.set_parent(self)
                new_values[child.name] = child
            else:
                new_values[name] = child
        self._values = new_values

    def set_parent(self, parent):
        self._parent = parent

    def path(self):
        path = []
        parent = self._parent
        while parent:
            path.append(parent.name)
            parent = parent._parent
        path.reverse()
        path.append(self.name)
        return path

    def overlay(self, overriding_group):
        """Merge a group or a dict to overlay the values in this one

        Returns a copy with the merged contents.

        :param overriding_group: the group or dict which to overlay
        """
        return utils.recursive_merge(self, overriding_group)

    def __getattr__(self, name):
        try:
            return self._values[name]
        except KeyError:
            path = self.path() + [name]
            raise exceptions.NoSuchConfig(".".join(path))

    def __getitem__(self, key):
        return self.__getattr__(key)

    def get(self, key):
        return self.__getattr__(key)

    def __contains__(self, key):
        return key in self._values

    def __str__(self):
        return "ConfigNameSpace: " + ".".join(self.path())

    def __deepcopy__(self, memo):
        new_values = {}
        for k, v in self._values.items():
            new_values[k] = copy.deepcopy(v, memo=memo)

        new_group = GroupNamespace(self.name, new_values)
        new_group.set_parent(self._parent)
        return new_group


class LazyLoadedGroupNamespace(GroupNamespace):
    """A lazy loaded groupnamespace

    This version will not process the group it is for until
    the group is accessed at least once. This allows for extra
    configs to be added to the group at runtime or app startup
    and for the conf for this group only to be parsed when that
    registration is well and truly finished.

    :param name: the name of the group
    :param group: the group which we want to lazy load later
    :param conf: the config dictionary we want to parse
    :param test_mode: are we running in test mode
    """

    def __init__(self, name, group, conf, test_mode):
        self.name = name
        self._group = group
        self._conf = conf
        self._test_mode = test_mode

        self._values = None
        self._parent = None

    def _lazy_load(self):
        if self._values is None:
            from confspirator import loader

            self._values = loader.process_group(
                self._group, self._conf, self._test_mode, lazy_loading=True
            )

            delattr(self, "_group")
            delattr(self, "_conf")
            delattr(self, "_test_mode")

            for child in self._values.values():
                if isinstance(child, GroupNamespace):
                    child.set_parent(self)

    def __getattr__(self, name):
        self._lazy_load()
        return super(LazyLoadedGroupNamespace, self).__getattr__(name)

    def __deepcopy__(self, memo):
        self._lazy_load()
        return super(LazyLoadedGroupNamespace, self).__deepcopy__(memo)
