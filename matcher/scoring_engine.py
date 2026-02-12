from typing import Set, List


class ScoringEngine:
    def __init__(self,
                 required_skills: Set[str],
                 preferred_skills: Set[str],
                 experience_keywords: List[str],
                 domain_keywords: List[str]):

        self.required_skills = required_skills
        self.preferred_skills = preferred_skills
        self.experience_keywords = experience_keywords
        self.domain_keywords = domain_keywords

    def calculate_score(self, resume_skills: Set[str], resume_text: str) -> float:
        resume_text_lower = resume_text.lower()

        # 1️⃣ Required Skills Score (50%)
        required_matches = len(resume_skills & self.required_skills)
        required_score = (required_matches / max(len(self.required_skills), 1)) * 50

        # 2️⃣ Preferred Skills Score (25%)
        preferred_matches = len(resume_skills & self.preferred_skills)
        preferred_score = (preferred_matches / max(len(self.preferred_skills), 1)) * 25

        # 3️⃣ Experience Score (15%)
        experience_matches = sum(
            1 for word in self.experience_keywords
            if word.lower() in resume_text_lower
        )
        experience_score = (experience_matches / max(len(self.experience_keywords), 1)) * 15

        # 4️⃣ Domain Keywords Score (10%)
        keyword_matches = sum(
            1 for word in self.domain_keywords
            if word.lower() in resume_text_lower
        )
        keyword_score = (keyword_matches / max(len(self.domain_keywords), 1)) * 10

        total_score = required_score + preferred_score + experience_score + keyword_score

        return round(total_score, 2)
