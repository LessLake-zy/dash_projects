from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd

df = pd.read_csv('Berlin_crimes.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

modal = html.Div([
    dbc.Button("Add comment", id='open'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("All About Berlin", style={'font-size': '24px', 'font-style': 'italic'})),
        dbc.ModalBody(
            dbc.Form([
                dbc.Row([
                    dbc.Label('Name', className='mt-1'),
                    dbc.Input(type='text', placeholder='Enter your name')
                ],
                    className='mb-2'
                ),
                dbc.Row([
                    dbc.Label('Email', className='mt-1'),
                    dbc.Input(type='email', placeholder='Enter email')
                ],
                    className='mb-2'
                ),
                dbc.Row([
                    dbc.Label('Comment', className='mt-1'),
                    dbc.Input(type='text', placeholder='Enter comment')
                ],
                    className='mb-2'
                ),
                dbc.Button("Submit", color='primary'),
            ])
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id='close', color='ml-auto'),
        )
    ],
        id='modal',
        is_open=False,
        size='xl',
        backdrop=True,
        scrollable=True,
        centered=True,
        fade=True
    )
])


alert = dbc.Alert("Please choose Districts from dropdown to avoid further disappointment", color='danger', dismissable=True)

image_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("The Lovely City of Berlin", className="card-title"),
                dbc.CardImg(src="/assets/berlinwall.jpg", title="Graffiti by Gabriel Heimler"),
                html.H6("Choose Berlin Districts:", className="card-text"),
                html.Div(id="the_alert", children=[]),
                dcc.Dropdown(id='district_chosen', options=[{'label': d, "value": d} for d in df["District"].unique()],
                             value=["Lichtenberg", "Pankow", "Spandau"], multi=True, style={"color": "#000000"}),
                html.Hr(),
                modal
            ]
        ),
    ],
    color="light",
)

graph_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Graffiti in Berlin 2012-2019", className="card-title", style={"text-align": "center"}),
                dbc.Button(
                    "About Berlin", id="popover-bottom-target", color="info"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("All About Berlin:"),
                        dbc.PopoverBody(
                            "Berlin (/bɜːrˈlɪn/; German: [bɛʁˈliːn] is the capital and largest city of Germany by both area and population. Its 3,769,495 (2019) inhabitants make it the most populous city proper of the European Union. The city is one of Germany's 16 federal states. It is surrounded by the state of Brandenburg, and contiguous with Potsdam, Brandenburg's capital. The two cities are at the center of the Berlin-Brandenburg capital region, which is, with about six million inhabitants and an area of more than 30,000 km2, Germany's third-largest metropolitan region after the Rhine-Ruhr and Rhine-Main regions. (Wikipedia)"),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom",
                    is_open=False,
                ),
                dcc.Graph(id='line_chart', figure={}),

            ]
        ),
    ],
    color="light",
)


# *********************************************************************************************************
app.layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=3), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************


@app.callback(
    Output("popover", "is_open"),
    [Input("popover-bottom-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output("line_chart", "figure"),
     Output("the_alert", "children")],
    [Input("district_chosen", "value")]
)
def update_graph_card(districts):
    if len(districts) == 0:
        return dash.no_update, alert
    else:
        df_filtered = df[df["District"].isin(districts)]
        df_filtered = df_filtered.groupby(["Year", "District"])[['Graffiti']].median().reset_index()
        fig = px.line(df_filtered, x="Year", y="Graffiti", color="District",
                      labels={"Graffiti": "Graffiti incidents (avg)"}).update_traces(mode='lines+markers')
        return fig, dash.no_update


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)