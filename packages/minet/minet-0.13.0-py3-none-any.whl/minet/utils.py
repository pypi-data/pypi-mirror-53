# =============================================================================
# Minet Utils
# =============================================================================
#
# Miscellaneous helper function used throughout the library.
#
import re
import chardet
import cgi
import certifi
import browser_cookie3
import urllib3
import time
from collections import OrderedDict
from ural import is_url
from urllib.parse import urljoin
from urllib3 import HTTPResponse
from urllib3.exceptions import ClosedPoolError, HTTPError
from urllib.request import Request

from minet.exceptions import (
    MaxRedirectsError,
    InfiniteRedirectsError,
    InvalidRedirectError,
    InvalidURLError,
    SelfRedirectError
)

from minet.defaults import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_SPOOFED_UA
)

# Handy regexes
CHARSET_RE = re.compile(rb'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
PRAGMA_RE = re.compile(rb'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
XML_RE = re.compile(rb'^<\?xml.*?encoding=["\']*(.+?)["\'>]', flags=re.I)
NOSCRIPT_RE = re.compile(rb'<noscript[^>]*>.*</noscript[^>]*>', flags=re.I)
META_REFRESH_RE = re.compile(rb'''<meta\s+http-equiv=['"]?refresh['"]?\s+content=['"]?([^"']+)['">]?''', flags=re.I)

# Constants
CHARDET_CONFIDENCE_THRESHOLD = 0.9
REDIRECT_STATUSES = set(HTTPResponse.REDIRECT_STATUSES)


def guess_response_encoding(response, data, is_xml=False, use_chardet=False):
    """
    Function taking an urllib3 response object and attempting to guess its
    encoding.
    """
    content_type_header = response.getheader('content-type')

    if content_type_header is not None:
        parsed_header = cgi.parse_header(content_type_header)

        if len(parsed_header) > 1:
            charset = parsed_header[1].get('charset')

            if charset is not None:
                return charset.lower()

    # TODO: use re.search to go faster!
    if is_xml:
        matches = re.findall(CHARSET_RE, data)

        if len(matches) == 0:
            matches = re.findall(PRAGMA_RE, data)

        if len(matches) == 0:
            matches = re.findall(XML_RE, data)

        # NOTE: here we are returning the last one, but we could also use
        # frequency at the expense of performance
        if len(matches) != 0:
            return matches[-1].lower().decode()

    if use_chardet:
        chardet_result = chardet.detect(data)

        if chardet_result['confidence'] >= CHARDET_CONFIDENCE_THRESHOLD:
            return chardet_result['encoding'].lower()

    return None


def parse_http_header(header):
    key, value = header.split(':', 1)

    return key.strip(), value.strip()


# TODO: take more cases into account...
#   http://www.otsukare.info/2015/03/26/refresh-http-header
def parse_http_refresh(value):
    try:

        if isinstance(value, bytes):
            value = value.decode()

        duration, url = value.strip().split(';', 1)

        if not url.lower().startswith('url='):
            return None

        return int(duration), str(url.split('=', 1)[1])
    except:
        return None


def find_meta_refresh(html_chunk):
    m = META_REFRESH_RE.search(html_chunk)

    if not m:
        return None

    return parse_http_refresh(m.group(1))


class CookieResolver(object):
    def __init__(self, jar):
        self.jar = jar

    def __call__(self, url):
        req = Request(url)
        self.jar.add_cookie_header(req)

        return req.get_header('Cookie') or None


def grab_cookies(browser='firefox'):
    if browser == 'firefox':
        try:
            return CookieResolver(browser_cookie3.firefox())
        except:
            return None

    if browser == 'chrome':
        try:
            return CookieResolver(browser_cookie3.chrome())
        except:
            return None

    raise Exception('minet.utils.grab_cookies: unknown "%s" browser.' % browser)


def dict_to_cookie_string(d):
    return '; '.join('%s=%s' % r for r in d.items())


DEFAULT_URLLIB3_TIMEOUT = urllib3.Timeout(connect=DEFAULT_CONNECT_TIMEOUT, read=DEFAULT_READ_TIMEOUT)


def create_safe_pool(timeout=None, **kwargs):
    """
    Helper function returning a urllib3 pool manager with sane defaults.
    """

    timeout = kwargs['timeout'] if 'timeout' in kwargs else DEFAULT_URLLIB3_TIMEOUT

    return urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
        timeout=timeout,
        **kwargs
    )


def request(http, url, method='GET', headers=None, cookie=None, spoof_ua=True,
            headers_only=False, redirect=None, stream=False):
    """
    Generic request helpers using a urllib3 pool to access some resource.
    """

    # Validating URL
    if not is_url(url):
        return InvalidURLError('Invalid URL'), None

    # Formatting headers
    final_headers = {}

    if spoof_ua:
        final_headers['User-Agent'] = DEFAULT_SPOOFED_UA

    if cookie:
        if not isinstance(cookie, str):
            cookie = dict_to_cookie_string(cookie)

        final_headers['Cookie'] = cookie

    # Note: headers passed explicitly by users always win
    if headers is not None:
        final_headers.update(headers)

    # Performing request
    try:
        response = http.request(
            method,
            url,
            headers=final_headers,
            preload_content=True if not headers_only and not stream else False,
            release_conn=True if not stream else False,
            redirect=redirect
        )
    except (ClosedPoolError, HTTPError) as e:
        return e, None

    return None, response


# TODO: refresh header + meta refresh
def resolve(http, url, max=5, follow_refresh_headers=True):
    """
    Helper function attempting to resolve the given url.
    """
    url_stack = OrderedDict()

    for _ in range(max):
        error, response = request(
            http,
            url,
            method='HEAD',
            redirect=False,
            headers_only=True,
            spoof_ua=False
        )

        if error:
            url_stack[url] = (None, url)
            return error, list(url_stack.values())

        if url in url_stack:
            return InfiniteRedirectsError('Infinite redirects'), list(url_stack.values())

        url_stack[url] = (response.status, url)
        location = None

        if response.status not in REDIRECT_STATUSES:

            if response.status < 400 and follow_refresh_headers:
                refresh = response.getheader('refresh')

                if refresh is not None:
                    _, location = parse_http_refresh(refresh)

            if location is None:
                return None, list(url_stack.values())
        else:
            location = response.getheader('location')

        if not location:
            return InvalidRedirectError('Redirection is invalid'), list(url_stack.values())

        # Go to next
        next_url = urljoin(url, location.strip())

        # Self loop?
        if next_url == url:
            return SelfRedirectError('Self redirection'), list(url_stack.values())

        url = next_url

    return MaxRedirectsError('Maximum number of redirects exceeded'), list(url_stack.values())


class RateLimiter(object):
    """
    Naive rate limiter context manager with smooth output ().

    Note that it won't work in a multi-threaded environment.

    Args:
        max_per_period (int): Maximum number of calls per period.
        period (float): Duration of a period in seconds. Defaults to 1.0.

    """

    def __init__(self, max_per_period, period=1.0, with_budget=False):
        max_per_second = max_per_period / period
        self.min_interval = 1.0 / max_per_second
        self.max_budget = period / 4
        self.budget = 0.0
        self.last_entry = None
        self.with_budget = with_budget

    def __enter__(self):
        self.last_entry = time.perf_counter()

    def exit_with_budget(self):
        running_time = time.perf_counter() - self.last_entry

        delta = self.min_interval - running_time

        # Consuming budget
        if delta >= self.budget:
            delta -= self.budget
            self.budget = 0
        else:
            self.budget -= delta
            delta = 0

        # Do we need to sleep?
        if delta > 0:
            time.sleep(delta)
        elif delta < 0:
            self.budget -= delta

        # Clamping budget
        # TODO: this should be improved by a circular buffer of last calls
        self.budget = min(self.budget, self.max_budget)

    def exit(self):
        running_time = time.perf_counter() - self.last_entry

        delta = self.min_interval - running_time

        if delta > 0:
            time.sleep(delta)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.with_budget:
            return self.exit_with_budget()

        return self.exit()
