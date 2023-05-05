import streamlit as st
from streamlit_extras.mention import mention
from helpers.helpers import set_page_config

set_page_config("YAG - About")

st.title("About")

mkd="""
<span style='color:grey'>
If I have <s>SEEN</s> *CODED* further, it is by standing on the shoulders of giants.
<br>
<em>- Sir Issac Newton, had he lived on the 21st century.</em>
</span>
<br>
<br>"""
st.markdown(mkd, unsafe_allow_html=True)

mkd = """
Though I'm really proud of this piece of code, I am I'm humbled by the fact that I would have no idea of how to code it on another language, 
or without one of the following libraries: streamlit, pandas, ipyvizzu, snowflake. A huge thanks to the teams behind them, the work they do 
is amazing and we unfairly take it for granted.

I guess it all boils down to the following conversation I had with my kid:
> Dad, so programers just do a bit of copy and paste code they google and then it works? 
>
> Of course not. You have to think a lot. Define the WHAT, the HOW, the WHY. And copy and paste A LOT of code.
"""
st.markdown(mkd)

st.header("About me")
tw_mention = mention(label="twitter", icon="twitter", url="https://www.twitter.com/sebastiandres", write=False)
gh_mention = mention(label="github", icon="github", url="https://github.com/sebastiandres/", write=False)
li_mention = mention(label="linkedin", icon="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg", 
                     url="https://www.linkedin.com/in/sebastiandres/", write=False)
hp_mention = mention(label="blog", icon=":globe_with_meridians:", url="https://sebastiandres.xyz/", write=False)
mkd = f"""
My name is Sebastian Flores, but you can find me as sebastiandres on the internet. 
I'm a data scientist and I live in Viña del Mar, Chile. 
While a bit introvert, I'd love to connect with like-minded people, so feel free to reach out to me on any of the following platforms:
<ul>
<li> {tw_mention} </li>
<li> {gh_mention} </li>
<li> {li_mention} </li>
<li> {hp_mention} </li>
</ul>
"""
st.write(mkd, unsafe_allow_html=True)

st.header("About the Code")
mkd = """
The code is available on GitHub at [https://github.com/sebastiandres/gapminder](https://github.com/sebastiandres/gapminder). 

Feel free to use it, modify it, learn from it, and share it.
"""
st.markdown(mkd)

st.header("Resources")
mkd = """
* [Streamlit](https://streamlit.io/): The app is built on top of streamlit. It's a great tool to build interactive apps with Python.
    * [Streamlit Extras](https://extras.streamlit.app/): The app uses the mention component from Streamlit Extras.
* [ipyvizzu](https://ipyvizzu.vizzuhq.com/): The animations are rendered using ipyvizzu, a Python wrapper for Vizzu.
    * [Blog post by Peter Vidos](https://blog.streamlit.io/create-an-animated-data-story-with-ipyvizzu-and-streamlit/)
    * [Streamlit app showcasing ipyvizzy by Avra](https://hellostvizzu.streamlit.app/)
    * [Kaggle post by Atri Saxena](https://www.kaggle.com/code/atrisaxena/animated-way-of-visualization-ipyvizzu)
* [Snowflake](https://www.snowflake.com/): The data is stored on Snowflake, a cloud data platform. 
    * [Medium post by Data Professor](https://towardsdatascience.com/how-to-connect-streamlit-to-snowflake-b93256d80a40)
    * [Getting Started With Snowpark for Python and Streamlit](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html)
    * [Connecting Streamlit to Snowflake](https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake)
* Cybersyn, the data-as-a-service company that provides the data for this app.
    * [Cybersyn on Snowflake Marketplace](https://app.snowflake.com/marketplace/listings/Cybersyn%2C%20Inc): Other datasets are available on the Snowflake Marketplace.
    * [Data Commons](https://app.snowflake.com/marketplace/listing/GZTSZAS2KCS/cybersyn-inc-data-commons-public-data): The dataset used. Public and free to use, you can find it on the Snowflake Marketplace.
    * [A Streamlit app to explore the Data Commons dataset](https://cybersyn-datacommons.streamlit.app/Time_Series) 
And for sure I'm forgetting many other resources that I did not kept track of.
"""
st.markdown(mkd)



