#!/usr/bin/env python3


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


# #### Exercise 1.1 (Performance measures)
# Classify the test data and evaluate the classification performance of the trained model 'clf_svm' using the scikit-learn metrics package. Compare vaious metrics (classification accuracy, precision, recall, f-score), interpret their values and argue which of them might be the most meaningful to report.

from sklearn import metrics

y_pred = clf_svm.predict( X_test )
print( 'OOB accuracy: ', metrics.accuracy_score( y_test, y_pred ) )
print( metrics.classification_report( y_test, y_pred, target_names=iris.target_names ) )
print('I would pick the f1 score, because it condenses both precision and recall.')
print('All the numbers coiside in our example.')


# #### Exercise 1.2 (ROC curve)
# helper to plot ROC curves
def plot_roc_curves(fprs, tprs):
    fig = plt.figure(figsize=(20,10))

    for fpr, tpr in zip(fprs, tprs):
        auc = metrics.roc_auc_score( y_test, y_pred )
        plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % auc)

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")


def plot_roc( y_true, y_pred ):
    fpr, tpr, threshold = metrics.roc_curve( y_true, y_pred )
    plot_roc_curves([fpr], [tpr])


plot_roc( y_test, y_pred )


# #### Exercise 1.3 (Model comparison)
# Train four more SVM models on the training data by varying the regularization parameter $C$ (the gamma parameter can be set to 10 again).
# Put the models into a list 'clfs' using the append method.
# You can add a name to each classifier by setting clf.name = "some description" to keep track of the configuration.


clfs = []
for c in [ 0.1, 0.5, 1, 10 ]:
    clf_svm = SVC( gamma=10, C=c )
    clf_svm.fit( X_train, y_train )
    clf_svm.name = 'gamma=10, C=' + str(c)
    clfs.append( clf_svm )

####################
# INSERT CODE HERE #
####################


# Let's have a look at the decision functions of the four classifiers...
# visualize the decision functions of the four different classifiers
fig, axes = plt.subplots(2, 2, figsize=(20, 10))

for clf, ax in zip(clfs, axes.ravel()):
    show_decision_function(clf, ax)
    ax.set_title(clf.name)


# ... and draw the ROC curves.


for clf in clfs:
    y_pred = clf.predict( X_test )
    plot_roc( y_test, y_pred)


# ## 2. Hyperparameter Tuning
# Many models have hyperparameters, parameters that can't directly be estimated from the data.
# They have to be manually tuned by the practioner, because there is no analytical formula available to calculate an appropriate value.
# One example is the regularization parameter $C$ in SVMs.
#
# #### Exercise 2.1 (Nested cross-validation)
#
# Train a SVM classifier for the detection of iris versicolor again, but this time with a proper tuning of the regularization parameter $C$
# (you may set the gamma parameter to 10 again).
# Select a reasonable range of parameter values for $C$ and implement a nested cross-validation (as shown on the slides) by yourself.

# You can use the following helper function that creates a list of masks. Each mask can be used as an index set to select the test samples.
# The function accepts the number of samples *num_samples* in the dataset and the desired number of folds *k* as input parameters.
# Since the data is sorted by the labels the k-fold CV will likely have trouble with class imbalances in the some cases.
# So you should randomly shuffle the data before applying the masks.

# helper function to create k-fold train-test-splits
def create_kfold_mask(num_samples, k):
    masks = []
    fold_size = num_samples / k
    for i in range(k):
        mask = np.zeros(num_samples, dtype=bool)
        mask[int(i*fold_size):int((i+1)*fold_size)] = True
        masks.append(mask)
    return masks

# visualization of the splits created by 'create_kfold_mask'
masks = create_kfold_mask(150, 10)
plt.matshow(masks)


class NCV:
    '''Nested Cross-Validation.'''
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split


    def __init__( self, X, y, loss=mean_squared_error, k=10 ):
        self._all_data = np.array( list( zip( X, y ) ) )
        np.random.shuffle( self._all_data )

        self._loss = loss

        # Number of groups in the inner loop.
        self._k = k


    def train( self ):
        X, y = zip( *self._all_data )
        X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2 )
        tr = np.array( list( zip( X_train, y_train ) ) )
        c = self.calc_hyperparams( tr )

        y_pred = fit_model( tr, c).predict( X_test )
        print( 'OOB accuracy: ', metrics.accuracy_score( y_test, y_pred ) )
        print( metrics.classification_report( y_test, y_pred, target_names=iris.target_names ) )

        m = fit_model( data=self._all_data, c=c )
        return m


    @staticmethod
    def fit_model( data, c, g=10 ):
        m = SVC( gamma=g, C=c )
        X, y = zip( *data )
        m.fit( X, y )
        return m


    @staticmethod
    def calc_risk( y_pred, y_true, loss ):
        '''Empirical risk on a sample.'''
        assert len( y_pred ) == len( y_true )
        return ( 1 / len(y) ) * sum([ loss( y_pred, y_true ) ])


    @classmethod
    def calc_OOB_risk( cls, train, test, loss, c=1, g=10 ):
        '''Train a model on a dataset. Return a risk estimate.'''
        m = cls.fit_model( train, c, g )
        X, y = zip( *test )
        pred = m.predict( X )
        r = cls.calc_risk( pred, y, loss )
        return r


    @staticmethod
    def calc_crossval_risk( dataset, body, k ):
        '''Apply `body` to overlapping batches of the dataset.'''
        risk = []
        for mask in create_kfold_mask( len( dataset ), k ):
            tr = dataset[ ~ mask ]
            te = dataset[ mask ]
            r = body( train=tr, test=te )
            risk.append( r )
        return sum(risk) / len(risk)


    def calc_hyperparams( self
                        , dataset
                        , c_grid=np.logspace( start=0, stop=2, num=50 ) ):
        '''Perform a grid search in hyperparameter space.'''
        risk = []
        for c in c_grid:
            body = lambda train, test: self.calc_OOB_risk( train=train, test=test
                                                         , loss=self._loss, c=c, g=10 )
            r = self.calc_crossval_risk( dataset, body, self._k )
            risk.append( r )

        best = c_grid[ np.argmax( risk ) ]
        return best



ncv = NCV( X_versi, y_versi )
m = ncv.train()
print( m )


plt.show()
