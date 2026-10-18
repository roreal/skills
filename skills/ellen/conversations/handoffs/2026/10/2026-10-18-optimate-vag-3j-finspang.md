---
handoff_id: "2026-10-18-003"
created_at: "2026-10-18T08:14:22+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3j — Finspångs Tekniska Verk

Robert instruerade efter den fjärrverifierade Wave 3i-leveransen:
**"Då tar vi nästa batch"**. Codex har inventerat de 15 återstående
ogranskade produkterna och väljer exakt
`finspangs-tekniska-verk-finspang`: den enda återstående produkten med
`piecewise_polynomial` + `conditional_flow`. Jönköping, de tolv
Vattenfallprodukterna och syntetiska `riksgenomsnitt` hålls utanför.

## Bas, scope och mål

- Neptune `origin/main`:
  `51e78a21c81f92c0b4f9dcc70a0d70d93bd20975`.
- skills `origin/main`:
  `480889ba1d5c86f3d71db0400b93842a6edd2803`.
- Basdisposition: **61 publika / 0 interna / 1 prototyp / 15 ogranskade**.
- Måldisposition: **61 publika / 1 intern / 1 prototyp / 14 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från livebasen,
exempelvis `optimate-vag-3j-finspang-conditional-flow`. Återanvänd inte
Wave 3i-worktreen och flytta inte ordinarie checkout eller lokal `main`.

Skapa ett fryst `WAVE_3J_PRODUCT_IDS` med exakt ID:t ovan och bind det
explicit till `kontraktsgatad_kostnadsled` i interna scenariokartan.
Finspång ska inte läggas i den publika allowlisten: intern snapshot 61→62,
publik lista fortsatt exakt 61. Flytta exakt matrisraden från
`not_reviewed` till `godkand_intern_pilot_ej_publik` och regenerera endast
via generatorn.

Ingen tariffdata, genererad tariffkatalog, kostnadsmotor, policyregister,
resultatkontrakt, kund-UI, browser/E2E, Enkey-fil eller annan produkt får
ändras i denna etapp. Befintliga funktioner och redan fungerande UI för
`piecewise_polynomial` och de två 12-elementsserierna ska återanvändas.

## Bindande scenariokontrakt

Endast månadens köpta energi och total MWh får ändras mellan referensen och
10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.

Följande ska återanvändas bit-identiskt i alla fyra beräkningar:

- `kapacitetKw` och dess bindning `finspang_debiterbar_effekt_kw`;
- hela serien `conditional_flow_returtemp_c`;
- hela serien `conditional_flow_flode_m3`;
- proveniens, attestering och alla andra kontraktsfält.

Kapacitetsledet får inte räknas om från lägre energi. Den villkorade
flödesavgiften ska vara oförändrad eftersom returtemperatur och flöde är
låsta. Ingen förbättrad returtemperatur, minskat flöde eller omedelbar
effektbesparing får tillskrivas Optimate.

## Oberoende literalfixtur och facit

Använd minst följande fixture. Förväntade värden får inte genereras via
produktionsfunktionerna.

- Köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: exakt 80 procent av varje månad.
- Energipriser:
  `[708.6,708.6,708.6,355,355,212.2,212.2,212.2,355,355,708.6,708.6]`
  kr/MWh.
- Debiterbar effekt: `36` kW.
- Returtemperaturserie:
  `[50,56,55,60,45,57,54,70,40,55,56,52]` °C.
- Flödesserie:
  `[100,110,120,130,140,150,160,170,180,190,200,210]` m³.

Handräknade komponenter exklusive moms:

- energi före: **69 745,60 kr**;
- kapacitet, låg gren:
  `(-0,204 × 36 + 1 093) × 36` = **39 083,616 kr**;
- villkorad flödesavgift: endast månader 2, 4, 6, 8 och 11 är strikt
  över 55 °C: `20 × (110+130+150+170+200)` = **15 200 kr**;
- referens exklusive moms: **124 029,216 kr**;
- referens inklusive moms: **155 036,52 kr**.

| Scenario | Energifaktor | Energi exkl. | Kapacitet | Flödesavgift | Summa exkl. | Summa inkl. | Besparing inkl. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 % | 0,92 | 64 165,952 | 39 083,616 | 15 200 | 118 449,568 | 148 061,96 | 6 974,56 |
| 15 % | 0,88 | 61 376,128 | 39 083,616 | 15 200 | 115 659,744 | 144 574,68 | 10 461,84 |
| 20 % | 0,84 | 58 586,304 | 39 083,616 | 15 200 | 112 869,920 | 141 087,40 | 13 949,12 |

Lägg separata gränsprov:

- exakt `P=2600` använder låg gren och ger **1 462 760 kr**;
- `P=2601` använder hög gren och ger **1 462 622,45 kr**;
- returtemperatur exakt 55 °C ger ingen avgift för månaden, medan ett
  värde strikt över 55 °C ger `20 × månadens flöde`;
- saknad, partiell, extra, icke-numerisk eller icke-ändlig serie samt
  noll/negativ/icke-ändlig kapacitet ska blockeras typat och fail-closed.

## Fail-closed-grindar

Bind i både Neptune och skills exakt hela Finspångs råkontrakt, ordnat och
utan extra egenskaper: moms, hela månadsprislistan, full
`piecewise_polynomial`-kapacitet inklusive tröskel och båda grenar,
periodisering, hela `conditional_flow`-objektet, exakt tre kompletta
policyfält, bindningar, serie-/historik-/behörighets-/exkluderingsfält samt
`cost_path`, `_kraver_kontrakt`, `stodjer_aktuell_arskostnad=true` och
`stodjer_besparing=false`.

Lägg mutationsprov som fäller saknat/extra Wave-3j-ID, fel backend/status,
ändrad prislista, polynomparameter/tröskel, flödessats/tröskel/fältnyckel,
policyfält/ordning/typ/gräns/upplösning/bindning, serie-/historikfält,
behörighet och dokumenterad exkludering. Bind den exakta globala mängden
`conditional_flow`-produkter mot Wave 3j.

Kör riktade Wave-3j-prov, berörda äldre snapshotprov, hela Vitest, ren
`tsc --noEmit`, produktionsbygge med återställd `dist`, hela skills-
pytestsviten, generatorns `--check` och `git diff --check` i båda repona.

Committera lokalt och avgränsat. Ingen publik aktivering, mainflytt eller
push. Lämna en ny unik, committad `REVIEW_READY: Codex` med fulla hashar,
ancestry, testutfall och disposition **61/1/1/14=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
