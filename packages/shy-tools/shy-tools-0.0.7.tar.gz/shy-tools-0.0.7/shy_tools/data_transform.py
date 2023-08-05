# coding=utf-8
'''
- 数据预处理类.
- 其中大部分处理方式是已经被封装好的, 直接使用.
- 若要反复使用, 利用save(path='../transformer/...', obj=...)保存.
- 少部分处理方式自己根据需求实现.
- 可用转换器:
    1. Normalizer
        nmtf = Normalizer(norm='l2', copy=True)

    2. StandardScaler
        stdtf = StandardScaler(copy=True, with_mean=True, with_std=True)

    3. RobustScaler
        rbtf = RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25.0, 75.0), copy=True)

    4. PowerTransformer
        ptf = PowerTransformer(method=’yeo-johnson’, standardize=True, copy=True)

    5. QuantileTransformer
        qttf = QuantileTransformer(n_quantiles=1000, output_distribution=’uniform’, random_state=None, copy=True)

    6. CatMeanEncoder
        cmecd = CatMeanEncoder(cat_ft_list=None, label=None)

    7. MissingValueImputer
        msvi = MissingValueImputer(missing_values=np.nan, strategy='constant',
            fill_value=None, verbose=0, model_type='gbdt', miss_perc_range=(0, 1))

'''

from __future__ import absolute_import
import numpy as np
import pandas as pd
from scipy.stats import binom
from collections import OrderedDict

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer
from sklearn.impute._iterative import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, PowerTransformer, MinMaxScaler

from .base_utils import save

import warnings

warnings.filterwarnings('ignore')


class MissingValueImputerWithTarget:
    '''
    缺失值填充, 主要用于生产环境融合模型.
    '''
    def __init__(self, min_miss_num=100, is_indicate=True, mode='mean'):
        self.is_indicate = is_indicate
        self.ft_list = None
        self.min_miss_num = min_miss_num
        if mode not in ('left', 'right', 'mean'):
            print('模式设定不正确, 目前只支持: left, right, mean')
        self.mode = mode
        self.map_dict = OrderedDict()
        self.miss_ft_set = set()

    def fit(self, X=None, y=None):
        self.ft_list = X.columns.tolist()
        for ft in self.ft_list:
            # 若缺失数量少, 则补中位数.
            miss_num = X[ft].isnull().sum()
            if miss_num > 0:
                self.miss_ft_set.add(ft)
            if miss_num < self.min_miss_num:
                self.map_dict[ft] = X[ft].median()
                continue
            # 若缺失样本多, 则根据分箱后的信息进行填充.
            df_copy = X[[ft]].copy()
            df_copy['target'] = y
            df_copy_miss = df_copy[df_copy[ft].isnull()]
            df_copy_notna = df_copy[df_copy[ft].notna()]
            # 计算缺失部分的逾期率.
            miss_overdue_rate = df_copy_miss['target'].mean()
            # 对非缺失进行分箱, 得到每箱的缺失率.
            df_copy_notna['bin'] = pd.qcut(df_copy_notna['target'], 10, precision=8, duplicates='drop')
            df_copy_notna_g = df_copy_notna.groupby('bin').agg(overdue_mean=('target', 'mean'))
            df_copy_notna_g.reset_index(inplace=True)
            # 找到与缺失值数据最接近的分箱, 根据预设模式选择填充值.
            df_copy_notna_g['abs_sub'] = df_copy_notna_g['overdue_mean'].apply(lambda x: abs(x - miss_overdue_rate))
            min_abs_sub = min(df_copy_notna_g['abs_sub'].values)
            interval = df_copy_notna_g.loc[df_copy_notna_g['abs_sub'] == min_abs_sub, 'bin'].values[0]
            if self.mode == 'left':
                self.map_dict[ft] = interval.left
            elif self.mode == 'right':
                self.map_dict[ft] = interval.right
            else:
                self.map_dict[ft] = (interval.right + interval.left) / 2

        return self

    def transform(self, X=None):
        for ft in self.map_dict:
            if ft in self.miss_ft_set and self.is_indicate:
                X[ft + '_indicate'] = X[ft].apply(lambda x: int(pd.isnull(x)))
            X[ft] = X[ft].fillna(self.map_dict[ft])
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)

    def save(self, name='miss.imputer'):
        save(path='./transformer/' + name, obj=self)
        print('成功保存.')


class StandardTransformer:
    def __init__(self):
        self.std_scl = StandardScaler()
        self.ft_list = None

    def fit(self, X=None, y=None):
        self.ft_list = X.columns.tolist()
        self.std_scl.fit(X=X)
        return self

    def transform(self, X=None):
        X_copy = self.std_scl.transform(X=X[self.ft_list])
        X_copy = pd.DataFrame(X_copy, columns=self.ft_list)
        return X_copy

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)

    def save(self, name='std.transformer'):
        save(path='./transformer/' + name, obj=self)
        print('成功保存.')


class MissingValueImputer:
    '''
    对scikit-learn的缺失值填充器的封装.
    根据自己对缺失值填充的常用需求以及理解进行改进.
    '''

    def __init__(self,missing_values=np.nan, strategy='constant',
                 fill_value=None, verbose=0, initial_strategy='median'):
        self.missing_values = missing_values
        self.strategy = strategy
        self.fill_value = fill_value
        self.initial_strategy = initial_strategy
        if strategy not in ('constant', 'mean', 'median', 'predict'):
            print('亲亲您的填充方法没有输入对呢, 这边只支持如下方法嗷~\n'
                  '1. constant\n'
                  '2. mean\n'
                  '3. median\n'
                  '4. predict')
        # 初始化填充器.
        if self.strategy != 'predict':
            self.tf = SimpleImputer(strategy=self.strategy, fill_value=self.fill_value, copy=True,
                                    add_indicator=True, verbose=verbose)
        elif self.strategy == 'predict':
            self.model = RandomForestRegressor(random_state=777, max_depth=4, max_features='sqrt')
            self.tf = IterativeImputer(estimator=self.model, initial_strategy=initial_strategy,
                                       imputation_order='ascending',
                                       random_state=777, add_indicator=True, verbose=verbose)
        self.ft_list = None
        self.ft_miss_list = None

    def fit(self, X=None, y=None):
        X.replace(to_replace=self.missing_values, value=np.nan, inplace=True)
        self.ft_list = X.columns.tolist()
        ft_miss_perc = X.isnull().mean(axis=0)
        self.ft_miss_list = ft_miss_perc[ft_miss_perc > 0].index.tolist()
        if self.strategy == 'predict':
            n_ft = len(self.ft_list)
            self.model.set_params(n_estimators=int(100 * (n_ft / (np.sqrt(n_ft) * self.model.max_depth))))
            self.tf.set_params(estimator=self.model)
        self.tf.fit(X=X)
        print('填充缺失值训练完毕.')
        return self

    def transform(self, X=None):
        X.replace(to_replace=self.missing_values, value=np.nan, inplace=True)
        copy_df = self.tf.transform(X[self.ft_list])
        indicat_col = [col + '_indicat' for col in self.ft_miss_list]
        copy_df = pd.DataFrame(copy_df, columns=self.ft_list + indicat_col)
        for col in copy_df:
            X[col] = copy_df[col]
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        print('缺失值训练填充完毕.')
        return self.transform(X=X)

    def save(self, name='miss_val.imputer'):
        save(path='./transformer/' + name, obj=self)
        print('成功保存.')


class BoxCoxTransformer:
    def __init__(self, boxcox_mode='yeo-johnson'):
        self.minmax = MinMaxScaler(feature_range=(2, 3))
        self.boxcox = PowerTransformer(method=boxcox_mode, standardize=False)
        self.ft_list = None

    def fit(self, X=None, y=None):
        # 记录特征名称.
        self.ft_list = X.columns.tolist()

        # 进行minmax.
        X = self.minmax.fit_transform(X)
        X = pd.DataFrame(X, columns=self.ft_list)

        # boxcox拟合.
        self.boxcox.fit(X, y)
        return self

    def transform(self, X=None):
        # 预处理.
        X = X[self.ft_list]
        X = self.minmax.transform(X)
        X = pd.DataFrame(X, columns=self.ft_list)
        # boxcox变换.
        X = self.boxcox.transform(X)
        X = pd.DataFrame(X, columns=self.ft_list)
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)

    def save(self, name='boxcox.transformer'):
        save(path='./transformer/' + name, obj=self)
        print('boxcox.transformer成功保存.')


class LinearModelPreprocessor:
    def __init__(self,
                 is_boxcox=True,
                 boxcox_mode='yeo-johnson',
                 is_std=True,
                 is_miss_impute=True,
                 min_miss_num=100,
                 miss_mode='mean',
                 is_indicate=True):
        self.is_boxcox = is_boxcox
        self.is_std = is_std
        self.is_miss_impute = is_miss_impute

        if self.is_boxcox:
            self.boxcox = BoxCoxTransformer(boxcox_mode=boxcox_mode)
        if self.is_std:
            self.std = StandardTransformer()
        if is_miss_impute:
            self.miss_impute = MissingValueImputerWithTarget(min_miss_num=min_miss_num,
                                                             mode=miss_mode,
                                                             is_indicate=is_indicate)
        self.ft_list = None

    def fit(self, X=None, y=None):
        self.ft_list = X.columns.tolist()
        if self.is_boxcox:
            X = self.boxcox.fit_transform(X)
        if self.is_std:
            X = self.std.fit_transform(X)
        if self.is_miss_impute:
            self.miss_impute.fit(X, y)
        return self

    def transform(self, X=None):
        X = X[self.ft_list]
        if self.is_boxcox:
            X = self.boxcox.transform(X)
        if self.is_std:
            X = self.std.transform(X)
        if self.is_miss_impute:
            X = self.miss_impute.transform(X)
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)

    def save(self, name='lilear.preprocessor'):
        save(path='./transformer/' + name, obj=self)
        print('成功保存.')


class CategoryMeanEncoder:
    def __init__(self, cat_ft_list=None, alpha_perc=0.1, n_splits=5):
        self.alpha_perc = alpha_perc
        self.cat_ft_list = cat_ft_list
        self.n_splits = n_splits
        self.skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=777)
        self.ft_attr_encode_dict = {}
        self.global_mean = None
        self.alpha = None

    def fit(self, X=None, y=None):
        self.ft_attr_encode_dict = {}
        self.global_mean = y.mean()
        self.alpha = self.alpha_perc * X.shape[0] * (1 - 1 / self.n_splits)
        cat_ft_list = X.select_dtypes('object').columns.tolist()
        if self.cat_ft_list is None:
            self.cat_ft_list = cat_ft_list
        else:
            for ft in cat_ft_list:
                if ft not in self.cat_ft_list:
                    self.cat_ft_list.append(ft)

        for ft in self.cat_ft_list:
            tmp_list = []
            for train_idx, _ in self.skf.split(X, y):
                train = X.loc[train_idx]
                tmp_df = train[[ft]].copy()
                tmp_df['target'] = y
                tmp_df_g = tmp_df.groupby(ft).agg(mean=('target', 'mean'),
                                                  count=('target', 'count'))

                tmp_df_g['mean_smooth'] = tmp_df_g.apply(lambda x:
                                                         (x['mean'] * x['count'] + self.global_mean * self.alpha) /
                                                         (x['count'] + self.alpha), axis=1)
                tmp_list.append(tmp_df_g[['mean_smooth']])
            attr_mean_df = pd.concat(tmp_list, axis=1, join='outer')
            attr_mean_df = attr_mean_df.fillna(self.global_mean)
            attr_mean_df['result'] = attr_mean_df.values.sum(axis=1)
            self.ft_attr_encode_dict[ft] = dict(zip(attr_mean_df.index.values, attr_mean_df['result'].values))
        print('均值编码训练完毕.')
        return self

    def transform(self, X=None):
        for ft in self.cat_ft_list:
            X[ft] = X[ft].map(self.ft_attr_encode_dict[ft])
        print('均值编码转换完毕.')
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)


    def save(self, name='bys_cat_mean_encoder.pkl'):
        save(path='../transformer/' + name, obj=self)
        print('成功保存.')


class CategoryPreprocessor:
    '''
    主要针对类别特征高基数, 或者存在某属性数量极少的情况, 进行预处理.
    不管缺失值, 等到缺失值填充步骤处理.
    利用二项分布找出显著的属性, 先保持不动.
    设定最小占比阈值, 尝试将小于该阈值的且不显著属性随机进行合并.
    若合并后还剩余小于阈值的, 则将其与另外不显著的最大属性合并.
    若没有, 和显著的最大属性合并.
    检查是否单值, 是则删除该特征.
    '''
    def __init__(self,
                 min_perc=0.05,
                 p_value=0.0001,
                 cat_ft_list=None,
                 label='target'):

        self.min_perc = min_perc
        self.p_value = p_value
        self.cat_ft_list = cat_ft_list
        self.label = label
        self.ft_attr_map_dict = {}


    def fit(self, X=None):
        np.random.seed(777)
        # 收集需要预处理的类别特征.
        if self.cat_ft_list is None:
            self.cat_ft_list = X.select_dtypes('object').columns.tolist()
        else:
            for col in X.select_dtypes('object').columns.tolist():
                if col not in self.cat_ft_list:
                    self.cat_ft_list.append(col)
        # 根据二项分布过滤出显著属性.
        len_X = X.shape[0]
        min_num_in_attr = len_X * self.min_perc
        global_mean = X[self.label].mean()

        def is_significant(data, count):
            if data > binom.ppf(1 - self.p_value, count, global_mean):
                return True
            elif data < binom.ppf(self.p_value, count, global_mean):
                return True
            else:
                return False
        def comb(attr_list, info_df, min_num):
            np.random.shuffle(attr_list)
            bin_list = []
            # 遍历.
            for i in range(len(attr_list)):
                attr = attr_list.pop()
                if len(bin_list) == 0 or bin_list[-1][1] > min_num:
                    bin_list.append([[attr], info_df.loc[attr, 'count_']])
                else:
                    bin_list[-1][0].append(attr)
                    bin_list[-1][1] += info_df.loc[attr, 'count_']
            # 检查.
            if len(bin_list) == 1 and bin_list[0][1] < min_num_in_attr:
                return bin_list, False
            elif len(bin_list) == 1 and bin_list[0][1] >= min_num_in_attr:
                return bin_list, True
            elif bin_list[-1][1] < min_num:
                attr_info = bin_list.pop()
                bin_list[-1][0] = bin_list[-1][0] + attr_info[0]
                bin_list[-1][1] += attr_info[1]
                return bin_list, True
            else:
                return bin_list, True

        for ft in self.cat_ft_list:
            tmp_df = X[[ft, self.label]].copy()
            tmp_df_g = tmp_df.groupby(ft).agg(count_=(self.label, 'count'),
                                              sum_=(self.label, 'sum'))
            tmp_df_g['is_significant'] = tmp_df_g.apply(lambda x: is_significant(x['sum_'], x['count_']), axis=1)
            main_attr = [x for x, y in zip(tmp_df_g.index, tmp_df_g['is_significant']) if y is True]
            not_main_attr = [x for x, y in zip(tmp_df_g.index, tmp_df_g['is_significant']) if y is False]
            # 对不显著, 且数量小于阈值的属性进行合并.
            not_main_small_attr = [x for x in not_main_attr if tmp_df_g.loc[x, 'count_'] < min_num_in_attr]
            not_main_big_attr = [x for x in not_main_attr if tmp_df_g.loc[x, 'count_'] >= min_num_in_attr]
            bin_list = None
            if not_main_small_attr:
                bin_list, is_good = comb(not_main_small_attr, tmp_df_g, min_num_in_attr)
                # 与不显著中最大的属性合并.
                if not is_good:
                    bigest_attr = None
                    bigest_num = 0
                    if len(not_main_big_attr) != 0:
                        for attr in not_main_big_attr:
                            if tmp_df_g.loc[attr, 'count_'] > bigest_num:
                                bigest_num = tmp_df_g.loc[attr, 'count_']
                                bigest_attr = attr
                        not_main_big_attr.remove(bigest_attr)
                        bin_list[-1][0].append(bigest_attr)
                    # 与显著属性中最大的合并.
                    else:
                        for attr in main_attr:
                            if tmp_df_g.loc[attr, 'count_'] > bigest_num:
                                bigest_num = tmp_df_g.loc[attr, 'count_']
                                bigest_attr = attr
                        main_attr.remove(bigest_attr)
                        bin_list[-1][0].append(bigest_attr)
            # 构建映射字典.
            self.ft_attr_map_dict[ft] = {}
            for attr in main_attr:
                self.ft_attr_map_dict[ft][attr] = attr
            for attr in not_main_big_attr:
                self.ft_attr_map_dict[ft][attr] = attr
            if bin_list is not None:
                for attr_list, _ in bin_list:
                    for attr in attr_list:
                        attr_name = ''.join(attr_list)
                        self.ft_attr_map_dict[ft][attr] = attr_name
        return self

    def transform(self, X=None):
        # 根据字典进行映射.
        for ft in self.ft_attr_map_dict:
            X[ft] = X[ft].map(self.ft_attr_map_dict[ft])
            # 转换为0-1特征.
            if X[ft].nunique(dropna=False) == 2:
                unique_tuple = X[ft].unique()
                map_dict = {unique_tuple[0]: 0, unique_tuple[1]: 1}
                X[ft] = X[ft].map(map_dict)
            if X[ft].nunique(dropna=False) == 1:
                del X[ft]
        return X

    def fit_transform(self, X=None):
        self.fit(X=X)
        return self.transform(X=X)



if __name__ == '__main__':

    from param_optimize import LightBayesOptimizer
    from sklearn.metrics import roc_auc_score
    train = pd.read_csv('./data/hr_train.csv')
    test = pd.read_csv('./data/hr_test.csv')
    me = CategoryMeanEncoder(label='target')
    train = me.fit_transform(train)
    test = me.transform(test)

    po = LightBayesOptimizer(df=train, label='target')
    po.run()
    po.fit_model()

    print(roc_auc_score(train['target'], po.predict(train)))
    print(roc_auc_score(test['target'], po.predict(test)))


    pass
'''
bc miss
lr
0
0.9955830753353974
0.9914021164021163
mean
0.9962641898864809
0.9914021164021165
median
0.9961197110423117
0.9904100529100529

lgb
miss
0.9997729618163054
0.9976851851851852
0 lr
0.999938080495356
0.9976851851851851
mean lr
0.9992569659442725
0.9993386243386243
median lr
0.9999793601651187
0.9986772486772486
predict mean gbdt
0.9998348813209493
0.9993386243386243
predict mean lr
0.9994840041279669
0.9996693121693121
'''
