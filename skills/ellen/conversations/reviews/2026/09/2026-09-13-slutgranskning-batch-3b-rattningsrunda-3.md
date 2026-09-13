---
review_id: "2026-09-13-039"
date: "2026-09-13"
reviewer: Codex
status: approved-for-separate-local-activation
scope: "Slutgranskning av Batch 3b rättningsrunda 3 efter granskning 038"
reviewed_heads:
  skills: "14cf1db"
  skills_catalog: "3b8c1aee0deb8cf8f170cbaff4672824821efbb4"
  enkey_agents: "09b0ef2"
  neptune_academy: "92de895"
activation_allowed: true
push_allowed: false
review_required_before_push: true
tariff_disposition_before_activation: "25 implemented / 39 ready / 28 blocked av 92"
tariff_disposition_after_approved_activation: "33 implemented / 31 ready / 28 blocked av 92"
follows: "2026-09-13-038"
---

# Slutgranskning av Batch 3b rättningsrunda 3

## Beslut

**Godkänd för en separat lokal aktiveringsrunda.** De två kvarvarande P2-fynden i
granskning 038 är stängda. TypeScript-provet pinnar nu energi, kapacitet och
flödesjustering med fristående litteraler för samtliga åtta produkter och testar både
saknad och ogiltig effekt, flöde, temperatur, band och period med typade/fältnära fel.
TypeScript-dokumentationen skiljer korrekt på månadsanropets verkliga målmatchning och
årsproduktens rena formatkrav. Generatorsynkprovet och all aktuell text beskriver nu
den faktiska semantiska JSON-objektjämförelsen.

Ingen kostnads-, motor-, tariff- eller aktiveringsändring gjordes i rättningsrunda 3.
De åtta `--bas-delvarme`-produkterna ligger fortfarande bakom spärr och den skarpa
dispositionen är fortsatt **25/39/28 av 92**. Aktivering får nu göras lokalt enligt
ordern nedan. **Ingen push före en ny Codex-granskning av aktiveringsdiffen.**

## Stängda fynd

1. `besparingsvardeBatch3b.test.ts` bär per variant oberoende energi-, effekt- och
   flödesfacit. Testet verifierar först fixturens publicerade priser och beräknar sedan
   `fast`, `energi` och `justering` utan att läsa förväntat pris ur motorindatan.
2. Felmatrisen täcker nu saknad/ogiltig kapacitet, flöde och temperatur samt fel band
   och saknad/ogiltig period. Relevanta fall kräver `KontraktBlockerat`, exakt `orsak`
   och fältnyckel/valideringsorsak.
3. `KravPost.matchningMotManad` dokumenterar nu års- och månadsanrop separat och
   bevarar Batch 3b som `annual/snapshot/complete`.
4. Fixtursynken heter och beskrivs nu semantisk, vilket motsvarar den verkliga
   `json.loads`-objektjämförelsen.

## Icke-blockerande rättning som ska följa med aktiveringsrundan

Facitvärdena `108.17`, `101.57` osv. är tariffens **månatliga** rörliga effektpriser:
katalogen anger `rate_period="month"`, generatorn serialiserar ett årspris genom
multiplikation med tolv och både Python-/TypeScript-facitet räknar korrekt
`effekt × månadspris × 12`. Namnet `variabelKrPerKwAr` samt kommentarerna
"kr/kW/år" i `besparingsvardeBatch3b.test.ts`, `test_batch_3b_bas_delvarme.py` och den
ärvda kommentaren i `test_batch_3_flodeskorrigering.py` är därför missvisande trots
korrekt aritmetik.

Byt dessa namn/kommentarer till `variabelKrPerKwManad` respektive `kr/kW/månad` under
aktiveringsrundan. Ändra inte talen eller multiplikationen med tolv. Detta är P3 och
blockerar inte att den separata lokala aktiveringen startar, men ska vara stängt före
push.

## Verifierat av Codex

- Full Python-svit: **1222 passed, 4 skipped**. Enda varningen var att sandboxen inte
  fick skriva `.pytest_cache`; testutfallet påverkades inte.
- Full TypeScript-svit: **1177 passed i 39 filer**.
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build`: godkänt; endast den kända bundelstorleksvarningen.
- E2E mot det isolerade bygget: **13/13 scenarier godkända**.
- `git diff --check`: rent i `cfb492b..14cf1db`, `950fd5b..09b0ef2` och
  `2be2452..92de895`.
- Diffomfattningen är korrekt avgränsad till sessionsloggen, ett Python-test samt ett
  TypeScript-test och kontraktsdokumentationen. Ingen katalog, genererad skarp payload
  eller produktionsmotor ändrades.
- Inget repo är pushat. Codex har inte rört användarens befintliga `dist/` eller andra
  orelaterade arbetskopiefiler.

## Bindande lokal aktiveringsorder till Claude

1. Ta bort endast de åtta rena Batch 3b-implementationsspärrarna. Ändra inga priser,
   tariffregler, källor, bastariffer, andra `investigation`-poster eller andra batcher.
2. Flytta exakt de åtta variantdispositionerna från `ready_to_implement` till
   `implemented_source_verified_annual`. Sluträkningen ska vara
   **33 implemented / 31 ready / 28 blocked av 92**; katalogen ska fortsatt ha 86
   fysiska poster.
3. Regenerera den skarpa TypeScript-katalogen med korrekt skills-commitproveniens.
   Diffen ska lägga till exakt åtta unika, årsoberoende `--bas-delvarme`-produkt-ID:n.
   De 25 tidigare aktiva katalogprodukternas pris-, policy- och kostnadsdata ska vara
   oförändrade bortsett från tillåten global generatorproveniens.
4. Lägg skarpa generator-/produktprov som bevisar exakt **33** aktiva
   katalogprodukter, exakt åtta aktiva Batch 3b-varianter och fortsatt åtta giltiga
   `variant_of`-föräldrar. Inga spärrade eller okända produkter får läcka in.
5. Lägg permanent skarpt UI-/E2E-bevis för att Fullvärme och Bas-/delvärme visas som
   separata, entydiga val för både en E.ON- och en Navirum-produkt. Bas-/delvärme ska
   kräva leverantörseffekt, band, flöde, temperatur och fakturamånad, ge ett synligt
   `annual/snapshot/complete`-resultat och inte återanvända effekt/period vid produktbyte.
6. Gör P3-enhetsrättningen ovan utan att ändra facitvärden eller aritmetik.
7. Synkronisera levande inventering, batchplan, verifieringslista, sessionslogg, handoff
   och index med den faktiska aktiveringen. Ändra inte historiska granskningsuppgifter.
8. Kör full Python, full TypeScript, `tsc`, isolerat bygge, E2E, generatorsynk,
   dispositionsräkning och `git diff --check`. Commitera fokuserat lokalt per repo,
   logga exakta commit-hashar och stanna för Codex granskning av aktiveringsdiffen.

**Lokal aktivering är tillåten. Push är inte tillåten.**
