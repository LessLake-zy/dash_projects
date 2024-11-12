import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 创建数据
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Value": [10, -5, 8, -3]
}
df = pd.DataFrame(data)

# 生成表格行，应用条件格式
table_rows = []
for index, row in df.iterrows():
    # 第一列不做判断，直接显示
    name_cell = html.Td(row["Name"])

    # 根据值确定颜色
    value_color = "green" if row["Value"] > 0 else "red"
    value_cell = html.Td(row["Value"], style={"color": value_color})

    # 创建表格行
    table_rows.append(html.Tr([name_cell, value_cell]))

# 创建Dash应用布局
app.layout = dbc.Container([
    html.H3("示例表格"),
    dbc.Table(
        # 表头
        [html.Thead(html.Tr([html.Th("Name"), html.Th("Value")]))] +
        # 表体
        [html.Tbody(table_rows)],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        className="table"
    )
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)