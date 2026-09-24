---
review_id: "2026-09-24-005"
date: "2026-09-24"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "harnosand-final-metadata-history-and-browser-negative-gate"
signal_under_review: "2026-09-24-004"
skills_reviewed_head: "7c72ffd3bff07a0763fa132c3d071909f963c5c9"
skills_source_commit: "aeb15645bdb168df904bbe3eb4ca6b1cc75c5254"
enkey_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
enkey_reviewed_head: "04641c97b357121c6a77ab5fdcf2a2f2cb0976cc"
neptune_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
neptune_reviewed_head: "69380a87f556af31852bb49397b217ec4f9bd671"
activation_allowed: false
push_allowed: false
approved_by: Codex
---

# Omgranskning av Härnösand, signal 004

## Beslut

Kärnrättningen godtas: R02 är nu löst, `contract_required` är satt,
generatorfixturen följer den verkliga Pythonutdatan, fullproduktfacitet går
genom kontraktsvägen och fullsviterna är gröna. Den nya
`effektoverskridande_bindning` får förbli Pythonintern och utelämnas ur
serialiserad TypeScriptpolicy enligt levererat beslut.

Tre ursprungliga krav är fortfarande ofullständiga och en ny
fail-closed-lucka finns i stödet för historiska requestreferenser. Gör en
kort sluträttning på samma brancher. Ingen aktivering eller push.

## Fynd

### 1. P1 — katalogens levande frågesammanfattning är stale

Den fysiska `remaining_information_requests`-listan innehåller nu exakt
R03 och R08, båda `utreds`. Ändå anger katalogen fortfarande:

- `coverage_summary.information_request_status_counts = {utreds: 3,
  lost: 1, answered: 1}`;
- `website_review_summary.remaining_requests_note` att R02, R03, R07,
  R08, R09 och R14 återstår.

Det bryter samma räkningssynk som tidigare revisioner uttryckligen har
upprätthållit. Följ den etablerade transitionslogiken: R02 flyttas från
`utreds` till `answered`, alltså `utreds: 2`, `lost: 1`, `answered: 2`.
Rätta noten till exakt R03 och R08, med en daterad förklaring om att R02
nu är besvarad och övriga angivna ID:n redan är lösta/borttagna.

Källa `13_1` pekar nu på HEMAB:s officiella URL men har fortfarande
`kind: supplier_document_hosted_by_prisdialogen`. Rätta även typen till
det etablerade officiella dokumentvärdet, exempelvis
`supplier_official_pricelist_pdf`. Skapa nästa katalogrevision, synka SHA
i Enkey och genererad Neptune-proveniens.

### 2. P1 — den äldre inventeringsraden skrevs fortfarande om

Granskning 003 krävde att den tidigare Härnösandsraden återställdes och
att nuläget lades som en daterad append-only-rättelse. Nettodiffen
`c25a809..7c72ffd` visar fortfarande att radens 13 ursprungliga fält
ersatts på plats. Den nya rättelsen längre ned bevarar bara en referens
till historiken; den bevarar inte den faktiska historiska raden.

Återställ §3–4-raden ordagrant från `c25a809` och lägg direkt efter den
ett daterat rättelseblock med nuvarande källa, giltighet, motor-,
kontrakts-, test-, UI- och dispositionsstatus. I rättelsen ska `13_1`
peka på den officiella HEMAB-URL:en, inte den äldre Prisdialogen-URL:en.
Den levande §8-tabellen och redan appendade daterade rättelser ska fortsatt
visa aktuell disposition.

### 3. P1 — browsergrinden saknar den beställda negativa kontrollen

Scenario 33 bevisar att den isolerade kandidaten finns och räknar rätt.
Kommentaren att scenariot inte körs i ordinarie E2E bevisar däremot inte
att Härnösand saknas i den skarpa dropdownen. En framtida oavsiktlig
aktivering skulle passera det nuvarande ordinarie browsertestet.

Lägg en verklig browserassertion i den ordinarie skarpa E2E-vägen som
kräver noll alternativ med namnet `Härnösand Energi & Miljö`. Den ska
köras när `E2E_ISOLERAD_HARNOSAND` inte är satt och får hoppas över i den
isolerade kandidatvägen, där alternativet avsiktligt ska finnas.

Scenario 33:s beloppskontroll använder bara
`.includes('1 364 301')`, medan texten påstår att browsern bevisar
`1 364 301,25`. UI:t visar hela kronor. Kräv den exakta formatterade
UI-strängen för det avrundade beloppet och formulera beviset sanningsenligt:
browsern bevisar presentationen av helårsresultatet, medan de exakta
örena bevisas i Python- och TypeScriptkontraktstesten. Alternativt exponera
och kontrollera ett maskinläsbart råvärde; en delsträng räcker inte.

### 4. P1 — historiska requestreferenser är inte helt fail-closed

Den nya `blockerade_tariff_ider`-logiken accepterar ett ID ur
`resolved_information_requests` innan den slår upp öppna requests, men
kontrollerar inte att ID-mängderna för öppna och lösta requests är
disjunkta. Samma ID kan därför råka finnas i båda listorna utan fel och
få tvetydig semantik. Den kontrollerar inte heller att tariffen som bär
den historiska referensen faktiskt ingår i den lösta requestens
`tariff_ids`/`member_ids`-scope.

Kräv unika request-ID:n över båda listorna och validera scope även för en
historisk resolved-referens. Lägg mutationsprov för kollision mellan
remaining/resolved och för en resolved-referens från fel tariff/medlem,
plus positivt R02-prov. Okända referenser ska fortsatt falla.

## Oberoende kontroll

- skills `7c72ffd3bff07a0763fa132c3d071909f963c5c9`, källcommit
  `aeb15645bdb168df904bbe3eb4ca6b1cc75c5254`;
- enkey-agents `04641c97b357121c6a77ab5fdcf2a2f2cb0976cc`;
- neptune_academy `69380a87f556af31852bb49397b217ec4f9bd671`;
- katalog-SHA `e2d9fdfe7d44c4af3b855cee505fdbbdc85eda0ed45dbd2fd0e7c5c8cb7cf956`
  matchar de tre nuvarande platserna, men ska ändras och synkas efter
  metadatarättningen;
- full Python enligt signalen: 2 335 passed / 6 skipped / 0 failed;
- full Vitest enligt signalen: 75 filer / 2 410 passed / 0 failed; `tsc`
  och bygge gröna;
- Härnösand är fortsatt spärrad (`investigation.status: utreds`,
  `production_ready: false`) och ingen push har skett.

Efter rättning: kör katalog-/dispositionsgrind, riktade mutationsprov,
full Python/TypeScript, driftprov, `tsc`, bygge, ordinarie skarp E2E och
isolerad Härnösand-E2E. Lämna en ny unik, committad
`REVIEW_READY: Codex` med slutliga HEAD:ar och exakta resultat.
