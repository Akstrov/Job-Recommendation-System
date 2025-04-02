from typing import List
from pydantic import BaseModel

# Define weightage for different criteria
WEIGHTS = {
    "skills": 0.4,  # 40% weight on skills match
    "experience": 0.3,  # 30% weight on experience relevance
    "education": 0.2,  # 20% weight on education match
    "location": 0.1,  # 10% weight on location preference
}


class Education(BaseModel):
    degree: str
    major: str


class UserProfile(BaseModel):
    id: str
    skills: List[str]
    experience: float
    education: List[Education]
    location: str
    remote_ok: bool


class JobRequirement(BaseModel):
    id: str
    required_skills: List[str]
    min_experience: float
    required_education: Education
    locations: List[str]
    remote_available: bool


def calculate_skills_score(
    required_skills: List[str], candidate_skills: List[str]
) -> float:
    """Calculates skill match score (0 to 1) based on overlap."""
    matched_skills = set(required_skills) & set(candidate_skills)
    return len(matched_skills) / len(required_skills) if required_skills else 1


def calculate_experience_score(
    required_experience: float, candidate_experience: float
) -> float:
    """Scores experience match (0 to 1). Full score if candidate has equal or more experience."""
    return (
        min(candidate_experience / required_experience, 1.0)
        if required_experience
        else 1.0
    )


def calculate_education_score(
    required_education: Education, candidate_education: List[Education]
) -> float:
    """Simple match function for education (1 if match, 0.5 if lower but acceptable degree, 0 otherwise)."""
    degree_levels = {"PhD": 4, "Master": 3, "Bachelor": 2, "High School": 1, "None": 0}

    required_level = degree_levels.get(required_education.degree, 0)
    candidate_levels = [degree_levels.get(edu.degree, 0) for edu in candidate_education]

    if not candidate_levels:
        return 0.0

    best_match = max(candidate_levels)

    if best_match == required_level:
        return 1.0
    elif best_match > 0 and best_match >= required_level - 1:
        return 0.5
    else:
        return 0.0


def calculate_location_score(
    job_locations: List[str], candidate_location: str, remote_allowed: bool
) -> float:
    """Improves location scoring:
    - 1.0 if same city
    - 0.8 if same country
    - 0.5 if remote job and remote is allowed
    - 0 otherwise
    """
    if candidate_location in job_locations:
        return 1.0  # Exact match

    candidate_city, candidate_country = candidate_location.split(", ")
    for job_location in job_locations:
        job_city, job_country = job_location.split(", ")
        if job_country == candidate_country:
            return 0.8  # Same country, different city

    if remote_allowed:
        return 0.5  # Remote work allowed, different country

    return 0.0  # No match


def compute_job_match_score(job: JobRequirement, candidate: UserProfile) -> tuple:
    """Computes overall job match score using weighted sum."""
    skill_score = calculate_skills_score(job.required_skills, candidate.skills)
    experience_score = calculate_experience_score(
        job.min_experience, candidate.experience
    )
    education_score = calculate_education_score(
        job.required_education, candidate.education
    )
    location_score = calculate_location_score(
        job.locations, candidate.location, job.remote_available or candidate.remote_ok
    )

    total_score = (
        WEIGHTS["skills"] * skill_score
        + WEIGHTS["experience"] * experience_score
        + WEIGHTS["education"] * education_score
        + WEIGHTS["location"] * location_score
    )
    explanation = "This job was recommended because "
    reasons = []

    if skill_score > 0.7:
        reasons.append("you have strong skills matching the job requirements")
    if experience_score > 0.7:
        reasons.append("your experience aligns well with the job expectations")
    if education_score > 0.7:
        reasons.append("your education meets the required qualifications")
    if location_score > 0.7:
        reasons.append("your location is a good match for this job")
    elif location_score > 0.5:
        reasons.append("remote work is an option for this job")

    explanation += (
        ", and ".join(reasons) if reasons else "it meets general suitability criteria."
    )

    return round(total_score, 2), explanation


# Tests
if __name__ == "__main__":
    job = JobRequirement(
        id="id_job123",
        required_skills=["Python", "Machine Learning"],
        min_experience=3.0,
        required_education=Education(degree="Master", major="Computer Science"),
        locations=["New York, USA"],
        remote_available=True,
    )

    candidate = UserProfile(
        id="id_user123",
        skills=["Python", "Data Science"],
        experience=2.5,
        education=[Education(degree="Bachelor", major="Computer Science")],
        location="Los Angeles, USA",
        remote_ok=True,
    )

    print("Job Match Score:", compute_job_match_score(job, candidate))
