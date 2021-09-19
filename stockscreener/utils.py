from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

buttons = [{"count": 5, "label": "5D", "step": "day","stepmode": "backward"}, 
{"count": 1, "label": "1M", "step": "month","stepmode": "backward"},
{"count": 3, "label": "3M", "step": "month","stepmode": "backward"},
{"count": 6, "label": "6M", "step": "month","stepmode": "backward"},
{"count": 1, "label": "1Y", "step": "year","stepmode": "backward"},]

def moving_average(series, window_size):
    
    windows = series.rolling(window_size)
    moving_avgs = windows.mean()
    return moving_avgs

def prep_graph_data(stock):
    ticker = [stock, "^GSPC"]
    num_months = 12
    end_date = date.today()
                
    start_date = end_date + relativedelta(months = -num_months)
    start_date_internal = start_date + relativedelta(months= -3) 
    start_date_datetime = datetime.combine(start_date, datetime.min.time()) 
    stocks = yf.download(ticker, start = start_date_internal, end = end_date)
    stocks.to_csv("stocks.csv")
    stocks = pd.read_csv("stocks.csv", header = [0, 1], index_col = [0], parse_dates = [0])
    stocks.columns = stocks.columns.to_flat_index()
    stocks.columns = pd.MultiIndex.from_tuples(stocks.columns)
    stocks.swaplevel(axis = 1).sort_index(axis = 1)
    close = stocks.loc[:, "Close"].copy()

    close["moving_avg_20"] = moving_average(close[stock].copy(), 20)
    close["moving_avg_50"] = moving_average(close[stock].copy(), 50)

    mask = (close.index >= start_date_datetime)
    close_spec = close.loc[mask]
    norm = close_spec.div(close_spec.iloc[0]).mul(100)
    norm = norm.reset_index()
    close_spec = close_spec.reset_index()
    # close_6months["buy_point"] = (close_6months["moving_avg_20"].round() == close_6months["moving_avg_50"].round())
    # close_6months["inc_20"] = close_6months["moving_avg_20"].diff()>0
    # close_6months["inc_50"] = close_6months["moving_avg_50"].diff()>0
    close_spec.to_csv("close.csv")

    return(close_spec, norm)

def get_change_info(data, stock):
    closing_price = data[stock].iloc[-1]
    previous_price = data[stock].iloc[-2]
    price_dif = closing_price - previous_price
    perc_dif = round(price_dif/previous_price*100, 2) 
    if price_dif > 0:
        sign = "+"
    else:
        sign = ""
    change = (f"{sign}${round(price_dif,2)}  ({sign}{perc_dif}%)")
    return (round(closing_price,2), change)   

def make_graph_1(data, stock, height, width):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock])) 
    fig.add_trace(go.Scatter(name="20 day moving avg", x=data["Date"], y=data["moving_avg_20"])) 
    fig.add_trace(go.Scatter(name="50 day moving avg", x=data["Date"], y=data["moving_avg_50"])) 
    fig.update_layout(title = f"{stock} prices over the past year", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
        xaxis = {
            "rangeselector": {
                "buttons": buttons
            }}) 
                
    # fig.add_trace(go.Scatter(
    # x=[pd.to_datetime("2021-07-09")],
    # y=["145.11350021362300"],
    # mode="markers+text",
    # name="Point to Buy",
    # text=["Point to buy"],
    # textposition="bottom center"
    # ))
                
    graph = fig.to_html(full_html=False, default_height=height, default_width=width)
    return graph

def make_graph_2(data, stock, height, width):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock]))
    fig.add_trace(go.Scatter(name="S&P 500", x=data["Date"], y=data["^GSPC"]))
    fig.update_layout(title = f"{stock} trading vs S&P 500 trading over the past year", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
                xaxis = {
                    "rangeselector": {
                        "buttons": buttons }}) 

    graph = fig.to_html(full_html=False, default_height=height, default_width=width)
    return graph
