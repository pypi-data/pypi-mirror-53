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

import unittest
from mock import patch


import confspirator
from confspirator import exceptions
from confspirator import groups
from confspirator import fields
from confspirator import types


class ConfigTests(unittest.TestCase):
    def test_config_register_same(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.StrConfig("some_value"))
        with self.assertRaises(exceptions.ConfigGroupAlreadyRegistered):
            config_group.register_child_config(fields.StrConfig("some_value"))

    def test_str_config_field_getters(self):
        default_val = "This is a default"
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig("some_value", default=default_val)
        )

        config = confspirator.load(config_group, {})
        self.assertEqual(config.get("some_value"), default_val)
        self.assertEqual(config["some_value"], default_val)
        self.assertEqual(config.some_value, default_val)

    def test_str_config_field_no_conf(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.StrConfig("some_value"))

        config = confspirator.load(config_group, {})
        with self.assertRaises(exceptions.NoSuchConfig):
            config.get("no_value")

    def test_str_config_field_with_default(self):
        default_val = "This is a default"

        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig("some_value", required=True, default=default_val)
        )

        config = confspirator.load(config_group, {})
        self.assertEqual(config.some_value, default_val)

    def test_str_config_field_with_required(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, {})

    def test_str_config_field_no_default_not_required(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.StrConfig("some_value"))

        config = confspirator.load(config_group, {})
        self.assertEqual(config.some_value, None)

    def test_str_config_field_with_required_for_tests(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig("some_value", required=True, required_for_tests=False)
        )

        confspirator.load(config_group, {}, test_mode=True)

    def test_str_config_field_with_default_for_tests(self):
        config_group = groups.ConfigGroup("test")
        default_val = "other value"
        test_val = "some value"
        config_group.register_child_config(
            fields.StrConfig("some_value", default=default_val, test_default=test_val)
        )

        config = confspirator.load(config_group, {}, test_mode=True)
        self.assertEqual(config.some_value, test_val)
        config = confspirator.load(config_group, {})
        self.assertEqual(config.some_value, default_val)

    def test_str_config_nested(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        conf_dict = {"test": {"test2": {"test3": {"some_value": val}}}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.test3.some_value, val)

    def test_str_config_envvar(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group2.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        with patch.dict("os.environ", {"TEST_TEST2_SOME_VALUE": val}):
            config = confspirator.load(config_group, {})
        self.assertEqual(config.test2.some_value, val)

    def test_str_config_deprecated_location(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group2.register_child_config(
            fields.StrConfig(
                "some_value",
                required=True,
                deprecated_location="test.test2.test3.old_value",
            )
        )

        val = "This is a value"
        conf_dict = {"test": {"test2": {"test3": {"old_value": val}}}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.some_value, val)

    def test_bool_config_field_with_no_default_not_required(self):
        """no default, and not required will return a None"""
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.BoolConfig("some_value"))

        config = confspirator.load(config_group, {})
        self.assertEqual(config.some_value, None)

    def test_config_group_lazy_load(self):
        config_group = groups.ConfigGroup("test", lazy_load=True)
        config_group.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config._values, None)
        self.assertEqual(config._conf, conf_dict)
        self.assertEqual(config.some_value, val)
        self.assertEqual(config._values, {"some_value": val})

    def test_config_overlay_basic(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        conf_dict = {"test": {"test2": {"test3": {"some_value": val}}}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.test3.some_value, val)

        val = "This is another value"
        conf_dict = {"test2": {"test3": {"some_value": val}}}
        new_conf = config.overlay(conf_dict)
        self.assertEqual(new_conf.test2.test3.some_value, val)

    def test_config_overlay_group(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group2.register_child_config(fields.StrConfig("a_value", required=True))
        config_group.register_child_config(config_group2)
        config_group25 = groups.ConfigGroup("test25")
        config_group.register_child_config(config_group25)
        config_group25.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        val2 = "This is another value"
        conf_dict = {
            "test": {"test2": {"a_value": val}, "test25": {"some_value": val2}}
        }
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.a_value, val)
        self.assertEqual(config.test25.some_value, val2)

        new_conf = config.test2.overlay(config.test25)
        self.assertEqual(new_conf.some_value, val2)

    def test_config_overlay_complex(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group35 = groups.ConfigGroup("test35")
        config_group2.register_child_config(config_group3)
        config_group2.register_child_config(config_group35)
        config_group3.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        config_group35.register_child_config(
            fields.DictConfig("some_dict", required=True)
        )

        val = "This is a value"
        val2 = "This is a value2"
        conf_dict = {
            "test": {
                "test2": {
                    "test3": {"some_value": val},
                    "test35": {"some_dict": {"some_inner_val": val2}},
                }
            }
        }
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.test3.some_value, val)
        self.assertEqual(config.test2.test35.some_dict["some_inner_val"], val2)

        val = "This is another value"
        val2 = "This is another value2"
        conf_dict = {
            "test2": {
                "test3": {"some_value": val},
                "test35": {"some_dict": {"some_inner_val": val2}},
            }
        }
        new_conf = config.overlay(conf_dict)
        self.assertEqual(new_conf.test2.test3.some_value, val)
        self.assertEqual(new_conf.test2.test35.some_dict["some_inner_val"], val2)

    def test_config_overlay_override_with_none(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        val = "This is a value"
        conf_dict = {"test": {"test2": {"test3": {"some_value": val}}}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.test3.some_value, val)

        val = "This is another value"
        conf_dict = {"test2": {"test3": None}}
        new_conf = config.overlay(conf_dict)
        self.assertEqual(new_conf.test2.test3, None)

    def test_config_group_extend(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group2.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        config_group3 = groups.ConfigGroup("test3")
        config_group2.register_child_config(config_group3)
        config_group3.register_child_config(
            fields.StrConfig("some_deeper_value", required=True)
        )
        extended_group2 = config_group2.extend(
            children=[fields.StrConfig("some_other_value", required=True)]
        )
        config_group.register_child_config(extended_group2)

        val = "This is a value"
        conf_dict = {"test": {"test2": {"some_value": val}}}
        with self.assertRaises(exceptions.InvalidConf):
            config = confspirator.load(config_group, conf_dict)

        val2 = "This is also a value"
        val3 = "This is also a value"
        conf_dict = {
            "test": {
                "test2": {
                    "some_value": val,
                    "some_other_value": val2,
                    "test3": {"some_deeper_value": val3},
                }
            }
        }
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.some_value, val)
        self.assertEqual(config.test2.some_other_value, val2)
        self.assertEqual(config.test2.test3.some_deeper_value, val2)

    def test_config_group_extend_dynamic(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.DynamicNameConfigGroup()
        config_group2.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        config_group25 = config_group2.extend(
            children=[fields.StrConfig("some_other_value", required=True)],
            remove_children=["some_value"],
        )
        config_group2.set_name("test2")
        config_group25.set_name("test25")
        config_group.register_child_config(config_group2)
        config_group.register_child_config(config_group25)

        val = "This is a value"
        conf_dict = {"test": {"test2": {"some_value": val}}}
        with self.assertRaises(exceptions.InvalidConf):
            config = confspirator.load(config_group, conf_dict)

        val2 = "This is also a value"
        conf_dict = {
            "test": {"test2": {"some_value": val}, "test25": {"some_other_value": val2}}
        }
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.some_value, val)
        self.assertEqual(config.test25.some_other_value, val2)

    def test_config_group_deep_copy(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.ConfigGroup("test2")
        config_group.register_child_config(config_group2)
        config_group2.register_child_config(
            fields.StrConfig("some_value", required=True)
        )

        new_group = config_group.copy()
        new_group._children["test2"].register_child_config(
            fields.StrConfig("some_other_value", required=True)
        )

        val = "This is a value"
        conf_dict = {"test": {"test2": {"some_value": val}}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.some_value, val)

        with self.assertRaises(exceptions.InvalidConf):
            config = confspirator.load(new_group, conf_dict)

        val2 = "This is also a value"
        conf_dict = {"test": {"test2": {"some_value": val, "some_other_value": val2}}}
        config = confspirator.load(new_group, conf_dict)
        self.assertEqual(config.test2.some_other_value, val2)

    def test_config_group_deep_copy_and_rename(self):
        config_group = groups.ConfigGroup("test")
        config_group2 = groups.DynamicNameConfigGroup()
        config_group2.register_child_config(
            fields.StrConfig("some_value", required=True)
        )
        config_group25 = config_group2.copy()
        config_group2.set_name("test2")
        config_group25.set_name("test25")
        config_group.register_child_config(config_group2)
        config_group.register_child_config(config_group25)

        val = "This is a value"
        conf_dict = {"test": {"test2": {"some_value": val}}}
        with self.assertRaises(exceptions.InvalidConf):
            config = confspirator.load(config_group, conf_dict)

        val2 = "This is also a value"
        conf_dict = {
            "test": {"test2": {"some_value": val}, "test25": {"some_value": val2}}
        }
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.test2.some_value, val)
        self.assertEqual(config.test25.some_value, val2)


class ConfigTypeTests(unittest.TestCase):
    def test_str_config_with_length(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.StrConfig("some_value", max_length=6))

        val = "1234567"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "123456"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_str_config_with_regex(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig(
                "some_value", regex=r"#?([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})"
            )
        )

        val = "not_hex"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "#F0F0F0"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_str_config_with_choices(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.StrConfig("some_value", choices=["opt1", "opt2"])
        )

        val = "opt3"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "opt2"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_bool_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.BoolConfig("some_value"))

        val = "nada"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = False
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = True
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "false"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, False)
        val = "true"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, True)

    def test_int_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.IntConfig("some_value"))

        val = "nada"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "5"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, int(val))
        val = 5
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_int_config_min_max(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.IntConfig("some_value", min=5, max=10)
        )

        val = 4
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = 11
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = 6
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_float_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.FloatConfig("some_value"))

        val = "nada"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "5.2"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, float(val))
        val = 5.5
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_list_config_from_list(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.ListConfig("some_list", required=True)
        )

        val = ["this", "is", "a", "comma", "separated", "list"]
        conf_dict = {"test": {"some_list": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_list, val)

    def test_list_config_from_str(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.ListConfig("some_list", required=True)
        )

        val = "this,is,a,comma,separated,list"
        conf_dict = {"test": {"some_list": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(
            config.some_list, ["this", "is", "a", "comma", "separated", "list"]
        )

    def test_dict_config_from_dict(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.DictConfig("some_dict", required=True)
        )

        val = {"dict": "config"}
        conf_dict = {"test": {"some_dict": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_dict, val)

    def test_dict_config_from_str(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.DictConfig("some_dict", required=True)
        )

        val = "dict:config,dict2:config2"
        conf_dict = {"test": {"some_dict": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_dict, {"dict": "config", "dict2": "config2"})

    def test_dict_config_from_str_as_json(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.DictConfig("some_dict", required=True, is_json=True)
        )

        val = '{"dict": "config", "dict2": "config2"}'
        conf_dict = {"test": {"some_dict": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_dict, {"dict": "config", "dict2": "config2"})

    def test_dict_config_from_dict_nested(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.DictConfig(
                "some_dict",
                required=True,
                value_type=types.Dict(),
                check_value_type=True,
            )
        )

        val = {"dict": "config"}
        conf_dict = {"test": {"some_dict": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = {"dict": {"thing": "config"}}
        conf_dict = {"test": {"some_dict": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_dict, val)

    def test_dict_config_from_json_nested(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.DictConfig(
                "some_dict",
                required=True,
                value_type=types.Dict(),
                check_value_type=True,
                is_json=True,
            )
        )

        val = '{"dict": "config"}'
        conf_dict = {"test": {"some_dict": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = '{"dict": {"thing": "config"}}'
        conf_dict = {"test": {"some_dict": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_dict, {"dict": {"thing": "config"}})

    def test_ip_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.IPConfig("some_value"))

        val = "not_an_ip"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "0.0.0.0"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "2001:db8::8a2e:370:7334"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "2001:0db8:0000:0000:0000:8a2e:0370:7334"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_ip_config_version(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.IPConfig("some_value", version=4))

        val = "2001:db8::8a2e:370:7334"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "0.0.0.0"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.IPConfig("some_value", version=6))
        val = "0.0.0.0"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "2001:db8::8a2e:370:7334"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_port_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.PortConfig("some_value"))

        val = "9999999"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "8888"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, int(val))
        val = 8888
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_hostname_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.HostNameConfig("some_value"))

        val = "this#is.not_a_valid*hostname"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_hostaddress_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.HostAddressConfig("some_value"))

        val = "this#is.not_a_valid*hostname"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "0.0.0.0"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_uri_config(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(fields.URIConfig("some_value"))

        val = "this#is.not_a_valid*hostname"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "https://this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "ftp://this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)

    def test_uri_config_scheme(self):
        config_group = groups.ConfigGroup("test")
        config_group.register_child_config(
            fields.URIConfig("some_value", schemes=["https", "http"])
        )

        val = "ftp://this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        with self.assertRaises(exceptions.InvalidConf):
            confspirator.load(config_group, conf_dict)
        val = "https://this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
        val = "http://this.is.a.valid.hostname"
        conf_dict = {"test": {"some_value": val}}
        config = confspirator.load(config_group, conf_dict)
        self.assertEqual(config.some_value, val)
