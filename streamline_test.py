#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[7]:


#read the file
df = pd.read_excel(io='supermarkt_sales.xlsx',engine='openpyxl',skiprows=3,usecols='B:R',nrows=1000)


# In[5]:


#web page config
st.set_page_config(page_title='Sale dashboard',page_icon=':bar_chart:',layout='wide')


# In[8]:

#
# st.dataframe(df)

#Side bar
st.sidebar.header("Please filter here")
city = st.sidebar.multiselect(
    "select the city",
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "select the Customer_type",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "select the Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

#filter using query mthod
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender "
)
# st.dataframe(df_selection)

#main page
st.title(':bar_chart: Sale Dahsboard')
st.markdown('##')

#KPI Top
Total_sale = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(),1)
star_rating = ":star:"*int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column,center_column,right_column = st.columns(3)
with left_column:
    st.subheader('Total Sales')
    st.subheader(f"US $ {Total_sale:,}")
with center_column:
    st.subheader('Rating')
    st.subheader(f"{average_rating}{star_rating}")
with right_column:
    st.subheader('Average Sales')
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

#sale product bar chart
sales_by_product_line = df_selection.groupby(by=['Product line'])[['Total']].sum().sort_values(by='Total')

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
st.plotly_chart(fig_product_sales)
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )


