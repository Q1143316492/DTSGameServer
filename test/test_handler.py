# coding=utf-8


class TestClass:

    def __init__(self):
        pass

    @staticmethod
    def test_func(req, res):
        print req
        print res


def func(req, res):
    print req
    print res


handler_dict = dict()


def add(id, handler):
    handler_dict[id] = handler


if __name__ == '__main__':

    add(1000, func)
    func_handler = handler_dict[1000]
    # func_handler("asd", "qwe")

    add(1001, TestClass.test_func)
    class_func_handler = handler_dict[1001]

    class_func_handler("asd", "eee")

    # print type(func)
    # print type(TestClass.test_func)
    #
    # print callable(func)

    print None in handler_dict