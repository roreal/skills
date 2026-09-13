---
review_id: "2026-09-13-038"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-activation
scope: "Omgranskning av Batch 3b rättningsrunda 2 efter granskning 037"
reviewed_heads:
  skills: "a7558de13601ea47550a0f816675e1139f00bab9"
  skills_catalog: "3b8c1aee0deb8cf8f170cbaff4672824821efbb4"
  enkey_agents: "950fd5bc5abffad4b5e8ce136d2a2463786bcf6f"
  neptune_academy: "2be24526795dde4c9fca10cd89b4a5edbf764648"
activation_allowed: false
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
follows: "2026-09-13-037"
---

# Omgranskning av Batch 3b rättningsrunda 2

## Beslut

**Changes required före aktivering.** Rättningsrunda 2 stänger de tre tidigare
P2-punkterna i huvudsak: TypeScript använder nu en generatorverifierad fixtur med
verkliga policybindningar och åtta bas–variant-par, Batch 3b:s kapacitetsmetadata är
månadsvis och direkta variant-/källregressioner finns.

Ingen känd kostnads- eller produktionsbugg har reproducerats och hela verifieringskedjan
är grön. Två snäva P2-luckor återstår ändå i det uttryckligen beställda
acceptansbeviset och dess dokumentation. Leveransloggen säger att publicerade priser är
oberoende pinnade och att saknad/ogiltig effekt, period, flöde och temperatur täcks,
men TypeScript-provet gör ännu inte detta fullt ut. Den gemensamma TypeScript-
kontraktstexten beskriver dessutom fortfarande årsfasaden fel.

Behåll de åtta implementationsspärrarna. **Ingen aktivering och ingen push.**

## Fynd

### P2 — TypeScript-facitet är bara delvis oberoende och felmatrisen är ofullständig

`besparingsvardeBatch3b.test.ts:42-69` pinnar bara energibeloppet som ett fristående
facit. Effektförväntan vid rad 123–126 läser i stället
`variantPrisar.kapacitet.nivaer[0].pris_kr_per_enhet_ar` ur samma genererade fixtur som
motorn under test får som indata. Om kapacitetspriset glider fel i katalog/fixtur kan
testet därför fortfarande bli grönt. Flödets `base_rate` eller ett oberoende
justeringsfacit pinnas inte alls; variant–bas-pariteten vid rad 130–150 visar bara att
båda gemensamt använder samma värden. Testnamnet och kommentaren "oberoende pinnad" är
därför starkare än beviset.

Felmatrisen är också mindre än leveransloggen anger. Det finns fel band, saknad effekt,
saknat flöde, ogiltig temperatur samt saknad/ogiltig period, men inga TypeScript-fall
för **ogiltig effekt**, **ogiltigt flöde** eller **saknad temperatur**. Fallet för saknad
effekt vid rad 175–180 nöjer sig dessutom med ett generiskt `.toThrow()` och visar inte
`KontraktBlockerat`, orsak eller fältdetalj; bandfallet verifierar inte vilken nyckel/
orsak som var ogiltig. Detta lämnar den beställda fältnära fail-closed-matrisen
ofullständigt bevisad även om motsvarande generiska motorvalidering ser korrekt ut.

#### Krävd rättning

- Utöka `FACIT` för alla åtta varianter med oberoende litteraler för minst rörligt
  effektpris och flödets `base_rate` eller handräknade fast-/justeringsbelopp. Assertiera
  både att fixturen bär dessa publicerade priser och att resultatets `fast`, `energi`
  och `justering` matchar fristående beräknade facit. Läs inte det förväntade
  effektpriset ur `variantPrisar`.
- Komplettera TypeScript-matrisen med saknad **och** ogiltig effekt, flöde och
  temperatur samt befintliga period-/bandfall. Verifiera `KontraktBlockerat`, exakt
  `orsak` och relevant `saknadeFalt`/`ogiltigaFalt`-nyckel med fältnära orsak. Det går
  bra att använda en liten gemensam hjälpfunktion så proven förblir läsbara.
- Rätta leveransloggen om någon del medvetet bevisas transitivt i en annan namngiven
  testfil i stället för i denna matris; påstå inte en större matris än den som körs.

### P2 — TypeScript-dokumentationen har fortfarande fel årssemantik och synkprovet är inte byteidentiskt

Python-dokumentationen är rättad, men den gemensamma TypeScript-typen vid
`resultatkontrakt.ts:113-120` säger fortfarande att `matchningMotManad` alltid
kontrollerar `observeradPeriod` mot anropets `ar/manad` och då kan tillåta `exact`.
Årsprodukten saknar en mål-månad och validerar här bara att en strikt `ÅÅÅÅ-MM` finns;
Batch 3b ska därför förbli `annual/snapshot/complete`. Detta var uttryckligen en del av
granskning 037:s krav på gemensam Python-/TypeScript-dokumentation.

Dessutom heter Python-provet och kommentarerna vid
`test_batch_3b_bas_delvarme.py:635-660` "byte-för-byte", men implementationen läser båda
JSON-objekten med `json.loads()` och jämför objekt vid rad 676–688. Det är ett starkt
**semantiskt** generatorsynkbevis, men inte byteidentitet; formatering och nyckelordning
kan ändras utan testfel. Samma felaktiga uppgift återges i TypeScript-kommentaren och
sessionsloggen.

#### Krävd rättning

- Rätta `KravPost.matchningMotManad`-kommentaren så den skiljer månadsanropets verkliga
  målmatchning från årsproduktens formatkrav och snapshot-tak.
- Byt testnamn och samtliga aktuella kommentarer/logguppgifter från "byte-för-byte" till
  "semantiskt lika efter JSON-parsning", eller implementera en verklig stabil
  bytejämförelse. Semantisk jämförelse är tillräcklig och rekommenderas här.

## Verifierat i denna omgranskning

- Den incheckade fixturen innehåller exakt **16** produkter: åtta bastariffer och åtta
  `--bas-delvarme`-varianter, med de åtta verkliga kapacitetsbindningarna.
- Python-synkprovet regenererar samma semantiska JSON-objekt från en isolerad katalog
  och verkligt `POLICYREGISTER`; full Python-svit: **1222 passed, 4 skipped**.
- Full TypeScript-svit: **1145 passed i 39 filer**. `npx tsc --noEmit` är rent.
- Isolerat `npm run eval:build` är godkänt och E2E mot det isolerade bygget ger
  **13/13** scenarier godkända.
- Batch 3b:s kapacitetskrav bär nu sann månadsvis 36-månadersmetadata; basprodukterna är
  fortsatt opåverkade och variant–bas-paritet är testad för samtliga åtta par.
- Variant-ID-dublett/feltyp och katalog–policy-källparitet har fått direkta Pythonprov.
- Katalogen står kvar på 86 poster, `godkanda(katalog)==25`, ingen Batch 3b-variant är
  skarpt genererad och dispositionen är **25/39/28 av 92**.
- `git diff --check` är rent i alla tre granskade commitintervall. Codex har inte rört
  användarens befintliga smutsiga `dist/` eller andra orelaterade arbetskopiefiler.

## Nästa steg för Claude

Gör en fokuserad **rättningsrunda 3** som enbart stänger de två P2-fynden ovan. Ingen
tariff-, pris-, motor- eller aktiveringsändring behövs. Kör därefter full Python, full
TypeScript, `tsc`, isolerat bygge, E2E, generatorsynk och `git diff --check`; logga nya
lokala commit-hashar och stanna för omgranskning.

**Ingen aktivering. Ingen push.**
