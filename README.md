# HireFlow — Advanced Job Portal & Recruitment Platform

HireFlow is a responsive job discovery and recruitment workspace built with Next.js, React, TypeScript and Tailwind CSS. It is designed as a portfolio project that can grow from a polished front-end prototype into a full-stack recruitment platform.

## Current demo features

🚀live demo
https://hireflow-advanced-job-app-recruitment-platform-cymk42fl2okcmxe.streamlit.app/

- Responsive candidate-facing job discovery dashboard
- Search by job title, company, location text or category
- Category filters for Engineering, Design, Marketing and Operations
- Save and unsave job listings
- Quick-apply interaction and a local application tracker
- Candidate application statuses: In review, Interview and Offer
- Recruiter workspace with listing overview and demo metrics
- Job-post form that adds a listing to the current browser session
- Mobile-friendly layout

## Important: demo vs. production

The current interface uses sample data and React state. Saved jobs, applications and newly posted roles are **not persisted**; they reset when the page is refreshed. The login flow, resume upload, real email notifications, admin controls and live analytics are not implemented yet.

A starter PostgreSQL schema and Row Level Security policies are included at `supabase/schema.sql`. The UI is not connected to Supabase yet.


## Streamlit demo

A separate Streamlit version is available alongside the original Next.js app.

- **Demo status:** Not deployed yet — Streamlit Cloud must generate the public URL.
- **Repository entrypoint:** `streamlit_app.py`
- **Python dependencies:** `requirements.txt`
- **Deployment guide:** [docs/streamlit-deployment.md](docs/streamlit-deployment.md)
- **Deploy:** [Open Streamlit Community Cloud](https://share.streamlit.io)

The Streamlit edition includes job search and filters, saved roles, a candidate application tracker with editable statuses, a recruiter workspace, job-post creation, dashboard metrics and CSV export. It uses illustrative sample data and Streamlit session state; it is not connected to the existing Supabase schema.

## Tech stack

- Next.js 15 App Router
- React 19
- TypeScript
- Tailwind CSS 3
- Supabase / PostgreSQL schema starter

## Run locally

You need Node.js 20 or newer and npm.

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

To create a production build:

```bash
npm run build
npm start
```

## Supabase setup (next development step)

1. Create a Supabase project.
2. Open the SQL Editor and run `supabase/schema.sql`.
3. Copy `.env.example` to `.env.local`.
4. Add your Supabase project URL and anon key to `.env.local`.
5. Add the Supabase client, authentication, protected routes and data queries before describing the app as a live full-stack service.

Never commit `.env.local`, service-role keys, passwords or other secrets.

## Suggested roadmap

- [ ] Supabase authentication for candidates and recruiters
- [ ] Profile onboarding and role-based dashboards
- [ ] Persist jobs, saved roles and applications in PostgreSQL
- [ ] Private resume storage with secure upload policies
- [ ] Recruiter applicant pipeline and status updates
- [ ] Admin moderation and reporting
- [ ] Automated tests and CI checks
- [ ] Deploy the production build

## Project structure

```text
app/
  globals.css
  layout.tsx
  page.tsx
supabase/
  schema.sql
.env.example
```

## License

This project is available under the MIT License. See [LICENSE](LICENSE).
