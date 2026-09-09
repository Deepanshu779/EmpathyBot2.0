import streamlit as st
import os

# ==========================================
# --- EmpathyBot 2.0 Modern Styles ---
# ==========================================

CSS_STYLES = """
<style>
/* Import Calming, Elegant Google Font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Apply font to text-bearing elements */
html, body, p, h1, h2, h3, h4, h5, h6, li, button, label, input, textarea, select, option, [data-testid="stMarkdownContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Background gradient styling for main area */
.stApp {
    background: radial-gradient(circle at 20% 15%, rgba(20, 184, 166, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 80% 75%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                linear-gradient(135deg, #0b0f19 0%, #131b2e 50%, #0d1322 100%) !important;
    color: #f3f4f6;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.95) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(14px);
}

/* Glassmorphic card custom element */
.glass-card {
    background: rgba(30, 41, 59, 0.5);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.35);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    border-color: rgba(20, 184, 166, 0.4);
    box-shadow: 0 12px 35px 0 rgba(20, 184, 166, 0.12);
    transform: translateY(-2px);
}

/* Accent Card for Crisis Warning */
.crisis-card {
    background: rgba(220, 38, 38, 0.15);
    border-radius: 16px;
    border: 1px solid rgba(220, 38, 38, 0.45);
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(220, 38, 38, 0.2);
}

/* Title text highlights */
.gradient-text {
    background: linear-gradient(90deg, #14b8a6 0%, #38bdf8 50%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Sentiment indicator pill */
.sentiment-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: capitalize;
    background: rgba(20, 184, 166, 0.15);
    color: #2dd4bf;
    border: 1px solid rgba(20, 184, 166, 0.3);
}

/* Prompt chip */
.prompt-chip {
    display: inline-block;
    padding: 7px 14px;
    margin: 4px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    font-size: 0.85rem;
    color: #e2e8f0;
    cursor: pointer;
    transition: all 0.2s ease;
}

.prompt-chip:hover {
    background: rgba(20, 184, 166, 0.2);
    border-color: #14b8a6;
    color: #ffffff;
}

/* Metric KPI card */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: rgba(30, 41, 59, 0.45);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 18px 20px;
    text-align: center;
    transition: all 0.2s;
}

.kpi-card:hover {
    border-color: rgba(167, 139, 250, 0.4);
    transform: translateY(-2px);
}

.kpi-val {
    font-size: 1.9rem;
    font-weight: 700;
    color: #14b8a6;
    line-height: 1.2;
}

.kpi-lbl {
    font-size: 0.82rem;
    color: #9ca3af;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Affirmation Card */
.affirmation-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(45, 30, 80, 0.4) 100%);
    border-radius: 16px;
    border: 1px solid rgba(167, 139, 250, 0.3);
    padding: 28px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.12);
}

.affirmation-quote {
    font-size: 1.35rem;
    font-weight: 600;
    color: #f8fafc;
    line-height: 1.6;
    margin-bottom: 10px;
}

.affirmation-author {
    font-size: 0.9rem;
    color: #a78bfa;
}

/* Clickable telephone button */
.tel-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 18px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #ffffff !important;
    font-weight: 600;
    font-size: 1.05rem;
    border-radius: 10px;
    text-decoration: none !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
    transition: all 0.2s ease;
    margin-top: 10px;
}

.tel-btn:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
    transform: translateY(-1px);
}

/* --- Breathing Animation Styles --- */
.breathing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
    width: 100%;
}

.breathing-circle-box {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background-color: rgba(20, 184, 166, 0.25);
    border: 3px solid #14b8a6;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 600;
    font-size: 1.15rem;
    text-align: center;
    box-shadow: 0 0 25px rgba(20, 184, 166, 0.45);
    animation: box-breathe 16s infinite cubic-bezier(0.4, 0, 0.2, 1);
}

.breathing-circle-calming {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background-color: rgba(56, 189, 248, 0.25);
    border: 3px solid #38bdf8;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 600;
    font-size: 1.15rem;
    text-align: center;
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.45);
    animation: calming-breathe 19s infinite cubic-bezier(0.4, 0, 0.2, 1);
}

.breathing-circle-relax {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background-color: rgba(167, 139, 250, 0.25);
    border: 3px solid #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 600;
    font-size: 1.15rem;
    text-align: center;
    box-shadow: 0 0 25px rgba(167, 139, 250, 0.45);
    animation: relax-breathe 10s infinite cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes box-breathe {
    0%, 100% { transform: scale(1); background-color: rgba(20, 184, 166, 0.2); box-shadow: 0 0 20px rgba(20, 184, 166, 0.4); }
    25% { transform: scale(1.45); background-color: rgba(20, 184, 166, 0.5); box-shadow: 0 0 50px rgba(20, 184, 166, 0.85); }
    50% { transform: scale(1.45); background-color: rgba(20, 184, 166, 0.5); box-shadow: 0 0 50px rgba(20, 184, 166, 0.85); }
    75% { transform: scale(1); background-color: rgba(20, 184, 166, 0.2); box-shadow: 0 0 20px rgba(20, 184, 166, 0.4); }
}

@keyframes calming-breathe {
    0%, 100% { transform: scale(1); background-color: rgba(56, 189, 248, 0.2); box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
    21% { transform: scale(1.5); background-color: rgba(56, 189, 248, 0.5); box-shadow: 0 0 50px rgba(56, 189, 248, 0.85); }
    58% { transform: scale(1.5); background-color: rgba(56, 189, 248, 0.5); box-shadow: 0 0 50px rgba(56, 189, 248, 0.85); }
}

@keyframes relax-breathe {
    0%, 100% { transform: scale(1); background-color: rgba(167, 139, 250, 0.2); box-shadow: 0 0 20px rgba(167, 139, 250, 0.4); }
    50% { transform: scale(1.5); background-color: rgba(167, 139, 250, 0.5); box-shadow: 0 0 50px rgba(167, 139, 250, 0.85); }
}

.breathing-subtext {
    font-size: 1rem;
    font-weight: 500;
    color: #e2e8f0;
    margin-top: 22px;
    height: 26px;
    text-align: center;
}

/* Custom Cards grid */
.help-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 15px;
}

.help-card {
    background: rgba(30, 41, 59, 0.55);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.25s ease;
}

.help-card:hover {
    border-color: rgba(20, 184, 166, 0.4);
    background: rgba(45, 30, 80, 0.25);
    transform: translateY(-2px);
}

.help-title {
    font-size: 1.18rem;
    font-weight: 600;
    color: #14b8a6;
    margin-bottom: 6px;
}

.help-number {
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin: 8px 0;
    font-family: monospace !important;
}

.help-meta {
    font-size: 0.88rem;
    color: #9ca3af;
    line-height: 1.5;
}

/* Grounding Step Styling */
.grounding-box {
    background: rgba(30, 41, 59, 0.45);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    margin-bottom: 16px;
}

.grounding-step {
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 12px;
    border-left: 4px solid #14b8a6;
    background: rgba(255, 255, 255, 0.02);
}

/* Style for Streamlit buttons */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* Custom styled tab selectors */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.4);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    background-color: transparent;
    border-radius: 8px;
    color: #9ca3af;
    font-weight: 500;
    border: none !important;
    padding: 0 18px;
}

.stTabs [aria-selected="true"] {
    background-color: #14b8a6 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}
</style>
"""


def apply_custom_styles():
    """Injects custom CSS styling for premium look and animations."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def draw_breathing_circle(mode="box"):
    """
    Renders an animated SVG/HTML container for breathing exercise.
    - box: Box Breathing (4s Inhale, 4s Hold, 4s Exhale, 4s Hold)
    - calming: Calming Breathing 4-7-8 (4s In, 7s Hold, 8s Out)
    - relax: Relaxing Breathing 5-5 (5s In, 5s Out)
    """
    if mode == "box":
        html_code = """
        <div class="breathing-container" style="font-family: 'Plus Jakarta Sans', sans-serif;">
            <div class="breathing-circle-box">
                <span id="breathing-text" style="font-size:1.15rem; font-weight:700;">Inhale 💨</span>
            </div>
            <div class="breathing-subtext" id="breathing-sub" style="font-size:1.05rem; color:#2dd4bf; margin-top:24px; font-weight:600;">Inhale slowly through your nose (4s)</div>
        </div>
        <script>
            const textEl = document.getElementById('breathing-text');
            const subEl = document.getElementById('breathing-sub');
            const phases = [
                { text: 'Inhale 💨', sub: 'Inhale slowly through your nose (4s)...', duration: 4000 },
                { text: 'Hold 🔒', sub: 'Hold your breath gently (4s)...', duration: 4000 },
                { text: 'Exhale 🌬️', sub: 'Exhale smoothly through your mouth (4s)...', duration: 4000 },
                { text: 'Rest 🌿', sub: 'Pause quietly before next breath (4s)...', duration: 4000 }
            ];
            let currentPhase = 0;
            
            function runBreathing() {
                const phase = phases[currentPhase];
                if(textEl) textEl.innerText = phase.text;
                if(subEl) subEl.innerText = phase.sub;
                
                setTimeout(() => {
                    currentPhase = (currentPhase + 1) % phases.length;
                    runBreathing();
                }, phase.duration);
            }
            runBreathing();
        </script>
        """
    elif mode == "calming":
        html_code = """
        <div class="breathing-container" style="font-family: 'Plus Jakarta Sans', sans-serif;">
            <div class="breathing-circle-calming">
                <span id="breathing-text-calm" style="font-size:1.15rem; font-weight:700;">Inhale 💨</span>
            </div>
            <div class="breathing-subtext" id="breathing-sub-calm" style="font-size:1.05rem; color:#38bdf8; margin-top:24px; font-weight:600;">Inhale quietly through your nose (4s)</div>
        </div>
        <script>
            const textEl = document.getElementById('breathing-text-calm');
            const subEl = document.getElementById('breathing-sub-calm');
            const phases = [
                { text: 'Inhale 💨 (4s)', sub: 'Inhale quietly through your nose...', duration: 4000 },
                { text: 'Hold 🔒 (7s)', sub: 'Retain the air comfortably...', duration: 7000 },
                { text: 'Exhale 🌬️ (8s)', sub: 'Release completely with a gentle whoosh...', duration: 8000 }
            ];
            let currentPhase = 0;
            
            function runBreathingCalm() {
                const phase = phases[currentPhase];
                if(textEl) textEl.innerText = phase.text;
                if(subEl) subEl.innerText = phase.sub;
                
                setTimeout(() => {
                    currentPhase = (currentPhase + 1) % phases.length;
                    runBreathingCalm();
                }, phase.duration);
            }
            runBreathingCalm();
        </script>
        """
    else:  # relax
        html_code = """
        <div class="breathing-container" style="font-family: 'Plus Jakarta Sans', sans-serif;">
            <div class="breathing-circle-relax">
                <span id="breathing-text-relax" style="font-size:1.15rem; font-weight:700;">Inhale 💨</span>
            </div>
            <div class="breathing-subtext" id="breathing-sub-relax" style="font-size:1.05rem; color:#a78bfa; margin-top:24px; font-weight:600;">Breathe in slowly (5s)</div>
        </div>
        <script>
            const textEl = document.getElementById('breathing-text-relax');
            const subEl = document.getElementById('breathing-sub-relax');
            const phases = [
                { text: 'Inhale 💨 (5s)', sub: 'Breathe in slowly and expand...', duration: 5000 },
                { text: 'Exhale 🌬️ (5s)', sub: 'Breathe out slowly and release tension...', duration: 5000 }
            ];
            let currentPhase = 0;
            
            function runBreathingRelax() {
                const phase = phases[currentPhase];
                if(textEl) textEl.innerText = phase.text;
                if(subEl) subEl.innerText = phase.sub;
                
                setTimeout(() => {
                    currentPhase = (currentPhase + 1) % phases.length;
                    runBreathingRelax();
                }, phase.duration);
            }
            runBreathingRelax();
        </script>
        """
    st.components.v1.html(html_code, height=280)


def render_sidebar():
    """
    Renders the unified sidebar across all pages, ensuring settings and
    state persist correctly with environment API key auto-detection.
    """
    from utils.data_store import clear_all_logs
    from utils.bot_engine import get_configured_api_key

    # Initialize states if not set yet
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = "🌿 Serene"
    if 'gemini_api_key' not in st.session_state:
        # Auto-detect from env or keep empty
        st.session_state.gemini_api_key = get_configured_api_key()
    if 'crisis_detected' not in st.session_state:
        st.session_state.crisis_detected = False

    with st.sidebar:
        st.markdown('<h2 style="color: #14b8a6; font-weight:800; margin-bottom:0;">🧠 EmpathyBot 2.0</h2>', unsafe_allow_html=True)
        st.caption("Your Premium Virtual Wellness Companion")
        st.write("---")
        
        # 1. Select Persona
        st.markdown('<p style="font-weight:600; color:#a78bfa; margin-bottom:5px;">🎭 Choose Your Companion</p>', unsafe_allow_html=True)
        
        personas = ["🌿 Serene", "⚡ Joy", "🧠 Sage"]
        try:
            p_index = personas.index(st.session_state.selected_persona)
        except ValueError:
            p_index = 0

        selected_persona = st.selectbox(
            "Select Companion:",
            personas,
            index=p_index,
            label_visibility="collapsed",
            help="🌿 Serene is calming and soft. ⚡ Joy is uplifting and bright. 🧠 Sage is reflective and analytical.",
            key="selected_persona_widget"
        )
        
        st.session_state.selected_persona = selected_persona
        
        # Persona description cards
        if selected_persona == "🌿 Serene":
            st.markdown(
                '<div class="glass-card" style="padding:14px; font-size:0.85rem; border-color: rgba(20,184,166,0.3); margin-bottom: 10px;">'
                '<strong>🌿 Serene:</strong> Focuses on mindfulness, breathing, and soothing reassurance. Ideal for calming anxiety and stress.'
                '</div>', 
                unsafe_allow_html=True
            )
        elif selected_persona == "⚡ Joy":
            st.markdown(
                '<div class="glass-card" style="padding:14px; font-size:0.85rem; border-color: rgba(139,92,246,0.3); margin-bottom: 10px;">'
                '<strong>⚡ Joy:</strong> Celebrates small wins, reinforces self-compassion, and brings uplifting positivity to your day.'
                '</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="glass-card" style="padding:14px; font-size:0.85rem; border-color: rgba(56,189,248,0.3); margin-bottom: 10px;">'
                '<strong>🧠 Sage:</strong> Uses analytical active listening and gentle cognitive reframing (CBT) to reason through dilemmas.'
                '</div>', 
                unsafe_allow_html=True
            )
            
        st.write("---")
        
        # 2. Advanced AI Settings
        with st.expander("⚙️ AI Mode & API Settings", expanded=False):
            # Check if environment key exists
            env_key = get_configured_api_key()
            if env_key and not st.session_state.gemini_api_key:
                st.session_state.gemini_api_key = env_key

            gemini_api_key = st.text_input(
                "Google Gemini API Key",
                type="password",
                placeholder="Key from Google AI Studio...",
                value=st.session_state.gemini_api_key,
                help="Enter your Gemini API key to activate advanced conversational AI. You can also save it in a .env file."
            )
            st.session_state.gemini_api_key = gemini_api_key
            
            if gemini_api_key:
                st.markdown('<p style="color:#22c55e; font-size:0.85rem; font-weight:600; margin:0;">🟢 Advanced AI Mode Active</p>', unsafe_allow_html=True)
                st.caption("Powered by Google Gemini models.")
            else:
                st.markdown('<p style="color:#38bdf8; font-size:0.85rem; font-weight:600; margin:0;">🔵 Offline Empathy Engine Active</p>', unsafe_allow_html=True)
                st.caption("Using local rules & empathetic knowledge base.")
                
        st.write("---")
        
        # 3. System Reset
        st.markdown('<p style="font-weight:600; color:#ef4444; margin-bottom:5px;">🗑️ Session & Data</p>', unsafe_allow_html=True)
        if st.button("Clear App Data", help="Resets chat history and persistent mood logs.", use_container_width=True):
            clear_all_logs()
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello. I am your emotional companion. How are you feeling today? I am here to listen without judgment."}
            ]
            st.session_state.last_significant_mood = None
            st.session_state.crisis_detected = False
            st.success("App data and chat history reset.")
            st.rerun()
