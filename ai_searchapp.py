import streamlit as st
import requests

# Replace with your actual Google API Key and Search Engine ID
API_KEY = "AIzaSyDj6-Q8AuHXAFmPWF5vELOpOn0wyXZjpXo"
SEARCH_ENGINE_ID = "64c42e1bdc7004bc8"

st.title("Companies Search")
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

            # Unique simulated fields for each result (this would be pulled from actual data if available)
            rating = 4.0 + (len(title) % 5) * 0.5  # Example: vary ratings based on title length (for illustration)
            reviews = len(title) % 50 + 1  # Example: random reviews count
            verified = len(title) % 2 == 0  # Example: alternate verified status
            budget = "$" + str((len(title) % 10) * 5000 + 5000) + "+"  # Example budget
            hourly_rate = "$" + str((len(title) % 20 + 1) * 10) + " - $" + str((len(title) % 20 + 10) * 10) + "/hr"  # Example hourly rate
            employees = str((len(title) % 5 + 1) * 10) + " - " + str((len(title) % 5 + 1) * 20)  # Example employees
            location = "Location #" + str(len(title) % 10)  # Example location
            services = str((len(title) % 80)) + "% Mobile App Development"  # Example service percentage

            # Display each result using custom UI layout with mobile-responsive design
            st.markdown(
                f"""
                <style>
                    @media (max-width: 768px) {{
                        .result-card {{
                            padding: 10px;
                        }}
                        .result-header {{
                            flex-direction: column;
                            align-items: flex-start;
                        }}
                        .result-logo {{
                            margin-bottom: 10px;
                        }}
                        .result-title {{
                            font-size: 1.1em;
                        }}
                        .result-info div {{
                            display: block;
                            margin-bottom: 5px;
                        }}
                    }}
                    .result-card {{
                        border: 1px solid #ddd;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start;
                    }}
                    .result-header {{
                        display: flex;
                        align-items: center;
                        width: 100%;
                    }}
                    .result-logo {{
                        width: 60px;
                        height: 60px;
                        border-radius: 8px;
                        margin-right: 15px;
                    }}
                    .result-title {{
                        font-size: 1.2em;
                        font-weight: bold;
                        margin: 0;
                    }}
                    .result-rating {{
                        color: #f39c12;
                        font-size: 1em;
                        display: inline-block;
                    }}
                    .result-info {{
                        margin-top: 10px;
                        font-size: 0.9em;
                        color: #555;
                        line-height: 1.4;
                    }}
                    .result-info div {{
                        margin-right: 15px;
                        display: inline-block;
                    }}
                    .progress-bar {{
                        background-color: #e0e0e0;
                        border-radius: 4px;
                        overflow: hidden;
                        height: 8px;
                        margin-top: 5px;
                        width: 100%;
                    }}
                    .progress-bar div {{
                        width: {services.split('%')[0]}%;
                        height: 100%;
                        background-color: #3498db;
                    }}
                    .result-link {{
                        display: inline-block;
                        padding: 10px 15px;
                        background-color: #e74c3c;
                        color: #fff;
                        border-radius: 5px;
                        text-decoration: none;
                        margin-top: 15px;
                        text-align: center;
                    }}
                </style>
                <div class="result-card">
                    <div class="result-header">
                        <img src="{logo_url}" alt="Logo" class="result-logo">
                        <div>
                            <h3 class="result-title">{title}</h3>
                            <div style="display: flex; align-items: center;">
                                <span class="result-rating">{'★' * int(rating)}{'☆' * (5 - int(rating))}</span>
                                <span style="margin-left: 10px;">{rating} ({reviews} reviews)</span>
                                {"<span style='margin-left: 10px; color: green; font-weight: bold;'>Premier Verified</span>" if verified else ""}
                            </div>
                        </div>
                    </div>
                    <p class="result-info">{snippet}</p>
                    <div class="result-info">
                        <div><strong>Budget:</strong> {budget}</div>
                        <div><strong>Hourly Rate:</strong> {hourly_rate}</div>
                        <div><strong>Employees:</strong> {employees}</div>
                        <div><strong>Location:</strong> {location}</div>
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Services Provided:</strong>
                        <div class="progress-bar">
                            <div></div>
                        </div>
                        <p style="font-size: 0.9em; color: #555;">{services}</p>
                    </div>
                    <a href="{link}" target="_blank" class="result-link">Visit Website</a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No results found.")
