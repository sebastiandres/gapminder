# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Environment Data Atlas",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
)

st.write("Snowflake had a little lamb")
# Create Session object
def create_session_object():
    connection_parameters = {
      "account": st.secrets["connections"]["snowpark"]["account"],
      "user": st.secrets["connections"]["snowpark"]["user"],
      "password": st.secrets["connections"]["snowpark"]["password"],
      "role": st.secrets["connections"]["snowpark"]["role"],
      "warehouse": st.secrets["connections"]["snowpark"]["warehouse"],
      "database": st.secrets["connections"]["snowpark"]["database"],
      "schema": st.secrets["connections"]["snowpark"]["schema"],
    }
    session = Session.builder.configs(connection_parameters).create()
    #print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
    return session
  
# Create Snowpark DataFrames that loads data from Knoema: Environmental Data Atlas
def load_data(session):
    snow_data = session.table("MYTABLE")
    df_data = snow_data.to_pandas()
    st.write(df_data)        

if __name__ == "__main__":
    session = create_session_object()
    #st.write(session)
    load_data(session)