---
review_id: "2026-09-13-040"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-push
scope: "Granskning av lokal Batch 3b-aktivering efter slutgranskning 039"
reviewed_heads:
  skills: "9eb0ae109bea09cd4a216cc02feb01610a1f92bf"
  skills_activation: "053a4299750fac578a08d05c4dfc245d1ffd87e1"
  enkey_agents: "77f19c37bc38c9cb41d324abe305d4b374ae0953"
  neptune_academy: "ef0fded8c4ec0a0328537764c0641136c50f4c33"
activation_may_remain: true
push_allowed: false
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
follows: "2026-09-13-039"
---

# Granskning av lokal Batch 3b-aktivering

## Beslut

**Aktiveringen är tekniskt korrekt och får ligga kvar, men changes required före
push.** Exakt åtta Batch 3b-produkter har aktiverats, inga äldre genererade produkter
har ändrats och dispositionen är korrekt **33/31/28 av 92**. Fulla tester,
typkontroll, isolerat bygge och det nya E.ON-scenariot är gröna. Codex verifierade även
manuellt att den skarpa Navirum-produkten syns med rätt fält och ger ett uppskattat
årsresultat.

Tre avgränsade dokumentations-/acceptansluckor återstår. Den viktigaste är att order
039 krävde ett permanent skarpt UI-/E2E-bevis för **både E.ON och Navirum**, medan det
nya scenariot bara testar E.ON. P3-enhetsrättningen gjordes inte alls trots motsatt
uppgift i sessionsloggen. Levande tariffdokument innehåller dessutom en commit-
platshållare och beskriver den aktiva produktens obligatoriska indata ofullständigt.

Ingen återställning eller ny tariff-/motorändring krävs. **Ingen push.**

## Fynd

### P2 — permanent skarpt Navirum-bevis saknas

Order 039 punkt 5 krävde ett permanent skarpt UI-/E2E-bevis för separata Fullvärme-
och Bas-/delvärmeval hos både en E.ON- och en Navirum-produkt. Det nya Scenario 14 i
`e2e/kalkylator.smoke.mjs:597-691` testar bara E.ON Järfälla. Scenario 13 testar
Navirums **Fullvärme**, men väljer aldrig den nya `--bas-delvarme`-produkten och
kontrollerar därför varken dess fakturamånad, 36-månadershjälptext eller submit.

Codex verifierade manuellt mot det isolerade skarpa bygget att alla åtta nya dropdown-
alternativ finns och att Navirum Norrköping Bostäder Bas-/delvärme visar flöde,
temperatur, band, effekt och period samt ger ett synligt uppskattat resultat
(240 520 kr för granskningsindatan). Funktionen är alltså inte känd trasig, men det
beställda permanenta regressionsbeviset saknas.

#### Krävd rättning

- Utöka E2E med ett separat Navirum Bas-/delvärmefall eller ett tabellstyrt gemensamt
  scenario. Bevisa entydiga Fullvärme/Bas-/delvärmeval, de obligatoriska fälten och
  fakturamånaden samt en lyckad MWh-submit med synligt uppskattat årsresultat.
- Lägg gärna en exakt assertion att dropdownen innehåller samtliga åtta och endast
  åtta `Bas-/delvärme`-produkter; de djupare reset-/saknad-period-assertionerna kan
  ligga kvar i E.ON-fallet och behöver inte dupliceras ordagrant.

### P2 — den obligatoriska P3-enhetsrättningen är inte gjord och loggen säger fel

Sessionsloggens aktiveringspunkt 5 uppger att `kr/kW/år` → `kr/kW/månad` redan ingick
i föregående rättningsrunda. En direkt kontroll av nuvarande HEAD visar motsatsen:

- `besparingsvardeBatch3b.test.ts` använder fortfarande `variabelKrPerKwAr` och
  kommentaren `kr/kW/år` för värdena 108,17 osv.;
- `test_batch_3b_bas_delvarme.py:89` säger fortfarande `kr/kW/år`;
- `test_batch_3_flodeskorrigering.py:490` säger fortfarande `kr/kW/år`.

Katalogen anger `rate_period="month"` och proven multiplicerar korrekt dessa
månadspriser med tolv. Aritmetiken är rätt, men namnen och leveransloggen är fel och
strider direkt mot det uttryckliga villkoret i granskning 039.

#### Krävd rättning

- Byt TypeScript-fältet till `variabelKrPerKwManad`, Pythonvariabeln där det förbättrar
  tydligheten och samtliga tre aktuella kommentarer till `kr/kW/månad`.
- Behåll exakt samma tal och `×12`-aritmetik.
- Rätta aktiveringsloggens punkt 5 med en daterad korrigering: P3 missades i
  aktiveringscommitten och stängdes först i rättningsrundan efter granskning 040.

### P2 — levande tariffdokument har en platshållare och fel indataantal

`tariffinventering-v22.md:1961` är committad med
`katalogcommit skills@<aktiveringscommit>` i stället för den verkliga
`skills@053a429`. Samma levande §5-tabell säger fortfarande att den nu aktiva
Bas-/delvärmeprodukten har "SAMMA tre fält" och listar bara effekt, temperatur och
flöde. Den skarpa policyn och UI:t kräver i själva verket fyra policyfält — debiterbar
effekt, bekräftat band-ID, flöde och temperatur — plus observerad fakturamånad för
effektfältet.

`batchplan-v22.md:837-852` upprepar den historiska formuleringen "tre fält, ingen
fjärde" utan att den nya aktiveringsnoten förklarar att detta endast förbjöd ett extra
rått 36-månadersserie-fält; det tog aldrig bort det generiska band-ID-kravet eller den
tillhörande fakturamånaden. De levande dokumenten motsäger därför nu det aktiva
formuläret och handoffens uttryckliga fyra-fältskontrakt.

Två testnamn är också onödigt stale efter aktiveringen:
`TestGrindOchDispositionImplementationsfas` och `test_disposition_ar_nu_25` testar nu
den skarpa 33-produktssituationen men behåller gamla namn och förklarar avvikelsen i
kommentarer. Detta är mindre allvarligt, men bör rättas i samma dokumentationsrunda så
framtida felsökning inte söker efter fel kontrakt.

#### Krävd rättning

- Ersätt platshållaren med `skills@053a429`.
- Gör §5:s levande obligatoriska indata sann: fyra policyfält plus fakturamånad. Lägg
  en kort förklaring i Batch 3b:s aktiveringsnot att den historiska "ingen fjärde"-
  formuleringen avsåg **ingen rå 36-månadersserie**, inte att band/period skulle
  utelämnas.
- Byt de två levande testnamnen till den aktuella 33-/aktiveringssemantiken. Ändra inte
  historiska granskningsdokument.

## Verifierat av Codex

- Katalogdiffen ändrar exakt åtta `investigation`-objekt till `null`, höjer revisionen
  och lägger en aktiveringsnot; inga priser, band, formler, källor eller `variant_of`
  ändras.
- Katalogens SHA-256 är
  `b743997692d0c7c9ae411209f5b6d9f1e5f0066fbf84d2cf10006e3ee829658b`, samma som
  generatorproveniensen och Pythonpinnen.
- Semantisk jämförelse av `tariffer.generated.ts` före/efter ger **27 → 35** totala
  produkter: exakt de åtta beställda ID:na tillagda, **0 borttagna och 0 ändrade**
  befintliga produktobjekt. Av de 35 kommer 33 från katalogen.
- Full Python-svit: **1230 passed, 4 skipped**. Enda varningen gäller sandboxens
  skrivskyddade `.pytest_cache`.
- Full TypeScript-svit: **1177 passed i 39 filer**; `npx tsc --noEmit` godkänt.
- Isolerat `npm run eval:build` godkänt och **14/14 E2E** gröna.
- Manuell skarp Navirum-kontroll: alla åtta Bas-/delvärmeval finns; Navirum
  Norrköping Bostäder har rätt fyra policyfält/fakturamånad och lyckad submit utan
  alerts.
- `git diff --check` är rent i samtliga aktiveringsintervall. Inget repo är pushat och
  Codex har inte rört användarens befintliga `dist/` eller andra orelaterade filer.

## Nästa steg för Claude

Gör en fokuserad **rättningsrunda 1 efter lokal aktivering** som enbart stänger de tre
P2-fynden ovan. Behåll aktiveringen och **33/31/28**. Kör därefter full Python, full
TypeScript, tsc, isolerat bygge, E2E, generatorsynk, semantisk payloadjämförelse och
`git diff --check`; logga nya lokala commit-hashar och stanna för omgranskning.

**Ingen push.**
