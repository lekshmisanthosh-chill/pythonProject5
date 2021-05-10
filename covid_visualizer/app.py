import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def main():

    st.title("Covid visualizer")
    st.markdown(
        "THis is an example eda of covid data solely using python scripts."
        "There are several interesting attributes to consider."
    )

    data = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    vaccinations_data = pd.read_csv(
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
        index_col=0,
    )

    agg_data = (
        data[["location", "handwashing_facilities", "life_expectancy"]]
        .groupby(["location"])
        .max()
        .reset_index()
    )

    # Aggregate by week.
    test_chart = (
        alt.Chart(agg_data)
        .mark_circle()
        .encode(x="handwashing_facilities", y="life_expectancy")
        .properties(height=300, width=500)
    )

    test_chart2 = (
        alt.Chart(agg_data)
            .mark_circle(color='orange')
            .encode(x="handwashing_facilities", y="life_expectancy")
            .properties(height=300, width=500, title='Yet another random chart')
    )

    st.write(test_chart)
    st.write(test_chart2)



if __name__ == "__main__":
    main()
