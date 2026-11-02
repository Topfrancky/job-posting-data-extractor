"""Extract job posting data from a locally saved HTML page."""
import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

ID_PATTERN = re.compile(r"^(?:JOB|REQ)-\d{4,}$", re.IGNORECASE)
PATH_ID_PATTERN = re.compile(r"(?:JOB|REQ)-\d{4,}", re.IGNORECASE)


def find_job_id(card):
    """Prioritize structured HTML attributes; fall back to IDs in job URLs."""
    attr_id = (card.get("data-job-id") or "").strip()
    if ID_PATTERN.fullmatch(attr_id):
        return attr_id.upper()

    link = card.select_one("a[href]")
    if not link:
        return None
    href = link["href"]
    parsed = urlparse(href)
    # Handle query parameters like ?jobId=1043.
    params = parse_qs(parsed.query)
    for name, values in params.items():
        if name.lower() == "jobid" and values:
            number = values[0].strip()
            if re.fullmatch(r"\d{4,}", number):
                return f"JOB-{number}"
    # Handle path segments like /careers/specialist/REQ-2044.
    match = PATH_ID_PATTERN.search(parsed.path)
    return match.group(0).upper() if match else None


def extract_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for card in soup.select("article.job-card"):
        title = card.select_one(".job-title")
        location = card.select_one(".job-location")
        if not title or not location:
            continue
        jobs.append({
            "job_title": title.get_text(" ", strip=True),
            "location": location.get_text(" ", strip=True),
            "job_id": find_job_id(card),
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description="Extract job titles, locations, and IDs from HTML.")
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("jobs.html"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("jobs.csv"))
    args = parser.parse_args()

    html = args.input.read_text(encoding="utf-8")
    jobs = extract_jobs(html)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["job_title", "location", "job_id"])
        writer.writeheader()
        writer.writerows(jobs)
    print(json.dumps(jobs, indent=2))
    print(f"Saved {len(jobs)} jobs to {args.output}")


if __name__ == "__main__":
    main()
