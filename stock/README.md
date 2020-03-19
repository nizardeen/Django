A Django App to check the Previous stocks for all the available symbols which comes under nseindia.

trade/stock.py --> file contains a Stocks() class which includes of following functions:
   checkTime(date) --> for checking the stock data updating to online time, the normally the files is uploaded on every weekdays on 18:30 P.M,
                   if the stocks checking time is before that then we could consider the previous day as a from_day.
                   
   get_prev_days_stocks(num_of_days) --> this function is a main key role player for this app, this gets the parameter num.of days
                                         and gets the previous num_of_days all the stock listing by returning stocks(pandas dataframes) and the
                                         stock unavailable dates except weekend holidays, this dates are made for the UI for the user

trade/views.py --> Its a django function based api views file 
   index() --> for loading a index.html front-end view
   getStocksData() --> this api gets the unique symbols for the number of given days, this function calls the above Stocks() class
                       This function keeps the track of generated dataframe into a session variable, and it passes the unique symbols list
                       to the front-end user for the drop-down value
   getSymbolData() --> api returns the stock datas list for the particular selected symbols from the drop-down option

trade/urls.py --> file has the function api urls on it

