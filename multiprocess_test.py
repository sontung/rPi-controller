from multiprocessing import Queue, Process


def process(x, queue):
    queue.put(x**2)


class Handler:
    def __init__(self):
        self.x = 0

    def run(self, queue):
        self.x += 1
        if self.x % 4 == 0:
            incrementer = Process(target=process, args=(self.x, queue))
            incrementer.start()
            print queue.get()
            incrementer.terminate()
            incrementer.join()


if __name__ == "__main__":
    handler = Handler()
    queue1 = Queue()
    while True:
        handler.run(queue1)
