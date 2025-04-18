import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Get API key from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_symptoms(symptoms, age, gender, duration, severity, additional_info=""):
    """
    Analyze symptoms using OpenAI's API and return possible conditions,
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
    {
        "possible_conditions": [
            {
                "name": "Condition name",
                "description": "Brief description",
                "common_symptoms": ["symptom1", "symptom2"],
                "diet_recommendations": ["recommendation1", "recommendation2"]
            }
        ],
        "risk_level": "low/moderate/high",
        "seek_medical_attention": true/false,
        "general_advice": "General health advice text",
        "medical_sources": ["Source 1", "Source 2"]
    }
    
    Include a clear disclaimer that this is not a medical diagnosis.
    """
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful medical advisor assistant that provides information about symptoms and possible conditions. Always remind users that your analysis is not a substitute for professional medical advice."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2  # Lower temperature for more consistent results
        )
        
        # Parse and return the JSON response
        result = json.loads(response.choices[0].message.content)
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
