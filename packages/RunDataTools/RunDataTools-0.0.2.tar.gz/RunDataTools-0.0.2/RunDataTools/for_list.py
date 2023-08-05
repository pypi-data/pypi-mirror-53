# -*- coding: utf-8 -*-
# @Time     : 2019/6/14 23:25
# @Author   : Run 
# @File     : for_list.py
# @Software : PyCharm


from collections import Iterable


def flatten_iterable(its, deep=False):
    """
    flatten instance of Iterable to list
    :param its: instance of Iterable
    :param deep: demo: [[[1], [2], [3]], 4], if True, flatten to [1, 2, 3, 4], if False, flatten to [[1], [2], [3], 4].
    :return: list
    """
    res = []
    for it in its:
        if isinstance(it, Iterable):
            if deep:
                res += flatten_iterable(it, True)
            else:
                res += list(it)
        else:
            res.append(it)
    return res


# if __name__ == "__main__":
#     l1 = [[[1], [2], [3]], 4]
#     print(flatten_iterable(l1))
#     print(flatten_iterable(l1, True))
#
#     l2 = [[1, 2], 3, {4, 5}, 6, (7, 8), [[[[{9}, 10]]]]]
#     print(flatten_iterable(l2))
#     print(flatten_iterable(l2, True))
