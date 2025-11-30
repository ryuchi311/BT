from urllib.parse import urljoin, urlparse
import requests
import re
import sys
import json


def _ensure_scheme(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


def _find_icon_link(html: str, base_url: str):
    # Look for typical link rel icon patterns
    patterns = [
        r'<link[^>]+rel=["\'](?:shortcut icon|icon|apple-touch-icon)["\'][^>]*href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\'](?:shortcut icon|icon|apple-touch-icon)["\']'
    ]
    for pat in patterns:
        m = re.search(pat, html, flags=re.I)
        if m:
            return urljoin(base_url, m.group(1))

    # Try open graph image as fallback
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, flags=re.I)
    if m:
        return urljoin(base_url, m.group(1))

    # No icon found
    return None


def _find_title(html: str):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, flags=re.I | re.S)
    if m:
        return m.group(1).strip()
    return None


def get_icon_and_domain(url: str, timeout: int = 10):
    """Fetch the page, return a dict with `domain`, `icon_url`, and `title`.

    Strategy:
    - Ensure scheme present
    - GET page HTML
    - Search for <link rel="icon"> variants and og:image
    - Fallback to /favicon.ico
    - Return domain (netloc from URL), icon_url (absolute), and title (if found)
    """
    try:
        orig = url.strip()
        base = _ensure_scheme(orig)
        parsed = urlparse(base)
        domain = parsed.netloc

        resp = requests.get(base, timeout=timeout, headers={
            'User-Agent': 'site-icon-fetcher/1.0'
        })
        resp.raise_for_status()
        html = resp.text

        icon = _find_icon_link(html, resp.url)
        title = _find_title(html)

        if not icon:
            # Try the conventional location
            icon_candidate = urljoin(resp.url, '/favicon.ico')
            # quick HEAD to see if it exists
            try:
                h = requests.head(icon_candidate, timeout=timeout, headers={'User-Agent': 'site-icon-fetcher/1.0'})
                if h.status_code == 200 and int(h.headers.get('Content-Length', '0')) != 0:
                    icon = icon_candidate
            except Exception:
                # ignore and leave icon as None
                icon = None

        return {
            'domain': domain,
            'icon_url': icon,
            'title': title
        }

    except Exception as e:
        return {
            'error': str(e)
        }


def _cli():
    if len(sys.argv) < 2:
        print('Usage: python scripts/get_website_icon.py <website-url-or-domain>')
        sys.exit(1)

    url = sys.argv[1]
    out = get_icon_and_domain(url)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    _cli()
