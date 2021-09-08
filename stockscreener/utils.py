from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

def moving_average(series, window_size):
    
    windows = series.rolling(window_size)
    moving_avgs = windows.mean()
    return moving_avgs

def prep_graph_data(stock):
    ticker = [stock, "^GSPC"]
    num_months = 6
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
    close_6months = close.loc[mask]
    norm = close_6months.div(close_6months.iloc[0]).mul(100)
    norm = norm.reset_index()
    close_6months = close_6months.reset_index()
    # close_6months["buy_point"] = (close_6months["moving_avg_20"].round() == close_6months["moving_avg_50"].round())
    # close_6months["inc_20"] = close_6months["moving_avg_20"].diff()>0
    # close_6months["inc_50"] = close_6months["moving_avg_50"].diff()>0
    close_6months.to_csv("close.csv")

    return(close_6months, norm)

def make_graph_1(data, stock):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock])) 
    fig.add_trace(go.Scatter(name="20 day moving avg", x=data["Date"], y=data["moving_avg_20"])) 
    fig.add_trace(go.Scatter(name="50 day moving avg", x=data["Date"], y=data["moving_avg_50"])) 
    fig.update_layout(title = f"{stock} prices over the past 6 months", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
        xaxis = {
            "rangeselector": {
                "buttons": [
                    {"count": 7, "label": "1W", "step": "day",
                       "stepmode": "backward"},
                    {"count": 14, "label": "2W", "step": "day",
                        "stepmode": "backward"},
                    {"count": 1, "label": "1M", "step": "month",
                        "stepmode": "backward"},
                    {"count": 6, "label": "6M", "step": "month",
                        "stepmode": "backward"}
                ]}}) 
                
    # fig.add_trace(go.Scatter(
    # x=[pd.to_datetime("2021-07-09")],
    # y=["145.11350021362300"],
    # mode="markers+text",
    # name="Point to Buy",
    # text=["Point to buy"],
    # textposition="bottom center"
    # ))
                
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    return graph

def make_graph_2(data, stock):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock]))
    fig.add_trace(go.Scatter(name="S&P 500", x=data["Date"], y=data["^GSPC"]))
    fig.update_layout(title = f"{stock} trading vs S&P 500 trading over the past 6 months", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
                xaxis = {
                    "rangeselector": {
                        "buttons": [
                            {"count": 7, "label": "1W", "step": "day",
                            "stepmode": "backward"},
                            {"count": 14, "label": "2W", "step": "day",
                             "stepmode": "backward"},
                            {"count": 1, "label": "1M", "step": "month",
                            "stepmode": "backward"},
                            {"count": 6, "label": "6M", "step": "month",
                            "stepmode": "backward"}
                        ]}}) 

    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    return graph
