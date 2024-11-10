import streamlit as st
import pandas as pd
import requests  # For fetching data from a URL
import os  # To check if file exists

# File path for the CSV file
CSV_FILE_PATH = "data.csv"
FETCH_DATA_URL = "https://clutch.co/"  # Replace with the actual URL

# Load data from CSV file
@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist

# Save data to CSV file
def save_data(data):
    data.to_csv(CSV_FILE_PATH, index=False)

# Fetch data from URL
def fetch_data_from_url(query):
    # Simulate a request to the specified URL (replace with actual request logic)
    response = requests.get(FETCH_DATA_URL, params={"query": query})
    if response.status_code == 200:
        return pd.DataFrame(response.json())  # Assume the response is JSON formatted
    else:
        st.error("Error fetching data from URL.")
        return pd.DataFrame()

# Search function to filter the data
def search_data(data, query):
    # Convert both data and query to lowercase for case-insensitive matching
    filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return filtered_data

# Main Streamlit app function
def main():
    st.title("CSV Search App with Data Fetching")
    
    # Load existing data from CSV file
    data = load_data()
    
    # Display the first few rows of the data if available
    if not data.empty:
        st.subheader("Existing Data Preview")
        st.write(data.head())

    # Search query input
    query = st.text_input("Enter search query")
    
    # Perform search when the query is provided
    if query:
        st.subheader("Search Results")
        results = search_data(data, query)
        
        if not results.empty:
            # Display results found in the CSV file
            st.write("Results found in local CSV:")
            st.write(results)
        else:
            # If no results, fetch data from the specified URL
            st.write("No results found in local CSV. Fetching data from URL...")
            new_data = fetch_data_from_url(query)
            
            if not new_data.empty:
                # Display fetched data
                st.write("Data fetched from URL:")
                st.write(new_data)
                
                # Append new data to existing data and save to CSV
                updated_data = pd.concat([data, new_data], ignore_index=True)
                save_data(updated_data)
                
                st.success("Fetched data has been saved to CSV.")
            else:
                st.write("No data found for the query on the specified URL.")

if __name__ == '__main__':
    main()
