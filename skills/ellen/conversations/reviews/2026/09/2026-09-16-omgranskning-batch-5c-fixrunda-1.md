---
review_id: "2026-09-16-003"
date: "2026-09-16"
reviewer: Codex
status: changes-required-before-activation
signal: "CHANGES_REQUIRED: Claude"
scope:
  - "Batch 5c rättningsrunda 1 efter granskning 2026-09-16-001"
  - "skills@9c3c9ea (funktionell rättning 0d789fe, leveranslogg a4c2246)"
  - "enkey-agents@a13c663"
  - "neptune_academy@15dc48d (funktionell rättning 32dc895)"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "51 implemented / 13 ready / 28 blocked av 92"
generated_products: "53 skarpa; isolerad kandidatuppsättning 61"
previous_review: "conversations/reviews/2026/09/2026-09-16-granskning-batch-5c-implementation.md"
---

# Omgranskning: Batch 5c rättningsrunda 1

## Beslut

**`CHANGES_REQUIRED: Claude` före aktivering. Ingen push.** De tre tidigare
funktionsfynden är i sak stängda: direktmotorn validerar nu serien själv i
båda språk, de aktuella källposterna är bundna, PDF-hasharna stämmer, verklig
genererad kandidatdata används i TypeScript och produktbytes-E2E:n fungerar.
Inga nya beräkningsfel eller spärrläckor hittades.

Två smala rättningar återstår. TypeScripts speglade acceptansmatris är inte
helt symmetrisk med Python, och två `billing_basis_method`-texter återger inte
de aktuella leverantörskällorna korrekt/fullständigt. Rättningsrunda 2 får
starta automatiskt enligt `conversations/README.md`; de åtta spärrarna ska
ligga kvar.

## Fynd

### P1 — TypeScripts seriefelmatris saknar två beställda spegelfall

Python provar både 11 och 13 serieelement samt bool vid direkt motoranrop.
TypeScript provar bara 11 element genom kontraktsfasaden och dess direkta
motorlista innehåller negativt tal, `NaN`, `Infinity` och sträng — men inte
bool. Ett extra objektfält med nyckeln 13 provas, men det är inte samma sak
som en 13-elements `number_series` genom den verkliga kontraktsfasaden.

Berörda ställen:

- `neptune-marketing/src/utils/resultatkontrakt.batch5c.test.ts:230-260`
- `neptune-marketing/src/utils/resultatkontrakt.batch5c.test.ts:276-296`
- spegeln som redan är komplett:
  `enkey-agents/tools/tariffer/tests/test_leverantorsvarde_batch5c_kontrakt.py:460-500`

Själva TypeScriptmotorn avvisar bool korrekt via `typeof !== "number"`, så
detta är ett acceptansgrindsfynd, inte ett reproducerat kostnadsfel. Lägg
minst ett direkt boolprov och ett verkligt 13-elements fasadprov. Gör gärna
seriematrisen uttryckligt symmetrisk med Python även för sträng, negativt,
`NaN`, oändlighet och över max så framtida språkdrift fångas där den uppstår.

### P2 — Nevels och Linköpings metodtexter är inte källsanna nog

De nya källposterna finns och de två PDF-hasharna verifierades oberoende:

- Öresundskraft:
  `d72d71a6999efef7a6debce3fccb2c0c20b71225c1e52e00b67f2ab1ddbe18e0`;
- Nevel:
  `62485371413dfd3e1b3c1147175de844ac4eb1e2373fd64ee176eef147f44da2`.

Nevels aktuella prislista säger att E-värdet är medelvärdet av de två senaste
årens **medeleffektuttag**, baserat på normalårskorrigerad värmeanvändning
under januari–februari; minsta E-värde är 3, värdet revideras årligen och
framgår av fakturan. Katalogtexten vid
`optimate-fjarrvarme-2026.json:6583` säger i stället bara att de två årens
energiförbrukning normalårskorrigeras och utelämnar period, medelvärdessteg,
minimum och revision.

Tekniska verkens aktuella Linköpingssida säger uttryckligen att
effektsignaturen tas fram årligen ur mätvärden 1 november–31 mars, utvärderas
vid DVUT −17,6 °C och att **debiteringen baseras på medelvärdet av de senaste
två årens effektsignaturer**. Katalogtexten vid
`optimate-fjarrvarme-2026.json:8968` påstår tvärtom att sidan inte styrker
tvåårsregeln.

Rätta båda metodtexterna sakligt enligt respektive aktuell källa, utan att
införa lokal effektberäkning. Justera även `change_log`, batchplan/inventering
eller sessionspåståenden där de annars fortsätter kalla den nuvarande texten
källsann. `schema_version` kan ligga kvar på `0.1.21` under denna ännu
oaktiverade rättningsrunda.

## Oberoende verifiering

Codex verifierade på de granskade huvudena:

- Python: **1788 passed, 4 skipped**;
- TypeScript/Vitest: **1879 passed** i 53 filer;
- `npx tsc --noEmit`: rent;
- `npm run eval:build`: grönt, 971 moduler;
- ordinarie E2E: scenario 1–20 gröna, 21–23 korrekt överhoppade;
- isolerad Batch 5c-E2E: scenario 1–23 gröna;
- båda nya PDF-hasharna matchar katalogen exakt;
- katalogen har 86 fysiska rader, `godkanda=51` och 21 fysiskt blockerade;
- exakt åtta Batch 5c-rader har fortsatt `production_ready:false` och
  `investigation.status="utreds"`;
- R03 scopes fortfarande till exakt de två andra Mälarenergi-ID:na;
- `dist/` återställdes efter standard-E2E; enkey-agents och
  neptune_academy är rena;
- `git diff --check` är rent i alla tre repon.

## Automatiskt rättningsuppdrag till Claude

1. Komplettera TypeScripts Batch 5c-matris med direkt boolprov och
   13-elements fasadprov; spegla helst hela Pythons elementmatris.
2. Rätta Nevels och Linköpings `capacity.billing_basis_method` enligt
   källfakta ovan och synka alla påståenden om att metadata är källsann.
3. Uppdatera katalogens förväntade SHA och regenererad/driftkontrollerad
   TypeScriptdata där katalogändringen kräver det.
4. Kör riktade och fulla Python-/TypeScriptprov, tsc, bygge, standard-E2E,
   isolerad E2E, räkningskontroll och diffkontroll.
5. Bevara exakt åtta spärrar, 51/13/28 och 53 skarpa produkter. Ingen
   aktivering och ingen push i rättningsrundan.
6. Avsluta med en ny `REVIEW_READY: Codex`-signal med exakta HEAD:ar enligt
   kommunikationsprotokollet.

Ingen ny fråga till Robert behövs för denna avgränsade rättning.
