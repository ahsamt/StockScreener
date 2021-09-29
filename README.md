# About this project

This application begins to pull together the fundamental components required to build a stock screening tool. Such a tool can be divided into the following functions:

- ability to download daily updates to the universe of applicable stocks and merge with the cache of historical data.
- ability to run analytics on the updated historical data to search for specific criteria of interest.
- ability to display to the user the stocks returned from such queries alongside relevant charts.

The current implementation focuses on the latter function by allowing the user to create a watchlist of instruments. Once an instrument is added to the watchlist, relevant graphs will be displayed alongside a text area to allow the user to keep their own notes.

Analytics included on the graphs:

### Graph 1

The graph includes a **_20 day_** and a **_50 day moving average_**. Such analytics may be typically used by users to provide final decisions on whether to buy or sell a stock. Example of such use would include:

If the 20 day moving average crosses above (below) the 50 day moving average then a signal to buy (sell) may be determined.
If the stock rebounds off the 50 day moving average then this may be considered a signal to buy.

### Graph 2

The graph illustrates the movement of the stock’s price versus the **_S&P 500 index_**. This may prove advantageous as a comparison of a stock versus a relevant index, and may often be utilised in order to determine whether the stock is trading in an abnormal fashion in comparison to its peers. Leaving aside the consideration that this may be due to unfavourable news related to the stock, some users of a stock screener may anticipate the stock moving back in line with the index. Therefore, if the stock had dropped in value, yet the index did not, a user may consider buying the stock (and potentially selling the index).

# How to use StockScreener

### Search page

- Enter the ticker of a S&P 500 stock you are interested in in the search box and click "Get results".
- If you would like to add the stock to your watchlist, click "Add to watchlist".

### Ticker List page

- Click on a letter to see all the tickers starting with this letter that are included in the S&P 500 index.

### Watchlist page

- All the stocks you have added to your watchlist will be shown here.
- Click on a button with the relevant ticker name to go to the relevant section of the watchlist.
- Type your notes on the performance of a specific stock in the "notes" area, then click "Save notes".
- Click the "Remove from watchlist" button to remove stock from your watchlist.

# Distinctiveness and Complexity

### Tools used to create the application:

1. Django

   - 2 models are created - User and SavedSearch;

2. JavaScript

   - Internal API routes are used to asynchronously update the database and fetch data without reloading the page
