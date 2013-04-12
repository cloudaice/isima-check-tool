#-*-coding: utf-8-*-
# @author: xiangchao<cloudaice@gmail.com>
# @file: Mongodb common connections

from pymongo import Connection
cnn = None


def conn(host, port):
    """
    Mongodb connections pool
    """
    global cnn
    if cnn is None:
        cnn = Connection(host, port, max_pool_size=10)
        return cnn
