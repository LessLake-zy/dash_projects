import pandas as pd
import plotly.express as px
from dash import Dash, html, Input, Output, dcc, dash

df = pd.read_csv('Mutual-Funds.csv')

colors = ['black', 'blue', 'red', 'yellow', 'pink', 'orange']

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='my-dropdown', multi=True,
                 options=[{'label': x, 'value': x} for x in sorted(df.fund_extended_name.unique())],
                 value=['Fidelity 500 Index Fund', 'Fidelity Advisor Freedom 2035 Fund Class A',
                        'Fidelity Freedom 2035 Fund']),
    html.Button(id='my-button', n_clicks=0, children='Show breakdown'),
    dcc.Graph(id='graph-output', figure={}),
    html.Div(id='sentence-output', children=["This is the color I love"], style={}),
    dcc.RadioItems(id='my-radioitem', value='black', options=[{'label': c, 'value': c} for c in colors], )
])


# @app.callback(
#     Output('graph-output', 'figure'),
#     Input('my-dropdown', 'value'),
#     prevent_initial_call=False
# )
# def update_my_graph(val_chosen):
#     if len(val_chosen) > 0:
#         print(f"value user chose: {val_chosen}")
#         print(type(val_chosen))
#
#         dff = df[df["fund_extended_name"].isin(val_chosen)]
#         fig = px.pie(dff, values="ytd_return", names="fund_extended_name", title="Year-to-Date Returns")
#         fig.update_traces(textinfo="value+percent").update_layout(title_x=0.5)
#         return fig
#     elif len(val_chosen) == 0:
#         raise dash.exceptions.PreventUpdate


@app.callback(
    [Output('graph-output', 'figure'),
     Output('sentence-output', 'style')],
    [Input(component_id='my-radioitem', component_property='value'),
     Input(component_id='my-dropdown', component_property='value')],
    prevent_initial_call=False
)
def update_graph(color_chosen, val_chosen):
    if len(val_chosen) == 0:
        return dash.no_update, {"color": color_chosen}
    else:
        dff = df[df["fund_extended_name"].isin(val_chosen)]
        fig = px.pie(dff, values="ytd_return", names="fund_extended_name", title="Year-to-Date Returns")
        fig.update_traces(textinfo="value+percent").update_layout(title_x=0.5)
        return fig, {"color": color_chosen}


if __name__ == '__main__':
    app.run_server(debug=True)