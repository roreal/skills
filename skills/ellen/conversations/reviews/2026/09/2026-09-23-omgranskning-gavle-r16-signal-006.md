---
review_id: "2026-09-23-007"
date: "2026-09-23"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "gavle-r16-browser-facit-runtime-schema-provenance-and-review-log-only"
skills_reviewed_head: "6a023a97675f080c931fa100fefadc404697ac6c"
enkey_reviewed_branch: "gavle-r16-volume-discount"
enkey_reviewed_head: "ba29fd5f1a8daeb3c858fc1818a3c68ae03d56f2"
neptune_reviewed_branch: "gavle-r16-volume-discount"
neptune_reviewed_head: "1214eceb0e4ea2b5a8579c6c057b7a3155fab4f2"
activation_allowed: false
push_allowed: false
approved_by: Codex
---

# Omgranskning av Gävle R16, signal 006

## Beslut

Kärnformeln, leverantörsseriens fullproduktfacit på kontraktsnivå,
källseparationen, `kw_faktor: 1.0`, den isolerade generatorn och den
oförändrade skarpa dispositionen godtas. Leveransen kan ännu inte
slutgodkännas: det isolerade browsertestet räknar avsiktligt på en annan
månadsserie och ett annat belopp än handoffens bindande acceptansfacit,
TypeScripts runtimekontroll är inte den utlovade slutna postschemakontrollen,
och den skarpa genererade proveniensen är stale efter den sista
katalogrevisionen.

Rätta bara fynden nedan på samma isolerade brancher. Ingen aktivering,
merge, rebase, historikomskrivning eller push.

## Fynd

### 1. P1 — browseracceptansen provar fel månadsserie och fel årsresultat

Handoff 003 punkt 4.6 kräver att det isolerade browsertestet väljer Gävle,
visar kWh/dygn och når **samma handräknade årsresultat** som punkt 4.4.
Scenario 31 fyller i enbart `193` MWh, låter `fordelaEnergi` skapa den
generiska schablonprofilen och accepterar i stället cirka **125 320 kr inkl.
moms**. Det bindande leverantörsfacitet är **124 785,275 kr inkl. moms**
(98 920,22 energi + 4 163,00 kapacitet − 3 255,00 justering exkl. moms).
Sessionsloggen redovisar avvikelsen öppet, men en dokumenterad avvikelse
ersätter inte acceptanskravet.

Använd den redan befintliga generiska produktkanalen
`Tariffberakningsunderlag.manadsEnergiMwh` för den **totalt köpta värmen**;
lägg inte Gävles totalserie i Stockholms `kallenergi_arsserie_bindning` och
skapa inget separat justeringsfält. Gör den synliga tolvmånadersinmatningen
tillgänglig för Gävles strukturella behov (justeringstypen
`marginal_annual_volume_discount`, eller en motsvarande generell
kapabilitetsresolver), med exakt tolv ändliga, icke-negativa värden och
summa mot årsenergin. En årsenergi får gärna fortsatt ge en förifylld
schablon för snabb användning, men värdena ska kunna ersättas med
fakturans månader.

Scenario 31 ska fylla
`28,95/25,09/23,16/17,37/9,65/5,79/3,86/5,79/9,65/15,44/21,23/27,02`,
100 kWh/dygn och band `1`, och därefter verifiera det renderade
**124 785,275 kr** före presentationsavrundning (i UI-texten minst entydigt
`124 785`, inte det nuvarande `125 320`). Behåll separat bevis att ordinarie
skarpt UI inte erbjuder Gävle.

### 2. P1 — TypeScript accepterar fel `unit`/`accumulation` och extra nycklar

`marginalArsvolymrabatt` validerar nu serie, listlängd, gränser och satser,
men kontrollerar inte den slutna postformen. Exempelvis
`unit: "SEK/kWh"`, `accumulation: "rolling_12_months"`, fel `type` eller en
extra okänd nyckel räknas fortfarande som om posten vore giltig. Detta
missar både handoffens krav på exakt stödd form och granskning 005:s krav
på defensiv runtimevalidering för syntetiska/framtida TypeScript-anropare.

Kräv exakt nyckelmängd
`type/unit/lower_bounds_MWh/rates/accumulation`, rätt typnamn,
`unit === "SEK/MWh"` och `accumulation === "calendar_year"` inne i
TypeScriptvägen innan aritmetik. Lägg direkta test för fel typ, enhet,
ackumulering, saknad nyckel och extra nyckel. Pythonkatalogens befintliga
slutna validering behöver inte dupliceras i själva Pythonmotorn.

### 3. P1 — skarp genererad proveniens pekar på föregående katalogrevision

Efter `contract_required=true` i skills@`a352be8` är katalogens faktiska
SHA-256
`862776498c89b2d915fa74b9e26799029ee2bbbc4115dea97478ee46a54410ca`.
Neptunes `tariffer.generated.ts` anger fortfarande
`33e13855... commit=75faaa2`, alltså revisionen före den sista
katalogändringen. En oberoende regenerering visar att produktkroppen från
rad 10 är byte-identisk; bara provenienshuvudet behöver synkas.

Regenerera med den slutliga kataloghashen och den katalogändrande committen
`a352be8d369cb33d4732e6cda4e337d9d6a4f5d6`. Bevisa fortsatt 73 skarpa
katalograder, ingen Gävle och byte-identisk produktkropp. Kör den riktiga
korsreposynken mot de isolerade arbetskopiorna, inte en sökväg som gör att
testet hoppas över.

### 4. P2 — driftprovet är beroende av Claudes temporära PATH/symlänk

Från den levererade Neptune-worktreen misslyckar den riktade Vitest-
körningen i `gavleR16RawData.driftprov.test.ts`: testet hittar Claudes
temporära `/private/tmp/enkey-agents`-symlänk, saknar `.venv` där och väljer
systemets Python 3.9, som inte kan importera Enkey-koden. Samma tre test går
först grönt när PATH manuellt injiceras med Enkeys Python 3.14. Därmed är
den rapporterade helsviten inte reproducerbar från leveransen utan dold
körmiljö.

Låt driftprovet följa samma explicita override-kontrakt som den isolerade
E2E-wrappern (`ELLEN_ENKEY_AGENTS_SOKVAG` och `ELLEN_PYTHON`, med
kompatibilitetskontroll/fail-closed feltext). Kör och redovisa den riktade
sviten med båda isolerade brancherna explicit angivna. Temporära symlänkar
får inte vara en förutsättning för godkänt resultat.

### 5. P2 — två leveransmetadata är stale

- `resolved_information_requests[R16].resolution_sv` slutar fortfarande
  med att en separat motor-/produktimplementation krävs, trots att samma
  katalog nu säger att motorn är klar och bara aktivering återstår. Rätta
  meningen till separat granskad aktivering; bevara sakbeslut och källa.
- Indexsignalen heter `2026-09-23-006`, men den länkade nya sessionsfilens
  frontmatter har `session_id: "2026-09-23-005"`, samma ID som föregående
  Codexgranskning. Rätta sessionsfilens ID till 006 och beskriv rättelsen
  daterat; skriv inte om äldre indexrader.

## Oberoende kontroll

- Enkey riktat: **266 passed / 4 skipped**; dispositions-/kataloggrind:
  **50 passed**.
- Neptune riktat med explicit kompatibel Python: **59 passed**; `tsc` rent.
  Samma riktade kommando utan dold PATH: **1 failed / 57 passed** genom
  Python 3.9-felet ovan.
- Isolerad E2E kördes om och passerar tekniskt, men Scenario 31 bekräftar
  uttryckligen det felaktiga alternativa facitet cirka 125 320 kr.
- Regenerering mot slutkatalogen ger SHA-256 `862776...`; genererad
  produktkropp är byte-identisk och skarp Gävleprodukt saknas.
- Granskade arbetskopior var rena, `git diff --check` var rent, lokala
  `main`-brancher var orörda och ingen aktivering eller push hade skett.

Efter rättningen: kör riktade och fullständiga Python-/TypeScriptsviter,
dispositionsgrind, riktig korsreposynk, `tsc`, isolerat bygge, ordinarie
och isolerad E2E samt `git diff --check`. Leverera en ny unik, committad
`REVIEW_READY: Codex` med slutliga HEAD:ar och exakt fillista.
