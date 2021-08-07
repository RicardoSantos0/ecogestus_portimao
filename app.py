'''This is will be a template simple dashboard to present to Portimao Municipality,
We will use Plotly and Dash as main tools. The goal is to show and compare the different
waste collection routes used by the authorities'''
# import libraries
import pandas as pd
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_auth
from dash.dependencies import Input, Output, State
from flask import Flask

#____________________________________________________________________________________
#Dealing with figures to show on dashboard
#Loading data to use for mapbox and and for other figures
with open('./assets/mapbox_tkn.txt', 'r') as f:
    mapbox_access_token = f.read().strip()

#open circuits
circuitos = pd.read_csv('./datasets/agg_circuitos.csv')
cont_recolha = pd.read_csv('./datasets/cont_recolha.csv')

#open other data
pass
#____________________________________________________________________________________
# Variáveis globais - dicionário de cores
# Necessitarei de verificar o que se passa, não estou a conseguir mapear cores de rotas

color_dict = {1: '#008490',
              2: '#580000',
              3: '#001563',
              4: '#005B46',
              5: '#6D017F',
              6: '#F75D50',
              7: '#EB6B02',
              8: '#98000D',
              9: '#ffba08'}

#____________________________________________________________________________________
# Manipulação de dados - criação de variáveis
#____________________________________________________________________________________
c1 = circuitos[circuitos['Circuit'] == 1]
c2 = circuitos[circuitos['Circuit'] == 2]
#c3 = circuitos[circuitos['Circuit'] == 3]
c4 = circuitos[circuitos['Circuit'] == 4]
c5 = circuitos[circuitos['Circuit'] == 5]
c6 = circuitos[circuitos['Circuit'] == 6]
#c7 = circuitos[circuitos['Circuit'] == 7]
c8 = circuitos[circuitos['Circuit'] == 8]
c9 = circuitos[circuitos['Circuit'] == 9]

#may need in future
#________________________________________________________________________________
#enterrados = cont_recolha[cont_recolha['tipo'] == 'Contentor semi-enterrado']
#superficie = cont_recolha[~(cont_recolha['tipo'] == 'Contentor semi-enterrado')]

del circuitos

#Figura 1
mapas = go.Figure()

mapas.add_trace(go.Scattermapbox(
        lat=c1['Latitude'],
        lon=c1['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#008490'
        ),
        name = 'Circuito 1',
        text = '<b>Minutos Passados:<b>' + c1["Tempo Acumulado (min)"].astype(str) +
                'Dist. Percorrida (km):' +  c1["Dist. Acumulada (km)"].astype(str),
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c2['Latitude'],
        lon=c2['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#580000',
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
            color = '#005B46',
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
            color = '#6D017F',
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
            size=9,
            color = '#F75D50',
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
            size=9,
            color = '#98000D',
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
            size=9,
            color = '#ffba08',
        ),
        name = 'Circuito 9',
        text='<b>Minutos Passados:<b>' + c9["Tempo Acumulado (min)"].astype(str) +
         'Dist. Percorrida (km):' + c9["Dist. Acumulada (km)"].astype(str),
        )
        )

#split between underground and surface level containers
mapas.add_trace(go.Scattermapbox(
        lat=cont_recolha['Latitude'],
        lon=cont_recolha['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size= (cont_recolha['litros']/70),
            color = cont_recolha['Circuit'].map(color_dict),
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
        style = 'streets',
        center=dict(
            lat=37.157381,
            lon=-8.552441
                    ),
        pitch=0,
        zoom=10
            ),
        )
#____________________________________________________________________________________________________________________
#Global Variables and Passwords
USER_PASS = [['ecogestus', 'emarp2021']]

#external stylesheet
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.SPACELAB]
external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
#____________________________________________________________________________________________________________________

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #changed to insert oil and gas stylesheet
#auth = dash_auth.BasicAuth(app, USER_PASS)

server = app.server
app.layout = html.Div(
    [
        dcc.Store(id='coisas'),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="https://www.ecogestus.com/pt/wp-content/uploads/2021/01/ecogestus_logotipo_moderno-2.jpeg",
                            style={'height':'7%', 'width':'7%'},
                            className='two columns',
                        ),
                        html.H2(
                            'Município de Portimão | Desempenho do Sistema de Recolha',
                        ),
                    ],
                    className='ten columns',
                ),
                html.A(
                    html.Button(
                        "Visite-nos",
                        id="learnMore"
                    ),
                    href="https://www.ecogestus.com",
                    className="two columns"
                )
            ],
            id="header",
            className='row',
        ),
    html.Div(
                    children=dcc.Graph(
                        id='Circuitos de Recolha',
                        figure=mapas)
                    )
                ]
            )

if __name__ == '__main__':
    app.run_server(debug = True)
#Análise dos circuitos de recolha de resíduos indiferenciados no Município de Portimão