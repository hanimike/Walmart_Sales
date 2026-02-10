import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import scipy as sp

st.title("Walmart Sales")

    # Load Data
st.header("Load Data")
data = pd.read_csv("Walmart_Sales.csv")

csv = data.to_csv(index=False)
st.download_button( label="Download dataset as CSV", 
                   data=csv, file_name="Walmart_Sales.csv", mime="text/csv" )
     # Show Data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
st.dataframe(data)
    
    # Basic Info
st.header("Info")
st.write(data.info())

st.header("Shape")
st.write(data.shape)

st.header("Columns")
st.write(data.columns)

st.header("Describe")
st.write(data.describe())

st.header("Shape")
st.write(data.shape)

st.header("Head")
st.write(data.head(20))

st.header("Tails")
st.write(data.tail(10))

# # Convert Date column to datetime format 
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month 
data['Quarter'] = data['Date'].dt.quarter

st.subheader("unique stores in the dataset")
unique_stores = data['Store'].nunique()
st.write(f" There are {unique_stores} unique stores in the dataset.")

st.header("The date range covered by the dataset")
date_range_start = data['Date'].min() 
date_range_end = data['Date'].max() 
st.write(f"The dataset covers from {date_range_start.date()} to {date_range_end.date()}")

st.subheader("The highest total weekly sales across the entire period")
store_total_sales = data.groupby('Store')['Weekly_Sales'].sum() 
max_sales_store = store_total_sales.idxmax() 
max_sales_value = store_total_sales.max() 
st.write(f"Store {max_sales_store} had the highest total weekly sales of ${max_sales_value:,.2f}")

st.subheader("The average weekly sales for holiday weeks vs non-holiday weeks")
holiday_sales = data.groupby('Holiday_Flag')['Weekly_Sales'].mean() 
st.write(f"Average weekly sales for non-holiday weeks: ${holiday_sales[0]:,.2f}") 
st.write(f"Average weekly sales for holiday weeks: ${holiday_sales[1]:,.2f}") 

st.subheader("The highest average weekly sales store")
store_avg_sales = data.groupby('Store')['Weekly_Sales'].mean() 
max_avg_store = store_avg_sales.idxmax() 
max_avg_value = store_avg_sales.max() 
st.write(f"Store {max_avg_store} had the highest average weekly sales of ${max_avg_value:,.2f}") 

st.subheader("The correlation between Temperature and Weekly_Sales for each store separately")
correlations = {} 
for store in data['Store'].unique(): 
 store_data = data[data['Store'] == store] 
corr = store_data['Temperature'].corr(store_data['Weekly_Sales']) 
correlations[store] = corr
corr_df = pd.DataFrame(list(correlations.items()), columns=['Store', 'Correlation']) 
st.write(corr_df.sort_values('Correlation', ascending=False))

st.subheader("For each store, The month with the highest average sales")
store_month_sales = data.groupby(['Store', 'Month'])['Weekly_Sales'].mean().reset_index() 
idx = store_month_sales.groupby('Store')['Weekly_Sales'].idxmax() 
best_months = store_month_sales.loc[idx] 
st.write(best_months[['Store', 'Month', 'Weekly_Sales']])

st.subheader("The average Fuel_Price during holiday weeks compared to non-holiday weeks")
fuel_by_holiday = data.groupby('Holiday_Flag')['Fuel_Price'].mean() 
st.write(f" Average fuel price for non-holiday weeks: ${fuel_by_holiday[0]:.3f}") 
st.write(f"Average fuel price for holiday weeks: ${fuel_by_holiday[1]:.3f}")

st.header("The highest average unemployment rate")
store_unemployment = data.groupby('Store')['Unemployment'].mean() 
max_unemp_store = store_unemployment.idxmax() 
max_unemp_value = store_unemployment.max() 
st.write(f"Store {max_unemp_store} has the highest average unemployment rate of {max_unemp_value:.3f}%")

st.header("The maximum Weekly_Sales for each store") 
idx_max_sales = data.groupby('Store')['Weekly_Sales'].idxmax() 
max_sales_weeks = data.loc[idx_max_sales, ['Store', 'Date', 'Weekly_Sales']] 
st.write(max_sales_weeks.sort_values('Store'))

st.header("Total sales for each year in the dataset")
yearly_sales = data.groupby('Year')['Weekly_Sales'].sum().reset_index()
st.write(yearly_sales)
fig = px.bar( yearly_sales, x='Year', y='Weekly_Sales', text='Weekly_Sales', labels={'Weekly_Sales': 'Total Sales'}, title="Total Sales by Year" )
fig.update_traces(texttemplate='$%{text:,.2f}', textposition='outside') 
fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
st.plotly_chart(fig, use_container_width=True)

st.subheader("The quarter with the highest average sales")
store_quarter_sales = data.groupby(['Store', 'Quarter'])['Weekly_Sales'].mean().reset_index()
idx_q = store_quarter_sales.groupby('Store')['Weekly_Sales'].idxmax() 
best_quarters = store_quarter_sales.loc[idx_q]
st.subheader("Best Quarter by Store (Average Weekly Sales)") 
st.write(best_quarters[['Store', 'Quarter', 'Weekly_Sales']])
fig, ax = plt.subplots(figsize=(10, 6)) 
ax.bar(best_quarters['Store'], best_quarters['Weekly_Sales'], color='skyblue')
ax.set_xlabel("Store")
ax.set_ylabel("Average Weekly Sales") 
ax.set_title("Best Quarter Sales by Store")
ax.tick_params(axis='x', rotation=90) 
st.pyplot(fig)

st.subheader("The average CPI value for weeks where Weekly_Sales were above the overall median")
store_quarter_sales = data.groupby(['Store', 'Quarter'])['Weekly_Sales'].mean().reset_index()
idx_q = store_quarter_sales.groupby('Store')['Weekly_Sales'].idxmax() 
best_quarters = store_quarter_sales.loc[idx_q]
st.subheader("Best Quarter by Store (Average Weekly Sales)") 
st.write(best_quarters[['Store', 'Quarter', 'Weekly_Sales']])
fig = px.box(store_quarter_sales, x="Quarter", y="Weekly_Sales", color="Quarter", points="all", labels={"Weekly_Sales": "Average Weekly Sales"}, title="Distribution of Weekly Sales by Quarter" )
st.plotly_chart(fig, use_container_width=True)

st.subheader("The most consistent weekly sales (lowest standard deviation)")
store_std = data.groupby('Store')['Weekly_Sales'].std()
min_std_store = store_std.idxmin() 
min_std_value = store_std.min() 
max_std_store = store_std.idxmax() 
max_std_value = store_std.max()
st.subheader("Store Sales Consistency") 
st.success(f"Store {min_std_store} has the most consistent sales " 
           f"with std deviation of ${min_std_value:,.2f}")
st.error(f"Store {max_std_store} has the least consistent sales " 
         f"with std deviation of ${max_std_value:,.2f}")
store_std_df = store_std.reset_index() 
store_std_df.columns = ['Store', 'Std_Weekly_Sales']          
fig = px.bar( store_std_df, x='Store', y='Std_Weekly_Sales', text='Std_Weekly_Sales', labels={'Std_Weekly_Sales': 'Standard Deviation of Weekly Sales'}, title="Sales Consistency by Store" )
fig.update_traces(texttemplate='$%{text:,.2f}', textposition='outside') 
fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
st.plotly_chart(fig, use_container_width=True)
