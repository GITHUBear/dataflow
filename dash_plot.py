import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from filelock import FileLock
import argparse
import pandas as pd
import os
import plotly.express as px

marker_symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'star']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('-i', '--interval', type=int, default=1000)

    args = parser.parse_args()
    files = args.files
    actual_files = [f"{file}.tmp" for file in files]

    app = dash.Dash(__name__)
    app.layout = html.Div([
        dcc.Graph(
            id='live-graph',
            style={'height': '80vh', 'width': '100%'}
        ),
        dcc.Interval(id='interval-component', interval=args.interval)  # 每秒更新
    ])
    num_lines = len(actual_files)
    df_list = [pd.DataFrame(columns=['Recall', 'QPS']) for _ in range(num_lines)]
    line_offsets = [0 for _ in actual_files]

    @app.callback(Output('live-graph', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph(n):
        for idx, path in enumerate(actual_files):
            if not os.path.exists(path):
                continue
            
            datas = []
            with FileLock(f"{path}.lock"):
                with open(path, 'r') as f:
                    cur_line_offset = 0
                    for line in f:
                        if line_offsets[idx] > cur_line_offset:
                            cur_line_offset += 1
                            continue

                        x, y = map(float, line.strip().split(' '))
                        datas.append((x, y))
                        cur_line_offset += 1
                    line_offsets[idx] = cur_line_offset

            new_row = pd.DataFrame([[x, y] for x, y in datas], columns=['Recall', 'QPS'])
            df_list[idx] = pd.concat([df_list[idx], new_row], ignore_index=True)
            df_list[idx] = df_list[idx].sort_values(by='Recall').reset_index(drop=True)

        fig = px.line(pd.concat([df.assign(Line=f'{actual_files[i]}') for i, df in enumerate(df_list)]), 
                                x='Recall', 
                                y='QPS', 
                                color='Line',
                                title='ANN-Benchmark',
                                markers=True)
        
        for i, line in enumerate(fig.data):
            line.marker.symbol = marker_symbols[i % len(marker_symbols)]

        return fig
    
    app.run_server(debug=True)

