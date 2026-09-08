---
review_id: "2026-09-08-003"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v3.md
  - Fjarrvarmetariffer/batchplan-v3.md
  - skills commit 7b2db36376e6e936b121b2a80e9a14da197169d0
reviewed_heads:
  skills: "7b2db36376e6e936b121b2a80e9a14da197169d0"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-002"
---

# Omgranskning av tariffinventering v3 och batchplan v3

## Bedömning

V3 är en tydlig förbättring. Exakt 78 unika katalog-ID:n finns, dispositionsräkningen
7 implementerade + 45 redo + 26 blockerade stämmer och samtliga 14 variant-ID:n är nu
räknade. Eskilstuna är blockerad, de kända säsongsmånaderna är tariffvisa, Familj 4 ligger
först och committen ändrar ingen produktkod eller tariffdata. `git diff --check` är rent.

Kontrollpunkten kan ändå inte godkännas för implementation. E.ON/Navirums
36-månadersmetod har fått fel fysisk storhet som indata, Kraftringens avvikande
minimifaktor har tappats i den gemensamma motorbeskrivningen och batchernas obligatoriska
indata avviker fortfarande från inventeringen för VänerEnergi och Mälarenergi. Dessutom
saknar varianttabellen den källproveniens som uttryckligen beställdes, och den incheckade
konversationsindexen länkar fortfarande till 35 filer som inte finns i committen. Ingen
implementation eller push godkänns före en fokuserad V4-rättning.

## Fynd

### P1 — E.ON/Navirums 36-månadersvariant beskriver fel mätvärde och fel kontrakt

Inventeringen §5 och batch 3b kräver ett "36 månaders rullande medelvärde av
framledningstemperatur". Det finns inte i den verifierade tariffregeln. Källunderlaget
anger i stället medelvärdet av de tre högsta **dygnsmedeleffekterna** under de senaste
36 månaderna, inklusive fakturamånaden. Månadens medelframledningstemperatur hör separat
till flödeskorrigeringen. Batchplanen säger dessutom först tre fält och därefter "samma tre
fält ... plus" 36-månadersvärdet.

**Begärd rättning:** välj och dokumentera ett av två kontrakt per variant:

1. leverantörens fakturerade/debiterbara effekt som obligatorisk månadsindata; då behövs
   ingen 36-månadersformel i kalkylatorn, men månadens volym och medelframledningstemperatur
   ska fortfarande vara egna fält; eller
2. egen beräkning från en komplett serie dygnsmedeleffekter för rullande 36 månader, med
   exakt topp-tre-regel, månadstäckning, reserv-/valideringsregler och ny motorkod.

Ange uttryckligen om årsvägen tar tolv månadsrader eller ett leverantörsvärde som bara ger
en märkt `snapshot`-uppskattning. Rätta samtliga åtta variant-ID:n och batch 3b konsekvent.

### P1 — batchernas indata är fortfarande inte identisk med tariffposterna

- Batch 1 kräver bara effekt för VänerEnergi, medan inventeringen och katalogens
  `volume`-post kräver helårsflöde i m³ utöver effekt.
- Batch 5c kräver effekt/band för samtliga åtta tariffer, trots att
  `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` uttryckligen saknar
  kapacitetsdel och bara behöver energi samt säsongsflöde utöver katalogens fasta avgift.

**Begärd rättning:** återge tariffens exakta obligatoriska fält, enheter, månader,
upplösning och fyndplats även i respektive batch. Lägg till ett maskinellt kontrolltest
eller en genererad matris som förhindrar att batchtexten divergerar från inventeringen.

### P1 — den delade E.ON/Navirum/Kraftringen-formeln tappar Kraftringens minimifaktor

Batch 3 beskriver en enda formel
`volym × base_rate × (0,02 × (Tf − 60) + 0,2)` för alla nio tariffer och påstår att
E.ON/Navirums `correction_formula` finns i katalogen. De åtta katalogposterna har i själva
verket `correction_formula: null`; deras formel är källverifierad i verifieringslistan.
Kraftringens katalog och källa har samtidigt den materiellt annorlunda faktorn
`max(0,2; 0,2 + (Tf − 60) × 0,02)`. En odelad implementation enligt batchtexten kan därför
underdebitera Kraftringen när `Tf < 60 °C`.

**Begärd rättning:** beskriv en parametriserad motortyp med två verifierade regelvarianter,
korrekt källproveniens och minst ett golden-/gränstest per variant, inklusive Kraftringens
golv vid 0,2.

### P1 — variantproveniens och Finspångs disposition är inte färdiga

Föregående granskning krävde källor per faktisk variant. §5 har 14 räknade rader men ingen
källkolumn eller direkt `source_id`/URL. Det är särskilt problematiskt för de åtta
E.ON/Navirum-varianterna, vars metod nu också är felskriven. Flera bastariffer hänvisar
dessutom endast till äldre 2025-dokument trots att verifieringslistan innehåller de
aktuella officiella 2026-källor som faktiskt bar godkännandet, bland annat E.ON Järfälla,
E.ON Malmö, båda Navirum-näten och VänerEnergi.

Finspångs spetsvärmetillägg är klassat `ready_to_implement`, samtidigt som både
inventeringen och batch 6b säger att vilka kunder/perioder som utlöser tillägget inte är
kartlagt och att kompletterande kartläggning krävs. Det strider mot V3:s egen definition
av `ready`, där samtliga regler ska vara verifierade utan ett nytt besked.

**Begärd rättning:** lägg `source_id` och aktuell officiell direktlänk på varje variant.
Mappa Finspångs publicerade villkor till ett entydigt kund-/avtalsfält och ange om
20 procent gäller samtliga prisdelar; om detta inte kan beläggas ska varianten flyttas till
`blocked_external_info` med exakt fråga. Räkna om status- och batchsummorna om statusen
ändras.

### P1 — dokumentationscommitten är fortfarande inte självbärande

V3 lade till de två närmast citerade granskningarna, men den incheckade
`conversations/index.md` länkar fortfarande till 35 review-, proposal-, session- och
handoff-filer som bara finns ospårade i den lokala arbetskopian. En ren checkout av
`7b2db36` får därför ett index med 35 saknade mål. Påståendet i handoffen och sessionsloggen
att dokumentationscommitten är självbärande är inte korrekt.

**Begärd rättning:** använd en explicit fillista och spåra de 35 filer som indexet är
beroende av, eller begränsa den incheckade indexen till dokument som faktiskt ingår i
committen. Ta inte med övriga ospårade Ellen-filer.

### P2 — inmatningslägena motsäger fortfarande varandra

- Sundsvall Indals produktpost säger att `kr` och `schablon` blockeras, medan batch 2 säger
  att båda ska visas och hävdar att ingen motsägelse finns.
- Stockholm Exergis produktpost/generella regel blockerar lägen utan verifierad modell,
  medan batch 7 lämnar `kr`/`schablon` öppet för beslut under implementation.

**Begärd rättning:** frys en och samma status per produkt och läge i både inventering och
batchplan. Ett nytt läge får öppnas först när dess verifierade invers-/schablonmodell och
test finns i den godkända arbetsordern.

### P2 — batchsumman är aritmetiskt eller semantiskt oklar

De redovisade raderna för batch 1–7, 3b och 6b summerar till 54, inte 55. Skillnaden är
Borås miljötillägg, som räknas som egen `ready`-variant i inventeringen men byggs inne i
batch 6 vars tabellrad fortfarande säger två tariffer. Bastariffens egen post och batch 6
inkluderar dessutom redan miljötilläggets kryssruta.

**Begärd rättning:** kalla kontrollmängden 78 bastariffer + 14 räknade
varianttäckningskrav om det är den avsedda modellen, och redovisa batch 6 som två
bastariffer + en varianttäckning. Annars ska dubbletten tas bort och totalen räknas om.

## Verifieringar

- Katalogens 78 ID:n jämfördes maskinellt med 78 produktubriker: inget saknas, inget är
  extra och ingen dubblett finns.
- Dispositionerna räknades oberoende: 7 implementerade, 45 redo och 26 blockerade.
- Varianttabellen innehåller 14 unika ID:n: 10 redo och 4 blockerade. Den formella totalen
  7 + 55 + 30 = 92 stämmer före sakrättningarna ovan.
- Samtliga `ready`-posters katalogjusteringar jämfördes med inventeringens
  `Obligatorisk indata`; inga ytterligare nyckelordsbaserade flödes-/temperaturluckor
  hittades i bastariffraderna.
- Katalogens `months`-listor jämfördes med batch 5c; de åtta listade säsongsperioderna
  stämmer. Felet där gäller Mälarenergis felaktiga effektkrav, inte månadslistan.
- E.ON/Navirums 36-månadersregel jämfördes med verifieringslistans källsammanfattning.
- Kraftringens och E.ON/Navirums faktorer jämfördes med både katalog-JSON och
  verifieringslistan.
- `git diff --check HEAD^ HEAD` är rent och committen ändrar endast dokumentation.
- En kontroll mot `git ls-files` hittade 35 lokala länkmål i den incheckade indexen som
  saknas i committen.
- Implementationsrepona är rena och oförändrade på redovisade HEAD-versioner. Inga
  produkttester kördes eftersom leveransen endast är dokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v4.md` och `batchplan-v4.md`; ändra inte V3 i efterhand.
2. Rätta E.ON/Navirums åtta 36-månadersvarianter enligt faktisk effekthistorik och välj ett
   entydigt leverantörsvärdes- eller tidsseriekontrakt.
3. Gör batchindatan identisk med inventeringen för VänerEnergi och Mälarenergi 2–4
   lägenheter.
4. Separera E.ON/Navirums flödesfaktor från Kraftringens golvbegränsade faktor i modell och
   tester.
5. Lägg aktuell, direkt källproveniens på alla 14 varianter och lös Finspångs
   `ready`-motsägelse genom verifierad mappning eller blockering.
6. Rätta Sundsvall/Stockholms lägesstatus och batchsummans Borås-semantik.
7. Gör committen självbärande mot den incheckade indexen med en explicit fillista.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `7b2db36` och stanna för ny
   Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha inte.
