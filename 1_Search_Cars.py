import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Price Master",
    page_icon=":car:"
)
@st.cache_data
def load_data():
    data = pd.read_csv('Resources/car_resale_prices_cleaned.csv')
    return data

df = load_data()

# Sidebar filters
# Sorting options
sort_options = {
    'Price: Low to High': 'resale_price',
    'Price: High to Low': 'resale_price',
    'Miles: Low to High': 'kms_driven',
    'Miles: High to Low': 'kms_driven',
    'Oldest': 'registered_year',
    'Newest': 'registered_year'
}

st.sidebar.header('Filters')
selected_sort_option = st.sidebar.selectbox('Sort by', list(sort_options.keys()))

# Sorting the data
sort_column = sort_options[selected_sort_option]
if 'Low to High' in selected_sort_option:
    df = df.sort_values(by=sort_column)
else:
    df = df.sort_values(by=sort_column, ascending=False)

selected_city = st.sidebar.multiselect('City',list(df['city'].unique()))
selected_body_type = st.sidebar.multiselect('Body Type',list(df['body_type'].unique()))
selected_fuel_type = st.sidebar.multiselect('Fuel Type',list(df['fuel_type'].unique()))
selected_insurance_type = st.sidebar.multiselect('Insurance Type', list(df['insurance'].unique()))
selected_transmission_type = st.sidebar.multiselect('Transmission Type', list(df['transmission_type'].unique()))
selected_owner_type = st.sidebar.multiselect('Owner Type', list(df['owner_type'].unique()))


# Filtering the data
if selected_city:
    df = df[df['city'].isin(selected_city)]
if selected_body_type:
    df = df[df['body_type'].isin(selected_body_type)]
if selected_fuel_type:
    df = df[df['fuel_type'].isin(selected_fuel_type)] 
if selected_insurance_type:
    df = df[df['insurance'].isin(selected_insurance_type)]
if selected_transmission_type:
    df = df[df['transmission_type'].isin(selected_transmission_type)]
if selected_owner_type:
    df = df[df['owner_type'].isin(selected_owner_type)]
    

    
    

# Display the filtered data
st.subheader('Filtered Cars')


price_range = st.slider('Price Range (₹)', min_value=int(df['resale_price'].min()), max_value=int(df['resale_price'].max()), value=(int(df['resale_price'].min()), int(df['resale_price'].max())))
col1, col2 = st.columns(2)
seats_range = col1.slider('Number of Seats', min_value=int(df['seats'].min()), max_value=int(df['seats'].max()), value= int(df['seats'].min()))
year_range = col2.slider('Registered Year Range', min_value=int(df['registered_year'].min()), max_value=int(df['registered_year'].max()), value=(int(df['registered_year'].min()), int(df['registered_year'].max())))
engine_capacity_range = col1.slider('Engine Capacity Range', min_value=int(df['engine_capacity'].min()), max_value=int(df['engine_capacity'].max()), value=(int(df['engine_capacity'].min()), int(df['engine_capacity'].max())))
km_driven_range = col2.slider('Kilometers Driven Range', min_value=int(df['kms_driven'].min()), max_value=int(df['kms_driven'].max()), value=(int(df['kms_driven'].min()), int(df['kms_driven'].max())))
max_power_range = col1.slider('Max Power Range', min_value=int(df['max_power'].min()), max_value=int(df['max_power'].max()), value=(int(df['max_power'].min()), int(df['max_power'].max())))
mileage_range = col2.slider('Mileage Range', min_value=int(df['mileage'].min()), max_value=int(df['mileage'].max()), value=(int(df['mileage'].min()), int(df['mileage'].max())))

df = df[(df['resale_price'] >= price_range[0]) & (df['resale_price'] <= price_range[1])]
df = df[(df['seats'] >= seats_range) ]
df = df[(df['registered_year'] >= year_range[0]) & (df['registered_year'] <= year_range[1])]
df = df[(df['engine_capacity'] >= engine_capacity_range[0]) & (df['engine_capacity'] <= engine_capacity_range[1])]
df = df[(df['kms_driven'] >= km_driven_range[0]) & (df['kms_driven'] <= km_driven_range[1])]
df = df[(df['max_power'] >= max_power_range[0]) & (df['max_power'] <= max_power_range[1])]
df = df[(df['mileage'] >= mileage_range[0]) & (df['mileage'] <= mileage_range[1])]

# Pagination
page_size = 10  # Number of items per page
total_items = len(df)
total_pages = (total_items - 1) // page_size + 1 if total_items > 0 else 1
current_page = st.number_input('Page', min_value=1, max_value=total_pages, value=1)

start_idx = (current_page - 1) * page_size
end_idx = min(start_idx + page_size, total_items)

# Display the data for the current page
# Exclude specific columns from the DataFrame
columns_to_exclude = ['insurance_value', 'transmission_type_value','fuel_type_value','body_type_value','owner_type_Value']  # Add the column names you want to exclude
df_filtered = df.drop(columns=columns_to_exclude)

# Display the filtered data

st.write(df_filtered.iloc[start_idx:end_idx],index=False)
st.write(f'Page {current_page} of {total_pages}')


