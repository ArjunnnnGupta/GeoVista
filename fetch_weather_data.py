import requests
import pandas as pd
import json
import os
from datetime import date, timedelta

cities = {
    "Patna": (25.5941, 85.1376),
    "Ranchi": (23.3441, 85.3096),
    "Bhubaneswar": (20.2961, 85.8245),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Vijayawada": (16.5062, 80.6480),
    "Visakhapatnam": (17.6868, 83.2185),
    "Surat": (21.1702, 72.8311),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Amritsar": (31.6340, 74.8723),
    "Imphal": (24.8170, 93.9368),
    "Aizawl": (23.7271, 92.7176),
    "Shillong": (25.5788, 91.8933)
}

# Date range
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=730)

# Output folder
os.makedirs("data", exist_ok=True)

# Fetch and store
for city, (lat, lon) in cities.items():
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,"
        "precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,"
        "sunshine_duration,daylight_duration"
        "&timezone=auto"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["daily"])
        
        df.to_csv(f"data/weather/{city}.csv", index=False)
        
            

        print(f"✅ {city} data saved.")
    except Exception as e:
        print(f"❌ Error fetching for {city}: {e}")