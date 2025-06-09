import argparse
import pandas as pd
import folium
import os
from folium import plugins
from geopy.distance import geodesic


def load_data(csv_path='data/spacex_launch_dash.csv'):
    """Load SpaceX launch data from CSV."""
    return pd.read_csv(csv_path)


def generate_launch_site_map(df, output_path='docs/launch_site_map.html', zoom_start=4):
    """Generate an enhanced Folium map with multiple SpaceX launch data features."""
    # Hardcoded coordinates for simplified site labels
    coordinates = {
        'Cape Canaveral': [28.562302, -80.577356],
        'Vandenberg': [34.632834, -120.610746],
        'Kennedy': [28.573255, -80.646895]
    }

    # Create base map centered around average location
    lat_center = sum([lat for lat, lon in coordinates.values()]) / len(coordinates)
    lon_center = sum([lon for lat, lon in coordinates.values()]) / len(coordinates)
    site_map = folium.Map(location=[lat_center, lon_center], zoom_start=zoom_start)

    # Add launch site circles and markers
    for site, (lat, lon) in coordinates.items():
        folium.Circle(
            [lat, lon],
            radius=1000,
            color='blue',
            fill=True,
            fill_opacity=0.1,
            popup=f"{site} (1km radius)"
        ).add_to(site_map)
        folium.Marker(
            [lat, lon],
            icon=folium.Icon(color='blue', icon='rocket', prefix='fa'),
            popup=site
        ).add_to(site_map)

    # Add all launch attempts with color-coded success/failure
    for _, row in df.iterrows():
        site = row['launch_site']
        if site not in coordinates:
            continue  # Skip unknown sites
        lat, lon = coordinates[site]
        status = "Success" if row['class'] == 1 else "Failure"
        color = 'green' if row['class'] == 1 else 'red'
        folium.Marker(
            [lat, lon],
            icon=folium.Icon(color=color),
            popup=f"{site}: {status}"
        ).add_to(site_map)

    # Optional: Add a click-for-marker feature
    site_map.add_child(folium.LatLngPopup())

    # Optional: Example distance line from Cape Canaveral to nearby point
    coast_point = [28.563, -80.567]  # Adjust as needed
    site_latlon = coordinates['Cape Canaveral']
    distance_km = geodesic(site_latlon, coast_point).km
    folium.PolyLine(locations=[site_latlon, coast_point], color='purple').add_to(site_map)
    folium.Marker(
        location=coast_point,
        popup=f"Coast (~{distance_km:.2f} km from Cape Canaveral)",
        icon=folium.Icon(color='purple', icon='flag')
    ).add_to(site_map)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    site_map.save(output_path)
    print(f"Map saved to {output_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a Folium map of SpaceX launch sites.")
    parser.add_argument('--output', type=str, default='docs/launch_site_map.html',
                        help='Output HTML file path')
    parser.add_argument('--zoom', type=int, default=4,
                        help='Zoom level for map (default: 4)')
    return parser.parse_args()


def main():
    args = parse_args()
    df = load_data()
    generate_launch_site_map(df, output_path=args.output, zoom_start=args.zoom)


if __name__ == '__main__':
    main()