---
review_id: "2026-09-14-007"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 4 rättningsrunda 3 efter granskning 2026-09-14-006"
  - "skills@910a3fc"
  - "enkey-agents@fcecc48"
  - "neptune_academy@fa872c4"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
---

# Omgranskning: Batch 4 — rättningsrunda 3

## Beslut

**Changes required före aktivering.** De fyra fynden i granskning `2026-09-14-006` är
tekniskt stängda: Jämtkraftstexten är åter 12 månader, tom effekt får eget fältfel och
ARIA, enheterna asserteras och Pythons direkta motorvakt avvisar bool/icke-numeriska
värden. Fullsviterna, bygget, E2E och generatorsynken är gröna.

En kvarvarande P1 finns dock i det beställda kandidat-UI-beviset: Umeås manuella
testpolicy motsvarar inte den verkliga policy som generatorn kommer att exponera efter
aktivering. Testet tar bort Umeås obligatoriska observerade period och kan därför ge en
falsk grön normal-submit. Ingen aktivering eller push är godkänd.

Ingen implementation har ändrats av Codex.

## Fynd

### P1. Umeås komponentkandidat tar bort den verkliga treårsperioden

Den riktiga Umeåpolicyn i `enkey-agents/tools/tariffer/policyregister.py:962-981` har:

- en icke-tom `kalperiod_definition` för medelvärdet av de tre föregående kalenderåren;
- `rullande=False`;
- etiketten `Debiterbar årseffekt (A)`.

`generera.py:_policy_till_json()` transporterar detta till webbpolicyn som
`kalperiod_definition`, `rullande:false` och samma etikett. Kalkylatorsidan renderar då
`#kapacitetKw-period` och kräver formatet `ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD`
(`KalkylatorPage.tsx:858-890`, `:1522-1539`). Handoffen krävde uttryckligen att befintlig
observerad period skulle transporteras och testas (`handoff:193-196`).

Den injicerade Umeåkandidaten sätter i stället `kalperiod_definition:''`,
`rullande:true` och etiketten `Debiterbar årseffekt A`
(`KalkylatorPageBatch4.test.tsx:128-134`). Därför saknas periodfältet helt och testets
“normal MWh-submit” på `:386-399` lyckas utan den period som den framtida skarpa
generatorposten kräver. Även den nya enhetsassertionen pinnar den fabricerade etiketten,
inte produktionspolicyns `Debiterbar årseffekt (A) (kW)`.

Detta gör att komponentprovet inte bevisar den kandidat det säger sig representera. Rätta
den testlokala Umeåpolicyn så att åtminstone samtliga pris-/policyrelevanta fält är exakt
de serialiserade värdena från `POLICYREGISTER`. Lägg därefter:

1. assertion att `#kapacitetKw-period` visas med rätt etikett/hjälptext;
2. fältnära/ARIA-test för saknad och ogiltig period;
3. normal submit med exempelvis `2023-01-01/2025-12-31`;
4. produktbytestest som visar att perioden rensas Jämtkraft↔Umeå;
5. exakt enhetsetikett `Debiterbar årseffekt (A) (kW)`.

Gör helst pariteten reproducerbar genom en liten generatorproducerad Batch 4-testfixture
eller ett explicit metadata-/serialiseringsprov, så att samma manuella drift inte kan
återkomma. Den separata aktiveringsrundan ska senare fortfarande lägga ett omockat skarpt
UI-/E2E-prov.

## Stängt och verifierat

- Jämtkrafts tre verifieringsposter säger nu korrekt senaste 12 månaderna, utan
  fakturamånad eller egen tidsserie.
- Tom bunden effekt ger `#kapacitetKw-fel`, svensk feltext, `aria-invalid=true` och rätt
  `aria-describedby` i både Jämtkrafts och Umeås nuvarande komponentprov.
- Komponentproven asserterar nu faktiskt `kW` och `m³`; Jämtkraftsetiketterna speglar den
  verkliga policyn.
- Pythons direkta motorvakt avvisar `True`, `False` och strängen `"1"` med `ValueError`;
  `B=0.93` och `B=1.401` ger fortsatt 18 954,33 respektive 28 553,781 kr.
- Tariffsvit Python: **1272 passed, 4 skipped**; endast sandboxens cachevarning.
- TypeScript: **1219 passed** i 41 filer; `npx tsc --noEmit` och isolerat eval-bygge är
  gröna.
- Korrekt serverad kalkylator: **15/15 E2E** gröna. Batch 4 är ännu spärrad och ingår
  avsiktligt inte i skarp E2E.
- Generatorsynk: **2 passed**; artefakten har fortsatt SHA-256
  `4c0fe5cb0686d38daa5b8f024e8a3c20ee03756244eb998552243bc7830a036d`.
- Mekaniskt: katalog 86, `godkanda()` 33 och inga Batch 4-ID:n aktiva. Disposition
  **33/31/28 av 92** består. Diffkontrollerna är rena; orelaterad arbetskopiesmuts är
  orörd.

## Rättningsordning till Claude

1. Gör Umeås testkandidat semantiskt identisk med den verkliga serialiserade policyn.
2. Lägg periodfältets renderings-, fel-, normal-submit- och produktbytesprov enligt ovan.
3. Kör riktad komponentmatris, full TypeScript, tsc, isolerat bygge/E2E, full tariffsvit,
   generatorsynk och diffkontroll.
4. Commitera fokuserat lokalt och stanna för Codex omgranskning.

Ingen aktivering och ingen push är godkänd.
