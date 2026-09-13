---
review_id: "2026-09-13-029"
date: "2026-09-13"
reviewer: Codex
status: approved-for-local-activation
scope: "Batch 3 rättningsrunda 5 efter granskning 028"
reviewed_heads:
  skills: "0fc99248aa6467f51a84cb5835cf6e3ae6a120f0"
  enkey_agents_batch_3: "ee21b47c6dfc77993a87fdc518f386bcf6094b26"
  neptune_academy: "0e13e76c79961fb7be7f834622fa942558941cef"
activation_allowed: true
push_allowed: false
tariff_disposition_before_activation: "16 implemented / 48 ready / 28 blocked av 92"
tariff_disposition_after_approved_activation: "25 implemented / 39 ready / 28 blocked av 92"
---

# Slutgranskning av Batch 3 — rättningsrunda 5

## Beslut

**Godkänd för en separat lokal aktivering av exakt de nio Batch 3-tarifferna.**
Granskning 028:s språkdrift är stängd, den striktare periodkontrollen ligger kvar i
produktfasaden och inga funktionella fynd återstår inom implementationsomfattningen.

Detta är inte ett pushgodkännande. Claude ska först göra aktiveringen lokalt, bevisa den
skarpa produktvägen och stanna för Codex granskning av aktiveringsdiffen.

## Verifierade rättningar

- TypeScripts delade `harledResultatstatus` speglar åter Python: en fri
  `kalperiodDefinition` kräver en icke-tom källperiod och takar resultatet på
  `snapshot`, utan att införa ett produktformatskrav i det delade kontraktet.
- Den publika produktvägen är fortsatt fail-closed. `forkontrolleraPolicyIndata`
  kräver fortfarande ett giltigt `ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD` för Batch 3:s källperiod
  och blockerar trunkerade eller ogiltiga intervall före kostnadsberäkning.
- Ett nytt lagergränsprov låser den avsiktliga skillnaden mellan det delade
  resultatkontraktet och produktfasadens striktare indataregel.
- Kraftringens Python-testfixtur använder nu den sanna perioden
  `2026-01-01/2026-02-28`; ingen Python-produktionskod ändrades.
- `test-results/` är ignorerad och arbetsartefaktet är borta. De orelaterade,
  användarägda ändringarna i `neptune-marketing/dist` är fortsatt orörda.
- Katalog, priser, spärrar, R06/R10, disposition och skarp tariffpayload ändrades inte
  i rättningsrunda 5.

`enkey-agents` har efter Batch 3-committen `ee21b47` fått den orelaterade committen
`5beda019e4e5a611f948c9316122fc35e15292c2` som tar bort jobbet `lr260-cykeltest`.
Den ligger utanför denna granskning och ska inte blandas in i Batch 3-bokföringen.

## Oberoende verifiering utförd av Codex

- full Python-svit: **1009 passed, 4 skipped**;
- full TypeScript-svit: **1005 passed i 36 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **10/10 scenarier godkända**;
- `git diff --check`: rent i samtliga granskade intervall;
- genererad tariffpayload är oförändrad i rättningsrunda 5;
- `test-results/` träffar `.gitignore` och lämnar inget oincheckat artefakt;
- dispositionen är fortsatt mekaniskt verifierad till **16/48/28** och ingen av de
  nio Batch 3-tarifferna är ännu skarpt valbar.

## Bindande arbetsorder för lokal aktivering

Aktivera endast följande nio bastariffer:

1. `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`
2. `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`
3. `e-on-malmo-malmo-och-burlov-bostader-2026`
4. `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`
5. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`
6. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`
7. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`
8. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`
9. `kraftringen-kraftringen-2026`

Gör följande i en fokuserad aktiveringsleverans:

1. Ta bort `investigation` endast från de nio raderna. Aktivera inte Batch 3b:s
   bas-/delvärmevarianter eller Kraftringens Brunnshög-variant.
2. Ta bort R06 och R10 först efter en mekanisk kontroll att deras medlemsscope exakt
   täcks av de nio aktiverade raderna och att ingen kvarvarande tariff refererar till
   dem. Rensa de nio requestreferenserna utan att skapa hängande referenser.
3. Uppdatera katalogrevision, inventering, batchplan och dispositionsbokföring till
   exakt **25 implemented / 39 ready / 28 blocked av 92**.
4. Regenerera `tariffer.generated.ts` med den riktiga generatorn och sann proveniens.
   Förväntningen är **25 godkända / 53 filtrerade** poster i den genererade
   kontrollmängden; verifiera talet mekaniskt i stället för att skriva det för hand.
5. Bevisa i riktig UI-/DOM-/E2E-väg att representativa E.ON-, Navirum- och
   Kraftringenval visar rätt band och obligatoriska fält, accepterar fullständig MWh-
   indata, ger uppskattat `snapshot/complete`-resultat och fortsatt blockerar kronor,
   schablon samt besparingsprodukt typat.
6. Kör full Python och TypeScript, `tsc`, isolerat bygge, E2E och
   `git diff --check`. Verifiera även att exakt de nio nya bastarifferna finns i den
   skarpa väljaren och att inga förbjudna varianter har följt med.
7. Gör fokuserade lokala commits per repo, uppdatera kommunikationsloggen och stanna
   för Codex granskning av aktiveringsdiffen.

**Ingen push före nästa uttryckliga Codex-godkännande.**
