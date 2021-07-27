import logging
logger = logging.getLogger(__name__)

import sys
import os
import json
import yaml
import hcl2
from startleft import threatmodel, sourcemodel, transformer, iriusrisk, diagram


class IacToOtmApp:

    EXIT_UNEXPECTED = 1
    EXIT_VALIDATION_FAILED = 2

    def __init__(self, name, id):
        self.threat_model = threatmodel.ThreatModel(name, id)
        self.source_model = sourcemodel.SourceModel()
        self.source_model.otm = self.threat_model
        self.transformer = transformer.Transformer(source_model=self.source_model, threat_model=self.threat_model)

        self.source_loader_map = {
            'JSON': self.load_yaml_source,
            'YAML': self.load_yaml_source,
            'CLOUDFORMATION': self.load_yaml_source,
            'HCL2': self.load_hcl2_source,
            'TERRAFORM': self.load_hcl2_source
        }

    def load_yaml_source(self, filename):
        logger.debug(f"Loading YAML source file: {filename}")
        with open(filename, 'r') as f:
            self.source_model.load(yaml.load(f, Loader=yaml.BaseLoader))

    def load_hcl2_source(self, filename):
        logger.debug(f"Loading HCL2 source file: {filename}")
        with open(filename, 'r') as f:
            self.source_model.load(hcl2.load(f))

    def load_source_files(self, loader, filenames):
        logger.debug(f"Parsing IaC source files of type {type} to OTM")
        if isinstance(filenames, str):
            filenames = [filenames]        
        for filename in filenames:
            logger.debug(f"Parsing source file '{filename}'")
            try:
                loader(filename)
            except FileNotFoundError:
                logger.warn(f"Cannot find source file '{filename}', skipping")

    def load_mapping_files(self, filenames):
        if isinstance(filenames, str):
            filenames = [filenames]
        for filename in filenames:
            logger.debug(f"Loading mapping file {filename}")
            try:
                with open(filename, 'r') as f:
                    self.transformer.load(yaml.load(f, Loader=yaml.BaseLoader))
            except FileNotFoundError:
                logger.error(f"Cannot find mapping file '{filename}'")
                sys.exit(IacToOtmApp.EXIT_UNEXPECTED)
        logger.debug("Validating mapping schema")
        schema = self.transformer.validate_mapping()
        if not schema.valid:
            logger.error('Mapping files are not valid')
            logger.error(f"--- Schema errors---\n{schema.errors}\n--- End of schema errors ---")
            sys.exit(IacToOtmApp.EXIT_VALIDATION_FAILED)            

    def write_threatmodel(self, out_file):
        logger.info(f"Writing threat model to '{out_file}'")
        try:
            with open(out_file, "w") as f:
                json.dump(self.threat_model.json(), f, indent=2)
        except Exception as e:
            logger.error(f"Unable to create the threat model: {e}")
            sys.exit(IacToOtmApp.EXIT_UNEXPECTED)

    def run(self, type, map_filenames, out_file, filenames):
        """
        Parses selected source files and maps them to the Open Threat Model format
        """
        loader = self.source_loader_map[type.upper()]
        self.load_source_files(loader, filenames)
        self.load_mapping_files(map_filenames)

        self.transformer.run()
        self.write_threatmodel(out_file)

    def search(self, type, query, filenames):
        """
        Runs a JMESPath search query against the provided source files and outputs the matching results
        """        
        loader = self.source_loader_map[type.upper()]
        self.load_source_files(loader, filenames)
        
        logger.info(f"Searching for '{query}' in source:")
        logger.info(json.dumps(self.source_model.data, indent=2))
        logger.info("--- Results ---")
        logger.info(json.dumps(self.source_model.query(query), indent=2))

    def validate(self, filename):
        """
        Vallidates a mapping file against the mapping file schema.
        """

        logger.debug(f"Validating mapper file '{filename}'")
        self.load_mapping_files(filename)
        logger.debug(f"--- File to validate ---\n{self.transformer.map}\n--- End of file ---")

        schema = self.transformer.validate_mapping()
        if schema.valid:
            logger.info('Mapper file is valid')
        else:
            logger.error('Mapper file is not valid')
            logger.error(f"--- Schema errors---\n{schema.errors}\n--- End of schema errors ---")
            sys.exit(IacToOtmApp.EXIT_VALIDATION_FAILED)


class OtmToIr:
    EXIT_UNEXPECTED = 3
    EXIT_VALIDATION_FAILED = 4

    def __init__(self):
        self.iriusrisk = iriusrisk.IriusRisk(os.getenv("IRIUS_SERVER"), os.getenv("IRIUS_API_TOKEN"))
        self.diagram = diagram.Diagram()

    def load_otm_files(self, filenames):
        for filename in filenames:
            logger.debug(f"Loading OTM file {filename}")
            with open(filename, 'r') as f:
                self.iriusrisk.load_otm_file(yaml.load(f, Loader=yaml.BaseLoader))            

    def load_map_files(self, filenames):
        for filename in filenames:
            logger.debug(f"Loading map file {filename}")
            with open(filename, 'r') as f:
                map = yaml.load(f, Loader=yaml.BaseLoader)
                self.iriusrisk.load_map(map)
                self.diagram.load_map(map)

    def run(self, map, recreate, filename):

        logger.debug("Loading OTM files")
        self.load_otm_files(filename)
        logger.debug("Loading mapping files")
        self.load_map_files(map)

        logger.debug("Processing diagram trustzones")
        for trustzone in self.iriusrisk.otm["trustzones"]:
            self.diagram.add_trustzone(trustzone)

        logger.debug("Processing diagram components")
        for component in self.iriusrisk.otm["components"]:
            self.diagram.add_component(component)

        logger.debug("Processing diagram dataflows")
        for dataflow in self.iriusrisk.otm["dataflows"]:
            self.diagram.add_dataflow(dataflow)

        logger.debug("Generating diagram layout")
        self.diagram.generate_layout()
        diagram_xml = self.diagram.xml()
        with open("diagram.xml", "wb") as f:
            logger.debug("Writing diagram to 'diagram.xml'")
            f.write(diagram_xml)

        logger.debug("Processing threat model trustzones")
        for trustzone in self.iriusrisk.otm["trustzones"]:
            self.iriusrisk.add_trustzone(trustzone)

        logger.debug("Processing threat model components")
        for component in self.iriusrisk.otm["components"]:
            self.iriusrisk.add_component(component)

        logger.debug("Processing threat model dataflows")
        for dataflow in self.iriusrisk.otm["dataflows"]:
            self.iriusrisk.add_dataflow(dataflow)

        logger.debug("Resolving component trustzones")
        self.iriusrisk.resolve_component_trustzones()
        if recreate:
            logger.debug("Recreating diagram in IriusRisk")
            self.iriusrisk.recreate_diagram(diagram_xml)
        else:
            logger.debug("Upserting diagram to IriusRisk")
            self.iriusrisk.upsert_diagram(diagram_xml)
        logger.debug("Running rules engine")
        self.iriusrisk.run_rules()

    def validate(self, filename):
        """
        Vallidates a mapping file against the mapping file schema.
        """

        logger.debug(f"Validating mapper file '{filename}'")
        self.load_otm_files(filename)
        logger.debug(f"--- File to validate ---\n{self.iriusrisk.otm}\n--- End of file ---")

        schema = self.iriusrisk.validate_otm()
        if schema.valid:
            logger.info('OTM file is valid')
        else:
            logger.error('OTM file is not valid')
            logger.error(f"--- Schema errors---\n{schema.errors}\n--- End of schema errors ---")
            sys.exit(OtmToIr.EXIT_VALIDATION_FAILED)