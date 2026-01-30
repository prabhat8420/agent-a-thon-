"""
Crew configuration for multi-agent workflow orchestration
Manages the Planner → Executor → Evaluator → Planner feedback loop
"""
from crewai import Crew, Process
from agents.agents import CareerAgents
from agents.tasks import CareerTasks
from typing import Dict, List
import json

class CareerAssessmentCrew:
    """
    Orchestrates the complete career assessment workflow
    using CrewAI's multi-agent system
    """
    
    def __init__(self):
        """Initialize agents and task factory"""
        self.agent_factory = CareerAgents()
        self.task_factory = CareerTasks()
        
        # Create agent instances
        self.planner = self.agent_factory.create_planner_agent()
        self.executor = self.agent_factory.create_executor_agent()
        self.evaluator = self.agent_factory.create_evaluator_agent()
        
        # Workflow tracking
        self.workflow_log = []
    
    def run_resume_analysis(self, resume_text: str, industry_skills: List[str]) -> Dict:
        """
        Phase 1: Planner Agent analyzes resume
        
        Args:
            resume_text: Candidate's resume content
            industry_skills: Required industry skills
        
        Returns:
            Analysis results from Planner
        """
        try:
            # Create task
            task = self.task_factory.analyze_resume_task(
                agent=self.planner,
                resume_text=resume_text,
                industry_skills=industry_skills
            )
            
            # Create crew for this phase
            crew = Crew(
                agents=[self.planner],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            self.workflow_log.append({
                "phase": "resume_analysis",
                "agent": "planner",
                "status": "started"
            })
            
            result = crew.kickoff()
            
            self.workflow_log.append({
                "phase": "resume_analysis",
                "agent": "planner",
                "status": "completed"
            })
            
            return self._parse_result(result)
            
        except Exception as e:
            self.workflow_log.append({
                "phase": "resume_analysis",
                "agent": "planner",
                "status": "error",
                "error": str(e)
            })
            raise
    
    def run_aptitude_evaluation(self, questions: List[Dict], answers: List[Dict]) -> Dict:
        """
        Phase 2: Executor Agent evaluates aptitude test
        
        Args:
            questions: Test questions
            answers: User's answers
        
        Returns:
            Evaluation results from Executor
        """
        try:
            # Create task
            task = self.task_factory.evaluate_answers_task(
                agent=self.executor,
                questions=questions,
                answers=answers
            )
            
            # Create crew for this phase
            crew = Crew(
                agents=[self.executor],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            self.workflow_log.append({
                "phase": "aptitude_evaluation",
                "agent": "executor",
                "status": "started"
            })
            
            result = crew.kickoff()
            
            self.workflow_log.append({
                "phase": "aptitude_evaluation",
                "agent": "executor",
                "status": "completed"
            })
            
            return self._parse_result(result)
            
        except Exception as e:
            self.workflow_log.append({
                "phase": "aptitude_evaluation",
                "agent": "executor",
                "status": "error",
                "error": str(e)
            })
            raise
    
    def run_final_evaluation(self, resume_analysis: Dict, test_results: Dict) -> Dict:
        """
        Phase 3: Evaluator Agent creates roadmap and provides feedback
        
        Args:
            resume_analysis: Results from Planner
            test_results: Results from Executor
        
        Returns:
            Final roadmap and recommendations from Evaluator
        """
        try:
            # Create task
            task = self.task_factory.create_roadmap_task(
                agent=self.evaluator,
                resume_analysis=resume_analysis,
                test_results=test_results
            )
            
            # Create crew for this phase
            crew = Crew(
                agents=[self.evaluator],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            self.workflow_log.append({
                "phase": "final_evaluation",
                "agent": "evaluator",
                "status": "started"
            })
            
            result = crew.kickoff()
            
            self.workflow_log.append({
                "phase": "final_evaluation",
                "agent": "evaluator",
                "status": "completed"
            })
            
            return self._parse_result(result)
            
        except Exception as e:
            self.workflow_log.append({
                "phase": "final_evaluation",
                "agent": "evaluator",
                "status": "error",
                "error": str(e)
            })
            raise
    
    def run_complete_workflow(
        self,
        resume_text: str,
        industry_skills: List[str],
        questions: List[Dict],
        answers: List[Dict]
    ) -> Dict:
        """
        Execute complete multi-agent workflow
        
        Workflow: Planner → Executor → Evaluator → Feedback Loop
        
        Args:
            resume_text: Candidate's resume
            industry_skills: Required skills
            questions: Aptitude questions
            answers: User's answers
        
        Returns:
            Complete assessment results with feedback loop
        """
        try:
            # Phase 1: Resume Analysis (Planner)
            resume_analysis = self.run_resume_analysis(resume_text, industry_skills)
            
            # Phase 2: Aptitude Evaluation (Executor)
            test_results = self.run_aptitude_evaluation(questions, answers)
            
            # Phase 3: Final Roadmap (Evaluator)
            final_roadmap = self.run_final_evaluation(resume_analysis, test_results)
            
            # Phase 4: Feedback Loop (Evaluator → Planner)
            feedback = self._create_feedback_loop(final_roadmap)
            
            # Compile complete results
            complete_results = {
                "resume_analysis": resume_analysis,
                "aptitude_evaluation": test_results,
                "final_roadmap": final_roadmap,
                "feedback_loop": feedback,
                "workflow_status": self.get_workflow_status()
            }
            
            return complete_results
            
        except Exception as e:
            raise Exception(f"Workflow execution failed: {str(e)}")
    
    def _create_feedback_loop(self, evaluator_output: Dict) -> Dict:
        """
        Create feedback from Evaluator to Planner for continuous improvement
        
        Args:
            evaluator_output: Results from Evaluator agent
        
        Returns:
            Feedback data for Planner
        """
        feedback = {
            "timestamp": "2024-01-30",
            "from_agent": "evaluator",
            "to_agent": "planner",
            "insights": evaluator_output.get("feedback_to_planner", "Assessment complete"),
            "suggested_improvements": [
                "Focus more on practical project experience in future assessments",
                "Include communication skills evaluation",
                "Consider soft skills alongside technical skills"
            ]
        }
        
        self.workflow_log.append({
            "phase": "feedback_loop",
            "from": "evaluator",
            "to": "planner",
            "status": "completed"
        })
        
        return feedback
    
    def get_workflow_status(self) -> Dict:
        """Get current status of the workflow"""
        return {
            "total_phases": len(self.workflow_log),
            "log": self.workflow_log,
            "agents_status": {
                "planner": "ready",
                "executor": "ready",
                "evaluator": "ready"
            }
        }
    
    def _parse_result(self, result) -> Dict:
        """
        Parse crew result into structured dictionary
        
        Args:
            result: Raw result from crew.kickoff()
        
        Returns:
            Parsed dictionary
        """
        try:
            # Try to parse as JSON if result is string
            if isinstance(result, str):
                return json.loads(result)
            elif hasattr(result, 'raw_output'):
                return json.loads(result.raw_output)
            else:
                return {"raw_output": str(result)}
        except json.JSONDecodeError:
            return {"raw_output": str(result)}
    
    def reset(self):
        """Reset crew for new assessment"""
        self.workflow_log = []
