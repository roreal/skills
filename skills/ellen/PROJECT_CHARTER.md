---
title: "Produktdirektiv för fjärrvärmekalkylatorn och Ellen"
version: "0.2"
date: "2026-09-08"
status: "täckningsmål beslutat; hantering av saknad leverantör återstår"
owner: "Enkey AB"
---

# Produktdirektiv för fjärrvärmekalkylatorn och Ellen

## 1. Beslutad målordning

### Primärt mål

Bygg en kalkyl på Enkeys webbplats där kundens val av fjärrvärmeleverantör, nät och
produkt påverkar den beräknade årskostnaden och besparingspotentialen genom rätt
fjärrvärmetariff.

### Sekundärt mål

Ellen ska kunna analysera verklig energi- och effektanvändning och föreslå hur kundens
påverkbara fjärrvärmekostnad kan minimeras inom ett avtalat klimatkrav. Ett medelvärde på
22 °C är ett möjligt börvärde, men ett färdigt komfortkontrakt måste även ange
toleransband, representativa zoner och tillåten tid utanför bandet.

### Gemensam teknisk kärna

Kalkylatorn och Ellen ska använda samma versionssatta tariffkatalog och deterministiska
kostnadsmotor. Kalkylatorn använder scenariodata; Ellen kompletterar senare med verkliga
tidsserier, tariffhistorik och komfortdata. Affärsregler ska inte dupliceras i
webbgränssnitt, agentinstruktion och analyskod.

## 2. Kalkylator v1

### Primär användare och uppgift

Den primära användaren är en fastighetsägare, förvaltare eller energiansvarig som vill få
en begriplig första bedömning av vilken ekonomisk potential Optimate kan ha för en
fastighet. Användaren ska kunna ange det underlag som finns tillgängligt och förstå vilka
värden som kommer från leverantören, användaren respektive kalkylatorns antaganden.

### Minsta användarflöde

1. Ange fastighets- och energiunderlag.
2. Välj fjärrvärmeleverantör, nät och produkt när modellen kräver det.
3. Ange synliga, tariffspecifika obligatoriska värden, exempelvis debiterbar effekt.
4. Beräkna ett årsscenario med aktuell tariffversion.
5. Visa beräknad årskostnad, möjlig besparing och relevanta kostnadskomponenter med
   källor, prisår, antaganden, avgränsning och kvalitetsorsaker.
6. Stoppa beräkningen när en obligatorisk uppgift saknas eller ett valt inmatningsläge
   inte stöds. Ersätt inte ett kritiskt avtalsvärde med ett dolt standardvärde.

### Beräkningsomfattning

- V1 är i första hand en leverantörsspecifik **årsberäkning**.
- Månadsbelopp får visas när den aktuella tariffmodellen har verifierad
  månadsperiodisering, men v1 lovar inte generell fakturaåterspelning per månad.
- Varje tariff får stödja de inmatningslägen som dess adapter faktiskt kan hantera.
  MWh-, kronor- och schablonläge är separata förmågor; ett läge som saknar entydig modell
  ska blockeras med begriplig förklaring.
- Besparingspotential är ett scenario och inte ett avtalslöfte eller bevisad besparing.
  En generell besparingsprocent får aldrig användas som bevis för ett faktiskt utfall.

## 3. Verifiering och redovisningsspråk

Modellens verifieringsstatus och det enskilda resultatets datakvalitet är två olika
dimensioner. En verifierad tariffmodell gör inte automatiskt kundens resultat
fakturaverifierat.

### Tariffmodellens verifiering

| Nivå | Krav | Tillåten formulering |
| --- | --- | --- |
| `source_verified_annual` | Aktuell officiell prislista/villkor, samtliga relevanta årsregler strukturerade och ett representativt årsfall kontrollerat mot leverantörens räkneexempel eller en oberoende manuell referensberäkning från samma källa | "Tariff verifierad mot publicerade villkor för [prisår]" |
| `invoice_validated` | Modellen har därutöver jämförts komponentvis med en verklig kundfaktura för den angivna omfattningen | "Fakturavaliderad för [period och omfattning]" |
| `unverified` eller `blocked` | Källan, en regel eller obligatorisk indata är olöst | Inget leverantörsspecifikt färdigresultat |

Fakturavalidering görs för Enkeys kunder eller när den uttryckligen efterfrågas. En
kundfaktura är inte ett generellt krav för att publicera en källverifierad årsmodell.

### Resultatets datakvalitet

| Resultat | Betydelse | Presentation |
| --- | --- | --- |
| Beräknat | Deterministisk kostnad från vald tariff och redovisade indata | "Beräknad årskostnad"; aldrig "faktisk" eller "exakt faktura" |
| Uppskattat | Minst ett relevant värde, en fördelning eller besparingsparameter är antagen eller härledd | "Uppskattning" plus de konkreta antagandena |
| Fakturaverifierat | Ett specifikt kundfall har jämförts mot faktura inom angiven tolerans och omfattning | "Fakturaverifierat utfall" med period och mätgräns |

Använd inte det fristående ordet **exakt** i kundgränssnittet. Intern status `exact` får
fortsätta betyda att motorn har fullständiga verifierade indata för sitt uttryckliga
beräkningsscope; den betyder inte att en verklig faktura har verifierats.

## 4. Leverantörstäckning

### Bekräftad startpunkt

Efter Sandviken-etappen innehåller katalogens produktionsurval sju tariffer från sex
leverantörer. Dessa är en utvärderings- och teknikbaslinje, inte v1:s beslutade
leveransomfattning.

### Beslutat täckningsmål

Kalkylatorn ska stödja **samtliga tariffer i den versionssatta tariffinventeringen som är
möjliga att återskapa som uppskattad årskostnad**. Inventeringen omfattar både den
gemensamma JSON-katalogen och separat förvaltade leverantörsfiler, exempelvis Stockholm
Exergi. Målet är alltså inte ett minsta antal bolag och inte heller att stanna efter en
representativ pilotbatch.

En tariff är möjlig när:

- rätt leverantör, nät, produkt, kundkategori och prisperiod kan identifieras;
- samtliga prisdelar som behövs för årssumman har publicerade eller på annat sätt
  verifierade belopp, formler, enheter och villkor;
- varje kundspecifikt eller historiskt värde som formeln kräver kan anges synligt av
  användaren från faktura/avtal, hämtas från en verifierad källa eller beräknas från ett
  uttryckligt datakrav;
- den deterministiska motorn kan reproducera årssumman utan dold standardtolkning;
- modellens avgränsning och alla kvarvarande uppskattningar kan redovisas begripligt.

Att leverantören själv kan fakturera visar att ett beräkningsunderlag existerar, men gör
inte en externt reproducerbar kalkyl möjlig om en nödvändig formel eller referens bara
finns i leverantörens interna system. Ett sådant fall klassas `blocked_external_info` med
en exakt fråga till leverantören och omprövas när svaret kommer; det ersätts aldrig med
en gissad regel.

Slutkriteriet gäller mot en namngiven inventeringsversion och ett angivet prisår. Varje
tariffprodukt i kontrollmängden ska då ha en av följande dispositioner:

- `implemented_source_verified_annual` — valbar och verifierad för deklarerat årsscope;
- `blocked_external_info` — inte valbar, med dokumenterat saknat besked eller data;
- `not_applicable` — uttryckligen utanför produkten, med motivering.

Ingen tariff får ligga kvar oklassificerad på grund av om den råkar ligga i den gemensamma
katalogen eller i en separat leverantörsfil. Nya prisår blir därefter förvaltning av den
färdiga produkten, inte ett skäl att v1 aldrig kan avslutas.

### Prioriteringsprincip

1. Leverantörer och produkter som används av Enkeys befintliga kunder.
2. Leverantörer som återkommer i konkreta prospekt eller försäljningsdialoger.
3. Tariffamiljer där en redan verifierad adapter kan återanvändas utan att dölja lokala
   skillnader.
4. Övriga möjliga tariffprodukter tills ingen genomförbar post återstår.

Prioriteringen styr genomförandeordningen, inte slutlig omfattning. Även en sent
prioriterad tariff ingår i målet om den uppfyller möjlighetskriterierna ovan.

### Leverantör som saknas — rekommendation, inväntar Robert

Visa ett separat val, exempelvis **"Mitt fjärrvärmebolag saknas"**. Användaren får då en
tydligt märkt generell uppskattning och kan lämna uppgift om leverantör/nät för kommande
prioritering. Kalkylatorn får aldrig tyst presentera riksgenomsnittet som om det vore den
namngivna leverantörens tariff.

## 5. Definition of Done för kalkylator v1

Kalkylator v1 kan kallas färdig när:

- en namngiven tariffinventering och ett prisår har frysts som v1:s kontrollmängd;
- samtliga tariffprodukter i kontrollmängden är implementerade eller uttryckligen
  klassade `blocked_external_info`/`not_applicable` enligt avsnitt 4;
- Robert har beslutat beteendet när leverantören saknas;
- samtliga visade leverantörer har rätt nät-/produktidentitet, aktuellt prisår och
  spårbara officiella källor;
- varje aktiv tariff är källverifierad för sitt deklarerade årsscope och har automatiska
  normal-, gräns-, fel- och regressionstester;
- kritiska tariffvärden är synliga och obligatoriska eller beräkningen blockeras;
- resultatet skiljer beräknat, uppskattat och fakturaverifierat enligt avsnitt 3;
- resultatet visar tariffkälla, prisår, användarindata, antaganden och begränsningar;
- generiskt resultat och leverantörsspecifikt resultat kan inte förväxlas;
- relevanta enhets-, typ-, bygg- och webbläsartester är gröna;
- Robert har godkänt funktion och presentation i testmiljön;
- releaseversion och granskningsunderlag är dokumenterade i Git och conversations.

## 6. Uttryckliga icke-mål för kalkylator v1

- Fakturaexakt månadsåterspelning för samtliga leverantörer.
- Tariffer vars nödvändiga faktureringsformel eller referensdata inte går att få fram;
  dessa dokumenteras och blockeras tills leverantören lämnar besked.
- Kundunika specialavtal som avviker från den valda katalogprodukten, om de inte har
  lämnats in för en uttrycklig kundberäkning.
- Automatisk optimering eller styrning av en verklig anläggning.
- Garanterad energi- eller kostnadsbesparing.
- Dolda uppskattningar av avtalskritisk effekt, produkt, flöde eller temperaturvillkor.
- Kronor-till-MWh-invers för en tariff där lösningen inte är entydig och verifierad.

## 7. Nästa leveranser

1. Robert godkänner eller ändrar det öppna produktvalet i avsnitt 8.
2. Claude tar fram ett separat, litet text-/metadataförslag för kalkylatorn som följer
   verifieringsspråket ovan. Codex granskar före implementation.
3. Claude implementerar den godkända språk-/metadataändringen och Codex webbläsartestar.
4. Nästa tariffbatch väljs efter verkligt kund-/prospektbehov. Om inget sådant behov
   ändrar ordningen används Sandviken som mall för en liten batch av återstående
   källgodkända Familj 4-tariffer. Batcharna fortsätter därefter tills samtliga möjliga
   tariffprodukter i kontrollmängden är implementerade.
5. Det sekundära Ellen-målet får därefter ett eget data- och komfortkontrakt innan någon
   automatisk styrning utvecklas eller tillåts.

## 8. Öppna beslut för Robert

1. **Saknad leverantör:** ska rekommendationen i avsnitt 4 gälla — ett separat val med
   uttryckligen generell uppskattning och möjlighet att efterfråga leverantören?

Täckningsmålet är beslutat: samtliga möjliga tariffer ska genomföras. Inga andra beslut
krävs för att Claude ska kunna förbereda språk-/metadataförslaget och nästa tariffplan.
