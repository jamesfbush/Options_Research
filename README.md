# SPY_Options_Research
A few tools for scraping and visualizing publicly available options data on the SPY ETF

options_data_scraper.py

Download a copy of options data from Yahoo Finance for listed securities. Prompts user for ticker symbol, number of desired exiprations, and file path for download. Creates .csv with columns for Time Pulled, Contract Name, Call/Put, Expiration, Strike Price, Bid, Ask, Volume, Open Interest, Last Trade, and Implied Volume. 

SPY_options_heatmap.py

Create html heatmap of options data for puts and calls showing strike price (y-axis), expiration (x-axis), and intensity of volume at given strike/expiry.

2020-08-02_SPY_Options_Data_25_expiries.csv

Batch of sample data in .csv for plotting heatmap with SPY_options_heatmap.py
