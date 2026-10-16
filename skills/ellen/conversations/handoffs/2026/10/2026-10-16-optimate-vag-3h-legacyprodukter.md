---
handoff_id: "2026-10-16-001"
created_at: "2026-10-16T19:17:31+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3h — återstående verkliga legacyprodukter

Robert bad Codex välja nästa grupp men invänta resan och återupptog nu
arbetet med: **"Då kan vi köra igen"**.

Implementera exakt följande tre verkliga, icke kontraktsgatade
legacyprodukter som **interna, ej publika 10/15/20-piloter**:

1. `gotlands-energi-gotland-taxa-21-over-50-mwh-ar`
2. `molndal-energi`
3. `norrenergi`

De utgör en sluten grupp bland de 19 ogranskade: alla har
`cost_path=legacy_besparing`, befintligt besparingsstöd och ska använda
`legacy_arskostnad`. Lägg dem inte i `SCENARIO_PUBLIKT_AKTIVERADE_ID` i
detta steg.

## Verifierad bas och avgränsning

- Neptune live `origin/main`:
  `00fe4bfe840f3d6ae998674f5bad709c7773f97f`.
- skills live `origin/main` och lokal bas före handoffen:
  `4338ef06a2009010e397af640449606226760174`.
- Nuvarande disposition:
  **57 publika / 0 interna / 1 prototyp / 19 ogranskade = 77**.
- Måldisposition efter intern pilot:
  **57 publika / 3 interna / 1 prototyp / 16 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från verifierad
live-bas, lämpligen `optimate-vag-3h-legacyprodukter`. Återanvänd inte
våg 3g-worktreen och flytta inte ordinarie checkout eller lokal `main`.

Ingen tariffdata, genererad tariffkatalog, prisformel, policy, kund-UI,
browser/E2E, Enkey-fil, publik allowlist eller annan produkt får ändras.
Återanvänd den befintliga tariffneutrala scenariomotorn och
`legacy_arskostnad`-backenden. Den enda nödvändiga domänutvidgningen är
de två exakta, fail-closed allowlisterna i `optimateScenario.ts` och
`besparingsvarde.ts`, med prov som binder att de inte glider isär.

## Gemensamt scenariokontrakt

1. Skapa/exportera ett fryst `WAVE_3H_PRODUCT_IDS` med exakt de tre ID:na
   ovan i alfabetisk ordning. Lägg exakt samma tre explicit i den interna
   backendkartan som `legacy_arskostnad` och i legacy-backendens separata
   domänallowlist. Ingen härledning eller fallback.
2. Endast `manadsEnergiMwh` och därav `totalMwh` får ändras mellan
   referensen och 10/15/20-scenarierna. Endast explicit styrbar rumsvärme
   reduceras.
3. Kapacitet, kapacitetsband, föregående års energi, högsta dygnsenergi,
   normalårskorrigerad energi, flöde, avkylning, returtemperatur och alla
   övriga fakturafält ska återanvändas bit-identiskt i samtliga fyra
   beräkningar.
4. Ingen effektbesparing, automatisk bandväxling, minskat fakturerat flöde,
   förbättrad avkylning/returtemperatur eller ändrat rabattunderlag får
   tillskrivas Optimate. Kostnadsled som beror på den köpta energin får
   däremot följa den lägre energiserien enligt tariffens oförändrade formel.
5. Intern grind ska vara sann för exakt de tre nya ID:na. Publik grind ska
   vara falsk och den publika allowlisten fortsatt exakt 57 unika, frysta
   ID:n.
6. `riksgenomsnitt` är syntetiskt och ingår inte. Finspång, Jönköping,
   Telge och samtliga Vattenfallprodukter ska förbli stängda.

Om någon katalogpost inte längre uppfyller kontraktet: stoppa fail-closed
med `BLOCKED: Codex`; bredda inte scope och ändra inte tariffen.

## Oberoende gemensam energifixtur

För samtliga tre produkter används:

- köpt värme januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh;
- styrbar rumsvärme: exakt 80 procent av varje månad;
- `energyProvenance=confirmed_mwh`;
- efterserierna är därför exakt 92/88/84 procent av referensserien och
  totalerna 110,4 / 105,6 / 100,8 MWh.

Förväntade belopp ska vara literaler som räknats ut från formlerna nedan.
Testets förväntade värden får aldrig genereras via
`beraknaOptimateScenario`, `beraknaArsprodukt*`, `arskostnad` eller någon
annan produktionsfunktion.

### Gotlands Energi taxa 21

Lås fälten till `avkylning_c=35` och `foregaende_ars_mwh=300`.
Föregående år ligger därmed i rabattbandet 250–1249 MWh med 4 kr/MWh;
detta fält får aldrig ersättas av efterfallets lägre energi. Taxa 21:s
>50-MWh-omfattning är uppfylld även i 20-procentsscenariot (100,8 MWh),
så inget produktbyte eller behörighetsantagande behövs.

- Energipris: 1 020 kr/MWh i tolv månader.
- Avkylningsavgift: 30 kr/MWh under jan–maj och sep–dec; referensens
  berörda energi är 112 MWh.
- Volymrabatt: −4 kr/MWh på all köpt energi.
- Referens exkl./inkl. moms: **125 280 / 156 600 kr**.
- Efter 10/15/20 procent exkl. moms:
  **115 257,60 / 110 246,40 / 105 235,20 kr**.
- Besparing 10/15/20 procent inkl. moms:
  **12 528 / 18 792 / 25 056 kr**.

Lägg gränsprov för dödbandet 38/48 °C samt rabattbandens kanter. Bevisa
att ändrat efterfall aldrig väljer om `foregaende_ars_mwh`.

### Mölndal Energi

Lås `kapacitetKw=50`, `hogsta_dygnsenergi_kwh=1200` och
`flode_m3=2000`. Kapacitetsbasen 1 200 kWh/dygn ligger i band 3 och
kapacitetsledet är `1200 × 72,84 = 87 408 kr`. Flödesavgiften är
`2000 × 4,31 = 8 620 kr` och ska vara oförändrad före/efter.

- Referensens energi: **42 486 kr**.
- Referens exkl./inkl. moms: **138 514 / 173 142,50 kr**.
- Efter 10/15/20 procent exkl. moms:
  **135 115,12 / 133 415,68 / 131 716,24 kr**.
- Besparing 10/15/20 procent inkl. moms:
  **4 248,60 / 6 372,90 / 8 497,20 kr**.

Lägg gränsprov runt kapacitetsbas 1 200/1 201 kWh/dygn och bevisa att
varken band, högsta dygn eller fakturerat flöde räknas om av efterenergin.

### Norrenergi

Lås `kapacitetKw=100`, `normalarskorrigerad_energi_mwh=150` och
`returtemperatur_c=40`. Kapacitetsledet är
`2 849 + 100 × 1 128 = 115 649 kr`. Normalårsvärdet ger 1 500
utnyttjningstimmar och en oförändrad lågutnyttjandeavgift
`(2100−1500) × 100 × 0,38 = 22 800 kr`.

Returtemperaturledet är marginellt: 10 grader över första tröskeln ×
3,40 kr/MWh/°C. Referensens energi i jan–apr och okt–dec är 100 MWh,
vilket ger 3 400 kr. Ledet får följa energin, men returtemperaturen hålls
40 °C.

- Referensens energi: **69 543 kr**.
- Referens exkl./inkl. moms: **211 392 / 264 240 kr**.
- Efter 10/15/20 procent exkl. moms:
  **205 556,56 / 202 638,84 / 199 721,12 kr**.
- Besparing 10/15/20 procent inkl. moms:
  **7 294,30 / 10 941,45 / 14 588,60 kr**.

Lägg gränsprov vid returtemperatur 30 och 60 °C, ett prov över 60 °C som
bevisar marginalsteget 26,50, samt utnyttjningstid på båda sidor om 2 100
timmar. Bevisa att normalårsvärde, effekt och returtemperatur inte ändras
mellan scenarierna.

## Fail-closed-grindar

Bind mekaniskt i både Neptune och skills att våg 3h innehåller exakt ovan
tre produkter och bind per produkt hela råkontraktet, minst:

- icke kontraktsgatad produkt, `cost_path=legacy_besparing`,
  `savings_today=true`, backend `legacy_arskostnad`;
- exakt månadsprislista, momsgrund, kapacitetstyp/enhet/`kw_faktor`,
  bandtabell, periodisering, justeringarnas ordning och fulla nyckelmängd;
- Gotland: exakt `cooling_deadband`- och `volume_discount`-kontrakt,
  indatafältens gränser/default/proveniens och ingen kapacitetsavgift;
- Mölndal: exakt 14 kapacitetsband, helårs-`volume` 4,31 kr/m³ samt
  `flode_m3`/`hogsta_dygnsenergi_kwh`;
- Norrenergi: exakt sju kapacitetsband, `low_utilization` och
  `incremental_return_temperature` inklusive månader, trösklar, satser,
  formelbas och fältkontrakt;
- inget nytt serie-/historik-/behörighetsfält och inga dokumenterade
  exkluderingar om snapshoten inte redan anger dem.

Lägg riktade mutationsprov som fäller saknad/extra produkt, fel backend,
pris, band, tröskel, sats, månad, enhet, fältnyckel/default/gräns,
periodisering, justeringsordning och status. Direkta backendprov ska fortsatt
avvisa okända, kontraktsgatade och genuint ogranskade ID:n.

## Skills-matris och leveransgrind

- Flytta exakt de tre raderna från `not_reviewed` till
  `godkand_intern_pilot_ej_publik`.
- Regenerera JSON/Markdown endast via generatorn.
- Bind måldispositionen **57/3/1/16=77**.
- Rör inte `conversations/automation/` eller befintliga orelaterade filer.

Kör minst riktade våg-3h-prov, berörda äldre snapshot-/legacyprov, hela
Vitest, `npx tsc --noEmit`, `npm run build` med återställning av enbart
genererad `dist/`-smuts, skills pytest, generatorns `--check` och
`git diff --check` i båda reporna.

Committera lokalt och avgränsat. Ingen publik aktivering, mainflytt eller
push. Lämna en ny unik, committad `REVIEW_READY: Codex` med fulla hashar,
ancestry, testutfall och disposition **57/3/1/16=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
