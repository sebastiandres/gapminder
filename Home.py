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

st.title("GapMinder")

mkd = """
This is the comment
"""
st.markdown(mkd)
c1, c2, c3 = st.columns([1,2,1])
c2.video("https://www.youtube.com/watch?v=hVimVzgtD6w")

mkd = """
This is the comment
"""
st.markdown(mkd)