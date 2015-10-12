import multiprocessing
import time


def handler(queue):
    val = False
    x = time.time()
    while True:
        if time.time() - x == 5:
            print "handling"
            val = not val
            queue.put([val])
            x = time.time()


def listener():
    x = 0
    while True:
        x += 1


if __name__ == "__main__":
    q = multiprocessing.Queue()
    h = multiprocessing.Process(target=handler, args=(q,))
    l = multiprocessing.Process(target=listener)
    h.start()
    while True:
        val1 = q.get()
        if val1 == [True]:
            print "start listening"
            l.start()
        elif val1 == [False]:
            print "terminate"
            l.terminate()
            l.join()
            l = multiprocessing.Process(target=listener)