# -*- coding: utf-8 -*-
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from service_manager import ServiceManager
from stat_result import StatResult


class InvStat:
    __svc_manager = None
    __data_generator = None
    __data_processor = None

    def __init__(self, global_dir: str, svc_name: str):
        self.__global_dir = global_dir
        self.__svc_name = svc_name
        self.__svc_dir = os.path.join(self.__global_dir, self.__svc_name)
        self.__config_file = os.path.join(self.__svc_dir, f'{self.__svc_name}.yml')
        self.__path = self.__svc_name
        self.__run = False

    def pause(self):
        self.__svc_manager.log(5, 'Service paused')

    def stop(self):
        self.__svc_manager.log(5, 'Stopping service')
        self.__svc_manager.dump_settings()

    def get_timeout(self) -> int:
        return self.__svc_manager.get_value('Timeout')

    def get(self, value):
        return self.__svc_manager.get_value(value)

    def __compute_schedule(self) -> bool:
        now = datetime.now()
        time_format = self.__svc_manager.get_value('ScheduleFormat')
        schedule = datetime.strptime(self.__svc_manager.get_value('Schedule'), time_format)
        res = now.year == schedule.year and now.month == schedule.month \
            and now.day == schedule.day and now.hour == schedule.hour
        if res:
            self.__svc_manager.set_value('Schedule', (now + relativedelta(months=1)).strftime(time_format))
            self.__svc_manager.dump_settings()
        return res

    def create_generator(self, svc_manager: ServiceManager):
        self.__data_generator = svc_manager.get_value('DataGenerator')
        self.__data_generator.initialize(svc_manager)

    def create_processor(self, svc_manager):
        self.__data_processor = svc_manager.get_value('DataProcessor')
        self.__data_processor.initialize(svc_manager)

    def start(self) -> (int, str):
        ret = 1
        try:
            self.__svc_manager = ServiceManager(self.__svc_name, self.__svc_dir, self.__config_file)
            ret = 0
        except Exception as _exception:
            return ret, f'<{_exception.__class__.__name__}> {_exception}'
        self.__svc_manager.log(5, 'Starting service')
        try:
            self.__run = self.__svc_manager.get_value('FirstRun')
        except Exception as _exception:
            self.__svc_manager.log(1, f'An error occurred while starting service: <{_exception.__class__.__name__}> {_exception}')
            ret = 1
        return ret, ''

    def work(self):
        self.__svc_manager.log(5, 'Start of working cycle')
        self.__svc_manager.load_settings()
        self.__svc_manager.set_log_level(self.__svc_manager.get_value('Log'))
        if self.__run or self.__compute_schedule():
            self.create_generator(self.__svc_manager)
            self.create_processor(self.__svc_manager)
            stat_result = StatResult()
            self.__svc_manager.log(4, f'Begin getting stat result by {self.__data_generator}')
            get_code = self.__data_generator.get_result(stat_result)
            # print(stat_result)
            self.__svc_manager.log(4, f'End getting stat result with status {get_code}')
            if get_code == 0:
                self.__svc_manager.log(4, f'Begin processing result by {self.__data_processor}')
                process_code = self.__data_processor.process(stat_result)
                # process_code = 0
                self.__svc_manager.log(4, f'End processing result with status {process_code}')
            self.__run = False
            # self.__svc_manager.log_settings()
        self.__svc_manager.log(5, 'End of working cycle')
