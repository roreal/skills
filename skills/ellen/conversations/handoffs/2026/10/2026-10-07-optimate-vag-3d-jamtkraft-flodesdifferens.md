---
handoff_id: "2026-10-07-002"
created_at: "2026-10-07T12:53:47+02:00"
from: Robert/Codex
to: Claude
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3d — intern pilot för Jämtkrafts flödesdifferens

## 1. Mål och exakt scope

Robert instruerade efter den avslutade pausen: **"Nu kan du köra vidare"**.
Implementera därför en **intern, ej publik** 10/15/20-pilot för exakt dessa
tre produkt-ID:n, i alfabetisk ordning:

1. `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge`
2. `jamtkraft-brunflo-och-opevagen`
3. `jamtkraft-ostersund-froson-as`

Detta är en sammanhållen beroendeklass i den checkade täckningsmatrisen:
verkliga 2026-produkter, `cost_path=kontrakt_arskostnad`,
`capacity_rule=effekt`, fem effektband, exakt en justering av typen
`flow_difference`, årsvärdet `flode_okt_apr_m3`, och inga seriefält eller
behörighetsvillkor. Umeå Energi ingår **inte**: dess
`asymmetric_flow_difference` är en annan formel och ska granskas separat.

Verifierade baser vid handoffen:

- Neptune `origin/main`:
  `8abed657b88acafe6700f2b7735702bb03c7286a`;
- skills `HEAD` och `origin/main`:
  `4a3316b468afe5dce0e3ccc186338e72c5383330` före denna handoffcommit.

Neptunes ordinarie checkout ligger på en äldre Wave-3b-gren och får inte
användas som bas. Skapa en ny isolerad worktree/gren direkt från exakt den
verifierade `origin/main`-spetsen ovan. Flytta inte lokal `main`.

## 2. Bindande scenariokontrakt

- Lägg samtliga tre explicit bakom backend
  `kontraktsgatad_kostnadsled`. Ingen automatisk härledning eller fallback.
- Skapa/exportera en fryst `WAVE_3D_PRODUCT_IDS` som mekaniskt innehåller
  exakt de tre ID:na ovan.
- Endast `manadsEnergiMwh` och därav `totalMwh` får ändras mellan referens
  och 10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.
- Återanvänd exakt samma indata för `flode_okt_apr_m3`, debiterbar effekt,
  band-ID, historik/proveniens och samtliga övriga policyfält i alla fyra
  beräkningar.
- Det låsta **flödesvärdet** innebär inte ett låst **kostnadsled**.
  Jämtkrafts befintliga tariffmotor räknar
  `3 × (flode_okt_apr_m3 − 19 × MWh_okt_apr)`. När energiserien minskar
  ska justeringen därför räknas om från samma flöde och den nya
  oktober–aprilenergin. Ändra eller specialbehandla inte kostnadsmotorn för
  att hålla justeringsbeloppet konstant.
- Debiterbar effekt och valt band hålls däremot helt oförändrade. Ingen
  påstådd effektbesparing eller automatisk omklassning av band ingår.
- Den interna pilotgrinden ska bli sann för alla tre. Den publika grinden
  och `SCENARIO_PUBLIKT_AKTIVERADE_ID` ska förbli exakt de redan
  publicerade 48 produkterna; publik grind ska vara falsk för de tre nya.

Om någon katalogpost inte längre uppfyller kontraktet ska leveransen stoppa
fail-closed med `BLOCKED: Codex`. Bredda inte scope och ändra inte tariffen.

## 3. Oberoende facit och testkrav

Lägg en ny tabellstyrd Wave-3d-testfil som täcker exakt alla tre ID:n och
använder den riktiga, checkade katalogen. Förväntade värden får inte
genereras genom `beraknaOptimateScenario`, `beraknaArsprodukt*`,
`flodesdifferens` eller annan produktionsfunktion.

Använd gärna följande gemensamma, avsiktligt icke-uniforma literalfixture;
den ger rena kontrolltal och provar säsongsberoendet:

- total köpt värme jan–dec:
  `[18, 16, 14, 10, 6, 3, 2, 3, 6, 10, 14, 18]` MWh, totalt 120 MWh;
- styrbar rumsvärme: exakt 80 % av respektive månad;
- `flode_okt_apr_m3=1900`;
- debiterbar effekt 20 kW och band `1`.

Oktober–aprilenergin är då 100 MWh och referensjusteringen exakt 0 kr.
Efter 10/15/20 % minskning av den styrbara rumsvärmen blir säsongsenergin
92/88/84 MWh och det oberoende flödesfacit blir 456/684/912 kr. Effektledet
är alltid `20 × 1606 = 32 120` kr.

Hårdkoda/litteralisera dessutom de tre produkternas tolv månadsenergipriser
ur katalogen. Med fixturen ovan är oberoende referensenergi:

| Produkt | Energi före | Summa exkl. före |
| --- | ---: | ---: |
| Östersund/Frösön/Ås | 62 768 kr | 94 888 kr |
| Brunflo/Opevägen | 67 568 kr | 99 688 kr |
| Åre/Järpen/m.fl. | 76 704 kr | 108 824 kr |

För 10/15/20 ska facit räknas i testet från de litteraliserade
månadspriserna och fixturevärdena med en handskriven formel, inte genom en
produktionsentry. Bevisa för varje produkt:

- referens och samtliga tre scenariers energi, effekt/fast, justering,
  summa exklusive/inklusive moms samt `kostnadsskillnadKr`;
- att energidelen minskar, effektledet är identiskt och
  flödesdifferensbeloppet ökar enligt 456/684/912 kr när samma flöde möter
  lägre säsongsenergi;
- att ändrad energi utanför justeringens månader inte ändrar
  flödesdifferensen, medan en ändring i en säsongsmånad ger exakt
  `-19 × 3 × deltaMWh` i justeringsledet;
- riktig katalogbindning: `flow_difference`, sats 3, referens 19,
  månader `[1,2,3,4,10,11,12]`, fem band, produktens exakta effekt- och
  bandnycklar, årsupplöst `flode_okt_apr_m3`, kontraktsgating samt
  `stodjer_aktuell_arskostnad=true`/`stodjer_besparing=false`;
- fail-closed för saknat, negativt, `NaN` och `Infinity` i
  `flode_okt_apr_m3`, saknad/ogiltig effekt eller band samt ett okänt ID;
- att befintlig aktuell-årskostnadsväg fortfarande ger samma referens som
  scenariomotorn för identiskt underlag.

Bind att pilotsnapshoten blir exakt 51 (48 tidigare + dessa 3), medan den
publika listan förblir exakt 48, fryst och utan dubbletter. Uppdatera äldre
snapshotförväntningar mekaniskt utan att ändra deras sakpåståenden.

## 4. Täckningsmatris i skills-repot

- Skapa en fail-closed `WAVE_3D_PRODUCT_IDS` med exakt samma tre ID:n.
- Bind varje ID mot exakt `adjustment_types=[flow_difference]`,
  `cost_path=kontrakt_arskostnad`, `capacity_rule=effekt`, fem band,
  `series_fields=[]`, årsupplöst `flode_okt_apr_m3`, produktspecifik
  effekt-/bandnyckel och rätt historikfält.
- Sätt endast dessa tre till `godkand_intern_pilot_ej_publik` och
  regenerera JSON/Markdown enbart via generatorns `--write`.
- Lägg mutationsprov som visar att fel justeringstyp, extra seriefält,
  fel/saknad flödesupplösning, fel antal band eller fel kapacitetsform
  stänger grinden.

Målfördelning: **48 publika / 3 interna / 1 prototyp / 25 ogranskade = 77**.

## 5. Tillåtet och förbjudet

Tillåtet: Neptunes Optimate-pilotallowlist/scenariokod, en ny Wave-3d-
testfil och minimala mekaniska snapshotuppdateringar i äldre Optimate-prov;
skills matrisgenerator, dess prov och de två genererade matrisartefakterna.

Förbjudet: tariffdata/genererad tariffkatalog, `fjarrvarme.ts`, övrig
kostnadsmotor, resultatkontrakt/policyregister, `stodjer_besparing`,
`stodjer_aktuell_arskostnad`, kund-UI, publik aktivering, browser/E2E-
aktivering, Enkey, Umeå eller andra produkter, mainflytt, push,
force/rebase/reset samt `conversations/automation/`.

Bevara samtliga befintliga orelaterade ändringar och otrackade filer i
skills-repot. Staga aldrig dem i batchcommittarna.

## 6. Leveransgrind

Kör minst:

- riktade Wave-3d-prov samt berörda bas-/Wave-2/3a/3b/3c-prov;
- hela Vitest;
- `npx tsc --noEmit`;
- `npm run build`, följt av återställning av enbart spårad `dist/`-smuts;
- skills matrisprov och generatorns `--check`;
- `git diff --check` i båda repona.

Committera avgränsat i respektive repo. Uppdatera den aktiva sessionsfilen
append-only och lägg en ny, unik toppost i `conversations/index.md` med
`REVIEW_READY: Codex`, exakta fullhashar, testresultat och
48/3/1/25. Ingen publik aktivering, mainflytt eller push.

`APPROVED_FOR_IMPLEMENTATION: Claude`
