# coding=utf-8
'''
工具.
'''
from __future__ import absolute_import
import os
import pickle
import warnings
import time
import numpy as np
import pandas as pd
from collections import defaultdict
from itertools import combinations
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import log_loss
from hashlib import md5


warnings.filterwarnings('ignore')


def save(path='smileshy.pkl', obj=None):
    prefix = '/'.join(path.split('/')[: -1])
    if len(prefix) == 0:
        pass
    else:
        mkdir(prefix)
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
        f.close()
    print('保存%s完毕!' % path)


def load(path='smileshy.pkl'):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
        f.close()
    print('加载%s完毕!' % path)
    return obj


def mkdir(path='./path'):
    '''
    根据给定的路径创建目录.
    '''
    os.makedirs(path.encode('utf-8'), exist_ok=True)


def timer(func):
    '''
    计算时间的装饰器.
    '''

    def wraper(*args, **kwargs):
        start_time = time.time()
        print('=' * 40)
        print('%s开始执行' % func.__doc__)
        result = func(*args, **kwargs)
        end_time = time.time()
        time_long = end_time - start_time
        if time_long < 3600:
            print('%s执行完毕, 花费时间为: %f 分钟.' % (func.__name__, round(time_long / 60, 2)))
        else:
            print('%s执行完毕, 花费时间为: %f 小时.' % (func.__name__, round(time_long / 3600, 2)))
        print('=' * 40)
        return result
    return wraper


def random_num_generator(n=1000, random_state=777):
    '''
    随机数生成器, 范围0-1.
    '''
    np.random.seed(random_state)
    for i in range(n):
        yield np.random.rand()


def make_miss_value(df=None, label='target', row_perc=0.2, col_perc=0.8, random_state=7):
    '''
    随机将原数据中部分数据设置为NaN.
    '''
    ft_list = df.columns.tolist()
    if label in ft_list:
        ft_list.remove(label)
    np.random.seed(7)
    np.random.shuffle(ft_list)
    ft_miss_list = []
    for i in range(int(len(ft_list) * col_perc)):
        ft_miss_list.append(ft_list.pop())
    for i, ft in enumerate(ft_miss_list):
        rand_num = random_num_generator(n=df.shape[0], random_state=i)
        df[ft] = [np.nan if rand_num.__next__() < row_perc else x for x in df[ft]]


def split_X_y(df=None, label='target'):
    if label in df.columns.tolist():
        return df.drop(label, axis=1).reset_index(drop=True), df[label].values
    else:
        print('数据集中没有目标列.')


def rank_sort(data):
    len_data = len(data)
    sort_data = sorted(data)
    rank_data = list(range(1, len_data + 1))
    map_dict = defaultdict(float)
    count_dict = defaultdict(int)
    for i, d in enumerate(sort_data):
        map_dict[d] += rank_data[i]
        count_dict[d] += 1
    for k in count_dict:
        map_dict[k] /= count_dict[k]
    return [map_dict[x] for x in data]


def rank_sort_combine(data_list, weight=None):
    rank_data_list = []
    for data in data_list:
        rank_data_list.append(rank_sort(data))
    res = 0
    if weight is None:
        for data in rank_data_list:
            res = res + np.array(data)
        return res
    else:
        for i, data in enumerate(rank_data_list):
            res = res + np.array(data) * weight[i]
        return res


def traversal_search(data_list, n_range=(1, 2)):
    for n in n_range:
        for cb in combinations(data_list, n):
            yield list(cb)


def neg_log_loss(y_true, y_pred):
    weight = compute_sample_weight(class_weight='balanced', y=y_true)
    return -log_loss(y_true=y_true, y_pred=y_pred, sample_weight=weight)


def clean_float_data(data=None, data_type='df'):
    def clean_data(data):
        try:
            return float(data)
        except:
            return np.nan

    if data_type == 'df':
        for ft in data.columns.tolist():
            data[ft] = data[ft].apply(clean_data)
    elif data_type == 'list':
        data = map(clean_data, data)
    return data


def md5_encode(data):
    return md5(data.encode()).hexdigest()


def equal_frequency_bin(data, n_bins=10):
    '''
    等频分箱.
    返回分箱后的编码和边界.
    '''
    return pd.qcut(data, n_bins, labels=False, retbins=True, precision=8, duplicates='drop')


if __name__ == '__main__':
    a=['a','b','c', 'w']
    for i in traversal_search(a, (1, 2, 3, 4)):
        print(i)
    pass