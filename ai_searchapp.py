import streamlit as st
import requests

# Replace with your actual Google API Key and Search Engine ID
API_KEY = "YOUR_GOOGLE_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

st.title("AI Apps, Tools, and Companies Search")
st.write("Search for AI apps, tools, and companies to see details like logo, name, description, website, functionality, and reviews.")

# Query input
query = st.text_input("Enter your search query")

if query:
    # Function to search using Google Custom Search JSON API
    def search_google(query):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url)
        return response.json()

    # Display search results
    results = search_google(query)

    if "items" in results:
        for item in results["items"]:
            title = item.get("title")
            snippet = item.get("snippet")
            link = item.get("link")
            pagemap = item.get("pagemap", {})

            # Extract logo if available
            logo_url = pagemap["cse_image"][0]["src"] if "cse_image" in pagemap else "https://via.placeholder.com/80"

            # Simulating additional fields for the example
            rating = 4.5  # Placeholder rating
            reviews = 42  # Placeholder number of reviews
            verified = True  # Placeholder verification status
            summary = snippet  # Use snippet as a placeholder summary
            budget = "$25,000+"  # Placeholder budget
            hourly_rate = "$150 - $199/hr"  # Placeholder hourly rate
            employees = "10 - 49"  # Placeholder number of employees
            location = "Irvine, CA"  # Placeholder location
            services = "60% Mobile App Development"  # Placeholder service description

            # Display each result using custom UI layout
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center;">
                        <img src="{logo_url}" alt="Logo" style="width: 80px; height: 80px; border-radius: 8px; margin-right: 20px;">
                        <div>
                            <h3 style="margin: 0;">{title}</h3>
                            <div style="display: flex; align-items: center;">
                                <span style="font-size: 1.2em; color: #f39c12;">{'★' * int(rating) + '☆' * (5 - int(rating))}</span>
                                <span style="margin-left: 10px; font-size: 0.9em;">{rating} ({reviews} reviews)</span>
                                {"<span style='margin-left: 10px; color: green; font-weight: bold;'>Premier Verified</span>" if verified else ""}
                            </div>
                        </div>
                    </div>
                    <p style="margin-top: 10px; font-size: 0.9em;">{summary}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; font-size: 0.9em; color: #555;">
                        <div><strong>Budget:</strong> {budget}</div>
                        <div><strong>Hourly Rate:</strong> {hourly_rate}</div>
                        <div><strong>Employees:</strong> {employees}</div>
                        <div><strong>Location:</strong> {location}</div>
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Services Provided:</strong>
                        <div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden; height: 8px; margin-top: 5px;">
                            <div style="width: 60%; height: 100%; background-color: #3498db;"></div>
                        </div>
                        <p style="font-size: 0.9em; color: #555;">{services}</p>
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <a href="{link}" target="_blank" style="padding: 10px 15px; background-color: #e74c3c; color: #fff; border-radius: 5px; text-decoration: none;">Visit Website</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No results found.")
