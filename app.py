# -*- coding: utf-8 -*-
import base64
import datetime
import io
import csv

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from sympy.solvers import solve
from sympy import Symbol, N, real_roots, plot
from sympy.solvers.inequalities import solve_poly_inequality

import pandas as pd

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

llala = 4

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True
app.layout = html.Div(children=[

    html.H1(children='Lucrative project', style={'margin-top':'30px'}),

    html.H3('''
        Which discount rate should be adopted to make your project lucrative ?
    '''),

    html.H5(children='''
        Please upload your business plan. You can find below an example of the needed csv format.
    ''', style={'margin-top':'30px'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '80%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin-top':'20px',
            'margin-bottom':'30px'
        },
        # Allow multiple files to be uploaded
        multiple=False,
    ),

        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Business Plan', value='tab-1-example'),
        dcc.Tab(label='Discount rate to make it profitable', value='tab-2-example'),
    ]),

    html.Div(id='tabs-content-example')


],
className="container"
)

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1-example':
        return  html.Div(id='output-data-upload')
    elif tab == 'tab-2-example':
        return dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [llala, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def parse_contents2(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])


def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        df = pd.read_csv('VAN_input.csv')
        return html.Div([
            html.H5('Business plan example'),
            html.H6(datetime.datetime.now()),

            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr()
    ])

def solving_rate(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df = [parse_contents2(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        print(df)
        print(type(df))


#with open('VAN_input.csv') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#    i = -1
#    x = Symbol('x', real="True")
#    expr = 0
#    annees= []
#    for row in csv_reader:
#        if i > -1:
#            print(row)
#            expr1 = (int(row[2]) - int(row[1])) * (1 + x)**(11-i)
#            expr = expr + expr1
#            print(expr)
#        i += 1

#result = solve(expr, x)

#print([solution.n(2) for solution in result])

#expr2 = expr / (1+x)**11
#plot(expr2, (x, 0, 1), ylabel='Discount rate')



if __name__ == '__main__':
    app.run_server(debug=True)