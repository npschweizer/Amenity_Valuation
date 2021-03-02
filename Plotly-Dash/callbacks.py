'''
Define all the callbacks on each page
'''
import plotly.graph_objects as go
import base64
import matplotlib.pyplot as plt
import io
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import numpy as np
import pickle
from sklearn.inspection import plot_partial_dependence
from mlxtend.regressor import StackingCVRegressor
from alepython import ale_plot
pd.set_option('display.max_columns', None)
df = pd.read_pickle("model_data.data")
df_amenity = pd.read_pickle("amenity.data")
pd.options.display.max_seq_items = None
print(df.columns)
stack= pickle.load(open('ridge_ri.sav', 'rb'))
stackO= pickle.load(open('finalized_model_o.sav', 'rb'))
df_ud = pd.read_csv("l2_detailed_listings.csv", encoding = "UTF-8")
CARD_KEYS = ['Rental Income', 'Occupancy']
Amenity_Names = df_amenity.columns.tolist()
NUMERICAL_TYPES = df_ud.columns.tolist()
for name in Amenity_Names:
    if name in NUMERICAL_TYPES:
        NUMERICAL_TYPES.remove(name)
NUMERICAL_TYPES.remove("occupancy")
NUMERICAL_TYPES.remove("rental_income")
NUMERICAL_TYPES.remove("neighborhood")
if 'Laptop friendly workspace' in NUMERICAL_TYPES:
    NUMERICAL_TYPES.remove("Laptop friendly workspace")
NUMERICAL_TYPES.remove("cancellation_policy")
NUMERICAL_TYPES.remove("property_type")
NUMERICAL_TYPES.remove("instant_book_enabled")
#print(NUMERICAL_TYPES)
####Homepage main feature plots

#Histogram
@app.callback(
    Output('main-features-histogram', 'src'),
    #Output('ale', 'children'),
    [Input('numerical_types', 'value')])
def update_amenity_ale(value):
    fig = px.histogram(df_ud, x=value,
                   title=str('Distribution of ' + value),
                   labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   log_y=True, # represent bars with log scale
                   color_discrete_sequence=['indianred'] # color of histogram bars
                   )
    return fig

#ALE Plot
@app.callback(
    Output('example', 'src'),
     #Output('ale', 'children'),
    [Input('numerical_types', 'value')])
def update_amenity_ale(amenity_checkbox_ale):
    buf = io.BytesIO()
    plot = ale_plot(model=stack,train_set= df.drop(["occupancy", "rental_income"], axis =1),
         features= 'bedrooms',
         bins=20, 
         monte_carlo=True).get_figure().savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    return "data:image/png;base64,{}".format(data)

#Amenity pages
@app.callback(
    Output('amenity-histogram', 'figure'),
    [Input('numerical_types', 'value')])
def update_amenity_hist(value):
    return px.histogram(df_ud, x="price",
                   title=str('Distribution of ' + value),
                   color= str(value),
                   labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   marginal="violin",
                   color_discrete_sequence=px.colors.qualitative.Bold # color of histogram bars
                   )
    #return fig.show()

#Occupancy and Rental_Income Outputs
@app.callback(
    Output('Rental_Income', 'children'),
    [Input('amenity_checkbox', 'value')],
    [Input('cancellation_policy', 'value')],
    [Input('property_type', 'value')],
    [Input('neighborhood', 'value')],
    [Input('instant_book_enabled', 'value')],
    Input('submit-button', 'n_clicks'),
    [Input("{}".format(_), 'value') for _ in NUMERICAL_TYPES])
def update_card_value(amenity_checkbox,property_type,cancellation_policy, neighborhood,instant_book_enabled, *vals):
    pred = pd.DataFrame(np.zeros((1,len(df.columns.drop(["rental_income","occupancy"])))),columns=df.drop(["rental_income","occupancy"],axis=1).columns)
    ri=np.median(df.rental_income)
    for i in df_ud.cancellation_policy.unique():
        if i in cancellation_policy:
            pred[str('cancellation_policy__' + i)] = 1
        else:
            pred[str('cancellation_policy__' + i)] = 0
    if instant_book_enabled =="True":
        pred['instant_book_enabled__True'] = 1
        pred['instant_book_enabled__False'] = 0
    else:
        pred['instant_book_enabled__True'] = 0
        pred['instant_book_enabled__False'] = 1
    for i in df_ud.property_type.unique():
        if i in property_type:
            pred[str('property_type__' + i)] = 1
        else:
            pred[str('property_type__' + i)] = 0
    for i in df_ud.neighborhood.unique():
        if i in neighborhood:
            pred[str('neighborhood__' + i)] = 1
        else:
            pred[str('neighborhood__' + i)] = 0
    for i in range(len(NUMERICAL_TYPES)):
        if vals[i] != "":
            pred[NUMERICAL_TYPES[i]] = vals[i]
    for i in df_amenity.columns:
        if i in amenity_checkbox:
            pred[i] = 1
        else:
            pred[i] = 0
    #print(pred)
    pred.fillna(0, inplace=True)
    #print(stack.predict(pred))
    ri = stack.predict(pred)
    return dash_table.DataTable(
        id='ri-table',
        columns=[{"name": i, "id": i} 
                 for i in pred.columns],
        data=pred.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )

@app.callback(
    Output('Occupancy', 'children'),
    [Input('amenity_checkbox', 'value')],
    [Input('neighborhood', 'value')],
    [Input("{}".format(_), 'value') for _ in NUMERICAL_TYPES])
def update_card_value(amenity_checkbox, neighborhood, *vals):
    pred = pd.DataFrame(columns=df.columns)
    pred.append(pd.Series(), ignore_index=True)
    oc=np.median(df.occupancy)
    for i in df_ud.neighborhood.unique():
        if i in neighborhood:
            pred.at[0,str('neighborhood__' + neighborhood)] = 1
        else:
            pred.at[0,str('neighborhood__' + neighborhood)] = 0
    for i in range(len(NUMERICAL_TYPES)):
        pred.at[0,NUMERICAL_TYPES[i]] = vals[i]
    for i in df_amenity.columns:
        if i in amenity_checkbox:
            pred.at[0,i] = 1
        else:
            pred.at[0,i] = 0
    #print(stack.predict(pred.iloc[0]))
    #ri = stack.predict(pred.iloc[0])
    return str(oc)




    

    # dbc.Card(dbc.CardBody(
    #      [
    #          html.H5("Rental Income"),
    #          html.P("Predicted Rental Income: " + str(ri),
    #          ),
    #      ]
    #  ), color= "success")

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

