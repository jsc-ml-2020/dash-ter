from airtable import *
from io import StringIO
import json
import pandas as pd

import plotly.express as px  
import plotly.graph_objects as go

import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

BASE_KEY = 'appslAQ47ii6IknLk'
TABLE_NAME = 'Produk Baticrom'
API_KEY = 'keypQCc8fO4bXQql3'

airtable_produk_baticrom = Airtable(BASE_KEY, TABLE_NAME, API_KEY)
data_produk = airtable_produk_baticrom.get_all()

json_data = json.dumps(data_produk)
df = pd.read_json(StringIO(json_data))
df = df["fields"]

new_df = pd.json_normalize(df, meta_prefix=False)
new_df.sample(5)    

countries = ['Indonesia', 'Malaysia', 'Thailand', 'Myanmar', 'Australia', 'Japan',  'China', \
             'Canada', 'USA', 'Brazil', 'India', 'Bangladesh', 'Srilanka', 'Pakistan', 'Turkey' ]

categories = ['Pepper|Bumbu|Serbuk|Salt|Garam', 'Beef|Sheep', 'Chicken', 'Fish|Ikan', 'Shrimp', 'Noodles|Mie', 'Rice', 'Vegetable', 'Soto|Curry', 'Tea', 'Milk',
              'Chocolate|Paneer|Cheese', 'Ruti|Paratha|Roti', 'Biscuits|Cookies', 'Manggo|Guava', 'Soji|Soya|Sirup|Soda',
              'Oil', 'Tepung|Powder', 'Chilli|Kecap|Tomato|Sambal']


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Baticrom Products", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_opt",
                 options=[
                     {"label": "Country", "value": "Country"},
                     {"label": "Category", "value": "Category"}],
                 multi=False,
                 value="Country",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={}),

    html.Br(),
    html.Br(),
    html.Div(id='output_container1', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map1', figure={}),

    html.Br(),
    html.Br(),
    html.Div(id='output_container2', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map2', figure={})
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_opt', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The category chosen by user was: {}".format(option_slctd)

    if option_slctd == 'Country':
        total_item_imported = [len(new_df.loc[new_df['description'].str.contains(i, na=False)]) for i in countries]
        data = pd.DataFrame({'Country' : countries,
                            'Total Product': total_item_imported})
    else:
        total_item_category = [len(new_df.loc[new_df['title'].str.contains(i, na=False)]) for i in categories]
        data = pd.DataFrame({'Category' : categories,
                            'Total Product': total_item_category})

    colors = ['Gray',] * data.shape[0]
    colors[0] = '#EC5354'

    fig = go.Figure()
    fig.add_trace(go.Bar(
                x=data[option_slctd], 
                y=data['Total Product'], 
                marker_color=colors))

    fig.update_layout(
        font_family='Open Sans',
        plot_bgcolor='white',
        titlefont={
            'size': 30,
            'color':'black'},
        title={
            'text': '<b>Total Imported Halal Food by {}</b>'.format(option_slctd),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis={
            'title': option_slctd},
        yaxis={
            'title': 'Total Product'})
    
    return container, fig


@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='my_bee_map1', component_property='figure')],
    [Input(component_id='slct_opt', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The category chosen by user was: {}".format(option_slctd)

    new_data = pd.DataFrame()

    if option_slctd == 'Country':
        for i in countries:
            country = new_df.loc[new_df['description'].str.contains(i, na=False)]
            country['Country'] = i
            new_data = pd.concat([new_data, country], ignore_index=True)
    else:
        for i in categories:
            category = new_df.loc[new_df['title'].str.contains(i, na=False)]
            category['Category'] = i
            new_data = pd.concat([new_data, category], ignore_index=True)

    new_data = new_data.astype({'price' : 'float'})

    fig_split = px.strip(new_data, 
               x=option_slctd, 
               y='price',
               title="Striplot of Price by Countries",
               color_discrete_sequence=['Gray'],
               template='simple_white')

    fig_split.update_layout(
        font_family="Open Sans",
        titlefont={
            'size': 30,
            'color':'black'},
        title={
            'text': '<b>Stripplot of Imported Halal Food by {}</b>'.format(option_slctd),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return container, fig_split


@app.callback(
    [Output(component_id='output_container2', component_property='children'),
     Output(component_id='my_bee_map2', component_property='figure')],
    [Input(component_id='slct_opt', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The category chosen by user was: {}".format(option_slctd)


    new_data = pd.DataFrame()
    if option_slctd == 'Country':
        for i in countries:
            country = new_df.loc[new_df['description'].str.contains(i, na=False)]
            country['Country'] = i
            new_data = pd.concat([new_data, country], ignore_index=True)
        colors = ['Gray',] * len(countries)
        colors[0] = '#EC5354'
    else:
        for i in categories:
            category = new_df.loc[new_df['title'].str.contains(i, na=False)]
            category['Category'] = i
            new_data = pd.concat([new_data, category], ignore_index=True)
        colors = ['Gray',] * len(categories)
        colors[0] = '#EC5354'

    new_data = new_data.astype({'price' : 'float'})

    fig_box = go.Figure()

    if option_slctd == 'Country':
        for xd, cls in zip(countries, colors):
            fig_box.add_trace(go.Box(
                y=new_data['price'][new_data[option_slctd]==xd],
                name=xd,
                hovertext=new_data['title'][new_data[option_slctd]==xd],
                marker_color=cls))
    else:
        for xd, cls in zip(categories, colors):
            fig_box.add_trace(go.Box(
                y=new_data['price'][new_data[option_slctd]==xd],
                name=xd,
                hovertext=new_data['title'][new_data[option_slctd]==xd],
                marker_color=cls))

    fig_box.update_layout(
        showlegend=False,
        font_family="Open Sans",
        plot_bgcolor='white',
        titlefont={
            'size': 30,
            'color':'black'},
        title={
            'text': '<b>Boxplot of Imported Halal Food by {}</b>'.format(option_slctd),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return container, fig_box

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
