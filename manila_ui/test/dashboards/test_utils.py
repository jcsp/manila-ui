# Copyright (c) 2015 Mirantis, Inc.
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ddt
from django.forms import ValidationError  # noqa

from manila_ui.dashboards import utils
from manila_ui.test import helpers as base


@ddt.ddt
class ManilaDashboardsUtilsTests(base.TestCase):

    @ddt.data(
        ("", {}, []),
        ("  ", {}, []),
        ("\n", {}, []),
        ("f", {}, ["f"]),
        ("f=b", {"f": "b"}, []),
        ("foo=bar", {"foo": "bar"}, []),
        ("\nfoo \n", {}, ["foo"]),
        ("'foo'=\"bar\"\n'bar'", {"foo": "bar"}, ["bar"]),
        ("   foo=   bar ", {"foo": "bar"}, []),
        ("foo= \"<is> bar\"\n", {"foo": "<is> bar"}, []),
        ("\n\nset_me_key = 'value with spaces and equality 2=2'\nunset_key  ",
         {"set_me_key": "value with spaces and equality 2=2"},
         ["unset_key"]),
        ("f" * 255, {}, ["f" * 255]),
        ("f" * 255 + "=" + "b" * 255, {"f" * 255: "b" * 255}, []),
    )
    @ddt.unpack
    def test_parse_str_meta_success(
            self, input_data, expect_set_dict, expected_unset_list):
        set_dict, unset_list = utils.parse_str_meta(input_data)

        self.assertEqual(expect_set_dict, set_dict)
        self.assertEqual(expected_unset_list, unset_list)

    @ddt.data(
        "a b",
        "'a b'",
        "\"a b\"",
        "f" * 256,
        "f" * 256 + "=bar",
        "foo=" + "b" * 256,
        "\"a b \"",
        "foo=bar\nfoo",
        "foo=bar\nfoo=quuz",
    )
    def test_parse_str_meta_validation_error(self, input_data):
        self.assertRaises(ValidationError, utils.parse_str_meta, input_data)
