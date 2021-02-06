from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler
from typing import Dict, Callable
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import mean_absolute_error, r2_score

class Models:

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
           self.train_R2 = r2_score(yTrain, self.model.predict(xTrain))
           self.test_R2 = r2_score(yTest, self.model.predict(xTest))
           self.train_MAE = mean_absolute_error(yTrain, self.model.predict(xTrain))
           self.test_MAE = mean_absolute_error(yTest, self.model.predict(xTest))

    def fitCV(self,xTrain, xTest, yTrain, yTest, cv=2, scoring = 'neg_mean_absolute_error'):
           print('Starting ', self.name)


           grid = GridSearchCV(self.model, self.hyperparams, cv=cv, return_train_score = False, n_jobs=-1, scoring=scoring)
           self.modelCV = grid.fit(xTrain,yTrain)
           self.bestParams = self.modelCV.best_params_
           self.trainScore = self.modelCV.best_estimator_.score(xTrain, yTrain)
           self.testScore = self.modelCV.best_estimator_.score(xTest, yTest)
           self.train_R2 = r2_score(yTrain, self.modelCV.best_estimator_.predict(xTrain))
           self.test_R2 = r2_score(yTest, self.modelCV.best_estimator_.predict(xTest))
           self.train_MAE = mean_absolute_error(yTrain, self.modelCV.best_estimator_.predict(xTrain))
           self.test_MAE = mean_absolute_error(yTest, self.modelCV.best_estimator_.predict(xTest))


            

    def plotHyperParams(self, trainX, testX, trainY, testY, i):


           for name, params in self.hyperparams.items():
               coefs = []
               intercepts = []
               train_R2 = []
               test_R2 = []
               train_MAE = []
               test_MAE = []

               if len(params) < 2:
                   continue

               for value in params:
                   self.model.set_params(**{name: value})
                   print(name, '   Value: ',value)
                   self.model.fit(trainX, trainY)
               # intercepts.append(self.model.intercept_)
               # coefs.append(self.model.coef_)
                   train_R2.append(r2_score(trainY, self.model.predict(trainX)))
                   test_R2.append(r2_score(testY, self.model.predict(testX)))
                   train_MAE.append(mean_absolute_error(trainY, self.model.predict(trainX)))
                   test_MAE.append(mean_absolute_error(testY, self.model.predict(testX)))


               plt.plot(params, train_R2, label=r'train set $R^2$')
               plt.plot(params, test_R2, label=r'test set $R^2$')

               plt.xlabel(name+' Value')
               plt.ylabel('R^2 Value')
               plt.title(self.name+' R^2 VS. '+ name)
               plt.legend(loc=4)
               plt.savefig('Output/'+str(i)+' - '+self.name+' '+name+' R2.png')
               plt.clf()

               plt.plot(params, train_MAE, label=r'train set $MAE$')
               plt.plot(params, test_MAE, label=r'test set $MAE$')

               plt.xlabel(name+' Value')
               plt.ylabel('Mean Absolute Error')
               plt.title(self.name+' MAE VS. '+ name)
               plt.legend(loc=4)
               plt.savefig('Output/'+str(i)+' - '+self.name+' '+name+' MAE.png')
               plt.clf()

    #@staticmethod
    def assembleModels(self):
           models = {
           'Linear'     : Models(LinearRegression(n_jobs=-1), 'Linear'),
           'Ridge'      :  Models(Ridge(normalize = True), 'Ridge', {'alpha': np.linspace(.001,1,100)}),
           'Lasso'      :  Models(Lasso(alpha = 1,tol = 0.00001, max_iter = 10000, normalize = True), 'Lasso', {'alpha': np.linspace(.001,1,100)}),
           'Elastic Net':  Models(ElasticNet(), 'ElasticNet', {'alpha': np.linspace(.001,1,100), 'l1_ratio': np.linspace(0, 1, 10)}),

            'Random Forest': Models(RandomForestRegressor(n_jobs=-1), 'Random Forest',
                        {'n_estimators': range(100, 1000, 300),
                        "max_features":["auto", "sqrt", "log2"],
                        "max_depth": range(1, 15, 4)}),
    
            'Gradient Boost': Models(GradientBoostingRegressor(), 'Gradient Boost',
                       {'learning_rate': np.linspace(.001, 0.1, 10),
                        'n_estimators': range(100, 1000, 300),
                        "max_features":["auto", "sqrt", "log2"],
                        "max_depth": range(1, 15, 4),
                        'loss': ['ls', 'lad']}), # use feature_importances for feature selection
    
            'SVM': Models(SVR(), 'Support Vector Regressor',
                       {'C': np.linspace(1, 10, 3),
                        'gamma': ['scale','auto'],
                        'kernel': ['linear']})
            #Regression((), ''),
            #Regression((), ''),
           }
           return models

    def getExecutionTime(self, fun: Callable):
        start_time = time.time()
        returnValue = fun()

        timeUsed = time.time() - start_time
        seconds = timeUsed % 60
        minutes = int(timeUsed // 60)

        if seconds < 1:
            seconds = round(seconds , 2)
        else:
            seconds = int(seconds)


        timeString = 'Minutes: '+ str(minutes)+ '  Seconds: '+ str(seconds)
        print(timeString,'\n')
        return timeString, returnValue   

    def performRegressions(self, df: pd.DataFrame, random_state = 0, test_size = .2, target = 'rental_income', drop = 'Null'):
           models = self.assembleModels()
           self.random_state = random_state
           self.test_size = test_size
           self.drop = drop
           self.target = target
           y = df[self.target]
           print(df.columns)
           
           if drop == "Null":
               X = df.drop(target, axis=1)
           else:
               X = df.drop(target, axis=1)
               X = X.drop(drop, axis=1)
            
           trainTestData = train_test_split(X, y, test_size=self.test_size, random_state= self.random_state)


           i=0
           for name, model in models.items():
               model.plotHyperParams(*trainTestData,i)
               i+=1

           models['Linear'].time,         returnValue = self.getExecutionTime(lambda: models['Linear'].fit(*trainTestData))
           models['Ridge'].time,          returnValue = self.getExecutionTime(lambda: models['Ridge'].fitCV(*trainTestData))
           models['Lasso'].time,          returnValue = self.getExecutionTime(lambda: models['Lasso'].fitCV(*trainTestData))
           models['Elastic Net'].time,    returnValue = self.getExecutionTime(lambda: models['Elastic Net'].fitCV(*trainTestData))

           models['Random Forest'].time,  returnValue = self.getExecutionTime(lambda: models['Random Forest'].fitCV(*trainTestData))
           models['Gradient Boost'].time, returnValue = self.getExecutionTime(lambda: models['Gradient Boost'].fitCV(*trainTestData))
           models['SVM'].time,            returnValue = self.getExecutionTime(lambda: models['SVM'].fitCV(*trainTestData))

           results = pd.DataFrame([r.__dict__ for r in models.values()]).drop(columns=['model', 'modelCV'] )

           
           results.to_excel('Target ' + self.target + ' Drop ' + self.drop +' Model Results.xlsx')
           print('Finished Regressions')
           return models


    def predictOutcomes(dfTest: pd.DataFrame, models: Dict):
        
           predictions = pd.DataFrame()

           for regression in models.values():
                prediction = pd.Series(regression.model.predict(x))
                predictions = pd.concat([predictions, prediction], axis = 1)

        #Outcome  = predictions.apply(np.exp, axis=1)
        #finalPrediction = salePrice.apply(np.mean, axis=1)

           output = pd.DataFrame({'Id': test['Id'].astype(int), self.target: predictions})
           output.to_csv('Submission.csv', index=False)
