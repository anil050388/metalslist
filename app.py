from dash.dependencies import Input, Output
from dash import Dash, html, Input, Output, ctx, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from numerize import numerize
import openpyxl

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}]

# Import style sheet CSS for Basic Dash App
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, meta_tags=metaTags, external_stylesheets=[
           dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])
server = app.server

# Retrieve the Unique Country codes
df = pd.read_excel('curency1.xlsx')
df = df[df['Symbol'] != '']
df = df[df['Currency Code'] != 'XOF']
Country_Codes = df['Country_x'].unique()

# df_table = pd.DataFrame()
# df_table.columns = ['Dates','Gold','Silver','Platinum','Palladium']
# Read Gold Price Sheet
GoldPrice = pd.read_excel('GoldPrice.xlsx')
SilverPrice = pd.read_excel('SilverPrice.xlsx')
PlatinumPrice = pd.read_excel('PlatinumPrice.xlsx')
PalladiumPrice = pd.read_excel('PalladiumPrice.xlsx')


fig = go.Figure()

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.H1("Precious Metal Values - Around the Globe")
    ]),


    # html.Br(),
    dbc.Container([
        dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(
                            id='country_dropdown',
                            multi=False,
                            options=[
                                {"label": x, "value": x}
                                for x in Country_Codes
                            ],
                            value=Country_Codes[0],
                            clearable=False,
                            style={'background': '#01020e', 'margin': '0px',
                                   'font-weight': 'bold'}
                        )
                    ]),
                ], className="seven columns"),

                dbc.Col([
                    html.Div(
                        html.Div(id='Country_Image')
                    ),
                ], className="five columns"),
                ])
    ], className="container_first display_row_center row"),

    html.Div([
        dcc.RadioItems(
            id='radio_items',
            options=[
                {'label': ['Grams', html.Span(
                    style={'font-size': 15, 'padding-left': 30})], 'value': 'Grams'},
                {'label': ['Ounce', html.Span(
                    style={'font-size': 15, 'padding-left': 30})], 'value': 'Ounce'}
            ],
            value='Ounce',
            inline=True, style={'padding': '5px'}
        )
    ], className="radio"),

    dbc.Container([
        dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="/assets/gold.jpg", top=True),
                        html.Div([
                            dbc.CardBody([
                                html.H3(id='Gold_Card'),
                                html.Div(id='percentage_gold')
                            ])
                        ]),
                    ], className="goldcard")
                ]),

                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="/assets/silver.jpg", top=True),
                        html.Div([
                            dbc.CardBody([
                                html.H3(id='Silver_Card'),
                                html.Div(id='percentage_silver')
                            ])
                        ]),
                    ], className="silvercard")
                ]),

                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="/assets/Platinum.jpg", top=True),
                        html.Div([
                            dbc.CardBody([
                                html.H3(id='Platinum_Card'),
                                html.Div(id='percentage_platinum')
                            ])
                        ]),
                    ], className="platinumcard")
                ]),

                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="/assets/Palladium.jpg", top=True),
                        html.Div([
                            dbc.CardBody([
                                html.H3(id='palladium_Card'),
                                html.Div(id='percentage_palladium')
                            ])
                        ]),
                    ], className="Palladiumcard")
                ]),
                ]),
    ], className="card_container1"),

    dbc.Container([
        dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                            html.Div([
                                html.Button(
                                    'Day', id='Day', n_clicks=0, hidden=True),
                                html.Button(
                                    'Week', id='Week', n_clicks=0),
                                html.Button(
                                    'Month', id='Month', n_clicks=0),
                                html.Button(
                                    'Year', id='Year', n_clicks=0),
                                html.Button(
                                    '5 Year', id='Year5', n_clicks=0),
                                html.Button(
                                    '10 Year', id='Year10', n_clicks=0),
                                html.Div(id='container-button-timestamp')
                            ])
                        ),
                    ], className="linechart text-center")
                ], className="twelve columns"),
                ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    # dcc.RadioItems(
                    #     id='radio_items',
                    #     options=[
                    #         {'label': ['Gold', html.Span(
                    #             style={'font-size': 15, 'padding-left': 30})], 'value': 'XAU'},
                    #         {'label': ['Silver',  html.Span(
                    #             style={'font-size': 15, 'padding-left': 30})], 'value': 'XAG'},
                    #         {'label': ['Platinum', html.Span(
                    #             style={'font-size': 15, 'padding-left': 30})], 'value': 'XPT'},
                    #         {'label': ['Palladium', html.Span(
                    #             style={'font-size': 15, 'padding-left': 30})], 'value': 'XPD'}
                    #     ],
                    #     value='XAU',
                    #     inline=True, style={'padding': '5px'}
                    # )
                ], className="card_container3")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="line_chart", config={'displayModeBar': 'hover',
                                                   'displaylogo': False,
                                                   'scrollZoom': False},
                          style={'background': 'black', 'padding-bottom': '0px', 'padding-left': '0px', 'height': '80vh'})
            ], className="linechart1 text-center")
        ]),

        dbc.Row([
            dbc.Col([
                my_table := dash_table.DataTable(
                    # columns=[
                    #     {'name': 'Dates', 'id': 'Dates', 'type': 'text'},
                    #     {'name': 'Gold', 'id': 'Gold', 'type': 'text'},
                    #     {'name': 'Silver', 'id': 'Silver', 'type': 'text'},
                    #     {'name': 'Platinum', 'id': 'Platinum', 'type': 'text'},
                    #     {'name': 'Palladium', 'id': 'Palladium', 'type': 'text'},
                    # ],
                    style_cell={'textAlign': 'left',
                                'font-family': 'sans-serif'
                                },
                    page_size=10,
                ),

                dbc.Label("Show number of rows", id="rowstable"),
                row_drop := dcc.Dropdown(value=10, clearable=False, style={'width': '35%'}, options=[10, 25, 50, 100]),

            ], className="mytable text-center")
        ])

    ], className="card_container4"),

    html.Div([
        dbc.Spinner(html.Div(id='data_update_time'))
    ], className="timer"),
])

# Curr_Symbol


@app.callback(Output('Silver_Card', 'children'),
              [Input('country_dropdown', 'value'),
               Input('radio_items', 'value')])
def updatecard(country_dropdown, radio_items):
    if country_dropdown:
        symbol = df[df['Country_x'] == country_dropdown]['Symbol'].unique()
        symbol = symbol[0]
        currencyCode = df[df['Country_x'] ==
                          country_dropdown]['Currency Code'].unique()
        currencyCode = currencyCode[0]
        Current = SilverPrice[['IDate', currencyCode]].tail(1)
        CurrentDate = datetime.strptime(
            Current['IDate'].to_string(index=False), '%Y-%m-%d').date()

        if radio_items == 'Ounce':
            Curr_price = float(Current[currencyCode].to_string(index=False))
        elif radio_items == 'Grams':
            Curr_price = float(Current[currencyCode].to_string(
                index=False))/(28.3495231)
        CurrentPrice = numerize.numerize(Curr_price)
        CurrentPrice = str(CurrentPrice)
        symbol = symbol + ' ' + CurrentPrice
        return symbol


@app.callback(Output('Platinum_Card', 'children'),
              [Input('country_dropdown', 'value'),
               Input('radio_items', 'value')])
def updatecard(country_dropdown, radio_items):
    if country_dropdown:
        symbol = df[df['Country_x'] == country_dropdown]['Symbol'].unique()
        symbol = symbol[0]
        currencyCode = df[df['Country_x'] ==
                          country_dropdown]['Currency Code'].unique()
        currencyCode = currencyCode[0]
        Current = PlatinumPrice[['IDate', currencyCode]].tail(1)
        CurrentDate = datetime.strptime(Current['IDate'].to_string
                                        (index=False), '%Y-%m-%d').date()

        if radio_items == 'Ounce':
            Curr_price = float(Current[currencyCode].to_string(index=False))
        elif radio_items == 'Grams':
            Curr_price = float(Current[currencyCode].to_string(
                index=False))/(28.3495231)

        CurrentPrice = numerize.numerize(Curr_price)
        CurrentPrice = str(CurrentPrice)
        symbol = symbol + ' ' + CurrentPrice
        return symbol


@app.callback(Output('palladium_Card', 'children'),
              [Input('country_dropdown', 'value'),
               Input('radio_items', 'value')])
def updatecard(country_dropdown, radio_items):
    if country_dropdown:
        symbol = df[df['Country_x'] == country_dropdown]['Symbol'].unique()
        symbol = symbol[0]
        currencyCode = df[df['Country_x'] ==
                          country_dropdown]['Currency Code'].unique()
        currencyCode = currencyCode[0]
        Current = PalladiumPrice[['IDate', currencyCode]].tail(1)
        CurrentDate = datetime.strptime(Current['IDate'].to_string
                                        (index=False), '%Y-%m-%d').date()
        if radio_items == 'Ounce':
            Curr_price = float(Current[currencyCode].to_string(index=False))
        elif radio_items == 'Grams':
            Curr_price = float(Current[currencyCode].to_string(
                index=False)) / (28.3495231)

        CurrentPrice = numerize.numerize(Curr_price)
        CurrentPrice = str(CurrentPrice)
        symbol = symbol + ' ' + CurrentPrice
        return symbol


@app.callback(Output('Gold_Card', 'children'),
              [Input('country_dropdown', 'value'),
               Input('radio_items', 'value')])
def updatecard(country_dropdown, radio_items):
    if country_dropdown:
        symbol = df[df['Country_x'] == country_dropdown]['Symbol'].unique()
        symbol = symbol[0]
        currencyCode = df[df['Country_x'] ==
                          country_dropdown]['Currency Code'].unique()
        currencyCode = currencyCode[0]
        Current = GoldPrice[['IDate', currencyCode]].tail(1)
        CurrentDate = datetime.strptime(
            Current['IDate'].to_string(index=False), '%Y-%m-%d').date()

        if radio_items == 'Ounce':
            Curr_price = float(Current[currencyCode].to_string(index=False))
        elif radio_items == 'Grams':
            Curr_price = float(Current[currencyCode].to_string(
                index=False))/(28.3495231)

        CurrentPrice = numerize.numerize(Curr_price)
        CurrentPrice = str(CurrentPrice)
        symbol = symbol + ' ' + CurrentPrice
        return symbol


@app.callback(Output('Country_Image', 'children'),
              [Input('country_dropdown', 'value')])
def update_value(country_dropdown):
    if country_dropdown:
        flags = df[df['Country_x'] ==
                   country_dropdown]['URL_FLAG'].unique()
        flag = flags[0]
        return html.Img(src=app.get_asset_url(flag),
                        style={'width': '150px',
                               'height': '32px',
                               'text-align': 'left',
                               'flex-wrap': 'wrap',
                               'flex-direction': 'column'})


@app.callback(Output('data_update_time', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    dates = GoldPrice.tail(1)['IDate'].to_string(index=False)
    # current_date = datetime.today()
    # current_date = datetime.strftime(current_date, '%Y-%m-%d %H:%M:%S')
    current_date = dates
    return [
        html.Div([
            html.Div('Last data update date:', style={
                     'text-align': 'right'}),
            html.Div(current_date, className='location_name')
        ], className='date_time_row')
    ]


@app.callback(
    [Output('container-button-timestamp', 'children'),
     Output('line_chart', 'figure'),
     Output(my_table, 'data'),
     Output(my_table, 'page_size'),
     Output('percentage_gold', 'children'),
     Output('percentage_silver', 'children'),
     Output('percentage_platinum', 'children'),
     Output('percentage_palladium', 'children')],
    Input('Day', 'n_clicks'),
    Input('Week', 'n_clicks'),
    Input('Month', 'n_clicks'),
    Input('Year', 'n_clicks'),
    Input('Year5', 'n_clicks'),
    Input('Year10', 'n_clicks'),
    Input('country_dropdown', 'value'),
    Input('radio_items', 'value'),
    Input(row_drop, 'value')
)
# radio_items):
def displayClick(btn1, btn2, btn3, btn4, btn5, btn6, country_dropdown,
                 radio_items1, row_drop):
    day = 0
    text = ''
    msg = "None of the buttons have been clicked yet"
    if "Day" == ctx.triggered_id:
        text = 'Day'
        day = 7
        msg = "Button 1 was most recently clicked"
    elif "Week" == ctx.triggered_id:
        text = 'Week'
        per_text = 'Last Week'
        day = 7
        msg = "Button 2 was most recently clicked"
    elif "Month" == ctx.triggered_id:
        text = '1 Month'
        per_text = 'Last Month'
        day = 30
        msg = "Button 3 was most recently clicked"
    elif "Year" == ctx.triggered_id:
        text = '1 Year'
        per_text = 'Last Year'
        day = 365
        msg = "Button 4 was most recently clicked"
    elif "Year5" == ctx.triggered_id:
        text = '5 Years'
        per_text = 'Last 5 Years'
        day = 1825
        msg = "Button 5 was most recently clicked"
    elif "Year10" == ctx.triggered_id:
        text = '10 Years'
        per_text = 'Last 10 Years'
        day = 3650
        msg = "Button 6 was most recently clicked"
    else:
        text = '5 Years'
        per_text = 'Last 5 Years'
        day = 1825
        msg = "Button 5 was most recently clicked"

    if country_dropdown:
        currencyCode = df[df['Country_x'] ==
                          country_dropdown]['Currency Code'].unique()
        currencyCode = currencyCode[0]
        Current = GoldPrice[['IDate', currencyCode]].tail(1)
        CurrentDate = datetime.strptime(
            Current['IDate'].to_string(index=False), '%Y-%m-%d').date()

        week_text = 'Last Week'
        if week_text == 'Last Week':
            PreviousWeek1 = str(CurrentDate - timedelta(days=7))
            GoldPrice_week1 = GoldPrice[GoldPrice['IDate']
                                        >= PreviousWeek1][['IDate', currencyCode]]

            Gold_Tail1 = GoldPrice_week1[['IDate', currencyCode]].tail(1)
            Gold_current1 = float(
                Gold_Tail1[currencyCode].to_string(index=False))
            Gold_Head1 = GoldPrice_week1[['IDate', currencyCode]].head(1)
            Gold_Previous1 = float(
                Gold_Head1[currencyCode].to_string(index=False))
            gold_percentage1 = (
                (Gold_current1-Gold_Previous1)/Gold_Previous1) * 100.0

            if gold_percentage1 > 0:
                gold_percentage1 = "{:.2f}".format(gold_percentage1)
                gold_id = html.H4(gold_percentage1 + "% " + week_text,
                                  className="bi bi-caret-up-fill text-success")
            else:
                gold_percentage1 = "{:.2f}".format(gold_percentage1)
                gold_id = html.H4(gold_percentage1 + "% " + week_text,
                                  className="bi bi-caret-down-fill text-danger")

            SilverPrice_week1 = SilverPrice[SilverPrice['IDate']
                                            >= PreviousWeek1][['IDate',
                                                               currencyCode]]
            Silver_Tail1 = SilverPrice_week1[['IDate', currencyCode]].tail(1)
            Silver_current1 = float(
                Silver_Tail1[currencyCode].to_string(index=False))
            Silver_Head1 = SilverPrice_week1[['IDate', currencyCode]].head(1)
            Silver_Previous1 = float(
                Silver_Head1[currencyCode].to_string(index=False))
            silver_percentage1 = (
                (Silver_current1-Silver_Previous1)/Silver_Previous1) * 100.0

            if silver_percentage1 > 0:
                silver_percentage1 = "{:.2f}".format(silver_percentage1)
                silver_id = html.H4(silver_percentage1 + "% " + week_text,
                                    className="bi bi-caret-up-fill text-success")
            else:
                silver_percentage1 = "{:.2f}".format(silver_percentage1)
                silver_id = html.H4(silver_percentage1 + "% " + week_text,
                                    className="bi bi-caret-down-fill text-danger")

            PlatinumPrice_week1 = PlatinumPrice[PlatinumPrice['IDate']
                                                >= PreviousWeek1][['IDate',
                                                                   currencyCode]]
            Platinum_Tail1 = PlatinumPrice_week1[[
                'IDate', currencyCode]].tail(1)
            Platinum_current1 = float(
                Platinum_Tail1[currencyCode].to_string(index=False))
            Platinum_Head1 = PlatinumPrice_week1[[
                'IDate', currencyCode]].head(1)
            Platinum_Previous1 = float(
                Platinum_Head1[currencyCode].to_string(index=False))
            platinum_percentage1 = (
                (Platinum_current1-Platinum_Previous1)/Platinum_Previous1) * 100.0

            if platinum_percentage1 > 0:
                platinum_percentage1 = "{:.2f}".format(platinum_percentage1)
                platinum_id = html.H4(platinum_percentage1 + "% " + week_text,
                                      className="bi bi-caret-up-fill text-success")
            else:
                platinum_percentage1 = "{:.2f}".format(platinum_percentage1)
                platinum_id = html.H4(platinum_percentage1 + "% " + week_text,
                                      className="bi bi-caret-down-fill text-danger")

            PalladiumPrice_week1 = PalladiumPrice[PalladiumPrice['IDate']
                                                  >= PreviousWeek1][['IDate', currencyCode]]
            Palladium_Tail1 = PalladiumPrice_week1[[
                'IDate', currencyCode]].tail(1)
            Palladium_current = float(
                Palladium_Tail1[currencyCode].to_string(index=False))
            Palladium_Head1 = PalladiumPrice_week1[[
                'IDate', currencyCode]].head(1)
            Palladium_Previous = float(
                Palladium_Head1[currencyCode].to_string(index=False))
            Palladium_percentage1 = (
                (Palladium_current-Palladium_Previous)/Palladium_Previous) * 100.0

            if Palladium_percentage1 > 0:
                Palladium_percentage1 = "{:.2f}".format(Palladium_percentage1)
                Palladium_id = html.H4(Palladium_percentage1 + "% " + week_text,
                                       className="bi bi-caret-up-fill text-success")
            else:
                Palladium_percentage1 = "{:.2f}".format(Palladium_percentage1)
                Palladium_id = html.H4(Palladium_percentage1 + "% " + week_text,
                                       className="bi bi-caret-down-fill text-danger")

        PreviousWeek = str(CurrentDate - timedelta(days=day))
        GoldPrice_week = GoldPrice[GoldPrice['IDate']
                                   >= PreviousWeek][['IDate', currencyCode]]

        SilverPrice_week = SilverPrice[SilverPrice['IDate']
                                       >= PreviousWeek][['IDate', currencyCode]]

        PlatinumPrice_week = PlatinumPrice[PlatinumPrice['IDate']
                                           >= PreviousWeek][['IDate', currencyCode]]

        PalladiumPrice_week = PalladiumPrice[PalladiumPrice['IDate']
                                             >= PreviousWeek][['IDate', currencyCode]]

        fig = go.Figure()
        radio_items = ''
        if radio_items == '':
            if radio_items1 == 'Grams':
                GoldPrice_week[currencyCode] = GoldPrice_week[currencyCode] / \
                    (28.3495231)
                SilverPrice_week[currencyCode] = SilverPrice_week[currencyCode] / \
                    (28.3495231)
                PlatinumPrice_week[currencyCode] = PlatinumPrice_week[currencyCode]/(
                    28.3495231)
                PalladiumPrice_week[currencyCode] = PalladiumPrice_week[currencyCode]/(
                    28.3495231)
            df_table = pd.DataFrame({'Dates': [],
                                    'Gold': [],
                                    'Silver':[],
                                    'Platinum':[],
                                    'Palladium':[]})
            date_list = []
            date_list = GoldPrice_week[["IDate"]].to_string(index=False)
            date_list = list(date_list.split("\n"))

            goldlist = GoldPrice_week[[currencyCode]].to_string(index=False)
            goldlist = list(goldlist.split("\n"))

            silverlist = SilverPrice_week[[currencyCode]].to_string(index=False)
            silverlist = list(silverlist.split("\n"))

            platinumlist = PlatinumPrice_week[[currencyCode]].to_string(index=False)
            platinumlist = list(platinumlist.split("\n"))

            palladiumlist = PalladiumPrice_week[[currencyCode]].to_string(index=False)
            palladiumlist = list(palladiumlist.split("\n"))
            df2 = pd.DataFrame(list(zip(date_list[1:],goldlist[1:],silverlist[1:],platinumlist[1:],palladiumlist[1:])))
            print(df2)
            print(type(date_list))
            # df_table['Dates'] = date_list
            # df_table['Gold'] = [GoldPrice_week[currencyCode]]
            # df_table['Silver'] = [SilverPrice_week[currencyCode]]
            # df_table['Platinum'] = [PlatinumPrice_week[currencyCode]]
            # df_table['Palladium'] = [PalladiumPrice_week[currencyCode]]
            df_table = df2
            df_table.columns = ['Dates','Gold','Silver','Platinum','Palladium']
            df_table['Country'] = country_dropdown
            df_table =  df_table.sort_values(by=['Dates'],ascending=False)

            fig.add_trace(go.Scatter(x=GoldPrice_week["IDate"],
                                     y=GoldPrice_week[currencyCode],
                                     hovertemplate='<b>Date </b>: %{x}<br>' +
                                     '<i>Price </i>: %{y:.2f}',
                                     mode='lines',
                                     name='<b> Gold </b>',))

            fig.add_trace(go.Scatter(x=SilverPrice_week["IDate"],
                                     y=SilverPrice_week[currencyCode],
                                     hovertemplate='<b>Date </b>: %{x}<br>' +
                                     '<i>Price </i>: %{y:.2f}',
                                     mode='lines',
                                     name='<b> Silver </b>',))

            fig.add_trace(go.Scatter(x=PlatinumPrice_week["IDate"],
                                     y=PlatinumPrice_week[currencyCode],
                                     hovertemplate='<b>Date </b>: %{x}<br>' +
                                     '<i>Price </i>: %{y:.2f}',
                                     mode='lines',
                                     name='<b> Platinum </b>',))

            fig.add_trace(go.Scatter(x=PalladiumPrice_week["IDate"],
                                     y=PalladiumPrice_week[currencyCode],
                                     hovertemplate='<b>Date </b>: %{x}<br>' +
                                     '<i>Price </i>: %{y:.2f}',
                                     mode='lines',
                                     name='<b> Palladium </b>',))

        fig.update_layout(legend_title='<b> Metals </b>',
                          title_text=text + ' History',
                          title_x=0.5,
                          title_font_color='white',
                          plot_bgcolor='rgb(17,17,17)',
                          paper_bgcolor='rgb(17,17,17)',
                          legend=dict(bgcolor='white',
                                        font=dict(family="sans-serif",
                                                  size=14,
                                                  color='chocolate'))
                          )
    msg = ""
    return html.Div(msg), fig, df_table.to_dict('records'), row_drop, gold_id, silver_id, platinum_id, Palladium_id


if __name__ == '__main__':
    app.run(debug=True, port=8050)
