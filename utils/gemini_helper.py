"""
Helper functions for using Google's Gemini API for symptom analysis
"""

import os
import json
import google.generativeai as genai

# Get API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_symptoms(symptoms, age, gender, duration, severity, additional_info=""):
    """
    Analyze symptoms using Google's Gemini API and return possible conditions,
    health advice, and diet recommendations.
    
    Args:
        symptoms (list): List of user-reported symptoms
        age (int): User's age
        gender (str): User's gender
        duration (str): Duration of symptoms
        severity (str): Severity of symptoms
        additional_info (str): Any additional information provided by the user
        
    Returns:
        dict: Dictionary containing analysis results
    """
    # Format symptoms for prompt
    symptoms_text = ", ".join(symptoms)
    
    # Create a structured prompt for the AI
    prompt = f"""
    Act as a medical advisor. Based on the following information, provide an analysis:
    
    Patient Information:
    - Age: {age}
    - Gender: {gender}
    - Symptoms: {symptoms_text}
    - Duration: {duration}
    - Severity: {severity}
    - Additional Information: {additional_info}
    
    Please analyze these symptoms and provide the following information in JSON format:
    
    1. Possible conditions (list at least 3, at most 5, with brief descriptions)
    2. Risk level (low, moderate, high)
    3. Whether immediate medical attention is recommended (true/false)
    4. General health advice related to these symptoms
    5. Diet recommendations for each possible condition
    6. Reliable medical sources to consult (at least 2)
    
    Important: For each condition, provide:
    - Name
    - Brief description
    - Common symptoms
    - Diet recommendations specific to this condition
    
    Your response should be structured as a valid JSON object with the following format:
    {{
        "possible_conditions": [
            {{
                "name": "Condition name",
                "description": "Brief description",
                "common_symptoms": ["symptom1", "symptom2"],
                "diet_recommendations": ["recommendation1", "recommendation2"]
            }}
        ],
        "risk_level": "low/moderate/high",
        "seek_medical_attention": true/false,
        "general_advice": "General health advice text",
        "medical_sources": ["Source 1", "Source 2"]
    }}
    
    Include a clear disclaimer that this is not a medical diagnosis.
    """
    
    try:
        # Get available models to use the correct one
        models = genai.list_models()
        available_models = [model.name for model in models]
        
        # Try to find the best available model (prefer gemini-1.5-pro or gemini-1.0-pro)
        model_name = None
        for candidate in ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
            for available in available_models:
                if candidate in available:
                    model_name = available
                    break
            if model_name:
                break
        
        # If no matching model found, use the first available text model
        if not model_name:
            for model in models:
                if hasattr(model, 'supported_generation_methods') and 'generateContent' in model.supported_generation_methods:
                    model_name = model.name
                    break
        
        if not model_name:
            raise Exception("No suitable generative models found in your Google API account")
            
        # Setup the model
        model = genai.GenerativeModel(model_name)
        
        # Call the Gemini API
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [prompt]}
            ],
            generation_config={"temperature": 0.2}  # Lower temperature for more consistent results
        )
        
        # Process and extract JSON from the response
        response_text = response.text
        
        # Sometimes the model returns the JSON with surrounding text, so we need to extract it
        try:
            # First, try to parse the entire response
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON between curly braces
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                result = json.loads(json_str)
            else:
                raise Exception("Failed to extract valid JSON from the response")
        
        return result
    
    except Exception as e:
        # Return error information
        return {
            "error": True,
            "message": f"Error analyzing symptoms: {str(e)}",
            "possible_conditions": [],
            "risk_level": "unknown",
            "seek_medical_attention": True,
            "general_advice": "We encountered an error analyzing your symptoms. Please try again or consult a healthcare professional.",
            "medical_sources": ["https://www.who.int", "https://www.mayoclinic.org"]
        }

# Add a function to provide a conversational response for specific symptoms
def get_symptom_conversation(symptoms, previous_conversation=None):
    """
    Get a conversational response about the user's symptoms
    
    Args:
        symptoms (list): List of user-reported symptoms
        previous_conversation (list, optional): Previous conversation history
        
    Returns:
        str: Conversational response from the AI
    """
    if not previous_conversation:
        previous_conversation = []
    
    symptoms_text = ", ".join(symptoms)
    
    prompt = f"""
    I'm experiencing the following symptoms: {symptoms_text}. 
    Can you provide me with some friendly advice and reassurance?
    Keep your response conversational and supportive, like a caring nurse or doctor would.
    Do not try to diagnose me specifically, but provide general information and wellness tips.
    """
    
    try:
        # Get available models to use the correct one
        models = genai.list_models()
        available_models = [model.name for model in models]
        
        # Try to find the best available model (prefer gemini-1.5-pro or gemini-1.0-pro)
        model_name = None
        for candidate in ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
            for available in available_models:
                if candidate in available:
                    model_name = available
                    break
            if model_name:
                break
        
        # If no matching model found, use the first available text model
        if not model_name:
            for model in models:
                if hasattr(model, 'supported_generation_methods') and 'generateContent' in model.supported_generation_methods:
                    model_name = model.name
                    break
        
        if not model_name:
            raise Exception("No suitable generative models found in your Google API account")
            
        # Setup the model
        model = genai.GenerativeModel(model_name)
        
        # Prepare the conversation history
        conversation = previous_conversation.copy()
        conversation.append({"role": "user", "parts": [prompt]})
        
        # Call the Gemini API
        response = model.generate_content(
            contents=conversation,
            generation_config={"temperature": 0.7}  # Higher temperature for more creative responses
        )
        
        return response.text
    
    except Exception as e:
        return f"I'm sorry, I couldn't process your request at the moment. Please try again later. Error: {str(e)}"