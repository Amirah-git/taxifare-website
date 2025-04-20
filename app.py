import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NYC Taxi Fare Predictor", page_icon="🚖", layout="centered")

st.title("🚖 NYC Taxi Fare Predictor")


st.markdown("Enter the details of your ride to get an estimated fare.")

st.sidebar.header("Ride Details")

ride_date = st.sidebar.date_input("Date", datetime.today())
ride_time = st.sidebar.time_input("Time", datetime.now().time())

pickup_lat = st.sidebar.number_input("Pickup Latitude", value=40.7614327, format="%.6f")
pickup_lon = st.sidebar.number_input("Pickup Longitude", value=-73.9798156, format="%.6f")

dropoff_lat = st.sidebar.number_input("Drop-off Latitude", value=40.6413111, format="%.6f")
dropoff_lon = st.sidebar.number_input("Drop-off Longitude", value=-73.7781391, format="%.6f")

passenger_count = st.sidebar.number_input("Passenger Count", min_value=1, max_value=6, value=1, step=1)

pickup_datetime = f"{ride_date} {ride_time}"

if st.sidebar.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }

    api_url = "https://taxifare.lewagon.ai/predict"

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        fare = response.json().get("fare", "N/A")
        st.success(f"Estimated Fare: ${fare:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching prediction: {e}")

# Display map with pickup and drop-off points
st.subheader("Ride Map")
map_data = pd.DataFrame({
    "lat": [pickup_lat, dropoff_lat],
    "lon": [pickup_lon, dropoff_lon]
})
st.map(map_data, zoom=11)
