-- HireFlow starter schema for Supabase (PostgreSQL).
-- Run this in Supabase SQL Editor after creating a project.
-- The current Next.js interface is a local demo and does not connect to this schema yet.

create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null default '',
  role text not null default 'candidate' check (role in ('candidate', 'recruiter', 'admin')),
  headline text,
  location text,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.jobs (
  id uuid primary key default gen_random_uuid(),
  recruiter_id uuid not null references public.profiles(id) on delete cascade,
  company_name text not null,
  title text not null,
  description text not null,
  location text not null,
  employment_type text not null default 'Full-time',
  category text not null default 'Other',
  salary_min integer,
  salary_max integer,
  currency text not null default 'USD',
  status text not null default 'draft' check (status in ('draft', 'active', 'paused', 'closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint salary_range_valid check (salary_min is null or salary_max is null or salary_max >= salary_min)
);

create table if not exists public.applications (
  id uuid primary key default gen_random_uuid(),
  job_id uuid not null references public.jobs(id) on delete cascade,
  candidate_id uuid not null references public.profiles(id) on delete cascade,
  cover_letter text,
  resume_url text,
  status text not null default 'submitted' check (status in ('submitted', 'reviewing', 'interview', 'offer', 'rejected', 'withdrawn')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (job_id, candidate_id)
);

create index if not exists jobs_status_created_idx on public.jobs(status, created_at desc);
create index if not exists jobs_category_idx on public.jobs(category);
create index if not exists applications_candidate_idx on public.applications(candidate_id, created_at desc);
create index if not exists applications_job_idx on public.applications(job_id, created_at desc);

alter table public.profiles enable row level security;
alter table public.jobs enable row level security;
alter table public.applications enable row level security;

-- Profiles: each signed-in user can read and update their own profile.
create policy "Users can read own profile"
  on public.profiles for select to authenticated
  using (id = auth.uid());

create policy "Users can create own profile"
  on public.profiles for insert to authenticated
  with check (id = auth.uid());

create policy "Users can update own profile"
  on public.profiles for update to authenticated
  using (id = auth.uid())
  with check (id = auth.uid());

-- Anyone can discover active job listings. Recruiters manage their own listings.
create policy "Active jobs are visible"
  on public.jobs for select to anon, authenticated
  using (status = 'active' or recruiter_id = auth.uid());

create policy "Recruiters can create own jobs"
  on public.jobs for insert to authenticated
  with check (recruiter_id = auth.uid());

create policy "Recruiters can update own jobs"
  on public.jobs for update to authenticated
  using (recruiter_id = auth.uid())
  with check (recruiter_id = auth.uid());

create policy "Recruiters can delete own jobs"
  on public.jobs for delete to authenticated
  using (recruiter_id = auth.uid());

-- Candidates see their applications; the owner of a job can review applications for it.
create policy "Applicants and job owners can read applications"
  on public.applications for select to authenticated
  using (
    candidate_id = auth.uid()
    or exists (
      select 1 from public.jobs
      where jobs.id = applications.job_id
        and jobs.recruiter_id = auth.uid()
    )
  );

create policy "Candidates can apply as themselves"
  on public.applications for insert to authenticated
  with check (candidate_id = auth.uid());

create policy "Candidates can withdraw or job owners can update status"
  on public.applications for update to authenticated
  using (
    candidate_id = auth.uid()
    or exists (
      select 1 from public.jobs
      where jobs.id = applications.job_id
        and jobs.recruiter_id = auth.uid()
    )
  )
  with check (
    candidate_id = auth.uid()
    or exists (
      select 1 from public.jobs
      where jobs.id = applications.job_id
        and jobs.recruiter_id = auth.uid()
    )
  );

-- Production note: add storage bucket policies for private resumes before accepting uploads.
