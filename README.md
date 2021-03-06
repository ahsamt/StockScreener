# StockScreener

## About this project

This application begins to pull together the fundamental components required to build a stock screening tool. Such a tool can be divided into the following functions:

- ability to download daily updates to the universe of applicable stocks and merge with the cache of historical data.
- ability to run analytics on the updated historical data to search for specific criteria of interest.
- ability to display to the user the stocks returned from such queries alongside relevant charts.

The current implementation focuses on the latter function by allowing the user to create a watchlist of stocks. Once a stock is added to the watchlist, relevant graphs will be displayed alongside a text area to allow the user to keep their own notes.

Analytics included on the graphs are as follows:

### Graph 1

The first graph includes a **20 day** and a **50 day moving average**. Such analytics may be typically utilised by users to provide final decisions on whether to buy or sell a stock. Examples of such use would include:

If the 20 day moving average crosses above (below) the 50 day moving average then a signal to buy (sell) may be determined.
If the stock rebounds off the 50 day moving average then this may be considered a signal to buy.

### Graph 2

The second graph illustrates the movement of the stock’s price versus the **S&P 500 index**. It may prove beneficial to compare a stock to a relevant index, and this may often be utilised in order to determine whether the stock is trading in an abnormal fashion in comparison to its peers. Leaving aside the consideration that this may be due to unfavourable news related to the stock, some users of a stock
screener may anticipate the stock moving back in line with the index. Therefore, if the stock had dropped in value, yet the index had not, a user may consider buying the stock (and potentially selling the index).

## How to use StockScreener

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

## How to run the application

1. Navigate to the project folder

2. Create virtual environment

   `virtualenv .`

3. Activate virtual environment

   - Linux and MacOS:

     `source myvenv/bin/activate`

   - Windows:

     `env\Scripts\activate.bat`

4. Install all the required packages

   `pip install -r requirements.txt`

5. Initialise the database

   `python manage.py makemigrations`

   `python manage.py migrate`

6. Start the development server

   `python manage.py runserver`

## Distinctiveness and Complexity

_This section is included to meet the Final Project requirements for the Harvard University CS50’s Web Programming with Python and JavaScript course_

### Tools used to create the application:

This application is distinct from the other projects I have worked on in the CS50’s Web Programming with Python and JavaScript course as it focuses on exploring the tools required for accessing and analysing financial data. Please note that while the application allows the user to create a watchlist (which can be seen as being similar to the watchlist functionality in the "commerce" project), this is implemented via an internal API route.

1. **Django**

   - 2 models are created - User and SavedSearch;

2. **JavaScript**

   - Internal API routes are used to asynchronously update the database and fetch data.

3. **Yfinance**

   - Yfanance (Python library) is used to access finance data.

4. **Pandas**

   - Pandas (Python library) is used to prepare data for the graphs.

5. **Plotly**

   - Plotly (Python library) Graph Objects are used to display the graphs.

## Stockscreener folder - key files included:

models.py - contains models created for the application

urls.py - URL routes used in the application

utils.py - "helper" functions used in the views.py

views.py - functions taking in Web requests and returning matching responses

_static/stockscreener folder_:

- index.js - JavaScript code used
- styles.css - CSS styling added

_templates/stockscreener folder_:

- about.html - template for the "About" page
- graphs.html - child template displaying the 2 graphs used
- index.html - template for the main "Search" page
- layout.html - base template
- login.html - template for the "Log In" page
- register.html - template for the "Register" page
- search_form.html - child template for the stock search form
- stock_details.html - child template displaying stock information
- ticker_list.html - template for the "Ticker List" page
- watchlist.html - template for the "Watchlist" page
