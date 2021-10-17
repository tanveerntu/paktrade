import streamlit as st 
import plotly.express as px 
import pandas as pd 


st.set_page_config(page_title="Pakistan Textile Exports",
                   page_icon=":bar_chart:"   #https://www.webfx.com/tools/emoji-cheat-sheet/

)

st.title('TEXTILE & CLOTHING EXPORTS FROM PAKISTAN')
st.write("Source: Pakistan Bureau of Statistics")

# to load dataset from computer as df
df = pd.read_excel('monthly_textile_exports_pbs.xlsx')

# Get sum of values in a column 'Exports_US$'
# for those rows only where 'year' is '2020'


exports_2019 = df.loc[(df['year'].isin(['2019'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum() #filtering only '2019' rows in 'year' column & 'Monthly total' rows in 'category' column
exports_2020 = df.loc[(df['year'].isin(['2020'])) & (df['Category'].isin(['Monthly total'])), 'Exports_US$'].sum()
change = exports_2020-exports_2019



#Key metrics
kpi1, kpi2 = st.columns(2)
kpi1.metric(label = "Pak Textile & Clothing Exports in 2019", value = "${:,.0f}".format(exports_2019)) #0f means 0 decimal places
kpi2.metric(label = "Pak Textile & Clothing Exports in 2020", value = "${:,.0f}".format(exports_2020), delta = "{:,.0f}".format(change), delta_color='normal')


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

#fig_product_exports.update_traces(textposition='outside')

st.plotly_chart(fig_product_exports)

#show dataframe table
#st.dataframe(df)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


