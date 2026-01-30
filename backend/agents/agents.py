"""
Multi-Agent System for Career Assessment
Agents: Planner → Executor → Evaluator
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from typing import List, Dict

class CareerAgents:
    """Factory class for creating career assessment agents"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        """
        Initialize agents with LLM configuration
        
        Args:
            model: OpenAI model to use
            temperature: Creativity level (0-1)
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY", "sk-dummy-key-for-demo")
        )
    
    def create_planner_agent(self) -> Agent:
        """
        Create Planner Agent (Career Planner)
        
        Responsibilities:
        - Analyze resume content
        - Extract technical skills
        - Compare with industry standards
        - Identify skill gaps
        - Generate assessment blueprint
        """
        return Agent(
            role="Career Planning Specialist",
            goal="Analyze resumes and identify skill gaps between academic background and industry requirements",
            backstory="""You are an expert career planner with deep knowledge of the tech industry.
            You analyze resumes to extract skills, compare them against current industry demands,
            and identify critical gaps that need to be addressed. You provide detailed, actionable
            insights about what skills are present, what's missing, and what areas need focus.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_executor_agent(self) -> Agent:
        """
        Create Executor Agent (Assessment Agent)
        
        Responsibilities:
        - Generate aptitude questions based on gaps
        - Evaluate candidate responses
        - Calculate performance metrics
        - Identify strengths and weaknesses
        """
        return Agent(
            role="Technical Assessment Executor",
            goal="Generate targeted aptitude tests and evaluate candidate performance accurately",
            backstory="""You are a technical assessment specialist who creates and evaluates
            industry-standard aptitude tests. You generate questions based on identified skill gaps,
            evaluate answers with precision, and provide detailed performance analysis. You focus on
            practical, real-world scenarios that test both theoretical knowledge and problem-solving ability.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_evaluator_agent(self) -> Agent:
        """
        Create Evaluator Agent (Feedback Agent)
        
        Responsibilities:
        - Compare pre-assessment vs post-assessment
        - Generate comprehensive final report
        - Create personalized learning roadmap
        - Provide feedback loop to Planner
        """
        return Agent(
            role="Career Development Evaluator",
            goal="Synthesize assessment results into actionable career roadmaps and improvement plans",
            backstory="""You are a senior career development advisor who specializes in creating
            personalized learning paths for fresh graduates. You analyze both resume data and
            aptitude test results to create comprehensive career roadmaps. You provide specific,
            achievable steps with timelines, recommend resources, and offer strategic career advice
            that bridges the gap between academic learning and industry expectations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """Return all agents as a dictionary"""
        return {
            "planner": self.create_planner_agent(),
            "executor": self.create_executor_agent(),
            "evaluator": self.create_evaluator_agent()
        }


class AgentOrchestrator:
    """
    Orchestrates the multi-agent workflow
    Manages communication between Planner → Executor → Evaluator → Planner (feedback loop)
    """
    
    def __init__(self):
        self.agents = CareerAgents()
        self.planner = self.agents.create_planner_agent()
        self.executor = self.agents.create_executor_agent()
        self.evaluator = self.agents.create_evaluator_agent()
        
        # Store workflow state
        self.workflow_state = {
            "planner": "initialized",
            "executor": "initialized",
            "evaluator": "initialized"
        }
    
    def execute_planner_analysis(self, resume_text: str, industry_skills: List[str]) -> Dict:
        """
        Execute Planner Agent task
        
        Args:
            resume_text: Raw resume content
            industry_skills: List of high-demand industry skills
        
        Returns:
            Dictionary with analysis results
        """
        try:
            self.workflow_state["planner"] = "processing"
            
            # In production, this would use agent.execute() or similar
            # For demo, we'll use a simplified approach
            analysis = {
                "agent": "planner",
                "status": "complete",
                "message": "Resume analyzed successfully"
            }
            
            self.workflow_state["planner"] = "complete"
            return analysis
            
        except Exception as e:
            self.workflow_state["planner"] = f"error: {str(e)}"
            raise
    
    def execute_executor_evaluation(self, questions: List[Dict], answers: List[Dict]) -> Dict:
        """
        Execute Executor Agent task
        
        Args:
            questions: List of aptitude questions
            answers: List of user answers
        
        Returns:
            Dictionary with evaluation results
        """
        try:
            self.workflow_state["executor"] = "processing"
            
            evaluation = {
                "agent": "executor",
                "status": "complete",
                "message": "Answers evaluated successfully"
            }
            
            self.workflow_state["executor"] = "complete"
            return evaluation
            
        except Exception as e:
            self.workflow_state["executor"] = f"error: {str(e)}"
            raise
    
    def execute_evaluator_synthesis(self, resume_analysis: Dict, test_results: Dict) -> Dict:
        """
        Execute Evaluator Agent task
        
        Args:
            resume_analysis: Results from Planner
            test_results: Results from Executor
        
        Returns:
            Dictionary with final roadmap and recommendations
        """
        try:
            self.workflow_state["evaluator"] = "processing"
            
            synthesis = {
                "agent": "evaluator",
                "status": "complete",
                "message": "Final report generated successfully"
            }
            
            self.workflow_state["evaluator"] = "complete"
            return synthesis
            
        except Exception as e:
            self.workflow_state["evaluator"] = f"error: {str(e)}"
            raise
    
    def get_workflow_status(self) -> Dict[str, str]:
        """Get current status of all agents in the workflow"""
        return self.workflow_state.copy()
    
    def reset_workflow(self):
        """Reset workflow state for new assessment"""
        self.workflow_state = {
            "planner": "initialized",
            "executor": "initialized",
            "evaluator": "initialized"
        }
