#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:00:06 2019

@author: shelley
"""

## 單純貝式比羅輯回歸稍微好一點
# In[] Preprocessing
import robert.preprocessor as pp

# Load Data
dataset = pp.dataset(file="Diabetes.csv")

# In[]
# X, Y decomposition
X, Y = pp.decomposition(dataset, x_columns=[0,1, 2, 3,4,5,6,7], y_columns=[8])

# In[]
# Feature Selection
from robert.preprocessor import KBestSelector
selector = KBestSelector()
X = selector.fit(x_ary=X, y_ary=Y, auto=True, verbose=True, sort=True).transform(x_ary=X)

# Split Training & Testing set
X_train, X_test, Y_train, Y_test = pp.split_train_test(X, Y)

# Feature Scaling
X_train, X_test = pp.feature_scaling(fit_ary=X_train, transform_arys=(X_train, X_test))
# In[] Logistic Regression with Robert's Class
from robert.regression import LogisticRegressor
from robert.performance import ClassificationPerformance

# Training & Predict
regressor = LogisticRegressor()
Y_predict = regressor.fit(X_train, Y_train).predict(X_test)

# Performance
pfm = ClassificationPerformance(Y_test, Y_predict)

print("Confusion Matrix:\n", pfm.confusion_matrix())
print("Accuracy: {:.2%}".format(pfm.accuracy()))
print("Recall: {:.2%}".format(pfm.recall()))
print("Precision: {:.2%}".format(pfm.precision()))
print("F1-score: {:.2%}".format(pfm.f_score()))

# In[] Visualize the Result
import robert.model_drawer as md
selector = KBestSelector(best_k = 2)
X = selector.fit(x_ary=X, y_ary=Y, auto=False).transform(x_ary=X)
# Split Training & Testing set
X_train, X_test, Y_train, Y_test = pp.split_train_test(X, Y)

# Feature Scaling
X_train, X_test = pp.feature_scaling(fit_ary=X_train, transform_arys=(X_train, X_test))
regressor = LogisticRegressor()
Y_predict = regressor.fit(X_train, Y_train).predict(X_test)

md.classify_result(x=X_train, y=Y_train, classifier=regressor.regressor, title="訓練集樣本點 vs. 模型")
md.classify_result(x=X_test, y=Y_test, classifier=regressor.regressor, title="測試集樣本點 vs. 模型")
