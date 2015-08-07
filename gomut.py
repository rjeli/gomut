import time
from multiprocessing import Process, Queue
import queue
import unittest

def go(func, *args):
    p = Process(target=func, args=args)
    p.start()

def select(chans):
    while True:
        for c, h in chans.items():
            try:
                val = c._queue.get(False)
            except queue.Empty:
                continue
            h(val)
            return

class chan:
    def __init__(self):
        self._queue = Queue()
        self._closed = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.get()
        except queue.Empty:
            raise StopIteration

    def put(self, x):
        self._queue.put(x)

    def get(self):
        if self._closed:
            return self._queue.get(False)
        else:
            return self._queue.get()

    def close(self):
        self._closed = True

class TestGoLib(unittest.TestCase):
    def test_go(self):
        c = chan()

        def f():
            c.put('hi!')

        go(f)
        self.assertEqual(c.get(), 'hi!')

        def sq(x):
            c.put(x*x)

        go(sq, 12)
        self.assertEqual(c.get(), 144)

    def test_chan(self):
        c = chan()

        c.put(1)
        self.assertEqual(c.get(), 1)

        c.put(2)
        c.put(3)
        self.assertEqual(c.get(), 2)
        self.assertEqual(c.get(), 3)

    def test_select(self):
        c1 = chan()
        c2 = chan()

        def f1():
            time.sleep(1)
            c1.put('one')
        go(f1)

        def f2():
            time.sleep(2)
            c2.put('two')
        go(f2)

        res = []
        for i in range(0, 2):
            select({
                c1: lambda x: res.append(x),
                c2: lambda x: res.append(x),
            })

        self.assertEqual(res, ['one', 'two'])

    def test_range(self):
        c = chan()
        c.put('one')
        c.put('two')
        c.close()

        res = []
        for elem in c:
            res.append(elem)

        self.assertEqual(res, ['one', 'two'])

if __name__ == '__main__':
    unittest.main()
