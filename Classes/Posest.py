from Classes.NepremicninaBase import NepremicninaBase
from Dtos.NepremicninaDto import NepremicninaDto


class Posest(NepremicninaBase):

    def __init__(self ):
        super().__init__()

    def getNepremicninaDto(self, response):
        ime = NepremicninaBase._getImeFromResponse(self, response)
        basicPodatki = NepremicninaBase._getBasicPodatkiFromResponse(self, response)
        kratekOpis = NepremicninaBase._getKratekOpisFromResponse(self, response)
        hisa = NepremicninaDto(
            ime,
            NepremicninaBase._getPosredovanjeFromBasicPodatkiOrIme(self, basicPodatki, ime),
            NepremicninaBase._getVrstaNepremicnineFromResponse(self, response),
            None,
           None,
            None,
            None,
            None,
            None,
            None,
            self._getParcelaFromKratekOpis(kratekOpis),
            self.getCenaParcele(kratekOpis),
            NepremicninaBase._getRegijaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getUpravnaEnotaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getObcinaFromBasicPodatki(self, basicPodatki),
            None,
            NepremicninaBase._getUrlFromResponse(self, response),
            NepremicninaBase._getOpisFromResponse(self, response)
        )

        return hisa.prepareDtoObject()

    def getCenaParcele(self, kratekOpis):
        cena = NepremicninaBase._getCenaFromKratekOpis(self, kratekOpis)
        m2 = self._getParcelaFromKratekOpis(kratekOpis)
        if m2 == None or cena == None:
            return None

        if not cena.isnumeric() or not m2.isnumeric():
            return None

        cena_float = float(cena)
        m2_float = float(''.join(m2))
        if cena_float < 1000.0:
            cena_float = cena_float * m2_float

        return str(cena_float).split(".")[0]

    def _getParcelaFromKratekOpis(self, kratekOpis):
        parcela = None
        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if kOpis == "m2,":
                parcela = kratekOpis[i - 1].replace(".", "").split(",")[0]

        return parcela