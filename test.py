from dash import Dash, dcc, html
import multiprocessing
import time

# 示例的后台任务
def background_task():
    for i in range(5):
        print(f"{i} Background task running...")
        time.sleep(5)

# 创建 Dash 应用
app = Dash(__name__)


if __name__ == '__main__':
    # 启动后台进程
    p = multiprocessing.Process(target=background_task)
    p.start()
    
    # 启动 Dash 服务器
    app.run_server(debug=True)
    
    # 等待后台进程结束（可选）
    p.join()
