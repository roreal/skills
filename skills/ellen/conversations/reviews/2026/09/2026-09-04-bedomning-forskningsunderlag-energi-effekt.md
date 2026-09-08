---
review_id: "2026-09-04-003"
date: "2026-09-04"
reviewer: Codex
status: usable-with-revisions
scope:
  - forskningsunderlaget om fjärrvärmeenergi och effektuttag
  - möjligheten att undanröja effektrelaterade tariffhinder
  - kopplingen till den tekniska kartläggningen av 28 källgodkända tariffer
implementation_changed: false
source_document_changed: false
---

# Bedömning av forskningsunderlaget om energi och effekt

## Samlad bedömning

Underlaget är användbart och i huvudsak metodiskt korrekt. Det kan hjälpa Optimate förbi
ett viktigt arkitekturhinder: olika leverantörers debiterbara effekt får inte ersättas med
en gemensam uppskattning från årsenergi. Effekt måste i stället behandlas som ett eget,
spårbart beräkningsunderlag med leverantörsspecifik metod.

Underlaget gör däremot **inte** en fakturakorrekt debiterbar effekt möjlig från enbart
årlig MWh. Det visar tvärtom varför en sådan generell omräkning inte är säker. För att
undanröja hindret krävs någon av följande vägar:

1. använd leverantörens eller fakturans redan fastställda effekt,
2. beräkna effekten från tillräckligt detaljerade mät- och väderdata exakt enligt
   leverantörens regel,
3. använd en forskningsbaserad uppskattning endast som ett separat, tydligt märkt
   analysläge som inte påstås motsvara fakturans debiteringsgrund.

Forskningsunderlaget bör därför godkännas som **metod- och utvecklingsunderlag**, men inte
som ensam verifieringskälla för en tariff eller som stöd för dagens tysta funktion
`uppskattaEffekt(totalMwh)`.

## Vad det kan lösa i den aktuella 28-gruppen

Den tekniska kartläggningen omfattar 27 tariffer med effekt-/kapacitetsdel och en ren
energitariff, Sundsvall Indal/Liden/Lucksta. Påståendet i kartläggningens v2 att det
gemensamma effekthindret berör "samtliga 28" är därför en mindre motsägelse; hindret berör
27 av 28.

| Väg | Vad som krävs | Resultatets status | Praktisk betydelse |
| --- | --- | --- | --- |
| Leverantörs-/fakturavärde | Debiterbar effekt, avtalsprodukt och relevant giltighetsperiod | Exakt för den leverantörsfastställda uppgiften | Snabbaste vägen förbi det gemensamma effektfältshindret. Fältet måste vara obligatoriskt och får inte ersättas med en schablon. |
| Kategorital eller annan publicerad energiformel | Exakt normalårskorrigerad energihistorik, kategorital, period och leverantörens avrundningsregler | Reproducerbar när hela leverantörsformeln är publicerad | Här får effekt härledas från energi eftersom leverantören själv har definierat sambandet. Ett forskningsbaserat kategorital får inte ersätta leverantörens. |
| Uppmätt topp eller toppmedel | Tim- eller dygnsserie med exakt urvalsperiod, blockindelning och kalenderregel | Reproducerbar debiteringsgrund | Kan stödja exempelvis högsta dygn, medel av toppdygn eller fasta 12-timmarsblock. |
| Effektsignatur/regression | Dygns- eller timdata, rätt väderkälla, tillåtna dagar, referenstemperatur, historik, kvalitetsgräns, reservregel och avrundning | Reproducerbar först när hela leverantörsmetoden är implementerad och fakturatestad | Relevant för bland annat E.ON/Navirum, Telge, Sandviken och Vattenfalls rekommenderade effekt. |
| Referensgrupp/fullasttimmar | Kvalitetssäkrat bestånd av jämförbara byggnader | Uppskattning med osäkerhetsintervall | Bra för avvikelsedetektering, prognos och tidig rådgivning, men inte som fakturaunderlag eller tariffgodkännande. |

Det första alternativet kan införas utan en ny beräkningsmotor för effekt. Det tar bort
det gemensamma hindret i användargränssnittet och datakontraktet, men löser inte andra
tariffproblem såsom flödesformler, månadsperiodisering, produktgiltighet eller okända
leverantörsparametrar.

Det andra till fjärde alternativet kräver en ny, separat tjänst eller modul för
effektunderlag. Dagens enda skalära `kapacitetKw` kan vara modulens utdata, men räcker inte
som indata när leverantören räknar om effekten månadsvis. E.ON/Navirums rullande effekt är
ett tydligt exempel: senaste fakturans tal ger en ögonblicksbild, medan en exakt
tolvmånaderssimulering behöver en effektserie.

## Rekommenderat datakontrakt

Varje effektuppgift bör minst bära följande information:

```text
value_kw
basis_type                 # supplier_value, measured, calculated eller estimated
billing_method             # leverantörens namngivna metod
measurement_resolution     # exempelvis 1 h, 12 h eller 24 h
source_period_start
source_period_end
valid_from
valid_to
weather_source
reference_temperature_c
calculation_version
quality_status
uncertainty_or_error_kw
source_reference
```

Fält som inte gäller ska markeras som ej tillämpliga. Ett saknat värde är okänt och får
inte ges noll eller ett dolt standardvärde.

## Nödvändiga rättningar och förtydliganden i forskningsunderlaget

### 1. Tre effektbegrepp måste hållas isär i hela dokumentet

Dokumentet gör redan skillnaden i den källkritiska anmärkningen, men rekommenderade fält
och formler bör genomgående skilja mellan:

- observerad toppeffekt i mätserien,
- beräknad dimensionerande effekt,
- leverantörens debiteringsgrundande effekt eller kapacitet.

`P_max` i fullasttimmar och lastfaktor behöver därför en uttrycklig metodetikett. En
leverantörs abonnerade eller regressionsberäknade kapacitet är inte automatiskt samma sak
som periodens observerade maximum.

### 2. Minimikravet ”en uppvärmningssäsong” är för svagt för tariffreproduktion

En säsong kan räcka för en första byggnadsanalys, men flera aktuella leverantörer använder
två eller tre års medelvärden, rullande perioder eller en reservregel över 36 månader.
Datakravet ska vara det längsta av:

- analysmodellens statistiska minimikrav,
- tariffens föreskrivna historikperiod,
- reservregelns historikperiod.

Det behövs även regler för datatäckning, dubbletter, tidszon/sommartid, mätarbyten,
driftstopp, vardagsurval och bortfiltrering av ogiltiga temperaturer.

### 3. Effektsignaturen måste skilja fysisk modell från tariffregel

Formeln på rad 193 är rimlig som en förenklad modell inom uppvärmningsområdet, men en
fysisk, generell signatur bör normalt vara styckvis eller begränsad vid balanstemperaturen,
så att uppvärmningsdelen inte fortsätter negativt under varma dagar. En leverantörstariff
ska däremot reproduceras exakt som publicerad, med leverantörens dagurval och eventuella
linjära extrapolering. Optimate får inte ”förbättra” tariffens egen formel i smyg.

`P_base` bör dessutom beskrivas som temperatur-oberoende last, där tappvarmvatten,
varmvatten-cirkulation och andra icke-väderberoende laster kan ingå; den är inte
nödvändigtvis en ren tappvarmvattenlast.

### 4. Lastfaktorns intervall behöver villkoras

Påståendet att lastfaktorn ligger mellan 0 och 1 gäller när nämnaren använder ett verkligt
maximum för samma period och samma mätdefinition. Det är inte ett generellt löfte om
`P_max` byts mot abonnerad, dimensionerad eller debiterad effekt eller om perioderna inte
matchar.

### 5. Källornas evidensnivå och primärlänkar bör framgå

- Calikus-påståendena om 1 222 byggnader, två nät, sex kategorier, 3,4 miljoner m² och
  1 540 TJ är verifierade i artikelns publicerade sammanfattning.
- Kensby-påståendena om fem flerbostadshus, 52 veckor och cirka 0,1 kWh/m² vid sällan mer
  än ±0,5 °C är verifierade. Länken bör bytas från EconPapers till Chalmers officiella
  publikationspost.
- Romanchenkos 134 representativa byggnader, timmodell och slutsatser om tung bebyggelse
  är verifierade. Studien gäller dock ett modellerat Göteborg 2050 och visar flexibilitet,
  inte en generell formel för kundens debiterbara effekt.
- Holmén och Larsson är examensarbeten på masternivå. De är relevanta, men bör benämnas
  och viktas som examensarbeten, inte jämställas med de sakkunniggranskade artiklarna.
- BeBo/Belok 2024 verifierar de fyra komponenterna och variationen mellan bland annat
  kategorital, dygnseffekt, effektsignatur och abonnerad effekt. Rapporten är ett mycket
  direkt stöd för tariffarkitekturen, men inte för ett universellt effektvärde.
- BeBo/Beloks publicerade steg 2 från 2025 bör läggas till. Det levererar ännu ingen färdig
  teknisk standard, men rekommenderar ett stegvis pilotprojekt med några olika
  prismodeller och bekräftar behovet av harmoniserad terminologi och maskinläsbara
  komponenter.

## Rekommenderad utvecklingsordning

1. Inför ett tariffstyrt, obligatoriskt faktura-/leverantörsfält för debiterbar effekt och
   stäng av `uppskattaEffekt` för dessa tariffer.
2. Märk varje resultat med `supplier_value`, `calculated` eller `estimated`; blanda inte
   statusarna.
3. Modellera leverantörens effektmetod som ett eget datakontrakt, skilt från tariffens
   prisband och från fysisk dimensionering.
4. Bygg tidsserieimport och gemensamma, testade byggstenar för tim-/dygnsaggregation,
   temperaturkoppling och historikfönster.
5. Implementera separata leverantörsregler ovanpå byggstenarna: urval, regression,
   referenstemperatur, kvalitetsgräns, reservregel, medelvärdesperiod och avrundning.
6. Fakturavalidera varje metod med minst en verklig, anonymiserad kund innan den får
   status produktionsgodkänd.
7. Bygg först därefter referensgrupper och probabilistiska uppskattningar från Optimate-data.
   Dessa ska alltid redovisa intervall och får inte användas som dold debiterbar effekt.

Ett lämpligt pilotupplägg är en tariff med direkt leverantörsvärde, en med uppmätt
toppmedel, en med effektsignatur och en med abonnerad effekt. Det följer BeBo/Beloks
rekommendation att börja stegvis med några olika prismodeller och gör att datakontraktet
prövas mot verkligt skilda metoder innan fler bolag ansluts.

## Kontrollerade källor

- [Calikus m.fl., arXiv och bibliografisk artikelpost](https://arxiv.org/abs/1901.04863)
- [Holmén, Högskolan i Gävles DiVA-post](https://hig.diva-portal.org/smash/record.jsf?pid=diva2%3A1694697)
- [Kensby m.fl., Chalmers officiella publikationspost](https://research.chalmers.se/en/publication/209419)
- [Romanchenko m.fl., Chalmers fulltext](https://research.chalmers.se/publication/520069/file/520069_Fulltext.pdf)
- [Larsson, Chalmers ODR](https://odr.chalmers.se/items/376afc24-5a4a-45c0-b25b-d535192b0422)
- [BeBo/Belok 2024, Maskinläsbara prismodeller för fjärrvärme](https://www.bebostad.se/media/7182/bebo-maskinl%C3%A4sbara-prismodeller-f%C3%B6r-fj%C3%A4rrv%C3%A4rme.pdf)
- [BeBo/Belok 2025, Maskinläsbara prismodeller steg 2](https://www.bebostad.se/projekt/avslutade-projekt/2025/maskinlasbara-prismodeller-for-fjarrvarme-steg-2)
