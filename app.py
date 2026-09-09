import streamlit as st
import os
from datetime import datetime

# Import custom modules
from utils.styles import apply_custom_styles, render_sidebar
from utils.data_store import init_data_store, append_mood_log
from utils.bot_engine import get_configured_api_key

# Initialize page configuration
st.set_page_config(
    page_title="EmpathyBot 2.0 - Virtual Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global custom styles & ensure data store exists
apply_custom_styles()
init_data_store()

# Initialize session state objects
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello. I am your emotional companion. How are you feeling today? I am here to listen without judgment."}
    ]
if 'last_significant_mood' not in st.session_state:
    st.session_state.last_significant_mood = None
if 'crisis_detected' not in st.session_state:
    st.session_state.crisis_detected = False
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "🌿 Serene"
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = get_configured_api_key()

# Render unified sidebar settings
render_sidebar()

# ==========================================
# --- Landing Page Hero & Navigation ---
# ==========================================

# Minimalist Centered Header
st.write("##")
st.markdown('<div style="text-align: center;"><h1 class="gradient-text" style="font-size: 3.5rem; margin-bottom:0; letter-spacing: -0.5px;">EmpathyBot 2.0</h1></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;"><p style="font-size:1.25rem; color:#9ca3af; margin-top:8px; margin-bottom:30px;">A peaceful, private sanctuary to reflect, converse, and track emotional wellness.</p></div>', unsafe_allow_html=True)

# Status Badge
configured_key = st.session_state.gemini_api_key or get_configured_api_key()
status_html = (
    '<span class="sentiment-pill" style="background:rgba(34,197,94,0.15); color:#4ade80; border-color:rgba(34,197,94,0.3);">'
    '🟢 Advanced AI Mode (Gemini Active)</span>'
    if configured_key else
    '<span class="sentiment-pill" style="background:rgba(56,189,248,0.15); color:#38bdf8; border-color:rgba(56,189,248,0.3);">'
    '🔵 Offline Empathy Engine Active</span>'
)

st.markdown(f'<div style="text-align: center; margin-bottom: 25px;">{status_html}</div>', unsafe_allow_html=True)

# Single elegant greeting banner
st.markdown(
    '<div class="glass-card" style="padding: 28px; text-align: center; border-color: rgba(20,184,166,0.25); max-width: 820px; margin: 0 auto 35px auto;">'
    '  <h3 style="color:#ffffff; margin-top:0; font-weight:700; font-size: 1.45rem;">Take a Deep Breath 🌿</h3>'
    '  <p style="font-size:1.05rem; color:#d1d5db; line-height:1.7; margin-bottom:15px;">'
    '    This is your private, judgment-free space. You can talk through your thoughts with compassionate virtual companions, '
    '    log your emotional journeys, engage in guided sensory grounding, and access emergency helplines anytime.'
    '  </p>'
    '  <p style="color:#a78bfa; font-weight:600; font-size:1.0rem; margin-bottom:0;">'
    '    👈 Use the sidebar navigation to explore features, or start with a quick check-in below.'
    '  </p>'
    '</div>',
    unsafe_allow_html=True
)

# Four visual column navigation cards
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(
        '<div class="glass-card" style="text-align: center; padding: 22px; height:100%;">'
        '  <span style="font-size: 2.3rem;">💬</span>'
        '  <h4 style="color:#14b8a6; font-weight:600; margin-top:12px; margin-bottom:8px;">Companion Chat</h4>'
        '  <p style="font-size:0.88rem; color:#9ca3af; line-height:1.5; margin-bottom:0;">'
        '    Converse with Serene, Joy, or Sage for calming, uplifting, or analytical guidance.'
        '  </p>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="glass-card" style="text-align: center; padding: 22px; height:100%;">'
        '  <span style="font-size: 2.3rem;">📊</span>'
        '  <h4 style="color:#8b5cf6; font-weight:600; margin-top:12px; margin-bottom:8px;">Mood Journey</h4>'
        '  <p style="font-size:0.88rem; color:#9ca3af; line-height:1.5; margin-bottom:0;">'
        '    Record wellness ratings, trace emotional timelines, and review lifestyle factor impacts.'
        '  </p>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="glass-card" style="text-align: center; padding: 22px; height:100%;">'
        '  <span style="font-size: 2.3rem;">🧘</span>'
        '  <h4 style="color:#38bdf8; font-weight:600; margin-top:12px; margin-bottom:8px;">Calm Zone</h4>'
        '  <p style="font-size:0.88rem; color:#9ca3af; line-height:1.5; margin-bottom:0;">'
        '    Paced breathing visualizers, 5-4-3-2-1 sensory grounding, and mindful affirmations.'
        '  </p>'
        '</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="glass-card" style="text-align: center; padding: 22px; height:100%;">'
        '  <span style="font-size: 2.3rem;">🚨</span>'
        '  <h4 style="color:#f43f5e; font-weight:600; margin-top:12px; margin-bottom:8px;">Crisis Helplines</h4>'
        '  <p style="font-size:0.88rem; color:#9ca3af; line-height:1.5; margin-bottom:0;">'
        '    Confidential, free 24/7 hotlines and regional emergency crisis resources worldwide.'
        '  </p>'
        '</div>',
        unsafe_allow_html=True
    )

st.write("##")

# ==========================================
# --- Quick Mood Check-In Widget ---
# ==========================================
st.markdown('<div class="glass-card" style="padding: 24px;">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#14b8a6; margin-top:0; font-size:1.3rem;">⚡ Quick 10-Second Mood Check-In</h3>', unsafe_allow_html=True)
st.write("Record how you feel right now in just a few clicks without navigating away:")

col_q1, col_q2, col_q3 = st.columns([1, 1, 1])

with col_q1:
    quick_mood = st.selectbox(
        "Current Feeling:",
        ["Happy 😊", "Neutral 😐", "Anxious 😰", "Sad 😢", "Tired 😴", "Angry 😤"],
        index=0
    )
with col_q2:
    quick_score = st.slider("Rating (1-10):", min_value=1.0, max_value=10.0, value=7.0, step=0.5)
with col_q3:
    st.write("##")
    if st.button("Log Check-In to History", type="primary", use_container_width=True):
        clean_mood = quick_mood.split(" ")[0].lower()
        append_mood_log(
            score=quick_score,
            mood=clean_mood,
            influencers="Quick Home Check-In",
            notes="Logged from home sanctuary dashboard."
        )
        st.success("Logged! Your reflection has been saved to the Mood Journey analytics.")

st.markdown('</div>', unsafe_allow_html=True)