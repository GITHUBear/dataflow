import os
from watchdog.observers import Observer
from producer import DataProducer
from observer import DataObserver, FileChangeHandler
import multiprocessing

import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

fig, ax = plt.subplots()
lines = [ax.plot([], [], label=f'{file_path}')[0] for file_path in file_list]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.legend()

def update_plot(frame, lines, data_lists, lock):
    with lock:
        for i, line in enumerate(lines):
            base_path = os.path.basename(file_list[i])
            data = data_lists[base_path]

            x_datas = [x for x, _ in data]
            y_datas = [y for _, y in data]

            print(f"update_plot: {base_path}: {x_datas} & {y_datas}")

            line.set_xdata(x_datas)
            line.set_ydata(y_datas)
    return lines

if __name__ == '__main__':
    processes = []
    for producer in producers:
        process = multiprocessing.Process(target=producer.product)
        processes.append(process)
        process.start()
    
    data_observer.start(handler=handler)
    
    ani = animation.FuncAnimation(
        fig,
        update_plot,
        fargs=(lines, data_observer.datas, data_observer.lock),
        interval=1000,
        blit=True
    )
    
    plt.show()

    for process in processes:
        process.join()
    
    data_observer.stop()
