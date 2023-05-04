# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget
from streamlit.components.v1 import html
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from helpers.helpers import set_page_config, eval_sql

set_page_config()

st.write("GapMinder Emulator")

# Create Session object
def create_session_object():
    connection_parameters = {
      "account": st.secrets.connections.snowpark["account"],
      "user": st.secrets.connections.snowpark["user"],
      "password": st.secrets.connections.snowpark["password"],
      "role": st.secrets.connections.snowpark["role"],
      "warehouse": st.secrets.connections.snowpark["warehouse"],
      "database": st.secrets.connections.snowpark["database"],
      "schema": st.secrets.connections.snowpark["schema"],
    }
    session = Session.builder.configs(connection_parameters).create()
    #print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
    return session
  
variable_options = [
"FertilityRate_Person_Female",
"LifeExpectancy_Person",
"Count_Person",
"Amount_Debt_Government",
"Amount_Debt_Government_AsAFractionOfGrossDomesticProduction",
"Amount_EconomicActivity_GrossDomesticProduction_Nominal",
"Amount_EconomicActivity_GrossNationalIncome_PurchasingPowerParity",
"Amount_Remittance_InwardRemittance_AsFractionOf_Amount_EconomicActivity_GrossDomesticProduction_Nominal",
"Amount_Remittance_OutwardRemittance",
"Annual_Consumption_Electricity",
"Count_Death_AsAFractionOfCount_Person",
"Count_MedicalConditionIncident_COVID_19_PatientHospitalized",
"Count_MedicalConditionIncident_COVID_19_PatientInICU",
"Count_Person_25To34Years",
"Count_Person_35To44Years",
"Count_Person_45To54Years",
"Count_Person_55To64Years",
"Count_Person_65OrMoreYears",
"Count_Person_Female",
"Count_Person_Male",
"CumulativeCount_MedicalConditionIncident_COVID_19_ConfirmedCase",
"CumulativeCount_Vaccine_COVID_19_Administered",
"GiniIndex_EconomicActivity",
"IncrementalCount_Vaccine_COVID_19_Administered",
"PrecipitationRate",
"PrecipitationRate_RCP85",
"UnemploymentRate_Person",  
]

# Provide options
x_axis_options = variable_options.copy()
x_axis_sel = st.selectbox("X-Axis", x_axis_options)
y_axis_options = x_axis_options.copy()
y_axis_options.remove(x_axis_sel)
y_axis_sel = st.selectbox("Y-Axis", y_axis_options)
bubble_options = y_axis_options.copy()
bubble_options.remove(y_axis_sel)
bubble_size_sel = st.selectbox("Bubble Size", bubble_options)

# Get the data
df = eval_sql(f"""
    SELECT 
        VARIABLE, VARIABLE_NAME, GEO_ID, date, year(date) as YEAR, VALUE, UNIT
    FROM 
        TIMESERIES
    WHERE
        GEO_ID LIKE 'country%' AND VARIABLE in ('{x_axis_sel}', '{y_axis_sel}', '{bubble_size_sel}')
    ORDER BY 
        DATE asc
""")
countries_options = [ _.split("/")[-1] for _ in df['GEO_ID'].unique().tolist()]
countries_sel = st.multiselect("Countries", countries_options)

# Subselect the data based on the selected countries
geo_id_sel = [f"country/{_}" for _ in countries_sel]
df_sel = df[df['GEO_ID'].isin(geo_id_sel)]

# Take average of value for each variable and year, if any duplication
df_sel_avg = df_sel.groupby(['GEO_ID', 'YEAR', 'VARIABLE'])['VALUE'].mean().reset_index() 
#st.write(df_sel_avg)

# Get the common years between the selected countries
years = df_sel_avg[df_sel_avg['GEO_ID'] == geo_id_sel[0]]['YEAR'].unique().tolist()
for geo_id in geo_id_sel[1:]:
    years = list(set(years).intersection(df_sel_avg[df_sel_avg['GEO_ID'] == geo_id]['YEAR'].unique().tolist()))
year_list = sorted(years)
#st.write("The selection has the common years:", years)

# Animate with vizzu
chart = Chart(
    width="640px", height="360px", display=DisplayTarget.MANUAL
)
# create and add data to Chart
data = Data()
data.add_data_frame(df_sel_avg)
chart.animate(data)
# Animate the data for each year
for year in year_list:
    # add config to Chart
    chart.animate(
            Data.filter(
                f"record['YEAR'] == '{year}'"
            ),
        Config.bubbleplot(
            {
                "x": x_axis_sel,
                "y": y_axis_sel,
                "color": "GEO_ID",
                #"dividedBy": "Country",
                "size": bubble_size_sel,
                "title": "Bubble Plot",
            }
        ),

    )

# display Chart
html(chart._repr_html_(), width=650, height=370)
