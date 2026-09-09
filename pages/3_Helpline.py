import streamlit as st
from utils.styles import apply_custom_styles, render_sidebar

# Page Setup
st.set_page_config(
    page_title="Emergency Helplines - Virtual Wellness Companion",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global custom styles & unified sidebar
apply_custom_styles()
render_sidebar()

# Page Title
st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom:0;">🚨 Emergency Helpline Directory</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:1.15rem; color:#9ca3af; margin-top:5px; margin-bottom:20px;">'
    'If you, a friend, or a loved one are in immediate distress or having thoughts of self-harm, please reach out right now. '
    'The following resources are <strong>100% free, confidential, and available 24/7</strong>.'
    '</p>', 
    unsafe_allow_html=True
)

# Controls
col_region, col_search = st.columns([2, 1])

with col_region:
    region = st.radio(
        "Select Your Region:",
        [
            "🇺🇸 United States", 
            "🇬🇧 United Kingdom", 
            "🇮🇳 India", 
            "🇨🇦 Canada", 
            "🇦🇺 Australia",
            "🇪🇺 Europe",
            "🌐 International"
        ],
        horizontal=True
    )

with col_search:
    search_query = st.text_input("🔍 Filter by keyword:", placeholder="e.g. youth, veterans, lgbtq, text...").lower()

st.write("##")

# Helpline data dictionary
HELPLINES = {
    "United States": [
        {
            "title": "988 Suicide & Crisis Lifeline",
            "number": "988",
            "tel": "tel:988",
            "meta": "Available 24/7 across the US in English & Spanish. Call or text 988. Free, confidential, and compassionate.",
            "tags": "suicide crisis depression general 24/7"
        },
        {
            "title": "Crisis Text Line",
            "number": "Text HOME to 741741",
            "tel": "sms:741741?body=HOME",
            "meta": "Connect with an empathetic volunteer crisis counselor via SMS anytime, 24/7.",
            "tags": "text sms crisis youth anxiety"
        },
        {
            "title": "The Trevor Project (LGBTQ+ Crisis)",
            "number": "1-866-488-7386",
            "tel": "tel:18664887386",
            "meta": "Dedicated crisis counselors supporting LGBTQ+ youth 24/7. Or text START to 678-678.",
            "tags": "lgbtq youth teens queer trans"
        },
        {
            "title": "Veterans Crisis Line",
            "number": "Dial 988, then Press 1",
            "tel": "tel:988",
            "meta": "Crisis support custom-tailored for Veterans, service members, and their families. Or text 838255.",
            "tags": "veterans military ptsd"
        },
        {
            "title": "National Domestic Violence Hotline",
            "number": "1-800-799-7233",
            "tel": "tel:18007997233",
            "meta": "24/7 confidential support for anyone experiencing domestic violence or relationship abuse.",
            "tags": "domestic abuse violence family safety"
        },
        {
            "title": "SAMHSA National Helpline",
            "number": "1-800-662-4357",
            "tel": "tel:18006624357",
            "meta": "Substance abuse and mental health treatment referral and information service.",
            "tags": "addiction substance drugs alcohol"
        }
    ],
    "United Kingdom": [
        {
            "title": "Samaritans Helpline",
            "number": "116 123",
            "tel": "tel:116123",
            "meta": "Free phone support for anyone struggling to cope, open 365 days a year, 24 hours a day.",
            "tags": "suicide crisis depression general"
        },
        {
            "title": "NHS Mental Health Services",
            "number": "Call 111",
            "tel": "tel:111",
            "meta": "Direct line to local UK National Health Service crisis teams for urgent assessment.",
            "tags": "nhs medical urgent hospital"
        },
        {
            "title": "Shout Crisis Text Line",
            "number": "Text SHOUT to 85258",
            "tel": "sms:85258?body=SHOUT",
            "meta": "A free, confidential 24/7 text support service in the UK for immediate help.",
            "tags": "text sms crisis anxiety youth"
        },
        {
            "title": "PAPYRUS HOPELINE247 (Youth)",
            "number": "0800 068 4141",
            "tel": "tel:08000684141",
            "meta": "Confidential support for children and young people under the age of 35 having thoughts of suicide.",
            "tags": "youth suicide children teens"
        }
    ],
    "India": [
        {
            "title": "Kiran Mental Health Helpline",
            "number": "1800-599-0019",
            "tel": "tel:18005990019",
            "meta": "Official Ministry of Social Justice & Empowerment helpline. 24/7, free, confidential in 13 languages.",
            "tags": "government official national 24/7"
        },
        {
            "title": "AASRA Suicide Prevention",
            "number": "+91-9820466726",
            "tel": "tel:+919820466726",
            "meta": "Mumbai-based 24/7 professional suicide prevention and emotional crisis support.",
            "tags": "suicide crisis aasra"
        },
        {
            "title": "Vandrevala Foundation",
            "number": "+91-9999 666 555",
            "tel": "tel:+919999666555",
            "meta": "Free 24/7 clinical mental health counseling and crisis support across India.",
            "tags": "counseling clinical 24/7"
        },
        {
            "title": "Tele-MANAS",
            "number": "14416 or 1800 891 4416",
            "tel": "tel:14416",
            "meta": "National Tele Mental Health Programme of India offering 24/7 psychiatric assistance.",
            "tags": "government telemanas national"
        }
    ],
    "Canada": [
        {
            "title": "Canada Suicide Crisis Helpline",
            "number": "Call or Text 988",
            "tel": "tel:988",
            "meta": "Bilingual (English & French) support available 24/7 for anyone in Canada. Free and confidential.",
            "tags": "suicide crisis 988 general"
        },
        {
            "title": "Kids Help Phone",
            "number": "1-800-668-6868",
            "tel": "tel:18006686868",
            "meta": "24/7 phone support and crisis text line (text CONNECT to 686868) for Canadian youth.",
            "tags": "youth children text"
        },
        {
            "title": "Hope for Wellness Helpline",
            "number": "1-855-242-3310",
            "tel": "tel:18552423310",
            "meta": "Immediate mental health counseling and crisis intervention for Indigenous peoples across Canada.",
            "tags": "indigenous first nations inuit"
        }
    ],
    "Australia": [
        {
            "title": "Lifeline Australia",
            "number": "13 11 14",
            "tel": "tel:131114",
            "meta": "24/7 crisis support and suicide prevention services across Australia. Or text 0477 13 11 14.",
            "tags": "lifeline suicide crisis 24/7"
        },
        {
            "title": "Beyond Blue",
            "number": "1300 22 4636",
            "tel": "tel:1300224636",
            "meta": "24/7 mental health information and support for depression, anxiety, and general distress.",
            "tags": "depression anxiety general"
        },
        {
            "title": "Kids Helpline (Australia)",
            "number": "1800 55 1800",
            "tel": "tel:1800551800",
            "meta": "Free private 24/7 telephone counseling service specifically for young people aged 5 to 25.",
            "tags": "youth children teens"
        }
    ],
    "Europe": [
        {
            "title": "European Emergency Number",
            "number": "112",
            "tel": "tel:112",
            "meta": "Universal emergency telephone number available free of charge across all European Union member states.",
            "tags": "emergency police ambulance urgent"
        },
        {
            "title": "SOS Amitié (France)",
            "number": "09 72 39 40 50",
            "tel": "tel:0972394050",
            "meta": "24/7 listening and emotional support service throughout France.",
            "tags": "france europe crisis"
        },
        {
            "title": "TelefonSeelsorge (Germany)",
            "number": "0800 111 0 111",
            "tel": "tel:08001110111",
            "meta": "Free confidential 24/7 counseling service across Germany.",
            "tags": "germany europe crisis"
        }
    ],
    "International": [
        {
            "title": "Find A Helpline (Global)",
            "number": "Visit findahelpline.com",
            "tel": "https://findahelpline.com",
            "meta": "Free, confidential crisis support from local organizations in over 130 countries.",
            "tags": "global search directory international"
        },
        {
            "title": "Befrienders Worldwide",
            "number": "Visit befrienders.org",
            "tel": "https://www.befrienders.org",
            "meta": "A worldwide network of emotional support helplines in dozens of languages.",
            "tags": "befrienders worldwide international"
        },
        {
            "title": "IASP Suicide Prevention Directory",
            "number": "Visit iasp.info/resources/Crisis_Centres",
            "tel": "https://www.iasp.info/resources/Crisis_Centres",
            "meta": "Global directory of crisis centers verified by the International Association for Suicide Prevention.",
            "tags": "iasp directory global"
        }
    ]
}

# Determine active region list
active_key = "United States"
for k in HELPLINES.keys():
    if k in region:
        active_key = k
        break

lines = HELPLINES[active_key]

# Apply filter
if search_query:
    lines = [
        item for item in lines
        if search_query in item["title"].lower() or search_query in item["meta"].lower() or search_query in item["tags"].lower()
    ]

# Render Grid
if not lines:
    st.info(f"No helplines matching '{search_query}' found in {active_key}. Showing all available resources:")
    lines = HELPLINES[active_key]

cards_html = '<div class="help-grid">'
for item in lines:
    btn_label = "🌐 Open Resource" if item["tel"].startswith("http") else "📞 Call / Contact"
    cards_html += f"""
    <div class="help-card">
        <div>
            <div class="help-title">{item['title']}</div>
            <div class="help-number">{item['number']}</div>
            <div class="help-meta">{item['meta']}</div>
        </div>
        <a href="{item['tel']}" target="_blank" class="tel-btn">{btn_label}</a>
    </div>
    """
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)

# Immediate Grounding Safety Plan
st.write("##")
st.markdown(
    '<div class="glass-card" style="border-color: rgba(20,184,166,0.25); padding:24px;">'
    '  <h3 style="color:#14b8a6; margin-top:0;">🛑 Immediate Crisis Grounding Routine</h3>'
    '  <p style="color:#d1d5db; line-height:1.6;">If you feel an overwhelming impulse or panic wave right now, try this 3-step anchor before making any decisions:</p>'
    '  <ol style="color:#e2e8f0; line-height:1.8; margin-bottom:0;">'
    '    <li><strong>Somatic temperature shift:</strong> Splash cold water on your face or hold an ice cube in your palm for 30 seconds to initiate the mammalian dive reflex.</li>'
    '    <li><strong>Firm physical touch:</strong> Place both feet firmly flat on the ground. Push your hands together firmly and focus on the contact points.</li>'
    '    <li><strong>Reach out right now:</strong> Call or text one of the free numbers listed above. You do not have to explain everything perfectly—just say, <em>"I\'m feeling overwhelmed and need someone to talk to."</em></li>'
    '  </ol>'
    '</div>',
    unsafe_allow_html=True
)
