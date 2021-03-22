# -*- coding: utf-8 -*-
from log_manager import LogManager
from settings_manager import SettingsManager
from base_manager import BaseServiceManager


class ServiceManager(BaseServiceManager):
    def __init__(self, app_name: str, svc_dir: str, config_file: str, sep: str = '/'):
        self.__app = app_name
        self.__lm = LogManager(app_name, svc_dir)
        self.log = self.__lm.get_log()  # Logging function
        self.__sm = SettingsManager(config_file, self.log, sep)
        self.set_log_level(int(self.get_value('Log')))

    def get_value(self, path: str):
        return self.__sm.get_value(f'{self.__app}/{path}')

    def set_value(self, path: str, value):
        self.__sm.set_value(f'{self.__app}/{path}', value)

    def del_value(self, path: str):
        self.__sm.del_value(f'{self.__app}/{path}')

    def load_settings(self):
        self.__sm.load_settings()

    def dump_settings(self):
        self.__sm.dump_settings()

    def log_settings(self):
        self.__sm.log_settings()

    def set_log_level(self, level: int):
        self.__lm.set_log_level(level)

    def join(self, *args) -> str:
        return self.__sm.join(*args)
