import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav_bar = dbc.NavbarSimple([
    dbc.NavLink(f"{page['name']}", href=page['relative_path'], style={'color': 'white'}) for page in dash.page_registry.values()
],
    brand='Dash App',
    brand_href="127.0.0.1:8050",
    brand_style={'color': 'white', 'font-weight': 'bold'},
    color="primary",
    fluid=True,
    className='mb-4',
)

app.layout = dbc.Container([
    nav_bar,
    dash.page_container
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
