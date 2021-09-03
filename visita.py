'''Esta página incluirá os elementos ainda não considerados'''
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
from dash.dependencies import Input, Output
from app import app

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
registos.style.format({'kg/km': "{:.2f}", 'ton/h': "{:.2f}", ',capacidade_usada': "{:.1f}", 'vol_instalado_m3': "{:.1f}",
                       'vol_recolhido_m3' : '{:.1f}'})

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

#layout da aplicação - especificamente do separador visita
visita_layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
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
                        ),
                    ],
                style={'text-align': 'center'},
                width = 12),
        ),
    #linha 3 - Cartões com indicadores de interesse
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='ton/km',
                    ),
                    style = {"margin": "10px"}),
                width = 2),
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='kg/m3',
                    ),
                    style={"margin": "10px"}),
                    width=2),
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='ton/h',
                    ),
                    style = {"margin": "10px"}),
                width = 2),
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='kg/ht',
                    ),style = {"margin": "10px"}),
                width = 2),
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='capacidade',
                ),style = {"margin": "10px"}),
                width = 2),
        ],
            justify="center",
            align="center",
            className="h-50",
        ),

    #linha 4 - Mapa e subplots
        dbc.Row(
                [dbc.Col(
                    [
                        html.Label(['Seleccione um modo de visualização no mapa'], style={'font-weight': 'bold', 'align' : 'center'}),
                        daq.ToggleSwitch(
                            id='tamanho-contentor',
                            label=['Grau de enchimento dos contentores', 'Volume de resíduos recolhidos'],
                            value=False,
                            style={'font-weight': 'bold'},
                            size=70,
                            ),
                        html.Div(
                            children=dcc.Graph(
                            id='c-rec'),
                            style={"margin": "10px"},),
                    ],
                style={'text-align': 'center'},
                width = 7,
        ),
                dbc.Col(html.Div(
                    children=dcc.Graph(
                        id='aux-graph',
                    )),
                    width = 5)
                ]
        ),
#         dbc.Row(
#             dbc.Col(
        #             )
        #         )

        ]
    )

#________________________________________________________________________________________________________________________
#Callbacks e Helper Functions
#________________________________________________________________________________________________________________________
#---------------------------------------------------------------

# Callback 1: Map visualization
@app.callback(
    [Output(component_id='ton/km', component_property='figure'),
    Output(component_id='kg/m3', component_property='figure'),
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
                size= ((trace_i['vol_recolhido_m3'] + 1)/0.2),
                color = trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["%_recolhidos"] * 100).astype(int),
                                     trace_i["vol_recolhido_m3"], trace_i["tipo"],
                                     trace_i['vol_instalado_m3'], trace_i['estado'], trace_i["Circuit"],
                                     ), axis=-1),
                hovertemplate=
                #lado esquerdo do hover
                '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
                '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
                '<b>Volume Recolhido (valor estimado)</b>: %{customdata[2]} m3<br>' +
                '<b>Coordenadas</b>: lon: %{lon:.2f}, lat: %{lat:.2f}' +
                #lado direito do hover
                '<extra><b>Tipo de Contentor: %{customdata[3]}</b><br>' +
                '<b>Capacidade do Contentor (m3): %{customdata[4]}</b><br>' +
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
                    size=(trace_i['percentagem']+0.05) * 70,
                    color=trace_i['Circuit'].map(color_dict),
                ),
                customdata=np.stack((trace_i["contentores"], (trace_i["%_recolhidos"] * 100).astype(int),
                                     (trace_i["percentagem"] * 100).astype(int), trace_i["tipo"],
                                     trace_i['vol_instalado_m3'], trace_i['estado'], trace_i["Circuit"],
                                     ), axis=-1),
                hovertemplate=
                # lado esquerdo do hover
                '<b>Contentores Visitados</b>: %{customdata[0]}<br>' +
                '<b>Contentores Recolhidos/Visitados</b>: %{customdata[1]}%<br>' +
                '<b>Grau de enchimento dos contentores</b>: %{customdata[2]}%<br>' +
                '<b>Coordenadas</b>: lon: %{lon:.2f}, lat: %{lat:.2f}' +
                # lado direito do hover
                '<extra><b>Tipo de Contentor: %{customdata[3]}</b><br>' +
                '<b>Capacidade do Contentor (m3): %{customdata[4]}</b><br>' +
                '<b>Estado: %{customdata[5]}</b><br>'
                '<b>Circuito de Recolha %{customdata[6]}</b><br></extra>',
                name='<b>Ilha Ecológica/Contentores</b>'
            ))

        #start
    map_1 =  {    'data' : traces,#, traces_i],
               'layout': go.Layout(
                uirevision= 'figure',
                autosize=True,
                height=500,
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
        mode="number",
        #delta={'position': "top", 'reference': 123.75, 'relative': True},
        value=reg_trace['kg/km'].mean(),
        title = '<b>Produtividade (kg/km)</b>'),)

    kg_m3 = go.Figure(go.Indicator(
        mode="number",
        #delta={'position': "top", 'reference': 123.75, 'relative': True},
        value=reg_trace['kg/m3'].mean(),
        title = '<b>Peso específico (kg/m3)</b>'))

    ton_h = go.Figure(go.Indicator(
        mode="number",
        #delta={'position': "top", 'reference': 1.95, 'relative': True},
        value=reg_trace['ton/h'].mean(),
        title = '<b>Produtividade (t/hora)</b>'))

    kg_ht = go.Figure(go.Indicator(
        mode="number",
        #delta={'position': "top", 'reference': 713.75, 'relative': True},
        value=reg_trace['kg/ht'].mean(),
        title = '<b>Produtividade (kg/horaT)</b>'))
    cap = go.Figure(go.Indicator(
        mode="number",
        value=reg_trace['massa_t'].sum() / 1000,
        title = '<b>Resíduos Recolhidos (t)</b>'))

    ##Figura 3 - Apoio ao Gráfico - criação condicional, again
    #nova condição dependente do modo de visualização
    if tamanho is True:
        # create subplot
        fig = make_subplots(
            rows=3, cols=2,
            specs=[[{"type": "domain"}, {"type": "domain"}],
                   [{"type": "domain"}, {"type": "domain"}],
                   [{"type": "domain"}, {"type": "domain"}]],
            column_titles=['<b>Cont. Superfície</b>', '<b>Cont. Semi-Enterrados</b>'],
            row_titles=['<b>N. Visitados</b>', '<b>N. Recolhidos</b>', '<b>V. Recolhido (est)</b>']
        )

        fig.add_trace(go.Indicator(
            mode="number",
            value=superficie['contentores'].sum()
        ),
            row=1, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            value=superficie['Recolhidos'].sum(),
        ),
            row=2, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            value=enterrados['contentores'].sum()),
            row=1, col=2),

        fig.add_trace(go.Indicator(
            mode="number",
            value=enterrados['Recolhidos'].sum(), ),
            row=2, col=2),

        fig.add_trace(go.Indicator(
            mode="number",
            number={'suffix': ' m3'},
            value=superficie['vol_recolhido_m3'].sum(),
        ),
            row=3, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            number={'suffix': ' m3'},
            value=enterrados['vol_recolhido_m3'].sum()),
            row=3, col=2),

    else:
        # create subplot
        fig = make_subplots(
            rows=3, cols=2,
            specs=[[{"type": "domain"}, {"type": "domain"}],
                   [{"type": "domain"}, {"type": "domain"}],
                   [{"type": "domain"}, {"type": "domain"}]],
            column_titles=['<b>Cont. Superfície</b>', '<b>Cont. Semi-Enterrados</b>'],
            row_titles=['<b>N. Visitados</b>', '<b>N. Recolhidos</b>', '<b>% Enchimento Rec.</b>']
        )

        fig.add_trace(go.Indicator(
            mode="number",
            value=superficie['contentores'].sum()
        ),
            row=1, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            value=superficie['Recolhidos'].sum(),
        ),
            row=2, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            value=enterrados['contentores'].sum()),
            row=1, col=2),

        fig.add_trace(go.Indicator(
            mode="number",
            value=enterrados['Recolhidos'].sum(), ),
            row=2, col=2),

        fig.add_trace(go.Indicator(
            mode="number",
            number = {'suffix' : '%'},
            value = (np.dot(superficie['percentagem'], superficie['Recolhidos']) / np.sum(superficie['Recolhidos'])) * 100,
            ),
            row=3, col=1),

        fig.add_trace(go.Indicator(
            mode="number",
            number = {'suffix' : '%'},
            value = (np.dot(enterrados['percentagem'], enterrados['Recolhidos']) / np.sum(enterrados['Recolhidos'])) * 100,
        ),
            row=3, col=2),

    fig.update_layout(height=600, showlegend=False)
    card_layout = {"paper_bgcolor" : "LightSteelBlue", 'autosize' : False,
                    "height" : 100, "margin" : {"l" : 50, "r":50,
                                                "b": 5, "t":40,
                                                "pad" : 4}
                   }
    cards = [kg_km, kg_m3, ton_h, kg_ht, cap]

    for i in cards:
        i.update_layout(card_layout)

    return [cap, kg_km, ton_h, kg_ht, kg_m3, map_1, fig]
#---------------------------------------------------------------