from st_vizzu import *
import pandas as pd
import streamlit as st

# Load Data
df = pd.read_csv("Data/music_data.csv", index_col=0)
# Create ipyvizzu Object with the DataFrame
obj = create_vizzu_obj(df)

# Preset plot usage. Preset plots works directly with DataFrames.
bar_obj = bar_chart(df,
            x = "Kinds", 
            y = "Popularity",
            title= "1.Using preset plot function `bar_chart()`"
            )

# Animate with defined arguments 
anim_obj = beta_vizzu_animate( bar_obj,
    x = "Genres",
    y =  ["Popularity", "Kinds"],
    title = "Animate with beta_vizzu_animate () function",
    label= "Popularity",
    color="Genres",
    legend="color",
    sort="byValue",
    reverse=True,
    align="center",
    split=False,
)

# Animate with general dict based arguments 
_dict = {"size": {"set": "Popularity"}, 
    "geometry": "circle",
    "coordSystem": "polar",
    "title": "Animate with vizzu_animate () function",
    }
anim_obj2 = vizzu_animate(anim_obj,_dict)

# Visualize within Streamlit
with st.container(): # Maintaining the aspect ratio
    st.button("Animate")
    vizzu_plot(anim_obj2)