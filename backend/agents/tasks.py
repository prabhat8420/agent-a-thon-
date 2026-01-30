"""
Tasks for each agent in the multi-agent workflow
"""
from crewai import Task
from typing import Dict, List

class CareerTasks:
    """Factory class for creating agent tasks"""
    
    @staticmethod
    def analyze_resume_task(agent, resume_text: str, industry_skills: List[str]) -> Task:
        """
        Task for Planner Agent: Analyze resume and identify gaps
        
        Args:
            agent: Planner agent instance
            resume_text: Resume content to analyze
            industry_skills: List of industry-required skills
        
        Returns:
            Task object for resume analysis
        """
        description = f"""
        Analyze the following resume and perform these steps:
        
        1. Extract all technical skills mentioned
        2. Compare against industry requirements: {', '.join(industry_skills[:10])}
        3. Identify skill gaps and missing competencies
        4. Calculate an overall resume score (0-100) based on:
           - Skill coverage
           - Relevance to industry needs
           - Experience indicators
        5. Categorize gaps by priority (Critical, Important, Nice-to-have)
        
        Resume Content:
        {resume_text}
        
        Provide a structured analysis with:
        - Detected skills list
        - Missing critical skills
        - Resume score with justification
        - Recommended focus areas for aptitude test
        """
        
        expected_output = """
        A comprehensive JSON-formatted analysis containing:
        - resume_score: integer (0-100)
        - detected_skills: list of strings
        - missing_skills: list of strings categorized by priority
        - focus_areas: list of categories for aptitude testing
        - summary: brief explanation of findings
        """
        
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
    
    @staticmethod
    def generate_aptitude_test_task(agent, skill_gaps: List[str], difficulty: str = "medium") -> Task:
        """
        Task for Executor Agent: Generate aptitude questions
        
        Args:
            agent: Executor agent instance
            skill_gaps: Areas where candidate needs testing
            difficulty: Test difficulty level
        
        Returns:
            Task object for test generation
        """
        description = f"""
        Generate a targeted aptitude test based on the following skill gaps:
        {', '.join(skill_gaps)}
        
        Requirements:
        1. Create 5 industry-level multiple-choice questions
        2. Focus on: {', '.join(skill_gaps[:3])}
        3. Difficulty level: {difficulty}
        4. Each question should have:
           - Clear problem statement
           - 4 options
           - One correct answer
           - Real-world relevance
        
        Question categories to cover:
        - System Design (if applicable)
        - Data Structures & Algorithms
        - Design Patterns
        - Cloud/DevOps concepts
        - API Design
        
        Ensure questions test practical understanding, not just theoretical knowledge.
        """
        
        expected_output = """
        A JSON array of 5 questions, each containing:
        - question_id: unique identifier
        - question_text: the problem statement
        - options: array of 4 possible answers
        - correct_answer_index: index of correct option (0-3)
        - category: skill category being tested
        - difficulty: question difficulty
        """
        
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
    
    @staticmethod
    def evaluate_answers_task(agent, questions: List[Dict], answers: List[Dict]) -> Task:
        """
        Task for Executor Agent: Evaluate test answers
        
        Args:
            agent: Executor agent instance
            questions: List of questions that were asked
            answers: List of user's answers
        
        Returns:
            Task object for answer evaluation
        """
        description = f"""
        Evaluate the candidate's aptitude test performance:
        
        Questions Asked: {len(questions)}
        Answers Submitted: {len(answers)}
        
        Tasks:
        1. Calculate overall aptitude score (0-100)
        2. Identify correctly answered categories
        3. Identify incorrectly answered categories
        4. Determine strengths based on performance
        5. Determine weak areas needing improvement
        6. Provide category-wise breakdown
        
        Evaluation Criteria:
        - Correctness of answers
        - Pattern recognition across categories
        - Consistency in strong/weak areas
        
        Questions and Answers Data:
        {questions[:2]}... (full data provided in context)
        """
        
        expected_output = """
        A detailed JSON evaluation containing:
        - aptitude_score: overall score (0-100)
        - correct_answers: count
        - incorrect_answers: count
        - strengths: list of categories performed well
        - weak_areas: list of categories need improvement
        - category_scores: breakdown by category
        - performance_summary: brief analysis
        """
        
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
    
    @staticmethod
    def create_roadmap_task(agent, resume_analysis: Dict, test_results: Dict) -> Task:
        """
        Task for Evaluator Agent: Create personalized roadmap
        
        Args:
            agent: Evaluator agent instance
            resume_analysis: Results from Planner agent
            test_results: Results from Executor agent
        
        Returns:
            Task object for roadmap creation
        """
        description = f"""
        Create a comprehensive, personalized career development roadmap.
        
        Input Data:
        1. Resume Analysis:
           - Detected Skills: {resume_analysis.get('detected_skills', [])}
           - Missing Skills: {resume_analysis.get('missing_skills', [])}
           - Resume Score: {resume_analysis.get('resume_score', 0)}
        
        2. Aptitude Test Results:
           - Score: {test_results.get('aptitude_score', 0)}
           - Strengths: {test_results.get('strengths', [])}
           - Weak Areas: {test_results.get('weak_areas', [])}
        
        Tasks:
        1. Synthesize both assessments into a holistic view
        2. Create a 4-6 step learning roadmap with:
           - Specific skills to learn
           - Estimated timeline for each step
           - Priority level (Critical/Important/Nice-to-have)
           - Concrete action items
        3. Recommend learning resources (courses, books, projects)
        4. Suggest career paths aligned with current skills
        5. Provide motivational summary
        
        Roadmap should be:
        - Actionable and specific
        - Time-bound (realistic timelines)
        - Progressive (builds from basics to advanced)
        - Industry-aligned
        """
        
        expected_output = """
        A comprehensive JSON roadmap containing:
        - roadmap_steps: array of learning phases with timelines
        - recommended_resources: books, courses, certifications
        - career_paths: suitable roles based on skills
        - priority_skills: top 5 skills to focus on immediately
        - project_ideas: 2-3 projects to build
        - evaluator_summary: motivational conclusion
        - feedback_to_planner: insights for future assessments
        """
        
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
