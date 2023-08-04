from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import logging


def scrape_brandfetch(company_url):
    """
    :param company_url: company url
    :return: [logo_url, social_links]
    """
    company_url = extract_domain(company_url)
    logging.info(f"url:{company_url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(f"https://brandfetch.com/{company_url}", headers=headers)
    web_page = response.text

    soup = BeautifulSoup(web_page, "html.parser")
    try:
        logo_url = soup.find(class_="sc-b83fdfed-3").find("img").get("src")  # get logo url
    except AttributeError:
        logo_url = ""
    try:
        all_social_icons = soup.find(class_="sc-638294dd-0").find_all("a")  # get social icons
        social_links = {icon.find("span").find("svg").get("data-icon"): icon.get("href") for icon in all_social_icons}
    except AttributeError:
        social_links = []
    return [logo_url, social_links]


def get_between(s, start, end):
    start_index = s.find(start) + len(start)
    end_index = s.find(end, start_index)
    return s[start_index:end_index]


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain
