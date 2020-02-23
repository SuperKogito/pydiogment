# -*- coding: utf-8 -*-
import random
from sklearn.svm import SVC
import multiprocessing as mp
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier

# init glabal variables
n_jobs = mp.cpu_count()
kernel = 1.0 * RBF(1.0)

# init classifiers
classifiers = {
                "K-Nearest Neighbors (distance weights)":
                KNeighborsClassifier(n_neighbors=5,
                                     weights='distance',
                                     algorithm='auto',
                                     leaf_size=30,
                                     p=2,
                                     metric='minkowski',
                                     metric_params=None,
                                     n_jobs=n_jobs),

                "K-Nearest Neighbors (uniform weights)":
                KNeighborsClassifier(n_neighbors=5,
                                     weights='uniform',
                                     algorithm='auto',
                                     leaf_size=30,
                                     p=2,
                                     metric='minkowski',
                                     metric_params=None,
                                     n_jobs=n_jobs),

                "Gaussian Process":
                GaussianProcessClassifier(kernel=None,
                                          optimizer='fmin_l_bfgs_b',
                                          n_restarts_optimizer=0,
                                          max_iter_predict=100,
                                          warm_start=False,
                                          copy_X_train=True,
                                          random_state=random.seed(42),
                                          multi_class='one_vs_rest',
                                          n_jobs=n_jobs),

                "Decision Tree":
                DecisionTreeClassifier(criterion='gini',
                                       splitter='best',
                                       max_depth=None,
                                       min_samples_split=2,
                                       min_samples_leaf=1,
                                       min_weight_fraction_leaf=0.0,
                                       max_features=None,
                                       random_state=random.seed(42),
                                       max_leaf_nodes=None,
                                       min_impurity_decrease=0.0,
                                       min_impurity_split=None,
                                       class_weight=None,
                                       presort='deprecated'),

                "Random Forest":
                RandomForestClassifier(n_estimators=100,
                                       criterion='gini',
                                       max_depth=None,
                                       min_samples_split=2,
                                       min_samples_leaf=1,
                                       min_weight_fraction_leaf=0.0,
                                       max_features='auto',
                                       max_leaf_nodes=None,
                                       min_impurity_decrease=0.0,
                                       min_impurity_split=None,
                                       bootstrap=True,
                                       oob_score=False,
                                       n_jobs=n_jobs,
                                       random_state=random.seed(42),
                                       verbose=0,
                                       warm_start=False,
                                       class_weight=None),

                "AdaBoost":
                AdaBoostClassifier(base_estimator=None,
                                   n_estimators=100,
                                   learning_rate=1.0,
                                   algorithm='SAMME.R',
                                   random_state=random.seed(42)),

                "Naive Bayes":
                GaussianNB(priors=None, var_smoothing=1e-09),
                "Quadratic Discriminant Analysis":
                QuadraticDiscriminantAnalysis(priors=None,
                                              reg_param=0.0,
                                              store_covariance=False,
                                              tol=0.0001),

                "Linear SVM":
                SVC(C=0.025,
                    kernel='linear',
                    degree=3,
                    gamma='auto',
                    coef0=0.0,
                    shrinking=True,
                    probability=False,
                    tol=0.001,
                    cache_size=200,
                    class_weight=None,
                    verbose=False,
                    max_iter=-1,
                    decision_function_shape='ovr',
                    random_state=random.seed(42)),

                "RBF SVM":
                SVC(C=0.025,
                    kernel='rbf',
                    degree=3,
                    gamma='auto',
                    coef0=0.0,
                    shrinking=True,
                    probability=False,
                    tol=0.001,
                    cache_size=200,
                    class_weight=None,
                    verbose=False,
                    max_iter=-1,
                    decision_function_shape='ovr',
                    random_state=random.seed(42)),

                "MLP Classifier":
                MLPClassifier(hidden_layer_sizes=(100, ),
                              activation='relu',
                              solver='adam',
                              alpha=0.0001,
                              batch_size='auto',
                              learning_rate='constant',
                              learning_rate_init=0.001,
                              power_t=0.5,
                              max_iter=200,
                              shuffle=True,
                              random_state=random.seed(42),
                              tol=0.0001,
                              verbose=False,
                              warm_start=False,
                              momentum=0.9,
                              nesterovs_momentum=True,
                              early_stopping=False,
                              validation_fraction=0.1,
                              beta_1=0.9,
                              beta_2=0.999,
                              epsilon=1e-08,
                              n_iter_no_change=10),

                "Extra Trees Classifier":
                ExtraTreesClassifier(n_estimators=100,
                                     criterion='gini',
                                     max_depth=None,
                                     min_samples_split=2,
                                     min_samples_leaf=1,
                                     min_weight_fraction_leaf=0.0,
                                     max_features='auto',
                                     max_leaf_nodes=None,
                                     min_impurity_decrease=0.0,
                                     min_impurity_split=None,
                                     bootstrap=False,
                                     oob_score=False,
                                     n_jobs=n_jobs,
                                     random_state=random.seed(42),
                                     verbose=0,
                                     warm_start=False,
                                     class_weight=None),

                "SGD Classifier":
                SGDClassifier(loss='hinge',
                              penalty='l2',
                              alpha=0.0001,
                              l1_ratio=0.15,
                              fit_intercept=True,
                              max_iter=1000,
                              tol=0.001,
                              shuffle=True,
                              verbose=0,
                              epsilon=0.1,
                              n_jobs=n_jobs,
                              random_state=None,
                              learning_rate='optimal',
                              eta0=0.0,
                              power_t=0.5,
                              early_stopping=False,
                              validation_fraction=0.1,
                              n_iter_no_change=5,
                              class_weight=None,
                              warm_start=False,
                              average=False)
}
