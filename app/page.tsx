"use client";

import { FormEvent, useMemo, useState } from "react";

type Job = {
  id: number;
  company: string;
  initials: string;
  color: string;
  role: string;
  location: string;
  type: string;
  salary: string;
  category: string;
  posted: string;
  featured?: boolean;
  description: string;
};

type Application = {
  id: number;
  jobId: number;
  role: string;
  company: string;
  status: "In review" | "Interview" | "Offer";
  applied: string;
};

const initialJobs: Job[] = [
  { id: 1, company: "Linear", initials: "L", color: "violet", role: "Senior Product Designer", location: "Remote · US / Europe", type: "Full-time", salary: "$130k–$165k", category: "Design", posted: "2 days ago", featured: true, description: "Shape the tools that help ambitious teams do their best work. You will partner with product and engineering to make complex workflows feel effortless." },
  { id: 2, company: "Vercel", initials: "V", color: "black", role: "Frontend Engineer", location: "New York, NY · Hybrid", type: "Full-time", salary: "$145k–$190k", category: "Engineering", posted: "1 day ago", description: "Build fast, thoughtful experiences for developers. Work across the stack with a team that cares deeply about craft, performance and simplicity." },
  { id: 3, company: "Notion", initials: "N", color: "peach", role: "Product Marketing Manager", location: "San Francisco, CA", type: "Full-time", salary: "$115k–$150k", category: "Marketing", posted: "3 days ago", featured: true, description: "Bring new product capabilities to life through clear positioning, launches and customer stories." },
  { id: 4, company: "Figma", initials: "F", color: "pink", role: "Software Engineer, Platform", location: "Remote · US", type: "Full-time", salary: "$155k–$205k", category: "Engineering", posted: "4 days ago", description: "Help create reliable infrastructure and delightful platform capabilities for millions of designers and developers." },
  { id: 5, company: "Ramp", initials: "R", color: "mint", role: "Business Operations Associate", location: "New York, NY · Hybrid", type: "Full-time", salary: "$90k–$120k", category: "Operations", posted: "5 days ago", description: "Solve high-impact operational challenges and help a fast-growing team scale with intention." },
  { id: 6, company: "Webflow", initials: "W", color: "blue", role: "UX Researcher", location: "Remote · US / Canada", type: "Contract", salary: "$75–$95 / hr", category: "Design", posted: "1 week ago", description: "Discover what customers need and turn research into product decisions that make the web more accessible." }
];

const filters = ["All roles", "Engineering", "Design", "Marketing", "Operations"];

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>(initialJobs);
  const [activeFilter, setActiveFilter] = useState("All roles");
  const [search, setSearch] = useState("");
  const [locationSearch, setLocationSearch] = useState("");
  const [saved, setSaved] = useState<number[]>([2]);
  const [applications, setApplications] = useState<Application[]>([
    { id: 101, jobId: 3, role: "Product Marketing Manager", company: "Notion", status: "Interview", applied: "Oct 18" },
    { id: 102, jobId: 6, role: "UX Researcher", company: "Webflow", status: "In review", applied: "Oct 16" }
  ]);
  const [activeTab, setActiveTab] = useState<"Discover" | "Applications" | "Saved">("Discover");
  const [recruiterMode, setRecruiterMode] = useState(false);
  const [showPostForm, setShowPostForm] = useState(false);
  const [appliedIds, setAppliedIds] = useState<number[]>([3, 6]);
  const [notice, setNotice] = useState("");

  const visibleJobs = useMemo(() => jobs.filter((job) => {
    const matchesFilter = activeFilter === "All roles" || job.category === activeFilter;
    const term = search.toLowerCase().trim();
    const matchesSearch = !term || [job.role, job.company, job.location, job.category].join(" ").toLowerCase().includes(term);
    const matchesLocation = !locationSearch.trim() || job.location.toLowerCase().includes(locationSearch.toLowerCase().trim());
    const matchesTab = activeTab !== "Saved" || saved.includes(job.id);
    return matchesFilter && matchesSearch && matchesLocation && matchesTab;
  }), [jobs, activeFilter, search, locationSearch, activeTab, saved]);

  function toggleSaved(id: number) {
    setSaved((current) => current.includes(id) ? current.filter((item) => item !== id) : [...current, id]);
  }

  function applyToJob(job: Job) {
    if (appliedIds.includes(job.id)) {
      setNotice("You have already applied to this role.");
      return;
    }
    setAppliedIds((current) => [...current, job.id]);
    setApplications((current) => [{ id: Date.now(), jobId: job.id, role: job.role, company: job.company, status: "In review", applied: "Just now" }, ...current]);
    setNotice("Application added to your tracker.");
  }

  function postJob(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const role = String(data.get("role") || "").trim();
    const company = String(data.get("company") || "").trim();
    const location = String(data.get("location") || "").trim();
    const category = String(data.get("category") || "Engineering");
    if (!role || !company || !location) return;
    const newJob: Job = {
      id: Date.now(),
      company,
      initials: company.slice(0, 1).toUpperCase(),
      color: "violet",
      role,
      location,
      type: String(data.get("type") || "Full-time"),
      salary: String(data.get("salary") || "Competitive"),
      category,
      posted: "Just now",
      featured: true,
      description: String(data.get("description") || "A great opportunity to make an impact with a growing team.")
    };
    setJobs((current) => [newJob, ...current]);
    setShowPostForm(false);
    setRecruiterMode(false);
    setActiveTab("Discover");
    setActiveFilter("All roles");
    setSearch("");
    setNotice("Your demo job post is now visible in the job board.");
    event.currentTarget.reset();
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="HireFlow home">
          <span className="brand-mark">h</span><span>hireflow<span className="brand-period">.</span></span>
        </a>
        <div className="workspace-label">WORKSPACE</div>
        <nav className="side-nav" aria-label="Main navigation">
          <button className={activeTab === "Discover" ? "nav-item active" : "nav-item"} onClick={() => { setActiveTab("Discover"); setRecruiterMode(false); }}>
            <span className="nav-icon">⌕</span> Discover jobs
          </button>
          <button className={activeTab === "Applications" ? "nav-item active" : "nav-item"} onClick={() => { setActiveTab("Applications"); setRecruiterMode(false); }}>
            <span className="nav-icon">▤</span> My applications <span className="nav-count">{applications.length}</span>
          </button>
          <button className={activeTab === "Saved" ? "nav-item active" : "nav-item"} onClick={() => { setActiveTab("Saved"); setRecruiterMode(false); }}>
            <span className="nav-icon">♡</span> Saved jobs
          </button>
          <div className="workspace-label second-label">RECRUITER</div>
          <button className={recruiterMode ? "nav-item active" : "nav-item"} onClick={() => { setRecruiterMode(true); setActiveTab("Discover"); }}>
            <span className="nav-icon">▦</span> Hiring workspace
          </button>
        </nav>
        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-spark">✳</div>
            <strong>Career tip of the day</strong>
            <p>Small, consistent steps lead to big career moves. Keep your profile fresh.</p>
            <button onClick={() => setNotice("Tip: tailor your resume summary to the role you want.")}>Read tip <span>↗</span></button>
          </div>
          <div className="profile-mini">
            <div className="avatar">KM</div>
            <div className="profile-copy"><strong>Kamlesh M.</strong><span>Personal workspace</span></div>
            <span className="more-dots">···</span>
          </div>
        </div>
      </aside>

      <section className="main-area">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> {recruiterMode ? "Hiring" : activeTab}</div>
          <div className="topbar-actions">
            <span className="status-pill"><i /> Demo workspace</span>
            <button className="icon-button" aria-label="Notifications" onClick={() => setNotice("You are all caught up.")}>♧</button>
            <div className="avatar top-avatar">KM</div>
          </div>
        </header>

        <div className="content-wrap">
          {recruiterMode ? (
            <section className="recruiter-panel">
              <div className="eyebrow"><span className="eyebrow-line" /> RECRUITER WORKSPACE</div>
              <div className="heading-row">
                <div><h1>Build your<br /><span>dream team.</span></h1><p className="page-subtitle">A clearer way to find people who move your business forward.</p></div>
                <button className="primary-button" onClick={() => setShowPostForm(true)}>＋ Post a job</button>
              </div>
              <div className="stats-grid">
                <Stat label="Active listings" value={String(jobs.length)} change="Across all categories" />
                <Stat label="Applications" value={String(applications.length + 18)} change="Demo sample activity" />
                <Stat label="Shortlisted" value="08" change="Ready for a closer look" />
                <Stat label="Avg. time to hire" value="18 days" change="Illustrative benchmark" />
              </div>
              <div className="section-heading"><div><h2>Your job listings</h2><p>Manage the roles you are sharing with the community.</p></div><button className="text-button" onClick={() => setRecruiterMode(false)}>View candidate side ↗</button></div>
              <div className="listing-table">
                <div className="table-head"><span>ROLE</span><span>LOCATION</span><span>TYPE</span><span>POSTED</span><span>STATUS</span></div>
                {jobs.slice(0, 5).map((job) => <div className="table-row" key={job.id}><div className="table-role"><CompanyLogo job={job} /><strong>{job.role}<small>{job.company}</small></strong></div><span>{job.location}</span><span>{job.type}</span><span>{job.posted}</span><span className="live-status"><i /> Active</span></div>)}
              </div>
            </section>
          ) : activeTab === "Applications" ? (
            <section>
              <div className="eyebrow"><span className="eyebrow-line" /> YOUR CAREER JOURNEY</div>
              <div className="heading-row"><div><h1>Keep your next<br /><span>move in motion.</span></h1><p className="page-subtitle">Every application, one organized place. You’ve got this.</p></div><div className="round-illustration">↗</div></div>
              <div className="application-summary"><div><span>Applications sent</span><strong>{applications.length}</strong></div><div><span>Interviews</span><strong>{applications.filter((a) => a.status === "Interview").length}</strong></div><div><span>Offers</span><strong>{applications.filter((a) => a.status === "Offer").length}</strong></div></div>
              <div className="section-heading"><div><h2>Application tracker</h2><p>Stay close to every opportunity.</p></div></div>
              <div className="application-list">{applications.map((app) => <div className="application-card" key={app.id}><div className="application-company"><div className="company-monogram">{app.company.slice(0, 1)}</div><div><strong>{app.role}</strong><span>{app.company} · Applied {app.applied}</span></div></div><span className={"application-status " + app.status.toLowerCase().replace(" ", "-")}>{app.status}</span><button className="dots-button" aria-label="Application options" onClick={() => setNotice("Your application is saved in this local demo.")}>···</button></div>)}
                {applications.length === 0 && <EmptyState title="Your tracker is ready" copy="Apply to a role and it will appear here." />}
              </div>
            </section>
          ) : (
            <>
              <section className="hero">
                <div className="hero-copy">
                  <div className="eyebrow"><span className="eyebrow-line" /> THE NEXT CHAPTER STARTS HERE</div>
                  <h1>Find work that<br /><span>moves you.</span></h1>
                  <p>Good work changes everything. Discover opportunities that fit your ambition, your life, and what you want to build next.</p>
                  <div className="hero-meta"><div className="avatar-stack"><span>J</span><span>A</span><span>M</span><span>+</span></div><span><strong>2,400+</strong> people exploring new paths</span></div>
                </div>
                <div className="hero-art" aria-hidden="true">
                  <div className="art-orbit orbit-one" /><div className="art-orbit orbit-two" /><div className="art-sun" />
                  <div className="art-card card-float"><span className="art-card-icon">✳</span><span><b>Make it matter.</b><small>Your next chapter awaits</small></span></div>
                  <div className="art-note">GOOD THINGS<br />ARE IN MOTION <span>↗</span></div>
                  <div className="art-squiggle">〰</div>
                </div>
              </section>

              <section className="search-panel">
                <div className="search-field"><span>⌕</span><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Job title, keyword or company" aria-label="Search jobs" /></div>
                <div className="search-divider" />
                <div className="location-field"><span>⌖</span><input value={locationSearch} onChange={(e) => setLocationSearch(e.target.value)} placeholder="City or remote" aria-label="Location" /></div>
                <button className="search-button" onClick={() => setNotice(visibleJobs.length + " matching roles found.")}>Search jobs <span>→</span></button>
              </section>

              <section className="jobs-section">
                <div className="section-heading jobs-heading"><div><div className="eyebrow small-eyebrow">CURATED FOR YOUR NEXT STEP</div><h2>{activeTab === "Saved" ? "Your saved roles" : "Explore opportunities"} <span className="result-count">{visibleJobs.length}</span></h2><p>Thoughtful teams. Meaningful work. Room to grow.</p></div><button className="sort-button" onClick={() => setNotice("Showing the newest opportunities first.")}>↕ <span>Most relevant</span></button></div>
                <div className="filter-row">{filters.map((filter) => <button key={filter} className={activeFilter === filter ? "filter-chip selected" : "filter-chip"} onClick={() => setActiveFilter(filter)}>{filter}</button>)}</div>
                <div className="job-grid">
                  {visibleJobs.map((job) => <JobCard key={job.id} job={job} isSaved={saved.includes(job.id)} isApplied={appliedIds.includes(job.id)} onSave={() => toggleSaved(job.id)} onApply={() => applyToJob(job)} />)}
                  {visibleJobs.length === 0 && <EmptyState title="No roles found" copy="Try another keyword or choose a different category." />}
                </div>
              </section>
            </>
          )}
          <footer className="footer"><span>© 2026 HireFlow</span><span>Made for what’s next <b>✳</b></span><span>Privacy · About · Help</span></footer>
        </div>
      </section>

      {notice && <div className="toast" role="status"><span>✳</span>{notice}<button onClick={() => setNotice("")} aria-label="Dismiss notification">×</button></div>}

      {showPostForm && <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setShowPostForm(false); }}><form className="post-modal" onSubmit={postJob}><div className="modal-top"><div><span className="eyebrow">GROW YOUR TEAM</span><h2>Post a new role</h2><p>Share an opportunity with the HireFlow community.</p></div><button type="button" className="close-button" onClick={() => setShowPostForm(false)}>×</button></div><label>Job title<input name="role" required placeholder="e.g. Product Designer" /></label><label>Company<input name="company" required placeholder="e.g. Acme Studio" /></label><label>Location<input name="location" required placeholder="e.g. Remote · India" /></label><div className="form-two"><label>Category<select name="category"><option>Engineering</option><option>Design</option><option>Marketing</option><option>Operations</option></select></label><label>Employment type<select name="type"><option>Full-time</option><option>Part-time</option><option>Contract</option><option>Internship</option></select></label></div><label>Salary range<input name="salary" placeholder="e.g. ₹12–18 LPA" /></label><label>About the role<textarea name="description" rows={3} placeholder="What will this person work on?" /></label><button className="primary-button modal-submit" type="submit">Publish demo listing <span>→</span></button><p className="modal-footnote">Demo mode: this listing is stored in browser memory only.</p></form></div>}
    </main>
  );
}

function Stat({ label, value, change }: { label: string; value: string; change: string }) {
  return <div className="stat-card"><span>{label}</span><strong>{value}</strong><small>{change}</small></div>;
}

function CompanyLogo({ job }: { job: Job }) {
  return <div className={"company-logo " + job.color}>{job.initials}</div>;
}

function JobCard({ job, isSaved, isApplied, onSave, onApply }: { job: Job; isSaved: boolean; isApplied: boolean; onSave: () => void; onApply: () => void }) {
  return <article className="job-card">
    <div className="job-card-top"><CompanyLogo job={job} /><button className={isSaved ? "save-button saved" : "save-button"} onClick={onSave} aria-label={isSaved ? "Remove saved job" : "Save job"}>{isSaved ? "♥" : "♡"}</button></div>
    <div className="job-company">{job.company} <span>·</span> <span>{job.posted}</span>{job.featured && <b className="featured-tag">FEATURED</b>}</div>
    <h3>{job.role}</h3>
    <p className="job-location">{job.location}</p>
    <div className="job-tags"><span>{job.type}</span><span>{job.category}</span></div>
    <div className="job-card-bottom"><div><strong>{job.salary}</strong><small>Estimated compensation</small></div><button className={isApplied ? "applied-button" : "apply-button"} onClick={onApply}>{isApplied ? "Applied ✓" : "Quick apply ↗"}</button></div>
  </article>;
}

function EmptyState({ title, copy }: { title: string; copy: string }) {
  return <div className="empty-state"><div>⌕</div><strong>{title}</strong><p>{copy}</p></div>;
}
