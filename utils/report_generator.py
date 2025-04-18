"""
Report generator for the Symptom Checker application.
This module creates printable and shareable reports from symptom analysis results.
"""

import json
import os
import datetime
import tempfile
from jinja2 import Template
from weasyprint import HTML

def format_date(date_obj=None):
    """Format date for reports"""
    if date_obj is None:
        date_obj = datetime.datetime.now()
    return date_obj.strftime("%B %d, %Y at %I:%M %p")

def generate_html_report(analysis, symptoms, user_data):
    """
    Generate an HTML report from the symptom analysis results.
    
    Args:
        analysis (dict): The symptom analysis results
        symptoms (list): List of reported symptoms
        user_data (dict): User information (age, gender, etc.)
        
    Returns:
        str: HTML report content
    """
    # HTML report template
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Symptom Analysis Report for {{ user_data.patient_name }}</title>
        <style>
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #ddd;
            }
            .header h1 {
                color: #1E88E5;
                margin-bottom: 5px;
            }
            .header h2 {
                color: #1976D2;
                margin-top: 0;
                margin-bottom: 15px;
            }
            .report-date {
                color: #666;
                font-style: italic;
            }
            .app-name {
                font-weight: bold;
                color: #1976D2;
                display: block;
                margin-bottom: 10px;
                font-size: 1.2em;
            }
            .section {
                margin-bottom: 30px;
            }
            .section h2 {
                color: #1E88E5;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            .user-info {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .user-info table {
                width: 100%;
            }
            .user-info table td {
                padding: 8px;
            }
            .user-info table td:first-child {
                font-weight: bold;
                width: 150px;
            }
            .symptoms-list {
                columns: 2;
                margin-bottom: 20px;
            }
            .risk-level {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 15px;
                font-weight: bold;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            .risk-high {
                background-color: #ffebee;
                color: #c62828;
                border: 1px solid #ef9a9a;
            }
            .risk-moderate {
                background-color: #fff8e1;
                color: #ff8f00;
                border: 1px solid #ffe082;
            }
            .risk-low {
                background-color: #e8f5e9;
                color: #2e7d32;
                border: 1px solid #a5d6a7;
            }
            .risk-unknown {
                background-color: #E0E0E0;
                color: #757575;
                border: 1px solid #BDBDBD;
            }
            .condition-card {
                border: 1px solid #eee;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 5px;
            }
            .condition-card h3 {
                margin-top: 0;
                color: #1E88E5;
            }
            .medical-advice {
                background-color: #E3F2FD;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .disclaimer {
                background-color: #FFF8E1;
                padding: 15px;
                border-radius: 5px;
                margin-top: 30px;
                font-size: 0.9em;
            }
            .sources {
                font-size: 0.9em;
                color: #666;
            }
            .print-button {
                background-color: #1E88E5;
                color: white;
                border: none;
                padding: 10px 15px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 20px;
            }
            .print-button:hover {
                background-color: #1976D2;
            }
            @media print {
                .print-button {
                    display: none;
                }
                body {
                    font-size: 12pt;
                    color: #000;
                }
                .header h1 {
                    color: #000;
                }
                .section h2, .condition-card h3 {
                    color: #000;
                }
                .disclaimer {
                    border: 1px solid #ccc;
                }
            }
        </style>
    </head>
    <body>
        <button class="print-button" onclick="window.print()">Print Report</button>
        
        <div class="header">
            <span class="app-name">AI Health Advisor - Medical Report</span>
            <h1>Symptom Analysis Report</h1>
            <h2>Patient: {{ user_data.patient_name }}</h2>
            <p class="report-date">Generated on {{ report_date }}</p>
        </div>
        
        <div class="section">
            <h2>Patient Information</h2>
            <div class="user-info">
                <table>
                    <tr>
                        <td>Age:</td>
                        <td>{{ user_data.age }}</td>
                    </tr>
                    <tr>
                        <td>Gender:</td>
                        <td>{{ user_data.gender }}</td>
                    </tr>
                    <tr>
                        <td>Symptom Duration:</td>
                        <td>{{ user_data.duration }}</td>
                    </tr>
                    <tr>
                        <td>Symptom Severity:</td>
                        <td>{{ user_data.severity }}</td>
                    </tr>
                    {% if user_data.additional_info %}
                    <tr>
                        <td>Additional Info:</td>
                        <td>{{ user_data.additional_info }}</td>
                    </tr>
                    {% endif %}
                </table>
            </div>
        </div>
        
        <div class="section">
            <h2>Reported Symptoms</h2>
            <div class="symptoms-list">
                <ul>
                    {% for symptom in symptoms %}
                    <li>{{ symptom }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>Analysis Results</h2>
            
            <h3>Risk Assessment</h3>
            {% if analysis.risk_level.lower() == "high" %}
                <div class="risk-level risk-high">High Risk</div>
                {% if analysis.seek_medical_attention %}
                <p><strong>⚠️ Recommendation: Please seek medical attention as soon as possible.</strong></p>
                {% endif %}
            {% elif analysis.risk_level.lower() == "moderate" %}
                <div class="risk-level risk-moderate">Moderate Risk</div>
                {% if analysis.seek_medical_attention %}
                <p><strong>⚠️ Recommendation: Please consult with a healthcare provider.</strong></p>
                {% endif %}
            {% elif analysis.risk_level.lower() == "low" %}
                <div class="risk-level risk-low">Low Risk</div>
                <p>Based on your symptoms, immediate medical attention may not be necessary, but consult a healthcare provider if symptoms persist or worsen.</p>
            {% else %}
                <div class="risk-level risk-unknown">Unknown Risk</div>
                <p>Risk level could not be determined. Please consult a healthcare provider.</p>
            {% endif %}
            
            <h3>Possible Conditions</h3>
            {% if analysis.possible_conditions %}
                {% for condition in analysis.possible_conditions %}
                <div class="condition-card">
                    <h3>{{ condition.name }}</h3>
                    <p><strong>Description:</strong> {{ condition.description }}</p>
                    
                    <p><strong>Common Symptoms:</strong></p>
                    <ul>
                        {% for symptom in condition.common_symptoms %}
                        <li>{{ symptom }}</li>
                        {% endfor %}
                    </ul>
                    
                    {% if condition.diet_recommendations %}
                    <p><strong>Diet Recommendations:</strong></p>
                    <ul>
                        {% for recommendation in condition.diet_recommendations %}
                        <li>{{ recommendation }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <p>No specific conditions identified based on the provided symptoms.</p>
            {% endif %}
            
            <h3>General Health Advice</h3>
            <div class="medical-advice">
                {{ analysis.general_advice }}
            </div>
            
            {% if analysis.medical_sources %}
            <h3>Medical Sources</h3>
            <div class="sources">
                <ul>
                    {% for source in analysis.medical_sources %}
                    <li><a href="{{ source }}">{{ source }}</a></li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
        
        <div class="disclaimer">
            <h3>Medical Disclaimer</h3>
            <p><strong>Important:</strong> This report is generated based on the symptoms you provided and is NOT a medical diagnosis.
            The information provided should not replace professional medical advice, diagnosis, or treatment.
            Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
            <p>If you are experiencing a medical emergency, please call your local emergency number or go to the nearest emergency room immediately.</p>
        </div>
        
        <script>
            // Add automatic print dialog when the button is clicked
            document.querySelector('.print-button').addEventListener('click', function() {
                window.print();
            });
        </script>
    </body>
    </html>
    """
    
    # Create template and render with data
    template = Template(template_str)
    
    rendered_html = template.render(
        report_date=format_date(),
        user_data=user_data,
        symptoms=symptoms,
        analysis=analysis
    )
    
    return rendered_html

def save_report_to_file(html_content, filename=None):
    """
    Save a generated HTML report to a file.
    
    Args:
        html_content (str): HTML report content
        filename (str, optional): Filename for the report
        
    Returns:
        str: Path to the saved file
    """
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"symptom_report_{timestamp}.html"
    
    # Save the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filename

def generate_pdf_report(html_content, patient_name="Patient"):
    """
    Generate a PDF report from HTML content.
    
    Args:
        html_content (str): HTML content to convert to PDF
        patient_name (str): Name of the patient for the filename
        
    Returns:
        tuple: (pdf_bytes, filename) - The PDF as bytes and suggested filename
    """
    # Create sanitized patient name for filename
    safe_name = patient_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    if safe_name == "Not_specified":
        safe_name = "Patient"
    
    # Create a date string for the filename
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"AI_Health_Advisor_{safe_name}_{date_str}.pdf"
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        temp_html.write(html_content.encode('utf-8'))
        temp_html_path = temp_html.name
    
    try:
        # Convert HTML to PDF
        html = HTML(filename=temp_html_path)
        pdf_bytes = html.write_pdf()
        return pdf_bytes, filename
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)