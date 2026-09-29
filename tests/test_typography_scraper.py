import pytest
from src.typography_scraper import load_page

@pytest.mark.asyncio
async def test_load_page():
    result = await load_page("https://www.wikipedia.org/")

    print(result)

    assert result["scrape_status"] == "success"
    assert result["font_family"] is not None
    assert result["font_size"] is not None
    assert result["font_weight"] is not None
    assert result["line_height"] is not None