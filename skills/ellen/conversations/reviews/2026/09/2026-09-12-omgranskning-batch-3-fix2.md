---
review_id: "2026-09-12-026"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope: "Batch 3 rättningsrunda 2 efter granskning 025"
reviewed_heads:
  skills: "0d042723416e1bb23a2ef6c81fc46d05f25c98a2"
  enkey_agents: "f0a030f4b6d2b03f30f13c09f9b8d85c9ce886ac"
  neptune_academy: "46e6b51160051352b8d521918918edd50093a16a"
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
---

# Omgranskning av Batch 3 — rättningsrunda 2

## Beslut

**Changes required före aktivering.** De fyra fynden i granskning 025 är tekniskt
åtgärdade: produktadaptern kan föra `observeradPeriod`, generatorproveniensen är sann,
energifacit är oberoende och de publika blockeringsproven täcker båda familjerna samt
schablon. Samtliga fullsviter är gröna i Codex oberoende omkörning.

Den nya periodvägen blandar dock ihop två olika kontraktsbegrepp och registrerar därför
inte Kraftringens januari–februari-underlag sanningsenligt. Dessutom överlever de nya
periodvärdena ett leverantörsbyte. Rätta dessa två avgränsade UI-/kontraktsfynd i en
tredje rättningsrunda; övriga delar ska lämnas oförändrade.

## Fynd

### P1 — generell källperiod har felaktigt gjorts till en enda kalendermånad

`kalperiodDefinition` och `matchningMotManad` är uttryckligen skilda i det etablerade
resultatkontraktet:

- `matchningMotManad` använder den maskinellt verifierbara formen `ÅÅÅÅ-MM` för ett
  månadsanrop;
- `kalperiodDefinition` beskriver en källperiod som motorn inte kan verifiera
  maskinellt. Kontraktets befintliga test använder exempelvis intervallet
  `2025-05-01/2026-04-30`.

Rättningen återanvänder nu `ISO_MANADSPERIOD`/`arGiltigManadsperiod` för **alla** krav
med `kalperiodDefinition`. UI:t kräver därmed `ÅÅÅÅ-MM` och Kraftringens DOM-prov
skickar `2026-01`. Det är inte en sann beskrivning av värdets källperiod: policyn säger
att den debiterbara effekten kommer från normalårskorrigerad energi för
**januari–februari** dividerad med 1416 timmar. En enda januarimånad kan därför inte
representera underlaget.

Detta syns också som en intern kontradiktion: samma kodbas godtar intervallet
`2025-05-01/2026-04-30` i `resultatkontrakt.test.ts`, men det nya generiska formuläret
avvisar det som felformaterat.

Rätta utan tariff-ID-kod:

- behåll `ÅÅÅÅ-MM` enbart där `matchningMotManad` faktiskt kräver en kalendermånad;
- ge `kalperiodDefinition` en separat, sann representation för källperioden. För den
  nuvarande årsfasaden räcker antingen en trimmad, icke-tom källperiod enligt det
  befintliga kontraktet eller ett uttryckligen beslutat och validerat ISO-intervall;
- låt Kraftringens fixture och normal-submit ange hela januari–februari-perioden, inte
  bara januari, och kontrollera att exakt samma värde når `IndataPost`;
- behåll saknad-period-felet fältnära och svenskt.

### P2 — periodvärden rensas inte vid leverantörs- eller energisystembyte

`handleFormChange` rensar sedan tidigare leverantörsbundna `faltVarden`,
`policyFaltRaw`, attesteringar och fältfel när `leverantorId` ändras eller användaren
byter bort från fjärrvärme. De två nya tillstånden
`policyFaltPerioderRaw` och `kapacitetObserveradPeriodRaw` rensas inte i någon av
grenarna.

Följden är att en period som angavs för en leverantör ligger latent kvar, återkommer om
användaren väljer tariffen igen och kan göra en senare submit komplett utan att
perioden har bekräftats på nytt. Detta bryter samma leverantörsbundna
tillståndsprincip som kommentaren i formuläret redan dokumenterar.

Rensa båda periodtillstånden i båda befintliga återställningsgrenarna. Lägg ett
DOM-regressionsprov som fyller Kraftringens period, byter leverantör och tillbaka och
visar att fältet är tomt samt att submit blockeras tills perioden anges igen. Bevisa
även att byte bort från fjärrvärme rensar värdet, gärna tabellstyrt i samma prov.

## Stängda fynd från granskning 025

- `byggIndataFranPolicy`/`byggKontraktIndata` och produkt-DTO:erna kan nu föra
  periodmetadata generiskt till rätt `IndataPost`.
- Kraftringens DOM-fixture använder nu sann `rullande=false` och icke-tom
  `kalperiod_definition`; normal submit når ett synligt uppskattat `snapshot` och
  saknad period ger fältnära fel utan rått kast.
- `tariffer.generated.ts` skiljer från Batch 2 med exakt en proveniensrad. Payloaden är
  oförändrad, den aktuella kataloghashen/committen är sann och synktestet är grönt.
- De nio energiprisproven använder hårdpinnade tolvmånaderspriser och oberoende
  handräknade belopp.
- E.ON/Navirum och Kraftringen provas tabellstyrt genom de publika års-, kronor-,
  schablon- och besparingsvägarna.
- Katalogscope, R06/R10, spärrar och dispositionen **16/48/28** är oförändrade; inga
  Batch 3-ID:n finns i den skarpa genererade tariffpayloaden.

## Oberoende verifiering utförd av Codex

- full Python-svit: **1009 passed, 4 skipped**;
- full TypeScript-svit: **997 passed i 36 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **10/10 scenarier godkända**;
- `git diff --check`: rent i samtliga tre granskade intervall;
- diff mot Batch 2 för `tariffer.generated.ts`: exakt **1 rad tillagd/1 borttagen**, bara
  katalogproveniens;
- inga Batch 3-ID:n hittades i skarp `tariffer.generated.ts`;
- de sedan tidigare orelaterade ändringarna i `neptune-marketing/dist` är orörda.

Codex första E2E-start stoppades av macOS-sandlådans Chromium-behörighet. Exakt samma
test kördes därefter med godkänd exekvering utanför sandlådan och blev 10/10 grönt;
detta är inte ett produktfel.

## Nästa steg för Claude

1. Separera generell `kalperiodDefinition`-källperiod från månadsformatet för
   `matchningMotManad`; använd hela januari–februari-perioden i Kraftringens verkliga
   produkt-/DOM-bevis.
2. Rensa båda nya periodtillstånden vid leverantörsbyte och byte bort från fjärrvärme,
   med ett DOM-regressionsprov.
3. Kör de riktade proven, full TypeScript, `tsc`, isolerat bygge, E2E och
   `git diff --check`. Python/katalog/generator behöver inte ändras eller köras om om
   diffen förblir helt begränsad till TypeScript-UI/kontrakt/test.
4. Dokumentera commit och stanna för Codex omgranskning.

**Ingen tariffaktivering, ingen borttagning av R06/R10 och ingen push.**
