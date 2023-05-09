# Snowpark
import streamlit as st
import pandas as pd

from helpers.other_helpers import set_page_config
from helpers.data_helpers import eval_sql, variable_name_options
from helpers.vizzu_helpers import st_vizzu, gapminder_1d_config

set_page_config()

st.title("GapMinder 1D")
st.caption("Plotting time evolution of one variable for multiple countries")

c1, c2 = st.columns(2)

# Provide options
x_axis_options = variable_name_options.copy()
x_axis_sel = c1.selectbox("Dimension", x_axis_options)

# Get the data
df_sql = eval_sql(f"""
    SELECT 
        VARIABLE, VARIABLE_NAME, GEO_ID, date, year(date) as YEAR, VALUE, UNIT
    FROM 
        TIMESERIES
    WHERE
        GEO_ID LIKE 'country%' AND VARIABLE_NAME='{x_axis_sel}'
    ORDER BY 
        DATE asc
""")
df_sql["ISO3"] = df_sql["GEO_ID"].str.split("/").str[1]                  
df_country = pd.read_excel("data/country_codes.xlsx", dtype="str")
df = df_sql.merge(df_country, how="inner", left_on="ISO3", right_on="ISO (3)")

default_values = ["United States", "Chile", "France", "China", "Mexico", "India", "Japan", "Germany"]
country_options = df['Country'].unique().tolist()
filtered_default_values = [x for x in default_values if x in country_options]
country_sel = st.multiselect("Countries", country_options, default=filtered_default_values)

# Subselect the data based on the selected countries
df_sel = df[df['Country'].isin(country_sel)]

# Take average of value for each variable and year, if any duplication
df_sel_avg = df_sel.groupby(['Country', 'Region', 'Continent', 'YEAR', 'VARIABLE_NAME'])['VALUE'].mean().reset_index() 
df_sel_avg = df_sel_avg.sort_values(['VARIABLE_NAME', 'YEAR', 'Country'])
#st.write(df_sel_avg)

# Get the common years between the selected countries
years = set(df_sel_avg['YEAR'].unique().tolist())
for country in country_sel[1:]:
    m = df_sel_avg['Country'] == country
    new_years = set(df_sel_avg[m]['YEAR'].unique().tolist())
    years = years.intersection(new_years)
year_list = sorted(list(years))

# Now we have to pivot the table to have the variables as columns!
df_data_aux = df_sel_avg[df_sel_avg['YEAR'].isin(year_list)]
df_data = df_data_aux.pivot(index=['Country', 'Region', 'Continent', 'YEAR'], columns='VARIABLE_NAME', values='VALUE').reset_index()
#st.write(df_data)

if len(year_list) <= 1:
    st.write("No common years between the selected countries")
else:
    c1, c2 = st.columns(2)
    year_min = min(year_list)
    year_max = max(year_list)
    year_min_sel, year_max_sel = c1.slider("Year range", year_min, year_max, (year_min, year_max))
    year_list_sel = [y for y in year_list if y >= year_min_sel and y <= year_max_sel]
    xmax = df_data[x_axis_sel].max()*1.2
    data, frame_list = gapminder_1d_config(df_data, year_list_sel, x_axis_sel, xmax=xmax)
    # Some Help and info
    with st.expander("Help"):
        mkd = """
        Simply clicking on the "Animation" or "Slide by Slide" buttons to create the corresponding animation. 
        You can change all the properties, and create a different plot.

        Another combinations you might want to try:
        **Who's using my electricity?**
        * X-Axis: "Annual Consumption of Electricity"

        **Is mortality reducing?**
        * X-Axis: "Count of Mortality Event (Per Capita)"
        """
        st.markdown(mkd)


    # Render the chart
    st_vizzu(data, frame_list, c2)


