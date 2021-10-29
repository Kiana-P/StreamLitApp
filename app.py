import streamlit as st
import pandas as pd
import plotly.express as px

#set basic page information
st.set_page_config(layout = "wide")
st.title("Interact with Gapminder Data")

#import data csv file
df_tidy = pd.read_csv("Data/gapminder_tidy.csv")

#organize graph columns into lists
continent_list = list(df_tidy['continent'].unique())
metric_list = list(df_tidy['metric'].unique())
year_list = list(df_tidy['year'].unique())

#dictionary to associate graph variables with english meanings
metric_labels = {"gdpPercap": "GDP Per Capita", "lifeExp": "Average Life Expectancy", "pop": "Population"}

#function to return ditionary values
def format_metric(metric_raw):
    return metric_labels[metric_raw]

#set up sidebar for the first graph
with st.sidebar:
    st.subheader("Configure the plot for Graph 1")
    continent = st.selectbox(label = "Choose a continent", options = continent_list)
    metric = st.selectbox(label = "Choose a metric", options = metric_list, format_func = format_metric)

query = f"continent=='{continent}' & metric=='{metric}'"
df_filtered = df_tidy.query(query)

title = f"{metric_labels[metric]} of countries in {continent}"
fig = px.line(df_filtered, x = "year", y = "value", color = "country", title = title, labels = {"value":f"{metric_labels[metric]}"})

st.plotly_chart(fig, use_container_width=True)

# after the plot is displayed, add some text describing the plot - markdown
st.markdown(f"Graph 1 displays the {metric_labels[metric]} for countries in {continent}")

# after the plot/text is displayed, also display the dataframe used to generate the plot - dataframe
with st.sidebar:
    show_data = st.checkbox(label = "Show the data used to generate Graph 1", value = False)

if show_data:
    st.markdown("This graph was configured using the following data set:")
    st.dataframe(df_filtered)

#set up sidebar for the second graph
with st.sidebar:
    st.subheader("Configure the plot for Graph 2")
    year = str(st.selectbox(label = "Choose a year", options = year_list))
    show_data2 = st.checkbox(label = "Show the data used to generate Graph 2", value = False)

df_all = px.data.gapminder()

query = f"continent=='{continent}' & year=={year}"
df_new = df_all.query(query)
title = f"GDP Per Capita vs. Life Expectancy of countries in {continent} during {year}"
fig2 = px.scatter(df_all.query(query),
                 x= "gdpPercap",
                 y= "lifeExp",
                 size="pop",
                 color="country",
                 hover_name="country", 
                 title = title,
                 log_x=True,
                 size_max=60)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"Graph 2 displays the GDP Per Capita vs. Life Expectancy for countries in {continent} during the year {year}")

if show_data2:
    st.markdown("This graph was configured using the following data set:")
    st.dataframe(df_all)