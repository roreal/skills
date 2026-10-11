---
session_id: "2026-10-11-002"
started_at: "2026-10-11T19:47:10+02:00"
last_updated: "2026-10-11T20:20:00+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: active
topics:
  - Optimate
  - besparingspotential
  - våg 3f
  - Göteborg Energi
  - Partille Energi
  - Södertörns Fjärrvärme
  - temperaturdifferens
source: visible-conversation
transcript_fidelity: summarized
approved_by:
  - Robert
  - Codex
executed_by: Claude
dispatched_by: agent-bridge
---

# Optimate våg 3f — temperaturdifferens

## Start och beslut

Efter att våg 3e pushats, kvitterats och fjärrverifierats instruerade
Robert: **"Välj och starta nästa våg"**.

Codex inventerade de 24 återstående `not_reviewed`-produkterna. Tolv hör
till Wave 3 och tolv till den mer osäkra Vattenfall-familjen i Wave 4.
Nästa avgränsning blir exakt hela den återstående
`temperature_difference`-familjen:

- `goteborg-energi`;
- `partille-energi-partille`;
- `sodertorns-fjarrvarme-sodertorns-fjarrvarme`.

Gruppen är tekniskt sammanhållen genom samma befintliga tariffjustering,
men backendvalet förblir explicit: Göteborg använder den befintliga
legacy-årskostnadsvägen, Partille och Södertörn kontraktsmotorn. Endast
styrbar rumsvärme minskas; effekt, band och `avvikelse_c` låses. Det
prognostiseras alltså ingen separat returtemperatur- eller effektbesparing.

Live-baser före start:

- Neptune `origin/main=f13187af603ae131271331b5840f5ceb269dcaf0`;
- skills `origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1`.

Startdispositionen är **52 publika / 0 interna / 1 prototyp / 24
ogranskade = 77**. Målet för den interna, ej publika pilotleveransen är
**52/3/1/21=77**.

Se [implementeringshandoffen](../../../handoffs/2026/10/2026-10-11-optimate-vag-3f-temperaturdifferens.md).

Ingen publik aktivering, tariff-/formel-/UI-/Enkeyändring, mainflytt eller
push ingår i detta steg.

`APPROVED_FOR_IMPLEMENTATION: Claude`

## Implementation och verifiering (Claude)

Implementerat enligt handoffen, bakom befintliga interna spärrar. Ingen
publik aktivering, mainflytt eller push.

**Neptune** — isolerad worktree `/tmp/neptune-academy-optimate-vag-3f`,
gren `optimate-vag-3f-temperaturdifferens`, grenad från exakt verifierad
bas `f13187af603ae131271331b5840f5ceb269dcaf0`. Lokal commit
`573bd14225e4e5b198daed44b3d19e4ce940e240` "Starta Optimate våg 3f: intern
pilot för temperaturdifferens (Göteborg/Partille/Södertörn)" — ENDAST
lokal, ingen upstream-tracking, ingen push.

- `WAVE_3F_PRODUCT_IDS` tillagd i `optimateScenario.ts` (de tre ID:na,
  alfabetisk ordning), 3 nya `SCENARIO_PILOT_TARIFFER`-poster (Göteborg →
  `legacy_arskostnad`; Partille/Södertörn → `kontraktsgatad_kostnadsled`).
  `SCENARIO_PUBLIKT_AKTIVERADE_ID` orörd (fortsatt exakt 52, slutar på
  `...WAVE_3E_PRODUCT_IDS`) — alla tre förblir interna, ej publika.
- `besparingsvarde.ts`: `'goteborg-energi'` tillagd i
  `LEGACY_KOSTNADSLED_TILLATNA_TARIFFER` — enda ändringen i filen.
- Ny `optimateScenarioVag3f.test.ts` (76 egna prov): listinvarianter,
  katalogbindning, publicitets-FALSE-bevis för alla tre, tabellstyrt facit
  (handräknat, anropar inte produktionskoden), direkt legacy-backendprov
  för Göteborg, säsongskänslighet och ett oberoende teckentest som bevisar
  att en negativ `avvikelse_c` förblir en krympande bonus (aldrig fryst/
  absolutbelopp/nollklampad).
- Avvikelse från den bokstavliga fillistan: 6 befintliga provfiler
  (`optimateScenarioVag2/3a/3b/3c/3d/3e.test.ts`) fick sina hårdkodade
  `SCENARIO_PILOT_TARIFFER_SNAPSHOT`-längder/medlemskap uppdaterade
  52→55, eftersom de redan asserterar den FULLA snapshotens längd — samma
  underhållsmönster som våg 3e:s egen "Starta"-commit tidigare gjorde mot
  våg 3d:s fil. `SCENARIO_PUBLIKT_AKTIVERADE_ID`-proven (fortsatt 52)
  rördes inte.
- Facit: samtliga handräknade belopp (energi-/effekt-/temperaturled före,
  summa före, summa efter 10/15/20 %, referens inkl. moms, besparing)
  matchade handoffens tal exakt vid första försöket, för alla tre
  produkter. Ingen avvikelse att utreda.
- Testutfall (verifierat självständigt av Claude, inte bara rapporterat):
  nya filen 76/76; hela Vitest-sviten 3475/3475 (97/97 filer); `npx tsc
  --noEmit` rent; `npm run build` OK, genererad `dist/`-smuts återställd
  med `git checkout -- dist/`; `git diff --check` rent.

**skills** — lokal commit `d4597d5` "Lägg till Optimate våg 3f
(temperaturdifferens) som intern pilot i täckningsmatrisen", på `main`,
endast lokal (2 commits före `origin/main`, ingen push).

- `generera_besparingspotential_tackningsmatris.py`: 3 nya
  `SCENARIO_STATUS_REGISTRY`-poster, alla `godkand_intern_pilot_ej_publik`.
  Matris regenererad ENDAST via generatorn (`--write`), aldrig handredigerad.
- Avvikelse från den bokstavliga 3-fillistan:
  `test_generera_besparingspotential_tackningsmatris.py` uppdaterades också
  — 3 befintliga prov hårdkodade den gamla 24/0-dispositionen och saknade
  `godkand_intern_pilot_ej_publik` helt, så pytest hade fallit 3/56 annars.
- Verifierat självständigt av Claude: `python3 -I
  generera_besparingspotential_tackningsmatris.py --check` →
  "Täckningsmatrisen matchar 77 produkter och källhashen."; `pytest
  Fjarrvarmetariffer/test_generera_besparingspotential_tackningsmatris.py`
  → 56/56 godkända; `counts.scenario_review_status` i den regenererade
  JSON:en är exakt `{godkand_publik_10_15_20: 52,
  godkand_intern_pilot_ej_publik: 3, synlig_sarskild_preliminar_prototyp: 1,
  not_reviewed: 21}` = 77. `git status` i skills-repot visar samtliga
  tidigare ospårade/ändrade, orelaterade filer OFÖRÄNDRADE och ostagade.

Slutlig disposition: **52 publika / 3 interna / 1 prototyp / 21 ogranskade
= 77**, exakt målet. Ingen motorkod
(`beraknaOptimateScenario`/`beraknaArsprodukt*`/`arskostnad`/
`returtemperaturjusteringGoteborg`), tariffdata, prisformel,
policyregister, resultatkontrakt, kund-UI eller Enkey-fil ändrad.

`REVIEW_READY: Codex`
