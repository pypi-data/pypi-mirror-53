# coding=utf-8
'''
暴力特征衍生.
根据给定的特征对象在原始数据中计算特征.
'''

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import featuretools

import warnings
warnings.filterwarnings('ignore')
from .base_utils import mkdir, save, timer, load

class SimpleFeatureGenerator:
    def __init__(self, gap_fill=''):
        self.gap_fill = gap_fill
        self.ft_obj_dict = {}
        self.trans_map_dict = {'*': 'multiply_numeric',
                               '/': 'divide_numeric',
                               '+': 'add_numeric',
                               '-': 'subtract_numeric'}
        self.agg_map_dict = {'max': 'max',
                             'min': 'min'}

    @timer
    def numerical_generate(self, df=None, label='target',
                           trans_types=('/', '*'),
                           agg_type=('min', 'max')):
        '''
        对数值型特征进行衍生.
        '''
        if label in df.columns.tolist():
            del df[label]
        trans_type_list = [self.trans_map_dict[x] if x in self.trans_map_dict else x for x in trans_types]
        agg_type_list = [self.agg_map_dict[x] if x in self.agg_map_dict else x for x in agg_type]
        es = featuretools.EntitySet(id='full_data')
        es.entity_from_dataframe(entity_id='data', dataframe=df,
                                 index='idx', make_index=True)
        ft_df, ft_name = featuretools.dfs(entityset=es, target_entity='data',
                                          trans_primitives=trans_type_list,
                                          agg_primitives=agg_type_list,
                                          max_depth=1,
                                          n_jobs=4)
        ft_df.columns = [self.gap_fill.join(x.split(' ')) for x in ft_df.columns]
        self.ft_obj_dict = dict(zip(ft_df.columns.tolist(), ft_name))

        return ft_df

    @timer
    def feature_generate(self, df=None, ft_list=None, label='target'):
        '''
        给定衍生后的特征, 从原始数据中进行计算.
        '''
        # 确定要原始数据集, 以及要计算的特征.
        if label in df.columns.tolist():
            del df[label]
        ft_obj_list = []
        for ft in ft_list:
            ft_obj_list.append(self.ft_obj_dict[ft])
        # 计算特征.
        es = featuretools.EntitySet(id='full_data')
        es.entity_from_dataframe(entity_id='data', dataframe=df,
                                 index='idx', make_index=True)
        ft_df = featuretools.calculate_feature_matrix(features=ft_obj_list,
                                                      entityset=es,
                                                      n_jobs=4)
        return ft_df

    def save(self, save_path='./model/ft_generator.obj'):
        save(save_path, self)
        print(save_path + ' 保存成功.')


class TimeFeatureGenerator:
    def __init__(self):

        pass

    def hour_generate(self, df=None, time_field='time',
                      time_interval=1,
                      time_fmt='%Y-%m-%d %H:%M:%S'):
        # 转换时间格式.
        time_data = df[time_field].copy()
        try:
            time_data = time_data.apply(lambda x: datetime.strptime(x, time_fmt))
        except:
            pass
        # 制作编码字典.
        time_delta = timedelta(hours=time_interval)
        start_time = datetime.strptime('00:00:00', '%H:%M:%S')
        end_time = datetime.strptime('23:59:59', '%H:%M:%S')
        time_interval_list = []
        for i in range(int(24 / time_interval) - 1):
            time_interval_list.append((start_time, start_time + time_delta))
            start_time = start_time + time_delta
        time_interval_list.append((start_time, end_time))
        # 按小时编码.
        time_encode = []
        for t in time_data:
            if pd.isnull(t):
                time_encode.append(np.nan)
                continue
            for i, t_interval in enumerate(time_interval_list):
                if t.time() >= t_interval[0].time() and t.time() < t_interval[1].time():
                    time_encode.append(str(i))
                    break
        df['hour_encode_' + str(time_interval)] = time_encode
        print(df['hour_encode_' + str(time_interval)].value_counts())
        return df

    def week_genetare(self):

        pass







if __name__ == '__main__':
    # from sklearn.datasets import load_breast_cancer
    #
    # data, target = load_breast_cancer(return_X_y=True)
    # df = pd.DataFrame(data, columns=[str(x) for x in range(data.shape[1])])
    # df['target'] = target
    # train, test = train_test_split(df, random_state=777, stratify=df['TARGET'], test_size=0.2)
    # train = train.reset_index(drop=True)
    # test = test.reset_index(drop=True)

    df = pd.DataFrame({'a':[1,2,3],
                       'b':[2,3,4],
                       'c':[4,5,6]})
    fg = SimpleFeatureGenerator()
    c = df['c'].tolist()
    df = fg.numerical_generate(df=df, label='c')
    print(df)
    df['c'] = c
    print(df)
