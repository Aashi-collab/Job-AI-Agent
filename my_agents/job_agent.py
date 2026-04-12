from tools.scraper import scrape_jobs


def job_agent(user_profile):

    role = user_profile.get("role", "data scientist")

    try:
        jobs = scrape_jobs(role)

        if not jobs:
            return [{"title": "No jobs found", "company": "N/A"}]

        return jobs

    except Exception as e:
        print("Job agent error:", e)

        return [{
            "title": "Error fetching jobs",
            "company": "System"
        }]