import scrapy
from sys import path

MY_PATH = "C:\\Users\\aljaz\Downloads\\Nepremicnine-ML-master"
path.append(MY_PATH)

from Classes.Posest import Posest
from Classes.Hisa import Hisa
from Classes.Stanovanje import Stanovanje
from Helpers.ParserHelper import ParserHelper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

HISA = "hisa/"
STANOVANJE = "stanovanje/"
POSEST = "posest/zazidljiva/"

BASE_URLS = ['https://www.nepremicnine.net/oglasi-prodaja/slovenija/ljubljana-mesto/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/ljubljana-okolica/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/gorenjska/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/juzna-primorska/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/severna-primorska/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/notranjska/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/savinjska/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/podravska/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/koroska/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/dolenjska/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/posavska/', 'https://www.nepremicnine.net/oglasi-prodaja/slovenija/zasavska/',
                'https://www.nepremicnine.net/oglasi-prodaja/slovenija/pomurska/',

                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/ljubljana-mesto/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/ljubljana-okolica/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/gorenjska/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/juzna-primorska/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/severna-primorska/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/notranjska/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/savinjska/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/podravska/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/koroska/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/dolenjska/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/posavska/', 'https://www.nepremicnine.net/oglasi-oddaja/slovenija/zasavska/',
                'https://www.nepremicnine.net/oglasi-oddaja/slovenija/pomurska/']
def generateUrls():
    allUrls = []
    for url in BASE_URLS:
        allUrls.append(url + STANOVANJE)
        allUrls.append(url + HISA)
        allUrls.append(url + POSEST)
    return allUrls


class NepremicnineSpider(scrapy.Spider):
    name = 'nepremicnine' #ime v terminalu
    allowed_domains = ['nepremicnine.net', 'api.zenrows.com']
    nepremicnine = {}

    def start_requests(self):
        urls = generateUrls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seznam_oglasov, headers=HEADERS)

    def parse_seznam_oglasov(self, response):
        stStrani = response.xpath('//div[@id="pagination"]').css('li.paging_last a::attr(href)').extract_first()
        if stStrani != None:
            stStrani = stStrani.split('/')[-2]
        else:
            stStrani = 1
        stStrani = int(stStrani)
        urlStrani = response.css("li.paging_active a::attr(href)").extract_first()
        links = []
        if int(stStrani) != 1:
            for i in range(1, stStrani + 1):
                links.append("https://www.nepremicnine.net" + urlStrani + str(i)+"/")
        else:
            links.append(response.url)

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_vse_strani_seznama_oglasov, headers=HEADERS)

    def parse_vse_strani_seznama_oglasov(self, response):
        linksOglasov = response.css('a.url-title-d::attr(href)').extract()

        for link in linksOglasov:
            yield scrapy.Request(url=link, callback=self.parse_oglas_podrobno, headers=HEADERS)

    def parse_oglas_podrobno(self, response):
        vrsta_nepremicnine = ParserHelper.getVrstaNepremicnineFromResponse(response)

        if ("Stanovanje" == vrsta_nepremicnine):
            yield self.parseStanovanje(response)

        elif ("Hiša" == vrsta_nepremicnine):
            yield self.parseHisa(response)

        elif ("Posest" == vrsta_nepremicnine):
            yield self.parsePosest(response)


    def parseStanovanje(self, response):
        print("Parsam stanovanje")
        stanovanje = Stanovanje()
        return stanovanje.getNepremicninaDto(response) #izhod

    def parseHisa(self, response):
        print("Parsam hišo")
        hisa = Hisa()
        return hisa.getNepremicninaDto(response) #izhod

    def parsePosest(self, response):
        print("Parsam posest")
        posest = Posest()
        return posest.getNepremicninaDto(response) #izhod
