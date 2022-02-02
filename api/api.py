from ast import Delete
from ssl import CHANNEL_BINDING_TYPES
from tokenize import cookie_re
from flask import Flask, url_for, request, g, render_template, Response
import sqlite3
from helpers import *
import os

cwd = os.path.dirname(__file__)
DB = 'honey.db'
DBpath = os.path.join(cwd, DB)
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DBpath)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def data_for_select(table):
    rows = get_all(get_db(), table, sort='name')
    return map(lambda row: (row['name'], row['id']), rows)

def modify_collector(conn, form):
    args = {'qty': float(form['quantity']), 'id': form['id_collector']}
    query = f'UPDATE collectors SET quantity = quantity + :qty WHERE id=:id'
    return save_execute(conn, query, args)


@app.route('/api/<table>', methods=['GET', 'POST'])
def tables(table):
    conn = get_db()
    changes = 0
    if request.method == 'POST':
        form = request.get_json() or request.form
        changes = new(conn, table, **form)

        if table == 'purchases':
            changes += modify_collector(conn, form)
        return {'success': changes > 0}

    data = get_all(conn, table, **request.args)
    return Response(to_json(data), content_type='application/json')


@app.route('/api/<table>/<Id>', methods=['GET', 'PUT', 'DELETE'])
def get(table, Id):
    conn = get_db()
    changes = 0
    if request.method == 'PUT':
        form = request.get_json() or request.form

        if table == 'purchases':
            start_qty = next(save_execute(conn, f'SELECT * FROM {table} WHERE id=:id', {'id': Id}, cursor=True))['quantity']
            coll_qty = float(form['quantity']) - float(start_qty)
            coll_form = dict(form)
            coll_form.update({'quantity': coll_qty})
            changes = modify_collector(conn, coll_form)

        changes += update_by_id(conn, table, Id, **form)

        return {'success': changes > 0}

    if request.method == 'DELETE':
        changes = 0
        if table != 'purchases':
            changes = delete_by_id(conn, table, Id)
        return {'success': changes > 0}

    query = f'SELECT * FROM {table} WHERE id={Id!r}'
    data = save_execute(get_db(), query, cursor=True)
    return Response(to_json(data), content_type='application/json')



if __name__ == '__main__':
    app.run(debug=True, port=3000)
