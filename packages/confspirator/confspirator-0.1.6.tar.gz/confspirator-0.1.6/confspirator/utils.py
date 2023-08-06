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

from confspirator import base


def recursive_merge(overridden, overrider):
    """Recursively merges a dict or a group over another group

    :param overridden: a dict or group to override
    :param overrider: a dict or group to override the other with

    If both overridden and overrider have a key who's value is a dict
    or group then recursive_merge is called on both values and the result
    stored in the returned dictionary.
    """
    if not isinstance(overrider, (base.BaseGroupNamespace, dict)):
        return overrider

    result = copy.deepcopy(overridden)
    if isinstance(overrider, base.BaseGroupNamespace):
        items = overrider._values.items()
    else:
        items = overrider.items()

    for k, v in items:
        if k in result and isinstance(result[k], (dict, base.BaseGroupNamespace)):
            result_value = recursive_merge(result[k], v)
        else:
            result_value = copy.deepcopy(v)

        if isinstance(result, base.BaseGroupNamespace):
            result._values[k] = result_value
        else:
            result[k] = result_value
    return result
