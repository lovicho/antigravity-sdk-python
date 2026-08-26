# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for schema_utils."""

import unittest
from google.genai import types as genai_types
from google.antigravity.tools import schema_utils


class SchemaUtilsTest(unittest.TestCase):

  def test_normalize_primitive_types(self):
    self.assertEqual(schema_utils.normalize_schema("STRING"), "string")
    self.assertEqual(schema_utils.normalize_schema("INTEGER"), "integer")
    self.assertEqual(schema_utils.normalize_schema("NUMBER"), "number")
    self.assertEqual(schema_utils.normalize_schema("BOOLEAN"), "boolean")
    self.assertEqual(schema_utils.normalize_schema("ARRAY"), "array")
    self.assertEqual(schema_utils.normalize_schema("OBJECT"), "object")
    self.assertEqual(schema_utils.normalize_schema("NULL"), "null")

  def test_normalize_genai_type_enums(self):
    self.assertEqual(
        schema_utils.normalize_schema(genai_types.Type.STRING), "string"
    )
    self.assertEqual(
        schema_utils.normalize_schema(genai_types.Type.OBJECT), "object"
    )
    self.assertEqual(
        schema_utils.normalize_schema(genai_types.Type.INTEGER), "integer"
    )
    self.assertEqual(
        schema_utils.normalize_schema(genai_types.Type.BOOLEAN), "boolean"
    )

  def test_normalize_dict_keywords_and_types(self):
    input_schema = {
        "type": "OBJECT",
        "properties": {
            "name": {"type": "STRING", "description": "User name"},
            "age": {"type": "INTEGER"},
            "scores": {
                "type": "ARRAY",
                "items": {"type": "NUMBER"},
            },
        },
        "required": ["name"],
    }
    expected = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "User name"},
            "age": {"type": "integer"},
            "scores": {
                "type": "array",
                "items": {"type": "number"},
            },
        },
        "required": ["name"],
    }
    self.assertEqual(schema_utils.normalize_schema(input_schema), expected)

  def test_normalize_combiners_and_keywords(self):
    input_schema = {
        "any_of": [{"type": "STRING"}, {"type": "INTEGER"}],
        "one_of": [{"type": "BOOLEAN"}],
        "all_of": [{"type": "OBJECT"}],
        "additional_properties": {"type": "STRING"},
        "pattern_properties": {"^[a-z]+$": {"type": "INTEGER"}},
        "min_items": 1,
        "max_items": 10,
        "min_length": 2,
        "max_length": 50,
        "min_properties": 1,
        "max_properties": 5,
        "unique_items": True,
        "$defs": {"CustomNode": {"type": "OBJECT"}},
        "definitions": {"LegacyNode": {"type": "ARRAY"}},
        "type": ["STRING", "NULL", genai_types.Type.BOOLEAN],
    }
    normalized = schema_utils.normalize_schema(input_schema)
    self.assertIn("anyOf", normalized)
    self.assertIn("oneOf", normalized)
    self.assertIn("allOf", normalized)
    self.assertIn("additionalProperties", normalized)
    self.assertIn("patternProperties", normalized)
    self.assertIn("minItems", normalized)
    self.assertIn("maxItems", normalized)
    self.assertIn("minLength", normalized)
    self.assertIn("maxLength", normalized)
    self.assertIn("minProperties", normalized)
    self.assertIn("maxProperties", normalized)
    self.assertIn("uniqueItems", normalized)
    self.assertEqual(normalized["anyOf"][0]["type"], "string")
    self.assertEqual(normalized["anyOf"][1]["type"], "integer")
    self.assertEqual(normalized["oneOf"][0]["type"], "boolean")
    self.assertEqual(normalized["allOf"][0]["type"], "object")
    self.assertEqual(normalized["additionalProperties"]["type"], "string")
    self.assertEqual(
        normalized["patternProperties"]["^[a-z]+$"]["type"], "integer"
    )
    self.assertEqual(normalized["$defs"]["CustomNode"]["type"], "object")
    self.assertEqual(normalized["definitions"]["LegacyNode"]["type"], "array")
    self.assertEqual(normalized["type"], ["string", "null", "boolean"])

  def test_preserve_literal_values(self):
    input_schema = {
        "type": "STRING",
        "enum": ["ACTIVE", "INACTIVE", "PENDING"],
        "const": "UPPERCASE_CONST",
        "default": "DEFAULT_VAL",
    }
    normalized = schema_utils.normalize_schema(input_schema)
    self.assertEqual(normalized["type"], "string")
    self.assertEqual(normalized["enum"], ["ACTIVE", "INACTIVE", "PENDING"])
    self.assertEqual(normalized["const"], "UPPERCASE_CONST")
    self.assertEqual(normalized["default"], "DEFAULT_VAL")

  def test_passthrough_non_schema_values(self):
    self.assertEqual(schema_utils.normalize_schema(42), 42)
    self.assertEqual(schema_utils.normalize_schema(3.14), 3.14)
    self.assertTrue(schema_utils.normalize_schema(True))
    self.assertIsNone(schema_utils.normalize_schema(None))
    self.assertEqual(
        schema_utils.normalize_schema("custom_literal"), "custom_literal"
    )


if __name__ == "__main__":
  unittest.main()
