import requests
from lxml import html
import datetime
import psycopg2
import sys

host = 'http://www.cv.lt/'
connection = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
cursor = connection.cursor()


def init():
    global host
    global connection
    global cursor
    print "Starting parse %s site" % host
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
    print "Pages to parse %d" % len(urls)
    url_number = 1
    for url in urls:
        parse_page(url)
        url_number += 1
        sys.stdout.write('\r')
        sys.stdout.write("Now parsing %d page of %d" % (url_number, len(urls)))
    close_all()


def get_urls():
    page = requests.get(host + 'darbas')
    tree = html.fromstring(page.content)
    pages = tree.xpath('//li[@class="has-sub last"]//ul//li//a/@href')
    urls = set()

    for uri in pages:
        urls.add(host + uri)

    urls = filter(lambda url: 'page' in url, urls)
    return urls


def parse_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    jobs = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="title"]//text()')
    hiring_organizations = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="hiringOrganization"]//text()')
    job_locations = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="jobLocation"]//@content')
    urls = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="url"]//@content')
    res = zip(jobs, hiring_organizations, job_locations, urls)
    for job, hiring_organization, job_location, url in res:
        process_record(job, hiring_organization, job_location, url)


def process_record(job, hiring_organization, job_location, url):
    cities = job_location.split(",")
    for city in cities:
        insert_record(job, hiring_organization, city.strip(), url)


def insert_record(job, hiring_organization, job_location, url):
    try:
        city_id = get_city_id(job_location)
        company_id = get_company_id(hiring_organization)
        cursor.execute(
            "INSERT INTO vacancy (site, city_id, time, date, jobtitle, company_id, url)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                host, city_id, datetime.datetime.now(), datetime.datetime.now(), job, company_id,
                url))
    except ValueError:
        print(ValueError)


def get_city_id(job_location):
    try:
        cursor.execute("SELECT id from city where name = %(name)s", {"name": escape_special_characters(job_location)})
        rows = cursor.fetchall()
        id_old = rows[0][0]
        return id_old
    except psycopg2.OperationalError:
        print psycopg2.OperationalError
    except IndexError:
        print job_location, escape_special_characters(job_location)
        cursor.execute(
            "INSERT INTO city (name) VALUES ('%s') RETURNING id;" % escape_special_characters(job_location))
        id_new = cursor.fetchone()[0]
        return id_new


def get_company_id(hiring_organization):
    try:
        cursor.execute("SELECT id from company where name = %(name)s",
                       {"name": escape_special_characters(hiring_organization)})
        rows = cursor.fetchall()
        id_old = rows[0][0]
        return id_old
    except psycopg2.OperationalError:
        print psycopg2.OperationalError
    except IndexError:
        cursor.execute(
            "INSERT INTO company (name) VALUES ('%s') RETURNING id;" % escape_special_characters(hiring_organization))
        id_new = cursor.fetchone()[0]
        return id_new


def escape_special_characters(string):
    return string.replace("'", "''").replace("\"", "\"")
