# coding=utf-8
'''
流程整合.
减少灵活性, 增加便利性.
'''
from __future__ import absolute_import
import gc
import pandas as pd
from sklearn.metrics import roc_auc_score

from .data_transform import LinearModelPreprocessor
from .param_optimize import LightBayesOptimizer, LROptimizer
from .feature_select import FeatureSelector
from .base_utils import mkdir, split_X_y
from .feature_select import ModelParamsGenerator, LGBRFE

def gen_model_params_and_ft_select(df=None, label='target'):
    mpg = ModelParamsGenerator(df=df, label=label)
    model_params_dict = mpg.run()

    lgbrfe = LGBRFE(df=df, label=label, params=model_params_dict)
    lgbrfe.run()
    lgbrfe.plot()



def ft_select_and_param_opt(select_method='null_imp', train=None,
                            test=None, label='target', time_filed=None,
                            is_pred=False, name='origin', n_iter=50):
    '''
    将特征选择与超参数调节, 模型评估放在一起.
    若没有测试集, 则保存训练好的模型.
    若没有测试集标签, 则进一步保存并输出测试集预测结果.
    若有测试集标签, 则输出测试集AUC.
    :param select_method: str, 特征选择的方法, 默认"null_imp".
    :param train: df, 训练集.
    :param test: df, 测试集.
    :param label: str, 标签列, 默认"target".
    :param time_filed: str, 时间列.
    :param is_pred: bool, 是否输出测试集预测结果, 默认False, 即输出AUC.
    :param name: str, 名称标准, 以区分不同的数据.
    :param n_iter: int, 超参数随机搜索次数, 默认20.
    :return: null or float, 根据模式不返回或返回AUC.
    '''
    # 创建文件夹保存信息.
    mkdir('./feature/')
    mkdir('./model/')
    mkdir('./result/')
    ###############################################################
    # 参数选择.
    if select_method == 'null_imp':
        if time_filed is None:
            fs = FeatureSelector(df=train, label=label)
        else:
            fs = FeatureSelector(df=train.drop(time_filed, axis=1), label=label)
        fs.null_imp_select(verbose=0)
        fs.save_feature(path='./feature/' + name + '_' + select_method,
                        is_save_ft_list=False, is_save_ft_list_dict=True)
        ft_list_dict = fs.select_ft_list_dict.copy()
    elif select_method == 'boruta':
        if time_filed is None:
            fs = FeatureSelector(df=train, label=label)
        else:
            fs = FeatureSelector(df=train.drop(time_filed, axis=1), label=label)
        fs.boruta_select(verbose=0)
        fs.save_feature(path='./feature/' + name + '_' + select_method,
                        is_save_ft_list=False, is_save_ft_list_dict=True)
        ft_list_dict = fs.select_ft_list_dict.copy()
    elif select_method == 'eli5':
        if time_filed is None:
            fs = FeatureSelector(df=train, label=label)
        else:
            fs = FeatureSelector(df=train.drop(time_filed, axis=1), label=label)
        fs.eli5_permutation_select()
        fs.save_feature(path='./feature/' + name + '_' + select_method,
                        is_save_ft_list=False, is_save_ft_list_dict=True)
        ft_list_dict = fs.select_ft_list_dict.copy()
    elif select_method == 'gain':
        if time_filed is None:
            fs = FeatureSelector(df=train, label=label)
        else:
            fs = FeatureSelector(df=train.drop(time_filed, axis=1), label=label)
        fs.gain_imp_select()
        fs.save_feature(path='./feature/' + name + '_' + select_method,
                        is_save_ft_list=False, is_save_ft_list_dict=True)
        ft_list_dict = fs.select_ft_list_dict.copy()
    # 释放内存.
    del fs
    gc.collect()

    ##############################################################
    # 模型训练.

    for p in ft_list_dict:
        ft_list = ft_list_dict[p]
    ##############################################################
        # cv logloss.
        lgb_opt = LightBayesOptimizer(df=train[ft_list + [label]], time_filed=None,
                                      label=label, opt_mode='cv', metrics='logloss')
        lgb_opt.run(init_points=n_iter, n_iter=0, verbose=0, is_verbose=0)
        lgb_opt.fit_model()
        # 保存模型.
        lgb_opt.save_model(path='./model/' + name + '_' + select_method + '_'
                                + str(p) + '_' + 'cv_logloss')
        # 模型预测/评估.
        if test is None:
            pass
        else:
            if is_pred:
                result = lgb_opt.predict(test)
                result = pd.DataFrame({'predict': result})
                result.to_csv('./result/' + name + '_' + select_method + '_'
                              + str(p) + '_' + 'cv_logloss.csv')
            else:
                print(name + '_' + select_method + '_'
                      + str(p) + '_' + 'cv_logloss AUC is : %f' %
                      roc_auc_score(test[label], lgb_opt.predict(test)))
    ##############################################################
        # ho logloss
        lgb_opt = LightBayesOptimizer(df=train[ft_list + [label]], time_filed=None,
                                      label=label, opt_mode='ho', metrics='logloss')
        lgb_opt.run(init_points=n_iter, n_iter=0, verbose=0, is_verbose=0)
        lgb_opt.fit_model()
        # 保存模型.
        lgb_opt.save_model(path='./model/' + name + '_' + select_method + '_'
                                + str(p) + '_' + 'ho_logloss')
        # 模型预测/评估.
        if test is None:
            pass
        else:
            if is_pred:
                result = lgb_opt.predict(test)
                result = pd.DataFrame({'predict': result})
                result.to_csv('./result/' + name + '_' + select_method + '_'
                              + str(p) + '_' + 'ho_logloss.csv')
            else:
                print(name + '_' + select_method + '_'
                      + str(p) + '_' + 'ho_logloss AUC is : %f' %
                      roc_auc_score(test[label], lgb_opt.predict(test)))
    ##############################################################
        # ho logloss time
        if time_filed is not None:
            lgb_opt = LightBayesOptimizer(df=train[ft_list + [label, time_filed]], time_filed=time_filed,
                                          label=label, opt_mode='ho', metrics='logloss')
            lgb_opt.run(init_points=n_iter, n_iter=0, verbose=0, is_verbose=0)
            lgb_opt.fit_model()
            # 保存模型.
            lgb_opt.save_model(path='./model/' + name + '_' + select_method + '_'
                                    + str(p) + '_' + 'ho_logloss_time')
            # 模型预测/评估.
            if test is None:
                pass
            else:
                if is_pred:
                    result = lgb_opt.predict(test)
                    result = pd.DataFrame({'predict': result})
                    result.to_csv('./result/' + name + '_' + select_method + '_'
                                  + str(p) + '_' + 'cv_logloss_time.csv')
                else:
                    print(name + '_' + select_method + '_'
                          + str(p) + '_' + 'cv_logloss_time AUC is : %f' %
                          roc_auc_score(test[label], lgb_opt.predict(test)))


def linear_model_preprocess_and_fit(train=None,
                                    test=None,
                                    label='target',
                                    is_boxcox=True,
                                    boxcox_mode='yeo-johnson',
                                    is_miss_impute=True,
                                    min_miss_num=100,
                                    miss_mode='mean',
                                    is_indicate=True,
                                    nfold=7,
                                    Cs=10):
    '''
    :param train: 数据集.
    :param label: 标签名称.
    :param is_boxcox: 是否BoxCox.
    :param boxcox_mode: boxcox模式.
    :param is_miss_impute: 是否填充缺失值.
    :param min_miss_num: 最小缺失填充阈值.
    :param miss_mode: 填充缺失值模式.
    :param is_indicate: 是否添加指示列.
    :param nfold: 交叉验证折数.
    :param Cs: 正则化系数.
    :return: 训练好的逻辑回归模型.
    '''
    # 数据预处理.
    lmp = LinearModelPreprocessor(is_boxcox=is_boxcox,
                                  boxcox_mode=boxcox_mode,
                                  is_miss_impute=is_miss_impute,
                                  min_miss_num=min_miss_num,
                                  miss_mode=miss_mode,
                                  is_indicate=is_indicate)
    train_X, train_y = split_X_y(train, label=label)
    test_X, test_y = split_X_y(test, label=label)

    train_X = lmp.fit_transform(X=train_X, y=train_y)
    test_X = lmp.transform(X=test_X)
    train_X_y, test_X_y = train_X, test_X
    train_X_y[label], test_X_y[label] = train_y, test_y
    del train_X, test_X
    gc.collect()

    # 逻辑回归调参.
    lro = LROptimizer(df=train_X_y, label=label, nfold=nfold, Cs=Cs)
    lro.run()

    # 输出结果.
    print('训练集结果:')
    print(roc_auc_score(train_X_y[label], lro.predict(train_X_y)))
    print('测试集结果.')
    print(roc_auc_score(test_X_y[label], lro.predict(test_X_y)))

    return lmp, lro



if __name__ == '__main__':

    train = pd.read_csv('./data/bc_train.csv')
    gen_model_params_and_ft_select(df=train)
