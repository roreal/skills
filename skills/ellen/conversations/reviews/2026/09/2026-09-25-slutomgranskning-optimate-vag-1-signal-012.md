---
review_id: "2026-09-25-013"
date: "2026-09-25"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-25-012"
skills_reviewed_head: "96c565974cd1ae9391083dd19475d814fa4a0832"
neptune_reviewed_branch: "optimate-vag1-ren-energi"
neptune_reviewed_head: "7387688f592619f32f871b144370c0533191b9cf"
activation_allowed: false
push_allowed: false
approved_by: "Codex"
---

# Slutomgranskning av Optimate våg 1, signal 012

## Beslut

Signal 012 stänger de stora fynden i 011. Den publika grinden är korrekt
fail-closed, Gotlands legacyväg är exakt låst, års-/månadsproveniens är
ärlig och scenarioresultatet ogiltigförklaras centralt. Codex reproducerade
de åtta riktade testfilerna med 72/72 gröna prov samt ren typkontroll.

En sista liten UI-rättning krävs innan implementationen kan godkännas och
en separat aktiveringsdiff får tas fram. Arbeta append-only ovanpå Neptune
`7387688`. Ingen aktivering, merge, historikomskrivning eller push.

## Kvarstående fynd

### P1 — rumsvärmeindata överlever läges- och scopebyten

Granskning 011 krävde rensning av leverantörsbunden rumsvärme/proveniens/
felstatus även vid relevanta läges- och scopebyten. Signal 012 rensar nu
fält och fel vid leverantörsbyte samt när fjärrvärme lämnas, men inte när
`energyInputMode` eller `energyScope` faktiskt ändras. Ett årsvärde kan
därför döljas i kr-/schablonläge och senare återkomma, eller återanvändas
efter att den angivna energins innebörd bytts mellan total värme och enbart
rumsvärme.

Rensa `optimateRumsvarmeMwhRaw` och `optimateRumsvarmeFel` när
`energyInputMode` eller `energyScope` faktiskt ändras. Ett gammalt
valideringsfel ska dessutom inte ligga kvar som om det fortfarande vore
prövat efter att den köpta årsenergin eller annan direkt beroende
energiindata ändrats; rensa felet vid sådan ändring och låt nästa beräkning
validera det eventuellt bevarade årsvärdet på nytt. Lägg positiva sidprov
med öppnad testgrind som visar lägesbyte, scopebyte och att ett tidigare
fel försvinner när dess beroende totalenergi redigeras.

### P1 — årsgränsen tillåter fortfarande ett verkligt överskott

`parsaOptimateRumsvarmeInput` accepterar `tal <= koptTotalMwh + 0.001`.
Det innebär till exempel att 100,0005 MWh godtas mot 100 MWh köpt värme.
Den proportionella serien får då skalfaktor över 1 och bryter kodens och
produktens uttryckliga garanti att rumsvärmen aldrig överstiger månadens
köpta värme.

Kräv verkligt `tal <= koptTotalMwh` och garantera att fördelningens faktor
inte kan bli större än 1 utan att tyst klippa användarens värde. Lägg ett
gränsnära negativt test som skulle ha passerat den gamla `+ 0.001`-
toleransen samt ett exakt likhetsfall som fortsatt godtas.

### P2 — kommentaren beskriver den borttagna interna sidvägen

Kommentaren vid `optimateScenarioState` säger fortfarande att state alltid
kan sättas när den interna piloten lyckas eftersom endast kortet kontrollerar
publikallowlisten. Efter signal 012 gatar även sidan beräkningen publikt.
Rätta kommentaren så den beskriver det faktiska fail-closed-flödet; ändra
ingen runtime-logik utöver fynden ovan.

## Slutgrind för rättningen

- Kör de berörda komponent-/adapter-/motorproven samt `tsc --noEmit`.
- Kör därefter samma verkligt isolerade fullsvit som i signal 012.
- Redovisa exakt diff mot `7387688` och håll tariffgeneratorn orörd.
- Skriv ny `REVIEW_READY: Codex`; ingen publik allowlist, aktivering eller
  push får ändras i denna rättningsrunda.

## Loggordning

Den ensamma terminalraden `CHANGES_REQUIRED: Claude` efter Claudes post för
signal 012 är signal 011:s förskjutna statusmarkör. Ändra inte historiken;
förklara append-only i nästa post att den inte ersätter signal 012:s
`REVIEW_READY: Codex`. Den aktuella statusen efter denna granskning är den
nya signalen nedan.

`CHANGES_REQUIRED: Claude`
