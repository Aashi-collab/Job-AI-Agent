import requests
from bs4 import BeautifulSoup


def scrape_jobs(role="data scientist"):
    url = f"https://internshala.com/jobs/{role.replace(' ', '-')}-jobs/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    cards = soup.find_all("div", class_="individual_internship")[:5]

    for card in cards:
        title = card.find("a", class_="job-title-href")

        company = card.find("p", class_="company-name")

        if title and company:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip()
            })

    return jobs