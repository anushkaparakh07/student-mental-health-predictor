import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Mental Health Score Predictor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #f7f9fc 0%, #eef2f9 100%);
        }
        .title-text {
            font-size: 2.4rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(90deg, #6a5af9, #d16ba5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .subtitle-text {
            text-align: center;
            color: #6b7280;
            font-size: 1.05rem;
            margin-bottom: 1.8rem;
        }
        .section-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #374151;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            border-left: 4px solid #6a5af9;
            padding-left: 0.6rem;
        }
        .result-card {
            background: linear-gradient(135deg, #6a5af9, #a56bd1 60%, #d16ba5);
            border-radius: 18px;
            padding: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(106, 90, 249, 0.35);
            margin-top: 1.5rem;
        }
        .result-score {
            font-size: 3.2rem;
            font-weight: 800;
            margin: 0.3rem 0;
        }
        .result-label {
            font-size: 1.1rem;
            opacity: 0.9;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .result-tag {
            display: inline-block;
            margin-top: 0.8rem;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.2);
            font-weight: 600;
        }
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #6a5af9, #d16ba5);
            color: white;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0.7rem 0;
            border-radius: 12px;
            border: none;
            transition: transform 0.15s ease;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            color: white;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

TOP_COUNTRIES = ['Other', 'India', 'USA', 'Canada', 'Australia', 'UK', 'Germany', 'Turkey', 'Mexico', 'France']
PLATFORMS = ['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
             'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp', 'WeChat']
PURPOSES = ['Networking', 'Education', 'Entertainment', 'News']
ACADEMIC_LEVELS = ['Undergraduate', 'Graduate', 'High School']
STRESS_LEVELS = ['Low', 'Medium', 'High', 'Very High']

st.markdown('<div class="title-text">🧠 Mental Health Score Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Estimate a student\'s mental health score based on lifestyle and social media habits</div>',
    unsafe_allow_html=True,
)

with st.form("prediction_form"):
    st.markdown('<div class="section-header">👤 Personal Details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=10, max_value=100, value=20, step=1)
    with c2:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c3:
        country = st.selectbox("Country", TOP_COUNTRIES + ["Other (type below)"])
    custom_country = ""
    if country == "Other (type below)":
        custom_country = st.text_input("Enter your country", value="")

    academic_level = st.selectbox("Academic Level", ACADEMIC_LEVELS)

    st.markdown('<div class="section-header">📱 Social Media Habits</div>', unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        most_used_platform = st.selectbox("Most Used Platform", PLATFORMS)
    with c5:
        purpose_of_use = st.selectbox("Purpose of Use", PURPOSES)

    c6, c7 = st.columns(2)
    with c6:
        avg_daily_usage_hours = st.slider("Avg Daily Usage (hours)", 0.0, 24.0, 3.0, 0.5)
    with c7:
        daily_unlocks = st.number_input("Daily Phone Unlocks", min_value=0, value=50, step=1)

    st.markdown('<div class="section-header">🌱 Lifestyle</div>', unsafe_allow_html=True)
    c8, c9, c10 = st.columns(3)
    with c8:
        study_hours = st.slider("Study Hours/day", 0.0, 24.0, 4.0, 0.5)
    with c9:
        physical_activity_hours = st.slider("Physical Activity (hours)", 0.0, 24.0, 1.0, 0.5)
    with c10:
        sleep_hours_per_night = st.slider("Sleep Hours/night", 0.0, 24.0, 7.0, 0.5)

    stress_level = st.select_slider("Stress Level", options=STRESS_LEVELS, value="Medium")

    submitted = st.form_submit_button("🔮 Predict Mental Health Score")

if submitted:
    final_country = custom_country.strip() if country == "Other (type below)" else country

    if country == "Other (type below)" and not final_country:
        st.error("⚠️ Please enter your country name.")
    else:
        payload = {
            "age": age,
            "gender": gender,
            "country": final_country,
            "academic_level": academic_level,
            "most_used_platform": most_used_platform,
            "purpose_of_use": purpose_of_use,
            "avg_daily_usage_hours": avg_daily_usage_hours,
            "daily_unlocks": daily_unlocks,
            "study_hours": study_hours,
            "physical_activity_hours": physical_activity_hours,
            "sleep_hours_per_night": sleep_hours_per_night,
            "stress_level": stress_level,
        }

        try:
            with st.spinner("Analyzing lifestyle data and predicting score..."):
                response = requests.post(API_URL, json=payload, timeout=15)

            if response.status_code == 200:
                score = response.json()["predicted_mental_health_score"]

                if score >= 7:
                    tag, tag_emoji = "Good", "🟢"
                elif score >= 4:
                    tag, tag_emoji = "Moderate", "🟡"
                else:
                    tag, tag_emoji = "Needs Attention", "🔴"

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">Predicted Mental Health Score</div>
                        <div class="result-score">{score} / 10</div>
                        <div class="result-tag">{tag_emoji} {tag}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption("This score is a model-based estimate and not a clinical diagnosis.")

            elif response.status_code == 422:
                st.error("⚠️ Validation error: please check your inputs and try again.")
                with st.expander("Details"):
                    st.json(response.json())
            else:
                st.error(f"⚠️ Server returned status code {response.status_code}.")
                with st.expander("Details"):
                    st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the API. Make sure the FastAPI backend is running at "
                      f"`{API_URL}`.")
        except requests.exceptions.Timeout:
            st.error("⏱️ The request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit • Powered by a FastAPI ML backend")