import streamlit as st
from utils.bot_engine import (
    check_crisis,
    detect_mood,
    get_offline_response,
    generate_ai_response,
    get_configured_api_key,
    EMERGENCY_RESPONSE
)

__all__ = [
    'check_crisis',
    'detect_mood',
    'get_offline_response',
    'generate_ai_response',
    'get_configured_api_key',
    'EMERGENCY_RESPONSE'
]

def bot_reply(msg):
    """
    Simple compatibility helper matching the notebook's early prototype signature.
    Routes to the offline/engine responses.
    """
    if check_crisis(msg):
        return EMERGENCY_RESPONSE
    
    mood = detect_mood(msg)
    return get_offline_response("🌿 Serene", mood)
