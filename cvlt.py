import requests
from lxml import html
import pprint as pp
import datetime
import psycopg2


def parsecvlt():
    host = 'http://www.cv.lt/'
    urls = geturls(host)
    for url in urls:
        parsepage(url)


def geturls(host):
    page = requests.get(host + 'darbas')
    tree = html.fromstring(page.content)
    pages = tree.xpath('//li[@class="has-sub last"]//ul//li//a/@href')
    urls = set()
    for url in pages:
        urls.add(host + url)
    urls = filter(lambda url: 'page' in url, urls)
    return urls


def parsepage(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    jobtitle = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="title"]//text()')
    hiringOrganization = tree.xpath('//div[@id="TablRes"]//tr//td//p//a[@itemprop="hiringOrganization"]//text()')
    jobLocation = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="jobLocation"]//@content')
    url = tree.xpath('//div[@id="TablRes"]//tr//td//p//meta[@itemprop="url"]//@content')
    res = zip(jobtitle, hiringOrganization, jobLocation, url)
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    for a, b, c, d in res:
        insertrecord(cur, a, b, c, d)
    conn.commit()
    cur.close()
    conn.close()


def insertrecord(cur, a, b, c, d):
    try:
        cur.execute(
            "INSERT INTO events (site, time, date, jobtitle, hiring_organisation, job_location, url) VALUES (%s,%s, %s, %s, %s, %s, %s)",
            ('http://www.cv.lt/', datetime.datetime.now(), datetime.datetime.now(), a, b, c, d))
    except ValueError:
        print ValueError
