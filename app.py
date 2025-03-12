import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="Students Performance", page_icon=":bar_chart:", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
options = ["Home", "Data Visualization", "Advanced Analysis"]
choice = st.sidebar.radio("Go to", options)

# Path to the dataset
file_path = r"D:\1.DA Projects\student_perfomance\Cleaned_Students_Performance.csv"

# Read the dataset
df = pd.read_csv(file_path)

if choice == "Home":
    st.title(" :bar_chart: Students Performance EDA")
    st.write("### Data Preview")
    st.write(df.head())

    st.write("### Descriptive Statistics")
    st.write(df.describe())

    # Feature to select the number of rows to display
    st.sidebar.header("Display Options")
    num_rows = st.sidebar.slider("Select number of rows to display", min_value=5, max_value=len(df), value=10)
    st.write(f"### Displaying first {num_rows} rows of the dataset")
    st.write(df.head(num_rows))

elif choice == "Data Visualization":
    st.title("Data Visualization")

    # Sidebar filters
    st.sidebar.header("Filter Options")

    gender = st.sidebar.multiselect("Select Gender", options=df["gender"].unique(), default=df["gender"].unique())
    race = st.sidebar.multiselect("Select Race/Ethnicity", options=df["race_ethnicity"].unique(), default=df["race_ethnicity"].unique())
    education = st.sidebar.multiselect("Select Parental Level of Education", options=df["parental_level_of_education"].unique(), default=df["parental_level_of_education"].unique())

    filtered_df = df[(df["gender"].isin(gender)) & (df["race_ethnicity"].isin(race)) & (df["parental_level_of_education"].isin(education))]

    st.write("### Filtered Data Preview")
    st.write(filtered_df.head())

    # Gender-wise score distribution
    st.write("### Score Distribution by Gender")
    fig = px.histogram(filtered_df, x="math_score", color="gender", barmode="group", title="Distribution of Math Scores by Gender")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(filtered_df, x="reading_score", color="gender", barmode="group", title="Distribution of Reading Scores by Gender")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(filtered_df, x="writing_score", color="gender", barmode="group", title="Distribution of Writing Scores by Gender")
    st.plotly_chart(fig, use_container_width=True)

    # Scores by race/ethnicity
    st.write("### Average Scores by Race/Ethnicity")
    numeric_columns = ["math_score", "reading_score", "writing_score", "total_score", "average_score"]
    avg_scores_race = filtered_df.groupby('race_ethnicity')[numeric_columns].mean()
    st.write(avg_scores_race)

    fig = px.bar(avg_scores_race.reset_index(), x="race_ethnicity", y=["math_score", "reading_score", "writing_score"], barmode="group", title="Average Scores by Race/Ethnicity", labels={'value': 'Average Score', 'variable': 'Subject'})
    st.plotly_chart(fig, use_container_width=True)

    # Scores by parental level of education
    st.write("### Average Scores by Parental Level of Education")
    avg_scores_education = filtered_df.groupby('parental_level_of_education')[numeric_columns].mean()
    st.write(avg_scores_education)

    fig = px.bar(avg_scores_education.reset_index(), x="parental_level_of_education", y=["math_score", "reading_score", "writing_score"], barmode="group", title="Average Scores by Parental Level of Education", labels={'value': 'Average Score', 'variable': 'Subject'})
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Advanced Analysis":
    st.title("Advanced Analysis")

    # Scores by lunch type
    st.write("### Scores by Lunch Type")
    fig = px.box(df, x="lunch", y="total_score", points="all", title="Total Scores by Lunch Type")
    st.plotly_chart(fig, use_container_width=True)

    # Scores by test preparation course
    st.write("### Scores by Test Preparation Course")
    fig = px.box(df, x="test_preparation_course", y="total_score", points="all", title="Total Scores by Test Preparation Course")
    st.plotly_chart(fig, use_container_width=True)

    # Relationship between math and reading scores
    st.write("### Relationship between Math and Reading Scores")
    fig = px.scatter(df, x="math_score", y="reading_score", color="gender", title="Math Score vs Reading Score")
    st.plotly_chart(fig, use_container_width=True)

    # Relationship between math and writing scores
    st.write("### Relationship between Math and Writing Scores")
    fig = px.scatter(df, x="math_score", y="writing_score", color="gender", title="Math Score vs Writing Score")
    st.plotly_chart(fig, use_container_width=True)

    # Scatter plot matrix for scores
    st.write("### Scatter Plot Matrix for Scores")
    fig = px.scatter_matrix(df, dimensions=["math_score", "reading_score", "writing_score"], color="gender", title="Scatter Plot Matrix for Scores")
    st.plotly_chart(fig, use_container_width=True)

# Download original DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Cleaned_Students_Performance.csv", mime="text/csv")

