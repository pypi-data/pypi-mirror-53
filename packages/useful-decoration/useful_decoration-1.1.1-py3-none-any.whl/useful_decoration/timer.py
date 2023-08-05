#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@User    : frank 
@Time    : 2019/9/22 10:09
@File    : timer.py
@Email  : frank.chang@xinyongfei.cn
"""
import time
from functools import partial, wraps

from loguru import logger

now = now_int = time.time


def fn_timer(fn=None, *, prefix="", interval=0.0):
    """
    计算 fn  的运算时间

    :param fn: 函数, callable 对象
    :param prefix: 给函数一个标识 前缀
    :param interval: float  给定一个阈值 ,超过某一个阈值,就记录时间. 否则不记录,默认是0 ,记录所有的函数的运行时间.
    :return:
    """
    if fn is None:
        return partial(fn_timer, prefix=prefix)

    @wraps(fn)
    def function_timer(*args, **kwargs):
        start = now()
        result = fn(*args, **kwargs)
        t = now() - start
        if t > interval:
            logger.info(f'{prefix}{fn.__name__} total running time {now() - start} seconds')
        return result

    return function_timer


@fn_timer()
def get_token():
    time.sleep(3)
    return 0


@fn_timer(prefix='frank_')
def pickup():
    print("pickup is running.")
    time.sleep(2)
    print("pickup is end.")


if __name__ == '__main__':
    # get_token()
    pickup()


    pass
