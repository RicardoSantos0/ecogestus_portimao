'''transfomar a aplicalção numa aplicação paginada'''
import dash
import dash_auth
import dash_bootstrap_components as dbc

#Global Variables and Passwords
USER_PASS = [['ecogestus', 'emarp2021']]

#external stylesheet
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.LUX]
#external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
#____________________________________________________________________________________________________________________

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
#insert authentication and start server
#auth = dash_auth.BasicAuth(app, USER_PASS)
server = app.server