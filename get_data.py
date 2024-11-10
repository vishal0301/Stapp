import streamlit as st
import requests
import pandas as pd

# Your Google API Key and CSE ID
API_KEY = 'AIzaSyDj6-Q8AuHXAFmPWF5vELOpOn0wyXZjpXo'  # Replace with your API Key
CSE_ID = '64c42e1bdc7004bc8'  # Replace with your CSE ID

# Function to perform search using Google Programmable Search Engine
def google_search(query, api_key, cse_id, num_results=10):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results  # You can adjust this number (1-10) for each query
    }
    response = requests.get(search_url, params=params)
    return response.json()

# Function to save results to CSV
def save_to_csv(results, filename='ai_tools.csv'):
    data = []
    for item in results['items']:
        data.append({
            "Title": item['title'],
            "Link": item['link'],
            "Snippet": item['snippet']
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

# Streamlit UI
def main():
    st.title("AI Tools, Apps, and Companies Search")

    # Allow user to input a search query
    query = st.text_input("Enter a search query (e.g., AI tools, AI apps, AI companies):", "AI tools, apps, and companies")

    if st.button("Fetch Listings"):
        if query:
            st.write("Fetching data...")

            # Fetch results using Google Custom Search API
            results = google_search(query, API_KEY, CSE_ID)

            # Check if results are found
            if 'items' in results:
                st.success("Data fetched successfully!")
                for item in results['items']:
                    st.write(f"**Title**: {item['title']}")
                    st.write(f"**Link**: {item['link']}")
                    st.write(f"**Snippet**: {item['snippet']}")
                    st.write("\n")

                # Save results to CSV and provide a download button
                filename = save_to_csv(results)
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download CSV",
                        data=file,
                        file_name=filename,
                        mime="text/csv"
                    )
            else:
                st.warning("No results found.")
        else:
            st.warning("Please enter a search query.")
    
    else:
        st.write("Click the button above to fetch listings.")

# Run the app
if __name__ == "__main__":
    main()
