---
review_id: "2026-09-11-012"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Batch 1-rättningsrunda 3 efter granskning 2026-09-11-011"
  - "Policystyrd kapacitetsvalidering, komplett driftprov, bandetiketter/ARIA och Övik-proveniens"
reviewed_heads:
  skills: "659d8436365f8843022b19408f69fb7680dbaff0"
  skills_catalog_commit: "d2b035e9ed27dcc1b7c8d0dafbef795570c996d3"
  enkey-agents: "1078098b056a568ea363182280d91d60c5b68654"
  neptune_academy: "0dc48d6fcbe7075fd76e1f869021c011f8bc08d9"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "58fb06e165bc1296ef48043e5a7ebc917a1972c8"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
tariff_activation_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
rechecks_review: "2026-09-11-011"
---

# Omgranskning av Batch 1, rättningsrunda 3

## Beslut

**Changes required.** Rättningsrunda 3 stänger huvuddelen av granskning 011:

- Karlstad 30,9 kW går nu genom normal knappsubmit, medan Övik 55,5 kWh/dygn och
  Sandviken 3,5 kW får rätt fältnära heltalsfel och ARIA-koppling.
- Driftprovet kör verkligen och jämför hela `till_prisar()`-objektet inklusive
  `indatafalt` samt hela den serialiserade policyn för alla sex kandidater.
- Dubbla legacy-/policyfält filtreras bort; för nuvarande policyregister överlappar
  exakt de fyra avsedda kandidaternas årsnycklar och inga monthly-only-nycklar.
- Bandtexten genereras med rätt enhet och decimaltecken. Öviks medlemsproveniens
  innehåller nu både historiska `30_0` och officiella 2026-källan `30_1`.
- Pythons 39-bandmatris kontrollerar nu även den oberoende kapacitetskostnaden.

Leveransen kan ändå inte aktiveras. Den nya kapacitetskontrollen är fortfarande inte
helt policystyrd: sidan lägger till ett eget positivkrav som motsäger två policyer.
Dessutom tappade Batch 1-policyn Telges källbelagda heltalsavrundning. Båda felen kan
ge ett annat beteende än leverantörsunderlaget och måste rättas innan de sex
kandidaterna blir valbara.

Alla sex ska fortsatt vara inaktiva. `godkanda(katalog)` är omverifierad till exakt
**9** och dispositionen är fortsatt **9/55/28**.

## P1 — UI:t överstyr två kontrakt med ett eget positivkrav

`KalkylatorPage.tsx:704–718` avvisar fortsatt varje kapacitet `<= 0`, även på den
kontraktsgatade vägen. `KalkylatorPage.tsx:1273–1285` annonserar samtidigt
`min={Math.max(1, policyMin)}`. Detta är inte härlett ur policyn.

Telge och Partille deklarerar båda `minvarde=0` i
`policyregister.py:455–464,488–496`, och de officiellt extraherade första banden är
`0–299` respektive `0–50`. Samma kompletta underlag med 0 kW ger därför korrekt
`complete` i båda domänimplementationerna:

- Telge: TypeScript `summaExkl=5 384`, Python komplett med fast del 0,
  energidel 5 132 och justering 252.
- Partille: TypeScript `summaExkl=9 310`, Python komplett med fast del 4 720,
  energidel 4 443 och justering 147.

Normal UI-submit stoppas däremot före domänkontrollen med texten att värdet måste vara
positivt. Ett värde som kontraktet uttryckligen tillåter kan alltså inte matas in i
produkten.

**Krav på rättning:** behåll legacyvägens separata `> 0`-/heltalsregel, men låt den
kontraktsgatade vägen följa den bundna `KravPost`-postens faktiska
`minVarde`/`minExklusiv`/`maxVarde`/`heltal`. Ta bort `Math.max(1, ...)` för kontrakt.
Med nuvarande käll- och policydata ska 0 accepteras för Telge och Partille. Om en ny
källkontroll i stället visar att gränsen ska vara strikt, ska det uttryckas som
`minvarde_exklusiv=True` i policyn och speglas i båda språk — aldrig bara i React.
Lägg permanenta normal-submit-prov för 0 i båda kandidaterna, med band 1 och komplett
övrig indata.

## P1 — Telges källbelagda heltalsregel saknas i policyn

Verifieringslistans Telge-post anger uttryckligen att tillsvidarevillkoren verifierar
**heltalsavrundning**. Katalogens `billing_basis_method` säger också att
dygnsmedeleffekten är heltalsavrundad. Trots detta skapar
`_familj4_kapacitet_krav` Telges kapacitetskrav med default `heltal=False`
(`policyregister.py:455–464`). Rättningskommentaren och TypeScript-testet påstår sedan
felaktigt att endast Övik har heltalskrav.

Codex hämtade även den länkade
[officiella villkorsbilagan](https://www.prisdialogen.se/wp-content/uploads/2020/11/TN-prislista-fjarrvarme-2025_Foretag.pdf)
på nytt. Sidan 3 säger uttryckligen: ”Den debiterade effekten avrundas till närmaste
heltal.” Villkoren anges där gälla tills vidare från 2021-01-01.

Codex körde samma kompletta Telgefall med `100,5 kW` direkt genom båda fasaderna.
Python och TypeScript rapporterade båda `heltal=false`, tom preflight-fellista och
`complete`; den fasta kapacitetsdelen blev **166 930,50 kr**. Det strider mot den
källbelagda heltalsavrundningen.

**Krav på rättning:** låt den delade kapacitetsbyggaren ta ett explicit heltalskrav
eller bygg Telgekravet separat, sätt endast de källbelagda kandidaterna till heltal och
uppdatera fixture/driftdata. Lägg direkta Python-/TypeScript-preflightprov samt ett
normalt UI-submitprov som visar att Telge 100,5 blockeras fältnära med ARIA och inget
resultat, medan ett heltal fungerar. Rätta kommentarer/testnamn som säger ”endast
Övik”.

## P2 — det beställda öppna bandet provas inte i den riktiga sidan

Formatteren har ett grönt enhetstest för både `3–30,9 kW` och `31+ kW`, och koden ser
korrekt ut. Sidtesterna i `KalkylatorPageBatch1.test.tsx:330–345` hävdar däremot att
ett stängt Karlstadband och ett stängt Övikband är ”öppna”; inget av dem har
`max=null`. Det första testnamnet medger till och med ”inte öppet”, och dess assertion
läser inte band 5 alls.

Batch 1 har redan ett verkligt öppet band: Partilles band 7 (`max=null`, genererad
label `7 (2501+ kW)`). Ersätt de missvisande testnamnen och lägg ett riktigt DOM-prov
som läser detta synliga alternativ. Detta är en testlucka, inte ett konstaterat fel i
formatteringskoden.

## Oberoende verifiering

- Riktade TypeScript-/UI-/driftprov: **69 passed, 0 skipped**.
- Full TypeScript-svit: **883 passed, 0 skipped** i 27 filer.
- Python, rätt tariffscope (`.venv/bin/python -m pytest -q tools/tariffer/tests`):
  **692 passed, 4 skipped**.
- Repo-roten samlar dessutom in orelaterade Milesight-tester och stannar på 14
  importfel (`pymodbus`/tests-paket); det är befintligt och utanför tariffleveransen.
- `npx tsc --noEmit`: godkänd.
- Produktionsbygge: godkänt; genererad `dist` återställd.
- Självbärande E2E: samtliga 8 scenarier godkända.
- Direkta Python-/TypeScriptreproduktioner: 0 kW komplett för Telge/Partille;
  Telge 100,5 kW felaktigt komplett i båda språk.
- Ingen aktuell policytariffs bandgränser har fler än en decimal; den nya
  bandformatteringen ändrar därför ingen nuvarande gräns genom sin
  endecimalsformatering.
- `git diff --check`: rent för de granskade produkt- och katalogintervallen.
- Remote `main` omverifierad: `skills@c045751`, `enkey-agents@58fb06e`,
  `neptune_academy@d0dfb92`. Rättningscommittarna är fortfarande lokala; Codex
  pushade inget.

## Nästa stoppunkt

Claude får göra en enda fokuserad rättningsrunda för de två P1-fynden och P2-testet
ovan. Ingen tariff får aktiveras och inget repo får pushas före ny Codex-granskning.
Efter rättningen ska fulla sviter, typkontroll, bygge och E2E köras igen, dispositionen
fortsatt vara exakt **9/55/28**, och de nya gränsfallen redovisas separat.
