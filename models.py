from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoCV
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVC, SVR
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from Modules.EDA import train
from typing import Dict
from Modules.EDA import test
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import mean_absolute_error

    def __init__(self, model, name: str, hyperparams={}):
        self.model = model
        self.name = name
        self.hyperparams = hyperparams
        self.bestParams: Dict
        self.time=''


    def fit(self, xTrain, xTest, yTrain, yTest):
        print('Starting ', self.name)

        self.model.fit(xTrain,yTrain)
        self.modelCV = self.model
        self.train_R2 = self.model.r2_score(xTrain, yTrain)
        self.test_R2 = self.model.r2_score(xTest, yTest)
        self.train_MAE = self.mean_absolute_error(yTrain, self.model.predict(xTrain))
        self.test_MAE = self.mean_absolute_error(yTest, self.model.predict(xTest))

     def fitCV(self,xTrain, xTest, yTrain, yTest, cv=2, scoring = 'mae'):
        print('Starting ', self.name)


        grid = GridSearchCV(self.model, self.hyperparams, cv=cv, return_train_score = False, n_jobs=-1, scoring=scoring)
        self.modelCV = grid.fit(xTrain,yTrain)
        self.bestParams = self.modelCV.best_params_
        self.trainScore = self.modelCV.best_estimator_.score(xTrain, yTrain)
        self.testScore = self.modelCV.best_estimator_.score(xTest, yTest)



        self.trainRMSE = self.getRMSE(yTrain, self.modelCV.predict(xTrain))
        self.testRMSE = self.getRMSE(yTest, self.modelCV.predict(xTest))

    def plotHyperParams(self, trainX, testX, trainY, testY, i):


        for name, params in self.hyperparams.items():
            coefs = []
            intercepts = []
            trainScore = []
            testScore = []

            if len(params) < 2:
                continue

            for value in params:
                self.model.set_params(**{name: value})
                print(name, '   Value: ',value)
                self.model.fit(trainX, trainY)
           # intercepts.append(self.model.intercept_)
           # coefs.append(self.model.coef_)
                train_R2.append(self.model.r2_score(trainX, trainY))
                test_R2.append(self.model.r2_score(trainX, trainY))
                train_MAE.append(self.mean_absolute_error(yTrain, self.model.predict(xTrain))
                test_MAE.append(self.mean_absolute_error(yTrain, self.model.predict(xTest))


            plt.plot(params, train_R2, label=r'train set $R^2$')
            plt.plot(params, test_R2, label=r'test set $R^2$')

            plt.xlabel(name+' Value')
            plt.ylabel('R^2 Value')
            plt.title(self.name+' R^2 VS. '+ name)
            plt.legend(loc=4)
            plt.savefig('Output/Hyperparams/'+str(i)+' - '+self.name+' '+name+' '+R2+' .png')
            plt.clf()

            plt.plot(params, train_MAE, label=r'train set $MAE$')
            plt.plot(params, test_MAE, label=r'test set $MAE$')

            plt.xlabel(name+' Value')
            plt.ylabel('Mean Absolute Error')
            plt.title(self.name+' MAE VS. '+ name)
            plt.legend(loc=4)
            plt.savefig('Output/Hyperparams/'+str(i)+' - '+self.name+' '+name+' '+MAE+'.png')
            plt.clf()


    def assembleModels():

        models = {
        'Linear'     : Regression(LinearRegression(n_jobs=-1), 'Linear'),
        'Ridge'      :  Regression(Ridge(), 'Ridge', {'alpha': np.linspace(1,6,100)}),
        'Lasso'      :  Regression(Lasso(), 'Lasso', {'alpha': np.linspace(.001,1,100)}),
        'Elastic Net': Regression(ElasticNet(), 'ElasticNet', {'alpha': np.linspace(.001,1,100), 'l1_ratio': np.linspace(0, 1, 10)}),

        'Random Forest': Regression(RandomForestRegressor(n_jobs=-1), 'Random Forest',
        {   'max_depth': range(5, 20),
            'n_estimators': range(20, 40, 2)}),

        'Gradient Boost': Regression(GradientBoostingRegressor(), 'Gradient Boost',
                   {'learning_rate': np.linspace(.001, 0.1, 10),
                    'n_estimators': range(60, 80, 5),
                    "max_depth": range(1, 15, 4),
                    'loss': ['ls']}), # use feature_importances for feature selection

        'SVM': Regression(SVR(), 'Support Vector Regressor',
                   {'C': np.linspace(1, 10, 30),
                    'gamma': np.linspace(1e-7, 0.1, 30)})
        #Regression((), ''),
        #Regression((), ''),
        }
        return models


    def performRegressions(df: pd.DataFrame, random_state = 0, test_size = .2, target = "rental_income", drop = "Null"):
        models = assembleModels()
        self.random_state = random_state
        self.test_size = test_size
        self.drop = drop
        self.target = target
        y = df[target]
        if drop == "Null":
            x = df.drop(target)
        else:
            x = df.drop(target)
            x = x.drop(drop)
        
        trainTestData = train_test_split(x, y, test_size=self.test_size, random_state= self.random_state)

        #models['Ridge'].plotHyperParams(*trainTestData, 1)
        # models['Lasso'].plotHyperParams(*trainTestData,2)
        # models['Elastic Net'].plotHyperParams(*trainTestData)

        # models['Ridge'].plotHyperParams(*trainTestData)
        # models['SVM'].plotHyperParams(*trainTestData)
        i=0
        for name, model in models.items():
            model.plotHyperParams(*trainTestData,i)
            i+=1

        models['Linear'],         returnValue = lambda: models['Linear'].fit(*trainTestData)
        models['Ridge'],          returnValue = lambda: models['Ridge'].fitCV(*trainTestData)
        models['Lasso'],          returnValue = lambda: models['Lasso'].fitCV(*trainTestData)
        models['Elastic Net'],    returnValue = lambda: models['Elastic Net'].fitCV(*trainTestData)

        models['Random Forest'],  returnValue = lambda: models['Random Forest'].fitCV(*trainTestData)
        models['Gradient Boost'], returnValue = lambda: models['Gradient Boost'].fitCV(*trainTestData)
        models['SVM'],            returnValue = lambda: models['SVM'].fitCV(*trainTestData)

        results = pd.DataFrame([r.__dict__ for r in models.values()]).drop(columns=['model', 'modelCV'] )

        r2_scores = ['train_R2', 'test_R2']
        MAE_scores = ['train_MAE', 'test_MAE']
        

        results.to_excel('Output/Model Results.xlsx')
        print('Finished Regressions')
        return models


def predictSalePrice(dfTest: pd.DataFrame, models: Dict):
    continuousColumns = getColumnType(dfTest, 'Continuous', True)

    x = scaleData(dfTest, continuousColumns)
    predictions = pd.DataFrame()

    for regression in models.values():
        prediction = pd.Series(regression.model.predict(x))
        predictions = ut.appendColumns([predictions, prediction])

    salePrice  = predictions.apply(np.exp, axis=1)
    finalPrediction = salePrice.apply(np.mean, axis=1)

    output = pd.DataFrame({'Id': test['Id'].astype(int), 'SalePrice': finalPrediction})
    output.to_csv('Output/Submission.csv', index=False)
