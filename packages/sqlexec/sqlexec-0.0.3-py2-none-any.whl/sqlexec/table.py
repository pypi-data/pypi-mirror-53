#coding=utf8
import contextlib


class Table(object):
    def __init__(self, client, table):
        self.client = client
        self.table = table

    def insert(self, kvs, ignore=False):
        return self.client.insert(self.table, kvs, ignore)

    def insertIgnore(self, kvs):
        return self.client.insertIgnore(self.table, kvs)

    def insertMany(self, rows, ignore=False):
        return self.client.insertMany(self.table, rows, ignore)

    def delete(self, idOrWhere):
        return self.client.delete(self.table, idOrWhere)

    def update(self, idOrWhere, kvs):
        return self.client.update(self.table, idOrWhere, kvs)

    def upsert(self, defaults, kvs):
        return self.client.upsert(self.table, defaults, kvs)

    def replace(self, kvs):
        return self.client.replace(self.table, kvs)

    def selectOne(self, idOrWhere, columns=None, dictCursor=True):
        return self.client.selectOne(self.table, idOrWhere, columns)

    def selectMany(self, where, columns=None, limit=2000, chunkSize=2000, dictCursor=True):
        return self.client.selectMany(self.table, where, columns, limit, chunkSize)
