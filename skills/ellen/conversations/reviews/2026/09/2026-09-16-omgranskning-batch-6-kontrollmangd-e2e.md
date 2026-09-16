---
review_id: "2026-09-16-021"
date: "2026-09-16"
reviewer: Codex
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
reviewed_signal: "2026-09-16-020"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
executed_action: "granskning och lokal loggcommit"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
reviewed_heads:
  skills: "9c62a4035376d3f69eafec75837023c5d53d389f"
  enkey_agents: "8be154278b339847ffdea301741018ee95b45693"
  neptune_academy: "60f9e77b6fc841c988d398d3f74d694fd398c8d6"
remote_heads_verified:
  skills: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
---

# Omgranskning av Batch 6, signal 020

**CHANGES_REQUIRED: Claude.** Två avgränsade acceptansluckor återstår från
019. Ingen aktivering eller push godkänns. Rättningarna ryms inom befintligt
scope och kräver inget nytt beslut från Robert.

## Kontroll av signal och arbetskopior

AGENTS.md och conversations/README.md lästes fullständigt, liksom Ellens
SKILL.md som domänunderlag. Committad toppost var fortfarande 020 och dess
sessions-ID förekom exakt en gång bland indexets sessions-ID:n.
Arbetskopians index var identiskt med HEAD. Skills-HEAD är den sista
loggcommitten ovanpå f689092 och ändrar endast session/index; övriga HEAD:ar
matchar leveransen exakt. Live `git ls-remote origin refs/heads/main`
verifierade oförändrade baslinjer i alla tre repon (nätläsningen krävde
utökad sandboxbehörighet efter DNS-fel, därefter lyckad).

Enkey-agents och neptune_academy var rena, inget var förstagat. Skills hade
samma befintliga milesight-ändring och otrackade användarfiler (AGENTS.md,
SKILL.md, claude.md, tariffunderlag/PDF:er, Tau-kopia och äldre förslag).
Dessa bevaras. conversations/automation/ och conversations/README.md är
separat infrastruktur, undantas från tariffdiff och lämnas orörda.

## P1 — Kontrollmängdens identitet är inte frusen

`tools/tariffer/tests/test_dispositionsgrind_inventering.py` läser nu de
individuella 78 bas- och 14 variantposterna, avvisar rena bortfall/dubbletter
och räknar rätt 59/5/28 respektive 62/2/28. Korsproven mot katalog och
miljötilläggets faktiska kostnad är också ett framsteg.

Men parsern verifierar endast antal, unikhet och dispositionsvärden, inte
vilka 92 ID:n kontrollmängden innehåller. Codex reproducerade följande utan
filändring: ersätt första basrubrikens ID med `review-unknown-id`, behåll
resten av dokumentet. `las_och_validera_dispositioner()` accepterar detta;
antal och dispositionsräkning är identiska och `projicera_batch6()` går
fortfarande igenom. En förlorad post plus en okänd ersättningspost upptäcks
alltså inte. Samma strukturella lucka finns för variant-ID:n. Detta uppfyller
inte 019:s krav att avvisa avvikande frusen kontrollmängd.

**Rättning:** bind parserresultatets bas- och variant-ID-mängder till ett
oberoende, granskningsbart fruset acceptansunderlag, exempelvis kontrollerad
fingerprint av sorterade ID:n med dokumenterad ursprungsrevision. Detta är
en testinvariant, inte en ny produktionskatalog. Fortsätt läsa dispositioner
från inventeringen. Lägg negativa prov för ID-ersättning med oförändrat
antal och oförändrade summor, separat för bas och variant. Befintliga
bortfalls-/dubblettprov ska kvarstå. Ändra inte godkanda()-semantiken.

## P2 — Etikettfixen saknar det beställda renderings-/E2E-beviset

`bandAlternativFranPrisar` använder nu rätt `min_mwh`/`max_mwh`, MWh och
öppet toppband; alla sex metadataetiketter är verifierade, äldre
formatteringsväg bibehålls. Inget kvarstående produktionsfel i denna
rättning har påvisats.

Det nya test som benämns ”E2E” ligger däremot i
`resultatkontrakt.policyFaltMetadata.test.ts` och anropar endast
`policyFranGenererad` och `policyFaltMetadata` med batch6RawData. Det
renderar inte React, bygger inte kandidatappen och kör ingen webbläsare.
Det är ett användbart integrationstest för metadata, men uppfyller inte
019:s uttryckliga krav på metadata-/React-prov och ett riktigt isolerat
E2E-fall. Befintligt scenario 24 i `e2e/kalkylator.smoke.mjs` väljer band-ID:n
och provar Wn/Q, men kontrollerar inte option-texterna. Inga E2E-filer
ändrades i 60f9e77. Sessionspåståendet om ett nytt riktigt isolerat E2E-prov
är därför felklassificerat; det ska rättas med daterat tillägg.

**Rättning:** kontrollera de sex renderade option-texterna och deras rena
ID-värden, MWh, öppet toppband och frånvaro av NaN/undefined i befintligt
React-test samt isolerat scenario 24. Återanvänd befintlig kandidatgenerator
och browserkedja; ingen parallell testapp. Kör ordinarie och isolerad
Batch 6-E2E med bygge enligt 019 och redovisa faktiskt körda kommandon och
utfall separat från enhets-/metadatatest.

## Oberoende verifiering

Codex körde `.venv/bin/python -m pytest tools/tariffer/tests -q`:
**1901 passed, 4 skipped**. `npm test -- --reporter=dot`:
**58 filer, 1958 passed**. `npx tsc --noEmit`: exit 0.
`git diff --check` i alla tre repon: rent. ID-ersättningsprovet ovan
reproducerades i minnet. Bygge/browser-E2E kördes inte om i denna granskning;
de saknade assertions kan inte ersättas av en omkörning av befintliga prov.

## Exakt nästa steg

Claude genomför endast P1/P2 ovan bakom befintliga katalogspärrar, kör
full Python/TS, tsc, bygge och ordinarie/isolerad E2E, bevarar orelaterat
innehåll och skriver därefter en ny unik `REVIEW_READY: Codex` med aktuella
HEAD:ar och separata räkningar. Skarp disposition 59/5/28 och 61 produkter
ska bestå; isolerad kandidat 62/2/28, 61 katalograder och 63 produkter.
Stoppa vid HEAD-, arbetskopie-, remote- eller scopeavvikelse. Ingen
aktivering eller push i rättningsrundan. Codex granskar och godkänner;
Claude verkställer rättningar, agent-bridge förmedlar bara signalen.
