# coding=utf-8
'''
lightgbm二分类问题的建模, 贝叶斯优化.
'''

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression

import lightgbm as lgb

from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs

from shy_tools.base_utils import save, timer, neg_log_loss, split_X_y, load
from shy_tools.data_visualization import Echart

import os
import warnings

warnings.filterwarnings('ignore')

# TODO
# 对逻辑回归调参添加随机/贝叶斯模式.

class CVStabilityEvaluator:
    '''
    CV稳定性验证.
    '''

    def __init__(self, train=None, test=None, label='target',
                 nfold=7, n_iter=50, save_path='./image/',
                 test_eval_metric='logloss', is_rank_corr_plot=False,
                 fig_title='1', plot_mode='html'):
        self.train = train
        self.test = test
        self.label = label
        self.nfold = nfold
        self.n_iter = n_iter
        self.test_eval_metric = test_eval_metric
        self.is_rank_corr_plot = is_rank_corr_plot
        self.fig_title = fig_title
        self.echart = Echart(mode=plot_mode)
        self.mean_list = []
        self.std_list = []
        self.test_result = []
        self.rank_corr_list = []
        self.params = {'objective': 'binary',
                       'num_tree': 1000,
                       'learning_rate': 0.05,
                       'max_depth': -1,
                       'num_leaf': 8,
                       'bagging_freq': 1,
                       'bagging_fraction': 0.6,
                       'feature_fraction': 0.4,
                       'min_data_in_leaf': 3,
                       'min_sum_hessian_in_leaf': 0.005,
                       'lambda_l1': 0.,
                       'lambda_l2': 0.,
                       'min_split_gain': 0.,
                       # 'is_unbalance': True,
                       'metrics': 'binary_logloss',
                       'seed': 7,
                       'num_thread': 4,
                       'verbose': -1
                       }
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.mkdir(save_path)

    def random_set_params(self, seed=7):
        np.random.seed(seed)
        self.params['num_leaf'] = np.random.randint(2, 16, 1)[0]
        self.params['bagging_fraction'] = np.random.rand(1)[0]
        self.params['feature_fraction'] = np.random.rand(1)[0]
        self.params['min_data_in_leaf'] = np.random.randint(2, 50, 1)[0]
        self.params['min_sum_hessian_in_leaf'] = np.random.rand(1)[0] * 0.01
        self.params['lambda_l1'] = np.random.rand(1)[0] * 0.01
        self.params['lambda_l2'] = np.random.rand(1)[0] * 0.01

    @timer
    def run(self):
        '''CV稳定性测试 '''
        # 划分数据.
        if self.test is None:
            train, test = train_test_split(self.train, test_size=0.3, random_state=7, stratify=self.train[self.label])
            train_X, train_y = split_X_y(df=train, label=self.label)
            test_X, test_y = split_X_y(df=test, label=self.label)
        else:
            train_X, train_y = split_X_y(df=self.train, label=self.label)
            test_X, test_y = split_X_y(df=self.test, label=self.label)
        # 一阶段得到不同超参数下的CV均值和标准差.
        weight = compute_sample_weight(class_weight='balanced', y=train_y)
        train = lgb.Dataset(data=train_X, label=train_y, free_raw_data=False, weight=weight)
        for n in range(self.n_iter):
            print('第%d轮CV...' % (n + 1))
            self.random_set_params(seed=n)
            cv_result = lgb.cv(params=self.params, train_set=train, nfold=self.nfold,
                               early_stopping_rounds=30, verbose_eval=0)
            model = lgb.train(params=self.params, train_set=train,
                              num_boost_round=len(cv_result['binary_logloss-mean']))

            self.mean_list.append(cv_result['binary_logloss-mean'][-1])
            self.std_list.append(cv_result['binary_logloss-stdv'][-1])
            if self.test_eval_metric == 'logloss':
                self.test_result.append(-neg_log_loss(test_y, model.predict(test_X)))
            elif self.test_eval_metric == 'auc':
                self.test_result.append(roc_auc_score(test_y, model.predict(test_X)))

        # 画图展示.

        # CV-test结果关系图
        x_y = sorted(zip(self.mean_list, self.test_result), key=lambda x: x[0])
        x = [x[0] for x in x_y]
        y = [x[1] for x in x_y]

        self.echart.line(x=x, y=y, title=self.fig_title + '_CV-test结果关系图', is_max_show=True,
                         x_name='CV result', y_name='test result')

        if self.is_rank_corr_plot:
            # 二阶段根据CV均值和标准差的组合, 提高秩相关系数.
            print('开始计算秩相关系数.')
            for alpha in range(50):
                alpha /= 100
                mean_std_combine = np.array(self.mean_list) + alpha * np.array(self.std_list)
                self.rank_corr_list.append(spearmanr(mean_std_combine, np.array(self.test_result))[0])

            # 秩相关系数-标准差系数图.
            self.echart.line(x=list(range(len(self.rank_corr_list))), y=self.rank_corr_list,
                             title=self.fig_title + '_秩相关系数-标准差系数图', is_max_show=True,
                             x_name='标准差权重', y_name='秩相关系数')


class CVStabilityEvaluatorWithLR:
    '''
    CV稳定性验证.
    '''

    def __init__(self, train=None, test=None, label='target',
                 nfold=10, n_iter=50, save_path='./image/'):
        self.train = train
        self.test = test
        self.label = label
        self.nfold = nfold
        self.n_iter = n_iter
        self.mean_list = []
        self.test_result = []
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.mkdir(save_path)

    def random_set_params(self, seed=7):
        np.random.seed(seed)
        C = (np.random.rand() * 2 - 1) * 5
        return pow(10, C)

    @timer
    def eval(self):
        '''CV稳定性测试 '''
        # 划分数据.
        if self.test is None:
            train, test = train_test_split(self.train, test_size=0.3, random_state=7, stratify=self.train[self.label])
            train_X, train_y = split_X_y(df=train, label=self.label)
            test_X, test_y = split_X_y(df=test, label=self.label)
        else:
            train_X, train_y = split_X_y(df=self.train, label=self.label)
            test_X, test_y = split_X_y(df=self.test, label=self.label)
        # 一阶段得到不同超参数下的CV均值.
        for n in range(self.n_iter):
            print('第%d轮CV...' % (n + 1))
            model = LogisticRegressionCV(Cs=[self.random_set_params(seed=n)],
                                         cv=self.nfold,
                                         penalty='l2',
                                         scoring='neg_log_loss',
                                         solver='liblinear',
                                         class_weight='balanced',
                                         max_iter=100,
                                         n_jobs=4,
                                         random_state=777,
                                         verbose=0
                                         )
            model.fit(train_X, train_y)
            cv_result = np.mean(model.scores_[1], axis=0).max()
            self.mean_list.append(cv_result)
            self.test_result.append(neg_log_loss(test_y, model.predict_proba(test_X)[:, 1]))

        # 画图展示.

        # CV-test结果关系图
        plt.figure(figsize=(16, 12))
        x_y = sorted(zip(self.mean_list, self.test_result), key=lambda x: x[0])
        x = [x[0] for x in x_y]
        y = [x[1] for x in x_y]
        plt.plot(x, y)
        plt.savefig(self.save_path + 'CV-test结果关系图')
        plt.show()


class LightCV:
    '''
    LGB CV.
    按层生长, 用于特征工程验证方法是否有效.
    '''

    def __init__(self,
                 df=None,
                 label='target',
                 nfold=7,
                 params=None,
                 eval_metric='logloss'):
        self.df = df
        self.label = label
        self.ft_list = self.df.columns.tolist()
        if self.label in self.ft_list:
            self.ft_list.remove(self.label)
        else:
            print('警告, 数据集中无目标列.')
        self.weight = compute_sample_weight(class_weight='balanced', y=self.df[self.label])
        self.train_set = lgb.Dataset(data=self.df[self.ft_list], label=self.df[self.label],
                                     free_raw_data=False, weight=self.weight)

        self.nfold = nfold
        if params is None:
            self.params = {'objective': 'binary',
                           'num_tree': 1000,
                           'learning_rate': 0.05,
                           'max_depth': 3,
                           'num_leaf': 256,
                           'bagging_freq': 1,
                           'bagging_fraction': 0.6,
                           'feature_fraction': 0.4,
                           'min_data_in_leaf': 3,
                           'min_sum_hessian_in_leaf': 0.005,
                           'lambda_l1': 0.,
                           'lambda_l2': 0.,
                           'min_split_gain': 0.,
                           'metrics': 'binary_logloss',
                           'seed': 7,
                           'num_thread': 4,
                           'verbose': -1
                           }
        # 保存路径.
        elif isinstance(params, str):
            self.params = load(params)
        # 参数字典对象.
        else:
            self.params = params
        if eval_metric == 'logloss':
            self.params['metrics'] = 'binary_logloss'
        elif eval_metric == 'auc':
            self.params['metrics'] = 'auc'
        else:
            print('警告, 评估指标错误.')
        self.eval_metric = eval_metric

    def run(self):
        cv_result = lgb.cv(params=self.params, train_set=self.train_set, nfold=self.nfold,
                           early_stopping_rounds=50)
        if self.eval_metric == 'logloss':
            return -cv_result['binary_logloss-mean'][-1], len(cv_result['binary_logloss-mean'])
        elif self.eval_metric == 'auc':
            return cv_result['auc-mean'][-1], len(cv_result['auc-mean'])


class LightBayesOptimizer:
    '''
    lightgbm二分类问题的贝叶斯优化.
    可以获得CV上的最佳超参数, 以及最佳模型.
    在创建对象的时候, 需要指定优化模式.
    1. 利用CV还是HO进行优化.
    2. 利用AUC还是LOGLOSS进行优化.
    '''

    def __init__(self, df=None, label=None, pbounds=None,
                 cv_verbose=-1, time_filed=None, val_size=0.3,
                 nfold=7, opt_mode='cv', metrics='logloss'):
        '''
        :param df: df, 数据集, 仅包含特征和目标列.
        :param label: str, 目标列名称.
        :param pbounds: dict, 超参数调参范围.
        :param cv_verbose: int, CV信息输出模式, 默认-1(不输出信息).
        :param time_filed: str, 时间字段名称.
        :param val_size: float, 验证集大小比例, 默认0.3.
        :param nfold: int, CV折数, 默认5.
        :param opt_mode: str, 优化模式, 可选'cv', 'ho', 默认'cv'
        :param metrics: str, 模型评估参数, 可选'auc', 'logloss', 默认'logloss'.
        '''
        target_data = df[label]
        ft_list = df.columns.tolist()
        ft_list.remove(label)
        if time_filed:
            ft_list.remove(time_filed)
        weight = compute_sample_weight(class_weight='balanced', y=df[label])
        self.df = lgb.Dataset(data=df[ft_list], label=target_data, free_raw_data=False, weight=weight)
        if opt_mode == 'cv':
            pass
        else:
            if time_filed:
                df = df.sort_values(time_filed)
                train = df.iloc[:int(len(df) * (1 - val_size))]
                val = df.iloc[int(len(df) * (1 - val_size)):]
                weight = compute_sample_weight(class_weight='balanced', y=train[label])
                self.train = lgb.Dataset(data=train[ft_list], label=train[label], free_raw_data=False, weight=weight)
                weight = compute_sample_weight(class_weight='balanced', y=val[label])
                self.val = lgb.Dataset(data=val[ft_list], label=val[label], free_raw_data=False, weight=weight)

            else:
                train, val = train_test_split(df, test_size=val_size,
                                              random_state=777, shuffle=True,
                                              stratify=df[label])

                weight = compute_sample_weight(class_weight='balanced', y=train[label])
                self.train = lgb.Dataset(data=train[ft_list], label=train[label], free_raw_data=False, weight=weight)
                weight = compute_sample_weight(class_weight='balanced', y=val[label])
                self.val = lgb.Dataset(data=val[ft_list], label=val[label], free_raw_data=False, weight=weight)
        if metrics == 'auc':
            self.metrics = 'auc'
        else:
            self.metrics = 'binary_logloss'
        self.opt_mode = opt_mode
        self.params = {'objective': 'binary',
                       'num_tree': 1000,
                       'learning_rate': 0.01,
                       'max_depth': -1,
                       'num_leaf': 8,
                       'bagging_freq': 1,
                       'bagging_fraction': 0.8,
                       'feature_fraction': 0.8,
                       'min_data_in_leaf': 3,
                       'min_sum_hessian_in_leaf': 0.005,
                       'lambda_l1': 0.,
                       'lambda_l2': 0.,
                       'min_split_gain': 0.,
                       # 'is_unbalance': True,
                       'metrics': self.metrics,
                       'seed': 7,
                       'num_thread': 4,
                       'verbose': -1
                       }

        # 设置叶斯优化的超参数范围.
        self.pbounds = {'num_leaf': (2, 42),
                        'bagging_fraction': (0.2, 1),
                        'feature_fraction': (0.2, 1),
                        'min_data_in_leaf': (1, 50),
                        'min_sum_hessian_in_leaf': (-5, 1),
                        'lambda_l1': (-5, 0),
                        'lambda_l2': (-5, 0),
                        'min_split_gain': (-5, 0)}
        if pbounds:
            for key in pbounds:
                self.pbounds[key] = pbounds[key]
        self.val_size = val_size
        self.nfold = nfold
        self.cv_verbose = cv_verbose

        self.model = None
        self.best_params = None
        self.best_result = -np.inf

    def cv(self, **kwargs):
        '''
        贝叶斯优化目标函数.
        通过传入不同的参数, 返回对应的函数值.
        '''
        params = self.params.copy()
        params['num_tree'] = 10000
        params['num_leaf'] = int(kwargs['num_leaf'])
        params['bagging_fraction'] = kwargs['bagging_fraction']
        params['feature_fraction'] = kwargs['feature_fraction']
        params['min_data_in_leaf'] = int(kwargs['min_data_in_leaf'])
        params['min_sum_hessian_in_leaf'] = pow(10, kwargs['min_sum_hessian_in_leaf']) - 1e-5
        params['lambda_l1'] = pow(10, kwargs['lambda_l1']) - 1e-5
        params['lambda_l2'] = pow(10, kwargs['lambda_l2']) - 1e-5
        params['min_split_gain'] = pow(10, kwargs['min_split_gain']) - 1e-5

        cv_result = lgb.cv(params=params, train_set=self.df, nfold=self.nfold,
                           early_stopping_rounds=50, verbose_eval=self.cv_verbose)
        if self.metrics == 'binary_logloss':
            result = -cv_result['binary_logloss-mean'][-1]
            num_tree = len(cv_result['binary_logloss-mean'])
        else:
            result = cv_result['auc-mean'][-1]
            num_tree = len(cv_result['auc-mean'])
        if result > self.best_result:
            self.best_params = params
            self.best_params['num_tree'] = num_tree
            self.best_result = result
        return result

    def ho(self, **kwargs):
        params = self.params.copy()
        params['num_tree'] = 10000
        params['num_leaf'] = int(kwargs['num_leaf'])
        params['bagging_fraction'] = kwargs['bagging_fraction']
        params['feature_fraction'] = kwargs['feature_fraction']
        params['min_data_in_leaf'] = int(kwargs['min_data_in_leaf'])
        params['min_sum_hessian_in_leaf'] = pow(10, kwargs['min_sum_hessian_in_leaf']) - 1e-5
        params['lambda_l1'] = pow(10, kwargs['lambda_l1']) - 1e-5
        params['lambda_l2'] = pow(10, kwargs['lambda_l2']) - 1e-5
        params['min_split_gain'] = pow(10, kwargs['min_split_gain']) - 1e-5

        model = lgb.train(params=params, train_set=self.train,
                          num_boost_round=10000, valid_sets=[self.val], valid_names=['val'],
                          early_stopping_rounds=50, verbose_eval=False)
        if self.metrics == 'binary_logloss':
            result = -model.best_score['val']['binary_logloss']
        else:
            result = model.best_score['val']['auc']
        if result > self.best_result:
            self.best_params = params
            self.best_params['num_tree'] = model.best_iteration
            self.best_result = result

        return result

    @timer
    def run(self, save_log_path='bayes_opt_log.json',
            if_save_log=False, if_load_log=False, init_points=50,
            n_iter=0, verbose=1, is_verbose=1, random_state=777):
        '''
        lgb贝叶斯优化主函数.
        :param save_log_path: log保存地址, str.
        :param if_save_log: 是否保存log.
        :param if_load_log: 是否加载log.
        :return: 贝叶斯优化结果.
        '''
        if self.opt_mode == 'ho':
            f = self.ho
        else:
            f = self.cv
        opt = BayesianOptimization(f=f, pbounds=self.pbounds,
                                   random_state=random_state, verbose=verbose)

        # 加载log.
        if if_load_log and os.path.exists(save_log_path):
            load_logs(opt, logs=[save_log_path])

        # 保存log.
        if if_save_log:
            logger = JSONLogger(path=save_log_path)
            opt.subscribe(Events.OPTMIZATION_STEP, logger)

        # 贝叶斯搜索.
        opt.maximize(init_points=init_points, n_iter=n_iter)

        # 打印最佳结果.
        if is_verbose:
            print('Best result is:')
            print(opt.max['target'])

        return opt.max['target']

    def fit_model(self, do_correct=True):
        params = self.best_params.copy()
        if do_correct:
            if self.opt_mode == 'ho':
                correct_ratio = 1 / (1 - self.val_size)
            else:
                correct_ratio = 1 / (1 - 1 / self.nfold)
            params['min_data_in_leaf'] = int(params['min_data_in_leaf'] * correct_ratio)
            params['min_sum_hessian_in_leaf'] *= correct_ratio
            params['lambda_l1'] *= correct_ratio
            params['lambda_l2'] *= correct_ratio
            params['min_split_gain'] *= correct_ratio
        self.model = lgb.train(params=params, train_set=self.df)

    def predict(self, data):
        return self.model.predict(data[self.model.feature_name()])

    def save_model(self, path='./model/lgb.model'):
        save(path=path, obj=self.model)

    def save_params(self, path='./model/lgb.params'):
        save(path=path, obj=self.best_params)


class LightBayesOptimizerRough:
    '''
    lightgbm二分类问题的贝叶斯粗优化, 主要用于特征工程中.
    '''

    def __init__(self, df=None, label=None, pbounds=None,
                 cv_verbose=-1, nfold=7):
        '''
        :param df: df, 数据集, 仅包含特征和目标列.
        :param label: str, 目标列名称.
        :param pbounds: dict, 超参数调参范围.
        :param cv_verbose: int, CV信息输出模式, 默认-1(不输出信息).
        :param nfold: int, CV折数, 默认5.
        '''
        target_data = df[label]
        ft_list = df.columns.tolist()
        ft_list.remove(label)
        weight = compute_sample_weight(class_weight='balanced', y=df[label])
        self.df = lgb.Dataset(data=df[ft_list], label=target_data, free_raw_data=False, weight=weight)
        self.params = {'objective': 'binary',
                       'num_tree': 1000,
                       'learning_rate': 0.05,
                       'max_depth': 3,
                       'num_leaf': 256,
                       'bagging_freq': 1,
                       'bagging_fraction': 0.6,
                       'feature_fraction': 0.4,
                       'min_data_in_leaf': 3,
                       'min_sum_hessian_in_leaf': 0.005,
                       'lambda_l1': 0.,
                       'lambda_l2': 0.,
                       'min_split_gain': 0.,
                       'metrics': 'binary_logloss',
                       'seed': 7,
                       'num_thread': 4,
                       'verbose': -1
                       }

        # 设置叶斯优化的超参数范围.
        self.pbounds = {'max_depth': (1, 6),
                        'bagging_fraction': (0.2, 1),
                        'feature_fraction': (0.2, 1),
                        'min_sum_hessian_in_leaf': (-5, 2)}
        if pbounds:
            for key in pbounds:
                self.pbounds[key] = pbounds[key]
        self.nfold = nfold
        self.cv_verbose = cv_verbose

        self.model = None
        self.best_params = None
        self.best_result = -np.inf

    def cv(self, **kwargs):
        '''
        贝叶斯优化目标函数.
        通过传入不同的参数, 返回对应的函数值.
        '''
        params = self.params.copy()
        params['num_tree'] = 10000
        params['max_depth'] = int(kwargs['max_depth'])
        params['bagging_fraction'] = kwargs['bagging_fraction']
        params['feature_fraction'] = kwargs['feature_fraction']
        params['min_sum_hessian_in_leaf'] = pow(10, kwargs['min_sum_hessian_in_leaf']) - 1e-5

        cv_result = lgb.cv(params=params, train_set=self.df, nfold=self.nfold,
                           early_stopping_rounds=50, verbose_eval=self.cv_verbose)
        result = -cv_result['binary_logloss-mean'][-1]
        num_tree = len(cv_result['binary_logloss-mean'])
        if result > self.best_result:
            self.best_params = params
            self.best_params['num_tree'] = num_tree
            self.best_result = result
        return result

    @timer
    def run(self, save_log_path='bayes_opt_log.json',
            if_save_log=False, if_load_log=False, init_points=30,
            n_iter=10, verbose=0, is_verbose=1, random_state=7):
        '''贝叶斯粗优化 '''
        opt = BayesianOptimization(f=self.cv, pbounds=self.pbounds,
                                   random_state=random_state, verbose=verbose)

        # 加载log.
        if if_load_log and os.path.exists(save_log_path):
            load_logs(opt, logs=[save_log_path])

        # 保存log.
        if if_save_log:
            logger = JSONLogger(path=save_log_path)
            opt.subscribe(Events.OPTMIZATION_STEP, logger)

        # 贝叶斯搜索.
        opt.maximize(init_points=init_points, n_iter=n_iter)

        # 打印最佳结果.
        if is_verbose:
            print('Best result is:')
            print(opt.max['target'])

        return opt.max['target']

    def fit_model(self, do_correct=True):
        params = self.best_params.copy()
        if do_correct:
            correct_ratio = 1 / (1 - 1 / self.nfold)
            params['min_sum_hessian_in_leaf'] *= correct_ratio
        self.model = lgb.train(params=params, train_set=self.df)

    def predict(self, data):
        return self.model.predict(data[self.model.feature_name()])

    def save_model(self, path='./model/lgb.model'):
        save(path=path, obj=self.model)

    def save_params(self, path='./model/lgb.params'):
        save(path=path, obj=self.best_params)


class LRCV:
    '''
    逻辑回归CV.
    '''

    def __init__(self, nfold=7, Cs=10, penalty='l2', metric='logloss'):
        if metric == 'logloss':
            scoring = 'neg_log_loss'
        elif metric == 'auc':
            scoring = self.auc
        else:
            print('警告, 评估参数输入错误.')

        self.model = LogisticRegressionCV(Cs=Cs,
                                          cv=nfold,
                                          penalty=penalty,
                                          scoring=scoring,
                                          solver='liblinear',
                                          class_weight='balanced',
                                          max_iter=100,
                                          n_jobs=4,
                                          random_state=7,
                                          verbose=0)

    def cv(self, X=None, y=None):
        self.model.fit(X, y)
        return np.mean(self.model.scores_[1], axis=0).max()

    def auc(self, estimator, X, y):
        y_pred = estimator.predict_proba(X)[:, 1]
        return roc_auc_score(y_true=y, y_score=y_pred)


class LROptimizer:
    '''
    二分类逻辑回归参数优化.
    '''

    def __init__(self, df=None, label='target',
                 nfold=7, Cs=10, val_perc=0.3, mode='cv',
                 class_weight='balanced'
                 ):
        self.label = label
        self.ft_list = df.columns.tolist()
        if label in self.ft_list:
            self.ft_list.remove(label)
        else:
            print('警告, 数据集中不包含目标列.')
        self.nfold = nfold
        self.Cs = Cs
        self.model = None
        self.df = df
        self.mode = mode
        self.val_perc = val_perc
        self.class_weight = class_weight

        # 若为hold out模式, 则划分出验证集.
        if self.mode == 'ho':
            self.train, self.val = train_test_split(self.df,
                                                    test_size=self.val_perc,
                                                    random_state=7,
                                                    stratify=self.df[self.label])

    @timer
    def run(self):
        '''逻辑回归参数调节 '''
        print('正在训练逻辑回归模型.')
        if self.mode == 'cv':
            # L1.
            lr_model_l1 = LogisticRegressionCV(Cs=self.Cs,
                                               cv=self.nfold,
                                               penalty='l1',
                                               scoring='neg_log_loss',
                                               solver='liblinear',
                                               class_weight=self.class_weight,
                                               max_iter=100,
                                               n_jobs=4,
                                               random_state=7,
                                               verbose=0)
            lr_model_l1.fit(self.df[self.ft_list], self.df[self.label])
            score_l1 = np.mean(lr_model_l1.scores_[1], axis=0).max()

            # L2
            lr_model_l2 = LogisticRegressionCV(Cs=self.Cs,
                                               cv=self.nfold,
                                               penalty='l2',
                                               scoring='neg_log_loss',
                                               solver='liblinear',
                                               class_weight=self.class_weight,
                                               max_iter=100,
                                               n_jobs=4,
                                               random_state=7,
                                               verbose=0)
            lr_model_l2.fit(self.df[self.ft_list], self.df[self.label])
            score_l2 = np.mean(lr_model_l2.scores_[1], axis=0).max()

            if score_l1 > score_l2:
                self.model = lr_model_l1
            else:
                self.model = lr_model_l2
            self.C = self.model.C_[0]
            self.penalty = self.model.get_params()['penalty']
            print('最佳模型的参数:')
            print('正则系数: %f, 正则模式: %s' % (self.C, self.penalty))
        else:
            for C in [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]:
                lr_model_l1 = LogisticRegression(penalty='l1',
                                                 C=C,
                                                 class_weight=self.class_weight,
                                                 random_state=7,
                                                 solver='liblinear',
                                                 max_iter=100,
                                                 n_jobs=4)
                lr_model_l1.fit(self.train[self.ft_list], self.train[self.label])

                score_l1 = neg_log_loss(self.val[self.label], lr_model_l1.predict_proba(self.val[self.ft_list]))

                lr_model_l2 = LogisticRegression(penalty='l2',
                                                 C=C,
                                                 class_weight=self.class_weight,
                                                 random_state=7,
                                                 solver='liblinear',
                                                 max_iter=100,
                                                 n_jobs=4)
                lr_model_l2.fit(self.train[self.ft_list], self.train[self.label])
                score_l2 = neg_log_loss(self.val[self.label], lr_model_l2.predict_proba(self.val[self.ft_list]))

                if score_l1 > score_l2:
                    self.model = lr_model_l1
                else:
                    self.model = lr_model_l2
                self.C = self.model.C
                self.penalty = self.model.get_params()['penalty']
            print('最佳模型的参数:')
            print('正则系数: %f, 正则模式: %s' % (self.C, self.penalty))

    def predict(self, data):
        data = data[self.ft_list]
        return self.model.predict_proba(data)[:, 1]

    def save_model(self, path='./model/LR.model'):
        save(path=path, obj=self.model)


if __name__ == '__main__':
    from base_utils import split_X_y

    train = pd.read_csv('./data/tw_train.csv')
    test = pd.read_csv('./data/tw_test.csv')
    df = train.append(test)
    df_X, df_y = split_X_y(df)
    cvse = CVStabilityEvaluator(nfold=10, n_iter=50)
    cvse.run(df_X, df_y)
