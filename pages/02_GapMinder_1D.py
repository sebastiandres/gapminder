# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget
from streamlit.components.v1 import html
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from helpers.helpers import set_page_config, eval_sql, create_session_object, variable_name_options
from helpers.vizzu_wrapper import st_vizzu, bubble_chart_config

set_page_config()

st.title("GapMinder 2D")
c1, c2 = st.columns(2)

# Provide options
x_axis_options = variable_name_options.copy()
x_axis_sel = c1.selectbox("X-Axis", x_axis_options)
y_axis_options = x_axis_options.copy()
y_axis_options.remove(x_axis_sel)
y_axis_sel = c1.selectbox("Y-Axis", y_axis_options)
bubble_options = y_axis_options.copy()
bubble_options.remove(y_axis_sel)
bubble_size_sel = c1.selectbox("Bubble Size", bubble_options)

# Get the data
df = eval_sql(f"""
    SELECT 
        VARIABLE, VARIABLE_NAME, GEO_ID, date, year(date) as YEAR, VALUE, UNIT
    FROM 
        TIMESERIES
    WHERE
        GEO_ID LIKE 'country%' AND VARIABLE_NAME in ('{x_axis_sel}', '{y_axis_sel}', '{bubble_size_sel}')
    ORDER BY 
        DATE asc
""")
default_values = ["country/USA", "country/CHL", "country/FRA"]
geo_id_options = df['GEO_ID'].unique().tolist()
geo_id_sel = c2.multiselect("Countries", geo_id_options, default=default_values)

# Subselect the data based on the selected countries
df_sel = df[df['GEO_ID'].isin(geo_id_sel)]

# Take average of value for each variable and year, if any duplication
df_sel_avg = df_sel.groupby(['GEO_ID', 'YEAR', 'VARIABLE_NAME'])['VALUE'].mean().reset_index() 
df_sel_avg = df_sel_avg.sort_values(['VARIABLE_NAME', 'YEAR', 'GEO_ID'])
#st.write(df_sel_avg)

# Get the common years between the selected countries
years = set(df_sel_avg['YEAR'].unique().tolist())
for geo_id in geo_id_sel[1:]:
    for variable in [x_axis_sel, y_axis_sel, bubble_size_sel]:
        m1 = df_sel_avg['GEO_ID'] == geo_id
        m2 = df_sel_avg['VARIABLE_NAME'] == variable
        new_years = set(df_sel_avg[m1 & m2]['YEAR'].unique().tolist())
        years = years.intersection(new_years)
year_list = sorted(list(years))

# Now we have to pivot the table to have the variables as columns!
df_data_aux = df_sel_avg[df_sel_avg['YEAR'].isin(year_list)]
df_data = df_data_aux.pivot(index=['GEO_ID', 'YEAR'], columns='VARIABLE_NAME', values='VALUE').reset_index()
#st.write(df_data)

if len(year_list) == 0:
    st.write("No common years between the selected countries")
else:
    year_min = min(year_list)
    year_max = max(year_list)
    year_min_sel, year_max_sel = c2.slider("Year", year_min, year_max, (year_min, year_max))
    year_list_sel = [y for y in year_list if y >= year_min_sel and y <= year_max_sel]

    xmax = df_data[x_axis_sel].max()*1.2
    ymax = df_data[y_axis_sel].max()*1.2
    #if st.button("Create Animation"):
    data, frame_list = bubble_chart_config(df_data, year_list_sel, x_axis_sel, y_axis_sel, bubble_size_sel, xmax=xmax, ymax=ymax)
    # Render the chart
    st_vizzu(data, frame_list, c2)