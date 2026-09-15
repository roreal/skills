---
review_id: "2026-09-15-015"
date: "2026-09-15"
reviewer: Codex
status: approved-for-separate-local-activation
scope:
  - "Batch 5b rättningsrunda 5 bakom spärr"
  - "skills@cab9dff"
  - "enkey-agents@18022c1 (oförändrad i fixrunda 5)"
  - "neptune_academy@c8554bd"
implementation_changed_by_reviewer: false
activation_status: approved-not-performed
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5b-fixrunda-4.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Slutgranskning: Batch 5b rättningsrunda 5

## Beslut

**Godkänd för en separat lokal aktivering av exakt sex Batch 5b-
kandidater efter Roberts uttryckliga klartecken. Ingen aktivering har
utförts och ingen push är godkänd.**

Samtliga fynd i granskningskedjan 009, 011, 012, 013 och 014 är stängda.
Fixrunda 5 gör previewserverns readiness processunik, stoppar före smoke
vid upptagen port och ersätter den gamla manuella filbytesguiden med det
säkra isolerade npm-kommandot. Normalfallet, konfliktfallet och hela den
befintliga regressionskedjan är oberoende verifierade.

## Stängda fynd från granskning 2026-09-15-014

- `vantaPaViteRedo()` väntar på den startade Viteprocessens egen ANSI-
  normaliserade `Local:`-signal innan HTTP-kontroll eller smoke får börja.
  En annan process som redan svarar på målporten kan därför inte godtas.
- Det permanenta kommandot
  `npm run test:e2e:batch5b-isolated:port-conflict` upptar porten med en
  riktig Viteprocess och kräver både icke-noll exit och att Scenario 1
  aldrig startar.
- Codex körde konfliktprovet: harnesset rapporterade `Port 4174 is already
  in use` och det permanenta provet blev grönt utan något smoke-scenario.
- Exakt `npm run test:e2e:batch5b-isolated` med fri port väljer projektets
  Python 3.14 och ger **20/20**.
- `kalkylator.smoke.mjs` hänvisar nu endast till den säkra isolerade
  npm-vägen. Receptet som skrev över spårad tariffdata och byggde `dist/`
  är borttaget.
- `dist/` är rent och inga testprocesser ligger kvar på granskningsportarna.

## Hela Batch 5b-underlagets godkända läge

- Sex tariffpolicyer har leverantörseffekt, leverantörsbekräftat band och
  obligatoriskt fakturaflöde genom samma fail-closed produktkontrakt.
- Jönköpings accesspris är ett slutet kundval 0/10/25/50 kr per central och
  månad. Antalet kommer endast från det globala dedikerade
  undercentralsfältet, heltal 1–20.
- Accessdeskriptor och policybindning är dubbelriktade och unika. Varken
  borttagen eller duplicerad accesspost kan nå generatorn.
- Jönköpings kostnadslås bekräftar `25 × 12 × 3 = 900` kr access och
  62 500 kr total exempelårskostnad exklusive moms.
- Den fulla sex-tariffmatrisen omfattar band, flöde, fältnära fel,
  produktlägen och blockerad kronor/schablon/besparing.
- Generatorprovet parserar produktordboken och låser **47 skarpa / 53
  isolerade produkter**, med exakt sex Batch 5b-kandidater endast i det
  isolerade läget.
- Alla sex katalograder ligger fortsatt bakom
  `investigation.status="utreds"`; dispositionen är **45/19/28**.

## Oberoende verifiering

- Python tariffsvit: **1608 passed, 4 skipped**.
- TypeScript: **1643 passed** i 51 testfiler.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt, 971 moduler, endast `dist-eval/`.
- Standard-E2E mot skarpa data: scenario **1–19** gröna och scenario 20
  korrekt överhoppat med hänvisning till isolerat kommando.
- Isolerad kandidat-E2E: **20/20** gröna.
- Permanent portkonfliktsprov: grönt och stoppar före Scenario 1.
- `git diff --check`: rent i samtliga tre leveransdiffar.
- `enkey-agents` och `neptune_academy` är rena; `skills` har endast sedan
  tidigare dokumenterade orelaterade filer.
- Remote `main` är oförändrad vid `skills@cd0bdb2`,
  `enkey-agents@4d5f8a6` och `neptune_academy@6331f27`.

## Nästa steg efter Roberts uttryckliga klartecken

Claude får då göra en **separat lokal aktiveringscommit**, utan push:

1. Aktivera exakt Borlänge, Falu tätort, Falu ytterorter, Habo, Mjölby och
   Jönköping; ändra inga andra tariffers status eller data.
2. Regenerera den skarpa `tariffer.generated.ts` från den riktiga katalogen
   och kontrollera exakt sex nya produkter, inga ändrade äldre produkter.
3. Uppdatera dispositionen till **51 implemented / 13 ready / 28 blocked
   av 92** och den skarpa produktmängden till **53** i samtliga levande
   dokument och permanenta räkningsprov.
4. När Jönköping är skarp ska Scenario 20 köras i den vanliga E2E-sviten,
   inte bara i kandidatläget. Anpassa villkor/testtexter utan att förlora
   den isolerade regressionsvägen.
5. Kör full Python-/TS-/tsc-/bygg-/standard-E2E-/generator-/diffverifiering,
   committa lokalt och stanna för Codex granskning av aktiveringsdiffen.
   `dist/` ska förbli regenererbar, ocommittad byggoutput.

Detta slutgodkännande är inte en pushauktorisation och utför inte
aktiveringen i förväg.
