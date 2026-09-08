---
review_id: "2026-09-08-001"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v1.md
  - Fjarrvarmetariffer/batchplan-v1.md
  - skills commit 1d52803ba871064509610394edb9d4eb9ba6fbb8
reviewed_heads:
  skills: "1d52803ba871064509610394edb9d4eb9ba6fbb8"
  enkey-agents: "fd8f8da"
  neptune_academy: "f1df177"
implementation_changed: false
push_status: local-unpushed-not-approved
---

# Granskning av tariffinventering v1 och batchplan v1

## Bedömning

Leveransen är en användbar första sammanställning och samtliga 78 katalog-ID:n förekommer i
dokumentet. Den kan däremot inte godkännas som frusen kontrollmängd eller
implementeringsplan ännu. Den beställda per-produktmatrisen saknas, flera tariffers
obligatoriska flödes-/temperaturindata och motorarbete är utelämnade, två årsberäkningsbara
tariffer är felaktigt externt blockerade och några möjliga produktvarianter skjuts undan med
`not_applicable` utan att lämna kontrollmängden.

Ingen tariffimplementation ska börja och commit `1d52803` ska inte pushas innan en v2 har
rättat fynden nedan och lämnats för omgranskning.

## Fynd

### P1 — den beställda per-produktmatrisen har inte levererats

Överlämning `2026-09-08-001` kräver för varje unik tariffprodukt bland annat nät, produkt,
kundkategori, prisår/giltighet, primärkällor, käll-/katalog-/motor-/kontrakts-/test-/UI-status,
årsreproducerbarhet, obligatorisk indata med fyndplats, inmatningslägen och adapter.

Inventeringens tabeller för `ready_to_implement` och `blocked_external_info` redovisar bara
delmängder av detta. Grupptext eller en hänvisning till verifieringslistan ersätter inte en
radvis kontrollmatris. Därmed går det inte att kontrollera att en `ready`-rad faktiskt har
alla prisdelar, indata och kodvägar som krävs.

**Begärd rättning:** lägg en normaliserad rad per unik tariffprodukt med samtliga beställda
fält. Separera aktuell teknisk status från slutdispositionen. Riksgenomsnittet ska ligga i en
separat tabell för syntetiska schabloner, inte bland tariffprodukterna.

### P1 — tre dispositioner strider mot källunderlaget eller godkänd scope

1. `borlange-energi-borlange-2026` är i verifieringslistan godkänd för årsberäkning med
   leverantörens effektgrupp. Det är samma leverantörsvärde-policy som inventeringen använder
   för bland annat Borås och ska därför vara `ready_to_implement`, med automatisk
   gruppindelning blockerad.
2. `c4-energi-kristianstad-2026` är av samma skäl årsberäkningsbar med leverantörens
   effektgrupp och ska inte vara `blocked_external_info` på grund av 500-kW-gränsen.
3. Stockholm Exergis `validated`-policy och godkännande `2026-09-06-003` täcker endast
   `monthly_invoice`. Godkännandet säger uttryckligen att kalkylatorns årsprognos och invers
   inte ingår. Den aktiva legacy-årsvägen saknar kontrakt för kall energi och returtemperatur
   och anropar i dag motorn utan dessa värden. Fakturavalideringen får därför inte ensam bära
   dispositionen `implemented_source_verified_annual`. Redovisa produkten som aktiv legacy
   i nulägeskolumnen, men håll slutdispositionen `ready_to_implement` tills årsmodellen har
   ett eget källverifierat referensfall, fullständiga synliga indata/antaganden och rätt
   inmatningslägen.

Provisoriskt, om inga produktvarianter läggs till enligt nästa fynd, blir kontrollen för de
78 katalogprodukterna därför **7 implementerade + 46 redo + 25 externt blockerade = 78**.
Detta är en kontrollhypotes för v2, inte ett slutligt godkännande av alla 46 `ready`-rader.

### P1 — obligatoriska indata och nya adapterbehov är systematiskt underskattade

Batchplanen behandlar stora delar av batch 4 som befintlig `selected_band_affine`-funktion,
men kostnaden består också av justeringsposter som dagens motor inte kan räkna eller som
kräver andra värden än effekt.

- Mälarenergi 2–4 lägenheter har ingen kapacitetsdel alls. Planen kräver ändå effekt för alla
  i batch 4a. Tariffen behöver fast årsavgift, energi och säsongens verkliga flöde i m³.
- Södertörn behöver både debiterbar effekt och temperaturavvikelse. Telge behöver effekt,
  normalårskorrigerad energi och returtemperatur. VänerEnergi behöver effekt och flöde.
- Jämtkrafts tre produkter använder den ännu ej stödda typen `flow_difference` och behöver
  flödesdata för oktober–april utöver effekt. Batch 4b kan alltså inte anges som utan ny
  motorkod.
- Eskilstuna använder `network_flow_difference` och behöver kundflöde samt nätets
  referensvärde eller en uttryckligt verifierad fakturapost. Inventeringen anger bara
  effekt/band.
- Kraftringen använder `supply_temperature_adjusted_flow`; Umeå använder
  `asymmetric_flow_difference`; Finspång använder `conditional_flow`. Alla kräver motorstöd
  och kompletta, tariffspecifika indata utöver det som batchplanen listar.
- Partille och flera andra temperatur-/flödesprodukter saknar sina justeringsfält i
  inventeringen trots att dessa påverkar årssumman.
- `volume`-implementationen i dagens Python- och TypeScript-motor använder ett enda
  årsflöde och beaktar inte postens `months`. Minst Luleå, Mälarenergi 2–4 lägenheter, Nevel,
  Öresundskraft Helsingborg normal, Öresundskraft Ängelholm normal, PiteEnergi centrala
  nätet, PiteEnergi Norrfjärden/Sjulnäs och Tekniska Verken Linköping har säsongsbegränsad
  flödesavgift. De behöver en verifierad säsongs-/månadsindata och motorsemantik; ett
  årsflöde får inte appliceras på fel månader. Fullårsvarianterna behöver fortfarande ett
  synligt flödesvärde eller ett uttryckligen redovisat antagande.
- Borås `optional_environmental_addon` är inte behandlat i batch 5. Det måste antingen bli
  ett synligt produkt-/avtalsval eller avgränsas uttryckligen.

**Begärd rättning:** härled alla obligatoriska fält från varje prisdel, inte bara från
kapacitetsdelen. Ange per produkt fältnamn, enhet, period/upplösning, källa på faktura/avtal,
om ett enda årsvärde är matematiskt tillräckligt samt exakt motor-/policy-/UI-arbete.

### P1 — möjliga specialvarianter får inte döljas som "ej tillämpliga i denna batch"

`not_applicable` är en slutdisposition för något som verkligen ligger utanför produkten, inte
en etikett för uppskjutet arbete. Följande kända fall måste antingen bli egna
tariffprodukter/varianter i kontrollmängden eller få en slutlig, saklig avgränsning som Robert
godkänner:

- E.ON/Navirums 36-månadersmetod för kunder med annan bas-/delvärmekälla;
- Södertörns kundvalda effekt och överuttagsavgift;
- Kraftringens Brunnshög;
- Tekniska Verken Linköpings lågtemperaturleverans;
- Finspångs spetsvärmetillägg på 20 procent;
- Jönköpings avtalsberoende accessavgift;
- Borås valbara miljötillägg.

Att bara aktivera "normal/fullvärme" kan vara rätt första delbatch, men kontrollmängden måste
fortfarande visa vad som återstår. Det slutliga antalet tariffprodukter kan därför bli större
än 78 när de aggregerade katalograderna delas korrekt.

### P2 — räkningsspråket och två delsummeringar är fel

- 78 katalograder + separat Stockholmfil + riksgenomsnitt ger 80 råa kontrollposter.
  Efter deduplicering återstår 79 unika enheter: **78 tariffprodukter + 1 syntetisk
  schablon**, inte 79 unika tariffprodukter.
- Katalogens 53 leverantörer inkluderar redan Stockholm Exergi. Den separata filen skapar
  ingen ny leverantör. Det är 53 fjärrvärmeleverantörer och en syntetisk schablonentitet, inte
  55 unika leverantörsentiteter.
- Inventeringens §4.3 innehåller 27 rader, inte 26.
- Batch 4a listar 8 tariffer, inte 7. Totalsumman 43 blir rätt först när dessa två
  delsummeringar rättas.

### P2 — batchplanen följer inte överlämningens ordning eller ID-krav

När ingen kund-/prospektprioritet finns säger överlämningen att återstående Familj 4 ska
komma först. Planen sätter Sundsvalls rena energitariff före Familj 4. Antingen ska ordningen
rättas eller ett nytt Robert-beslut dokumenteras. Skriv dessutom ut samtliga stabila
tariff-ID:n utan `...`; förkortade ID:n går inte att maskinellt eller manuellt stämma av mot
kontrollmängden.

Codex svar på inventeringens öppna frågor är:

1. Låt Vattenfall ligga helt `blocked` tills flödesreferensen är löst. Bygg inte osynliga
   delkomponenter före de verkligt genomförbara batcherna.
2. Följ teknisk kartläggning v4 och håll Sundsvall Matfors blockerad.
3. Leverantörsvärde-mönstret godtas i princip, men endast efter tariffvis kontroll av varje
   kostnadspåverkande fält och var kunden hittar det.
4. De uppräknade specialvarianterna får inte få slutstatus `not_applicable` enbart för att de
   skjuts ur en batch.

### P1 — dokumentationscommitten är inte självbärande och innehåller brutna länkar

Commit `1d52803` refererar till `PROJECT_CHARTER.md`, den tekniska kartläggningen och
agentfundamentet, men dessa filer är fortfarande ospårade. Tariff-to-do:n är ändrad men inte
med i committen. En push av den nuvarande committen skulle därför sakna delar av sitt eget
styrande underlag.

Dessutom är länkarna från handoff- och sessionsfilen till `Fjarrvarmetariffer/` en katalog för
korta (`../../../...` i stället för `../../../../...`). Länkkontrollen hittar sex brutna
länkar. `delivered_at` och ändringsloggen anger 10:15 trots att committen är tidsstämplad
09:53:32; använd verklig känd tid eller markera tiden som okänd. `git diff --check HEAD^ HEAD`
rapporterar även en extra tom rad sist i handoff-filen.

## Verifieringar

- Samtliga 78 katalog-ID:n jämfördes maskinellt mot ID:n i inventeringen: inget ID saknas.
- Katalogen bekräftar 78 tariffobjekt och 53 medlems-/leverantörsposter.
- Inventeringens och batchplanens radantal räknades oberoende.
- Aktuell motor kontrollerades i `justeringar.py`, `faktura.py`, `katalog.py` och
  TypeScript-spegeln `fjarrvarme.ts`.
- Stockholm Exergis policyregister, legacy-produktväg och tidigare Codex-godkännande
  `2026-09-06-003` jämfördes mot den nya dispositionen.
- Båda implementationsrepona var rena vid granskningen. Ingen produkttestsvit kördes eftersom
  leveransen endast ändrar dokumentation.
- Lokal länkkontroll fann sex brutna länkar. `git diff --check` fann en blankrad vid EOF.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v2.md` som en verklig per-produktmatris med alla fält i
   överlämningen och en separat schablontabell.
2. Rätta dispositionerna för Borlänge, C4 och Stockholm Exergis årsprodukt och redovisa en
   ny, härledbar räkningskontroll.
3. Gör en tariffvis indatainventering för samtliga prisdelar och rätta batchernas adapter-,
   motor-, kontrakts-, test- och UI-arbete.
4. Dela upp eller spåra alla kända specialvarianter; använd inte `not_applicable` som
   uppskjutningsstatus.
5. Rätta räkning, ordning, fullständiga ID:n, länkar och metadata.
6. Gör dokumentationshistoriken självbärande genom att ta med de styrande underlag som
   leveransen refererar till, utan att fånga orelaterade arbetskopieändringar.
7. Skapa en fokuserad lokal rättningscommit ovanpå `1d52803` och stanna för Codex
   omgranskning. Ändra ingen produktkod eller tariffdata och pusha inte.
