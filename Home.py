import streamlit as st

st.set_page_config(
     page_title="GapMinder App",
     page_icon=":globe_with_meridians:",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "A gapminder emulator with free resources"
     }
)

st.title("YAG - Yet Another GapMinder")

st.header("What is this")
mkd = """
This is a interactive app to explore world data and create stunning animations. It provides configuration to the user though Streamlit, 
reads the data from Snowflake and renders animations using Vizzu.
"""
st.markdown(mkd)
c1, c2, c3 = st.columns([1,2,1])
#c2.video("https://www.youtube.com/watch?v=hVimVzgtD6w")
c2.write("EXAMPLE OF ANIMATION")


st.header("Motivation")

mkd = """
One of my favorite Ted Talks is Hans Rosling's "The best stats you've ever seen". If you haven't already, here's the video for your visual delight:
"""
st.markdown(mkd)
c1, c2, c3 = st.columns([1,2,1])
c2.video("https://www.youtube.com/watch?v=hVimVzgtD6w")
c2.caption("https://www.ted.com/talks/hans_rosling_the_best_stats_you_ve_ever_seen")
mkd = """
This Ted Talk was recorded on 2006! Can you imagine? That's before smartphones era!

When I first saw it, it amazed me on two levels:
* First, there's the content: world is getting better, and there are some very interesting correlations to learn. 
* Second, the plots and animations were instrumental to get the impact. I wanted to learn how to create that kind of awe through technical abilities.

Doing that graph, the gapminder, was probably a huge effort 15 years ago. 
I can easily imagine a team of 3 persons working a couple of months, scrapping the data, coding their way, and making the plots.
Fast forward 2023, and you can do all that WITH FREE RESOURCES in A COUPLE OF DAYS OF WORK.
If that's not a strong statement of how technology makes us more productive, I don't know what will ever be.

Anyway. That's it. This is gapminder emulator using Python (streamlit, pandas, ipyvizzu), SQL and Snowflake. 
"""
st.markdown(mkd)