import streamlit as st
import random

# Import custom modules
from utils.styles import apply_custom_styles, render_sidebar, draw_breathing_circle

# Page Setup
st.set_page_config(
    page_title="Calm Zone & Mindfulness - Virtual Wellness Companion",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles
apply_custom_styles()

# Render unified sidebar
render_sidebar()

# Page Title
st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom:0;">🧘 Calm Zone & Mindfulness Studio</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size:1.15rem; color:#9ca3af; margin-top:5px; margin-bottom:25px;">Science-backed mindfulness, grounding tools, and rhythmic breathing to restore inner peace.</p>', unsafe_allow_html=True)

# Tabs for features
tab_breathe, tab_ground, tab_affirm = st.tabs(["🌬️ Breathing Studio", "🖐️ 5-4-3-2-1 Sensory Grounding", "✨ Mindful Affirmations"])

# =========================================================
# TAB 1: BREATHING STUDIO
# =========================================================
with tab_breathe:
    st.markdown('<h3 style="color:#14b8a6; margin-top:10px;">Guided Rhythmic Breathing</h3>', unsafe_allow_html=True)
    st.write("Match your breath to the animated circle. Slow, deliberate breathing triggers your parasympathetic nervous system to decrease cortisol and heart rate.")
    
    col_ctrl, col_visual = st.columns([1, 2], gap="large")
    
    with col_ctrl:
        st.markdown('<div class="glass-card" style="padding:20px;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#ffffff; margin-top:0;">Select Breathing Technique</h4>', unsafe_allow_html=True)
        technique = st.radio(
            "Technique:",
            [
                "🌿 Box Breathing (4-4-4-4)",
                "🌊 Calming 4-7-8 Breath",
                "💜 Coherent Rhythm (5-5)"
            ],
            label_visibility="collapsed"
        )
        
        st.write("---")
        if "Box" in technique:
            mode_code = "box"
            st.markdown(
                "**Box Breathing (Square Pattern)**\n\n"
                "* **Used by:** First responders & athletes under pressure\n"
                "* **Pattern:** Inhale 4s ➔ Hold 4s ➔ Exhale 4s ➔ Hold 4s\n"
                "* **Benefits:** Regulates blood pressure and clears mental fog."
            )
        elif "4-7-8" in technique:
            mode_code = "calming"
            st.markdown(
                "**4-7-8 Calming Technique**\n\n"
                "* **Developed by:** Dr. Andrew Weil\n"
                "* **Pattern:** Inhale 4s ➔ Hold 7s ➔ Exhale 8s\n"
                "* **Benefits:** A natural tranquilizer for the nervous system, excellent for panic and bedtime."
            )
        else:
            mode_code = "relax"
            st.markdown(
                "**Coherent Breathing (Resonant Rhythm)**\n\n"
                "* **Optimal Rate:** ~5-6 breaths per minute\n"
                "* **Pattern:** Inhale 5s ➔ Exhale 5s\n"
                "* **Benefits:** Synchronizes heart rate variability (HRV) with respiratory cycles for sustained calm."
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_visual:
        st.markdown('<div class="glass-card" style="padding:25px; text-align:center;">', unsafe_allow_html=True)
        draw_breathing_circle(mode_code)
        st.caption("Tip: Keep your eyes softly focused on the circle and release your jaw and shoulders.")
        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# TAB 2: 5-4-3-2-1 SENSORY GROUNDING
# =========================================================
with tab_ground:
    st.markdown('<h3 style="color:#38bdf8; margin-top:10px;">5-4-3-2-1 Sensory Grounding Technique</h3>', unsafe_allow_html=True)
    st.write("When anxiety or intrusive thoughts spike, your attention gets trapped in your mind. This exercise forces your brain to reconnect with physical reality through your 5 senses.")
    
    # Session state for grounding checklist
    if "grounding_items" not in st.session_state:
        st.session_state.grounding_items = {
            "see": ["", "", "", "", ""],
            "touch": ["", "", "", ""],
            "hear": ["", "", ""],
            "smell": ["", ""],
            "taste": [""]
        }
    
    col_g1, col_g2 = st.columns(2, gap="medium")
    
    with col_g1:
        st.markdown('<div class="grounding-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#14b8a6; margin-top:0;">👀 5 Things You Can SEE</h4>', unsafe_allow_html=True)
        st.caption("Look around your room: a shadow, a pen, a plant, a coffee mug, light on the wall.")
        see1 = st.text_input("1. Item seen:", value=st.session_state.grounding_items["see"][0], key="g_see_1")
        see2 = st.text_input("2. Item seen:", value=st.session_state.grounding_items["see"][1], key="g_see_2")
        see3 = st.text_input("3. Item seen:", value=st.session_state.grounding_items["see"][2], key="g_see_3")
        see4 = st.text_input("4. Item seen:", value=st.session_state.grounding_items["see"][3], key="g_see_4")
        see5 = st.text_input("5. Item seen:", value=st.session_state.grounding_items["see"][4], key="g_see_5")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="grounding-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#38bdf8; margin-top:0;">✋ 4 Things You Can TOUCH</h4>', unsafe_allow_html=True)
        st.caption("Notice physical sensations: the texture of your shirt, the cool desk, feet on floor.")
        touch1 = st.text_input("1. Physical sensation:", value=st.session_state.grounding_items["touch"][0], key="g_touch_1")
        touch2 = st.text_input("2. Physical sensation:", value=st.session_state.grounding_items["touch"][1], key="g_touch_2")
        touch3 = st.text_input("3. Physical sensation:", value=st.session_state.grounding_items["touch"][2], key="g_touch_3")
        touch4 = st.text_input("4. Physical sensation:", value=st.session_state.grounding_items["touch"][3], key="g_touch_4")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="grounding-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#a78bfa; margin-top:0;">👂 3 Things You Can HEAR</h4>', unsafe_allow_html=True)
        st.caption("Listen closely: bird chirping, car passing, computer fan humming, distant clock.")
        hear1 = st.text_input("1. Sound heard:", value=st.session_state.grounding_items["hear"][0], key="g_hear_1")
        hear2 = st.text_input("2. Sound heard:", value=st.session_state.grounding_items["hear"][1], key="g_hear_2")
        hear3 = st.text_input("3. Sound heard:", value=st.session_state.grounding_items["hear"][2], key="g_hear_3")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="grounding-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f43f5e; margin-top:0;">👃 2 Things You Can SMELL</h4>', unsafe_allow_html=True)
        st.caption("Soap, rain outside, coffee, fresh laundry, or your own skin.")
        smell1 = st.text_input("1. Scent noticed:", value=st.session_state.grounding_items["smell"][0], key="g_smell_1")
        smell2 = st.text_input("2. Scent noticed:", value=st.session_state.grounding_items["smell"][1], key="g_smell_2")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="grounding-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f59e0b; margin-top:0;">👅 1 Thing You Can TASTE</h4>', unsafe_allow_html=True)
        st.caption("A sip of cool water, mint, tea, or simply noticing the neutral taste in your mouth.")
        taste1 = st.text_input("1. Taste noticed:", value=st.session_state.grounding_items["taste"][0], key="g_taste_1")
        st.markdown('</div>', unsafe_allow_html=True)

    # Compute progress
    total_slots = 15
    filled_slots = sum([
        bool(see1), bool(see2), bool(see3), bool(see4), bool(see5),
        bool(touch1), bool(touch2), bool(touch3), bool(touch4),
        bool(hear1), bool(hear2), bool(hear3),
        bool(smell1), bool(smell2),
        bool(taste1)
    ])
    
    st.write("---")
    st.markdown(f"**Grounding Completion: {filled_slots} of {total_slots} Anchors Identified**")
    st.progress(filled_slots / total_slots)
    
    if filled_slots == total_slots:
        st.balloons()
        st.markdown(
            '<div class="glass-card" style="text-align:center; border-color:#10b981; background:rgba(16,185,129,0.1); padding:20px;">'
            '<h3 style="color:#10b981; margin:0;">🌿 You are grounded. You are present. You are safe.</h3>'
            '<p style="color:#d1d5db; margin-top:8px; margin-bottom:0;">Take one slow breath and carry this centered presence into your next moment.</p>'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# TAB 3: MINDFUL AFFIRMATIONS
# =========================================================
AFFIRMATIONS = {
    "🌿 Anxiety & Stress Relief": [
        ("This feeling is uncomfortable, but it is not dangerous. It will pass just like weather.", "Mindful Anchor"),
        ("I don't have to control everything. Right now, in this moment, I am safe.", "Compassionate Grounding"),
        ("I give myself permission to pause, breathe, and slow down.", "Pacing Principle"),
        ("Breathe in calm, exhale tension. My body knows how to return to peace.", "Somatic Reassurance"),
        ("I have survived every hard day that came before today. I will get through this one too.", "Inner Resilience")
    ],
    "💛 Self-Compassion & Worth": [
        ("My value does not depend on my productivity or other people's approval.", "Self-Worth"),
        ("I treat myself with the same kindness and warmth I would offer my dearest friend.", "Self-Compassion"),
        ("It is okay to be a work in progress. I am doing the best I can with the tools I have.", "Acceptance"),
        ("I am allowed to take up space, have boundaries, and rest without guilt.", "Healthy Boundaries"),
        ("I honor my emotions without judging myself for feeling them.", "Emotional Permission")
    ],
    "⚡ Courage & Resilience": [
        ("Courage isn't the absence of fear; it is taking one tiny step forward despite it.", "Inner Strength"),
        ("Every challenge I encounter is building emotional endurance and wisdom within me.", "Growth Mindset"),
        ("I am much stronger, wiser, and more resourceful than my self-doubt claims.", "Empowerment"),
        ("One small step at a time is enough. Progress does not need to be frantic.", "Gentle Momentum")
    ],
    "🌙 Evening Peace & Sleep": [
        ("The day is done. I lay down every expectation and release what I cannot change tonight.", "Evening Surrender"),
        ("My mind and body deserve gentle, restorative rest. Tomorrow will have its own light.", "Bedtime Calm"),
        ("Even resting quietly in the dark is replenishing my energy.", "Rest Acceptance")
    ]
}

with tab_affirm:
    st.markdown('<h3 style="color:#a78bfa; margin-top:10px;">Mindful Affirmations Deck</h3>', unsafe_allow_html=True)
    st.write("Consciously repeating grounded affirmations rewires automatic negative cognitive loops.")
    
    col_cat, col_act = st.columns([2, 1])
    with col_cat:
        selected_category = st.selectbox(
            "Choose affirmation theme:",
            list(AFFIRMATIONS.keys())
        )
    with col_act:
        st.write("##")
        draw_new = st.button("🔄 Draw New Affirmation", use_container_width=True)

    if "current_affirmation" not in st.session_state or draw_new or st.session_state.get("last_affirm_cat") != selected_category:
        deck = AFFIRMATIONS[selected_category]
        st.session_state.current_affirmation = random.choice(deck)
        st.session_state.last_affirm_cat = selected_category
        
    quote_text, quote_tag = st.session_state.current_affirmation
    
    st.markdown(
        f'<div class="affirmation-card">'
        f'  <div class="affirmation-quote">"{quote_text}"</div>'
        f'  <div class="affirmation-author">— {quote_tag}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    st.caption("Take 10 seconds to close your eyes, breathe in deeply, and let these words resonate within.")
