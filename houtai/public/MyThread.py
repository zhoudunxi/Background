#coding=UTF-8

from threading import Thread


class _MyThread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        try:
            self.result = self.func(self.args)
        except:
            #When the function without any argument.
            self.result = self.func()

    def get_result(self):
        return self.result


def MyThread(func, **args):
    """
    Call a function by multiple threads parallel, and return the function result.
    :param func: string, A function name.
    :param args: Must include a iteration argument object 'a'.
    :return: the function result.
    """

    threads = []
    results = []
    for i in args['a']:
            thread = _MyThread(func, i)
            threads.append(thread)
            thread.start()

    for t in threads:
            t.join()
            results.append(t.get_result())

    return results