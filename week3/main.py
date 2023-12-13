import folium
from folium.plugins import MarkerCluster
from PIL import Image, ImageDraw
import pandas as pd
import io
import tempfile

def create_colored_icon(icon_path, background_color, size=(30, 30)):
    base = Image.open(icon_path).convert("RGBA")

    # Ensure the base icon has the same dimensions as the background
    base = base.resize(size, Image.LANCZOS)

    # Create a blank image with a colored background
    background = Image.new("RGBA", size, background_color)

    # Ensure the base icon has the same mode as the background
    base = base.convert(background.mode)

    # Paste the icon onto the colored background
    icon = Image.alpha_composite(background, base)

    # Save the image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    icon.save(temp_file.name, format="PNG")
    temp_file.close()

    return temp_file.name


# Assuming your dataset is in a CSV file named 'coffee_data.csv'
file_path = 'data/coffeedata.csv'
df = pd.read_csv(file_path)

# Create a folium map centered around the mean latitude and longitude with a title
map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=12, title="Coffee I drank over the last weekend, visualised")

# Create a single MarkerCluster to hold all markers
marker_cluster = MarkerCluster().add_to(mymap)

# Define base icons for each unique type of coffee
base_icons = {
    'Coffee with milk': 'coffee-with-milk-icon.png',
    'Cappuccino': 'cappuccino-icon.png',
    'Coffee "verkeerd"': 'verkeerd-coffee-icon.png',
    'Cappuccino extra': 'cappuccino-extra-icon.png',
    'Black Coffee': 'black-coffee-icon.png',
    'Irish Coffee': 'irish-coffee-icon.png',
    'Latte Machiato': 'latte-machiato-icon.png'
    # Add more icons for each unique type of coffee
}

# Add coffee cup icons for each data point in the dataset
for index, row in df.iterrows():
    # Assign colors based on the quality scale (assuming 1 is poor, 2 is medium, and 3 is good)
    quality_color = 'red' if row['Quality'] == 1 else 'orange' if row['Quality'] == 2 else 'green'

    # Use a different icon for each unique type of coffee
    base_icon_path = "img/" + base_icons.get(row['Type'], 'default-coffee-icon.png')
    icon_path = create_colored_icon(base_icon_path, quality_color)

    # Use a coffee cup icon with the adjusted size based on the Quantity(ml) column
    icon_size = row['Quantity(ml)'] / 6  # Adjust the division factor to control the size

    # Create popup content with additional information
    popup_content = (
        f"{row['Type']} - {row['Quantity(ml)']}ml\n"
        f"Day: {row['Day']}\n"
        f"Date: {row['Date']}\n"
        f"Time: {row['Time']}"
    )

    icon = folium.CustomIcon(
        icon_image=icon_path,
        icon_size=(icon_size, icon_size)
    )

    # Add marker to the MarkerCluster
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_content, parse_html=True),
        icon=icon,
    ).add_to(marker_cluster)

# Save the map as an HTML file
mymap.save('index.html')
