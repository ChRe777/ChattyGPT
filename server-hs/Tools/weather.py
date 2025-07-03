# -----------------------------------------------------------------------------

from bs4 import BeautifulSoup
def _extract_visible_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    organic_items = soup.find_all('li', attrs={'data-layout': 'organic'})

    texts = ""
    for item in organic_items:
        texts += item.text

    return texts

from urllib.parse import urlencode
from playwright.sync_api import sync_playwright
def _get_content(query):

    base_url = "https://duckduckgo.com/"
    params = {"q": query,
        "ia": "web",
        "t":"h_"
    }

    # Encode parameters
    query_string = urlencode(params)

    # Join base URL with encoded query string
    full_url = f"{base_url}?{query_string}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                viewport={"width": 1280, "height": 800})

        page.goto(full_url, wait_until="networkidle", timeout=10000)

        # Alternatively: wait for a specific element to be visible (recommended)
        # page.wait_for_selector("div")
        # page.wait_for_selector("div#z2", timeout=10000)

        text = page.content()
        browser.close()

        return text

def _search_ddg_web(query):
    text = _extract_visible_text(_get_content(query))
    return text[100:MAX_CHARS+100]

_parameters = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
    },
    "required": ["query"]
}

# -----------------------------------------------------------------------------

from haystack.tools import Tool

MAX_CHARS = 500

weather_tool = Tool(name="weather_tool",
            description="This tool search for weather",
            parameters=_parameters,
            function=_search_ddg_web)

#search_ddg_web(query="Wetter in Berlin")
#

__all__ = ['weather_tool']
