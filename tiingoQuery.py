# File:         tiingoQuery.py
# Author:       James Bush
# Updted:       April 2, 2021
# Description:  Quick implementation of query to the Tiingo API for price data
#               of a listed security.
#               Print line chart to screen if selected by user.
#               Make sure to store Tiingo api_key in a file api_key.txt in same
#               directory as this file.

from tiingo import TiingoClient
import pandas as pd
import plotly.express as px


#Config client dict to access Tiingo API
config = {}
config['session'] = True
with open('api_key.txt','r') as infile:
    config['api_key'] = infile.read()[:-1]
    client = TiingoClient(config)

def ticker_metadata(ticker):
    """
    Take ticker symbol; obtain ticker_metadata from Tiingo API.
    """
    ticker_metadata = client.get_ticker_metadata(ticker)
    return ticker_metadata

def get_data(ticker,startDate,endDate,frequency):
    """
    Submit request to Tiingo API for ticker data; return Pandas dataframe.
    """
    ticker_price = client.get_dataframe(    ticker,
                                            startDate=startDate,
                                            endDate=endDate,
                                            frequency=frequency
                                        )
    return ticker_price

def input_query():
    """
    Take user input and return values for ticker, startDate, endDate, and
    frequency.
    """
    ticker = input('Enter ticker symbol: ')
    startDate = input('Enter start date for data in YYYY-MM-DD format: ')
    endDate = input('Enter end date for data in YYYY-MM-DD format: ')
    frequency = input('Enter frequency of data (e.g., "daily"): ')

    return(ticker,startDate,endDate,frequency)

#live query based on user input
input_vals = input_query()
ticker_price = get_data(    input_vals[0],
                            input_vals[1],
                            input_vals[2],
                            input_vals[3]
                        )

#once obtained data, print data head to confirm
print(input_vals[0],"\n",ticker_price.head(10))

#create line plot of security price
def plotly_line_plot(df, ticker):
    """
    Take Pandas dataframe and ticker symbol. Invoke Plotly to create line plot,
    and to show plot in HTML.
    """
    fig = px.line(  df,
                    x=df.index,
                    y='close',
                    title=ticker
                )
    #update layout here
    fig.show()

#prompt whether user wants to see a chart
chart = ""
while chart == "":
    chart = input("Show chart? [y/n]\n")
    if chart.lower() == 'y':
        plotly_line_plot(ticker_price, input_vals[0])
    elif chart.lower() == 'n':
        pass
    else:
        chart = ""
        print("Please enter 'y' or 'n'.")
