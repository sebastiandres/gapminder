# Snowpark
import ssl
import pandas as pd
from math import ceil
import streamlit as st 
from streamlit.components.v1 import html

from ipyvizzustory import Story, Slide, Step
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget

from helpers.data_helpers import set_page_config, eval_sql
from helpers.vizzu_helpers import vizzu_story

ssl._create_default_https_context = ssl._create_unverified_context

set_page_config()

st.title("Available Measures")
st.caption("This page shows the measures (variables) available in the TIMESERIES table")

# Get the data
df_sql = eval_sql(f"""
    SELECT 
        VARIABLE_NAME, 
        UNIT, 
        COUNT( DISTINCT GEO_ID) AS N_COUNTRIES,
        COUNT( DISTINCT year(DATE)) AS N_YEARS, 
        COUNT( DISTINCT GEO_ID) * COUNT( DISTINCT year(DATE)) AS N_YEARS_TIMES_N_COUNTRIES, 
        COUNT( DISTINCT GEO_ID, year(DATE)) AS N_DATAPOINTS,
        min(year(DATE)) as MIN_YEAR, 
        max(year(DATE)) as MAX_YEAR
    FROM 
        TIMESERIES
    WHERE
        GEO_ID LIKE 'country%'
    GROUP BY 
        VARIABLE_NAME, UNIT
    ORDER BY
        N_DATAPOINTS DESC
""")

# The table
st.write(f"The (hidden) table shows the number of countries and years for each measure (variable). The table contains {df_sql.shape[0]} rows.")
with st.expander("Show the dataframe"):
    st.write(df_sql)

# The graphical representation
mkd = """
The graphical representation shows that not all the measures have the same amount of data on a given year. 
The number of years and countries for each measure (variable) is shown in the x and y axis, respectively.
The number of datapoints is shown as the size of the circle.
Hover over the circles to see the name of the measure (variable).

You can lookup a specific measure (variable) by typing its name on the SQL explorer page.
"""
st.write(mkd)
df_sql["Number of Countries"] = df_sql["N_COUNTRIES"]
df_sql["Number of Years"] = df_sql["N_YEARS"]
df_sql["nrow"] = df_sql.index
data = Data()
data.add_data_frame(df_sql)
frame_list = []
frame = (
        Style({"legend": {"width": 0}}),
        Config(
        {
            "x": "Number of Countries",
            "y": "Number of Years",
            "title": "Number of years and number of countries for each measure (variable)",
            "color": "VARIABLE_NAME",
            "geometry": "circle",
            "size": "N_DATAPOINTS",
        }
    ),
)
frame_list.append(frame)
vizzu_story(data, frame_list, 800)
