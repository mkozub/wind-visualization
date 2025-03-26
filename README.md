# Wind Visualization Microservice

This microservice generates an interactive wind visualization map using real-time weather data from the Tomorrow.io API. It is designed to be integrated into larger weather applications as a lightweight backend service.

## Features

- **Real-Time Data:** Retrieves wind speed and direction from the Tomorrow.io API.
- **Interactive Map:** Displays an interactive map with a wind field visualization using Folium.
- **Stylized Wind Direction Indicator:** A custom, stylized arrow in the header shows the wind direction and speed.
- **Base Layer Toggle:** Switch between a light (default, using OpenStreetMap) and dark (using CartoDB Dark Matter) map view.
- **Responsive UI:** The header and legend adjust dynamically for various screen sizes.

## Requirements

- Python 3.6+
- [requests](https://pypi.org/project/requests/)
- [folium](https://pypi.org/project/folium/)
- [geopy](https://pypi.org/project/geopy/)
- [numpy](https://pypi.org/project/numpy/)

Install the required packages with:

```bash
pip install requests folium geopy numpy
```

## Setup

1. Clone this repository.
2. In `windvisualization.py`, replace the placeholder `putAPIKey` with your Tomorrow.io API key.
3. Optionally, provide a location as a command-line argument. If none is provided, the service defaults to **Folly Beach, SC**.

## Usage

Run the microservice with:

```bash
python windvisualization.py [location]
```

Example:

```bash
python windvisualization.py "Folly Beach, SC"
```

This will generate an HTML file (`wind_map.html`) that you can open in your web browser to view the interactive wind visualization.

## Purpose

This microservice is intended as a backend component for weather applications. It visualizes real-time wind data on an interactive map and can be easily integrated into larger systems for forecasting, weather analytics, or any application requiring wind visualization.

## API Key

You must have a valid Tomorrow.io API key. Replace the placeholder `putAPIKey` in `windvisualization.py` with your API key.

## License

This project is released under the MIT License.
