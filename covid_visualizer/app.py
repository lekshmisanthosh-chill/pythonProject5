import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import altair as alt


st.set_page_config(layout="wide")
alt.data_transformers.disable_max_rows()


def plot_scatter_with_regression(x_col, source, y_col="death_per_population_pct"):
    scatter = (
        alt.Chart(source)
        .mark_circle(color="#E57373")
        .encode(x=x_col, y=y_col)
        .properties(width=400, height=200, title=f"Death per population % by {x_col}")
    )
    regression = scatter.transform_regression(x_col, y_col).mark_line(
        color="#E57373", opacity=0.4
    )
    return scatter + regression


def main():

    # Extract data
    data = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    data["date"] = pd.to_datetime(data.date)
    data["week"] = data["date"].apply(lambda x: x - pd.Timedelta(days=x.weekday()))
    data["week"] = data["week"].dt.date.apply(lambda x: str(x))

    # Aggregate data
    # Weekly aggregation
    weekly_data = (
        data.groupby(["location", "week"])
        .agg(
            {
                "new_cases": "sum",
                "stringency_index": "max",
                "total_deaths": "max",
                "population": "max",
                "total_tests": "max",
            }
        )
        .reset_index()
        .dropna()
    )
    # Latest snapshot
    max_week = weekly_data.groupby("location").agg({"week": "max"}).reset_index()
    latest_data = weekly_data.merge(max_week)
    latest_data["death_per_population_pct"] = (
        latest_data["total_deaths"] * 100 / latest_data["population"]
    )
    latest_data["tests_per_population"] = (
        latest_data["total_tests"] / latest_data["population"]
    )

    list_of_countries = latest_data["location"]

    # Country dimension table
    country_dimension = (
        data.groupby(["location"])
        .agg(
            {
                "median_age": "max",
                "aged_65_older": "max",
                "aged_70_older": "max",
                "gdp_per_capita": "max",
                "cardiovasc_death_rate": "max",
                "diabetes_prevalence": "max",
                "female_smokers": "max",
                "male_smokers": "max",
                "handwashing_facilities": "max",
                "life_expectancy": "max",
                "human_development_index": "max",
            }
        )
        .reset_index()
    )

    country_dimension = country_dimension.merge(
        latest_data[["location", "death_per_population_pct", "tests_per_population"]],
        how="left",
    )

    # Plot dashboards
    st.title("Covid visualizer")
    st.markdown(
        "THis is an example eda of covid data solely using python scripts."
        "There are several interesting attributes to consider."
    )

    st.header("Stringency Index and Cases")
    st.subheader(
        "This is a composite measure based on nine response indicators including school closures, workplace closures, "
        "and travel bans, rescaled to a value from 0 to 100, 100 being strictest"
    )

    country_filter = st.selectbox("Select country", list_of_countries, index=0)
    st.markdown("There is some more explanation which I like to give")

    weekly_new_cases = (
        alt.Chart(weekly_data[weekly_data.location == country_filter])
        .mark_line()
        .encode(x="week:T", y="sum(new_cases)")
        .properties(width=1000, height=500)
    )
    weekly_stringency = (
        alt.Chart(weekly_data[weekly_data.location == country_filter])
        .mark_bar(color="#CFD8DC", opacity=0.5)
        .encode(x="week:T", y="mean(stringency_index)")
        .properties(width=1000, height=500)
    )

    cases_stringency_corr = (
        alt.Chart(weekly_data[weekly_data.location == country_filter])
        .mark_point()
        .encode(y="new_cases", x="stringency_index")
        .properties(width=300, height=300)
    )

    final = alt.layer(weekly_stringency, weekly_new_cases).resolve_scale(
        y="independent"
    )

    col1, col2 = st.beta_columns((3, 1))

    col1.write(final)
    col2.markdown(
        "THis is an example where I write additional data with many more analysis. Showing India as an example for visualizzation. There will be"
        "more and more text to explain how to inteact with this chart and pick a country of choice."
        "Add a lot more text to make the point clear and also how to take the data with a grain of salt."
    )
    col2.write(cases_stringency_corr)

    # Plot Section 2
    st.header("Death % against various socioeconomic variables")
    st.subheader("Scatterplot grid show several values")
    grid = alt.vconcat(
        alt.hconcat(
            plot_scatter_with_regression("median_age", source=country_dimension),
            plot_scatter_with_regression("gdp_per_capita", source=country_dimension),
        ),
        alt.hconcat(
            plot_scatter_with_regression(
                "cardiovasc_death_rate", source=country_dimension
            ),
            plot_scatter_with_regression(
                "diabetes_prevalence", source=country_dimension
            ),
        ),
        alt.hconcat(
            plot_scatter_with_regression(
                "handwashing_facilities", source=country_dimension
            ),
            plot_scatter_with_regression(
                "human_development_index", source=country_dimension
            ),
        ),
    )

    col1, col2 = st.beta_columns((3, 1))
    col1.write(grid)
    col2.markdown("Here is where the explanation goes by each chart")

    # Plot section 3

    st.header("Testing and gdc per capita")
    st.subheader("Scatterplot grid show several values")

    test_by_gdp = country_dimension[
        ["location", "gdp_per_capita", "tests_per_population"]
    ].dropna()

    test_by_gdp = test_by_gdp.sort_values('tests_per_population', ascending=False).iloc[:60, ]

    tests_chart = (
        alt.Chart(test_by_gdp)
        .mark_bar()
        .encode(
            x=alt.X("location", sort="-y"),
            y="tests_per_population",
            color="gdp_per_capita",
        )
    ).properties(height=500)

    st.write(tests_chart)


if __name__ == "__main__":
    main()
