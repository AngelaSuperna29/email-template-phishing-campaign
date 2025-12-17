import requests
from bs4 import BeautifulSoup
from mistral_client import call_mistral

def infer_industry(company: str, url: str) -> str:
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return "Corporate"

        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = " ".join(soup.get_text().split())[:2000]

        prompt = f"""
Identify the company's primary industry.

Company: {company}
Website content:
{text}

Rules:
- Return ONLY industry name
- 1 or 2 words
- No explanation
"""

        return call_mistral(prompt).strip()

    except Exception:
        return "Corporate"
