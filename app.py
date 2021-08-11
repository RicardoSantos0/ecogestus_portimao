'''This is will be a template simple dashboard to present to Portimao Municipality,
We will use Plotly and Dash as main tools. The goal is to show and compare the different
waste collection routes used by the authorities'''
# import libraries
import pandas as pd
import numpy as np
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
circuitos.style.format({'Dist. Acumulada (km)': "{:.2f}", 'Longitude': "{:.2f}", 'Latitude': "{:.2f}"})

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
cont_recolha.replace('Ã£','ã', inplace = True)
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
        customdata= np.stack((c1["Dist. Acumulada (km)"], c1["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' # +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 1</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c2['Latitude'],
        lon=c2['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#580000',
        ),
        customdata= np.stack((c2["Dist. Acumulada (km)"], c2["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' # +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 2</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c4['Latitude'],
        lon=c4['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#005B46',
        ),
        customdata= np.stack((c4["Dist. Acumulada (km)"], c4["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' # +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 4</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c5['Latitude'],
        lon=c5['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#6D017F',
        ),
        customdata= np.stack((c5["Dist. Acumulada (km)"], c5["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' # +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 5</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c6['Latitude'],
        lon=c6['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#F75D50',
        ),
        customdata= np.stack((c6["Dist. Acumulada (km)"], c6["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' # +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 6</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c8['Latitude'],
        lon=c8['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#98000D',
        ),
        customdata= np.stack((c8["Dist. Acumulada (km)"], c8["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>'# +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 8</b>',
        ))

mapas.add_trace(go.Scattermapbox(
        lat=c9['Latitude'],
        lon=c9['Longitude'],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color = '#ffba08',
        ),
        customdata= np.stack((c9["Dist. Acumulada (km)"], c9["Tempo Acumulado (min)"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>'# +
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        ,
        name = '<b>Circuito 9</b>',
        ))

#split between underground and surface level containers not possible yet
mapas.add_trace(go.Scattermapbox(
        lat=cont_recolha['Latitude'],
        lon=cont_recolha['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size= cont_recolha['litros']/200,
            color = cont_recolha['Circuit'].map(color_dict),
        ),
        customdata=np.stack((cont_recolha["contentores"], (cont_recolha["recolhas"] * 100).astype(int),
                            (cont_recolha["percentagem"] * 100).astype(int), cont_recolha["tipo"],
                             cont_recolha['volume'], cont_recolha['estado'], cont_recolha["Circuit"],
                             ), axis=-1),
        hovertemplate=
        #lado esquerdo do hover
        '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
        '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
        '<b>Grau de enchimento contentores recolhidos</b>: %{customdata[2]}%<br>' +
        '<b>Coordenadas</b>: lon - %{lon:.2f}, lat - %{lat:.2f}' +
        #lado direito do hover
        '<extra><b>Tipo de Contentor: %{customdata[3]}</b><br>' +
        '<b>Capacidade do Contentor (l): %{customdata[4]}</b><br>' +
        '<b>Estado: %{customdata[5]}</b><br>'
        '<b>Circuito de Recolha %{customdata[6]}</b><br></extra>',
        name = '<b>Ilha Ecológica/Contentores</b>'
))

#care with size on final upload
mapas.update_layout(dict(
    autosize=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode='closest',
    showlegend = False,
    title = 'Circuitos de Recolha de RU',
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
app.layout = dbc.Container([
    #cabeçalho - Título, logo e botão
    dbc.Row([html.Div([
        dcc.Store(id='coisas'),
                html.Div(
                    [
                        html.Img(
                            src="https://www.ecogestus.com/pt/wp-content/uploads/2021/01/ecogestus_logotipo_moderno-2.jpeg",
                            style={'height': '10%', 'width': '10%', 'verticalAlign': 'middle'},
                            className='two columns',
                        ),
                        #html.Img(
                        #    src = "https://www.emarp.pt/wp-content/uploads/2021/07/EMARP_LOGO-PRINCIPAL.png",
                        #    #src="https://www.ecogestus.com/pt/wp-content/uploads/2021/01/ecogestus_logotipo_moderno-2.jpeg",
                        #    style={'height':'20%', 'width':'20%', 'verticalAlign': 'middle'},
                        #    className='two columns',
                        #),
                        html.H2(
                            'Portimão | Avaliação de Desempenho da Recolha de RU', style={'textAlign': 'center', 'fontWeight': 'bold',  'verticalAlign': 'middle'},
                            className='eight columns'),
                    html.A(
                        html.Button(
                        "Visite-nos",
                        id="learnMore",
                        ),
                        href="https://www.ecogestus.com",
                        className="two columns",
                        style=dict(verticalAlign ='middle', display = 'inline')
                        )
            ],
            id="header",
            className='row',
        )])
        ]),
    #linha 2: Mapa e outras representações
    dbc.Row([dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='Circuitos de Recolha',
                        figure=mapas,
                    ),
                    style={"margin": "10px"},
                    className='eight columns'),
                    ),
        dbc.Col([html.P('O mapa à esquerda ilustra e resume o acompanhamento no terreno dos circuitos de recolha da EMARP. ' +
                        'Para cada localização foram registados:', style = {'textAlign': 'justify'}),
                html.P(),
                html.P('O número de contentores visitados e a respetiva capacidade volumétrica,', style = {'font-weight': 'bold', 'textAlign': 'justify'}),
                html.P('O número de contentores recolhidos e o grau de enchimento observado,', style = {'font-weight': 'bold', 'textAlign': 'justify'}),
                html.P('Tendo por base os indicadores observados, foi feita uma estimativa da contribuição (em volume) de cada localização para o total dos resíduos recolhidos. Essa contribuição está representada no diâmetro de cada ponto.',
                       style = {'textAlign': 'justify'})],
                className = 'three columns',
                style={'display': "inline-block"})
        ], no_gutters=True, justify='start')
    ], fluid = True)

if __name__ == '__main__':
    app.run_server(debug = True)
#Análise dos circuitos de recolha de resíduos indiferenciados no Município de Portimão