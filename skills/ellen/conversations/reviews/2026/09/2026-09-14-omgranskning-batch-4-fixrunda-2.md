---
review_id: "2026-09-14-006"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 4 rättningsrunda 2 efter granskning 2026-09-14-005"
  - "skills@62b0bc9"
  - "enkey-agents@5a56c27"
  - "neptune_academy@8e5bb96"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
---

# Omgranskning: Batch 4 — rättningsrunda 2

## Beslut

**Changes required före aktivering.** Multiplikatorns exakta katalog–policy–motorbindning,
de två andra-pass-regressionerna, produktbytet och statusbeviset är nu stängda. Alla sviter
är gröna och de fyra kandidaterna ligger fortsatt bakom spärr. Rättningsrundan införde dock
en felaktig 36-månadersregel för Jämtkraft i verifieringslistan, och UI-matrisen uppfyller
ännu inte det beställda fältnära felet för tom effekt eller sina påstådda enhetsassertioner.
Pythons direkta motorvakt har dessutom en typglipa mot TypeScript.

Ingen implementation har ändrats av Codex. Ingen aktivering eller push är godkänd.

## Fynd

### P1. Jämtkrafts verifierade 12-månadersregel har skrivits om till fel 36-månadersregel

`verifieringslista-fjarrvarmebolag.md:135`, `:140` och `:145` säger nu att Jämtkrafts
debiteringseffekt bygger på de senaste **36 månaderna inklusive fakturamånaden**, att en
bekräftad fakturamånad krävs och att kalkylatorn slipper en egen 36-månadersserie. Det är
E.ON/Navirums bas-/delvärmeregel, inte Jämtkrafts.

Jämtkrafts officiella [prisändringsmodell 2026–2028](https://www.jamtkraft.se/wt/documents/519/Pris%C3%A4ndringsmodellen_2026-2028.pdf)
anger på tryckt sida 11 att debiteringseffekten bygger på medelvärdet av de tre högsta
dygnsmedeleffekterna under de senaste **12 månaderna**. Den interna källpinnade katalogen
och policyn säger också 12 månader (`optimate-fjarrvarme-2026.json:4760` m.fl.;
`enkey-agents/tools/tariffer/policyregister.py:942-959`) och har inget krav på
fakturamånad. Dokumentet motsäger alltså både källan och den implementerade policyn.

Återställ alla tre Jämtkraftrader till “tre högsta dygn under senaste 12 månaderna”, ta
bort fakturamånad/36-månadersserie och lägg gärna ett käll-/dokumentationsprov som hindrar
att bas-/delvärmetexten kopieras hit igen. Detta är ett proveniensfel och måste vara stängt
innan raderna kan aktiveras.

### P2. Tom obligatorisk effekt visas fortfarande inte med applikationens fältnära fel

Handoffen kräver att saknad eller ogiltig effekt ger fältnära `saknadeFalt`/`ogiltigaFalt`
före motoranrop. De nya testen har i stället bytt namn till “inget resultat visas” och
beskriver uttryckligen att `#kapacitetKw-fel` inte visas
(`KalkylatorPageBatch4.test.tsx:279-295`, `:417-431`). När fältet är tomt stoppar HTML:s
`required` formulärets submit innan Reacts felmappning körs. Därmed bevisas bara
webbläsarens generiska constraint validation, inte kalkylatorns svenska fältnära fel,
`aria-invalid` och `aria-describedby` som beställdes.

Gör den tomma vägen till en riktig applikationsvalidering för det bundna
`kapacitetBindning`-fältet och assertera `#kapacitetKw-fel`, feltext, `aria-invalid=true`
och `aria-describedby="kapacitetKw-fel"` för både Jämtkraft och Umeå. Behåll gärna
`required` som extra webbläsarskydd, men låt inte det ersätta det explicita kontraktsfelet.

### P2. Enhetsproven pinnar inte enheterna de säger sig verifiera

Jämtkraftstestet söker hjälptexten om effekt och delar av flödesetiketten, men ingen
assertion kräver texten `kW` eller `m³` (`KalkylatorPageBatch4.test.tsx:246-249`).
Umeåtestet pinnar bara att B är dimensionslös; det kontrollerar inte effektens `kW` eller
flödets `m³` (`:350-369`). En felaktig renderad enhet skulle därför fortfarande ge grönt.

Pinna de fullständiga synliga etiketter eller tillgängliga namnen, exempelvis
`Debiterbar effekt (kW)`, `Debiterbar årseffekt (A) (kW)` och
`Flöde 1 oktober–30 april (m³)`, samt fortsatt exakt `Kapacitetsfaktor B` utan suffix.

### P2. Pythons direkta motorvakt accepterar bool som faktor B

`_arskostnad_kapacitet()` använder `math.isfinite()` och numeriska intervall utan att först
utesluta `bool` (`faktura.py:342-378`). Eftersom `bool` är en underklass till `int` i
Python ger ett direkt anrop med Umeås riktiga prispost och `kapacitet_multiplikator=True`
kapacitetskostnaden **20 381 kr**. TypeScriptmotorn avvisar samma värde genom
`Number.isFinite(true)`, och produktkontraktet avvisar bool, men den uttryckligen beställda
direkta motorvakten är därför inte språkparitär eller helt fail-closed.

Avvisa `bool` (och andra icke-numeriska typer) explicit före `math.isfinite`, returnera ett
kontrollerat `ValueError` och lägg ett direkt Python-regressionstest. Bekräfta samtidigt
att TypeScriptprovet för icke-numeriskt B består.

## Stängt och verifierat

- Exakta nyckelmängder för Umeås `post_multiplier` och varje `pieces`-post avvisar nu extra
  struktur; policyintervallet måste vara exakt `[0.93, 1.401]`.
- Python- och TypeScriptmotorn avvisar okänt typ-ID, `B=14`, värden precis utanför
  intervallet, NaN och oändlighet; båda gränsvärdena fungerar.
- Kompositgrindens andra pass har permanenta tester för dold okänd `issue` och okänd
  justering.
- Komponenten räknar rätt antal fält, testar normal submit, alla generiska band-/flöde-/B-
  fel och produktbyte. `annual/snapshot/complete` är explicit pinnat via den publika
  kontraktsentryn.
- Tariffsvit Python: **1271 passed, 4 skipped**; endast sandboxens cachevarning.
- TypeScript: **1218 passed** i 41 filer; `npx tsc --noEmit` och produktionsbygge gröna.
- Isolerat eval-bygge och korrekt serverad kalkylator: **15/15 E2E** gröna. Batch 4 är ännu
  spärrad och finns därför avsiktligt inte som skarpt E2E-scenario.
- Generatorsynkprovet ingår i den gröna Python-sviten. Den incheckade filen har fortsatt
  33 katalogprodukter + 2 leverantörsfiler, SHA-256
  `4c0fe5cb0686d38daa5b8f024e8a3c20ee03756244eb998552243bc7830a036d`, och inga Batch
  4-ID:n.
- Mekaniskt: katalog 86, `godkanda()` 33, alla fyra Batch 4-ID:n frånvarande. Disposition
  **33/31/28 av 92** består. Diffkontrollerna är rena; orelaterad arbetskopiesmuts är orörd.

## Rättningsordning till Claude

1. Rätta Jämtkrafts tre dokumentationsrader till den verifierade 12-månadersregeln utan
   fakturamånad och 36-månadersindata.
2. Ge tom bunden effekt kalkylatorns fältnära svenska fel och komplettera båda UI-proven
   med fel-ID/ARIA.
3. Pinna faktiskt `kW`/`m³` i komponentproven och stäng Pythons bool-/typglipa.
4. Kör riktade tester, full tariffsvit, full TypeScript, tsc, isolerat bygge, E2E,
   generatorsynk och diffkontroll; commitera fokuserat lokalt och stanna för ny Codex
   omgranskning.

Ingen aktivering och ingen push är godkänd.
