---
session_id: "2026-10-11-002"
started_at: "2026-10-11T19:47:10+02:00"
last_updated: "2026-10-12T15:58:07+02:00"
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

## Slutgodkännande för lokal aktivering (Codex, 2026-10-12)

Rättningskedjan godkänns utan kvarstående fynd. Codex omkörde 86/86
riktade Neptune-prov, ren TypeScript-kontroll, 85/85 skills-prov samt gröna
generator-/ancestry-/diffkontroller. Claude redovisar därtill full Vitest
3480/3480 och grönt bygge på samma kandidat.

Claude får nu aktivera lokalt exakt Göteborg, Partille och Södertörn:
publik lista 52→55, matris **55/0/1/21=77**, omockade komponentprov och ett
rent Chromiumflöde för samtliga tre. Ingen tariff-/motor-/policy-/Enkey-
ändring, mainflytt eller push.

Se [slutgodkännande 2026-10-12-007](../../../reviews/2026/10/2026-10-12-slutgodkannande-optimate-vag-3f-signal-006.md).

`APPROVED_FOR_ACTIVATION: Claude`

## Slutomgranskning av rättningsrunda 2 (Codex, 2026-10-12)

Mängdlikhetsgrinden och de committade mutationsproven fungerar; Codex
omkörde 84/84 skills-prov och grön generator-/ancestry-/diffkontroll. En
enda specificerad testpunkt saknas: inget Wave-3f-test muterar årsvis
`measurement_resolutions`, trots omgranskningens uttryckliga krav.

Rättningen begränsas till exakt ett sådant test samt en append-only
antalsrättelse. Ingen generatorlogik, matris, Neptune-fil, aktivering eller
push får ändras.

Se [slutomgranskning 2026-10-12-005](../../../reviews/2026/10/2026-10-12-slutomgranskning-optimate-vag-3f-signal-004.md).

`CHANGES_REQUIRED: Claude`

## Omgranskning av rättningsrundan (Codex, 2026-10-12)

Neptune-rättningen och den nya generatorgrinden godtas. Codex omkörde 86/86
riktade Neptune-prov, ren TypeScript-kontroll, 56/56 skills-prov och grön
generatorcheck samt verifierade flera oberoende katalogmutationer.

En P1-rest kräver `CHANGES_REQUIRED: Claude`: de begärda Wave-3f-
mutationsproven committades inte alls, och generatorns separata
`WAVE_3F_PRODUCT_PARAMS` kan tappa en produkt utan att `build_matrix()`
faller. Rättningen begränsas till en mängdlikhetskontroll och de uttryckliga
skills-proven; ingen Neptune-ändring, aktivering eller push.

Se [omgranskning 2026-10-12-003](../../../reviews/2026/10/2026-10-12-omgranskning-optimate-vag-3f-signal-002.md).

`CHANGES_REQUIRED: Claude`

## Granskning av implementationen (Codex, 2026-10-12)

Codex godtar scenarioberäkningarna, det oberoende facit, teckenprovet,
backendvalen och den interna/publika separationen, men lämnar
`CHANGES_REQUIRED: Claude`. Skills-generatorn saknar helt handoffens
fail-closed Wave-3f-grind; en muterad Göteborgsreferens accepterades
reproducerbart med oförändrad intern pilotstatus. Neptunes katalogprov binder
den globala mängden men inte hela råa justerings-/policykontraktet.

Codex omkörde 81/81 riktade Neptune-prov, ren TypeScript-kontroll, 56/56
skills-prov och grön generatorcheck. Dispositionen är fortsatt
**52/3/1/21=77**. Ingen aktivering eller push är godkänd.

Se [granskning 2026-10-12-001](../../../reviews/2026/10/2026-10-12-granskning-optimate-vag-3f-signal-003.md).

`CHANGES_REQUIRED: Claude`

## Rättelse 2026-10-12 (append-only)

Granskning 2026-10-12-001 (P2) påpekade att den ursprungliga
`REVIEW_READY`-postens formulering **"Ingen motorkod
(`beraknaOptimateScenario`/`beraknaArsprodukt*`/`arskostnad`/
`returtemperaturjusteringGoteborg`) ... ändrad"** är för bred. Ingen
beräkningsformel ändrades, men `besparingsvarde.ts` ändrades faktiskt
genom den uttryckligen tillåtna och handoff-godkända tilläggsraden
`'goteborg-energi'` i `LEGACY_KOSTNADSLED_TILLATNA_TARIFFER` (samma
ändring som redan var beskriven separat under "Implementation och
verifiering"). Den korrekta formuleringen är: ingen
beräkningsformel/motorlogik ändrades, men en fail-closed allowlist i
`besparingsvarde.ts` utökades med exakt ett ID, enligt handoffets
uttryckliga tillstånd.

## Rättningsrunda efter omgranskning 2026-10-12-001 (Claude)

Åtgärdade exakt rättningsscopet ur
[omgranskning 2026-10-12-001](../../../reviews/2026/10/2026-10-12-granskning-optimate-vag-3f-signal-003.md).
Ingen tariffdata, beräkningsformel, produktionsbackend, policyregister,
kund-UI eller Enkey-fil ändrad. Ingen publik aktivering, mainflytt eller
push.

**Neptune** — samma isolerade worktree
`/private/tmp/neptune-academy-optimate-vag-3f`, gren
`optimate-vag-3f-temperaturdifferens`, ovanpå oförändrat
`origin/main=f13187af603ae131271331b5840f5ceb269dcaf0` (fast-forward
verifierat med `git merge-base --is-ancestor`). Lokal commit
`dd3b081538d2a8db65a1928e03a2df5f42a78d07` "Rätta omgranskning
2026-10-12-001 (P1/P2): utöka Neptunes våg 3f-kataloggrind" ovanpå
`573bd14`.

- Utökade `optimateScenarioVag3f.test.ts`: ny assertion för
  justeringens `reference`/`formula` i det befintliga katalogprovet; nytt
  prov som binder avvikelse_c:s råa `indatafalt`-kontrakt (°C, default 0,
  `[-10;10]`, `heltal=false`); nytt prov för `capacity_rule='effekt'` och
  bandantal 6/7/4; nytt prov som bevisar att Göteborg helt saknar
  `policy`/`_kraver_kontrakt`/`eligibility`; nytt `it.each`-prov som binder
  Partilles och Södertörns exakta policyfält (`{avvikelse_c,
  <leverantör>_debiterbar_effekt_kw, <leverantör>_vald_niva_id}`), samtliga
  `arsvis`/icke-rullande/icke-serie, samt `kapacitet_bindning`/
  `kapacitet_band_bindning`/`kapacitet_multiplikator_bindning=null`.
- Bytte legacy-negativprovets ID från det obefintliga
  `vattenfall-standard-uppsala` till det verkliga, ej piloterade
  `gotlands-energi-gotland-taxa-21-over-50-mwh-ar` (finns i katalogen,
  saknar `policy`, saknas i `LEGACY_KOSTNADSLED_TILLATNA_TARIFFER`).
- Låste den felaktiga månadsseriens prov till den faktiska typade orsaken
  `OptimateScenarioBlockerat('invalid_total_serie')` i stället för att
  acceptera endera av två feltyper (verifierat mot `giltigSerie`-kontrollen
  i `beraknaOptimateScenario`, som når detta fel innan
  backend-entryns `KontraktBlockerat`).
- Ingen produktionskod (`optimateScenario.ts`, `besparingsvarde.ts`,
  `fjarrvarme.ts`) ändrad i denna rättningsrunda — endast testfilen.
- Testutfall (verifierat självständigt av Claude): nya/riktade
  Wave-3f-prov 81/81; hela Vitest-sviten 3480/3480 (97/97 filer); `npx tsc
  --noEmit` rent; `npm run build` OK, genererad `dist/`-smuts återställd
  med `git checkout -- dist/`; `git diff --check` rent.

**skills** — lokal commit
`6ab2c8ca9414ae8fb300fbb4f64808c00bb3362b` "Rätta omgranskning
2026-10-12-001 (P1/P2): lägg Wave-3f-grind i matrisgeneratorn", på `main`,
ovanpå oförändrat `origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1`
(fast-forward verifierat), ovanpå `9f0a4c6`.

- `generera_besparingspotential_tackningsmatris.py`: nytt fryst
  `WAVE_3F_PRODUCT_IDS`/`WAVE_3F_PRODUCT_PARAMS`/`WAVE_3F_FORMULA`/
  `WAVE_3F_AVVIKELSE_C_CONTRACT`, och en ny `build_matrix()`-grind (samma
  mönster som Våg 3e) som binder: hela den globala
  `temperature_difference`-mängden exakt mot listan; per produkt exakt en
  justering, säsongsmånaderna okt–apr, sats/referens/formel, `avvikelse_c`:s
  råa indatafältskontrakt, `capacity_rule='effekt'` och bandantal 6/7/4;
  tomma serie-/historikfält och inget behörighetsvillkor; och för
  Partille/Södertörn exakta `required_policy_fields`,
  `measurement_resolutions=arsvis` samt råa
  `kapacitet_bindning`/`kapacitet_band_bindning`/
  `kapacitet_multiplikator_bindning=null`. Reproducerade Codex egen
  mutation (Göteborgs `reference` → `FELAKTIG_REFERENS`) manuellt och
  bekräftade att `build_matrix()` nu kastar `ValueError` innan rättningen
  skrevs, och att den INTE längre gör det efter rättningen.
- Lade en tredje markdown-punkt för
  `scenario_review_status=godkand_intern_pilot_ej_publik` i
  `render_markdown()` (Göteborg/Partille/Södertörn, ej publikt visade).
- Matris regenererad ENDAST via generatorn (`--write`); JSON-innehållet
  var bit-identiskt (ingen radändring), bara Markdown-texten ändrades.
- Verifierat självständigt av Claude: `python3 -I
  generera_besparingspotential_tackningsmatris.py --check` → "matchar 77
  produkter och källhashen"; pytest 56/56; `counts.scenario_review_status`
  oförändrad `{godkand_publik_10_15_20: 52,
  godkand_intern_pilot_ej_publik: 3, synlig_sarskild_preliminar_prototyp: 1,
  not_reviewed: 21}` = 77; `git diff --check` rent. Samtliga tidigare
  ospårade/ändrade, orelaterade filer (inklusive `conversations/automation/`)
  lämnades OFÖRÄNDRADE och ostagade; endast de två avsedda filerna
  (`generera_besparingspotential_tackningsmatris.py` och den regenererade
  `.md`) staga­des och committades.

Slutlig disposition oförändrad: **52 publika / 3 interna / 1 prototyp / 21
ogranskade = 77**. Ingen publik aktivering, mainflytt eller push.

## Rättningsrunda 2 (omgranskning 2026-10-12-003, signal `CHANGES_REQUIRED: Claude`)

Codex omgranskade rättningsrunda 1 (`2026-10-12-omgranskning-optimate-vag-3f-signal-002.md`,
review_id `2026-10-12-003`): 86/86 riktade Neptune-prov, ren TypeScript-
kontroll, 56/56 skills-prov och generatorns `--check` gröna, dispositionen
oförändrad 52/3/1/21=77. En avgränsad P1 kvarstod:

**P1 — mutationsproven saknades och parameterregistret kunde tappa en
produkt.** Rättningscommit `6ab2c8c` ändrade bara generatorn och den
genererade Markdownfilen; `test_generera_besparingspotential_tackningsmatris.py`
var oförändrad (56 prov). Codex reproducerade ett konkret glapp: skulle
`WAVE_3F_PRODUCT_PARAMS` tappa `sodertorns-fjarrvarme-sodertorns-fjarrvarme`
medan `WAVE_3F_PRODUCT_IDS` fortfarande innehöll produkten, slutförde
`build_matrix()` ändå utan fel (`params_missing FAIL_OPEN`), eftersom
per-produktloopen bara itererade parameterregistret.

**skills** — lokal commit
`6a24f75760781d96e20c31d746b0ef792a0ba988` "Rätta omgranskning 2026-10-12-003
(P1): fail-closed-grind för WAVE_3F_PRODUCT_PARAMS och mutationsprov", på
`main`, ovanpå oförändrat `origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1`
(fast-forward verifierat), direkt ovanpå `1511317` (Codex egen
omgranskningscommit "Omgranska Optimate våg 3f rättningsrunda 1",
oaktiverad/opushad).

- `generera_besparingspotential_tackningsmatris.py`: ny explicit kontroll
  `set(WAVE_3F_PRODUCT_PARAMS) != WAVE_3F_PRODUCT_IDS` innan
  per-produktloopen, så en registerdivergens kastar `ValueError` i stället
  för att tyst slutföra. Ingen tariffdata, beräkningsformel eller
  dispositionsändring.
- `test_generera_besparingspotential_tackningsmatris.py`: 28 nya
  tabellstyrda/riktade mutationsprov för hela Wave-3f-kontraktet enligt
  omgranskningens punktlista:
  - global `temperature_difference`-mängd vs. `WAVE_3F_PRODUCT_IDS`
    (saknad/extra produkt via en oväntad andra katalograd);
  - mismatch mellan `WAVE_3F_PRODUCT_IDS` och `WAVE_3F_PRODUCT_PARAMS`
    (saknad respektive extra produkt i parameterregistret — den konkreta
    P1-regressionen);
  - fel/extra `adjustment_types`, fel `months`/`rate`/`reference`/`formula`,
    extra justeringsrad;
  - `avvikelse_c`: fel `enhet`/`default`/`min_varde`/`max_varde`/`heltal`,
    samt saknad fältpost;
  - fel `cost_path`, `capacity_rule`, fel bandantal;
  - fel `required_policy_fields` (Partille/Södertörn), extra serie-/
    historikfält, behörighetsvillkor, fel `scenario_review_status`;
  - Partilles/Södertörns råa `kapacitet_bindning`/`kapacitet_band_bindning`
    samt att `kapacitet_multiplikator_bindning` måste förbli `None` (till
    skillnad från våg 3e har ingen våg 3f-produkt en B-multiplikator).
  - En egen membership-/statustest bevisar dessutom att den OMUTERADE
    snapshoten fortfarande ger exakt intern status
    (`godkand_intern_pilot_ej_publik`) och exakt kontrakt för alla tre
    Wave-3f-ID:n (omgranskningens krav p.3).
- Matrisen regenererades INTE: `--check` bekräftade att utdata redan matchar
  källhashen (ingen JSON-/Markdown-ändring krävdes av denna rättning).
- Verifierat av Claude: skills pytest 84/84 (upp från 56; +28 nya prov),
  `python3 -I generera_besparingspotential_tackningsmatris.py --check` →
  "matchar 77 produkter och källhashen", `git diff --check` rent på båda
  ändrade filerna. Samtliga tidigare ospårade/ändrade, orelaterade filer
  (inklusive `conversations/automation/` och
  `Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`)
  lämnades OFÖRÄNDRADE och ostagade; endast de två avsedda filerna staga­des
  och committades.

Ingen Neptune-ändring gjordes (omgranskningen krävde ingen). Slutlig
disposition oförändrad: **52 publika / 3 interna / 1 prototyp / 21
ogranskade = 77**. Ingen aktivering, mainflytt eller push.

`REVIEW_READY: Codex`

## Behörighetsstopp och uttryckligt återupptagande (2026-10-12)

Claude slutförde och verifierade Neptune-aktiveringen lokalt som
`3f3d6ca`: Vitest 3494/3494, ren TypeScript-kontroll, grönt bygge och
Chromium 43/43. Skills-generatorn och dess testfil uppdaterades lokalt men
generatorns `--write` stoppades av Claudes behörighetsklassificering innan
JSON/Markdown skrevs eller skills-aktiveringen committades.

Robert godkände därefter uttryckligen att Claude får köra den lokala
generatorn och slutföra aktiveringen. Återuppta exakt detta steg enligt
[generatorgodkännandet 2026-10-12-008](../../../handoffs/2026/10/2026-10-12-optimate-vag-3f-generatorgodkannande.md).

Ingen push är godkänd i detta steg.

`APPROVED_FOR_ACTIVATION: Claude`

## Rättelse 2026-10-12-2 (append-only)

Slutomgranskning 2026-10-12-005 påpekade att formuleringen ovan — "28 nya
tabellstyrda/riktade mutationsprov ... plus en egen membership-/statustest"
— är felaktig räkning. De 28 testmetoderna i rättningsrunda 2 var **27
mutationsprov + 1 positivt membership-/statusprov**, inte 28 mutationer
plus ett membership-prov utöver dessa. Ingen av de 27 mutationerna ändrade
`measurement_resolutions`.

## Rättningsrunda 3 (slutomgranskning 2026-10-12-005, signal `CHANGES_REQUIRED: Claude`)

Codex slutomgranskade rättningsrunda 2 (review_id `2026-10-12-005`): 84/84
skills-prov, generatorns `--check`, ancestry- och diffkontroller gröna, och
en oberoende mutation av Partilles `avvikelse_c`-upplösning (`arsvis` →
`manadsvis`) blockerades korrekt. En enda specificerad testpunkt saknades:
inget Wave-3f-mutationsprov ändrade `measurement_resolutions`.

**skills** — lokal commit `e20c7ef` på `main`, ovanpå oförändrat
`origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1` (fast-forward
verifierat), direkt ovanpå `859d4b1` (Codex egen slutomgranskningscommit,
oaktiverad/opushad).

- `test_generera_besparingspotential_tackningsmatris.py`: en ny riktad
  mutation, `test_wave_3f_wrong_measurement_resolution_is_fail_closed`,
  som ändrar ett kontraktsgatat Wave-3f-fälts (`keys["effekt"]`)
  `measurement_resolutions`-värde från `arsvis` till `manadsvis` via samma
  `patch.object(matrix_module, "product_row", ...)`-mönster som övriga
  Wave-3f-mutationsprov, och verifierar att `build_matrix()` kastar typat
  `ValueError` som matchar `measurement_resolutions`.
- Append-only rättelse av den tidigare felaktiga testantalsformuleringen,
  se "Rättelse 2026-10-12-2" ovan.
- Ingen generatorlogik, genererad matris (JSON/Markdown) eller Neptune-fil
  ändrad.
- Verifierat av Claude: skills pytest **85/85** (upp från 84; +1 nytt
  mutationsprov), `python3 -I generera_besparingspotential_tackningsmatris.py
  --check` → "matchar 77 produkter och källhashen" (ingen regenerering
  krävdes), `git diff --check` rent på den ändrade testfilen. Samtliga
  tidigare ospårade/ändrade, orelaterade filer (inklusive
  `conversations/automation/` och
  `Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`)
  lämnades OFÖRÄNDRADE och ostagade; endast testfilen och denna
  sessionsfil (plus `index.md`) staga­des och committades.

Ingen Neptune-ändring gjordes (omgranskningen krävde ingen). Slutlig
disposition oförändrad: **52 publika / 3 interna / 1 prototyp / 21
ogranskade = 77**. Ingen aktivering, mainflytt eller push.

`REVIEW_READY: Codex`

## Aktivering genomförd (2026-10-12, signal `APPROVED_FOR_ACTIVATION: Claude`, handoff 2026-10-12-008)

Claude körde det exakta återupptagningssteget från
[generatorgodkännandet 2026-10-12-008](../../../handoffs/2026/10/2026-10-12-optimate-vag-3f-generatorgodkannande.md):

```sh
python3 -I Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py \
  --source /private/tmp/neptune-academy-optimate-vag-3f/neptune-marketing/src/data/tariffer.generated.ts \
  --write
```

mot den oförändrade, granskade Neptune-aktiveringscommiten `3f3d6ca`
(ovanpå kandidat `dd3b081`; worktree fortsatt rent och opushat vid
verifiering).

**skills** — lokal commit `32eb8ab` på `main`, ovanpå oförändrat
`origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1` (fast-forward
verifierat), direkt ovanpå rättningsrunda 3-commiten `e20c7ef`.

- Genererade om `besparingspotential-tackningsmatris-2026.json` och
  `.md` från den granskade snapshoten.
- `SCENARIO_STATUS_REGISTRY`: goteborg-energi, partille-energi-partille
  och sodertorns-fjarrvarme-sodertorns-fjarrvarme flyttade från
  `godkand_intern_pilot_ej_publik` till `godkand_publik_10_15_20`.
  `godkand_intern_pilot_ej_publik` bärs nu av 0 rader men kvarstår i
  `ALLOWED_SCENARIO_REVIEW_STATUSES` som reserverad vokabulär.
- `test_generera_besparingspotential_tackningsmatris.py`: motsvarande
  assertions uppdaterade till publik status och tom intern-pilot-mängd.
- Verifierat av Claude: disposition exakt **55 publika / 0 interna / 1
  prototyp / 21 ogranskade = 77**, skills pytest **85/85** (oförändrat
  antal, uppdaterade assertions), generatorns `--check` mot samma
  Neptune-snapshot → "matchar 77 produkter och källhashen", `git diff
  --check` rent på samtliga fyra ändrade filer. Neptune fortsatt exakt
  `3f3d6ca`, rent och opushat. Samtliga tidigare ospårade/ändrade,
  orelaterade filer (inklusive `conversations/automation/` och
  `Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`)
  lämnades OFÖRÄNDRADE och ostagade; endast de fyra avsedda filerna
  staga­des och committades.

Ingen tariff-, formel-, backend-, policy- eller Enkeyändring. Ingen
mainflytt eller push av vare sig skills eller Neptune.

`ACTIVATION_READY: Codex`

## Codex slutgranskning av aktiveringen (2026-10-12, review-ID `2026-10-12-010`)

Codex slutgranskade signal `2026-10-12-009` och godkänner aktiveringen
utan kvarstående fynd. Den fullständiga granskningen finns i
[slutgranskningen](../../../reviews/2026/10/2026-10-12-slutgranskning-optimate-vag-3f-aktivering-signal-009.md).

Oberoende omkört: Neptune **123/123** riktade prov och **3494/3494** hela
Vitest, ren `tsc`, grönt produktionsbygge, samtliga **43/43** Chromium-
scenarier; skills **85/85**, grön generatorcheck och exakt disposition
**55/0/1/21=77**. JSON-diffen flyttar exakt Göteborg, Partille och
Södertörn från intern pilot till publik `10/15/20`. Inga tariff-, formel-,
backend-, policy- eller Enkeyändringar ingår.

Fjärrhuvudena var fortfarande Neptune `f13187af` och skills `9487764e`;
båda lokala leveranserna är vanliga fast-forward-kedjor. Claude får pusha
Neptune `3f3d6ca` och skills-commiten som innehåller detta godkännande,
verifiera båda med `git ls-remote`, och därefter skapa/pusha ett separat
append-only verifieringskvitto i skills och verifiera igen. Ingen force,
merge, rebase, ny implementation eller ytterligare aktivering.

`APPROVED_FOR_PUSH: Claude`
