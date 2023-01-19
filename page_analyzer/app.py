from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    flash,
    get_flashed_messages
)
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from validators import url as validate
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_domain(url):
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


def parse(data):
    """
    Parse webpage content and return values of
    tags <h1> and <title>, and value of attribute
    content of tag <meta name="description" content="...">
    :param data: html text
    :return: h1, title, description
    """
    soup = BeautifulSoup(data, 'html.parser')
    if soup.h1:
        h1 = soup.h1.text
    else:
        h1 = ''
    if soup.title:
        title = soup.title.text
    else:
        title = ''
    if soup.find('meta', {'name': 'description'}):
        description = soup.find('meta', {'name': 'description'})['content']
        if len(description) > 255:
            description = f'{description[:252]}...'
    else:
        description = ''
    return h1, title, description


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("""SELECT
                                urls.id, urls.name,
                                url_checks.status_code,
                                url_checks.created_at
                                FROM urls LEFT JOIN url_checks
                                ON urls.id = url_checks.url_id
                                AND url_checks.created_at = (SELECT
                                MAX(created_at) FROM url_checks
                                WHERE url_id = urls.id)
                                ORDER BY urls.id;""")
            urls = curs.fetchall()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    raw_url = request.form.get('url')
    if not validate(raw_url) or len(raw_url) > 255:
        flash('Некорректный URL', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html', messages=messages, url=raw_url), 422
    try:
        with conn:
            with conn.cursor() as curs:
                url = get_domain(raw_url)
                curs.execute(
                    """
                    INSERT INTO urls (name, created_at)
                    VALUES (%(name)s, %(created_at)s)
                    RETURNING id;
                    """,
                    {'name': url, 'created_at': datetime.now()})
                id = curs.fetchone()[0]
                flash('Страница успешно добавлена', 'alert-success')
                return redirect(url_for('get_url', id=id))
    except psycopg2.errors.UniqueViolation:
        with conn:
            with conn.cursor() as curs:
                curs.execute("SELECT id FROM urls WHERE name=(%s);", (url,))
                id = curs.fetchone()[0]
                flash('Страница уже существует', 'alert-info')
                return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id=(%s);", (id,))
            site = curs.fetchone()
            curs.execute("SELECT * FROM url_checks WHERE url_id=(%s);", (id,))
            checks = curs.fetchall()
            messages = get_flashed_messages(with_categories=True)
            return render_template('url.html',
                                   site=site,
                                   checks=checks,
                                   messages=messages)


@app.post('/urls/<int:id>/checks')
def get_checks(id):
    with conn:
        with conn.cursor() as curs:
            try:
                curs.execute("SELECT name FROM urls WHERE id=(%s);", (id,))
                url = curs.fetchone()[0]
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                status_code = resp.status_code

                h1, title, description = parse(resp.text)

                curs.execute(
                    """INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at)
                    VALUES (
                        %(url_id)s,
                        %(status_code)s,
                        %(h1)s,
                        %(title)s,
                        %(description)s,
                        %(created_at)s);""", {
                        'url_id': id,
                        'status_code': status_code,
                        'h1': h1,
                        'title': title,
                        'description': description,
                        'created_at': datetime.now()
                    })

                flash('Страница успешно проверена', 'alert-success')
                return redirect(url_for('get_url', id=id))

            except requests.exceptions.RequestException:
                flash('Произошла ошибка при проверке', 'alert-danger')
                return redirect(url_for('get_url', id=id))
