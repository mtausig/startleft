from _pytest.python_api import raises
from jmespath.exceptions import JMESPathTypeError

from startleft.api.errors import MappingFileSchemaNotValidError
from startleft.project.otm_project import OtmProject
from tests.resources import test_resource_paths

SAMPLE_OTM_FILENAME = test_resource_paths.otm_file_example
SAMPLE_YAML_IAC_FILENAME = test_resource_paths.cloudformation_for_mappings_tests_json
IAC_VALID_MAPPING_FILENAME = test_resource_paths.default_mapping
INVALID_YAML_FILENAME = test_resource_paths.invalid_yaml


class TestOtmProjectService:

    def test_from_otm_id_and_name_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename, project_id, project_name)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == project_name

    def test_from_otm_id_and_name_not_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project id
        project_id = 'id'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename=otm_filename, project_id=project_id)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == otm_project.otm['project']['id']

    def test_from_iac_custom_mapping_files_not_provided_ok(self):
        # Given a sample valid OTM file
        otm_filename = SAMPLE_OTM_FILENAME

        # And a project name
        project_name = 'name'

        # When creating OTM project from OTM file
        otm_project = OtmProject.from_otm_file(otm_filename=otm_filename, project_name=project_name)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == otm_project.otm['project']['id']
        assert otm_project.project_name == project_name

    def test_from_iac_valid_yaml_mapping_files_provided_ok(self):
        # Given a sample valid IaC file
        iac_file = [open(SAMPLE_YAML_IAC_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # And a valid iac mappings file
        custom_iac_mapping_files = [IAC_VALID_MAPPING_FILENAME]

        # When creating OTM project from IaC file
        otm_project = OtmProject.from_iac_file(project_id, project_name, 'YAML', iac_file,
                                               custom_iac_mapping_files)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == project_name

    def test_from_iac_valid_yaml_mapping_files_not_provided_ok(self):
        # Given a sample valid IaC file
        iac_file = [open(SAMPLE_YAML_IAC_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from IaC file
        otm_project = OtmProject.from_iac_file(project_id, project_name, 'YAML', iac_file)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == project_name

    def test_from_iac_invalid_yaml_iac_file_error_jmes_error(self):
        # Given a sample valid IaC file
        iac_file = [open(INVALID_YAML_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from IaC file
        # Then raises MappingFileSchemaNotValidError
        with raises(JMESPathTypeError):
            OtmProject.from_iac_file(project_id, project_name, 'YAML', iac_file)

    def test_from_iac_invalid_mapping_files_error_invalid_schema(self):
        # Given a sample valid IaC file
        iac_file = [open(SAMPLE_YAML_IAC_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # And a invalid iac mappings file
        custom_iac_mapping_files = [INVALID_YAML_FILENAME]

        # When creating OTM project from IaC file
        # Then raises MappingFileSchemaNotValidError
        with raises(MappingFileSchemaNotValidError):
            OtmProject.from_iac_file(project_id, project_name, 'YAML', iac_file, custom_iac_mapping_files)

    def test_from_iac_file_to_otm_stream_ok(self):
        # Given a sample valid IaC file
        iac_file = [open(SAMPLE_YAML_IAC_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from IaC file having result as stream instead of file
        otm_project = OtmProject.from_iac_file_to_otm_stream(project_id, project_name, 'YAML', iac_file, None)

        # Then
        assert otm_project.otm is not None
        assert otm_project.project_id == project_id
        assert otm_project.project_name == project_name
        assert otm_project.get_otm_as_json() is not None

    def test_from_iac_file_otm_stream_invalid_file_ok(self):
        # Given a sample valid IaC file
        iac_file = [open(INVALID_YAML_FILENAME, 'r')]

        # And a project id
        project_id = 'id'

        # And a project name
        project_name = 'name'

        # When creating OTM project from IaC file having result as stream instead of file
        # Then raises JMESPathTypeError
        with raises(JMESPathTypeError):
            OtmProject.from_iac_file_to_otm_stream(project_id, project_name, 'YAML', iac_file, None)
