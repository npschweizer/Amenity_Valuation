from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from mlxtend.regressor import StackingRegressor
import pickle
import pandas as pd
import numpy as np
X = pd.read_pickle("model_data.data")

imputer=KNNImputer()
mlr=LinearRegression()
ridge=Ridge()
lasso=Lasso()
ElasticNet=ElasticNet()
rf=RandomForestRegressor()
gb=GradientBoostingRegressor()
regressors= [ridge,lasso,ElasticNet,rf,gb]
stack=StackingRegressor(regressors=regressors,
                        meta_regressor=mlr,
                        use_features_in_secondary=True,
                        store_train_meta_features=True,)


params= {'lasso__alpha': np.linspace(.001,100,100),
         'ridge__alpha': np.linspace(.001,100,100),
         'ElasticNet__alpha': np.linspace(.001,100,100),
         'ElasticNet__l1_ratio': np.linspace(0, 1, 10),
         'rf__n_estimators': range(100, 1000, 300),
         'rf__max_features': ["auto", "sqrt", "log2"],
         'rf__max_depth': range(1,15,4),
         'gb__learning_rate':np.linspace(.001,.1,10),
         'gb__n_estimators': range(100, 1000, 300),
         "gb__max_features":["auto", "sqrt", "log2"],
         "gb__max_depth": range(1, 15, 4)}


                              
pipeline_ri=Pipeline([('imputer', imputer),
                     ('stack', stack)])
grid_search_stack = GridSearchCV(
       estimator=pipeline_ri,
       cv = 5,
       param_grid=params,
       return_train_score=True,
       scoring= 'neg_mean_absolute_error', 
       verbose=2)

grid_search_stack=grid_search_stack.fit(X.drop(["rental_income","occupancy"], axis=1), X.rental_income)

filename = 'Plotly-Dash/finalized_model_ri.sav'
pickle.dump(grid_search_stack, open(filename, 'wb'))