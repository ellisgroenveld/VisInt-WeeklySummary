import os
import pandas as pd
import plotly.express as px

# Get the current script directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Load the dataset
data_path = os.path.join(current_dir, "data", "orderdata.csv")
data = pd.read_csv(data_path)

# Fill NaN or empty values in the DataFrame with "No Commentary"
data.fillna(value={"Notes": "No Commentary"}, inplace=True)

# Create a new column for the end date of each event
data['End_date'] = pd.to_datetime(data['Arrivaldate'])

# Define a custom color palette with more contrast
custom_palette = px.colors.qualitative.Set3

# Create a figure with the custom color palette
fig = px.timeline(
    data,
    x_start="Orderdate",
    x_end="End_date",
    y="Productname",
    labels={
        "Productname": "Product",
        "Orderdate": "Order Date",
        "End_date": "Arrival Date",
        "Brand": "Brand",
        "Category": "Category",
        "Notes": "Notes",
    },
    color="Enjoy",
    hover_name="Productname",
    hover_data=["Brand", "Category", "Notes"],
    color_discrete_sequence=custom_palette
    
)

# Update layout
fig.update_layout(
    xaxis=dict(title="Date"),
    yaxis=dict(title="Product"),
    title="Interactive Timeline",
)

# Save the figure as an HTML file named "index.html" in the same subfolder
html_path = os.path.join(current_dir, "index.html")
fig.write_html(html_path)
