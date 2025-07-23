import pandas as pd
import json
import os
import joblib
from datetime import timedelta

# Constants
MODEL_PATH = "models/xgboost_rainfall_model.pkl"
DATA_PATH = "data/weather"
OUTPUT_PATH = "data/forecast.json"
TARGET_COL = "precipitation_sum"
LAG_DAYS = 2

FEATURES = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "sunshine_duration",
    "daylight_duration",
    "precipitation_sum_lag1",
    "precipitation_sum_lag2"
]

CITY_COORDS = {
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Chennai": [13.0827, 80.2707],
    "Bangalore": [12.9716, 77.5946],
    "Guwahati": [26.1445, 91.7362],
    "Hyderabad": [17.3850, 78.4867],
    "Ahmedabad": [23.0225, 72.5714],
    "Pune": [18.5204, 73.8567],
    "Kolkata": [22.5726, 88.3639],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462],
    "Kanpur": [26.4499, 80.3319],
    "Nagpur": [21.1458, 79.0882],
    "Indore": [22.7196, 75.8577],
    "Bhopal": [23.2599, 77.4126],
    "Patna": [25.5941, 85.1376],
    "Ranchi": [23.3441, 85.3096],
    "Bhubaneswar": [20.2961, 85.8245],
    "Thiruvananthapuram": [8.5241, 76.9366],
    "Vijayawada": [16.5062, 80.6480],
    "Visakhapatnam": [17.6868, 83.2185],
    "Surat": [21.1702, 72.8311],
    "Coimbatore": [11.0168, 76.9558],
    "Madurai": [9.9252, 78.1198],
    "Amritsar": [31.6340, 74.8723],
    "Imphal": [24.8170, 93.9368],
    "Aizawl": [23.7271, 92.7176],
    "Shillong": [25.5788, 91.8933]
}

def add_lag_features(df, target_col, lag_days):
    for i in range(1, lag_days + 1):
        df[f"{target_col}_lag{i}"] = df[target_col].shift(i)
    return df

def predict_next_two_days(city, file_path, model):
    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").reset_index(drop=True)

    df = add_lag_features(df, TARGET_COL, LAG_DAYS)
    df = df.dropna().reset_index(drop=True)

    forecasts = []
    lat, lon = CITY_COORDS.get(city, [0.0, 0.0])

    for day in range(1, 3):  # Predict next 2 days
        latest_row = df.iloc[-1].copy()

        input_data = latest_row[FEATURES].values.reshape(1, -1)
        prediction = model.predict(input_data)[0]
        predicted_value = round(float(prediction), 2)

        next_date = (latest_row["time"] + timedelta(days=1)).strftime("%Y-%m-%d")
        forecasts.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "date": next_date,
            "predicted_rainfall": predicted_value,
            "type": "rainfall"
        })

        # Append prediction to DataFrame for recursive prediction
        new_row = latest_row.copy()
        new_row["time"] = latest_row["time"] + timedelta(days=1)
        new_row["precipitation_sum"] = prediction

        # Shift lag features
        new_row["precipitation_sum_lag1"] = latest_row["precipitation_sum"]
        new_row["precipitation_sum_lag2"] = latest_row["precipitation_sum_lag1"]

        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

    return forecasts

def main():
    if not os.path.exists(MODEL_PATH):
        print("Model not found.")
        return

    model = joblib.load(MODEL_PATH)
    all_forecasts = []

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".csv"):
            city = filename.replace(".csv", "")
            file_path = os.path.join(DATA_PATH, filename)
            try:
                forecasts = predict_next_two_days(city, file_path, model)
                all_forecasts.extend(forecasts)
            except Exception as e:
                print(f"Error for {city}: {e}")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_forecasts, f, indent=2)

    print(f"Saved forecast for {len(all_forecasts)//2} cities × 2 days = {len(all_forecasts)} predictions.")

if __name__ == "__main__":
    main()
