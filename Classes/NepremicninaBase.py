from abc import ABC, abstractmethod
from Helpers.ParserHelper import ParserHelper

class NepremicninaBase(ABC):

    @abstractmethod
    def getNepremicninaDto(self, response):
        pass

    def _getImeFromResponse(self, response):
        return response.css("h1.podrobnosti-naslov::text").extract_first()

    def _getM2FromIme(self, ime):
        m2 = ime.split(',')[-1].strip().split(' ')[0].replace('.', '').split(',')[0]
        if m2.isnumeric():
            return m2
        return None

    def getPosredovanjeFromIme(self, ime):
        return ime.split(',')[0]

    def _getKratekOpisFromResponse(self, response):
        opis_tmp = response.xpath('//div[@id="opis"]').css('div.kratek::text').extract()
        return opis_tmp[1].strip().split(' ')

    def _getCenaFromKratekOpis(self, kratekOpis):
        cena = kratekOpis[-2].split(',', 1)[0].replace('.', '')
        if cena.isnumeric():
            return cena
        return None

    def _getLetoGradnjaFromKratekOpis(self, kratekOpis):
        leto_gradnja = None

        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if kOpis == "gradnje":
                leto_gradnja = kratekOpis[i + 2].replace(',', '')
            elif kOpis == "zgrajeno" or kOpis == "zgrajena" or kOpis == "zgr.":
                leto_gradnja = kratekOpis[i + 2].replace(',', '')

        return leto_gradnja

    def _getLetoAdaptacijaFromKratekOpis(self, kratekOpis):
        leto_adaptacija = None

        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if kOpis == "adaptirano" and kratekOpis[i + 1] == "l.":
                leto_adaptacija = kratekOpis[i + 2].replace(',', '')

        return leto_adaptacija

    def _getBasicPodatkiFromResponse(self, response):
        return ParserHelper.getBasicPodatkiFromResponse(response)

    def _getPosredovanjeFromBasicPodatkiOrIme(self, basicPodatki, ime):
        posArray = ["Prodaja", "Oddaja"]
        posr_size = len(basicPodatki.split("|")[0].split(" "))
        if posr_size <= 3:
            posredovanje = basicPodatki.split("|")[0].split(" ")[1]  # 'Prodaja'
        else:
            posredovanje = basicPodatki.split("|")[0].split(" ")[3]  # 'Prodaja'

        if posredovanje not in posArray:
            posredovanje = self.getPosredovanjeFromIme(ime)

        return posredovanje

    def _getRegijaFromBasicPodatki(self, basicPodatki):
        tmpRegija = basicPodatki.split("|")[2].split(" ")[2]  # 'LJ-mesto'
        if tmpRegija == 'J.':
            regija = 'J.Primorska'
        else:
            regija = tmpRegija
        return regija

    def _getVrstaNepremicnineFromResponse(self, response):
        return ParserHelper.getVrstaNepremicnineFromResponse(response)

    def _getUpravnaEnotaFromBasicPodatki(self, basicPodatki):
        return basicPodatki.split("|")[3].replace(' Upravna enota: ', '').strip()  # 'Lj. Šiška'

    def _getObcinaFromBasicPodatki(self, basicPodatki):
        return basicPodatki.split("|")[4].replace(' Občina: ', '').strip()  # 'Ljubljana'

    def _getOpisFromResponse(self, response):
        return response.css("div.web-opis div[itemprop='disambiguatingDescription'] p::text").extract()

    def _getEnergijskiRazredFromResponse(self, response):
        energijskiRazredList = response.css('div.icon16::text').extract()  # A, B...
        energijskiRazred = None
        for el in energijskiRazredList:
            energijskiRazred = ''.join(el).strip()

        if energijskiRazred != None:
            energijskiRazred = energijskiRazred.strip()

        return energijskiRazred

    def _getUrlFromResponse(self, response):
        return response.css("link[itemprop='url']::attr(href)").extract()[1]  # url response.request.url #url