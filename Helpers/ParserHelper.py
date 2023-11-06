class ParserHelper:

    @staticmethod
    def getBasicPodatkiFromResponse(response):
        galerija_container = response.css('div.galerija-container')
        more_info_elements = galerija_container.css('div.more_info')
        podatki = None
        for more_info_element in more_info_elements:
            podatki = ' '.join(more_info_element.css('::text').getall()).strip()  # Posredovanje: Prodaja | Vrsta: Stanovanje | Regija: LJ-mesto | Upravna enota: Lj. Šiška | Občina: Ljubljana

        return podatki

    @staticmethod
    def getVrstaNepremicnineFromResponse(response):
        basicPodatki = ParserHelper.getBasicPodatkiFromResponse(response)
        if basicPodatki != None:
            return basicPodatki.split("|")[1].split(" ")[2]
        return None