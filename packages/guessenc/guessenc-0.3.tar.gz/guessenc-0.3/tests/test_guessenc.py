import bz2
import codecs
import json
import re
import unicodedata
import os.path

import pytest
from requests.structures import CaseInsensitiveDict

from guessenc import infer_encoding, Pair, Source

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
assert os.path.exists(DATA_DIR), "Data directory not found"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


data = [
    (
        "http://cen.ce.cn/more/201909/23/t20190923_33202170.shtml",
        (Source.META_CHARSET, codecs.lookup("gb2312").name),
        (Source.COULD_NOT_DETECT, None),
        (Source.META_CHARSET, codecs.lookup("gb2312").name),
    ),
    (
        "http://www.arirang.com/news/News_View.asp?nseq=244581",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://www.nytimes.com/2019/09/23/us/politics/trump-un-biden-ukraine.html",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://www.currenttime.tv/a/semsorok-irrational/30180436.html",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "http://www.xinhuanet.com/politics/70zn/fbh2/index.htm",
        (Source.META_HTTP_EQUIV, codecs.lookup("utf-8").name),
        (Source.COULD_NOT_DETECT, None),
        (Source.META_HTTP_EQUIV, codecs.lookup("utf-8").name),
    ),
    (
        "http://www.sanaanews.net/news-66176.htm",
        (Source.META_HTTP_EQUIV, codecs.lookup("cp1256").name),
        (Source.COULD_NOT_DETECT, None),
        (Source.META_HTTP_EQUIV, codecs.lookup("cp1256").name),
    ),
    (
        "http://alfajertv.com/news/4037470.html",
        (Source.META_HTTP_EQUIV, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://www.presstv.com/Detail/2019/09/23/606960/Rouhani-newyork-hope-initiative-hormuz-peace",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://www.dap-news.com/archives/70763 ",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "http://www.fatehwatan.ps/page-183525.html",
        (Source.META_HTTP_EQUIV, codecs.lookup("windows-1256").name),
        (Source.COULD_NOT_DETECT, None),
        (Source.META_HTTP_EQUIV, codecs.lookup("windows-1256").name),
    ),
    (
        "https://klse.i3investor.com/blogs/kianweiaritcles/211663.jsp",
        (Source.META_HTTP_EQUIV, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://www.theguardian.com/society/2018/dec/25/"
        "doubletree-steps-in-after-hotel-cancels-booking-for-homeless-people",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "http://koreabizwire.com/bts-goes-beyond-barriers-through-web-based-content/139261",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "http://www.ashburtononline.co.nz/site/news/news-headlines/"
        "us-china-trade-war-officials-to-resume-talks-before-g20.html",
        (Source.META_HTTP_EQUIV, codecs.lookup("iso-8859-1").name),
        (Source.COULD_NOT_DETECT, None),
        (Source.META_HTTP_EQUIV, codecs.lookup("iso-8859-1").name),
    ),
    (
        "https://www.aljazeera.net/news/politics/2019/9/23/"
        "%D9%87%D8%AC%D9%88%D9%85-%D8%A3%D8%B1%D8%A7%D9%85%D9%83%D9%88-"
        "%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D8%A8%D9%8A%D8%A7%D9%86-%D8%AB%D9%84%D8%A7%D8%AB%D9%8A",
        (Source.META_CHARSET, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
    (
        "https://api.gdeltproject.org/api/v2/doc/doc?mode=artList&format=JSON&maxrecords=10&query=Litvinenko",
        (Source.COULD_NOT_DETECT, None),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
        (Source.CHARSET_HEADER, codecs.lookup("utf-8").name),
    ),
]


@pytest.mark.parametrize("url,with_content_only,with_headers_only,with_content_and_headers", data)
def test_infer_encoding(url: str, with_content_only: Pair, with_headers_only: Pair, with_content_and_headers: Pair):
    slug = slugify(url)
    html_fp = os.path.join(DATA_DIR, "html", slug + ".bz2")
    headers_fp = os.path.join(DATA_DIR, "headers", slug)

    content = bz2.decompress(open(html_fp, "rb").read())
    with open(headers_fp) as f:
        headers = CaseInsensitiveDict(json.load(f))

    assert infer_encoding(content=content, headers=None) == with_content_only
    assert infer_encoding(content=None, headers=headers) == with_headers_only
    assert infer_encoding(content=content, headers=headers) == with_content_and_headers
