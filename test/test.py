
class TestLock:

    def __init__(self):
        pass

    def __enter__(self):
        print "enter"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "exit"


if __name__ == '__main__':
    t = TestLock()

    with t:
        pass