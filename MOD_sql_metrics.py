# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_TIME, 'ru')
from base_manager import DataManager


class SQLMetric1(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_sql_metrics.SQLMetric1'
    # yaml_tag = '!SQLMetric1'
    LABEL = ''
    QUERY = 'select /*+parallel(ic,4) parallel(ch,4)*/ to_char(sum(ic.summ_charge_$)), ' \
            'to_char(sum(ic.summ_charge_$)-round(sum(ic.summ_charge_$)/1.2,2)) ' \
            'from itog_client ic join client_history ch on ch.clnt_id=ic.clnt_id ' \
            'and ic.edate between ch.stime and ch.etime-1/86400 and ct_id not in (-1,0,3,4,2,6,7,8,9,11,12) ' \
            'where trunc(ic.edate, \'mm\')=trunc(add_months(sysdate, -{months}), \'mm\')'

    def construct_query(self) -> str:
        self.hide_attr('LABEL')
        self.hide_attr('QUERY')
        mon_qty = 1
        self.LABEL = datetime.strftime(datetime.now()-relativedelta(months=mon_qty), '%B %Y')
        return self.QUERY.format(months=mon_qty)


class SQLMetric2(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_sql_metrics.SQLMetric2'
    # yaml_tag = '!SQLMetric2'
    LABEL = 'Активные абоненты'
    QUERY = 'select \'%s\' from dual'

    def construct_query(self) -> str:
        self.hide_attr('QUERY')
        return self.QUERY % datetime.now()


class SQLMetric3(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_sql_metrics.SQLMetric3'
    # yaml_tag = '!SQLMetric3'
    LABEL = 'Активные абоненты'
    QUERY = 'select \'%s\' from dual'

    def construct_query(self) -> str:
        self.hide_attr('QUERY')
        return self.QUERY % datetime.now()


class SQLMetric4(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_sql_metrics.SQLMetric4'
    # yaml_tag = '!SQLMetric4'
    LABEL = 'Статистика актуальна на'
    QUERY = datetime.strftime(datetime.now()-relativedelta(months=1), '%B %Y')

    def construct_query(self) -> str:
        self.hide_attr('QUERY')
        return self.QUERY
