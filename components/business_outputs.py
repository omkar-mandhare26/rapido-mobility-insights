import plotly.express as px
import pandas as pd

df = pd.read_csv("./dataset/final_dataset.csv")

def business_outputs(st):
    st.title("Business Outputs")
    st.write("---")

    # 1. Identify peak cancellation windows
    st.header("1. Identify Peak Concellation Windows")
    cancel_df = (
        df[df["booking_status"] == "Cancelled"]
        .groupby("hour_of_day")
        .size()
        .reset_index(name="cancel_count")
    )

    fig1 = px.bar(
        cancel_df,
        x="hour_of_day",
        y="cancel_count",
    )
    st.plotly_chart(fig1, width="stretch")
    st.write("---")

    # 2. Predict high-risk rides
    st.header("2. Predict high-risk rides")
    risk_df = (
        df
        .groupby(["traffic_level", "weather_condition"])["booking_status"]
        .apply(lambda x: (x == "Cancelled").mean())
        .reset_index(name="cancellation_rate")
    )

    fig2 = px.bar(
        risk_df,
        x="traffic_level",
        y="cancellation_rate",
        color="weather_condition",
        barmode="group",
    )

    st.plotly_chart(fig2, width="stretch")
    st.write("---")

    # 3. Driver allocation strategy
    st.header("3. Driver allocation strategy")
    driver_alloc_df = (
        df
        .groupby("hour_of_day")
        .agg(avg_wait_time=("avg_wait_time_min", "mean"))
        .reset_index()
    )

    fig3 = px.bar(
        driver_alloc_df,
        x="hour_of_day",
        y="avg_wait_time",
        title="Average Rider Wait Time by Hour"
    )

    st.plotly_chart(fig3, width="stretch")
    st.write("---")

    # 4. Estimate fare more accurately
    st.header("4. Estimate fare more accurately")
    fare_df = df.copy()
    fare_df["fare_error"] = fare_df["booking_value"] - fare_df["base_fare"]

    fig4 = px.histogram(
        fare_df,
        x="fare_error",
        nbins=50,
    )

    st.plotly_chart(fig4, width="stretch")
    st.write("---")

    # 5. Ops Decision-Making Signals
    st.header("5. Ops Decision-Making Signals")
    fig5 = px.density_heatmap(
        df,
        x="demand_level",
        y="booking_status",
        title="Demand Level vs Booking Status"
    )

    st.plotly_chart(fig5, width="stretch")
    st.write("---")
