---
date: "2026-09-24"
status: approved-phase-a
participants:
  - Robert
  - Codex
topics:
  - Optimate
  - besparingspotential
  - Stockholm Exergi
  - portfoljutrullning
---

# Besparingspotential 10/15/20 och utrullning i portföljen

## Beslut

Robert vill ersätta Stockholm Exergis preliminära energiscenarier
15/20/25 procent med det försiktigare intervallet 10/15/20 procent. När
presentationen och beräkningen har accepterats för Stockholm ska motsvarande
funktion arbetas igenom för samtliga godkända energibolag.

Genomförandet sker på **nät-/tariffproduktnivå**, inte enbart per bolagsnamn.
Ett bolag kan ha flera produkter vars energi-, kapacitets-, flödes- och
returtemperaturdelar reagerar olika på samma energiminskning.

## Fas A – Stockholm som synligt acceptanstest

1. Ändra enbart Stockholm-prototypens huvudscenarier till 10, 15 och
   20 procent mindre **styrbar rumsvärme**.
2. Varmvatten och annan icke styrbar last ska vara oförändrad.
3. Samma Stockholmstariff och samma tariffmotor ska räkna både referens och
   scenario.
4. Debiterbar effekt, returtemperatur och kölddygnsvolym ska vara frysta i
   huvudscenarierna.
5. Den separata känslighetsanalysen för 20 procent lägre **debiterbar
   effekt** ska vara kvar oförändrad och får inte adderas in i
   huvudscenarioresultaten.
6. Resultaten ska fortsatt beskrivas som preliminära uppskattningar, inte
   uppmätt eller garanterad besparing. Komfortkravet verifieras separat.

Den generiska scenariomotorns interna Sundsvall-pilot ändras inte i denna
fas. Det gör Stockholmändringen liten och möjlig att bedöma visuellt innan
produktstandarden flyttas till den gemensamma motorn.

## Fas B – gemensam standard och aktuell täckningsmatris

Efter Roberts acceptans av Stockholm:

1. Gör 10/15/20 till gemensam scenariostandard i
   `optimateScenario.ts` och uppdatera kontrakt/tester.
2. Regenerera täckningsmatrisen från de då aktuella pushade
   `main`-versionerna. Äldre räkningar i 2026-09-22-planen får inte användas
   som aktuellt facit efter senare tariffaktiveringar.
3. Klassificera varje valbar verklig produkt efter vilka kostnadsled som
   påverkas eller måste frysas: energi, debiterbar kapacitet, flöde,
   returtemperatur, historik och behörighetsvillkor.
4. Håll den publika allowlisten stängd tills respektive tariffprodukt har
   klarat sina acceptansprov.

## Fas C – aktivering familjevis

Föreslagen ordning:

1. rena energi-/säsongstariffer och den redan interna Sundsvall-piloten,
2. kapacitets- och bandtariffer med fryst debiterbar kapacitet i
   huvudscenariot och separat villkorad effektkänslighet,
3. flödes-, avkylnings- och returtemperaturtariffer med uttryckliga
   antaganden och utan dold bonus,
4. produkter som kräver fakturahistorik, effektprofil, abonnemangsval eller
   andra behörighetsvillkor.

Varje produkt ska ha prov som visar att referensen är identisk med den redan
godkända årskostnaden och att endast tillåtna indata ändras. Den befintliga
formella flaggan `stodjer_besparing` ska inte massaktiveras; preliminär
Optimate-potential och formell verifierad besparing är skilda förmågor.

## Godkännandekriterium för hela utrullningen

- Alla aktuellt valbara verkliga tariffprodukter finns i den maskinellt
  genererade matrisen.
- Varje produkt är antingen publikt aktiverad med gröna prov eller har en
  konkret, dokumenterad blockerare.
- Energi, fysisk effekt, debiterbar kapacitet, flöde/retur och kostnad
  redovisas separat.
- Inga generella procentsatser beskrivs som bevis på faktisk besparing.
