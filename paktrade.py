import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly
import plotly.express as px
import urllib.request
import openpyxl

# Use the full page instead of a narrow central column
st.set_page_config(layout='centered')

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
('Textile Trade Statistics', 'Overall Trade Statistics')
)

if option == 'Overall Trade Statistics': 

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



    #defining two columns

    #l1c1, l1c2 =st.beta_columns(2) #define two columns l1c1 (for line 1 column1) and l1c2

    st.subheader("Current Trade Balance of Pakistan")

    #bar chart
    fig = px.bar(df_w, x='Trade Value (US$)',y='Trade Flow',orientation='h', text='Trade Value (US$)', template="plotly_white")
    fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
    fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

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

    st.subheader("Pak Imports and Exports Over the Years")

    fig = px.line(df_all_years_export, x="Year", y="Trade Value (US$)", text="Trade Flow", template="plotly_white")
    fig.update_traces(mode='markers+lines')
    fig.update_xaxes(showgrid=False, 
                    ticks="outside",
                    tickson="boundaries",
                    ticklen=10)
    fig.update_yaxes(showgrid=True,
                    ticks="outside",
                    tickson="boundaries",
                    ticklen=10)
    # x axis line thickness and color
    fig.update_xaxes(showline=True,  
                    linewidth=2.5, 
                    linecolor='black')
    fig.add_bar(x=df_all_years_import["Year"],y=df_all_years_import["Trade Value (US$)"], name="Imports")
    st.plotly_chart(fig)

    #TEXTILE RELATED TRADE DATA
    #to get hs code-wise data of all textile related HS codes
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

    #excluding 'World' as partner

    # create bar charts

    st.subheader("Top 10 Importing Countries from Pakistan")
    fig = px.bar(top10exp, x='Trade Value (US$)',y='Partner', orientation='h', text='Trade Value (US$)', template="plotly_white")
    fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
    fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)


    st.subheader("Top 10 Exporting Countries to Pakistan")
    fig = px.bar(top10imp, x='Trade Value (US$)',y='Partner',orientation='h', text='Trade Value (US$)', template="plotly_white")
    fig.update_traces(texttemplate='%{text:$,.2}') #to format text on graphs
    fig.update_layout(template="seaborn", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

    ####
    import numpy as np

    #For treeplots
    st.subheader("Share of Exporting Countries to Pakistan (Values in US$)")
    fig = px.treemap(dfi, path=[px.Constant(''), 'Partner'], values='Trade Value (US$)', 
        hover_data=['Trade Value (US$)'])
    fig.data[0].textinfo = 'label+text+value+percent entry'
    st.plotly_chart(fig)

    st.subheader("Share of Exporting Countries to Pakistan (Values in US$)")
    fig = px.pie(dfi, values='Trade Value (US$)', names='Partner')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig)

    st.subheader("Share of Importing Countries from Pakistan (Values in US$)")
    fig = px.treemap(dfe, path=[px.Constant(''), 'Partner'], values='Trade Value (US$)', 
        hover_data=['Trade Value (US$)'])
    fig.data[0].textinfo = 'label+text+value+percent entry'
    st.plotly_chart(fig)


    st.subheader("Share of Importing Countries from Pakistan (Values in US$)")
    fig = px.pie(dfe, values='Trade Value (US$)', names='Partner')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
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
    fig = px.treemap(df_hsexport, path=['Commodity Code'], values='Trade Value (US$)', 
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
    fig = px.treemap(df_hsimport, path=['Commodity Code'], values='Trade Value (US$)', 
        hover_data=['Commodity'])
    fig.data[0].textinfo = 'label+value+percent entry'
    st.plotly_chart(fig)

    #treemap
    st.subheader("Share of Textile & Clothing exports from Pakistan by Commodity Codes")
    fig = px.treemap(df2_export, path=['Commodity Code'], values='Trade Value (US$)', 
        hover_data=['Commodity'])
    fig.data[0].textinfo = 'label+value+percent entry'
    st.plotly_chart(fig)


    st.subheader("Pie Chart of Textile & Clothing exports from Pakistan")
    fig = px.pie(df2_export, values='Trade Value (US$)', names='Commodity Code', hover_name="Commodity", labels={'Commodity':'Trade Value (US$)'}, hole=.3)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    st.plotly_chart(fig)
    #TABLES
    import plotly.figure_factory as ff

    st.subheader("Textile & Clothing Exports from Pakistan")
    df2_export.reset_index(drop=True, inplace=True)
    st.table(df2_export[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']]) #shows df2_export selected columns
    #fig =  ff.create_table(df2_export[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])
    #st.plotly_chart(fig)


    st.subheader("All types of Commodity-wise exports from Pakistan")
    st.table(df_hsexport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])
    #fig =  ff.create_table(df_hsexport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])
    #st.plotly_chart(fig)


    st.subheader("All types of  Commodity-wise imports in Pakistan")
    st.table(df_hsimport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])
    #fig =  ff.create_table(df_hsimport[['Year', 'Commodity Code', 'Commodity', 'Trade Value (US$)']])
    #st.plotly_chart(fig)


    st.subheader("Country-wise Total Exports of Pakistan, including all commodities")
    #st.table(df_export[['Year', 'Partner', 'Trade Value (US$)']])
    fig =  ff.create_table(df_export[['Year', 'Partner', 'Trade Value (US$)']])
    st.plotly_chart(fig)

    st.subheader("Country-wise Total Imports of Pakistan, including all commodities")
    #st.table(df_import[['Year', 'Partner', 'Trade Value (US$)']])


    fig =  ff.create_table(df_import[['Year', 'Partner', 'Trade Value (US$)']])
    st.plotly_chart(fig)

else:

    st.title('Textile & Clothing Exports')
    st.write("Source: Pakistan Bureau of Statistics/National Textile University, Pakistan")

    # to load dataset from computer as df
    df=pd.read_excel('monthly_textile_exports_pbs.xlsx', engine='openpyxl')

    # Get sum of values in a column 'Exports_US$'
    # for those rows only where 'year' is '2020'


    exports_2019 = df.loc[(df['year'].isin(['2019'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum() #filtering only '2019' rows in 'year' column & 'Monthly total' rows in 'category' column
    exports_2020 = df.loc[(df['year'].isin(['2020'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum()
    change_year = exports_2020-exports_2019
    change =(change_year / exports_2019)
    percentage_change = (change * 100)



    #Key metrics
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label = "Pak Textile & Clothing Exports in 2019", value = "${:,.0f}".format(exports_2019)) #0f means 0 decimal places
    kpi2.metric(label = "Pak Textile & Clothing Exports in 2020", value = "${:,.0f}".format(exports_2020), delta = "{:,.0f}".format(percentage_change)+' % change from last year', delta_color='normal')




    exports_sep_20 = df.loc[(df['month_year'].isin(['Sep, 20'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum() #filtering only '2019' rows in 'year' column & 'Monthly total' rows in 'category' column
    exports_sep_21 = df.loc[(df['month_year'].isin(['Sep, 21'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum()
    change_month = exports_sep_21-exports_sep_20
    change_m =(change_month / exports_sep_20)
    percentage_change_m = (change_m * 100)

    kpi3, kpi4 = st.columns(2)
    kpi3.metric(label = "September, 2020", value = "${:,.0f}".format(exports_sep_20)) #0f means 0 decimal places
    kpi4.metric(label = "September, 2021", value = "${:,.0f}".format(exports_sep_21), delta = "{:,.0f}".format(percentage_change_m)+' % change from same month of last year', delta_color='normal')


    # filter rows for monthly total
    st.subheader("Monthly Total Textile & Clothing Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Monthly total"])], x="month_year", y="Exports_US$", title="Monthly Total Textile & Clothing Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for cotton fiber
    st.subheader("Monthly raw cotton fiber Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Raw cotton"])], x="month_year", y="Exports_US$", title="Monthly raw cotton fiber Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for cotton fiber
    st.subheader("Monthly Exports of carded or combed cotton from Pakistan")
    fig = px.area(df[df["Category"].isin(["Ctn Crd/Cmd"])], x="month_year", y="Exports_US$", title="Monthly Exports of carded or combed cotton from Pakistan")
    st.plotly_chart(fig)

    # filter rows for cotton yarn
    st.subheader("Monthly Cotton Yarn Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Cotton Yarn"])], x="month_year", y="Exports_US$", title="Monthly Cotton Yarn Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for Non-cotton yarn
    st.subheader("Monthly Non-Cotton Yarn Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Non-cotton Yarn"])], x="month_year", y="Exports_US$", title="Monthly Non-Cotton Yarn Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for cotton cloth
    st.subheader("Monthly Cotton Cloth Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Cotton Cloth"])], x="month_year", y="Exports_US$", title="Monthly Cotton Cloth Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for garments
    st.subheader("Monthly Garments Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Garments"])], x="month_year", y="Exports_US$", title="Monthly Garments Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for knitwear
    st.subheader("Monthly Knitwear Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Knitwear"])], x="month_year", y="Exports_US$", title="Monthly Knitwear Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for bedwear
    st.subheader("Monthly Bedwear Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Bedwear"])], x="month_year", y="Exports_US$", title="Monthly Bedwear Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for towels
    st.subheader("Monthly Towels Exports from Pakistan")
    fig = px.area(df[df["Category"].isin(["Towels"])], x="month_year", y="Exports_US$", title="Monthly Towels Exports from Pakistan")
    st.plotly_chart(fig)

    # filter rows for tents, tarpaulines
    st.subheader("Monthly Exports of Tents & Tarpaulines from Pakistan")
    fig = px.area(df[df["Category"].isin(["Tents, Tarpaulines"])], x="month_year", y="Exports_US$", title="Monthly Exports of Tents & Tarpaulines from Pakistan")
    st.plotly_chart(fig)

    # filter rows for tents, tarpaulines
    st.subheader("Monthly Exports of Artificial Silk & Synthetics Textiles from Pakistan")
    fig = px.area(df[df["Category"].isin(["Art. Silk & Synth"])], x="month_year", y="Exports_US$", title="Monthly Exports of Artificial Silk & Synthetics Textiles from Pakistan")
    st.plotly_chart(fig)

    # filter rows for made-ups
    st.subheader("Monthly Madeups exports (excluding towels & beddwear) from Pakistan")
    fig = px.area(df[df["Category"].isin(["Madeups (excl. twl & Bdwr)"])], x="month_year", y="Exports_US$", title="Monthly Madeups exports (excluding towels & beddwear) from Pakistan")
    st.plotly_chart(fig)

    # filter rows for other textiles
    st.subheader("Monthly Exports of other textiles from Pakistan")
    fig = px.area(df[df["Category"].isin(["Other Textiles"])], x="month_year", y="Exports_US$", title="Monthly Exports of other textiles from Pakistan")
    st.plotly_chart(fig)


    df2= df[df.Category != 'Monthly total'] #droping "Monthly total" rows, in "Category"

    st.subheader("Break-up of Textile & Clothing Exports in 2021")
    fig = px.bar(df2[df2["year"].isin(["2021"])], x="Month", y="Exports_US$", color="Category", text="Exports_US$", title="Break-up of Textile & Clothing Exports in 2021")
    st.plotly_chart(fig)


    st.subheader("Exports Trends of Various Categories in 2021")
    fig = px.line(df2[df2["year"].isin(["2021"])], x="Month", y="Exports_US$", color="Category", text="Category", title="Export of different textile categories in 2021", template="plotly_white")
    fig.update_traces(mode='markers+lines')
    st.plotly_chart(fig)

    #treemap of 2020 data
    df_2020 = df[df["year"].isin(["2020"])] #filtering data on 2020 only
    df_2020_wo_total= df_2020[df_2020.Category != 'Monthly total'] #droping "Monthly total" rows, in "Category"
    df_2020_wo_total_sorted = (
        df_2020_wo_total.groupby(by=["Category"]).sum()[["Exports_US$"]].sort_values(by="Exports_US$")
    )   #sorting in descending order

    st.subheader("Textile exports of different categories in 2020")
    fig = px.treemap(df_2020_wo_total, path=['Category'], values='Exports_US$', title="Pakistani export of different textile categories in 2020. (Data source: Pakistan Bureau of Statistics)",
            hover_data=['Category'])
    fig.data[0].textinfo = 'label+value+percent entry'
    st.plotly_chart(fig)

    

    #bubble chart

    df_2020_grouped = df_2020_wo_total.groupby(by=["Category"]).sum()[["Exports_US$"]].sort_values(by="Exports_US$")
    fig = px.scatter(df_2020_grouped, y="Exports_US$", text = 'Exports_US$', size="Exports_US$")
    st.plotly_chart(fig)
    #fig_product_exports.update_traces(textposition='outside')
    
   
    #sorted bar chart
    fig_product_exports = px.bar(
        df_2020_wo_total_sorted,
        x="Exports_US$",
        y=df_2020_wo_total_sorted.index,
        orientation="h",
        text = 'Exports_US$',
        title="<b>Textile exports by Product Line in 2020</b>",
        color_discrete_sequence=["#0083B8"] * len(df_2020_wo_total_sorted),
        template="plotly_white",
    )
    st.plotly_chart(fig_product_exports)
    #show dataframe table
    #st.dataframe(df)






