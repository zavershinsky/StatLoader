# -*- coding: utf-8 -*-
class StatResult:
    def __init__(self):
        self.__value = None

    def set(self, value):
        self.__value = value

    def get(self):
        return self.__value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return repr(self.__value)
