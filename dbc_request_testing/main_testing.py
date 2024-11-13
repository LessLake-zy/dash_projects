import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 样例数据
data = [
    {"text": "Item 1", "value1": 5, "value2": -3},
    {"text": "Item 2", "value1": -1, "value2": 4},
    {"text": "Item 3", "value1": 10, "value2": -2},
]

# 主页布局
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # 用于页面导航
    html.Div(id='page-content')             # 动态加载内容
])

# 表格页面布局
def table_page():
    table_rows = []
    for row in data:
        # 根据value1和value2的值设置样式
        value1_style = {"color": "green"} if row["value1"] > 0 else {"color": "red"}
        value2_style = {"color": "green"} if row["value2"] > 0 else {"color": "red"}

        # 构建表格行
        table_rows.append(html.Tr([
            html.Td(dcc.Link(row["text"], href=f"/item/{row['text']}")),  # 超链接跳转
            html.Td(row["value1"], style=value1_style),
            html.Td(row["value2"], style=value2_style),
        ]))

    # 创建表格
    table = dbc.Table(
        # 添加表头
        [html.Thead(html.Tr([html.Th("Text"), html.Th("Value 1"), html.Th("Value 2")]))] +
        # 添加表行
        [html.Tbody(table_rows)],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

    return html.Div([html.H2("Table Page"), table])

# 显示单项内容页面布局
def item_page(item_text):
    return html.Div([
        html.H2("Item Page"),
        html.P(f"Selected item: {item_text}"),
        html.Br(),
        dcc.Link("Back to Table", href="/")
    ])

# 回调用于动态加载页面内容
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname and pathname.startswith("/item/"):
        item_text = pathname.split("/item/")[1]
        return item_page(item_text)  # 加载item页面
    else:
        return table_page()  # 默认加载表格页面

# 运行应用
if __name__ == "__main__":
    app.run_server(debug=True)