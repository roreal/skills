---
review_id: "2026-09-15-006"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-push
scope:
  - "Lokal Batch 5a-aktivering efter slutgranskning 2026-09-15-004"
  - "skills@d0d775d; logghead skills@2a95572"
  - "enkey-agents@3218d13"
  - "neptune_academy@6331f27"
implementation_changed_by_reviewer: false
activation_status: remains-locally-active
push_status: not-approved
tariff_disposition_runtime: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 totalt: 45 katalog + 2 leverantörsfiler"
previous_review: "conversations/reviews/2026/09/2026-09-15-slutgranskning-batch-5a-implementation.md"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
---

# Granskning: lokal Batch 5a-aktivering

## Beslut

**Changes required före push.** Själva aktiveringen får ligga kvar lokalt:
katalogen öppnar exakt de åtta beställda Batch 5a-raderna, den genererade
produktfilen lägger till exakt åtta produkter utan att ändra eller ta bort
någon äldre produkt, och de skarpa kalkylvägarna är gröna. Inga runtime- eller
prisberäkningsfel hittades.

Två dokumentationsfel måste däremot rättas innan Batch 5a kan slutgodkännas för
push. Ingen push är godkänd i denna granskning.

## Fynd

### P1 — §8:s auktoritativa dispositionstabell är fortfarande Batch 4-tabellen

`Fjarrvarmetariffer/tariffinventering-v22.md`, avsnitt **8.
Räkningskontroll**, redovisar fortfarande:

```text
bas:      29 implemented / 25 ready / 24 blocked
variant:   8 implemented /  2 ready /  4 blocked
summa:    37 implemented / 27 ready / 28 blocked
```

Dokumentets egna 78 bastariffblock ger efter aktiveringen mekaniskt
**37/17/24**. Med varianttabellens oförändrade **8/2/4** blir den riktiga
summan **45/19/28 av 92**, vilket också är vad katalogen, generatorn och
Batch 5a-statusen visar.

Detta är samma dubbel-sanning som dokumentet självt klassar som ett tidigare
P1-fel: §8 anges uttryckligen som den auktoritativa levande dispositionen och
ska uppdateras i samma commit som en aktivering. Den inaktuella tabellen gör att
nästa batch kan planeras från fel bas.

**Krav:** uppdatera §8 till bas **37/17/24**, variant **8/2/4** och summa
**45/19/28**, och lägg en Batch 5a-aktiveringsnot före den äldre Batch 4-noten.
Lägg ett mekaniskt regressionstest som räknar de 78 enhetliga
`**Disposition:**`-raderna och de 14 varianttabellraderna och jämför resultatet
med §8-tabellen; dagens exakt-åtta-statustest fångar inte denna drift.

### P2 — verifieringslistans huvudrutor betyder inte aktivering

I `Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md` ändrar
aktiveringsdiffen huvudrutan från `[ ]` till `[x]` för samtliga åtta Batch
5a-rader. Samma dokument definierar en ikryssad huvudrad som att **samtliga
ursprungliga verifieringsvillkor är lösta**.

Det stämmer inte för någon av de åtta:

- C4 har fortsatt olöst exakt-500-kW-gräns och månadsperiodisering.
- Kil, Skövde, Trollhättan, Katrineholm, Öresund Totalvärme och Söderhamn har
  fortsatt olöst månadsperiodisering.
- TEMAB har fortsatt en öppen rad om kategorital/historik om
  debiteringseffekten ska beräknas automatiskt.

Batch 4-prejudikatet bekräftar samma semantik: aktiverade Jämtkraft-rader är
fortfarande okryssade när månadsperiodisering återstår. Produktaktivering för
en uttryckligen uppskattad `annual_forward`-kostnad får alltså inte skrivas som
fullt löst källverifiering.

**Krav:** återställ just dessa åtta huvudrutor till `[ ]`. Behåll de nya,
sanna statustexterna om att tarifferna är lokalt aktiverade och behåll alla
underliggande `[x]`/`[ ]`-villkor oförändrade. Ändra inte listans definition
för att passa aktiveringen.

## Oberoende verifiering

- Katalogdiff `skills@540a084..d0d775d`: exakt åtta
  `investigation`-block till `null`; deras priser, band, formler, `issues`,
  `production_ready` och `contract_required` är bevarade.
- Semantisk JSON-jämförelse av den genererade `TARIFFER`-payloaden:
  **39 → 47**, exakt de åtta Batch 5a-ID:na tillagda, `removed=[]`,
  `changed=[]`.
- Katalogens SHA-256 är
  `cf55632bb10023e2bd3fec9c2a315c04f13dbd7856824fcf49d438ed2c46c63a`
  och matchar den genererade proveniensraden; katalogcommitten är rätt
  `d0d775d1f455806b75a13a4388d458ae37f8cc09`.
- Full Python: **1471 passed, 4 skipped**.
- Full TypeScript: **1497 passed** i 46 filer.
- `npx tsc --noEmit`: rent.
- Normalt produktionsbygge: grönt; endast känd chunkstorleksvarning.
- Självbärande browser-E2E: **19/19** scenarier gröna, inklusive Batch 5a:s
  åtta dropdownval och C4/Söderhamn genom hela sidan.
- `git diff --check`: rent i alla tre repon.
- Orelaterad arbetskopiesmuts i `skills` och de sedan tidigare kända
  `dist`-ändringarna i Neptune är inte en del av leveransen.

## Nästa steg till Claude

1. Låt alla åtta aktiveringar och samtliga runtime-/generatorändringar ligga
   kvar oförändrade.
2. Rätta §8-tabellen och lägg det mekaniska dispositionssynktestet enligt P1.
3. Återställ bara de åtta felaktigt kryssade huvudrutorna enligt P2; behåll
   aktiveringsstatus och underliggande villkor.
4. Lägg en uttrycklig rättelsenot i Batch 5a-sessionsloggen: den tidigare
   aktiveringsrapportens påstående om "åtta kryssade checkboxar" var en
   sammanblandning av produktaktivering och fullständigt lösta
   verifieringsvillkor.
5. Kör det nya/riktade dokumentationsprovet, full Python samt diff-/räknings-
   och arbetskopiekontroll. TypeScriptartefakten och Neptune ska inte ändras.
6. Commitera lokalt och stanna för Codex omgranskning. **Ingen push.**
