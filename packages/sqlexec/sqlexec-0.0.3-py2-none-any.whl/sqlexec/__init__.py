#coding=utf8

__version__ = '0.0.3'

from .client import Client
from .table import Table
from .statement import e


_globalClient = None


def connect(host='127.0.0.1', port=3306, user='root', passwd='', db='', charset='utf8', autocommit=True):
    global _globalClient
    _globalClient = Client.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset, autocommit=autocommit)

def connectDSN(dsn):
    global _globalClient
    _globalClient = Client.connectDSN(dsn)


def getTable(name):
    return _globalClient.getTable(name)

def enableLog(enabled=True):
    return _globalClient.enableLog(enabled)


def insert(table, kvs, ignore=False):
    return _globalClient.insert(table, kvs, ignore)

def insertIgnore(table, kvs):
    return _globalClient.insertIgnore(table, kvs)

def insertMany(table, rows, ignore=False):
    return _globalClient.insertMany(table, rows, ignore)

def delete(table, idOrWhere):
    return _globalClient.delete(table, idOrWhere)

def update(table, idOrWhere, kvs):
    return _globalClient.update(table, idOrWhere, kvs)

def upsert(table, defaults, kvs):
    return _globalClient.upsert(table, defaults, kvs)

def replace(table, kvs):
    return _globalClient.replace(table, kvs)

def selectOne(table, idOrWhere, columns=None, dictCursor=True):
    return _globalClient.selectOne(table, idOrWhere, columns, dictCursor)

def selectMany(table, where, columns=None, chunkSize=2000, limit=2000, dictCursor=True):
    return _globalClient.selectMany(table, where, columns, limit, chunkSize, dictCursor)
