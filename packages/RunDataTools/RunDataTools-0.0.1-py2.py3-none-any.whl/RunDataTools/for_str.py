# -*- coding: utf-8 -*-
# @Time     : 2019/6/14 23:28
# @Author   : Run 
# @File     : for_str.py
# @Software : PyCharm


def check_brackets(strs):
    """
    check if brackets(and parentheses) come in pairs, besides, left should occur before right.
    :param strs:
    :return: bool
    """
    rights = {')', ']', '}'}
    lefts = {'(': ')', '[': ']', '{': '}'}
    l = []
    for i, c in enumerate(strs):
        if c in lefts:
            l.append((i, c))
        elif c in rights:
            if len(l) == 0:
                print("redundant '{}' at position {}".format(c, i))
                return False
            i0, c0 = l.pop()
            if lefts[c0] != c:
                print("unmatched '{}' at position {} with '{}' at position {}".format(c0, i0, c, i))
                return False
    if len(l) > 0:
        print("redundant parentheses and their positions: {}".format(l))
        return False
    return True


# if __name__ == "__main__":
#     print(check_brackets("{(a, b): {c, ...}, ...}"))
#     print(check_brackets("{"))
#     print(check_brackets("{)(}"))
