---
review_id: "2026-09-04-012"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit e05b58e
  - neptune_academy commit df0f6ef
  - rättningar efter granskning 2026-09-04-011
reviewed_heads:
  enkey-agents: "e05b58e"
  neptune_academy: "df0f6ef"
implementation_changed: false
push_status: local-unpushed
---

# Omgranskning av rättningar i policyregister och produktgrind

## Bedömning

Tre av tre tidigare P1-fynd är rättade i själva beräkningsflödet:
`contract_required` måste nu vara exakt booleska `True`, E.ON/Navirums skalära rullande
effekt ger avtalat `snapshot/complete`, och de nakna hjälpfunktionerna har fått privata namn
samt arkitekturtester. Den konfigurerbara korsreposökvägen uppfyller också det dokumenterade
P2-villkoret. Samtliga 291 Python- och 307 TypeScript-tester, typkontrollen och
produktionsbygget passerar.

Kontrollpunkten behåller ändå **`changes-required` före push**, nu på ett enda avgränsat
fynd. Arkitekturtesterna är den enda mekaniska spärren mot den alltjämt importerbara nakna
kostnadsfunktionen, men de söker inte igenom hela produktionskoden. Därför upprätthåller de
inte ännu regeln de säger sig kontrollera.

## Fynd

### P1 — arkitekturtestet missar merparten av produktens möjliga konsumenter

TypeScripts `_arskostnadForKontraktfasad` är fortfarande en vanlig namngiven export från
`fjarrvarme.ts:794`. Det nya testet anger att det skannar varje källfil i `src`, men
`kallfiler()` använder endast `readdirSync` på `src/utils` och tar bara filer som slutar på
`.ts` (`resultatkontraktArkitektur.test.ts:20–28`). Det söker alltså varken rekursivt eller i
`.tsx`-filer.

Codex räknade 74 produktionsfiler av typen `.ts`/`.tsx` under `src`; testet granskar bara
fem. Bland de 69 missade filerna finns `src/pages/KalkylatorPage.tsx`, `src/App.tsx` och
samtliga komponentkataloger. Ett direktimporterat anrop från någon av dessa produktfiler
skulle därför inte fälla arkitekturtestet. Pythonvarianten använder på motsvarande sätt
`tools/tariffer/*.py` med icke-rekursiv `glob`, så en framtida konsument i en underkatalog
eller utanför tariffpaketets toppnivå missas.

Detta är viktigt eftersom namnbytet till inledande understreck inte är ett körningsskydd.
Codex importerade `_arskostnad_for_kontraktfasad` direkt på `e05b58e`, skickade ett
`_kraver_kontrakt=True`-prisobjekt och fick tillbaka en naken `Kostnad`. Det beteendet är
avsiktligt internt; därför måste arkitekturtestet verkligen täcka alla produktionskonsumenter.

**Begärd rättning:** låt TypeScript-testet söka rekursivt under hela `src` och inkludera
både `.ts` och `.tsx`, med endast definitionsfilen och `resultatkontrakt.ts` som tillåtna
produktionsundantag. Låt Python-testet söka rekursivt i relevant versionsstyrd produktkod,
exkludera testfiler och tillåt endast `faktura.py` respektive `resultatkontrakt.py`. Lägg en
självkontroll som bevisar att en representativ produktfil utanför `utils`, exempelvis
`KalkylatorPage.tsx`, faktiskt ingår i mängden som skannas. Ett AST-/importbaserat test är
robustare, men rekursiv textsökning räcker för denna avgränsade grundetapp.

### P3 — två kommentarer beskriver fortfarande det gamla beteendet

Docstringen för `berakna_arskostnad_med_kontrakt` säger fortfarande att en
kapacitetsbindning ”får inte vara rullande” (`resultatkontrakt.py:358`), trots att committen
korrekt åter tillåter just detta för ett skalärt snapshot. Kommentaren över TypeScripts
exporterade hjälpfunktion kallar samtidigt gränsen ”en riktig modulgräns”, fast funktionen
fortfarande exporteras och spärren i praktiken är arkitekturtestet. Rätta formuleringarna i
samma lilla commit så dokumentationen matchar koden.

## Godkända delar i denna runda

- generatorn skickar nu råvärdet och grinden kräver `contract_required is True`,
- negativa tester täcker sträng, tal, lista och objekt,
- en rullande kapacitetsbindning kan konstrueras och ett skalärt leverantörsvärde ger
  `snapshot/complete` med prissatt kapacitet,
- en faktisk serie utan reduceringsregel stoppas tydligt före kostnadsanropet,
- passersedeln är fortsatt oexporterad och de nakna hjälpfunktionerna är privat namngivna,
- korsreposökvägen kan anges med `ELLEN_NEPTUNE_MARKETING_SOKVAG` och fristående opt-out är
  dokumenterad,
- inga riktiga tariffer, policyer eller genererade produktdata har aktiverats.

## Sista avgränsade rättningsbeställning till Claude

1. Gör båda arkitekturtesternas källfilsinventering rekursiv och heltäckande enligt fyndet.
2. Lägg självkontroll av att en fil utanför den nuvarande toppnivån verkligen skannas.
3. Rätta de två inaktuella kommentarerna.
4. Kör hela Python- och TypeScript-sviten, `tsc --noEmit` och produktionsbygget.

Ändra ingen affärslogik, aktivera inga tariffer och pusha inte före nästa Codex-kontroll.

## Utförda kontroller

- `enkey-agents@e05b58e`: 291/291 tariff-pytest passerar.
- `neptune_academy@df0f6ef`: 307/307 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda committerna.
- Båda implementationsarbetskopiorna är rena och ligger lokalt 7 respektive 34 commits
  före sina fjärrgrenar.
- Maskinell inventering bekräftade 74 TypeScript-/TSX-produktionsfiler men endast fem filer
  i arkitekturtestets faktiska skanningsmängd.
- Direkt Pythonanrop bekräftade att den privat namngivna hjälpfunktionen fortfarande är
  importerbar och returnerar naken `Kostnad`; arkitekturtestet är därför den avgörande
  kodbasregeln.

Codex ändrade ingen implementation, tariffdata, commit eller push under granskningen.
