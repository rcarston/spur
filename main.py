import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd

# Supabase connection details
url = "https://opjkbdccpbiosetkkiuv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wamtiZGNjcGJpb3NldGtraXV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU4NDE4OTUsImV4cCI6MjAzMTQxNzg5NX0.tNF-ZUlPA66G80tBOvbAc3PSQh_dyV_yWzucpnTV-p0"
supabase: Client = create_client(url, key)

# Fetch the data
def fetch_all_data():
    data = []
    offset = 0
    limit = 1000  # Fetch in batches of 1000
    while True:
        response = supabase.table("SalesOrders1").select("total").range(offset, offset + limit - 1).execute()
        batch = response.data
        if not batch:
            break
        data.extend(batch)
        offset += limit
    return data

# Calculate the sum of the "total" column
data = fetch_all_data()

# Convert data to pandas DataFrame for better manipulation and display
df = pd.DataFrame(data)


# Calculate the sum
total_sum = df['total'].sum() if not df.empty else 0

# Define the goal
goal = 6000000

# Create the gauge chart
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_sum,
    title={"text": "Sales Goal"},
    gauge={
        "axis": {"range": [None, goal]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, goal * 0.25], "color": "#FFF5E1"},  # Light sand color
            {"range": [goal * 0.25, goal * 0.5], "color": "#FFE4B5"},  # Sand color
            {"range": [goal * 0.5, goal * 0.75], "color": "#98FB98"},  # Pale green
            {"range": [goal * 0.75, goal], "color": "#00FA9A"},  # Medium spring green
        ],
    }
))

# Display the gauge chart in Streamlit
st.title("Goal Progress")
st.plotly_chart(fig)
