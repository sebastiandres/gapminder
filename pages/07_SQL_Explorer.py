# Snowpark
import streamlit as st

from helpers.data_helpers import set_page_config, eval_sql

set_page_config()

st.title("Table Explorer")

# Get the column structure for all the tables

# Query name and query structure
query_dict = {
"FIRST 10 ROWS": """SELECT * FROM {table_name} LIMIT 10""",
"DISTINCT VALUES FOR EACH COLUMN": "SELECT {distinct_columns} FROM {table_name}",
"NUMBER OF ROWS": "SELECT COUNT(*) AS NROWS FROM {table_name}",
"CUSTOM": ""
}

# Available tables and their columns
table_dict = {
    "TIMESERIES": ["GEO_ID", "VARIABLE", "VARIABLE_NAME", "DATE", "VALUE", "UNIT", "CATEGORY", "MEASUREMENT_METHOD", "PROVENANCE_DOMAIN", "PROVENANCE_URL"],
    "GEO_INDEX": ["ID", "GEO_NAME", "LEVEL", "ISO_NAME", "ISO_ALPHA2", "ISO_ALPHA3", "ISO_NUMERIC_CODE", "ISO_3166_2_CODE"],
    "MEASURES": ["VARIABLE", "VARIABLE_NAME", "CATEGORY", "UNIT"],
    "GEO_HIERARCHY": ["PARENT_GEO_ID", "GEO_ID"],
    "GEO_OVERLAPS": ["GEO_ID", "OVERLAPS_WITH"],
    "PUBLIC_HOLIDAYS": ["ID", "ISO_ALPHA2", "DATE", "HOLIDAY_NAME", "SUBDIVISION", "IS_FINANCIAL"],
}

# Provide options
c1, c2, c3 = st.columns([2,2,1])
query_description = c1.selectbox("Query:", list(query_dict.keys()))
if query_description != "CUSTOM":
    table_name = c2.selectbox("Table:", list(table_dict.keys()))
    c3.markdown("")
    c3.markdown("")
    distinct_columns = ", ".join(f"COUNT( DISTINCT {col})" for col in table_dict[table_name])
    query = query_dict[query_description].format(table_name=table_name, distinct_columns=distinct_columns)
    for word in ["SELECT", "COUNT", "FROM", "WHERE", "ORDER BY", "LIMIT"]:
        query = query.replace(word, "\n"+word)
        query = query.replace("COUNT", " COUNT")    
    st.code(query)
    if c3.button("Execute"):
        df = eval_sql(query)
        st.write(df)
else:
    c1, c3 = st.columns([4,1])
    default_query_text = """SELECT * \nFROM TIMESERIES \nLIMIT 10"""
    user_query = c1.text_area("Query:", value=default_query_text, height=200)
    c3.markdown("")
    c3.markdown("")
    if c3.button("Execute"):
        invalid_keywords = [";", "UPDATE", "DELETE", "INSERT", "CREATE", "ALTER", "RENAME", "TRUNCATE", "GRANT", "REVOKE", "DROP"]
        invalid_query = False
        for keyword in invalid_keywords:
            if keyword.upper() in user_query.upper():
                invalid_query = True or invalid_query
        if invalid_query:
            st.error("Your query seems to have a forbidden keyword. Please avoid the following keywords: " + ", ".join(invalid_keywords)[2:])
        else:
            df = eval_sql(user_query)
            st.write(df)