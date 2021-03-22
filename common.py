# # -*- coding: utf-8 -*-
# import InvStat
# from datetime import datetime
# import time
#
#
# svc_dir = 'C:\\PyServices'
# svc_name = 'InvoiceStatistics'
# stat = InvStat.InvStat(svc_dir, svc_name)
# print(stat.start())
# print(datetime.strptime(stat.get('Schedule'), stat.get('ScheduleFormat')))
# # print(stat.get('DataGenerator'))
# # print(stat.get('DataProcessor'))
# # print(stat.get('Schedule'))
# # print(stat.get('FirstRun'))
# try:
#     while True:
#         stat.work()
#         time.sleep(stat.get_timeout()/1000.0)
# except KeyboardInterrupt:
#     stat.stop()
###############################################################################
# from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox
# from exchangelib.configuration import Configuration
#
#
# _creds = Credentials(
#     username='BERCUT\\zavershinskiy-m',
#     password='17MaxizavR0202'
# )
# _config = Configuration(
#     credentials=_creds,
#     server='sync.bercut.com'
# )
# _account = Account(
#     primary_smtp_address='noreply@bercut.com',
#     config=_config,
#     access_type=DELEGATE
# )
#
# m = Message(
#     account=_account,
#     subject='IN@Voice Statistics',
#     body='Some SQL results for you',
#     to_recipients=[Mailbox(email_address='maksim.zavershinskiy@bercut.com')]
# )
# m.send_and_save()
###############################################################################
# import sys
# from yaml import load, dump
# from yaml import Loader, Dumper
# __import__('db_manager')
# o = load("""!DatabaseManager
# database: BERCUT
# user: smaster
# password: smaster
# sql_metrics: []""", Loader)
# print(o)
# dump(o, sys.stdout, Dumper)
###############################################################################
# import os
#
# for _file in os.listdir(os.path.dirname(__file__)):
#     _mod = os.path.splitext(_file)[0]
#     if _mod.startswith('MOD_'):
#         # __import__(_mod)
#         print(_mod)
###############################################################################
# import cx_Oracle
# import os
# import sys
# os.environ['PATH'] = 'C:\\oracle\\instantclient_19_10;%s' % os.environ['PATH']
# sys.path.insert(0, 'C:\\oracle\\instantclient_19_10')
# os.environ['TNS_ADMIN'] = 'C:\\app\client\product\\12.1.0\\client_1\\network\\admin'
# SQL = 'select /*+parallel(ic,4) parallel(ch,4)*/ to_char(sum(ic.summ_charge_$)), ' \
#       'to_char(sum(ic.summ_charge_$)-round(sum(ic.summ_charge_$)/1.2,2)) ' \
#       'from itog_client ic join client_history ch on ch.clnt_id=ic.clnt_id ' \
#       'and ic.edate between ch.stime and ch.etime-1/86400 and ct_id not in (-1,0,3,4,2,6,7,8,9,11,12) ' \
#       'where trunc(ic.edate, \'mm\')=trunc(add_months(sysdate, -1), \'mm\')'
#
# with cx_Oracle.connect('smaster/smaster@WMDB_BERCUT') as conn:
#     with conn.cursor() as cur:
#         cur.execute(SQL)
#         cur_res = ''
#         fields = next(cur)
#         for _field in fields:
#             cur_res = f'{cur_res}{_field}   '
#         print(cur_res)
###############################################################################
# import os
#
#
# list(map(print, (f'{k} = {os.environ[k]}' for k in os.environ)))
###############################################################################
# import os
# import cx_Oracle
#
#
# ORACLE_HOME = 'C:\\oracle\\instantclient_19_10'
# cx_Oracle.init_oracle_client(ORACLE_HOME)
# if ORACLE_HOME not in os.environ['PATH']:
#     os.environ['PATH'] = f"{ORACLE_HOME};{os.environ['PATH']}"
# print(cx_Oracle.clientversion())
# print(os.environ['PATH'])
###############################################################################
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class WholeIntervalRotatingFileHandler(TimedRotatingFileHandler):
    def computeRollover(self, currentTime):
        if self.when[0] == 'W' or self.when == 'MIDNIGHT':
            # use existing computation
            return super().computeRollover(currentTime)
        # round time up to nearest next multiple of the interval
        return ((currentTime // self.interval) + 1) * self.interval


print(datetime.now())   # current time
handler = WholeIntervalRotatingFileHandler('C:\\maxizavr\\logfile.log', 'M', 1,)
print(datetime.fromtimestamp(handler.rolloverAt))
