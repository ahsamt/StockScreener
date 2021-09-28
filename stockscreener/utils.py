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


def get_SP_500_dict():
    """gets the latest S&P 500 list from Wikipedia 
    and returns it as a dictionary in a format {"ticker":"company name"}
    """
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    dictSP500 = pd.Series(df.Security.values,index=df.Symbol).to_dict()
    return dictSP500

def moving_average(series, window_size):
    """(pd Series, integer) -> pd series 
    Calculates moving average for the given window size (in days).  
    """ 
    windows = series.rolling(window_size)
    movingAvgs = windows.mean()
    return movingAvgs

def prep_graph_data(stock, numMonths = 12):
    """(string) => (pd DataFrame, pd DataFrame)
    Takes in the stock ticker, returns two Pandas DataFrames for the period of time specified:
    1st df - stock prices with 20 days and 50 days moving averages;
    2nd df - normalised stock and S&P 500 prices. 
    """
    ticker = [stock, "^GSPC"]
    endDate = date.today()              
    startDate = endDate + relativedelta(months = -numMonths)
    startDateInternal = startDate + relativedelta(months= -3) 
    startDateDatetime = datetime.combine(startDate, datetime.min.time()) 
    stocks = yf.download(ticker, start = startDateInternal, end = endDate)
    stocks.to_csv("stocks.csv")
    stocks = pd.read_csv("stocks.csv", header = [0, 1], index_col = [0], parse_dates = [0])
    stocks.columns = stocks.columns.to_flat_index()
    stocks.columns = pd.MultiIndex.from_tuples(stocks.columns)
    stocks.swaplevel(axis = 1).sort_index(axis = 1)

    closeData = stocks.loc[:, "Close"].copy()
    closeData["moving_avg_20"] = moving_average(closeData[stock].copy(), 20)
    closeData["moving_avg_50"] = moving_average(closeData[stock].copy(), 50)

    mask = (closeData.index >= startDateDatetime)
    closeDataForGraph = closeData.loc[mask]
    normSPData = closeDataForGraph.div(closeDataForGraph.iloc[0]).mul(100)
    normSPData = normSPData.reset_index()

    closeDataForGraph = closeDataForGraph.reset_index()

    return(closeDataForGraph, normSPData)

def get_change_info(data, stock):
    """(pd DataFrame, string) => (float, tuple)
    Takes in Pandas DataFrame with stock prices and a stock ticker, 
    returns:
    1 - a float for the last closing price 
    2 - a tuple:
        - a string showing the changes in price since previous trading day,
        - a colour name (red or green) to use in HTML template to display the change.
    """
    closingPrice = data[stock].iloc[-1]
    previousPrice = data[stock].iloc[-2]
    priceDif = closingPrice - previousPrice
    percDif = round(priceDif/previousPrice*100, 2) 
    if priceDif > 0:
        sign = "+"
        color = "green"
    else:
        sign = ""
        color = "red"
    change = (f"{sign}${round(priceDif,2)}  ({sign}{percDif}%)", color)
    return (round(closingPrice,2), change)   

def make_graph_1(data, stock, height, width):
    """(pd DataFrame, string, integer, integer) => string
    Takes in Pandas DataFrame with stock prices and moving averages,
    stock ticker, desired height and width of the graph. 
    Returns an HTML string representing the graph. 
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock])) 
    fig.add_trace(go.Scatter(name="20 day moving avg", x=data["Date"], y=data["moving_avg_20"])) 
    fig.add_trace(go.Scatter(name="50 day moving avg", x=data["Date"], y=data["moving_avg_50"])) 
    fig.update_layout(title = f"{stock} prices over the past year", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
        xaxis = {
            "rangeselector": {
                "buttons": buttons
            }}, width = width, height=height 
        )     
    graph = fig.to_html(full_html=False)
    return graph

def make_graph_2(data, stock, height, width):
    """(pd DataFrame, string, integer, integer) => string
    Takes in Pandas DataFrame with stock and S&P 500 prices,
    stock ticker, desired height and width of the graph. 
    Returns an HTML string representing the graph. 
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=stock, x=data["Date"], y=data[stock]))
    fig.add_trace(go.Scatter(name="S&P 500", x=data["Date"], y=data["^GSPC"]))
    fig.update_layout(title = f"{stock} trading vs S&P 500 trading over the past year (normalised values)", template="seaborn", legend = {"orientation": "h","xanchor":"left"},
                xaxis = {
                    "rangeselector": {
                        "buttons": buttons }}, width=width, height=height) 

    graph = fig.to_html(full_html=False)
    return graph
