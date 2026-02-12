import re
from typing import Set, Dict


class KeywordExtractor:
    def __init__(self):
        # Skills taxonomy
        self.skills_taxonomy: Dict[str, Dict[str, list]] = {
            "Programming Languages": {
                "Python": ["python"],
                "Java": ["java"],
                "C++": ["c++", "cpp"],
                "JavaScript": ["javascript", "js"],
            },
            "Web Development": {
                "HTML": ["html"],
                "CSS": ["css"],
                "React": ["react"],
                "Django": ["django"],
                "Flask": ["flask"],
            },
            "Data Science": {
                "Machine Learning": ["machine learning", "ml"],
                "Deep Learning": ["deep learning", "dl"],
                "Pandas": ["pandas"],
                "NumPy": ["numpy"],
                "TensorFlow": ["tensorflow"],
            }
        }

    def extract_skills(self, text: str) -> Set[str]:
        text_lower = text.lower()
        found_skills = set()

        for category, skills_dict in self.skills_taxonomy.items():
            for skill_name, variations in skills_dict.items():
                for variation in variations:
                    pattern = r"\b" + re.escape(variation) + r"\b"
                    if re.search(pattern, text_lower):
                        found_skills.add(skill_name)
                        break

        return found_skills
