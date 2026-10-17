---
handoff_id: "2026-10-17-006"
created_at: "2026-10-17T11:42:51+02:00"
status: prepared-awaiting-user-approval
signal: "READY_FOR_APPROVAL: Robert"
requested_by: Robert
prepared_by: Codex
---

# Optimate våg 3i — Telge Nät, låg utnyttjning och returtemperatur

Robert instruerade efter den fjärrverifierade Wave 3h-leveransen:
**"Förbered Wave 3i"**. Detta dokument förbereder implementationen men
startar inte Claude och godkänner inte publik aktivering eller push.

Codex har inventerat de 16 återstående `not_reviewed`-produkterna och valt
den minsta sammanhållna, verkliga beroendeklassen:

- `telge-nat-telge-foretag-och-bostadsrattsforeningar`.

Telge är den enda återstående verkliga produkten med kombinationen
`low_utilization` + `incremental_return_temperature`. Norrenergi har samma
två justeringstyper men är redan granskad och publik i Wave 3h via
legacybackenden; Telge ska återanvända den befintliga
`kontraktsgatad_kostnadsled`-backenden. Övriga återstående produkter hålls
utanför scopet: Finspång kräver två månadsserier, Jönköping har
access-/årsflödesled, tolv Vattenfall-produkter har profil-/behörighets- och
exkluderingslogik, och `riksgenomsnitt` är syntetiskt.

Första steget ska vara en **intern, ej publik 10/15/20-pilot**. Telge får
inte läggas i `SCENARIO_PUBLIKT_AKTIVERADE_ID` i denna etapp.

## Verifierad bas och mål

- Neptune live `origin/main`:
  `14d7b8c78c3eb8b49976dfe8ea2ace826b51923b`.
- skills live `origin/main`:
  `6ad4adaca4a687e64938c6a709ba5949cc7be090`.
- Nuvarande disposition:
  **60 publika / 0 interna / 1 prototyp / 16 ogranskade = 77**.
- Måldisposition efter intern pilot:
  **60 publika / 1 intern / 1 prototyp / 15 ogranskade = 77**.

Skapa vid godkänd start en ny isolerad Neptune-worktree och gren direkt
från live-basen, exempelvis `optimate-vag-3i-telge-retur-lagutnyttjande`.
Återanvänd inte Wave 3h-worktreen och flytta inte ordinarie checkout eller
lokal `main`.

Ingen tariffdata, genererad tariffkatalog, prisformel, policyregister,
resultatkontrakt, kund-UI, browser/E2E, Enkey-fil eller annan produkt får
ändras. De befintliga funktionerna för låg utnyttjning, stegvis
returtemperatur och kontraktsgatad årskostnad ska återanvändas oförändrade.

## Tillåten implementation

1. Skapa/exportera ett fryst `WAVE_3I_PRODUCT_IDS` med exakt Telges ID.
2. Lägg ID:t explicit i den interna backendkartan som
   `kontraktsgatad_kostnadsled`; ingen härledning eller fallback.
3. Håll ID:t utanför den publika allowlisten. Intern pilotsnapshot ska bli
   61 medan publik lista förblir exakt 60 unika, frysta ID:n.
4. Flytta exakt Telge-raden i skills-matrisen från `not_reviewed` till
   `godkand_intern_pilot_ej_publik` och regenerera JSON/Markdown endast via
   generatorn till **60/1/1/15=77**.

## Bindande scenariokontrakt

Endast månadens köpta energi och total MWh får ändras mellan referensen och
10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.

Följande ska återanvändas bit-identiskt i alla fyra beräkningarna:

- debiterbar effekt/`kapacitetKw` och policyfältet
  `telge_debiterbar_effekt_kw`;
- bekräftat effektband `telge_vald_niva_id`;
- `normalarskorrigerad_energi_mwh` för perioden juni–maj;
- `returtemperatur_c`;
- proveniens, attestering och alla övriga policyfält.

Effektledet får inte minska och bandet får inte väljas om. Låg-
utnyttjandeavgiften ska vara bit-identisk före/efter eftersom både
normalårsenergin och debiterbar effekt är låsta:

```text
utnyttjningstid = normalarskorrigerad_energi_mwh × 1000 / debiterbar_effekt_kw
lågnyttjande = max(0, 2300 − utnyttjningstid) × debiterbar_effekt_kw × 0,31
```

Returtemperaturen hålls fast men dess kostnadsbelopp ska räknas om mot den
lägre scenariobundna energin för januari–april och oktober–december:

```text
sats_per_MWh = 2,4 × min(max(Tretur − 30, 0), 30)
              + 28 × max(Tretur − 60, 0)
returled = MWh_jan_apr_okt_dec × sats_per_MWh
```

Ingen förbättrad returtemperatur eller omedelbar effektbesparing får
tillskrivas Optimate.

## Oberoende facit

Använd minst denna literalfixture. Förväntade värden får inte genereras via
`beraknaOptimateScenario`, `beraknaArsprodukt*`, kontraktsfasaden,
`lagutnyttjandeavgift`, returtemperaturfunktionen eller annan
produktionsfunktion.

- Köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: exakt 80 procent av varje månad.
- Energipriser:
  `[584,584,584,442,294,294,294,294,294,442,442,584]` kr/MWh.
- Debiterbar effekt: `100` kW, heltal; policyfältet har samma värde.
- Bekräftat band: `1`.
- Normalårskorrigerad energi juni–maj: `200` MWh.
- Returtemperatur: `45` °C.

Oberoende komponentfacit exklusive moms:

- energi före: **59 452 kr**;
- kapacitetsled, låst: `100 × 1 661` = **166 100 kr**;
- utnyttjningstid: `200 × 1000 / 100` = **2 000 h**;
- lågnyttjandeavgift, låst:
  `(2 300 − 2 000) × 100 × 0,31` = **9 300 kr**;
- säsongsenergi före: **100 MWh**;
- returtemperatursats vid 45 °C: `(45 − 30) × 2,4` = **36 kr/MWh**;
- returtemperaturled före: `100 × 36` = **3 600 kr**.

| Scenario | Energifaktor | Energi | Lågnyttjande | Returled | Summa exkl. | Summa inkl. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Referens | 1,00 | 59 452,00 | 9 300,00 | 3 600,00 | 238 452,00 | 298 065,00 |
| 10 % | 0,92 | 54 695,84 | 9 300,00 | 3 312,00 | 233 407,84 | 291 759,80 |
| 15 % | 0,88 | 52 317,76 | 9 300,00 | 3 168,00 | 230 885,76 | 288 607,20 |
| 20 % | 0,84 | 49 939,68 | 9 300,00 | 3 024,00 | 228 363,68 | 285 454,60 |

Besparing inklusive moms ska vara exakt
**6 305,20 / 9 457,80 / 12 610,40 kr**.

Lägg dessutom separata gränsprov:

- `normalarskorrigerad_energi_mwh=230`, effekt 100 kW ger exakt
  2 300 timmar och **0 kr** lågnyttjandeavgift, före och efter;
- returtemperatur 30 °C ger **0 kr/MWh**;
- returtemperatur 60 °C ger `30 × 2,4 = 72 kr/MWh`;
- returtemperatur 65 °C ger `30 × 2,4 + 5 × 28 = 212 kr/MWh`, så den andra
  marginaltrappan bevisligen används utan genomsnittssats eller nollklampning.

## Fail-closed-grindar

Bind mekaniskt i både Neptune och skills att Wave 3i innehåller exakt den
enda kontraktsgatade katalogprodukten vars ordnade justeringstyper är
`low_utilization` och `incremental_return_temperature`. Bind hela Telges
råkontrakt, inte bara valda toppfält:

- `cost_path=kontrakt_arskostnad`, `_kraver_kontrakt=true`,
  `stodjer_aktuell_arskostnad=true`, `stodjer_besparing=false`;
- moms, full ordnad månadsprislista, `manadsperiodisering`, `fast_avgift`;
- full kapacitet: kW, `kw_faktor=1`, tre ordnade band och alla prisparametrar;
- båda ordnade justeringsobjekten med samtliga parametrar, månader,
  trösklar, satser, enheter, formler och periodiseringsfält;
- exakt fyra policyfält med fulla råegenskaper:
  `telge_debiterbar_effekt_kw`, `normalarskorrigerad_energi_mwh`,
  `returtemperatur_c`, `telge_vald_niva_id`;
- effektfältet är årsvis heltal inom befintlig nollgräns, bandfältet
  `band_id`, övriga två årsvisa numeriska fält med katalogens exakta gränser;
- exakt effekt-/bandbindning, `series_fields=[]`, `history_fields=[]`, inget
  behörighetsvillkor och inga dokumenterade exkluderingar.

Lägg mutationsprov som minst fäller saknat/extra Wave-3i-ID, fel backend,
status eller cost path, ändrad prislista/kapacitet/band, extra eller ändrat
justeringsfält, fel ordning, formel, sats, tröskel eller månad, fel
policyfält/gräns/typ/upplösning/bindning samt extra serie-/historikfält.

Scenario-/adapterproven ska typat blockera saknad eller ogiltig energi,
icke-heltalseffekt, saknad eller fel debiterbar effekt, band,
normalårsenergi eller returtemperatur. Jönköping och det syntetiska
`riksgenomsnitt` ska fortsatt vara stängda för både intern och publik grind.

## Leveransgrind vid en senare godkänd start

Kör riktade Wave-3i-prov, alla berörda äldre snapshot-/backendprov, hela
Vitest, `npx tsc --noEmit`, produktionsbygge med återställd genererad
`dist`, hela skills-pytestsviten, generatorns `--check` samt
`git diff --check` i båda repona.

Committera lokalt och avgränsat. Bevara samtliga befintliga orelaterade
ändringar och otrackade filer; rör inte `conversations/automation/`.
Ingen publik aktivering, mainflytt eller push. Lämna en ny unik, committad
`REVIEW_READY: Codex` med fulla hashar, ancestry, testutfall och disposition
**60/1/1/15=77**.

`READY_FOR_APPROVAL: Robert`
