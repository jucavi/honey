from flask import Flask, url_for, request, g, render_template
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


def get_name(func):
    return func.__name__.replace('_', ' ').title()


def data_for_select(table):
    rows = get_all(get_db(), table, sort='name')
    return map(lambda row: (row['name'], row['id']), rows)


@app.route('/')
def home():
    return render_template('index.html', name=home.__name__.title())


@app.route('/api')
def api_home():
    return 'Make life easier!'


@app.route('/api/collectors', methods=['GET', 'POST'])
def collectors():
    if request.method == 'POST':
        form = request.get_json()
        new(get_db(), 'collectors', **form)
    data = get_all(get_db(), 'collectors', **request.args)
    return to_json(data)


@app.route('/api/providers', methods=['GET', 'POST'])
def providers():
    if request.method == 'POST':
        form = request.get_json()
        new(get_db(), 'providers', **form)

    data = get_all(get_db(), 'providers', **request.args)
    return to_json(data)


@app.route('/api/purchases', methods=['GET', 'POST'])
def purchases():
    if request.method == 'POST':
        query = f'UPDATE collectors SET quantity = quantity + :qty WHERE id=:id'
        form = request.get_json()
        args = {'qty': float(form['quantity']), 'id': form['id_collector']}
        new(get_db(), 'purchases', **form)
        save_execute(get_db(), query, args)
        print(form)
    data = get_all(get_db(), 'purchases', **request.args)
    return to_json(data)


@app.route('/collectors/new')
def new_collector():
    name = get_name(new_collector)
    return render_template('new_collector.html', name=name)


@app.route('/providers/new')
def new_provider():
    name = get_name(new_provider)
    return render_template('new_provider.html', name=name)


@app.route('/purchases/new')
def new_purchase():
    name = get_name(new_purchase)
    providers = data_for_select('providers')
    collectors = data_for_select('collectors')
    return render_template('new_purchase.html', name=name, providers=providers, collectors=collectors)


if __name__ == '__main__':
    app.run(debug=True)
