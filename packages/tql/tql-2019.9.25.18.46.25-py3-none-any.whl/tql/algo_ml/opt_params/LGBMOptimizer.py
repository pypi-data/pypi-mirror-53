#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import numpy as np
import lightgbm as lgb

from .Optimizer import Optimizer


class LGBMOptimizer(Optimizer):
    """https://www.jianshu.com/p/1100e333fcab"""

    def __init__(self, X, y, cv=5, cv_seed=None, params_bounds=None):
        super().__init__(X, y, cv, cv_seed, params_bounds)
        self.best_iterations = []
        self.data = lgb.Dataset(X, y, silent=True, free_raw_data=True)

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        for p in ('max_depth', 'depth', 'num_leaves', 'subsample_freq', 'min_child_samples'):
            if p in params:
                params[p] = int(np.round(params[p]))
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        rst = lgb.cv(_params,
                     self.data,
                     num_boost_round=10000,
                     nfold=self.cv,
                     early_stopping_rounds=0,
                     verbose_eval=100,
                     show_stdv=False,
                     stratified=True,
                     shuffle=True,
                     seed=self.cv_seed)

        scores = rst['auc-mean']
        self.best_iterations.append(len(scores))
        return scores[-1]
