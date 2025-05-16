import streamlit as st
import pandas as pd
import os

from recommendation import filter_and_rank, explain

# Constants
FEEDBACK_CSV = "feedback.csv"
RECOMMENDATION_CSV = "recommendation_results.csv"
cuisines_list = ['indian', 'chinese', 'italian']
locations_list = ['delhi', 'mumbai', 'cairo']

# Sidebar
st.sidebar.header("🍽️ Choose Your Preferences")
cuisine = st.sidebar.selectbox("Select Cuisine", cuisines_list)
budget = st.sidebar.selectbox("Budget", ["Low", "Medium", "High"])
location = st.sidebar.selectbox("Select Location", locations_list)

# Functions
def save_feedback(feedback_dict):
    feedback_df = pd.DataFrame([feedback_dict])
    if os.path.exists(FEEDBACK_CSV):
        existing_df = pd.read_csv(FEEDBACK_CSV)
        combined_df = pd.concat([existing_df, feedback_df], ignore_index=True)
    else:
        combined_df = feedback_df
    combined_df.to_csv(FEEDBACK_CSV, index=False)

def save_recommendations(df, cuisine, budget, location):
    df_copy = df.copy()
    df_copy["Selected_Cuisine"] = cuisine
    df_copy["Selected_Budget"] = budget
    df_copy["Selected_Location"] = location
    if os.path.exists(RECOMMENDATION_CSV):
        existing = pd.read_csv(RECOMMENDATION_CSV)
        combined = pd.concat([existing, df_copy], ignore_index=True)
    else:
        combined = df_copy
    combined.to_csv(RECOMMENDATION_CSV, index=False)

# Main Logic
if st.sidebar.button("🔍 Find Restaurants"):
    st.session_state["show_results"] = True  # Flag to control rendering later

if st.session_state.get("show_results", False):
    st.header("🍴 Recommended Restaurants")
    results = filter_and_rank(cuisine, budget, location)

    if results.empty:
        st.warning("No matching restaurants found. Please try different preferences.")
    else:
        save_recommendations(results, cuisine, budget, location)

        for _, row in results.iterrows():
            st.markdown(f"### {row['Restaurant Name']}")
            st.write(f"**Cuisine:** {row['primary_cuisine'].title()}")
            st.write(f"**Cost for two:** {row['Currency']} {row['Average Cost for two']}")
            st.write(f"**Rating:** {row['Aggregate rating']} ⭐ ({row['Votes']} votes)")
            st.info(explain(row))
            st.markdown("---")

        # Feedback section
        st.header("🗣️ Please give your feedback")
        with st.form(key="feedback_form"):
            relevance = st.radio("Was this recommendation relevant?", ["Yes", "No"])
            satisfaction = st.slider("How satisfied are you? (1 to 5)", 1, 5)
            comments = st.text_area("Any suggestions or comments?")
            submitted = st.form_submit_button("✅ Submit Feedback")

        if submitted:
            feedback = {
                "cuisine": cuisine,
                "budget": budget,
                "location": location,
                "relevance": relevance,
                "satisfaction": satisfaction,
                "comments": comments,
            }
            save_feedback(feedback)
            st.success("✅ Feedback saved successfully!")  
