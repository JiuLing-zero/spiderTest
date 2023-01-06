import multiprocessing

def process(index):
    print(f'Process: {index}')

if __name__ == '__main__':
    for i in range(5):
        # args必须是一个元组  所以i后面要有一个,
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()