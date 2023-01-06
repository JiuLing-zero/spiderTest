import multiprocessing
import time

def process():
    print('Staring')
    time.sleep(5)
    print('Finished')

if __name__ == '__main__':
    p = multiprocessing.Process(target=process)
    print('Before:',p,p.is_alive())

    p.start()
    print('During:',p,p.is_alive())

    p.terminate()
    print('Terminate:',p,p.is_alive())
    # 在join时才会给进程 一些时间来更新状态，这时进程才会终止
    p.join()
    print('Joined:',p,p.is_alive())