import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="TaxiFareModel",
    page_icon="🚖",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("TaxiFareModel 🚖")

st.markdown("Predict your taxi fare in NYC")

st.write("""
This is a simple web app that predicts the taxi fare in NYC using the TaxiFareModel.
The model is trained on a dataset of taxi rides in NYC and uses various features such as pickup and dropoff locations, passenger count, and time of day to predict the fare.
""")

col1, col2 = st.columns(2)
with col1:
    st.header("Enter Ride Details")

    ride_date = st.date_input("Ride Date", datetime.today())
    ride_time = st.time_input("Ride Time", datetime.now().time())

    st.subheader("Pickup Location")
    pickup_longitude = st.number_input("Pickup Longitude", format="%.6f")
    pickup_latitude = st.number_input("Pickup Latitude", format="%.6f")

    st.subheader("Dropoff Location")
    dropoff_longitude = st.number_input("Dropoff Longitude", format="%.6f")
    dropoff_latitude = st.number_input("Dropoff Latitude", format="%.6f")

    st.subheader("Passenger Count")
    passenger_count = st.number_input("Number of Passengers", min_value=1, max_value=6, value=1)

with col2:
    st.header("Ride Map")
    map_data = pd.DataFrame({
        "lat": [40.7826],
        "lon": [-73.9656]
    })
    st.map(map_data, zoom=12)



if st.button("Predict Fare"):
    params = {
        'pickup_datetime': f'{ride_date} {ride_time}',
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }


    api_url = 'https://taxifare.lewagon.ai/predict'

    with st.spinner("Calling the API..."):
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                prediction = response.json().get('fare', 0)
                st.success(f"Predicted Fare: ${prediction:.2f}")
                st.write("#### Parameters used:")
                st.json(params)
            else:
                st.error("Failed to get a prediction. API returned status code: " + str(response.status_code))
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
