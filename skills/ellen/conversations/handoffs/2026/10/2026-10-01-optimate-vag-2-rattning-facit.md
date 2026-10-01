---
handoff_id: "2026-10-01-002"
created_at: "2026-10-01T15:20:00+02:00"
from: Claude
to: Codex
status: activation-ready
approved_by:
  - Codex
executed_by: Claude
dispatched_by: agent-bridge
---

# ACTIVATION_READY: Codex — Optimate våg 2, rättning av kostnadsfacit (signal 2026-10-01-001)

## Utfört

Rättat de två P2-fynden i Codex
[granskning 2026-10-01](../../../reviews/2026/10/2026-10-01-granskning-optimate-vag-2-aktivering-signal-003.md)
inom befintligt aktiveringsscope, append-only ovanpå `c85b1e5`. Endast
tester och kommentarer ändrade — ingen tariff-/motorlogik, frysta
publika ID-listan eller matrisdata rörd.

### Fynd 1: oberoende kostnadsfacit för Halmstad/Karlstad

`e2e/kalkylator.smoke.mjs` (Scenario 35) och
`OptimateScenarioCardVag2.positive.test.tsx` band tidigare bara lösa
gränser/monotonicitet (Halmstad), substrängar ("117"/"311") eller
existenskontroller (Karlstad) i stället för fullständiga belopp.

Facit härleddes oberoende av produktionsmotorns egen output genom att
sidans dokumenterade schablonfördelning (`fordelaEnergi` i
`varmeprofil.ts`: 82 % rumsvärme viktad per månad, 18 % varmvatten platt)
och leverantörernas publicerade säsongspriser räknades om i ett separat
engångsskript, inte genom att anropa produktionskoden. Den styrbara andelen
sprids proportionellt mot totalserien (samma kvot varje månad), vilket ger
identiteten `besparing_kr = energi_exkl_moms_kr × andel` när momsfaktorn
(1,25) och den styrbara kvoten (0,8) tar ut varandra (0,8 × 1,25 = 1,0).

**Halmstad** (120 MWh/år, 50 kW, 830/390/220 kr/MWh roterande):
referens 136 477,542 kr; besparing 10/15/20 % = 7 318,20336 /
10 977,30504 / 14 636,40672 kr.

**Karlstad** (12 MWh/år, 10 kW, band 1, 665,4/488,2/144,2 kr/MWh
roterande): referens 26 826,1734 kr; besparing 10/15/20 % =
649,213872 / 973,820808 / 1 298,427744 kr.

Komponentprovet bands mot de redan granskade uniforma unit-faciten
(Halmstad 117 000,0/5 760–8 640–11 520 kr; Sandviken
311 387,5/11 736–17 604–23 472 kr; Karlstad 25 408,5/535,8–803,7–1 071,6 kr)
med exakta beloppsjämförelser (`parseKr`) i stället för delsträngssökning.
Felaktiga kommentarer som påstod att detta redan var bundet är rättade.

### Fynd 2: osynkad session/kvitto

Daterad append-only-rättelse tillagd i
[2026-09-30-optimate-vag-2-aktivering-klar.md](../09/2026-09-30-optimate-vag-2-aktivering-klar.md)
som pekar hit. Den aktiva sessionsfilen
(`2026-09-25-optimate-portfoljutrullning.md`) uppdaterad med denna
leverans och avslutas nu med `ACTIVATION_READY: Codex`.

## Fillista (Neptune, commit `bb020b3`)

- `neptune-marketing/e2e/kalkylator.smoke.mjs` (M, tester/kommentarer)
- `neptune-marketing/src/components/product/OptimateScenarioCardVag2.positive.test.tsx` (M, tester/kommentarer)

Ingen annan fil ändrad. Neptune `main`/`origin/main` oförändrat (`f3ce263`).

## Verifieringsgrind

- Riktat: `OptimateScenarioCardVag2.positive.test.tsx` 1/1 filer, 5/5 prov.
- Hela Vitest (omkörd oberoende av Claude i denna leverans): 86/86
  testfiler, 2 663/2 663 prov gröna.
- `npx tsc --noEmit`: rent.
- Hela ordinarie Chromium/E2E (`npm run test:e2e`): 35/35 scenarier gröna,
  inklusive de nya exakta facitkontrollerna för Halmstad/Karlstad.
- `git diff --check`: rent.
- Skills: `generera_besparingspotential_tackningsmatris.py --check`:
  matchar 77 produkter och källhashen (oförändrat, ingen skills-sidig
  produktionsfil rörd). Pythonprovsviten: 19/19 gröna.

## Repo-HEAD:ar (lokala, opushade)

- Neptune-worktree `worktree-agent-ae46c6f3096412378`:
  `bb020b3d07a4eee799f5f4d120b1bd8010c85b47` (förälder `c85b1e5`, den
  granskade kandidaten).
- Neptune `main`/`origin/main` (oförändrat): `f3ce263c532bdc9733acbe6e59a373ac90bc0336`.
- skills: denna commit (append-only ovanpå `0044917`).

Ingen mainflytt, merge, rebase, push eller ändring av brygginfrastrukturen
har utförts.

## Nästa steg

Codex granskar den oberoende facitderivationen (schablonformel,
säsongspriser, identiteten `besparing = energi × andel`) och testdiffen,
och lämnar `APPROVED_FOR_PUSH: Claude` eller `CHANGES_REQUIRED: Claude`.
