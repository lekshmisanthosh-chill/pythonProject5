import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
alt.data_transformers.disable_max_rows()

def main():

    st.title("Covid visualizer")
    st.markdown(
        "THis is an example eda of covid data solely using python scripts."
        "There are several interesting attributes to consider."
    )

    st.header("Stringency Index and Cases")
    st.subheader('This is a composite measure based on nine response indicators including school closures, workplace closures, '
                 'and travel bans, rescaled to a value from 0 to 100, 100 being strictest')
    # Extract data
    data = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    data['date'] = pd.to_datetime(data.date)
    data['week'] = data['date'].apply(lambda x: x - pd.Timedelta(days=x.weekday()))
    data['week'] = data['week'].dt.date.apply(lambda x: str(x))


    weekly_data = data.groupby(['location', 'week']).agg(
        {'new_cases': 'sum', 'stringency_index': 'max'}).reset_index().dropna()

    max_week = weekly_data.groupby('location').agg({'week': 'max'}).reset_index()
    latest_data = weekly_data.merge(max_week)

    list_of_countries = latest_data['location']

    country_filter = st.selectbox("Select country", list_of_countries, index=0)
    st.markdown('There is some more explanation which I like to give')

    weekly_new_cases = alt.Chart(weekly_data[weekly_data.location == country_filter]).mark_line().encode(x='week:T', y='sum(new_cases)').properties(width=1000, height=500)
    weekly_stringency = alt.Chart(weekly_data[weekly_data.location == country_filter]).mark_bar(color='#CFD8DC', opacity=0.5).encode(x='week:T', y='mean(stringency_index)').properties(width=1000, height=500)

    cases_stringency_corr = alt.Chart(weekly_data[weekly_data.location == country_filter]).mark_point().encode(y='new_cases', x='stringency_index').properties(width=300, height=300)


    final = alt.layer(weekly_stringency, weekly_new_cases).resolve_scale(y = 'independent')

    col1, col2 = st.beta_columns((3, 1))

    col1.write(final)
    col2.markdown('THis is an example where I write additional data with many more analysis. Showing India as an example for visualizzation. There will be'
                  'more and more text to explain how to inteact with this chart and pick a country of choice.'
                  'Add a lot more text to make the point clear and also how to take the data with a grain of salt.')
    col2.write(cases_stringency_corr)



if __name__ == "__main__":
    main()
