import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'
invalid_tf = path + '/generic/invalid-tf.tf'

# tf
terraform_for_mappings_tests_json = path + '/tf/terraform_for_mappings_tests.tf'
terraform_aws_simple_components = path + '/tf/aws_simple_components.tf'
terraform_aws_multiple_components = path + '/tf/aws_multiple_components.tf'
terraform_aws_singleton_components = path + '/tf/aws_singleton_components.tf'
terraform_aws_altsource_components = path + '/tf/aws_altsource_components.tf'
terraform_aws_security_groups_components = path + '/tf/aws_security_groups_components.tf'
terraform_aws_dataflows = path + '/tf/aws_dataflows.tf'
terraform_aws_parent_children_components = path + '/tf/aws_parent_children_components.tf'
terraform_aws_singleton_components_unix_line_breaks = path + '/tf/aws_singleton_components_unix_line_breaks.tf'
terraform_component_without_parent = path + '/tf/aws_component_without_parent.tf'
terraform_skipped_component_without_parent = path + '/tf/aws_component_without_parent_skipped.tf'
terraform_unknown_resource = path + '/tf/terraform_unknown_resource.tf'
terraform_unknown_module = path + '/tf/terraform_unknown_module.tf'
terraform_no_resources = path + '/tf/no_resources.tf'
terraform_gz = path + '/tf/terraform.gz'
terraform_specific_functions = path + '/tf/terraform_specific_functions.tf'
terraform_modules = path + '/tf/terraform_modules_sample.tf'
terraform_extra_modules_sample = path + '/tf/terraform_extra_modules_sample.tf'
terraform_elb = path + '/tf/elb.tf'
terraform_single_tf = path + '/tf/single_tf_file.tf'
terraform_networks = path + '/tf/networks_tf_file.tf'
terraform_resources = path + '/tf/resources_tf_file.tf'
terraform_invalid_size = path + '/tf/terraform_invalid_size.tf'
terraform_minimal_content = path + '/tf/terraform_minimal_content.tf'
terraform_orphan_component = path + '/tf/terraform_orphan_component.tf'
terraform_main_referenced_variables = path + '/tf/terraform_main_referenced_variables.tf'
terraform_vars_referenced_variables = path + '/tf/terraform_vars_referenced_variables.tf'
terraform_variables_file_referenced_variables = path + '/tf/terraform_variables_files_referenced_variables.tfvars'
terraform_components_from_same_resource = path + '/tf/terraform_components_from_same_resource.tf'
terraform_resources_with_same_name = path + '/tf/terraform_resources_with_same_name.tf'
terraform_define_parent_relationship = path + '/tf/calculate_parents/terraform_define_parent_relationship.tf'
terraform_aws_security_group_in_and_eg_gress \
    = path + '/tf/mapping_functions/terraform_aws_security_group_in_and_eg_gress.tf'
terraform_multiple_aws_security_group = path + '/tf/mapping_functions/terraform_multiple_aws_security_group.tf'
terraform_components_with_trustzones_of_same_type = path + '/tf/terraform_components_with_trustzones_of_same_type.tf'

# mapping
terraform_mapping_aws_component_without_parent = path + '/mapping/terraform_mapping_component_without_parent.yaml'
terraform_mapping_specific_functions = path + '/mapping/terraform_mapping_specific_functions.yaml'
terraform_mapping_modules = path + '/mapping/terraform_mapping_modules.yaml'
terraform_mapping_extra_modules = path + '/mapping/terraform_mapping_extra_modules.yaml'
terraform_iriusrisk_tf_aws_mapping = path + '/mapping/iriusrisk-tf-aws-mapping.yaml'
terraform_iriusrisk_tf_aws_mapping_v180 = path + '/mapping/iriusrisk-tf-aws-mapping-1.8.0.yaml'
empty_terraform_mapping = path + '/mapping/empty_terraform_mapping.yaml'
tf_mapping_parent_by_full_path_attribute = path + \
                                           '/mapping/calculate_parents/tf_mapping_parent_by_full_path_attribute.yaml'
tf_mapping_parent_by_type_name = path + \
                                 '/mapping/calculate_parents/tf_mapping_parent_by_type_name.yaml'
tf_mapping_parent_by_name = path + \
                                 '/mapping/calculate_parents/tf_mapping_parent_by_name.yaml'
tf_mapping_children_by_full_path_attribute = path + \
                                           '/mapping/calculate_children/tf_mapping_children_by_full_path_attribute.yaml'
tf_mapping_children_by_type_name = path + \
                                 '/mapping/calculate_children/tf_mapping_children_by_type_name.yaml'
tf_mapping_children_by_name = path + \
                                 '/mapping/calculate_children/tf_mapping_children_by_name.yaml'
terraform_trustzone_types_mapping = path + '/mapping/terraform_trustzone_types_mapping.yaml'
terraform_multiple_trustzones_same_type_mapping = path + '/mapping/terraform_multiple_trustzones_same_type_mapping.yaml'
invalid_no_dataflows = path + '/mapping/invalid-mapping-without-dataflows.yaml'

# otm
tf_file_expected_result = path + '/otm/tf-file-expected-result.otm'
otm_with_only_default_trustzone_expected_result = path + '/otm/otm_with_only_default_trustzone_expected_result.otm'
minimal_otm_expected_result = path + '/otm/minimal_otm_expected_result.otm'
expected_orphan_component_is_not_mapped = path + '/otm/expected_orphan_component_is_not_mapped.otm'
expected_separated_networks_components = path + '/otm/expected_separated_network_components.otm'
expected_aws_altsource_components = path + '/otm/expected_aws_altsource_components.otm'
expected_aws_dataflows = path + '/otm/expected_aws_dataflows.otm'
expected_aws_parent_children_components = path + '/otm/expected_aws_parent_children_components.otm'
expected_aws_security_groups_components = path + '/otm/expected_aws_security_groups_components.otm'
expected_aws_singleton_components = path + '/otm/expected_aws_singleton_components.otm'
expected_elb_example = path + '/otm/expected_elb_example.otm'
expected_extra_modules = path + '/otm/expected_extra_modules.otm'
expected_mapping_modules = path + '/otm/expected_mapping_modules.otm'
expected_mapping_skipped_component_without_parent = path + '/otm/expected_mapping_skipped_component_without_parent.otm'
expected_no_resources = path + '/otm/expected_no_resources.otm'
expected_run_valid_mappings = path + '/otm/expected_run_valid_mappings.otm'
tf_file_referenced_vars_expected_result = path + '/otm/tf-file-referenced-vars-expected-result.otm'
terraform_minimal_content_otm = f'{path}/otm/terraform_minimal_content.otm'
tf_components_with_trustzones_of_same_type_otm = f'{path}/otm/tf_components_with_trustzones_of_same_type.otm'
