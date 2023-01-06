# 在4的基础上设置了守护进程
from multiprocessing import Process
import time

class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print(f'Pid: {self.pid} LoopCount: {count}')

if __name__ == '__main__':
    # 传参2,3,4
    for i in range(2,5):
        p = MyProcess(i)
        # 设置守护进程，主进程结束时会同时结束
        p.daemon = True
        p.start()
        # join后主进程会等待子进程，但为了避免长时间等待 以及 等待都运行完时设置守护进程没有意义
        # 可以传参一个数字，来表明主进程能等待子进程的期限是多久
        p.join(1)
 
    print('Main Process ended')
