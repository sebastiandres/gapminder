import streamlit as st

from helpers.other_helpers import set_page_config

set_page_config()

st.title("YAG - Yet Another GapMinder")

st.header("What is this")
mkd = """
I created this app to show the powerful combination of snowflake, streamlit and vizzu, providing an alternative to other visualization tools (*cough cough, PowerBi, cough cough Tableau cough cough*).

This app allows you to explore world data and create stunning animations on 1D or 2D. 
The user can select the variables to plot, thanks to the interactivity provided by Streamlit. 
The data is read in real time from CyberSyn's Data Common (freely available at Snowflake's Marketplace) with SQL queries 
using the snowflake-streamlit connector and renders smooth animations using Vizzu. It makes use of st.cache_data and the snowflake-snowpark-python connector, among other tricks. 

Henceforth the conclusion: A complete gapminder emulator using only free resources and simple code! 
"""
st.markdown(mkd)

st.header("Motivation")

mkd = """
One of my favorite Ted Talks is Hans Rosling's "The best stats you've ever seen". If you haven't already, here's the video for your visual delight:
"""
st.markdown(mkd)
c1, c2, c3 = st.columns([1,3,1])
c2.video("https://www.youtube.com/watch?v=hVimVzgtD6w")
c2.caption("https://www.ted.com/talks/hans_rosling_the_best_stats_you_ve_ever_seen")
mkd = """
This Ted Talk was recorded on 2006! Can you imagine? That's before smartphones era! There was no Streamlit, no Pandas, and Numpy was just being released!

When I first saw this Ted Talk, I was amazed by two things:
* First, the content: world is getting better, and there are some very interesting correlations to learn. 
* Second, the plots and animations! You could do storytelling with data, and create huge impact! 

Doing those animations was probably a huge effort +15 years ago. 
I can easily imagine a team of 3 persons working a couple of months, scrapping the data, coding their way, and making the plots and animations.

Fast forward 2023, and you can do all that WITH FREE RESOURCES in A COUPLE OF DAYS OF CODING after work (my case).
If that's not a strong statement of how technology makes us more productive, I don't know what will ever be.

Anyway. That's it. This is gapminder emulator using Python (streamlit, pandas, ipyvizzu), SQL and Snowflake. Hope you enjoy it and learn something new!
"""
st.markdown(mkd)

st.header("How to use it")
mkd = """
* Use the sidebar to select the page you want to see.
* On GapMinder 1D or 2D, select the variables and configuration you want to plot.
* On Variable Explorer, browse through some preconfigured queries, or write your own to explore the data.
"""
st.markdown(mkd)
