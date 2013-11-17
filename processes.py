from multiprocessing import Process, Manager
from pyparsley import PyParsley


def f(dictionary, ten_range):
    dictionary[1] = '1'
    ten_range.reverse()

    structure = {"title": "/div/div/div"}
    filepath = '/home/ubuntu/Programs/drupal/scrapy-parsley_wrappers/scrapy_parsley/tests/yelp/yelp.html'
    parselet = PyParsley(structure)
    dictionary['sub'] = parselet.parse(file=filepath, output='json')
    dictionary['2'] = 2
    dictionary[0.25] = None


if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, l))
    p.start()
    p.join()

    print d
    print l
    if 'sub' not in d:
        raise Exception('Parsing is not successful. For exact error message apply this parselet manually')
