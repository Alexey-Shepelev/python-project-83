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

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def take_domain(url):
    url = urlparse(url)
    return url._replace(
        path='',
        params='',
        query='',
        fragment='').geturl()


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls')
def get_urls():
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("""SELECT
                                urls.id, urls.name,
                                MAX(url_checks.created_at) AS created_at
                                FROM urls LEFT JOIN url_checks
                                ON urls.id = url_checks.url_id
                                GROUP BY urls.id
                                ORDER BY urls.id;""")
            urls = curs.fetchall()

    # conn.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    data = request.form.to_dict()
    url = take_domain(data['url'])
    if not validate(url) or len(url) > 255:
        messages = get_flashed_messages(with_categories=True)
        flash('Incorrect URL', 'alert-danger')
        return render_template('index.html', messages=messages, url=url), 422
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    INSERT INTO urls (name, created_at)
                    VALUES (%(name)s, %(created_at)s)
                    RETURNING id;
                    """,
                    {'name': url, 'created_at': datetime.now()})
                id = curs.fetchone()[0]
                flash('Website successfully added', 'alert-success')
                return redirect(url_for('get_url', id=id))
    except psycopg2.errors.UniqueViolation:
        with conn:
            with conn.cursor() as curs:
                curs.execute("SELECT id FROM urls WHERE name=(%s);", (url,))
                id = curs.fetchone()[0]
                flash('Website already exist', 'alert-info')
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
            curs.execute(
                """INSERT INTO url_checks (
                    url_id,
                    created_at)
                VALUES (
                    %(url_id)s,
                    %(created_at)s);""", {
                    'url_id': id,
                    'created_at': datetime.now()
                })
            flash('Website successfully checked', 'alert-success')
            return redirect(url_for('get_url', id=id))
