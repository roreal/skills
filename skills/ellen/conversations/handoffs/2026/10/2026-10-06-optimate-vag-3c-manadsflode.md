---
handoff_id: "2026-10-06-002"
created_at: "2026-10-06T08:46:56+02:00"
from: Robert/Codex
to: Claude
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3c — intern pilot för åtta månadsvisa flödesprodukter

## 1. Mål och avgränsning

Implementera en **intern, ej publik** 10/15/20-pilot för exakt dessa åtta
produkt-ID:n, i alfabetisk ordning:

1. `lulea-energi-lulea`
2. `malarenergi-vasteras-och-hallstahammar-24-lagenheter`
3. `nevel-gimo-osterbybruk-och-osthammar`
4. `oresundskraft-angelholm-normal`
5. `oresundskraft-helsingborg-normal`
6. `piteenergi-norrfjarden-och-sjulnas`
7. `piteenergi-pitea-centrala-natet`
8. `tekniska-verken-linkoping-linkoping`

De utgör en sammanhållen beroendeklass i den checkade täckningsmatrisen:
verkliga 2026-produkter, `cost_path=kontrakt_arskostnad`, en `volume`-
justering, `series_fields=[flode_m3]` och
`measurement_resolutions.flode_m3=manadsvis`, utan dokumenterade
exkluderingar. Lågtemperaturvarianten för Tekniska Verken ingår **inte**.

Verifierade baser:

- Neptune `origin/main`:
  `ae179f0feb0ef0a8ec6e09b6b084d0365883b24f`;
- skills publicerade `origin/main`-bas:
  `17796b686edd76eaad3356376b7e5804491e7a35`; implementationsarbetet ska
  utgå från den committade handoff-signalen ovanpå denna bas, inte kräva att
  lokal skills-HEAD fortfarande är identisk med remote efter signalcommitten.

Skapa en isolerad Neptune-gren/worktree direkt från exakt den verifierade
`origin/main`-spetsen. Flytta inte lokal `main` och återanvänd inte den gamla
Wave-3b-grenen som implicit bas.

## 2. Bindande scenariokontrakt

- Endast `manadsEnergiMwh` och därav `totalMwh` får ändras mellan referens
  och 10/15/20-scenarierna. Endast styrbar rumsvärme reduceras.
- Hela tolvmånadersserien `policyFalt.flode_m3` ska återanvändas oförändrad,
  med samma månadsordning och värden. Säsongsjusteringen ska därför vara
  exakt bit-identisk i referens och samtliga tre efter-scenarier.
- För Luleå, Nevel, båda Öresundskraft-produkterna, båda PiteEnergi-
  produkterna och Tekniska Verken ska debiterbar effekt, band-ID,
  bindningsnycklar, historik och alla övriga policyfält också vara låsta.
- Mälarenergis 2–4-lägenhetsprodukt har ingen kapacitetsavgift och noll band;
  den ska hanteras/provas uttryckligen som fast årsavgift + energi +
  säsongsflöde, aldrig tvingas genom ett påhittat effekt- eller bandfält.
- Lägg samtliga åtta explicit bakom backend
  `kontraktsgatad_kostnadsled`. Ingen automatisk härledning eller fallback.
- Skapa/exportera en fryst `WAVE_3C_PRODUCT_IDS` som mekaniskt är exakt
  mängden ovan. Intern pilotgrind ska vara sann för alla åtta, men
  `SCENARIO_PUBLIKT_AKTIVERADE_ID` ska förbli exakt de redan publicerade
  40 produkterna och publik grind ska vara falsk för alla åtta nya.

Om någon katalogpost inte längre uppfyller detta kontrakt: stoppa
fail-closed med `BLOCKED: Codex`; bredda inte scope och ändra inte tariffen.

## 3. Oberoende facit och regressionskrav

Lägg en ny tabellstyrd Wave-3c-testfil som täcker exakt alla åtta ID:n.

- Använd en avsiktligt **icke-uniform tolvmånadersserie** för `flode_m3`,
  så att fel månadsordning eller helårssummering inte kan passera.
- Hårdkoda/litteralisera per produkt de katalogvärden som behövs för ett
  oberoende facit: justeringens sats och exakta säsongsmånader,
  månadsenergipriser, fast avgift samt giltigt effekt-/bandfacit där det
  finns. Generera aldrig förväntat resultat genom
  `beraknaOptimateScenario`, `beraknaArsprodukt*` eller annan
  produktionsfunktion.
- Bevisa referenskostnad och 10/15/20 för varje produkt. Energidelen får
  minska; fast/kapacitet och säsongsflödesled ska vara exakt oförändrade.
- Bevisa att flödesjusteringen är `rate × summa(flode_m3)` för exakt postens
  egna säsongsmånader: en ändring i en säsongsmånad ska ge exakt satsens
  effekt, medan en ändring utanför säsongen ska ge noll.
- Bind per ID den riktiga katalogpostens `volume`-typ, månadsdelmängd,
  tolvmånaderskrav, kontraktsgating och rätt policy-/bandbindning.
- Lägg fail-closed-prov för saknad serie, fel antal värden, negativt värde,
  `NaN` och `Infinity`. Minst den direkta motorvakten och den auktoritativa
  kontraktsfasaden ska bevisas; återanvänd befintliga testhjälpare när det
  minskar duplicering utan att dölja vilket lager som testas.
- Bind att pilotsnapshoten blir exakt 48 (40 tidigare + dessa 8), medan den
  publika listan fortsatt är exakt 40, fryst och utan dubbletter. Uppdatera
  äldre snapshotförväntningar mekaniskt; ändra inte deras sakpåståenden.

## 4. Täckningsmatris

I skills-repot:

- skapa en fail-closed `WAVE_3C_PRODUCT_IDS` med exakt samma åtta ID:n;
- bind varje ID mot `volume`, `cost_path=kontrakt_arskostnad`, exakt
  `series_fields=[flode_m3]` och månadsvis upplösning;
- bind dessutom de sju kapacitetsprodukternas effekt-/bandform och
  Mälarenergis avsaknad av kapacitetsavgift/band separat;
- sätt endast dessa åtta till
  `godkand_intern_pilot_ej_publik` och regenerera JSON/Markdown via
  generatorn.

Målfördelning: **40 publika / 8 interna / 1 prototyp / 28 ogranskade = 77**.

## 5. Tillåtna och förbjudna ändringar

Tillåtet: Neptunes Optimate-allowlist/scenariokod, ny Wave-3c-testfil och
minimala mekaniska uppdateringar i äldre Optimate-tester; skills-
matrisgeneratorn, dess test och de två genererade matrisartefakterna.

Förbjudet: tariffdata/genererad tariffkatalog, kostnadsmotor,
resultatkontrakt/policyregister, `stodjer_besparing`,
`stodjer_aktuell_arskostnad`, kund-UI, publik aktivering, browser/E2E-
aktivering, Enkey, andra produkter, mainflytt, push, force/rebase/reset och
`conversations/automation/`.

## 6. Leveransgrind

Kör minst:

- riktade Wave-3c- samt berörda bas/Wave-2/3a/3b-prov;
- hela Vitest;
- `npx tsc --noEmit`;
- `npm run build`, följt av återställning av spårad `dist/`-testsmuts;
- skills matrisprov och generatorns `--check`;
- `git diff --check` i båda repona.

Committera avgränsat i respektive repo och skriv en ny unik
`REVIEW_READY: Codex` i aktiv session och index med exakta hashar,
testresultat och 40/8/1/28. Ingen publik aktivering, mainflytt eller push.

`APPROVED_FOR_IMPLEMENTATION: Claude`
