from flask import Flask, render_template, request, url_for, redirect, flash
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
uri = f'http://localhost:3000/api/'

def insert_name(foreign_name, foreign_id):
    _, table = foreign_name.split('_')
    res = requests.get(f'{uri}{table}s/{foreign_id}').json()
    print(res)
    return res['data'][0].get('name')


def data_for_select(table):
    rows = requests.get(f'{uri}{table}').json()['data']
    return map(lambda row: (row['name'], row['id']), rows)

def create_context(res, table):
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
            # f'{uri}{table}/{row["id"]}'
            row['id']
        ]
        for row in res
    ]
    return {'fields': fields, 'rows': rows, 'table': table}


@app.route('/<table>', methods=['GET', 'POST'])
def home(table):
    context = {}
    if request.method == 'POST':
        success = requests.post(f'{uri}{table}', data=request.form).json().get('success')
        if success:
            flash('succesfully created!')
            return redirect(url_for('home', table=table))
        else:
            flash('Something went wrong!')
            return redirect(url_for(f'new_{table[:-1]}'))

    res = requests.get(f'{uri}{table}').json()['data']
    if res:
        context = create_context(res, table)

    return render_template('index.html', **context)


@app.route('/<table>/new')
def new(table):
    context = {'name': table}
    if table == 'purchases':
        context.update({
            'providers':data_for_select('providers'),
            'collectors':data_for_select('collectors')
            })

    return render_template(f'new_{table[:-1]}.html', **context)

@app.route('/card/<table>/<Id>' methods=['GET', 'PUT'])
def card(table, Id):
    if requests.method == 'PUT':
        success = requests.put(f'{uri}{table}/{Id}', data=request.form).json().get('success')

    if table == 'providers':
        img_uri = 'img/revolt-QJfew6cDpR4-unsplash.jpg'
    elif table == 'collectors':
        img_uri = 'img/christina-branco-G_xYDS6UuXo-unsplash.jpg'
    else:
        img_uri = 'img/duncan-meyer-Xc6boi5lsfI-unsplash.jpg',

    res = requests.get(f'{uri}{table}/{Id}').json()['data']
    if res:
        context = create_context(res, table)
        rows, Id = context['rows'][0]
        fields_rows = zip(context['fields'],rows)
    else:
        flash('No data Found!')
    return render_template('card.html', img_uri=img_uri, table=context['table'], fields_rows=fields_rows)


if __name__ == '__main__':
    app.run(debug=True)