from Classes.NepremicninaBase import NepremicninaBase
from Dtos.NepremicninaDto import NepremicninaDto


class Hisa(NepremicninaBase):

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
            NepremicninaBase._getLetoGradnjaFromKratekOpis(self, kratekOpis),
            NepremicninaBase._getLetoAdaptacijaFromKratekOpis(self, kratekOpis),
            self._getTipHiseFromKratekOpis(kratekOpis),
            None,
            None,
            self._getEtaznostFromKratekOpis(kratekOpis),
            NepremicninaBase._getM2FromIme(self, ime),
            self._getParcelaFromKratekOpis(kratekOpis),
            NepremicninaBase._getCenaFromKratekOpis(self, kratekOpis),
            NepremicninaBase._getRegijaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getUpravnaEnotaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getObcinaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getEnergijskiRazredFromResponse(self, response),
            NepremicninaBase._getUrlFromResponse(self, response),
            NepremicninaBase._getOpisFromResponse(self, response)
        )

        return hisa.prepareDtoObject()



    def _getEtaznostFromKratekOpis(self, kratekOpis):
        etaznost = None
        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if "+" in kOpis:
                etaznost = kOpis.replace(",", "")

        return etaznost

    def _getParcelaFromKratekOpis(self, kratekOpis):
        parcela = None
        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if kOpis == "zemljišča,":
                parcela = kratekOpis[i - 2].replace(".", "").split(",")[0]


        if parcela == None:
            return None

        if not parcela.isnumeric():
            return None

        return parcela

    def _getTipHiseFromKratekOpis(self, kratekOpis):
        return kratekOpis[3].replace(",", "")