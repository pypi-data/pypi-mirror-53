#coding=utf8

from .statement import (
    formatColumns,
    formatWhere,
)


def iterChunkSize(limit, chunkSize):
    n = (limit + chunkSize - 1) / chunkSize
    for i in range(n):
        yield min(limit, (i+1) * chunkSize) - (i * chunkSize)


class Chunk(object):
    def __init__(self, table, where, columns, orderBy, limit, chunkSize, dictCursor):
        self.table = table
        self.where = where
        self.columns = columns
        self.orderBy = orderBy
        self.limit = limit
        self.chunkSize = chunkSize
        self.dictCursor = dictCursor

        if self.needChunk:
            if not self.dictCursor:
                raise Exception('chunk select must use dict cursor')
            if self.where and not isinstance(self.where, (dict, basestring)):
                raise Exception('chunk select where argument type error')

    @property
    def needChunk(self):
        return self.chunkSize < self.limit

    @property
    def formatColumns(self):
        if not self.needChunk:
            return formatColumns(self.columns)

        columns = self.columns
        if not columns:
            pass
        elif isinstance(columns, list) and 'id' not in columns:
            columns.insert(0, 'id')
        elif isinstance(columns, basestring) and 'id' not in columns.split(','):
            columns = 'id,' + columns

        return formatColumns(columns)

    @property
    def chunkedWhere(self):
        if not self.needChunk:
            return formatWhere(self.where)

        #TODO
        return self.where

    @property
    def chunkedLimit(self):
        pass

    @property
    def chunkedOrderBy(self):
        pass

    def execute(self, cursor):
        pass

