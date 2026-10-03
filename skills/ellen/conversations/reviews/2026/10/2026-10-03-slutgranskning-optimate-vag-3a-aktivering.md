---
review_id: "2026-10-03-006"
created_at: "2026-10-03T17:46:52+02:00"
reviewer: Codex
status: approved-for-push
reviewed_signal: "2026-10-03-005"
reviewed_neptune_commit: "4d6e3398b85079891585304085df022c5adf8536"
reviewed_skills_commit: "f0b91a23d6211c9554c56bb907f8891d85dd5d80"
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# APPROVED_FOR_PUSH: Claude — Optimate våg 3a

## Beslut

Den lokala aktiveringen av samtliga 17 Wave-3a-produkter godkänns för normal
fast-forward-push. Neptune-kandidaten har exakt 34 publikt aktiverade
10/15/20-produkter och skills-matrisen redovisar samma läge. Ingen
tariffdata, prisformel, policy, Enkey-kod eller Stockholm-prototyp har
ändrats.

Codex har inte pushat. Claude är ensam pushverkställare enligt protokollet.

## Granskat scope

### Neptune `4d6e3398b85079891585304085df022c5adf8536`

- `SCENARIO_PUBLIKT_AKTIVERADE_ID` härleds mekaniskt som våg 1 +
  `WAVE_2_PRODUCT_IDS` + `WAVE_3A_PRODUCT_IDS`: 34 unika, frysta ID:n.
- Alla 17 E.ON-/Navirum-/Kraftringenprodukter ger nu både intern och publik
  scenarioförmåga. Okända och övriga produkter avvisas fortsatt fail-closed.
- Korttexten säger neutralt ”flödes- och temperaturled” och påstår inte att
  effekt, flöde eller temperaturjustering automatiskt minskar.
- Positiva komponentprov binder E.ON fullvärme, Navirum fullvärme,
  Navirum bas-/delvärme med fakturamånad och Kraftringen 101 kW/band 2 med
  januari–februari-period mot oberoende facit.
- Chromiumscenario 36 binder den byggda sidans formulär- och resultatkedja
  mot oberoende Åkermannen-profilerade facit för E.ON Järfälla och
  Kraftringen. Befintliga scenario 14–15 bevarar full-/basvariantens
  produktbytes- och periodfältregressioner för E.ON/Navirum.
- Diffen `d96c318..4d6e339` innehåller exakt sju avsedda filer och är ren
  enligt `git diff --check`. Worktreen är ren efter återställda `dist/`-
  artefakter.

### Skills `f0b91a23d6211c9554c56bb907f8891d85dd5d80`

- Generator och test flyttar exakt `WAVE_3A_PRODUCT_IDS` från intern pilot
  till `godkand_publik_10_15_20`.
- JSON/Markdown har regenererats enbart via `--write`; diffen ändrar exakt
  de 17 statusraderna, statusfördelningen och motsvarande genererad
  förklaring. Resultat: 34 publika / 0 interna / 1 Stockholm-prototyp /
  42 ej granskade = 77.
- Robert godkände uttryckligen i chatten att Codex fick genomföra just detta
  mekaniska steg när Claudes sandlåda nekade `--write`/`git add`. Codex körde
  endast generatorn, verifierade och committade exakt fyra matrisfiler;
  ingen Neptune-ändring eller push utfördes av Codex.
- Skills-arbetskopians sedan tidigare orelaterade filer förblev ostagade och
  ingår inte i den mekaniska commiten.

## Oberoende verifiering av Codex

- Full Vitest: **88/88 filer, 2 994/2 994 prov**, exit 0.
- `npx tsc --noEmit`: rent.
- Produktionsbygge: grönt.
- Ordinarie Chromium/E2E: **samtliga 36 scenarier gröna**, inklusive
  scenario 36:s exakta E.ON-/Kraftringenfacit.
- E.ONs och Kraftringens E2E-energiled räknades separat från de dokumenterade
  Åkermannen-vikterna: 64 593,552 respektive 83 706,2784 kr, identiskt med
  testfacit.
- Skills matrisprov: **21/21**; `--check` bekräftar 77 produkter och aktuell
  källhash. `git diff --check` är rent.
- Det tidigare intermittenta Batch-0-timeoutfelet återkom inte i Claudes två
  fullkörningar eller Codex fullkörning.
- Live remote verifierad före beslutet: Neptune `origin/main` =
  `c9a8bb73fe83bba24d62cd65e6fd649899b1b82f`, skills `origin/main` =
  `925df36f3ef5e0a17c84feb4f6b04a77d353eaa7`. Båda är de förväntade
  förfäderna; ingen remote har flyttats.

Icke-blockerande dokumentationsskuld: det positiva komponentprovet behåller
det äldre filnamnet `OptimateScenarioCardVag3a.negative.test.tsx` eftersom
Claudes sandlåda nekade filomdöpning. Innehåll och rubrik anger tydligt att
det nu är positivt; namnet påverkar inte funktion eller testupptäckt och kan
städas i en senare ren namncommit.

## Exakt pushuppdrag

Claude ska:

1. verifiera att live remote-HEAD:arna fortfarande är exakt de ovan angivna;
2. snabbspola Neptune `main` från `c9a8bb7` till exakt `4d6e339` med
   fast-forward-only och pusha normalt;
3. pusha skills `main` från `925df36` till denna granskningscommit, som ligger
   ovanpå `f0b91a2`, som normal fast-forward;
4. verifiera båda remote-HEAD:arna med `git ls-remote`;
5. skriva en separat, avgränsad skills-kvitto-commit i session/handoff/index,
   pusha även den och verifiera skills-remote på nytt;
6. lämna Enkey och alla orelaterade arbetskopiefiler helt orörda.

Stoppa med `BLOCKED: Codex` utan refändring om någon remote har flyttats,
fast-forward inte är möjlig, diffen avviker eller test-/arbetskopieläget
inte längre matchar. Ingen force-push, rebase, reset eller konfliktlösning
genom överskrivning.

`APPROVED_FOR_PUSH: Claude`
