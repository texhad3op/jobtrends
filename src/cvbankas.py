import requests
from lxml import html
import datetime
import psycopg2
import sys
import pprint as pp
import xml.etree.ElementTree as ET
import codecs

host = 'http://www.cvbankas.lt/'
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
        sys.stdout.write('\r')
        sys.stdout.write("Now parsing %d page of %d" % (url_number, len(urls)))
        url_number += 1
    close_all()


def get_urls():
    page = requests.get(host)

    tree = html.fromstring(page.content)
    pa = tree.xpath('//ul[@class="pages_ul_inner"]//li//a/@href')
    url_for_page = pa[1].split("=")[0]
    pages = tree.xpath('//ul[@class="pages_ul_inner"]//li//a/text()')
    pages_range = range(int(min(pages)), int(max(pages)) + 1)
    urls = set()
    for page in pages_range:
        urls.add(url_for_page + "=" + str(page))
    return urls


def parse_page(page_url):
    page = requests.get(page_url)
    tree = html.fromstring(page.content)
    job_records = tree.xpath('.//div[@class="list_a_wrapper"]')
    for job_record in job_records:
        parse_single_record(job_record)


def parse_single_record(record):
    xml_str = ET.tostring(record, encoding='utf8', method='xml')
    tree = html.fromstring(xml_str)
    positions = tree.xpath('//div[@class="list_a_wrapper"]//div[@class="list_cell"]//h3[@class="list_h3"]//text()')
    # print positions
    companies = tree.xpath('//div[@class="list_a_wrapper"]//div[@class="list_cell list_logo_c"]//img//@alt')
    # print companies
    cities = tree.xpath(
        '//div[@class="list_a_wrapper"]//div[@class="list_cell list_ads_c_last"]//span[@class="txt_list_1"]//span[@class="list_city"]//text()')
    # print cities
    salaries = tree.xpath(
        '//div[@class="list_a_wrapper"]//div[@class="list_cell"]//span[@class="heading_secondary"]//span[@class="jobadlist_salary"]//text()')
    # print salaries
    # print '========================================'
    insert_record(set_value_aware(positions), set_value_aware(companies), set_value_aware(cities), set_value_aware(salaries))


def insert_record(job, hiring_organization, job_location, salary):
    try:
        print codecs.encode(job, '8859', 'strict'), codecs.encode(hiring_organization, '8859', 'strict'), codecs.encode(job_location, '8859', 'strict'), codecs.encode(salary, '8859', 'strict')
        city_id = get_city_id(job_location)
        company_id = get_company_id(hiring_organization)
        cursor.execute(
            "INSERT INTO vacancy (site, city_id, time, date, jobtitle, salary, company_id)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                host, city_id, datetime.datetime.now(), datetime.datetime.now(), unicode(job), unicode(salary), company_id))
    except ValueError:
        print(ValueError)


def set_value_aware(val):
    if 1 > len(val):
        return ""
    else:
        return val[0]


def get_city_id(job_location):
    try:
        cityp = escape_special_characters(job_location)
        city = cityp[0:4] + '%'
        cursor.execute("SELECT id from city where name ilike %(name)s", {"name": city})
        rows = cursor.fetchall()
        id_old = rows[0][0]
        return id_old
    except psycopg2.OperationalError:
        print psycopg2.OperationalError
    except IndexError:
        cursor.execute(
            "INSERT INTO city (name) VALUES ('%s') RETURNING id;" % escape_special_characters(unicode(job_location)))
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
