'''
Define all the callbacks on each page
'''

from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import pickle
from sklearn.inspection import plot_partial_dependence
# Read the picked data frame from the project folder
df = pd.read_pickle("app.data")
df_ammenity = pd.read_pickle("ammenity.data")
stack= pickle.load(open('finalized_model_ri.sav', 'rb'))
stackO= pickle.load(open('finalized_model_o.sav', 'rb'))
df_ud = pd.read_csv("l2_detailed_listings.csv", encoding = "UTF-8")

# CARD_KEYS = ['Rental Income', 'Occupancy']

# ALLOWED_TYPES = df_ud.columns.tolist()

# #Occupancy and Rental_Income Outputs
# @app.callback(
#     [Output(key +'_card', 'children') for key in CARD_KEYS],
#     [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
    
#     pred = {[]}
# def update_card_value(value):
    

#     state_df = df.loc[df.state==value].copy()
#     state_df['new_cases'] = state_df['cases'].diff()
#     state_df['new_deaths'] = state_df['deaths'].diff()
#     correlations = state_df.corr().loc[:'residential', 'new_cases']
#     return [dbc.Card(dbc .CardBody(
#         [
#             html.H5(key.title(), className="card-title"),
#             html.P("Correlation: " + str(correlations[key]), className="card-text",
#             ),
#         ]
#     ), color="danger" if correlations[key] < 0 else "success") for key in CARD_KEYS]               

# @app.callback(
#     [Output('line_chart', 'figure'),
#      Output('trend_chart', 'figure')],
#     [Input('state-dropdown', 'value')])
# def display_line_chart(value):


#     features = ['beds']
#     partial_ri = plot_partial_dependence(stack,     
#                 X=df.drop(["occupancy"], axis = 1), # raw predictors data.
#                 features=features, # column numbers of plots we want to show
#                 #feature_names=['Distance', 'Landsize', 'BuildingArea'], # labels on graphs
#                  grid_resolution=10) # number of values to plot on x axis
#     partial_O = plot_partial_dependence(stackO,     
#                                    X=df.drop(["rental_income", "occupancy"], axis = 1), # raw predictors data.
#                                    features=features, # column numbers of plots we want to show
#                                    #feature_names=['Distance', 'Landsize', 'BuildingArea'], # labels on graphs
#                                    grid_resolution=10) # number of values to plot on x axis
#     state_df = df.loc[df.state==value].copy()
#     state_df['new_cases'] = state_df['cases'].diff()
#     state_df['new_deaths'] = state_df['deaths'].diff()
#     return partial_ri, \
#            partial_O \


# @app.callback(
#     [Output(key +'_card', 'children') for key in CARD_KEYS],
#     [Input('state-dropdown', 'value')])
# def update_card_value(value):
#     state_df = df.loc[df.state==value].copy()
#     state_df['new_cases'] = state_df['cases'].diff()
#     state_df['new_deaths'] = state_df['deaths'].diff()
#     correlations = state_df.corr().loc[:'residential', 'new_cases']
#     return [dbc.Card(dbc .CardBody(
#         [
#             html.H5(key.title(), className="card-title"),
#             html.P("Correlation: " + str(correlations[key]), className="card-text",
#             ),
#         ]
#     ), color="danger" if correlations[key] < 0 else "success") for key in CARD_KEYS]

