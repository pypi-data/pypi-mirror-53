#!/usr/bin/env python3

import argparse
import json
import urllib.parse

import requests

from tests.test_guessenc import slugify

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
}


def download(url):
    slug = slugify(url)
    headers = HEADERS.copy()
    headers["Host"] = urllib.parse.urlparse(url).netloc
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    with open(f"data/html/{slug}", "wb") as f:
        f.write(resp.content)
    with open(f"data/headers/{slug}", "w") as f:
        json.dump(dict(resp.headers), f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="+", help="URL string")
    args = parser.parse_args()
    for u in args.url:
        print("Downloading", u)
        download(u)
        print("...Done")
