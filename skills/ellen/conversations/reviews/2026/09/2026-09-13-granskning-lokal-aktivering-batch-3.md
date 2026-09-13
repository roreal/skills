---
review_id: "2026-09-13-030"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-push
scope: "Lokal aktivering av Batch 3 efter granskning 029"
reviewed_heads:
  skills: "a8847d0238eccc963ee84b0b03922b0a105e9d99"
  skills_catalog_activation: "bcaa28bd582093a8a6ec48246bc97169cd68d826"
  enkey_agents: "5ed21abd2f00948bf893be1c3010ee4e7e6f5a88"
  neptune_academy: "46c4f8f8005e11f18f45a1db67620293a83ef04b"
activation_may_remain: true
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
---

# Granskning av lokal Batch 3-aktivering före push

## Beslut

**Changes required före push. Själva tariffaktiveringen är tekniskt korrekt och ska
ligga kvar.** Exakt de nio godkända E.ON-/Navirum-/Kraftringen-bastarifferna har släppts,
R06/R10 är korrekt borttagna, generatorn är reproducerbar och de skarpa
beräkningsflödena fungerar.

Push blockeras av en P1-motsägelse i projektets aktiva statusdokumentation samt två
P2-luckor i de beständiga regressionsbevisen. Ingen katalog-, pris-, motor- eller
generatorrättelse behövs utifrån denna granskning.

## Fynd

### P1 — den aktiva inventeringen och batchplanen motsäger implementationen

`tariffinventering-v22.md` blandar tre oförenliga tillstånd:

- de nio Batch 3-raderna har fått dispositionen
  `implemented_source_verified_annual`;
- samma rader säger fortfarande `investigation.status: utreds`, att motorn inte finns,
  att policyn/testerna saknas, att UI:t inte är valbart och att katalogrättelsen återstår;
- §8:s huvudtabell visar fortfarande **7/57/28**, medan en efterföljande not säger att
  det verkliga talet är **25/39/28** och uttryckligen avstår från att synkronisera tabellen.

Exempel finns i E.ON-blocket på raderna 641–650 och Kraftringen-blocket på raderna
907–916. Samma gamla statusfält finns för alla nio. En mekanisk räkning av dokumentets
78 bastariffers `Disposition`-rader ger **16 implemented / 38 ready / 24 blocked**;
varianttabellen ger **0/10/4**. Dokumentets egna produktposter summerar alltså till
**16/48/28**, varken §8-tabellens 7/57/28 eller katalogens verkliga 25/39/28.

`batchplan-v22.md` har samma dubbla sanning. Inledningen säger att ingen batch är
påbörjad och att 7/57/28 gäller, den aktiva Batch 3-noten säger 25/39/28, och den senare
summeringen säger åter att 57 är batchade och 7/57/28 oförändrat. En extra korrigeringsnot
gör inte filen entydig för nästa agent eller nästa batchval.

Detta strider mot granskningsorder 029:s krav att uppdatera inventering, batchplan och
dispositionsbokföring till 25/39/28 och mot repots regel att dokumentationen ska vara
synkroniserad med implementationen. Felen kan leda nästa arbetsrunda till att försöka
implementera redan aktiva tariffer eller använda fel återstående kontrollmängd.

#### Krävd rättning

Välj en enda auktoritativ modell och genomför den fullt ut; lägg inte bara till ännu en
not. Den minsta vägen i nuvarande filstruktur är:

1. uppdatera samtliga nu aktiva bastariffers dispositionsrader så deras mekaniska summa
   blir **25/29/24 bas**, tillsammans med **0/10/4 varianter** = **25/39/28 av 92**;
2. synkronisera §8:s huvudtabell och aktiva rubriker/översikter till samma tal;
3. ersätt de nio Batch 3-blockens gamla katalog-, motor-, kontrakts-, test-, UI- och
   kvarstående-arbete-texter med det verkliga aktiverade annual_forward-läget;
4. uppdatera batchplanens aktiva status och återstående mängd. Historiska v22-beslut får
   ligga kvar endast där de uttryckligen är märkta som historik, inte som samtidig
   nulägesbeskrivning.

Om V22-filerna i stället ska vara strikt frusna historiska planer måste deras partiella
nulägesmutationer tas bort och en separat, tydligt länkad och mekaniskt kontrollerbar
levande statusfil bli enda nulägeskälla. Blanda inte de två modellerna.

### P2 — det katalogbreda grindprovet tappar tariffidentitet

`test_katalog.py::test_de_sexton_fria_tarifferna_passerar_alla_grinden` bygger `fria`
som en dictionary nycklad på `member_id`. Lidköping, E.ON och Navirum har flera godkända
tariffer per medlem; tidigare poster skrivs därför över av den sist itererade. Kommentaren
påstår att iterationen ändå bekräftar båda, men det stämmer inte: en felaktig första tariff
kan döljas av en godkänd andra tariff.

Batch 3:s separata nio-ID-matris gör att detta inte döljer ett fel i just den aktuella
leveransen, men det generella katalogprovet uppfyller inte sitt eget löfte. Nyckla på
tariff-ID eller iterera och kontrollera varje godkänd tariff separat. Bevara en separat
medlemsmängd för kontrollen av exakt 19 medlemmar.

Rätta samtidigt funktionsnamnen som fortfarande beskriver gamla tal eller assertions:

- `test_grinden_slapper_igenom_16_tariffer` verifierar 25;
- `test_godkanda_tariffer_kommer_fran_14_medlemmar` verifierar 19;
- `test_de_sexton_fria_tarifferna_passerar_alla_grinden` avser 25;
- `test_dispositionen_ar_16_48_28` verifierar nu bara att Sundsvall finns;
- `test_godkanda_ar_nu_exakt_sexton_och_omfattar_alla_sex` verifierar nu bara Batch 1:s
  sex medlemskap.

### P2 — det skarpa UI-beviset är permanent endast för Kraftringen

Det nya `besparingsvardeBatch3Katalogaktivering.test.ts` använder riktig genererad data
för E.ON, Navirum och Kraftringen, men det är ett utility-/produktprov utan React-DOM.
Det befintliga `KalkylatorPageBatch3.test.tsx` mockar två lokala poster (E.ON och
Kraftringen) och innehåller ingen Navirum-post. Det nya E2E-scenario 11 kör endast
Kraftringen.

Codex körde därför två extra manuella headless-flöden mot den byggda sidan och bekräftade
att både E.ON Järfälla och Navirum Norrköping visar rätt fyra fält, fullvärmetext och ger
synligt `snapshot`-resultat utan formulärfel. Det finns alltså inget reproducerat
produktfel, men granskningsorder 029:s bevis för verklig UI-väg är inte beständigt i
testsviten.

Utöka det omockade E2E-scenariot tabellstyrt med representativ E.ON och Navirum, eller
lägg ett omockat DOM-prov mot den riktiga `TARIFFER`. Bevisa för var och en dropdown,
kapacitet, band, flöde, temperatur, scope-text och normal MWh-submit till synligt
`snapshot/complete`. Kraftringens befintliga periodfall ska ligga kvar.

## Det som är godkänt och ska bevaras

- exakt nio Batch 3-bastariffer har `investigation: null`;
- de fem berörda medlemsposterna omfattar exakt dessa nio katalograder;
- R06/R10 är borttagna och inga tariffreferenser till dem återstår;
- alla nio och endast de nio nya produkterna finns i den genererade tariffmängden;
- ingen `bas-delvarme`- eller `brunnshog`-variant finns i skarp genererad data;
- generatorn ger 25 godkända och 53 filtrerade, med korrekt kataloghash och commit;
- en fristående regenerering mot `skills@bcaa28b` matchar
  `tariffer.generated.ts` byte för byte;
- E.ON/Navirums månadseffekt och Kraftringens årseffekt samt båda
  flödeskorrigeringsvarianterna är oförändrade från den godkända implementationen;
- kända månadsperiodiseringsissues ligger kvar och annual_forward-resultatet märks
  `snapshot`, inte fakturagaranti eller exakt månadsresultat;
- användarens orelaterade `neptune-marketing/dist`-ändringar är orörda.

## Oberoende verifiering utförd av Codex

- full Python-svit: **1009 passed, 4 skipped**;
- full TypeScript-svit: **1023 passed i 37 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **11/11 scenarier godkända**;
- extra omockade webbläsarflöden: E.ON Järfälla gav **889 828 kr** och Navirum
  Norrköping **804 440 kr**, båda med rätt fält, fullvärmetext och inga fel;
- generatoromkörning: **byte-för-byte MATCH**;
- `git diff --check`: rent i samtliga tre aktiveringsintervall.

## Nästa steg för Claude

1. Låt katalogaktiveringen och genererad tariffdata ligga kvar.
2. Rätta P1-dokumentationen till en enda, mekaniskt sann nulägesbild.
3. Rätta de missvisande testnamnen och gör det katalogbreda grindprovet tariffscopat.
4. Permanenta det redan manuellt verifierade E.ON-/Navirum-UI-beviset.
5. Kör dokumenträkning, full Python/TypeScript, `tsc`, isolerat bygge, 13 förväntade
   E2E-scenarier om E.ON/Navirum läggs som separata fall, generatorjämförelse och
   `git diff --check`.
6. Gör fokuserade lokala rättningscommits, logga exakta resultat och stanna för Codex
   omgranskning.

**Ingen push. Ingen ny tariffaktivering.**
