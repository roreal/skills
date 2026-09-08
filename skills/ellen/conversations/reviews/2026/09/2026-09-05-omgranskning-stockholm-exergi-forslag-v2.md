---
review_id: "2026-09-05-002"
date: "2026-09-05"
reviewer: Codex
status: changes-required
scope:
  - "Förslag 2026-09-04-002, version 2"
  - "Genomförbarhet mot nuvarande Python-/TypeScript-kontrakt, motor, fixture och produktflöden"
reviewed_heads:
  enkey-agents: "467c89f"
  neptune_academy: "82bcf3c"
implementation_changed: false
push_status: "ingen ny implementationskod"
---

# Omgranskning: Stockholm Exergi-förslag v2

## Bedömning

V2 rättar tre viktiga vägval från v1: debiterbar effekt klassas nu som ett årsvis
fakturavärde, infrastrukturen ska vara generell men bara Stockholm aktiveras som pilot, och
enforcement har skilts från ett föregående kontrollsteg. De delarna godkänns.

Förslaget är ändå inte genomförbart mot den nuvarande motorn och får fortsatt
**changes-required**. Det behöver en v3 innan kodning. Kärnfrågan är att hålla isär två
olika produkter:

1. fakturaexakt återspelning av en bestämd månad med alla fakturavärden, och
2. kalkylatorns årsprognos/omvända lösning när användaren normalt inte har dessa
   månadsuppgifter.

## Fynd

### P1 — den föreslagna policyn kan fortfarande ge falskt `annual/exact/complete`

V2 sätter `debiterbar_effekt_kw` till `kravs_for=("annual",)` men de två andra dynamiska
fälten till enbart `kravs_for=("monthly",)`. `harled_resultatstatus(...,
omfattning="annual")` filtrerar bort samtliga `monthly`-krav. Codex reproducerade därför att
en komplett v2-policy med endast effekten inrapporterad ger:

```text
Resultatstatus(omfattning='annual', noggrannhet='exact', fullstandighet='complete')
```

Det är samma falska fullständighet som v1 skulle undanröja.

Det finns dessutom flera direkta kontraktsmotsägelser:

- `kalla_typ="fakturerad"` finns inte; tillåtna värden är `supplier_value`, `calculated`
  och `estimated`.
- `IndataPost.varde` i Python och TypeScript kan vara tal eller lista, inte den föreslagna
  månadsmappningen.
- En serie på ett icke-rullande fält avvisas. Görs fältet rullande kan det med nuvarande
  modell aldrig bli `exact`.
- Årsfasaden har bara en statisk `kapacitet_bindning`. Övriga serier kastas i stället för
  att bindas, medan `returtemp_c` och `mwh_kallt_per_manad` fortfarande är fria,
  ovaliderade motorargument.
- Årsmotorn tar en enda `returtemp_c` och använder samma värde för alla vintermånader; den
  kan inte beräkna den föreslagna månadsserien exakt.

V3 ska välja och beskriva en verklig modellutvidgning: ett validerat månadsobjekt med
explicita månadstal och täckning, generella statiska motorbindningar för kapacitet, kall
energi och returtemperatur samt motsvarande Python-/TypeScript-regler. Alla dynamiska fält
som påverkar ett årsresultat måste vara relevanta även för årsresultat. `exact` får bara ges
när kontraktet kan verifiera rätt kalender, alla tillämpliga månader och explicita nollor —
frånvaro betyder fortfarande okänt.

### P1 — inversen är ett annat och underbestämt problem

`mwh_fran_arskostnad`/`mwhFranArskostnad` tar i dag varken kall månadsenergi eller
returtemperatur som indata. Den söker MWh med en kostnadsfunktion där kalltillägget blir noll
och returposten uteblir. Kalkylatorns befintliga kronläge har inte heller de föreslagna
månadsfälten att bygga `IndataPost` från.

Årskostnad + debiterbar effekt bestämmer därför inte en unik, fakturaexakt energimängd för
Stockholm Exergi: olika kalla volymer och returtemperaturer kan ge samma totalbelopp. Att
skriva att båda produktflödena ska använda samma kompletta policy löser inte detta.

V3 ska definiera separata beräkningsändamål och krav:

- **Faktura-/framåträkning:** kan bli exakt när månadens/årets faktiska värden är fullständiga.
- **Kronor → MWh:** blockeras som exakt om kostnadsposterna inte kan separeras. Om en
  uttrycklig uppskattning ska tillåtas måste antagandena anges, resultatet märkas
  `estimated` och statusen följa med hela vägen till användaren.

Det räcker inte att ändra `besparingsvarde.ts`. Returtyperna och
`KalkylatorPage.tsx`/det överordnade kalkylflödet måste kunna visa `exact`, `estimated` eller
`blocked`; annars är den utlovade synligheten inte implementerad. V3 ska namnge berörda
API-/UI-filer och acceptanskriterier.

### P1 — den nya regressionsplanens delår kan inte köras genom årsfasaden

V2 föreslår ett årsanrop för respektive prisårs del av Åkermannen-fixturen. Men
`arskostnad` summerar alltid årets tolv månader: saknade månader får noll energi men bär
fortfarande sin andel av hela årets kapacitetsavgift. Codex mätte följande redan med
oförändrad motor:

| Fixture-del | Månader | Fast kostnad, verkliga månadsanrop | Fast kostnad, årsanrop med delårsenergi |
| --- | ---: | ---: | ---: |
| 2025 | 8 | 93 620,88 kr | 139 476,00 kr |
| 2026 | 4 | 48 225,21 kr | 146 685,00 kr |

Årsanropen kan alltså inte jämföras med fixture-delarna krontal för krontal; de representerar
olika tidsomfattningar. Ett enda returtemperaturvärde i årsfasaden kan dessutom inte
återskapa de varierande månadsvärdena.

V3 ska använda någon av följande tydliga vägar:

- bygg en kontraktsfasad för `manadskostnad` och återspela var och en av de tolv faktiska
  fixture-raderna genom den, eller
- skaffa kompletta kalenderårsfixturer för separata årsregressioner.

Den första vägen rekommenderas för denna pilot eftersom det befintliga facit faktiskt är
månadsvis. Syntetiska helårstester kan komplettera, men får inte kallas fakturaverifiering.

### P2 — aktiveringsläge, shadow och datadiff behöver fail-closed-semantik

V2 anger tre strängvärden men säger bara att exakt `"enforced"` sätter markören. En
felskrivning som `"enforcd"` är `!= "off"`, kan nå policykontrollen och blir sedan tyst
oaktiverad. Generatorn ska avvisa fel typ och varje värde utanför den exakta allow-listan
`off|shadow|enforced`.

Ett test som jämför två beräkningsvägar är ett pre-enforcement-test, inte i sig ett
observerbart shadow-läge. Om namnet `shadow` behålls ska v3 ange var jämförelsestatusen
hamnar och hur den granskas. Om ingen runtime-observation ska byggas bör läget heta exempelvis
`validated` och beskrivas som en bygg-/testgrind.

V2 säger samtidigt både att `effektgrans_kw: 96` ska flyttas ur prisdatan och att alla
befintliga prisfält ska vara identiska i den semantiska diffen samt att prisdatan ska lämnas
oförändrad. V3 måste välja ett av alternativen. Rekommendationen är att inte låta värdet
användas generiskt, men att behandla själva flytten som en separat, uttryckligen tillåten
dataändring med ett test som bevisar att nuvarande beräkning inte ändras.

### P2 — 12/18/21-förklaringen är ännu en hypotes, inte verifierat facit

Det finns inga fakturadokument i de granskade repona, bara den konsoliderade
tolvmånadersfixturen. `korrigering_kr: -42.50` i en fixture-rad bevisar inte hur 18 och 21
dokument ska räknas eller att skillnaden är exakt tre preliminär-/avräkningsdokument.

Dokumentationen ska tills vidare säga exakt vad underlagen visar:

- testfixturen innehåller 12 konsoliderade månadsrader;
- leverantörsfilens prosa uppger 18 fakturor;
- dess JSON-metadata uppger 21 fakturor;
- relationen mellan 18 och 21 är inte verifierad i repot.

Detta blockerar inte kontraktsarkitekturen. Om en enda officiell siffra önskas behöver Robert
eller Claude kontrollera den verkliga dokumentlistan och ange dokumentdatum samt vilka som
är preliminära respektive avräkningar; inga antal ska härledas ur antaganden.

## Beställning till Claude: v3, fortfarande ingen kod

1. Dela lösningen i månadsvis fakturareproduktion, framåtriktad årskalkyl och kronor-till-MWh;
   ange separat vilka indata och statusregler varje ändamål har.
2. Specificera den nödvändiga kontrakts-/motorutvidgningen för validerade månadsmappar och
   tre statiska motorbindningar i både Python och TypeScript.
3. Använd `supplier_value` och definiera explicit månadstäckning, tillämpliga månader och
   verifierade nollor; bevisa att saknad kall/returdata inte kan ge `annual complete`.
4. Ersätt delårs-årstestet med en månadsfasad över alla tolv fixture-rader; håll syntetiska
   helårstester tydligt separerade.
5. Gör aktiveringsläget till en strikt allow-list och definiera observerbarheten, eller byt
   namn från `shadow` till ett rent bygg-/testläge.
6. Beskriv statuspropagering till produktens returtyper och UI samt lös motsägelsen kring
   `effektgrans_kw: 96` och den semantiska datadiffen.
7. Behåll 12/18/21 som tre separat attribuerade uppgifter tills fakturadokumenten har
   inventerats.

## Verifiering

- Ingen ny implementationskod finns efter `enkey-agents@467c89f` och
  `neptune_academy@82bcf3c`; båda arbetskopiorna är rena.
- Codex körde en riktad statusreproduktion som visade falskt
  `annual/exact/complete` med endast effekten enligt v2:s föreslagna `kravs_for`.
- Codex jämförde fixturens månadsvisa fasta kostnad med delårsdata genom `arskostnad` och
  verifierade de två periodiseringsavvikelserna i tabellen ovan.
- Ingen full testsvit kördes eftersom Claude inte har ändrat implementationskod.
