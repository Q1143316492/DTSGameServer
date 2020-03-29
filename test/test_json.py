# coding=utf-8
import json


def unicode_convert(item):
    if isinstance(item, dict):
        return { unicode_convert(key): unicode_convert(value) for key, value in item.iteritems() }
    elif isinstance(item, list):
        return [ unicode_convert(element) for element in item ]
    elif isinstance(item, unicode):
        return item.encode('utf-8')
    else:
        return item


if __name__ == '__main__':

    # name = u'asd'
    # print name, type(name)
    # name = name.encode('utf-8')
    # print name, type(name)

    a = { "username" : "cwl", "password" : "你好"}

    ret = json.dumps(a, ensure_ascii=True)

    # print ret, type(ret)

    # ret = json.loads(ret)
    #
    # print ret, type(ret)

    # ret = unicode_convert(ret)
    #
    # print ret, type(ret)

    # [{"username": "cwl", "password": "\u4f60\u597d"}]

    a = {"name":"cwl", "passwd" : 123456}

    s = json.dumps(a)
    print s, type(s)

    try:
        print json.loads(s)
    except ValueError as err:
        print err