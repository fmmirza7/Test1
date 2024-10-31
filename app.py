import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import pandas as pd
import numpy as np

import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import yfinance as yf

# Specify title and logo for the webpage.
# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar
st.sidebar.title("Input")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()

# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date',value=datetime.date(2024,1,1))
with col2:
    edate = st.date_input('End Date',value=datetime.date.today())

st.title(f"{symbol}")

stock = yf.Ticker(symbol)
if stock is not None:
  # Display company's basics
  st.write(f"# Sector : {stock.info['sector']}")
  st.write(f"# Company Beta : {stock.info['beta']}")
  st.write(f"# Price : {stock.info['currentPrice']}")
else:
  st.error("Failed to fetch historical data.")

from datetime import datetime

start_date = st.slider("Data from:", value = datetime(2020, 1, 1), format = "DD/MM/YYYY")
st.write("Start Date:", start_date)

end_date = st.slider("To:", value = datetime(2023, 1, 1), format = "DD/MM/YYYY")
st.write("End Date:", end_date)

data = yf.download(symbol,start=start_date,end=end_date)

if data is not None:

  st.write(data.describe())
  chart_data = pd.DataFrame((data['Close']))
  st.area_chart(chart_data)

else:
  st.error("Failed to fetch historical data.")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df(data)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="Data.csv",
    mime="text/csv")
