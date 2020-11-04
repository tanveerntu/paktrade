
import streamlit as st
import pandas as pd
import requests
import plotly.express as px


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


response = requests.get(api_url)

data = response.content

with open('output.csv', 'wb') as output:
    output.write(data)
    df = pd.read_csv("output.csv")

st.title("Latest Pakistan Trade Statistics from UNComtrade Database")
st.write("Compiled by: National Textile Univeristy, Pakistan.")
#to filter values based on trade flow code
df_import = df[df['Trade Flow Code'] == 1]
df_export = df[df['Trade Flow Code'] == 2]

#to show dataframes
df_import.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False) #to sort values in descending order
df_export.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False)

df_import.reset_index(drop=True, inplace=True) #to reset index numbering of DF
df_export.reset_index(drop=True, inplace=True)

df_w = df[df['Partner'] == 'World'] #filtering only by partner 'world'

st.subheader("Trade Balance of Pakistan")

df_w.reset_index(drop=True, inplace=True)
st.table(df_w[['Year', 'Trade Flow', 'Trade Value (US$)']])
#bar chart
fig = px.bar(df_w, x='Trade Value (US$)',y='Trade Flow',orientation='h', text='Trade Value (US$)', width =900, height =600)
fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

#TEXTILE RELATED TRADE DATA
#to get hs code-wise data of all textile related HS codes
api_url2 = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&cc=52,53,54,55,56,57,58,59,60,61,62,63&ps=now&r=586&p=all&rg=all&cc=TOTAL&fmt=csv'

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

#excluding 'World' as partner

# create bar charts

st.subheader("Top 10 Importing Countries from Pakistan")
fig = px.bar(top10exp, x='Trade Value (US$)',y='Partner', orientation='h', text='Trade Value (US$)', width =900, height =600)
fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

st.subheader("Top 10 Exporting Countries to Pakistan")
fig = px.bar(top10imp, x='Trade Value (US$)',y='Partner',orientation='h', text='Trade Value (US$)', width =900, height =600)
fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)


import numpy as np

#For treeplots
st.subheader("Share of Exporting Countries to Pakistan (Values in US$)")
fig = px.treemap(dfi, path=[px.Constant(''), 'Partner'], values='Trade Value (US$)', width =900, height =600,
    hover_data=['Trade Value (US$)'])
fig.data[0].textinfo = 'label+text+value+percent entry'
st.plotly_chart(fig)

fig = px.pie(dfi, values='Trade Value (US$)', names='Partner')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig)

st.subheader("Share of Importing Countries from Pakistan (Values in US$)")
fig = px.treemap(dfe, path=[px.Constant(''), 'Partner'], values='Trade Value (US$)', width =900, height =600,
    hover_data=['Trade Value (US$)'])
fig.data[0].textinfo = 'label+text+value+percent entry'
st.plotly_chart(fig)

fig = px.pie(dfe, values='Trade Value (US$)', names='Partner')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig)

st.subheader("Textile & Clothing Exports from Pakistan")
df2_export.reset_index(drop=True, inplace=True)
st.table(df2_export[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']]) #shows df2_export selected columns

#treemap
st.subheader("Share of Textile & Clothing exports from Pakistan by Commodity Codes")

fig = px.treemap(df2_export, path=['Commodity Code'], values='Trade Value (US$)', width =900, height =600,
    hover_data=['Commodity'])
fig.data[0].textinfo = 'label+value+percent entry'
st.plotly_chart(fig)


#COMMODITY-WISE EXPORTS FROM PAKISTAN
api_url3 = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&ps=now&r=586&rg=2&fmt=csv'

response = requests.get(api_url3)
data = response.content
with open('output.csv', 'wb') as output:
    output.write(data)
    df3 = pd.read_csv("output.csv")
 

#to filter values based on trade flow code
df_hsexport = df3[df3['Trade Flow Code'] == 2][df3['Partner Code'] == 0]

#to show dataframes
df_hsexport.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False)

df_hsexport.reset_index(drop=True, inplace=True)

st.subheader("Share of all types of exports from Pakistan by Commodity Codes")

fig = px.treemap(df_hsexport, path=['Commodity Code'], values='Trade Value (US$)', width =900, height =600,
    hover_data=['Commodity'])
fig.data[0].textinfo = 'label+value+percent entry'
st.plotly_chart(fig)





#COMMODITY-WISE IMPORTS FROM PAKISTAN
api_url4 = 'https://comtrade.un.org/api/get?max=A&type=C&freq=A&px=HS&ps=now&r=586&rg=1&fmt=csv'

response = requests.get(api_url4)
data = response.content
with open('output.csv', 'wb') as output:
    output.write(data)
    df4 = pd.read_csv("output.csv")
 

#to filter values based on trade flow code
df_hsimport = df4[df4['Trade Flow Code'] == 1][df4['Partner Code'] == 0]

df_hsimport.sort_values(by=['Trade Value (US$)'], inplace=True, ascending=False) #to sort values in descending order

df_hsimport.reset_index(drop=True, inplace=True) #to reset index numbering of DF

st.subheader("Share of all types of imports to Pakistan by Commodity Codes")
fig = px.treemap(df_hsimport, path=['Commodity Code'], values='Trade Value (US$)', width =900, height =600,
    hover_data=['Commodity'])
fig.data[0].textinfo = 'label+value+percent entry'
st.plotly_chart(fig)



#TABLES


st.subheader("All types of Commodity-wise exports from Pakistan")
st.table(df_hsexport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])

st.subheader("All types of  Commodity-wise imports in Pakistan")
st.table(df_hsimport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])

st.subheader("Country-wise Total Exports of Pakistan, including all commodities")
st.table(df_export[['Year', 'Partner', 'Trade Value (US$)']])

st.subheader("Country-wise Total Imports of Pakistan, including all commodities")
st.table(df_import[['Year', 'Partner', 'Trade Value (US$)']])

