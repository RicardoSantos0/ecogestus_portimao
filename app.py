'''This is will be a template simple dashboard to present to Portimao Municipality,
We will use Plotly and Dash as main tools. The goal is to show and compare the different
waste collection routes used by the authorities'''

# import libraries
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import dash_auth
USER_PASS = [['ecogestus', 'emarp2021']]

#____________________________________________________________________________________
#Loading data to use for mapbox and and for the figure
#load mapbox utilities
with open('./assets/mapbox_tkn.txt', 'r') as f:
    mapbox_access_token = f.read().strip()

#open c1
c1 = pd.read_csv('./datasets/c1.csv')
c2 = pd.read_csv('./datasets/c2.csv')
c4 = pd.read_csv('./datasets/c4.csv')
c5 = pd.read_csv('./datasets/c5.csv')
c6 = pd.read_csv('./datasets/c6.csv')
c8 = pd.read_csv('./datasets/c8.csv')
c9 = pd.read_csv('./datasets/c9.csv')
cont_recolha = pd.read_csv('./datasets/cont_recolha.csv')
# Legendas aldrabadas

mapas = go.Figure()

mapas.add_trace(go.Scattermapbox(
        lat=c1['Latitude'],
        lon=c1['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#001219'
        ),
        name = 'Circuito 1',
        text = '<b>Minutos Passados:<b>' + c1["Tempo Acumulado (min)"].astype(str) +
                'Dist. Percorrida (km):' +  c1["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c2['Latitude'],
        lon=c2['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#005f73',
        ),
        name = 'Circuito 2',
        text = '<b>Minutos Passados:<b>' + c2["Tempo Acumulado (min)"].astype(str) +
                'Dist. Percorrida (km):' +  c2["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c4['Latitude'],
        lon=c4['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#ca6702',
        ),
        name = 'Circuito 4',
        text = '<b>Minutos Passados:<b>' + c4["Tempo Acumulado (min)"].astype(str) +
                'Dist. Percorrida (km):' +  c4["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c5['Latitude'],
        lon=c5['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#bb3e03',
        ),
        name = 'Circuito 5',
        text = '<b>Minutos Passados:<b>' + c5["Tempo Acumulado (min)"].astype(str) +
                'Dist. Percorrida (km):' +  c5["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c6['Latitude'],
        lon=c6['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=3,
            color = '#9b2226',
        ),
        name = 'Circuito 6',
        text='<b>Minutos Passados:<b>' + c6["Tempo Acumulado (min)"].astype(str) +
         'Dist. Percorrida (km):' + c6["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c8['Latitude'],
        lon=c8['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=3,
            color = '#283618',
        ),
        name = 'Circuito 8',
        text='<b>Minutos Passados:<b>' + c8["Tempo Acumulado (min)"].astype(str) +
         'Dist. Percorrida (km):' + c8["Dist. Acumulada (km)"].astype(str),
        )
        )

mapas.add_trace(go.Scattermapbox(
        lat=c9['Latitude'],
        lon=c9['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=3,
            color = '#5f0f40',
        ),
        name = 'Circuito 9',
        text='<b>Minutos Passados:<b>' + c9["Tempo Acumulado (min)"].astype(str) +
         'Dist. Percorrida (km):' + c9["Dist. Acumulada (km)"].astype(str),
        )
        )

#color_dict = ['#001219', '#005f73', '#ca6702', '#bb3e03', '#9b2226', '#283618', '#5f0f40']
mapas.add_trace(go.Scattermapbox(
        lat=cont_recolha['Latitude'],
        lon=cont_recolha['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color = cont_recolha['Circuit'],
        ),
        name = 'Contentores',
        text = 'Circuito: ' + cont_recolha['Circuit'].astype(str)
        )
        )

mapas.update_layout(dict(
    autosize=True,
    #margin=dict(
    #    l=30,
    #    r=30,
    #    b=20,
    #    t=40
    ),
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=37.157381,
            lon=-8.552441
                    ),
        pitch=0,
        zoom=10
            ),
        )

# create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
auth = dash_auth.BasicAuth(app, USER_PASS)

#test layout
#https://codepen.io/chriddyp/pen/bWLwgP.css

server = app.server
app.layout = html.Div(children = [html.H1('Ecogestus - Desempenho do Sistema de Recolha'),
                        html.Div(children='Representação Geográfica - Prova de Conceito - Versão Teste'),
                        dcc.Graph(
                        id='Circuitos de Recolha',
                        figure=mapas)
                        ])

if __name__ == '__main__':
    app.run_server(debug = True)