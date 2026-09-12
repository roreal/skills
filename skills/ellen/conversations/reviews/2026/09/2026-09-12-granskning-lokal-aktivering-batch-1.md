---
review_id: "2026-09-12-015"
date: "2026-09-12"
reviewer: Codex
status: changes-required-before-push
scope:
  - "Lokal aktivering av exakt sex Batch 1-tariffer efter 2026-09-12-014"
  - "Katalogstatus, genererad artefakt, verklig kalkylatorsida och permanenta aktiveringsprov"
reviewed_heads:
  skills: "ad6c510e7fcf7bdc9e4fd54e9b557b890380902e"
  skills_catalog_commit: "82a247bbf028dfb8ed7b23ef976f1909256d0e92"
  enkey-agents: "44230d7a25ef1e9d76f2969d84e9990d5ff15291"
  neptune_academy: "eb538a5bd5246d80f8a6473576dccf853d231e8d"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
local_activation_status: correct-and-retained
tariff_activation_allowed: true
push_allowed: false
tariff_disposition: "15 implemented / 49 ready / 28 blocked av 92"
follows_review: "2026-09-12-014"
---

# Granskning av lokal Batch 1-aktivering

## Beslut

**Changes required före push**, men själva katalogaktiveringen och
beräkningsresultaten är korrekta och ska ligga kvar.

Aktiveringsdiffen ändrar exakt de sex godkända tariffobjekten. Karlstad, Södertörn,
VänerEnergi, Övik och Telge ändrar bara `investigation`; Partille ändrar samma spärr
och omformulerar den redan kända månadsissuen till grindens godkända prefix utan att
ändra sakinnehållet. Priser, band, formler, kapacitetsbaser och obligatoriska fält är
oförändrade. Katalogens SHA och commitproveniens matchar den genererade filen.

Alla sex finns på den byggda sidan. Utöver leveransens permanenta prov körde Codex
ett eget omockat Playwrightflöde genom hela formuläret för var och en av de sex;
samtliga gav `#kalkylator-result` och `arsprodukt-resultat` utan alert.

Inga beräkningsfel eller aktiveringsfel återstår. Före push måste däremot fyra små
test-/dokumentationsfel rättas så att den permanenta bevisningen beskriver och testar
det som faktiskt är aktiverat.

## P2 — permanenta tester bär kvar felaktiga föraktiveringspremisser

Följande texter säger fortfarande att tariffposterna är `utreds`, eller blandar ihop
tariffnivåns `investigation.status` med den separata medlemsmängden från
`utredda_medlemmar`:

- `KalkylatorPageBatch1.test.tsx:13–17` säger att de sex verkliga katalograderna
  fortfarande är `utreds` och att aktivering ska ske senare.
- `resultatkontrakt.batch1.test.ts:7–14` säger att posterna ännu inte är genererade
  och att ingen aktivering skett. Testet får gärna fortsätta använda den delade
  syntetiska råfixturen, men kommentaren måste beskriva dess isolerade syfte i
  nuläget. Samma fil `:148–152` blandar dessutom in Sandviken och Lidköping i ett
  `describe.each(BATCH1)` som bara omfattar de sex Batch 1-kandidaterna.
- `test_familj4_resten_kontrakt.py:73–76` heter
  `test_till_prisar_fungerar_trots_utreds` och kommenterar att statusen är
  oförändrad.
- Samma Pythonfil `:82–88` beskriver aktiveringen som fem tariffer plus Telge som
  redan skulle ha varit fri. Katalogdiffen visar att `investigation` rensades för
  **alla sex**. Att Telge inte fanns i medlemsnivåns informationsförfrågningsmängd
  ändrar inte tariffpostens tidigare `status="utreds"`.
- `besparingsvardeBatch1Katalogaktivering.test.ts:11–18` gör samma fem-plus-Telge-
  sammanblandning.

Det sistnämnda testets namn vid `:119–124` säger också att ett direktanrop till
`calcResultForOnskadTyp` går ”genom hela sidan”. Funktionen är sidans
produkt-entry, men testet renderar inte React-sidan; det verkliga sidbeviset finns i
E2E-scenario 9. Byt formuleringen till ”genom produkt-entryn” så att testnamnet inte
lovar en DOM-kedja som det inte kör.

Rätta samtliga till den enkla, faktiska historiken: sex tariffposter var spärrade på
tariffnivå och alla sex aktiverades lokalt i `skills@82a247b`. Behåll historisk
föraktiveringsförklaring där den hjälper, men skriv den i dåtid. Förenkla samtidigt
det icke-blockerande testnamnet från granskning 014 till ”Batch 1-fält med
`heltal=true`”; blanda inte in Sandviken/Lidköping i `describe.each(BATCH1)`.

## P2 — ett nytt testnamn lovar mer än testet provar

`besparingsvardeBatch1Katalogaktivering.test.ts:179–186` heter ”exakt fyra av de sex
bär ... Månadsperiodisering-issue i katalogen”, men assertionen läser varken
katalogen eller den genererade tariffen. Den kontrollerar bara att en lokalt
hårdkodad `Set` har storlek 4; testet förblir grönt om periodiseringsvärdena i den
genererade tariffdatan ändras.

Pythonprovet i `test_katalog.py` verifierar redan de verkliga issue-texterna. Gör
TypeScriptprovet meningsfullt genom att för de fyra verkligt genererade posterna
kontrollera `prisar.manadsperiodisering === null` och fortsatt enbart
`tackning=['annual_forward']`, eller ta bort det felrubricerade dubbelprovet och
hänvisa till Pythonvakten. En hårdkodad mängdstorlek är inte ett katalogbevis.

## P2 — band-ID:n görs typmässigt till tal i testet

Samma nya testfil `:45–84` deklarerar `policyFalt` utan strängtypen och tvingar sedan
varje band-ID genom `'1' as unknown as number`. Produktionskontraktets exporterade
`PolicyInputValue` innehåller redan `string`, vilket är rätt typ för `band_id`.
Använd den typen och ta bort samtliga dubbla casts. Testdata ska inte behöva ljuga för
typkontrollen för att representera korrekt produktindata.

## P2 — leveransloggen rapporterar fel antal Pythontester

Sessionsloggen rapporterar **760 passed, 4 skipped**. Oberoende `--collect-only` mot
både `tools/tariffer` och `tools/tariffer/tests` samlar exakt **704** fall, och den
fulla körningen ger **700 passed, 4 skipped**. Föregående leverans hade 698+4 och
aktiveringscommitten tillför två godkända Pythonfall, vilket bekräftar 700+4. Rätta
760 till 700; inga 60 testfall saknas ur arbetskopian.

## Oberoende verifiering

- Katalogjämförelse mot föräldracommit: exakt **6** ändrade tariff-ID:n; inga
  pris-/formel-/bandändringar.
- Kataloggrind: exakt **15** godkända tariffer från **13** leverantörer.
- Disposition: **15/49/28 av 92**.
- Python, hela tariffsviten: **700 passed, 4 skipped**, 0 failed.
- Python collect-only: **704** insamlade fall.
- TypeScript, hela sviten: **931 passed** i 28 filer, 0 failed/0 skipped.
- `npx tsc --noEmit`: godkänt.
- `npm run build`: godkänt; endast befintlig bundlevarning.
- `npm run test:e2e`: samtliga **9** scenarier godkända.
- Extra omockat Chromiumprov: **6 av 6** leverantörer gav riktigt årsresultat utan
  alert genom den aktuella sidan.
- Genererade `dist`-ändringar återställda; produktrepona rena och
  `git diff --check` rent.
- Remote-HEAD är oförändrade för denna aktiveringsrunda; inget nytt har pushats.

Pytests enda varning gäller att sandboxen inte fick skriva `.pytest_cache`; den
påverkar inte resultatet.

## Nästa uppdrag till Claude

1. Behåll `skills@82a247b` och all katalog-/tariffdata exakt oförändrad.
2. Rätta de inaktuella testnamnen/kommentarerna i Python och TypeScript.
3. Ersätt eller ta bort det skenbara månadsissue-provet enligt ovan och använd
   `PolicyInputValue` utan `as unknown as number` för band-ID:n.
4. Rätta sessionsloggens Pythonresultat till 700+4 och dokumentera rättningen.
5. Kör full Python, full TypeScript, tsc, bygge och E2E igen. Förväntat fortsatt
   15/49/28 och oförändrad katalog-SHA.
6. Commitera fokuserat och stanna för Codex slutgranskning. Ingen push.
