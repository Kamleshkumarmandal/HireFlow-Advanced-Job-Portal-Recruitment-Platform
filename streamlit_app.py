from __future__ import annotations

import io
from datetime import datetime

import pandas as pd
import streamlit as st

from hireflow_engine import (
    APPLICATION_STATUSES,
    INITIAL_APPLICATIONS,
    INITIAL_JOBS,
    filter_jobs,
    make_application,
    validate_job_post,
)

st.set_page_config(
    page_title="HireFlow | Find work that moves you forward",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f7f8fc;color:#202b42}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e9ecf2}
.brand{font:800 25px Manrope;letter-spacing:-1.2px;color:#202b42;margin:3px 0 22px}
.brand span{color:#7061e8}
.side-caption{font-size:9px;font-weight:800;letter-spacing:1.4px;color:#9aa3b1;margin:15px 0 7px}
.hero{background:linear-gradient(112deg,#292347,#514579);border-radius:17px;padding:27px 30px;color:white;margin:8px 0 18px}
.hero .eyebrow{color:#d0c6ff;font-size:9px;font-weight:800;letter-spacing:1.6px;margin-bottom:10px}
.hero h1{font:800 32px Manrope;letter-spacing:-1.6px;color:white;margin:0 0 7px}
.hero p{font-size:12px;line-height:1.7;color:#e0dced;max-width:690px;margin:0}
.section-title{font:800 19px Manrope;letter-spacing:-.5px;color:#26314a;margin:10px 0 3px}
.section-sub{font-size:10px;color:#909bad;margin-bottom:13px}
div[data-testid="stMetric"]{background:#fff;border:1px solid #e9ecf2;border-radius:11px;padding:13px 15px;box-shadow:0 3px 14px #17243b07}
div[data-testid="stMetricLabel"]{font-size:10px;color:#8994a6}
div[data-testid="stMetricValue"]{font:800 23px Manrope;color:#26314a}
.job-card{background:#fff;border:1px solid #e9ecf2;border-radius:12px;padding:15px 17px;margin:0 0 10px}
.job-card strong{font-size:13px;color:#26314a}
.muted{font-size:10px;color:#8994a6}
.pill{display:inline-block;padding:4px 8px;border-radius:18px;background:#f0efff;color:#695ce1;font-size:9px;font-weight:700}
.good{display:inline-block;padding:4px 8px;border-radius:18px;background:#eaf8f2;color:#278b67;font-size:9px;font-weight:700}
.warn{display:inline-block;padding:4px 8px;border-radius:18px;background:#fff5e8;color:#b67a29;font-size:9px;font-weight:700}
.insight{background:#efedff;border:1px solid #e4e1ff;border-radius:10px;padding:12px 15px;color:#5449c2;font-size:11px;line-height:1.6;margin:10px 0 15px}
.smallcaps{font-size:8px;letter-spacing:1.1px;color:#9da6b4;font-weight:800}
.footer{font-size:9px;color:#9ba4b2;text-align:center;padding:22px 0 8px}
.stButton>button{border-radius:8px;font-weight:600}
.stButton>button[kind="primary"]{background:#6b5de7;border-color:#6b5de7}
div[data-testid="stDataFrame"]{border:1px solid #e9ecf2;border-radius:10px;overflow:hidden}
hr{border-color:#e9ecf2}
</style>
""", unsafe_allow_html=True)

if "jobs" not in st.session_state:
    st.session_state.jobs = [dict(job) for job in INITIAL_JOBS]
if "applications" not in st.session_state:
    st.session_state.applications = [dict(app) for app in INITIAL_APPLICATIONS]
if "saved_ids" not in st.session_state:
    st.session_state.saved_ids = {2}
if "active_view" not in st.session_state:
    st.session_state.active_view = "Discover jobs"
if "notice" not in st.session_state:
    st.session_state.notice = ""

jobs = st.session_state.jobs
applications = st.session_state.applications
saved_ids = st.session_state.saved_ids

with st.sidebar:
    st.markdown('<div class="brand">hireflow<span>.</span></div>', unsafe_allow_html=True)
    st.caption("CAREER WORKSPACE · DEMO")
    view = st.radio(
        "WORKSPACE",
        ["Discover jobs", "My applications", "Saved jobs", "Hiring workspace"],
        index=["Discover jobs", "My applications", "Saved jobs", "Hiring workspace"].index(st.session_state.active_view),
    )
    st.session_state.active_view = view
    st.divider()
    st.markdown("**YOUR ACTIVITY**")
    st.metric("Applications", len(applications))
    st.metric("Saved roles", len(saved_ids))
    st.divider()
    if st.button("↻ Reset sample workspace", use_container_width=True):
        st.session_state.jobs = [dict(job) for job in INITIAL_JOBS]
        st.session_state.applications = [dict(app) for app in INITIAL_APPLICATIONS]
        st.session_state.saved_ids = {2}
        st.rerun()
    st.caption("Sample records only. No real candidate or recruiter accounts are connected.")

st.markdown('<div class="hero"><div class="eyebrow">DISCOVER · APPLY · GROW</div><h1>Your next opportunity starts here.</h1><p>Explore roles, keep applications organized and give recruiters a simple workspace to share opportunities. HireFlow brings both sides of the hiring journey into one place.</p></div>', unsafe_allow_html=True)

if view in ("Discover jobs", "Saved jobs"):
    st.markdown('<div class="section-title">Find your next role</div><div class="section-sub">Search open opportunities and narrow the list to what matters to you.</div>', unsafe_allow_html=True)
    filters_a, filters_b, filters_c = st.columns([1.5, 1.1, 1])
    query = filters_a.text_input("Search roles", placeholder="Job title, company or keyword", label_visibility="collapsed")
    location = filters_b.text_input("Location", placeholder="Location", label_visibility="collapsed")
    category = filters_c.selectbox("Category", ["All roles", "Engineering", "Design", "Marketing", "Operations"], label_visibility="collapsed")
    type_filter = st.selectbox("Employment type", ["All types", "Full-time", "Contract", "Part-time", "Internship"], label_visibility="collapsed")
    visible = filter_jobs(
        jobs,
        query=query,
        location=location,
        category=category,
        job_type=type_filter,
        saved_ids=saved_ids,
        saved_only=(view == "Saved jobs"),
    )
    count_col, featured_col = st.columns([1, 1])
    count_col.caption(f"{len(visible)} opportunities match your filters")
    featured_col.caption("Sample job listings · Not live vacancies")
    left, right = st.columns([1.8, 1])
    with left:
        if not visible:
            st.info("No roles match these filters. Try a broader search or reset the filters.")
        for job in visible:
            with st.container(border=True):
                initials = job.get("initials", job["company"][:1])
                top_a, top_b = st.columns([4, 1])
                top_a.markdown(f"**{job['role']}**")
                top_a.caption(f"{initials}  {job['company']} · {job['posted']}")
                top_b.markdown('<span class="pill">'+job["category"]+'</span>', unsafe_allow_html=True)
                st.write(job["description"])
                meta_a, meta_b, meta_c = st.columns(3)
                meta_a.caption("📍 " + job["location"])
                meta_b.caption("◷ " + job["type"])
                meta_c.caption("◎ " + job["salary"])
                action_a, action_b, action_c = st.columns([1, 1, 2])
                if job["id"] in saved_ids:
                    if action_a.button("♥ Saved", key=f"unsave-{job['id']}"):
                        st.session_state.saved_ids.remove(job["id"])
                        st.rerun()
                else:
                    if action_a.button("♡ Save role", key=f"save-{job['id']}"):
                        st.session_state.saved_ids.add(job["id"])
                        st.rerun()
                already_applied = any(int(app["job_id"]) == int(job["id"]) for app in applications)
                if already_applied:
                    action_b.button("Applied ✓", key=f"applied-{job['id']}", disabled=True)
                elif action_b.button("Quick apply", key=f"apply-{job['id']}", type="primary"):
                    application = make_application(job, int(datetime.now().timestamp() * 1000))
                    st.session_state.applications.insert(0, application)
                    st.session_state.notice = f"Application for {job['role']} was added to your demo tracker."
                    st.rerun()
        with st.expander("＋ Add a sample job listing"):
            with st.form("candidate_add_job", clear_on_submit=True):
                role = st.text_input("Role title")
                company = st.text_input("Company")
                job_location = st.text_input("Location")
                job_category = st.selectbox("Category", ["Engineering", "Design", "Marketing", "Operations"])
                submit = st.form_submit_button("Add listing")
                if submit:
                    valid, error = validate_job_post(role, company, job_location, job_category)
                    if not valid:
                        st.error(error)
                    else:
                        st.session_state.jobs.insert(0, {
                            "id": max([int(x["id"]) for x in st.session_state.jobs] + [0]) + 1,
                            "company": company.strip(), "initials": company.strip()[:1].upper(),
                            "role": role.strip(), "location": job_location.strip(),
                            "type": "Full-time", "salary": "Competitive",
                            "category": job_category, "posted": "Just now",
                            "featured": False, "description": "New sample opportunity added to this session.",
                        })
                        st.success("Sample listing added.")
                        st.rerun()
    with right:
        st.markdown('<div class="section-title">Your career snapshot</div>', unsafe_allow_html=True)
        st.metric("Saved roles", len(saved_ids))
        st.metric("Applications sent", len(applications))
        st.metric("Interviews", sum(app["status"] == "Interview" for app in applications))
        st.markdown('<div class="insight"><b>✳ A small career tip</b><br/>Tailor the first few lines of your resume to the role, and keep a short note about why the team interests you.</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Popular categories</div>', unsafe_allow_html=True)
        category_counts = pd.Series([job["category"] for job in jobs]).value_counts()
        st.bar_chart(category_counts, horizontal=True, color="#7669ec")

elif view == "My applications":
    st.markdown('<div class="section-title">Your application tracker</div><div class="section-sub">Keep every opportunity organized from application to outcome.</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("Applications", len(applications))
    b.metric("Interviews", sum(app["status"] == "Interview" for app in applications))
    c.metric("Offers", sum(app["status"] == "Offer" for app in applications))
    st.divider()
    if not applications:
        st.info("No applications yet. Explore jobs and use Quick apply to add one.")
    for application in applications:
        with st.container(border=True):
            left, mid, right = st.columns([2, 1, 1])
            left.markdown(f"**{application['role']}**")
            left.caption(f"{application['company']} · Applied {application['applied']}")
            current_index = APPLICATION_STATUSES.index(application["status"]) if application["status"] in APPLICATION_STATUSES else 0
            new_status = mid.selectbox("Status", APPLICATION_STATUSES, index=current_index, key=f"status-{application['id']}")
            if new_status != application["status"]:
                application["status"] = new_status
                st.session_state.notice = f"Application status updated to {new_status}."
                st.rerun()
            if right.button("Remove", key=f"remove-app-{application['id']}"):
                st.session_state.applications = [item for item in st.session_state.applications if item["id"] != application["id"]]
                st.rerun()
    if applications:
        frame = pd.DataFrame(applications)
        st.download_button("⬇ Download application tracker CSV", frame.to_csv(index=False), "hireflow-applications.csv", "text/csv")

elif view == "Hiring workspace":
    st.markdown('<div class="section-title">Build your dream team.</div><div class="section-sub">A lightweight recruiter workspace for publishing roles and reviewing demo activity.</div>', unsafe_allow_html=True)
    x, y, z = st.columns(3)
    x.metric("Active listings", len(jobs))
    y.metric("Applications in demo", len(applications) + 18, "Illustrative sample activity")
    z.metric("Saved candidate roles", len(saved_ids), "Candidate-side saves")
    st.markdown('<div class="section-title">Your job listings</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{
        "Role": job["role"], "Company": job["company"], "Location": job["location"],
        "Category": job["category"], "Type": job["type"], "Posted": job["posted"],
    } for job in jobs]), use_container_width=True, hide_index=True)
    with st.expander("＋ Publish a sample job"):
        with st.form("recruiter_job_form", clear_on_submit=True):
            role = st.text_input("Role title")
            company = st.text_input("Company")
            location = st.text_input("Location")
            category = st.selectbox("Category", ["Engineering", "Design", "Marketing", "Operations"])
            job_type = st.selectbox("Employment type", ["Full-time", "Contract", "Part-time", "Internship"])
            salary = st.text_input("Salary range", value="Competitive")
            description = st.text_area("Role description")
            submitted = st.form_submit_button("Publish sample listing", type="primary")
            if submitted:
                valid, error = validate_job_post(role, company, location, category)
                if not valid:
                    st.error(error)
                else:
                    st.session_state.jobs.insert(0, {
                        "id": max([int(item["id"]) for item in st.session_state.jobs] + [0]) + 1,
                        "company": company.strip(), "initials": company.strip()[:1].upper(),
                        "role": role.strip(), "location": location.strip(), "type": job_type,
                        "salary": salary.strip() or "Competitive", "category": category,
                        "posted": "Just now", "featured": False,
                        "description": description.strip() or "A new sample opportunity.",
                    })
                    st.success("Your sample job listing is now visible in Discover jobs.")
                    st.rerun()
    st.caption("Recruiter metrics are illustrative; there is no real candidate database or applicant inbox connected.")

if st.session_state.notice:
    st.success(st.session_state.notice)
    st.session_state.notice = ""

st.divider()
st.markdown('<div class="smallcaps">HIREFLOW · CAREERS IN MOTION</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Independent portfolio demo · Sample listings and in-session actions only · Changes reset when the app session restarts.</div>', unsafe_allow_html=True)
