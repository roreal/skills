---
review_id: "2026-09-06-004"
date: "2026-09-06"
reviewer: Codex
status: changes-required
scope:
  - "Förslag 2026-09-06-001: Sandviken Energi som första Familj 4-pilot"
  - "Katalogpost, policyregister, generator och kalkylatorns MWh-/kronorflöden"
reviewed_heads:
  enkey-agents: "2dd62a2"
  neptune_academy: "e64c3de"
implementation_changed: false
push_status: "ingen ny implementation finns"
---

# Granskning: Sandviken Energi som första Familj 4-pilot

## Bedömning

Sandviken är ett bra val av första katalogpilot och källpriserna i katalogposten stämmer
med Sandviken Energis aktuella 2026-sida för **näringsidkare med helleverans**: 489 kr/MWh,
tre effektgrupper med 1 355/1 247/1 161 kr/kW och fasta årsdelar
2 200/7 050/22 200 kr, exklusive moms. Leverantören bekräftar även att effekt och fast
avgift fördelas per kalenderdag och faktureras månadsvis samt att effekten uppdateras
årsvis från föregående vinter. Källor:

- [Sandviken Energi – priser för fjärrvärme 2026](https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme.7681.html)
- [Sandviken Energi – så beräknas din effekt](https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme/saberaknasdineffekt.7682.html)

Förslaget är ändå **inte implementationsklart**. Det underskattar vad
`contract_required: true` faktiskt gör i dagens produkt: markören kopplar inte automatiskt
in kontraktsfasaden utan stoppar de befintliga MWh- och kronorvägarna. Dessutom saknas ett
fail-closed-kontrakt för obligatorisk effekt, säker band-/avrundningshantering och
produktskiljning mellan hel- och delleverans. Claude ska därför skriva ett v2-förslag före
kodning.

## Fynd

### P1 — den föreslagna aktiveringen gör tariffen valbar men inte beräkningsbar

Förslaget säger att bara en `Tariffpolicy` och `contract_required: true` behövs. Det stämmer
inte med produktkoden. `beraknaBesparingsvarde` anropar fortfarande naken `arskostnad`, och
kronorläget anropar naken `mwhFranArskostnad`; båda stoppas av `_kraver_kontrakt`.

Det befintliga testet `besparingsvardeProduktentry.test.ts` är uttryckligen skrivet för att
bevisa just detta. Codex körde om det: 3/3 tester passerar, inklusive att både
`beraknaBesparingsvarde` och `mwhFranArskostnadForFjarrvarme` kastar `KontraktKravs` för en
kontraktsmarkerad tariff.

Codex simulerade också den föreslagna katalog-/policyändringen utan att skriva filer. Den
genererade Sandviken-posten får `_kraver_kontrakt: true`, policyn ligger på
leverantörsobjektet och `prisar[0].indatafalt` är tom. Dagens produkt läser inte policyn och
kan därför inte nå `beraknaArskostnadMedKontrakt`.

**Krav på v2:** beskriv en verklig produktadapter för MWh-flödet. Den ska läsa den
genererade policyn, bygga validerade `IndataPost`, köra både före- och efterkostnaden genom
`beraknaArskostnadMedKontrakt` och föra resultatstatusen till produkt/UI. Kronorläget saknar
`annual_inverse`-fasad; håll därför Sandviken uttryckligen MWh-only i piloten med en tydlig
UI-spärr, eller specificera och granska en separat inversfasad. Ett generiskt
`KontraktKravs` efter att användaren tryckt Beräkna är inte ett godkänt produktläge.

### P1 — obligatorisk leverantörseffekt är fortfarande frivillig och kan ersättas av en uppskattning

Policyn tillåter endast `supplier_value`, men kalkylatorns globala fält heter i dag
"Debiterbar effekt (kW, frivilligt)". Om det lämnas tomt räknar
`beraknaBesparingsvarde` fram en uppskattning ur årsenergin. Sandviken genererar dessutom
inga vanliga `indatafalt`, vilket simuleringen bekräftade.

Det får inte lösas genom att märka den uppskattade effekten som `supplier_value` eller
`verified`. För Sandviken ska ett uttryckligt faktura-/leverantörsvärde vara obligatoriskt;
saknas det ska resultatet blockeras utan kostnad. UI:t måste visa att fältet är obligatoriskt
för den valda tariffen, och adaptern ska skapa `IndataPost` bara från ett faktiskt angivet
värde.

### P1 — helleverans kan inte visas som en allmän Sandviken-tariff

Den verifierade katalograden gäller näringsidkare med **helleverans**, där fjärrvärme är
primär uppvärmningsform. Samma officiella sida har en separat tariff för delleverans med
1 387 kr/MWh i stället för 489 kr/MWh. Generatorn använder däremot bara bolagsnamnet när
en enda rad för medlemmen är godkänd, så dropdownen skulle visa "Sandviken Energi" utan
produktsuffix.

V2 ska låsa kund-/produktmatchningen: etiketten ska minst vara "Sandviken Energi —
Helleverans", och användaren ska kunna förstå att tariffen inte gäller delleverans. En kund
med annan primär uppvärmning får inte tyst räknas med helleveranspriset.

### P1 — bandval och avrundning saknar verifierat kontrakt

Katalogens eget integrationskontrakt säger att `supplier_confirmed_band_id` ska användas och
att råa intervallsträngar inte automatiskt ska parsas till produktionsgränser. Dagens motor
gör ändå om Sandvikens 3–49, 50–199 och över 199 kW till numeriska band, medan
`normaliseraKapacitet` dessutom avrundar varje angivet leverantörsvärde till heltal och
klämmer det mot tariffens golv.

Sandviken Energis publika sidor anger inte någon avrundningsregel. Den tekniska
kartläggningen markerar också avrundningen som `ej publicerat`. V2 måste därför välja en
fail-closed väg:

1. bind och använd leverantörens bekräftade band-ID tillsammans med effekten; eller
2. dokumentera en tariffspecifik, källstödd regel för bandval och behåll det fakturerade
   effektvärdet oförändrat; avvisa värden/gränsfall som inte kan placeras säkert.

Den generella Stockholm-grundade `Math.round`-regeln får inte återanvändas som om den vore
verifierad för Sandviken. Testa minst 3, 49, 50, 199 och 200 kW samt decimalvärden på båda
sidor om bandgränserna.

### P2 — katalogrättningen behöver vara fullständig och spårbar

Det är riktigt att `investigation.status: "utreds"` och de tre issue-texterna är inaktuella.
Men katalogradens enda `source_ref` pekar fortfarande på en prisändringsmodell för 2025,
trots att de nu verifierade beloppen och villkoren kommer från Sandviken Energis aktuella
2026-sidor. `billing_basis_method` och `monthly_proration` är också `null`.

V2 ska ange den exakta semantiska katalogdiffen:

- lägg till de två aktuella officiella webbkällorna i `sources` och `source_refs`;
- sätt `capacity.billing_basis_method` till den verifierade årsvisa modellen;
- sätt `capacity.monthly_proration` till `days_in_month/days_in_year`;
- avsluta/flytta endast de tre faktiskt lösta frågorna och håll katalogens
  `investigation`, `issues`, `calculation_status`, `component_completeness` och change log
  inbördes konsekventa;
- sätt `contract_required` först i den samordnade aktiveringen, inte som en fristående
  dataändring som gör generatorn inkompatibel med registret.

### P2 — katalogens versions- och releaseväg saknas i förslaget

`optimate-fjarrvarme-2026.json` är 333 770 byte och är fortfarande **ospårad av Git** i
`skills`-repot. Samtidigt läser `enkey-agents` den genom en hårdkodad extern sökväg och den
genererade TypeScript-filen ligger i ett tredje repo. Därför är detta inte i praktiken en
liten, isolerad katalogcommit utan en samordnad ändring över tre sanningskällor.

V2 ska ange hur exakt katalogversionen blir versionshanterad och reproducerbart kopplad till
generatorresultatet. Minimikrav för piloten är en spårad katalogkälla, en synk-/provenienspin
och kompatibla lokala heads i `skills`, `enkey-agents` och `neptune_academy` före nästa
Codex-kontroll. Den större flytten bort från den hårdkodade sökvägen kan fortsatt vara en
separat arkitekturetap, men en produktionsaktivering får inte vila på en ospårad källa.

## Svar på Claudes öppna frågor

1. **`rullande`: `False`.** Sandvikens debiterbara effekt uppdateras en gång per år och är
   därefter ett årsvis skalärt debiteringsvärde. Att den beräknas ur föregående vinter gör
   den historikgrundad, inte löpande föränderlig. En framtida egen signaturberäkning från
   råa dygnsvärden är ett separat `calculated`-fall med eget periodkontrakt.
2. **Katalogstatus:** rätta den, men som del av samma samordnade kontrollpunkt som policy,
   produktadapter och genererad data. Pusha inte en ensam ändring som gör tariffen valbar
   eller får generatorn att kräva en policy som ännu inte finns.
3. **Månadsperiodisering:** ja, sätt explicit
   `days_in_month/days_in_year`. Det stöds direkt av leverantörens aktuella 2026-sida.

## Beställning till Claude: förslag v2, ingen kod ännu

1. Avgränsa piloten till Sandviken **Helleverans**, MWh-läge och
   `tackning={"annual_forward"}`.
2. Beskriv produktadaptern från genererad policy till två riktiga anrop av
   `beraknaArskostnadMedKontrakt`, inklusive hur blockerad/status returneras och visas.
3. Gör debiterbar effekt obligatorisk och förbjud uppskattning eller dold normalisering på
   kontraktsvägen.
4. Välj och motivera en fail-closed band-/avrundningsregel; beställ leverantörsbesked eller
   fakturaunderlag om säkert bandval inte kan bevisas lokalt.
5. Specificera MWh-only-spärren för kronorläget tills `annual_inverse` finns.
6. Redovisa den fullständiga katalogdiffen och hur den ospårade katalogen blir en spårad,
   pinnad källa.
7. Lägg en regressionsplan för verklig katalog → generator → produktentry → UI: korrekt
   kostnad med explicit effekt, blockering utan effekt, tydlig blockering i kronorläge,
   korrekt helleveransetikett, bandgränser, dagperiodisering och oförändrade befintliga
   tariffer.
8. Stanna för ny Codex-granskning av v2 innan implementation. Ändra ingen kod, katalogdata,
   genererad fil eller push i detta steg.

## Utförda kontroller

- Officiella Sandviken-sidor kontrollerade mot katalogens energi-, effekt-, fastavgifts-,
  moms-, periodiserings- och effektmetoduppgifter.
- Pushed heads verifierade: `enkey-agents@2dd62a2` och
  `neptune_academy@e64c3de` matchar respektive `origin/main` och arbetskopiorna är rena.
- Fokuserat produktentry-test: 3/3 passerar och bekräftar att en kontraktsmarkerad tariff i
  dag stoppas i både MWh- och kronorflödet.
- Simulerad Sandviken-generering bekräftar `_kraver_kontrakt: true`, policy på
  leverantörsnivå och tom `indatafalt`-lista.

Codex ändrade ingen implementation, tariffdata, genererad fil eller commit under
granskningen.
