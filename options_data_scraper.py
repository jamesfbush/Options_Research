#Date:          February 7, 2021
#Description:   Download a copy of options data from Yahoo Finance for listed securities.
#               Prompts user for ticker symbol, number of desired exiprations,
#               and file path for download.
#               NOTE: Please read/observe Yahoo Finance's robots.txt:
#               https://finance.yahoo.com/robots.txt
#               Do not violate Yahoo's Terms of Service.

################################################################################
#Suggested Additions / Will Add in Future
#Support for failure to pull one or more expirations.
#Error for ticker if not valid.
################################################################################

import requests
import pandas as pd
import time as tm
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from tqdm import tqdm

def setup_info():
    """
    Intro and request input desired ticker and number of expirations;
    set request URL; request main ticker page; parse all forward expiration
    URLs from main page; prompt download in progress.
    """
    ticker = input("Enter ticker symbol: ")
    main_url = "https://finance.yahoo.com/quote/"+ticker+"/options"
    num_exps = int(input("\nEnter the number of expirations to pull (e.g, 15 = 30days, 25 = 6mos; max is 34]: "))
    file_path = input("\nEnter a file path for your download: ")
    soup = bs(requests.get(main_url).content, 'html.parser')
    print("\nPlease wait while options data downloads...\n")
    exp_dates_lst = list((str(soup)[(int(str(soup).find("expirationDates")) + 18):(int(str(soup).find("expirationDates")) + 414)]).split(",")) #Change 1 #Note this assumes there are the same number of expiration dates always.

    return [[(main_url+"?date="+date) for date in exp_dates_lst[0:num_exps]],num_exps,file_path]

def get_table_html(url):
    """
    Pull html from URL; parse w/ BeautifulSoup; return 'call' & 'put'
    table html and expiration date.
    """
    soup = bs(requests.get(url).content, 'html.parser')
    call_table_html = soup.find(class_="calls W(100%) Pos(r) Bd(0) Pt(0) list-options")
    put_table_html = soup.find(class_="puts W(100%) Pos(r) list-options")
    exp_date = dt.utcfromtimestamp((int(url[-10:]))).strftime('%Y-%m-%d')

    return call_table_html, put_table_html, exp_date

def html_to_df(table_html, option_type, exp_date):
    """
    For each expiration (an HTML table), take table_html, option_type, exp_date;
    parse table from html; load strike, bid, ask, vol, OI, and last trade
    columns into Pandas dataframe.
    """
    soup_lst = ["Fz(s) Ell C($linkColor)", #0 contracts
                "data-col2 Ta(end) Px(10px)", #1 strike
                "data-col4 Ta(end) Pstart(7px)", #2 bid
                "data-col5 Ta(end) Pstart(7px)", #3 ask
                "data-col8 Ta(end) Pstart(7px)", #4 vol
                "data-col9 Ta(end) Pstart(7px)", #5 oi
                "data-col1 Ta(end) Pstart(7px)", #6 lst trd
                "data-col10 Ta(end) Pstart(7px) Pend(6px) Bdstartc(t)" #7 imp vol
                ]
    txt_lst = []
    for col in soup_lst:
        html = table_html.find_all(class_=col)
        txt_lst.append([i.get_text() for i in html])

    return pd.DataFrame({   "datePulled": str(dt.now().strftime("%Y-%m-%d")),
                                    "timePulled": tm.strftime("%H:%M:%S"),
                                    "contract": txt_lst[0],
                                    "type": option_type,
                                    "expiry": exp_date,
                                    "strike": txt_lst[1],
                                    "bid": txt_lst[2],
                                    "ask": txt_lst[3],
                                    "volume": txt_lst[4],
                                    "oi": txt_lst[5],
                                    "lastTrd": txt_lst[6],
                                    "impVol": txt_lst[7]
                                    })

def create_and_write_df():
    """
    Take list of URLs for all forward expirations; get data through calls to
    get_table_html() and html_to_df(); concatenate dataframes; write full
    dataframe to .csv with number of expirations, and date pulled in filename
    """
    setup = setup_info() #urls for all expiries [0], number of expiries [1], save file path [2]
    full_frames = []
    for url in tqdm(setup[0]):
        optns_tbls_html = get_table_html(url) #This will return call and put table text html as [0] and [1]
        full_frames.append(html_to_df(optns_tbls_html[0], "CALL", optns_tbls_html[2]))
        full_frames.append(html_to_df(optns_tbls_html[1], "PUT", optns_tbls_html[2]))
        tm.sleep(0.4) #Throttle requests to be nice to server / not get blocked.
    #Concatenate all dfs and write to file
    col_lst = ["datePulled","timePulled","contract", "type", "expiry","strike","bid","ask","volume","oi","lastTrd","impVol"]
    pd.concat(full_frames).to_csv (r''+setup[2]+str(dt.now().strftime("%Y-%m-%d"))+'_SPY_Options_Data_'+str(setup[1])+'_expiries.csv',mode='w', index = False, header=True,columns=col_lst)

create_and_write_df()
print("\nDownload complete!")
