import re

import config

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {"User-Agent": f"JarvisCollegeProject/1.0 (student project; {config.CONTACT_MAIL})"}
WIKI_API = "https://en.wikipedia.org/w/api.php"
STOPWORDS = {"a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on",
             "for", "and", "or", "what", "who", "how", "why", "when", "where",
             "do", "does", "i", "me", "my", "you", "can"}
SKIP_PHRASES = ["co-authored", "fact checked", "last updated", "cookie", "subscribe", 
                "sign up", "all rights reserved", "copyright", "advertisement"]



def wikipedia(topic):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": topic,
        "gsrlimit": 1,
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
    }
    try:
        response = requests.get(WIKI_API, params = params, headers = HEADERS, timeout = 8)
    except requests.RequestException as error:
        print(f"Wikipedia error: {error}")
        return None
    if response.status_code != 200:
        print(f"Wikipedia returned status {response.status_code}")
        return None

    pages = response.json().get("query", {}).get("pages", {})
    for page in pages.values():
        return page.get("extract") or None
    return None


def search_web(query, count = 5):
    try:
        return DDGS().text(query, max_results = count)
    except Exception as error:
        print(f"Search error: {error}")
        return []


def read_page(url):
    try:
        response = requests.get(url, headers = HEADERS, timeout = 8)
        response.raise_for_status()
    except requests.RequestException:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "aside", "sup"]):
        tag.decompose()

    blocks = []
    for tag in soup.find_all(["p", "li"]):
        block = tag.get_text(" ", strip = True)
        if len(block) < 40:
            continue
        if block[-1] not in '.!?':
            block += '.'
        blocks.append(block)
    return " ".join(blocks)


def important_words(text):
    return {word for word in re.findall(r"\w+", text.lower()) if word not in STOPWORDS}


def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


def best_sentences(text, question, count = 3):
    question_words = important_words(question)
    page_words = set(re.findall(r"\w+", text.lower()))
    if not question_words <= page_words:
        return ""
    
    scored = []
    for position, sentence in enumerate(split_sentences(text)):
        if not 40 <= len(sentence) <= 300:
            continue
        if any(phrase in sentence.lower() for phrase in SKIP_PHRASES):
            continue
        overlap = len(question_words & important_words(sentence))
        if overlap > 0:
            scored.append((overlap, position, sentence))
    scored.sort(key = lambda item: item[0], reverse = True)
    top = sorted(scored[:count], key = lambda item: item[1])
    return " ".join(sentence for overlap, position, sentence in top)    


if __name__ == "__main__":
    print(wikipedia('lando norris'))
    for result in search_web("python list reverse"):
        print(result["title"], result['href'])


