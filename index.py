'''este ficheiro será o índice da aplicação, será a partir das ligações aqui colocadas que será
depois, possível, fazer a ligação entre diferentes páginas'''
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#ligação à aplicação
from app import app
from app import server

#ligação àquelas que serão as futuras tabs
from visita import visita_layout
#from historico import historico_layout

# our app's Tabs *********************************************************
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Dados Históricos", tab_id="hist", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Dados Observados", tab_id="obs", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="obs",
        ),
    ], className="mt-2"
)

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.Img(
                            src="https://www.ecogestus.com/pt/wp-content/uploads/2021/01/ecogestus_logotipo_moderno-2.jpeg",
                            style={'height': '100%', 'width': '100%', 'verticalAlign': 'middle'},
                            width = 2,
                        )),
            dbc.Col(html.H2("Portimão | Desempenho da Recolha de RU",
                            style={"textAlign": "center"}), width=8),
            dbc.Col(
                html.A(dbc.Button(
                        "Visite-nos",
                        color = 'success',
                        className= "mr-1",
                        id="learnMore"),
                        href="https://www.ecogestus.com",
                ),
                width = 2,
            )
    ]),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-2"),
    html.Div(id='content', children=[])
    ], fluid = True)

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "obs":
        return visita_layout
    elif tab_chosen == "hist":
        #return historico_layout
        return html.P('Página em construção')

if __name__=='__main__':
    app.run_server(debug=True)