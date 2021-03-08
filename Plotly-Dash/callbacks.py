'''
Define all the callbacks on each page
'''
import plotly.graph_objects as go
import base64
import matplotlib.pyplot as plt
import io
from dash.dependencies import Input, Output, State
from app import app
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import pickle
from eli5 import explain_prediction
from eli5.formatters.html import format_as_html
from sklearn.inspection import plot_partial_dependence
from mlxtend.regressor import StackingCVRegressor
pd.set_option('display.max_columns', None)
df = pd.read_pickle("model_data.data")
df_amenity = pd.read_pickle("amenity.data")
pd.options.display.max_seq_items = None
print('w')
stack= pickle.load(open('finalized_model_ri.sav', 'rb'))
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
print(NUMERICAL_TYPES)
####Homepage main feature plots

#Histogram
@app.callback(
    Output('main-features-histogram', 'figure'),
    #Output('ale', 'children'),
    [Input('numerical_types', 'value')])
def update_amenity_ale(value):
    return px.histogram(df, x=value,
                   title=str('Distribution of ' + value),
                   #labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   #log_y=True, # represent bars with log scale
                   color_discrete_sequence=px.colors.qualitative.Bold # color of histogram bars
                   )


#ALE Plot
# @app.callback(
#     Output('example', 'src'),
#      #Output('ale', 'children'),
#     [Input('numerical_types', 'value')])
# def update_amenity_ale(amenity_checkbox_ale):
#     buf = io.BytesIO()
#     plt.plot([1, 2, 3, 4])
#     plt.ylabel('some numbers')
#     plt.get_figure().savefig(buf, format='png')
#     data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#     return "data:image/png;base64,{}".format(data)

#Amenity pages
@app.callback(
    Output('amenity-histogram', 'figure'),
    [Input('amenity_dist', 'value')])
def update_amenity_hist(value):
    return px.histogram(df_ud, x="price",
                   title=str('Percent Distribution of ' + value),
                   color= str(value),
                   #labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   marginal="violin",
                   #histnorm='percent',
                   color_discrete_sequence=px.colors.qualitative.Bold # color of histogram bars
                   )
    #return fig.show()
#print("change")
#Occupancy and Rental_Income Outputs
@app.callback(
    Output('Rental_Income', 'children'),
    [Input('amenity_checkbox', 'value')],
    [Input('cancellation_policy', 'value')],
    [Input('property_type', 'value')],
    [Input('neighborhood', 'value')],
    [Input('instant_book_enabled', 'value')],
    [Input("{}".format(_), 'value') for _ in NUMERICAL_TYPES])
def update_card_value(amenity_checkbox,cancellation_policy,property_type, neighborhood,instant_book_enabled, *vals):
    pred = pd.DataFrame(np.zeros((1,len(df.columns.drop(["rental_income","occupancy"])))),columns=df.drop(["rental_income","occupancy"],axis=1).columns)
    #pred = pd.DataFrame(columns=df.drop(["rental_income","occupancy"],axis=1).columns)
    #pred.append(pd.Series(), ignore_index=True)
    ri=np.median(df.rental_income)
    print(vals)
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
        if vals[i] != None:
            pred[NUMERICAL_TYPES[i]] = vals[i]
        else:
            pred[NUMERICAL_TYPES[i]] = 0
        print(str(NUMERICAL_TYPES[i]) + " " + str(vals[i]))
    for i in df_amenity.columns:
        if i in amenity_checkbox:
            pred[i] = 1
        else:
            pred[i] = 0
    feature_names=df.drop(["rental_income", "occupancy"], axis=1).columns.tolist()
    ri = stack.predict(pred)
    print(ri)
    #pred.iloc[0]=stack.named_steps['imputer'].transform(pred)
    #for i in range(len(NUMERICAL_TYPES)):
    #    print(str(NUMERICAL_TYPES[i]) + " " + str(vals[i]))
    #print(pred)
    #fig=eli5.explain_prediction(stack.named_steps['R'], pred.iloc[-1], top=20, feature_names = feature_names)
    print(format_as_html(explain_prediction(stack.named_steps['R'], pred.iloc[0], top=20, feature_names = feature_names)))
    return ri#, format_as_html(explain_prediction(stack.named_steps['R'], pred.iloc[0], top=20, feature_names = feature_names))



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


    #dash_table.DataTable(
    #     id='ri-table',
    #     columns=[{"name": i, "id": i} 
    #              for i in pred.columns],
    #     data=pred.to_dict('records'),
    #     style_cell=dict(textAlign='left'),
    #     style_header=dict(backgroundColor="paleturquoise"),
    #     style_data=dict(backgroundColor="lavender")
    #)