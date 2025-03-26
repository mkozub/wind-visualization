#!/usr/bin/env python3
import requests
import folium
import sys
import numpy as np
from geopy.geocoders import Nominatim
from datetime import datetime
from folium.plugins import ScrollZoomToggler

def get_coordinates(place_name):
    """
    Get coordinates for a given place name using geopy.
    """
    print(f"Looking up coordinates for: {place_name}")
    geolocator = Nominatim(user_agent="wind_map_app")
    try:
        location = geolocator.geocode(place_name)
        if location:
            print(f"Found location: {location.address}")
            print(f"Coordinates: {location.latitude}, {location.longitude}")
            return location.latitude, location.longitude, location.address
        else:
            print(f"Could not find coordinates for: {place_name}")
            return None, None, None
    except Exception as e:
        print(f"Error looking up coordinates: {e}")
        return None, None, None

print("Starting wind visualization application...")
api_key = 'putAPIKey'  # Replace 'putAPIKey' with your Tomorrow.io API key

# Default location: Folly Beach, SC
default_latitude = 32.66
default_longitude = -79.96
default_place_name = "Folly Beach, SC"

if len(sys.argv) > 1:
    place_name = ' '.join(sys.argv[1:])
    latitude, longitude, location_address = get_coordinates(place_name)
    if latitude is None or longitude is None:
        print(f"Using default location: {default_latitude}, {default_longitude}")
        latitude = default_latitude
        longitude = default_longitude
        location_address = default_place_name
else:
    print("No location specified. Using default location.")
    latitude = default_latitude
    longitude = default_longitude
    place_name = default_place_name
    location_address = default_place_name

location_str = f"{latitude},{longitude}"
print(f"Using location: {latitude}, {longitude}")

print("Getting weather data from Tomorrow.io API...")
url = f'https://api.tomorrow.io/v4/weather/realtime?location={location_str}&apikey={api_key}'
response = requests.get(url)
print(f"API Response status code: {response.status_code}")

data = response.json()
print("API returned data successfully")
print(f"Here is the weather data the API returned: {data}")

wind_speed = data['data']['values'].get('windSpeed', 'N/A')
wind_direction = data['data']['values'].get('windDirection', 0)
print(f"Wind speed: {wind_speed} m/s")
print(f"Wind direction: {wind_direction}°")

try:
    wind_speed_numeric = float(wind_speed)
except ValueError:
    wind_speed_numeric = 0.0
wind_speed_knots = wind_speed_numeric * 1.94384

if wind_speed_knots <= 5:
    arrow_color = "#3498db"  # Blue
elif wind_speed_knots <= 10:
    arrow_color = "#2ecc71"  # Green
elif wind_speed_knots <= 15:
    arrow_color = "#f1c40f"  # Yellow
elif wind_speed_knots <= 20:
    arrow_color = "#e67e22"  # Orange
elif wind_speed_knots <= 25:
    arrow_color = "#e74c3c"  # Red
elif wind_speed_knots <= 30:
    arrow_color = "#c0392b"  # Dark Red
else:
    arrow_color = "#8e44ad"  # Dark Purple

corrected_direction = (wind_direction + 180) % 360
compass_points = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]
text_compass_index = round(wind_direction / 22.5) % 16
text_compass_direction = compass_points[text_compass_index]

print("Creating map...")
m = folium.Map(location=[latitude, longitude], zoom_start=14, min_zoom=10, tiles=None)
# Add two base layers: Light (default) and Dark.
folium.TileLayer('OpenStreetMap', name='Light', control=True, show=True).add_to(m)
folium.TileLayer('CartoDB dark_matter', name='Dark', control=True, show=False).add_to(m)
folium.LayerControl(position='bottomright', collapsed=False).add_to(m)
print("Map created successfully")

print("Adding wind field visualization to map...")
grid_size = 40
grid_spacing = 0.0025
x_min = longitude - (grid_size / 2) * grid_spacing
y_min = latitude - (grid_size / 2) * grid_spacing
arrow_opacity = 0.7

for i in range(grid_size):
    for j in range(grid_size):
        point_lat = y_min + j * grid_spacing
        point_lon = x_min + i * grid_spacing
        arrow_size = min(30, max(16, 20 * (wind_speed_numeric / 10)))
        folium.Marker(
            location=[point_lat, point_lon],
            icon=folium.DivIcon(html=f"""
                <div style="font-size:{arrow_size}pt; transform: rotate({corrected_direction}deg); opacity: {arrow_opacity}; color: {arrow_color};">↑</div>
            """),
            tooltip=f"Wind: {wind_speed} m/s ({wind_speed_knots:.1f} kts), Direction: {wind_direction}°"
        ).add_to(m)

ScrollZoomToggler().add_to(m)

# ------------------ TOP TITLE BAR with Stylized Arrow ------------------
title_html = f"""
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
    background-color: #1E1E1E;
    color: #D4D4D4;
    border: 2px solid #0B84FF;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    padding: 15px;
    font-family: 'Arial', sans-serif;
    display: flex;
    align-items: center;
    z-index: 9999;
">
    <!-- Stylized arrow shape with thick blue border -->
    <div style="flex: 0 0 auto; text-align: center; white-space: nowrap; margin-right: 10px;">
        <div style="width: 60px; height: 60px; display: inline-block;">
            <svg viewBox="0 0 200 200"
                 width="100%" height="100%"
                 style="transform: rotate({corrected_direction}deg); transform-origin: 50% 50%;">
                <path d="
                  M100,20
                  L140,60
                  L110,60
                  L110,110
                  L90,110
                  L90,60
                  L60,60
                  Z
                "
                fill="#D4D4D4"
                stroke="#0B84FF"
                stroke-width="8"/>
            </svg>
        </div>
        <div style="font-weight: bold; font-size: clamp(10px, 2vw, 16px); white-space: nowrap; margin-top: 5px;">
            {text_compass_direction}, {wind_speed_knots:.1f} kts
        </div>
    </div>
    <!-- Title and details section -->
    <div style="flex: 1 1 auto; text-align: center; white-space: nowrap;">
        <h2 style="
            margin: 0;
            font-weight: bold;
            color: #D4D4D4;
            font-size: clamp(12px, 3vw, 20pt);
            white-space: nowrap;
        ">
            Live Wind Visualization: {place_name}
        </h2>
        <div style="
            font-size: clamp(8px, 2vw, 10pt);
            color: #D4D4D4;
            white-space: nowrap;
        ">
            {location_address}
        </div>
        <div style="
            margin-top: 5px;
            font-size: clamp(10px, 2vw, 14pt);
            font-weight: 500;
            color: #D4D4D4;
            white-space: nowrap;
        ">
            Visualization updated at {datetime.now().strftime("%H:%M %B %d, %Y")}
        </div>
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# ------------------ BOTTOM LEGEND BAR (Dark UI) ------------------
legend_html = f"""
<div style="
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
    background-color: #1E1E1E;
    color: #D4D4D4;
    border: 2px solid #0B84FF;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    padding: 10px;
    z-index: 9999;
    font-family: 'Arial', sans-serif;
">
    <div style="
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 10px;
        font-size: clamp(12px, 2vw, 16px);
        white-space: nowrap;
    ">
        <div style="font-weight: bold;">Wind Speed in Knots</div>
        <span><i style='background:#3498db; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>0-5</span>
        <span><i style='background:#2ecc71; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>6-10</span>
        <span><i style='background:#f1c40f; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>11-15</span>
        <span><i style='background:#e67e22; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>16-20</span>
        <span><i style='background:#e74c3c; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>21-25</span>
        <span><i style='background:#c0392b; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>26-30</span>
        <span><i style='background:#8e44ad; width: 12px; height: 12px; display: inline-block; margin-right: 4px;'></i>31+</span>
    </div>
    <div style="
        font-size: clamp(8px, 2vw, 10pt);
        color: #D4D4D4;
        text-align: center;
        margin-top: 5px;
        white-space: nowrap;
    ">
        Data provided by Tomorrow.io API • Visualization created by Mike Kozub
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

print("Writing map to file...")
m.save('wind_map.html')
print("Map saved to wind_map.html")
print("Application completed successfully")