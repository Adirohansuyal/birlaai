"""
Database utilities for the Symptom Checker application.
This module handles database connections and operations.
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a base class for our models
Base = declarative_base()

# Define our models
class SymptomCheck(Base):
    """
    Model to store symptom check information.
    """
    __tablename__ = 'symptom_checks'
    
    id = Column(Integer, primary_key=True)
    user_age = Column(Integer)
    user_gender = Column(String(10))
    symptoms = Column(Text)  # JSON formatted string of symptoms
    duration = Column(String(50))
    severity = Column(String(20))
    additional_info = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    using_ai = Column(Boolean, default=False)
    
    # Relationship to results
    results = relationship("SymptomResult", back_populates="symptom_check", cascade="all, delete-orphan")
    
    # Relationship to conversations
    conversations = relationship("Conversation", back_populates="symptom_check", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "user_age": self.user_age,
            "user_gender": self.user_gender,
            "symptoms": json.loads(self.symptoms),
            "duration": self.duration,
            "severity": self.severity,
            "additional_info": self.additional_info,
            "timestamp": self.timestamp.isoformat(),
            "using_ai": self.using_ai
        }

class SymptomResult(Base):
    """
    Model to store symptom check results.
    """
    __tablename__ = 'symptom_results'
    
    id = Column(Integer, primary_key=True)
    symptom_check_id = Column(Integer, ForeignKey('symptom_checks.id'))
    analysis_result = Column(Text)  # JSON formatted string of the analysis result
    risk_level = Column(String(20))
    seek_medical_attention = Column(Boolean, default=False)
    
    # Relationship to symptom check
    symptom_check = relationship("SymptomCheck", back_populates="results")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "symptom_check_id": self.symptom_check_id,
            "analysis_result": json.loads(self.analysis_result),
            "risk_level": self.risk_level,
            "seek_medical_attention": self.seek_medical_attention
        }

class Conversation(Base):
    """
    Model to store conversation histories with the AI assistant.
    """
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    symptom_check_id = Column(Integer, ForeignKey('symptom_checks.id'))
    user_message = Column(Text)
    ai_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to symptom check
    symptom_check = relationship("SymptomCheck", back_populates="conversations")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "symptom_check_id": self.symptom_check_id,
            "user_message": self.user_message,
            "ai_response": self.ai_response,
            "timestamp": self.timestamp.isoformat()
        }

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

def get_session():
    """Get a database session"""
    return SessionFactory()

def store_symptom_check(age, gender, symptoms, duration, severity, additional_info="", using_ai=False):
    """
    Store a symptom check in the database
    
    Args:
        age (int): User's age
        gender (str): User's gender
        symptoms (list): List of symptoms
        duration (str): Duration of symptoms
        severity (str): Severity of symptoms
        additional_info (str): Additional information
        using_ai (bool): Whether AI was used for analysis
        
    Returns:
        int: ID of the created symptom check
    """
    session = get_session()
    try:
        # Create new symptom check
        symptom_check = SymptomCheck(
            user_age=age,
            user_gender=gender,
            symptoms=json.dumps(symptoms),
            duration=duration,
            severity=severity,
            additional_info=additional_info,
            using_ai=using_ai
        )
        
        # Add to session and commit
        session.add(symptom_check)
        session.commit()
        
        return symptom_check.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def store_symptom_result(symptom_check_id, analysis_result, risk_level, seek_medical_attention):
    """
    Store a symptom analysis result in the database
    
    Args:
        symptom_check_id (int): ID of the related symptom check
        analysis_result (dict): Analysis result
        risk_level (str): Risk level assessment
        seek_medical_attention (bool): Whether medical attention is recommended
        
    Returns:
        int: ID of the created result
    """
    session = get_session()
    try:
        # Create new symptom result
        result = SymptomResult(
            symptom_check_id=symptom_check_id,
            analysis_result=json.dumps(analysis_result),
            risk_level=risk_level,
            seek_medical_attention=seek_medical_attention
        )
        
        # Add to session and commit
        session.add(result)
        session.commit()
        
        return result.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def store_conversation(symptom_check_id, user_message, ai_response):
    """
    Store a conversation with the AI assistant
    
    Args:
        symptom_check_id (int): ID of the related symptom check
        user_message (str): User's message
        ai_response (str): AI's response
        
    Returns:
        int: ID of the created conversation
    """
    session = get_session()
    try:
        # Create new conversation
        conversation = Conversation(
            symptom_check_id=symptom_check_id,
            user_message=user_message,
            ai_response=ai_response
        )
        
        # Add to session and commit
        session.add(conversation)
        session.commit()
        
        return conversation.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_recent_symptom_checks(limit=10):
    """
    Get recent symptom checks
    
    Args:
        limit (int): Maximum number of records to return
        
    Returns:
        list: List of symptom checks
    """
    session = get_session()
    try:
        # Query recent symptom checks
        symptom_checks = session.query(SymptomCheck).order_by(
            SymptomCheck.timestamp.desc()
        ).limit(limit).all()
        
        # Convert to dictionaries
        return [check.to_dict() for check in symptom_checks]
    finally:
        session.close()

def get_symptom_check_with_result(symptom_check_id):
    """
    Get a symptom check with its result
    
    Args:
        symptom_check_id (int): ID of the symptom check
        
    Returns:
        dict: Symptom check with results
    """
    session = get_session()
    try:
        # Query symptom check
        symptom_check = session.query(SymptomCheck).filter(
            SymptomCheck.id == symptom_check_id
        ).first()
        
        if not symptom_check:
            return None
        
        # Get the result
        result = session.query(SymptomResult).filter(
            SymptomResult.symptom_check_id == symptom_check_id
        ).first()
        
        check_dict = symptom_check.to_dict()
        
        if result:
            check_dict["result"] = result.to_dict()
        else:
            check_dict["result"] = None
            
        return check_dict
    finally:
        session.close()

def get_conversations_for_symptom_check(symptom_check_id):
    """
    Get conversations for a symptom check
    
    Args:
        symptom_check_id (int): ID of the symptom check
        
    Returns:
        list: List of conversations
    """
    session = get_session()
    try:
        # Query conversations
        conversations = session.query(Conversation).filter(
            Conversation.symptom_check_id == symptom_check_id
        ).order_by(Conversation.timestamp).all()
        
        # Convert to dictionaries
        return [conv.to_dict() for conv in conversations]
    finally:
        session.close()