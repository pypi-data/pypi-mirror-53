#coding=utf8
import urlparse
import contextlib

import MySQLdb

from .table import Table
from .statement import (formatWhereKV,
                        formatSetKV,
                        formatValues,
                        formatWhere,
                        formatSlots,
                        formatColumns,
                        )


class Client(object):
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='', db='', charset='utf8', autocommit=True):
        self.c = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        if autocommit:
            self.c.autocommit(True)

        self._logLevel = 0

    def _log(self, sql):
        if self._logLevel > 0:
            print sql

    @classmethod
    def connect(cls, host='127.0.0.1', port=3306, user='root', passwd='', db='', charset='utf8', autocommit=True):
        return cls(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset, autocommit=autocommit)

    @classmethod
    def connectDSN(cls, dsn):
        r = urlparse.urlparse(dsn)
        return cls(
            host=r.hostname,
            port=r.port,
            user=r.username,
            passwd=r.password,
            db=r.path.strip('/'),
        )

    def enableLog(self, enabled=True):
        self._logLevel = 1 if enabled else 0

    def getTable(self, name):
        return Table(self, name)

    @contextlib.contextmanager
    def cursor(self, dictCursor=False):
        cursorclass = MySQLdb.cursors.DictCursor if dictCursor else None
        cursor = self.c.cursor(cursorclass)
        yield cursor
        cursor.close()

    def insert(self, table, kvs, ignore=False):
        columns, values = zip(*kvs.items())

        sql = 'INSERT {modifier}INTO {table} ({columns}) VALUES ({values})'.format(
            modifier='IGNORE ' if ignore else '',
            table=table,
            columns=formatColumns(columns),
            values=formatSlots(len(columns)),
        )

        self._log(sql)
        with self.cursor() as c:
            c.execute(sql, values)
            return c.lastrowid

    def insertIgnore(self, table, kvs):
        return self.insert(table, kvs, True)

    def insertMany(self, table, rows, ignore=False):
        pass

    def delete(self, table, idOrWhere):
        sql = 'DELETE FROM {table} {where}'.format(
            table=table,
            where=formatWhere(idOrWhere),
        )

        self._log(sql)
        with self.cursor() as c:
            return c.execute(sql)

    def update(self, table, idOrWhere, kvs):
        sql = 'UPDATE {table} SET {kvs} {where}'.format(
            table=table,
            kvs=formatSetKV(kvs),
            where=formatWhere(idOrWhere),
        )

        self._log(sql)
        with self.cursor() as c:
            return c.execute(sql)

    def upsert(self, table, defaults, kvs):
        """
        """
        merged = dict(defaults)
        merged.update(kvs)

        mergedKeys, mergedValues = zip(*merged.items())

        sql = 'INSERT INTO {table} ({columns}) VALUES ({values}) ON DUPLICATE KEY UPDATE {updates}'.format(
            table=table,
            columns=formatColumns(mergedKeys),
            values=formatValues(mergedValues),
            updates=formatSetKV(defaults),
        )

        self._log(sql)
        with self.cursor() as c:
            c.execute(sql)
            return c.lastrowid

    def replace(self, table, kvs):
        keys, values = zip(*kvs.items())

        sql = 'REPLACE INTO {table} ({columns}) VALUES ({values})'.format(
            table=table,
            columns=formatColumns(keys),
            values=formatValues(values),
        )

        self._log(sql)
        with self.cursor() as c:
            c.execute(sql)
            return c.lastrowid

    def _select(self, table, columns, idOrWhere, limit=2000, chunkSize=2000, dictCursor=True):
        sql = 'SELECT {columns} FROM {table} {where}'.format(
            columns=formatColumns(columns),
            table=table,
            where=formatWhere(idOrWhere),
        )

        sql += ' LIMIT {}'.format(limit)

        self._log(sql)
        with self.cursor(dictCursor) as c:
            c.execute(sql)
            return c.fetchall()

    def selectOne(self, table, idOrWhere, columns=None, dictCursor=True):
        rows = self._select(table=table, columns=columns, idOrWhere=idOrWhere, dictCursor=dictCursor)
        if rows:
            return rows[0]
        else:
            return None

    def selectMany(self, table, where, columns=None, limit=2000, chunkSize=2000, dictCursor=True):
        return self._select(table=table, idOrWhere=where, columns=columns, limit=limit, chunkSize=chunkSize, dictCursor=dict)

    def selectRaw(self, sql, dictCursor=True):
        pass
