import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data = pd.read_csv('Resources/car_resale_prices_cleaned.csv')
    return data

df = load_data()

# Sidebar filters
st.sidebar.header('Filters')
selected_city = st.sidebar.selectbox('City', ['All'] + list(df['city'].unique()))
selected_body_type = st.sidebar.selectbox('Body Type', ['All'] + list(df['body_type'].unique()))
selected_fuel_type = st.sidebar.selectbox('Fuel Type', ['All'] + list(df['fuel_type'].unique()))

# Filtering the data
if selected_city != 'All':
    df = df[df['city'] == selected_city]
if selected_body_type != 'All':
    df = df[df['body_type'] == selected_body_type]
if selected_fuel_type != 'All':
    df = df[df['fuel_type'] == selected_fuel_type]

# Display the filtered data
st.subheader('Filtered Cars')
st.write(df)
