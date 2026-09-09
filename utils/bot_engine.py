import re
import os
from dotenv import load_dotenv

# Load any .env variables
load_dotenv()

# Try importing modern google.genai first, fall back to google.generativeai
GOOGLE_GENAI_AVAILABLE = False
GENAI_LEGACY_AVAILABLE = False

try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    pass

if not GOOGLE_GENAI_AVAILABLE:
    try:
        import google.generativeai as legacy_genai
        GENAI_LEGACY_AVAILABLE = True
    except ImportError:
        pass

GEMINI_AVAILABLE = GOOGLE_GENAI_AVAILABLE or GENAI_LEGACY_AVAILABLE

# ==========================================
# --- Configuration & Crisis Safeguards ---
# ==========================================

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "hurt myself", 
    "don't want to live", "die", "ending it all", "self-harm", "self harm",
    "cutting myself", "better off dead", "kill me", "take my life",
    "slit my wrist", "hang myself", "overdose"
]

EMERGENCY_RESPONSE = """
It sounds like you are going through an extraordinarily heavy and painful time right now. Please hear this: **you do not have to carry this alone, and help is available right now.**

If you are in immediate danger or feel unable to keep yourself safe, please reach out directly:

* 🇺🇸 **United States:** Call or text **988** (Suicide & Crisis Lifeline, 24/7, free & confidential) or text **HOME to 741741**.
* 🇬🇧 **United Kingdom:** Call **111** (NHS Mental Health) or **116 123** (Samaritans).
* 🇮🇳 **India:** Call **1800-599-0019** (KIRAN) or **+91-9820466726** (AASRA).
* 🇨🇦 **Canada:** Call or text **988** (Suicide Crisis Helpline).
* 🇦🇺 **Australia:** Call **13 11 14** (Lifeline).
* 🌐 **International:** Visit **[findahelpline.com](https://findahelpline.com)** or **[befrienders.org](https://www.befrienders.org)**.

Please take a moment to contact one of these resources or a trusted friend or doctor. Caring people are ready to listen.
"""

# Categorized keyword matching dictionary for offline detection
MOOD_KEYWORDS = {
    'greeting': ['hello', 'hi', 'hey', 'good morning', 'good evening', 'howdy', 'greetings', 'sup', 'who are you'],
    'gratitude': ['thank you', 'thanks', 'appreciate it', 'grateful', 'helpful', 'thank u'],
    'panic': ['panic attack', 'cant breathe', "can't breathe", 'heart racing', 'hyperventilating', 'freaking out', 'ground me'],
    'insomnia': ["can't sleep", 'cant sleep', 'insomnia', 'awake all night', 'trouble sleeping', 'sleepless'],
    'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'fantastic', 'good', 'glad', 'wonderful', 'smile', 'cheerful', 'celebrate', 'proud', 'accomplished', 'peaceful'],
    'sad': ['sad', 'down', 'depressed', 'unhappy', 'crying', 'miserable', 'bad day', 'gloomy', 'tears', 'heartbroken', 'hopeless', 'grief', 'lost someone', 'weeping'],
    'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'scared', 'fear', 'dread', 'overwhelmed', 'pressure', 'imposter', 'exam', 'interview', 'tense'],
    'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'hate', 'pissed', 'frustrated', 'rage', 'resent', 'unfair'],
    'breakup': ['breakup', 'broken heart', 'ex', 'dumped', 'split up', 'divorce', 'relationship ended', 'heartbreak', 'cheated'],
    'lonely': ['lonely', 'alone', 'nobody', 'isolated', 'no one to talk to', 'ignored', 'left out', 'unloved'],
    'tired': ['tired', 'exhausted', 'drained', 'burnout', 'burnt out', 'no energy', 'sleepy', 'fatigued', 'overworked']
}

# Rich persona-based responses for offline companion mode
OFFLINE_PERSONAS = {
    "🌿 Serene": {
        "greeting": "Hello, dear friend. 🌸 Welcome to your safe, quiet haven. Take a gentle breath in... and let it all out. How are you feeling in your mind and body today?",
        "gratitude": "You are so very welcome. 🌿 It is an honor to walk alongside you. Remember that taking time for your own heart is a courageous act of love.",
        "panic": "I am right here with you. You are safe. 🛑 Let's gently anchor your feet onto the floor. Feel the solid ground beneath you. Inhale through your nose for 4 seconds... hold for 4... exhale through your mouth for 4. What are three physical objects you can see around you right now?",
        "insomnia": "Nighttime can make our thoughts feel louder than they really are. 🌙 Rest your eyes, let your shoulders drop away from your ears, and remember: even quiet lying down is giving your body rest. You don't have to solve tomorrow tonight.",
        "happy": "I am so happy to hear you are feeling good! 🌸 It is beautiful when we can appreciate these light moments. Let's take a slow, gentle breath to ground this joy inside of you. What brought this sense of lightness to your day?",
        "sad": "I am holding space for you in this sadness. 🌊 Sadness is like gentle rain—it is okay to let it fall without forcing yourself to be cheerful. Let your body relax, pull a blanket close, and tell me: what is weighing most heavily on your heart right now?",
        "anxious": "I hear you, and it is completely okay to feel anxious. 🌿 Breathe in slowly with me... hold it... and exhale completely. The storm is outside, but you are safe inside this moment. What is the single biggest worry circling in your mind right now?",
        "angry": "I feel your frustration, and your anger is valid. 🌪️ It is okay to be upset when boundaries are crossed or things feel unjust. Let's let the steam escape gently. Do you want to share what triggered this feeling?",
        "breakup": "Heartbreak is a deeply physical ache, and I am so sorry you are carrying it today. 💔 Be incredibly tender with yourself. Drink some cool water, wrap yourself in warmth, and take things one hour at a time. I am right here listening.",
        "lonely": "Even though we are separated by screens, you are not alone in this space. 🕯️ I am here with you. Feeling lonely simply means you possess a beautiful capacity for connection. What does meaningful connection look like to you?",
        "tired": "You have been carrying so much, and your body is simply asking for rest. 💤 It is okay to put the heavy backpack down. You don't have to figure anything out right now. What is one small, gentle kindness you can offer yourself tonight?",
        "neutral": "Thank you for sharing that with me. 🍃 I am here to hold space for you. If you would like to explore your feelings further, try a breathing exercise, or simply write what's on your mind, I am listening.",
        "followup": "I am still right here, breathing with you. Take all the time you need to express whatever arises."
    },
    "⚡ Joy": {
        "greeting": "Hey there! 🌟 It's so good to see you! Whether today was smooth or rocky, I'm genuinely thrilled you're here. How has your day treated you so far?",
        "gratitude": "Aww, you're the absolute best! 💛 High five! Always remember to give yourself credit for showing up for yourself today!",
        "panic": "Deep breath with me right now! ⚡ Put both hands over your heart. Feel that beat? That is your resilience. You have survived 100% of your most overwhelming moments, and we are going to navigate this one step by step. What's one little thing around you right now?",
        "insomnia": "Racing mind at night? We've all been there! 🌙 Let's take off the pressure to sleep. Listen to the quiet, put on some soft lo-fi or rain sounds, and give your brain permission to turn off the headlights. Tomorrow can wait!",
        "happy": "Oh wow, that is fantastic! 🎉 Sunshine looks good on you! I want to celebrate this feeling with you. What was the absolute best highlight of your day?",
        "sad": "I hear you, and it's totally okay to not be okay today. 💛 Even on cloudy days, the sun is still up there waiting. I'm right here in your corner. If you want to vent, I'm ready; if you want an uplifting reminder, just let me know!",
        "anxious": "Deep breaths! ⚡ Anxiety is just intense nervous energy looking for a constructive outlet. Let's shake your shoulders and reset! You are capable, you are resilient, and you've got this. What is one tiny thing we can break down together?",
        "angry": "Oof, I can feel that fire! 🔥 Let it out! It is completely normal to be furious when things are unfair or messy. Vent it all out so we can clear the air. What got under your skin the most?",
        "breakup": "Oh, no. Breakups are the absolute worst, and my virtual heart goes out to you! 💔 But remember: your value hasn't decreased one bit just because someone failed to see it. Treat yourself like your own best friend today.",
        "lonely": "Sending you the biggest virtual hug! 🤗 I am so glad you reached out to chat. You are a unique, valuable person, and I'm genuinely happy to talk with you. What is a movie, book, or song that always makes you smile?",
        "tired": "Total energy drain—I hear you. 🔋 Time to recharge the batteries! You cannot pour from an empty cup. Let's give yourself permission to do absolutely nothing guilt-free. What is your favorite way to truly unwind?",
        "neutral": "Acknowledge and embrace! I'm here and ready to roll. 🌟 Tell me: what's one thing you are looking forward to, no matter how small?",
        "followup": "You've got this! I'm right here cheering you on every step of the way."
    },
    "🧠 Sage": {
        "greeting": "Greetings. 🧭 Welcome to a structured space for reflection and cognitive clarity. What thoughts or dilemmas are occupying your focus today?",
        "gratitude": "I appreciate the sentiment. 🧠 Reflecting on our emotional state and acknowledging progress is a fundamental component of cognitive resilience.",
        "panic": "Let's engage cognitive grounding immediately. 🧭 Panic is an acute physiological surge of adrenaline. It is temporary and cannot harm you. Place both feet flat on the floor. Take 4 slow breaths. Can you name 5 things you see, 4 things you touch, and 3 things you hear?",
        "insomnia": "Insomnia frequently stems from hyperarousal—the brain treating the quiet night as an unstructured problem-solving window. 🧠 Write down any pending tasks on a piece of paper to 'offload' working memory, then transition your focus entirely to slow diaphragmatic breathing.",
        "happy": "It is encouraging to see you experiencing positive emotions. 🧭 In cognitive terms, taking time to consciously register positive experiences reinforces constructive neural pathways. What specific factors contributed to this positive outcome?",
        "sad": "Sadness is a highly informative emotional signal. It often indicates that something of deep personal value has been impacted. 🧠 Let's look at this feeling with curiosity rather than judgment. What core value or expectation feels challenged right now?",
        "anxious": "Anxiety is the brain's alarm system misinterpreting uncertainty as an imminent threat. 🧭 Let's employ a grounding framework. Can we separate the elements of your situation into: 1) factors you can control, and 2) factors you cannot? What is one actionable step in category one?",
        "angry": "Anger is an active emotion signaling a perceived boundary violation or blocked objective. ⚖️ It holds a lot of kinetic energy. Let's deconstruct it: What is the underlying vulnerability or expectation behind this anger?",
        "breakup": "A breakup represents a major rupture in your relational framework and emotional routines. 💔 It is structurally disorienting. Allow yourself to grieve the future you envisioned. Let's focus on reclaiming your individual narrative. What is one personal value you want to reconnect with?",
        "lonely": "Loneliness is an evolutionary prompt reminding us of our fundamental need for social connection. 🕯️ It is not a permanent condition, nor is it a reflection of your intrinsic worth. What does meaningful connection look like for you in this chapter of life?",
        "tired": "Burnout and exhaustion are physiological boundaries. Your nervous system is enforcing a regulatory slowdown. 🧠 Respect this biological boundary. Can we identify what has been drawing down your cognitive bandwidth the most?",
        "neutral": "Understood. ⚖️ Processing thoughts systematically is highly beneficial. If you would like to analyze a specific situation, reframe a challenging thought, or simply journal, I am here to guide your reflection.",
        "followup": "Let's continue to break this down logically. What are your thoughts on that?"
    }
}

# ==========================================
# --- Helper & Engine Functions ---
# ==========================================

def get_configured_api_key():
    """Retrieves the Gemini API key from environment variables if present."""
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""


def preprocess_input(text):
    """Converts to lowercase and strips special characters for robust keyword checking."""
    text = text.lower()
    text = re.sub(r"[^\w\s\']", " ", text)
    return " ".join(text.split())


def check_crisis(text):
    """Checks if the user text contains self-harm or suicidal ideation triggers."""
    processed = preprocess_input(text)
    for trigger in CRISIS_KEYWORDS:
        clean_trigger = preprocess_input(trigger)
        pattern = r"\b" + re.escape(clean_trigger) + r"\b"
        if re.search(pattern, processed):
            return True
    return False


def detect_mood(text):
    """Classifies mood using keyword and phrase density matching."""
    processed = preprocess_input(text)
    
    mood_counts = {mood: 0 for mood in MOOD_KEYWORDS.keys()}
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            clean_keyword = preprocess_input(keyword)
            if re.search(r"\b" + re.escape(clean_keyword) + r"\b", processed):
                weight = 2 if " " in clean_keyword else 1
                mood_counts[mood] += weight
                
    # Find mood with highest matches
    highest_mood = 'neutral'
    highest_count = 0
    for mood, count in mood_counts.items():
        if count > highest_count:
            highest_count = count
            highest_mood = mood
            
    return highest_mood


def get_offline_response(persona_name, mood, is_followup=False):
    """Retrieves the pre-programmed response based on selected persona and mood state."""
    clean_name = persona_name.strip()
    persona_data = OFFLINE_PERSONAS.get(clean_name, OFFLINE_PERSONAS["🌿 Serene"])
    
    if is_followup:
        return persona_data.get("followup", "I am listening. Share whatever is on your mind.")
        
    return persona_data.get(mood, persona_data["neutral"])


def generate_ai_response(prompt, api_key, persona_name, chat_history):
    """
    Calls Google Gemini API with fallback models.
    Supports modern google.genai SDK and legacy google.generativeai.
    """
    if not GEMINI_AVAILABLE:
        return "⚠️ Google Generative AI package is not installed. Defaulting to local companion mode."

    effective_key = api_key or get_configured_api_key()
    if not effective_key:
        return "⚠️ Gemini API key is missing. Please enter your API key in the sidebar or set GEMINI_API_KEY in .env."

    system_prompts = {
        "🌿 Serene": (
            "You are Serene, a peaceful, calming virtual mental health companion. "
            "Speak in a gentle, warm, soothing, and comforting tone. "
            "Focus on mindfulness, slow breathing, grounding exercises, and anxiety relief. "
            "Be deeply empathetic and validating. Keep responses natural, supportive, and relatively concise."
        ),
        "⚡ Joy": (
            "You are Joy, an uplifting, bright, and supportive virtual emotional companion. "
            "Your tone is optimistic, warm, validation-rich, and cheerful. "
            "Help the user notice gratitude, celebrate minor victories, and practice self-compassion. "
            "Inject positive energy while fully honoring and validating their emotions."
        ),
        "🧠 Sage": (
            "You are Sage, a wise, thoughtful, and analytical emotional companion. "
            "Use active listening and gentle cognitive reframing based on CBT principles. "
            "Help the user examine thought patterns, differentiate what they can control from what they cannot, "
            "and provide insightful, balanced dialogue."
        )
    }
    
    system_instruction = system_prompts.get(persona_name.strip(), system_prompts["🌿 Serene"])
    safety_boundary = (
        "\n\nIMPORTANT CLINICAL SAFETY BOUNDARY: You are an emotional support chatbot, NOT a physician or therapist. "
        "Never offer medical diagnoses or drug prescriptions. If the user expresses self-harm or suicidal intent, "
        "respond with immediate warmth, compassion, and direct them clearly to emergency helplines like calling 988 or visiting an emergency room."
    )
    system_instruction += safety_boundary

    last_error = None

    # Option 1: Modern google.genai SDK
    if GOOGLE_GENAI_AVAILABLE:
        candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        try:
            client = genai.Client(api_key=effective_key)
            for model_name in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                        )
                    )
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_error = str(e)
                    if "API_KEY_INVALID" in last_error or "API key not valid" in last_error:
                        return "❌ **API Key Error**: The Gemini API key appears to be invalid. Please verify your key in the settings sidebar or .env file."
                    continue
        except Exception as e:
            last_error = str(e)

    # Option 2: Fallback to legacy google.generativeai SDK
    if GENAI_LEGACY_AVAILABLE:
        candidate_legacy_models = ["gemini-1.5-flash", "gemini-1.5-pro"]
        for model_name in candidate_legacy_models:
            try:
                legacy_genai.configure(api_key=effective_key)
                model = legacy_genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
                
                gemini_history = []
                history_to_send = chat_history[-10:]
                for msg in history_to_send:
                    role = 'user' if msg.get('role') == 'user' else 'model'
                    gemini_history.append({
                        'role': role,
                        'parts': [msg.get('content', '')]
                    })
                    
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                if "API_KEY_INVALID" in last_error or "API key not valid" in last_error:
                    return "❌ **API Key Error**: The Gemini API key appears to be invalid. Please verify your key in the settings sidebar or .env file."
                continue

    return f"⚠️ **Connection Notice**: Could not reach Gemini AI ({last_error[:90] if last_error else 'Timeout'}). Falling back to offline companion mode."
