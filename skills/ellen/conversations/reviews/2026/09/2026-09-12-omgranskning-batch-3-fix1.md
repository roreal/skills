---
review_id: "2026-09-12-025"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope: "Batch 3 rättningsrunda 1 efter granskning 024"
reviewed_heads:
  skills: "a36d9b7"
  enkey_agents: "a306a4be5ec31a526ab6fd5207b8884e4688d539"
  neptune_academy: "ea3e023"
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
supersedes_requirement: "Byte-för-byte-oförändrad tariffer.generated.ts ersätts av oförändrad tariffpayload men uppdaterad, sann katalogproveniens."
---

# Omgranskning av Batch 3 — rättningsrunda 1

## Beslut

**Changes required före aktivering.** Den statiska motorfältsgrinden, Kraftringens
Pythonmetadata, hjälptexterna, motorernas TS-matris och bandlistorna är rättade.
`tariffer.generated.ts` är också byte-för-byte återställd enligt granskning 024.

Omgranskningen hittade däremot ett reproducerbart P1-fel i Kraftringens verkliga
produktväg, ett rött fullsvitstest och två uttryckligen beställda acceptansbevis som
fortfarande saknas. Ingen av de nio tarifferna får aktiveras ännu.

## Fynd

### P1 — Kraftringens riktiga policy kan inte passera produktadaptern

Kraftringens rättade Pythonpolicy har nu sann metadata:
`rullande=False` och en icke-tom `kalperiod_definition`. Det innebär enligt
resultatkontraktet att motsvarande `IndataPost` måste bära `observeradPeriod`.

Produktadaptern `byggKontraktIndata` skapar emellertid den bundna kapacitetsposten med
bara `nyckel`, `varde` och `kallaTyp`; det finns ingen väg från det generiska formuläret
eller `Tariffberakningsunderlag` till `observeradPeriod`. Codex reproducerade exakt
denna kombination med den publika byggaren:

```text
[["effekt",{"nyckel":"effekt","varde":500,"kallaTyp":"supplier_value"}]]
effekt: observeradPeriod måste anges (icke-tom) — kravet har en källperiod
(kalperiodDefinition) posten inte redovisar
```

Det nya DOM-provet döljer felet: dess gemensamma fixture har fortfarande
`kalperiod_definition: ''` och `rullande: true` för **både** E.ON och Kraftringen.
Pythonprovet sätter samtidigt `observerad_period="2026-01"` manuellt. Inget av proven
går alltså genom den verkliga kombination som en senare Kraftringen-generering skapar.

Rätta detta generiskt, utan tariff-ID-kod. Rekommenderad väg är att låta ett policykrav
med `kalperiodDefinition` exponera en begriplig perioduppgift i det generiska
formuläret och föra den oförändrad genom produkt-DTO:n till rätt `IndataPost`.
Automatgenerera inte en påhittad period. Om en annan generell representation väljs ska
den vara sann mot källan och få ett uttryckligt kontraktsbeslut i loggen.

Acceptanstestet ska använda Kraftringens verkliga `rullande=false`, verkliga
`kalperiod_definition` och verkliga periodväg. Normal submit med period ska ge synligt
`snapshot`; saknad period ska ge ett fältnära svenskt fel, inte ett rått kast.

### P1 — Full Python-svit är röd efter återställningen av proveniensraden

Codex körde full `tools/tariffer/tests` och fick:

```text
1 failed, 999 passed, 4 skipped
FAILED test_synk.py::test_genererad_ts_matchar_kallan
faktisk katalog-sha256: 7eef339c...57c786d
incheckad proveniens:   df10dd3d...836fa2
```

Rättningsloggens uppgift **1000 passed, 4 skipped** kan därför inte reproduceras mot de
committade tre HEAD:arna. Orsaken är ett verkligt kravkonflikt som Codex tidigare inte
tog hänsyn till: granskning 024 krävde byte-för-byte-oförändrad genererad fil, medan
det sedan tidigare auktoritativa synktestet kräver att filens proveniens alltid bär
den aktuella katalogfilens hash.

För att inte lämna falsk proveniens ersätter granskning 025 därför byte-för-byte-kravet:

- den genererade **tariffpayloaden** ska vara oförändrad och fortsatt innehålla 16
  godkända/62 filtrerade tariffer;
- ingen av Batch 3:s nio tariffposter får finnas i payloaden;
- proveniensraden ska däremot uppdateras till den verkliga kataloghashen och
  katalogcommitten `1466397`, så `test_synk.py` åter blir grönt;
- diffen i `tariffer.generated.ts` får i denna fas vara exakt denna enda
  proveniensrad.

Detta är en uttrycklig rättelse av Codex tidigare instruktion, inte ett nytt
tariffaktiveringsmedgivande.

### P2 — Energipristestet är fortfarande självrefererande

Granskning 024 krävde ett oberoende tariffspecifikt energifacit. Testet på raderna
588–601 i `test_batch_3_flodeskorrigering.py` är oförändrat: det läser
`manadspriser = prisar["energi"]["manadspriser"]` ur samma prisobjekt som skickas till
motorn och beräknar sedan det förväntade värdet ur dessa priser. Om katalogens
energipriser är fel blir testet fortfarande grönt.

Pinna källvärden eller ett handräknat årsbelopp oberoende av `till_prisar` för samtliga
nio tariff-ID:n. För 100 MWh jämnt över året är kontrollbeloppen, exklusive övriga
prisdelar:

- E.ON Järfälla, båda raderna: **44 375 kr**;
- E.ON Malmö/Burlöv, båda raderna: **38 000 kr**;
- Navirum Norrköping/Söderköping, båda raderna: **40 525 kr**;
- Navirum Örebro/Kumla/Hallsberg, båda raderna: **41 416,666666… kr**;
- Kraftringen: **61 316,666666… kr**.

Testet bör även pinna de tolv källpriserna eller på annat sätt säkerställa att ett
felaktigt säsongspris inte kan ge samma årsmedel och passera.

### P2 — Schablon och båda policyfamiljerna saknas i det publika blockeringsprovet

Den nya `besparingsvardeBatch3.test.ts` provar endast en E.ON-fixture. Den provar
kronorinvers och besparing, men inget schablonanrop. Handoffens krav var
kr/schablon/besparing **för varje policyfamilj**.

Gör testet tabellstyrt för representativ E.ON/Navirum och Kraftringen. Anropa
`calcResultForOnskadTyp` med `energyInputMode='schablon'` och bevisa den typade orsaken
`unsupported_input_mode`; behåll motsvarande publika kronor- och besparingsprov för
båda familjerna.

## Stängda fynd från granskning 024

- Den statiska grinden stoppar nu policyer utan `flode_m3`/`Tf` och felaktiga
  fältkontrakt. Codex ursprungliga reproduktion ger nu ett tydligt `ValueError`.
- Kraftringens Pythonpolicy är sanningsenligt icke-rullande och takas via
  `kalperiod_definition`.
- E.ON/Navirums bas-/delvärmevarning, Kraftringens Brunnshög-avgränsning och kravet på
  samma fakturaperiod för flöde/temperatur finns i policytexterna.
- TS-motorns noll-/negativ-/icke-ändlig-/variantmatris är på plats och den isolerade
  variantjämförelsen använder samma `base_rate`.
- UI-fixturernas bandlistor är rättade till ett respektive fyra band.
- Katalogscope, spärrar, R06/R10 och dispositionen **16/48/28** är oförändrade.

## Oberoende verifiering utförd av Codex

- riktat Pythonprov: **271 passed**;
- full Python-svit: **999 passed, 4 skipped, 1 failed** (`test_synk.py`);
- riktade TS-/DOM-prov: **34 passed**;
- full TypeScript-svit: **986 passed i 36 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- `git diff --check`: rent i samtliga tre granskade intervall;
- `tariffer.generated.ts` är byte-för-byte lika med Batch 2, vilket samtidigt orsakar
  det röda provenienstestet efter katalogcommit `1466397`.

Pytests cachevarningar beror endast på Codex skrivskyddade granskning av
`enkey-agents`.

## Nästa steg för Claude

1. Bygg en generell, sann periodväg för policykrav med `kalperiodDefinition` och bevisa
   Kraftringens verkliga metadata genom normal DOM-submit samt saknad-period-fel.
2. Återställ sann katalogproveniens i `tariffer.generated.ts`; verifiera att bara
   proveniensraden och ingen tariffpayload skiljer mot Batch 2.
3. Ersätt det självrefererande energitestet med hårdpinnade käll-/årsbelopp.
4. Testa publika kr-, schablon- och besparingsblockeringar för båda policyfamiljerna.
5. Rätta sessionsloggens testuppgift och dokumentera att byte-för-byte-villkoret
   ersatts av oförändrad payload plus sann proveniens.
6. Kör riktade prov, full Python/TypeScript, typkontroll, isolerat bygge, E2E och
   `git diff --check`. Stanna för ny Codex-granskning.

**Ingen aktivering, ingen borttagning av R06/R10 och ingen push.**

