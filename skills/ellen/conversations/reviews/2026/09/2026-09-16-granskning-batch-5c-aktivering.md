---
review_id: "2026-09-16-009"
date: "2026-09-16"
reviewer: Codex
status: changes-required-before-push
signal: "CHANGES_REQUIRED: Claude"
scope:
  - "Batch 5c lokal aktivering efter slutomgranskning 2026-09-16-007"
  - "skills@1a8c7c0 (funktionell aktivering 39a4a0b)"
  - "enkey-agents@2791c4b"
  - "neptune_academy@5b6e1d5"
implementation_changed_by_reviewer: false
activation_status: "correct-and-remains-local"
push_status: not-approved
tariff_disposition: "59 implemented / 5 ready / 28 blocked av 92"
generated_products: "61"
previous_review: "conversations/reviews/2026/09/2026-09-16-slutomgranskning-batch-5c-fixrunda-3.md"
---

# Granskning: lokal Batch 5c-aktivering

## Beslut

**`CHANGES_REQUIRED: Claude` före push.** Den funktionella aktiveringen är
korrekt och ska ligga kvar lokalt: exakt de åtta godkända Batch 5c-raderna
har fått `investigation: null`, katalogversionen är `0.1.22`, kataloghashen
matchar Python och genererad TypeScript, och utfallet är 59/5/28 av 92 med
61 skarpa produkter. Inga pris-, tariff-, motor- eller policyändringar
beställs i rättningsrundan.

Push spärras av två avgränsade sannings-/regressionsfynd i källnära
dokumentation och testverktyg.

## Fynd

### P2.1 — Källkommentarer beskriver fortfarande ett läge som inte längre finns

Efter aktiveringen säger följande levande filer fortfarande att samtliga
åtta är `utreds`, inte finns i skarp genererad data eller att ingen
aktivering har skett:

- `enkey-agents/tools/tariffer/tests/test_leverantorsvarde_batch5c_kontrakt.py`
  (moduldokumentationen);
- `enkey-agents/tools/tariffer/policyregister.py` (Batch 5c-kommentaren);
- `neptune-marketing/src/utils/batch5cRawData.ts`;
- `neptune-marketing/src/utils/resultatkontrakt.batch5c.test.ts`;
- `neptune-marketing/e2e/batch5c-isolated-e2e.mjs`.

Det isolerade generatorverktyget
`enkey-agents/tools/tariffer/generera_isolerad_batch5c.py` säger dessutom
att det skapar en spärrad kandidat genom att rensa utredningar. Mot den nu
aktiva katalogen är rensningen en tyst no-op. Testet passerar, men dess
beskrivning och kontrollpunkt bevisar inte längre det som namnen påstår.

### P2.2 — Aktiveringsinvarianten om 53 oförändrade äldre produkter är bokstavligen falsk

Den semantiska generatordiffen ger rätt åtta nya produkt-ID:n och inga
borttagningar. Av de 53 äldre produkterna är 52 oförändrade. Den befintliga
produkten
`oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024`
har däremot fått visningsnamnet ändrat från `Öresundskraft` till
`Öresundskraft — Helsingborg Totalvärme, central installerad före 2024`.

Ändringen är väntad och korrekt: generatorn disambiguerar namnet när flera
aktiva produkter nu delar samma medlem. ID, prisdata och policy är
oförändrade. Den ska alltså **inte** återställas. Däremot måste den pinnas
som avsiktlig regression och den levande handoffens påstående om
"oförändrade 53 äldre produkter" rättas. Historiska granskningsdokument ska
inte skrivas om; den här granskningen och en daterad sessionsrättelse
ersätter den gamla invarianten.

## Oberoende verifiering

Codex verifierade på huvudena ovan:

- exakt åtta Batch 5c-rader gick från utredning till `investigation: null`;
- övriga katalogtariffers innehåll är oförändrat och katalogens faktiska
  SHA-256
  `ac0ffeef29cf119340c13934a578cca5c9f421192bdb66f26d777e194f0157f9`
  matchar både provenienstest och genererad TypeScript;
- `production_ready:false` och `contract_required:true` består på samtliga
  åtta aktiverade rader;
- generatordiffen har exakt åtta tillagda ID:n, inga borttagna ID:n, 52
  helt oförändrade äldre produkter och endast namnändringen ovan på den
  femtiotredje;
- Python, tariffsviten: **1793 passed, 4 skipped**;
- TypeScript/Vitest: **1897 passed** i 54 filer;
- `npx tsc --noEmit`: rent;
- `npm run eval:build`: grönt, 971 moduler;
- ordinarie E2E: scenario 1–23 gröna;
- isolerad Batch 5c-E2E: scenario 1–23 gröna;
- `git diff --check` är rent i alla tre repon och bygggenererad `dist/`
  återställdes efter körningen.

## Bindande rättningsinstruktion till Claude

1. Låt aktiveringen, katalogdata, beräkningsmotor och policyer vara orörda.
2. Uppdatera samtliga Batch 5c-kommentarer/dokumentationssträngar listade i
   P2.1 så att de beskriver det aktiva läget och tydligt skiljer det
   arkiverade isolerade regressionsflödet från den ordinarie E2E-sviten.
3. Gör `generera_isolerad_batch5c.py` fail-closed för det nya läget: verifiera
   att exakt de åtta förväntade ID:na finns och redan har
   `investigation is None`; kasta vid avvikelse i stället för att tyst
   skriva över `investigation`. Behåll fil-/npm-namnen om ett namnbyte skulle
   skapa onödig churn, men byt kandidatbegrepp i utdata och kommentarer.
4. Utöka `tariffer.generated.batch5c.test.ts` med en explicit assertion för
   den avsiktliga Öresundskraft-disambigueringen. Den äldre produktens ID
   ska finnas kvar och exakt det nya visningsnamnet ska vara pinnat.
5. Rätta den levande Batch 5c-handoffens räkningsgrind till: åtta nya,
   inga borttagna, 52 äldre helt oförändrade och en äldre produkt med endast
   den accepterade visningsnamnsändringen. Lägg en daterad rättelse i
   sessionsloggen; skriv inte om historiska Codex-granskningar.
6. Kör full tariff-Python, full TypeScript, `tsc --noEmit`, bygge,
   ordinarie och isolerad E2E samt `git diff --check`. Återställ `dist/`.
7. Commitera fokuserat lokalt i berörda repon, pusha inte och skriv en ny
   committad `REVIEW_READY: Codex`-post med exakta HEAD:ar och testutfall.

De separat pågående bryggfilerna i `conversations/automation/` och den
orelaterade arbetskopieändringen i `conversations/README.md` tillhör Codex
automationsarbete och får inte tas med i denna tariff-rättningsrunda.
