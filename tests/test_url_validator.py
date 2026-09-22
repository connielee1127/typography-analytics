from src.url_validator import normalize_url, classify_website
import pytest
from unittest.mock import Mock


### Normalization Tests ###

def test_url_normalization_adds_https():
    assert normalize_url("example.com") == "https://example.com"

def test_url_normalization_none():
    assert normalize_url(None) == None

def test_url_normalization_blank():
    assert normalize_url("") == None

def test_url_normalization_bad_scheme():
    assert normalize_url("ftp://example.com") == None

def test_url_normalization_wspace():
    assert normalize_url("  example.com ") == "https://example.com"

def test_url_preserves_https():
    assert normalize_url("https://example.com") == "https://example.com"

def tes_url_preserves_http():
    assert normalize_url("http://example.com") == "http://example.com"


### Classification Tests ###

@pytest.fixture
def mock_response():
    response = Mock()
    response.url = "https://example.com"
    response.text = "<html></html>"
    return response

def test_classify_company_website(mock_response):
    assert classify_website(mock_response) == "company_website"

def test_classify_social_media_website(mock_response):
    mock_response.url = "https://facebook.com/example"
    assert classify_website(mock_response) == "social_media"

def test_classify_directory_website(mock_response):
    mock_response.url = "https://yelp.com/example"
    assert classify_website(mock_response) == "directory"

def test_classify_url_shortener_website(mock_response):
    mock_response.url = "https://bit.ly/example"
    assert classify_website(mock_response) == "url_shortener"


def test_classify_domain_for_sale(mock_response):
    mock_response.text = "domain for sale."
    assert classify_website(mock_response) == "domain_for_sale"

def test_classify_parked_domain(mock_response):
    mock_response.text = "This domain is parked."
    assert classify_website(mock_response) == "parked_domain"



 
