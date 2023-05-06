# YAG - Yet Another Gapminder

Link: [https://gapminder.streamlit.app/](https://gapminder.streamlit.app/)

I created this app to show the powerful combination of snowflake, streamlit and vizzu, providing an alternative to other visualization tools (cough cough, PowerBi, cough cough Tableau cough cough).

This app allows you to explore world data and create stunning animations on 1D or 2D. The user can select the variables to plot, thanks to the interactivity provided by Streamlit. The data is read in real time from CyberSyn's Data Common (freely available at Snowflake's Marketplace) with SQL queries using the snowflake-streamlit connector and renders smooth animations using Vizzu. It makes use of st.cache_data, st.cache_resource, and the snowflake-snowpark-python connector, among other tricks.

Henceforth the conclusion: A complete gapminder emulator using only free resources and simple code!
