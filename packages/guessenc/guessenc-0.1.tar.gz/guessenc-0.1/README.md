# guessenc

Infer HTML encoding from response headers &amp; content.  Goes above and beyond the encoding detection done by most HTTP client libraries.

## Basic Usage

The main function exported by `guessenc` is `infer_encoding()`.

```python
>>> import requests
>>> from guessenc import infer_encoding

>>> resp = requests.get("http://www.fatehwatan.ps/page-183525.html")
>>> resp.raise_for_status()
>>> infer_encoding(resp.content, resp.headers)
(<Source.META_HTTP_EQUIV: 2>, 'cp1256')
```

This tells us that the detected encoding is cp1256, and that it was retrieved from a <meta> HTML tag with ``http-equiv='Content-Type'``.

Detail on the signature of `infer_encoding()`:

```python
def infer_encoding(
    content: Optional[bytes] = None,
    headers: Optional[Mapping[str, str]] = None
) -> Pair:
    ...
```

The `content` represents the page HTML, such as `response.content`.

The `headers` represents the HTTP response headers, such as `response.headers`.
If provided, this should be a data structure supporting a case-insensitive lookup, such as `requests.structures.CaseInsensitiveDict`
or `multidict.CIMultiDict`.

Both parameters are optional.

The return type is a `tuple`.

The first element of the tuple is a member of the `Source` enum (see [Search Process](#search-process) below).  The source indicates where
the detected encoding comes from.

The second element of the tuple is either a `str`, which is the canonical name of the detected encoding, or `None` if no encoding is found.

## Where Do Other Libraries Fall Short?

The `requests` library "[follows] RFC 2616 to the letter" in using the HTTP headers to determine the encoding of the response content.  This
means, among other things, using `ISO-8859-1` as a fallback if no charset is given, despite the fact that UTF-8 has [absolutely
dwarfed](https://en.wikipedia.org/wiki/UTF-8#/media/File:Utf8webgrowth.svg) all other encodings in usage on web pages.

```python
# requests/adapters.py
response.encoding = get_encoding_from_headers(response.headers)
```

If `requests` does not find an HTTP `Content-Type` header at all, it will fall back to detection via `chardet` rather than looking in the
HTML tags for meaningful information.  There's nothing at all _wrong_ with this; it just means that the `requests` maintainers have chosen to
focus on the power of `requests` [as an HTTP library, not an HTML library](https://github.com/psf/requests/issues/2266).  If you want more fine-grained control over encoding detection,
try `infer_encoding()`.

This is not to single out `requests` either; there are other libraries that do the same dance with encoding detection;
[`aiohttp`](https://github.com/aio-libs/aiohttp/blob/master/aiohttp/client_reqrep.py) checks the `Content-Type` header, or otherwise
defaults to UTF-8 without looking anywhere else.

## Search Process

The function `guessenc.infer_encoding()` looks in a handful of places to extract an encoding, in this order, and stops when it finds one:

1. In the `charset` value from the [`Content-Type` HTTP entity header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type).
2. In the `charset` value from a `<meta charset="xxxx">` HTML tag.
3. In the `charset` value from a `<meta>` tag with `http-equiv="Content-Type"`.
4. Using the [`chardet`](https://chardet.readthedocs.io/en/latest/) library.

Each of the above "sources" is signified by a corresponding member of the `Source` enum:

```python
class Source(enum.Enum):
    """Indicates where our detected encoding came from."""

    CHARSET_HEADER = 0
    META_CHARSET = 1
    META_HTTP_EQUIV = 2
    CHARDET = 3
    COULD_NOT_DETECT = 4
```

If none of the 4 sources from the list above return a viable encoding, this is indicated by `Source.COULD_NOT_DETECT`.
