import numpy as np
import pandas as pd

def reg_comparator(Xt, xt, Yt, yt):
    '''
    Author: Aru Raghuvanshi

    Function takes 4 arguments of datasets split by train test split
    method and fits 5 regressive machine learning algos of LinearReg,
    Random Forest, Decision Tree, XGBoost and LightGBM Regressors and
    returns a dataframe with metrics.

    Arguments: 4 products of train test split method
    Returns: Dataframe
    '''

    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor

    models = []
    models.append(('LR', LinearRegression()))
    models.append(('DTR', DecisionTreeRegressor()))
    models.append(('RFR', RandomForestRegressor()))
    models.append(('XGR', XGBRegressor()))
    models.append(('LGR', LGBMRegressor()))

    results = []
    names = []

    for name, model in models:
        model.fit(Xt, Yt)
        prd = model.predict(xt)
        trs = model.score(Xt, Yt)
        tes = model.score(xt, yt)
        RMSE = np.round(np.sqrt(mean_squared_error(yt, prd)), 4)
        names.append(name)

    allscores = pd.DataFrame({'LR': [trs, tes, RMSE], 'DTR': [trs, tes, RMSE],
                              'RFR': [trs, tes, RMSE], 'XGR': [trs, tes, RMSE],
                              'LGR': [trs, tes, RMSE], 'Scores': ['Training', 'Test', 'RMSE']})

    allscores.set_index('Scores', drop=True, inplace=True)
    allscores.plot(kind='bar', rot=0, figsize=(14, 4), colormap='Purples')
    return allscores


def clf_comparator(Xt, xt, Yt, yt, k):
    '''
        Author: Aru Raghuvanshi

        Function takes 4 arguments of datasets split by train test split
        method along with one of KFold value 'k', and fits 5 classifier
        machine learning algos of LogisticReg, Random Forest, Decision Tree,
        XGBoost and LightGBM classifiers and returns a dataframe with metrics.

        Arguments: four products of train test split method and kfold 'k'
        Returns: Dataframe
        '''


    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from sklearn.model_selection import KFold, cross_val_score
    import seaborn as sns
    sns.set()

    models = []
    models.append(('LG', LogisticRegression(solver='lbfgs')))
    models.append(('DT', DecisionTreeClassifier()))
    models.append(('RF', RandomForestClassifier(n_estimators=100)))
    models.append(('XG', XGBClassifier()))
    models.append(('LGB', LGBMClassifier()))

    results = []
    names = []

    for name, model in models:
        model.fit(Xt, Yt)
        prd = model.predict(xt)
        Kfold = KFold(n_splits=k, random_state=42)
        cv_result = np.mean(cross_val_score(model, X_train, y_train, cv=Kfold, scoring='accuracy'))
        results.append(cv_result)

        tes = model.score(xt, yt)
        names.append(name)

    allscores = pd.DataFrame({'LogReg': [cv_result, tes], 'DTClass': [cv_result, tes], 'RFClass': [cv_result, tes],
                              'XGClass': [cv_result, tes], 'LGBMClass': [cv_result, tes],
                              'Score': ['Training', 'Test']})

    allscores.set_index('Score', drop=True, inplace=True)
    allscores.plot(kind='bar', rot=0, figsize=(14, 4), colormap='Greens')
    return allscores