
import ssl
import pandas as pd
import streamlit as st 
from streamlit.components.v1 import html

from ipyvizzustory import Story, Slide, Step
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget

ssl._create_default_https_context = ssl._create_unverified_context


def vizzu_animation(data, frame_list, height):
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
    chart.animate(data, delay=0.0, duration=0.0)
    # add animation frames
    for frame in frame_list:
        chart.animate(*frame, delay=0.25, duration=1.0) # delay = time on slide, duration=animation_duration
    return html(chart._repr_html_(), height=height)


def vizzu_story(data, frame_list, height):
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
    return html(story._repr_html_(), height=height)


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
        vizzu_animation(data, frame_list, height)
    if c2.button("Slide by Slide", type='primary'):
        st.caption("Use the arrows on the tooltip to navigate through the story.")
        vizzu_story(data, frame_list, height)
    return


@st.cache_data
def gapminder_2d_config(df_data, year_list, 
                        x_axis_sel, y_axis_sel, 
                        bubble_size_sel, bubble_color_sel,
                        xmin = 0, xmax = "auto",
                        ymin = 0, ymax = "auto",
                        smin = 0, smax = "auto",
                        ):
    """
    Creates the data and the frame_list to be ready to pass to the vizzu chart.
    """
    print(y_axis_sel)
    # Data to be used
    data = Data()
    data.add_data_frame(df_data)
    # Frames to use in vizzu
    frame_list = []
    # Initial configuration
    frame = (   Style({"legend": {"width": 150}}),
                Config(
                    {
                        "channels": {
                            "x": { "range": {"min": xmin, "max": xmax} },
                            "y": { "range": {"min": ymin, "max": ymax} },
                            "size": { "range": {"min": smin, "max": smax} },
                            "color": bubble_color_sel,
                            "label": "Country",
                        },
                        "title": f"Yearly evolution",
                    }
                ),
            )
    frame_list.append(frame)
    for year in year_list:
        year = str(year)
        frame = (
                    data.filter(
                        f'record["YEAR"] == "{year}"'
                    ),
                    Config(
                        {
                        "channels": {
                                "x": x_axis_sel,
                                "y": y_axis_sel,
                                "size": bubble_size_sel,
                        },
                            "geometry": "circle",
                            "title": f"Year {year}",
                        }
                    ),
                )
        frame_list.append(frame)
    return data, frame_list


@st.cache_data
def gapminder_1d_config(df_data, year_list, 
                        x_axis_sel,
                        xmin = 0, xmax = "auto",
                        ):
    """
    Creates the data and the frame_list to be ready to pass to the vizzu chart.
    """
    # Data to be used
    data = Data()
    data.add_data_frame(df_data)
    # Frames to use in vizzu
    frame_list = []
    # Initial configuration
    frame = (   Style(
                    {"legend": {"width": 0}, "fontSize": "0.75em"}
                ),
                Config(
                    {
                        "channels": {
                            "x": { "range": {"min": xmin, "max": xmax} },
                            "label": "Country",
                            "color": "Country",
                        },
                        "title": f"Yearly evolution",
                    }
                ),
            )

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
                            "y": "Country",
                            "title": f"Year {year}",
                            "channels": {
                                "label": x_axis_sel,
                            },
                            "geometry": "rectangle",
                        }
                    )
                )
        frame_list.append(frame)
    return data, frame_list

if __name__=="__main__":
    test = "gapminder_1d"
    if test=="titanic":
        data_frame = pd.read_csv("data/titanic.csv")
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
        _, col, _ = st.columns([1,4,1])
        st_vizzu(data_frame, frames, col, height=600)
    elif test=="gapminder_2d":
        df_data = pd.read_csv("data/gapminder_2d.csv")
        year_list = ["1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        x_axis_sel = "Fertility Rate"
        y_axis_sel = "Life Expectancy"
        bubble_size_sel = "Total Population"
        bubble_color_sel = "Continent"
        data_frame, frame_list = gapminder_2d_config(df_data, year_list, 
                        x_axis_sel, y_axis_sel, 
                        bubble_size_sel, bubble_color_sel)
        _, col, _ = st.columns([1,4,1])
        st_vizzu(data_frame, frame_list, col, height=600)
    elif test=="gapminder_1d":
        df_data = pd.read_csv("data/gapminder_2d.csv")
        year_list = ["1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        x_axis_sel = "Fertility Rate"
        y_axis_sel = "Life Expectancy"
        bubble_size_sel = "Total Population"
        bubble_color_sel = "Continent"
        data_frame, frame_list = gapminder_1d_config(df_data, year_list, 
                        x_axis_sel)
        _, col, _ = st.columns([1,4,1])
        st_vizzu(data_frame, frame_list, col, height=600)

