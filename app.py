# nakonec uložím jako app.py
# 1. Import potřebných knihoven
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input

df = pd.read_csv('Spotify 2010 - 2019 Top 100.csv')

app = dash.Dash(__name__)
server = app.server  # DŮLEŽITÉ PŘIDÁNÍ: Odkaz na Flask server pro hosting

app.layout = html.Div([
    html.H1('Spotify Top 100 – Analýza skladeb', id='graph_title'),

    html.H3('Vyberte rok v žebříčku (top year):', id='slider_title'),

    dcc.Slider(
        id='year_slider',
        min=int(df['top year'].min()),
        max=int(df['top year'].max()),
        step=1,
        value=int(df['top year'].min()),
        marks={str(year): str(year) for year in sorted(df['top year'].unique())}
    ),

    html.Br(),

    dcc.Graph(
        id='my_graph',
        style={'height': '600px'}
    )
])


@app.callback(
    Output('my_graph', 'figure'),
    [Input('year_slider', 'value')]
)
def update_chart(selected_year):
    filtered_df = df[df['top year'] == selected_year]
    top_15 = filtered_df.sort_values(by='pop', ascending=False).head(15)
    chart = px.bar(
        top_15, 
        x='title', 
        y='bpm', 
        color='artist',
        title=f'Top 15 skladeb z roku {selected_year} – Tempo (BPM)',
        labels={'title': 'Název skladby', 'bpm': 'Tempo (BPM)', 'artist': 'Interpret'}
    )
    chart.update_layout(xaxis_tickangle=-45)

    return chart

# DŮLEŽITÉ PŘIDÁNÍ: Spuštění pro webový server (Render si sám řekne o port)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
