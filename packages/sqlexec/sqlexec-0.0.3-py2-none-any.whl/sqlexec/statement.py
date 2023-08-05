#coding=utf8

class e(str):
    pass


def escape(value):
    if isinstance(value, long):
        return repr(value)[:-1]
    elif isinstance(value, e):
        return value
    elif isinstance(value, unicode):
        return repr(value.encode('utf8'))

    return repr(value)


def formatValues(values):
    return ', '.join(escape(v) for v in values)


def formatSlots(n):
    return ', '.join(['%s'] * n)


def formatColumns(values):
    if not values:
        return '*'
    elif isinstance(values, basestring):
        return values
    else:
        return ','.join('`{}`'.format(v) for v in values)

def formatSetKV(kv):
    segments = []
    for k, v in kv.items():
        segments.append('{}={}'.format(k, escape(v)))

    return ', '.join(segments)


def formatWhereKV(kv):
    segments = []
    for k, v in kv.items():
        if isinstance(v, list):
            segments.append('{} in ({})'.format(k, formatValues(v)))
        else:
            segments.append('{}={}'.format(k, escape(v)))

    return ' and '.join(segments)


def formatWhere(idOrWhere):
    if not idOrWhere:
        return ''
    if isinstance(idOrWhere, (int, long)):
        return 'WHERE ' + str(idOrWhere)
    elif isinstance(idOrWhere, basestring):
        return 'WHERE ' + idOrWhere
    elif isinstance(idOrWhere, list):
        return 'WHERE ' + 'id in ({})'.format(formatValues(idOrWhere))
    elif isinstance(idOrWhere, dict):
        return 'WHERE ' + formatWhereKV(idOrWhere)
    else:
        return None


def formatOrderBy(orderBy):
    if not orderBy:
        return ''
    else:
        return 'ORDER BY ' + orderBy
