---
handoff_id: "2026-10-02-004"
created_at: "2026-10-02T20:14:48+02:00"
from: Codex
to: Claude
status: approved-for-implementation
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# APPROVED_FOR_IMPLEMENTATION: Claude – Optimate våg 3a

## Mandat och mål

Robert har efter den publicerade våg 2 sagt **"OK kör igång Claude"**.
Implementera en intern, ej publik 10/15/20-pilot för exakt de 17 produkter
som använder `supply_temperature_adjusted_flow`: E.ON, Navirum och
Kraftringen.

Målet är en tariffkorrekt och konservativ före/efter-jämförelse där endast
validerad styrbar rumsvärme minskas. Leverantörens debiterbara effekt,
effekthistorik, valt band, uppmätt flöde och framledningstemperatur hålls
oförändrade. Leveransen får inte påstå att Optimate automatiskt sänker
flödes-/temperaturavgiften eller den debiterbara effekten.

Detta är endast implementation bakom intern spärr. Ingen publik aktivering,
mainflytt, merge, rebase eller push ingår. Lämna en committad
`REVIEW_READY: Codex` när hela kontrollpunkten är klar.

## Verifierade utgångslägen

- skills `main@925df36f3ef5e0a17c84feb4f6b04a77d353eaa7`, och
  `origin/main` matchar.
- neptune_academy `main@c9a8bb73fe83bba24d62cd65e6fd649899b1b82f`, och
  `origin/main` matchar. Den befintliga isolerade worktreen
  `.claude/worktrees/agent-ae46c6f3096412378` är ren vid samma commit.
- enkey-agents lokal `main@c0185263c2b8be2e4c1d7aa2ef5bd4f93e3c8d27` har
  orelaterade, lokala Milesight-ändringar och är helt utanför scope.
- Skills-arbetskopian har sedan tidigare orelaterade ändringar och ospårade
  underlag, inklusive brygginfrastruktur. Bevara dem och stagea endast exakt
  avsedda filer; använd aldrig `git add .`.

Stoppa med en unik committad `BLOCKED: Codex` om Neptune-basen har flyttats,
den isolerade kandidaten inte kan hållas ren, eller implementationen kräver
ändring av tariffdata, prisformler eller Enkey. Skriv inte om historik.

## Exakt produktmängd

1. `e-on-jarfalla-jarfalla-och-upplands-bro-bostader`
2. `e-on-jarfalla-jarfalla-och-upplands-bro-bostader--bas-delvarme`
3. `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter`
4. `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter--bas-delvarme`
5. `e-on-malmo-malmo-och-burlov-bostader`
6. `e-on-malmo-malmo-och-burlov-bostader--bas-delvarme`
7. `e-on-malmo-malmo-och-burlov-ovriga-fastigheter`
8. `e-on-malmo-malmo-och-burlov-ovriga-fastigheter--bas-delvarme`
9. `kraftringen-kraftringen`
10. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader`
11. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader--bas-delvarme`
12. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter`
13. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter--bas-delvarme`
14. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader`
15. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader--bas-delvarme`
16. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter`
17. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter--bas-delvarme`

Bind listan som en namngiven, fryst `WAVE_3A_PRODUCT_IDS` och bevisa
maskinellt att den är exakt samma mängd som matrisens 17 våg-3-rader med
`adjustment_types` innehållande `supply_temperature_adjusted_flow`. Ingen
annan våg-3-produkt, syntetisk produkt eller publik produkt får följa med.

## Bindande scenariokontrakt

Klassificera varje prisberoende uttryckligen:

- **Ändras:** endast den validerade månadsserien för styrbar rumsvärme,
  minskad med 10, 15 respektive 20 procent. Övrig köpt värme ligger kvar.
- **Låses:** produkt-ID, prisår, månadskalender, fasta avgifter,
  debiterbar effekt/kapacitet, valt band, alla historik-/snapshotfält,
  `flode_m3`, `framledningstemperatur_c` och andra policyfält.
- **Följer av de låsta indata:** kapacitetskostnad och
  flödes-/temperaturjustering ska vara identiska före och efter. Energiledet
  räknas om av den befintliga tariffmotorn från efterfallets energiserie.
- **Okänt och inte påstått:** verkligt framtida flöde,
  fram-/returtemperatur, framtida debiterbar effekt och fakturagenomslag av
  eventuell fysisk toppeffektreduktion.

E.ON/Navirums fullvärmevärde är ett leverantörs-/historiksnapshot och ska
inte räknas om. Bas-/delvärmeprodukternas 36-månadersbaserade effekt ska
också ligga fast. Kraftringens befintliga golvbegränsade variant ska
fortsätta räknas av tariffmotorn med exakt samma flöde och temperatur i
båda scenarierna. Skapa ingen parallell tariff- eller justeringsformel.

Den befintliga separata beskrivningen av möjlig fysisk toppeffekt ska inte
göras till tariffbesparing i huvudscenariot. Energi, fysisk effekt,
debiterbar kapacitet och pengar ska hållas begreppsligt åtskilda.

## A. Intern implementation

1. Utöka den befintliga interna scenarioallowlisten med exakt de 17 ID:na.
   Välj backend explicit per produkt; automatisk fallback från tariffens
   form är inte tillåten. Återanvänd i första hand
   `kontraktsgatad_kostnadsled` och den befintliga kostnadsmotorn.
2. Behåll samtliga 17 nu publika våg-1/våg-2-produkter oförändrade och
   behåll Stockholm Exergi som särskild preliminär prototyp.
3. `SCENARIO_PUBLIKT_AKTIVERADE_ID` ska förbli exakt 17 produkter. Alla
   17 nya Wave 3a-ID:n ska ge positiv intern förmåga men negativ publik
   förmåga.
4. Ändra inte prisdata, genererad tariffdata, tariffmotorernas formler,
   `stodjer_besparing`, `stodjer_aktuell_arskostnad`, kontraktspolicyer eller
   befintliga kostnadsresultat. Om ett sådant behov upptäcks: stoppa
   `BLOCKED: Codex` med reproducerbart skäl.
5. Ingen publik React-funktion behövs i denna etapp. Publika kort,
   dropdownar och texter ska vara oförändrade.

## B. Facit och tester

För samtliga 17 produkter ska tester binda:

1. minsta giltiga fixture med uttryckligt effektvärde/band, flöde och
   framledningstemperatur samt full tolvmånaders energiserie;
2. referenskostnad, tre efterkostnader och besparing vid 10/15/20 med
   förväntade värden som inte genereras genom funktionen under test;
3. oförändrade fasta, kapacitets- och justeringsled samt oförändrade
   policyfält före/efter;
4. korrekt minskad styrbar rumsvärme, oförändrad övrig last och korrekt
   säsongs-/månadsprisning;
5. moms, prisår, preliminär resultatstatus och oförändrat produkt-ID;
6. fail-closed-beteende för saknat/ogiltigt flöde, temperatur, effekt eller
   band där respektive tariff kräver det;
7. negativ publik gate för hela den exakta Wave 3a-mängden.

Dokumentera oberoende, handräkningsbara komponentfacit minst för:

- en E.ON-fullvärmeprodukt med golvfri justering;
- en E.ON- eller Navirum-bas-/delvärmeprodukt med låst 36-månaderseffekt;
- en Navirum-fullvärmeprodukt;
- Kraftringen med den golvbegränsade justeringen.

Den fullständiga produktmängden ska bindas tabellstyrt så att ingen av de
17 posterna kan falla ur utan testfel. Testet får använda gemensamma
hjälpfunktioner för decimalaritmetik men får inte anropa
`beraknaOptimateScenario`, `beraknaArsproduktMedKostnadsled` eller annan
produktionsväg för att skapa förväntade svar.

## C. Matris och förväntat läge

Uppdatera det fail-closed statusregistret i
`generera_besparingspotential_tackningsmatris.py` för exakt de 17 ID:na,
regenerera JSON och Markdown endast via generatorn och bind aktuell
Neptune-käll-SHA.

Förväntad fördelning av 77 produkter efter den interna piloten:

- 17 `godkand_publik_10_15_20`;
- 17 `godkand_intern_pilot_ej_publik`;
- 1 `synlig_sarskild_preliminar_prototyp`;
- 42 `not_reviewed`.

Kör generatorns testsvit, `--check` och en andra deterministisk generering.
Ingen rad får få publik status i detta steg.

## Tillåtna huvudsakliga ändringar

Neptune:

- `neptune-marketing/src/utils/optimateScenario.ts`;
- nya eller befintliga riktade `optimateScenarioVag3a*.test.ts`;
- högst ett avgränsat negativt sid-/komponent-/E2E-prov om det behövs för
  att bevisa att piloten inte är publik.

Skills:

- `Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py`;
- generatorns test;
- de två maskingenererade matrisartefakterna;
- denna sessions-/handoff-/indexkedja.

En avvikande produktionsfil kräver uttrycklig motivering i nästa signal.
Tariffkatalog, genererad tariffdata, Enkey och brygginfrastruktur är utanför
scope.

## Arbetsform och verifieringsgrind

Arbeta i den rena isolerade Neptune-worktreen vid `c9a8bb7` eller skapa en
ny isolerad worktree från exakt samma bas. Flytta inte Neptune-main.
Committa fokuserat per repo och stagea endast namngivna filer.

Kör minst:

- riktade scenario-, tariff-, kontrakts- och gateprov för samtliga 17;
- hela Vitest i dokumenterad syskonlayout med rätt Enkey-snapshot;
- `npx tsc --noEmit` och isolerat bygge utan spårade `dist/`-ändringar;
- negativt UI/E2E-bevis för minst E.ON, Navirum och Kraftringen att inget
  publikt Optimate-kort visas;
- Python-matrisprov, generatorns `--check`, deterministisk omgenerering och
  `git diff --check` i båda repon;
- exakta fillistor, commithashar och kontroll att orelaterade filer är
  orörda.

När huvudkörningen själv har granskat och sammanfört hela resultatet ska
Claude skriva en ny globalt unik, committad toppsignal
`REVIEW_READY: Codex` med faktiska testtal, fullständiga commit-hashar,
avvikelser och kvarstående risker. Ingen aktivering, mainflytt eller push.
