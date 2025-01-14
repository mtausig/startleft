from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.representation import DiagramRepresentation, RepresentationType
from otm.otm.entity.trustzone import Trustzone
from otm.otm.otm_builder import OTMBuilder
from otm.otm.otm_pruner import OTMPruner
from slp_base import ProviderParser
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper
from slp_visio.slp_visio.parse.mappers.diagram_connector_mapper import DiagramConnectorMapper
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper
from slp_visio.slp_visio.parse.representation.representation_calculator import RepresentationCalculator, \
    build_size_object, calculate_diagram_size


class VisioParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        self.project_id = project_id
        self.project_name = project_name
        self.diagram = diagram
        self.mapping_loader = mapping_loader

        self.representation_id = f'{self.project_id}-diagram'
        self.representations = [
            DiagramRepresentation(
                id_=self.representation_id,
                name=f'{self.project_id} Diagram Representation',
                type_=RepresentationType.DIAGRAM,
                size=build_size_object(calculate_diagram_size(self.diagram.limits))
            )
        ]

        self._representation_calculator = RepresentationCalculator(self.representation_id, self.diagram.limits)
        self._trustzone_mappings = self.mapping_loader.get_trustzone_mappings()
        self._component_mappings = self.mapping_loader.get_component_mappings()
        self.__default_trustzone = self.mapping_loader.get_default_otm_trustzone()

    def build_otm(self):
        self.__prune_diagram()

        components = self.__map_components()
        trustzones = self.__map_trustzones()
        dataflows = self.__map_dataflows()

        otm = self.__build_otm(trustzones, components, dataflows)

        OTMPruner(otm).prune_orphan_dataflows()

        return otm

    def __prune_diagram(self):
        DiagramPruner(self.diagram, self.mapping_loader.get_all_labels()).run()

    def __map_trustzones(self):
        trustzone_mapper = DiagramTrustzoneMapper(
            self.diagram.components,
            self._trustzone_mappings,
            self._representation_calculator
        )
        return trustzone_mapper.to_otm()

    def __map_components(self):
        return DiagramComponentMapper(
            self.diagram.components,
            self._component_mappings,
            self._trustzone_mappings,
            self.__default_trustzone,
            self._representation_calculator,
        ).to_otm()

    def __map_dataflows(self):
        return DiagramConnectorMapper(self.diagram.connectors).to_otm()

    def __build_otm(self, trustzones: [Trustzone], components: [Component], dataflows: [Dataflow]):
        otm_builder = OTMBuilder(self.project_id, self.project_name, self.diagram.diagram_type) \
            .add_representations(self.representations, extend=False) \
            .add_trustzones(trustzones) \
            .add_components(components) \
            .add_dataflows(dataflows)

        if self.__default_trustzone and self.__any_default_tz(components):
            otm_builder.add_default_trustzone(self.__default_trustzone)

        return otm_builder.build()

    def __any_default_tz(self, components):
        for component in components:
            if self.__default_trustzone and component.parent \
                    and component.parent == self.__default_trustzone.id:
                return True
        return False
