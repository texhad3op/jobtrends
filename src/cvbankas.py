import requests
from lxml import html
import datetime
import psycopg2
import sys
import pprint as pp


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
    # init()
    urls = get_urls()
    print "Pages to parse %d" % len(urls)
    url_number = 1
    # for url in urls:
    parse_page("http://www.cvbankas.lt/?page=1")
    #     sys.stdout.write('\r')
    #     sys.stdout.write("Now parsing %d page of %d" % (url_number, len(urls)))
    #     url_number += 1
    # # close_all()


def get_urls():
    page = requests.get(host)
    tree = html.fromstring(page.content)
    pa = tree.xpath('//ul[@class="pages_ul_inner"]//li//a/@href')
    url_for_page = pa[1].split("=")[0]
    pages = tree.xpath('//ul[@class="pages_ul_inner"]//li//a/text()')
    pages_range = range(int(min(pages)), int(max(pages))+1)
    urls = set()
    for page in pages_range:
        urls.add(url_for_page+"="+str(page))
    return urls


def parse_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    jobs = tree.xpath('//div[@class="list_a_wrapper"]')
    print jobs
    print len(jobs)
    print 'kkkkkkkkkkkkkkkkk'
    pp.pprint(jobs[0])
    jj = html.fromstring(jobs[0])
    print jj.xpath('//div[@class="list_cell"]//h3[@class="list_h3"]//text()')
    # print jobs[0][0][0].xpath('//h3[@class="list_h3"]//text()')
    # print jobs[0].xpath('//h3[@class="list_h3"]//text()')

    # hiring_organizations = tree.xpath('//span[@class="heading_secondary"]//text()')
    # print hiring_organizations
    # job_locations = tree.xpath('//span[@class="list_city"]//text()')
    # print len(job_locations)
    # res = zip(jobs, hiring_organizations)
    # print res
    # salaries = tree.xpath('//span[@class="jobadlist_salary"]//text()')
    # print len(salaries)



    # urls = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="url"]//@content')
    # res = zip(jobs, hiring_organizations, job_locations, urls)
    # for job, hiring_organization, job_location, url in res:
    #     process_record(job, hiring_organization, job_location, url)


# def process_record(job, hiring_organization, job_location, url):
#     cities = job_location.split(",")
#     for city in cities:
#         insert_record(job, hiring_organization, city.strip(), url)
#
#
# def insert_record(job, hiring_organization, job_location, url):
#     try:
#         city_id = get_city_id(job_location)
#         company_id = get_company_id(hiring_organization)
#         cursor.execute(
#             "INSERT INTO vacancy (site, city_id, time, date, jobtitle, company_id, url)"
#             " VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (
#                 host, city_id, datetime.datetime.now(), datetime.datetime.now(), job, company_id,
#                 url))
#     except ValueError:
#         print(ValueError)
#
#
# def get_city_id(job_location):
#     try:
#         cursor.execute("SELECT id from city where name = %(name)s", {"name": escape_special_characters(job_location)})
#         rows = cursor.fetchall()
#         id_old = rows[0][0]
#         return id_old
#     except psycopg2.OperationalError:
#         print psycopg2.OperationalError
#     except IndexError:
#         print job_location, escape_special_characters(job_location)
#         cursor.execute(
#             "INSERT INTO city (name) VALUES ('%s') RETURNING id;" % escape_special_characters(job_location))
#         id_new = cursor.fetchone()[0]
#         return id_new
#
#
# def get_company_id(hiring_organization):
#     try:
#         cursor.execute("SELECT id from company where name = %(name)s",
#                        {"name": escape_special_characters(hiring_organization)})
#         rows = cursor.fetchall()
#         id_old = rows[0][0]
#         return id_old
#     except psycopg2.OperationalError:
#         print psycopg2.OperationalError
#     except IndexError:
#         cursor.execute(
#             "INSERT INTO company (name) VALUES ('%s') RETURNING id;" % escape_special_characters(hiring_organization))
#         id_new = cursor.fetchone()[0]
#         return id_new
#
#
# def escape_special_characters(string):
#     return string.replace("'", "''").replace("\"", "\"")
