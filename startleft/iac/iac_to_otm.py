import json
import logging
from io import StringIO

import hcl2
import xmltodict
import yaml

from startleft.iac.iac_type import IacType
from startleft.iac.mapping import transformer, sourcemodel
from startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.otm import otm
from startleft.provider import Provider
from startleft.validators.mapping_validator import MappingValidator

logger = logging.getLogger(__name__)


class IacToOtm:
    """
    This class is in charge of the methods to convert IaC code to OTM files
    """
    EXIT_UNEXPECTED = 1
    EXIT_VALIDATION_FAILED = 2

    def __init__(self, project_name, project_id, provider: Provider):
        self.otm = otm.OTM(project_name, project_id, provider)
        self.source_model = sourcemodel.SourceModel()
        self.source_model.otm = self.otm
        self.transformer = transformer.Transformer(source_model=self.source_model, threat_model=self.otm)
        self.mapping_file_loader = MappingFileLoader()
        self.mapping_validator = MappingValidator('iac_mapping_schema.json')
        self.source_loader_map = {
            IacType.CLOUDFORMATION: self.load_yaml_source,
            IacType.TERRAFORM: self.load_hcl2_source
        }

    def load_xml_source(self, filename):
        if isinstance(filename, str):
            with open(filename, 'rb') as f:
                self.source_model.load(xmltodict.parse(f.read(), xml_attribs=True))
        else:
            self.source_model.load(xmltodict.parse(filename.read(), xml_attribs=True))

    def load_yaml_source(self, filename):
        if isinstance(filename, str):
            with open(filename, 'r') as f:
                self.source_model.load(yaml.load(f, Loader=yaml.BaseLoader))
        else:
            self.source_model.load(yaml.load(filename, Loader=yaml.BaseLoader))

    def load_hcl2_source(self, filename):
        if isinstance(filename, str):
            with open(filename, 'r') as f:
                self.source_model.load(hcl2.load(f))
        else:
            self.source_model.load(hcl2.load(StringIO(initial_value=str(filename.read(), 'utf-8'), newline=None)))

    def load_source_files(self, loader, filenames):
        if isinstance(filenames, str):
            filenames = [filenames]        
        for filename in filenames:
            logger.info(f"Loading source file '{filename}'")
            try:
                loader(filename)
            except FileNotFoundError:
                logger.warning(f"Cannot find source file '{filename}', skipping")
        logger.debug("Source files loaded successfully")

    def get_otm_stream(self):
        logger.info(f"Getting OTM stream")
        return self.otm.json()

    def run(self, type_, map_filenames, filenames):
        """
        Parses selected source files and maps them to the Open Threat Model format
        """
        loader = self.source_loader_map[type_]
        self.load_source_files(loader, filenames)

        iac_mapping = self.mapping_file_loader.load(map_filenames)
        self.mapping_validator.validate(iac_mapping)

        self.transformer.run(iac_mapping)

    def search(self, type_, query, filenames):
        """
        Runs a JMESPath search query against the provided source files and outputs the matching results
        """        
        loader = self.source_loader_map[type_]
        self.load_source_files(loader, filenames)
        
        logger.info(f"Searching for '{query}' in source:")
        logger.info(json.dumps(self.source_model.data, indent=2))
        logger.info("--- Results ---")
        logger.info(json.dumps(self.source_model.query(query), indent=2))