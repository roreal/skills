---
proposal_id: "2026-09-17-001"
version: 1
date: "2026-09-17"
author: Codex
status: "godkänd inriktning; källnormalisering beställd, produktimplementation ej påbörjad"
approved_by: Robert
relates_to:
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
  - "Fjarrvarmetariffer/batchplan-v22.md"
  - "Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md"
  - "Fjarrvarmetariffer/optimate-fjarrvarme-2026.json"
  - "Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md"
implementation_changed: false
tariff_activation_changed: false
push_changed: false
---

# Källrevision och angreppsplan för de 28 blockerade dispositionerna

## Beslut

Den tidigare beskrivningen "28 externt blockerade" är inte längre korrekt. En ny
genomgång av leverantörernas aktuella officiella 2026-sidor, PDF:er och publika
beräkningsverktyg ger följande arbetsklassning:

| Klass | Antal dispositioner | Betydelse |
| --- | ---: | --- |
| Källösta, väntar på intern modellering/implementation | 22 | Kan byggas utan bolagssvar, men ska förbli spärrade tills kod, tester och separat aktivering är granskade. |
| Verkligt externt blockerade | 6 | Fem avgränsade mejlfrågor måste besvaras innan taxan/varianten kan modelleras utan antagande. |
| **Totalt** | **28** | Oförändrad frusen dispositionsmängd. |

Det här ändrar inte dagens skarpa disposition `62 implemented / 2 ready / 28 blocked
av 92`. Omklassningen gäller varför posterna är blockerade, inte om de redan är
implementerade. En post flyttas först vid en separat, testad och granskad
implementations-/aktiveringskedja.

Om båda befintliga redo-dispositionerna och alla 22 nu källösta dispositioner senare
implementeras kan kalkylatorn nå `86 implemented / 0 ready / 6 blocked av 92`. De sex
sista kan nås först efter fem entydiga leverantörssvar.

## 22 dispositioner som inte längre behöver bolagssvar

| Grupp | Antal | Källbeslut och säkert produktkontrakt |
| --- | ---: | --- |
| Vattenfall Standard/Spetsig, sex nätgrupper | 12 | Leverantörens officiella 2026-kalkylator publicerar nätens energipriser, Standard-effektpriser, månadsprofiler, flödeskategorier och volymrabatt. Spetsig är 1 724 kr/kW; gränsen är energi/effekt 1,2. Bygg en uttryckligt **uppskattad** årsprodukt med kundens/leverantörens effekt, rätt profil och synligt flödesval — inte fakturareproduktion. |
| Skellefteå Kraft, pellets- och kraftvärmeort | 2 | Prislistorna ger energi, effekt, avkylningsregel och rabattfunktion. Rabattfunktionens kontinuitet och prisskala visar att resultatet är öre/kWh; denna dimensionsslutsats ska dokumenteras och resultatet märkas uppskattat. Leverantörens effektvärde används, så saknade ortstemperaturer behöver inte härledas. |
| Sundsvall Energi, Matfors samt Kvissleby/Njurunda | 2 | 2026-tabellen är komplett t.o.m. 1 999 kW. Hård övre produktgräns 1 999 kW; 2 000+ stoppas som individuellt avtal. Flödesdelen kräver explicita månadsvisa kund- och nätvärden eller leverantörens fakturerade justering; inget dolt nätmedel. |
| Eskilstuna Energi & Miljö | 1 | Formel och faktor är publicerade. Kräv kundens månadsflöde/energi och explicit månadsreferens `Q alla/W alla`, alternativt fakturerad justering. Leverantörens exempelvärde 28 får bara användas som ett synligt valt snapshot, aldrig som dold 2026-sanning. |
| Mälarenergi större fastigheter | 1 | 2026-priser, 2 217 kr i första stora 25–79-bandet, maxeffektens bränsleår samt flödesformel är publicerade. Kräv månadsvis kundflöde och publicerad/angiven nätreferens; en äldre säsong får bara användas som synligt snapshot. |
| VB Energi | 1 | Aktuell 2026-sida anger samma villkor i Ludvika, Grängesberg, Fagersta och Norberg. Produkten begränsas till dessa fyra nät och använder leverantörens effekt/fem dygnstoppar. Björnmossen inkluderas inte utan svar. |
| Södertörn/SFAB kundvald effekt | 1 | 2026-villkoren definierar överuttag, 1 032 kr/kW, efterföljande justering och retroaktiv differens inom bindningstiden. Detta kräver en stateful årsmodell eller uttryckligt fakturerat justeringsbelopp; inte en statisk `capacity_overrun`. |
| Kraftringen Brunnshög | 1 | Officiell sida anger 647 kr/MWh och en styckvis returtemperaturdel: 6,90 kr/MWh/°C över 20 till 35 °C, därefter ytterligare 20,40 kr/MWh/°C över 35 °C. Officiella kontrollpunkter är 750,50 vid 35 °C och 954,50 vid 45 °C. |
| Tekniska Verken Linköping lågtemperatur | 1 | Ordinarie Linköpingstariff gäller, men flödespriset oktober–april är 2,67 i stället för 5,35 kr/m³. Modellera som en variant som bara ersätter flödessatsen. |
| **Summa** | **22** | |

### Vattenfalls maskinläsbara 2026-underlag

Den officiella priskalkylatorns inbäddade konfiguration gav följande exklusive moms:

| Nätgrupp | Standard kr/kW, år | Energipris jan–dec, kr/MWh |
| --- | ---: | --- |
| Haninge/Tyresö/Älta | 1 319 | 816, 816, 816, 542, 289, 289, 289, 289, 289, 542, 542, 816 |
| Gustavsberg | 1 302 | 821, 821, 821, 513, 289, 289, 289, 289, 289, 513, 513, 821 |
| Motala/Askersund | 1 263 | 813, 813, 813, 515, 288, 288, 288, 288, 288, 515, 515, 813 |
| Nyköping | 1 295 | 784, 784, 784, 532, 288, 288, 288, 288, 288, 532, 532, 784 |
| Uppsala | 1 326 | 809, 809, 809, 545, 285, 285, 285, 285, 285, 545, 545, 809 |
| Vänersborg | 1 239 | 763, 763, 763, 519, 287, 287, 287, 287, 287, 519, 519, 763 |

Officiella månadsprofiler, procent januari–december:

- flerbostadshus: `17,17,11,9,4,2,1,1,3,8,10,17`;
- industri: `15,16,10,9,4,3,2,2,4,8,10,17`;
- lokal: `14,14,10,9,5,4,2,3,5,9,10,15`;
- egen månadsprofil: användarens tolv värden.

Flödesvalen motsvarar `−7,5`, `−3,75`, `0`, `+3,75` och `+7,5`, multiplicerat
med 4 kr/MWh januari–april och oktober–december. Volymrabattens årsband är
`0/249/1249/2499/4999/7500` MWh med avdrag `0/5/10/20/25/30` kr/MWh under
samma sju månader. Detta är kalkylatorns estimatmodell. Den får inte återanvända
befintlig helårs-volymrabatt eller flödestyp om deras period- och indatasemantik inte
är identisk.

Lokalt hämtade granskningskopior vid revisionen:

- kalkylatorsida SHA-256 `8e1707e28d6f6972b8dc75cf3f8e0ee87ad9cdf0392ec02f6f797bd840caa314`;
- komponentmodul SHA-256 `4288641b675b0220c1fe68d464e7abf5a9b9e039dea7a8e97b955860fb0d0c7e`.

Kopiorna i `/tmp` är revisionsunderlag, inte ännu godkända repoartefakter.

## Sex dispositioner som fortfarande kräver fem svar

| Prioritet | Bolag/fråga | Dispositioner | Varför internet inte räcker |
| ---: | --- | ---: | --- |
| 1 | Hässleholm Miljö: hela effekten eller marginalintervall | 2 | Prisbanden publiceras men tillämpningssemantiken framgår inte. Ett svar frigör Hässleholm och Tyringe. |
| 2 | HEMAB: tabell eller motsägande 1 750-MWh-exempel | 1 | Tabellen ger 50 575 kr marginalrabatt, exemplet 45 050 kr. Båda kan inte vara normerande. |
| 3 | Gävle Energi: brytmånad för ackumulerat volymavdrag | 1 | Villkoren säger ackumulerat kalenderår och avdrag varje månad, men inte om tröskelmånaden får avdrag på hela, marginaldelen eller först nästa månad. |
| 4 | Mälarenergi: flödespremie för gruppanslutna småhus | 1 | Aktuell prissida grupperar energipriset, medan flödessidan säger stora fastigheter och äldre PDF säger att småhus inte omfattas. |
| 5 | Finspång: 20-procentigt spetsvärmetillägg | 1 | Det framgår inte vilka prisdelar som multipliceras eller exakt när klassningen börjar/slutar. |
| **Summa** | **Fem mejl** | **6** | |

Färdiga mejl finns i
`Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`.

## Frivilliga följdfrågor som inte ska stoppa implementation

Tre mejl kan förbättra precision eller nätomfattning men är inte produktblockerande:

1. EEM: var kunden hämtar månadens `Q alla/W alla`.
2. Sundsvall Energi: var kunden hämtar nätets månadsvisa `Q/W` för flödespremien.
3. VB Energi: om Björnmossen omfattas av samma 2026-villkor som de fyra publicerade
   orterna.

## Genomförandeordning

### Etapp 0 — käll- och blockeringsbokföring, skills-repot

Normalisera först de 28 dispositionerna 1:1 i JSON, inventering, batchplan och teknisk
kartläggning. Flytta inte någon post till implementerad eller valbar. Gör tydlig skillnad
mellan:

- `external_answer_required` — exakt sex dispositioner;
- `source_resolved_implementation_pending` — exakt 22 dispositioner;
- dynamiskt kund-/nätvärde som obligatorisk indata — inte en extern formelfråga;
- avtalsgräns som ska stoppas fail-closed — inte ett skäl att blockera alla andra kunder.

### Etapp 1 — Vattenfall, 12 dispositioner

Högst utväxling per gemensam motor. Implementera officiell profil, sju månaders
volymrabatt, kategoriskt flödesestimat och Standard/Spetsig-validering. Kräv
leverantörens effekt eller tillräckliga mätvärden. Alla resultat ska tydligt heta
uppskattad årskostnad enligt Vattenfalls 2026-kalkylator.

### Etapp 2 — dynamisk nät-/flödesfamilj, 4 dispositioner

EEM, Sundsvall två rader och Mälarenergi större fastigheter. Återanvänd ett typat
kontrakt för explicit månadsvis kundvärde + nätvärde, men håll leverantörernas olika
formler och perioder separata. Snapshot kräver synligt val, källperiod och
`accuracy=snapshot`.

### Etapp 3 — specialvarianter och leverantörsvärden, 4 dispositioner

SFAB kundvald effekt, Brunnshög, Linköping lågtemperatur och VB Energi fyra publicerade
nät. Varje variant ska ha eget goldenfall och fail-closed gräns.

### Etapp 4 — Skellefteå, 2 dispositioner

Implementera gemensam avkylningsmotor och den källhärledda rabattfunktionen med
explicit enhetsproveniens och gränstester vid 300 och 10 000 MWh.

### Etapp 5 — svarsbatchen, högst 6 dispositioner

Varje svar arkiveras med datum, avsändare, full frågetråd och bilagor. Codex granskar
svaret mot frågan innan status ändras. Ofullständigt svar leder till en avgränsad
följdfråga, inte ett antagande.

## Stoppregler

- Ingen av de 28 får aktiveras genom denna källrevision.
- Inga okända nätmedel, returtemperaturer, effekter, band eller avtalsval får få dolda
  standardvärden.
- En individuell prisdel ska stoppas med begriplig orsak i stället för att gissas.
- Resultat utan fakturavalidering ska beskrivas som uppskattade, enligt projektmålet.
- Batch 7:s separata historikomskrivningsfråga, dess lokala produktcommits och
  `neptune-marketing/dist/` får inte beröras av etapp 0.
- Aktivering och push kräver egna granskade signaler enligt samtalsprotokollet.

## Officiella huvudkällor

- Vattenfall, 2026-kalkylator: https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/
- Vattenfall, Standard/Spetsig: https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/fragor-och-svar-om-fjarrvarmepriset/
- SFAB 2026: https://sfab.se/media/33mnnexa/prislista-normal-2026.pdf
- Kraftringen Brunnshög: https://prod.kraftringen.se/foretag/varme-och-kylalosningar/fjarrvarme/lagtempererad-fjarrvarme/priser/
- Tekniska Verken 2026: https://tekniskaverken.se/foretag/fjarrvarme/priser
- Mälarenergi priser: https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/
- Mälarenergi flödespremie: https://www2.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/
- Gävle Energi priser: https://www.gavleenergi.se/foretag/fjarrvarme/fjarrvarmeavgifter/
- HEMAB 2026: https://www.hemab.se/download/18.727ad6af19ac23cdb98120ae/1764247260203/Prislista%20flerbostadshus%202026.pdf
- Hässleholm prismodell: https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell
- Sundsvall Energi priser: https://sundsvallenergi.se/foretag-och-brf/fjarrvarme/fjarrvarme-for-verksamheten/fjarrvarmepriser
- VB Energi 2026: https://www.vbenergi.se/fjarrvarme/priser/prisvillkor-20222222/
- Finspång 2026: https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf
