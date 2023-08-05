# coding=utf-8
'''
连接数据库脚本.
'''
import pymysql
import pymongo

import pandas as pd

class MySQLConnector:
    def __init__(self):
        self.mysql_engine = pymysql.connect(host='172.20.6.9',
                                            port=9030,
                                            user='fengkong_read_only',
                                            passwd='mT2HFUgI',
                                            db='risk_analysis',
                                            charset='utf8')
        pass


    def query(self, sql):
        try:
            return pd.read_sql(sql, self.mysql_engine)
        except:
            print('SQL查询出现错误.')
            return None



class MongoConnector:
    def __init__(self, mode='all'):
        # 审核+空跑
        if mode == 'all':
            table_name = 'wf_audit_log_with_feature'
        # 审核
        elif mode == 'online':
            table_name = 'wf_audit_log_with_feature_online'
        # 空跑
        elif mode == 'offline':
            table_name = 'wf_audit_log_with_feature_offline'
        else:
            print('警告, 模式设置错误.')

        self.mongo_client = pymongo.MongoClient(
            "mongodb://haoyue.shu:x2egwRHk7WhQ4So1@172.18.3.22:27017/?authSource=rc_mgo_feature_dp")
        self.mongo_db = self.mongo_client['rc_mgo_feature_dp']
        self.mongo_table = self.mongo_db[table_name]


    def query(self, condition, fields):
        try:
            return pd.DataFrame(list(self.mongo_table.find(condition, fields)))
        except:
            print('Mongo查询出现错误.')


if __name__ == '__main__':
    # MySQL查询.
    field_list = \
        '''
        'order_no', 'loan_id', 'user_id', 'uuid',
        'applied_from', 'applied_channel',
        'applied_at', 'deadline',  'passdue_day',
        'term_no', 
        'transacted', 
        'reloan_v3_point'
        '''
    field_list = field_list.replace('\n', ' ').replace('\'', ' ')
    mysql_con = MySQLConnector()
    mysql_df = mysql_con.query('SELECT %s \
                         FROM risk_analysis \
                         WHERE  transacted=1 \
                         AND applied_at >= "2019-05-10 00:00:00" \
                         AND applied_at <= "2019-07-10 00:00:00"' % field_list)


    # Mongo查询.
    # mongo_db中可能需要的字段。

    need_cols = {'order_id': 1,  # 订单号
                 'wf_loan_type': 1,  # 申请类型
                 'wf_created_at': 1,  # 申请时间
                 'wf_biz_channel': 1,  # 申请渠道号
                 'passdue_day': 1,  # 逾期时间
                 'user_uuid': 1,  # uuid
                 'lam_transaction_status': 1,  # 2和5表示放款成功.
                 'repayment_status': 1, # 不等于4表示放款成功.
                 'model_exec_data_source#fst_v6_xy_br_dhb_raw': 1,
                 'model_exec_data_source#fst_withoutoperator_v1': 1,
                 'model_exec_data_source#fst_v6_xy_br_dhb_tencent_contact_raw': 1,
                 'model_exec_data_source#reloan_v6_xy_tz_bj': 1,
                 'model_exec_data_source#reloan_xy_tz_bj': 1,
                 'model_exec_data_source#bairong_raw': 1,
                 'model_exec_data_source#bairong_v2_raw': 1,
                 'model_exec_data_source#dhb_score': 1,
                 'model_exec_data_source#dhb_v2': 1,
                 'model_exec_data_source#tanzhi_score': 1,
                 'lxf_score_scale_v2': 1,
                 'model_exec_data_source#reloan_v4_raw': 1,
                 'model_exec_data_source#xinyan_v2': 1,
                 'model_exec_data_source#xinyan_v3': 1,
                 'model_exec_data_source#moxie_raw': 1,
                 'model_exec_data_source#tongdun_v2': 1,
                 'model_exec_data_source#operator_score_raw': 1,
                 'tongdunScore': 1,
                 'third_data_source#qcaf_af_rscore': 1,
                 'third_data_source#bj_hawk_bj_score': 1
                 }
    mongo_con = MongoConnector(mode='all')
    condition = {'wf_created_at': {'$gte': '%s 00:00:00' % '2019-01-01',
                                   '$lte': '%s 00:00:00' % '2019-02-01'},
                 'passdue_day': {'$ne': None}}
    mongo_df = mongo_con.query(condition, need_cols)
    pass