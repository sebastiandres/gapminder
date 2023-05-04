import streamlit as st
from snowflake.snowpark.session import Session
import iso3166


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

def eval_sql(query):
    # Initialize session, if not already done
    if "session" not in st.session_state:
        st.session_state.session = create_session_object()
    # Eval the query
    snow_data = st.session_state.session.sql(query)
    df_data = snow_data.to_pandas()
    return df_data

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
