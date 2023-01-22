from bs4 import BeautifulSoup


def parse(data):
    """
    Parse webpage content and return values of
    tags <h1> and <title>, and value of attribute
    content of tag <meta name="description" content="...">
    :param data: html text
    :return: h1, title, description
    """
    soup = BeautifulSoup(data, 'html.parser')
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    if soup.find('meta', {'name': 'description'}):
        description = soup.find('meta', {'name': 'description'})['content']
        if len(description) > 255:
            description = f'{description[:252]}...'
    else:
        description = ''
    return h1, title, description
