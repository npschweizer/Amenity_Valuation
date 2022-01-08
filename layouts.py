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
                        ),
                    dbc.Row(
                        [
                            dbc.Card(dbc.CardBody(
                            [
                            html.H3(str("Amenity-Specific")),
                            dcc.Markdown([
                                "These are terms from the amenity you selected above",
                            ]),
                            #html.H4(id='Rental_Income'),
                            html.Img(id='image'),
                            ]
                        )),
                        dbc.Card(dbc.CardBody(
                            [
                            html.H3("All Listings"),
                            dcc.Markdown([
                                "These are terms from all listings in the dataset",
                            ]),
                            #html.H4(id='Occupancy'),
                            html.Img(id='no_image'),
                            ]
                        )),
                    ],
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
    {'children': 'Predictor', 'href': '/predictor', 'id': 'predictor'},
    {'children': 'Terms', 'href': '/terms', 'id': 'terms'}
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


terms_layout = html.Div(children=[
                    dbc.Row(
                        [
                            dbc.Col(dcc.Markdown([
                                "##### Terms and Conditions \n",
                                "Agreement between User and https://amenityshmenity.herokuapp.com/\n",
                                "Welcome to https://amenityshmenity.herokuapp.com/. The https://amenityshmenity.herokuapp.com/ website (the \"Site\") is comprised of various web pages operated by Amenity-Shmenity (\"Amenity-Shmenity\"). https://amenityshmenity.herokuapp.com/ is offered to you conditioned on your acceptance without modification of the terms, conditions, and notices contained herein (the \"Terms\"). Your use of https://amenityshmenity.herokuapp.com/ constitutes your agreement to all such Terms. Please read these terms carefully, and keep a copy of them for your reference. \n",
                                "https://amenityshmenity.herokuapp.com/ is a Blog Site. \n",
                                "This website provides information, predictions and analysis of Airbnb listings.\n",
                                "**Electronic Communications **\n",
                                "Visiting https://amenityshmenity.herokuapp.com/ or sending emails to Amenity-Shmenity constitutes electronic communications. You consent to receive electronic communications and you agree that all agreements, notices, disclosures and other communications that we provide to you electronically, via email and on the Site, satisfy any legal requirement that such communications be in writing. \n",
                                "**Children Under Thirteen **\n",
                                "Amenity-Shmenity does not knowingly collect, either online or offline, personal information from persons under the age of thirteen. If you are under 18, you may use https://amenityshmenity.herokuapp.com/ only with permission of a parent or guardian. \n",
                                "**Links to Third Party Sites/Third Party Services **\n",
                                "https://amenityshmenity.herokuapp.com/ may contain links to other websites (\"Linked Sites\"). The Linked Sites are not under the control of Amenity-Shmenity and Amenity-Shmenity is not responsible for the contents of any Linked Site, including without limitation any link contained in a Linked Site, or any changes or updates to a Linked Site. Amenity-Shmenity is providing these links to you only as a convenience, and the inclusion of any link does not imply endorsement by Amenity-Shmenity of the site or any association with its operators. \n",
                                "Certain services made available via https://amenityshmenity.herokuapp.com/ are delivered by third party sites and organizations. By using any product, service or functionality originating from the https://amenityshmenity.herokuapp.com/ domain, you hereby acknowledge and consent that Amenity-Shmenity may share such information and data with any third party with whom Amenity-Shmenity has a contractual relationship to provide the requested product, service or functionality on behalf of https://amenityshmenity.herokuapp.com/ users and customers. \n",
                                "**No Unlawful or Prohibited Use/Intellectual Property **\n", 
                                "You are granted a non-exclusive, non-transferable, revocable license to access and use https://amenityshmenity.herokuapp.com/ strictly in accordance with these terms of use. As a condition of your use of the Site, you warrant to Amenity-Shmenity that you will not use the Site for any purpose that is unlawful or prohibited by these Terms. You may not use the Site in any manner which could damage, disable, overburden, or impair the Site or interfere with any other party's use and enjoyment of the Site. You may not obtain or attempt to obtain any materials or information through any means not intentionally made available or provided for through the Site. \n",
                                "All content included as part of the Service, such as text, graphics, logos, images, as well as the compilation thereof, and any software used on the Site, is the property of Amenity-Shmenity or its suppliers and protected by copyright and other laws that protect intellectual property and proprietary rights. You agree to observe and abide by all copyright and other proprietary notices, legends or other restrictions contained in any such content and will not make any changes thereto. \n",
                                "You will not modify, publish, transmit, reverse engineer, participate in the transfer or sale, create derivative works, or in any way exploit any of the content, in whole or in part, found on the Site. Amenity-Shmenity content is not for resale. Your use of the Site does not entitle you to make any unauthorized use of any protected content, and in particular you will not delete or alter any proprietary rights or attribution notices in any content. You will use protected content solely for your personal use, and will make no other use of the content without the express written permission of Amenity-Shmenity and the copyright owner. You agree that you do not acquire any ownership rights in any protected content. We do not grant you any licenses, express or implied, to the intellectual property of Amenity-Shmenity or our licensors except as expressly authorized by these Terms.\n",
                                "**International Users**\n",
                                "The Service is controlled, operated and administered by Amenity-Shmenity from our offices within the USA. If you access the Service from a location outside the USA, you are responsible for compliance with all local laws. You agree that you will not use the Amenity-Shmenity Content accessed through https://amenityshmenity.herokuapp.com/ in any country or in any manner prohibited by any applicable laws, restrictions or regulations.\n",
                                "**Indemnification**\n",
                                "You agree to indemnify, defend and hold harmless Amenity-Shmenity, its officers, directors, employees, agents and third parties, for any losses, costs, liabilities and expenses (including reasonable attorney's fees) relating to or arising out of your use of or inability to use the Site or services, any user postings made by you, your violation of any terms of this Agreement or your violation of any rights of a third party, or your violation of any applicable laws, rules or regulations. Amenity-Shmenity reserves the right, at its own cost, to assume the exclusive defense and control of any matter otherwise subject to indemnification by you, in which event you will fully cooperate with Amenity-Shmenity in asserting any available defenses.\n",
                                "**Arbitration**\n",
                                "In the event the parties are not able to resolve any dispute between them arising out of or concerning these Terms and Conditions, or any provisions hereof, whether in contract, tort, or otherwise at law or in equity for damages or any other relief, then such dispute shall be resolved only by final and binding arbitration pursuant to the Federal Arbitration Act, conducted by a single neutral arbitrator and administered by the American Arbitration Association, or a similar arbitration service selected by the parties, in a location mutually agreed upon by the parties. The arbitrator's award shall be final, and judgment may be entered upon it in any court having jurisdiction. In the event that any legal or equitable action, proceeding or arbitration arises out of or concerns these Terms and Conditions, the prevailing party shall be entitled to recover its costs and reasonable attorney's fees. The parties agree to arbitrate all disputes and claims in regards to these Terms and Conditions or any disputes arising as a result of these Terms and Conditions, whether directly or indirectly, including Tort claims that are a result of these Terms and Conditions. The parties agree that the Federal Arbitration Act governs the interpretation and enforcement of this provision. The entire dispute, including the scope and enforceability of this arbitration provision shall be determined by the Arbitrator. This arbitration provision shall survive the termination of these Terms and Conditions. \n",
                                "**Class Action Waiver**\n",
                                "Any arbitration under these Terms and Conditions will take place on an individual basis. Class arbitrations and class/representative/collective actions are not permitted. The parties agree that a party may bring claims against the other only in each\'s individual capacity, and not as a plaintiff or class member in any putative class, collective and\/or representative proceeding, such as in the form of a private attorney general action against the other. Further, unless both you and Amenity\-Shmenity agree otherwise, the arbitrator may not consolidate more than one person\'s claims, and may not otherwise preside over any form of a representative or class proceeding.\n",
                                "**Liability Disclaimer**\n",
                                "THE INFORMATION, SOFTWARE, PRODUCTS, AND SERVICES INCLUDED IN OR AVAILABLE THROUGH THE SITE MAY INCLUDE INACCURACIES OR TYPOGRAPHICAL ERRORS. CHANGES ARE PERIODICALLY ADDED TO THE INFORMATION HEREIN. AMENITY-SHMENITY AND/OR ITS SUPPLIERS MAY MAKE IMPROVEMENTS AND/OR CHANGES IN THE SITE AT ANY TIME.\n",
                                "AMENITY-SHMENITY AND/OR ITS SUPPLIERS MAKE NO REPRESENTATIONS ABOUT THE SUITABILITY, RELIABILITY, AVAILABILITY, TIMELINESS, AND ACCURACY OF THE INFORMATION, SOFTWARE, PRODUCTS, SERVICES AND RELATED GRAPHICS CONTAINED ON THE SITE FOR ANY PURPOSE. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, ALL SUCH INFORMATION, SOFTWARE, PRODUCTS, SERVICES AND RELATED GRAPHICS ARE PROVIDED \"AS IS\" WITHOUT WARRANTY OR CONDITION OF ANY KIND. AMENITY-SHMENITY AND/OR ITS SUPPLIERS HEREBY DISCLAIM ALL WARRANTIES AND CONDITIONS WITH REGARD TO THIS INFORMATION, SOFTWARE, PRODUCTS, SERVICES AND RELATED GRAPHICS, INCLUDING ALL IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. \n",
                                "TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL AMENITY-SHMENITY AND/OR ITS SUPPLIERS BE LIABLE FOR ANY DIRECT, INDIRECT, PUNITIVE, INCIDENTAL, SPECIAL, CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF USE, DATA OR PROFITS, ARISING OUT OF OR IN ANY WAY CONNECTED WITH THE USE OR PERFORMANCE OF THE SITE, WITH THE DELAY OR INABILITY TO USE THE SITE OR RELATED SERVICES, THE PROVISION OF OR FAILURE TO PROVIDE SERVICES, OR FOR ANY INFORMATION, SOFTWARE, PRODUCTS, SERVICES AND RELATED GRAPHICS OBTAINED THROUGH THE SITE, OR OTHERWISE ARISING OUT OF THE USE OF THE SITE, WHETHER BASED ON CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY OR OTHERWISE, EVEN IF AMENITY-SHMENITY OR ANY OF ITS SUPPLIERS HAS BEEN ADVISED OF THE POSSIBILITY OF DAMAGES. BECAUSE SOME STATES/JURISDICTIONS DO NOT ALLOW THE EXCLUSION OR LIMITATION OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES, THE ABOVE LIMITATION MAY NOT APPLY TO YOU. IF YOU ARE DISSATISFIED WITH ANY PORTION OF THE SITE, OR WITH ANY OF THESE TERMS OF USE, YOUR SOLE AND EXCLUSIVE REMEDY IS TO DISCONTINUE USING THE SITE. \n",
                                "**Termination/Access Restriction**\n",
                                "Amenity-Shmenity reserves the right, in its sole discretion, to terminate your access to the Site and the related services or any portion thereof at any time, without notice. To the maximum extent permitted by law, this agreement is governed by the laws of the Commonwealth of Pennsylvania and you hereby consent to the exclusive jurisdiction and venue of courts in Pennsylvania in all disputes arising out of or relating to the use of the Site. Use of the Site is unauthorized in any jurisdiction that does not give effect to all provisions of these Terms, including, without limitation, this section. \n",
                                "You agree that no joint venture, partnership, employment, or agency relationship exists between you and Amenity-Shmenity as a result of this agreement or use of the Site. Amenity-Shmenity's performance of this agreement is subject to existing laws and legal process, and nothing contained in this agreement is in derogation of Amenity-Shmenity's right to comply with governmental, court and law enforcement requests or requirements relating to your use of the Site or information provided to or gathered by Amenity-Shmenity with respect to such use. If any part of this agreement is determined to be invalid or unenforceable pursuant to applicable law including, but not limited to, the warranty disclaimers and liability limitations set forth above, then the invalid or unenforceable provision will be deemed superseded by a valid, enforceable provision that most closely matches the intent of the original provision and the remainder of the agreement shall continue in effect. \n", 
                                "Unless otherwise specified herein, this agreement constitutes the entire agreement between the user and Amenity-Shmenity with respect to the Site and it supersedes all prior or contemporaneous communications and proposals, whether electronic, oral or written, between the user and Amenity-Shmenity with respect to the Site. A printed version of this agreement and of any notice given in electronic form shall be admissible in judicial or administrative proceedings based upon or relating to this agreement to the same extent and subject to the same conditions as other business documents and records originally generated and maintained in printed form. It is the express wish to the parties that this agreement and all related documents be written in English.  \n", 
                                "**Changes to Terms**\n",
                                "Amenity-Shmenity reserves the right, in its sole discretion, to change the Terms under which https://amenityshmenity.herokuapp.com/ is offered. The most current version of the Terms will supersede all previous versions. Amenity-Shmenity encourages you to periodically review the Terms to stay informed of our updates.   \n",
                                "Effective as of August 12, 2021\n"
                            ]))
                        ]
                    )
                ]
)

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}