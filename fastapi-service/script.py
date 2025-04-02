from typing import List, Dict

# Define weightage for different criteria
WEIGHTS = {
    "skills": 0.4,  # 40% weight on skills match
    "experience": 0.3,  # 30% weight on experience relevance
    "education": 0.2,  # 20% weight on education match
    "location": 0.1,  # 10% weight on location preference
}


def calculate_skills_score(
    required_skills: List[str], candidate_skills: List[str]
) -> float:
    """Calculates skill match score (0 to 1) based on overlap."""
    matched_skills = set(required_skills) & set(candidate_skills)
    return len(matched_skills) / len(required_skills) if required_skills else 0


def calculate_experience_score(
    required_experience: int, candidate_experience: int
) -> float:
    """Scores experience match (0 to 1). Full score if candidate has equal or more experience."""
    return (
        min(candidate_experience / required_experience, 1.0)
        if required_experience
        else 1.0
    )


def calculate_education_score(required_degree: str, candidate_degree: str) -> float:
    """Simple match function for education (1 if match, 0.5 if lower degree, 0 otherwise)."""
    degree_levels = {"PhD": 3, "Master": 2, "Bachelor": 1, "None": 0}
    return (
        1.0
        if candidate_degree == required_degree
        else (
            0.5
            if degree_levels.get(candidate_degree, 0)
            >= degree_levels.get(required_degree, 0)
            else 0
        )
    )


def calculate_location_score(
    job_location: str, candidate_location: str, remote_allowed: bool = False
) -> float:
    """Improves location scoring:
    - 1.0 if same city
    - 0.8 if same country
    - 0.5 if remote job and remote is allowed
    - 0 otherwise
    """
    if job_location == candidate_location:
        return 1.0  # Exact match

    job_city, job_country = job_location.split(", ")
    candidate_city, candidate_country = candidate_location.split(", ")

    if job_country == candidate_country:
        return 0.8  # Same country, different city

    if remote_allowed:
        return 0.5  # Remote work allowed, different country

    return 0.0  # No match


def compute_job_match_score(job: Dict, candidate: Dict) -> float:
    """Computes overall job match score using weighted sum."""
    skill_score = calculate_skills_score(job["required_skills"], candidate["skills"])
    experience_score = calculate_experience_score(
        job["required_experience"], candidate["experience"]
    )
    education_score = calculate_education_score(
        job["required_degree"], candidate["degree"]
    )
    location_score = calculate_location_score(job["location"], candidate["location"])

    total_score = (
        WEIGHTS["skills"] * skill_score
        + WEIGHTS["experience"] * experience_score
        + WEIGHTS["education"] * education_score
        + WEIGHTS["location"] * location_score
    )

    return round(total_score, 2)


# Example usage
if __name__ == "__main__":
    job_posting = {
        "required_skills": ["Python", "Machine Learning", "NLP"],
        "required_experience": 3,
        "required_degree": "Master",
        "location": "New York, USA",
    }

    candidate_profile = {
        "skills": ["Python", "NLP", "Deep Learning"],
        "experience": 2,
        "degree": "Bachelor",
        "location": "New York, USA",
    }

    score = compute_job_match_score(job_posting, candidate_profile)
    print(f"Job Match Score: {score}")
