---
review_id: "2026-09-11-009"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Komplett lokal Batch 1-leverans mot handoff 2026-09-11-001 och V22"
  - "Sex policyer, katalogrättelser, Python/TypeScript-paritet, produkt- och UI-acceptans"
reviewed_heads:
  skills: "4ba7aec2917ed8256d0cc02bfb5aaaadb0031116"
  enkey-agents: "4f8bb578b17552277b596024982f5a8e0f86a241"
  neptune_academy: "9eccbfc8cafa3e4c3b10ba3d9c828d88dbaa575b"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
follows_handoff: "2026-09-11-001"
rechecks_review: "2026-09-11-008"
---

# Granskning av komplett Batch 1-leverans

## Beslut

**Changes required.** Leveransen är nu komplett i meningen att alla tre repon och de
beställda testlagren finns, och hela den körda verifieringssviten är grön. Den kan
ändå inte godkännas för aktivering eller push: det finns två kontraktsfel som skulle ge
fel tariffindata, testfixturerna döljer ett av felen och Telges redan lösta R11-spärr
ligger kvar.

De sex kandidaterna ska fortsätta vara inaktiva. Dispositionen är mekaniskt omverifierad
till **9/55/28**.

## P1 — alla sex saknar det obligatoriska bekräftade band-ID:t

Samtliga sex katalograder har
`capacity.band_selection="supplier_confirmed_band_id_required"`. V22 kräver därför en
`KravPost` med `vardetyp="band_id"`, `Tariffpolicy.kapacitet_band_bindning`, ett synligt
val bland tariffens verkliga band-ID:n och direkt transport som `vald_niva_id`. Automatisk
intervallmatchning från det numeriska kapacitetsvärdet får inte ersätta leverantörens
bekräftade band.

Ingen av de sex nya policyerna har denna kravpost eller bindning. En separat reproduktion
visar dessutom att `kontrollera_aktiveringsgrind(..., tariff=rå_tariff)` returnerar en
godkänd policy för var och en trots kombinationen
`supplier_confirmed_band_id_required` + `kapacitet_band_bindning=None`. Felet skulle
alltså inte fångas i den senare aktiveringsrundan.

Konsekvensen syns även i Batch 1-provet för Karlstad: 31 kW väljer automatiskt band 2 via
`_niva()`. Det är precis det V22-kontraktet förbjuder för dessa rader.

**Krav på rättning:**

1. Lägg till en unik, obligatorisk `band_id`-post och `kapacitet_band_bindning` för varje
   kandidatpolicy.
2. Låt UI:t visa faktiska band-ID:n/tydliga intervall och skicka valt ID genom hela
   produktkedjan.
3. Blockera saknat, tomt och okänt band-ID fältnära i båda språk.
4. Lägg en generell aktiveringspreflight som korsvaliderar den råa
   `band_selection`-markören mot policyns bandbindning. Därmed kan samma lucka inte
   återkomma i senare batcher.
5. Kör års-goldenfall och samtliga golv/tak med uttryckligt korrekt `vald_niva_id`, inte
   automatisk bandgissning.

Styrande avsnitt finns i `tariffinventering-v22.md` §6a.2 och tabellen med de sex
Batch 1-radernas 5/4/4/16/3/7 band.

## P1 — Övik kräver ett påhittat extrafält och modellerar fel leverantörsvärde

Öviks officiella 2026-prislista beskriver ett enda **kapacitetsbehov**, i kWh/dygn:
leverantören bestämmer det via energisignatur eller, om korrelationen är sämre än 0,7,
medelvärdet av de tre högsta dygnsförbrukningarna. Värdet avrundas till närmaste heltal
och har golvet 55 kWh/dygn. Kapacitetskostnaden är detta värde multiplicerat med
bandpriset i kr/kWh/år.

Den levererade policyn kräver i stället både:

- `ovik_debiterbar_effekt_kw`, ett kW-värde som källan inte använder i
  kapacitetskostnaden, och
- `hogsta_dygnsenergi_kwh`, som sedan övertrumfar det första värdet.

Användaren tvingas alltså mata in ett redundant eller påhittat kW-värde för att få
beräkna en kostnad. Benämningen "Högsta dygnsenergi" är också för snäv eftersom
leverantörens förstahandsmetod är energisignatur, och fältet saknar `heltal=True` trots
källans avrundningsregel.

Detta är den verkliga kod/käll-motsägelse som ursprungshandoffen sade skulle rapporteras
i stället för att lösas med en generell gissning. Källan är Övik Energis
[officiella prislista 2026](https://www.ovikenergi.se/download/18.22c9a27819936f83d5c305b2/1758525271448/Prislista%20giltig%20fr%C3%A5n%201%20jan%202026%20-%20n%C3%A4ringsidkare%20%C3%96rnsk%C3%B6ldsvik%20t%C3%A4tort.pdf).

**Krav på rättning:** modellera ett enda, sanningsenligt leverantörsfält,
`kapacitetsbehov` i kWh/dygn, heltal 55–71 999, plus det separata bekräftade band-ID:t.
Transportera kapacitetsbehovet som kapacitetsbas utan att kräva ett dummyvärde i kW och
utan att falla tillbaka på `kW × 24`. En liten explicit basbindning eller motsvarande
enkällslösning är acceptabel om den speglas fail-closed i båda språk och dokumenteras;
en ny beräkningsheuristik är det inte.

## P1 — produkt- och UI-fixturerna är inte tariffidentiska och ger falskt grönt Övik

`besparingsvardeBatch1.test.ts` och `KalkylatorPageBatch1.test.tsx` bygger samtliga sex
testtariffer med `kapacitet.enhet='kW'` och `kw_faktor=1`. Den riktiga Öviksposten har
`kWh/dygn` och faktor 24. Funktionen `hogstaDygnsenergiBas()` använder dessutom
`hogsta_dygnsenergi_kwh` endast när enheten är `kWh/dygn`.

Öviks produktentrytest fyller därför 500 kWh/dygn men fixturen ignorerar värdet; den
räknar 100 × 49,3 i stället för 500 × 49,3. Testet blir ändå grönt eftersom det bara
kräver en ändlig positiv kostnad. Samma fixturer innehåller bara första bandet och saknar
bandbindning, så de kan inte bevisa den verkliga kandidatprodukten.

**Krav på rättning:** bygg kandidatfixturerna i tariffens faktiska råform, helst från en
delad auktoritativ testfixture för att undvika tre manuella kopior. Kontrollera exakt
oberoende årsfacit och komponenter genom den publika produktvägen för alla sex; ett
`kostnad > 0`-påstående är inte acceptansbevis. Övik måste uttryckligen bevisa att rätt
kWh/dygn-bas och rätt band-ID når motorn.

## P1 — den bindande negativa-, band- och ARIA-matrisen saknas

Handoffen kräver för **varje obligatoriskt fält**: saknat, fel typ, icke-ändligt och
utanför deklarerad domän. Den kräver också samtliga relevanta bandgolv/-tak och svenska
fältfel/ARIA i UI:t.

Nuvarande prov täcker huvudsakligen normalfall och vissa saknade fält. Python har bara
enstaka gränser för Karlstad och Södertörn; produktprovet nöjer sig med positiv kostnad;
UI-provet kontrollerar att ett fel-element finns men inte korrekt `aria-invalid`,
`aria-describedby` eller labelkoppling. De 39 verkliga banden över de sex tarifferna
provas inte. Södertörns TypeScript-variantprov är tautologiskt: det visar bara att en
sträng med suffix skiljer sig från strängen utan suffix.

**Krav på rättning:** leverera den fulla parametriserade matrisen i Python och
TypeScript, inklusive alla band-ID:n/gränser och ett riktigt UI-prov per fälttyp. Prova
Södertörns blockering mot en fixture eller katalogrepresentation som faktiskt skulle
kunna innehålla varianten; kontrollera inte en mockad lista som konstruerats utan den.

## P1 — Telges lösta issue och R11 ligger kvar och blockerar framtida aktivering

V22 och Batchplan V22 säger uttryckligen att Telges gamla issue ska tas bort och att R11
ska tas bort ur `remaining_information_requests`, eftersom verifieringslistan redan har
bekräftat att tillsvidarevillkoren gäller. Den levererade katalogen har fortfarande:

- issue-texten om att kontrollera 2025-villkoren,
- `investigation.request_ids=["R11"]`, och
- den fulla R11-posten under `remaining_information_requests`.

Det motsäger leveransens uppgift att kontraktsbeviset är färdigt och lämnar en onödig
medlems-/aktiveringsspärr. Ta bort issue och R11 samt rätta sammanfattning och
revisionslogg. Behåll en sann `investigation.status="utreds"` med endast väntande
Batch 1-granskning/aktivering tills denna rättningsrunda är godkänd. Regenerera därefter
artefakt och proveniens från exakt katalogcommit.

## P2 — dokumentationsfel

- `policyregister.py` modultext säger fortfarande att övrig Familj 4/Telge ligger
  utanför registret. Det stämmer inte efter denna leverans.
- Karlstads Python-goldenkommentar räknar energin till 4 692,6 kr och anger
  `665,4 × 2`; de tolv värdena och det korrekta assertionen ger 5 358,0 kr med
  `665,4 × 3`. Rätta kommentaren så det dokumenterade facit inte motsäger testet.

## Det som är korrekt

- De tidigare 16 röda Pythonproven är reparerade utan att den riktiga kontraktsspärren
  försvagats.
- Katalog-SHA och den regenererade TypeScript-artefaktens proveniens matchar levererad
  katalogcommit.
- Alla sex policyer är current-only: MWh/aktuell årskostnad stöds och besparing samt
  kr/schablon blockeras fail-closed.
- Öviks fasta del är explicit noll och kalenderdagsperiodiseringen är rättad. Partilles
  `annual_forward` fungerar utan att okänd månadsperiodisering gissas.
- Inga kandidater har aktiverats och inget repo har pushats.

## Oberoende verifiering

- Python: **549 passed**.
- TypeScript: **26 testfiler, 681 passed**.
- `npx tsc --noEmit`: godkänd.
- Produktionsbygge: godkänt; genererad `dist` återställd.
- Självbärande E2E: **8 scenarier godkända**.
- `godkanda(katalog)`: exakt **9**; fortsatt **9/55/28**.
- `git diff --check`: rent i produktrepona vid verifieringen.

Grönt testutfall ändrar inte beslutet eftersom flera av de bindande scenarierna saknas
och Öviks produktfixture uttryckligen testar en annan kapacitetsform än katalogen.

## Exakt fortsatt uppdrag till Claude

1. Committera Codex kommunikationsändringar separat; ta inte med övriga ospårade filer.
2. Gör den generella råkatalog→policy-kontrollen för
   `supplier_confirmed_band_id_required`, och lägg `band_id`-krav/bindning på samtliga
   sex policyer.
3. Rätta Övik till ett enda källtroget kapacitetsbehov i kWh/dygn, heltal, utan dummy-kW
   eller ×24-gissning. Spegla den minsta explicita transporten i Python, TypeScript och
   UI.
4. Ta bort Telges inaktuella issue/R11 och uppdatera katalogens request-sammanfattning,
   change log, SHA och genererade proveniens.
5. Ersätt/reparera Batch 1-fixturerna så de återger verklig kapacitetsenhet, faktor,
   samtliga band och policybindningar. Kontrollera exakta publika årsfacit.
6. Slutför hela negativa-, bandgräns- och UI/ARIA-matrisen och ersätt det tautologiska
   Södertörn-provet med ett verkligt blockeringsbevis.
7. Rätta de två P2-kommentarerna, kör hela verifieringsmatrisen och logga nya fulla
   HEAD-hashar och exakt disposition. Stanna för ny Codex-granskning.

Ingen tariff får aktiveras och inget repo får pushas i rättningsrundan. Claude behöver
inte invänta ett nytt startbesked; detta är fortsatt arbete inom redan godkänt Batch 1-
scope.

Codex ändrade ingen katalog-, produkt-, policy-, motor- eller testkod i granskningen.
