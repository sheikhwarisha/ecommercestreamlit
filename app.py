import streamlit as st #streamlit - Front end framework
import pandas as pd #data wrangling library in python
import plotly.express as px #Dynamic Visualization library in python


st.title("E-commerce Sales analysis Dashboard")

# data=pd.read_csv("supermarket_sales.csv")

# st.dataframe(data)


def load_data(file_path):
    data=pd.read_csv(file_path)
    
    data["Region"]=data["Region"].replace("East","South")
    data["Region"]=data["Region"].replace("South","West")
    data["Region"]=data["Region"].replace("West","East")
    return data

data_path="./ecommerce.csv"

data= load_data(data_path)
st.sidebar.header("Filters")




select_year=st.sidebar.multiselect("Select Year",options=data["Year"].unique())
select_category=st.sidebar.multiselect("Select Category",options=data["Category"].unique())
select_productname=st.sidebar.multiselect("Select Product Name",options=data["Product Name"].unique())
select_customername=st.sidebar.multiselect("Select Customer Name",options=data["Customer Name"].unique())

filtered_data= data[(data["Year"].isin(select_year)) & (data["Category"].isin(select_category)) & (data["Product Name"].isin(select_productname)) & (data["Customer Name"].isin(select_customername))]

st.dataframe(filtered_data)

total_sales=filtered_data["Sales"].sum().round(2)
total_quantity=filtered_data["Quantity"].sum().round(2)
total_discount=filtered_data["Discount"].sum().round(2)
profit=filtered_data["Profit"].sum().round(2)
region=filtered_data["Region"].nunique()
ord_id=filtered_data["Order ID"].nunique()

st.subheader("Key Metrics")

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.metric(label="Total Sales",value=total_sales)

with col2:
    st.metric(label="Total Quantity",value=total_quantity)

with col3:
    st.metric(label="Total Discount",value=total_discount)

with col4:  
    st.metric(label="Profit",value=profit)

with col5:
    st.metric(label="Region",value=region)

with col6:
    st.metric(label="Order Id",value=ord_id)


col7,col8=st.columns(2)

sales_by_country=filtered_data.groupby("Country")["Sales"].sum().sort_values().reset_index()
with col7:
    fig_country = px.bar(
    sales_by_country,
    x="Country",
    y="Sales",
    title="Total Sales By Country",
    text="Sales",
    color="Country"
    )
    st.plotly_chart(fig_country)
sales_by_region=filtered_data.groupby("Region")["Sales"].sum().sort_values().reset_index()
with col8:
    fig_region = px.bar(
    sales_by_region,
    x="Region",
    y="Sales",
    text="Sales",
    color="Region"
    )
    st.plotly_chart(fig_region)
sales_by_city = filtered_data.groupby("City")["Sales"].sum().sort_values().reset_index()

fig_city_pie = px.pie(
    sales_by_city,
    values="Sales",
    names="City",
    title="Sales Distribution by City",
    hole=0.4  
)

st.plotly_chart(fig_city_pie, use_container_width=True)