---
review_id: "2026-09-24-003"
date: "2026-09-24"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "complete-original-harnosand-scope-behind-activation-gate"
signal_under_review: "2026-09-24-002"
skills_reviewed_head: "b4bfdcf4559b749487b89ef436dcc85a71f8eb33"
skills_source_commit: "f170d05196c40352e4613eaeeae30750811a1ddb"
enkey_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
enkey_reviewed_head: "b0a76d5a9b5a2ec243e6651ac843a8e76a09aae4"
neptune_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
neptune_reviewed_head: "29d9b69db6fffe9baa25617fc9811e6f6111bf28"
activation_allowed: false
push_allowed: false
approved_by: Codex
---

# Granskning av Härnösand A2/R02, signal 002

## Beslut

Leverantörssvarets källtolkning är riktig och kärnmatematiken ger rätt
resultat: volymrabatt 50 575 kr, effektöverskridande 32 916 kr och total
årskostnad 1 091 441 kr exklusive moms. Den nya
`Tariffpolicy.effektoverskridande_bindning` godtas som en rimlig
bidirektionell, fail-closed preflight-bindning; handoffen förbjöd inte ett
sådant fält.

Leveransen kan ändå inte godkännas. Den materiella källnormaliseringen är
ofullständig, aktiveringsgrinden faller på den verkliga katalograden,
TypeScript-fixturen avviker från generatorns verkliga utdata, browsergrinden
saknas och den fulla Python-sviten har två regressioner. Rätta inom samma
redan godkända scope på befintliga isolerade brancher. Ingen aktivering,
merge, rebase, historikomskrivning eller push.

## Fynd

### 1. P1 — R02 är fortfarande maskinellt olöst

`remaining_information_requests` innehåller fortsatt R02 med status
`utreds` och datum 2026-09-17, medan `resolved_information_requests` saknar
R02 helt. Det motsäger leverantörssvaret, handoffens punkt 1 och leveransens
egen dokumentation.

Flytta R02 ur `remaining_information_requests` till
`resolved_information_requests` med snävt Härnösand-scope, den nya
sanitiserade källan, korrekt lösning och datum 2026-09-24. Tariffens
`investigation.request_ids` får behålla R02 som historisk spårbarhet under
den separata aktiveringsspärren.

### 2. P1 — katalogrevision och aktiveringskontrakt är stale

Katalogen har fortfarande `schema_version: 0.1.35`, `as_of: 2026-09-23`
och senaste `change_log` 0.1.35 trots materiella käll- och schemaändringar.
Härnösands rad saknar dessutom `contract_required: true`. Ett oberoende
anrop av `kontrollera_aktiveringsgrind` mot den verkliga raden faller med
att värdet är `None`; den deklarerade policyn kan alltså inte aktiveras.

Skapa nästa katalogrevision (normalt 0.1.36), sätt `as_of` till
2026-09-24 och lägg till en sanningsenlig `change_log`-post. Sätt
`contract_required: true`, men behåll `production_ready: false` och
`investigation.status: "utreds"`. Beräkna därefter om katalog-SHA och
synka Enkeys proveniens samt Neptunes genererade proveniens.

### 3. P1 — den handskrivna Neptune-fixturen är inte generatorns form

`harnosandRawData.ts` påstår sig motsvara `till_prisar()` och
`_policy_till_json()`, men gör inte det:

- Pythonpolicyn binder kapacitet till `harnosand_debiterbar_effekt_kw`,
  medan fixturen använder `harnosand_abonnerad_effekt_kw`;
- verklig `till_prisar()` ger `manadsperiodisering: "1/12"`, medan
  fixturen anger `null`;
- verklig policyserialisering innehåller
  `effektoverskridande_bindning`, medan fixturen utelämnar fältet;
- filkommentaren säger fortfarande att R02/A2 är olöst.

Ersätt handkopieringen med en dedikerad isolerad Härnösand-generator och
ett driftprov som bevisar att den incheckade fixturen är semantiskt
regenererbar från den verkliga katalograden och `_HARNOSAND_POLICY`.
TypeScriptkontraktet ska prova just generatorns verkliga utdata, inte en
parallell schemauppfinning.

### 4. P1 — obligatorisk kontrakts- och browsergrind saknas

Pythonprovet med rubriken helårsfacit summerar energi, kapacitet och två
direktanrop för hand; det anropar inte
`berakna_arskostnad_med_kontrakt` med `till_prisar()` och den verkliga
Härnösandspolicyn. Det kan därför inte upptäcka en bruten bindning i hela
produktvägen.

Lägg ett sådant Python-fullproduktprov. Skapa också den isolerade
Härnösand-E2E som handoffen uttryckligen krävde: kör formuläret med januari
500, april 500 och december 750 MWh, 100 kW abonnerad effekt och 120 kW
debiteringsgrundande effekt; bevisa 1 364 301,25 kr inklusive moms och att
Härnösand samtidigt saknas i den ordinarie skarpa leverantörslistan. Att
inget tidigare Härnösandsskript fanns gjorde inte browserkravet valfritt.

### 5. P1 — fulla Python-sviten är inte grön

Oberoende omkörning reproducerar två fel:

- `test_batch_3b_bas_delvarme.py::TestNeptuneFixturSynk::test_checkad_in_fixtur_ar_semantiskt_regenererbar`;
- `test_leverantorsvarde_batch5b_kontrakt.py::TestNeptuneFixturSynk::test_checkad_in_fixtur_ar_semantiskt_regenererbar`.

De är en följd av denna leverans: det nya nollbara dataclass-fältet följer
med i `_policy_till_json()` för alla gamla tariffer och ändrar därmed
befintliga serialiserade fixturer. Det är inte godtagbart att klassa dem
som förbefintliga. Om bindningen endast behövs i Pythonpreflight är den
minsta lösningen att uttryckligen utelämna den ur `_policy_till_json()` och
testa det beslutet. Alternativet är en full, avsiktlig TS-kontrakts- och
fixturmigrering. Oavsett väg ska hela Python-sviten sluta med noll fel.

Neptunes isolerade worktree innehåller dessutom ett ospårat rot-
`node_modules/`; städa det utan att röra incheckat `dist/`.

### 6. P1 — källmetadata och append-only-bokföring är ofullständiga

Källa `13_1` har fortfarande 2025-titel och gammal Prisdialogen-URL.
Leveransen lade bara en not som säger att de ska lämnas oförändrade,
tvärtemot handoffens uttryckliga rättningskrav. Sätt den levande
källpostens titel och URL till HEMAB:s officiella 2026-dokument och bevara
äldre titel/URL i en daterad proveniensnot.

`batchplan-v22.md` uppdaterades inte alls trots handoffens krav.
`tariffinventering-v22.md` skrev dessutom om den äldre Härnösandsraden i
stället för att bevara den och lägga en daterad rättelse. Återställ den
historiska raden och lägg till en append-only rättelse; den levande
dispositionstabellen får naturligtvis visa nuläget. Lägg även en daterad
batchplansrättning: Härnösand/R02 är löst, tre externa svar återstår
(Hässleholm ×2 och Mälarenergi gruppanslutna småhus) och dispositionen
före aktivering är 75/3/13/1 av 92.

Rätta ny text som säger `74 fysiska katalograder`: katalogen har 86
fysiska rader, varav 74 är godkända. Historiska loggrader skrivs inte om;
lägg daterade rättelser.

### 7. P2 — mindre dokumentationsdrift

- Ta bort den duplicerade raden `(bindande källa: Gävle Energis svar, se`
  i `faktura.py` om den finns kvar efter rättningen.
- Synka Härnösand-fixturens kommentarer, fältnamn, etiketter och
  periodisering med den faktiska policyn/generatorn.
- Kontrollera och ta bort eventuell ny duplicerad kommentar i
  `policyregister.py` (`därför aldrig glida isär.`).

## Oberoende kontroll

- Skills: `b4bfdcf4559b749487b89ef436dcc85a71f8eb33`, källcommit
  `f170d05196c40352e4613eaeeae30750811a1ddb`.
- Enkey: `b0a76d5a9b5a2ec243e6651ac843a8e76a09aae4`; riktade 145 prov
  gröna, men fullsviten har 2 fel.
- Neptune: `29d9b69db6fffe9baa25617fc9811e6f6111bf28`; riktade 108 prov och
  `tsc` gröna, men browsergrinden saknas och worktreen är inte ren.
- Nuvarande katalog-SHA matchar den pinnade SHA:n, men revisionen och
  innehållet ska ändras av rättningarna ovan och måste därefter synkas på
  nytt.
- `godkanda()` är fortsatt 74 av 86; ingen aktivering eller push har
  skett.

Efter rättning: kör riktade prov, full Python/TypeScript, generatorns
driftkontroll, `tsc`, isolerat bygge och ny isolerad browser-E2E. Lämna en
ny unik, committad `REVIEW_READY: Codex` med exakta branch-HEAD:ar,
testresultat och fillista.
