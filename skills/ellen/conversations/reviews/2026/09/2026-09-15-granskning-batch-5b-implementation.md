---
review_id: "2026-09-15-009"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5b lokal implementation bakom spärr"
  - "skills@fe55aaf (funktionell katalogcommit 73f3035)"
  - "enkey-agents@5f1529f"
  - "neptune_academy@3bd4d5d"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5b.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Granskning: Batch 5b lokal implementation

## Beslut

**Changes required före aktivering. Ingen push.** De sex
`investigation.status="utreds"`-spärrarna ligger korrekt kvar och den skarpa
generatorn har inte läckt ut någon Batch 5b-produkt. Pythonmotorns
fullårsflöde, Jönköpings grundformel `pris × 12 × antal`, Habo-/Jönköpings
effektmetoder och de handräknade Pythonfaciten är i huvudsak rätt.

Leveransen stannar ändå före aktivering eftersom Jönköpings verkliga
produktväg inte kan skapa giltig kontraktsindata, accessavgiftens statiska
grind inte korsvaliderar det kontrakt den uppges skydda och den bindande
speglade acceptansmatrisen saknas. Dokumentens levande status är dessutom
självmotsägande.

## Fynd

### P1 — Jönköpings produktväg är inte implementerad och kan inte ge ett resultat

`byggIndataFranPolicy()` sätter fortfarande `kallaTyp: 'supplier_value'` på
**varje** generiskt policyfält. Jönköpings accessval och antal undercentraler
tillåter däremot bara `customer_value`; ett framtida skarpt anrop blir därför
`invalid_policy_fields`. `Tariffberakningsunderlag`/`argsFranInputs()` bär
inte heller det globala `substations`-värdet till `byggKontraktIndata()`, så
det bundna antalet kan inte injiceras därifrån.

Samtidigt filtrerar `policyFaltMetadata()` bara bort
`kapacitetBindning`, inte `antalUndercentralerBindning`. En isolerat genererad
Jönköpingspolicy skulle därför visa ett **andra** synligt antal-undercentraler-
fält i stället för att återanvända formulärets globala fält. Det generiska
enum-UI:t visar dessutom bara `0`, `10`, `25`, `50`; de fyra föreskrivna
accessbeskrivningarna och villkoret om tillsynstjänst/avtal från 2024 saknas.

Berörda ställen:

- `neptune-marketing/src/utils/besparingsvarde.ts:221-298`
- `neptune-marketing/src/utils/energiPotential.ts:457-499`
- `neptune-marketing/src/utils/resultatkontrakt.ts:1131-1146`
- `neptune-marketing/src/pages/KalkylatorPage.tsx:1369-1379`

Detta är ett funktionsfel, inte något som kan skjutas till
aktiveringsrundan. Handoff `2026-09-15-001` krävde uttryckligen en verklig,
isolerat genererad produkt-/UI-väg före Codex kodgranskning.

### P1 — accessavgiftens deskriptor och aktiveringspreflight är inte fail-closed

Katalogposten innehåller bara `type`, `unit`, `allowed_prices` och `months`.
De två kostnadsbärande policynycklarna refereras inte explicit; både Python-
och TypeScript-motorn hårdkodar i stället
`access_pris_kr_per_central_manad` och `antal_undercentraler`.

`kontrollera_accessavgiftsbindning()` validerar prisfältets typ/allow-list/
källa men inte att det gäller `annual`. För antalsfältet kontrollerar den
bara att bindningen inte är `None`. `Tariffpolicy.__post_init__` kontrollerar
nummer, heltal och att `customer_value` finns bland källorna, men inte
`kravs_for="annual"`, exakt källmängd eller gränserna 1–20.

Codex reproducerade detta genom att ersätta antalskravet med
`kravs_for=('monthly',)`, källor `customer_value + supplier_value` och
intervall 0–999. Den verkliga `kontrollera_accessavgiftsbindning()`
accepterade kontraktet utan fel (`PRECHECK_ACCEPTED_INVALID_COUNT_CONTRACT`).
Det motsäger handoffens krav att preflighten ska korsvalidera båda
fältnycklarna, annual-omfattning, heltal och intervall före generering.

Berörda ställen:

- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:5150-5171`
- `tools/tariffer/policyregister.py:2092-2147`
- `tools/tariffer/resultatkontrakt.py:529-554`
- `tools/tariffer/faktura.py:799-834`
- TypeScriptmotsvarigheten i `neptune-marketing/src/utils/fjarrvarme.ts`

### P1 — den bindande speglade acceptansmatrisen har inte levererats

Den nya Pythonfilen testar motorn väl för ett band per tariff och de fyra
accesspriserna, men följande uttryckliga acceptanskrav saknas fortfarande:

- alla band-ID:n samt saknat/tomt/okänt band för samtliga sex;
- saknat/ogiltigt/över max-flöde och exakt `delta_m3 × rate`;
- antal undercentraler 0, 21, decimal, NaN och oändlighet;
- produktbyte som rensar tariffsärskilda värden men bevarar globalt antal;
- blockerade kronor-, schablon- och besparingslägen;
- speglade TypeScriptfacit genom verklig, isolerat genererad kandidatpolicy;
- renderat Reactprov och omockat Jönköping-E2E med minst två centraler och
  icke-noll accessval;
- permanent 47/53-generatorprov och relevanta legacy-/Batch 3–5a-
  regressioner.

TypeScripts fullsvit är fortfarande exakt **1497** test, utan någon ny
Batch 5b-testfil. E2E-sviten har fortfarande exakt **19** scenarier och inget
Jönköpingsfall. Att kandidaterna ligger bakom spärr hindrar inte dessa prov:
tidigare batcher använder isolerat genererade fixturer just för detta.

### P2 — katalogens requestbokföring och de levande planavsnitten motsäger data

Katalogen har nu sex poster i `remaining_information_requests`, men
`coverage_summary.information_request_status_counts` står kvar på
`utreds: 14`, och `remaining_requests_note` beskriver fortfarande de gamla
intervallen R02–R10/R12–R15. `tariffinventering-v22.md` säger samtidigt att
katalogen har 14 kvarstående frågor och sammanfattar R04/R15 som helt
borttagna, trots att tabellraderna korrekt säger att de flyttats till
`resolved_information_requests`.

De sex levande tariffavsnitten står också kvar på "ej i POLICYREGISTER",
"inga tariffspecifika automattester" och "väntar på denna
implementationsomgång". Jönköpings avsnitt säger uttryckligen att
accessavgiften **inte** byggs i delbatchen. En konsoliderad not ovanför
avsnitten gör inte två motsatta aktuella statusar entydiga. Detta strider
mot både handoffens synkkrav och Ellens lokala regel att hålla tariffdata,
status och källa åtskilda och aktuella.

Slutligen uppdaterades datumen men inte de efterfrågade källtitlarna:
`web-review-falu-final` heter fortsatt `falu-final` och
`web-review-mjolby-final` fortsatt `mjolby-final`; Habotiteln innehåller
`varme`/`foretag` utan svenska tecken. Sessionsindexet har dessutom två
rader med ID `2026-09-15-002`, vilket gör referensen tvetydig.

Berörda ställen:

- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:55-58,715-719,757-761,11499`
- `Fjarrvarmetariffer/tariffinventering-v22.md:624-640,738-773,795-811,871-887,985-1001,4727-4748`
- `conversations/index.md:5-6`

## Oberoende verifiering

- Python tariffsvit: **1527 passed, 4 skipped**.
- Batch 5b + proveniens riktat: **53 passed**.
- TypeScript: **1497 passed**.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt.
- `npm run test:e2e`: **19/19**, men inget Batch 5b-scenario finns.
- Oberoende generatorräkning: nu **45 godkända / 47 skarpa**, isolerad
  kopia **51 godkända / 53 skarpa**, noll Batch 5b-läckage.
- `git diff --check`: rent i alla tre leveransdifferna.
- Ett oscopeat `pytest -q` från hela `enkey-agents` samlar även Milesight-
  tester och stoppade på 14 redan orelaterade import-/beroendefel; den
  avsedda `tools/tariffer/tests`-sviten är helt grön enligt ovan.

Gröna befintliga sviter upphäver inte fynden: de nya TypeScript-/UI-vägarna
saknas och kan därför inte fallera i dagens testmängd.

## Rättningsorder till Claude — fixrunda 1

1. Slutför produktadaptern generiskt: injicera validerat `substations` som
   `customer_value` i `antalUndercentralerBindning`, filtrera bindningen ur
   `policyFaltMetadata` och ge `customer_value` även åt accessvalet utan att
   felmärka övriga leverantörsfält. Båda publika produktvägarna ska omfattas.
2. Gör `metered_access_fee` till en sluten, explicit fältrefererande
   deskriptor i katalog/Python/TypeScript. Preflighten ska korsvalidera
   exakt prisnyckel, antalsnyckel, annual-omfattning, typer, exakt källtyp,
   prisallow-list, heltal och 1–20. Lägg negativa mutationsprov som bevisar
   att varje avvikelse stoppas före generering.
3. Bygg accessvalets fyra begripliga etiketter och fulla villkorstext utan
   tariff-ID-hårdkodning. Noll ska kräva ett aktivt val och inte vara
   default.
4. Leverera hela acceptansmatrisen i Python **och** TypeScript via verklig
   katalog/policy/fasad/motor. Använd en genererad isolerad 53-produkts-
   fixture för React-/produktprov och ett omockat Jönköping-E2E.
5. Synka katalogens requesträkning/not, de sex levande tariffavsnitten,
   §7-sammanfattningen, källtitlarna och det dubblerade sessions-ID:t.
6. Kör fulla tariff-/TS-/tsc-/isolerat bygg-/E2E-/generator-/diffkontroller,
   committa fokuserat lokalt och logga exakta hashar. Låt alla sex spärrar
   ligga kvar. **Ingen aktivering och ingen push.**
