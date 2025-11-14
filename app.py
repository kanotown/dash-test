import dash
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from pages import calc_page, test_page

app = dash.Dash(__name__)
server = app.server  # デプロイ用

# テストデータ
df = pd.DataFrame({
    '月': ['1月', '2月', '3月', '4月', '5月'],
    '売上': [100, 150, 130, 180, 200]
})

# ナビゲーションボタンのスタイル
NAV_BTN = {'color': 'white', 'padding': '8px 20px', 'margin': '0 5px', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer', 'fontWeight': 'bold'}

# レイアウト
app.layout = html.Div([
    # ナビ
    html.Div([
        html.Div('📊 Sample', style={'color': 'white', 'fontSize': '24px', 'fontWeight': 'bold'}),
        html.Div([
            html.Button('予測', id='nav-calc'),
            html.Button('テスト', id='nav-test'),
        ])
    ], style={'position': 'fixed', 'top': 0, 'left': 0, 'right': 0, 'height': '60px', 'backgroundColor': "#3c3aa0", 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '0 1rem', 'zIndex': 1000}),

    # ページ
    html.Div([
        html.Div(id='page-calc', children=calc_page.get_layout()),
        html.Div(id='page-test', children=test_page.get_layout(), style={'display': 'none'})
    ], style={'padding': '5rem 1rem 1rem', 'maxWidth': '1200px', 'margin': 'auto', 'textAlign': 'center'})
])

@app.callback(
    [Output('page-calc', 'style'), Output('page-test', 'style'), Output('nav-calc', 'style'), Output('nav-test', 'style')],
    [Input('nav-calc', 'n_clicks'), Input('nav-test', 'n_clicks')]
)
def switch(_, __):
    ctx = dash.callback_context
    page = 'calc' if not ctx.triggered or 'calc' in ctx.triggered[0]['prop_id'] else 'test'

    return (
        {'display': 'block' if page == 'calc' else 'none'},
        {'display': 'block' if page == 'test' else 'none'},
        {**NAV_BTN, 'backgroundColor': "#6e6cec" if page == 'calc' else 'transparent'},
        {**NAV_BTN, 'backgroundColor': '#6e6cec' if page == 'test' else 'transparent'}
    )

calc_page.register_callbacks(app, df)

if __name__ == '__main__':
    app.run(debug=True)
