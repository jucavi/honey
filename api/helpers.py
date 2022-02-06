import json

def to_json(items, one=False):
    if one:
        return json.dumps(dict(items), sort_keys=False, indent=4)
    return json.dumps({'data': [dict(item) for item in items]}, sort_keys=False, indent=4)


def get_all(conn, table, **params):
    sort = params.get('sort', 'NULL')
    order = params.get('order', 'ASC')
    if order.upper() not in ['ASC', 'DESC']:
        order = 'ASC'

    query = f'SELECT * FROM {table} ORDER BY {sort} {order};'
    cur = save_execute(conn, query, cursor=True)
    if cur:
        return cur.fetchall()
    return []


def get_by_id(conn, table, Id, fields=('*',)):
    cur = conn.cursor()
    fields = ','.join(fields)
    cur.execute(f'SELECT {fields} FROM {table} WHERE id=:id;', {'id': Id})
    return cur.fetchone()


def get_by(conn, table, field, value, fields=('*',)):
    cur = conn.cursor()
    fields = ','.join(fields)
    cur.execute(f'SELECT {fields} FROM {table} WHERE {field}=:value;', {
                'value': value})
    return cur.fetchone()


def save_execute(conn, query, args={}, cursor=False):
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        conn.commit()
    except Exception as e:
        print(f'Error! {e}')
    else:
        if cursor:
            return cur
        return cur.rowcount


def delete_by_id(conn, table, Id):
    return delete_by(conn, table, 'id', Id)


def delete_by(conn, table, field, value):
    query = f'DELETE FROM {table} WHERE {field}=:value;'
    return save_execute(conn, query, {'value': value})


def update_by_id(conn, table, Id, **params):
    return update(conn, table, 'id', Id, **params)


def update(conn, table, field, value, **params):
    set = ','.join(f'{key}={value!r}' for key, value in params.items())
    query = f'UPDATE {table} SET {set} WHERE {field}=:value;'
    return save_execute(conn, query, {'value': value})


def id_gen(conn, table):
    max_id = conn.execute(f'SELECT max(id) FROM {table}')
    try:
        num = int(tuple(next(max_id))[0][3:]) + 1
    except:
        num = 1
    return f'{table[:2].upper()}_{num:04d}'


def make_seq(iter, sep=','):
    return sep.join(iter)


def make_params(conn, table, **params):
    rows = conn.execute(f'PRAGMA table_info({table})')
    args = []
    for row in rows:
        if row[-1]:
            args.append(id_gen(conn, table))
        else:
            args.append(params.get(row[1], 0 if row[2] in ('REAL', 'INTEGER') else None))
    return tuple(args)

def new(conn, table, **params):
    args = make_params(conn, table, **params)
    query = f'INSERT INTO {table} VALUES{args};'
    return save_execute(conn, query)


if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('./honey.db')
    conn.row_factory = sqlite3.Row
    print(id_gen(conn, 'purchases'))
    conn.close()
