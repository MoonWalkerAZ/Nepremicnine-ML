# Nepremicnine-ML
Napoved cene stanovanja glede na različne karakteristike.

Izdelava projekta pri predmetu Tehnologije razvoja inteligentnih sistemov (TRIR).
Projekt je razdeljen na dva dela. 
* V prvem delu s pomočjo knjižnice `scrapy` pridobim vsa stanovanja v Sloveniji, ki se nahajajo na spletni strani 
<a href="https://www.nepremicnine.net/" target="_blank">nepremicnine.net</a>. Te podatke shranim v `.csv` datoteko. 
* V drugem delu pa shranjeno datoteko preberem s pomočjo knjižnice `pandas` s katero tudi manipuliram s podatki o stanovanjih. Na podlagi pridobljenih podatkov napovem ceno stanovanja glede na specifične karakteristike posameznega stanovanja (lokacija, velikost, letnik...). Podatke napovem s pomočjo knjižnic iz sklopa `sklearn` in sicer sem preizkusil več algoritmov za napovedovanje. Ti so  `AdaBoostRegressor`, `RandomForestRegressor`, `DecisionTreeRegressor`, ter izmeril metrike uspešnosti napovedovanja.
* Vsa programska koda se nahaja v tem repozitoriju.
Spider se nahaja v datoteki `scrapy/nepremicnine/spiders/nepremicnine_spider.py`
