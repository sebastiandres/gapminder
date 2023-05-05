# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="YAG Data Exporer",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
)

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

def eval_sql(session, query):
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    st.write(df_data)
    return df_data

def get_countries(session):
    """
    Using the session, allows to explore the data
    """
    query = """
    SELECT 
        distinct iso_alpha2
    FROM 
        public_holidays
    ORDER BY 
        iso_alpha2 asc
    """
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    return df_data

def get_years(session):
    """
    Using the session, allows to explore the data
    """
    query = """
    SELECT 
        distinct YEAR(date) as year
    FROM 
        public_holidays
    ORDER BY 
        year asc
    """
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    return df_data

def get_measures(session):
    """
    Using the session, allows to explore the data
    """
    query = """
    SELECT 
        distinct variable, variable_name, unit 
    FROM 
        measures
    ORDER BY 
        unit asc
    """
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    return df_data

def public_holiday(session):
    """
    Using the session, allows to explore the data
    """
    query = """
    SELECT 
        distinct id, iso_alpha2
    FROM 
        public_holidays
    """
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    st.write(df_data)   
    return

# Create Snowpark DataFrames that loads data from Knoema: Environmental Data Atlas
def load_data(session):
    #snow_data = session.table("GEO_INDEX")
    snow_data = session.sql("""
    SELECT 
        variable_name, 
        geo_name, 
        geo_id, 
        date,
        value 
    FROM cybersyn.timeseries 
    JOIN cybersyn.geo_index 
    ON timeseries.geo_id = geo_index.id
    WHERE 
        variable ='Count_Person' 
        AND timeseries.geo_id IN ('country/USA', 'country/CAN', 'country/MEX') 
        AND date >= '2000-01-01'
    ORDER BY date desc;
    """)
    df_data = snow_data.to_pandas()
    st.write(df_data)        

def load_table(session, table, nrows=10):
    """
    Using the session, queries the first nrows rows
    """
    query = """
    SELECT 
        *
    FROM 
        {table} 
    LIMIT
        {nrows}
    """.format(table=table, nrows=nrows)
    snow_data = session.sql(query)
    df_data = snow_data.to_pandas()
    st.write(df_data)        


if __name__ == "__main__":
    session = create_session_object()
    #st.write(session)
    #load_data(session)
    #table_options = ["geo_index", "measures", "public_holidays", "timeseries", "variable_summary", "geo_hierarchy"]
    #table_sel = st.selectbox("Select the table", table_options)
    #load_table(session, table_sel)
    #public_holiday(session)
    #countries = get_countries(session)
    #years = get_years(session)
    #st.write(countries)
    #st.write(years)
    #st.write(get_measures(session))
    #st.write(load_table(session, "measures", 1000))
    #st.write(load_table(session, "timeseries", 1000))
    #Good Query, keep it
    df = eval_sql(session, 
    """
    SELECT
        variable, variable_name, count(geo_id) as nrows, count(distinct geo_id) as geo_ids, count(distinct date) as dates
    FROM 
        timeseries
    where 
        geo_id like 'country%'
    group by
        variable, variable_name
    order by
        count(geo_id) desc
    """)
    #df.to_excel("geo_id_country.xlsx")

    df = eval_sql(session, 
    """
    SELECT
        distinct geo_id, count(date) as nrows
    FROM 
        timeseries
    group by
        geo_id
    """)

    #from IPython import embed; embed()
    df2 = df["GEO_ID"].apply(lambda x: x.split('/')[0]).drop_duplicates()
    st.write(df2)


