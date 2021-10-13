import os


class ApiConfig:
    iriusrisk_server: str

    @classmethod
    def set_iriusrisk_server(cls, server: str):
        cls.iriusrisk_server = server

    @classmethod
    def get_iriusrisk_server(cls):
        if not hasattr(cls, 'iriusrisk_server'):
            cls.iriusrisk_server = os.environ['IRIUS_SERVER']
        return cls.iriusrisk_server