---
session_id: "2026-10-08-001"
started_at: "2026-10-08T08:57:54+02:00"
last_updated: "2026-10-08T09:15:00+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: active
topics:
  - Optimate
  - besparingspotential
  - våg 3e
  - Umeå Energi
  - asymmetrisk flödesdifferens
source: visible-conversation
transcript_fidelity: summarized
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3e — Umeå Energi Enkel

## Start och beslut

Efter att Wave 3d pushats och fjärrverifierats instruerade Robert:
**"OK dags för nästa batch"**.

Codex inventerade de 25 återstående `not_reviewed`-produkterna och valde
den minsta sammanhållna beroendeklassen: exakt
`umea-energi-umea-enkel`. Produkten är ensam om
`asymmetric_flow_difference` och hålls därför skild från de tre
`temperature_difference`-produkterna, Lidköpings månadsserier,
returtemperaturprodukterna och Vattenfalls behörighetsfamilj.

Live-baserna verifierades före start:

- Neptune `origin/main=d2976151749466258ea96ce987ca5f75ffbc392b`.
- skills `origin/main=98f9d0e9652e2e9a337aa5a22c790974abb3082d`.

Uppdraget är en intern, ej publik 10/15/20-pilot. A, band, B,
treårsperiod och oktober–aprilflöde hålls fasta, medan det asymmetriska
flödesledet räknas om mot lägre säsongsenergi. Ett oberoende facit korsar
avsiktligt från bonus till avgift. Måldispositionen är
**51 publika / 1 intern / 1 prototyp / 24 ogranskade = 77**.

Se [handoffen](../../../handoffs/2026/10/2026-10-08-optimate-vag-3e-umea-asymmetrisk-flodesdifferens.md).

Ingen tariff-/motor-/policyregister-/UI-/Enkeyändring, publik aktivering,
mainflytt eller push.

## Implementation (Claude)

Ny isolerad Neptune-worktree `optimate-vag-3e-umea-flodesdifferens`,
grenad direkt från den verifierade `origin/main=d297615`
(återanvände inte en äldre Wave 3-worktree).

- Lade `WAVE_3E_PRODUCT_IDS` (`umea-energi-umea-enkel`) i
  `SCENARIO_PILOT_TARIFFER` (`kontraktsgatad_kostnadsled`) —
  EXPLICIT INTE i `SCENARIO_PUBLIKT_AKTIVERADE_ID`. Den befintliga
  motorfunktionen `asymmetriskFlodesdifferens` (fjarrvarme.ts) och
  kontraktsfasaden återanvänds oförändrade; ingen tariff-, motor-,
  policyregister-, UI- eller Enkeyändring.
- Ny `optimateScenarioVag3e.test.ts` (37 prov) med ett oberoende,
  handskrivet brytpunktsfacit direkt ur handoffens tabell: referensen
  (diff=−100 m³) använder bonus-grenen (3×−100=−300 kr), alla tre
  10/15/20-efterfall (diff 36/104/172 m³) använder avgifts-grenen
  (7×diff=252/728/1204 kr). Referens 89 367,10 kr exkl./111 708,875 kr
  inkl., besparing 6 034,80/8 802,20/11 569,60 kr vid 10/15/20 % —
  exakt handoffens tabell. Täcker katalogbindning (7 band, 4 krävda
  policyfält inkl. B=kapacitetsfaktor), säsongskänslighet,
  brytpunktsbevis (fel om bonus_rate/fee_rate skulle bytas), och
  fail-closed för saknat/negativt/NaN/Infinity `flode_okt_apr_m3`, fel
  band-ID, saknad/ogiltig effekt och blockerad besparingsväg.
  `umea_enkel_arseffekt_a_kw` kräver en observerad kalperiod
  (`kapacitetObserveradPeriod="2023-01-01/2025-12-31"`, bit-identisk i
  referens och alla scenarier) — upptäckt under testkörning, inte en
  ändring av motorn.
- Mekanisk uppdatering: `SCENARIO_PILOT_TARIFFER_SNAPSHOT`-längden 51→52
  i våg 2/3a/3b/3c/3d-provens redan existerande totalräkningar, och
  rättning av Våg 3d:s negativprov (Umeå är nu en intern pilot men
  fortsatt inte publik — tidigare provet antog felaktigt att Umeå var
  helt opiloterad).
- skills-sidan (samma repo): `generera_besparingspotential_tackningsmatris.py`
  — ny `WAVE_3E_PRODUCT_IDS`/`WAVE_3E_PRODUCT_KEYS`/
  `WAVE_3E_ADJUSTMENT_PARAMS`, flyttade exakt `umea-energi-umea-enkel`
  från `not_reviewed` till `godkand_intern_pilot_ej_publik` i
  `SCENARIO_STATUS_REGISTRY`, och en ny build_matrix-grind som binder de
  RÅA `asymmetric_flow_difference`-parametrarna (bonus_rate=3, fee_rate=7,
  reference_m3_per_MWh=17, säsongsmånaderna okt–apr) mot katalogen — inte
  bara `adjustment_types`. JSON/Markdown regenererades ENBART via
  generatorn (`--write`, därefter `--check` grönt). 17 nya pytest-prov.

### Testutfall

- Neptune: `npx vitest run` → **3389/3389 gröna** (inkl. 37 nya
  Wave 3e-prov och de 5 mekaniskt uppdaterade äldre vågfilerna).
- `npx tsc --noEmit` → rent, inga fel.
- `npm run build` → OK; genererad `dist/`-smuts återställd med
  `git checkout -- neptune-marketing/dist` (samma innehåll som
  `origin/main`).
- `git diff --check` (Neptune) → rent.
- skills pytest (`Fjarrvarmetariffer/`) → **51/51 gröna** (17 nya
  Wave 3e-prov).
- `generera_besparingspotential_tackningsmatris.py --check` → grönt,
  disposition **51 publika / 1 intern / 1 prototyp / 24 ogranskade = 77**.
- `git diff --check` (skills) → rent.

### Repo-HEAD:ar efter lokal commit

- Neptune `optimate-vag-3e-umea-flodesdifferens`:
  `ae4c641ed63c64f6d57f0ad6c2a87129be6c07e5` (ovanpå oförändrat
  `origin/main=d297615...`, fast-forward-kandidat).
- skills `main`: `c19c01ad1aaabe6386fa6e3ede8086f62ba7e281` (ovanpå
  oförändrat `origin/main=98f9d0e9...`, fast-forward-kandidat; endast de
  fyra avgränsade filerna committades, orelaterat ocommitterat arbete i
  arbetskopian lämnades orört).

Ingen publik aktivering, mainflytt eller push i detta steg — exakt
handoffens scope.

`REVIEW_READY: Codex`
