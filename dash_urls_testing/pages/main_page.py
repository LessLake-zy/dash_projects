import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd

dash.register_page(__name__, path='/')

cards_pd = dbc.Card([
    dbc.CardHeader(html.H5('PD AUM'), className='card-title'),
    dbc.CardBody([html.H6('USD 888 Million')])
], className='bg-secondary', style={'height': '180px', 'color': 'white'})

cards_td = dbc.Card([
    dbc.CardHeader(html.H5('TD AUM'), className='card-title'),
    dbc.CardBody([html.H6('USD 999 Million')]),
    dbc.CardFooter([html.H6('+ 111 Million')])
], className='bg-success', style={'height': '180px', 'color': 'white'})

cards_callout = dbc.Card([
    dbc.CardHeader(html.H5('Callout'), className='card-title'),
    dbc.CardBody([html.H6("On today's SOD/EOD report, we found that xxxx")]),
], className='bg-danger', style={'height': '180px', 'color': 'white'})

cards = dbc.Container([
    dbc.Row([
        dbc.Col([cards_pd], width=3, className='mb-4'),
        dbc.Col([cards_td], width=3, className='mb-4'),
        dbc.Col([cards_callout], width=6, className='mb-4'),
    ]),
], fluid=True, style={'margin-right': '5px'})

# 获取文件
file_path = r'/Users/zhangyi/Desktop/hsbc_dash/hsbc.csv'
df = pd.read_csv(file_path, keep_default_na=False, parse_dates=['date'])


# 提取数据
def get_data(df):
    yesterday, today = '2024-10-17', '2024-10-18'
    new_dict = {}
    platforms = list(df['platform'].unique())
    owner_teams = list(df['owner_team'].unique())
    for owner in owner_teams:
        temp_list = []
        dff = df[df['owner_team'] == owner]
        for plat in platforms:
            td_value = dff[(dff['date'] == today) & (dff['platform'] == plat)]['open_issues'].values[0]
            pd_value = dff[(dff['date'] == yesterday) & (dff['platform'] == plat)]['open_issues'].values[0]
            diff = td_value - pd_value
            per = round(diff / pd_value * 100, 2)
            final_value = f"""{td_value} [{diff}|{per}%]"""
            temp_list.append(final_value)
        new_dict[owner] = temp_list
    df_new = pd.DataFrame.from_dict(new_dict)
    df_new['platforms'] = platforms
    owner_teams.insert(0, 'platforms')
    df_new = df_new[owner_teams]
    return df_new


df_table = get_data(df)


def generate_table(df_table):
    table_header = [
        html.Thead(html.Tr([html.Th(col) for col in df_table.columns]))
    ]
    table_body = []
    for index, row in df_table.iterrows():
        # platform_cell = html.Td(row["platforms"])
        table_row = []
        for value in row:
            check_value = int(value.split('[')[1].split('|')[0])
            color = 'green' if check_value > 0 else 'red' if check_value < 0 else 'black'
            table_row.append(html.Td(value, style={"color": color}))
        table_body.append(html.Tr(table_row))

    return dbc.Table(table_header + [html.Tbody(table_body)], bordered=True, hover=True, responsive=True,
                     striped=True, style={'margin-right': '5px', 'margin-left': '5px'})


layout = html.Div([
    cards,
    generate_table(df_table),
])
