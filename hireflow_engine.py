"""Shared demo data and helpers for the HireFlow Streamlit edition."""

from __future__ import annotations

from typing import Any


INITIAL_JOBS: list[dict[str, Any]] = [
    {
        "id": 1, "company": "Linear", "initials": "L", "role": "Senior Product Designer",
        "location": "Remote · US / Europe", "type": "Full-time", "salary": "$130k–$165k",
        "category": "Design", "posted": "2 days ago", "featured": True,
        "description": "Shape the tools that help ambitious teams do their best work. Partner with product and engineering to make complex workflows feel effortless.",
    },
    {
        "id": 2, "company": "Vercel", "initials": "V", "role": "Frontend Engineer",
        "location": "New York, NY · Hybrid", "type": "Full-time", "salary": "$145k–$190k",
        "category": "Engineering", "posted": "1 day ago", "featured": False,
        "description": "Build thoughtful developer experiences across the stack with a team that cares deeply about craft and performance.",
    },
    {
        "id": 3, "company": "Notion", "initials": "N", "role": "Product Marketing Manager",
        "location": "San Francisco, CA", "type": "Full-time", "salary": "$115k–$150k",
        "category": "Marketing", "posted": "3 days ago", "featured": True,
        "description": "Bring new product capabilities to life through clear positioning, launches and customer stories.",
    },
    {
        "id": 4, "company": "Figma", "initials": "F", "role": "Software Engineer, Platform",
        "location": "Remote · US", "type": "Full-time", "salary": "$155k–$205k",
        "category": "Engineering", "posted": "4 days ago", "featured": False,
        "description": "Create reliable infrastructure and delightful platform capabilities for millions of designers and developers.",
    },
    {
        "id": 5, "company": "Ramp", "initials": "R", "role": "Business Operations Associate",
        "location": "New York, NY · Hybrid", "type": "Full-time", "salary": "$90k–$120k",
        "category": "Operations", "posted": "5 days ago", "featured": False,
        "description": "Solve high-impact operational challenges and help a fast-growing team scale with intention.",
    },
    {
        "id": 6, "company": "Webflow", "initials": "W", "role": "UX Researcher",
        "location": "Remote · US / Canada", "type": "Contract", "salary": "$75–$95 / hr",
        "category": "Design", "posted": "1 week ago", "featured": False,
        "description": "Discover what customers need and turn research into product decisions that make the web more accessible.",
    },
    {
        "id": 7, "company": "Stripe", "initials": "S", "role": "Backend Engineer",
        "location": "Remote · Europe", "type": "Full-time", "salary": "$125k–$175k",
        "category": "Engineering", "posted": "2 days ago", "featured": True,
        "description": "Build dependable APIs and services that help internet businesses accept payments and manage revenue.",
    },
]


INITIAL_APPLICATIONS: list[dict[str, Any]] = [
    {
        "id": 101, "job_id": 3, "role": "Product Marketing Manager",
        "company": "Notion", "status": "Interview", "applied": "Oct 18",
    },
    {
        "id": 102, "job_id": 6, "role": "UX Researcher",
        "company": "Webflow", "status": "In review", "applied": "Oct 16",
    },
]

APPLICATION_STATUSES = ["In review", "Interview", "Offer", "Rejected"]


def filter_jobs(
    jobs: list[dict[str, Any]],
    *,
    query: str = "",
    location: str = "",
    category: str = "All roles",
    job_type: str = "All types",
    saved_ids: set[int] | None = None,
    saved_only: bool = False,
) -> list[dict[str, Any]]:
    """Filter jobs by text, location, category, type and saved state."""
    term = query.casefold().strip()
    location_term = location.casefold().strip()
    result = []
    for job in jobs:
        searchable = " ".join(
            str(job.get(key, "")) for key in ("role", "company", "location", "category", "description")
        ).casefold()
        if term and term not in searchable:
            continue
        if location_term and location_term not in str(job.get("location", "")).casefold():
            continue
        if category != "All roles" and job.get("category") != category:
            continue
        if job_type != "All types" and job.get("type") != job_type:
            continue
        if saved_only and (saved_ids is None or int(job["id"]) not in saved_ids):
            continue
        result.append(job)
    return result


def validate_job_post(
    role: str,
    company: str,
    location: str,
    category: str,
) -> tuple[bool, str]:
    """Validate required fields and allowed job categories."""
    if not role.strip() or not company.strip() or not location.strip():
        return False, "Role, company and location are required."
    if category not in {"Engineering", "Design", "Marketing", "Operations"}:
        return False, "Choose a supported job category."
    return True, ""


def make_application(job: dict[str, Any], application_id: int, applied: str = "Just now") -> dict[str, Any]:
    """Create a candidate application record for a job."""
    return {
        "id": application_id,
        "job_id": int(job["id"]),
        "role": job["role"],
        "company": job["company"],
        "status": "In review",
        "applied": applied,
    }
