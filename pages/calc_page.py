from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np

def get_layout():
    return html.Div([
        html.H1('売上予測シミュレーション'),
        html.Div([
            html.Div([
                html.Label('予測期間（月）'),
                dcc.Input(id='months', type='number', value=6, min=3, max=24, persistence=True, persistence_type='session', style={'width': '100%', 'padding': '12px', 'fontSize': '16px', 'boxSizing': 'border-box'}),
                html.Label('グラフの種類', style={'marginTop': '15px', 'display': 'block'}),
                dcc.Dropdown(id='graph-type', options=[
                    {'label': '折れ線', 'value': 'line'},
                    {'label': '棒', 'value': 'bar'}
                ], value='line', persistence=True, persistence_type='session'),
                html.Button('予測', id='calc-btn', n_clicks=0,
                           style={'width': '100%', 'padding': '15px', 'fontSize': '18px', 'marginTop': '20px', 'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none','borderRadius': '5px', 'cursor': 'pointer', 'fontWeight': 'bold'})
            ], style={'width': '350px', 'height': '500px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
            html.Div(id='graph', style={'flex': '1', 'marginLeft': '20px', 'height': '500px'})
        ], style={'display': 'flex', 'gap': '20px', 'alignItems': 'stretch'})
    ])

def register_callbacks(app, df):
    @app.callback(
        Output('graph', 'children'),
        [Input('calc-btn', 'n_clicks'), Input('graph-type', 'value')],
        State('months', 'value')
    )
    def simulate(n_clicks, graph_type, months):
        if n_clicks == 0:
            # 初期表示
            df_with_type = df.assign(区分='実績')
            if graph_type == 'bar':
                fig = px.bar(df_with_type, x='月', y='売上', color='区分')
            else:
                fig = px.line(df_with_type, x='月', y='売上', color='区分', markers=True)
            fig.update_layout(
                title='売上データ',
                xaxis_title='月',
                yaxis_title='売上（万円）',
                hovermode='x unified',
                height=500
            )
            return dcc.Graph(figure=fig, style={'height': '100%'})

        # データ生成
        growth = np.random.uniform(5, 20)
        volatility = np.random.uniform(10, 30)
        changes = 1 + (growth + np.random.uniform(-volatility, volatility, months)) / 100
        values = df['売上'].iloc[-1] * np.cumprod(changes)

        # グラフ作成
        if graph_type == 'bar':
            combined = pd.concat([
                df.assign(区分='実績'),
                pd.DataFrame({'月': [f'{i+6}月' for i in range(months)], '売上': values, '区分': '予測'})
            ], ignore_index=True)
            fig = px.bar(combined, x='月', y='売上', color='区分')
        else:
            combined = pd.concat([
                df.assign(区分='実績'),
                df.iloc[[-1]].assign(区分='予測'),  # 接続用ポイント
                pd.DataFrame({'月': [f'{i+6}月' for i in range(months)], '売上': values, '区分': '予測'})
            ], ignore_index=True)
            fig = px.line(combined, x='月', y='売上', color='区分', markers=True)

        fig.update_layout(
            title=f'シミュレーション（実行: {n_clicks}回）',
            xaxis_title='月',
            yaxis_title='売上（万円）',
            hovermode='x unified',
            height=500
        )

        return dcc.Graph(figure=fig, style={'height': '100%'})