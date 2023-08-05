import pandas as pd
import numpy as np

# VERSION 1.2.1

### DROP, BINARIZE OR ENCODE


def cleanandencode(val):

    '''
    Author: Aru Raghuvanshi

    This functions takes a dataframe and drops columns from it if it has just one
    unique value (recurring values or constant). If a column has two values, it
    binarizes them and OneHotEncodes the remaining.

    Arguments: Dataframe
    Returns: Dataframe
    '''

    from sklearn.preprocessing import LabelBinarizer

    lb = LabelBinarizer()
    for i in val.columns:
        count = val[i].nunique()
        if count == 1:
            val.drop(i, axis=1, inplace=True)
        elif count == 2:
            val[i] = lb.fit_transform(val[i])
        elif val[i].dtype == 'object':
            val = pd.get_dummies(val, columns=[i], drop_first=True)

    return val


#### FEATURE SELECTOR

def featureselector(val, var, coef):

    '''
    Author: Aru Raghuvanshi

    This function takes three parameters val and var and correlation coefficient
    where val can be a dataframe and var can be an independent variable from that 
    dataframe. It returns a new dataframe with all those variables dropped whose 
    correlation is lower than coefficient with the independent variable var.

    Arguments: DataFrame, variable of comparison, value of coef below to drop.
    Returns: DataFrame
    '''

    corr_status = val[val.columns].corr()[var]
    to_drop = {}
    for k, v in list(abs(corr_status).items()):
        if v < coef:
            to_drop[k] = v
            val_1 = val.drop(list(to_drop), axis=1)

    return val_1



#### Data Qualiity Report


def qualityreport(val):
    '''

    Author: Aru Raghuvanshi

    This function displays various attributes of a dataframe
    imported from an external file like csv, excel etc. and
    doesn't return a dataframe but only displays.

    Arguments: Dataframe
    Returns: Dataframe

    '''

    dtypes = val.dtypes
    rows = val.T.apply(lambda x: x.count(), axis=1)
    nuniq = val.T.apply(lambda x: x.nunique(), axis=1)
    total = val.isna().sum()
    count = len(total)
    percent = total / count * 100
    mean = val.T.apply(lambda x: x.mean() if (x.dtype == 'float64' or x.dtype == 'int64') else x.mode()[0], axis=1)

    qualitydf = pd.concat([rows, total, percent, mean, nuniq, dtypes],
                          keys=['Rows', 'Missing', 'Missing%', 'Mean-Mode', 'Unique', 'Dtype'], axis=1)

    a = len(qualitydf[qualitydf.Dtype == 'object'])
    b = len(qualitydf[qualitydf.Dtype == 'int64'])
    c = len(qualitydf[qualitydf.Dtype == 'float64'])

    catfeat = a
    numfeat = b + c

    print(f'Categorical Features: {catfeat} | Numerical Features: {numfeat} \
            \nDataset Shape: {val.shape}  | Integrity : {np.round(100 - sum(percent), 1)} %')

    return qualitydf



#### CUSTOM REGRESSORS


def fit_regress(model, Xtrain, Xtest, ytrain, ytest):

    '''
    Author: Aru Raghuvanshi

    This Functions Fits a model with the Train Datasets and
    predicts on a Test Dataset and evaluates its RMSE metric.

    Arguments: 5 - estimator, X_train, X_test, y_train, y_test
    Returns: Train score, Test score, RMSE
    --ASR
    '''

    from sklearn.metrics import mean_squared_error

    model.fit(Xtrain, ytrain)
    tr = model.score(Xtrain, ytrain)
    te = model.score(Xtest, ytest)
    tred = model.predict(Xtrain)
    pred = model.predict(Xtest)

    rmse = np.sqrt(mean_squared_error(ytest, pred))

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

    table = pd.DataFrame({'Training Score': [tr], 'Test Score': [te], 'RMSE': [rmse],
                          'Fit': [fit]}).T
    table.rename(columns={0: 'Score'}, inplace=True)

    print('\nPredictions stored in global variable "pred".')
    return table




def fit_classify(model, Xtrain, Xtest, ytrain, ytest, k=2):
    '''
    Author: Aru Raghuvanshi

    This Functions Fits a Classifier model with the Train Datasets
    and predicts on a Test Dataset and evaluates metrics via n_splits
    K-fold cross validation.

    Arguments: estimator, X_train, X_test, y_train, y_test, n_splits
    Returns: Train score, Test score, accuracy score, and displays
             classification report.
    '''

    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.metrics import classification_report

    model.fit(Xtrain, ytrain)
    tr = model.score(Xtrain, ytrain)
    te = model.score(Xtest, ytest)
    tred = model.predict(Xtrain)
    global pred
    pred = model.predict(Xtest)

    kf = KFold(n_splits=k, random_state=22)
    sc = np.mean(cross_val_score(model, Xtrain, ytrain, cv=kf))

    cr = classification_report(ytest, pred)

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

    table = pd.DataFrame({'Training Score': [tr], 'Test Score': [te], 'CV-Score': [sc],
                          'Fit': [fit]}).T
    table.rename(columns={0: 'Score'}, inplace=True)

    print(cr)
    print('\nPredictions stored in global variable "pred".')
    return table


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