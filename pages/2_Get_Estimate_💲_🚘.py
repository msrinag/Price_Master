import streamlit as st
import pandas as pd
import pickle
import os
from xgboost import XGBRegressor

st.set_page_config(
    page_title="Price Master",
    page_icon=":car:"
)

# Function to map categorical data to numerical values
def map_data_to_model(data):
    insurance_mapping = {'Zero Dep':6,'Comprehensive': 5, 'First Party': 4, 'Second Party':3,'Third Party': 2, 'Not Available': 1}
    transition_mapping = {'Manual': 1, 'Automatic': 2}
    fuel_mapping = {'Petrol': 1, 'Diesel': 2, 'CNG': 3, 'LPG': 4, 'Electric': 5}
    body_mapping = {'Hatchback': 1, 'Sedan': 2, 'SUV': 3, 'MUV': 4, 'Minivans': 5, 'unknown_type': 6, 'Pickup': 7,'Coupe':8,'Convertibles':9}
    owner_mapping = {'First Owner':1, 'Second Owner':2, 'Third Owner':3, 'Fifth Owner':5, 'Fourth Owner':4}
    
    data['insurance_value'] = data['insurance_value'].map(insurance_mapping)
    data['transmission_type_value'] = data['transmission_type_value'].map(transition_mapping)
    data['fuel_type_value'] = data['fuel_type_value'].map(fuel_mapping)
    data['body_type_value'] = data['body_type_value'].map(body_mapping)
    data['owner_type_Value'] = data['owner_type_Value'].map(owner_mapping)
    nacheck(data)
    
    return data
    
    
def nacheck(df):
    na_mask = df.isna().any(axis=1)
    if na_mask.any():
    # Print the row numbers where missing values exist
        st.write("Recheck values for Rows: "+" ".join(map(str,na_mask[na_mask].index)))

# Load the trained model
with open('Resources/xgb_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Streamlit UI
st.title('Car Price Estimator')

# Input form
st.write('Enter Car Details to get Estimated price') 

col1, col2 = st.columns(2)
name = col1.text_input('Car Name')
owner_type = col2.selectbox('Owner Type', ['First Owner', 'Second Owner', 'Third Owner', 'Fifth Owner', 'Fourth Owner'])
registered_year = col1.number_input('Registered Year', value=2016,step=1,min_value=1900, max_value=2024)
engine_capacity = col2.number_input('Engine Capacity (cc)', value=814.0,step=100.0,min_value=50.0, max_value=100000.0)
kms_driven = col1.number_input('Kilometers Driven', value=68336.4,step=1000.0,min_value=0.0)
max_power = col2.number_input('Maximum Power (bhp)', value=55.0,step=1.0,min_value=1.0)
seats = col1.number_input('Number of Seats', value=5,step=1,min_value=1)
mileage = col2.number_input('Mileage', value=21.0,step=0.5,min_value=0.0)
insurance = col1.selectbox('Insurance', ['Zero Dep','Comprehensive', 'First Party', 'Second Party','Third Party', 'Not Available'])
transmission_type = col2.selectbox('Transmission Type', ['Manual', 'Automatic'])
fuel_type = col1.selectbox('Fuel Type', ['Petrol','Diesel', 'CNG', 'LPG', 'Electric'])
body_type = col2.selectbox('Body Type', ['Hatchback', 'Sedan','SUV', 'MUV','Minivans', 'unknown_type', 'Pickup','Coupe','Convertibles'])


# Button to get estimated price
if st.button('Get Price'):
    input_data = pd.DataFrame({
        'name': [name],
        'registered_year': [registered_year],
        'engine_capacity': [engine_capacity],
        'kms_driven': [kms_driven],
        'max_power': [max_power],
        'seats': [seats],
        'mileage':[mileage],
        'insurance_value': [insurance],
        'transmission_type_value': [transmission_type],
        'fuel_type_value': [fuel_type],
        'body_type_value': [body_type],
        'owner_type_Value': [owner_type]
    })

    # Map categorical data to numerical values
    input_data = map_data_to_model(input_data)
 
    df = input_data.loc[:, ~input_data.columns.isin(['name'])]
    # Make predictions
    predictions = loaded_model.predict(df)
    
    # Display estimated price
    st.success(f"Estimated Price: ₹ {predictions[0]:.2f}")
    
    
# Add sidebar heading
st.sidebar.header('Try Our Batch Estimator')

# Add file uploader for CSV file
csv_file = st.sidebar.file_uploader('Upload CSV File', type=['csv'])

# Function to add predicted price column to CSV file
def add_predicted_price(df):
    # Map categorical data to numerical values
    df = map_data_to_model(df)
    
    # Make predictions
    predictions = loaded_model.predict(df.drop(columns=['name']))
    
    # Add predicted price column to DataFrame
    df['Predicted Price'] = predictions
    
    return df

# Process CSV file and display predictions
if csv_file is not None:
    # Read CSV file into DataFrame
    df_upload = pd.read_csv(csv_file)
    
    # Add predicted price column
    df_upload_with_predictions = add_predicted_price(df_upload)
    
    
    # Display the filtered data
    user_friendly_names=['Name','Registered year','Engine capacity','Kms driven','Max power','Seats','Mileage','Insurance','Transmission type','Fuel type','Body Type','Owner_type_Value','Predicted Price']
    df_upload_with_predictions.rename(columns=dict(zip(df_upload_with_predictions.columns, user_friendly_names)), inplace=True)

    # Display DataFrame with predicted price
    st.write(df_upload_with_predictions)
    

    # Download button for updated CSV file
    st.sidebar.download_button(label='Download Predictions CSV', data=df_upload_with_predictions.to_csv(index=False), file_name='predictions.csv')
 
def generate_download_button():
    # Define the path to the sample template CSV file
    file_path = 'Resources/Price_Master_sample_template.csv'
    
    # Read the file data
    with open(file_path, 'rb') as f:
        st.sidebar.download_button(
        label='Download Sample Template',
        data=f.read(),
        file_name='Price_Master_Template.csv'
    )
    
  
st.sidebar.write(':car:\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')
generate_download_button()  






