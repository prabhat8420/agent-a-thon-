"""
FastAPI Backend for Agentic AI Career Bridge
Multi-agent system for career assessment and roadmap generation
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import (
    ResumeUploadRequest,
    ResumeAnalysisResponse,
    AptitudeTestResponse,
    AptitudeQuestion,
    SubmitAnswersRequest,
    FinalReportResponse,
    HealthResponse
)
from services.assessment_service import (
    ResumeAnalyzer,
    QuestionGenerator,
    AnswerEvaluator,
    RoadmapGenerator
)
from utils.data_loader import data_loader
from agents.crew import CareerAssessmentCrew
import uuid
from typing import Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic AI Career Bridge API",
    description="Multi-agent system for bridging academic-industry gap",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_analyzer = ResumeAnalyzer()
question_generator = QuestionGenerator()
answer_evaluator = AnswerEvaluator()
roadmap_generator = RoadmapGenerator()

# Initialize agent crew
crew = CareerAssessmentCrew()

# In-memory storage for demo (use database in production)
test_sessions: Dict[str, Dict] = {}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic AI Career Bridge API",
        "version": "1.0.0",
        "agents": ["Planner", "Executor", "Evaluator"],
        "endpoints": ["/upload_resume", "/start_aptitude", "/submit_answers"]
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check if data is loaded
        skills = data_loader.load_skills()
        questions = data_loader.load_aptitude_questions()
        
        return HealthResponse(
            status="healthy",
            agents_loaded=True,
            data_loaded=len(skills) > 0 and len(questions) > 0
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            agents_loaded=False,
            data_loaded=False
        )


@app.post("/upload_resume", response_model=ResumeAnalysisResponse, tags=["Assessment"])
async def upload_resume(request: ResumeUploadRequest):
    """
    Phase 1: Planner Agent analyzes resume
    
    Endpoint for resume upload and skill gap analysis
    
    Args:
        request: ResumeUploadRequest with resume text
    
    Returns:
        ResumeAnalysisResponse with detected skills, gaps, and score
    """
    try:
        logger.info("Starting resume analysis with Planner Agent")
        
        # Extract skills from resume
        detected_skills = resume_analyzer.extract_skills(request.resume_text)
        
        if not detected_skills:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No recognizable skills found in resume. Please ensure your resume contains technical skills."
            )
        
        # Calculate resume score
        resume_score = resume_analyzer.calculate_resume_score(detected_skills)
        
        # Identify missing skills
        missing_skills_dict = resume_analyzer.identify_missing_skills(detected_skills)
        
        # Flatten missing skills for response
        all_missing = (
            missing_skills_dict.get("critical", []) +
            missing_skills_dict.get("important", [])
        )
        
        # Determine focus areas for aptitude test
        focus_areas = []
        if missing_skills_dict.get("critical"):
            focus_areas.extend(missing_skills_dict["critical"][:3])
        if missing_skills_dict.get("important"):
            focus_areas.extend(missing_skills_dict["important"][:2])
        
        logger.info(f"Resume analysis complete. Score: {resume_score}")
        
        return ResumeAnalysisResponse(
            resume_score=resume_score,
            detected_skills=detected_skills[:10],  # Limit for response size
            missing_skills=all_missing[:8],
            skill_gaps=missing_skills_dict,
            recommended_focus_areas=focus_areas,
            agent_status="Planner Agent: Analysis Complete ✓"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume analysis failed: {str(e)}"
        )


@app.post("/start_aptitude", response_model=AptitudeTestResponse, tags=["Assessment"])
async def start_aptitude(focus_areas: list[str] = None):
    """
    Phase 2: Executor Agent generates aptitude test
    
    Generate aptitude test based on identified skill gaps
    
    Args:
        focus_areas: Optional list of skill areas to focus on
    
    Returns:
        AptitudeTestResponse with questions and test ID
    """
    try:
        logger.info("Generating aptitude test with Executor Agent")
        
        # Generate test ID
        test_id = str(uuid.uuid4())
        
        # Generate questions
        if not focus_areas:
            focus_areas = ["System Design", "Data Structures", "API Design"]
        
        questions = question_generator.generate_test(
            focus_areas=focus_areas,
            num_questions=5
        )
        
        # Store test session
        test_sessions[test_id] = {
            "questions": questions,
            "focus_areas": focus_areas,
            "timestamp": "2024-01-30"
        }
        
        # Convert to response format
        question_responses = [
            AptitudeQuestion(
                id=q['id'],
                question=q['question'],
                options=q['options'],
                category=q.get('category', 'general'),
                difficulty=q.get('difficulty', 'medium')
            )
            for q in questions
        ]
        
        logger.info(f"Aptitude test generated. Test ID: {test_id}")
        
        return AptitudeTestResponse(
            questions=question_responses,
            test_id=test_id,
            total_questions=len(question_responses),
            agent_status="Executor Agent: Test Generated ✓"
        )
        
    except Exception as e:
        logger.error(f"Aptitude test generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test generation failed: {str(e)}"
        )


@app.post("/submit_answers", response_model=FinalReportResponse, tags=["Assessment"])
async def submit_answers(request: SubmitAnswersRequest):
    """
    Phase 3: Executor evaluates answers, Evaluator creates roadmap
    
    Complete workflow: Executor → Evaluator → Feedback Loop
    
    Args:
        request: SubmitAnswersRequest with test_id and answers
    
    Returns:
        FinalReportResponse with complete assessment and roadmap
    """
    try:
        logger.info(f"Processing submitted answers for test: {request.test_id}")
        
        # Retrieve test session
        if request.test_id not in test_sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test session not found. Please start a new test."
            )
        
        test_session = test_sessions[request.test_id]
        questions = test_session["questions"]
        
        # Validate answer count
        if len(request.answers) != len(questions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected {len(questions)} answers, got {len(request.answers)}"
            )
        
        # Convert answers to evaluation format
        answers_list = [
            {
                "question_id": answer.question_id,
                "selected_option": answer.selected_option
            }
            for answer in request.answers
        ]
        
        # Phase 1: Executor Agent evaluates answers
        logger.info("Executor Agent: Evaluating answers")
        aptitude_score, strengths, weak_areas, category_breakdown = \
            answer_evaluator.evaluate_answers(questions, answers_list)
        
        # Get resume analysis if provided
        resume_analysis = request.resume_analysis or {
            "detected_skills": [],
            "missing_skills": {"critical": [], "important": [], "nice_to_have": []},
            "resume_score": 70
        }
        
        detected_skills = resume_analysis.get("detected_skills", [])
        missing_skills = resume_analysis.get("missing_skills", {})
        
        # Phase 2: Evaluator Agent creates roadmap
        logger.info("Evaluator Agent: Creating personalized roadmap")
        roadmap = roadmap_generator.generate_roadmap(
            detected_skills=detected_skills,
            missing_skills=missing_skills,
            aptitude_score=aptitude_score,
            weak_areas=weak_areas
        )
        
        # Get recommended resources
        focus_areas = test_session.get("focus_areas", []) + weak_areas
        resources = roadmap_generator.get_recommended_resources(focus_areas)
        
        # Generate career recommendations
        career_recommendations = []
        if aptitude_score >= 80:
            career_recommendations = [
                "You're ready for mid-level engineering roles",
                "Consider applying to product companies",
                "Focus on system design for senior roles"
            ]
        elif aptitude_score >= 60:
            career_recommendations = [
                "Target entry-level positions at startups or mid-size companies",
                "Build 2-3 strong projects before applying",
                "Practice coding interviews intensively"
            ]
        else:
            career_recommendations = [
                "Focus on strengthening fundamentals first",
                "Complete structured learning programs",
                "Build confidence through practice projects"
            ]
        
        # Generate evaluator summary
        evaluator_summary = f"""
        Based on your resume analysis and aptitude test performance (Score: {aptitude_score}/100), 
        you demonstrate {'strong' if aptitude_score >= 75 else 'good' if aptitude_score >= 60 else 'developing'} 
        technical capabilities. Your roadmap focuses on bridging the gap between academic learning and 
        industry expectations through structured skill development, hands-on projects, and continuous practice.
        
        Key Focus: {', '.join(weak_areas[:2]) if weak_areas else 'Continue building on your strengths'}
        
        With dedication to this roadmap, you can become industry-ready in 3-6 months.
        """
        
        # Agent workflow status
        workflow_status = {
            "planner": "Complete ✓",
            "executor": "Complete ✓",
            "evaluator": "Complete ✓",
            "feedback_loop": "Active ✓"
        }
        
        logger.info("Assessment complete. Generating final report.")
        
        # Clean up test session
        del test_sessions[request.test_id]
        
        return FinalReportResponse(
            aptitude_score=aptitude_score,
            strengths=strengths[:5],
            weak_areas=weak_areas[:5],
            personalized_roadmap=roadmap,
            recommended_resources=resources,
            career_recommendations=career_recommendations,
            evaluator_summary=evaluator_summary.strip(),
            agent_workflow_status=workflow_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Answer submission failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {str(e)}"
        )


@app.get("/agent_status", tags=["Agents"])
async def get_agent_status():
    """Get current status of all agents"""
    return {
        "agents": {
            "planner": {
                "name": "Career Planning Specialist",
                "status": "ready",
                "role": "Resume analysis and skill gap identification"
            },
            "executor": {
                "name": "Technical Assessment Executor",
                "status": "ready",
                "role": "Test generation and answer evaluation"
            },
            "evaluator": {
                "name": "Career Development Evaluator",
                "status": "ready",
                "role": "Roadmap creation and feedback synthesis"
            }
        },
        "workflow": "Planner → Executor → Evaluator → Feedback Loop",
        "active_sessions": len(test_sessions)
    }


@app.delete("/clear_sessions", tags=["Admin"])
async def clear_sessions():
    """Clear all test sessions (admin endpoint)"""
    count = len(test_sessions)
    test_sessions.clear()
    return {
        "message": f"Cleared {count} test sessions",
        "status": "success"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
