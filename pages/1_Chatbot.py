import streamlit as st
import json
from datetime import datetime

# Import custom modules
from utils.styles import apply_custom_styles, render_sidebar
from utils.data_store import append_mood_log
from utils.bot_engine import get_configured_api_key
from utils.bot_logic import (
    check_crisis,
    detect_mood,
    get_offline_response,
    generate_ai_response,
    EMERGENCY_RESPONSE
)

# Safe baseline scores for auto-logging chat moods
MOOD_SCORES_MAP = {
    'happy': 8.5,
    'neutral': 5.0,
    'anxious': 3.5,
    'sad': 2.5,
    'angry': 2.0,
    'breakup': 1.5,
    'lonely': 2.0,
    'tired': 3.5,
    'panic': 1.5,
    'insomnia': 3.0,
    'crisis': 1.0
}

# Page Setup
st.set_page_config(
    page_title="Companion Chat - Virtual Wellness Companion",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles
apply_custom_styles()

# Initialize session states
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

# Fetch active configurations
active_persona = st.session_state.selected_persona
gemini_key = st.session_state.gemini_api_key or get_configured_api_key()

# Top Header with Action Bar
col_title, col_actions = st.columns([3, 2])

with col_title:
    st.markdown('<h1 class="gradient-text" style="font-size: 2.7rem; margin-bottom:0;">💬 Companion Chat</h1>', unsafe_allow_html=True)
    last_mood = st.session_state.last_significant_mood or "calm"
    st.markdown(
        f'<p style="font-size:1.1rem; color:#9ca3af; margin-top:4px; margin-bottom:12px;">'
        f'Companion: <strong>{active_persona}</strong> | '
        f'<span class="sentiment-pill">Emotional Tone: {last_mood}</span>'
        f'</p>',
        unsafe_allow_html=True
    )

with col_actions:
    st.write("##")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        # Download chat history
        chat_text = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.chat_history])
        st.download_button(
            "📥 Export Chat",
            data=chat_text,
            file_name=f"empathybot_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_a2:
        if st.button("🔄 Restart Chat", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"Welcome back. I am {active_persona}. What is on your mind today?"}
            ]
            st.session_state.last_significant_mood = None
            st.session_state.crisis_detected = False
            st.rerun()

# Safety Disclaimer Banner
st.markdown(
    '<div class="glass-card" style="padding: 10px 16px; margin-bottom:18px; border-left: 4px solid #ef4444; font-size:0.84rem;">'
    '⚠️ <strong>Safety Notice:</strong> EmpathyBot offers emotional listening and grounding support, but is <em>not</em> a healthcare provider or crisis service. '
    'If you are feeling overwhelmed, safe and free emergency help is available anytime on our <strong>Crisis Helplines</strong> page.'
    '</div>',
    unsafe_allow_html=True
)

# Display crisis override if detected in session
if st.session_state.crisis_detected:
    st.markdown(
        f'<div class="crisis-card">'
        f'<h2 style="color:#ef4444; margin-top:0;">🛑 Immediate Crisis Support Triggered</h2>'
        f'<p style="font-size:1.05rem; line-height:1.7;">{EMERGENCY_RESPONSE}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("🚨 Open Emergency Helplines Directory", type="primary", use_container_width=True):
            st.switch_page("pages/3_Helpline.py")
    with col_c2:
        if st.button("🌿 I feel calmer now. Restart conversation.", use_container_width=True):
            st.session_state.crisis_detected = False
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Welcome back. Let's take things slow and steady. How can I support you right now?"}
            ]
            st.rerun()
        
else:
    # Quick Starter Chips
    st.markdown('<p style="font-size:0.85rem; color:#9ca3af; margin-bottom:6px;">Suggested conversation starters:</p>', unsafe_allow_html=True)
    
    chip_cols = st.columns(5)
    prompt_to_send = None
    
    if chip_cols[0].button("Anxious about work", use_container_width=True):
        prompt_to_send = "I'm feeling really anxious about work and deadlines right now."
    if chip_cols[1].button("Need to vent", use_container_width=True):
        prompt_to_send = "I had a really exhausting day and I just need to vent for a moment."
    if chip_cols[2].button("Celebrate a win 🎉", use_container_width=True):
        prompt_to_send = "I finished something important today and wanted to celebrate a small win!"
    if chip_cols[3].button("Can't sleep 🌙", use_container_width=True):
        prompt_to_send = "I can't sleep. My mind keeps replaying thoughts."
    if chip_cols[4].button("Need grounding 🧘", use_container_width=True):
        prompt_to_send = "Can you help me ground myself? My thoughts feel scrambled."

    # Chat Message Container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            avatar = "🤖" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    
    # User input box
    user_input = st.chat_input("Type a message to your companion...")
    
    # Process either chip click or text input
    active_input = prompt_to_send or user_input
    
    if active_input:
        # 1. Append User Input
        st.session_state.chat_history.append({"role": "user", "content": active_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_input)
            
        # 2. Crisis check (Highest Priority)
        if check_crisis(active_input):
            st.session_state.crisis_detected = True
            append_mood_log(
                score=MOOD_SCORES_MAP['crisis'],
                mood='crisis',
                influencers='Crisis Triggered',
                notes=f"Crisis trigger detected in message: '{active_input[:40]}...'"
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "I detected that you may be in distress. Please review the immediate crisis numbers displayed on screen."
            })
            st.rerun()
            
        # 3. Standard Chat Processing
        else:
            detected_mood = detect_mood(active_input)
            
            # Auto-log mood score in background if a recognizable emotion was detected
            if detected_mood not in ['neutral', 'greeting', 'gratitude']:
                st.session_state.last_significant_mood = detected_mood
                score = MOOD_SCORES_MAP.get(detected_mood, 5.0)
                append_mood_log(
                    score=score,
                    mood=detected_mood,
                    influencers="Chat Sentiment Analysis",
                    notes=f"Auto-logged from chat: '{active_input[:40]}...'"
                )
            
            # Generate Bot response
            with st.spinner(f"{active_persona} is listening and reflecting..."):
                if gemini_key:
                    bot_reply_msg = generate_ai_response(
                        prompt=active_input,
                        api_key=gemini_key,
                        persona_name=active_persona,
                        chat_history=st.session_state.chat_history[:-1]
                    )
                else:
                    is_followup = (detected_mood == 'neutral' and st.session_state.last_significant_mood is not None)
                    mood_state = detected_mood if detected_mood != 'neutral' else st.session_state.last_significant_mood
                    if mood_state is None:
                        mood_state = 'neutral'
                    bot_reply_msg = get_offline_response(active_persona, mood_state, is_followup=is_followup)
            
            # Append assistant reply
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply_msg})
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(bot_reply_msg)
                
            st.rerun()
