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

from slugify import slugify

from confspirator import exceptions
from confspirator import constants
from confspirator import types


class BaseConfigField(object):

    """Base class for all configuration options.
    The only required parameter is the config's name. However, it is
    common to also supply a default and help string for all options.

    :param name: the config's name
    :param config_type: the option's type. Must be a callable object that
                        takes string and returns converted and validated value
    :param help: an explanation of how the option is used
    :param default: the default value of the option
    :param test_default: a default for when running in test mode
    :param sample_default: a default for sample config files
    :param unsafe_default: true if the default value must be overridden
    :param secret: true if the value should be obfuscated in log output
    :param required: true if a value must be supplied for this option
    :param deprecated_location: deprecated dot separated location.
                                e.g. 'service.group1.old_name'
                                Acts like an alias.
    :param deprecated_for_removal: indicates whether this opt is planned for
                                   removal in a future release
    :param deprecated_reason: indicates why this opt is planned for removal in
                              a future release. Silently ignored if
                              deprecated_for_removal is False
    :param deprecated_since: indicates which release this opt was deprecated
                             in. Accepts any string, though valid version
                             strings are encouraged. Silently ignored if
                             deprecated_for_removal is False
    :param advanced: a bool True/False value if this option has advanced usage
                             and is not normally used by the majority of users
    """

    def __init__(
        self,
        name,
        config_type=None,
        help_text=None,
        default=None,
        test_default=None,
        sample_default=None,
        unsafe_default=False,
        secret=False,
        required=False,
        required_for_tests=None,
        deprecated_location=None,
        deprecated_for_removal=False,
        deprecated_reason=None,
        deprecated_since=None,
        advanced=False,
        reformat_name=True,
    ):
        if reformat_name:
            name = slugify(name)
        # we still at the very least do some basic formatting
        name = name.replace("-", "_")
        if name.startswith("_"):
            raise ValueError("illegal name %s with prefix _" % (name,))
        self.name = name

        if config_type is None:
            config_type = types.String()

        if not callable(config_type):
            raise TypeError("type must be callable")
        self.type = config_type

        self.help_text = help_text
        self.default = default
        self.test_default = test_default
        self.sample_default = sample_default
        self.unsafe_default = unsafe_default
        self.secret = secret
        self.required = required
        if required_for_tests is None:
            self.required_for_tests = required
        else:
            self.required_for_tests = required_for_tests
        self.deprecated_location = deprecated_location
        self.deprecated_for_removal = deprecated_for_removal
        self.deprecated_reason = deprecated_reason
        self.deprecated_since = deprecated_since
        self.advanced = advanced

        self._group = None

    def set_parent(self, parent):
        self._group = parent

    def path(self, deprecated=False):
        if deprecated:
            return self.deprecated_location.split(".")
        return self._group.path() + [self.name]

    def path_str(self):
        return ".".join(self.path())

    def envvar_name(self, deprecated=False):
        """Make the expected envvar key

        This is in the style of 'GROUPNAME_SUBGROUPNAME_KEY'
        and is generated automatically based on the path into
        the conf.
        """
        return "_".join(self.path(deprecated)).upper()

    def __str__(self):
        if self._group:
            return self.path_str()
        else:
            return self.name

    def parse_value(self, value, test_mode):
        conf_name = ".".join(self.path())
        errors = []
        if value == constants.DEFAULT_NONE_VALUE:
            if self.unsafe_default and not test_mode:
                print(
                    "WARNING(%s): "
                    "This conf has an unsafe default you must override." % conf_name
                )

            if test_mode:
                if self.required and (self.default is None and self.test_default is None):
                    if self.required_for_tests:
                        errors.append("This conf is required.")
                if self.test_default is not None:
                    value = self.test_default
                else:
                    value = self.default
            else:
                if self.required and self.default is None:
                    errors.append("This conf is required.")
                value = self.default

        if self.deprecated_for_removal:
            print("WARNING(%s): " "This conf has been deprecated." % conf_name)

        if value is not None:
            try:
                return self.type(value)
            except ValueError as e:
                errors.append(str(e))

        if errors:
            raise exceptions.InvalidConfValue(errors)


class StrConfig(BaseConfigField):
    """Config with String type

    :param name: the config's name
    :param choices: Optional sequence of either valid values or tuples of valid
        values with descriptions.
    :param quotes: If True and string is enclosed with single or double
                   quotes, will strip those quotes.
    :param regex: Optional regular expression (string or compiled
                  regex) that the value must match on an unanchored
                  search.
    :param ignore_case: If True case differences (uppercase vs. lowercase)
                        between 'choices' or 'regex' will be ignored.
    :param max_length: If positive integer, the value must be less than or
                       equal to this parameter.
    """

    def __init__(
        self,
        name,
        choices=None,
        quotes=None,
        regex=None,
        ignore_case=False,
        max_length=None,
        **kwargs
    ):
        super(StrConfig, self).__init__(
            name,
            config_type=types.String(
                choices=choices,
                quotes=quotes,
                regex=regex,
                ignore_case=ignore_case,
                max_length=max_length,
            ),
            **kwargs
        )


class BoolConfig(BaseConfigField):
    """Boolean config

    :param name: the config's name
    """

    def __init__(self, name, **kwargs):
        super(BoolConfig, self).__init__(name, config_type=types.Boolean(), **kwargs)


class IntConfig(BaseConfigField):
    """Config with Integer type

    :param name: the config's name
    :param min: minimum value the integer can take
    :param max: maximum value the integer can take
    """

    def __init__(self, name, min=None, max=None, **kwargs):
        super(IntConfig, self).__init__(
            name, config_type=types.Integer(min, max), **kwargs
        )


class FloatConfig(BaseConfigField):
    """Config with Float type

    :param name: the config's name
    :param min: minimum value the float can take
    :param max: maximum value the float can take
    """

    def __init__(self, name, min=None, max=None, **kwargs):
        super(FloatConfig, self).__init__(
            name, config_type=types.Float(min, max), **kwargs
        )


class ListConfig(BaseConfigField):
    """Option with List(String) type

    :param name: the config's name
    :param item_type: type of items (see :class:`oslo_config.types`)
    """

    def __init__(self, name, item_type=None, **kwargs):
        super(ListConfig, self).__init__(
            name, config_type=types.List(item_type=item_type), **kwargs
        )


class DictConfig(BaseConfigField):
    """Config with Dict(String) type

    :param name: the config's name
    """

    def __init__(
        self, name, value_type=None, check_value_type=False, is_json=False, **kwargs
    ):
        super(DictConfig, self).__init__(
            name,
            config_type=types.Dict(
                value_type=value_type,
                check_value_type=check_value_type,
                is_json=is_json,
            ),
            **kwargs
        )


class IPConfig(BaseConfigField):
    """Config with IPAddress type

    :param name: the config's name
    :param version: one of either ``4``, ``6``, or ``None`` to specify
       either version.
    """

    def __init__(self, name, version=None, **kwargs):
        super(IPConfig, self).__init__(
            name, config_type=types.IPAddress(version), **kwargs
        )


class PortConfig(BaseConfigField):
    """Config for a TCP/IP port number.  Ports can range from 0 to 65535.

    :param name: the config's name
    :param min: minimum value the port can take
    :param max: maximum value the port can take
    :param choices: Optional sequence of either valid values or tuples of valid
        values with descriptions.
    """

    def __init__(self, name, min=None, max=None, choices=None, **kwargs):
        type = types.Port(min=min, max=max, choices=choices, type_name="port value")
        super(PortConfig, self).__init__(name, config_type=type, **kwargs)


class HostNameConfig(BaseConfigField):
    """Config for a hostname.  Only accepts valid hostnames.

    :param name: the config's name
    """

    def __init__(self, name, **kwargs):
        super(HostNameConfig, self).__init__(
            name, config_type=types.Hostname(), **kwargs
        )


class HostAddressConfig(BaseConfigField):
    """Option for either an IP or a hostname.

    Accepts valid hostnames and valid IP addresses.

    :param name: the config's name
    :param version: one of either ``4``, ``6``, or ``None`` to specify
       either version.
    """

    def __init__(self, name, version=None, **kwargs):
        super(HostAddressConfig, self).__init__(
            name, config_type=types.HostAddress(version), **kwargs
        )


class URIConfig(BaseConfigField):
    """Opt with URI type

    :param name: the config's name
    :param max_length: If positive integer, the value must be less than or
                       equal to this parameter.
    :param schemes: list of valid URI schemes, e.g. 'https', 'ftp', 'git'
    """

    def __init__(self, name, max_length=None, schemes=None, **kwargs):
        type = types.URI(max_length=max_length, schemes=schemes)
        super(URIConfig, self).__init__(name, config_type=type, **kwargs)
