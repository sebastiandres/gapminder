from streamlit.components.v1 import html
import ssl
import streamlit as st 
import pandas as pd
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget
from ipyvizzustory import Story, Slide, Step

ssl._create_default_https_context = ssl._create_unverified_context

button = st.button("Animate", type='primary')

# Story
st.title("Story")
def create_story():
    # Setup data
    data = Data()
    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.15/showcases/titanic/titanic.csv"
    )
    data.add_data_frame(data_frame)    
    # Config
    story = Story(data=data)
    story.set_size(width=650, height=370)
    # First slide
    slide1 = Slide(
                    Step(
                        Config(
                            {
                                "x": "Count",
                                "y": "Sex",
                                "label": "Count",
                                "title": "Passengers of the Titanic",
                            }
                        )
                    )
                )
    # Add the slide to the story
    story.add_slide(slide1)        
    # Second slide
    slide2 = Slide(
                    Step(
                        Config(
                            {
                                "x": ["Count", "Survived"],
                                "label": ["Count", "Survived"],
                                "color": "Survived",
                            }
                        )
                    )
                )
    # Add the slide to the story
    story.add_slide(slide2)        
    # Third slide
    slide3 = Slide(
            Step(Config({"x": "Count", "y": ["Sex", "Survived"]}))
        )
    # Add the slide to the story
    story.add_slide(slide3)
    # Add tooltip
    story.set_feature('tooltip', True)
    # return generated html code
    return story._repr_html_()

# generate Chart's html code
CHART = create_story()
# display Chart
html(CHART, width=650, height=370)
#story.set_size(750, 450)
#html(story._repr_html_(), width=750, height=450)


# Animation
st.title("Animation")

def create_animation():
    # initialize Chart
    chart = Chart(
        width="640px", height="360px", display=DisplayTarget.MANUAL
    )
    # create and add data to Chart
    data = Data()
    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.15/showcases/titanic/titanic.csv"
    )
    data.add_data_frame(data_frame)
    chart.animate(data)
    # add config to Chart
    chart.animate(
        Config(
            {
                "x": "Count",
                "y": "Sex",
                "label": "Count",
                "title": "Passengers of the Titanic",
            }
        )
    )
    chart.animate(
        Config(
            {
                "x": ["Count", "Survived"],
                "label": ["Count", "Survived"],
                "color": "Survived",
            }
        )
    )
    chart.animate(Config({"x": "Count", "y": ["Sex", "Survived"]}))
    # add style to Chart
    chart.animate(Style({"title": {"fontSize": 35}}))
    # return generated html code
    return chart._repr_html_()

# generate Chart's html code
CHART = create_animation()
# display Chart
html(CHART, width=650, height=370)