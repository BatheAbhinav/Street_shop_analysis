import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and display JSON data
def load_json(file):
    return json.load(file)

# Function to display business data in a table format
def display_businesses(data):
    df = pd.json_normalize(data['businesses'])
    st.write("### Businesses Data")
    st.dataframe(df)

# Function to visualize the unique categories
def display_category_distribution(data):
    categories = [business['category'] for business in data['businesses']]
    category_count = pd.Series(categories).value_counts()
    
    st.write("### Category Distribution")
    st.bar_chart(category_count)

# Function to show features for businesses in a selected category
def display_features_by_category(data, selected_category):
    filtered_data = [business for business in data['businesses'] if business['category'] == selected_category]
    features = []
    for business in filtered_data:
        features.extend(business['features'])
    
    st.write(f"### Features of {selected_category} Businesses")
    feature_count = pd.Series(features).value_counts()
    st.write(feature_count)

# Streamlit UI
st.title("Business Data Visualization")
st.write("Upload a JSON file to visualize the data.")

uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])

if uploaded_file is not None:
    data = load_json(uploaded_file)
    
    # Display businesses data as a table
    display_businesses(data)
    
    # Display category distribution
    display_category_distribution(data)
    
    # Show a selection for categories to filter features
    unique_categories = data['analysis_summary']['unique_categories']
    selected_category = st.selectbox("Select a category to view features", unique_categories)
    
    if selected_category:
        display_features_by_category(data, selected_category)
    
    # Display the analysis summary
    st.write("### Analysis Summary")
    analysis_summary = data['analysis_summary']
    st.json(analysis_summary)
