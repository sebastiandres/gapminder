import streamlit as st

st.set_page_config(
     page_title="GapMinder App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "A gapminder emulator with free resources"
     }
)

st.title("About")

c1, c2, c3 = st.columns([1,2,1])
mkd = """
This is the comment
"""
c2.markdown(mkd)