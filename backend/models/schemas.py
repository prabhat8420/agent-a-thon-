"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional

class ResumeUploadRequest(BaseModel):
    """Request model for resume upload"""
    resume_text: str = Field(..., min_length=50, max_length=10000)
    
    @validator('resume_text')
    def validate_resume(cls, v):
        # Basic security: prevent prompt injection attempts
        suspicious_patterns = ['ignore previous', 'ignore above', 'system:', 'admin:', '```']
        v_lower = v.lower()
        for pattern in suspicious_patterns:
            if pattern in v_lower:
                raise ValueError("Invalid resume content detected")
        return v

class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    resume_score: int
    detected_skills: List[str]
    missing_skills: List[str]
    skill_gaps: Dict[str, List[str]]
    recommended_focus_areas: List[str]
    agent_status: str

class AptitudeQuestion(BaseModel):
    """Model for a single aptitude question"""
    id: str
    question: str
    options: List[str]
    category: str
    difficulty: str

class AptitudeTestResponse(BaseModel):
    """Response model for aptitude test"""
    questions: List[AptitudeQuestion]
    test_id: str
    total_questions: int
    agent_status: str

class Answer(BaseModel):
    """Model for a single answer"""
    question_id: str
    selected_option: int = Field(..., ge=0, le=3)

class SubmitAnswersRequest(BaseModel):
    """Request model for submitting answers"""
    test_id: str
    answers: List[Answer]
    resume_analysis: Optional[Dict] = None
    
    @validator('answers')
    def validate_answers(cls, v):
        if len(v) < 1 or len(v) > 20:
            raise ValueError("Number of answers must be between 1 and 20")
        return v

class FinalReportResponse(BaseModel):
    """Response model for final assessment report"""
    aptitude_score: int
    strengths: List[str]
    weak_areas: List[str]
    personalized_roadmap: List[Dict[str, str]]
    recommended_resources: List[str]
    career_recommendations: List[str]
    evaluator_summary: str
    agent_workflow_status: Dict[str, str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agents_loaded: bool
    data_loaded: bool
