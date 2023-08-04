from bs4 import BeautifulSoup
import requests


def scrape_jobsdb():
    """
    Able to scrape all jobs from side panel, but info is not as detailed
    """
    result = []
    t = []
    for page in range(1, 10):
        print(page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        jobsdb_url = f"https://th.jobsdb.com/th/en/Search/FindJobs?JSRV=1&page={page}"
        response = requests.get(jobsdb_url, headers=headers)
        web_page = response.text
        soup = BeautifulSoup(web_page, "html.parser")

        res = soup.find_all('div', attrs={'data-search-sol-meta': True})
        for r in res:
            try:
                company_url = r.find(
                    class_="z1s6m00 _1hbhsw67i _1hbhsw66e _1hbhsw69q _1hbhsw68m _1hbhsw6n _1hbhsw65a _1hbhsw6ga _1hbhsw6fy") \
                    .find('div', attrs={"data-automation": "job-card-logo"}) \
                    .find('img') \
                    .get("src")
            except AttributeError:
                company_url = ""
            job_title = r.find(
                class_="z1s6m00 _1hbhsw67i _1hbhsw66e _1hbhsw69q _1hbhsw68m _1hbhsw6n _1hbhsw65a _1hbhsw6ga _1hbhsw6fy") \
                .find('h1', class_="z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ii") \
                .text
            result.append(job_title)
            t.append(company_url)
    print(result)
    print(len(result))
    print(t)
    print(len(t))
    fail = 0
    for url in t:
        if not url:
            fail += 1
    print(fail)


scrape_jobsdb()
