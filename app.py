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
import plotly.graph_objs as go

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

max_year = 100
interval = 0.1

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
        return html.Div(id='output-graph')

def parse_csv(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
           df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
           return df
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

def parse_contents(contents, filename, date):
    df = parse_csv(contents)
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

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])


def update_output(contents, name, date):
    if contents is not None:
        children = [
            parse_contents(contents, name, date)]
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

@app.callback(Output('output-graph', 'children'),
              [Input('upload-data', 'contents')])

def update_graph(contents):
    if contents is not None:
        df = parse_csv(contents)
    else:
        df = pd.read_csv('VAN_input.csv')
    x = Symbol('x', real="True")
    x_plot = [x*interval for x in range(0, int(1.0/interval))]
    y_plot = [0 for x in range(0, int(1.0/interval))]
    expr = 0
    for index, row in df.iterrows():

        expr1 = (int(row[2]) - int(row[1])) * (1 + x)**(max_year-row[0])
        y_plot1 = [ (int(row[2]) - int(row[1])) * (1 + x)**(max_year-row[0]) for x in x_plot]

        expr = expr + expr1
        y_plot = [a + b for a,b in list(zip(y_plot,y_plot1))]
        print(y_plot)
        
    result = solve(expr, x)
    solutions = set([str((solution.n(2))*100) for solution in result if solution > 0])
    solutions.discard('-100')
    #print(solutions)
    sol = "Your project is balanced for a discount rate of {} %".format(','.join(solutions))

    y_plot = [ y / (1+x)**max_year for y,x in list(zip(y_plot,x_plot))]
    x_plot = [x*100 for x in x_plot]
    expr2 = expr / (1+x)**max_year
    #print(type(expr2))
    #print(expr(1))
    plot(expr2, (x, 0, 1), ylabel='Discount rate')
    return html.H4(children=sol, style={'margin-top':'20px'}), dcc.Graph(
        figure=go.Figure(
            data=go.Scatter(
                    x=x_plot,
                    y=y_plot,
                    )
                )
        , style={'height': 300})




if __name__ == '__main__':
    app.run_server(debug=True)