#!/usr/bin/env python3


# Problem setup.
# Problem setup and tests written by Scheffer, Prasse, Makowski, Jaeger.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.datasets import make_classification, make_regression

X, y = make_classification(n_samples = 1000,n_features=2, n_redundant=0, n_informative=2,
                           random_state=1, n_clusters_per_class=1)


# Visualise the data.
plt.scatter(X[:,0], X[:,1], c=y)


# Pbolem setup
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.33, random_state=42)


# Train a random forest with default parameters and reports its accuracy.
from sklearn.metrics import accuracy_score as acc

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
print(acc(y_test, clf.predict(X_test) ) )


# Plot train and test accuracy for forests of 1 to 20 trees.
def measure(samples, labels, n=10):
    clf = RandomForestClassifier(n_estimators=n)
    clf.fit(X_train, y_train)
    return acc(labels, clf.predict(samples))

r = range(1, 20)
train_acc = [ measure(X_train, y_train, i) for i in r]
test_acc = [ measure(X_test, y_test, i) for i in r]

plt.plot(train_acc)
plt.plot(test_acc)


# Problem setup
churn_df = pd.read_csv('extern/telecom_churn.csv')
label = churn_df['Churn']
churn_df = churn_df.drop(columns=['Churn'])


# Drop non-numeric columns.
df = churn_df.drop('State', axis=1).drop('International plan', axis=1).drop('Voice mail plan', axis=1)


# Plot feature importance.
forest = RandomForestClassifier()
forest.fit(df, label)
important = forest.feature_importances_
plt.barh(range(len(important)), important)
plt.yticks(range(len(list(df))), list(df), size='small')

# Report mean square error on a random forest regressor.
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse
rfr = RandomForestRegressor()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.33)
rfr.fit(X_train, y_train)
print(mse(y_train, rfr.predict(X_train)))
print(mse(y_test, rfr.predict(X_test)))
