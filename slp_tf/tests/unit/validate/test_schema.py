from unittest import TestCase

import yaml

from slp_base.slp_base.schema import Schema
from slp_tf import TerraformMappingFileValidator
from slp_tf.tests.resources import test_resource_paths

SCHEMA_FILENAME = TerraformMappingFileValidator.schema_filename
VALID_MAPPING_FILE = test_resource_paths.terraform_iriusrisk_tf_aws_mapping
INVALID_MAPPING_FILE = test_resource_paths.invalid_no_dataflows


class TestSchema(TestCase):

    def test_valid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_tf', SCHEMA_FILENAME)
        mapping_file = VALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert mapping_file_schema.valid

    def test_invalid_mapping(self):
        mapping_file_schema = Schema.from_package('slp_tf', SCHEMA_FILENAME)
        mapping_file = INVALID_MAPPING_FILE

        with open(mapping_file) as file:
            mapping_file_content = file.read()

        mapping_file_data = yaml.load(mapping_file_content, Loader=yaml.SafeLoader)

        mapping_file_schema.validate(mapping_file_data)

        assert not mapping_file_schema.valid
        assert mapping_file_schema.errors == "'dataflows' is a required property"