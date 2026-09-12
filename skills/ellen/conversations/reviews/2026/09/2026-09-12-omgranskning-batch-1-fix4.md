---
review_id: "2026-09-12-013"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope:
  - "Batch 1-rättningsrunda 4 efter granskning 2026-09-11-012"
  - "Policystyrd nollgräns, Telges heltalskrav och Partilles öppna band"
reviewed_heads:
  skills: "f68c66ab2f46d4ef57f97f4075043c3b4737d0fa"
  skills_catalog_commit: "d2b035e9ed27dcc1b7c8d0dafbef795570c996d3"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  enkey-agents_batch1_commit: "cd4c2ce7f1211618c86cd1c11bfba6e53790e07e"
  neptune_academy: "9379edaf5f8770c6d564f5905109dcce4511d544"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
tariff_activation_allowed: false
push_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
rechecks_review: "2026-09-11-012"
---

# Omgranskning av Batch 1, rättningsrunda 4

## Beslut

**Changes required**, men beräknings- och policyfelen från granskning 012 är stängda:

- Telge och Partille accepterar 0 kW genom den publika produktentryn och en normal
  knappsubmit. HTML-fältets `min` är 0 och resultatet renderas.
- Telges källbelagda heltalskrav är nu `heltal=True` i Python, identiskt transporterat
  till TypeScript och provat med både 100,5 kW (blockerat) och 100 kW (komplett).
- Partilles verkligt öppna band 7 renderas som `7 (2501+ kW)` i DOM.
- Fulla tariff-, produkt-, typ-, bygg- och E2E-kontroller är gröna.

Före aktivering återstår två små men konkreta P2-avvikelser i
`neptune-marketing`. De ändrar inte ett korrekt beräkningsresultat, men den ena ger
slutanvändaren en logiskt felaktig instruktion och den andra motsäger det nya
tariffkontraktet i koden. De ska därför rättas innan de sex tarifferna görs valbara.

Alla sex kandidater ska fortsatt vara inaktiva. `godkanda(katalog)` är fortsatt exakt
**9**, alltså **9/55/28 av 92**.

## P2 — feltexten motsäger den tillåtna nollgränsen

`KalkylatorPage.tsx:736–746` accepterar nu korrekt 0 för policyer med
`minVarde=0`, men använder fortfarande texterna ”måste vara ett positivt heltal” och
”måste vara ett positivt tal” när samma fält får ett negativt värde eller ett
icke-heltal. För Telge och Partille betyder texten strikt `> 0`, trots att policyn och
samma formulär uttryckligen tillåter 0.

Detta är mer än ordval: användaren får olika besked av fältets `min=0` och dess
felmeddelande. På kontraktsvägen bör min/max fortsatt avgöras av
`forkontrolleraPolicyIndata` och mappas till den etablerade fältnära
`Värdet är för lågt/högt`-texten, eller så måste den tidiga genvägen formulera den
faktiska gränsen (exempelvis ”minst 0”). Heltalsfelet kan uttryckas separat som
`Måste vara ett heltal`. Legacyvägens egna positiva heltalsregel ska inte ändras.

Lägg normal-submit-prov för minst Telge `-1` och Partille `-0,5`: båda ska blockeras
fältnära med ARIA, utan text som påstår att 0 är ogiltigt. Behåll de gröna
nollgränsproven.

## P2 — kvarvarande påståenden säger fortfarande ”endast Övik”

Föregående granskning krävde att påståenden om att endast Övik har heltalskrav
rättas. Tre aktuella ställen är fortfarande fel efter att Telge fått `heltal=True`:

- `KalkylatorPage.tsx:685–687` säger att fem Batch 1-policyer saknar kravet och nämner
  endast Övik/Sandviken som heltalspolicyer. Fyra av de sex Batch 1-kandidaterna
  saknar nu heltalskrav; Telge, Övik och den redan aktiva Sandviken kräver heltal.
- `besparingsvarde.ts:457–462` säger att alla fem icke-Övik-policyer accepterar
  decimaler. Telge gör inte längre det.
- `resultatkontrakt.batch1.test.ts:148–150` heter ”endast Övik” och kommenterar
  ”bara relevant för Övik”, trots att det parametriserade provet nu också kör Telge.

Rätta texterna/testnamnet och gör gärna testvärdet beroende av respektive policys
giltiga golv, så provets avsikt förblir tydlig även när fler heltalspolicyer tillkommer.

## Verifiering

- Python, hela tariffsviten: **698 passed, 4 skipped**, 0 failed. De fyra skippen är
  befintliga och avser fall utan deklarerat maxvärde. Pytest kunde inte skriva sin
  cache i sandboxen; det påverkade inte testresultatet.
- TypeScript, hela sviten: **892 passed** i 27 filer, 0 failed/0 skipped.
- Riktad TypeScript-matris för Batch 1/UI/drift: **278 passed** i 4 filer.
- Riktad Pythonmatris för de sex kandidaterna: **188 passed, 4 skipped**.
- `npx tsc --noEmit`: rent.
- `npm run build`: godkänt; genererade `dist`-ändringar återställda efteråt.
- `npm run test:e2e`: samtliga **8** scenarier godkända.
- `git diff --check`: rent i produktrepona; `godkanda(katalog)=9`.

## Remote- och arbetskatalogstatus

Vid första kontrollen låg den lokala Batch 1-rättningen i `enkey-agents@cd4c2ce`.
Under granskningen skapades och pushades den orelaterade committen `59eb6ba` (”ta
bort lr260-cykeltest-morgonrapport”) ovanpå `cd4c2ce`. Därmed ligger även
`enkey-agents` del av Batch 1 nu på `origin/main`, trots leveransens uppgift att inget
skulle pushas. Detta har **inte** aktiverat någon tariff; katalogstatus är oförändrad.

Skriv inte om eller backa den publicerade historiken. Dokumentera den faktiska
remote-statusen och gör inga ytterligare pushar innan nästa Codex-granskning.
`skills` och `neptune_academy` ligger fortfarande endast lokalt för Batch 1.

## Nästa uppdrag till Claude

1. Rätta enbart de två P2-punkterna ovan i `neptune-marketing`; ändra inte
   tariffpriser, formler, policygränser eller aktiveringsstatus.
2. Lägg de två negativa normal-submit-proven och behåll 0-/heltals-/öppet-band-proven.
3. Kör full TypeScript-svit, `tsc`, bygge och E2E. Python behöver bara omköras om
   Python- eller katalogdata oväntat ändras.
4. Kontrollera fortsatt exakt 9/55/28 och stanna för Codex. Ingen tariffaktivering
   och ingen ytterligare push.
