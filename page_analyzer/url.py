from validators import url as validate
from urllib.parse import urlparse
from flask import flash


def get_domain(url):
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


def valid_url(raw_url):
    """
    Check URL if it's correct (using validators.url),
    not empty and not more than 255 characters
    :param raw_url: URL
    :return: True or False
    """
    result = True
    url = get_domain(raw_url)
    if not raw_url:
        flash('URL обязателен', 'alert-danger')
        result = False
    if not validate(raw_url):
        flash('Некорректный URL', 'alert-danger')
        result = False
    if len(url) > 255:
        flash('URL превышает 255 символов', 'alert-danger')
        result = False
    return result
