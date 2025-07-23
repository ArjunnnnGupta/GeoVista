const map = L.map('map').setView([22.5937, 78.9629], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18
}).addTo(map);

const eqLayer = L.layerGroup().addTo(map);
const rainLayer = L.layerGroup().addTo(map);
const forecastLayer = L.layerGroup().addTo(map);  // New layer for predictions

function classifyRain(mm) {
  if (mm === 0) return "No Rain";
  if (mm < 2.5) return "Light Rain";
  if (mm < 64.5) return "Moderate Rain";
  if (mm < 115.6) return "Heavy Rain";
  if (mm < 204.5) return "Very Heavy Rain";
  return "Extremely Heavy Rain";
}

function formatDate(isoString) {
  const d = new Date(isoString);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth()+1).toString().padStart(2, '0')}/${d.getFullYear()}`;
}

function loadIncidents() {
  fetch('/api/incidents')
    .then(r => r.json())
    .then(data => {
      eqLayer.clearLayers();
      rainLayer.clearLayers();
      forecastLayer.clearLayers();

      data.forEach(i => {
        if (i.type === 'earthquake') {
          const dateStr = i.time ? `<br><i>${formatDate(i.time)}</i>` : '';
          L.circle([i.latitude, i.longitude], {
            color: 'red',
            fillColor: 'red',
            fillOpacity: 0.5,
            radius: 2500 * (i.magnitude || 1)
          })
            .bindPopup(`<b>Earthquake</b><br>${i.place || ''}<br>Mag: ${i.magnitude}${dateStr}`)
            .addTo(eqLayer);

        } else if (i.type === 'rainfall') {
          const rainType = classifyRain(i.precipitation);
          const dateStr = i.date ? `<br><i>${formatDate(i.date)}</i>` : '';
          L.marker([i.latitude, i.longitude], {
            icon: L.icon({
              iconUrl: '/static/icons/rain.png',
              iconSize: [26, 26]
            })
          })
            .bindPopup(`<b>${i.city}</b><br>Rain: ${i.precipitation} mm<br><b>${rainType}</b>${dateStr}`)
            .addTo(rainLayer);

        } else if (i.type === 'forecast') {
          const rainType = classifyRain(i.predicted_rainfall);
          const dateStr = i.date ? `<br><i>${formatDate(i.date)}</i>` : '';
          L.marker([i.latitude, i.longitude], {
            icon: L.icon({
              iconUrl: '/static/icons/rain_pred.png',
              iconSize: [26, 26]
            })
          })
            .bindPopup(`<b>${i.city}</b><br><u>Predicted Rain:</u> ${i.predicted_rainfall} mm<br><b>${rainType}</b>${dateStr}`)
            .addTo(forecastLayer);
        }
      });
    });
}

document.getElementById('earthquake-toggle').onchange = function () {
  this.checked ? map.addLayer(eqLayer) : map.removeLayer(eqLayer);
};

document.getElementById('rainfall-toggle').onchange = function () {
  this.checked ? map.addLayer(rainLayer) : map.removeLayer(rainLayer);
};
document.getElementById('forecast-toggle').onchange = function () {
    this.checked ? map.addLayer(forecastLayer) : map.removeLayer(forecastLayer);
};

loadIncidents();
setInterval(loadIncidents, 10 * 60 * 1000);  // Refresh every 10 minutes
