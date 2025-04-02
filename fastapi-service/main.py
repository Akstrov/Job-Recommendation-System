from fastapi import FastAPI, status
from typing import List
from pydantic import BaseModel
from script import UserProfile, JobRequirement, compute_job_match_score

app = FastAPI(
    title="Job Matching API",
    description="API for matching candidates and jobs",
    version="0.1.0",
)


# Existing endpoints remain unchanged
@app.get("/")
def read_root():
    return {"message": "Welcome to Job Matching API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/match-jobs-for-user", status_code=status.HTTP_200_OK)
async def match_user_to_jobs(user: UserProfile, jobs: List[JobRequirement]):
    """
    Returns sorted jobs for a user with explanations
    Example response:
    {
        "matches": [
            {
                "job_id": 1,
                "score": 0.85,
                "explanation": "Skills: 3/5 matched, Experience met"
            }
        ]
    }
    """
    matches = []
    for job in jobs:
        score, explanation = compute_job_match_score(job, user)
        matches.append({"job_id": job.id, "score": score, "explanation": explanation})
    return {"matches": sorted(matches, key=lambda x: x["score"], reverse=True)}


@app.post("/match-candidates-for-job", status_code=status.HTTP_200_OK)
async def match_job_to_users(job: JobRequirement, users: List[UserProfile]):
    """
    Returns sorted candidates for a job with explanations
    """
    return {"matches": []}  # Placeholder
