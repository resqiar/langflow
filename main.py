import streamlit as st
import json
from ai import ask_ai, run_main_flow
from profiles import get_notes, get_profile, create_profile
from submit import add_note, delete_note, update_personal_info

st.title("Personal Content Planner")

@st.fragment()
def forms():
    with st.form("social_data"):
        st.header("Social Media")

        profile = st.session_state.profile

        name = st.text_input("Social Media Name", value=profile["social_data"]["name"])
        foll = st.number_input("Total Followers", min_value=0, step=1, value=profile["social_data"]["followers"])
        likes = st.number_input("Total Likes", min_value=0, step=1, value=profile["social_data"]["likes"])

        status_value = ["Personal", "Business"]
        status = st.radio("Account Status", status_value, status_value.index(profile["social_data"].get("gender", "Personal")))
        
        pref_freq = (
            "Once a day",
            "Once a week",
            "Twice a day",
            "Everyday",
            "Once a month",
            "Bruh, never and dont ask again.",
        )

        prefs = st.selectbox(
            "Post Frequency Preference", 
            pref_freq, 
            pref_freq.index(profile["social_data"].get("post_preferences", "Once a month"))
        )

        submit = st.form_submit_button("Save")

        if submit:
            if all([name, foll, likes, status, prefs]):
                with st.spinner():
                    # save social media data
                    update_personal_info(
                        existing=profile,
                        update_type="social_data",
                        name=name,
                        followers=foll,
                        likes=likes,
                        post_preferences=prefs,
                    )

                    st.success("Saved")
            else:
                st.warning("Complete first bro")

@st.fragment()
def goals():
    with st.form("goals_data"):
        st.header("Goals")

        profile = st.session_state.profile

        goals = st.multiselect(
            "Select Goals", 
            [
                "Followers Gain",
                "Engangement Gain", 
                "First Sponsorship", 
                "1000 Folls",
                "10K Folls",
                "100K Folls",
                "1M Folls",
                "1M Likes",
                "People hate your account"
            ],
            default=profile.get("goals", ["Followers Gain"])
        )

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.success("Saved")
            else:
                st.warning("Dont you have goals?")

@st.fragment()
def generate_result():
    profile = st.session_state.profile

    container = st.container(border=True)
    container.header("Generate AI Recommendation")
    if container.button("Generate"):
        result = run_main_flow(profile=profile.get("social_data"), goals=", ".join(profile.get("goals")))
        result_json = json.loads(result)
        print(result_json)
        container.success("Successfully generated recommendation")

        container.markdown("Recommendation")
        container.number_input("Post per Day", value=result_json["posts_per_day"])
        container.number_input("Stories per Day", value=result_json["stories_per_day"])
        container.text_input("Engagement Time", value=result_json["engagement_time"])
        container.text_input("Recommended Topics", value=', '.join(result_json["recommended_topics"]))

        container.markdown("Topic Ideas")
        st.markdown("""
            <style>
            .card {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
            }
            .card-content {
                font-size: 1.2em;
                font-weight: bold;
                color: #333;
                margin-bottom: 8px;
            }
            .card-hashtags {
                font-size: 0.9em;
                color: #666;
            }
            </style>
        """, unsafe_allow_html=True)
        for post in result_json["post_ideas"]:
            container.markdown(f"""
            <div class="card">
                <div class="card-content">{post["content"]}</div>
                <div class="card-hashtags">{" ".join([f'#{tag}' for tag in post["hashtags"]])}</div>
            </div>
            """, unsafe_allow_html=True)

def start():
    if "profile" not in st.session_state:
        profile_id = 1 # make it unique later on
        profile = get_profile(profile_id)
        
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)


    forms()
    goals()
    generate_result()

if __name__ == "__main__":
    start()