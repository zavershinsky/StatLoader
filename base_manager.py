# -*- coding: utf-8 -*-
from yaml import YAMLObject
from copy import deepcopy


class BaseServiceManager:
    def get_value(self, path: str):
        raise NotImplementedError

    def set_value(self, path: str, value):
        raise NotImplementedError

    def del_value(self, path: str):
        raise NotImplementedError

    def log(self, level: int, msg: str):
        pass

    def set_log_level(self, level: int):
        raise NotImplementedError


class DataManager(YAMLObject):
    _svc_manager = BaseServiceManager()
    _hidden = {'_svc_manager'}

    @classmethod
    def to_yaml(cls, dumper, data):
        new_data = deepcopy(data)
        for item in cls._hidden:
            if item in new_data.__dict__:
                del new_data.__dict__[item]
        return dumper.represent_yaml_object(cls.yaml_tag, new_data, cls,
                                            flow_style=cls.yaml_flow_style)

    def __str__(self):
        return f'{self.__module__}.{self.__class__.__name__}'

    def construct_query(self) -> str:
        raise NotImplementedError

    def hide_attr(self, attr: str):
        self._hidden.add(attr)

    def initialize(self, svc_manager):
        self._svc_manager = svc_manager
