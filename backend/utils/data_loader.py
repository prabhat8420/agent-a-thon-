"""
Data loaders for skills, aptitude questions, and job roles
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List

class DataLoader:
    """Centralized data loader for all datasets"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._skills_df = None
        self._aptitude_data = None
        self._roles_data = None
    
    def load_skills(self) -> pd.DataFrame:
        """Load industry skills from CSV"""
        if self._skills_df is None:
            skills_path = self.data_dir / "skills.csv"
            self._skills_df = pd.read_csv(skills_path)
        return self._skills_df
    
    def load_aptitude_questions(self) -> Dict:
        """Load aptitude questions from JSON"""
        if self._aptitude_data is None:
            aptitude_path = self.data_dir / "aptitude.json"
            with open(aptitude_path, 'r') as f:
                self._aptitude_data = json.load(f)
        return self._aptitude_data
    
    def load_roles(self) -> Dict:
        """Load job roles and requirements from JSON"""
        if self._roles_data is None:
            roles_path = self.data_dir / "roles.json"
            with open(roles_path, 'r') as f:
                self._roles_data = json.load(f)
        return self._roles_data
    
    def get_high_demand_skills(self) -> List[str]:
        """Get list of high-demand skills"""
        df = self.load_skills()
        high_demand = df[df['demand_level'].isin(['High', 'Very High'])]
        return high_demand['skill'].tolist()
    
    def get_skills_by_category(self, category: str) -> List[str]:
        """Get skills filtered by category"""
        df = self.load_skills()
        filtered = df[df['category'] == category]
        return filtered['skill'].tolist()
    
    def get_questions_by_category(self, category: str, count: int = 2) -> List[Dict]:
        """Get random questions from a specific category"""
        questions = self.load_aptitude_questions()
        if category in questions:
            import random
            category_questions = questions[category]
            return random.sample(category_questions, min(count, len(category_questions)))
        return []
    
    def get_mixed_questions(self, total: int = 5) -> List[Dict]:
        """Get a mix of questions from different categories"""
        questions = self.load_aptitude_questions()
        all_questions = []
        
        for category, q_list in questions.items():
            all_questions.extend(q_list)
        
        import random
        return random.sample(all_questions, min(total, len(all_questions)))

# Global instance
data_loader = DataLoader()
