mapbox_access_token = 'pk.eyJ1Ijoia2V2aW56ZXBlZGEiLCJhIjoiY2psaXkyeTBrMDVoYTNrbnhlaDI4Y2kwOCJ9.M8Z5WXXFTo6Wxyrm_ch7AQ'

import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go

df = pd.read_csv("mapa_heat.csv")

app = dash.Dash(__name__)

blackbold={'color':'black', 'font-weight': 'bold'}

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map

    html.Div([
        html.Div([
            # Map-legend
            html.Ul([
                html.Li(html.Span("0-20 Golden"), className='circle', style={'background': '#ff0000','color':'black',
                    'list-style':'none','text-indent': '17px'}),

                html.Li(html.Span("20-40 Golden"), className='circle', style={'background': '#ff7800','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li(html.Span("40-60 Golden"), className='circle', style={'background': '#ffe200','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li(html.Span("60-80 Golden"), className='circle', style={'background': '#c9ff00','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li(html.Span("80-100 Golden"), className='circle',  style={'background': '#83ff00','color':'black',
                    'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 0px','padding-top': '6px','margin-left':'-32px'}
            ),

            # Borough_checklist
            html.Label(children=['Regiones: '], style=blackbold),
            dcc.Checklist(id='boro_name',
                    options=[{'label':str(b),'value':b} for b in sorted(df['region'].unique())],
                    value=[b for b in sorted(df['region'].unique())],
            ),
            # Recycling_type_checklist
            html.Label(children=['Golden configs: '], style=blackbold),
            dcc.Checklist(id='recycling_type',
                    options=[{'label':str(b),'value':b} for b in sorted(df['golden'].unique())],
                    value=[b for b in sorted(df['golden'].unique())],
            ),
            # Web_link
            html.Br(),
            html.Pre(id='web_link', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px',
                 'display': 'none'}
            ),

        ], className='showing'
        ),

        #
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            )
        ], className='twelve columns'
        ),

    ], className='row'
    ),

], className='twelve columns'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('boro_name', 'value'),
               Input('recycling_type', 'value')])

def update_figure(chosen_boro,chosen_recycling):
    df_sub = df[(df['region'].isin(chosen_boro)) &
                (df['golden'].isin(chosen_recycling))]

    #Remplace colors
    df_sub.loc[df_sub['golden'] >= 80, 'color'] = '#04B404' # Verde
    df_sub.loc[(df_sub['golden'] >= 60) & (df_sub['golden'] <= 80), 'color'] = '#5FB404' # Verde amarillento
    df_sub.loc[(df_sub['golden'] >= 40) & (df_sub['golden'] <= 60), 'color'] = '#FFFF00' # Amarillo
    df_sub.loc[(df_sub['golden'] >= 20) & (df_sub['golden'] <= 40), 'color'] = '#FF8000' # Rojo amarillento
    df_sub.loc[df_sub['golden'] <= 20, 'color'] = '#B40404' # Rojo

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['lng'],
                    lat = df_sub['lat'],
                    mode='markers',
                    marker={'color' : df_sub['color'], 'size': df_sub['nodos'] * 10, 'opacity':0.5 },
                    unselected={'marker' : {'opacity':0.5 }},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=df_sub['nodos'],
                    customdata=df_sub['nodos']
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo',
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=20,
            title='',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='light',
                center=dict(
                    lat=19,
                    lon=-99
                ),
                pitch=20,
                zoom=5
            ),
        )
    }
#---------------------------------------------------------------

@app.callback(
    Output('web_link', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:

        the_link=clickData['points'][0]['customdata']
        if the_link is None:
            return 'No Website Available'
        else:
            return None
# #--------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
