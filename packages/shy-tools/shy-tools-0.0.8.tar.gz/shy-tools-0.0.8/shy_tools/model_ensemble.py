# coding=utf-8

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.preprocessing import StandardScaler

from shy_tools.base_utils import save

from category_encoders.james_stein import JamesSteinEncoder
from category_encoders.target_encoder import TargetEncoder
from category_encoders.woe import WOEEncoder

from collections import OrderedDict
import warnings

np.random.seed(777)
warnings.filterwarnings('ignore')


class Stacker:
    '''
    模型融合.
    准备好sub_model_dict非常重要.
    '''

    def __init__(self, train_df=None, label=None, sub_model_dict=None, test_df=None,
                 show_sub_model=False, with_origin_ft=True, origin_ft_name=None):
        '''
        :param train_df: df, 数据集, 包含所有特征和目标列.
        :param label: str, 目标列名称.
        :param sub_model_dict: dict, 子模型信息字典. {model_name: (ft_name, model_class, params)}
        '''
        self.origin_ft_name = origin_ft_name
        self.with_origin_ft = with_origin_ft
        self.show_sub_model = show_sub_model
        self.train_df = train_df.reset_index(drop=True)
        self.label = label
        self.sub_model_dict = sub_model_dict
        self.test_df = test_df.reset_index(drop=True)

    def make_up_data(self, data=None, mode='h'):
        '''
        拼接数据.
        :param data: list[array_0, ...].
        :param mode: str, 拼接模式, 水平'h', 竖直'v'.
        :return: array(2d)
        '''
        if mode == 'h':
            for i, array in enumerate(data):
                data[i] = data[i].reshape((-1, 1))
            return np.concatenate(data, axis=1)
        else:
            return np.concatenate(data)

    def avg_array(self, data):
        '''
        计算array的平均.
        :param data: list[array_0, ...].
        :return: array.
        '''
        res_array = np.zeros_like(data[0])
        for array in data:
            res_array = res_array + array
        return res_array / len(data)

    def logloss(self, model, x, y):
        weight = compute_sample_weight(class_weight='balanced', y=y)
        return -log_loss(y, model.predict_proba(x)[:, 1], sample_weight=weight)

    def sub_model_result(self):
        for model_name in self.sub_model_dict:
            ft_name = self.sub_model_dict[model_name][0]
            model_class = self.sub_model_dict[model_name][1]
            params = self.sub_model_dict[model_name][2]
            # 训练模型.
            model = model_class(**params)
            model.run(self.train_df[ft_name], self.train_df[self.label])
            # 预测结果.
            print('%s的结果为: %f' % (
                model_name, roc_auc_score(self.test_df[self.label], model.predict_proba(self.test_df[ft_name])[:, 1])))

    def stack_two_layer(self, kfold=5):
        if self.show_sub_model:
            self.sub_model_result()
        pred_y_on_cv_list = []
        pred_y_on_test_list = []
        skf = StratifiedKFold(n_splits=kfold, random_state=777, shuffle=True)
        for model_name in self.sub_model_dict:
            print('正在训练%s模型.' % model_name)
            ft_name = self.sub_model_dict[model_name][0]
            model_class = self.sub_model_dict[model_name][1]
            params = self.sub_model_dict[model_name][2]
            # 切分数据集.
            tmp_pred_y_on_cv_list = []
            tmp_pred_y_on_test_list = []
            for train_index, test_index in skf.split(self.train_df[ft_name], self.train_df[self.label]):
                train_x, train_y = self.train_df.loc[train_index, ft_name], self.train_df.loc[train_index, self.label]
                test_x, test_y = self.train_df.loc[test_index, ft_name], self.train_df.loc[test_index, self.label]
                # 训练模型.
                model = model_class(**params)
                model.run(train_x, train_y)
                # 预测结果.
                tmp_pred_y_on_cv_list.append(model.predict_proba(test_x)[:, 1])
                tmp_pred_y_on_test_list.append(model.predict_proba(self.test_df[ft_name])[:, 1])

            # 拼接预测结果.

            pred_y_on_cv_list.append(self.make_up_data(data=tmp_pred_y_on_cv_list, mode='v'))
            pred_y_on_test_list.append(self.avg_array(tmp_pred_y_on_test_list))

        # 拼接结果.
        pred_y_on_cv_mat = self.make_up_data(data=pred_y_on_cv_list, mode='h')
        pred_y_on_test_mat = self.make_up_data(data=pred_y_on_test_list, mode='h')
        # 每个模型输出的结果.
        for i in range(pred_y_on_test_mat.shape[1]):
            print(roc_auc_score(self.test_df[self.label], pred_y_on_test_mat[:, i]))

        # 二阶模型.
        print('正在训练二阶逻辑回归模型.')
        if self.with_origin_ft:
            pred_y_on_cv_mat = np.concatenate([self.train_df[self.origin_ft_name].values, pred_y_on_cv_mat], axis=1)
            pred_y_on_test_mat = np.concatenate([self.test_df[self.origin_ft_name].values, pred_y_on_test_mat], axis=1)
        # 特征归一化.
        scl = StandardScaler()
        scl.fit(pred_y_on_cv_mat)
        pred_y_on_cv_mat = scl.transform(pred_y_on_cv_mat)
        pred_y_on_test_mat = scl.transform(pred_y_on_test_mat)

        lr_model_l1 = LogisticRegressionCV(Cs=100, cv=5, n_jobs=4,
                                           solver='liblinear', scoring=self.logloss,
                                           penalty='l1', class_weight='balanced', random_state=777)
        lr_model_l1.fit(X=pred_y_on_cv_mat, y=self.train_df[self.label])

        lr_model_l2 = LogisticRegressionCV(Cs=100, cv=5, n_jobs=4,
                                           solver='liblinear', scoring=self.logloss,
                                           penalty='l2', class_weight='balanced', random_state=777)
        lr_model_l2.fit(X=pred_y_on_cv_mat, y=self.train_df[self.label])

        # 测试集结果.
        lr_model_l1_score = roc_auc_score(self.test_df[self.label], lr_model_l1.predict_proba(pred_y_on_test_mat)[:, 1])
        lr_model_l2_score = roc_auc_score(self.test_df[self.label], lr_model_l2.predict_proba(pred_y_on_test_mat)[:, 1])
        if lr_model_l1_score > lr_model_l2_score:
            self.lr_model = lr_model_l1
            print('测试集结果: %f' % lr_model_l1_score)
        else:
            self.lr_model = lr_model_l2
            print('测试集结果: %f' % lr_model_l2_score)
        print(roc_auc_score(self.test_df[self.label], pred_y_on_test_mat.sum(axis=1)))

    def stack_three_layer(self):
        pass


class CategoryEncodeCombiner:
    '''
    对几种不同的类别特征编码方式的融合.
    遇事不决上融合.
    考虑到不同编码方式的输出数值范围不一样, 先进行标准化, 再加权融合.
    用于融合的编码方式和默认权重:
                编码方式                    权重
        1. JamesSteinEncoder - binary       50
        2. JamesSteinEncoder - beta         20
        3. TargetEncoder                    20
        4. WOEEncoder                       10
    '''

    def __init__(self, weight=None):
        self.weight = (50, 10, 20, 20) if weight is None else weight
        self.encoder_dict = OrderedDict({'JamesSteinEncoder_binary': JamesSteinEncoder(handle_missing='return_nan',
                                                                                       model='binary', random_state=7,
                                                                                       return_df=False),
                                         'JamesSteinEncoder_beta': JamesSteinEncoder(handle_missing='return_nan',
                                                                                     model='beta', random_state=7,
                                                                                     return_df=False),
                                         'TargetEncoder': TargetEncoder(handle_missing='return_nan', return_df=False),
                                         'WOEEncoder': WOEEncoder(handle_missing='return_nan', random_state=7,
                                                                  return_df=False)})
        self.stdscl_dict = OrderedDict({'JamesSteinEncoder_binary': StandardScaler(),
                                        'JamesSteinEncoder_beta': StandardScaler(),
                                        'TargetEncoder': StandardScaler(),
                                        'WOEEncoder': StandardScaler()})
        self.ft_cat_list = None

    def fit(self, X=None, y=None):
        self.ft_cat_list = X.select_dtypes('object').columns.tolist()
        for ecd in self.encoder_dict:
            X_ecd = self.encoder_dict[ecd].fit_transform(X=X[self.ft_cat_list], y=y)
            self.stdscl_dict[ecd].fit(X=X_ecd)
        return self

    def transform(self, X=None):
        X_res = 0
        for i, ecd in enumerate(self.encoder_dict):
            X_ecd = self.encoder_dict[ecd].transform(X=X[self.ft_cat_list])
            X_ecd_stdscl = self.stdscl_dict[ecd].transform(X=X_ecd)
            X_res = X_res + X_ecd_stdscl * self.weight[i]
        X_res = X_res / 100
        X_res = pd.DataFrame(X_res, columns=self.ft_cat_list)
        for col in X_res.columns.tolist():
            X[col] = X_res[col]
        return X

    def fit_transform(self, X=None, y=None):
        self.fit(X=X, y=y)
        return self.transform(X=X)

    def save(self, path='TransformCombiner.pkl'):
        save(path=path, obj=self)


if __name__ == '__main__':
    train = pd.read_csv('./data/hr_train.csv')
    train_X, train_y = train.drop('target', axis=1), train['target']
    cat_ecd_cb = CategoryEncodeCombiner()
    print(train_X.head(20))
    train_X = cat_ecd_cb.fit_transform(train_X, train_y)
    print(train_X.info())
    print(train_X.head(20))

