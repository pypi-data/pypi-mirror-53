# coding=utf-8
'''
GBDT, LR.
'''
import numpy as np
import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.linear_model import LogisticRegression

import lightgbm as lgb


from shy_tools.base_utils import save, timer, neg_log_loss, split_X_y, load
from shy_tools.data_transform import StandardTransformer
from shy_tools.data_visualization import Echart

import os
import warnings

warnings.filterwarnings('ignore')


class LR:
    def __init__(self, df=None, label='target',
                 penalty='l2', C=1, is_std=True):
        self.label = label
        self.ft_list = df.columns.tolist()
        if label in self.ft_list:
            self.ft_list.remove(label)
        self.model = LogisticRegression(penalty=penalty,
                                        C=C,
                                        class_weight='balanced',
                                        random_state=7,
                                        solver='liblinear',
                                        n_jobs=4)

        self.X, self.y = split_X_y(df=df, label=label)
        if is_std:
            std_scl = StandardTransformer()
            self.X = std_scl.fit_transform(X=self.X)


    def run(self):
        self.model.fit(X=self.X, y=self.y)


    def predict(self, X=None):
        return self.model.predict_proba(X=X[self.ft_list])[:, 1]


    def score(self, X=None, y=None, metric='auc'):
        if metric == 'auc':
            res = roc_auc_score(y_true=y, y_score=self.predict(X=X))
            return res
        elif metric == 'logloss':
            res = neg_log_loss(y_true=y, y_pred=self.predict(X=X))
        else:
            print('警告, 评估参数输入错误.')
        return res


    def save(self, save_path='LR.model'):
        save(path='./model/' + save_path, obj=self.model)



class Light:
    def __init__(self):

        pass


    def run(self):

        pass

    def save(self):

        pass


if __name__ == '__main__':

    pass