from validators import url as validate
from urllib.parse import urlparse


def get_domain(url):
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


def is_valid(raw_url):
    """
    Check URL if it's correct (using validators.url),
    not empty and not more than 255 characters
    :param raw_url: URL
    :return: List of errors
    """
    err_list = []
    url = get_domain(raw_url)
    if not raw_url:
        err_list.append('URL обязателен')
    if not validate(raw_url):
        err_list.append('Некорректный URL')
    if len(url) > 255:
        err_list.append('URL превышает 255 символов')
    return err_list
