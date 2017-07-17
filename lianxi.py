#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/11 下午10:23
# @Author  : Sylor_Huang
# @File    : test11.py
# @Software: PyCharm
def gen(n):
    for i in range(n):
        yield i**2

for i in gen(5):
    print(i," ",end="")
