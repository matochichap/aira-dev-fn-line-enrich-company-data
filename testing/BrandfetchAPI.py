import json
import os
import requests
from urllib.parse import urlparse

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
BRANDFETCH_ENDPOINT = "https://api.brandfetch.io/v2/brands/"


def update_logos():
    """
    Get company information from Brandfetch API.
    Not using since we can scrape directly from website, but there may be other useful info that we can use.
    Needs subscription.
    """
    def extract_domain(link):
        parsed_link = urlparse(link)
        domain = parsed_link.netloc
        if domain.startswith("www."):
            domain = domain[4:]  # Remove the 'www' prefix
        return domain

    def get_brand_info(url):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        response = requests.get(url, headers=headers).json()
        return response

    with open("../data/raw_data.json", "r") as f:
        raw_data = json.load(f)

    with open("../data/logos.json", "r") as f:
        logos = json.load(f)

    for data in raw_data:
        data = json.loads(data)
        company_url = data.get("company_details", {}).get("company_url", None)
        company_domain = extract_domain(company_url)
        if company_domain and company_domain not in logos:
            endpoint = f"{BRANDFETCH_ENDPOINT}{company_domain}"
            json_response = get_brand_info(endpoint)
            domain = json_response.get("domain")
            if domain:
                with open("../data/logos.json", "w") as f:
                    logos[domain] = json_response
                    json.dump(logos, f)


# update_logos()
# with open("data/raw_data.json", "r") as f:
#     raw_data = json.load(f)
#     print(raw_data)
