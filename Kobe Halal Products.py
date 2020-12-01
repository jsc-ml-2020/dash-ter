from airtable import *
from io import StringIO
import json
import pandas as pd

import re

from io import BytesIO
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import datetime, nltk, string
import matplotlib.pyplot as plt

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
TABLE_NAME = 'Produk Kobe Halal Shop'
API_KEY = 'keypQCc8fO4bXQql3'

airtable_produk_kobe = Airtable(BASE_KEY, TABLE_NAME, API_KEY)
data_produk = airtable_produk_kobe.get_all()

json_data = json.dumps(data_produk)
df = pd.read_json(StringIO(json_data))

df = df["fields"]
df

df = pd.json_normalize(df, meta_prefix=False)
df.sample(5)

new_df = df.copy()

new_df['new_title'] = new_df['title'].apply(lambda x: re.split(r'/', x.lower())[0])
new_df['new_title'] = new_df['new_title'].apply(lambda x: re.sub(r'\d+\s?.', '', x))
new_df.sample(5)

duplicateRows = new_df[new_df['new_title'].duplicated()]

new_df.drop_duplicates(subset=['new_title'], keep=False, inplace=True)

df['Categories'] = df['product_taxonomy'].apply(lambda x: re.split(r'[>/]', x)[1])
categories = df['Categories'].value_counts()
other = categories[categories <= 10]
others = other.index[0:].append(pd.Index(['2019年10月1日(火)より10%税率の商品cosmetics and Other']))

df['Categories'] = df['Categories'].replace(others, 'Other')

total_category = pd.DataFrame({'Total' : df.groupby(['Categories'])['title'].count()}).reset_index()
total_category = total_category.sort_values('Total').reset_index(drop=True)

colors = ['Gray',] * total_category.shape[0]
colors[len(colors)-1] = '#EC5354'

# def wordcloud():
#     stopwords = set(STOPWORDS)

#     words_text = WordCloud(background_color = 'white', 
#                         max_words = 3000,
#                         stopwords = stopwords)

#     text = " ".join(news for news in new_df['new_title'])

#     fig = plt.figure()
#     fig.set_figwidth(14)
#     fig.set_figheight(18)
#     plt.imshow(words_text, interpolation='bilinear')
#     plt.axis('off')

#     return plt


def bar_chart():

    fig = go.Figure()
    fig.add_trace(go.Bar(
                x=total_category['Total'], 
                y=total_category['Categories'], 
                orientation='h',
                marker_color=colors))

    fig.update_layout(
        font_family='Open Sans',
        titlefont={
            'size': 30,
            'color':'black'},
        plot_bgcolor='white',
        title={
            'text': 'Total Product by Category in Kobe Halal Food'},
        xaxis={
            'title': 'Categories'},
        yaxis={
            'title': 'Total Product'})

    return fig

def splitplot():
    fig = px.strip(df, 
                x='Categories', 
                y='main_price',
                hover_name='title',
                color_discrete_sequence=['Gray'],
                template='simple_white')


    fig.update_layout(
        font_family="Open Sans",
        titlefont={
            'size': 30,
            'color':'black'},
        title={
            'text': 'Striplot of Price by Countries',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig


def boxplot():

    fig = go.Figure()

    categories = df['Categories'].unique()
    colors = ['Gray',] * len(categories)
    colors[1] = '#EC5354'

    for xd, cls in zip(categories, colors):
        fig.add_trace(go.Box(
            y=df['main_price'][df['Categories']==xd],
            name=xd,
            hovertext=df['title'][df['Categories']==xd],
            marker_color=cls))

    fig.update_layout(
        showlegend=False,
        font_family="Open Sans",
        titlefont={
            'size': 30,
            'color':'black'},
        plot_bgcolor='white',
        title={
            'text': 'Boxplot of Price by Category',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig

def pie_chart():

    data = df['is_soldout'].value_counts().rename_axis('Categories').reset_index(name='Total')
    labels = data['Categories']
    values = data['Total']

    fig = go.Figure(data=[go.Pie(
                        labels=labels, 
                        values=values,
                        marker_colors= ['Gray', '#FF1616'],
                        pull=[0, 0, 0.2, 0])])

    fig.update_layout(
        font_family="Open Sans",
        titlefont={
            'size': 20,
            'color':'black'},
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        font=dict(
            size=14,
            color='black'
        ),
        title={
            'text': 'The Percentage of Stuff Availability in Kobe Halal Shop',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    
    return fig


app.layout = html.Div([

    html.H1("Kobe Halal Products", style={'text-align': 'center'}),
    dcc.Graph(figure=pie_chart()),
    # dcc.Graph(figure=wordcloud()),
    dcc.Graph(figure=bar_chart()),
    dcc.Graph(figure=splitplot()),
    dcc.Graph(figure=boxplot()),
  
])


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
