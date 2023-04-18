{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOZ9xjBRgizgLe89JbWS9PA"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "cOo4uw3DYUbq"
      },
      "outputs": [],
      "source": [
        "import requests\n",
        "import pandas as pd\n",
        "\n",
        "url = 'https://dde-api.data.imgarena.com/soccer/fixtures?subscribed=true&dateFrom=2023-04-19&dateTo=2023-04-19&type=official'\n",
        "headers = {\n",
        "    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NGIwZmI2Ny0zNDVjLTRlMzctYjU1ZS05OGMxY2E1MmE3ZWUiLCJleHAiOiIyMDIzLTA1LTAyVDE0OjE3OjIxLjc5NzU1OCIsImlhdCI6IjIwMjMtMDQtMThUMTQ6MTc6MjEuNzk3NTU4Iiwic3ViIjoicHJhdGlrLnNoZXR0eUBpbWdhcmVuYS5jb20iLCJyb2xlIjp7InJvbGVOYW1lIjoiQWRtaW4ifX0.0bi61SWREdE0Q5OZajZioQWP4GGK7_JjZbFLiFLBnNxWs27EyPqH0rXwE4XndhUDne2R5j4H4A14ty2CqRK8TQ',\n",
        "    'Accept': 'text/csv, application/json, text/plain, application/vnd.imggaming.dde.api+json;version=1'\n",
        "}\n",
        "\n",
        "response = requests.get(url, headers=headers)\n",
        "\n",
        "if response.status_code == 200:\n",
        "    # Get the JSON data from the response\n",
        "    data = response.json()\n",
        "    # Do something with the data\n",
        "    \n",
        "else:\n",
        "    print(f'Request failed with status code {response.status_code}')"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "final_data = pd.DataFrame({\"ID\": [data[x]['id'] for x in range(0,len(data))],\n",
        "                           \"NAME\": [data[x]['name'] for x in range(0,len(data))],\n",
        "                           \"COLLEXTION_SATUS\": [data[x]['collectionStatus'] for x in range(0,len(data))],\n",
        "                           \"COVERAGE_LEVEL\": [data[x]['coverageLevel'] for x in range(0,len(data))],\n",
        "                           \"START_DATE_UTC\": [data[x]['startDateUTC'] for x in range(0,len(data))],\n",
        "                           \"LEAGUE_NAME\": [data[x]['stage']['season']['competition']['name'] for x in range(0,len(data))]})"
      ],
      "metadata": {
        "id": "x7ntMbbHYbxS"
      },
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import plotly.express as px\n",
        "\n",
        "# Set the title of the app\n",
        "st.title(\"Interactive Dashboard\")\n",
        "\n",
        "# Add a sidebar with filters\n",
        "st.sidebar.title(\"Filters\")\n",
        "league_filter = st.sidebar.multiselect(\"Select League(s)\", final_data[\"LEAGUE_NAME\"].unique())\n",
        "status_filter = st.sidebar.multiselect(\"Select Status(es)\", final_data[\"COLLECTION_STATUS\"].unique())\n",
        "coverage_filter = st.sidebar.multiselect(\"Select Coverage Level(s)\", final_data[\"COVERAGE_LEVEL\"].unique())\n",
        "\n",
        "# Filter the data based on the selected filters\n",
        "filtered_data = final_data[\n",
        "    (final_data[\"LEAGUE_NAME\"].isin(league_filter)) &\n",
        "    (final_data[\"COLLECTION_STATUS\"].isin(status_filter)) &\n",
        "    (final_data[\"COVERAGE_LEVEL\"].isin(coverage_filter))\n",
        "]\n",
        "\n",
        "# Display the filtered data\n",
        "st.write(\"### Final Data\")\n",
        "st.dataframe(filtered_data)\n",
        "\n",
        "# Display a scatter plot of the data\n",
        "st.write(\"### Scatter Plot\")\n",
        "fig = px.scatter(filtered_data, x=\"START_DATE_UTC\", y=\"ID\", color=\"COLLECTION_STATUS\", size=\"COVERAGE_LEVEL\")\n",
        "st.plotly_chart(fig)"
      ],
      "metadata": {
        "id": "jTrbbcbqYqTN"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "WQbsU99-Yr5v"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}