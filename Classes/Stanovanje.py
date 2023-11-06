from Classes.NepremicninaBase import NepremicninaBase
from Dtos.NepremicninaDto import NepremicninaDto


class Stanovanje(NepremicninaBase):

    def __init__(self ):
        super().__init__()

    def getNepremicninaDto(self, response):
        ime = NepremicninaBase._getImeFromResponse(self, response)
        basicPodatki = NepremicninaBase._getBasicPodatkiFromResponse(self, response)
        kratekOpis = NepremicninaBase._getKratekOpisFromResponse(self, response)
        stanovanje = NepremicninaDto(
            ime,
            NepremicninaBase._getPosredovanjeFromBasicPodatkiOrIme(self, basicPodatki, ime),
            NepremicninaBase._getVrstaNepremicnineFromResponse(self, response),
            NepremicninaBase._getLetoGradnjaFromKratekOpis(self, kratekOpis),
            NepremicninaBase._getLetoAdaptacijaFromKratekOpis(self, kratekOpis),
            None,
            self.getSteviloSobFromIme(ime),
            self._getNadstropjeFromKratekOpis(kratekOpis),
            None,
            NepremicninaBase._getM2FromIme(self, ime),
            None,
            NepremicninaBase._getCenaFromKratekOpis(self, kratekOpis),
            NepremicninaBase._getRegijaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getUpravnaEnotaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getObcinaFromBasicPodatki(self, basicPodatki),
            NepremicninaBase._getEnergijskiRazredFromResponse(self, response),
            NepremicninaBase._getUrlFromResponse(self, response),
            NepremicninaBase._getOpisFromResponse(self, response)
        )

        return stanovanje.prepareDtoObject()

    def getSteviloSobFromIme(self, ime):
        stSob = ime.split(',')[2].split(' ')[1][:-1]
        sobe = ["3-sobno", "2-sobno", "4-sobno", "garsonjera", "soba", "drugo", "apartma"]
        obstaja = False
        for el in sobe:
            if el == stSob:
                obstaja = True
                break
        if obstaja == False:
            stSob = [el.split(":")[0].strip() for el in ime.split(",") if "sob" in el]
            stSob = stSob[0]

        return stSob

    def _getNadstropjeFromKratekOpis(self, kratekOpis):
        nadstropje = None
        for i in range(len(kratekOpis)):

            kOpis = kratekOpis[i].replace('"', '')
            kOpis = kOpis.strip()

            if kOpis == "nad.,":
                nadstropje = kratekOpis[i - 1].split("/")[0].replace(".", "")
            elif "/" in kOpis:
                nadstropje = kratekOpis[i].split("/")[0].replace(".", "")

        return nadstropje