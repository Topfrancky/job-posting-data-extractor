# Job Posting Data Extractor

A beginner-friendly Python portfolio exercise demonstrating **HTML structure, CSS selectors, regex, and structured job-data capture**. Uses a local mock job board; does not scrape a live website.

## Quick start

```bash
cd job_data_extractor
python -m pip install -r requirements.txt
python extract_jobs.py
python -m unittest -v
```

To use another saved HTML page:

```bash
python extract_jobs.py --input another_jobs_page.html --output extracted_jobs.csv
```

## How it works

1. `BeautifulSoup(html, "html.parser")` parses HTML.
2. `soup.select("article.job-card")` finds job posting cards using a **CSS selector**.
3. `card.select_one(".job-title")` and `.job-location` find elements within each card.
4. Regex `^(?:JOB|REQ)-\d{4,}$` validates IDs in `data-job-id` attributes.
5. If that attribute is absent/invalid, the code looks for `jobId=1043` in the link query or `REQ-2044` in the path.
6. The extractor creates a CSV with columns `job_title`, `location`, `job_id`.

## Expected output

| job_title | location | job_id |
|---|---|---|
| Technical Analyst I | Remote - USA | JOB-1042 |
| Data Quality Analyst | Atlanta, GA | JOB-1043 |
| Web Data Specialist | Hybrid - Boston, MA | REQ-2044 |
| Junior HTML Analyst | New York, NY | JOB-1045 |
| Missing Identifier Example | Remote | *(empty)* |

The missing ID stays empty rather than being invented.

## What to practice

- Change `article.job-card` to `.job-card`, rerun, and explain the difference.
- Add a sixth `<article>` to `jobs.html`, then update the count assertion in the tests.
- Add a `department` field using another HTML element and CSS selector.
- Try an ID format such as `REQ-99999` and check the regex.
- Explain why HTML parsers + CSS selectors are more reliable than regex for extracting nested HTML.

## Interview description

"I built a Python extractor for sample job postings. It used BeautifulSoup CSS selectors to capture job titles and locations, regex to validate job requisition IDs, URL parsing for fallback ID retrieval, and automated tests to handle missing identifiers. It exports a clean CSV for further analysis."
