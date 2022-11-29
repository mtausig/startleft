import jmespath
import yaml
from deepmerge import always_merger

from otm.otm.otm import Trustzone
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_base import MappingLoader
from slp_base.slp_base.mapping_file_loader import MappingFileLoader


def load_mappings(mapping_file):
    if isinstance(mapping_file, dict):
        return mapping_file
    else:
        if isinstance(mapping_file, str):
            with open(mapping_file, 'r') as f:
                return always_merger.merge(mapping_file, yaml.load(f, Loader=yaml.BaseLoader))
        else:
            return always_merger.merge(mapping_file, yaml.load(mapping_file, Loader=yaml.BaseLoader))


class VisioMappingFileLoader(MappingLoader):

    def __init__(self, mapping_files):
        self.component_mappings = None
        self.trustzone_mappings = None
        self.default_otm_trustzone = None
        mapping = MappingFileLoader(mapping_files).load()
        self.mappings = load_mappings(mapping)

    def load(self):
        self.default_otm_trustzone = self.__load_default_otm_trustzone()
        self.trustzone_mappings = self.__load_trustzone_mappings()
        self.component_mappings = self.__load_component_mappings()

    def get_all_labels(self) -> [str]:
        component_and_tz_mappings = self.mappings['components'] + self.mappings['trustzones']
        return [c['label'] for c in component_and_tz_mappings]

    def __load_default_otm_trustzone(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.mappings)
        default_trustzones = [v for v in trustzone_mappings_list if 'default' in v and v['default']]
        default_otm_trustzone = default_trustzones[-1] if len(default_trustzones) > 0 else None
        if default_otm_trustzone:
            name = default_otm_trustzone['label']
            return Trustzone(id=deterministic_uuid(name), name=name, type=default_otm_trustzone['type'],
                             properties={"default": True})

    def __load_trustzone_mappings(self):
        trustzone_mappings_list = jmespath.search("trustzones", self.mappings)
        return dict(zip([tz['label'] for tz in trustzone_mappings_list], trustzone_mappings_list))

    def __load_component_mappings(self):
        component_mappings_list = jmespath.search("components", self.mappings)
        return dict(zip([tz['label'] for tz in component_mappings_list], component_mappings_list))

    def get_trustzone_mappings(self):
        return self.trustzone_mappings

    def get_default_otm_trustzone(self):
        return self.default_otm_trustzone

    def get_component_mappings(self):
        return self.component_mappings
