#!/usr/bin/env python3
"""
set_all_category_images.py

Real website images (Openverse - free, no API key needed) ah fetch pannitu,
duplicate images varama dedupe pannitu, ovvoru category ku unique image assign pannum.

Run:
    python set_all_category_images.py
    (or) python set_all_category_images.py --dry-run   # just print, don't touch DB
"""

import subprocess
import sys
import time
import requests

OPENVERSE_SEARCH_URL = "https://api.openverse.org/v1/images/"

# category -> search query (thematic keyword for better image match)
CATEGORY_QUERIES = {
    "Classic Fiction": "classic literature books",
    "Gothic Fiction / Horror": "gothic horror old castle",
    "Mystery / Detective": "detective noir mystery",
    "Adventure": "adventure exploration mountains",
    "Romance": "romance couple sunset",
    "Fantasy": "fantasy magic castle",
    "Fairy Tales": "fairy tale storybook illustration",
    "Drama / Plays": "theatre stage drama",
    "Comedy": "comedy theatre masks",
    "Historical Fiction": "historical vintage era",
    "Biographical / Autobiographical Fiction": "old portrait biography",
    "Psychological Fiction": "psychology mind abstract",
    "Non-Fiction": "library reading nonfiction",
    "Political Science / Philosophy": "philosophy books government",
    "Feminist Fiction": "women empowerment portrait",
    "Bildungsroman (Coming-of-age)": "coming of age youth journey",
    "Epistolary Fiction": "old letters handwriting",
    "Short Story": "short story collection books",
}

used_urls = set()


def fetch_image_url(query, retries=3):
    """Fetch one real, unused image URL from Openverse for a given query."""
    params = {
        "q": query,
        "license_type": "commercial,modification",  # safely reusable images
        "page_size": 10,
        "orientation": "landscape",
    }
    for attempt in range(retries):
        try:
            resp = requests.get(OPENVERSE_SEARCH_URL, params=params, timeout=10)
            resp.raise_for_status()
            results = resp.json().get("results", [])
            for item in results:
                url = item.get("url")
                if url and url not in used_urls:
                    used_urls.add(url)
                    return url
        except requests.RequestException as e:
            print(f"  ! attempt {attempt+1} failed: {e}")
            time.sleep(1)
    return None


def main():
    dry_run = "--dry-run" in sys.argv

    for category, query in CATEGORY_QUERIES.items():
        print(f"Processing: {category}  (query: '{query}')")
        url = fetch_image_url(query)

        if not url:
            print(f"  ! No unique image found for '{category}', skipping.")
            print("---")
            continue

        print(f"  -> {url}")

        if not dry_run:
            result = subprocess.run(
                ["python", "manage.py", "set_category_image", category, url],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"  ! Command failed: {result.stderr.strip()}")
            else:
                print(f"  ✓ {result.stdout.strip()}")

        print("---")
        time.sleep(0.5)  # be nice to the API


if __name__ == "__main__":
    main()
