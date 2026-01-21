import plotly.express as px
import pandas as pd

df = pd.read_csv("./dataset/final_dataset.csv")

def dashboard(st): 
    st.title("Dashboard")
    st.write("---")
    
    with st.expander("1. Ride volume by hour, weekday, city"):
        filter_options_dict = {
            "Hour": "hour_of_day",
            "Weekday": "day_of_week",
        }
        filter_option = st.selectbox("Filter by", filter_options_dict.keys())
        
        fig = px.histogram(
            df[[filter_options_dict[filter_option],"city"]],
            x=filter_options_dict[filter_option],
            color="city",
            barmode="group",
        )

        if filter_option == "Hour":
            fig.update_xaxes(
                tickmode="linear",
                tick0=0,
                dtick=1,
                range=[-0.5, 23.5]
            )
        elif filter_option == "Weekday":
            weekday_order = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]
            fig.update_xaxes(categoryorder="array",categoryarray=weekday_order)

        st.plotly_chart(fig, width="stretch")

    with st.expander("2. Cancellation heatmap across cities"):
        cancel_df = (
            df
            .groupby(["city", "booking_status"])
            .size()
            .reset_index(name="count")
        )

        cancel_df = cancel_df[cancel_df["booking_status"] == "Cancelled"]

        fig = px.density_heatmap(
            cancel_df,
            x="city",
            y="booking_status",
            z="count",
            title="Cancellation heatmap across cities"
        )
        st.plotly_chart(fig, width="stretch")

    with st.expander("3. Distance vs Fare correlation"):
        fig = px.scatter(
            df,
            x="ride_distance_km",
            y="booking_value",
            color="vehicle_type",
            title="Ride Distance vs Booking Value"
        )
        st.plotly_chart(fig, width="stretch")

    with st.expander("4. Rating distribution"):
        filter_df = df[["avg_customer_rating", "avg_driver_rating"]]

        fig_customer = px.histogram(
            filter_df,
            x="avg_customer_rating",
            nbins=10,
            title="Customer Rating Distribution"
        ).update_layout(
            xaxis_title="Average Customer Rating",
            yaxis_title="Number of Customers",
        )

        fig_driver = px.histogram(
            filter_df,
            x="avg_driver_rating",
            nbins=10,
            title="Driver Rating Distribution"
        ).update_layout(
            xaxis_title="Average Driver Rating",
            yaxis_title="Number of Drivers",
        )

        st.plotly_chart(fig_customer, width="stretch")
        st.write("---")
        
        st.plotly_chart(fig_driver, width="stretch")

    with st.expander("5. Customer Cancellation vs Driver Delay Behaviour"):
        behavior_df = df[[
            "customer_cancel_flag",
            "driver_delay_flag"
        ]].melt(
            var_name="behavior_type",
            value_name="flag"
        )

        fig = px.histogram(
            behavior_df,
            x="behavior_type",
            color="flag",
            barmode="group",
            title="Customer Cancellation vs Driver Delay Behaviour"
        )
        st.plotly_chart(fig, width="stretch")


    with st.expander("6. Traffic/Weather vs Cancellation"):
        filter_df = df[["traffic_level", "weather_condition", "booking_status"]]
        filter_df = filter_df.query("booking_status != 'Completed'")
        fig = px.histogram(
            filter_df,
            x="traffic_level",
            color="booking_status",
            barmode="group",
            title="Traffic Level vs Booking Status"
        )
        st.plotly_chart(fig, width="stretch")

        fig = px.histogram(
            filter_df,
            x="weather_condition",
            color="booking_status",
            barmode="group",
            title="Weather condition vs Booking Status"
        )
        st.plotly_chart(fig, width="stretch")