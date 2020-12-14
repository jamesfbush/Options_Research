# Date:         12/13/20
# Description:  Create html heatmap of options data for puts and calls showing
#               strike price (y-axis), expiration (x-axis), and intensity of
#               volume (z-axis) at given strike/expiry.

import pandas as pd
import plotly.graph_objects as go

#Global variables
csv_data = "[path_to_csv]"
heatmap_title = (' Volume SPY | {:s}' .format(csv_data[(csv_data.find("2020")):]))

def csv_to_df(csv_data):
    """Read option data from .csv; clean, arrange, and create Pandas dataframe."""
    #Create dataframe from .csv
    df = pd.DataFrame(pd.read_csv(
        csv_data,
        usecols=[2,3,4,7],
        names=['TYPE', 'EXPIRY', 'STRIKE', 'VOL'],
        skiprows=1,
        parse_dates=[0])
        )
    #Clean extraneous punctuation and zeros
    df.replace('-','0',inplace = True)
    df.replace(',','',inplace = True)
    df["VOL"] = df["VOL"].str.replace(",","").astype(float)
    df.fillna(0, inplace=True)
    #Split into separate "PUT" and "CALL" dataframs
    call_df = df[df.TYPE != 'PUT']
    del call_df['TYPE']
    put_df = df[df.TYPE != 'CALL']
    del put_df['TYPE']
    #Preview and return dataframes
    print("CALL",call_df.head(),"PUT",put_df.head())
    return call_df, put_df

def heatmap(df, type):
    """ Create .html based Plotly heatmap with expiry (x-axis), strike (y-axis),
    and volume (z-axis)."""
    #Invoke heatmap object and set x, y, z axes
    fig = go.Figure(data=go.Heatmap(
            x=df["EXPIRY"],
            y=df["STRIKE"],
            z=df["VOL"],
            colorbar=dict(title='VOL'),
            #Non-default green/orange/red color scheme on a log-ish scale for display.
            colorscale=[
                    [0, 'rgb(39, 125, 161)'],        #0
                    [1./160000, 'rgb(87, 117, 144)'], #10
                    [1./8000, 'rgb(67, 170, 139)'], #100
                    [1./400, 'rgb(249, 199, 79)'],  #1000
                    [1./20, 'rgb(248, 150, 30)'],  #10000
                    [1., 'rgb(249, 65, 68)'],
                    ])
            )
    #Adjust labeling of plot title and x-axis
    fig.update_layout(
        title=str(type+heatmap_title),
        xaxis_nticks=25,
        xaxis_tickangle=-45
        )
    #Display each heatmap and write html file to chosen directory
    fig.show()
    #fig.write_html(r"[path/title.html]")

#Call Heatmap
heatmap(csv_to_df(csv_data)[0],"CALL")
#Put Heatmap
heatmap(csv_to_df(csv_data)[1],"PUT")
