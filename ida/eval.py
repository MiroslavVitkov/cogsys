#!/usr/bin/env python3


plot = False


import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

iris = load_iris()
print('Loaded {} data points'.format(len(iris.data)))
X, y = iris.data, iris.target
print('Class labels: {}'.format(list(zip(range(3), iris.target_names))))

# We try to classify the iris versicolor with the help of the first two features.
import numpy as np

X_versi = X[:, :2]
y_versi = np.zeros(len(y))
y_versi[y == 1] = 1

# plot iris data with two features
plt.scatter(X_versi[y_versi == 1, 0], X_versi[y_versi == 1, 1], c='red', label='iris versicolor')
plt.scatter(X_versi[y_versi == 0, 0], X_versi[y_versi == 0, 1], c='green', label='other')
plt.xlabel("x1")
plt.ylabel("x2")
plt.title('Iris data')
plt.legend()
if plot:
    plt.show()

# We split the data into a train and test (holdout) set with a split ratio of 75% to 25%.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_versi, y_versi, test_size=0.25, random_state=3)

# The following function is a little visualization helper that draws the values of the decision function on a heat map given a matplotlib axe.
def show_decision_function(clf, ax):
    xx, yy = np.meshgrid(np.linspace(4.5, 8, 200), np.linspace(1.5, 4.0, 200))
    try:
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    except AttributeError:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 0]

    Z = Z.reshape(xx.shape)
    ax.pcolormesh(xx, yy, Z, cmap=plt.cm.jet)
    ax.set_xlim(4.5, 8)
    ax.set_ylim(1.5, 4.0)
    ax.set_xticks(())
    ax.set_yticks(())
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=100)

# We now train a SVM classifier on the training data and plot its decision boundary.
from sklearn.svm import SVC

clf_svm = SVC(gamma=10, C=1)
clf_svm.fit(X_train, y_train)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
show_decision_function(clf_svm, ax)
ax.set_title('Decision function of a SVM classifier with gamma = 10, C = 1')
if plot:
    plt.show()


# #### Exercise 1.1 (Performance measures)
# Classify the test data and evaluate the classification performance of the trained model 'clf_svm' using the scikit-learn metrics package. Compare vaious metrics (classification accuracy, precision, recall, f-score), interpret their values and argue which of them might be the most meaningful to report.

from sklearn import metrics

y_pred = clf_svm.predict( X_test )
print( 'OOB accuracy: ', metrics.accuracy_score( y_test, y_pred ) )
print( metrics.classification_report( y_test, y_pred, target_names=iris.target_names ) )
print('???')


# #### Exercise 1.2 (ROC curve)
# helper to plot ROC curves
def plot_roc_curves(fprs, tprs):
    fig = plt.figure(figsize=(20,10))

    for fpr, tpr in zip(fprs, tprs):
        plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % metrics.auc(fpr, tpr))

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()

# fpr, tpr =

# plot the curve
plot_roc_curves([fpr], [tpr])
