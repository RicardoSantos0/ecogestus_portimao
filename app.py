'''This is will be a template simple dashboard to present to Portimao Municipality,
We will use Plotly and Dash as main tools. The goal is to show and compare the different
waste collection routes used by the authorities'''
# import libraries
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
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

#created list as placeholder for better solution of line_color since plotly does not seem to handle it well
color_list = ['#008490', '#580000', '#001563', '#005B46', '#6D017F', '#F75D50', '#EB6B02', '#98000D', '#ffba08']

#____________________________________________________________________________________
# Manipulação de dados - criação de variáveis
#may need in future
cont_recolha.replace('Ã£','ã', inplace = True)
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
    #linha 2, Dropdown de selecção : Mapa e outras representações
    dbc.Row([html.Div(),
    html.Br(),
    html.Label(['Seleccione o(s) circuito(s) de recolha que pretende observar:'], style={'font-weight': 'bold'}),
    dcc.Dropdown(id='my_dropdown',
                 options=[
                     {'label': 'Circuito 1', 'value': 1},
                     {'label': 'Circuito 2', 'value': 2},
                     {'label': 'Circuito 3', 'value': 3, 'disabled':True},
                     {'label': 'Circuito 4', 'value': 4},
                     {'label': 'Circuito 5', 'value': 5},
                     {'label': 'Circuito 6', 'value': 6},
                     {'label': 'Circuito 7', 'value': 7, 'disabled': True},
                     {'label': 'Circuito 8', 'value': 8},
                     {'label': 'Circuito 9', 'value': 9},
                 ],
                 value = [1],
                 optionHeight=25,  # height/space between dropdown options
                 disabled=False,  # disable dropdown value selection
                 multi=True,  # allow multiple dropdown values to be selected
                 searchable=True,  # allow user-searching of dropdown values
                 search_value='',  # remembers the value searched in dropdown
                 placeholder='Escolha, pelo menos, um circuito de recolha...',  # gray, default text shown when no option is selected
                 clearable=True,  # allow user to removes the selected value
                 style= {'width' : '100%'},  # use dictionary to define CSS styles of your dropdown
                 className='select_box',           #activate separate CSS document in assets folder
                 # persistence=True,                 #remembers dropdown value. Used with persistence_type
                 # persistence_type='memory'         #remembers dropdown value selected until...
                 ),  # 'memory': browser tab is refreshed
                #html.Br()
    # 'session': browser tab is closed
    # 'local': browser cookies are deleted
    daq.ToggleSwitch(
                id='tamanho-contentor',
                label = ['Potencial acumulação de resíduos', 'Volume de resíduos recolhidos'],
                value = False,
                style={'font-weight': 'bold'},
                size = 70,
                theme = 'dark'
            ),
    ],
    className='eight columns'),
#linha 3 - Mapa e subplots
    dbc.Row([dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='c-rec',
                    ),
                    style={"margin": "10px"},
                    className='eight columns'),
                    ),
        dbc.Col([html.P('Acompanhamento dos Circuitos de Recolha',
                 style = {'textAlign': 'center', 'font-weight': 'bold'}),
                html.P('O mapa à esquerda ilustra e resume o acompanhamento no terreno dos circuitos de recolha da EMARP. ' +
                        'Para cada localização foram registados:',
                        style = {'textAlign': 'justify'}),
                html.P('O número de contentores visitados e a respetiva capacidade volumétrica,', style = {'font-weight': 'bold', 'textAlign': 'justify'}),
                html.P('O número de contentores recolhidos e o grau de enchimento observado,', style = {'font-weight': 'bold', 'textAlign': 'justify'}),
                html.P('Tendo por base os indicadores observados, foi feita uma estimativa da contribuição (em volume) de cada localização para o total dos resíduos recolhidos. Essa contribuição está representada no diâmetro de cada ponto.',
                       style = {'textAlign': 'justify'})],
                className = 'three columns',
                style={'display': "inline-block"})
        ], no_gutters=True, justify='start')
    ], fluid = True)

#________________________________________________________________________________________________________________________
#Callbacks e Helper Functions
#________________________________________________________________________________________________________________________
#---------------------------------------------------------------

# Callback 1: Map visualization
@app.callback(
    Output(component_id='c-rec', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value'),
     Input(component_id = 'tamanho-contentor', component_property='value')]
)

def build_graph(circuito, tamanho):
    '''constrói um mapa representativo dos circuitos seleccionados a partir do circuito escolhido pelo utilizador'''

    if not circuito:
        raise dash.exceptions.PreventUpdate

    #parte 1: manipulação dos dfs
    passeios = circuitos[circuitos["Circuit"].isin(circuito)]
    c_lista = list(passeios.Circuit.unique())

    ilhas = cont_recolha[cont_recolha['Circuit'].isin(circuito)]

    #parte 2: criação do mapa - circuitos
    #trace vazio
    traces = []
    for i in c_lista:

        trace = passeios[passeios['Circuit'] == i]
        traces.append(go.Scattermapbox(
        lat=trace['Latitude'],
        lon=trace['Longitude'],
        mode='lines',
        line_color = color_list[i-1],
        customdata= np.stack((trace["Dist. Acumulada (km)"], trace["Tempo Acumulado (min)"], trace["Circuit"]), axis = -1),
        hovertemplate =
        '<b>Tempo (min):</b>: %{customdata[1]}<br>' +
        '<b>Kms Percorridos</b>: %{customdata[0]:.2f}<br>' +
        '<extra><b>Circuito: %{customdata[2]}</b></extra>',
        #'<b>Longitude</b>: %{lon:.2f}<br>' +
        #'<b>Latitude</b>: %{lat:.2f}<br>'
        name = 'rotas',
        ))

        if tamanho is True:
        #split between underground and surface level containers not possible yet
            trace_i = ilhas[ilhas['Circuit'] == i]
            traces.append(go.Scattermapbox(
            lat=trace_i['Latitude'],
            lon=trace_i['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size= ((trace_i['litros'] + 1000)/200),
                color = trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["recolhas"] * 100).astype(int),
                                    (trace_i["percentagem"] * 100).astype(int), trace_i["tipo"],
                                     trace_i['volume'], trace_i['estado'], trace_i["Circuit"],
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

        else:
            # split between underground and surface level containers not possible yet
            trace_i = ilhas[ilhas['Circuit'] == i]
            traces.append(go.Scattermapbox(
                lat=trace_i['Latitude'],
                lon=trace_i['Longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=(trace_i['enchimento']+0.05) * 70,
                    color=trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["recolhas"] * 100).astype(int),
                                     (trace_i["percentagem"] * 100).astype(int), trace_i["tipo"],
                                     trace_i['volume'], trace_i['estado'], trace_i["Circuit"],
                                     ), axis=-1),
                hovertemplate=
                # lado esquerdo do hover
                '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
                '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
                '<b>Grau de enchimento contentores recolhidos</b>: %{customdata[2]}%<br>' +
                '<b>Coordenadas</b>: lon - %{lon:.2f}, lat - %{lat:.2f}' +
                # lado direito do hover
                '<extra><b>Tipo de Contentor: %{customdata[3]}</b><br>' +
                '<b>Capacidade do Contentor (l): %{customdata[4]}</b><br>' +
                '<b>Estado: %{customdata[5]}</b><br>'
                '<b>Circuito de Recolha %{customdata[6]}</b><br></extra>',
                name='<b>Ilha Ecológica/Contentores</b>'
            ))
        #start
    return {    'data' : traces,#, traces_i],
               'layout': go.Layout(
                uirevision= 'figure',
                autosize=True,
                margin=dict(
                    l=30,
                    r=30,
                    b=20,
                    t=40
                ),
                hovermode='closest',
                showlegend = False,
                #title = 'Circuitos de Recolha de RU',
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
        }

#---------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug = True)
#Análise dos circuitos de recolha de resíduos indiferenciados no Município de Portimão