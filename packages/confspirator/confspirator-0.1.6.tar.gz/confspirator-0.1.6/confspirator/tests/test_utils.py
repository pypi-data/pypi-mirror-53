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

from unittest import TestCase

from confspirator import exceptions
from confspirator.tests import utils
from confspirator import groups


DEFAULT_CONF = groups.GroupNamespace(
    "test",
    values={
        "list_val": [1, 2, 3, 4],
        "dict_val": {"one": 1, "two": 2},
        "int_val": 5,
        "str_val": "stuff",
        "group_val": groups.GroupNamespace("group_val", values={"nested_val": 16}),
    },
)


@utils.modify_conf(
    DEFAULT_CONF, {"test.list_val": [{"operation": "append", "value": 5}]}
)
class ModifyConfClassTests(TestCase):
    """test that the class overriding works"""

    def test_list_val(self):
        self.assertTrue(5 in DEFAULT_CONF.list_val)


class ModifyConfFunctionTests(TestCase):
    """Test that function overriding works"""

    def test_list_val_1(self):
        self.assertFalse(5 in DEFAULT_CONF.list_val)

    @utils.modify_conf(
        DEFAULT_CONF, {"test.list_val": [{"operation": "append", "value": 5}]}
    )
    def test_list_val_2(self):
        self.assertTrue(5 in DEFAULT_CONF.list_val)

    def test_list_val_3(self):
        self.assertFalse(5 in DEFAULT_CONF.list_val)


class ModifyConfContextTests(TestCase):
    """test that 'with' context works

    And here we also test that each operation and conf type
    works since this is the easiest way to test it.
    """

    def test_int_val(self):
        self.assertEqual(DEFAULT_CONF.int_val, 5)
        with utils.modify_conf(
            DEFAULT_CONF, {"test.int_val": [{"operation": "override", "value": 6}]}
        ):
            self.assertEqual(DEFAULT_CONF.int_val, 6)
        self.assertEqual(DEFAULT_CONF.int_val, 5)

    def test_list_val_append(self):
        self.assertFalse(5 in DEFAULT_CONF.list_val)
        with utils.modify_conf(
            DEFAULT_CONF, {"test.list_val": [{"operation": "append", "value": 5}]}
        ):
            self.assertTrue(5 in DEFAULT_CONF.list_val)
            self.assertEqual(5, DEFAULT_CONF.list_val[-1])
        self.assertFalse(5 in DEFAULT_CONF.list_val)

    def test_list_val_prepend(self):
        self.assertFalse(5 in DEFAULT_CONF.list_val)
        with utils.modify_conf(
            DEFAULT_CONF, {"test.list_val": [{"operation": "prepend", "value": 5}]}
        ):
            self.assertTrue(5 in DEFAULT_CONF.list_val)
            self.assertEqual(5, DEFAULT_CONF.list_val[0])
        self.assertFalse(5 in DEFAULT_CONF.list_val)

    def test_list_val_remove(self):
        self.assertTrue(4 in DEFAULT_CONF.list_val)
        with utils.modify_conf(
            DEFAULT_CONF, {"test.list_val": [{"operation": "remove", "value": 4}]}
        ):
            self.assertFalse(4 in DEFAULT_CONF.list_val)
        self.assertTrue(4 in DEFAULT_CONF.list_val)

    def test_dict_val_update(self):
        self.assertFalse("three" in DEFAULT_CONF.dict_val)
        with utils.modify_conf(
            DEFAULT_CONF,
            {"test.dict_val": [{"operation": "update", "value": {"three": 3}}]},
        ):
            self.assertTrue("three" in DEFAULT_CONF.dict_val)
        self.assertFalse("three" in DEFAULT_CONF.dict_val)

    def test_dict_val_delete(self):
        self.assertTrue("two" in DEFAULT_CONF.dict_val)
        with utils.modify_conf(
            DEFAULT_CONF, {"test.dict_val": [{"operation": "delete", "value": "two"}]}
        ):
            self.assertFalse("two" in DEFAULT_CONF.dict_val)
        self.assertTrue("two" in DEFAULT_CONF.dict_val)

    def test_dict_val_overlay(self):
        self.assertFalse("three" in DEFAULT_CONF.dict_val)
        self.assertEqual(2, DEFAULT_CONF.dict_val["two"])
        with utils.modify_conf(
            DEFAULT_CONF,
            {
                "test.dict_val": [
                    {"operation": "overlay", "value": {"three": 3, "two": 5}}
                ]
            },
        ):
            self.assertTrue("three" in DEFAULT_CONF.dict_val)
            self.assertEqual(5, DEFAULT_CONF.dict_val["two"])
        self.assertFalse("three" in DEFAULT_CONF.dict_val)
        self.assertEqual(2, DEFAULT_CONF.dict_val["two"])

    def test_group_val_overlay(self):
        self.assertFalse("three" in DEFAULT_CONF.group_val)
        self.assertEqual(16, DEFAULT_CONF.group_val["nested_val"])
        with utils.modify_conf(
            DEFAULT_CONF,
            {
                "test.group_val": [
                    {"operation": "overlay", "value": {"three": 3, "nested_val": 5}}
                ]
            },
        ):
            self.assertTrue("three" in DEFAULT_CONF.group_val)
            self.assertEqual(5, DEFAULT_CONF.group_val["nested_val"])
        self.assertFalse("three" in DEFAULT_CONF.group_val)
        self.assertEqual(16, DEFAULT_CONF.group_val["nested_val"])

    def test_group_invalid_op(self):
        with self.assertRaises(exceptions.InvalidTestOperation):
            with utils.modify_conf(
                DEFAULT_CONF,
                {"test.group_val": [{"operation": "update", "value": {"three": 3}}]},
            ):
                pass
