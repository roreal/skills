---
handoff_id: "2026-10-12-012"
created_at: "2026-10-12T20:57:05+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3g — Lidköpings signerade månadsvisa flödesjustering

Robert instruerade efter den fjärrverifierade våg 3f-leveransen:
**"Ok då kör vi nästa batch, välj ut lämpligt antal och dra igång Claude"**.

Codex har valt nästa minsta sammanhållna beroendeklass: exakt de två
återstående verkliga 2026-produkterna med justeringstypen
`signed_monthly_flow_adjustment`:

1. `lidkoping-energi-lidkoping-041-kw`
2. `lidkoping-energi-lidkoping-42-kw`

Implementera dem först som **interna, ej publika 10/15/20-piloter**. Lägg
dem inte i `SCENARIO_PUBLIKT_AKTIVERADE_ID` i detta steg.

## Verifierad bas och avgränsning

- Neptune live `origin/main`:
  `3f3d6ca97493df90a16b5d095724a42d5b126d33`.
- skills live `origin/main` och lokal bas före denna handoff:
  `9a9fe40171b392372b73a940daec1ce3964bd1df`.
- Nuvarande disposition:
  **55 publika / 0 interna / 1 prototyp / 21 ogranskade = 77**.
- Måldisposition efter intern pilot:
  **55 publika / 2 interna / 1 prototyp / 19 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från den verifierade
live-basen, lämpligen `optimate-vag-3g-lidkoping-signed-flow`. Återanvänd
inte en äldre Wave-3-worktree och flytta inte ordinarie checkout eller
lokal `main`.

Ingen tariffdata, genererad tariffkatalog, prisformel, befintlig
flödesmotor, policyregister, resultatkontrakt, kund-UI, browser/E2E,
Enkey-fil eller annan produkt får ändras. Återanvänd den befintliga
`signedMonthlyFlowAdjustment`-motorn och
`kontraktsgatad_kostnadsled`-backenden oförändrade.

## Bindande scenariokontrakt

1. Skapa/exportera ett fryst `WAVE_3G_PRODUCT_IDS` med exakt de två ID:na
   ovan, i alfabetisk ordning, och lägg båda explicit i den interna
   backendkartan som `kontraktsgatad_kostnadsled`. Ingen härledning eller
   fallback.
2. Endast `manadsEnergiMwh` och därav `totalMwh` får ändras mellan
   referensen och 10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.
3. Återanvänd bit-identiskt i samtliga fyra beräkningar:
   - debiterbar effekt/`kapacitetKw`;
   - bekräftat effektband;
   - de tre tolvmånadersserierna
     `lidkoping_kund_volym_m3`, `lidkoping_kund_avkylning_c` och
     `lidkoping_nat_avkylning_c`;
   - attestering, proveniens och alla övriga policyfält.
4. Ingen effektbesparing, automatisk bandväxling, förbättrad avkylning,
   minskad volym eller uppskattat nätmedel får tillskrivas Optimate.
   Serierna är faktura-/leverantörsvärden och hålls fast.
5. Eftersom den befintliga formeln
   `5 × Q_m × (1 − T_m/Tm_m)` inte använder energiserien ska hela
   flödesjusteringen vara exakt bit-identisk före och efter. Den får vara
   positiv avgift eller negativ kreditering; inget absolutbelopp,
   nollgolv eller teckenbyte.
6. Intern grind ska vara sann för båda. Publik grind ska vara falsk och
   den publika allowlisten fortsatt exakt 55 unika, frysta ID:n.

Om en katalogpost inte längre uppfyller kontraktet: stoppa fail-closed med
`BLOCKED: Codex`; bredda inte scope och ändra inte tariffen.

## Oberoende facit

Använd minst följande gemensamma literalfixture. Förväntade värden får
inte genereras genom `beraknaOptimateScenario`, `beraknaArsprodukt*`,
`beraknaArskostnadMedKontrakt`, `arskostnad` eller annan
produktionsfunktion.

- Köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: exakt 80 procent av respektive månad.
- Kundvolym Q:
  `[10,20,30,40,50,60,70,80,90,100,110,120]` m³.
- Kundavkylning T:
  `[20,22,24,26,28,30,32,34,36,38,40,42]` °C.
- Nätavkylning Tm: tolv gånger `40` °C, uttryckligen attesterad.
- Flödesjusteringens handräknade facit: exakt **520 kr exkl. moms** i
  referensen och alla tre efterfall.
- 0–41 kW: effekt `20` kW och bekräftat band `2`; kapacitetsled
  `3 852 + 20 × 1 521 = 34 272` kr.
- 42+ kW: effekt `100` kW och bekräftat band `1`; kapacitetsled
  `11 670 + 100 × 1 317 = 143 370` kr.

Hårdkoda de två produkternas tolv månadsenergipriser från katalogen i
testet. Oberoende facit:

| Produkt | Energi före | Kapacitet | Justering | Referens exkl./inkl. moms | Efter 10/15/20 % exkl. moms | Besparing 10/15/20 % inkl. moms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0–41 kW | 54 312 | 34 272 | 520 | 89 104 / 111 380 | 84 759,04 / 82 586,56 / 80 414,08 | 5 431,20 / 8 146,80 / 10 862,40 |
| 42+ kW | 57 106 | 143 370 | 520 | 200 996 / 251 245 | 196 427,52 / 194 143,28 / 191 859,04 | 5 710,60 / 8 565,90 / 11 421,20 |

Lägg också ett separat teckenprov med samma Q, `T=50` och `Tm=40` i alla
månader: flödesjusteringen ska vara exakt **−975 kr** både före och efter
10/15/20. Provet ska fälla nollklampning, absolutbelopp och felaktig
energikoppling.

## Fail-closed-grindar

Bind mekaniskt i både Neptune och skills att `WAVE_3G_PRODUCT_IDS` är
exakt hela katalogmängden vars enda justering har
`type === 'signed_monthly_flow_adjustment'`. Bind per produkt minst:

- `cost_path=kontrakt_arskostnad`, kontraktsgating,
  `stodjer_aktuell_arskostnad=true`, `stodjer_besparing=false`;
- justeringens `faktor_n=5` och exakt de tre fältnycklarna;
- `capacity_rule=effekt`, exakt två band, `kw_faktor=1`,
  `min_debiteringsbas=3`, rätt effektintervall och rätt prisparametrar;
- exakt fem policyfält: årsvis debiterbar effekt och band samt tre
  månadsvisa `number_series` med exakt 12 värden;
- Q: min 0 inklusive; T: inget påhittat min/max; Tm: min 0 exklusiv och
  `krav_attestering=true`;
- exakt effekt-/bandbindning;
- `series_fields` och `history_fields` exakt de tre serierna;
- inget behörighetsvillkor och inga extra justeringar eller
  dokumenterade exkluderingar.

Lägg riktade mutationsprov som minst fäller saknad/extra produkt, fel
justeringstyp/faktor/fältnyckel, fel backend/cost path, fel bandantal eller
bandparametrar, fel policyfält/upplösning/kardinalitet/gräns/attestering,
fel bindning, extra/saknad serie eller historikfält och fel status.

Scenario-/adapterproven ska typat blockera saknad serie, fel längd,
icke-ändligt element, negativ Q, Tm ≤ 0, saknad attestering samt
saknad/ogiltig effekt eller band. Ett okänt och ett genuint ogranskat
katalog-ID ska förbli stängda för båda grindarna.

## Skills-matris och leveransgrind

- Flytta exakt de två Lidköping-raderna från `not_reviewed` till
  `godkand_intern_pilot_ej_publik`.
- Regenerera JSON/Markdown endast via generatorn.
- Bind måldispositionen **55/2/1/19=77** och bevara den reserverade
  statusvokabulären.

Kör minst riktade Wave-3g-prov, berörda äldre snapshotprov, hela Vitest,
`npx tsc --noEmit`, `npm run build` med efterföljande återställning av
endast genererad `dist/`-smuts, skills pytest, generatorns `--check` samt
`git diff --check` i båda reporna.

Committera lokalt och avgränsat. Bevara alla befintliga orelaterade
ändringar och otrackade filer i skills; staga dem aldrig. Rör inte
`conversations/automation/`.

Ingen publik aktivering, mainflytt eller push. Lämna en ny unik,
committad `REVIEW_READY: Codex` med fulla hashar, ancestry, testutfall och
disposition **55/2/1/19=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
