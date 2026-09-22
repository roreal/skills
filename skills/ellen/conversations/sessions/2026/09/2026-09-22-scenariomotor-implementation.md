---
session_id: "2026-09-22-008"
started_at: "2026-09-22T13:44:00+02:00"
last_updated: "2026-09-22T15:40:00+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: active
topics:
  - Optimate
  - gemensam scenariomotor
  - Sundsvall-pilot
source: visible-conversation
transcript_fidelity: summarized
---

# Session: implementation av handoff 007 (gemensam scenariomotor, Sundsvall-pilot)

## Sammanfattning

Claude implementerade exakt scopet i
[handoff 2026-09-22-007](../../../handoffs/2026/09/2026-09-22-optimate-scenariomotor-sundsvall-pilot.md)
i Neptune, ovanpå oförändrad baslinje `main@86be35a`. Arbetet delegerades till en
lokal subagent för själva kodningen; Claude granskade diffen, körde hela
testsviten och `tsc` självständigt på nytt innan leverans, i stället för att
bara lita på subagentens rapport.

## Vad som byggdes

1. `neptune-marketing/src/utils/besparingsvarde.ts` — `beraknaArsprodukt` bröts
   isär i en privat gemensam kärna (`beraknaArsproduktKarna`) och en ny,
   separat exporterad `beraknaArsproduktMedKostnadsled`, som utöver
   `beraknaArsprodukt`s befintliga returtyp även exponerar hela motorns
   `Kostnad`-objekt (`fast`, `energi`, `retur`, `justering`, `summaExkl`,
   `summaInkl`). `beraknaArsprodukt`s publika returtyp och beteende är
   oförändrat — verifierat genom att hela den befintliga testsviten
   fortfarande går grönt.
2. `neptune-marketing/src/utils/optimateScenario.ts` (ny) — tariffneutral
   före/efter-scenariomotor. Håller kapacitet, flöde, retur, kölddygnsserie
   och behörighet vid referensvärdet; ändrar bara styrbar rumsvärme (15/20/25
   %). Spärrad bakom en allowlist (`SCENARIO_PILOT_TARIFFER`) med exakt en
   post: `sundsvall-energi-indal-liden-och-lucksta` (ingen
   kapacitets-/flödesbindning i katalogen, `stodjer_besparing=false`
   oförändrat). Alla andra `leverantorId`, inklusive Stockholm Exergi och
   Vattenfalls profilprodukter, blockeras explicit innan någon generisk
   månadsserie når tariffmotorn.
3. `neptune-marketing/src/utils/optimateScenario.test.ts` (ny) — 15 test:
   15/20/25-procentiga scenarier, oförändrad övrig last, noll
   sommarrumsvärme, ogiltig/negativ/otillräcklig serie (avvisas), oförändrad
   debiterbar effekt, referenskostnad identisk med `beraknaArsprodukt` för
   samma underlag, samt att pilotgrinden blockerar icke-listade
   leverantörer.
4. `stockholmOptimatePotential.ts` lämnades oförändrat — en refaktorering in
   i den gemensamma kärnan bedömdes som en högre risk än detta avgränsade
   scope motiverar. Dess befintliga 5 test kördes oförändrat som
   regressionsbevis.

## Oberoende verifiering (Claude, efter subagentens leverans)

- `npm test` i `neptune-marketing/`: **2286/2286 test gröna, 69/69 filer**
  (körd på nytt av Claude, inte bara subagentens rapporterade siffra).
- `npx tsc --noEmit`: rent, inga typfel.
- `git diff 86be35a..HEAD --stat` granskad rad för rad; endast de tre
  avsedda filerna ändrade.
- `git status` i skills- och enkey-agents-repona verifierat oförändrat mot
  körningens startläge (samma HEAD:ar, samma redan smutsiga/orelaterade
  filer, inget nytt rört).
- Enkey `main@2e30bb2` och skills `main@4e296d6` orörda under hela
  uppdraget.

## Beslut

- Scenariomotorn exponeras inte i UI och ändrar ingen `stodjer_besparing`.
- Ingen aktivering, ingen push. Nästa steg är Codex granskning enligt
  kedjan i `conversations/README.md` punkt 10.

## Öppna frågor

- Om Codex vill se `stockholmOptimatePotential.ts` refaktorerad in i den
  delade kärnan som en separat, senare granskad ändring.
- Skills-repots egen täckningsmatris-`--check` kördes inte i denna
  omgång (ligger utanför Neptune-scopet); flaggas för Codex att avgöra om
  den behövs innan aktivering av fler tariffer.

## Rättningsrunda (Claude, `CHANGES_REQUIRED: Claude` 2026-09-22-009)

Codex granskning [2026-09-22-009](../../../reviews/2026/09/2026-09-22-granskning-optimate-scenariomotor-008.md)
krävde tre avgränsade rättningar i `optimateScenario.ts`/`optimateScenario.test.ts`,
ovanpå granskad Neptune-HEAD `0958f61` (bas `86be35a`). Ingen annan fil
rörd; `stockholmOptimatePotential.ts` och `besparingsvarde.ts` oförändrade
i denna runda.

1. **P1 (rumsvärmeproveniens/scenariostatus).** Nytt obligatoriskt fält
   `OptimateScenarioInput.rumsvarmeProvenance` (`confirmed_mwh` |
   `estimated_mwh`), validerat med samma mönster som övriga serier (nya
   orsaker `missing_rumsvarme_provenance`/`invalid_rumsvarme_provenance`).
   Varje scenario bär nu en egen, alltid `'preliminar'` `status` samt en
   `antaganden`-lista (andelsantagandet + ev. not om skattad rumsvärme).
   `efter.status.noggrannhet` nedgraderas alltid från `'exact'` till
   `'estimated'` i scenariot — oavsett `energyProvenance`/
   `rumsvarmeProvenance` — eftersom 15/20/25-procentsandelen alltid är ett
   antagande. `referens.status` (den befintliga årskostnaden) är orörd.
2. **P2 (ackumulerad övrig last).** Ny årsnivåkontroll
   `underlag.totalMwh - rumsvarmeForeMwh < -0.001` kastar
   `rumsvarme_overstiger_kopt_varme` innan resultatet byggs — fångar t.ex.
   tolv månader × 0,0005 MWh överskott som var för sig klarar
   månadstoleransen men ackumulerat ger negativ "icke styrbar last".
   `ovrigLastForeMwh` klämd till lägst 0 som sista skyddsnät. Nytt
   gränstest tillagt.
3. **P2 (publik/aktiverad förmåga).** Ny, separat exporterad
   `stodjerOptimateScenarioPubliktAktiverad(leverantorId)` — fail-closed
   tom allowlist (`SCENARIO_PUBLIKT_AKTIVERAD_TARIFFER`), skild från den
   interna beräkningspilotgrinden `stodjerOptimateScenario`. Sundsvall är
   `true` för den interna piloten men `false` för den publika förmågan; ett
   framtida UI måste kontrollera den senare. Två nya test verifierar detta
   uttryckligen, inklusive fail-closed för `undefined`.

### Oberoende verifiering (Claude)

- `npx tsc --noEmit` i `neptune-marketing/`: rent.
- `npx vitest run`: **2292/2292 test gröna, 69/69 filer** (2286 + 6 nya
  test för rättningen).
- `npm run eval:build`: ren `tsc` + Vite-bygge, inga nya fel (samma
  förbyggda chunk-storleksvarning som tidigare, orelaterad).
- `grep` bekräftar att ingen annan fil i `src/` importerar
  `beraknaOptimateScenario`/`OptimateScenarioInput`/`stodjerOptimateScenario`
  — ingen UI-anropare att uppdatera, i linje med Codex granskning.
- `git diff --stat` mot Neptune-HEAD innan denna runda: endast
  `optimateScenario.ts` och `optimateScenario.test.ts` ändrade.

## Git

Neptune, lokala commits (ingen push):

- `e1521c9` — Expose Kostnad-led ur beraknaArsprodukt utan att ändra dess
  returtyp
- `0958f61` — Lägg tariffneutral Optimate-scenariomotor, piloterad för
  Sundsvall (granskad av Codex, `neptune_reviewed_head` i granskning 009)
- `605bddd` — Rätta scenarioprovenienss, ackumulerad lastgräns och publik
  pilotgrind (denna rättningsrunda, ovanpå `0958f61`)

## Ändringslogg

- 2026-09-22 13:44 — Session skapad, implementation granskad och
  verifierad, `REVIEW_READY: Codex` skrivet i `conversations/index.md`.
- 2026-09-22 15:40 — Rättningsrunda för `CHANGES_REQUIRED: Claude`
  (2026-09-22-009) genomförd och oberoende verifierad, ny
  `REVIEW_READY: Codex` skriven i `conversations/index.md`.
