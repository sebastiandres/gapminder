from streamlit.components.v1 import html
import ssl
import streamlit as st 
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget
from ipyvizzustory import Story, Slide, Step
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

def vizzu_story(data, frame_list):
    """
    Creates a vizzu chart with stories using the frames elements.
    data_frame: a pandas dataframe.
    frame_list: a list of tuples, where the tuple contains
    at least one element of Data, Config or Style.
    width: width of the chart.
    height: height of the chart.
    """
    # Setup data
    if isinstance(data, pd.DataFrame):
        new_data = Data()
        new_data.add_data_frame(data)
        data = new_data
    # Config
    story = Story(data=data)
    for frame in frame_list:
        slide = Slide(Step(*frame))
        story.add_slide(slide)        
    # Add tooltip
    story.set_feature('tooltip', True)
    return story._repr_html_()


def vizzu_animation(data, frame_list):
    """
    Creates a vizzu chart with animation using the frames elements.
    data_frame: a pandas dataframe.
    frame_list: a list of tuples, where the tuple contains
    at least one element of Data, Config or Style.
    width: width of the chart.
    height: height of the chart.
    """
    # create and add data to Chart
    if isinstance(data, pd.DataFrame):
        new_data = Data()
        new_data.add_data_frame(data)
        data = new_data
    # initialize Chart
    chart = Chart(width=f"100%", display=DisplayTarget.MANUAL)
    # Animation
    chart.animate(data)
    # add animation frames
    for frame in frame_list:
        chart.animate(*frame)
    return chart._repr_html_()


def st_vizzu(data, frame_list, col=None, height=800):
    """
    Creates a vizzu chart using story or animation.
    data_frame: a pandas dataframe.
    frame_list: a list of tuples, where the tuple contains
    at least one element of Data, Config or Style.
    width: width of the chart.
    height: height of the chart.
    """
    _, c1, c2, _ = col.columns([1,2,2,1])
    if c1.button("Animation", type='primary'):
        html(vizzu_animation(data, frame_list), height=height)
    if c2.button("Slide by Slide", type='primary'):
        html(vizzu_story(data, frame_list), height=height)
        st.caption("Use the arrows on the tooltip to navigate through the story.")
    #else:
    return


@st.cache_data
def bubble_chart_config(df_data, year_list, x_axis_sel, y_axis_sel, bubble_size_sel,
                        xmin = "auto", xmax = "auto", ymin = "auto", ymax = "auto"):
    """
    Creates the data and the frame_list to be ready to pass to the vizzu chart.
    """
    # Data to be used
    data = Data()
    data.add_data_frame(df_data)
    # Frames to use in vizzu
    frame_list = []
    # Initial configuration
    frame = (
                Config(
                    {
                        "channels": {
                            "x": { "range": {"min": xmin, "max": xmax},  },
                            "y": { "range": {"min": ymin, "max": ymax} },
                            "color": "GEO_ID",
                            #"label": "GEO_ID",
                        },
                        "geometry": "circle",
                        "title": f"Yearly evolution",
                    }
                ),
            )
    frame_list.append(frame)
    # Data
    for year in year_list:
        # add config to Chart
        frame = (
                    data.filter(
                        f'record["YEAR"] == "{year}"'
                    ),
                    Config(
                        {
                            "x": x_axis_sel,
                            "y": y_axis_sel,
                            "channels": {
                                "size": bubble_size_sel,
                                #"label": False,
                            },
                            "title": f"Year {year}",
                        }
                    ),
                )
        frame_list.append(frame)
    return data, frame_list

if __name__=="__main__":
    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.15/showcases/titanic/titanic.csv"
    )
    frames = [
                (
                    Config(
                        {
                            "x": "Count",
                            "y": "Sex",
                            "label": "Count",
                            "title": "Passengers of the Titanic",
                        }
                    ),
                ),
                (
                    Config(
                        {
                            "x": ["Count", "Survived"],
                            "label": ["Count", "Survived"],
                            "color": "Survived",
                        }
                    ), 
                ),
                (
                    Config({"x": "Count", "y": ["Sex", "Survived"]}),
                )
    ]

    st_vizzu(data_frame, frames, width=650, height=370)