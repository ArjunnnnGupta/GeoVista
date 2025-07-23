import requests
import json
from datetime import date

CITIES = {
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

def fetch_rainfall():
    today = date.today().isoformat()
    incidents = []
    for city, (lat, lon) in CITIES.items():
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&daily=precipitation_sum"
            "&forecast_days=1"
            "&timezone=auto"
        )
        resp = requests.get(url).json()
        pf = resp.get("daily", {})
        for d, rain in zip(pf.get("time", []), pf.get("precipitation_sum", [])):
            incidents.append({
                "type": "rainfall",
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "date": d,
                "precipitation": rain
            })
    with open("data/rainfall.json", "w") as f:
        json.dump(incidents, f, indent=2)
    print(f"🌧 Saved rainfall data for {len(incidents)} records.")
