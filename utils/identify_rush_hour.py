def identify_rush_hour(row):
    if row["actual_ride_time_min"] <= 0:
        return 0
    
    est = row["estimated_ride_time_min"]
    act = row["actual_ride_time_min"]

    deviation_pct = abs(act - est) / est

    if deviation_pct >= 0.10 and row["traffic_level"] == "High":
        return 1
    
    return 0