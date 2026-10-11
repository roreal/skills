---
handoff_id: "2026-10-11-002"
created_at: "2026-10-11T19:47:10+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3f — temperaturdifferens för Göteborg, Partille och Södertörn

Robert har efter den fjärrverifierade våg 3e-leveransen instruerat:
**"Välj och starta nästa våg"**. Nästa sammanhållna beroendeklass är exakt
hela den kvarvarande katalogmängden med justeringstypen
`temperature_difference`:

1. `goteborg-energi`
2. `partille-energi-partille`
3. `sodertorns-fjarrvarme-sodertorns-fjarrvarme`

Implementera dem först som **interna, ej publika 10/15/20-piloter**. Ingen
av dem får läggas i `SCENARIO_PUBLIKT_AKTIVERADE_ID` i detta steg.

## Verifierad bas

- Neptune live `origin/main`:
  `f13187af603ae131271331b5840f5ceb269dcaf0`.
- skills live `origin/main` och lokal bas före denna handoff:
  `9487764ee64afa9df57b94bf22dfc337689e0dc1`.
- Nuvarande disposition:
  **52 publika / 0 interna / 1 prototyp / 24 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från exakt den
verifierade live-basen. Återanvänd inte en äldre Wave 3-worktree och flytta
inte den ordinarie checkoutens gren eller lokala `main`.

## Tillåten implementation och backendval

1. Lägg ett fryst, namngivet `WAVE_3F_PRODUCT_IDS` med exakt de tre ID:na
   ovan i alfabetisk ordning.
2. Lägg dem explicit i den interna backendkartan, utan härledning eller
   fallback:
   - Göteborg: `legacy_arskostnad`;
   - Partille: `kontraktsgatad_kostnadsled`;
   - Södertörn: `kontraktsgatad_kostnadsled`.
3. Utöka den befintliga fail-closed-mängden
   `LEGACY_KOSTNADSLED_TILLATNA_TARIFFER` med exakt Göteborgs ID. Detta är
   den enda tillåtna ändringen i `besparingsvarde.ts`; ingen formel eller
   annan backend får ändras. Bevisa med ett direkt backendprov att Göteborg
   accepteras och att ett annat ogranskat legacy-ID fortsatt avvisas.
4. Håll samtliga tre helt utanför den publika allowlisten. Publik lista ska
   fortsatt vara exakt 52 unika, frysta ID:n; intern pilotsnapshot blir 55.
5. Flytta exakt dessa tre matrisrader från `not_reviewed` till
   `godkand_intern_pilot_ej_publik`. Regenerera JSON/Markdown enbart via
   generatorn. Mål: **52/3/1/21=77**.

Ingen tariffdata, genererad tariffkatalog, prisformel, policyregister,
resultatkontrakt, kund-UI, browser/E2E-scenario, Enkey-fil eller annan
produkt får ändras. Den befintliga `temperature_difference`-motorn ska
återanvändas oförändrad.

## Bindande scenariokontrakt

Endast `manadsEnergiMwh` och därav `totalMwh` får ändras mellan referensen
och 10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.

Följande ska återanvändas bit-identiskt i samtliga fyra beräkningar:

- `avvikelse_c`;
- debiterbar effekt/`kapacitetKw`;
- bekräftat effektband för de kontraktsgatade produkterna;
- alla övriga fält, proveniensvärden och produkt-ID.

Ingen effektbesparing, automatisk effektuppskattning eller omklassning av
band får tillskrivas Optimate. Temperaturavvikelsen är en faktura-/
leverantörsuppgift och hålls fast: scenariot antar **ingen förbättring av
returtemperaturen**.

Det låsta temperaturvärdet innebär däremot inte ett låst kostnadsbelopp.
Den befintliga tariffmotorn ska räkna om ledet mot efterfallets lägre
energi under januari–april och oktober–december:

```text
temperaturled = MWh_jan_apr_okt_dec × rate × avvikelse_c
```

Ett positivt värde är en avgift. Ett negativt värde är en bonus. Motorn får
inte använda absolutbelopp, klampa tecknet, frysa referensjusteringen eller
anta en ny temperaturavvikelse.

## Oberoende facit

Använd minst följande gemensamma, icke-uniforma literalfixture. Förväntade
värden får inte genereras genom `beraknaOptimateScenario`,
`beraknaArsprodukt*`, `arskostnad`, `returtemperaturjusteringGoteborg` eller
annan produktionsfunktion.

- Köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: exakt 80 procent av respektive månad.
- Debiterbar effekt/`kapacitetKw=20` kW.
- Bekräftat band `1` för Partille och Södertörn.
- `avvikelse_c=3` °C i alla fyra beräkningar.
- Säsongsenergi januari–april och oktober–december: 100 MWh i referensen,
  därefter 92/88/84 MWh.
- Total energi efter 10/15/20 procent av styrbar rumsvärme:
  110,4/105,6/100,8 MWh.

Hårdkoda produkternas tolv månadsenergipriser från den checkade katalogen
i testet. Oberoende facit exklusive moms:

| Produkt | Energi före | Effektled | Temperaturled före | Summa före | Summa efter 10/15/20 % |
| --- | ---: | ---: | ---: | ---: | ---: |
| Göteborg | 50 308,00 | 39 030,00 | 2 100,00 | 91 438,00 | 87 245,36 / 85 149,04 / 83 052,72 |
| Partille | 59 036,00 | 28 860,00 | 2 100,00 | 89 996,00 | 85 105,12 / 82 659,68 / 80 214,24 |
| Södertörn | 53 992,00 | 37 500,00 | 660,00 | 92 152,00 | 87 779,84 / 85 593,76 / 83 407,68 |

Temperaturleden efter 10/15/20 procent är:

- Göteborg och Partille: `1 932,00 / 1 848,00 / 1 764,00` kr;
- Södertörn: `607,20 / 580,80 / 554,40` kr.

Förväntad referenskostnad inklusive moms och besparing inklusive moms:

| Produkt | Referens inkl. moms | Besparing 10/15/20 % |
| --- | ---: | ---: |
| Göteborg | 114 297,50 | 5 240,80 / 7 861,20 / 10 481,60 |
| Partille | 112 495,00 | 6 113,60 / 9 170,40 / 12 227,20 |
| Södertörn | 115 190,00 | 5 465,20 / 8 197,80 / 10 930,40 |

Lägg dessutom ett oberoende teckentest med negativ `avvikelse_c` som
bevisar att bonusen förblir negativ men minskar i absolutbelopp när samma
temperaturavvikelse multipliceras med mindre säsongsenergi. Testet ska
fälla fryst justering, absolutbelopp och nollklampning.

## Fail-closed-grindar

Bind både Neptune- och skills-sidan till att `WAVE_3F_PRODUCT_IDS` är exakt
hela katalogmängden vars `justeringar` innehåller
`type === 'temperature_difference'`. Ingen fjärde produkt eller annan
justeringstyp får öppnas indirekt.

Bind per produkt exakt:

- en enda justering, utan extra led;
- månader `[1,2,3,4,10,11,12]`;
- formel
  `energy_MWh * rate * (customer_return_degC - reference_return_degC)`;
- Göteborg och Partille: `rate=7`,
  `reference='network_monthly_mean'`;
- Södertörn: `rate=2.2`,
  `reference='previous_winter_network_mean'`;
- `indatafalt` för `avvikelse_c`: °C, default 0, slutet intervall
  `[-10;10]`, `heltal=false`;
- `cost_path`: Göteborg `legacy_besparing`, övriga två
  `kontrakt_arskostnad`;
- `capacity_rule='effekt'` och bandantal Göteborg/Partille/Södertörn
  exakt 6/7/4;
- Göteborg: inga kontraktsfält, serie- eller historikfält;
- Partille: exakta policyfält
  `{avvikelse_c, partille_debiterbar_effekt_kw,
  partille_vald_niva_id}`, alla `arsvis`, exakt effekt- och bandbindning;
- Södertörn: exakta policyfält
  `{avvikelse_c, sodertorn_debiterbar_effekt_kw,
  sodertorn_vald_niva_id}`, alla `arsvis`, exakt effekt- och bandbindning;
- samtliga: `series_fields=[]`, `history_fields=[]`, inget
  behörighetsvillkor.

Lägg negativa mutationsprov som minst fäller fel/extra justeringstyp,
saknad produkt i den globala temperaturmängden, fel sats, månader,
referens eller formel, fel inputfältsgräns, fel backend/cost path, fel
bandantal, fel/saknad effekt- eller bandbindning, fel policyfält, extra
serie-/historikfält och fel upplösning.

Scenario-/adapterproven ska typat blockera ogiltig energi, effekt eller
band enligt respektive backend. Partille och Södertörn ska blockera
saknat/ogiltigt `avvikelse_c`, effektfält och band. Göteborg ska bevara sin
befintliga dokumenterade neutral-default `avvikelse_c=0` när fältet saknas,
och ett explicit giltigt värde ska nå den riktiga motorn. Ändra inte
Göteborgs befintliga generella `resolveraFalt`-/klampningskontrakt i denna
våg; bind i stället katalogens gränser mekaniskt och använd värden inom
intervallet i scenarioproven. Alla tre ska vara sanna i den interna grinden
och falska i den publika.

## Leveransgrind

Kör minst:

- riktade Wave-3f-prov inklusive direkt legacy-backendprov;
- berörda bas-/Wave-2/3a/3b/3c/3d/3e-snapshotprov;
- hela Vitest;
- `npx tsc --noEmit`;
- `npm run build`, därefter återställ endast genererad `dist/`-smuts;
- skills pytest;
- matrisgeneratorns `--check`;
- `git diff --check` i båda reporna.

Committera lokalt och avgränsat. Bevara samtliga befintliga orelaterade
ändringar och otrackade filer i skills-repot; staga dem aldrig. Rör inte
`conversations/automation/`.

Ingen publik aktivering, mainflytt eller push. Lämna en ny unik,
committad `REVIEW_READY: Codex` med fulla hashar, ancestry, testutfall och
disposition **52/3/1/21=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
