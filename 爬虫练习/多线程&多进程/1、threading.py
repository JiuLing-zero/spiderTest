import threading
import time


def target(second):
    print(f'Threding {threading.current_thread().name} is running')
    print(f'Threding {threading.current_thread().name} sleep {second}s')
    time.sleep(second)
    print(f'Threding {threading.current_thread().name} is ended')

def test1():
    print(f'Threading {threading.current_thread().name} is running')
    for i in [1,5]:
        t = threading.Thread(target=target, args=[i])
        t.start()
        # 不join时主线程会直接结束，不会等待子线程运行。各个子线程会继续运行到自己结束
        t.join()
    print(f'Threading {threading.current_thread().name} is ended')

def test2():
    print(f'Threading {threading.current_thread().name} is running')
    t1 = threading.Thread(target=target, args=[2])
    t1.start()
    t2 = threading.Thread(target=target, args=[5])
    # 设置为守护线程，意味着这个线程不重要，比主线程慢时会强制结束
    t2.setDaemon(True)
    t2.start()
    # 如果两个都调用join，则主线程仍会等待所有子线程都运行完才结束
    print(f'Threading {threading.current_thread().name} is ended')


count = 0
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global count
        lock.acquire()
        temp = count + 1
        time.sleep(0.001)
        count = temp
        lock.release()

# 声明了一个lock对象
lock = threading.Lock()

def test3():
    threads = []
    for _ in range(1000):
        thread = MyThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f'Final count: {count}')

if __name__ == '__main__':
    # 两个简单线程
    # test1()
    # 守护线程
    # test2()
    # 加锁保护
    test3()