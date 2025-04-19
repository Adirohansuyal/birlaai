"""
UI Helper functions for the Symptom Checker application.
This module provides functions to help with UI rendering.
"""

import streamlit as st
import base64
from pathlib import Path


def local_css(file_name):
    """
    Load local CSS file
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def display_header():
    """
    Display the application header
    """
    # Title with icon and styling
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <h1 style="margin: 0; display: inline-block;">🏥 Birla AI Symptoms Checker</h1>
    </div>
    <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
        Enter your symptoms for a comprehensive health analysis powered by AI
    </p>
    """,
                unsafe_allow_html=True)


def display_medical_disclaimer(expanded=True):
    """
    Display the medical disclaimer
    """
    with st.expander("⚠️ IMPORTANT MEDICAL DISCLAIMER", expanded=expanded):
        st.warning("""
            This tool is for informational purposes only and does not provide medical advice.
            
            The content provided by this application is not a substitute for professional medical 
            advice, diagnosis, or treatment. Always seek the advice of your physician or other 
            qualified health provider with any questions you may have regarding a medical condition.
            
            If you are experiencing a medical emergency, please call your local emergency number 
            or go to the nearest emergency room immediately.
            """)


def display_risk_badge(risk_level):
    """
    Display a styled risk level badge
    """
    risk_level = risk_level.lower()
    if risk_level == "high":
        badge_html = """
        <div class="risk-badge risk-high">
            ⚠️ HIGH RISK
        </div>
        """
    elif risk_level == "moderate":
        badge_html = """
        <div class="risk-badge risk-moderate">
            ⚠️ MODERATE RISK
        </div>
        """
    elif risk_level == "low":
        badge_html = """
        <div class="risk-badge risk-low">
            ✅ LOW RISK
        </div>
        """
    else:
        badge_html = """
        <div class="risk-badge" style="background-color: #E0E0E0; color: #757575; border: 1px solid #BDBDBD;">
            ℹ️ UNKNOWN RISK
        </div>
        """

    st.markdown(badge_html, unsafe_allow_html=True)


def display_medical_attention_alert(seek_medical_attention):
    """
    Display a styled medical attention alert
    """
    if seek_medical_attention:
        st.markdown("""
        <div style="background-color: #ffebee; border-left: 5px solid #c62828; padding: 1rem; border-radius: 4px; margin: 1rem 0;">
            <h3 style="color: #c62828; margin-top: 0;">🚨 SEEK MEDICAL ATTENTION</h3>
            <p>Based on your symptoms, we recommend consulting a healthcare professional as soon as possible.</p>
        </div>
        """,
                    unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #e8f5e9; border-left: 5px solid #388e3c; padding: 1rem; border-radius: 4px; margin: 1rem 0;">
            <h3 style="color: #388e3c; margin-top: 0;">ℹ️ MONITOR YOUR SYMPTOMS</h3>
            <p>Based on your symptoms, immediate medical attention may not be necessary. However, monitor your condition and consult a healthcare provider if symptoms persist or worsen.</p>
        </div>
        """,
                    unsafe_allow_html=True)


def display_symptom_list(symptoms):
    """
    Display a styled list of symptoms
    """
    st.markdown('<ul class="symptom-list">', unsafe_allow_html=True)
    for symptom in symptoms:
        st.markdown(f'<li>{symptom}</li>', unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)


def display_condition_card(condition):
    """
    Display a styled condition card
    """
    st.markdown(f"""
    <div class="condition-card">
        <h4>{condition['name']}</h4>
        <p><strong>Description:</strong> {condition['description']}</p>
        <p><strong>Common Symptoms:</strong></p>
        <ul>
    """,
                unsafe_allow_html=True)

    for symptom in condition.get('common_symptoms', []):
        st.markdown(f'<li>{symptom}</li>', unsafe_allow_html=True)

    st.markdown('</ul>', unsafe_allow_html=True)

    # Diet recommendations
    if condition.get('diet_recommendations', []):
        st.markdown('<p><strong>Diet Recommendations:</strong></p><ul>',
                    unsafe_allow_html=True)
        for recommendation in condition.get('diet_recommendations', []):
            st.markdown(f'<li>{recommendation}</li>', unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def display_chat_message(message, is_user=False):
    """
    Display a styled chat message
    """
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {message}
        </div>
        """,
                    unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message ai-message">
            <strong>AI Assistant:</strong><br>
            {message}
        </div>
        """,
                    unsafe_allow_html=True)


def display_footer():
    """
    Display the application footer
    """
    st.markdown("""
    <div class="footer">
        <p>© 2025 Birla AI Symptom Checker | This application is for informational purposes only</p>
        <p>Designed by Aditya Suyal @Birla Institute of Applied Sciences</p>
    </div>
    """,
                unsafe_allow_html=True)
