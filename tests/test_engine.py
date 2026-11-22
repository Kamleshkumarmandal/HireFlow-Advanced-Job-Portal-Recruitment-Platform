import unittest

from hireflow_engine import (
    INITIAL_APPLICATIONS,
    INITIAL_JOBS,
    filter_jobs,
    make_application,
    validate_job_post,
)


class HireFlowEngineTests(unittest.TestCase):
    def test_filter_by_category(self):
        jobs = filter_jobs(INITIAL_JOBS, category="Engineering")
        self.assertTrue(jobs)
        self.assertTrue(all(job["category"] == "Engineering" for job in jobs))

    def test_search_matches_company_and_role(self):
        by_company = filter_jobs(INITIAL_JOBS, query="vercel")
        by_role = filter_jobs(INITIAL_JOBS, query="backend engineer")
        self.assertEqual([job["company"] for job in by_company], ["Vercel"])
        self.assertEqual([job["company"] for job in by_role], ["Stripe"])

    def test_location_and_type_filters(self):
        jobs = filter_jobs(INITIAL_JOBS, location="remote", job_type="Contract")
        self.assertEqual([job["company"] for job in jobs], ["Webflow"])

    def test_saved_only_filter(self):
        jobs = filter_jobs(INITIAL_JOBS, saved_ids={2, 4}, saved_only=True)
        self.assertEqual({job["id"] for job in jobs}, {2, 4})

    def test_validate_job_post_requires_fields(self):
        valid, message = validate_job_post("", "Acme", "Remote", "Engineering")
        self.assertFalse(valid)
        self.assertIn("required", message)

    def test_validate_job_post_checks_category(self):
        valid, _ = validate_job_post("Engineer", "Acme", "Remote", "Engineering")
        self.assertTrue(valid)
        valid, message = validate_job_post("Engineer", "Acme", "Remote", "Other")
        self.assertFalse(valid)
        self.assertIn("category", message)

    def test_make_application(self):
        app = make_application(INITIAL_JOBS[1], 999, "Today")
        self.assertEqual(app["job_id"], 2)
        self.assertEqual(app["company"], "Vercel")
        self.assertEqual(app["status"], "In review")
        self.assertEqual(app["applied"], "Today")

    def test_seed_applications_have_expected_statuses(self):
        self.assertEqual({app["status"] for app in INITIAL_APPLICATIONS}, {"Interview", "In review"})


if __name__ == "__main__":
    unittest.main()
