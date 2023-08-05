# coding=utf-8
'''
特征选择.
'''
import numpy as np
import pandas as pd
from collections import OrderedDict
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import log_loss

import lightgbm as lgb
from eli5.permutation_importance import get_score_importances
from eli5.sklearn.permutation_importance import PermutationImportance
from shy_tools.base_class import BorutaPy
from shy_tools.base_utils import timer, rank_sort_combine, save, traversal_search, neg_log_loss, load
from shy_tools.param_optimize import LightCV, LRCV, LightBayesOptimizerRough
from shy_tools.data_transform import StandardTransformer
from shy_tools.data_visualization import Echart

import matplotlib.pyplot as plt
import seaborn as sns

import pickle
import warnings

warnings.filterwarnings('ignore')


class ModelParamsGenerator:
    '''
    利用重要性, 得到不同特征数量对应的模型参数.
    '''

    def __init__(self, df=None, label='target',
                 imp_type='split',
                 ft_percs=[20, 40, 60, 80, 100],
                 ft_percs_range=[(0., .3), (.3, .5), (.5, .7), (.7, .9), (.9, 1.)],
                 nfolds=7,
                 init_points=20,
                 n_iter=10,
                 save_path='ft_perc_range_params.dict'):
        self.label = label
        self.df = df
        self.n_ft = self.df.shape[1] - 1
        self.nfolds = nfolds
        self.init_points = init_points
        self.n_iter = n_iter
        self.imp_type = imp_type
        self.ft_percs = ft_percs
        self.ft_percs.reverse()
        self.ft_percs_range = ft_percs_range
        self.ft_percs_range.reverse()
        self.save_path = save_path

        self.ft_list = df.columns.tolist()
        if label in self.ft_list:
            self.ft_list.remove(label)
        else:
            print('警告, 数据中没有目标列')

        self.ft_params_dict = OrderedDict()

    @timer
    def run(self):
        '''获取不同特征数量对应模型参数 '''
        tmp_ft_list = self.ft_list.copy()

        for i in range(len(self.ft_percs)):
            print('第%d轮, 特征数量%d' % (i + 1, len(tmp_ft_list)))
            # 跑CV得到一组相对合适的超参数.
            lbo = LightBayesOptimizerRough(df=self.df[tmp_ft_list + [self.label]], label=self.label, nfold=self.nfolds)
            lbo.run(init_points=self.init_points, n_iter=self.n_iter, verbose=0)
            lbo.fit_model()
            self.ft_params_dict[self.ft_percs_range[i]] = lbo.best_params

            # 利用该超参数训练模型并筛选特征.
            imp_list = lbo.model.feature_importance(importance_type=self.imp_type)
            ft_imp_list = list(zip(tmp_ft_list, imp_list))
            ft_imp_list = sorted(ft_imp_list, key=lambda x: x[1], reverse=True)
            if i + 1 < len(self.ft_percs):
                tmp_ft_list = [x[0] for x in ft_imp_list][: int(self.ft_percs[i + 1] / 100 * self.n_ft)]

        save(path='./model/' + self.save_path, obj=self.ft_params_dict)
        print('运行完成, 保存模型参数成功.')
        return self.ft_params_dict


class LGBRFE:
    def __init__(self, df=None, label='target',
                 nfold=7,
                 imp_type='split',
                 min_num_ft=0.1,
                 n_ft_rm_per_iter=0.05,
                 params=None):
        self.df = df
        self.n_sample = self.df.shape[0]
        self.label = label
        self.imp_type = imp_type
        self.nfold = nfold
        self.ft_list = self.df.columns.tolist()
        if self.label in self.ft_list:
            self.ft_list.remove(self.label)
        else:
            print('警告, 数据中不包含目标列.')

        self.min_num_ft = min_num_ft if isinstance(min_num_ft, int) \
            else int(self.df.shape[1] * min_num_ft)
        self.n_ft_rm_per_iter = n_ft_rm_per_iter if isinstance(n_ft_rm_per_iter, int) \
            else int(self.df.shape[1] * n_ft_rm_per_iter)
        if self.n_ft_rm_per_iter == 0:
            self.n_ft_rm_per_iter = 1

        self.rfe_result = []
        self.best_ft_list = None
        self.best_result = None
        self.weight = compute_sample_weight(class_weight='balanced', y=self.df[self.label])

        if params is None:
            self.params = {'objective': 'binary',
                           'num_tree': 1000,
                           'learning_rate': 0.05,
                           'max_depth': 3,
                           'num_leaf': 64,
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
        elif isinstance(params, str):
            self.params = load(params)
        else:
            self.params = params
        if not isinstance(list(self.params.keys())[0], tuple):
            self.params = {(0., 1.): self.params}

    def choose_params(self, ft_list):
        perc = len(ft_list) / self.n_sample
        for perc_range in self.params:
            if perc >= perc_range[0] and perc <= perc_range[1]:
                return self.params[perc_range], perc_range

    @timer
    def run(self):
        '''LGBRFE '''
        remain_ft_list = self.ft_list.copy()
        print('开始RFE特征选择...')
        cv = LightCV(df=self.df,
                     label=self.label,
                     nfold=self.nfold,
                     params=self.choose_params(remain_ft_list)[0])
        cv_result, n_tree = cv.run()
        self.rfe_result.insert(0, (len(remain_ft_list), cv_result, remain_ft_list))
        self.best_ft_list, self.best_result = remain_ft_list, cv_result
        print('第1轮, 特征数量%d, cv结果%f' % (len(remain_ft_list), cv_result))
        n_iter = 1
        while len(remain_ft_list) > self.min_num_ft:

            train_set = lgb.Dataset(data=self.df[remain_ft_list], label=self.df[self.label],
                                    free_raw_data=False, weight=self.weight)
            model = lgb.train(params=self.choose_params(remain_ft_list)[0], train_set=train_set)

            imp_list = model.feature_importance(importance_type=self.imp_type)
            ft_imp_list = sorted(zip(remain_ft_list, imp_list), key=lambda x: x[1], reverse=True)
            remain_ft_list = [x[0] for x in ft_imp_list]
            if len(remain_ft_list) > self.n_ft_rm_per_iter + self.min_num_ft:
                remain_ft_list = remain_ft_list[: -self.n_ft_rm_per_iter]
            else:
                remain_ft_list = remain_ft_list[: self.min_num_ft]
            cv = LightCV(df=self.df[remain_ft_list + [self.label]],
                         label=self.label,
                         nfold=self.nfold,
                         params=self.choose_params(remain_ft_list)[0])
            cv_result, n_tree = cv.run()
            self.rfe_result.insert(0, (len(remain_ft_list), cv_result, remain_ft_list))
            n_iter += 1
            self.best_result = cv_result if cv_result > self.best_result else self.best_result
            self.best_ft_list = remain_ft_list if cv_result == self.best_result else self.best_ft_list
            print('第%d轮, 特征数量%d, cv结果%f' % (n_iter, len(remain_ft_list), cv_result))
        print('最佳特征数量%d, 最佳CV结果%f' % (len(self.best_ft_list), self.best_result))

    def plot(self, mode='html', title='LGBRFE',
             x_name='feature nums', y_name='CV result'):

        X, Y = [], []
        for item in self.rfe_result:
            X.append(item[0])
            Y.append(item[1])
        echart = Echart(mode=mode)
        echart.line(x=X, y=Y,
                    title=title,
                    is_max_show=True,
                    x_name=x_name,
                    y_name=y_name)


class RFECV:
    def __init__(self, nfold=10,
                 rank_type='gain',
                 min_num_ft=0.1,
                 n_ft_rm_per_iter=0.05):
        self.min_num_ft = min_num_ft
        self.n_ft_rm_per_iter = n_ft_rm_per_iter
        self.cv = LightCV(nfold=nfold)
        self.rank_type = rank_type
        self.rfe_result = []
        self.model = lgb.LGBMClassifier(boosting_type='gbdt',
                                        num_leaves=64,
                                        max_depth=5,
                                        learning_rate=0.01,
                                        n_estimators=1000,
                                        class_weight='balanced',
                                        min_child_weight=0.001,
                                        min_child_samples=1,
                                        subsample=0.6,
                                        subsample_freq=1,
                                        colsample_bytree=1,
                                        random_state=7,
                                        n_jobs=4,
                                        importance_type='gain')
        self.imp_generator = None

    def fit_transform(self, X=None, y=None):
        self.min_num_ft = self.min_num_ft if isinstance(self.min_num_ft, int) \
            else int(X.shape[1] * self.min_num_ft)
        self.n_ft_rm_per_iter = self.n_ft_rm_per_iter if isinstance(self.n_ft_rm_per_iter, int) \
            else int(X.shape[1] * self.n_ft_rm_per_iter)
        remain_ft_list = X.columns.tolist()
        print('开始RFE特征选择...')
        cv_result = self.cv.run(X=X[remain_ft_list], y=y)
        self.rfe_result.insert(0, (len(remain_ft_list), cv_result, remain_ft_list))
        print('第1轮, 特征数量%d, cv结果%f' % (len(remain_ft_list), cv_result))
        n_iter = 1
        while len(remain_ft_list) > self.min_num_ft:
            self.model.set_params(n_estimators=int(100 * (len(remain_ft_list) /
                                                          (np.sqrt(len(remain_ft_list)) *
                                                           self.model.get_params()['max_depth']))),
                                  colsample_bytree=np.sqrt(len(remain_ft_list)) / len(remain_ft_list))
            if self.rank_type == 'gain':
                self.imp_generator = self.model
            elif self.rank_type == 'split':
                self.model.set_params(importance_type='split')
                self.imp_generator = self.model
            elif self.rank_type == 'eli5':
                self.imp_generator = PermutationImportance(estimator=self.model, scoring=self.neg_log_loss,
                                                           n_iter=5, random_state=7, cv=5, refit=False)
            elif self.rank_type == 'mix':
                self.imp_generator = PermutationImportance(estimator=self.model, scoring=self.neg_log_loss,
                                                           n_iter=5, random_state=7, cv=5, refit=True)
            else:
                print('不支持该排序类型.')
                return None

            self.imp_generator.fit(X, y, verbose=False)
            if self.rank_type != 'mix':
                imp_list = self.imp_generator.feature_importances_
            else:
                imp_list = rank_sort_combine([self.imp_generator.feature_importances_.tolist(),
                                              self.imp_generator.estimator_.feature_importances_.tolist()])
            ft_imp_list = sorted(zip(remain_ft_list, imp_list), key=lambda x: x[1], reverse=True)
            remain_ft_list = [x[0] for x in ft_imp_list]
            if len(remain_ft_list) > self.n_ft_rm_per_iter + self.min_num_ft:
                remain_ft_list = remain_ft_list[: -self.n_ft_rm_per_iter]
            else:
                remain_ft_list = remain_ft_list[: self.min_num_ft]
            cv_result = self.cv.run(X=X[remain_ft_list], y=y)
            self.rfe_result.insert(0, (len(remain_ft_list), cv_result, remain_ft_list))

            n_iter += 1
            print('第%d轮, 特征数量%d, cv结果%f' % (n_iter, len(remain_ft_list), cv_result))

    def neg_log_loss(self, model, X, y):
        y_pred = model.predict_proba(X)[:, 1]
        return neg_log_loss(y, y_pred)

    def plot(self):
        X, Y = [], []
        for item in self.rfe_result:
            X.append(item[0])
            Y.append(item[1])

        plt.figure(figsize=(16, 12))
        plt.plot(X, Y)
        plt.xlabel('feature nums')
        plt.ylabel('cv result')
        plt.savefig('rfe')
        plt.show()

        pass


class ForwardSelector:
    def __init__(self, df=None, label='target', nfold=7, Cs=10,
                 is_break=True, retain_ft_list=None):
        self.df = df.reset_index(drop=True)
        self.label = label
        self.is_break = is_break
        self.ft_list = df.columns.tolist()
        self.ft_list.remove(label)
        self.retain_ft_list = retain_ft_list
        self.model = LogisticRegressionCV(Cs=Cs, solver='liblinear', class_weight='balanced',
                                          n_jobs=4, random_state=7, cv=nfold, scoring='neg_log_loss')

        self.best_ft_list = None
        self.best_cv_result = -np.inf
        self.ft_result_dict = {}

    def cv_lr(self, ft_list):
        self.model.fit(self.df[ft_list], self.df[self.label])
        result = self.model.scores_
        return np.mean(result[1], axis=0).max()

    def run(self):
        if self.retain_ft_list is None:
            ft_result_list = []
            for ft in self.ft_list:
                ft_result_list.append((ft, self.cv_lr([ft])))
            ft_result_list = sorted(ft_result_list, key=lambda x: x[1], reverse=True)
            select_ft_list = [ft_result_list[0][0]]
            ft_list = self.ft_list.copy()
            ft_list.remove(select_ft_list[0])
            print('添加特征: ', ft_result_list[0][0], 'CV结果: ', ft_result_list[0][1])
            self.best_cv_result = ft_result_list[0][1]
            self.best_ft_list = [ft_result_list[0][0]]
            self.ft_result_dict[1] = (self.best_ft_list.copy(), self.best_cv_result)
        else:
            select_ft_list = self.retain_ft_list.copy()
            ft_list = self.ft_list.copy()
            for ft in select_ft_list:
                ft_list.remove(ft)
            self.best_cv_result = self.cv_lr(select_ft_list)
            self.best_ft_list = select_ft_list.copy()
            self.ft_result_dict[len(self.best_ft_list)] = (self.best_ft_list.copy(), self.best_cv_result)
            print('初始特征数量: ', len(self.best_ft_list), 'CV结果: ', self.best_ft_list)

        while len(ft_list) > 0:
            result_list = []
            for ft in ft_list:
                tmp_ft_list = select_ft_list + [ft]
                result = self.cv_lr(tmp_ft_list)
                result_list.append((ft, result))
            result_list = sorted(result_list, key=lambda x: x[1], reverse=True)

            if result_list[0][1] > self.best_cv_result:
                self.best_cv_result = result_list[0][1]
                select_ft_list.append(result_list[0][0])
                ft_list.remove(result_list[0][0])
                self.best_ft_list = select_ft_list.copy()
                print('添加特征: ', result_list[0][0], 'CV结果上升: ', result_list[0][1])
            else:
                if self.is_break:
                    break
                else:
                    select_ft_list.append(result_list[0][0])
                    ft_list.remove(result_list[0][0])
                    print('添加特征: ', result_list[0][0], 'CV结果下降: ', result_list[0][1])
            self.ft_result_dict[len(select_ft_list)] = (select_ft_list.copy(), result_list[0][1])
        return self.best_ft_list

    def save(self, save_path='./model/forward_ft.dict'):
        save(save_path, self.ft_result_dict)


class BackwardSelector:
    def __init__(self, df=None, label='target', nfold=7, Cs=10,
                 is_break=True, retain_ft_list=None):
        self.df = df.reset_index(drop=True)
        self.label = label
        self.is_break = is_break
        self.ft_list = df.columns.tolist()
        self.ft_list.remove(label)
        self.retain_ft_list = set(retain_ft_list) if retain_ft_list is not None else set()
        self.model = LogisticRegressionCV(Cs=Cs, solver='liblinear', class_weight='balanced',
                                          n_jobs=4, random_state=7, cv=nfold, scoring='neg_log_loss')

        self.best_ft_list = None
        self.best_cv_result = -np.inf
        self.ft_result_dict = {}

    def cv_lr(self, ft_list):
        self.model.fit(self.df[ft_list], self.df[self.label])
        result = self.model.scores_
        return np.mean(result[1], axis=0).max()

    def run(self):

        ft_list = self.ft_list.copy()
        self.best_cv_result = self.cv_lr(ft_list)
        self.best_ft_list = ft_list.copy()
        self.ft_result_dict[len(self.best_ft_list)] = (self.best_ft_list.copy(), self.best_cv_result)
        print('初始特征数量: ', len(self.best_ft_list), 'CV结果: ', self.best_ft_list)

        while len(ft_list) > len(self.retain_ft_list):
            result_list = []
            for ft in ft_list:
                tmp_ft_list = ft_list.copy()
                if ft not in self.retain_ft_list:
                    tmp_ft_list.remove(ft)
                else:
                    continue
                result = self.cv_lr(tmp_ft_list)
                result_list.append((ft, result))
            result_list = sorted(result_list, key=lambda x: x[1], reverse=True)

            if result_list[0][1] > self.best_cv_result:
                self.best_cv_result = result_list[0][1]
                ft_list.remove(result_list[0][0])
                self.best_ft_list = ft_list.copy()
                print('去掉特征: ', result_list[0][0], 'CV结果上升: ', result_list[0][1])
            else:
                if self.is_break:
                    break
                else:
                    ft_list.remove(result_list[0][0])
                    print('去掉特征: ', result_list[0][0], 'CV结果下降: ', result_list[0][1])
            self.ft_result_dict[len(ft_list)] = (ft_list.copy(), result_list[0][1])
        return self.best_ft_list

    def save(self, save_path='./model/backward_ft.dict'):
        save(save_path, self.ft_result_dict)


class FeatureSelector:
    def __init__(self, df=None, label=None, time_filed=None, val_size=0.3, nfold=5,
                 params=None, num_leaf_list=[6], metrics='logloss'):
        '''
        :param df: df, 数据集.
        :param label: str, 目标变量.
        :param time_filed: str, 时间变量.
        :param val_size: float, 验证集大小, 默认0.3.
        :param nfold: int, cv折数, 默认5.
        :param params: dict, LGB参数.
        :param num_leaf_list: list[int], 叶子数量, 在筛选的时候选择一个最好的叶子数量, 默认[4].
        '''
        self.df = df.reset_index(drop=True)
        self.label = label
        self.ft_list = df.columns.tolist()
        self.ft_list.remove(label)
        self.time_filed = time_filed
        self.val_size = val_size
        self.nfold = nfold
        self.model = None
        self.num_leaf_list = num_leaf_list

        if time_filed:
            self.ft_list.remove(self.time_filed)
            tmp_data = self.df.sort_values(by=self.time_filed)
            self.train = tmp_data.iloc[: int(len(df) * (1 - self.val_size))]
            self.val = tmp_data.iloc[int(len(df) * (1 - self.val_size)):]
            del tmp_data
        else:
            self.train, self.val = train_test_split(self.df, test_size=self.val_size,
                                                    random_state=777, stratify=self.df[self.label])

        self.df_weight = compute_sample_weight(class_weight='balanced', y=self.df[label])
        self.train_weight = compute_sample_weight(class_weight='balanced', y=self.train[label])
        self.val_weight = compute_sample_weight(class_weight='balanced', y=self.val[label])

        if metrics == 'auc':
            self.metrics = 'auc'
        else:
            self.metrics = 'binary_logloss'
        self.params = {'objective': 'binary',
                       'num_tree': 10000,
                       'learning_rate': 0.01,
                       'max_depth': -1,
                       'num_leaf': 6,
                       'bagging_freq': 1,
                       'bagging_fraction': 0.8,
                       'feature_fraction': 0.8,
                       'min_data_in_leaf': 1,
                       'min_sum_hessian_in_leaf': 0.001,
                       'lambda_l1': 0.,
                       'lambda_l2': 0.,
                       'min_split_gain': 0.,
                       # 'is_unbalance': True,
                       'seed': 777,
                       'num_thread': 4,
                       'verbose': -1,
                       'metrics': self.metrics
                       }
        if params:
            for k in params:
                self.params[k] = params[k]

        self.select_ft_list = self.ft_list
        self.select_ft_list_dict = {}

    def neg_logloss(self, y_ture, y_pred):
        weight = compute_sample_weight(class_weight='balanced', y=y_ture)
        return -log_loss(y_true=y_ture, y_pred=y_pred, sample_weight=weight)

    def hold_out(self, ft_list, num_leaf_list=None):
        '''
        Hold out.
        :param ft_list: list[str], 特征列表.
        :return: auc: float, AUC.
        '''
        best_result = -np.inf
        best_model = None
        train = lgb.Dataset(data=self.train[ft_list], label=self.train[self.label], weight=self.train_weight)
        val = lgb.Dataset(data=self.val[ft_list], label=self.val[self.label], weight=self.val_weight)
        if num_leaf_list is None:
            num_leaf_list = self.num_leaf_list
        for num_leaf in num_leaf_list:
            params = self.params.copy()
            params['num_leaf'] = num_leaf
            params['num_tree'] = 10000
            model = lgb.train(params=params, train_set=train, valid_sets=[val], valid_names=['val'],
                              early_stopping_rounds=20, verbose_eval=False)
            if self.metrics == 'auc':
                result = model.best_score['val']['auc']
            else:
                result = -model.best_score['val']['binary_logloss']
            if result > best_result:
                best_result = result
                best_model = model
        return best_result, best_model

    def cv_lgb(self, ft_list, num_leaf_list=None):
        '''
        CV.
        :param ft_list: list[str], 特征列表.
        :return: auc: float, AUC.
        '''
        best_result = -np.inf
        train = lgb.Dataset(data=self.df[ft_list], label=self.df[self.label], weight=self.df_weight)
        if num_leaf_list is None:
            num_leaf_list = self.num_leaf_list
        for num_leaf in num_leaf_list:
            params = self.params.copy()
            params['num_leaf'] = num_leaf
            params['num_tree'] = 10000
            cv_res = lgb.cv(params=params, train_set=train, nfold=self.nfold,
                            early_stopping_rounds=20, verbose_eval=False, seed=777)
            if self.metrics == 'auc':
                if cv_res['auc-mean'][-1] > best_result:
                    best_result = cv_res['auc-mean'][-1]
            else:
                if cv_res['binary_logloss-mean'][-1] > best_result:
                    best_result = cv_res['binary_logloss-mean'][-1]
        return best_result

    def cv_lr(self, ft_list):
        model = LogisticRegressionCV(Cs=10, solver='liblinear', class_weight='balanced',
                                     n_jobs=4, random_state=777, cv=5, scoring='neg_log_loss')
        model.fit(self.df[ft_list].fillna(0), self.df[self.label])
        result = model.scores_
        return np.mean(result[1], axis=0).max()

    @timer
    def boruta_select(self, perc=60, verbose=2, max_iter=100, is_ergodic=True):
        '''
        利用Boruta筛选特征.
        基模型为随机森林.
        :param perc: int, 默认90, 统计阈值, 越小得到的特征越多.
        :param verbose: int, 默认为2, 打印信息模式.
        :param max_iter: int, 默认100, 最大迭代轮数.
        :return: None.
        '''

        if not is_ergodic:
            ft_selector = BorutaPy(perc=perc, n_estimators='auto', verbose=verbose,
                                   max_iter=max_iter, random_state=777)
            train = self.df[self.select_ft_list].values

            target = self.df[self.label].values
            ft_selector.fit(train, target)
            select_ft_list = [ft for ft, support in zip(self.select_ft_list, ft_selector.support_) if support == True]
            print('-' * 20)
            print('Boruta select %d features from %d features.' % (len(select_ft_list), len(self.select_ft_list)))
            self.select_ft_list = select_ft_list
        if is_ergodic:
            for p in range(40, 90, 10):
                ft_selector = BorutaPy(perc=p, n_estimators='auto', verbose=verbose,
                                       max_iter=max_iter, random_state=777)
                train = self.df[self.ft_list].values

                target = self.df[self.label].values
                ft_selector.fit(train, target)
                self.select_ft_list_dict[p] = [ft for ft, support in zip(self.select_ft_list, ft_selector.support_) if
                                               support == True]
                print('Boruta select %d features from %d features.' % (
                    len(self.select_ft_list_dict[p]), len(self.ft_list)))

    @timer
    def null_imp_select(self, n_iter=50, num_leaf=128, perc=60, max_depth=5,
                        imp_type='gain', boosting='rf', is_plot=False, is_ergodic=True,
                        verbose=1):
        params = self.params.copy()
        params['boosting'] = boosting
        params['num_leaf'] = num_leaf
        params['max_depth'] = max_depth
        n_ft = len(self.ft_list)
        params['num_tree'] = int(100 * (n_ft / (np.sqrt(n_ft) * params['max_depth'])))
        params['bagging_fraction'] = 0.7
        params['feature_fraction'] = np.sqrt(n_ft) / n_ft

        self.df['fake_label'] = self.df[self.label].values

        # 不打乱标签列得到特征重要性.
        if verbose:
            print('正在训练模型.')
        train = lgb.Dataset(data=self.df[self.ft_list], label=self.df[self.label], weight=self.df_weight)
        model = lgb.train(params=params, train_set=train)
        ft_real_imp_list = model.feature_importance(importance_type=imp_type)
        # 打乱标签列得到特征重要性.
        np.random.seed(777)
        ft_fake_imp_list = []
        for i in range(n_iter):
            if verbose:
                print('正在训练第%d轮模型.' % (i + 1))
            np.random.shuffle(self.df['fake_label'])
            df_weight = compute_sample_weight(class_weight='balanced', y=self.df['fake_label'])
            train = lgb.Dataset(data=self.df[self.ft_list], label=self.df['fake_label'], weight=df_weight)
            model = lgb.train(params=params, train_set=train)
            ft_fake_imp_list.append(model.feature_importance(importance_type=imp_type))

        # 删除打乱的标签列.
        del self.df['fake_label']

        # 计算null_imp指标.
        ft_fake_imp_array = np.array(ft_fake_imp_list)
        null_imp_list = []
        for i in range(len(self.ft_list)):
            null_imp_list.append(np.log((1e-8 + ft_real_imp_list[i]) /
                                        (1e-8 + np.percentile(ft_fake_imp_array[:, i], perc))))
        # 根据指标筛选特征.
        self.select_ft_list = [ft for i, ft in enumerate(self.ft_list) if null_imp_list[i] > 0]
        if is_ergodic:
            for p in range(40, 90, 10):
                null_imp_list = []
                for i in range(len(self.ft_list)):
                    null_imp_list.append(np.log((1e-8 + ft_real_imp_list[i]) /
                                                (1e-8 + np.percentile(ft_fake_imp_array[:, i], p))))
                self.select_ft_list_dict[p] = [ft for i, ft in enumerate(self.ft_list) if null_imp_list[i] > 0]
                print('Null importance select %d features from %d features with perc %d.' %
                      (len(self.select_ft_list_dict[p]), len(self.ft_list), p))
        else:
            print('Null importance select %d features from %d features with perc %d.' %
                  (len(self.select_ft_list), len(self.ft_list), perc))

        # 画图.
        if is_plot:
            null_imp_list.sort(reverse=True)
            sns.barplot(x=null_imp_list, y=list(range(len(null_imp_list))), orient='h')
            plt.show()

    @timer
    def eli5_permutation_select(self, mode='cv', n_iter=50, num_leaf=128, max_depth=5,
                                boosting='rf', perc=40, is_ergodic=True):
        params = self.params.copy()
        params['boosting'] = boosting
        params['num_leaf'] = num_leaf
        params['max_depth'] = max_depth
        n_ft = len(self.ft_list)
        params['num_tree'] = int(100 * (n_ft / (np.sqrt(n_ft) * params['max_depth'])))
        params['bagging_fraction'] = 0.7
        params['feature_fraction'] = np.sqrt(n_ft) / n_ft

        if mode == 'cv':
            score_list_list = []
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=777)
            for train_idx, val_idx in skf.split(self.df, self.df[self.label]):
                train = self.df.loc[train_idx]
                val = self.df.loc[val_idx]

                weight = compute_sample_weight(class_weight='balanced', y=train[self.label])
                train = lgb.Dataset(data=train[self.ft_list], label=train[self.label], weight=weight)
                model = lgb.train(params=params, train_set=train)

                def eli5_score_func(x, y):
                    y_pred = model.predict(x)
                    return self.neg_logloss(y, y_pred)

                _, score_list = get_score_importances(eli5_score_func, val[self.ft_list].values, val[self.label],
                                                      n_iter=n_iter, random_state=777)
                score_list = np.mean(score_list, axis=0)
                score_list_list.append(score_list)
            score_list = np.array(score_list_list).mean(axis=0)
        else:
            train = lgb.Dataset(data=self.train[self.ft_list], label=self.train[self.label], weight=self.train_weight)
            model = lgb.train(params=params, train_set=train)

            def eli5_score_func(x, y):
                y_pred = model.predict(x)
                return self.neg_logloss(y, y_pred)

            _, score_list = get_score_importances(eli5_score_func, self.val[self.ft_list].values, self.val[self.label],
                                                  n_iter=n_iter, random_state=777)
            score_list = np.mean(score_list, axis=0)
        ft_score_list = list(zip(self.ft_list, score_list))
        ft_score_list.sort(key=lambda x: x[1], reverse=True)
        ft_list = [x[0] for x in ft_score_list]
        if not is_ergodic:
            self.select_ft_list = ft_list[: int(len(ft_list) * perc / 100)]
        else:
            for p in range(30, 90, 10):
                self.select_ft_list_dict[p] = ft_list[: int(len(ft_list) * p / 100)]
        # self.select_ft_list = [ft for ft, score in zip(self.ft_list, score_list) if score > 0]

        print(len(self.select_ft_list))

    @timer
    def gain_imp_select(self, num_leaf=128, perc=60, max_depth=5,
                        boosting='rf', is_ergodic=True):
        params = self.params.copy()
        params['boosting'] = boosting
        params['num_leaf'] = num_leaf
        params['max_depth'] = max_depth
        n_ft = len(self.ft_list)
        params['num_tree'] = 100 * (n_ft / (np.sqrt(n_ft) * params['max_depth']))
        params['bagging_fraction'] = 0.7
        params['feature_fraction'] = np.sqrt(n_ft) / n_ft
        train = lgb.Dataset(data=self.df[self.ft_list], label=self.df[self.label], weight=self.df_weight)
        model = lgb.train(params=params, train_set=train)
        imp_list = model.feature_importance(importance_type='gain')
        ft_imp_list = list(zip(self.ft_list, imp_list))
        ft_imp_list.sort(key=lambda x: x[1], reverse=True)
        ft_list = [ft for ft, imp in ft_imp_list]
        if not is_ergodic:
            self.select_ft_list = ft_list[: int(len(ft_list) * perc / 100)]
        else:
            for p in range(50, 90, 10):
                self.select_ft_list_dict[p] = ft_list[: int(len(ft_list) * p / 100)]

    def same_distribution_select(self, psi_threshold=0.1, min_num_in_bin=50):
        '''
        利用训练集和验证集特征的分布是否相同进行特征筛选.
        分布是否相同利用PSI进行衡量.
        :param psi_threshold: float, 分布差异较大的阈值, 默认0.1.
        :return: None.
        '''

        def calc_psi(array_0, array_1, smooth_val=0.001):
            '''
            计算PSI.
            '''
            array_0 = array_0 * 5 + smooth_val
            array_1 = array_1 * 5 + smooth_val
            return ((array_0 - array_1) * np.log10(array_0 / array_1)).sum()

        ft_psi_dict = {}

        for ft in self.ft_list:
            train_df = self.train[[ft, self.label]].fillna(-999999).copy()
            val_df = self.val[[ft, self.label]].fillna(-999999).copy()
            # 调节训练集和验证集的正负样板比例一致.
            train_bad_rate = train_df[self.label].mean()
            val_bad_rate = val_df[self.label].mean()
            # 把逾期率小的抽取部分负样本.
            if train_bad_rate > val_bad_rate:
                bad_num = val_df[self.label].sum()
                good_num = bad_num * (1 - train_bad_rate) / train_bad_rate
                val_df_bad = val_df[val_df[self.label] == 1]
                val_df_good = val_df[val_df[self.label] == 0].sample(int(good_num), random_state=777)
                val_df = val_df_bad.append(val_df_good)
            else:
                bad_num = train_df[self.label].sum()
                good_num = bad_num * (1 - val_bad_rate) / val_bad_rate
                train_df_bad = train_df[train_df[self.label] == 1]
                train_df_good = train_df[train_df[self.label] == 0].sample(int(good_num), random_state=777)
                train_df = train_df_bad.append(train_df_good)
            # 分箱
            bins = np.quantile(train_df[ft].values, [x * 0.1 for x in range(1, 10)]).tolist()
            bins = list(sorted(set(bins)))
            bins = [-np.inf] + bins + [np.inf]
            try:
                train_df['bins'] = pd.cut(train_df[ft], bins, duplicates='drop')
                val_df['bins'] = pd.cut(val_df[ft], bins, duplicates='drop')
            except:
                ft_psi_dict[ft] = psi_threshold + 1
                continue
            train_df_g = train_df.groupby('bins').agg({self.label: ['count', 'mean']})
            train_df_g.columns = ['_'.join(x) for x in train_df_g.columns.ravel()]

            val_df_g = val_df.groupby('bins').agg({self.label: ['count', 'mean']})
            val_df_g.columns = ['_'.join(x) for x in val_df_g.columns.ravel()]

            train_df_g = train_df_g[train_df_g[self.label + '_count'] >= min_num_in_bin]
            val_df_g = val_df_g[val_df_g[self.label + '_count'] >= min_num_in_bin]

            merge_df = pd.merge(left=train_df_g, right=val_df_g, on='bins', how='outer').fillna(0)
            train_array = merge_df[self.label + '_mean_x'].values
            val_array = merge_df[self.label + '_mean_y'].values

            # 计算PSI
            ft_psi_dict[ft] = calc_psi(train_array, val_array)
        # 按阈值筛选同分布特征.
        self.select_ft_list = [x for x in ft_psi_dict if ft_psi_dict[x] <= psi_threshold]
        print('利用同分布选择%d个特征.' % len(self.select_ft_list))

    def rfe_ho(self, ft_imp_mode='gain', num_leaf_list=None):
        '''
        根据特征的重要性进行特征筛选.
        特征重要性可选模式:
            1. split
            2. gain
            3. shap
        默认gain.
        '''

        # 定序字典用于记录信息. {order: (result, ft_list), ...}
        result_dict = OrderedDict()
        ft_list = self.ft_list.copy()
        for i in range(len(ft_list)):
            result, model = self.hold_out(ft_list, num_leaf_list=num_leaf_list)
            if ft_imp_mode == 'split':
                imp_list = model.feature_importance(importance_type='split')
            elif ft_imp_mode == 'gain':
                imp_list = model.feature_importance(importance_type='gain')
            elif ft_imp_mode == 'shap':
                imp_list = None
                pass
            else:
                print('亲亲, 没有这种计算特征重要性的模式呢0.0')
                return None
            # 记录信息.
            result_dict[i] = (result, ft_list.copy())
            print('选择%d个特征, 评估结果为: %f.' % (len(ft_list), result))
            # 找到最小重要性特征.
            min_imp_ft = sorted(zip(ft_list, imp_list), key=lambda x: x[1])[0][0]
            # 移除最小重要性特征.
            ft_list.remove(min_imp_ft)
        best_result_ft = sorted(result_dict.items(), key=lambda x: x[1])[-1]

        print('最佳选择%d个特征, 评估结果为: %f.' % (len(best_result_ft[1][1]), best_result_ft[1][0]))
        self.select_ft_list = best_result_ft[1][1]

    @timer
    def lr_l1_select(self):
        '''
        利用L1正则进行特征选择.
        利用CV训练一个最优的LR模型, 提取其系数不为0的特征.
        '''
        model = LogisticRegressionCV(Cs=20,
                                     cv=5,
                                     penalty='l1',
                                     scoring='neg_log_loss',
                                     solver='liblinear',
                                     class_weight='balanced',
                                     max_iter=100,
                                     n_jobs=4,
                                     random_state=777,
                                     verbose=0)
        model.fit(X=self.df.drop(self.label, axis=1),
                  y=self.df[self.label])
        coef = model.coef_[0]
        self.select_ft_list = [x for i, x in enumerate(self.ft_list) if coef[i] != 0]
        print('L1逻辑回归在%d个特征中选择%d个特征.' % (len(self.ft_list), len(self.select_ft_list)))

    def set_metrics(self, metrics):
        self.metrics = metrics
        self.params['metrics'] = metrics

    def set_params(self, params):
        for p in params:
            if p in self.params:
                self.params[p] = params[p]

    def save_feature(self, path='select_ft', is_save_ft_list=True,
                     is_save_ft_list_dict=False):
        '''
        保存特征.
        :param path: str, 特征保存路径.
        :return: None
        '''
        if is_save_ft_list_dict:
            with open(path + '_list.pkl', 'wb') as f:
                pickle.dump(self.select_ft_list_dict, f)
                f.close()
        if is_save_ft_list:
            with open(path + '.pkl', 'wb') as f:
                pickle.dump(self.select_ft_list, f)
                f.close()


class TraversalSearchSelector:
    def __init__(self, df=None,
                 label='target',
                 nfold=7,
                 ft_num_range=(7, 8),
                 verbose=10):
        self.df = df
        self.label = label
        self.ft_list = df.columns.tolist()
        if label in self.ft_list:
            self.ft_list.remove(label)
        else:
            print('警告, 没有目标列.')

        self.ft_num_range = ft_num_range
        self.cv = LRCV(nfold=nfold)
        self.result_dict = {}
        self.best_ft_list = None
        self.best_result = -np.inf
        self.verbose = verbose


    @timer
    def run(self):
        '''遍历搜索特征'''
        # 数据标准化.
        all_ft_list = self.ft_list.copy()
        for i, ft_list in enumerate(traversal_search(all_ft_list, n_range=self.ft_num_range)):
            cv_result = self.cv.cv(X=self.df[ft_list], y=self.df[self.label])
            self.result_dict[i] = (len(ft_list), cv_result, ft_list)
            self.best_result = cv_result if cv_result > self.best_result else self.best_result
            self.best_ft_list = ft_list if cv_result > self.best_result else self.best_ft_list
            if i % self.verbose == 0:
                print('第%d轮, 特征数量%d, CV结果为%f, 最佳CV结果为%f' % (i, len(ft_list), cv_result, self.best_result))

    def save(self, path='./model/traversal_search_ft.dict'):
        save(path=path, obj=self.result_dict)


class TraversalSearchSelectorWithIndicator:
    def __init__(self, df=None,
                 label='target',
                 nfold=5,
                 ft_num_range=(5, 6, 7),
                 verbose=10):
        self.df = df
        self.label = label
        self.ft_list = df.columns.tolist()
        if label in self.ft_list:
            self.ft_list.remove(label)
        else:
            print('警告, 没有目标列.')
        self.indicate_ft_list = []
        for ft in self.ft_list:
            if ft.endswith('_indicate'):
                self.indicate_ft_list.append(ft)

        for ft in self.indicate_ft_list:
            self.ft_list.remove(ft)
        print('包含的特征有%d个' % len(self.ft_list))
        print('包含指示列的特征有%d个.' % len(self.indicate_ft_list))

        self.ft_num_range = ft_num_range
        self.cv = LRCV(nfold=nfold)
        self.result_dict = {}
        self.best_ft_list = None
        self.best_result = -np.inf
        self.verbose = verbose


    @timer
    def run(self):
        '''遍历搜索特征'''
        # 数据标准化.
        all_ft_list = self.ft_list.copy()
        for i, ft_list in enumerate(traversal_search(all_ft_list, n_range=self.ft_num_range)):
            n_ft = len(ft_list)
            indicate_list = []
            for ft in ft_list:
                if ft + '_indicate' in self.indicate_ft_list:
                    indicate_list.append(ft + '_indicate')
            ft_list = ft_list + indicate_list
            cv_result = self.cv.cv(X=self.df[ft_list], y=self.df[self.label])
            self.result_dict[i] = (n_ft, cv_result, ft_list)
            self.best_result = cv_result if cv_result > self.best_result else self.best_result
            self.best_ft_list = ft_list if cv_result > self.best_result else self.best_ft_list
            if i % self.verbose == 0:
                print('第%d轮, 特征数量%d, CV结果为%f, 最佳CV结果为%f' % (i, n_ft, cv_result, self.best_result))

    def save(self, path='./model/traversal_search_indicate_ft.dict'):
        save(path=path, obj=self.result_dict)



if __name__ == '__main__':
    train = pd.read_csv('./data/bc_train.csv')
    is_ = ModelParamsGenerator(df=train, label='target', nfolds=3,
                               ft_percs=(100, 60, 30), init_points=5, n_iter=0)
    is_.run()
