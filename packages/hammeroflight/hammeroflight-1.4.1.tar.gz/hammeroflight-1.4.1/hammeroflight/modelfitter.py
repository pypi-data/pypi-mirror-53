import pandas as pd
import numpy as np


# ======================= CUSTOM REGRESSORS ===================== ]


def fit_regress(model, xtr, xt, ytr, yt):

    '''
    Author: Aru Raghuvanshi

    This Functions Fits a model with the Train Datasets and
    predicts on a Test Dataset and evaluates its RMSE metric.

    Arguments: 5 - estimator, X_train, X_test, y_train, y_test
    Returns: Dataframe

    '''

    from sklearn.metrics import mean_squared_error

    model.fit(xtr, ytr)
    tr = model.score(xtr, ytr)
    te = model.score(xt, yt)
    # tred = model.predict(xtr)
    # global pred
    pred = model.predict(xt)

    rmse = np.sqrt(mean_squared_error(yt, pred))

    tr = tr * 100
    te = te * 100

    if 1.1 > tr / te > 1.07:
        fit = 'Towards Over-Fit'
    elif 0.89 < tr / te < 0.93:
        fit = 'Towards Under-Fit'
    elif tr / te > 1.1:
        fit = 'Over-Fitted'
    elif tr / te < 0.89:
        fit = 'Under-Fitted'
    else:
        fit = 'Good Fit'

    table = pd.DataFrame({'Training Score': [tr],
                          'Test Score': [te],
                          'RMSE': [rmse],
                          'Fit': [fit]
                          }).T

    table.rename(columns={0: 'Score'}, inplace=True)

    # print('\nPredictions on X_test stored in global variable "pred".')
    return table


# ============================= FIT CLASSIFY ============================ ]


def fit_classify(model, xtr, xt, ytr, yt, k=2):

    '''
    Author: Aru Raghuvanshi

    This Functions Fits a Classifier model with the Train Datasets
    and predicts on a Test Dataset and evaluates metrics via n_splits
    K-fold cross validation.

    Arguments: estimator, X_train, X_test, y_train, y_test, n_splits
    Returns: Dataframe
    '''

    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.metrics import classification_report

    model.fit(xtr, ytr)
    tr = model.score(xtr, ytr)
    te = model.score(xt, yt)
    # tred = model.predict(xtr)
    # global pred
    pred = model.predict(xt)

    kf = KFold(n_splits=k, random_state=22)
    sc = np.mean(cross_val_score(model, xtr, ytr, cv=kf))

    cr = classification_report(yt, pred)

    tr = tr * 100
    te = te * 100

    if 1.1 > tr / te > 1.07:
        fit = 'Towards Over-Fit'
    elif 0.89 < tr / te < 0.93:
        fit = 'Towards Under-Fit'
    elif tr / te > 1.1:
        fit = 'Over-Fitted'
    elif tr / te < 0.89:
        fit = 'Under-Fitted'
    else:
        fit = 'Good Fit'

    table = pd.DataFrame({'Training Score': [tr],
                          'Test Score': [te],
                          'CV-Score': [sc],
                          'Fit': [fit]
                          }).T

    table.rename(columns={0: 'Score'}, inplace=True)

    print(cr)
    # print('\nPredictions on X_test stored in global variable "pred".')
    return table



# ------------------------------ GOOODNESS OF FIT -----------------------]


def goodness_fit(tr, te):
    '''
    Author: Aru Raghuvanshi

    The functions takes train score and testscore and returns
    goodness of fit in a DataFrame.

    Arguments: trainscore, testscore
    Returns: Dataframe
    '''

    tr = tr * 100
    te = te * 100

    if tr / te > 1.61:
        fit = 'Badly Over-Fitted'
    elif 1.6 > tr / te > 1.11:
        fit = 'Over-Fitted'
    elif 1.1 > tr / te > 1.07:
        fit = 'Towards Over-Fit'

    elif tr / te < 0.829:
        fit = 'Badly Under-Fitted'
    elif 0.83 < tr / te < 0.891:
        fit = 'Under Fitted'
    elif 0.89 < tr / te < 0.93:
        fit = 'Towards Under-Fit'

    else:
        fit = 'Good Fit'

    val = pd.DataFrame({'Training Score': [tr], 'Test Score': [te], 'Result': [fit]}).T
    val.rename(columns={'index': 'Score', 0: 'Fitting'}, inplace=True)

    return val


# --------------------------------------- R PLOT ---------------------------]


def r_plot(clf, a, b):

    '''
    Author: Aru Raghuvanshi

    This functions takes a single feature and target variable, and plots
    the regression line on that  data to see the fit of the model. The shapes
    of input data should X.shape=(abc,1) and y.shape=(abc, ).

    Argument: estimator, X, y
    Returns: Plot
    '''

    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    a = np.asarray(a).reshape(-1,1)

    X_grid = np.arange(min(a), max(a), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))

    plt.figure(figsize=(14, 6))
    plt.scatter(a, b, color='purple')
    clf.fit(a, b)
    plt.plot(X_grid, clf.predict(X_grid), color='black')

    plt.title('Fitting Plot', fontsize=16)
    plt.xlabel('Predictor Feature', fontsize=14)
    plt.ylabel('Target Feature', fontsize=14)

    plt.show()