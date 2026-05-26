#Basic job webscrape search that saves output to csv

import requests
import certifi
import time
import csv

all_jobs = []

for page in range(1,2): #change how many pages to scrape

    url = 'https://tjapi.timesjobs.com/search/api/v1/search/jobs/list'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0',
        'Content-Type': 'application/json'
    }

    payload = {
        "keyword": "python",    #job search term
        "page": page
    }

    res = requests.post(
        url,
        headers=headers,
        json=payload,
        verify=certifi.where(),
        timeout=10
    )

    data = res.json()
    jobs = data["jobs"]

    if not jobs:
        break

    all_jobs.extend(jobs)

    time.sleep(3)   #rate limit, 1 request per second

#debug, uncomment if needed, will print output to terminal
#for job in all_jobs:
#    print(job["title"])

with open("job_results.csv", "w", newline="", encoding="utf-8") as f:
    csv_file = csv.writer(f)
    csv_file.writerow(["Title",
                       "Job Function",
                       "Skills",
                       "Post Date",
                       "Company",
                       "Job Type",
                       "URL Link"
                       ])

    for job in all_jobs:
        csv_file.writerow([
            job.get("title", "No title"),
            job.get("jobFunction"),
            job.get("skills", "No skills"),
            job.get("postDate", "Post date unknown"),
            job.get("company", "No company"),
            job.get("jobType", "Job type unknown"),
            job.get("jobDetailUrl", "No link")
        ])


print("Search complete. Results saved in: job_results.csv")