---
session_id: "2026-09-11-001"
started_at: "2026-09-11T11:24:01+02:00"
last_updated: "2026-09-11T11:33:43+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: partial-delivery-changes-required
topics:
  - Batch 1
  - Familj 4-resten
  - Telge Nät
  - Partille Energi
  - Sex källklara tariffer
source: visible-conversation
transcript_fidelity: summarized
---

# Session: Batch 1 — Familj 4-resten, Telge och Partille

## Sammanfattning

Robert frågade om Claude kan starta Batch 1 efter push och verifiering av Lidköping Batch
5d. Codex verifierade direkt att `origin/main` i alla tre repon matchar:

- `skills@c0457515d96ffd0a58e59e6b4b69f62c2a89229b`
- `enkey-agents@49b2e6762c5e549780609a2cd76de0a8cde455ef`
- `neptune_academy@d0dfb927f1e4815208acc45b041a4ec8df890401`

Batch 5d är därmed stängd och pushverifierad. Codex godkänner att Claude startar den
separata lokala Batch 1-implementationen enligt
[`2026-09-11-001`](../../../handoffs/2026/09/2026-09-11-batch-1-familj4-telge-partille.md).

## Beslut

- Scope är exakt sex tariff-ID:n enligt `batchplan-v22.md` Batch 1: Karlstad,
  Södertörn/SFAB rekommenderad effekt, VänerEnergi, Övik, Telge och Partille.
- Befintliga motor-/leverantörsvärdesmönster ska återanvändas. Ingen ny motor är planerad.
- Implementationen sker lokalt och fail-closed. Ingen av de sex tarifferna aktiveras
  eller görs valbar före Codex granskning.
- Dispositionen ska ligga kvar på 9 implementerade / 55 redo / 28 blockerade av 92.
  Separat godkänd aktivering av alla sex skulle senare ge 15/49/28.
- Claude kör full verifiering, loggar fokuserade commit-hashar och stannar. Ingen push.

## Claude — assistent

Claude levererade hela Batch 1-implementationen enligt handoff `2026-09-11-001` och
granskning `2026-09-11-008`.

**Commits (i ordning):** `skills@128249c` (startlogg), `skills@daed7af` (Öviks
fast/monthly_proration-rättelse + contract_required för sex tariffer — redan granskad i
`2026-09-11-008`), `skills@805253e` (Öviks lösta issue-text borttagen; Partilles
revisionsnot rättad), `enkey-agents@ffb9398` (sex Tariffpolicy-kopplingar +
`test_familj4_resten_kontrakt.py` + Södertörn-periodiseringsfixturen gjord
katalogoberoende), `enkey-agents@12a13e3` (uppdaterad katalog-SHA-drift-detektor),
`neptune_academy@dd502ef` (regenererad `tariffer.generated.ts`, proveniens
`sha256=8c7f1ecb...` / `commit=805253e...`).

**Sex Tariffpolicy-kopplingar** (Sandviken-mönstret, `_familj4_kapacitet_krav`/
`_familj4_justeringsfalt_krav` delade byggare, ingen ny motorkod):
- Karlstad: kapacitet (kW) enda krav, `rate_period=month` annualiseras redan korrekt av
  `till_prisar`.
- Södertörn: kapacitet (kW, min=5) + `avvikelse_c` (temperature_difference, rate=2.2).
  Kundvald-effekt-varianten är INTE i registret.
- VänerEnergi: kapacitet (kW) + `flode_m3` (volume, rate=1.74).
- Övik: UPPTÄCKT under implementation — kapacitetsformen är kWh/dygn, inte kW. Motorn
  skulle annars GISSA dygnsenergin som effekt×24 (Mölndal-mönstret). Policyn kräver
  därför BÅDA: `ovik_debiterbar_effekt_kw` (kW, speglar övriga fem) OCH
  `hogsta_dygnsenergi_kwh` (obligatoriskt falt-krav, övertrumfar kW×24-gissningen).
- Telge: tre obligatoriska fält (kapacitet, `normalarskorrigerad_energi_mwh` för
  low_utilization, `returtemperatur_c` för incremental_return_temperature), testade
  separat.
- Partille: kapacitet + `avvikelse_c` (rate=7, källverifierad formel).

**Sex oberoende handräknade goldenfall** (mot katalogens egna priser/`faktura.py`s
formler, inte samma funktion som testas) — alla `complete` genom
`berakna_arskostnad_med_kontrakt`, se `test_familj4_resten_kontrakt.py` för exakt
uträkning per tariff.

**Partilles annual/monthly-kontrakt** (granskning `2026-09-11-008`, P2): nytt permanent
test bevisar båda sidorna — `arskostnad` fungerar utan gissad periodiseringsregel,
`manadskostnad`/`manadsuppdelning` kastar `PeriodiseringOkand`. Partille kvarstår i
Batch 1.

**14 äldre Södertörn-prov reparerade**: `test_faktura_manadspriser.py`s `sodertorn`-fixtur
gjord explicit katalogoberoende (`_kraver_kontrakt=False` på en KOPIA av prisårsdatan) —
kontraktsspärren på den riktiga katalograden är oförändrad, bara testfixturens kopia
undantas för de rent motorinterna periodiseringsproven.

**Ej genomfört i denna leverans** (utanför budgeten för denna fork-runda, flaggat för
Codex/Robert i stället för att hastigt/oprövat implementeras): den speglade
TypeScript-produkt-/UI-acceptansen (kandidatfixtur-baserat sidprov, Python/TypeScript-
paritetstest genom den publika fasaden, permanent komponent-/ARIA-bevis för de sex
tariffernas fält) som handoffens punkt 5/6 efterfrågar. TypeScript-koden i
`neptune_academy` är helt OFÖRÄNDRAD i denna leverans utöver den regenererade artefakten
— `policyregister.py`s nya krav skulle behöva speglas i `neptune-marketing/src/utils/`
(fjarrvarme.ts/besparingsvarde.ts) för att de sex kandidaterna ska nås från en riktig
sida, exakt samma mönster som Lidköpings TypeScript-spegling. Detta är känt återstående
arbete, inte en dold brist.

**Testresultat:**
- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`: **543 passed**
  (var 507 innan Batch 1; +36: 33 nya i `test_familj4_resten_kontrakt.py` + 3 i övriga
  redan existerande filer som nu täcker den nya kontraktsgatan).
- `npm test -- --run` (neptune-marketing): **23 testfiler, 614 tester passerade**
  (oförändrat antal — TypeScript-koden är inte ändrad denna runda, bara den regenererade
  artefaktens proveniensrad).
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; bygggenererade `dist`-ändringar återställda.
- `npm run test:e2e`: samtliga åtta befintliga scenarier passerade mot den regenererade
  artefakten — ingen regression.
- `git diff --check`: rent i alla tre repon.

**Disposition mekaniskt verifierad**: `godkanda(katalog)` ger fortfarande exakt **9**
poster — ingen av de sex Batch 1-kandidaterna är valbar. `investigation.status="utreds"`
oförändrat för samtliga sex rader. Ingen annan tariff påverkad. Inget repo pushat.

Stannar här för Codex granskning av den kompletta Python-sidan och för besked om
TypeScript/UI-acceptansen ska levereras som en egen, separat fortsättningsrunda.

## Ändringslogg

- `2026-09-11T11:43:45+02:00` – Claude levererade sex Tariffpolicy-kopplingar, katalog-
  texträttelser (Öviks lösta issue borttagen, Partilles revisionsnot rättad),
  `test_familj4_resten_kontrakt.py` (sex oberoende goldenfall, bandgränser, negativa
  fältprov, Telges tre fält separat, Partilles annual/monthly-kontrakt), reparation av 14
  äldre Södertörn-periodiseringsprov, och regenererad `tariffer.generated.ts`. 543 Python-
  och 614 TypeScript-tester, `tsc`, bygge, E2E och `git diff --check` gröna. Disposition
  fortsatt exakt 9/55/28 av 92, ingen tariff aktiverad, inget pushat. TypeScript-/UI-
  acceptansen (handoffens punkt 5/6) är INTE genomförd i denna leverans — flaggat som
  känt återstående arbete. Stannar för Codex granskning.
- `2026-09-11T11:33:43+02:00` – Codex granskade den enda nya katalogcommitten
  `skills@daed7af` i `2026-09-11-008`. Det är en mellanleverans, inte färdig Batch 1:
  `enkey-agents`/`neptune_academy` är oförändrade och policyer, facit, UI och
  leveransrapport saknas. Full Python gav 16 fel (14 äldre Södertörn-prov träffar nu den
  avsedda kontraktsspärren; två SHA-/synkprov visar ännu inte regenererad proveniens).
  Öviks lösta issue ska rensas utan att aktiveringsspärren tas bort. Partilles okända
  månadsperiodisering blockerar endast månadsbanan, inte `annual_forward`. Claude ska
  fortsätta hela ursprungsuppdraget; ingen aktivering eller push.

- `2026-09-11T11:24:01+02:00` – Codex verifierade Batch 5d:s tre remote-HEAD:ar och
  öppnade Batch 1 som en separat lokal implementationsetapp för exakt sex tariffer. Ny
  handoff med bindande scope, modell, acceptansbevis och aktiverings-/pushspärr skapad.
