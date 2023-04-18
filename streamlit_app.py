import requests
import pandas as pd
import streamlit as st
import plotly.express as px

url = 'https://dde-api.data.imgarena.com/soccer/fixtures?subscribed=true&dateFrom=2023-04-19&dateTo=2023-04-19&type=official'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NGIwZmI2Ny0zNDVjLTRlMzctYjU1ZS05OGMxY2E1MmE3ZWUiLCJleHAiOiIyMDIzLTA1LTAyVDE0OjE3OjIxLjc5NzU1OCIsImlhdCI6IjIwMjMtMDQtMThUMTQ6MTc6MjEuNzk3NTU4Iiwic3ViIjoicHJhdGlrLnNoZXR0eUBpbWdhcmVuYS5jb20iLCJyb2xlIjp7InJvbGVOYW1lIjoiQWRtaW4ifX0.0bi61SWREdE0Q5OZajZioQWP4GGK7_JjZbFLiFLBnNxWs27EyPqH0rXwE4XndhUDne2R5j4H4A14ty2CqRK8TQ',
    'Accept': 'text/csv, application/json, text/plain, application/vnd.imggaming.dde.api+json;version=1'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Get the JSON data from the response
    data = response.json()
    
else:
    print(f'Request failed with status code {response.status_code}')

final_data = pd.DataFrame({"ID": [data[x]['id'] for x in range(0,len(data))],
                           "NAME": [data[x]['name'] for x in range(0,len(data))],
                           "COLLEXTION_SATUS": [data[x]['collectionStatus'] for x in range(0,len(data))],
                           "COVERAGE_LEVEL": [data[x]['coverageLevel'] for x in range(0,len(data))],
                           "START_DATE_UTC": [data[x]['startDateUTC'] for x in range(0,len(data))],
                           "LEAGUE_NAME": [data[x]['stage']['season']['competition']['name'] for x in range(0,len(data))]})

# Set the title of the app
st.title("Football 19/04/2023")

# Add a sidebar with filters
st.sidebar.title("Filters")
league_filter = st.sidebar.multiselect("Select League(s)", final_data["LEAGUE_NAME"].unique())
status_filter = st.sidebar.multiselect("Select Status(es)", final_data["COLLECTION_STATUS"].unique())
coverage_filter = st.sidebar.multiselect("Select Coverage Level(s)", final_data["COVERAGE_LEVEL"].unique())

# Filter the data based on the selected filters
filtered_data = final_data[
    (final_data["LEAGUE_NAME"].isin(league_filter)) &
    (final_data["COLLECTION_STATUS"].isin(status_filter)) &
    (final_data["COVERAGE_LEVEL"].isin(coverage_filter))
]

# Display the filtered data
st.write("### Final Data")
st.dataframe(filtered_data)

# Display a scatter plot of the data
st.write("### Scatter Plot")
fig = px.scatter(filtered_data, x="START_DATE_UTC", y="ID", color="COLLECTION_STATUS", size="COVERAGE_LEVEL")
st.plotly_chart(fig)
    
  
