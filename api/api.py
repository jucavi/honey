from ast import Delete
from ssl import CHANNEL_BINDING_TYPES
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


@app.route('/api/<table>', methods=['GET', 'POST'])
def tables(table):
    if request.method == 'POST':
        form = request.get_json() or request.form
        changes = new(get_db(), table, **form)

        if table == 'purchases':
            args = {'qty': float(form['quantity']), 'id': form['id_collector']}
            query = f'UPDATE collectors SET quantity = quantity + :qty WHERE id=:id'
            changes += save_execute(get_db(), query, args)

        return {'success': changes > 0}

    data = get_all(get_db(), table, **request.args)
    return Response(to_json(data), content_type='application/json')


@app.route('/api/<table>/<Id>', methods=['GET', 'PUT', 'DELETE'])
def get(table, Id):
    changes = 0
    if request.method == 'PUT':
        form = request.get_json() or request.form
        print('------>', form.get('id_collector'))
        # changes = update_by_id(get_db(), table, Id, **form)
        if table == 'purchases':
            qty = save_execute(
                get_db(),
                'SELECT (quantity) FROM collectors WHERE id=:id', {'id': form.get('id_collector')},
                cursor=True
            ).fetchone()
            print(qty)
            # args = {'qty': float(form['quantity']), 'id': form['id_collector']}
            # query = f'UPDATE collectors SET quantity = quantity + :qty WHERE id=:id'
            # changes += save_execute(get_db(), query, args)
        return {'success': changes > 0}

    if request.method == 'DELETE':
        changes = None
        if table != 'purchases':
            changes = delete_by_id(get_db(), table, Id)
        return {'success': changes > 0}

    query = f'SELECT * FROM {table} WHERE id={Id!r}'
    data = save_execute(get_db(), query, cursor=True)
    return Response(to_json(data), content_type='application/json')



if __name__ == '__main__':
    app.run(debug=True, port=3000)
