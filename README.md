# Options Research Tools
A few tools for scraping and visualizing publicly available options data. 

## options_data_scraper.py

Download a copy of options data from Yahoo Finance for listed securities. Prompts user for ticker symbol, number of desired exiprations, and file path for download. Creates .csv with columns for Time Pulled, Contract Name, Call/Put, Expiration, Strike Price, Bid, Ask, Volume, Open Interest, Last Trade, and Implied Volume. 

Dependencies: requests, pandas, time, bs4, datetime, tqdm

## options_heatmap.py

Create html heatmap of options data for puts and calls showing strike price (y-axis), expiration (x-axis), and intensity of volume at given strike/expiry.

Dependencies: pandas, plotly.graph_objects

## 2020-08-02_SPY_Options_Data_25_expiries.csv

Batch of sample data in .csv for plotting heatmap with SPY_options_heatmap.py

## tiingoQuery.py

With a Tiingo account set up and a Tiingo API key saved to same directory as the Python file ("api_key.txt"), this program will request the user input a ticker symbol, start date, end date, and frequency (e.g., "daily") and return a Pandas dataframe and Poltly line chart for any listed security. 

Dependencies: pandas, tiingo, plotly.express. 
