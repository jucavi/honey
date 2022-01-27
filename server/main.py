from crypt import methods
from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

def insert_name(foreign_name, foreign_id):
    _, table = foreign_name.split('_')
    res = requests.get(f'http://localhost:3000/api/{table}s/{foreign_id}').json()
    print(res)
    return res['data'][0].get('name')


def data_for_select(table):
    rows = requests.get(f'http://localhost:3000/api/{table}').json()['data']
    return map(lambda row: (row['name'], row['id']), rows)


@app.route('/<table>', methods=['GET', 'POST'])
def home(table):
    if request.method == 'POST':
        success = requests.post(f'http://localhost:3000/api/{table}', data=request.form).json().get('success')

    res = requests.get(f'http://localhost:3000/api/{table}').json()['data']
    if res:
        raw_fields = [key for key in res[0].keys() if key != 'id']
        fields = [key.split('_')[1] if key.startswith('id_') else key for key in raw_fields]
        rows = [[insert_name(key, row[key]) if key.startswith('id_') else row[key] for key in raw_fields] for row in res]
    return render_template('index.html', fields=fields, rows=rows, table=table, msg=success)


@app.route('/collectors/new')
def new_collector():
    return render_template('new_collector.html', name='New Collector')


@app.route('/providers/new')
def new_provider():
    return render_template('new_provider.html', name='New Provider')


@app.route('/purchases/new')
def new_purchase():
    return render_template('new_purchase.html',
                           name='New Purchase',
                           providers=data_for_select('providers'),
                           collectors=data_for_select('collectors'))

if __name__ == '__main__':
    app.run(debug=True)