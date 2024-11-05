#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data from CSV file
df = pd.read_csv('modified_dataset.csv')

# Main title
st.title("🏆 Summer Olympics(1896-2024) Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.write("Use the navigation below to explore different sections:")

# Sidebar tabs (as a radio selection)
page = st.sidebar.radio("Select a Section", [
    "Medal Count by Country", 
    "Performance by Gender", 
    "Medal Trends Over Time", 
    "Top Medalists", 
    "Most Popular Sports", 
    "Top 5 Countries Over Time", 
    "Medal Distribution by Gender and Sport", 
    "Top 10 Athletes by Medals", 
    "Fun Facts"
])

# Sidebar filters
st.sidebar.title("🔎 Filters")
selected_year = st.sidebar.slider("Select Year Range", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=(int(df["Year"].min()), int(df["Year"].max())))
selected_gender = st.sidebar.multiselect("Select Gender", options=df["Sex"].unique(), default=df["Sex"].unique())
selected_medal = st.sidebar.multiselect("Select Medal Type", options=df["Medal"].unique(), default=["Gold", "Silver", "Bronze"])
selected_sport = st.sidebar.multiselect("Select Sport", options=df["Sport"].unique(), default=df["Sport"].unique())
selected_country = st.sidebar.multiselect("Select Country", options=df["Country"].unique(), default=df["Country"].unique())

# Apply filters to the dataframe
df_filtered = df[
    (df["Year"] >= selected_year[0]) & (df["Year"] <= selected_year[1]) &
    (df["Sex"].isin(selected_gender)) &
    (df["Country"].isin(selected_country)) &
    (df["Medal"].isin(selected_medal)) &
    (df["Sport"].isin(selected_sport))
]

# Page content based on selected tab
if page == "Medal Count by Country":
    st.subheader("🥇 Medal Count by Country")
    medal_count = df_filtered[df_filtered["Medal"] != "No medal"].groupby("Country")["Medal"].count().sort_values(ascending=False)
    fig1 = px.bar(medal_count, x=medal_count.index, y="Medal", labels={'x': 'Country', 'y': 'Medal Count'})
    st.plotly_chart(fig1)

elif page == "Performance by Gender":
    st.subheader("👫 Performance by Gender")
    gender_medal_count = df_filtered[df_filtered["Medal"] != "No medal"].groupby("Sex")["Medal"].count()
    fig2 = px.pie(gender_medal_count, names=gender_medal_count.index, values="Medal")
    st.plotly_chart(fig2)

elif page == "Medal Trends Over Time":
    st.subheader("📈 Medal Trends Over Time")
    trend = df_filtered[df_filtered["Medal"] != "No medal"].groupby("Year")["Medal"].count()
    fig3 = px.line(trend, x=trend.index, y="Medal", labels={'x': 'Year', 'y': 'Medal Count'})
    st.plotly_chart(fig3)

elif page == "Top Medalists":
    st.subheader("🏅 Top Medalists")
    top_medalists = df_filtered[df_filtered["Medal"] != "No medal"].groupby("Name")["Medal"].count().sort_values(ascending=False).head(10)
    fig4 = px.bar(top_medalists, x=top_medalists.index, y="Medal", labels={'x': 'Athlete', 'y': 'Medal Count'})
    st.plotly_chart(fig4)

elif page == "Most Popular Sports":
    st.subheader("🏋️ Most Popular Sports")
    sport_count = df_filtered.groupby("Sport")["Event"].count().sort_values(ascending=False).head(10)
    fig5 = px.bar(sport_count, x=sport_count.values, y=sport_count.index, orientation='h', labels={'x': 'Event Count', 'y': 'Sport'})
    st.plotly_chart(fig5)

elif page == "Top 5 Countries Over Time":
    st.subheader("Top 5 Countries Over Time")
    top_5_countries = df[df['Medal'] != 'No medal']['Country'].value_counts().head(5).index
    filtered_df = df[(df['Medal'] != 'No medal') & (df['Country'].isin(top_5_countries))]
    medals_cumulative = filtered_df.groupby(['Year', 'Country']).size().unstack(fill_value=0).cumsum()
    fig6 = go.Figure()
    for country in top_5_countries:
        fig6.add_trace(go.Scatter(
            x=medals_cumulative.index,
            y=medals_cumulative[country],
            mode='lines+markers',
            name=country
        ))
    fig6.update_layout(
        xaxis_title='Year',
        yaxis_title='Cumulative Number of Medals',
        xaxis=dict(tickmode='linear', dtick=4),
        yaxis=dict(tickformat="d")
    )
    st.plotly_chart(fig6)

elif page == "Medal Distribution by Gender and Sport":
    st.subheader("Medal Distribution by Gender and Sport")
    medals_by_gender_sport = df[df['Medal'] != 'No medal'].groupby(['Sport', 'Sex']).size().reset_index(name='Count')
    fig7 = px.bar(
        medals_by_gender_sport,
        x='Sport',
        y='Count',
        color='Sex',
        barmode='group',
        labels={'Count': 'Number of Medals', 'Sport': 'Sport', 'Sex': 'Gender'}
    )
    fig7.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig7)

elif page == "Top 10 Athletes by Medals":
    st.subheader("Top 10 Athletes by Medals")
    top_athletes = df[df['Medal'] != 'No medal'].groupby(['Name', 'Medal']).size().unstack(fill_value=0).reset_index()
    top_athletes['Total'] = top_athletes[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    top_10_athletes = top_athletes.sort_values('Total', ascending=False).head(10)
    top_10_athletes_melted = top_10_athletes.melt(id_vars=['Name'], value_vars=['Gold', 'Silver', 'Bronze'], var_name='Medal', value_name='Count')
    fig8 = px.bar(
        top_10_athletes_melted,
        x='Count',
        y='Name',
        color='Medal',
        orientation='h',
        labels={'Count': 'Number of Medals', 'Name': 'Athlete'},
        color_discrete_map={'Gold':'#FFD700', 'Silver':'#C0C0C0', 'Bronze':'#CD7F32'}
    )
    fig8.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig8)

elif page == "Fun Facts":
    st.subheader("✨ Fun Facts about the Olympics")
    st.write("- The Tug-of-War was once an Olympic event!")
    st.write("- Edgar Aabye from Denmark won a gold medal in the Tug-of-War event.")
    st.write("- Some countries like India and China have shown rapid improvement in medal counts over the years.")
    st.write("- Did you know? The longest Olympic event in history was the marathon run by Dorando Pietri in 1908, which took him nearly three hours!")

# Video embedding
st.video("https://www.youtube.com/watch?v=YtyXgRFa5Qo&t=51s")


# In[ ]:





# In[ ]:




