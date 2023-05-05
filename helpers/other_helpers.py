import streamlit as st

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