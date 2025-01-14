import pytest

from sl_util.sl_util.file_utils import get_data
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import expected_aws_parent_children_components, \
    tf_mapping_children_by_full_path_attribute, tf_mapping_children_by_type_name, tf_mapping_children_by_name
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping
from slp_tf.tests.utility import excluded_regex
from slp_base.tests.util.otm import validate_and_compare

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformCalculateChildren:

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_aws_parent_children_components(self, mapping_file):
        # GIVEN a valid TF file with some resources
        terraform_file = get_data(test_resource_paths.terraform_aws_parent_children_components)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_aws_parent_children_components, excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(tf_mapping_children_by_type_name), id="by {type}.{name}"),
        pytest.param(get_data(tf_mapping_children_by_full_path_attribute), id="by full path attribute"),
        pytest.param(get_data(tf_mapping_children_by_name), id="by {name}")])
    def test_define_children_relationship(self, mapping_file):
        """
        Generate an OTM for TF file with children definition
        """
        # GIVEN a TF file with two resources
        #    AND a mapping file with children definition
        tf_file = get_data(test_resource_paths.terraform_aws_parent_children_components)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND resource_be defines resource_a as parent
        assert len(otm.components) == 2
        assert otm.components[0].name == "mongo"
        assert otm.components[0].type == "elastic-container-service"
        assert otm.components[0].parent == otm.trustzones[0].id

        assert otm.components[1].name == "service"
        assert otm.components[1].type == "docker-container"
        assert otm.components[1].parent == otm.components[0].id


