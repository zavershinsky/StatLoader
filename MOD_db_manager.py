# -*- coding: utf-8 -*-
import os
ORACLE_HOME = 'C:\\oracle\\instantclient_19_10'
if ORACLE_HOME not in os.environ['PATH']:
    os.environ['PATH'] = f"{ORACLE_HOME};{os.environ['PATH']}"
os.environ['TNS_ADMIN'] = 'C:\\app\\client\\product\\12.1.0\\client_1\\network\\admin'
import cx_Oracle
from datetime import datetime
from dateutil.relativedelta import relativedelta
from stat_result import StatResult
from base_manager import DataManager


class DatabaseManager(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_db_manager.DatabaseManager'
    # yaml_tag = u'!DatabaseManager'
    # __connected = False

    def __init__(self, database: str, user: str, password: str, sql_metrics: list):
        self.database = database
        self.user = user
        self.password = password
        self.sql_metrics = sql_metrics

    def __str__(self):
        return f'{super(DatabaseManager, self).__str__()}({self.user}@{self.database})'

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        super(DatabaseManager, self).__del__()
        del self.database, self.user, self.password, self.sql_metrics

    def get_result(self, stat_result: StatResult) -> int:
        ret = 0
        try:
            _res = ''
            with cx_Oracle.connect(f'{self.user}/{self.password}@{self.database}') as conn:
                self._svc_manager.log(5, f'Service successfully connected to {self.database}')
                with conn.cursor() as cur:
                    for _sql in self.sql_metrics:
                        constructed_query = _sql.construct_query()
                        if 'select' in constructed_query.lower():
                            cur.execute(constructed_query)
                            self._svc_manager.log(5, f'SQL query "{constructed_query}" successfully executed')
                            ###
                            cur_res = ''
                            fields = next(cur)
                            for _field in fields:
                                if _field:
                                    cur_res = f'{cur_res}{_field}   '
                            ###
                            if not cur_res:
                                ret = 1
                                new_schedule = (datetime.now() + relativedelta(days=1)).strftime(self._svc_manager.get_value('ScheduleFormat'))
                                self._svc_manager.log(3, f'SQL cursor is empty. Next attempt will be on {new_schedule}')
                                self._svc_manager.set_value('Schedule', new_schedule)
                                self._svc_manager.dump_settings()
                                return ret
                            _res = f'{_res}{_sql.LABEL}: {cur_res.strip()}\n'
                        else:
                            _res = f'{_res}{_sql.LABEL}: {constructed_query}\n'
            stat_result.set(_res)
        except Exception as _exception:
            self._svc_manager.log(2, f'An error occurred while getting data: <{_exception.__class__.__name__}> {_exception}')
            ret = 1
        return ret

    # def connect(self):
    #     self.hide_attr('_DatabaseManager__connected')
    #     self.__connected = True
