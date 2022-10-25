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

# mapping
default_terraform_mapping = path + '/mapping/default-terraform-mapping.yaml'
default_terraform_aws_mapping = path + '/mapping/aws_terraform_mapping.yaml'
terraform_mapping_aws_component_without_parent = path + '/mapping/terraform_mapping_component_without_parent.yaml'
terraform_malformed_mapping_wrong_id = path + '/mapping/terraform-malformed-mapping-wrong-id.yaml'
terraform_mapping_specific_functions = path + '/mapping/terraform_mapping_specific_functions.yaml'
terraform_mapping_modules = path + '/mapping/terraform_mapping_modules.yaml'
terraform_mapping_extra_modules = path + '/mapping/terraform_mapping_extra_modules.yaml'
terraform_iriusrisk_tf_aws_mapping = path + '/mapping/iriusrisk-tf-aws-mapping.yaml'
empty_terraform_mapping = path + '/mapping/empty_terraform_mapping.yaml'

# otm
tf_file_expected_result = path + '/otm/tf-file-expected-result.otm'
otm_with_only_default_trustzone_expected_result = path + '/otm/otm_with_only_default_trustzone_expected_result.otm'
minimal_otm_expected_result = path + '/otm/minimal_otm_expected_result.otm'
expected_orphan_component_is_not_mapped = path + '/otm/expected_orphan_component_is_not_mapped.otm'