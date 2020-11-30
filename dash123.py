import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd

app = dash.Dash()

df = pd.read_csv('D:/deeplearningteam/touristchar.csv') #

sexage = df[df['Survey_item'] == 'Sex/Age']
sexage = sexage.drop([79,87])
sexage = sexage.reset_index(drop=True)

women_bins = -(sexage['2019'][7:])
men_bins = sexage['2019'][:7]

y = ['Under 20', '20-29', '30-39', '40-49', '50-59', '60-69', 'Over 70']

layout = go.Layout(yaxis=go.layout.YAxis(title=''),
                   xaxis=go.layout.XAxis(
                       range=[-250, 250],
                       tickvals=[-200, -150, -50, 0, 50, 150, 200],
                       ticktext=[200, 150, 50, 0, 50, 150, 200],
                       title='Number of People'),
                   barmode='overlay',
                   bargap=0.1)

data = [go.Bar(y=y,
               x=men_bins,
               orientation='h',
               name='Men',
               hoverinfo='x',
               marker=dict(color='#646161')
               ),
        go.Bar(y=y,
               x=women_bins,
               orientation='h',
               name='Women',
               text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               marker=dict(color='#EC5354')
               )]

# pio.write_html(dict(data=data, layout=layout), file='hello_world.html', auto_open=True)

app.layout = html.Div(children=[
    html.H1(children='Survey Result of International Visitors Travelling to Japan'),
    html.Div(children='''Distribution of Gender and Age'''),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label':'2019', 'value':''},
                 {'label':'2018', 'value':''},
                 {'label':'2017', 'value':''},
                 {'label':'2016', 'value':''}],
        value='2019'
    ),
    html.Div(id='dd-output-container')

    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout':layout
        })
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph()

if __name__ == '__main__':
    app.run_server(debug=True)