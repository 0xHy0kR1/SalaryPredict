import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# Define a function to shorten categories based on a cutoff count.
def shorten_categories(categories, cutoff):
    # Initialize an empty dictionary to store the mapping of categories.
    categorical_map = {}
    # Iterate through the categories.
    for i in range(len(categories)):
        # Check if the count of the category is greater than or equal to the cutoff.
        if categories.values[i] >= cutoff:
            # If yes, keep the original category name.
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            # If not, label the category as "Other".
            categorical_map[categories.index[i]] = 'Other'
    # Return the mapping of categories.
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return "Bachelor's degree"
    if 'Master’s degree' in x:
        return "Master's degree"
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    # Selecting specific columns ("Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly") from the DataFrame.
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    # Renaming the column "ConvertedCompYearly" to "Salary".
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    # Filtering the DataFrame to include only rows where the "Salary" column is not null.
    df = df[df["Salary"].notnull()]
    # Dropping any rows with missing values from the DataFrame.
    df = df.dropna()
    # Filtering the DataFrame to include only rows where the "Employment" column equals "Employed, full-time".
    df = df[df["Employment"] == "Employed, full-time"]

    # Dropping the "Employment" column from the DataFrame.
    df = df.drop("Employment", axis=1)

    # Generate a mapping of countries using the shorten_categories function with a cutoff count of 400.
    country_map = shorten_categories(df.Country.value_counts(), 400)

    # Map the countries in the DataFrame using the generated mapping.
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""
    ### Stack Overflow Developer Survey 2023                
             """)

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write(
        """
    #### Mean Salary Based on Country
        """
    )

    data = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)

    st.bar_chart(data)
    
    st.write(
        """
        #### Mean Salary Based on Experience
        """
    )

    data = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)