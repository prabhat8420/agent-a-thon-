"""
Business logic layer for career assessment
Handles skill extraction, question generation, and scoring
"""
import re
from typing import List, Dict, Tuple
import random
from utils.data_loader import data_loader

class ResumeAnalyzer:
    """Analyzes resume and extracts skills"""
    
    def __init__(self):
        self.skills_df = data_loader.load_skills()
        self.all_skills = set(self.skills_df['skill'].str.lower().tolist())
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text
        
        Args:
            resume_text: Raw resume content
        
        Returns:
            List of detected skills
        """
        resume_lower = resume_text.lower()
        detected = []
        
        for skill in self.all_skills:
            # Check for whole word matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, resume_lower, re.IGNORECASE):
                # Get original casing from dataframe
                original = self.skills_df[
                    self.skills_df['skill'].str.lower() == skill
                ]['skill'].iloc[0]
                detected.append(original)
        
        return detected
    
    def calculate_resume_score(self, detected_skills: List[str]) -> int:
        """
        Calculate resume score based on skills
        
        Args:
            detected_skills: List of skills found in resume
        
        Returns:
            Score from 0-100
        """
        if not detected_skills:
            return 30
        
        # Get high-demand skills
        high_demand = data_loader.get_high_demand_skills()
        high_demand_lower = [s.lower() for s in high_demand]
        detected_lower = [s.lower() for s in detected_skills]
        
        # Calculate coverage
        high_demand_count = sum(1 for skill in detected_lower if skill in high_demand_lower)
        coverage_ratio = high_demand_count / len(high_demand) if high_demand else 0
        
        # Base score from coverage
        base_score = int(coverage_ratio * 60)
        
        # Bonus for total skills
        skill_bonus = min(len(detected_skills) * 2, 30)
        
        # Final score
        total_score = min(base_score + skill_bonus, 95)
        
        # Add some randomness for realism (±5)
        total_score += random.randint(-5, 5)
        
        return max(30, min(total_score, 95))
    
    def identify_missing_skills(self, detected_skills: List[str]) -> Dict[str, List[str]]:
        """
        Identify critical missing skills
        
        Args:
            detected_skills: Skills found in resume
        
        Returns:
            Dictionary categorizing missing skills
        """
        detected_lower = [s.lower() for s in detected_skills]
        high_demand = data_loader.get_high_demand_skills()
        
        missing = {
            "critical": [],
            "important": [],
            "nice_to_have": []
        }
        
        for skill in high_demand:
            if skill.lower() not in detected_lower:
                # Categorize by importance
                skill_data = self.skills_df[
                    self.skills_df['skill'].str.lower() == skill.lower()
                ]
                if not skill_data.empty:
                    importance = skill_data.iloc[0]['importance']
                    if importance == 'Very High':
                        missing["critical"].append(skill)
                    elif importance == 'High':
                        missing["important"].append(skill)
                    else:
                        missing["nice_to_have"].append(skill)
        
        # Limit each category
        missing["critical"] = missing["critical"][:5]
        missing["important"] = missing["important"][:5]
        missing["nice_to_have"] = missing["nice_to_have"][:3]
        
        return missing


class QuestionGenerator:
    """Generates aptitude test questions based on skill gaps"""
    
    def __init__(self):
        self.questions_data = data_loader.load_aptitude_questions()
    
    def generate_test(self, focus_areas: List[str], num_questions: int = 5) -> List[Dict]:
        """
        Generate aptitude test based on focus areas
        
        Args:
            focus_areas: Skill categories to focus on
            num_questions: Number of questions to generate
        
        Returns:
            List of question dictionaries
        """
        selected_questions = []
        
        # Map focus areas to question categories
        category_map = {
            "system design": "system_design",
            "data structures": "data_structures",
            "algorithms": "data_structures",
            "design patterns": "design_patterns",
            "cloud": "cloud",
            "api": "api_design",
            "microservices": "system_design"
        }
        
        # Get relevant categories
        relevant_categories = []
        for area in focus_areas:
            area_lower = area.lower()
            for key, category in category_map.items():
                if key in area_lower and category in self.questions_data:
                    relevant_categories.append(category)
        
        # If no matches, use all categories
        if not relevant_categories:
            relevant_categories = list(self.questions_data.keys())
        
        # Remove duplicates
        relevant_categories = list(set(relevant_categories))
        
        # Distribute questions across categories
        questions_per_category = max(1, num_questions // len(relevant_categories))
        
        for category in relevant_categories:
            if category in self.questions_data:
                category_questions = self.questions_data[category]
                count = min(questions_per_category, len(category_questions))
                selected = random.sample(category_questions, count)
                selected_questions.extend(selected)
        
        # Ensure we have exactly num_questions
        if len(selected_questions) < num_questions:
            # Add more random questions
            all_questions = [q for qs in self.questions_data.values() for q in qs]
            remaining = num_questions - len(selected_questions)
            additional = random.sample(
                [q for q in all_questions if q not in selected_questions],
                min(remaining, len(all_questions) - len(selected_questions))
            )
            selected_questions.extend(additional)
        elif len(selected_questions) > num_questions:
            selected_questions = selected_questions[:num_questions]
        
        return selected_questions


class AnswerEvaluator:
    """Evaluates aptitude test answers"""
    
    @staticmethod
    def evaluate_answers(
        questions: List[Dict],
        answers: List[Dict]
    ) -> Tuple[int, List[str], List[str], Dict]:
        """
        Evaluate test answers and calculate score
        
        Args:
            questions: List of questions
            answers: List of user answers
        
        Returns:
            Tuple of (score, strengths, weak_areas, category_breakdown)
        """
        # Create question lookup
        question_lookup = {q['id']: q for q in questions}
        
        # Evaluate each answer
        correct_count = 0
        category_performance = {}
        
        for answer in answers:
            q_id = answer['question_id']
            if q_id in question_lookup:
                question = question_lookup[q_id]
                is_correct = answer['selected_option'] == question['correct']
                
                # Track by category
                category = question.get('category', 'general')
                if category not in category_performance:
                    category_performance[category] = {'correct': 0, 'total': 0}
                
                category_performance[category]['total'] += 1
                if is_correct:
                    correct_count += 1
                    category_performance[category]['correct'] += 1
        
        # Calculate overall score
        total_questions = len(answers)
        score = int((correct_count / total_questions * 100)) if total_questions > 0 else 0
        
        # Determine strengths and weak areas
        strengths = []
        weak_areas = []
        
        for category, perf in category_performance.items():
            accuracy = perf['correct'] / perf['total'] if perf['total'] > 0 else 0
            category_name = category.replace('_', ' ').title()
            
            if accuracy >= 0.7:
                strengths.append(category_name)
            elif accuracy < 0.5:
                weak_areas.append(category_name)
        
        # Add generic strengths/weaknesses if needed
        if score >= 80:
            strengths.insert(0, "Strong problem-solving skills")
            strengths.append("Excellent grasp of fundamentals")
        elif score >= 60:
            strengths.insert(0, "Good analytical thinking")
        else:
            weak_areas.insert(0, "Needs more practice with fundamentals")
        
        if score < 70:
            weak_areas.append("Could improve technical depth")
        
        return score, strengths, weak_areas, category_performance


class RoadmapGenerator:
    """Generates personalized career roadmap"""
    
    @staticmethod
    def generate_roadmap(
        detected_skills: List[str],
        missing_skills: Dict[str, List[str]],
        aptitude_score: int,
        weak_areas: List[str]
    ) -> List[Dict[str, str]]:
        """
        Generate personalized learning roadmap
        
        Args:
            detected_skills: Skills already present
            missing_skills: Categorized missing skills
            aptitude_score: Score from aptitude test
            weak_areas: Areas needing improvement
        
        Returns:
            List of roadmap steps
        """
        roadmap = []
        
        # Step 1: Address critical gaps
        if missing_skills.get("critical"):
            critical = missing_skills["critical"][:3]
            roadmap.append({
                "step": "1",
                "title": f"Master Critical Skills: {', '.join(critical[:2])}",
                "description": f"Focus on {', '.join(critical)}. These are essential for industry readiness.",
                "duration": "4-6 weeks",
                "priority": "Critical"
            })
        
        # Step 2: Improve weak areas from test
        if weak_areas:
            roadmap.append({
                "step": str(len(roadmap) + 1),
                "title": f"Strengthen {weak_areas[0]}",
                "description": f"Deep dive into {weak_areas[0]} through structured learning and practice problems.",
                "duration": "3-4 weeks",
                "priority": "High"
            })
        
        # Step 3: Build projects
        roadmap.append({
            "step": str(len(roadmap) + 1),
            "title": "Build Real-World Projects",
            "description": "Create 2-3 production-grade projects showcasing full-stack capabilities, system design, and best practices.",
            "duration": "8-10 weeks",
            "priority": "Critical"
        })
        
        # Step 4: Cloud/DevOps if missing
        if any('cloud' in skill.lower() or 'docker' in skill.lower() or 'aws' in skill.lower() 
               for skill in missing_skills.get("important", [])):
            roadmap.append({
                "step": str(len(roadmap) + 1),
                "title": "Learn Cloud & DevOps",
                "description": "Get hands-on with AWS/Azure, Docker, Kubernetes, and CI/CD pipelines.",
                "duration": "6-8 weeks",
                "priority": "High"
            })
        
        # Step 5: Soft skills
        roadmap.append({
            "step": str(len(roadmap) + 1),
            "title": "Develop Communication Skills",
            "description": "Practice technical presentations, write documentation, and participate in mock interviews.",
            "duration": "Ongoing",
            "priority": "Important"
        })
        
        # Step 6: Interview prep
        if aptitude_score < 75:
            roadmap.append({
                "step": str(len(roadmap) + 1),
                "title": "Interview Preparation",
                "description": "Solve coding problems daily, practice system design interviews, and review CS fundamentals.",
                "duration": "4-6 weeks",
                "priority": "High"
            })
        
        return roadmap
    
    @staticmethod
    def get_recommended_resources(focus_areas: List[str]) -> List[str]:
        """Get learning resources based on focus areas"""
        resources = [
            "📚 Designing Data-Intensive Applications by Martin Kleppmann",
            "🎓 System Design Interview Course (educative.io)",
            "💻 LeetCode Premium for coding practice",
        ]
        
        focus_lower = [area.lower() for area in focus_areas]
        
        if any('cloud' in area or 'aws' in area for area in focus_lower):
            resources.append("☁️ AWS Certified Solutions Architect Course")
        
        if any('system' in area or 'design' in area for area in focus_lower):
            resources.append("🏗️ Grokking the System Design Interview")
        
        if any('algorithm' in area or 'data structure' in area for area in focus_lower):
            resources.append("📖 Introduction to Algorithms (CLRS)")
        
        resources.append("🚀 Contribute to Open Source Projects on GitHub")
        
        return resources
