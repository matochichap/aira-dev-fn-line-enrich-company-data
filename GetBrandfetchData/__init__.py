import json
import azure.functions as func
from GetBrandfetchData.ScrapeBrandfetchWebsite import scrape_brandfetch


def main(request: func.HttpRequest):
    url = request.params.get("url")
    if request.method == "GET":
        logo_url, social_links = scrape_brandfetch(url)
        response = {
            "logo_url": logo_url,
            "social_links": social_links
        }
        return func.HttpResponse(json.dumps(response))
