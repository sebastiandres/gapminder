import streamlit as st
from snowflake.snowpark.session import Session
import iso3166

variable_name_options = [
"Fertility Rate",
"Life Expectancy",
"Population",
"Population: Male",
"Population: Female",
"Unemployment Rate",
"Amount of Debt: Government (As Fraction of Gross Domestic Production)",
"Amount of Debt: Government",
"Population Density",
"Cumulative Count of Medical Condition Incident: COVID-19, Confirmed Case",
"Count of Medical Condition Incident: COVID-19, Patient Hospitalized",
"Precipitation Rate: Based on RCP 8.5",
"Count of Medical Condition Incident: COVID-19, Patient in ICU",
"Cumulative Count of Vaccine: COVID-19, Vaccine Administered",
"Incremental Count of Vaccine: COVID-19, Vaccine Administered",
"Precipitation Rate",
"Amount of Economic Activity (Nominal): Gross Domestic Production",
"Count of Mortality Event (Per Capita)",
"Amount of Remittance: Outward Remittance",
"Amount of Remittance: Inward Remittance (As Fraction of Amount Economic Activity Gross Domestic Production Nominal)",
"Gini Index of Economic Activity",
"Amount of Economic Activity (Purchasing Power Parity): Gross National Income",
"Population: 65 Years or More",
"Annual Consumption of Electricity",
"Population: 45 - 54 Years",
"Population: 55 - 64 Years",
"Population: 25 - 34 Years",
"Population: 35 - 44 Years",
"Amount of Economic Activity (Nominal): Gross Domestic Production, EUR",
"Amount of Economic Activity (Nominal): Gross Domestic Production, National Currency",
"Amount of Economic Activity (Nominal): Gross Domestic Production, Purchasing Power Standard",
"Amount of Economic Activity (Nominal): Gross Domestic Production (Per Capita), EUR",
"Amount of Economic Activity (Nominal): Gross Domestic Production (Per Capita), Purchasing Power Standard",
"Count of Mortality Event (Age Adjusted) (Per Capita)",
]    

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

def set_page_config(page_title="GapMinder App", page_icon=":globe_with_meridians:"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "A gapminder emulator with free resources"
        }
    )    

@st.cache_data
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
    return session


@st.cache_data
def eval_sql(query):
    # Initialize session, if not already done
    if "session" not in st.session_state:
        st.session_state.session = create_session_object()
    # Eval the query
    snow_data = st.session_state.session.sql(query)
    df_data = snow_data.to_pandas()
    return df_data


@st.cache_data
def flag_emoji(name):
    """
    Courtesy of: https://www.johndcook.com/blog/2022/10/02/flags-unicode/
    """
    try:
        alpha = iso3166.countries.get(name).alpha2
        box = lambda ch: chr( ord(ch) + 0x1f1a5 )
        return box(alpha[0]) + box(alpha[1])
    except:
        return "?"

if __name__ == "__main__":
    print(flag_emoji(name="Chile"))
    print(flag_emoji(name="CL"))
    print(flag_emoji(name="CHL"))
    print(flag_emoji(name='152'))
