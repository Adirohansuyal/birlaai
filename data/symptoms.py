"""
Common symptoms for the symptom checker application.
These symptoms are organized by body system to help users identify and select their symptoms.
"""

# Organized symptoms by body system
BODY_SYSTEMS = {
    "Respiratory": [
        "Cough",
        "Shortness of breath",
        "Sore throat",
        "Runny nose",
        "Congestion",
        "Wheezing",
        "Chest tightness",
        "Rapid breathing",
        "Loss of taste or smell"
    ],
    "Cardiovascular": [
        "Chest pain",
        "Heart palpitations",
        "High blood pressure",
        "Irregular heartbeat",
        "Shortness of breath during activity",
        "Swelling in legs or ankles",
        "Dizziness when standing",
        "Cold extremities"
    ],
    "Digestive": [
        "Nausea",
        "Vomiting",
        "Diarrhea",
        "Constipation",
        "Abdominal pain",
        "Bloating",
        "Loss of appetite",
        "Difficulty swallowing",
        "Heartburn",
        "Blood in stool"
    ],
    "Nervous": [
        "Headache",
        "Dizziness",
        "Confusion",
        "Numbness",
        "Tingling sensation",
        "Tremors",
        "Memory problems",
        "Difficulty speaking",
        "Seizures",
        "Blurred vision"
    ],
    "Musculoskeletal": [
        "Muscle pain",
        "Joint pain",
        "Back pain",
        "Stiffness",
        "Swelling in joints",
        "Limited range of motion",
        "Muscle weakness",
        "Muscle cramps",
        "Bone pain"
    ],
    "Skin": [
        "Rash",
        "Itching",
        "Hives",
        "Dry skin",
        "Blisters",
        "Discoloration",
        "Abnormal growths",
        "Excessive sweating",
        "Easy bruising"
    ],
    "General": [
        "Fever",
        "Fatigue",
        "Chills",
        "Sweating",
        "Weight loss",
        "Weight gain",
        "Night sweats",
        "General weakness",
        "Malaise"
    ],
    "Mental Health": [
        "Anxiety",
        "Depression",
        "Insomnia",
        "Mood swings",
        "Irritability",
        "Excessive worry",
        "Panic attacks",
        "Changes in sleep patterns",
        "Difficulty concentrating"
    ]
}

# Create a flat list of all symptoms for backward compatibility
COMMON_SYMPTOMS = []
for system_symptoms in BODY_SYSTEMS.values():
    COMMON_SYMPTOMS.extend(system_symptoms)

# Remove duplicates and sort
COMMON_SYMPTOMS = sorted(list(set(COMMON_SYMPTOMS)))

SYMPTOM_SEVERITY = [
    "Mild",
    "Moderate",
    "Severe",
]

SYMPTOM_DURATION = [
    "Hours",
    "Days",
    "Weeks",
    "Months",
    "Years",
]
