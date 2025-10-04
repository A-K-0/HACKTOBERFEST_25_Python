import pandas as pd
import pickle as pk
import streamlit as st

# Load the trained model using raw string to avoid backslash issues
model = pk.load(open('model/bangalore_home_prices_model.pickle', 'rb'))


# Set the header of the web app
st.header('🏠 Banglore House Prices Predictor')

# Load the cleaned dataset
data = pd.read_csv(r'C:\Users\DELL\Desktop\houseprediction\Cleaned_data.csv')

# UI Inputs
loc = st.selectbox('📍 Choose the location', data['location'].unique())
sqft = st.number_input('📐 Enter total square feet:', min_value=100.0, max_value=10000.0, step=10.0)
beds = st.number_input('🛏️ Enter number of bedrooms:', min_value=1, max_value=10, step=1)
bath = st.number_input('🛁 Enter number of bathrooms:', min_value=1, max_value=10, step=1)
balc = st.number_input('🚪 Enter number of balconies:', min_value=0, max_value=5, step=1)

# Prepare the input DataFrame
input_df = pd.DataFrame({
    'location': [loc],
    'total_sqft': [sqft],
    'bath': [bath],
    'balcony': [balc],
    'bedrooms': [beds]
})

# Predict the price when the button is clicked
if st.button('💰 Predict Price'):
    try:
        prediction = model.predict(input_df)
        st.success(f"🏷️ Predicted price of the house is ₹{prediction[0] * 100000:,.2f}")
    except Exception as e:
        st.error(f"❌ Prediction failed. Reason: {str(e)}")
