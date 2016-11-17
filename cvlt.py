import requests
from lxml import html
import pprint as pp


def parsecvlt():
    host = 'http://www.cv.lt/'
    urls = geturls(host)
    # pp.pprint(urls)
    # for url in urls:
    parsepage(urls[0])


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
    res = zip(jobtitle,hiringOrganization,jobLocation,url)
    print jobtitle
    print hiringOrganization
    print jobLocation
    print url
    print res