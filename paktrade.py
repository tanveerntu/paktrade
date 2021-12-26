import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly
import plotly.express as px
import urllib.request
import openpyxl
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import yfinance as yf


# Use the full page instead of a narrow central column
#st.set_page_config(layout='centered')
st.set_page_config(layout='wide')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("PAKISTAN TRADE STATISTICS")

# Add a selectbox to the sidebar:
option = st.selectbox(
'Please select an option',
('Textile Trade Statistics', 'Overall Trade Statistics', 'Cotton Statistics')
)

##########
if option == 'Cotton Statistics':
            import yfinance as yf

            from plotly import graph_objs as go

            import pandas as pd
            import streamlit as st 

            #
            # defining style color
            #colors = {"background": "#000000", "text": "#ffFFFF"}
            # Use the full page instead of a narrow central column

            from datetime import datetime, timedelta

            #data = yf.download(tickers=stock_price, period = ‘how_many_days’, interval = ‘how_long_between_each_check’, rounding= bool)
            #data = yf.download(tickers='CT=F', period = '5Y', interval = '1D', rounding= True)
            data = yf.download(tickers='CT=F', start = '2017-01-01', end = datetime.now().date(), rounding= True)

            #data 
            data= data.reset_index() # to show date as column header
            #data 

            ## getting the live ticker price

            # import stock_info module from yahoo_fin
            from yahoo_fin import stock_info as si

            #to get live price of ticker/cotton CT=F
            price = si.get_live_price('CT=F')
            prev_close = data.Close.iloc[-2] #iloc[-2] is second last row of res_df ; iloc[0] is first row 


            ##




            fig = go.Figure()

            fig.add_trace(go.Scatter(x=data['Date'], 
                                    y=data['Close'], 
                                    name = '',
                                    texttemplate='%{text:.2s}', # to  shorten text into 3 digits, use '%{text:.3s}'
                                    ))
            fig.update_traces(hovertemplate='Date: %{x} <br>Price: %{y} cents per pound') #<br> adds space or shifts to next line; x & y is repected axis value; 

            fig.add_trace(go.Indicator(
                        domain={"x": [0, 1], "y": [0.5, 1]},
                        value=price,
                        mode="number+delta",
                        title={"text": "Live Price in cents per pound"},
                        delta={"reference": prev_close},
                    ))

            fig.update_xaxes(
            rangeslider_visible = False,
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1W', step = 'day', stepmode = 'backward'),
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(count = 5, label = '5Y', step = 'year', stepmode = 'backward'),
                #dict(step = 'all')
                ])))

            fig.update_yaxes(title_text = 'Cents Per Pound', tickprefix = '')
            #fig.update_xaxes(showspikes=True, spikecolor="red", spikesnap="cursor", spikemode="across", spikethickness=3) #xaxis spike on hover
            #fig.update_yaxes(showspikes=True, spikecolor="red", spikesnap="cursor", spikemode="across", spikethickness=3) #yais spike on hover

            fig.update_layout(
                autosize=True, height=700, width=1100,
                title="Cotton Rates - ICE Futures", 
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=36, color='#111111', family="fjalla one, sans-serif"),
                #hovermode='x unified',
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"),    #font of lablels of axises
                template='presentation'
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig.add_annotation(
                        text="Source: Yahoo Finance/NTU",
                        xref="x domain", yref="y domain",
                        x=0.5, y=-0.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig, use_container_width=True) # to show Figure; container width true makes fig. size responsive
            
            ####################
            ###cotton arrivals
            ###################
            df_cotton_arrivals = pd.read_csv('cotton_arrivals.csv')

            fig_cotton_arrivals = go.Figure()

            fig_cotton_arrivals.add_trace(go.Scatter(
                x=df_cotton_arrivals["Date"], 
                y=df_cotton_arrivals["2018-19"], 
                name="2018-19", 
                text=df_cotton_arrivals['2018-19'],
                texttemplate='%{text:.3s}', #text shorten into 3 digits
                mode="markers+lines",
                textposition="bottom right",
                textfont=dict(family="roboto, sans-serif", size=18, color="Purple"),
                marker=dict(size=12, color="Purple"),
                line=dict(width=2.5, color="Purple"),
            ))

            fig_cotton_arrivals.add_trace(go.Scatter(
                x=df_cotton_arrivals["Date"], 
                y=df_cotton_arrivals["2019-20"], 
                name="2019-20", 
                text=df_cotton_arrivals['2019-20'],
                texttemplate='%{text:.3s}', #text shorten into 3 digits
                mode="markers+lines",
                textposition="bottom right",
                textfont=dict(family="roboto, sans-serif", size=18, color="Green"),
                marker=dict(size=12, color="Green"),
                line=dict(width=2.5, color="Green"),
            ))

            fig_cotton_arrivals.add_trace(go.Scatter(
                x=df_cotton_arrivals["Date"], 
                y=df_cotton_arrivals["2020-21"], 
                name="2020-21", 
                text=df_cotton_arrivals['2020-21'],
                texttemplate='%{text:.3s}', #text shorten into 3 digits
                mode="markers+lines",
                textposition="bottom right",
                textfont=dict(family="roboto, sans-serif", color="Blue", size=18),
                marker=dict(size=12, color="Blue"),
                line=dict(width=2.5, color="Blue"),
            ))

            fig_cotton_arrivals.add_trace(go.Scatter(
                x=df_cotton_arrivals["Date"], 
                y=df_cotton_arrivals["2021-22"], 
                name="2021-22", 
                text=df_cotton_arrivals['2021-22'],
                texttemplate='%{text:.3s}', # to text shorten into 3 digits, use '%{text:.3s}'
                mode="markers+lines+text",
                textposition="bottom right",
                textfont=dict(family="fjalla one, sans-serif", color="Red", size=20),
                marker=dict(size=12, color="Red"),
                line=dict(width=2.5, color="Red")
            ))

            fig_cotton_arrivals.update_layout(
                autosize=True, height=700, width=1100,
                title="Cotton Arrivals in Pakistani Factories",
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Cumulative No. of Cotton Bales",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_cotton_arrivals.add_annotation(
                        text="Source: PCGA/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_cotton_arrivals, use_container_width=True) # to show Figure; container width true makes fig. size responsive


#############

elif option == 'Overall Trade Statistics': 

            api_url = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&ps=now&r=586&p=all&rg=all&cc=TOTAL&fmt=csv'


            #get.Comtrade <- function(url="http://comtrade.un.org/api/get?"
                #,maxrec=50000
                #,type="C"
                #,freq="A"
                #,px="HS"
                #,ps="now"
                #,r
                #,p
                #,rg="all"
                #,cc="TOTAL"
                #,fmt="json"


            #,"max=",maxrec,"&" #maximum no. of records returned
            #,"type=",type,"&" #type of trade (c=commodities)
            #,"freq=",freq,"&" #frequency
            #,"px=",px,"&" #classification
            #,"ps=",ps,"&" #time period
            #,"r=",r,"&" #reporting area ; put r= 586 for Pakistan
            #,"p=",p,"&" #partner country
            #,"rg=",rg,"&" #trade flow
            #,"cc=",cc,"&" #classification code
            #,"fmt=",fmt        #Format
            #,sep = ""


            response=requests.get(api_url)

            data = response.content

            with open('output.csv', 'wb') as output:
                output.write(data)
                df = pd.read_csv("output.csv")

            st.title("Overall Pakistan Trade")
            st.write("Compiled by: National Textile Univeristy Pakistan, from UNComtrade Database.")
            #to filter values based on trade flow code
            df_import = df[df['Trade Flow Code'] == 1]
            df_export = df[df['Trade Flow Code'] == 2]

            #to show dataframes
            df_import.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False) #to sort values in descending order
            df_export.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False)

            df_import.reset_index(drop=True, inplace=True) #to reset index numbering of DF
            df_export.reset_index(drop=True, inplace=True)

            df_w = df[df['Partner'] == 'World'] #filtering only by partner 'world'


            df_w.reset_index(drop=True, inplace=True)





            ######################
            ########################################
            #Pakistan Imports and Exports
            ######################################

            #IMPORT EXPORT ALL YEARS
            api_url = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&ps=all&r=586&p=0&rg=all&cc=TOTAL&fmt=csv'
            response = requests.get(api_url)

            data = response.content

            with open('output.csv', 'wb') as output:
                output.write(data)
                df_all_years = pd.read_csv("output.csv")

            df_all_years_import = df_all_years[df_all_years['Trade Flow Code'] == 1]
            df_all_years_export = df_all_years[df_all_years['Trade Flow Code'] == 2]
            df_all_years_export.sort_values(by=['Year'], inplace=True, ascending=False)
            df_all_years.sort_values(by=['Year'], inplace=True, ascending=False)

            #st.subheader("Pak Imports and Exports Over the Years")


            ############################
            #fig = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col

            ###############################
            fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.04) # to make subplot with 1 row and 1 col #column_widths
            fig.add_trace(go.Bar(x=df_all_years_import['Year'], 
                                y=df_all_years_import['Trade Value (US$)'],
                                name='Imports', 
                                text=df_all_years_import['Trade Value (US$)'],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                marker_color='crimson', 
                                hovertemplate='%{y}B'
                                #yaxis_title='Imports US$'
                                ), row=1, col=1)

            fig.add_trace(go.Bar(x=df_all_years_export['Year'], 
                                y=df_all_years_export['Trade Value (US$)'],
                                name='Exports', 
                                text=df_all_years_export['Trade Value (US$)'],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                marker_color='darkcyan', 
                                hovertemplate='%{y}B'
                                #yaxis_title='Exports US$'
                                ), row=2, col=1)
            fig.update_yaxes(title_text="Exports US$", row=2, col=1)
            fig.update_yaxes(title_text="Imports US$", row=1, col=1)


            fig.update_xaxes(
                rangeslider_visible = False,
                rangeselector = dict(
                buttons = list([
                #dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                #dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                #dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig.add_annotation(
                        text="Source: UNComtrade/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))
            fig.update_layout(
                autosize=True, height=700, width=1100,
                #legend_traceorder="reversed",
                margin=dict(t=80, b=0, l=40, r=40),
                title="Pakistan Exports and Imports Over the Years",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
            )
            st.plotly_chart(fig, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            ###############################
            ########################################
            #Top 10 Trading partners
            ######################################
            api_url2 = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&cc=52,53,54,55,56,57,58,59,60,61,62,63&ps=now&r=586&p=all&rg=2&cc=TOTAL&fmt=csv'

            response = requests.get(api_url2)
            data = response.content
            with open('output.csv', 'wb') as output:
                output.write(data)
                df2 = pd.read_csv("output.csv")

            df2_export = df2[df2['Trade Flow Code'] == 2][df2['Partner Code'] == 0] #filtering only by exports code 2 and partner code 0
            df2_export.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False)
            #df['column name'] = df['column name'].replace(['old value'],'new value') # stntex to replace values
            ###
            top10importers = df_import.nlargest(11,'Trade Value (US$)')
            top10exporters = df_export.nlargest(11,'Trade Value (US$)')

            top10exp = top10exporters[top10exporters.Partner != 'World'] #excluding 'world' as partner
            top10imp = top10importers[top10importers.Partner != 'World'] #excluding 'world' as partner

            dfi = df_import[df_import.Partner != 'World']
            dfe = df_export[df_export.Partner != 'World']
            ########################################
            #Top 10  countries Importing from Pakistan
            ########################################
            fig = make_subplots(rows=1, cols=2) # to make subplot with 1 row and 1 col
            fig.add_trace(go.Bar(x=top10exp['Trade Value (US$)'],
                                    y=top10exp['Partner'],
                                    text=top10exp['Trade Value (US$)'],
                                    textposition='auto',
                                    texttemplate='$%{text:,}',
                                    hovertemplate='%{x}',
                                    name='Countries Importing from Pakistan',
                                    orientation='h', 
                                    marker_color='darkcyan'
                                ), row=1, col=1)

            fig.add_trace(go.Bar(x=top10imp['Trade Value (US$)'],
                                    y=top10imp['Partner'],
                                    text=top10imp['Trade Value (US$)'],
                                    textposition='auto',
                                    texttemplate='$%{text:,}',
                                    hovertemplate='%{x}',
                                    name='Countries Exporting to Pakistan',
                                    orientation='h', 
                                    marker_color='crimson'
                                ), row=1, col=2)

            fig.update_yaxes({'categoryorder':'total ascending'}, row=1, col=1)
            fig.update_yaxes({'categoryorder':'total ascending'}, row=1, col=2)
            fig.update_xaxes(
                rangeslider_visible = False,
                rangeselector = dict(
                buttons = list([
                #dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                #dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                #dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig.add_annotation(
                        text="Source: UNComtrade/NTU",
                        xref="x domain", yref="y domain",
                        x=2.2, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))
            fig.update_layout(
                autosize=True, height=700, width=1100,
                #legend_traceorder="reversed",
                margin=dict(t=80, b=0, l=40, r=40),
                title="Pakistan's Top 10 Trading Partners",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
            )
            st.plotly_chart(fig, use_container_width=True) # to show Figure; container width true makes fig. size responsive


else:

    #Required imports

            import plotly.express as px
            from plotly import graph_objs as go
            from plotly.subplots import make_subplots
            import pandas as pd
            import streamlit as st 

            ##
            # Use the full page instead of a narrow central column
            st.title("Pakistan Textile Exports")
            st.write("Data Source: Pakistan Bureau of Statistics")




            # ---- HIDE STREAMLIT STYLE ----
            # ---- HIDE STREAMLIT STYLE ----
            hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                        """
            st.markdown(hide_st_style, unsafe_allow_html=True)



            ###
            #importing csv file as dataframe
            df = pd.read_csv('monthly_textile_exports_pbs.csv')
            #df # to see dataframe
            #df
            #convert date columns into datetime format
            df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True) 
            #df 
            df['year'] = df['date'].dt.year #creates a year column out of datetime columns
            #df
            df['month'] = df['date'].dt.month #creates a month column out of datetime columns
            #df 
            df['year'] = df['year'].astype('string') #converting year column into string for filtering 
            df['month'] = df['month'].astype('string') #converting year column into string for filtering
            #creating different dataframe from the main df by filtering, etc.

            #filtering date between specific dates
            #df_2020_21 = df[(df['date'] > '2020-01-01') & (df['date'] < '2021-12-31')]

            df_2020_21 = df.loc[(df['date'] >= '2020-01-01') & (df['date'] < '2021-12-31')] #filtering date only between specific dates
            df_2020 = df.loc[(df['date'] >= '2020-01-01') & (df['date'] < '2020-12-31')] #filtering date only between specific dates
            df_2021 = df.loc[(df['date'] >= '2021-01-01') & (df['date'] < '2021-12-31')] #filtering date only between specific dates



            #grouping all categories of exports in monthly frequency, preserving datetime index
            df_monthly_sum = df.groupby(pd.Grouper(key = 'date', freq='1M')).sum().reset_index()
            df_2020_21_monthly_sum = df_2020_21.groupby(pd.Grouper(key = 'date', freq='1M')).sum().reset_index()
            df_2020_monthly_sum = df_2020.groupby(pd.Grouper(key = 'date', freq='1M')).sum().reset_index()
            df_2021_monthly_sum = df_2021.groupby(pd.Grouper(key = 'date', freq='1M')).sum().reset_index()


            #adding 'Fiscal Year' columns
            df_monthly_sum['Fiscal Year'] = df_monthly_sum['date'].dt.to_period('Q-JUN').dt.qyear.apply(lambda x: str(x-1) + "-" + str(x))
            #adding month column
            df_monthly_sum['month'] = df_monthly_sum['date'].dt.strftime('%b') #creating month names column


            #calculating year-to-date YTD exports
            df_monthly_sum['Exports_YTD'] = df_monthly_sum.groupby(['Fiscal Year'])['Exports_US$'].cumsum()


            df_monthly_sum['pct_change_yoy'] = df_monthly_sum.groupby(['month'])['Exports_YTD'].pct_change()*100


            df_2021_22 = df_monthly_sum.loc[df_monthly_sum['Fiscal Year'].isin(['2021-2022'])]
            df_2020_21 = df_monthly_sum.loc[df_monthly_sum['Fiscal Year'].isin(['2020-2021'])]

            ########################################
            ########################################
            #Year to date chart of fiscal year
            #########################################
            fig_ytd = go.Figure()
            fig_ytd = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col

            # Add traces
            fig_ytd.add_trace(go.Bar(x=df_2020_21['month'], y=df_2020_21['Exports_YTD'],
                                name='Exports in 2020-21', 
                                text=df_2020_21['Exports_YTD'],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                hovertemplate='%{x} <br>Exports to date: %{y}'
                                ), row=1, col=1, secondary_y=True)
            fig_ytd.add_trace(go.Scatter(x=df_2021_22['month'], y=df_2021_22['Exports_YTD'],
                                mode='markers+lines+text',
                                marker=dict(size=16, color="Green"), 
                                name='Exports in 2021-22',
                                text=df_2021_22['Exports_YTD'],
                                textposition='top left',
                                texttemplate="%{text:,}",
                                line=dict(color='Green', width=4),
                                hovertemplate='%{x} <br>Exports to date: %{y}B'
                                ), row=1, col=1, secondary_y=True)
            fig_ytd.add_trace(go.Scatter(x=df_2021_22['month'], 
                                    y=df_2021_22['pct_change_yoy'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=16, color="Red"), 
                                    name="pct_change_yoy", 
                                    text=df_2021_22['pct_change_yoy'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text:.2s}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Year: %{x} <br>YOY: %{y} %',
                                    ), row=1, col=1 )
            fig_ytd.update_yaxes(title_text="Cumulative Exports in US$", secondary_y=True)
            fig_ytd.update_layout(
                autosize=True, height=700, width=1100,
                legend_traceorder="reversed",
                margin=dict(t=80, b=0, l=40, r=40),
                title="Pakistan Textile Exports",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="YOY change %",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
            )
            fig_ytd.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_ytd.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))
            st.plotly_chart(fig_ytd, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            ################


            ###################################
            ###################################

            df_2020_21_monthly_sum['year_month'] = df_2020_21_monthly_sum['date'].dt.strftime('%Y-%m') #creating year_month columns
            df_2020_21_monthly_sum['year_month'] = df_2020_21_monthly_sum['year_month'].astype('string') #converting year_month column into string for filtering

            df_2020_21_monthly_sum['month'] = df_2020_21_monthly_sum['date'].dt.month #creates a month column out of datetime columns
            df_monthly_sum['month'] = df_monthly_sum['date'].dt.month #creates a month column out of datetime columns


            #filtering dataframes for each category of exports
            df_yarn = df.loc[df['category'].isin(['Cotton Yarn'])] #df contain yarn data only
            df_cloth = df.loc[df['category'].isin(['Cotton Cloth'])]
            df_towels = df.loc[df['category'].isin(['Towels'])]
            df_knitwear = df.loc[df['category'].isin(['Knitwear'])]
            df_bedwear = df.loc[df['category'].isin(['Bedwear'])]
            df_garments = df.loc[df['category'].isin(['Garments'])]
            #

            ###############################
            #adding percentate chage columns

            df_monthly_sum['pct_change_value'] = df_monthly_sum.groupby(['month'])['Exports_US$'].pct_change()*100

            #adding column pct_change_volume 
            df_yarn['pct_change_volume'] = df_yarn.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_yarn['pct_change_value'] = df_yarn.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_yarn['pct_change_unit_price'] = df_yarn.groupby(['month'])['unit_price'].pct_change()*100
            #df_yarn

            ###############################
            #adding column pct_change_volume 
            df_cloth['pct_change_volume'] = df_cloth.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_cloth['pct_change_value'] = df_cloth.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_cloth['pct_change_unit_price'] = df_cloth.groupby(['month'])['unit_price'].pct_change()*100


            ###############################
            #adding column pct_change_volume 
            df_knitwear['pct_change_volume'] = df_knitwear.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_knitwear['pct_change_value'] = df_knitwear.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_knitwear['pct_change_unit_price'] = df_knitwear.groupby(['month'])['unit_price'].pct_change()*100
            #df_knitwear

            ###############################
            #adding column pct_change_volume 
            df_bedwear['pct_change_volume'] = df_bedwear.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_bedwear['pct_change_value'] = df_bedwear.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_bedwear['pct_change_unit_price'] = df_bedwear.groupby(['month'])['unit_price'].pct_change()*100
            #df_bedwear



            ###############################
            #adding column pct_change_volume 
            df_garments['pct_change_volume'] = df_garments.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_garments['pct_change_value'] = df_garments.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_garments['pct_change_unit_price'] = df_garments.groupby(['month'])['unit_price'].pct_change()*100

            df_garments['pct_change_yoy'] = df_garments['volume'].pct_change(12)*100 #add 12 in pct_change brackets for 12 months in a year

            ###############################
            #adding column pct_change_volume 
            df_towels['pct_change_volume'] = df_towels.groupby(['month'])['volume'].pct_change()*100
            #adding column pct_change_value
            df_towels['pct_change_value'] = df_towels.groupby(['month'])['Exports_US$'].pct_change()*100
            #adding column pct_change_unit_price
            df_towels['pct_change_unit_price'] = df_towels.groupby(['month'])['unit_price'].pct_change()*100



            df_garments_yearly_vol = df_garments.groupby(["year"]).agg({"volume": "sum"}).reset_index() #group by year, getting sum of exports
            df_garments_yearly_vol['YOY % change'] = df_garments_yearly_vol['volume'].pct_change()*100


            df_knitwear_yearly_vol = df_knitwear.groupby(["year"]).agg({"volume": "sum"}).reset_index() #group by year, getting sum of exports
            df_knitwear_yearly_vol['difference']=df_knitwear_yearly_vol['volume'].diff(1) # create 'difference' column with difference of 1 year each
            df_knitwear_yearly_vol['YOY % change']=round(df_knitwear_yearly_vol['difference']/df_knitwear_yearly_vol['volume']*100,2) #YOY% column; values rounded to 2 decimals
            #df_knitwear_yearly_vol

            df_bedwear_yearly_vol = df_bedwear.groupby(["year"]).agg({"volume": "sum"}).reset_index() #group by year, getting sum of exports
            df_bedwear_yearly_vol['difference']=df_bedwear_yearly_vol['volume'].diff(1) # create 'difference' column with difference of 1 year each
            df_bedwear_yearly_vol['YOY % change']=round(df_bedwear_yearly_vol['difference']/df_bedwear_yearly_vol['volume']*100,2) #YOY% column; values rounded to 2 decimals
            #df_bedwear_yearly_vol

            df_towels_yearly_vol = df_towels.groupby(["year"]).agg({"volume": "sum"}).reset_index() #group by year, getting sum of exports
            df_towels_yearly_vol['difference']=df_towels_yearly_vol['volume'].diff(1) # create 'difference' column with difference of 1 year each
            df_towels_yearly_vol['YOY % change']=round(df_towels_yearly_vol['difference']/df_towels_yearly_vol['volume']*100,2) #YOY% column; values rounded to 2 decimals
            #df_towels_yearly_vol

            df_yarn_yearly_vol = df_yarn.groupby(["year"]).agg({"volume": "sum"}).reset_index() #group by year, getting sum of exports
            df_yarn_yearly_vol['difference']=df_yarn_yearly_vol['volume'].diff(1) # create 'difference' column with difference of 1 year each
            df_yarn_yearly_vol['YOY % change']=round(df_yarn_yearly_vol['difference']/df_yarn_yearly_vol['volume']*100,2) #YOY% column; values rounded to 2 decimals
            #df_yarn_yearly_vol



            #
            yearly_sum = df.groupby(["year", "category"]).agg({"Exports_US$": "sum"}).reset_index() #group by year, then category, getting sum of exports

            #yearly_sum
            #


            year_summary = df.groupby('year').sum()
            year_summary = year_summary.reset_index()
            #adding columns 'YOY % change'
            year_summary['YOY % change'] = year_summary['Exports_US$'].pct_change()*100

            #filtering data of 2021
            df_2021 = df.loc[df['year'].isin(['2021'])].reset_index()


            ## creating df containing only yearly aggregate of exports
            df_yearly = df.groupby(['year']).agg(**{'Exports_US$_sum': ('Exports_US$', 'sum')}).reset_index()
            #groupby year, then category



            # setting first name as index column
            df_yearly.set_index("year", inplace = True)
            #getting exact value of exports in each year
            exports_2019=df_yearly.loc['2019']['Exports_US$_sum']
            exports_2020=df_yearly.loc['2020']['Exports_US$_sum']
            exports_2021=df_yearly.loc['2021']['Exports_US$_sum']


            ### 


            from datetime import datetime, date, time

            ##########################################
            ##########################################
            #Adding yearly indicators
            #########################################
            #Yearly indicators subplots
            # Initialize figure with subplots
            fig_yearly_indicators = make_subplots(
                rows=1, cols=3, 
            )
            # Add traces
            fig_yearly_indicators.add_trace(go.Indicator(
                mode = "number+delta",
                title = {"text": "Exports in 2019"},
                value = int(exports_2019),           #int converts value to integer
                number = {'prefix': "$"},
                domain = {'row': 1, 'column': 0}))

            fig_yearly_indicators.add_trace(go.Indicator(
                mode = "number+delta",
                title = {"text": "Exports in 2020"},
                value = int(exports_2020),
                number = {'prefix': "$"},
                delta = {'reference': int(exports_2019), 'relative': True}, #relative argument gives delta in %
                domain = {'row': 1, 'column': 1}))

            fig_yearly_indicators.add_trace(go.Indicator(
                mode = "number+delta",    
                title = {"text": "Exports in Jan-Nov 2021"},
                value = int(exports_2021),
                number = {'prefix': "$"},
                delta = {'reference': int(exports_2020), 'relative': True},
                domain = {'row': 1, 'column': 2}))

            fig_yearly_indicators.update_layout(
                grid = {'rows': 1, 'columns': 3, 'pattern': "independent"}, #defining grid is important before assigning properties in domain of add_trace
                autosize=True, height=400, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Pakistan Textile Exports in the Last 3 Years",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                template="presentation",
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
            )

            st.plotly_chart(fig_yearly_indicators, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #2021 indicators subplots
            df_year_category = df.groupby(['year', 'category']).agg(**{'Exports_US$_sum': ('Exports_US$', 'sum')}).reset_index()

            #df_year_category 
            df_category_2021 = df_year_category.loc[df_year_category['year'].isin(['2021'])].reset_index()
            ##
            #get value of categorywise exports in specific year
            knitwear2021 = df_year_category.loc[(df_year_category['year'] == "2021") & (df_year_category['category'] == "Knitwear")]['Exports_US$_sum'].item()
            bedwear2021 = df_year_category.loc[(df_year_category['year'] == "2021") & (df_year_category['category'] == "Bedwear")]['Exports_US$_sum'].item()

            #knitwear2021
            ########################################
            #########################################

            #######################################
            #######################################
            #2021 pie chart
            #######################################
            #pie chart
            ####
            fig_all2 = px.pie(df_2021, values='Exports_US$', 
                                names='category', 
                                color='category',
                                labels={"category":"Category"},
                                hole=0.7, 
                                title="Pakistan Textile Exports Jan-Nov 2021",
                                template='plotly'
                                )

            fig_all2.update_traces(textposition='outside', textinfo='value+percent+label',
                                    marker=dict(line=dict(color='#111111', width=0.5)), #color and size of lines between slices
                                    pull=[0, 0, 0, 0], opacity=1, rotation=170,
                                    automargin=True) #increasing value of pull from 0-1 will pull a slice out

            fig_all2.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=100, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=16, family="roboto, sans-serif"),    #font of lablels of axises
            )
            fig_all2.add_annotation( #number = str("{:,}".format(number)) , to fomat with comma separator
                        text="Total: $" + str("{:,}".format(exports_2021)), #variable value is printed inside piechart only as string
                        font=dict(color='#111111', size=36, family="roboto, sans-serif"),
                        #xanchor="left",
                        #yanchor="bottom",
                        showarrow=False,
                        arrowhead=1)
            fig_all2.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1.3, y=-0.2, 
                        showarrow=False,
                        arrowhead=1)

            #
            #
            st.plotly_chart(fig_all2, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #

            #
            ##################################################
            ##################################################
            #yearly charts
            ##################################################
            ##################################################

            #combine two plots

            from plotly.subplots import make_subplots
            fig = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig.add_trace(go.Bar(x=year_summary['year'], 
                                y=year_summary['Exports_US$'], 
                                name="Exports_US$", 
                                text = year_summary["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=year_summary['year'], 
                                    y=year_summary['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=year_summary['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text:.2s}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Year: %{x} <br>YOY: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig.update_yaxes(title_text="YOY % change", secondary_y=True)

            fig.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Textile Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)


            st.plotly_chart(fig, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #################################################
            #################################################
            #yearly summary of categories

            st.header("Category-wise Yearly Pakistan Textile Exports by Value")
            st.write("Cick on category names in the legend to select or de-select")

            fig_yearly_sum = px.bar(yearly_sum, x="year", y="Exports_US$", color="category", text ="Exports_US$", title="Category-wise Yearly Pakistan Textile Exports by Value",
                template='plotly_white')
            fig_yearly_sum.update_traces(texttemplate='%{text:,}') #adding comma separators in numbers in bars

            fig_yearly_sum.update_layout(
                autosize=True, height=700, width=1100,
                legend_traceorder="reversed",
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_yearly_sum.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            #
            # Add dropdown 
            # giving chart type change option Using Restyle Method
            fig_yearly_sum.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="up", #sets direction of buttons, right, left, up, or down
                        buttons=list([
                            dict(
                                args=["type", "scatter"],
                                label="Scatter Plot",
                                method="restyle"
                            ),
                            dict(
                                args=["type", "bar"],
                                label="Bar Chart",
                                method="restyle"
                            )
                        ]),
                    ),
                ]
            )


            st.plotly_chart(fig_yearly_sum, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            ##################################################
            ##################################################
            #bar chart for garments
            fig_garments_yearly = px.bar(df_garments_yearly_vol, x="year", y="volume", text="volume", title="Yearly Pakistan Ready-made Garment Exports by Volume",
                template='plotly_dark')


            fig_garments_yearly.update_traces(texttemplate='%{text:.4s}') #to convert figures in short short form, e.g. millions

            fig_garments_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_garments_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            #st.plotly_chart(fig_garments_yearly, use_container_width=True) # to show Figure

            ## garment volume chart with YOY
            fig_garments_yearly = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_garments_yearly.add_trace(go.Bar(x=df_garments_yearly_vol['year'], 
                                y=df_garments_yearly_vol['volume'], 
                                name="volume", 
                                text = df_garments_yearly_vol["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig_garments_yearly.add_trace(go.Scatter(x=df_garments_yearly_vol['year'], 
                                    y=df_garments_yearly_vol['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=df_garments_yearly_vol['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text:.2s}%",
                                    line=dict(color='Red', width=2, dash='dash')
                                    ), row=1, col=1, secondary_y=True)
            fig_garments_yearly.update_yaxes(title_text="YOY % change", secondary_y=True)


            fig_garments_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Ready-made Garment Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig_garments_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_garments_yearly, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            ##################################################
            #bar chart for knitwear

            ##
            fig_knitwear_yearly = px.bar(df_knitwear_yearly_vol, x="year", y="volume", text="volume", title="Yearly Pakistan Knitwear Exports by Volume",
                template='plotly_dark')


            fig_knitwear_yearly.update_traces(texttemplate='%{text:.4s}') #to convert figures in short short form, e.g. millions

            fig_knitwear_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_knitwear_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            #st.plotly_chart(fig_knitwear_yearly, use_container_width=True) # to show Figure

            ## yearly chart of knitwear with YOY
            fig_knitwear_yearly = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_knitwear_yearly.add_trace(go.Bar(x=df_knitwear_yearly_vol['year'], 
                                y=df_knitwear_yearly_vol['volume'], 
                                name="volume", 
                                text = df_knitwear_yearly_vol["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig_knitwear_yearly.add_trace(go.Scatter(x=df_knitwear_yearly_vol['year'], 
                                    y=df_knitwear_yearly_vol['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=df_knitwear_yearly_vol['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text}%",
                                    line=dict(color='Red', width=2, dash='dash')
                                    ), row=1, col=1, secondary_y=True)
            fig_knitwear_yearly.update_yaxes(title_text="YOY % change", secondary_y=True)
            fig_knitwear_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Knitwear Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig_knitwear_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_knitwear_yearly, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            ##
            ##

            ## yearly chart of yarn with YOY
            fig_yarn_yearly = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_yarn_yearly.add_trace(go.Bar(x=df_yarn_yearly_vol['year'], 
                                y=df_yarn_yearly_vol['volume'], 
                                name="volume", 
                                text = df_yarn_yearly_vol["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig_yarn_yearly.add_trace(go.Scatter(x=df_yarn_yearly_vol['year'], 
                                    y=df_yarn_yearly_vol['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=df_yarn_yearly_vol['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text}%",
                                    line=dict(color='Red', width=2, dash='dash')
                                    ), row=1, col=1, secondary_y=True)
            fig_yarn_yearly.update_yaxes(title_text="YOY % change", secondary_y=True)
            fig_yarn_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Yarn Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig_yarn_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_yarn_yearly, use_container_width=True) # to show Figure; container width true makes fig. size responsive
            ###

            ##
            #
            ## yearly chart of towels with YOY
            fig_towels_yearly = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_towels_yearly.add_trace(go.Bar(x=df_towels_yearly_vol['year'], 
                                y=df_towels_yearly_vol['volume'], 
                                name="volume", 
                                text = df_towels_yearly_vol["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig_towels_yearly.add_trace(go.Scatter(x=df_towels_yearly_vol['year'], 
                                    y=df_towels_yearly_vol['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=df_towels_yearly_vol['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text}%",
                                    line=dict(color='Red', width=2, dash='dash')
                                    ), row=1, col=1, secondary_y=True)
            fig_towels_yearly.update_yaxes(title_text="YOY % change", secondary_y=True)
            fig_towels_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Towel Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig_towels_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_towels_yearly, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #############################################
            ## yearly chart of bedwear with YOY
            fig_bedwear_yearly = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_bedwear_yearly.add_trace(go.Bar(x=df_bedwear_yearly_vol['year'], 
                                y=df_bedwear_yearly_vol['volume'], 
                                name="volume", 
                                text = df_bedwear_yearly_vol["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}',
                                ), row=1, col=1)
            fig_bedwear_yearly.add_trace(go.Scatter(x=df_bedwear_yearly_vol['year'], 
                                    y=df_bedwear_yearly_vol['YOY % change'], 
                                    mode="lines+markers+text", 
                                    marker=dict(size=20, color="Red"), 
                                    name="YOY % change", 
                                    text=df_bedwear_yearly_vol['YOY % change'],
                                    textposition='top center',
                                    texttemplate="YOY: %{text}%",
                                    line=dict(color='Red', width=2, dash='dash')
                                    ), row=1, col=1, secondary_y=True)
            fig_bedwear_yearly.update_yaxes(title_text="YOY % change", secondary_y=True)
            fig_bedwear_yearly.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Yearly Pakistan Bedwear Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=24, family="roboto, sans-serif"))
            fig_bedwear_yearly.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            st.plotly_chart(fig_bedwear_yearly, use_container_width=True) # to show Figure; container width true makes fig. size responsive
            ##


            ##################################################
            ###################################################

            ###
            #monthly summary of the last two years
            fig_monthly_summary = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_monthly_summary.add_trace(go.Bar(x=df_monthly_sum['date'], 
                                y=df_monthly_sum['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_monthly_sum["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:,}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_monthly_summary.add_trace(go.Scatter(x=df_monthly_sum['date'], 
                                    y=df_monthly_sum['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_monthly_sum['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_monthly_summary.update_xaxes(
                title_text = 'Date',
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_monthly_summary.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title="Monthly Pakistan Textile Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_monthly_summary.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_monthly_summary.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_monthly_summary.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%Y",
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 25)

            st.plotly_chart(fig_monthly_summary, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            ###


            ##

            ##




            #plot with two y-axis
            ###

            df_total = df.groupby(pd.Grouper(key='date',axis=0, freq='M')).sum()
            # to show date as column header, not as index
            df_total = df_total.reset_index() # to show date as column header
            #df_total

            #creating figures from dataframes

            # line chart of all categories



            ###
            #bar chart of all categories

            st.header("Monthly Pakistan Textile Exports by Value")
            st.write("Cick on category names in the legend to select or de-select")

            fig_all1 = px.bar(df, x="date", y="Exports_US$", color="category", text ="Exports_US$", title="Monthly Pakistan Textile Exports by Value",
                template='plotly_dark')


            fig_all1.update_xaxes(
                title_text = 'Date',
                rangeslider_visible = False,
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_all1.update_traces(texttemplate='%{text:.2s}') #to convert figures in short short form, e.g. millions

            fig_all1.update_layout(
                autosize=True, height=700, width=1100,
                legend_traceorder="reversed",
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=16, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_all1.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)

            fig_all1.update_xaxes(
                    tickangle = 90,
                    ticks="inside",
                    title_text = "",
                    dtick='M1',
                    title_font = {"size": 2},
                    title_standoff = 25)
            st.plotly_chart(fig_all1, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            ##
            st.header("Monthly Trend of Category-wise Pakistan Textile Exports by Value")
            st.write("Cick on category names in the legend to select or de-select")

            fig_all = px.line(df, x="date", y="Exports_US$", color="category", title="Monthly Trend of Category-wise Pakiatan Textile Exports by Value",
                template='plotly_dark', markers=True)

            fig_all.update_xaxes(
            title_text = 'Date',
            rangeslider_visible = False,
            rangeselector = dict(
            buttons = list([
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))

            fig_all.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=16, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_all.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1, 
                        showarrow=False,
                        arrowhead=1)
            #fig_all.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig_all, use_container_width=True) # to show Figure

            ##


            ###
            #bar chart of df_total

            #bar chart of all categories
            fig_total = px.bar(df_total, x="date", y="Exports_US$", title="",
                template='plotly_dark')


            fig_total.update_xaxes(
                title_text = 'Date',
                rangeslider_visible = False,
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))

            fig_total.update_layout(
                autosize=True, height=700, width=1100,
                #margin=dict(t=60, b=0, l=40, r=40),
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Exports in US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=16, family="roboto, sans-serif"),    #font of lablels of axises
                bargap=0.2,                             #value can be An int or float in the interval [0, 1]
                #legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            #st.plotly_chart(fig_total) # to show Figure

            ###
            #df_garments

            ###


            #df_monthly = df.groupby(['month']).agg(**{'Exports_US$_sum': ('Exports_US$', 'sum')}).reset_index()

            df_monthly = df.groupby(['year', 'month'])['Exports_US$'].sum().reset_index()
            df_monthly['pct_change'] = df_monthly.groupby(['month'])['Exports_US$'].pct_change()*100

            #####################################################
            #monthly garment exports by value with mom pct_change
            #####################################################
            fig_garments_mom_val = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_garments_mom_val.add_trace(go.Bar(x=df_garments['date'], 
                                y=df_garments['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_garments["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:,}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_garments_mom_val.add_trace(go.Scatter(x=df_garments['date'], 
                                    y=df_garments['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_garments['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_garments_mom_val.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_garments_mom_val.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Garment Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_garments_mom_val.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_garments_mom_val.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_garments_mom_val.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_garments_mom_val.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_garments_mom_val, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            #####################################################
            #monthly garment exports by volume with mom pct_change
            ######################################################
            fig_garments_mom_vol = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_garments_mom_vol.add_trace(go.Bar(x=df_garments['date'], 
                                y=df_garments['volume'], 
                                name="volume", 
                                text = df_garments["volume"],
                                textposition='auto',
                                texttemplate='%{text:,}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_garments_mom_vol.add_trace(go.Scatter(x=df_garments['date'], 
                                    y=df_garments['pct_change_volume'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_volume", 
                                    text=df_garments['pct_change_volume'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_garments_mom_vol.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_garments_mom_vol.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Garment Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_garments_mom_vol.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_garments_mom_vol.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_garments_mom_vol.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_garments_mom_vol.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_garments_mom_vol, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly garment exports by unit price with mom pct_change
            ######################################################
            fig_garments_mom_price = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_garments_mom_price.add_trace(go.Bar(x=df_garments['date'], 
                                y=df_garments['unit_price'], 
                                name="unit_price", 
                                text = df_garments["unit_price"],
                                textposition='auto',
                                texttemplate='$%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_garments_mom_price.add_trace(go.Scatter(x=df_garments['date'], 
                                    y=df_garments['pct_change_unit_price'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_unit_price", 
                                    text=df_garments['pct_change_unit_price'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_garments_mom_price.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_garments_mom_price.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Garment Exports by Unit Price",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$ Per Dozen",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_garments_mom_price.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_garments_mom_price.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_garments_mom_price.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_garments_mom_price.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_garments_mom_price, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly yarn exports by value with mom pct_change
            ######################################################
            fig_yarn_mom_val = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_yarn_mom_val.add_trace(go.Bar(x=df_yarn['date'], 
                                y=df_yarn['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_yarn["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_yarn_mom_val.add_trace(go.Scatter(x=df_yarn['date'], 
                                    y=df_yarn['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_yarn['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_yarn_mom_val.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_yarn_mom_val.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Yarn Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_yarn_mom_val.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_yarn_mom_val.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_yarn_mom_val.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_yarn_mom_val.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_yarn_mom_val, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            #####################################################
            #monthly yarn exports by volume with mom pct_change
            ######################################################
            fig_yarn_mom_vol = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_yarn_mom_vol.add_trace(go.Bar(x=df_yarn['date'], 
                                y=df_yarn['volume'], 
                                name="volume", 
                                text = df_yarn["volume"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_yarn_mom_vol.add_trace(go.Scatter(x=df_yarn['date'], 
                                    y=df_yarn['pct_change_volume'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_volume", 
                                    text=df_yarn['pct_change_volume'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_yarn_mom_vol.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_yarn_mom_vol.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Yarn Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Metric Tons",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_yarn_mom_vol.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_yarn_mom_vol.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_yarn_mom_vol.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_yarn_mom_vol.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_yarn_mom_vol, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly yarn exports by unit price with mom pct_change
            ######################################################
            fig_yarn_mom_price = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_yarn_mom_price.add_trace(go.Bar(x=df_yarn['date'], 
                                y=df_yarn['unit_price'], 
                                name="unit_price", 
                                text = df_yarn["unit_price"],
                                textposition='auto',
                                texttemplate='$%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_yarn_mom_price.add_trace(go.Scatter(x=df_yarn['date'], 
                                    y=df_yarn['pct_change_unit_price'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_unit_price", 
                                    text=df_yarn['pct_change_unit_price'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_yarn_mom_price.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_yarn_mom_price.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Yarn Exports by Unit Price",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$ Per Kg",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_yarn_mom_price.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_yarn_mom_price.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_yarn_mom_price.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_yarn_mom_price.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_yarn_mom_price, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly knitwear exports by value with mom pct_change
            ######################################################
            fig_knitwear_mom_val = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_knitwear_mom_val.add_trace(go.Bar(x=df_knitwear['date'], 
                                y=df_knitwear['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_knitwear["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_knitwear_mom_val.add_trace(go.Scatter(x=df_knitwear['date'], 
                                    y=df_knitwear['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_knitwear['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_knitwear_mom_val.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_knitwear_mom_val.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Knitwear Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_knitwear_mom_val.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_knitwear_mom_val.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_knitwear_mom_val.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_knitwear_mom_val.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_knitwear_mom_val, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            #####################################################
            #monthly knitwear exports by volume with mom pct_change
            ######################################################
            fig_knitwear_mom_vol = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_knitwear_mom_vol.add_trace(go.Bar(x=df_knitwear['date'], 
                                y=df_knitwear['volume'], 
                                name="volume", 
                                text = df_knitwear["volume"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_knitwear_mom_vol.add_trace(go.Scatter(x=df_knitwear['date'], 
                                    y=df_knitwear['pct_change_volume'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_volume", 
                                    text=df_knitwear['pct_change_volume'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_knitwear_mom_vol.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_knitwear_mom_vol.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Knitwear Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_knitwear_mom_vol.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_knitwear_mom_vol.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_knitwear_mom_vol.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_knitwear_mom_vol.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_knitwear_mom_vol, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly yarn exports by unit price with mom pct_change
            ######################################################
            fig_knitwear_mom_price = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_knitwear_mom_price.add_trace(go.Bar(x=df_knitwear['date'], 
                                y=df_knitwear['unit_price'], 
                                name="unit_price", 
                                text = df_knitwear["unit_price"],
                                textposition='auto',
                                texttemplate='$%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_knitwear_mom_price.add_trace(go.Scatter(x=df_knitwear['date'], 
                                    y=df_knitwear['pct_change_unit_price'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=8, color="Red"), 
                                    name="pct_change_unit_price", 
                                    text=df_knitwear['pct_change_unit_price'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_knitwear_mom_price.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_knitwear_mom_price.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Knitwear Exports by Unit Price",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$ Per Dozens",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_knitwear_mom_price.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_knitwear_mom_price.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_knitwear_mom_price.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_knitwear_mom_price.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_knitwear_mom_price, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly bedwear exports by value with mom pct_change
            ######################################################
            fig_bedwear_mom_val = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_bedwear_mom_val.add_trace(go.Bar(x=df_bedwear['date'], 
                                y=df_bedwear['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_bedwear["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_bedwear_mom_val.add_trace(go.Scatter(x=df_bedwear['date'], 
                                    y=df_bedwear['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_bedwear['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_bedwear_mom_val.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_bedwear_mom_val.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Bedwear Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_bedwear_mom_val.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_bedwear_mom_val.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_bedwear_mom_val.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_bedwear_mom_val.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_bedwear_mom_val, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            #####################################################
            #monthly Bedwear exports by volume with mom pct_change
            ######################################################
            fig_bedwear_mom_vol = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_bedwear_mom_vol.add_trace(go.Bar(x=df_bedwear['date'], 
                                y=df_bedwear['volume'], 
                                name="volume", 
                                text = df_bedwear["volume"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_bedwear_mom_vol.add_trace(go.Scatter(x=df_bedwear['date'], 
                                    y=df_bedwear['pct_change_volume'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_volume", 
                                    text=df_bedwear['pct_change_volume'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_bedwear_mom_vol.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_bedwear_mom_vol.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Bedwear Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Metric Tons",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_bedwear_mom_vol.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_bedwear_mom_vol.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_bedwear_mom_vol.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_bedwear_mom_vol.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_bedwear_mom_vol, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly Bedwear exports by unit price with mom pct_change
            ######################################################
            fig_bedwear_mom_price = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_bedwear_mom_price.add_trace(go.Bar(x=df_bedwear['date'], 
                                y=df_bedwear['unit_price'], 
                                name="unit_price", 
                                text = df_bedwear["unit_price"],
                                textposition='auto',
                                texttemplate='$%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_bedwear_mom_price.add_trace(go.Scatter(x=df_bedwear['date'], 
                                    y=df_bedwear['pct_change_unit_price'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=8, color="Red"), 
                                    name="pct_change_unit_price", 
                                    text=df_bedwear['pct_change_unit_price'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_bedwear_mom_price.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_bedwear_mom_price.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Bedwear Exports by Unit Price",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$ Per Kg",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_bedwear_mom_price.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_bedwear_mom_price.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_bedwear_mom_price.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_bedwear_mom_price.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_bedwear_mom_price, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly towels exports by value with mom pct_change
            ######################################################
            fig_towels_mom_val = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_towels_mom_val.add_trace(go.Bar(x=df_towels['date'], 
                                y=df_towels['Exports_US$'], 
                                name="Exports_US$", 
                                text = df_towels["Exports_US$"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_towels_mom_val.add_trace(go.Scatter(x=df_towels['date'], 
                                    y=df_towels['pct_change_value'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_value", 
                                    text=df_towels['pct_change_value'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_towels_mom_val.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_towels_mom_val.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Towels Exports by Value",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_towels_mom_val.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_towels_mom_val.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_towels_mom_val.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_towels_mom_val.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_towels_mom_val, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            #####################################################
            #monthly Towels exports by volume with mom pct_change
            ######################################################
            fig_towels_mom_vol = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_towels_mom_vol.add_trace(go.Bar(x=df_towels['date'], 
                                y=df_towels['volume'], 
                                name="volume", 
                                text = df_towels["volume"],
                                textposition='auto',
                                texttemplate='%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_towels_mom_vol.add_trace(go.Scatter(x=df_towels['date'], 
                                    y=df_towels['pct_change_volume'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=12, color="Red"), 
                                    name="pct_change_volume", 
                                    text=df_towels['pct_change_volume'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_towels_mom_vol.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_towels_mom_vol.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Towel Exports by Volume",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="Metric Tons",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_towels_mom_vol.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_towels_mom_vol.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_towels_mom_vol.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_towels_mom_vol.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_towels_mom_vol, use_container_width=True) # to show Figure; container width true makes fig. size responsive

            #####################################################
            #monthly Towels exports by unit price with mom pct_change
            ######################################################
            fig_towels_mom_price = make_subplots(specs=[[{'secondary_y': True}]], rows=1, cols=1) # to make subplot with 1 row and 1 col
            fig_towels_mom_price.add_trace(go.Bar(x=df_towels['date'], 
                                y=df_towels['unit_price'], 
                                name="unit_price", 
                                text = df_towels["unit_price"],
                                textposition='auto',
                                texttemplate='$%{text:.3s}', 
                                xperiod="M1",
                                xperiodalignment="middle",
                                ), row=1, col=1)
            fig_towels_mom_price.add_trace(go.Scatter(x=df_towels['date'], 
                                    y=df_towels['pct_change_unit_price'], 
                                    mode="lines+markers+text", 
                                    xperiod="M1",
                                    xperiodalignment="middle",
                                    marker=dict(size=8, color="Red"), 
                                    name="pct_change_unit_price", 
                                    text=df_towels['pct_change_unit_price'],
                                    textposition='top center',
                                    texttemplate="%{text:.0f}%",
                                    line=dict(color='Red', width=2, dash='dash'),
                                    hovertemplate='Month: %{x} <br>mom: %{y} %',
                                    ), row=1, col=1, secondary_y=True)
            fig_towels_mom_price.update_xaxes(
                rangeslider_visible = True,
                rangeslider_thickness = 0.1, #adjust rangeslider height
                rangeselector = dict(
                buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(count = 2, label = '2Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))
            fig_towels_mom_price.update_layout(
                autosize=True, height=700, width=1100,
                margin=dict(t=85, b=0, l=40, r=40),
                title="Monthly Pakistan Towel Exports by Unit Price",
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                xaxis_title='', yaxis_title="US$ Per Kg",
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=20, family="roboto, sans-serif"))
            fig_towels_mom_price.add_annotation(
                        text="Source: PBS/NTU",
                        xref="x domain", yref="y domain",
                        x=1, y=1.1, 
                        showarrow=False,
                        arrowhead=1)
            fig_towels_mom_price.update_yaxes(title_text="% change from same month last year", secondary_y=True)
            fig_towels_mom_price.update_xaxes(
                    tickangle = 90,
                    ticks="outside",
                    title_text = "",
                    tickformat="%b%y", #capital B and Y will give full name instead of short name of month & year
                    ticklabelmode="period",
                    dtick="M1", #distance between ticks is one month
                    title_font = {"size": 2},
                    title_standoff = 0)
            fig_towels_mom_price.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7
            ))

            st.plotly_chart(fig_towels_mom_price, use_container_width=True) # to show Figure; container width true makes fig. size responsive


            ####################################################

            ####################################################



            ##

            #df['year'] = df['year'].astype('string') #converting year column into streng for filtering 




            ##
            # tree plot



            fig_tree = px.treemap(df_2021, path=[px.Constant("category"), 'category'], values='Exports_US$',
                              color='category',
                              #color_continuous_scale='RdBu',
                              title="Pakistan Textile Exports by Category in the Current Year (Values in US$)",)

            fig_tree.update_layout(
                autosize=True, height=700, width=1100,
                title_font=dict(size=25, color='#111111', family="fjalla one, sans-serif"),
                plot_bgcolor='#ededed',
                paper_bgcolor='#ffffff',
                font=dict(color='#111111', size=18, family="roboto, sans-serif"),    #font of lablels of axises
            )
            fig_tree.data[0].textinfo = 'label+value+percent parent'

            #fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))

            #st.plotly_chart(fig_tree, use_container_width=True) # to show Figure; container width true makes fig. size responsive




