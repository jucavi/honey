from flask import Flask, render_template, request, url_for, redirect, flash
import requests


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

uri = f'http://localhost:3000/api/'

def insert_name(foreign_name, foreign_id):
    _, table = foreign_name.split('_')
    res = requests.get(f'{uri}{table}s/{foreign_id}').json()
    if res['data']:
        return res['data'][0].get('name')
    else:
        return 'Unknown'


def get_by_id(table, Id):
    res = requests.get(f'{uri}{table}/{Id}').json()['data']
    return res[0] if res else None


def data_for_select(table):
    rows = requests.get(f'{uri}{table}').json()['data']
    return map(lambda row: (row['name'], row['id']), rows)

def create_context(res):
    raw_fields = [key for key in res[0].keys() if key != 'id']
    fields = [
        key.split('_')[1] if key.startswith('id_') else key
        for key in raw_fields
    ]
    rows = [
        [
            [
                insert_name(key, row[key]) if key.startswith(
                    'id_') else row[key]
                for key in raw_fields
            ],
            row['id']
        ]
        for row in res
    ]
    return {'fields': fields, 'rows': rows}


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/<table>', methods=['GET', 'POST'])
def home(table):
    context = {'table': table}
    if request.method == 'POST':
        success = requests.post(f'{uri}{table}', data=request.form).json().get('success')
        if success:
            flash('succesfully created!')
            return redirect(url_for('home', table=table))
        else:
            flash('something went wrong!')
            return redirect(url_for('new', table=table))

    res = requests.get(f'{uri}{table}').json()['data']
    if res:
        context.update(create_context(res))

    return render_template('index.html', **context)


@app.route('/<table>/new', methods=['GET', 'POST'])
def new(table):
    context = {'table': table}
    Id = request.args.get('Id')
    obj = get_by_id(table, Id) or {}

    if table == 'purchases':
        context.update({
            'providers':data_for_select('providers'),
            'collectors':data_for_select('collectors')
        })

    return render_template(f'new.html', **context, obj=obj)


@app.route('/<table>/<Id>', methods=['GET', 'POST'])
def card(table, Id):
    obj = get_by_id(table, Id)
    verb = request.args
    img_uris = {
        'providers': 'img/provider.jpg',
        'collectors': 'img/collector.jpg',
        'purchases': 'img/purchase.jpg'
    }

    if not obj:
        flash('no data Found!')
        return redirect(url_for('home', table=table))

    if request.method == 'POST':
        success = requests.put(f'{uri}{table}/{Id}', data=request.form).json().get('success')
        obj = get_by_id(table, Id)
        if success:
            flash('successfully updated!')
        else:
            flash('upps!')

    if verb.get('delete'):
        success = requests.delete(f'{uri}{table}/{Id}').json().get('success')
        if success:
            flash('successfully deleted!')
        else:
            flash('upps!')
        return redirect(url_for('home', table=table))

    if verb.get('update'):
        return redirect(url_for('new', table=table, Id=Id))

    context = create_context((obj, ))
    rows, _ = context['rows'][0]
    fields_rows = zip(context['fields'], rows)

    return render_template('card.html', img_uri=img_uris.get(table), table=table, fields_rows=fields_rows, Id=Id)


if __name__ == '__main__':
    app.run(debug=True)