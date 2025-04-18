"""
Rule-based symptom analyzer that doesn't require external API keys.
This module provides functions to analyze symptoms and suggest possible conditions,
health advice, and diet recommendations based on predefined rules.
"""

import random

# Dictionary of common conditions with their symptoms, descriptions, and diet recommendations
CONDITIONS_DATABASE = {
    "Common Cold": {
        "description": "A viral infection of the upper respiratory tract",
        "common_symptoms": ["Cough", "Sore throat", "Runny nose", "Congestion", "Sneezing", "Fever"],
        "diet_recommendations": [
            "Stay hydrated with water, herbal teas, and broths",
            "Consume vitamin C rich foods like citrus fruits",
            "Eat honey for sore throat (not for children under 1)",
            "Consider warm soups like chicken soup"
        ],
        "risk_level": "low",
        "seek_medical_attention": False
    },
    "Influenza (Flu)": {
        "description": "A contagious respiratory illness caused by influenza viruses",
        "common_symptoms": ["Fever", "Cough", "Fatigue", "Body aches", "Headache", "Chills"],
        "diet_recommendations": [
            "Increase fluid intake to prevent dehydration",
            "Easy-to-digest foods like toast and crackers",
            "Vitamin C and zinc-rich foods to boost immunity",
            "Avoid alcohol and caffeine"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": False
    },
    "COVID-19": {
        "description": "A respiratory illness caused by the SARS-CoV-2 virus",
        "common_symptoms": ["Fever", "Cough", "Shortness of breath", "Fatigue", "Loss of taste or smell"],
        "diet_recommendations": [
            "Stay well-hydrated with water and electrolyte drinks",
            "Consume protein-rich foods for recovery",
            "Vitamin D-rich foods may support immune function",
            "Zinc and vitamin C rich foods"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": True
    },
    "Migraine": {
        "description": "A neurological condition characterized by severe headaches",
        "common_symptoms": ["Headache", "Nausea", "Sensitivity to light", "Blurred vision"],
        "diet_recommendations": [
            "Avoid trigger foods (aged cheese, alcohol, chocolate)",
            "Stay hydrated throughout the day",
            "Magnesium-rich foods like nuts and seeds",
            "Regular, balanced meals to maintain blood sugar"
        ],
        "risk_level": "low",
        "seek_medical_attention": False
    },
    "Gastroenteritis": {
        "description": "Inflammation of the stomach and intestines",
        "common_symptoms": ["Nausea", "Vomiting", "Diarrhea", "Abdominal pain", "Fever"],
        "diet_recommendations": [
            "Follow the BRAT diet (bananas, rice, applesauce, toast)",
            "Clear liquids to prevent dehydration",
            "Avoid dairy, fatty, and spicy foods",
            "Gradually reintroduce normal diet as symptoms improve"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": False
    },
    "Hypertension": {
        "description": "High blood pressure that can lead to serious health problems",
        "common_symptoms": ["Headache", "Dizziness", "Chest pain", "Shortness of breath"],
        "diet_recommendations": [
            "Reduce sodium intake (less processed foods)",
            "DASH diet (fruits, vegetables, whole grains)",
            "Limit alcohol consumption",
            "Potassium-rich foods like bananas and potatoes"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": True
    },
    "Anxiety Disorder": {
        "description": "A mental health condition characterized by persistent worry and fear",
        "common_symptoms": ["Anxiety", "Restlessness", "Rapid heartbeat", "Sweating", "Fatigue", "Insomnia"],
        "diet_recommendations": [
            "Complex carbohydrates for serotonin production",
            "Omega-3 fatty acids (fish, walnuts, flaxseed)",
            "Limit caffeine and alcohol intake",
            "Magnesium-rich foods to support nervous system"
        ],
        "risk_level": "low",
        "seek_medical_attention": False
    },
    "Asthma": {
        "description": "A chronic condition affecting the airways in the lungs",
        "common_symptoms": ["Shortness of breath", "Wheezing", "Chest tightness", "Cough"],
        "diet_recommendations": [
            "Vitamin D-rich foods (fatty fish, egg yolks)",
            "Antioxidant-rich fruits and vegetables",
            "Omega-3 fatty acids to reduce inflammation",
            "Stay hydrated and maintain healthy weight"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": True
    },
    "Allergic Rhinitis": {
        "description": "Inflammation of the nasal passages caused by allergens",
        "common_symptoms": ["Runny nose", "Sneezing", "Congestion", "Itchy eyes", "Fatigue"],
        "diet_recommendations": [
            "Anti-inflammatory foods (fatty fish, berries)",
            "Vitamin C-rich foods to support immune system",
            "Local honey may help with pollen allergies",
            "Avoid known food allergens"
        ],
        "risk_level": "low",
        "seek_medical_attention": False
    },
    "Irritable Bowel Syndrome (IBS)": {
        "description": "A chronic disorder affecting the large intestine",
        "common_symptoms": ["Abdominal pain", "Bloating", "Diarrhea", "Constipation"],
        "diet_recommendations": [
            "Low-FODMAP diet (limit certain carbohydrates)",
            "Increase soluble fiber intake gradually",
            "Avoid trigger foods (caffeine, alcohol, fatty foods)",
            "Stay hydrated and eat smaller, regular meals"
        ],
        "risk_level": "low",
        "seek_medical_attention": False
    },
    "Type 2 Diabetes": {
        "description": "A chronic condition affecting how the body processes blood sugar",
        "common_symptoms": ["Increased thirst", "Frequent urination", "Fatigue", "Blurred vision", "Weight loss"],
        "diet_recommendations": [
            "Focus on low glycemic index foods",
            "Control carbohydrate intake and portion sizes",
            "Increase fiber intake through whole grains",
            "Limit sugary and processed foods"
        ],
        "risk_level": "high",
        "seek_medical_attention": True
    },
    "Urinary Tract Infection (UTI)": {
        "description": "An infection affecting the urinary system",
        "common_symptoms": ["Burning during urination", "Frequent urination", "Cloudy urine", "Pelvic pain"],
        "diet_recommendations": [
            "Increase water intake significantly",
            "Cranberry juice or supplements",
            "Probiotic-rich foods like yogurt",
            "Vitamin C to make urine more acidic"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": True
    },
    "Anemia": {
        "description": "A condition where you lack enough healthy red blood cells",
        "common_symptoms": ["Fatigue", "Weakness", "Pale skin", "Shortness of breath", "Dizziness"],
        "diet_recommendations": [
            "Iron-rich foods (lean meats, beans, spinach)",
            "Vitamin C to enhance iron absorption",
            "Vitamin B12 sources (meat, eggs, dairy)",
            "Folate-rich foods (leafy greens, citrus)"
        ],
        "risk_level": "moderate",
        "seek_medical_attention": True
    }
}

# Medical sources for citation
MEDICAL_SOURCES = [
    "Mayo Clinic (https://www.mayoclinic.org)",
    "Centers for Disease Control and Prevention (https://www.cdc.gov)",
    "World Health Organization (https://www.who.int)",
    "National Institutes of Health (https://www.nih.gov)",
    "Cleveland Clinic (https://my.clevelandclinic.org)",
    "American Academy of Family Physicians (https://www.aafp.org)"
]

# General health advice for different symptom categories
GENERAL_ADVICE = {
    "respiratory": "Ensure adequate rest, stay hydrated, and consider using a humidifier to ease breathing. Avoid smoking and secondhand smoke.",
    "digestive": "Stay hydrated, eat small and frequent meals, and avoid foods that trigger your symptoms. Consider keeping a food diary to identify triggers.",
    "cardiovascular": "Maintain a heart-healthy diet low in sodium and saturated fats. Regular physical activity and stress management are important.",
    "neurological": "Ensure adequate rest, maintain regular sleep patterns, and practice stress-reduction techniques like meditation or deep breathing.",
    "musculoskeletal": "Apply ice to reduce inflammation and heat to relieve muscle tension. Gentle stretching and proper ergonomics can help prevent further issues.",
    "mental_health": "Practice stress management techniques, maintain social connections, and establish regular sleep and exercise routines.",
    "general": "Ensure adequate rest, stay hydrated, and maintain a balanced diet rich in fruits and vegetables. Regular moderate exercise can help boost your immune system."
}

def get_system_category(symptoms):
    """Determine which body system category the symptoms primarily affect."""
    
    system_mapping = {
        "respiratory": ["Cough", "Shortness of breath", "Sore throat", "Runny nose", "Congestion", "Wheezing"],
        "digestive": ["Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal pain", "Bloating"],
        "cardiovascular": ["Chest pain", "Rapid heartbeat", "Shortness of breath", "Dizziness", "Fatigue"],
        "neurological": ["Headache", "Dizziness", "Confusion", "Numbness", "Tingling sensation", "Blurred vision"],
        "musculoskeletal": ["Muscle pain", "Joint pain", "Back pain", "Weakness"],
        "mental_health": ["Anxiety", "Depression", "Insomnia", "Fatigue"]
    }
    
    symptom_counts = {system: 0 for system in system_mapping}
    
    for symptom in symptoms:
        for system, system_symptoms in system_mapping.items():
            if symptom in system_symptoms:
                symptom_counts[system] += 1
    
    # Find the system with the most matching symptoms
    if any(count > 0 for count in symptom_counts.values()):
        primary_system = max(symptom_counts.items(), key=lambda x: x[1])[0]
        return primary_system
    else:
        return "general"

def calculate_symptom_match(user_symptoms, condition_symptoms):
    """Calculate how well the user's symptoms match a condition's symptoms."""
    if not condition_symptoms:
        return 0
    
    matches = sum(1 for symptom in user_symptoms if symptom in condition_symptoms)
    coverage = matches / len(condition_symptoms)
    relevance = matches / len(user_symptoms) if user_symptoms else 0
    
    # Score is a weighted average of coverage and relevance
    score = (coverage * 0.7) + (relevance * 0.3)
    return score

def determine_risk_level(symptom_match, severity, age):
    """Determine risk level based on symptom match, severity, and age."""
    # Base risk from symptom match
    if symptom_match > 0.7:
        base_risk = 3  # High
    elif symptom_match > 0.4:
        base_risk = 2  # Moderate
    else:
        base_risk = 1  # Low
    
    # Severity factor
    severity_factor = {"Mild": 0, "Moderate": 1, "Severe": 2}
    
    # Age factor (higher risk for very young and elderly)
    if age < 5 or age > 65:
        age_factor = 1
    else:
        age_factor = 0
    
    total_risk = base_risk + severity_factor.get(severity, 0) + age_factor
    
    if total_risk >= 4:
        return "high"
    elif total_risk >= 2:
        return "moderate"
    else:
        return "low"

def should_seek_medical_attention(risk_level, severity, duration):
    """Determine if the user should seek medical attention."""
    if risk_level == "high":
        return True
    
    if severity == "Severe":
        return True
    
    if severity == "Moderate" and duration in ["Weeks", "Months", "Years"]:
        return True
    
    return False

def analyze_symptoms(symptoms, age, gender, duration, severity, additional_info=""):
    """
    Analyze symptoms without using external APIs and return possible conditions,
    health advice, and diet recommendations based on predefined rules.
    
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
    try:
        # Match user symptoms with conditions in our database
        condition_matches = []
        
        for condition_name, condition_data in CONDITIONS_DATABASE.items():
            match_score = calculate_symptom_match(symptoms, condition_data["common_symptoms"])
            if match_score > 0:  # Only include if there's some match
                condition_matches.append((condition_name, match_score, condition_data))
        
        # Sort conditions by match score (descending)
        condition_matches.sort(key=lambda x: x[1], reverse=True)
        
        # Take top matches (at most 5)
        top_matches = condition_matches[:5]
        
        # Determine overall risk level based on best match
        if top_matches:
            best_match_score = top_matches[0][1]
            risk_level = determine_risk_level(best_match_score, severity, age)
        else:
            risk_level = "low"  # Default if no matches
        
        # Determine if medical attention is needed
        seek_medical_attention = should_seek_medical_attention(risk_level, severity, duration)
        
        # Get general advice based on symptom category
        primary_system = get_system_category(symptoms)
        general_advice = GENERAL_ADVICE.get(primary_system, GENERAL_ADVICE["general"])
        
        # Prepare the result in the same format as the OpenAI version
        possible_conditions = []
        for condition_name, _, condition_data in top_matches:
            possible_conditions.append({
                "name": condition_name,
                "description": condition_data["description"],
                "common_symptoms": condition_data["common_symptoms"],
                "diet_recommendations": condition_data["diet_recommendations"]
            })
        
        # Randomly select 2-3 medical sources
        selected_sources = random.sample(MEDICAL_SOURCES, min(3, len(MEDICAL_SOURCES)))
        
        # Add a disclaimer to the general advice
        general_advice += "\n\nDISCLAIMER: This analysis is not a medical diagnosis. It's based on a rule-based system using common symptom patterns."
        
        return {
            "possible_conditions": possible_conditions,
            "risk_level": risk_level,
            "seek_medical_attention": seek_medical_attention,
            "general_advice": general_advice,
            "medical_sources": selected_sources
        }
            
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