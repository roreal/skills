---
handoff_id: "2026-10-18-009"
created_at: "2026-10-18T15:29:08+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3k — Jönköping Energi

Robert instruerade efter den fjärrverifierade Wave 3j-leveransen:
**"OK då tar vi nästa batch"**. Codex väljer exakt
`jonkoping-energi-jonkoping-och-granna`: den enda återstående verkliga
produkten med `metered_access_fee + volume`. De tolv Vattenfallprodukterna
och syntetiska `riksgenomsnitt` hålls utanför.

## Bas, scope och mål

- Neptune `origin/main`:
  `db218c0b4d8247a5577e4b6bc3cf980658dbf7a9`.
- skills `origin/main`:
  `cce4c8895583f9dc84281fde8cfc9eeef7839b10`.
- Basdisposition: **62 publika / 0 interna / 1 prototyp / 14 ogranskade**.
- Måldisposition: **62 publika / 1 intern / 1 prototyp / 13 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från livebasen,
exempelvis `optimate-vag-3k-jonkoping-access-flode`. Återanvänd inte Wave
3j-worktreen och flytta inte ordinarie checkout eller lokal `main`.

Skapa ett fryst `WAVE_3K_PRODUCT_IDS` med exakt ID:t ovan och bind det
explicit till `kontraktsgatad_kostnadsled` i interna scenariokartan.
Jönköping ska inte läggas i den publika allowlisten: intern snapshot
62→63, publik lista fortsatt exakt 62. Flytta exakt matrisraden från
`not_reviewed` till `godkand_intern_pilot_ej_publik` och regenerera endast
via generatorn.

Ingen tariffdata, genererad tariffkatalog, kostnadsmotor, policyregister,
resultatkontrakt, kund-UI, browser/E2E, Enkey-fil eller annan produkt får
ändras i denna etapp. Befintlig Jönköping-produktväg, bandval,
helårsflöde, accessval och globala undercentralsfält ska återanvändas.

## Bindande scenariokontrakt

Endast månadens köpta energi och total MWh får ändras mellan referensen
och 10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.

Följande ska återanvändas bit-identiskt i alla fyra beräkningarna:

- `kapacitetKw` och bindningen `jonkoping_debiterbar_effekt_kw`;
- bekräftat effektband `jonkoping_vald_niva_id`;
- helårsflödet `flode_m3`;
- accessvalet `access_pris_kr_per_central_manad`;
- `substations`, bundet endast genom `antal_undercentraler_bindning` — det
  får inte smugglas in via `policyFalt`;
- proveniens, attestering och alla andra kontraktsfält.

Kapacitetsledet får inte räknas om eller byta band när energin minskar.
Flödesavgiften `flode_m3 × 3,7` och accessavgiften
`accesspris × antal undercentraler × 12` ska vara oförändrade. Ingen
minskad effekt, minskat flöde eller ändrad access får tillskrivas Optimate.

## Oberoende literalfixtur och facit

Använd minst följande fixture. Förväntade värden får inte genereras via
produktionsfunktionerna.

- Köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: exakt 80 procent av varje månad.
- Energipriser:
  `[717,717,421,421,142,142,142,142,142,421,421,717]` kr/MWh.
- Debiterbar effekt: `100` kW.
- Bekräftat effektband: `2` (51–270 kW).
- Helårsflöde: `1 000` m³.
- Accessval: `25` kr per central och månad.
- Antal undercentraler: `3` via `underlag.substations`.

Handräknade komponenter exklusive moms:

- energi före: **60 332 kr**;
- kapacitet, band 2: `8 900 + 904 × 100` = **99 300 kr**;
- flödesavgift: `1 000 × 3,7` = **3 700 kr**;
- accessavgift: `25 × 3 × 12` = **900 kr**;
- referens exklusive moms: **164 232 kr**;
- referens inklusive moms: **205 290 kr**.

| Scenario | Energifaktor | Energi exkl. | Kapacitet | Flöde + access | Summa exkl. | Summa inkl. | Besparing inkl. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 % | 0,92 | 55 505,44 | 99 300 | 4 600 | 159 405,44 | 199 256,80 | 6 033,20 |
| 15 % | 0,88 | 53 092,16 | 99 300 | 4 600 | 156 992,16 | 196 240,20 | 9 049,80 |
| 20 % | 0,84 | 50 678,88 | 99 300 | 4 600 | 154 578,88 | 193 223,60 | 12 066,40 |

Lägg separata gräns- och fail-closed-prov:

- band 1 vid 50 kW ger `2 050 + 1 040 × 50 = 54 050 kr`;
- band 2 vid 51 kW ger `8 900 + 904 × 51 = 55 004 kr`;
- band 3 vid 271 kW ger `87 700 + 612 × 271 = 253 552 kr`;
- band 4 vid 1 201 kW ger `408 100 + 345 × 1 201 = 822 445 kr`;
- fel band för angiven effekt, okänt band eller saknat band blockerar;
- accessvärdena 0/10/25/50 accepteras, medan exempelvis 7 blockerar;
- 1 och 20 undercentraler accepteras; 0, 21, decimal och icke-ändligt tal
  blockerar;
- flöde 0 och 1 000 000 accepteras; negativt, över max eller
  icke-ändligt värde blockerar;
- saknad/icke-numerisk/icke-ändlig kapacitet och saknade policyfält
  blockerar typat och fail-closed.

## Fail-closed-grindar

Bind i både Neptune och skills exakt hela Jönköpings råkontrakt, ordnat
och utan extra egenskaper:

- `cost_path=kontrakt_arskostnad`, `_kraver_kontrakt=true`,
  `stodjer_aktuell_arskostnad=true`, `stodjer_besparing=false`;
- moms exklusive, hela den ordnade månadsprislistan, `fast_avgift=null`
  och `manadsperiodisering=null`;
- full kapacitet med `kw_faktor=1` och fyra ordnade band inklusive samtliga
  gränser, fasta avgifter och kW-priser;
- de två ordnade råjusteringarna: först `volume` med 3,7 kr/m³ och
  månad 1–12, därefter `metered_access_fee` med exakt allow-list
  0/10/25/50, båda fältnycklarna och månad 1–12;
- exakt fem kompletta policyfält i rå ordning:
  `jonkoping_debiterbar_effekt_kw`, `flode_m3`,
  `jonkoping_vald_niva_id`, `access_pris_kr_per_central_manad`,
  `antal_undercentraler`;
- effektfältets rullande historik, bandfältets `band_id`, accessfältets
  numeriska allow-list och etiketter samt undercentralsfältets heltals-
  och källkrav;
- exakta effekt-/band-/undercentralsbindningar,
  `series_fields=[]`, `history_fields=[jonkoping_debiterbar_effekt_kw]`,
  inget behörighetsvillkor och inga dokumenterade exkluderingar.

Lägg mutationsprov som minst fäller saknat/extra Wave-3k-ID, fel backend,
status eller cost path, ändrad prislista, kapacitet, band, justeringsordning,
sats, allow-list, fältnyckel eller månad, fel policyfält/ordning/typ/gräns/
upplösning/källa/bindning, extra serie-/historik-/behörighets-/
exkluderingsfält. Bind den exakta globala mängden
`metered_access_fee`-produkter mot Wave 3k.

Kör riktade Wave-3k-prov, berörda äldre snapshotprov, hela Vitest, ren
`tsc --noEmit`, produktionsbygge med återställd `dist`, hela skills-
pytestsviten, generatorns `--check` och `git diff --check` i båda repona.

Committera lokalt och avgränsat. Ingen publik aktivering, mainflytt eller
push. Lämna en ny unik, committad `REVIEW_READY: Codex` med fulla hashar,
ancestry, testutfall och disposition **62/1/1/13=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
