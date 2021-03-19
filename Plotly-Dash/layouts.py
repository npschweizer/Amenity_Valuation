'''
Define the layouts of each page/url
'''
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from callbacks import df, df_amenity, df_ud, stack, stackO, NUMERICAL_TYPES  # import the df loaded from callbacks so we don't need to load it again
import pandas as pd
pd.set_option('display.max_columns', None)
# the layout of homepage
homepage_layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col([        
                                html.H6(
                                    'Main Features',
                                        style={'text-align': 'center'}
                                ),
                                dcc.Dropdown(
                                    id='numerical_types',
                                    options=
                                        [{"label": num_type, "value": num_type} for num_type in NUMERICAL_TYPES],
                                    value='Bedrooms',
                                    multi = False,
                                    clearable=False,
                                    persistence = True,
                                ),
                            ]),
                            dbc.Col(dcc.Markdown([
                                "##### Main Feature Distributions\n",
                                "The plot below displays the distribution of the feature you select in the dropdown.\n"
                                "You can use it to get a sense of how many properties exist at your point in the dataset.\n "
                                "If your listing is in a range with a lot of similar properties near it, then predictions\n"
                                "will be better, but if it is in an area where data is limited, then predictions are less\n"
                                "reliable."
                            ])),
                        ]
                    ),
                    dbc.Row([
                        dbc.Col([

                            dcc.Graph(id="main-features-histogram")])
                        ]),
                    dbc.Row([
                        dbc.Col([
                            html.H5('Main Feature Conditional Effects'),
                            html.H6('Target Variable'),
                            dcc.Dropdown(
                                    id='ICE_target',
                                    options=
                                        [{"label": 'Rental Income', "value": 'rental_income'},
                                        {'label': 'Occupancy', 'value': 'occupancy'}],
                                    value='rental_income',
                                    multi = False,
                                    clearable=False,
                                    persistence = True,
                                ),
                            
                            dcc.Markdown([
                                "The plot to the right randomly selects 5% of the listings in the dataset and\n"
                                "generates predictions for it along a continuum of values for the feature you selected above.\n "
                                "You can use this to get a sense of how much your target variable changes as you adjust the feature\n"
                                "that you're interested in.\n"
                                ])
                        ]),
                        dcc.Loading(dcc.Graph(id='ICE'))]                        
                        )
                        
                    ])

amenities_layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col([        
                                html.H6(
                                    'Select Amenity',
                                        style={'text-align': 'center'}
                                ),
                                dcc.Dropdown(
                                    id='amenity_dist',
                                    options=
                                        [{"label": amenity, "value": amenity} for amenity in df_amenity.columns]
                                    ,
                                    value='Dishwasher',
                                    clearable=False,
                                    multi = False,
                                    persistence = True,
                                ),
                                #html.Img(id='example')
                            ]),
                            dbc.Col(dcc.Markdown([
                                "##### Amenity Distributions\n",
                                "The histogram below indicates how many listings at a given nightly price have the amenity you select with color indicating it's precence or absence.\n",
                                "1 indicates that an amenity is present and 0 indicates that it's absent. Please note that the histogram features are stacked rather than overlaid."
                            ])),
                        ]
                    ),
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(id="amenity-histogram"),
                            )]
                        )
                ]
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
# this allows us to have the sidebar unmoved on the left side of the page
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# save all the parameters of the pages for easy accessing
PAGES = [
    {'children': 'Home', 'href': '/', 'id': 'home'},
    {'children': 'Amenities', 'href': '/amenities', 'id': 'amenities'},
    {'children': 'Predictor', 'href': '/predictor', 'id': 'predictor'}
]

# the layout of the sidebar
sidebar_layout = html.Div(
    [
        html.Div([
                    dbc.Row([html.H4("Amenity-Shmenity"), 
                            #html.Img(src=('/assets/logo.jpeg'), width=50,
                            #        style={"margin-left": "2rem"})
                            ])
                    ]),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(**page) for page in PAGES
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

# the layout of the correlation page
predictor_layout = html.Div(children=[
        html.H1(
            'Predictor',
            style={'text-align': 'center'}
        ),
        html.H6(
            'Amenities',
            style={'text-align': 'center'}
        ),
        dcc.Dropdown(
            id='amenity_checkbox',
            options=
                [{"label": amenity, "value": amenity} for amenity in df_amenity.columns]
            ,
            value='Dishwasher',
            multi = True,
            persistence = True,
        ),
        dbc.Row([
            dbc.Col([
                html.Div(
                    [
                        html.H6("Neighborhood",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='neighborhood',
                            options=
                                [{"label": neighborhood, "value": neighborhood} for neighborhood in df_ud.neighborhood.unique()]
                            ,
                            value='University City',
                            clearable=False,
                            style={"width": 100},
                            persistence = True,
                        ),
                        html.H6("Instant Book Enabled?",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='instant_book_enabled',
                            options=
                                [{"label":"True", "value": "True"},
                                {"label":"False", "value":"False"}],
                            value='True',
                            clearable=False,
                            style={"width": 100},
                            persistence = True,
                        ),
                        html.H6("Cancellation Policy",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='cancellation_policy',
                            options=
                                [{"label":cancellation_policy, "value": cancellation_policy} for cancellation_policy in df_ud.cancellation_policy.unique()],
                            #,
                            value='University City',
                            clearable=False,
                            style={"width": 100},
                            optionHeight = 50,
                            persistence = True,
                        ),
                        html.H6("Property Type",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='property_type',
                            options=
                                [{"label":property_type, "value": property_type} for property_type in df_ud.property_type.unique()]
                            ,
                            value='House',
                            clearable=False,
                            style={"width": 100},
                            persistence = True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ]),
            dbc.Col([
                html.H6("Price",
                    style={'text-align': 'left'}),
                dcc.Input(
                    id="Nightly Price", 
                    type="number",
                    debounce=True, placeholder="0" , 
                    persistence = True,
                ),
                html.H6("Weekend Price",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Weekend Nightly Price", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Cleaning Fee",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Cleaning Fee", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Weekly Discount",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Weekly Price Factor", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Monthly Discount",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Monthly Price Factor", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Security Deposit",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Security Deposit", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Number of Guests Included",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Guests Included", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Fee for Additional Guests (per person)",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Price per Extra Guest", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),    
            ]),
            dbc.Col([
                html.H6("Beds",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Beds", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Bathrooms",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Bathrooms", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,

                ),
                html.H6("Bedrooms",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Bedrooms", 
                    type="number",
                    max=4,
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Maximum Guest Capacity",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Maximum Guest Capacity", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Number of Properties Hosted",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Number of Properties Hosted", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
            ]),
            dbc.Col([
                html.H6("Minimum Nights per Stay",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="Minimum Nights", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("# of Reviews",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="Review Count", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("# of Pictures",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="Picture Count", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Check-In Time",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="Check-In Time", 
                    type="number",
                    max=23.5,
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Check-Out Time",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="Check-Out Time", 
                    type="number",
                    max=23.5,
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.H6("Star Rating",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="Star Rating", 
                    type="number",
                    debounce=True, placeholder="0",
                    persistence = True,
                ),
                html.Button(
                    id='submit-button', 
                    n_clicks=0, 
                    children='Submit'),
                                html.H6("Star Rating",
                    style={'text-align': 'justify'}
                ),
            ]),
        ]),
        html.Hr(),
        dbc.Row(
            [
            dbc.Card(dbc.CardBody(
                [
                html.H3("Rental Income"),
                html.P("Predicted Rental Income (USD): "),
                html.H4(id='Rental_Income'),
                dcc.Loading(html.Div(id='income-table')),
                ]
            )),
            dbc.Card(dbc.CardBody(
                [
                html.H3("Occupancy"),
                dcc.Markdown([
                    "Predicted Occupancy *(Average percentage of nights booked per month)* : \n",
                ]),
                html.H4(id='Occupancy'),
                dcc.Loading(html.Div(id="occupancy-table"))
                ]
            )),
            ],
        ),
])

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}