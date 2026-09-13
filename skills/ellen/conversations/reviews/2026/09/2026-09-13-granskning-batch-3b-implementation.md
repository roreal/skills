---
review_id: "2026-09-13-036"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-activation
scope: "Lokal Batch 3b-implementation bakom spärr"
reviewed_heads:
  skills: "e712cea464d45e75afdc5186c86294f27b4e8dd6"
  skills_catalog: "2af09b2e3b11f69be60ac110e4f6e328820d364d"
  enkey_agents: "f237ef1dfcbb93c234f4aa7cf39a6ac6db8a9583"
  neptune_academy: "6ce65e845fbb2db50251c3f8f283d070ee33e908"
activation_allowed: false
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
follows: "2026-09-13-035"
---

# Granskning av Batch 3b:s lokala implementation

## Beslut

**Changes required före aktivering.** De åtta rätta variantraderna finns bakom
implementationsspärren, prispariteten och stabila variant-ID:n är i huvudsak rätt och
samtliga befintliga tariff-/TypeScript-sviter är gröna. Tre P1-fynd innebär ändå att
produktkontraktet ännu kan använda ett periodlöst eller återanvänt effektvärde och att
de skarpa fullvärmepolicyerna pekar på historiska käll-ID:n. Tre P2-fynd gäller de
beständiga acceptansbevisen och katalogens levande metadata.

Behåll alla åtta `investigation.status="utreds"`. **Ingen aktivering och ingen push.**

## Fynd

### P1 — fakturamånaden saknas ur 36-månaderseffektens kontrakt

Den officiella 2026-prislistan säger att bas-/delvärmeeffekten är medelvärdet av de tre
högsta uppmätta dygnsmedeleffekterna under de föregående 36 månaderna **inklusive
månaden som fakturan avser**, och att effekt-, flödes- och energidelen debiteras för
förbrukningsmånaden. Handoff 001 kräver därför att observerad period är fakturamånaden
och att saknad/ogiltig period blockerar eller felar fältnära.

`tools/tariffer/policyregister.py:935-944` anger däremot
`matupplosning="arsvis"`, tom `kalperiod_definition` och ingen annan periodmarkör.
`test_batch_3b_bas_delvarme.py:288-297` får följaktligen
`annual/snapshot/complete` utan `observerad_period`, och DOM-fixturen gör samma sak.
`rullande=True` takar noggrannheten men bevisar inte vilken fakturamånad kundvärdet
kommer från.

#### Krävd rättning

- Representera leverantörsvärdet som månadsbundet och kräv ett `ÅÅÅÅ-MM`-värde för
  fakturamånaden genom den befintliga `observeradPeriod`-kedjan i både Python och
  TypeScript. Behåll ett enda skalärt leverantörsvärde; bygg ingen rå 36-månadersserie.
- Låt periodvärdet nå den bundna `IndataPost`-posten. Saknad period ska blockera,
  ogiltigt format ska ge ett fältnära fel och giltig period ska ge
  `annual/snapshot/complete`, aldrig `exact`.
- Uppdatera Python-golden, TypeScript-produktprov och komponentprov så en normal submit
  faktiskt fyller perioden. Använd inte det befintliga fria datumintervallformatet för
  Kraftringens januari–februari-bas som om det vore en fakturamånad.

### P1 — skarpa fullvärmepolicyer pekar fortfarande på de historiska `_0`-källorna

Katalogens åtta bastariffer pekar nu korrekt på `03_1`, `04_1`, `25_1` och `26_1`, men
de redan skarpa fullvärmepolicyerna i `tools/tariffer/policyregister.py:678-871` har
fortfarande totalt 32 `kalla`-texter med `03_0`, `04_0`, `25_0` eller `26_0`. Den
genererade skarpa filen bär därför samma 32 gamla hänvisningar, exempelvis
`tariffer.generated.ts:594-675`, trots att `_0` i katalogen uttryckligen är ett
historiskt 2025-dokument. Texten kallar samtidigt dokumentet en officiell prislista
för 2026.

Batch 3b-komponentens fullvärmefixtur använder redan `_1`, så provet är inte troget den
faktiska skarpa posten och döljer avvikelsen.

#### Krävd rättning

- Byt endast dessa 32 icke-prissättande källtexter i de åtta fullvärmepolicyerna till
  rätt `_1`-ID och lägg ett regressionsprov som jämför bas- och variantpolicyernas
  käll-ID med katalogens aktuella `source_refs`.
- Regenerera artefakten. Granskning 036 utvidgar uttryckligen den tillåtna diffen före
  aktivering till just dessa källtexter, utöver proveniensraden och de åtta
  `Fullvärme`-etiketterna. Inga priser, bindningar, täckningsflaggor eller beräknings-
  värden får ändras.
- Byt formuleringen `leverantörens ... effektsignatur` i variantens
  `capacity.billing_basis_method` till `leverantörens ... debiterbara effekt`.
  Prislistan kallar fullvärmeregressionen effektsignatur men 36-månadersfallet ett
  uppmätt medelvärde; de två metoderna ska inte blandas språkligt.

### P1 — produktbyte återanvänder fullvärmeeffekten under variantens nya bindning

Vid ändring av `leverantorId` rensar `KalkylatorPage.tsx:372-386` policyfält, fel och
perioder men inte `form.kapacitetKw`. Det dedikerade effektfältet ligger i `form`, inte i
`policyFaltRaw`, så värdet `50` från fullvärmeprodukten står kvar när användaren väljer
Bas-/delvärme. De två fälten har olika betydelse: fullvärmens temperaturregresserade
effekt respektive bas-/delvärmens 36-månadersmedel.

Testet på `KalkylatorPageBatch3b.test.tsx:221-259` säger att effekt inte återanvänds men
kontrollerar bara band, flöde och temperatur. Slutsubmittens blockering bevisar inte
effekten, eftersom de tre andra tomma fälten redan blockerar.

#### Krävd rättning

- Rensa eller nyckla om den dedikerade `kapacitetKw`-staten vid produkt-/leverantörsbyte
  så ett värde aldrig flyttas mellan två olika `kapacitetBindning`-nycklar.
- Låt komponentprovet direkt verifiera att `#kapacitetKw` är tomt efter byte i båda
  riktningarna. Fyll sedan band/flöde/temperatur/period men inte effekt och bevisa att
  just den saknade effekten blockerar; återinmatad effekt ska därefter ge resultat.

### P2 — TypeScript-golden över samtliga åtta varianter saknas

`neptune_academy@6ce65e8` lägger bara till ett DOM-prov med ett handbyggt
Järfälla-bostäder-par. Det finns inget tabellstyrt TypeScript-goldenprov för de åtta
variant–bastariff-paren, trots handoffens acceptanspunkt 3. Provet använder dessutom
årsbärande yttre mock-ID:n (`...-2026--bas-delvarme`) medan generatorns avsedda publika
produkt-ID är årsoberoende (`...--bas-delvarme`). Python bevisar motorn och räknar åtta
genererade nycklar, men det bevisar inte TypeScript-adapterns åtta serialiserade
policyer och kostnadsdelar.

#### Krävd rättning

Lägg ett tabellstyrt TypeScript-prov över exakt alla åtta med produktionslika,
årsoberoende yttre produkt-ID:n och rätt katalog-ID i `prisar.tariff_id`. Pinna de
publicerade energi-/effekt-/flödespriserna oberoende av funktionen som testas och jämför
variant mot bas för fast/energi/justering samt `annual/snapshot/complete`. Täck också
`unsupported_input_mode`, `besparing_ej_stodd`, fel band och saknad/ogiltig period,
effekt, flöde och temperatur enligt handoffen.

### P2 — levande katalogräkning och paritetsallow-list är för vida

Katalogen har 86 rader och alla 86 bär `price_status="published_2026"`, men
`coverage_summary.price_status_counts.published_2026` står kvar på 78
(`optimate-fjarrvarme-2026.json:46-53`). Det är en maskinläsbar levande summa, inte den
frusna kontrollmängden 92.

Samtidigt tillåter `_TILLATNA_SKILLNADER` i Batch 3b-provet att `issues`,
`production_ready`, `calculation_status`, `component_completeness` och
`raw_data_validation` glider fritt. Handoff 001 tillåter bara ID, etikett,
`variant_of`, effektmetod och spärrstatus. Särskilt `issues` påverkar aktiveringsgrinden
och får inte normaliseras bort ur driftsskyddet.

#### Krävd rättning

- Sätt den levande `published_2026`-summan till 86 och lägg ett invariantprov som räknar
  `price_status` ur de faktiska tariffobjekten.
- Snäva paritetsallow-listan till handoffens uttryckliga undantag. Nuvarande objekt är
  redan lika i de extra metadatafälten, så detta ska inte kräva någon datamutation.

### P2 — två generiska fail-closed-bevis är ofullständiga

`valider_variant_lankar()` bygger `per_id` med en dictionary och kan därför själv tyst
kollapsa två föräldrar med samma ID. Produktionsvägen fångar visserligen dubletten i
det efterföljande `blockerade_tariff_ider()`, men den nya generiska funktionen och dess
direkta prov uppfyller inte löftet att föräldern ska vara unik. Lägg ett direkt prov på
dubblerad förälder samt feltypade `variant_of`-värden och låt variantvalideringen själv
eller en gemensam validerad ID-indexbyggare kasta.

`test_omkastad_katalogordning_paverkar_inte_id_harledningen` jämför samma rena funktion
med sig själv två gånger och omkastar aldrig en katalog. Ersätt det med ett verkligt
generatorprov som aktiverar de åtta i en isolerad kopia, kastar om tariffordningen och
jämför de parsade produkt-ID:na samt deras innehåll. Ordningen i den serialiserade JSON-
texten behöver inte vara identisk.

## Verifierat i denna granskning

- Officiella E.ON-PDF:er för Järfälla/Upplands-Bro, Malmö/Burlöv,
  Norrköping/Söderköping och Örebro/Kumla/Hallsberg bekräftar de katalogförda 2026-
  priserna. De två direkt öppnade dokumenten är två sidor och bekräftar ordagrant att
  36-månadersvärdet inkluderar fakturamånaden.
- Katalogdiffen lägger till exakt åtta variant-ID:n; inga tariff-ID:n tas bort. Exakt de
  åtta bastarifferna ändrar endast etikett och `source_refs`. Fyra nya källposter och
  fyra medlemskopplingar tillkommer; gamla `_0`-källposter är orörda.
- De åtta varianterna är fortsatt spärrade, `godkanda(katalog)==25`, katalogen har 86
  poster och skarp payload saknar `--bas-delvarme`.
- Riktad Python: **159 passed**. Hela tariffsviten:
  **1145 passed, 4 skipped**.
- TypeScript: **1028 passed i 38 filer**; `npx tsc --noEmit` godkänt.
- `git diff --check` är rent i berörda commitintervall.
- En helt oavgränsad pytest-körning från repo-roten samlar även orelaterade Milesight-
  tester och stoppas av saknade `pymodbus`-/`tests.*`-beroenden. Det motsäger inte den
  redovisade fulla tariffsviten och är inte ett Batch 3b-fynd.
- Direkt bytehämtning för oberoende SHA-omräkning mötte E.ON:s aktuella Cloudflare-403.
  Källposternas fyra SHA-värden har därför inte omräknats av Codex i denna runda; deras
  officiella URL, tvåsidiga innehåll, priser och metod har däremot kontrollerats.

## Nästa steg för Claude

Rätta exakt fynden ovan i en fokuserad lokal rättningsrunda. Behåll tariffspärrarna och
dispositionen **25/39/28 av 92**. Regenerera den fortfarande 25-produktiga skarpa
artefakten med endast de nu uttryckligen tillåtna metadataändringarna, kör full tariff-
Python, full TypeScript, `tsc`, isolerat bygge, E2E, generator-synk och
`git diff --check`, logga nya exakta lokala commit-hashar och stanna för omgranskning.

**Ingen aktivering. Ingen push.**
