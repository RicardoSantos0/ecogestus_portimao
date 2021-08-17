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
from plotly.subplots import make_subplots
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
registos = pd.read_csv('./datasets/dados_registos.csv')

circuitos.style.format({'Dist. Acumulada (km)': "{:.2f}", 'Longitude': "{:.2f}", 'Latitude': "{:.2f}"})
registos.style.format({'kg/km': "{:.2f}", 'ton/h': "{:.2f}", ',capacidade_usada': "{:.2f}"})

#open other data
pass
#____________________________________________________________________________________
# Variáveis globais
# dicionário de cores
color_dict = {1: '#008490',
              2: '#580000',
              3: '#001563',
              4: '#005B46',
              5: '#6D017F',
              6: '#F75D50',
              7: '#EB6B02',
              8: '#98000D',
              9: '#ffba08',
              }

#created list as placeholder for better solution of line_color since plotly does not seem to handle it well
color_list = ['#008490', '#580000', '#001563', '#005B46', '#6D017F', '#F75D50', '#EB6B02', '#98000D', '#ffba08']
carga_util = 10.906

#____________________________________________________________________________________
# Manipulação de dados - criação de variáveis
#may need in future
cont_recolha.replace('Ã£','ã', inplace = True)
#____________________________________________________________________________________________________________________
#Global Variables and Passwords
USER_PASS = [['ecogestus', 'emarp2021']]

#external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.SPACELAB]
#external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
#____________________________________________________________________________________________________________________

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #changed to insert oil and gas stylesheet
auth = dash_auth.BasicAuth(app, USER_PASS)

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
                 #className='select_box',           #activate separate CSS document in assets folder
                 # persistence=True,                 #remembers dropdown value. Used with persistence_type
                 # persistence_type='memory'         #remembers dropdown value selected until...
                 ),  # 'memory': browser tab is refreshed
                #html.Br()
    # 'session': browser tab is closed
    # 'local': browser cookies are deleted
    ],
    className='twelve columns'),

    #linha 3 - Cartões com indicadores de interesse
    dbc.Row([dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='ton/km',
                    ),
                    style = {"margin": "10px"}),
                className = 'three columns'),
            dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='ton/h',
                    ),
                    style = {"margin": "10px"}),
                className = 'three columns'),
            dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='kg/ht',
                    ),style = {"margin": "10px"}),
                className = 'three columns'),
            dbc.Col(html.Div(
            children=dcc.Graph(
                id='capacidade',
            ),style = {"margin": "10px"}),
            className='three columns'),
        ]),
    #linha 4 - Mapa e subplots
    dbc.Row([dbc.Col([html.Div(
        daq.ToggleSwitch(
            id='tamanho-contentor',
            label=['Potencial acumulação de resíduos', 'Volume Recolhido'],
            value=False,
            style={'font-weight': 'bold', 'vertical-align' : 'middle'},
            size=70,
            className='button'
        ), className= 'seven columns'),
        html.Div(
                    children=dcc.Graph(
                        id='c-rec',
                    ),
                    style={"margin": "10px"},
                    className='seven columns'),
                    ],
        ),
        dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='aux-graph',
                    ),
                className = 'five columns'),),
        dbc.Row(dcc.Markdown('''
###### **Notas:**

Os valores de produtividade calculados têm, como termo de comparação, os seguintes valores de referência obtidos pela Equipa Técnica da Ecogestus num estudo semelhante realizado no Município de Mafra:

**Quilogramas por km**: 123.75 kg/km

**Toneladas por hora**: 1.95 ton/h

**Kg por hora trabalhada**: 723.75 kg/horaT

**Capacidade**: O peso útil de referência da viatura de recolha - 10906 kg

###### **Modos de visualização dos pontos:**      

**Potencial acumulação de resíduos**: Neste modo de visualização, o diâmetro de cada ponto é proporcional ao grau de enchimento (em percentagem) dos contentores visitados numa determinada localização*.

**Volume de resíduos recolhidos**: Neste modo de visualização, o tamanho de cada ponto é proporcional ao volume estimado de resíduos recolhidos em cada localização.
A estimativa de volume é uma função do número de contentores recolhidos, da sua capacidade volumétrica (em litros) e do seu grau de enchimento (em percentagem)*. 

    *ver notas metodológicas adicionais para aceder aos detalhes sobre a recolha de dados.

###### **Notas metodológicas adicionais:**

As informações presentes neste separador ilustram as observações realizadas pela equipa técnica da Ecogestus, Lda. ao longo do acompanhamento dos circuitos de recolha da EMARP.
O acompanhamento decorreu **entre os dias 5 e 9 de Julho de 2021**. No total, foram observados 8 circuitos de recolha: 
>
> Os circuitos **1**, **2**, **4**, **5**, **6** e **8** foram **acompanhados de forma integral**,
> 
> Os circuitos **3** e **9** foram acompanhados apenas em parte. **As observações relacionadas com o circuito 3 não foram incluídas**. 
>

###### Para cada circuito:

**1. Foi registado o trajeto (coordenadas, distância percorrida e o tempo de duração do circuito)** realizado pela viatura de recolha desde o estaleiro da EMARP até ao local de descarga (_Aterro Sanitário do Barlavento_). Estas informações encontram-se representadas no mapa (na forma de linhas).

**2. Foram registadas as localizações dos contentores e ilhas ecológicas associados ao circuito (representadas, no mapa, na forma de pontos). Para cada localização, obteve-se**:

>    
>*  O número de contentores visitados e a respetiva capacidade volumétrica,
>*  O número de contentores recolhidos e o grau de enchimento observado nos contentores recolhidos,
>
  
        ''', style = {'text-align': 'justify', 'textAlign': 'justify'}),
            className = 'twelve columns')
        ],  no_gutters=True, justify='start')
    ], fluid = True)

#________________________________________________________________________________________________________________________
#Callbacks e Helper Functions
#________________________________________________________________________________________________________________________
#---------------------------------------------------------------

# Callback 1: Map visualization
@app.callback(
    [Output(component_id='ton/km', component_property='figure'),
    Output(component_id='ton/h', component_property='figure'),
    Output(component_id='kg/ht', component_property='figure'),
    Output(component_id='capacidade', component_property='figure'),
    Output(component_id='c-rec', component_property='figure'),
    Output(component_id = 'aux-graph', component_property='figure')],
    [Input(component_id ='my_dropdown', component_property='value'),
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
    enterrados = ilhas[ilhas['volume'] == 3000]
    superficie = ilhas[ilhas['volume'] != 3000]

    reg_trace = registos[registos['Circuit'].isin(circuito)]

    #create subplot
    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"type": "domain"}, {"type": "domain"}],
               [{"type": "domain"}, {"type": "domain"}],
               [{"type": "domain"}, {"type": "domain"}]],
        column_titles= ['<b>C. Superfície</b>', '<b>C. Semi-Enterrados</b>'],
        row_titles= ['<b>Visitados</b>', '<b>Recolhidos</b>', '<b>% Enchimento</b>']
    )

    #parte 2: criação do mapa - circuitos
    #trace vazio
    traces = []

    #criar placeholder para segunda figura que usará mesmo input
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

        trace_i = ilhas[ilhas['Circuit'] == i]
        if tamanho is True:
        #split between underground and surface level containers not possible yet
            traces.append(go.Scattermapbox(
            lat=trace_i['Latitude'],
            lon=trace_i['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size= ((trace_i['litros'] + 1000)/200),
                color = trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["recolhas"] * 100).astype(int),
                                     trace_i["litros"], trace_i["tipo"],
                                     trace_i['volume'], trace_i['estado'], trace_i["Circuit"],
                                     ), axis=-1),
                hovertemplate=
                #lado esquerdo do hover
                '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
                '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
                '<b>Volume Recolhido (valor estimado)</b>: %{customdata[2]}l<br>' +
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
            traces.append(go.Scattermapbox(
                lat=trace_i['Latitude'],
                lon=trace_i['Longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=(trace_i['enchimento']+0.05) * 70,
                    color=trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["recolhas"] * 100).astype(int),
                                     (trace_i["enchimento"] * 100).astype(int), trace_i["tipo"],
                                     trace_i['volume'], trace_i['estado'], trace_i["Circuit"],
                                     ), axis=-1),
                hovertemplate=
                # lado esquerdo do hover
                '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
                '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
                '<b>Grau de enchimento dos contentores</b>: %{customdata[2]}%<br>' +
                '<b>Coordenadas</b>: lon - %{lon:.2f}, lat - %{lat:.2f}' +
                # lado direito do hover
                '<extra><b>Tipo de Contentor: %{customdata[3]}</b><br>' +
                '<b>Capacidade do Contentor (l): %{customdata[4]}</b><br>' +
                '<b>Estado: %{customdata[5]}</b><br>'
                '<b>Circuito de Recolha %{customdata[6]}</b><br></extra>',
                name='<b>Ilha Ecológica/Contentores</b>'
            ))

        #start
    map_1 =  {    'data' : traces,#, traces_i],
               'layout': go.Layout(
                uirevision= 'figure',
                autosize=True,
                height=600,
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
                    zoom=11
                        ),
                    )
        }
    #criar os novos indicadores

    kg_km = go.Figure(go.Indicator(
    mode="number + delta",
    delta={'position': "top", 'reference': 123.75, 'relative': True},
    value=reg_trace['kg/km'].mean(),
    title = '<b>kg/km</b>'))
    ton_h = go.Figure(go.Indicator(
        mode="number+delta",
        delta={'position': "top", 'reference': 1.95, 'relative': True},
        value=reg_trace['ton/h'].mean(),
        title = '<b>ton/hora</b>'))
    kg_ht = go.Figure(go.Indicator(
        mode="number+delta",
        delta={'position': "top", 'reference': 713.75, 'relative': True},
        value=reg_trace['kg/ht'].mean(),
        title = '<b>kg/horaT</b>'))
    cap = go.Figure(go.Indicator(
        mode="number+delta",
        delta={'position': "top", 'reference': carga_util, 'relative': True,
               "decreasing": {"symbol": "👍", "color" : "#3D9970"}, "increasing": {"symbol": "❌", "color" : "#FF4136"}},
        number={"suffix" : " t"},
        value=reg_trace['capacidade_usada'].mean(),
        title = '<b>Peso em transporte</b>'))

    fig.add_trace(go.Indicator(
        mode="number",
        value= superficie['contentores'].sum()
    ),
        row=1, col=1),

    fig.add_trace(go.Indicator(
        mode="number",
        value= superficie['Recolhidos'].sum(),
        ),
        row=2, col=1),

    fig.add_trace(go.Indicator(
        mode="number",
        number = {'suffix' : '%'},
        value=superficie['enchimento'].mean() * 100,
        ),
        row=3, col=1),

    fig.add_trace(go.Indicator(
        mode="number",
        value= enterrados['contentores'].sum()),
        row=1, col=2),

    fig.add_trace(go.Indicator(
        mode="number",
        value= enterrados['Recolhidos'].sum(),),
        row=2, col=2),

    fig.add_trace(go.Indicator(
        mode="number",
        number = {'suffix' : '%'},
        value=enterrados['enchimento'].mean() * 100),
        row=3, col=2),

    fig.update_layout(height=600, showlegend=False)
    card_layout = {"paper_bgcolor" : "LightSteelBlue", 'autosize' : False,
                    "width" : 325, "height" : 200, "margin" : {"l" : 50, "r":50,
                                                                "b": 5, "t":40,
                                                                "pad" : 4}
                   }
    cards = [kg_km, ton_h, kg_ht, cap]

    for i in cards:
        i.update_layout(card_layout)

    return [kg_km, ton_h, kg_ht, cap, map_1, fig]
#---------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug = True)
#Análise dos circuitos de recolha de resíduos indiferenciados no Município de Portimão