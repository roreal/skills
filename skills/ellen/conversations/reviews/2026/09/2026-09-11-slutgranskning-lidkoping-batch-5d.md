---
review_id: "2026-09-11-004"
date: "2026-09-11"
reviewer: Codex
status: approved
scope:
  - "Slutgranskning av Lidköping Batch 5d efter rättningsrunda 7"
  - "Samtliga öppna krav i granskning 2026-09-11-003 samt den kumulativa lokala Batch 5d-leveransen"
reviewed_heads:
  skills: "b73b974971aceb550ef3fa7d79c0bd0b53122f48"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "09131a9089f35d00f99899df00aa4fbc16ec1da0"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: true
approved_activation_scope: "local-only; exakt två Lidköpingstariffer; ny Codex-granskning före push"
tariff_disposition_before_activation: "7 implemented / 57 ready / 28 blocked av 92"
tariff_disposition_after_approved_local_activation: "9 implemented / 55 ready / 28 blocked av 92"
follows_review: "2026-09-11-003"
---

# Slutgranskning av Lidköping Batch 5d

## Beslut

**Godkänd för en separat lokal aktiveringsetapp.** Rättningsrunda 7 stänger samtliga
återstående fynd i `2026-09-11-003`, och den kumulativa Batch 5d-implementationen för de
två Lidköpingstarifferna är därmed tekniskt färdig för att kopplas in i den genererade
produktionskatalogen.

Godkännandet innebär inte pushgodkännande. Tarifferna är fortfarande avstängda i de
granskade versionerna och dispositionen är fortsatt 7 implementerade / 57 redo / 28
blockerade av 92. Claude får nu göra en fokuserad **lokal** aktiveringsleverans för exakt
de två tariff-ID:na. Den leveransen ska stanna för en sista Codex-granskning innan något
repo pushas.

## Stängda fynd från rättningsrunda 7

- `MIN_POSITIVE_NUMERIC_FIELD = 1` är nu samma källa för HTML-attribut,
  JavaScriptgränser och svenska feltexter för area, MWh, kronor och eget energipris.
- Icke-kontraktsgatad kapacitet har HTML `min=1`, i linje med den befintliga
  positiv-heltalsregeln i JavaScript. Kontraktsgatade produktgränser ägs fortsatt av
  tariffpolicyn.
- Fakturafälten valideras nu före varje beräkningskonsument, inklusive
  `rawEnergyFranArskostnad` i kronläget. `validity.badInput` fångas från den verkliga
  formulärkontrollen, så ett värde som Chromium sanerar till tom sträng kan inte längre
  omtolkas som ett genuint tomt fält och falla tillbaka på tariffens standardvärde.
- Den permanenta komponentmatrisen provar area, MWh, kronor och eget pris under gränsen,
  exakt vid gränsen och med en giltig decimal. Kapacitet provas med noll, decimal och
  positivt heltal i både legacy- och kontraktsgatad väg.
- E2E-sviten bevarar de sex tidigare scenarierna och lägger till `area=0.5` samt ett
  verkligt Chromium-`badInput` för Göteborgs fakturafält.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **507 passed**.
- `npm test -- --run`: **21 testfiler, 594 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast den befintliga bundlevarningen. Bygggenererade
  `dist`-ändringar återställdes.
- `npm run test:e2e`: **samtliga åtta scenarier passerade** mot en ny
  produktionsbuild, inklusive riktig Chromium-`badInput`. `dist` återställdes.
- En separat headless Chromium-matris provade normal knappsubmit för area, MWh, kronor
  och eget pris med `0.5`, `1` och `1.5`, samt legacy-kapacitet med `0`, `3.5` och `10`.
  Alla 15 fall gav samma HTML- och JavaScriptutfall: värden under gränsen stoppades utan
  resultat, exakt gräns och tillåtna decimaler/heltal gav resultat. Inga `pageerror`
  uppstod.
- `git diff --check` är rent och båda produktrepona är rena. Sedan tidigare orelaterade
  filer i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude: lokal aktivering

Aktivera nu **endast** följande två tariff-ID:n lokalt:

- `lidkoping-energi-lidkoping-041-kw-2026`
- `lidkoping-energi-lidkoping-42-kw-2026`

Arbetsordning och acceptanskrav:

1. Avsluta bara de två katalogposternas nu lösta utrednings-/issue-spärrar. Bevara
   priser, band, formel, månadsperiodisering, obligatoriska Q/T/Tm-serier, attestering,
   `contract_required`, MWh-only och blockerad besparingsprodukt oförändrade. Gör inga
   andra tariffer valbara.
2. Gör först en fokuserad `skills`-commit som innehåller den exakta katalogändringen och
   nödvändiga styrande dispositions-/revisionsuppdateringar. Rör inte orelaterade
   ospårade eller modifierade filer.
3. Regenerera därefter `tariffer.generated.ts` med generatorn och den exakta
   `skills`-commit som faktiskt innehåller katalogbytesen. Redigera aldrig den genererade
   filen för hand. Proveniensens katalog-SHA och commit ska verifieras av synktestet.
4. Ändra permanenta tester där deras tidigare premiss var att den verkliga
   Lidköpingskatalogen fortfarande var `utreds`. Bevisa mot de **verkligt aktiva,
   genererade** posterna — inte bara muterade testkopior — att båda finns i
   produktväljaren, att explicit rätt band-ID krävs, att MWh-lägets aktuella
   årskostnad går genom hela sidan och att kr-/schablon-/besparingsvägarna fortsatt
   blockeras med avsedda orsaker.
5. Kör aktiveringspreflighten och hela verifieringsmatrisen: 507+-sviten i Python,
   594+-sviten i TypeScript, `tsc --noEmit`, produktionsbygge, självbärande E2E och
   `git diff --check`. Återställ bygggenererade `dist`-ändringar.
6. Verifiera mekaniskt att katalogens disposition efter aktiveringen är exakt
   **9 implementerade / 55 redo / 28 blockerade av 92**, och att ingen av de övriga 55
   redo- eller 28 blockerade posterna oavsiktligt passerar grinden.
7. Gör fokuserade lokala commits och logga fulla HEAD-hashar samt testresultat. Pusha
   inget repo. Stanna för Codex aktiverings-/pushgranskning.

Codex ändrade ingen produktkod, katalogdata eller aktiveringsstatus i denna granskning.
