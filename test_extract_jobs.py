import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from extract_jobs import extract_jobs, find_job_id


class ExtractJobsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jobs = extract_jobs(Path(__file__).with_name("jobs.html").read_text(encoding="utf-8"))

    def test_extracts_all_five_cards(self):
        self.assertEqual(len(self.jobs), 5)

    def test_extracts_title_and_location(self):
        self.assertEqual(self.jobs[0]["job_title"], "Technical Analyst I")
        self.assertEqual(self.jobs[1]["location"], "Atlanta, GA")

    def test_extracts_attribute_and_url_ids(self):
        self.assertEqual([job["job_id"] for job in self.jobs[:4]],
                         ["JOB-1042", "JOB-1043", "REQ-2044", "JOB-1045"])

    def test_missing_id_is_none(self):
        self.assertIsNone(self.jobs[4]["job_id"])

    def test_invalid_attribute_falls_back_to_url(self):
        card = BeautifulSoup('<article data-job-id="INVALID"><a href="/jobs?jobId=3333">Go</a></article>', "html.parser").article
        self.assertEqual(find_job_id(card), "JOB-3333")


if __name__ == "__main__":
    unittest.main()
