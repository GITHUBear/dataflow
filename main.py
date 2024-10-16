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

app = dash.Dash(__name__)

# 初始化4个数据框
num_lines = 4
df_list = [pd.DataFrame(columns=['X', 'Y']) for _ in range(num_lines)]

app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=1000)  # 每秒更新
])

@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    global df_list
    for i in range(num_lines):
        base_path = os.path.basename(file_list[i])
        with data_observer.lock:
            data = data_observer.datas[base_path]
            print(f"########### update {data}")
            # 生成随机时间和数据
            new_row = pd.DataFrame([[x, y] for x, y in data], columns=['X', 'Y'])
            data_observer.datas[base_path].clear()

        # 将新行添加到相应的 DataFrame
        df_list[i] = pd.concat([df_list[i], new_row], ignore_index=True)

        # 按 Time 进行排序
        df_list[i] = df_list[i].sort_values(by='X').reset_index(drop=True)

    # 创建图表，合并三个 DataFrame 以便于绘图
    fig = px.line(pd.concat([df.assign(Line=f'Value_{i}') for i, df in enumerate(df_list)]), 
                           x='X', 
                           y='Y', 
                           color='Line',
                           title='Dynamic Data Visualization with Multiple Lines')
    return fig

if __name__ == '__main__':
    try:
        processes = []
        for producer in producers:
            process = multiprocessing.Process(target=producer.product)
            processes.append(process)
            process.start()
        
        data_observer.start(handler=handler)
        app.run_server(debug=True)
    except Exception:
        for process in processes:
            process.join()
        
        data_observer.stop()
