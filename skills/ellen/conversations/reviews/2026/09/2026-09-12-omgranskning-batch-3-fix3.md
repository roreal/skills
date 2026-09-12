---
review_id: "2026-09-12-027"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope: "Batch 3 rättningsrunda 3 efter granskning 026"
reviewed_heads:
  skills: "257824c2e5abd194ee63edb6b20f55093d426517"
  enkey_agents: "f0a030f4b6d2b03f30f13c09f9b8d85c9ce886ac"
  neptune_academy: "1209f3d160051352b8d521918918edd50093a16a"
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
---

# Omgranskning av Batch 3 — rättningsrunda 3

## Beslut

**Changes required före aktivering.** Båda UI-fynden i granskning 026 är rättade:
Kraftringen använder nu ett kalenderriktigt ISO-intervall för hela januari–februari och
de nya periodtillstånden rensas vid leverantörs- och energisystembyte. Full TypeScript,
typkontroll, isolerat bygge och E2E är reproducerat gröna.

En smal men viktig kontraktslucka återstår. Intervallvalideringen körs bara i
`KalkylatorPage`; den publika produktfasaden `beraknaArsprodukt` godtar fortfarande en
osann eller felformaterad källperiod. Det befintliga publika Kraftringen-provet bevisar
självt luckan genom att ännu skicka gamla `2026-01` och ändå få
`annual/snapshot/complete`.

## Fynd

### P1 — källperioden är bara UI-validerad, inte produktkontraktsvaliderad

`arGiltigKalperiod` används i `KalkylatorPage.tsx`, men varken
`byggKontraktIndata`, `forkontrolleraPolicyIndata` eller `beraknaArsprodukt` validerar
den period som en programmatisk anropare skickar. För ett annual-anrop kräver
`harledResultatstatus` endast att `observeradPeriod` är icke-tom; därför passerar gamla
`2026-01` hela produktfasaden trots att UI:t nu korrekt avvisar samma värde.

Det är inte bara en teoretisk väg. `besparingsvardeBatch3.test.ts` beskriver sitt anrop
som den faktiska publika vägen och har fortfarande:

```text
kapacitetObserveradPeriod: '2026-01'
```

Codex körde fullsviten med detta prov: den blir grön och returnerar
`snapshot/complete`. Produktkontraktet och UI-kontraktet motsäger därmed varandra, och
ett framtida API-/komponentanrop kan kringgå den sanningsgrind som rättningsrunda 3
avsåg att införa.

Rätta generiskt i TypeScript-produktlagret, inte med tariff-ID:

1. Validera periodmetadata från de redan byggda `IndataPost`-posterna mot motsvarande
   `KravPost`: `matchningMotManad` ska kräva giltigt `ÅÅÅÅ-MM`, medan
   `kalperiodDefinition` utan månadsmatchning ska kräva det beslutade, kalenderriktiga
   ISO-intervallet.
2. Låt saknad eller ogiltig period blockeras typat av den publika produktfasaden innan
   kostnad returneras. Återanvänd gärna `forkontrolleraPolicyIndata` med en uttrycklig
   periodorsak, men lämna UI:s tidiga fältnära kontroll kvar som UX-grind.
3. Ändra Kraftringen-fixturen i `besparingsvardeBatch3.test.ts` till
   `2026-01-01/2026-02-28`. Bevisa där eller i ett fokuserat test att `2026-01`, ett
   omvänt/kalenderogiltigt intervall och saknad period blockeras genom
   `beraknaArsprodukt`, medan hela intervallet ger `snapshot/complete`.
4. Lägg det uttryckligen beställda beviset att exakt
   `2026-01-01/2026-02-28` når den bundna `IndataPost.observeradPeriod` oförändrat.

Rättningen ska stanna i TypeScript-produktkontrakt/test. Ändra inte Python,
tariffkatalog, priser, generatorfil, spärrar, R06/R10 eller disposition.

## Stängda fynd från granskning 026

- UI:t skiljer korrekt på `matchningMotManad` (`ÅÅÅÅ-MM`) och
  `kalperiodDefinition` (validerat ISO-intervall).
- `arGiltigKalperiod` kontrollerar två kalenderriktiga ISO-datum samt stigande ordning.
- Kraftringens DOM-fixture använder hela `2026-01-01/2026-02-28`; en ensam månad och
  omvänd ordning ger fältnära svenskt fel.
- `policyFaltPerioderRaw` och `kapacitetObserveradPeriodRaw` rensas i båda befintliga
  återställningsgrenarna.
- DOM-prov visar att leverantörsbyte respektive byte bort från fjärrvärme tömmer
  periodfältet; ny submit blockeras tills perioden anges igen.
- Ingen Python-, katalog-, pris-, generator- eller dispositionsändring gjordes.

## Oberoende verifiering utförd av Codex

- full TypeScript-svit: **1000 passed i 36 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **10/10 scenarier godkända**;
- `git diff --check`: rent;
- rättningsrunda 3 ändrar exakt de fyra dokumenterade TypeScript-filerna;
- full Python-svit **1009 passed, 4 skipped** från föregående oberoende granskning
  gäller oförändrat eftersom `enkey-agents@f0a030f` inte har ändrats;
- de sedan tidigare orelaterade ändringarna i `neptune-marketing/dist` är orörda.

## Nästa steg för Claude

1. Gör ISO-periodgrinden gemensam för UI och den publika TypeScript-produktfasaden.
2. Rätta den kvarvarande gamla Kraftringen-fixturen och lägg produkt-/forwardingproven
   ovan.
3. Kör riktade prov, full TypeScript, `tsc`, isolerat bygge, E2E och
   `git diff --check`.
4. Dokumentera en fokuserad commit och stanna för Codex slutgranskning.

**Ingen tariffaktivering, ingen borttagning av R06/R10 och ingen push.**
