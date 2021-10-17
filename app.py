import plotly.graph_objs as go
from plotly.offline import plot
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# download vader
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# define the main function
def get_sentiment_score(text):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    score = sentiment_analyzer.polarity_scores(text)['compound']
    verdict = 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'
    return verdict, score


# create dash structure
app = dash.Dash(
    name='Sentiment Analysis',
    #external_stylesheets=[dbc.themes.BOOTSTRAP],
    #external_stylesheets=['./assets/bootstrap_adjusted.css'],
)
app.title = 'Sentiment Analysis'

content = (
    html.Div([
        html.H4('Text sentiment analyzer', style={'padding-left':'10px'}),
        html.Div([
            html.P(
                'Provide below a phrase or sentence(s) to generate sentiment score.',
                style={'padding-left':'10px'}
            ),
            dcc.Input(
                id='input_text',
                type='text',
                placeholder='Input text',
                value='',
                style={'width':'30%'},
                #debounce=True # press Enter to send the input
            )
        ]),     
        html.Div([
            dcc.Loading(
                id='output_div', type='default',
                children=[
                    html.Div(dcc.Graph(id="output_gauge")),
                    #html.H4(id='output_verdict')
                    
                ]
            )
        ]),
        html.Br()
    ])
)

footer = html.Div(
    [
        html.Small("Designed by "),
        html.Small(html.A("Svilen Stefanov", href="https://www.linkedin.com/in/svilen-stefanov/", target="_blank")),
        html.Br(),
        html.Small(html.A("Source code", href="https://github.com/svilens/sentiment_analysis/", target="_blank")),
    ], style={'font-style':'italic', 'padding-left':'10px', 'textAlign':'left'}
)

app.layout = html.Div([
    html.H1(children='Sentiment Analysis', style={'padding-left':'5px'}),
    html.Br(),
    content,
    footer
])


# callbacks
@app.callback(
        dash.dependencies.Output('output_gauge', 'figure'),
    [
        dash.dependencies.Input('input_text', 'value')
    ])
def create_gauge(text):
    sentiment_verdict, sentiment_score = get_sentiment_score(text)

    fig_gauges = go.Figure()
    fig_gauges.add_trace(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        title = {'text': sentiment_verdict, 'font': {'size': 20, 'color':'white'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "grey", 'thickness':0.25},
            'steps': [
                 {'range': [-1, -0.05], 'color': "red"},
                 {'range': [-0.05, 0.05], 'color': "gold"},
                 {'range': [0.05, 1], 'color': "green"},
            ],
        }
    ))
    
    fig_gauges.update_layout(
        height = 200, width = 300,
        margin={"r":0,"t":70,"l":0,"b":20},
        font = {'color': "white"},
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig_gauges


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)