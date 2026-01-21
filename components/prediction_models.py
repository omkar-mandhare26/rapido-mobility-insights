from datetime import date
import streamlit as st
import pandas as pd
import pickle
import joblib
import os

@st.cache_resource
def load_artifacts():
    df = pd.read_csv("./dataset/final_dataset.csv")

    # Importing Ride outcome prediction model & encoder
    ride_outcome_ordinal_encoder = joblib.load("./encoders/ride_outcome_ordinal_encoder.joblib")
    with open("./models/ride_outcome_prediction_model.pkl", "rb") as f:
        ride_outcome_prediction_model = pickle.load(f)
    
    # Importing Fare prediction model & encoder
    fare_prediction_ordinal_encoder = joblib.load("./encoders/fare_prediction_ordinal_encoder.joblib")
    with open("./models/fare_prediction_model.pkl", "rb") as f:
        fare_prediction_model = pickle.load(f)
    
    # Importing Customer cancellation risk model & encoder
    customer_cancellation_risk_ordinal_encoder = joblib.load("./encoders/customer_cancellation_risk_ordinal_encoder.joblib")
    with open("./models/customer_cancellation_risk_model.pkl", "rb") as f:
        customer_cancellation_risk_model = pickle.load(f)
    
    # Importing Driver delay prediction model & encoder
    driver_delay_ordinal_encoder = joblib.load("./encoders/driver_delay_ordinal_encoder.joblib")
    with open("./models/driver_delay_prediction_model.pkl", "rb") as f:
        driver_delay_prediction_model = pickle.load(f)

    return df, {
        "Ride Outcome Prediction Model" : {"encoder": ride_outcome_ordinal_encoder, "model": ride_outcome_prediction_model},
        "Fare Prediction Model": {"encoder": fare_prediction_ordinal_encoder, "model": fare_prediction_model},
        "Customer Cancellation Risk Model": {"encoder": customer_cancellation_risk_ordinal_encoder, "model": customer_cancellation_risk_model},
        "Driver Delay Prediction Model": {"encoder": driver_delay_ordinal_encoder, "model": driver_delay_prediction_model}
    }

df, models_data = load_artifacts()

def prediction_models():
    st.header("Prediction Models")
    st.write("---")

    selected_model = st.radio("Select which prediction you want", options=["Ride Outcome Prediction Model", "Fare Prediction Model", "Customer Cancellation Risk Model", "Driver Delay Prediction Model"])

    st.header(f"Selected Model: {selected_model}")
    st.write("---")

    with st.expander("Please fill booking information"):
        # Date & time inputs
        selected_date = st.date_input(
            "Select booking date",
            value=date(2025, 1, 1), 
            min_value=date(2025, 1, 1),
            max_value=date(2025, 12, 31)
        )
        month = selected_date.month
        day = selected_date.day
        day_of_week = selected_date.strftime("%A")
        is_weekend = int(selected_date.weekday() >= 5)

        hour_of_day = st.selectbox("Select hour", list(range(24)))
        minutes = st.selectbox("Select minute", list(range(60)))

        # Vehicle type inputs
        vehicle_type = st.selectbox("Select vehicle type", sorted(df["vehicle_type"].unique()))

        # City, Pickup & drop location inputs
        city = st.selectbox("Choose city", sorted(df["city"].unique()))
        pickup_location = st.selectbox("Choose pickup location", sorted(df["pickup_location"].unique()))
        drop_location = st.selectbox("Choose drop location", sorted(df["drop_location"].unique()))

        # Ride distance km inputs
        filter_df = df.query(f"pickup_location == '{pickup_location}' and drop_location == '{drop_location}' and vehicle_type == '{vehicle_type}'")
        ride_distance_km = st.slider(
            "Select approx distance",
            min_value= filter_df["ride_distance_km"].min(),
            max_value= filter_df["ride_distance_km"].max(),
            value=  filter_df["ride_distance_km"].mean()
        )

        # Conditions and pricing inputs
        traffic_level = st.selectbox("Select traffic level", sorted(df["traffic_level"].unique()))
        weather_condition = st.selectbox("Select traffic level", sorted(df["weather_condition"].unique()))
        rush_hour_flag = st.radio("Select Rush hour",options=[1,0])

        if selected_model != "Fare Prediction Model":
            base_fare = st.number_input("Enter base fare", min_value=0, step=1)
            surge_multiplier = st.number_input("Enter surge multiplier", min_value=0.0, step=0.05)
            fare_per_km = round((base_fare * surge_multiplier) / ride_distance_km, 4)

    with st.expander("Please fill customer information"):
        # Basics customer inputs
        customer_gender = st.selectbox("Select customer gender", ["Male", "Female", "Non-Binary"])
        customer_age = st.number_input("Enter customer age", min_value=0, step=1)
        customer_city = st.selectbox("Select customer city", sorted(df["customer_city"].unique()))

        # meta data of customer
        preferred_vehicle_type = st.selectbox("Select customer preferred vehicle", sorted(df["preferred_vehicle_type"].unique()))
        customer_signup_days_ago = st.number_input("Enter customer signup days ago", min_value=0, step=1)
        customer_total_bookings = st.number_input("Enter customer total bookings", min_value=0, step=1)
        customer_cancelled_rides = st.number_input("Enter customer cancelled rides", min_value=0, step=1)
        customer_incomplete_rides = st.number_input("Enter customer incomplete rides", min_value=0, step=1)
        avg_customer_rating = st.number_input("Enter average customer rating", min_value=0.0, step=0.1)
        customer_cancel_flag = st.radio("Select customer cancel flag",options=[1,0])

    with st.expander("Please fill driver information"):
        driver_age = st.number_input("Enter driver age", min_value=0, step=1)
        driver_city = st.selectbox("Select driver city", sorted(df["driver_city"].unique()))
        driver_vehicle_type = st.selectbox("Select driver vehicle type", sorted(df["driver_vehicle_type"].unique()))
        driver_experience_years = st.number_input("Enter driver experience years", min_value=0, step=1)
        total_assigned_rides = st.number_input("Enter driver total assigned rides", min_value=0, step=1)
        driver_incomplete_rides = st.number_input("Enter driver incompleted rides", min_value=0, step=1)
        
        if selected_model != "Driver Delay Prediction Model":
            delay_count = st.number_input("Enter driver delay count", min_value=0, step=1)
        
        acceptance_rate = st.number_input("Enter driver acceptance rate", min_value=0.0, step=0.1)
        avg_driver_rating = st.number_input("Enter driver average rating", min_value=0.0, step=0.1)
        avg_pickup_delay_min = st.number_input("Enter driver average pickup delay in minutes", min_value=0.0, step=0.1)
        if selected_model != "Driver Delay Prediction Model":
            driver_delay_flag = st.radio("Select driver delay flag", options=[1,0])

    with st.expander("Please fill location demand information"):
        total_requests = st.number_input("Enter total requests", min_value=0, step=1)
        
        if selected_model != "Driver Delay Prediction Model":
            location_completed_rides = st.number_input("Enter location completed rides", min_value=0, step=1)

        location_cancelled_rides = st.number_input("Enter location cancelled rides", min_value=0, step=1)
        avg_wait_time_min = st.number_input("Enter average wait time minutes", min_value=0, step=1)

        if selected_model != "Fare Prediction Model":
            avg_surge_multiplier = st.number_input("Enter average surge multiplier", min_value=0.0, step=0.1)

        demand_level = st.selectbox("Select demand level", sorted(df["demand_level"].unique()))

    if st.button("Predict"):      
        encoder = models_data[selected_model]["encoder"]
        model = models_data[selected_model]["model"]

        input_df = pd.DataFrame([locals()]).reindex(
            columns=model.feature_names_in_
        )
        string_columns = input_df.select_dtypes(include='object').columns
        input_df[string_columns] = encoder.transform(input_df[string_columns])

        prediction = model.predict(input_df)[0]
        st.write(f"Model Prediction Value: {prediction}")

        if selected_model == "Ride Outcome Prediction Model":
            pred_message = {0 : "Cancelled", 1 : "Completed", 2 : "Incomplete"}
            st.header(f"Ride will be {pred_message[prediction]}")
        elif selected_model == "Fare Prediction Model": 
            prediction = round(float(prediction), 2)
            st.header(f"Fare for the ride will be {prediction}")
        elif selected_model == "Customer Cancellation Risk Model":
            pred_message = {0: "Completed", 1 : "Cancelled"}
            st.header(f"Customer will {pred_message[prediction]} ride")
        elif selected_model == "Driver Delay Prediction Model":
            if prediction == 0: pred_message = "Driver will not delay the ride"
            elif prediction == 1: pred_message = "Driver will delay the ride"
            st.header(f"{pred_message}")