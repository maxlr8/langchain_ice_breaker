# pylint: disable-all

import os
import requests

from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str):

    """Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn Profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": "Bearer " + os.environ["PROXYCURL_API"]}
    params = {"linkedin_profile_url": linkedin_profile_url}
    response = requests.get(api_endpoint, params=params, headers=headers)

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("grouops"):
            group_dict.pop("profile_pic_url")

    return data
