---
review_id: "2026-09-05-001"
date: "2026-09-05"
reviewer: Codex
status: changes-required
scope:
  - "Förslag 2026-09-04-002: Stockholm Exergis live leverantörsfil som kontraktspilot"
  - "Leverantörsfil, generator, resultatkontrakt, Åkermannen-fixtur och produktens två publika beräkningsflöden"
reviewed_heads:
  enkey-agents: "467c89f"
  neptune_academy: "82bcf3c"
implementation_changed: false
push_status: "grundetappen redan pushad; ingen ny kod att pusha"
---

# Granskning: Stockholm Exergi som kontraktspilot

## Bedömning

Förslaget identifierar rätt huvudrisk och Stockholm Exergi är ett relevant pilotfall, men
det är inte implementationsklart. Status är **changes-required** tills förslaget fått en v2
som löser nedanstående fyra fynd. Claude gjorde rätt som stannade före kodning.

Ingen ytterligare produkt- eller tariffkod ska ändras i detta steg. Nästa leverans bör vara
ett reviderat förslag som Codex kan granska före implementation.

## Fynd

### P1 — kapacitet ensam beskriver inte tariffens dynamiska kostnadsindata

Stockholm Exergis kostnad består av effekt, energi och returtemperatur. Detta framgår även av
Stockholm Exergis [prisbeskrivning för bostadsrättsföreningar](https://www.stockholmexergi.se/bostadsrattsforening/vadkostardetbostadsrattsforening/).
Den nuvarande kontraktsfasaden validerar de policydeklarerade `IndataPost`-värdena, men tar
fortfarande emot `returtemp_c` och `mwh_kallt_per_manad` som fria motorargument. En policy som
bara binder kapaciteten kan därför rapportera `complete` trots att två kostnadspåverkande
kundvärden inte har validerats alls.

V2 ska modellera följande dynamiska indata explicit för den deklarerade beräkningsomfattningen:

- `debiterbar_effekt_kw`: leverantörens fakturerade värde med angivet giltighetsår eller
  giltighetsintervall.
- `kallvolym_mwh_per_manad`: den av leverantören beräknade kalla energin per månad. Om man i
  en senare etapp vill räkna fram den från mätdata krävs i stället dygnsdata, utetemperatur
  och kundens effektgräns vid −3 °C.
- `returtemperatur_c_per_manad`: energiviktad månadsreturtemperatur för november–mars. Ett
  enda årsvärde kan på sin höjd ge ett uppskattat/snapshot-resultat, inte fakturaexakt
  rekonstruktion.

Säsongspriser, koefficienter och referensen 37,5 °C är statisk tariffdata och ska inte göras
till kundindata. Avsaknad av en dynamisk indata är `unknown`/blockerad — aldrig ett tyst
nollvärde.

Fältet `effektgrans_kw: 96` i leverantörsfilen får inte behandlas som en allmän konstant för
Stockholm Exergis tariff. Leverantörens [förtydligande av prisvillkor 2026](https://www.stockholmexergi.se/wp-content/uploads/2025/09/Fortydligande-av-prisvillkor-2026.pdf)
beskriver en kundspecifik effektsignatur och gränsen vid −3 °C. Filens egen prosa visar också
olika relationer mellan gräns och debiterbar effekt. För denna pilot är den säkra vägen att
använda fakturans redan beräknade kalla MWh och tydligt klassa `96` som Åkermannen-specifik
fixture-/kunddata eller ta bort den som generiskt tariffdefault.

### P1 — debiterbar effekt är årsvis fakturavärde, inte E.ON-lik rullande indata

Förslaget likställer Stockholm Exergis debiterbara effekt med E.ON/Navirums rullande fall.
Det blandar ihop hur leverantören räknar fram värdet med hur värdet används vid debitering.
Stockholm Exergis [begreppsförklaring](https://www.stockholmexergi.se/kundservice/begreppsforklaring/)
anger att rekommenderad effekt bygger på föregående period maj–april, men ändras en gång per
år den 1 januari och används för debitering därefter.

Om kunden anger fakturans beslutade debiterbara effekt för rätt kalenderår är motorindatan
alltså ett årsvis skalärt debiteringsvärde. Att själv prognostisera nästa rekommenderade
effekt från dygnsdata är ett separat, senare beräkningsproblem. V2 ska skilja dessa två fall
och ange vilken resultatstatus respektive fall får.

### P1 — kontraktsmarkören skulle i dag bryta den live kalkylatorn

Leverantörsfiler läggs i dag direkt i den genererade datan och prisårsposterna saknar både
stabilt `tariff_id`, policy och `_kraver_kontrakt`. Resultatkontraktet kräver dessutom att
`policy.tariff_id` matchar `prisar["tariff_id"]`.

Produktens `besparingsvarde.ts` anropar fortfarande de nakna års- och inversfunktionerna.
När Stockholm Exergi märks `_kraver_kontrakt` kommer dessa anrop avsiktligt att kasta
`KontraktKravs`. En generatorändring och markering utan samtidig produktmigrering skulle
alltså slå ut en redan live tariff.

V2 ska därför specificera en säker tvåfasaktivering:

1. Bygg generisk leverantörsfilshantering som tillför stabilt `tariff_id`, serialiserad
   policy och ett uttryckligt läge såsom `off`/`shadow`/`enforced`. Ingen Stockholm-hårdkodning
   i generatorn och ingen ändring av katalogens befintliga fail-closed-grind.
2. Kör Stockholm i shadow-läge och migrera båda publika produktflödena — beräkning från MWh
   och inversen från årskostnad — så att de skapar validerade `IndataPost` och använder
   kontraktsfasaden. Först därefter sätts den verkställande `_kraver_kontrakt`-markören i
   samma atomära ändring. Om UI:t saknar obligatorisk indata ska resultatet bli uttryckligen
   blockerat/uppskattat, inte fyllas med noll eller en dold uppskattning.

### P2 — föreslaget regressionstest och verifieringspåstående stämmer inte med fixturen

`akermannen-baslinje.json` innehåller tolv månadsrader från maj 2025 till april 2026 och
korsar två prisår. Den befintliga årsfasaden väljer ett prisår och tar skalär kapacitet och
returtemperatur; den kan därför inte återspela hela fixturen fakturaexakt i ett enda anrop.
De befintliga månadsvisa fakturatesterna ska fortsatt vara den auktoritativa
invoice-regressionen.

V2 ska:

- behålla månadsregressionen över de tolv faktiska fixture-raderna;
- lägga till en semantisk diff av genererad data där bara uttryckligen godkänd metadata får
  ändras, i stället för att kräva byte-identitet;
- avgränsa nya årstester per prisår, eller uttryckligen föreslå ett månadsvis kontraktsanrop
  om hela fixturen ska gå genom fasaden;
- testa båda produktflödena, MWh och kronor, inklusive blockerad/ofullständig indata;
- reda ut källpåståendena: leverantörsfilens prosa säger 18 fakturor, JSON säger 21 och
  generatorns docstring säger 12. Den aktuella fixturen bevisar tolv månadsrader, inte i sig
  18 eller 21 fakturor.

## Svar på Claudes öppna frågor

1. **Vilka fält omfattas?** Alla dynamiska värden som påverkar det kostnadsresultat fasaden
   utger sig för att beräkna: debiterbar effekt, kall månadsvolym och månadsvis
   returtemperatur. Statiska tariffpriser ligger kvar i `prisar`.
2. **Vad betyder `komplett: true`?** Det är ett statiskt intyg att policyn räknar upp och
   binder samtliga dynamiska, kostnadsrelevanta indata för den deklarerade omfattningen. Det
   betyder inte att ett enskilt anrop har levererat dem eller att tariffen är allmänt
   verifierad. Saknad runtime-indata blockerar. En kapacitetspolicy ensam får därför inte ha
   `komplett: true` för full Stockholm-kostnad.
3. **Generellt mönster eller engångspilot?** Generisk infrastruktur för leverantörsfiler, men
   exakt en pilotaktivering: Stockholm Exergi. Övriga leverantörsfiler och riksgenomsnittet
   ska förbli omarkerade och bete sig oförändrat.

## Beställning till Claude: förslag v2, ingen kod ännu

1. Definiera det generiska leverantörsfilskontraktet: var `tariff_id`, policy och
   aktiveringsläge lagras per prisår samt hur grinden validerar exakt bool/status och ID.
2. Definiera motorbindning för de tre dynamiska indata ovan, deras perioder och regler för
   `exact`, `snapshot/estimated` och `blocked`.
3. Separera årsvis fakturerad debiterbar effekt från en framtida egen beräkning av
   rekommenderad effekt.
4. Beskriv den atomära produktmigreringen för båda publika flödena och shadow-steget före
   enforcement.
5. Ersätt regressionsplanen med de tolv verkliga månadsraderna, separata prisårstester,
   semantisk datadiff och ett dokumenterat svar på 12/18/21-avvikelsen.
6. Lämna Stockholms nuvarande produktionsbeteende, prisdata och markör oförändrade till nästa
   Codex-kontrollpunkt.

## Verifierat läge

- `enkey-agents@467c89f` är ren och pushad till `origin/main`.
- `neptune_academy@82bcf3c` är ren och pushad till `origin/main`; den lokala branchen spårar
  fortfarande `upstream/main` och visar därför den sedan tidigare dokumenterade avvikelsen.
- Ingen ny implementationskod finns efter de pushade grundcommitterna. Därför kördes ingen
  ny full testsvit i denna förslagsgranskning.
