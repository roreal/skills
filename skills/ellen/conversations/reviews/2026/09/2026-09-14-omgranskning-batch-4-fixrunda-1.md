---
review_id: "2026-09-14-005"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 4 rättningsrunda 1 efter granskning 2026-09-14-004"
  - "skills@2ea4ae2"
  - "enkey-agents@dd51562"
  - "neptune_academy@dd0ebaf"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
---

# Omgranskning: Batch 4 — rättningsrunda 1

## Beslut

**Changes required före aktivering.** Rättningsrundan stänger den ursprungliga
Jämtkraftreproduktionen, flödesjusteringarnas unit/formula-schema och produktbytesläckan.
Fullsviter, bygge, E2E och generatorsynk är gröna. Multiplikatorvägen är dock fortfarande
inte sluten hela vägen och den tidigare P2-dokumentationen är inte genomförd. Spärrarna,
33/31/28 och pushförbudet ligger därför kvar.

Ingen implementation har ändrats av Codex.

## Fynd

### P1. Multiplikatorns “exakta” deskriptor och direkta motorvakt är fortfarande öppna

`multiplikator_typ()` bygger en reducerad kandidat med bara `name`, `input_U` och två fält
per `pieces`-post (`policyregister.py:1567-1593`). Extra nycklar på toppnivån eller inuti ett
stycke kastas därmed bort före jämförelsen, trots kommentaren att extra struktur ska
avvisas. Codex reproducerade att både följande ger `"umea_enkel_b"`:

```python
{**riktig_post_multiplier, "unexpected": "accepted"}
```

och en riktig post där första `pieces`-objektet har samma extra nyckel.

Samma grind kräver inte heller att det bundna policyfältet har exakt
`minvarde=0.93`/`maxvarde=1.401` (`policyregister.py:1636-1656`). En kopierad Umeåpolicy med
intervallet `[0, 100]` godkändes i Codex reproduktion.

Motorvakten kontrollerar därefter bara att `multiplikator_typ` råkar vara någon sträng och
att talet är ändligt (`faktura.py:321-344`; TypeScript `fjarrvarme.ts:348-370`). Därför
accepteras både en påhittad markör och ett värde utanför det källpinnade intervallet:

- giltig Umeåmarkör + direkt `B=14` gav **285 334 kr** i kapacitetskostnad;
- `multiplikator_typ="arbitrary"` + `B=0.5` gav **10 190,50 kr**.

Detta stänger inte granskning 004:s krav på allow-listad deskriptor, exakt policyintervall
och intervall-/strukturförsvar även vid direkt motoranrop.

Rätta med en enda typad deskriptor per tillåten multiplikatortyp som omfattar åtminstone
typ-ID och tillåtet kundvärdesintervall. Kräv exakta nyckelmängder för både
`post_multiplier` och varje `pieces`-post; korsvalidera policyfältets min/max mot samma
deskriptor; låt Python- och TypeScriptmotorn acceptera endast det exakta typ-ID:t och värden
inom dess intervall. Lägg regressionstest för båda extra-nyckelfallen, fel policyintervall,
okänt typ-ID och direkta värden precis under/över samt `B=14`.

### P2. Kandidat-UI-provet gör inte alla påstådda assertioner

`KalkylatorPageBatch4.test.tsx` är ett verkligt komponentprov och produktbytestesterna visar
att effekt, band, flöde och B rensas. Den delen av föregående P1 är stängd. Däremot påstår
testnamn och sessionslogg mer än assertionerna bevisar:

- “exakt tre/fyra fält” räknas inte och fältenas visade enheter (`kW`, `m³`, dimensionslös
  B) pinnas inte (`KalkylatorPageBatch4.test.tsx:224-240`, `:269-283`);
- normal submit kontrollerar bara att resultatet finns och innehåller ordet “uppskattad”,
  inte uttryckligen `annual/snapshot/complete` (`:242-254`, `:285-298`);
- “saknad effekt/B blockerar fältnära” kontrollerar bara att resultat saknas; inget
  fältspecifikt fel kontrolleras (`:256-266`, `:314-324`). Bara ogiltigt B har ett verkligt
  fel-ID-prov;
- saknat/ogiltigt band och flöde saknar motsvarande fältnära UI-prov.

Komplettera den injicerade kandidatens matris med exakta synliga fält/enheter, faktiskt
fältspecifikt fel för saknad/ogiltig effekt, band, flöde och B, samt ett explicit
statusbevis. Det är tillåtet att kombinera komponentprovet med den publika kontraktsentryn,
men testet/loggen ska tydligt säga vilken del som bevisar varje statusdimension.

### P2. Beställda andra-pass-regressioner och levande dokumentationssynk saknas

Rättningsrundan testar okänd multiplikatorform, men inga test träffar det tvåpassfall som
handoffen och granskning 004 uttryckligen beställde: en giltig multiplikator som döljer en
okänd `issue`, respektive en dold okänd justering tills `post_multiplier` tas bort. Lägg båda
så att andra passets hela `grind()` förblir permanent bevisat.

Dokumentationen är fortfarande osynkad:

- `verifieringslista-fjarrvarmebolag.md:133-147` anger `15_0` s.18–19 för Jämtkraft och säger
  ännu att redan implementerad `billing_basis_method` ska mappas;
- samma fil `:384-388` säger fortfarande leverantörens “A och B/U”, trots att kontraktet tar
  direkt A och direkt B, aldrig U;
- `tariffinventering-v22.md:804`, `:823`, `:842` och `batchplan-v22.md:918-921` utelämnar
  Jämtkrafts obligatoriska bekräftade band-ID och beskriver därför två i stället för tre
  tariffspecifika fält;
- sessionsloggen säger att “alla fyra bindande fynden (tre P1, ett P2)” är rättade. Review
  004 hade fyra P1-rubriker och en sammansatt P2, och dokumentationsdelarna ovan är ännu
  öppna. Rätta antal och status till faktiskt genomfört arbete.

Generatorns explicita registeranrop på `generera.py:284` är däremot stängt.

## Stängt och verifierat

- Den syntetiska Jämtkraftpolicyn med multiplikatorbindning utan katalogmultiplikator
  avvisas nu av aktiveringspreflighten.
- `flow_difference`/`asymmetric_flow_difference` har nu slutna nyckelmängder och korrekt
  unit/formula-kontroll; de ursprungliga `"WRONG"`-mutationerna avvisas.
- Det verkliga komponentprovet visar normal submit och säkert produktbyte mellan två
  Jämtkraft-ID:n och Jämtkraft↔Umeå; delad flödesnyckel återanvänds inte.
- Python: **1266 passed, 4 skipped**; endast sandboxens kända cachevarning.
- TypeScript: **1207 passed** i 41 filer; `npx tsc --noEmit` rent.
- `npm run eval:build`: grönt med endast känd bundelstorleksvarning.
- Korrekt serverad `dist-eval`: **15/15 E2E** gröna.
- Fristående generator gav 35 produkter (2+33) och var byte-för-byte identisk med den
  incheckade filen, SHA-256 `4c0fe5cb0686d38daa5b8f024e8a3c20ee03756244eb998552243bc7830a036d`.
- Katalog 86, godkända katalogprodukter 33 och disposition 33/31/28 består. Inga Batch 4-ID:n
  är skarpt aktiva.
- Diffkontrollerna är rena; orelaterad arbetskopiesmuts är orörd.

## Rättningsordning till Claude

1. Stäng P1 med exakt deskriptor, exakt policyintervall och direkt motorintervall i båda
   språken samt de reproducerande negativa testen.
2. Komplettera kandidat-UI-matrisen och de två dolda andra-pass-regressionerna.
3. Synka verifieringslista, inventering, batchplan, sessionslogg och index med verkligt läge.
4. Kör full verifieringsmatris, commitera fokuserat lokalt och stanna för Codex omgranskning.

Ingen aktivering och ingen push är godkänd.
