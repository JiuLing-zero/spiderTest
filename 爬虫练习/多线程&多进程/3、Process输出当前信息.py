import multiprocessing
import time

def process(index):
    time.sleep(index)
    print(f'Process: {index}')

if __name__ == '__main__':
    for i in range(15):
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()
    # 查看cpu核心的数量
    print(f'CPU number: {multiprocessing.cpu_count()}')
    # active_children()获取正在活跃的进程列表
    for p in multiprocessing.active_children():
        print(f'Child process name: {p.name} id: {p.pid}')
    print('Process Ended')