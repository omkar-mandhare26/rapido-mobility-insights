import plotly.express as px
import pandas as pd
import math 

df = pd.read_csv("./dataset/final_dataset.csv")

def visualization_outputs(st): 
    st.title("Visualization Outputs")
    st.write("---")
    
    with st.expander("1. Pickup vs Drop Location Heatmap"):
        city_list = sorted(df["city"].unique())
        selected_city = st.selectbox("Select city", options=city_list)

        pickup_drop = (
            df[df["city"] == selected_city]
            .groupby(["pickup_location", "drop_location"])
            .size()
            .reset_index(name="ride_count")
        )

        pickup_locations = sorted(pickup_drop["pickup_location"].unique())

        mid = math.ceil(len(pickup_locations) / 2)
        first_half = pickup_locations[:mid]
        second_half = pickup_locations[mid:]

        df_1 = pickup_drop[pickup_drop["pickup_location"].isin(first_half)]
        df_2 = pickup_drop[pickup_drop["pickup_location"].isin(second_half)]

        fig1 = px.density_heatmap(
            df_1,
            x="pickup_location",
            y="drop_location",
            z="ride_count",
            color_continuous_scale="Blues",
            title=f"Pickup vs Drop Heatmap — {selected_city}"
        ).update_layout(
            xaxis_title="Pickup Location",
            yaxis_title="Drop Location"
        )

        fig2 = px.density_heatmap(
            df_2,
            x="pickup_location",
            y="drop_location",
            z="ride_count",
            color_continuous_scale="Blues",
            title=f"Pickup vs Drop Heatmap — {selected_city}"
        ).update_layout(
            xaxis_title="Pickup Location",
            yaxis_title="Drop Location"
        )

        st.plotly_chart(fig1, width="stretch")
        st.plotly_chart(fig2, width="stretch")



    with st.expander("2. Cancellations by Hour of Day"):
        cancel_hour = df[["hour_of_day", "city"]][df["booking_status"] == "Cancelled"]

        fig = px.histogram(
            cancel_hour,
            x="hour_of_day",
            color="city",
            barmode="group",
            title="Cancellations by Hour"
        )
        st.plotly_chart(fig, width="stretch")

    with st.expander("3. Surge Multiplier Behavior Patterns"):
        surge_hour = (
            df.groupby(["hour_of_day", "demand_level"])["surge_multiplier"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            surge_hour,
            x="hour_of_day",
            y="surge_multiplier",
            color="demand_level",
            markers=True,
            title="Average Surge Multiplier by Hour and Demand Level"
        )

        st.plotly_chart(fig, use_container_width=True)

    with st.expander("4. Customer vs Driver Cancellation / Incompletion Reasons"):
        base_df = df[df["booking_status"] != "Completed"]

        customer_reasons = (
            base_df[base_df["customer_cancel_flag"] == 1]
            .groupby("incomplete_ride_reason")
            .size()
            .reset_index(name="count")
            .assign(actor_type="Customer")
        )

        driver_reasons = (
            base_df[base_df["driver_delay_flag"] == 1]
            .groupby("incomplete_ride_reason")
            .size()
            .reset_index(name="count")
            .assign(actor_type="Driver")
        )

        reason_compare = pd.concat([customer_reasons, driver_reasons])

        fig = px.bar(
            reason_compare,
            x="incomplete_ride_reason",
            y="count",
            color="actor_type",
            barmode="group",
            title="Cancellation / Incompletion Reasons: Customer vs Driver"
        )

        st.plotly_chart(fig, use_container_width=True)
