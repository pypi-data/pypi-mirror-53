# -*- coding: utf-8 -*-
# @Time     : 2019/4/10 14:32
# @Author   : Run 
# @File     : utils.py
# @Software : PyCharm

import numpy as np
import pandas as pd
from string import ascii_lowercase
import time
import logging
import random


def gen_df(row_num, col_num, lb=0, ub=100):
    """
    generate dataframe consist of int data and lowercase_headers
    :param row_num:
    :param col_num:
    :param lb: lower bound
    :param ub: upper bound
    :return:
    """
    shape = (row_num, col_num)
    data = np.random.randint(lb, ub, shape)
    cols = list(ascii_lowercase[:col_num])
    df = pd.DataFrame(data, columns=cols)
    print("shape:", df.shape)
    print(df.head(2))
    return df


def timer(func):
    """
    a decorator for timing
    old function results         new function results
    r1, r2, ..., rn       ->     (r1, r2, ..., rn), cost_time

    :param func:
    :return:
    """

    def dec(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        cost_t = t2 - t1
        if cost_t < 1:  # 耗时低于1s重复10遍
            n = 10
        elif cost_t < 10:  # 耗时低于10s重复5遍
            n = 5
        else:  # 耗时超过10s，不进行重复试验
            n = 1
            #
        for _ in range(n - 1):
            t1 = time.time()
            res = func(*args, **kwargs)
            t2 = time.time()
            cost_t += t2 - t1
        cost_t /= n
        print("{0} cost time: {1}s, {2} loops".format(func.__name__, t2 - t1, n))
        return res

    return dec


class Timer:
    """
    mainly for timing execution

    Examples
    --------
    timer = Timer()
    <code_block1: to measure>
    timer.toc("block1")
    <code_block2: not to measure>
    timer.tic()
    <code_block3: to measure>
    timer.toc("block3")
    <code_block4: to measure>
    timer.toc("block4")
    timer.total()  # block1's time + block3's time + block4's time
    timer.order()
    """
    def __init__(self):
        self.index = 0
        self.records = []  # [(index, comments, cost_time), ...]
        self.prev = time.time()

    def tic(self):
        self.prev = time.time()

    def toc(self, comments="", display=True, round_num=3):
        cost_time = round(time.time() - self.prev, round_num)
        self.records.append((self.index, comments, cost_time))
        if display:
            # print("{}. {} {}s".format(self.index, comments, cost_time))
            print("{} {}s".format(comments, cost_time))
        self.index += 1
        self.prev = time.time()

    def total(self):
        return sum(x[2] for x in self.records)

    def order(self, descending=True):
        """

        :param descending: bool
        :return:
        """
        return sorted(self.records, key=lambda x: x[2], reverse=descending)


def gen_logger(logger_name=None, logger_level=logging.WARNING):
    """

    :param logger_name:
    :param logger_level:
    :return:
    """
    logger = logging.getLogger(str(random.random()))  # set random name to avoid influence between different loggers
    logger.setLevel(logger_level)  # set log's level
    logger.name = logger_name

    if logger_name is None:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    else:
        formatter = logging.Formatter('[%(asctime)s] [%(name)s~%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    stream_handler = logging.StreamHandler()  # print to screen
    # file_handler = logging.FileHandler("output.log", mode='w')  # print to file `output.log`
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger








