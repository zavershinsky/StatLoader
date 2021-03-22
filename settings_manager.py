# -*- coding: utf-8 -*-
from os.path import abspath, dirname, splitext
from os import listdir
import sys
from yaml import load, dump
from yaml import Loader, Dumper


class SettingsManager:

    class VariableNotFoundError(Exception):
        pass

    def __init__(self, config_file: str, log, sep: str = '/'):
        self.__config_file = config_file
        self.__log = log
        self.__separator = sep
        self._settings = {}
        self.load_settings()

    def get_value(self, path: str):
        try:
            return eval(f'self._settings{self.__correct_path(path)}')
        except(TypeError, KeyError):
            raise self.VariableNotFoundError(f'Variable or Group not found by path {path}')

    def set_value(self, path: str, value):
        if isinstance(value, str):
            exec(f'self._settings{self.__correct_path(path)} = \'{value}\'')
        else:
            exec(f'self._settings{self.__correct_path(path)} = {value}')

    def del_value(self, path: str):
        exec(f'del self._settings{self.__correct_path(path)}')

    def load_settings(self):
        for _file in listdir(dirname(__file__)):
            _mod = splitext(_file)[0]
            if _mod.startswith('MOD_'):
                if _mod in sys.modules:
                    del sys.modules[_mod]
                __import__(_mod)
        with open(self.__config_file, 'r') as f:
            self._settings = load(f, Loader=Loader)

    def dump_settings(self):
        with open(self.__config_file, 'w') as f:
            dump(self._settings, f, Dumper=Dumper, default_flow_style=False,
                 allow_unicode=True, indent=4, default_style='"')
        self.log(5, f'Settings dumped to {abspath(self.__config_file)}')

    def log_settings(self):
        self.log(5, f'Current settings: {self._settings}')

    def log(self, level: int, msg: str):
        self.__log(level, f'{self.__class__.__name__} - {msg}')

    def __correct_path(self, path: str):
        return '["' + '"]["'.join(list(filter(None, path.split(self.__separator)))) + '"]'

    def join(self, *args) -> str:
        return self.__separator.join(args)
