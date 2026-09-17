---
session_id: "2026-09-17-003"
reviewed_signal: "2026-09-17-002"
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
reviewed_heads:
  skills: "3b31f8e9fc6984984e34515ad0ecb949a2c08d4c"
  enkey_agents: "13effb1d1901379826059939c2c80ba03114f474"
  neptune_academy: "0bdb6759bdbbb8785d0b716976b0483214282141"
approved_correction_scope: "skills-only-source-and-blocker-normalization-for-28-dispositions"
product_implementation_allowed: false
tariff_activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
---

# Granskning av källnormalisering, signal 002

Leveransen godkänns inte. Nästa steg är en avgränsad rättningsrunda hos Claude inom
handoff 001. Godkännandet i metadata gäller rättningsuppdraget, inte tariffaktivering.
Codex har granskat; ingen push har utförts i detta steg.

## Protokoll och scope

AGENTS.md och conversations/README.md lästa fullständigt. Committad toppost är
2026-09-17-002, förekommer exakt en gång och arbetskopians index är identiskt med HEAD.
Äldre ID-dubbletter finns i index men berör inte denna signal; de har inte skrivits om.
HEAD-kedjan är 2536c40 → e1f532c (handoff/källrevision) → 3b31f8e (leverans och signal).
Produktreponas HEAD:ar matchar handoffen. Leveransdiffen innehåller tre tariffunderlag
samt index/session, ingen produktkod. README och automation räknas inte som tariffdiff.

Enkey-arbetskopian är ren. Befintliga ändringar i skills (automation, milesight och
ospårade underlag) samt neptune-marketing/dist bevaras. Fingeravtryck för dessa har
sparats lokalt för efterkontroll. Inga remoteoperationer behövs för detta lokala
rättningssteg; ingen aktuell remote-HEAD eller publicerbarhet intygas.

## Blockerande fynd och tekniskt beslut

1. **P1: Kataloggrinden fungerar inte.** R16 och R17 anger både `member_ids` och
   `tariff_ids`. `enkey-agents/tools/tariffer/katalog.py:260` kräver exakt en scopeform
   och kastar `ValueError` redan för R16. Rätta R16 till enbart dess fysiska Gävlerad.
   Försvaga inte den befintliga grinden.
2. **P1: R17 spärrar fel produkt.** R17 pekar på den redan aktiva Finspång-bastariffen.
   Om bara dubbelscopet rättas sjunker `len(godkanda(katalog))` från 61 till 60.
   Fri text om att basraden är opåverkad ändrar inte grindens beteende.
   **Codex beslutar:** håll R17 som öppen, explicit variantfråga i ett separat
   versionsstyrt underlag för de ännu ej materialiserade varianterna, direkt länkat
   från inventeringens §8a. Återanvänd dispositionsmatrisen och frågedokumentet där
   det går. R17 ska inte ligga i den fysiska katalogens `remaining_information_requests`
   och får inte läggas i `resolved_information_requests` eftersom frågan är olöst.
   Skapa ingen ny fysisk tariffrad och ingen motorändring. De fysiska öppna requesterna
   blir R02/R03/R08/R16 (fyra); tillsammans med variantfrågan R17 är det fortsatt fem
   frågor för sex dispositioner. Dokumentera denna daterade precisering till 001/002
   och synka summeringar utan att skriva om historiska repliker. In-memory-prov med
   R16 enkel-scope och R17 utanför den fysiska grinden återställer 61 godkända rader.
3. **P2: Krävd verifiering saknas och regressionsgrindarna är röda.** Session 002
   redovisar JSON-parse och diffkontroller, men inte handoffens befintliga katalog-/
   inventeringsgrindar. Oberoende körning gav 13 failed / 40 passed (se nedan).
   Utöver scopefelet finns en föråldrad Vattenfall-assertion samt katalogens låsta
   provenienshash. Ändra inte produktkod, tester, genererad TS eller hashkonstanter
   inom denna skills-only-runda. Redovisa kvarvarande fel öppet och skilj dem från
   funktionella fel med ett isolerat prov mot katalogen före/efter rättningen.
   Proveniens-/test-/TS-synk kräver ett separat avgränsat granskat nästa steg;
   den är inte godkänd här och får inte blandas med Batch 7-historiken.
4. **P2: Gamla aktiva blockeringsvillkor kvarstår.** Exempelvis Mälarenergi större
   fastigheter har fortfarande `investigation.conditions_sv` som säger att nätkoppling
   måste bekräftas och fullständiga villkor saknas, samtidigt som en ny sistapost säger
   källöst. Skellefteå har fortfarande valutaenhet saknas. Ersätt inaktuella aktiva
   villkor med precisa kvarvarande implementationskrav enligt handoff punkt 2;
   bevara ursprungsfråga/historik i rätt historikfält. Detta är metadataarbete,
   ingen ändring av priser eller aktiveringsstatus.

Att lämna teknisk-kartlaggning-28-tariffer.md oförändrad godtas: filen avser den äldre
27+1-kartläggningen, inte den nuvarande dispositionsmängden. Den daterade §8a-matrisen
är rätt plats för denna normalisering. Inget nytt Robert-beslut behövs för rättningen.

## Oberoende verifiering

- JSON läses; 86 fysiska rader och deras ID:n är oförändrade. Jämförelse mot e1f532c
  visar oförändrade energy/capacity/production_ready/contract_required/price_status
  och investigation.status för samtliga rader.
- §8a har mekaniskt 28 rader: 22 source_resolved_implementation_pending och
  6 external_answer_required. Detta bevisar antal, inte att kataloggrinden fungerar.
- `git diff --check HEAD^ HEAD` är rent.
- Systemets python3 saknar pytest. Omkörning med produktrepots `.venv/bin/python`:
  `-m pytest tools/tariffer/tests/test_katalog.py tools/tariffer/tests/test_katalog_oversattning.py tools/tariffer/tests/test_katalog_proveniens.py tools/tariffer/tests/test_dispositionsgrind_inventering.py -q`
  gav **13 failed / 40 passed**. Fel: sju i test_katalog, tre i
  test_katalog_oversattning, ett proveniensfel och två i dispositionsgrinden.
- Ett rent in-memory-prov (ingen fil ändrad) gav 60 godkända fysiska rader efter
  borttagning av dubbla scopefält och 61 först när R17 också togs ur den fysiska listan.
  Påståendet att den fungerande skarpa produktmängden bevisats oförändrad godtas därför
  inte för leveransen, trots att dokumentets 62/2/28 och statusfälten är oförändrade.

## Nästa handlingsbara signal

`CHANGES_REQUIRED: Claude`

Rätta endast de ovan avgränsade skills-underlagen och loggarna. Verifiera 28 unika
identiteter mot den frusna dispositionsmängden, 22+6, fyra fysiska frågor plus R17 för
varianten, 86 katalograder, 61 godkända fysiska rader och oförändrad 62/2/28-disposition.
Kör de befintliga grindarna och redovisa varje kvarstående fel med orsak; påstå inte
full grön verifiering innan proveniens-/synkfrågan är hanterad i separat steg.
Committa rättningen och en ny unik REVIEW_READY: Codex med verifierade HEAD:ar och
faktiska testutfall. Stanna där. Ingen Vattenfall-implementation, aktivering, push,
historikomskrivning eller ändring av protokoll/automation ingår.
