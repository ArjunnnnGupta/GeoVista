import requests
import json
from datetime import datetime, timedelta

def fetch_earthquakes():
    end = datetime.utcnow().date()
    start = end - timedelta(days=365)
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson&starttime={start}&endtime={end}"
        "&minmagnitude=4&minlatitude=6&maxlatitude=38&minlongitude=68&maxlongitude=98"
    )
    r = requests.get(url)
    data = r.json()
    incidents = []
    for f in data.get("features", []):
        c = f["geometry"]["coordinates"]
        p = f["properties"]
        incidents.append({
            "type": "earthquake",
            "latitude": c[1],
            "longitude": c[0],
            "magnitude": p["mag"],
            "time": datetime.utcfromtimestamp(p["time"]/1000).isoformat(),
            "place": p["place"]
        })
    with open("data/earthquakes.json", "w") as f:
        json.dump(incidents, f, indent=2)
    print(f"🌍 Saved {len(incidents)} earthquake events.")
