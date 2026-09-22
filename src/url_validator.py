import pandas as pd
import requests
from urllib.parse import urlparse 


def normalize_url(url):
    """
    Convert a raw URL into a consistent format.
    """
    # check for null values
    if pd.isna(url) or url is None:
        return None

    # convert to string and remove whitespace
    url = str(url.strip())
    if not url:
        return None

    # add https if missing; reject non-http/https schemes
    if "://" in url:
        scheme = url.split("://", 1)[0].lower()

        if scheme not in {"http", "https"}:
            return None
        
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    return url



def check_url_reachability(url):
    """
    Check whether the normalized URL returns usable HTML.
    """
    result = {
        "accessible": False,
        "http_status": None,
        "final_url": None,
        "content_type": None,
        "failure_reason": None,
        "website_type": None
    }
    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )
    
        result["http_status"] = response.status_code
        result["final_url"] = response.url
        result["content_type"] = response.headers.get("Content-Type", "")

        if not 200 <= response.status_code < 300:
            result["failure_reason"] = "http_error"
            return result
        
        if "text/html" not in result["content_type"].lower():
            result["failure_reason"] = "non_html_content"
            return result
        
        result["accessible"] = True
        result["website_type"] = classify_website(response)

        return result
  
    except requests.exceptions.Timeout:
        result["failure_reason"] = "timeout"
        return result
    except requests.exceptions.ConnectionError:
        result["failure_reason"] = "connection_error"
        return result
    except requests.exceptions.TooManyRedirects:
        result["failure_reason"] = "too_many_redirects"
        return result
    except requests.exceptions.SSLError:
        result["failure_reason"] = "ssl_error"
        return result
    except requests.exceptions.RequestException:
        result["failure_reason"] = "request_error"
        return result



def classify_website(response):
    """
    Determine whether the page is a company website,
    social media page, directory listing, etc.
    """
    domain = urlparse(response.url).hostname
    
    social_media_domains = {
        "facebook.com",
        "instagram.com",
        "linkedin.com",
        "twitter.com",
        "x.com",
        "tiktok.com",
        "youtube.com",
    }

    directory_domains = {
        "yelp.com",
        "yellowpages.com",
        "bbb.org",
        "mapquest.com",
    }

    url_shortener_domains = {
        "bit.ly",
        "t.co",
        "tinyurl.com",
    }

    if domain in social_media_domains:
        return "social_media"
    if domain in directory_domains:
        return "directory"
    if domain in url_shortener_domains:
        return "url_shortener"
    
    page_text = response.text.lower()
    
    if "domain for sale" in page_text:
        return "domain_for_sale"

    if "domain is parked" in page_text:
        return "parked_domain"
        
    return "company_website"




def validate_website(url):
    """
    Run the URL-validation pipeline and return
    a structured result.
    """
    normalized_url = normalize_url(url)
    result = check_url_reachability(normalized_url)

    return result