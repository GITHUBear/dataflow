import os
from producer import DataProducer
from observer import DataObserver, FileChangeHandler
import multiprocessing

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px

file_list = ['./test1.txt', './test2.txt', './test3.txt', './test4.txt']

def do_product(
    producer: DataProducer
):
    producer.product()

# def dash_plot():
#     app = dash.Dash(__name__)
#     app.layout = html.Div([
#         dcc.Graph(id='live-graph'),
#         dcc.Interval(id='interval-component', interval=1000)  # 每秒更新
#     ])
#     num_lines = 4
#     df_list = [pd.DataFrame(columns=['X', 'Y']) for _ in range(num_lines)]
#     @app.callback(Output('live-graph', 'figure'),
#                   Input('interval-component', 'n_intervals'))
#     def update_graph(n):
#         for i in range(num_lines):
#             base_path = os.path.basename(file_list[i])
#             with data_observer.lock:
#                 data = data_observer.datas[base_path]
#                 print(f"########### update {data}")
#                 new_row = pd.DataFrame([[x, y] for x, y in data], columns=['X', 'Y'])
#                 data_observer.datas[base_path].clear()

#             df_list[i] = pd.concat([df_list[i], new_row], ignore_index=True)
#             df_list[i] = df_list[i].sort_values(by='X').reset_index(drop=True)

#         fig = px.line(pd.concat([df.assign(Line=f'Value_{i}') for i, df in enumerate(df_list)]), 
#                                x='X', 
#                                y='Y', 
#                                color='Line',
#                                title='Dynamic Data Visualization with Multiple Lines')
#         return fig
    
#     app.run_server(debug=True)

if __name__ == "__main__":
    producers = [
        DataProducer(
            "p1", 
            [(1.0, 2.0), (3.0, 4.0), (3.4, 1.0)],
            file_list[0],
            5000,
            2000,
        ),
        DataProducer(
            "p2", 
            [(0.5, 1.323), (0.99, 1.2343), (3.13, 1.132)],
            file_list[1],
            5000,
            2000,
        ),
        DataProducer(
            "p3", 
            [(1.0, 2.0), (3.0, 9.0), (9.4, 9.0)],
            file_list[2],
            5000,
            2000,
        ),
        DataProducer(
            "p4", 
            [(1.33, 3.33), (9.345, 4.0), (9.4, 1.0)],
            file_list[3],
            5000,
            2000,
        ),
    ]

    data_observer = DataObserver(file_list)
    handler = FileChangeHandler(data_observer)

    processes = []
    for producer in producers:
        process = multiprocessing.Process(target=do_product, args=(producer,))
        processes.append(process)

    for i, process in enumerate(processes):
        print(f"start {i}")
        process.start()

    data_observer.start(handler=handler)
    
    # dash_plot()
