'''
Define the layouts of each page/url
'''
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from callbacks import df, df_amenity, df_ud # import the df loaded from callbacks so we don't need to load it again

# the layout of homepage
homepage_layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Markdown([
                                "##### Mobility Types\n",
                                "**Grocery & pharmacy**\n",
                                "Mobility trends for places like grocery markets, food warehouses, \
                                    farmers markets, specialty food shops, drug stores, and pharmacies.\n",
                                "**Parks**\n",
                                "Mobility trends for places like local parks, national parks, public beaches,\
                                    marinas, dog parks, plazas, and public gardens.\n",
                                "**Transit stations**\n",
                                "Mobility trends for places like public transport hubs such as subway, bus, and train stations.\n",
                                "**Retail & recreation**\n",
                                "Mobility trends for places like restaurants, cafes, shopping centers, \
                                    theme parks, museums, libraries, and movie theaters.\n",
                                "**Residential**\n", "Mobility trends for places of residence.\n",
                                "**Workplaces**\n", "Mobility trends for places of work."

                            ])),
                            dbc.Col(dcc.Markdown([
                                "##### Correlation Coefficients between Daily Cases and Mobility\n",
                                "It is the number that describes how people reacted to the reported daily cases "\
                                    "in the previous days. It takes values between -1 and 1. A positive value indicates that "\
                                        "as the reported daily cases increased, people's mobility decreased in the following day.\n",
                                "##### Data resources\n",
                                "[Google COVID-19 Community Mobility Reports](https://www.google.com/covid19/mobility/index.html?hl=en)\n",
                                "[John Hopkins Daily Reports](https://github.com/CSSEGISandData/COVID-19)\n",
                                "[New York Times COVID-19 Reports](https://github.com/nytimes/covid-19-data)"
                            ])),
                        ]
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
    {'children': 'Predictor', 'href': '/predictor', 'id': 'predictor-page'}
]

# the layout of the sidebar
sidebar_layout = html.Div(
    [
        html.Div([
                    dbc.Row([html.H4("Amenity-Shmenity"), 
                            html.Img(src=('/assets/logo.jpeg'), width=50,
                                    style={"margin-left": "2rem"})
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

CARD_KEYS = ['Rental Income', 'Occupancy']

# the layout of the correlation page
predictor_layout = html.Div(children=[
        html.H3(
            'Predictor',
            style={'text-align': 'center'}
        ),
        html.H6(
            'Amenities',
            style={'text-align': 'center'}
        ),
        dcc.Dropdown(
            id='amenity-checkbox',
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
                        ),
                        html.H6("Instant Book Enabled?",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='instant_book_enabled',
                            options=
                                [{"label":instant_book_enabled, "value": instant_book_enabled} for instant_book_enabled in df_ud.instant_book_enabled.unique()]
                            ,
                            value='True',
                            clearable=False,
                            style={"width": 100}
                        ),
                        html.H6("Cancellation Policy",
                            style={'text-align': 'left'}),
                        dcc.Dropdown(
                            id='cancellation_policy',
                            options=
                                [{"label":cancellation_policy, "value": cancellation_policy} for cancellation_policy in df_ud.cancellation_policy.unique()]
                            ,
                            value='University City',
                            clearable=False,
                            style={"width": 100},
                            optionHeight = 50
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
                            style={"width": 100}
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ]),
            dbc.Col([
                html.H6("Price",
                    style={'text-align': 'left'}),
                dcc.Input(
                    id="price", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Weekend Price",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="listing_weekend_price_native", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Cleaning Fee",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="cleaning_fee_native", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Weekly Discount",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="weekly_price_factor", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Monthly Discount",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="monthly_price_factor", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Security Deposit",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="security_deposit_native", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Number of Guests Included",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="guests_included", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Fee for Additional Guests (per person)",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="price_for_extra_person_native", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),    
            ]),
            dbc.Col([
                html.H6("Beds",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="beds", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Bathrooms",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="bathrooms", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Bedrooms",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="bedrooms", 
                    type="number",
                    max=4,
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Maximum Guest Capacity",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="person_capacity", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
            ]),
            dbc.Col([
                html.H6("Minimum Nights per Stay",
                    style={'text-align': 'justify'}),
                dcc.Input(
                    id="min_nights", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("# of Reviews",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="reviews_count", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("# of Pictures",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="picture_count", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Check In Time",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="check_in_time", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Check Out Time",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="check_out_time", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
                html.H6("Star Rating",
                    style={'text-align': 'justify'}
                ),
                dcc.Input(
                    id="star_rating", 
                    type="number",
                    debounce=True, placeholder="Debounce True"
                ),
            ]),
        ]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([], id='Rental Income')
            ],
            className="mb-4",
        ),
])

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}