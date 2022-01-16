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
import os
from eli5 import explain_prediction
from eli5.formatters.html import format_as_html
from eli5.formatters.as_dataframe import format_as_dataframe
from sklearn.inspection import plot_partial_dependence
from mlxtend.regressor import StackingCVRegressor
from sklearn.inspection import partial_dependence
import boto3
import botocore


AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')

def download_file(file_name, output):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY
                        )
    print('Output is ' + output)
    print('File name is ' + file_name)
    try:
        s3.Bucket(S3_BUCKET).download_file(file_name, output)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    return output


pd.set_option('display.max_columns', None)
df = pd.read_pickle(download_file(f'model_data.data', 'model_data.data'))
df_amenity = pd.read_pickle(download_file(f"amenity.data", 'amenity.data'))
pd.options.display.max_seq_items = None
stack= pickle.load(open(download_file(f'finalized_model_ri.sav', 'finalized_model_ri.sav'), 'rb'))
stackO= pickle.load(open(download_file(f'finalized_model_O.sav', 'finalized_model_O.sav'), 'rb'))
df_ud = pd.read_csv(download_file(f"l2_detailed_listings.csv", 'l2_detailed_listings.csv'), encoding = "UTF-8")
df_words= pd.read_csv(download_file(f"l1_detailed_listings.csv", 'l1_detailed_listings.csv'), encoding = "UTF-8")
df_words=df_words.drop("status", axis=1)
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


#ICE Plot
# @app.callback(
#     Output('ICE', 'src'),
#      #Output('ale', 'children'),
#     [Input('numerical_types', 'value')])
# def update_amenity_ale(value):
#     buf = io.BytesIO()
#     plot=plot_partial_dependence(stack,     
#         X=df.drop(["occupancy", "rental_income"], axis = 1), # raw predictors data.
#             features=[str(value)],
#             #ax=ax,# column numbers of plots we want to show
#             kind='individual'
#             #feature_names=['Distance', 'Landsize', 'BuildingArea'], # labels on graphs
#             #grid_resolution=10,
#             ) # number of values to plot on x axis
#     #plt.ylabel('some numbers')
#     plot.figure_.savefig(buf, format='png')
#     data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#     return "data:image/png;base64,{}".format(data)
@app.callback(
    Output('ICE', 'figure'),
    [Input('numerical_types', 'value')],
    [Input('ICE_target', 'value')])
def update_amenity_ale(numerical_types, ICE_target):
    mask = np.random.choice([False, True], df.shape[0], p=[0.95, 0.05])
    graph_df=df[mask]
    if ICE_target == 'rental_income':
        model=stack
    else:
        model=stackO
    plot = partial_dependence(model,     
        X=graph_df.drop(["occupancy", "rental_income"], axis = 1), # raw predictors data.
        features=[numerical_types],
        #ax=ax,# column numbers of plots we want to show
        kind='individual',
        #feature_names=str(numerical_types), # labels on graphs
        #grid_resolution=10,
        ) # number of values to plot on x axis
    fig=px.line(x=plot['values'][0].tolist(), y=plot.individual[0].tolist(), 
                color_discrete_sequence= px.colors.qualitative.Antique,
                title=str(' Individual Conditional Effects Plot for ' + numerical_types + ' Feature'))
    fig.update_layout(showlegend=False,
        xaxis_title=str(numerical_types),
        yaxis_title=str(ICE_target))
    return fig

#Amenity pages
@app.callback(
    Output('amenity-histogram', 'figure'),
    [Input('amenity_dist', 'value')])
def update_amenity_hist(value):
    return px.histogram(df_ud, x="Nightly Price",
                   title=str('Distribution of ' + value),
                   color= str(value),
                   #labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   marginal="violin",
                   #histnorm='percent',
                   color_discrete_sequence=px.colors.qualitative.Bold # color of histogram bars
                   )

@app.callback(
    Output('image', 'src'),
    Output('no_image', 'src'),
    [Input('amenity_dist', 'value')])
def update_image_src(value):
    am_image_value=value
    print('/static/' + am_image_value+ '.png')
    img=download_file(str('static/' + am_image_value + '.png'), str('static/' + am_image_value + '.png'))
    no_img=download_file(f'static/main.png', f'static/main.png')
    return 'static/' + am_image_value + '.png', 'static/main.png'

#Occupancy and Rental_Income Outputs
@app.callback([
    Output('Rental_Income', 'children'),
    Output('income-table', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('amenity_checkbox', 'value')],
    [State('cancellation_policy', 'value')],
    [State('property_type', 'value')],
    [State('neighborhood', 'value')],
    [State('instant_book_enabled', 'value')],
    [State("{}".format(_), 'value') for _ in NUMERICAL_TYPES])
def update_card_value(n_clicks, amenity_checkbox,cancellation_policy,property_type, neighborhood,instant_book_enabled, *vals):
    pred = pd.DataFrame(np.zeros((1,len(df.columns.drop(["rental_income","occupancy"])))),columns=df.drop(["rental_income","occupancy"],axis=1).columns)
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
    for i in range(len(NUMERICAL_TYPES)):
        print(str(NUMERICAL_TYPES[i]) + " " + str(vals[i]))
    #fig=eli5.explain_prediction(stack.named_steps['R'], pred.iloc[-1], top=20, feature_names = feature_names)
    exp=format_as_dataframe(explain_prediction(stack.named_steps['R'], pred.iloc[0], top=30, feature_names = feature_names))
    exp=exp[exp.feature.isin(Amenity_Names)]
    #print(exp)
    exp = dash_table.DataTable(
         id='ri-table',
         columns=[{"name": i, "id": i} 
                  for i in exp.drop(['target'],axis=1).columns],
         data=exp.to_dict('records'),
         style_cell=dict(textAlign='left'),
         style_header=dict(backgroundColor="paleturquoise"),
         style_data=dict(backgroundColor="lavender")
    )
    #print(exp)
    return ri, exp



@app.callback([
    Output('Occupancy', 'children'),
    Output('occupancy-table', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('amenity_checkbox', 'value')],
    [State('cancellation_policy', 'value')],
    [State('property_type', 'value')],
    [State('neighborhood', 'value')],
    [State('instant_book_enabled', 'value')],
    [State("{}".format(_), 'value') for _ in NUMERICAL_TYPES])
def update_card_value(n_clicks,amenity_checkbox,cancellation_policy,property_type, neighborhood,instant_book_enabled, *vals):
    pred = pd.DataFrame(np.zeros((1,len(df.columns.drop(["rental_income","occupancy"])))),columns=df.drop(["rental_income","occupancy"],axis=1).columns)
    oc=np.median(df.occupancy)
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
    oc= stackO.predict(pred)
    print(oc)
    #pred.iloc[0]=stack.named_steps['imputer'].transform(pred)
    #for i in range(len(NUMERICAL_TYPES)):
    #    print(str(NUMERICAL_TYPES[i]) + " " + str(vals[i]))
    #fig=eli5.explain_prediction(stack.named_steps['R'], pred.iloc[-1], top=20, feature_names = feature_names)
    exp=format_as_dataframe(explain_prediction(stackO.named_steps['R'], pred.iloc[0], top=30, feature_names = feature_names))
    exp=exp[exp.feature.isin(Amenity_Names)]
    print(exp)
    exp = dash_table.DataTable(
         id='oc-table',
         columns=[{"name": i, "id": i} 
                  for i in exp.drop(['target'],axis=1).columns],
         data=exp.to_dict('records'),
         style_cell=dict(textAlign='left'),
         style_header=dict(backgroundColor="paleturquoise"),
         style_data=dict(backgroundColor="lavender")
    )
    print(exp)
    return oc, exp
