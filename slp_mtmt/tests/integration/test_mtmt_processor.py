import json
from unittest.mock import patch

from pytest import mark

from otm.otm.entity.representation import Representation, DiagramRepresentation, RepresentationElement
from sl_util.sl_util.file_utils import get_byte_data
from slp_base.tests.util.otm import validate_and_compare
from slp_mtmt import MTMTProcessor
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import mapping_mtmt_mvp_legacy, mapping_mtmt_mvp_no_type

SAMPLE_ID = 'example-project'
SAMPLE_NAME = 'Example Project'
SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mapping_mtmt_mvp
DEFAULT_MAPPING_FILE = test_resource_paths.mtmt_default_mapping
MTMT_MISSING_POSITION = test_resource_paths.missing_position
MTMT_EXAMPLE_POSITION = test_resource_paths.example_position_tm7
OTM_EXAMPLE_POSITION = test_resource_paths.example_position_otm
MTMT_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_tm7
OTM_EXAMPLE_1LINE = test_resource_paths.position_1line_tz_otm
MTMT_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_tm7
OTM_EXAMPLE_1ORPHAN = test_resource_paths.position_1orphan_otm


class TestMtmtProcessor:
    excluded_regex = [
        r"root\['components'\]\[.+?\]\['threats'\]",
        r"root\['threats'\]",
        r"root\['mitigations'\]"
    ]

    @mark.parametrize('mapping_file', [SAMPLE_VALID_MAPPING_FILE, mapping_mtmt_mvp_legacy, mapping_mtmt_mvp_no_type])
    def test_run_valid_mappings(self, mapping_file):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(SAMPLE_VALID_MTMT_FILE)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(mapping_file)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 6
        assert len(otm.threats) == 43
        assert len(otm.mitigations) == 43

        # AND the project info is also right
        assert otm.project_id == "example-project"
        assert otm.project_name == "Example Project"

        # AND the representations info is also right
        assert len(otm.representations) == 2
        tm_representation: Representation = otm.representations[0]
        assert tm_representation.id == 'Microsoft Threat Modeling Tool'
        assert tm_representation.name == 'Microsoft Threat Modeling Tool'
        assert tm_representation.type == 'threat-model'
        diag_representation: DiagramRepresentation = otm.representations[1]
        assert diag_representation.id == 'example-project-diagram'
        assert diag_representation.name == 'example-project Diagram Representation'
        assert diag_representation.type == 'diagram'
        assert diag_representation.size == {'width': 2000, 'height': 2000}

        # AND the info inside trustzones is also right
        for trustzone in otm.trustzones:
            assert len(trustzone.representations) == 1
            element_representation: RepresentationElement = trustzone.representations[0]
            assert element_representation.representation == 'example-project-diagram'
            assert element_representation.name == trustzone.name + ' Representation'
        trustzone = otm.trustzones[0]
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        assert trustzone.type == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        element_representation = trustzone.representations[0]
        assert element_representation.position == {'x': 332, 'y': 136}
        assert element_representation.size == {'height': 311, 'width': 320}
        trustzone = otm.trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'
        assert trustzone.type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        element_representation = trustzone.representations[0]
        assert element_representation.position == {'x': 744, 'y': 142}
        assert element_representation.size == {'height': 308, 'width': 371}

        # AND the info inside components is also right
        for component in otm.components:
            assert len(component.representations) == 1
            element_representation = component.representations[0]
            assert element_representation.representation == 'example-project-diagram'
            assert element_representation.id == component.id + '-representation'
            assert element_representation.name == component.name + ' Representation'

        component = otm.components[0]
        assert component.id == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert component.name == 'Accounting PostgreSQL'
        assert component.type == 'CD-MICROSOFT-AZURE-DB-POSTGRESQL'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        element_representation = component.representations[0]
        assert element_representation.position == {'x': 231, 'y': 40}
        assert element_representation.size == {'height': 82, 'width': 82}
        assert len(component.threats) == 3
        component = otm.components[1]
        assert component.id == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert component.name == 'Mobile Client'
        assert component.type == 'android-device-client'
        assert component.parent == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        element_representation = component.representations[0]
        assert element_representation.position == {'x': 101, 'y': 104}
        assert element_representation.size == {'height': 82, 'width': 82}
        assert len(component.threats) == 2
        component = otm.components[2]
        assert component.id == '5d15323e-3729-4694-87b1-181c90af5045'
        assert component.name == 'Public API v2'
        assert component.type == 'web-service'
        assert component.parent == "24cdf4da-ac7f-4a35-bab0-29256d4169bf"
        element_representation = component.representations[0]
        assert element_representation.position == {'x': 21, 'y': 101}
        assert element_representation.size == {'height': 82, 'width': 82}
        assert len(component.threats) == 31
        component = otm.components[3]
        assert component.id == '91882aca-8249-49a7-96f0-164b68411b48'
        assert component.name == 'Azure File Storage'
        assert component.type == 'azure-storage'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        element_representation = component.representations[0]
        assert element_representation.position == {'x': 230, 'y': 169}
        assert element_representation.size == {'height': 82, 'width': 82}
        assert len(component.threats) == 7

        # AND the info inside dataflows is also right
        dataflow = otm.dataflows[0]
        assert dataflow.id == 'eb072144-af37-4b75-b46b-b78111850d3e'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert not dataflow.bidirectional
        dataflow = otm.dataflows[1]
        assert dataflow.id == '36091fd8-dba8-424e-a3cd-784ea6bcb9e0'
        assert dataflow.source_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = otm.dataflows[2]
        assert dataflow.id == 'f5fe3c6e-e10b-4252-a4aa-4ec6108c96a6'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '91882aca-8249-49a7-96f0-164b68411b48'
        dataflow = otm.dataflows[3]
        assert dataflow.id == 'd826de3d-1464-4d1f-8105-aa0449a50aec'
        assert dataflow.source_node == '91882aca-8249-49a7-96f0-164b68411b48'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = otm.dataflows[4]
        assert dataflow.id == '9840bcdf-c444-437d-8289-d5468f41b0db'
        assert dataflow.source_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = otm.dataflows[5]
        assert dataflow.id == '5861370d-b333-4d4b-9420-95425026e9c9'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'

    @patch('slp_base.slp_base.otm_validator.OtmValidator.validate')
    def test_run_some_missing_source_coordinates(self, validate):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(MTMT_MISSING_POSITION)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # AND we avoid the otm validation
        validate.side_effect = None

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 6

        # AND the project info is also right
        assert otm.project_id == "example-project"
        assert otm.project_name == "Example Project"

        # AND the representations info is also right
        assert len(otm.representations) == 2
        tm_representation: Representation = otm.representations[0]
        assert tm_representation.id == 'Microsoft Threat Modeling Tool'
        assert tm_representation.name == 'Microsoft Threat Modeling Tool'
        assert tm_representation.type == 'threat-model'
        diag_representation: DiagramRepresentation = otm.representations[1]
        assert diag_representation.id == 'example-project-diagram'
        assert diag_representation.name == 'example-project Diagram Representation'
        assert diag_representation.type == 'diagram'
        assert diag_representation.size == {'width': 2000, 'height': 2000}

        # AND we check the trust zone without representations
        assert otm.trustzones[0].representations is None

        # AND we check the trust zone with representations
        assert otm.trustzones[1].representations is None

        # AND we check the component representations
        assert len(otm.components) == 4
        assert otm.components[0].representations is None
        assert otm.components[1].representations is None
        assert otm.components[2].representations is None
        assert otm.components[3].representations is None


    @mark.parametrize('source, expected', [
        (MTMT_EXAMPLE_POSITION, OTM_EXAMPLE_POSITION),
        (MTMT_EXAMPLE_1LINE, OTM_EXAMPLE_1LINE),
        (MTMT_EXAMPLE_1ORPHAN, OTM_EXAMPLE_1ORPHAN)
    ])
    def test_coordinates_borders(self, source, expected):
        # GIVEN a valid MTMT file
        source_file = get_byte_data(source)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(DEFAULT_MAPPING_FILE)

        # AND the expected OTM
        expected_otm = json.loads(get_byte_data(expected))

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # AND we get the json OTM
        otm_json = otm.json()

        # THEN we check the result is as expected
        left, right = validate_and_compare(otm_json, expected_otm, self.excluded_regex)
        assert left == right
