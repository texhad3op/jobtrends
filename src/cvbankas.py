import codecs
import datetime
import psycopg2
import requests
import sys
import xml.etree.ElementTree as ET
from lxml import html

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
    # job_records = tree.xpath('.//div[@class="list_a_wrapper"]')
    job_records = tree.xpath('.//a[@class="list_a can_visited"]')
    # print job_records
    # print  hrefs
    # exit()
    for job_record in job_records:
        parse_single_record(job_record)


def parse_single_record(record):
    xml_str = ET.tostring(record, encoding='utf8', method='xml')
    tree = html.fromstring(xml_str)
    positions = tree.xpath('//div[@class="list_a_wrapper"]//div[@class="list_cell"]//h3[@class="list_h3"]//text()')
    companies = tree.xpath('//div[@class="list_a_wrapper"]//div[@class="list_cell list_logo_c"]//img//@alt')
    cities = tree.xpath(
        '//div[@class="list_a_wrapper"]//div[@class="list_cell list_ads_c_last"]//span[@class="txt_list_1"]//span[@class="list_city"]//text()')
    salaries = tree.xpath(
        '//div[@class="list_a_wrapper"]//div[@class="list_cell"]//span[@class="heading_secondary"]//span[@class="jobadlist_salary"]//text()')
    urls = tree.xpath('//a[@class="list_a can_visited"]//@href')
    insert_record(set_value_aware(positions), set_value_aware(companies), set_value_aware(cities),
                  set_value_aware(salaries), set_value_aware(urls))


def insert_record(job, hiring_organization, job_location, salary, url):
    # print job,"====",hiring_organization,"====", job_location,"====", salary,"====", url
    try:
        city_id = get_city_id(job_location)
        company_id = get_company_id(hiring_organization)
        cursor.execute(
            "INSERT INTO vacancy (site, city_id, time, date, jobtitle, salary, url, company_id)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                host, city_id, datetime.datetime.now(), datetime.datetime.now(), codecs.encode(job, '8859', 'strict'),
                codecs.encode(salary, '8859', 'strict'), url ,
                company_id))
    except ValueError:
        pass


def set_value_aware(val):
    if 1 > len(val):
        return ""
    else:
        return val[0]


def get_city_id(job_location):
    try:
        city = codecs.encode(job_location, '8859', 'strict')
        cursor.execute("SELECT id from city where name ilike substring(%(name)s for 4)||'%%'", {"name": city})
        rows = cursor.fetchall()
        id_old = rows[0][0]
        return id_old
    except psycopg2.OperationalError:
        print psycopg2.OperationalError
    except IndexError:
        cursor.execute(
            "INSERT INTO city (name) VALUES (%(name)s) RETURNING id;",
            {"name": city})
        id_new = cursor.fetchone()[0]
        return id_new


def get_company_id(hiring_organization):
    try:
        organization = codecs.encode(hiring_organization, '1257', 'strict')
        cursor.execute("SELECT id from company where name = %(name)s",
                       {"name": escape_special_characters(organization)})
        rows = cursor.fetchall()
        id_old = rows[0][0]
        return id_old
    except psycopg2.OperationalError:
        print psycopg2.OperationalError
    except IndexError:
        cursor.execute(
            "INSERT INTO company (name) VALUES (%(name)s) RETURNING id;", {
                "name": organization})
        id_new = cursor.fetchone()[0]
        return id_new


def escape_special_characters(string):
    return string.replace("'", "''").replace("\"", "\"")
