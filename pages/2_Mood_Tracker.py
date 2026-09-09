import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import custom modules
from utils.styles import apply_custom_styles, render_sidebar
from utils.data_store import load_mood_logs, append_mood_log, populate_sample_data, delete_mood_log

# Try importing Plotly Express
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Mood Tracker & Analytics - Virtual Wellness Companion",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles & unified sidebar
apply_custom_styles()
render_sidebar()

# Page Title & Actions
col_head, col_ctrls = st.columns([3, 2])

with col_head:
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom:0;">📊 Mood Journey & Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.15rem; color:#9ca3af; margin-top:5px; margin-bottom:15px;">Reflect on your emotional patterns and uncover positive lifestyle correlations.</p>', unsafe_allow_html=True)

# Load data
df_logs = load_mood_logs()

with col_ctrls:
    st.write("##")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("✨ Load Sample Data", help="Populates 14 days of realistic sample trends to explore graphs immediately", use_container_width=True):
            populate_sample_data()
            st.success("Sample history loaded!")
            st.rerun()
    with col_b2:
        if not df_logs.empty:
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export CSV",
                data=csv_data,
                file_name=f"mood_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# ==========================================
# --- KPI Summary Metric Cards ---
# ==========================================
if not df_logs.empty:
    total_entries = len(df_logs)
    avg_score = df_logs["score"].mean()
    dominant_mood = df_logs["mood"].value_counts().index[0] if not df_logs["mood"].empty else "N/A"
    
    # Extract top factor
    all_factors = []
    for f_str in df_logs["influencers"].dropna():
        if f_str and f_str not in ["Baseline", "Quick Home Check-In", "Chat Sentiment Analysis"]:
            for item in f_str.split(","):
                clean = item.strip()
                if clean:
                    all_factors.append(clean)
    top_factor = pd.Series(all_factors).value_counts().index[0] if all_factors else "Rest"
    
    st.markdown(
        f'<div class="kpi-container">'
        f'  <div class="kpi-card">'
        f'    <div class="kpi-val">{total_entries}</div>'
        f'    <div class="kpi-lbl">Total Reflections</div>'
        f'  </div>'
        f'  <div class="kpi-card">'
        f'    <div class="kpi-val" style="color:#38bdf8;">{avg_score:.1f} <span style="font-size:1rem; color:#9ca3af;">/10</span></div>'
        f'    <div class="kpi-lbl">Average Score</div>'
        f'  </div>'
        f'  <div class="kpi-card">'
        f'    <div class="kpi-val" style="color:#a78bfa; text-transform:capitalize;">{dominant_mood}</div>'
        f'    <div class="kpi-lbl">Primary Emotion</div>'
        f'  </div>'
        f'  <div class="kpi-card">'
        f'    <div class="kpi-val" style="color:#f59e0b; font-size:1.4rem; padding-top:4px;">{top_factor}</div>'
        f'    <div class="kpi-lbl">Top Lifestyle Driver</div>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ==========================================
# --- Main Content Split ---
# ==========================================
col_logger, col_stats = st.columns([1, 2], gap="large")

with col_logger:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#14b8a6; margin-top:0;">📝 Log Reflection</h3>', unsafe_allow_html=True)
    st.write("Take a mindful pause to record how you feel right now.")
    
    with st.form("mood_logger_form", clear_on_submit=True):
        input_score = st.slider(
            "Wellness Rating (1-10):",
            min_value=1.0,
            max_value=10.0,
            value=6.0,
            step=0.5,
            help="1 = Severe distress, 5 = Centered/Neutral, 10 = Radiantly peaceful and joyful."
        )
        
        input_mood = st.selectbox(
            "Primary Emotional Tone:",
            ["happy", "neutral", "anxious", "sad", "tired", "angry", "lonely", "breakup"]
        )
        
        input_influencers = st.multiselect(
            "Contributing Lifestyle Factors:",
            ["💤 Sleep/Rest", "💼 Work/Study", "👥 Relationships", "🏃 Exercise/Sport", "🌡️ Health", "🍏 Diet/Nutrition", "🧘 Mindfulness", "🎭 Hobbies/Play"]
        )
        
        input_notes = st.text_area(
            "Reflections & Insights (optional):",
            placeholder="What triggered this feeling? What did you learn about yourself today?"
        )
        
        submit_log = st.form_submit_button("Save Reflection", use_container_width=True)
        
        if submit_log:
            clean_factors = [f.split(" ")[-1] for f in input_influencers]
            success = append_mood_log(
                score=input_score,
                mood=input_mood,
                influencers=clean_factors,
                notes=input_notes
            )
            if success:
                st.success("Your reflection has been recorded!")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with col_stats:
    # Filter Controls
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        st.markdown('<h3 style="color:#a78bfa; margin-top:0; margin-bottom:0;">📈 Wellness Analytics</h3>', unsafe_allow_html=True)
    with col_f2:
        timeframe = st.selectbox(
            "Timeframe:",
            ["All Time", "Past 30 Days", "Past 7 Days"],
            label_visibility="collapsed"
        )
        
    # Apply timeframe filter
    df_filtered = df_logs.copy()
    if not df_filtered.empty and "timestamp" in df_filtered.columns:
        now = datetime.now()
        if timeframe == "Past 7 Days":
            cutoff = now - timedelta(days=7)
            df_filtered = df_filtered[df_filtered["timestamp"] >= cutoff]
        elif timeframe == "Past 30 Days":
            cutoff = now - timedelta(days=30)
            df_filtered = df_filtered[df_filtered["timestamp"] >= cutoff]

    if len(df_filtered) <= 1:
        st.info("💡 You currently have 1 or fewer entries in this timeframe. Click **Load Sample Data** above or log a few entries to experience the interactive Plotly graphs!")
    else:
        if PLOTLY_AVAILABLE:
            st.markdown('<p style="font-weight:600; margin-bottom:4px;">Wellness Score Trend</p>', unsafe_allow_html=True)
            
            fig_trend = px.area(
                df_filtered, 
                x="timestamp", 
                y="score",
                hover_data=["mood", "influencers", "notes"],
                color_discrete_sequence=["#14b8a6"]
            )
            fig_trend.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Date & Time"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Rating (1-10)", range=[0.5, 10.5]),
                margin=dict(l=10, r=10, t=10, b=10),
                height=260
            )
            fig_trend.update_traces(
                fill='tozeroy',
                fillcolor='rgba(20, 184, 166, 0.12)',
                line=dict(width=3, color='#14b8a6')
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Split chart columns
            col_pie, col_bar = st.columns(2)
            
            with col_pie:
                st.markdown('<p style="font-weight:600; margin-bottom:4px;">Emotion Breakdown</p>', unsafe_allow_html=True)
                mood_counts = df_filtered["mood"].value_counts().reset_index()
                mood_counts.columns = ["mood", "count"]
                
                fig_donut = px.pie(
                    mood_counts,
                    values="count",
                    names="mood",
                    hole=0.45,
                    color_discrete_sequence=["#14b8a6", "#38bdf8", "#a78bfa", "#f43f5e", "#f59e0b", "#10b981", "#6366f1"]
                )
                fig_donut.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=230,
                    showlegend=True
                )
                st.plotly_chart(fig_donut, use_container_width=True)
                
            with col_bar:
                st.markdown('<p style="font-weight:600; margin-bottom:4px;">Average Score by Lifestyle Factor</p>', unsafe_allow_html=True)
                
                influencer_rows = []
                for _, row in df_filtered.iterrows():
                    infl_str = row["influencers"]
                    if infl_str and infl_str not in ["Baseline", "Quick Home Check-In", "Chat Sentiment Analysis"]:
                        for item in infl_str.split(","):
                            clean_item = item.strip()
                            if clean_item:
                                influencer_rows.append({"factor": clean_item, "score": row["score"]})
                                
                if influencer_rows:
                    df_factors = pd.DataFrame(influencer_rows)
                    df_avg = df_factors.groupby("factor")["score"].mean().reset_index()
                    df_avg = df_avg.sort_values(by="score", ascending=True)
                    
                    fig_factors = px.bar(
                        df_avg,
                        x="score",
                        y="factor",
                        orientation='h',
                        color="score",
                        color_continuous_scale=[[0, '#8b5cf6'], [1, '#14b8a6']]
                    )
                    fig_factors.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Average Score"),
                        yaxis=dict(title="Factor"),
                        coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=230
                    )
                    st.plotly_chart(fig_factors, use_container_width=True)
                else:
                    st.caption("No specific lifestyle factors recorded yet in this timeframe.")
        else:
            st.line_chart(df_filtered, x="timestamp", y="score")

# ==========================================
# --- Reflection Journal Timeline ---
# ==========================================
st.write("---")
st.markdown('<h3 style="color:#ffffff; margin-top:10px;">📖 Reflection Journal Feed</h3>', unsafe_allow_html=True)
st.write("Review past entries, track your thoughts, or prune individual entries:")

if df_logs.empty:
    st.info("No reflection entries found.")
else:
    # Display recent 10 entries in reverse chronological order
    recent_logs = df_logs.tail(10).iloc[::-1]
    
    for idx, row in recent_logs.iterrows():
        ts_str = row["timestamp"].strftime("%b %d, %Y - %I:%M %p") if isinstance(row["timestamp"], datetime) else str(row["timestamp"])
        mood_str = str(row["mood"]).capitalize()
        score_str = f"{row['score']:.1f}/10"
        influencers_str = str(row["influencers"]) if str(row["influencers"]) else "None"
        notes_str = str(row["notes"]) if str(row["notes"]) else "No reflection notes recorded."
        
        with st.expander(f"{ts_str} | {mood_str} ({score_str})", expanded=False):
            col_entry, col_del = st.columns([5, 1])
            with col_entry:
                st.markdown(f"**Emotion:** {mood_str} &nbsp;|&nbsp; **Score:** {score_str} &nbsp;|&nbsp; **Factors:** {influencers_str}")
                st.markdown(f"*{notes_str}*")
            with col_del:
                if st.button("🗑️ Delete", key=f"del_{idx}", help="Remove this entry"):
                    delete_mood_log(idx)
                    st.success("Entry removed.")
                    st.rerun()
