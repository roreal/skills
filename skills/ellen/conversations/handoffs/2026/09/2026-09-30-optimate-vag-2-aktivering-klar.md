---
handoff_id: "2026-09-30-003"
created_at: "2026-09-30T19:35:00+02:00"
from: Claude
to: Codex
status: activation-ready
approved_by:
  - Robert
  - Codex
executed_by: Claude
dispatched_by: agent-bridge
---

# ACTIVATION_READY: Codex — Optimate våg 2 lokalt aktiverad

## Utfört

Signal `2026-09-30-002` (`APPROVED_FOR_ACTIVATION: Claude`,
[direktuppdraget](2026-09-30-optimate-vag-2-direkt-aktivering.md)) utförd
direkt i huvudsessionen, utan underagent, exakt enligt det bindande
aktiveringsscopet i
[slutgodkännandet för signal 004](../../../reviews/2026/09/2026-09-30-slutgodkannande-optimate-vag-2-signal-004.md):

1. `SCENARIO_PUBLIKT_AKTIVERADE_ID` (`optimateScenario.ts`) är nu
   mekaniskt härledd som våg 1 (2 ID) + samtliga `WAVE_2_PRODUCT_IDS`
   (15 ID) = 17 unika, frysta ID — ingen andra, handskriven 15-raderslista.
2. Nytt prov binder att listan är exakt denna sammanslagning, fryst, utan
   dubbletter, och att varje publikt ID har samma backend i
   `SCENARIO_PILOT_TARIFFER_SNAPSHOT`.
3. Negativa prov kvarstår: Gotland taxa 21 (våg 3), okänt ID och
   `undefined` är fortsatt fail-closed. Stockholm-prototypen är oförändrad.
4. Ingen ändring av tariffdata, prisformler, backendval,
   `stodjer_besparing`/`stodjer_aktuell_arskostnad`, Enkey eller
   10/15/20-logiken.
5. Synligt scenario bevisat för en representant per backendfamilj:
   Halmstad (`legacy_arskostnad`), Sandviken
   (`kontraktsgatad_besparingsled`) och Karlstad
   (`kontraktsgatad_kostnadsled`) — komponentnivå (nytt
   `OptimateScenarioCardVag2.positive.test.tsx`, exakt facit mot den
   uniforma unit-facit) och sidnivå (Halmstad i
   `KalkylatorPageOptimateScenario.positive.test.tsx`).
6. Ordinarie Chromium/E2E (`e2e/kalkylator.smoke.mjs`) utökat med Scenario
   35: positiva produktionskontroller för alla tre backendfamiljer plus en
   negativ våg-3-kontroll (Gotland taxa 21). Kostnadsfacit bundet — exakt
   för Sandviken (flat energipris), korsbundet mot den oberoende
   `#arsprodukt-kostnad`-rutan för Karlstad, och mot monotona
   besparingsinvarianter för Halmstad (säsongspriser gör sidans
   schablonfördelade kronsumma icke-handräknad på sidnivå; det exakta
   facitet är redan bundet på komponentnivå).
7. Täckningsmatrisen (`Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py`)
   regenererad via `--write`: samtliga 15 våg-2-rader
   `godkand_intern_pilot_ej_publik` → `godkand_publik_10_15_20`. Fördelning
   efter aktivering: 17 `godkand_publik_10_15_20`, 0
   `godkand_intern_pilot_ej_publik`, 1
   `synlig_sarskild_preliminar_prototyp`, 59 `not_reviewed` — exakt den
   förväntade fördelningen.

## Verifieringsgrind

- Neptune, isolerad syskonlayout (`.claude/worktrees/agent-ae46c6f3096412378`):
  riktade filer (`optimateScenario.test.ts`, `optimateScenarioVag2.test.ts`,
  `optimateScenarioVag2HalmstadSandviken.test.ts`,
  `OptimateScenarioCard.test.tsx`, `OptimateScenarioCard.positive.test.tsx`,
  `OptimateScenarioCardVag2.positive.test.tsx`,
  `KalkylatorPageOptimateScenario.test.tsx`,
  `KalkylatorPageOptimateScenario.positive.test.tsx`) — 8 filer / 243 prov
  gröna.
- Hela Vitest: 86/86 testfiler, 2 663/2 663 prov gröna.
- `npx tsc --noEmit`: rent.
- Isolerat bygge (`npm run build`, körs av `test:e2e`): grönt.
- Hela ordinarie Chromium/E2E (`npm run test:e2e`): 35/35 scenarier gröna,
  inklusive nya Scenario 35.
- Skills: `generera_besparingspotential_tackningsmatris.py --check`: matchar
  77 produkter och källhashen. Pythonprovsviten
  (`test_generera_besparingspotential_tackningsmatris.py`): 19/19 gröna.
- `git diff --check`: rent i båda repona.

## Repo-HEAD:ar (lokala aktiveringsdiffar, opushade)

- Neptune-worktree `worktree-agent-ae46c6f3096412378`:
  `c85b1e5f6f1400a33803a8ef652aaf40883009e2` (föräldrar:
  `5d91de6feec313f2f5d0f802d198e40d41cf2c15`, den granskade kandidaten).
- Neptune `main`/`origin/main` (oförändrat, ingen mainflytt utförd):
  `f3ce263c532bdc9733acbe6e59a373ac90bc0336`.
- skills `main`: `8df11b266f336e4b7c54006b056200114ddc4ad8` (förälder:
  `f6c7ae2`, den tidigare toppen).

Ingen mainflytt, merge, rebase, push, force eller historikomskrivning har
utförts — exakt enligt scopet.

## Nästa steg

Codex granskar aktiveringsdiffen (kommentardiff rad för rad, räkning,
regressioner) i båda repona ovan och lämnar `APPROVED_FOR_PUSH: Claude`
eller `CHANGES_REQUIRED: Claude`.
