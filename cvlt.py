import requests
from lxml import html
import pprint as pp
import datetime
import psycopg2

host = 'http://www.cv.lt/'
connection = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
cursor = connection.cursor()


def init():
    global host
    global connection
    global cursor
    host = 'http://www.cv.lt/'
    connection = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    cursor = connection.cursor()


def close_all():
    global connection
    global cursor
    connection.commit()
    cursor.close()
    connection.close()


def parse_site():
    init()
    urls = get_urls()
    for url in urls:
        parse_page(url)
    close_all()


def get_urls():
    page = requests.get(host + 'darbas')
    tree = html.fromstring(page.content)
    pages = tree.xpath('//li[@class="has-sub last"]//ul//li//a/@href')
    urls = set()
    for url in pages:
        urls.add(host + url)
    urls = filter(lambda url: 'page' in url, urls)
    return urls


def parse_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    job = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="title"]//text()')
    hiring_organization = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="hiringOrganization"]//text()')
    job_location = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="jobLocation"]//@content')
    url = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="url"]//@content')
    res = zip(job, hiring_organization, job_location, url)
    for job, hiring_organization, jobLocation, url in res:
        insert_record(job, hiring_organization, job_location, url)


def insert_record(job, hiring_organization, job_location, url):
    try:
        cursor.execute(
            "INSERT INTO events (site, time, date, jobtitle, hiring_organisation, job_location, url) VALUES (%s,%s, %s, %s, %s, %s, %s)",
            (
                host, datetime.datetime.now(), datetime.datetime.now(), job, hiring_organization,
                job_location,
                url))
    except ValueError:
        print ValueError


def get_city_id():
    cur.execute("SELECT vals from sites")
    rows = cur.fetchall()
    for row in rows:
        print "ID = ", row[0]
        return 5


import psycopg2

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    print "Opened database successfully"

    cur = conn.cursor()

    cur.execute("SELECT vals from sites")
    rows = cur.fetchall()
    for row in rows:
        print "ID = ", row[0]

    print "Operation done successfully";
    conn.close()

except:
    print "I am unable to connect to the database"
