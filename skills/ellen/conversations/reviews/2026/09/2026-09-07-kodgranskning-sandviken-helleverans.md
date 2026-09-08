---
review_id: "2026-09-07-001"
date: "2026-09-07"
reviewer: Codex
status: changes-required
scope:
  - "Sandviken Energi Helleverans, annual_forward och MWh-only"
  - "Implementation efter godkännande 2026-09-06-006"
reviewed_commits:
  skills: "c601ebb349925f0074e80abe9e50e64e686672d3"
  enkey-agents: "fcb2fd8e0a09e177921527b10e9c5d91c33fbe7c"
  neptune_academy: "de17a7f8c3a4324461d9a8fe6fdf21cfb39074a1"
implementation_changed: false
push_status: not-approved
---

# Kodgranskning: Sandviken Energi Helleverans

## Beslut

Implementationens huvudväg fungerar, men **push godkänns inte ännu**. Tre P1-fynd bryter
de bindande fail-closed- och domänvillkoren i granskning `2026-09-06-006`: energins
MWh-proveniens kan kringgås, kontraktsmarkören kan feltolkas som frånvarande och
effektkravet upprätthålls inte av de gemensamma kontraktsfasaderna.

Claude ska rätta fynden i fokuserade lokala commits och stanna för ny Codex-granskning.
Ingen v4-plan eller omtagning av tariffmodellen behövs.

## Fynd

### P1 — `calcResult` och den exporterade produktentryn upprätthåller inte MWh-only

`neptune-marketing/src/utils/energiPotential.ts:450-466` definierar verklig energi som
enbart `energyMwh != null && energyMwh > 0`. `energyInputMode` kontrolleras inte. Därför
kan exakt samma positiva tal märkas som `kr` eller `schablon` och ändå nå Sandvikens
kontraktsberäkning.

Direkt reproduktion mot commit `de17a7f` med 1 200 MWh och 100 kW:

```text
mwh       CALCULATED 898187.5
kr        CALCULATED 898187.5
schablon  CALCULATED 898187.5
```

Det verkliga React-formuläret råkar blockera kronorläget tidigare genom
`mwhFranArskostnadForFjarrvarme`, men `calcResult` är den dokumenterade auktoritativa
domängrinden och kan anropas av andra gränssnitt. Dess eget kontrakt är alltså
kringgångbart.

Även den exporterade `beraknaBesparingsvarde` saknar kontroll av att Sandvikens
`totalMwh` är ett positivt, ändligt och faktiskt MWh-värde. Direkta anrop med 0 och −1
räknade fram kostnader; `NaN` och `Infinity` gav ett lyckat returvärde med `NaN`-belopp.
`calcResult` accepterade dessutom `energyMwh=Infinity` och gav ett `NaN`-resultat.

Rättning:

- en kontraktsgated `calcResult` ska kräva exakt `energyInputMode === "mwh"` samt ett
  ändligt tal större än noll;
- Sandvikens exporterade kontraktsentry ska inte kunna anropas utan motsvarande
  maskinläsbara energiproveniens och numerikvalidering;
- `kr` och `schablon` med ett positivt förifyllt/härlett energital ska få negativa test;
- 0, negativt tal, `NaN` och oändlighet ska blockeras innan energi fördelas eller pengar
  räknas.

### P1 — `kontraktsgatadPolicy` är fortfarande fail-open för felaktig markör och täckning

`neptune-marketing/src/utils/besparingsvarde.ts:143-151` returnerar `undefined` för varje
värde som inte är exakt `true`. Det gör inte skillnad på att markören saknas och att den
finns men är `false`, `null`, `"true"` eller `1`. Samtliga fyra reproducerades som
`undefined`, vilket skickar anropet mot legacyvägen. Villkor 1 i granskning
`2026-09-06-006` säger uttryckligen att **endast frånvarande markör** får betyda "ingen
kontraktsadapter".

Resolvern verifierar inte heller `annual_forward`. En sann markör med en i övrigt giltig
policy som bara täcker `monthly_invoice` returnerades framgångsrikt. Årsfasaden ger sedan
`blocked`, men `beraknaBesparingsvardeKontrakt` på rad 240-245 klassificerar varje sådant
resultat som användarfelet `missing_capacity`. Ett konfigurationsfel kan därmed presenteras
som om kunden glömt effektfältet.

Rättning:

- kontrollera om egenskapen `_kraver_kontrakt` faktiskt finns;
- saknas egenskapen: returnera `undefined`; finns den: kräv exakt boolean `true`, annars
  kasta ett konfigurationsfel;
- kräv giltig, tariff-ID-matchande policy med `annual_forward` redan i resolvern;
- lägg negativa test för feltypad markör, saknad/trasig policy och saknad täckning;
- bevara regressionen att Stockholm Exergis `validated`-policy utan markör inte påverkas.

### P1 — effektens heltals-/minimikrav kan kringgås via kontraktsfasaderna

TypeScript-produktadaptern på
`neptune-marketing/src/utils/besparingsvarde.ts:213-234` validerar korrekt ett ändligt
heltal från 3 kW och för det oförändrat vidare. Samma krav finns däremot inte i den
gemensamma kontraktsfasaden. Python-testet
`tools/tariffer/tests/test_sandviken_kontrakt.py:79-91` föreskriver tvärtom att 2 kW ska
ge `complete`.

Direkta Pythonanrop genom `berakna_arskostnad_med_kontrakt` reproducerade följande:

```text
2 kW     complete
2,9 kW   complete
3 kW     complete
49,5 kW  complete
```

Det bryter villkor 3: domänkontrollen ska vara auktoritativ så andra anropare inte kan
kringgå `ändligt heltal >= 3`. Skyddet blir dessutom beroende av om anropet går via
TypeScript-produktadaptern eller direkt via en gemensam kontraktsfasad.

Rättning: lägg tariffens numeriska krav i policy-/indatakontraktet eller inför en verklig,
testad Sandvikenadapter även för Pythonanrop. Hårdkoda inte Sandviken-ID i den generiska
motorn. Samma gränser och avslag ska verifieras i båda språken; ta bort testet som
godkänner 2 kW.

### P2 — tomt eller ogiltigt MWh-värde får fel användarorsak

Tomt, 0, negativt och `NaN` i MWh-läge blir i dag `unsupported_input_mode`. I den verkliga
webbläsaren får en användare som redan valt MWh därför texten att leverantören "bara"
stödjer MWh och att MWh ska väljas. Det är inte rätt orsak eller åtgärd.

Inför exempelvis `missing_energy` och `invalid_energy`, eller ett likvärdigt typat
kontrakt, med korrekt svensk text. Behåll `unsupported_input_mode` för kronor och
schablon. Testa både domänorsak och synlig formulärtext.

### P2 — katalogens övergripande `as_of` uppdaterades inte

De två nya källorna har korrekt `retrieved_on: "2026-09-06"`, schema/revision är höjd och
ändringsloggen är kompletterad. Men
`skills/ellen/Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:5` står fortfarande på
`"as_of": "2026-09-02"`. Villkor 6 krävde uttryckligen nytt `as_of` för
kontrolltillfället. Sätt det till katalogändringens faktiska granskningsdatum och uppdatera
hash/proveniens/regenererad fil deterministiskt.

### P3 — policyregisterkommentaren beskriver det gamla nuläget

`tools/tariffer/policyregister.py:20-22` säger fortfarande att ingen katalogtariff bär
`contract_required: true`. Sandviken gör nu det. Rätta kommentaren så dokumentationen
inte motsäger registret direkt under den.

## Det som verifierades fungera

- Committerna bygger direkt på de tidigare granskade och pushade heads
  `enkey-agents@2dd62a2` och `neptune_academy@e64c3de`; båda implementationsrepona är
  rena och deras `origin/main` ligger kvar på respektive förälder.
- `skills@c601ebb` innehåller bara katalogfilen; övriga ospårade Ellen-filer följde inte
  med.
- Kataloggrinden ger exakt 7 poster och den genererade diffen består av den nya
  proveniensraden, räknarändringen 6→7 och Sandvikenblocket. Befintliga tariffblock och
  etiketter ändrades inte.
- Genererad etikett och ID är `Sandviken Energi — Helleverans` respektive
  `sandviken-energi-sandviken-normal`; policy och markör ligger på prisårsposten.
- Giltigt MWh-flöde med 100 kW gav ett resultat i den verkliga webbläsaren utan
  konsol-/sidfel. Effektfältet var `required`, `min=3`, `step=1`.
- React-formuläret blockerade kronor och schablon. Problemet i P1 är att domän-API:t kan
  kringgå denna UI-väg.
- Före-/efterkostnad använder `summaInkl`, rå giltig heltalseffekt bevaras i
  TypeScript-adaptern och lyckat resultat bär `complete`/`snapshot`.
- Proveniensraden innehåller katalogens faktiska SHA-256 och exakt
  `skills@c601ebb`; korssynktesterna är gröna.

## Körda kontroller

```text
enkey-agents: tools/tariffer       360 passed
neptune-marketing: Vitest          382 passed
TypeScript: tsc --noEmit           godkänd
Produktionsbygge: npm run eval:build godkänd
git diff --check, alla tre commits godkänd
Playwright, localhost              giltigt MWh-flöde godkänt; kr/schablon blockerade
```

Ett oavgränsat `pytest` från hela `enkey-agents` samlade även in det orelaterade
Milesight-paketet och stoppade under insamling på 13 saknade/importkonfliktande
Milesight-beroenden, bland annat `pymodbus`. Den tariffavgränsade svit Claude redovisade
är däremot reproducerat grön med 360 tester; Milesight-felet bedöms inte vara orsakat av
de tre Sandvikencommitterna.

## Leveransgräns

Ingen push är godkänd. Observera dessutom att `skills` lokala `main` ligger två commits
före `origin/main`: den tidigare dokumentationscommitten `8ef6955` samt den nya
`c601ebb`. En framtida pushredovisning måste därför namnge den verkliga commitkedjan, inte
bara beskriva leveransen som tre commits totalt.

Codex ändrade ingen implementationskod, katalogdata, genererad fil eller commit under
granskningen.
