class NepremicninaDto:
    ime: str
    posredovanje: str
    vrsta_nepremicnine: str
    leto_gradnja: int
    leto_adaptacija: int
    tip_hise: str
    stevilo_sob: str
    nadstropje: str
    etaznost: str
    m2: float
    m2_parcela: float
    cena: float
    regija: str
    upravna_enota: str
    obcina: str
    energijski_razred: str
    url: str
    opis: str

    def __init__(self,
                 ime,
                 posredovanje,
                 vrsta_nepremicnine,
                 leto_gradnja,
                 leto_adaptacija,
                 tip_hise,
                 stevilo_sob,
                 nadstropje,
                 etaznost,
                 m2,
                 m2_parcela,
                 cena,
                 regija,
                 upravna_enota,
                 obcina,
                 energijski_razred,
                 url,
                 opis):
        self.opis = opis
        self.url = url
        self.energijski_razred = energijski_razred
        self.obcina = obcina
        self.upravna_enota = upravna_enota
        self.regija = regija
        self.cena = cena
        self.m2_parcela = m2_parcela
        self.m2 = m2
        self.nadstropje = nadstropje
        self.etaznost = etaznost
        self.stevilo_sob = stevilo_sob
        self.tip_hise = tip_hise
        self.leto_adaptacija = leto_adaptacija
        self.leto_gradnja = leto_gradnja
        self.vrsta_nepremicnine = vrsta_nepremicnine
        self.posredovanje = posredovanje
        self.ime = ime

    def prepareDtoObject(self):
        izhod = {}
        izhod["ime"] = self.ime
        izhod["vrsta_nepremicnine"] = self.vrsta_nepremicnine
        izhod["posredovanje"] = self.posredovanje
        izhod["leto_gradnja"] = self.leto_gradnja
        izhod["leto_adaptacija"] = self.leto_adaptacija
        izhod["tip_hise"] = self.tip_hise
        izhod["stevilo_sob"] = self.stevilo_sob
        izhod["nadstropje"] = self.nadstropje
        izhod["etaznost"] = self.etaznost
        izhod["m2"] = self.m2
        izhod["m2_parcela"] = self.m2_parcela
        izhod["cena"] = self.cena
        izhod["regija"] = self.regija
        izhod["upravna_enota"] = self. upravna_enota
        izhod["obcina"] = self.obcina
        izhod["energijski_razred"] = self.energijski_razred
        izhod["url"] = self.url
        izhod["opis"] = self.opis

        return izhod


