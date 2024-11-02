import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

# Set up API connection
API_KEY = 'AIzaSyDj6-Q8AuHXAFmPWF5vELOpOn0wyXZjpXo'  # Replace with your actual Google API Key
CX = '64c42e1bdc7004bc8'  # Replace with your Custom Search Engine ID

def search_google(query):
    """Fetch top search results from Google Custom Search."""
    service = build("customsearch", "v1", developerKey=API_KEY)
    response = service.cse().list(q=query, cx=CX, num=10).execute()
    return response.get('items', [])

def display_results(results):
    """Display search results in a Streamlit app."""
    data = []
    for item in results:
        data.append({
            "Title": item.get("title"),
            "Link": item.get("link"),
            "Snippet": item.get("snippet"),
        })
    return pd.DataFrame(data)

# Streamlit UI
st.title("AIvigator")
st.write("Enter a search term to find the latest AI apps and tools from Google.")

# Search input
query = st.text_input("Search Query", value="Top AI tools")

# Perform search and display results
if st.button("Search"):
    if query:
        results = search_google(query)
        if results:
            results_df = display_results(results)
            st.write("**Top Search Results:**")
            st.table(results_df)
        else:
            st.error("No results found. Try another search term.")
    else:
        st.warning("Please enter a search term.")
