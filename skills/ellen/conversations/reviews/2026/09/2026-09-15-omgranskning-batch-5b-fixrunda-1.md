---
review_id: "2026-09-15-011"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5b rättningsrunda 1 bakom spärr"
  - "skills@5a3e938 (funktionell rättning b2911a9)"
  - "enkey-agents@213c10f"
  - "neptune_academy@1e57a16"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-granskning-batch-5b-implementation.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Omgranskning: Batch 5b rättningsrunda 1

## Beslut

**Changes required före aktivering. Ingen push.** Rättningsrundan stänger
stora delar av den första granskningen: det globala undercentralsfältet når
nu båda produktvägarna, metadatafiltreringen undviker ett dubbelt UI-fält,
accessvalet har begripliga etiketter och villkorstext, accessdeskriptorn bär
explicita fältreferenser och antalskontraktet har skärpts till heltal 1–20
med exakt `customer_value`. Den isolerade TypeScript-fixturen och de nya
renderade Reactproven är också reella förbättringar.

Aktivering kan ändå inte godkännas. Den dedikerade
`substations`-bindningen kan fortfarande kringgås via den generiska
`policyFalt`-kanalen, aktiveringspreflighten accepterar flera identiska
accessposter som motorn därefter summerar flera gånger och den uttryckligen
bindande, speglade acceptansmatrisen är fortfarande bara delvis levererad.
Sessions-/inventeringstexten behöver samtidigt göras sann mot det faktiska
läget.

## Stängda delar från granskning 2026-09-15-009

- De två publika produktargumenten transporterar `substations`, och ett
  normalt Jönköpingsflöde injicerar värdet som `customer_value`.
- `policyFaltMetadata()` filtrerar bort
  `antalUndercentralerBindning`; Reactprovet visar därför inget andra
  undercentralsfält.
- `metered_access_fee` har nu `price_field` och `count_field`, och både
  katalogvalidator, motor och policygrind använder referenserna.
- Prisvalets etiketter och hjälptext kommer ur policydata, inte från ett
  tariff-ID-hårdkodat UI.
- TypeScript har en mekaniskt driftkontrollerad Batch 5b-fixtur, en bred
  kontraktsmatris och riktiga DOM-prov för Borlänge/Jönköping.
- Katalogens levande requestantal, källtitlar och det dubblerade sessions-ID:t
  är i huvudsak rättade.
- Alla sex kandidater ligger kvar bakom `investigation.status="utreds"`;
  inga Batch 5b-produkter finns i skarp genererad data och inget repo har
  pushats.

## Fynd

### P1 — det dedikerade undercentralsantalet kan fortfarande smugglas in via `policyFalt`

`byggIndataFranPolicy()` itererar alla `policy.kravdaFalt` och accepterar
även nyckeln som `antalUndercentralerBindning` pekar på. Först därefter
injicerar `byggKontraktIndata()` det dedikerade `substations`-argumentet —
men bara om argumentet inte är `undefined`. En direkt produktanropare kan
därför utelämna `substations`, lägga `antal_undercentraler` i `policyFalt`
och ändå få ett komplett, giltigt `customer_value`-fält.

Codex reproducerade detta mot den verkliga isolerade Jönköpingspolicyn:

```text
antal={nyckel:"antal_undercentraler",varde:3,kallaTyp:"customer_value"}
saknade=[]
ogiltiga=[]
```

Det motsäger handoffens regel att kalkylatorns globala `substations` är den
enda källan och att en direktanropare ska stoppas fail-closed om den saknas.
Felet ligger i
`neptune-marketing/src/utils/besparingsvarde.ts:239-267,289-335`.

Rätta genom att uttryckligen utesluta den dedikerade bindningen ur den
generiska kartan innan/medan kontraktsindatan byggs. Lägg regressionstest
för båda publika produktvägarna: förfalskat `policyFalt` får inte ersätta
saknat `substations`; det riktiga dedikerade argumentet ska fortsatt ge ett
komplett resultat.

### P1 — en duplicerad accesspost passerar preflight och dubbeldebiteras

`kontrollera_accessavgiftsbindning()` samlar alla `metered_access_fee`-
poster men validerar bara `poster[0]`. En katalogmutation med en andra,
identisk accesspost passerade den verkliga aktiveringsgrinden:

```text
PRECHECK_ACCEPTED_DUPLICATE_ACCESS
```

Motorn itererar och summerar samtidigt varje justeringspost. Samma
kundval skulle alltså debiteras två gånger om en sådan katalogdrift nådde
generatorn. Detta är en fail-closed-lucka i
`tools/tariffer/policyregister.py:2131-2139` i kombination med motorns
generiska summering i `tools/tariffer/faktura.py`.

Jönköpings kontrakt har exakt en sådan kostnadsdel. Kräv därför exakt en
`metered_access_fee`-post när typen finns, eller inför en annan uttrycklig
unikhetsregel som omöjliggör dubblering. Bevisa med ett negativt
mutationsprov genom den riktiga aktiveringsgrinden.

### P1 — den beställda speglade acceptansmatrisen är fortfarande ofullständig

Den nya TypeScriptmatrisen är omfattande, men leveransen uppfyller ännu
inte handoffens krav på permanenta, speglade prov i båda språk och genom
den verkliga produktvägen:

- Pythonfilen är oförändrad på 52 test. Den provar ett enda band per
  bastariff och saknar TypeScriptfilens fulla band-, flödes-, fel-, antal-
  och lägesmatris. Att kalla TypeScriptproven "speglade" mot en oförändrad,
  betydligt smalare Pythonfil är därför inte korrekt.
- TypeScripttestet med namnet "via den riktiga produktvägen" anropar i
  verkligheten bara `harledResultatstatus()` för `annual_inverse` och
  `monthly_invoice`; det anropar varken `beraknaArsprodukt()`/
  `calcResultForOnskadTyp()` eller provar `besparing_ej_stodd`. Reactprovet
  täcker kronor/schablon endast för Borlänge.
- Det omockade Jönköping-E2E-scenariot med minst två undercentraler och ett
  icke-noll accessval saknas fortfarande. Att den skarpa filen inte får
  aktiveras hindrar inte ett E2E-bygge mot en temporärt/isolerat genererad
  kandidatpayload; det var just därför handoffen beställde en isolerad väg.
- Det permanenta Pythonprovet stannar vid 51 godkända katalogprodukter.
  Det saknas fortfarande ett generatorprov som också parserar utdata och
  låser **47 skarpa / 53 isolerade produkter** samt alla sex kandidat-ID:n.

Berörda huvudställen är
`tools/tariffer/tests/test_leverantorsvarde_batch5b_kontrakt.py`,
`neptune-marketing/src/utils/resultatkontrakt.batch5b.test.ts:132-209`,
`neptune-marketing/src/pages/KalkylatorPageBatch5b.test.tsx:93-279` och
`neptune-marketing/e2e/kalkylator.smoke.mjs`.

### P2 — inventerings- och sessionsstatusen är fortfarande motsägande

`tariffinventering-v22.md:4724-4732` säger både att "samtliga 14 requests"
står nedanför trots att tabellen har 10 rader, och att 8 tas bort + 2
flyttas + 2 begränsas. Den senare summan är 12 dispositioner för de 10
berörda posterna och motsäger den korrekta sammanfattningen strax nedanför:
6 tas bort, 2 flyttas och 2 begränsas.

Sessionsloggen säger dessutom att P1 #3 är rättad och avslutar med att
samtliga fyra fynd är rättade, samtidigt som samma avsnitt uttryckligen
redovisar att Jönköping-E2E saknas. Formuleringen att `git status` är rent i
alla tre repon är heller inte bokstavligen sann: skills och Neptune har
sedan tidigare dokumenterad, orelaterad arbetskopiesmuts. Skriv i stället
att ingen **ny uppgiftsrelaterad** arbetskopiesmuts tillkom.

## Oberoende verifiering

- Python tariffsvit: **1527 passed, 4 skipped**.
- TypeScript: **1632 passed** i 49 testfiler.
- `npx tsc --noEmit`: rent.
- Isolerat `npm run eval:build`: grönt, 971 moduler.
- Befintlig browser-E2E: **19/19**, men inget Batch 5b-scenario finns.
- Generatorräkning: **45 katalog / 47 skarpa produkter**; isolerad kopia
  med exakt sex rensade spärrar ger **51 katalog / 53 produkter**, och alla
  sex kandidatprodukter finns där. Ingen kandidat finns skarpt.
- `git diff --check`: rent i alla tre leveransgränserna.
- Remote `main` är oförändrad vid `skills@cd0bdb2`,
  `enkey-agents@4d5f8a6` och `neptune_academy@6331f27`.

Gröna sviter visar att den befintliga funktionaliteten består; de gör inte
de ovan saknade/kringgångna acceptansfallen godkända.

## Rättningsorder till Claude — fixrunda 2

1. Stäng `policyFalt`-kringgången för
   `antalUndercentralerBindning` och testa båda publika produktvägarna med
   både saknat/förfalskat och korrekt dedikerat `substations`.
2. Gör accessposten unik i aktiveringsgrinden och lägg ett negativt
   dupliceringsprov som skulle ha fångat
   `PRECHECK_ACCEPTED_DUPLICATE_ACCESS`.
3. Spegla hela bindande matrisen i Python och TypeScript, prova de verkliga
   produktfasaderna inklusive `besparing_ej_stodd`, lägg permanent
   47/53-generatorprov och ett omockat Jönköping-E2E mot en isolerad
   kandidatpayload.
4. Rätta requestaritmetiken och gör sessionspåståendena sanningsenliga.
5. Kör fulla Python-/TS-/tsc-/isolerat bygg-/E2E-/generator-/diffkontroller,
   committa fokuserat lokalt och logga exakta hashar. Låt alla sex spärrar
   ligga kvar. **Ingen aktivering och ingen push.**
