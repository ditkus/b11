'Automated Valuation Model'

import pdb
import numpy as np
import pandas as pd
from pprint import pprint
import sklearn
import sklearn.ensemble
import sklearn.linear_model
import sklearn.preprocessing


from columns_contain import columns_contain
import AVM_elastic_net
import AVM_gradient_boosting_regressor
import AVM_random_forest_regressor
from Features import Features
cc = columns_contain


def avm_scoring(estimator, df):
    'return error from using fitted estimator with test data in the dataframe'
    # TODO: make a static method of class AVM
    assert isinstance(estimator, AVM)
    X, y = estimator.extract_and_transform(df)
    assert len(y) > 0
    y_hat = estimator.predict(df)
    errors = y_hat - y
    median_abs_error = np.median(np.abs(errors))
    return -median_abs_error  # because GridSearchCV chooses the model with the highest score


class AVM(sklearn.base.BaseEstimator):
    'one estimator for several underlying models'
    def __init__(self,
                 model_name=None,          # parameters for all models
                 forecast_time_period=None,
                 n_months_back=None,
                 random_state=None,
                 verbose=0,
                 features_group=None,
                 implementation_module=None,
                 alpha=None,               # for ElasticNet
                 l1_ratio=None,
                 units_X=None,
                 units_y=None,
                 n_estimators=None,        # for RandomForestRegressor
                 max_depth=None,
                 max_features=None,
                 learning_rate=None,       # for GradientBoostingRegressor
                 loss=None,
                 ):
        # NOTE: just capture the parameters (to conform to the sklearn protocol)
        self.model_name = model_name
        self.forecast_time_period = forecast_time_period
        self.n_months_back = n_months_back
        self.random_state = random_state
        self.verbose = verbose
        self.features_group = features_group
        self.implementation_module = implementation_module

        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.units_X = units_X
        self.units_y = units_y

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features

        self.learning_rate = learning_rate
        self.loss = loss

    def fit(self, samples):
        'convert samples to X,Y and fit them'
        self.implementation_module = {
            'ElasticNet': AVM_elastic_net,
            'GradientBoostingRegressor': AVM_gradient_boosting_regressor,
            'RandomForestRegressor': AVM_random_forest_regressor,
        }[self.model_name]
        X_train, y_train = self.extract_and_transform(samples)
        fitted = self.implementation_module.fit(self, X_train, y_train)
        return fitted.model  # scikit learn's fitted model

    def get_attributes(self):
        'return both sets of attributes, with None if not used by that model'
        pdb.set_trace()
        attribute_names = (
            'coef_', 'sparse_coef_', 'intercept_', 'n_iter_',                        # for linear
            'estimators_', 'feature_importances_', 'oob_score_', 'oob_prediction_',  # for random forest
        )
        return {name: getattr(self.model, name, None) for name in attribute_names}

    def extract_and_transform(self, samples, transform_y=True):
        'return X and y'
        result = self.implementation_module.extract_and_transform(self, samples, transform_y)
        return result

    def predict(self, samples):
        X_test, y_test = self.extract_and_transform(samples, transform_y=False)
        assert y_test is None
        return self.implementation_module.predict(self, X_test)

    def setattr(self, parameter, value):
        setattr(self, parameter, value)
        return self


if False:
    pd()
    pprint()
    Features()
