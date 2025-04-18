import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Using our local symptom analyzer instead of OpenAI
from utils.symptom_analyzer import analyze_symptoms
from data.symptoms import COMMON_SYMPTOMS, BODY_SYSTEMS, SYMPTOM_SEVERITY, SYMPTOM_DURATION

def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Symptom Checker",
        page_icon="🏥",
        layout="wide"
    )
    
    # App title and introduction
    st.title("🏥 Symptom Checker")
    
    # Medical disclaimer
    with st.expander("⚠️ IMPORTANT MEDICAL DISCLAIMER - Please Read", expanded=True):
        st.warning(
            """
            This tool is for informational purposes only and does not provide medical advice.
            
            The content provided by this application is not a substitute for professional medical 
            advice, diagnosis, or treatment. Always seek the advice of your physician or other 
            qualified health provider with any questions you may have regarding a medical condition.
            
            If you are experiencing a medical emergency, please call your local emergency number 
            or go to the nearest emergency room immediately.
            """
        )
    
    # Sidebar for user information input
    st.sidebar.header("User Information")
    
    # User information form
    with st.sidebar.form("user_info_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        # Symptom selection
        st.subheader("Select Your Symptoms")
        
        # Allow users to select from common symptoms or add their own
        selected_symptoms = st.multiselect(
            "Select symptoms from the list",
            options=COMMON_SYMPTOMS,
            default=None
        )
        
        # Additional custom symptoms
        custom_symptoms = st.text_input("Add other symptoms (comma-separated)")
        
        # Symptom details
        duration = st.selectbox("Duration of Symptoms", SYMPTOM_DURATION)
        severity = st.selectbox("Severity of Symptoms", SYMPTOM_SEVERITY)
        
        # Additional information
        additional_info = st.text_area("Additional Information (allergies, medical history, etc.)")
        
        # Submit button
        submit_button = st.form_submit_button("Analyze Symptoms")
    
    # Process user input when the form is submitted
    if submit_button:
        # Validate input
        if not selected_symptoms and not custom_symptoms:
            st.error("Please select at least one symptom.")
            return
        
        # Process custom symptoms if provided
        all_symptoms = selected_symptoms.copy()
        if custom_symptoms:
            custom_symptoms_list = [s.strip() for s in custom_symptoms.split(',') if s.strip()]
            all_symptoms.extend(custom_symptoms_list)
        
        # Show processing message
        with st.spinner("Analyzing your symptoms..."):
            # Call local symptom analyzer
            analysis_result = analyze_symptoms(
                all_symptoms, 
                age, 
                gender, 
                duration, 
                severity, 
                additional_info
            )
        
        # Check for error
        if analysis_result.get("error", False):
            st.error(analysis_result.get("message", "An error occurred during analysis."))
            return
        
        # Display results
        display_results(analysis_result, all_symptoms)
    
    # Information section about the app
    st.sidebar.markdown("---")
    st.sidebar.subheader("About this App")
    st.sidebar.info(
        """
        This Symptom Checker uses a comprehensive symptom database to analyze your symptoms and 
        provide potential health conditions, advice, and diet recommendations.
        
        Remember that this tool does not replace professional medical advice.
        """
    )

def display_results(analysis, symptoms):
    """Display the analysis results in a structured format."""
    st.header("Analysis Results")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display risk level with color-coded alert
        risk_level = analysis.get("risk_level", "unknown").lower()
        
        if risk_level == "high":
            st.error(f"⚠️ Risk Level: HIGH")
        elif risk_level == "moderate":
            st.warning(f"⚠️ Risk Level: MODERATE")
        elif risk_level == "low":
            st.success(f"✅ Risk Level: LOW")
        else:
            st.info(f"ℹ️ Risk Level: UNKNOWN")
        
        # Medical attention recommendation
        seek_medical_attention = analysis.get("seek_medical_attention", False)
        if seek_medical_attention:
            st.error("🚨 RECOMMENDATION: Please seek medical attention!")
        else:
            st.info("ℹ️ Based on your symptoms, immediate medical attention may not be necessary, but consult a healthcare provider if symptoms persist or worsen.")
    
    with col2:
        # Display reported symptoms
        st.subheader("Your Reported Symptoms:")
        for symptom in symptoms:
            st.write(f"• {symptom}")
    
    # Display possible conditions
    st.subheader("Possible Conditions")
    possible_conditions = analysis.get("possible_conditions", [])
    
    if not possible_conditions:
        st.info("No specific conditions identified. Please consult a healthcare professional.")
    else:
        # Create tabs for each possible condition
        condition_tabs = st.tabs([condition["name"] for condition in possible_conditions])
        
        for i, tab in enumerate(condition_tabs):
            condition = possible_conditions[i]
            with tab:
                st.markdown(f"### {condition['name']}")
                st.markdown(f"**Description:** {condition['description']}")
                
                # Common symptoms
                st.markdown("**Common Symptoms:**")
                for symptom in condition.get("common_symptoms", []):
                    st.write(f"• {symptom}")
                
                # Diet recommendations
                st.markdown("**Diet Recommendations:**")
                for recommendation in condition.get("diet_recommendations", []):
                    st.write(f"• {recommendation}")
    
    # General advice
    st.subheader("General Health Advice")
    st.info(analysis.get("general_advice", "No specific advice available."))
    
    # Medical sources
    st.subheader("Medical Sources")
    sources = analysis.get("medical_sources", [])
    for source in sources:
        st.write(f"• {source}")
    
    # Reminder about medical advice
    st.markdown("---")
    st.warning(
        """
        **Remember:** This analysis is based on the symptoms you provided and is not a medical diagnosis.
        The information provided should not replace professional medical advice.
        If you're concerned about your health, please consult a healthcare professional.
        """
    )

if __name__ == "__main__":
    main()
