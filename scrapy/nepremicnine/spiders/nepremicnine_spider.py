import scrapy

class NepremicnineSpider(scrapy.Spider):
    name = 'nepremicnine' #ime v terminalu
    allowed_domains = ['www.nepremicnine.net']
    nepremicnine = {}

    def start_requests(self):

        # 13 regij prodaja stanovanj + 13 regij oddaje stanovanj
        urls = ['https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/gorenjska/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/juzna-primorska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/severna-primorska/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/notranjska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/savinjska/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/podravska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/koroska/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/dolenjska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/posavska/stanovanje/', 'https://www.nepremicnine.net/oglasi-prodaja/zasavska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-prodaja/pomurska/stanovanje/',

                'https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/ljubljana-okolica/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/gorenjska/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/juzna-primorska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/severna-primorska/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/notranjska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/savinjska/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/podravska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/koroska/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/dolenjska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/posavska/stanovanje/', 'https://www.nepremicnine.net/oglasi-oddaja/zasavska/stanovanje/',
                'https://www.nepremicnine.net/oglasi-oddaja/pomurska/stanovanje/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seznam_oglasov)

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
            # Pripravimo URL za parsanje
            yield scrapy.Request(link, callback=self.parse_vse_strani_seznama_oglasov)

    def parse_vse_strani_seznama_oglasov(self, response):
        linksOglasov = response.css('a.slika::attr(href)').extract()
        linksOglasov = ["https://www.nepremicnine.net" + link for link in linksOglasov]
        for link in linksOglasov:
            # Pripravimo URL za parsanje
            yield scrapy.Request(link, callback=self.parse_oglas_podrobno)

    def parse_oglas_podrobno(self, response):
        ime = response.css("h1.podrobnosti-naslov::text").extract_first() #Prodaja, stanovanje, 4-sobno: LJUBLJANA  CENTER, DEVANA PARK, 78.68 m2
        stSob = ime.split(',')[2].split(' ')[1][:-1] #'4-sobno'
        sobe = ["3-sobno", "2-sobno","4-sobno", "garsonjera", "soba", "drugo", "apartma"]
        obstaja = False
        for el in sobe:
            if el == stSob:
                obstaja = True
                break
        if obstaja == False:
            stSob = [el.split(":")[0].strip() for el in ime.split(",") if "sob" in el]
        m2 = ime.split(',')[-1].strip().split(' ')[0] # 96,9
        kratekOpis = response.xpath('//div[@id="opis"]').css('div.kratek::text').extract_first() # , 96,9 m2, 3-sobno, zgrajeno l. 1909, VP/3 nad., V centru prodamo staromeščansko stanovanje, s kletno shrambo, balkonom in čudovitim vrtom (60 m2), prodamo. Cena: 280.000,00 EUR
        cena = kratekOpis.split(" ")[-2].split(",")[0].replace('.', '') # '280000'
        leto = kratekOpis.split(" ")
        leto = [el[:-1] for el in leto if len(el) is 5]
        leto = [element for element in leto if element.isnumeric()]
        if leto != []:
            leto = leto[-1]  # '1901'
        nadstropje = [el for el in kratekOpis.split(" ") if "/" in el]
        okNadstropje = False
        if nadstropje != []:
            nad = ["1", "2", "P", "3", "4", "VP", "5", "M", "6", "PK", "7", "10", "8", "9", "11", "K", "12", "P+1",
                   "14", "16", "17", "13", "K+P", "2K", "19", "K+P+M", "P+M", "18", "K+P+1", "P+1+M", "15", "Klet",
                   "P+1+2", "P+1+2+M", "K+P+1+M"]
            for el in nad:
                if el == nadstropje[0].split("/")[0]:
                    nadstropje = nadstropje[0].split("/")[0]# 'VP/3 -> VP'
                    okNadstropje = True
                    break

        if okNadstropje == False:
            nadstropje = None

        podatki = response.css("div.more_info::text").extract_first() #Posredovanje: Prodaja | Vrsta: Stanovanje | Regija: LJ-mesto | Upravna enota: Lj. Šiška | Občina: Ljubljana
        posredovanje = podatki.split("|")[0].split(" ")[1] #'Prodaja'
        tmpRegija = podatki.split("|")[2].split(" ")[2] #'LJ-mesto'
        if tmpRegija == 'J.':
            regija = 'J.Primorska'
        else:
            regija = tmpRegija
        upravnaEnota = podatki.split("|")[3].replace(' Upravna enota: ', '').strip() #'Lj. Šiška'
        obcina = podatki.split("|")[4].replace(' Občina: ', '').strip() # 'Ljubljana'
        opis = response.css("div.web-opis div[itemprop='disambiguatingDescription'] p::text").extract() #besedilo
        energijskiRazred = response.css('div.icon16::text').extract_first() # A, B...
        link = response.request.url #url

        izhod = {}

        izhod["ime"] = ime
        izhod["stevilo_sob"] = stSob
        izhod["m2"] = m2
        izhod["opis"] = opis
        izhod["cena"] = cena
        izhod["leto"] = leto
        izhod["nadstropje"] = nadstropje
        izhod["posredovanje"] = posredovanje
        izhod["regija"] = regija
        izhod["upravna_enota"] = upravnaEnota
        izhod["obcina"] = obcina
        izhod["energijski_razred"] = energijskiRazred
        izhod["link"] = link

        yield izhod