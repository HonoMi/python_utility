from multiprocessing import Process, Pipe


class MyPool:

    def __init__(self, proc_num=1):
        self.proc_num = proc_num

    def map(self, func, args):

        def pipefunc(conn, arg):
            conn.send(func(arg))
            conn.close()
        ret = []
        k = 0
        while(k < len(args)):
            plist = []
            clist = []
            end = min(k + self.proc_num, len(args))
            for arg in args[k:end]:
                pconn, cconn = Pipe()
                plist.append(Process(target = pipefunc, args=(cconn, arg,)))
                clist.append(pconn)
            for p in plist:
                p.start()
            for conn in clist:
                ret.append(conn.recv())
            for p in plist:
                p.join()
            k += self.proc_num
        return ret


class Test:

    def fuga(self, x):
        return x * x

    def hoge(self):
        p = MyPool(8)
        print(p.map(self.fuga, range(10)))


if __name__ == '__main__':
    test = Test()
    test.hoge()
