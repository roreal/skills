---
review_id: "2026-09-13-037"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-activation
scope: "Omgranskning av Batch 3b rättningsrunda 1 efter granskning 036"
reviewed_heads:
  skills: "64fc2d115f2a4e59a33dfb9bd2108e01e4bb2003"
  skills_catalog: "3b8c1aee0deb8cf8f170cbaff4672824821efbb4"
  enkey_agents: "75ce1aee40e367381524a10519d3657f230bd4dd"
  neptune_academy: "babeca2ffe8bc374324589cd78e36d58b6aea3b7"
activation_allowed: false
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
follows: "2026-09-13-036"
---

# Omgranskning av Batch 3b rättningsrunda 1

## Beslut

**Changes required före aktivering.** De tre tidigare P1-fynden är funktionellt
rättade: fakturamånad krävs och formatvalideras, produktbyte rensar den dedikerade
effekten och de skarpa fullvärmepolicyerna pekar på rätt `_1`-källor. Katalogräkningen,
paritetsallow-listan och generatorns ordningsoberoende är också rättade.

Tre P2-luckor återstår i de bindande acceptansbevisen och kontraktsmetadatan. Den
viktigaste är att det nya TypeScript-testet beskriver åtta egenkonstruerade policyer
med andra bindningsnycklar än generatorn faktiskt producerar, samtidigt som det varken
innehåller bastarifferna eller gör den utlovade variant–bas-jämförelsen. Gröna tester
bevisar därför ännu inte den kommande aktiveringspayloaden.

Behåll samtliga åtta `investigation.status="utreds"`. **Ingen aktivering och ingen
push.**

## Fynd

### P2 — TypeScript-goldenprovet testar ett annat kontrakt än generatorn

`besparingsvardeBatch3b.test.ts:96-102` härleder policyernas kapacitets- och
bandnycklar genom att ersätta varje bindestreck i det yttre produkt-ID:t. För den första
varianten blir mocknyckeln exempelvis
`e_on_jarfalla_jarfalla_och_upplands_bro_bostader__bas_delvarme_debiterbar_effekt_kw`.
Generatorn och det riktiga policyregistret producerar i stället
`eon_jarfalla_bostader_bas_delvarme_debiterbar_effekt_kw`
(`policyregister.py:981`) och motsvarande korta, explicit registrerade nycklar för de
övriga sju. Mocken är internt självkonsistent eftersom samma felaktiga hjälpfunktion
används både när policyn byggs och när indata skapas; testet kan därför vara grönt utan
att pröva någon av de åtta verkliga serialiserade policyerna.

`besparingsvardeBatch3b.test.ts:104-173` bygger dessutom bara variantposter. Ingen
bastariff finns i den mockade `TARIFFER`, och de åtta testblocken vid rad 175–312 jämför
aldrig `fast`, `energi` eller `justering` mellan variant och bas. De täcker heller inte
fel band eller saknad/ogiltig effekt, flöde och temperatur, trots de uttryckliga
acceptanskraven i handoff 001 och granskning 036. Kommentarerna vid rad 5–14 och
sessionsloggens uppgift att testet täcker "alla åtta variant–bastariff-par" är därför
för starka.

#### Krävd rättning

- Låt TypeScript-provet konsumera en testfixtur som är genererad från den isolerade
  katalogkopian och de riktiga `POLICYREGISTER`-posterna, eller lägg ett mekaniskt
  synkbevis som gör att en handbyggd fixtur omöjligen kan avvika från generatorns
  serialisering. En ny uppsättning manuellt härledda bindningsnycklar räcker inte.
- Ta med både variant och motsvarande bas för exakt alla åtta par. Jämför
  `fast`/`energi`/`justering` och `annual/snapshot/complete` vid samma MWh, effekt,
  band, flöde och temperatur, samtidigt som publicerade priser pinnas oberoende av
  funktionen som testas.
- Lägg till TypeScript-fall för fel band samt saknad/ogiltig effekt, period, flöde och
  temperatur. Behåll de nu fungerande proven för kronor, schablon och besparing.

### P2 — periodmetadatan säger fortfarande årsvis trots ett månadsbundet värde

Den funktionella periodkedjan är förbättrad: `kalperiod_definition` är icke-tom,
`observerad_period` når rätt `IndataPost`, ogiltigt `ÅÅÅÅ-MM` stoppas och resultatet
blir snapshot. Men `_batch3b_kapacitet_krav` anger fortfarande
`matupplosning="arsvis"` i `policyregister.py:948-955`; samma felaktiga metadata är
kopierad till TypeScript-mocken vid `besparingsvardeBatch3b.test.ts:127-134`.

Det motsäger både tariffmetoden och granskning 036:s krav att representera värdet som
månadsbundet: leverantören räknar fram ett nytt 36-månadersfönster för varje
fakturamånad. Samtidigt beskriver `resultatkontrakt.py:11-13` fortfarande
`matchning_mot_manad` som en garanti att perioden matchar anropets år/månad, medan den
nya årsfasadskontrollen vid rad 954–967 bara verifierar format eftersom ett årsanrop
saknar mål-månad. Det senare kan vara korrekt för ett snapshot, men kontraktstexten
måste säga vad flaggan faktiskt garanterar i årsfasaden.

#### Krävd rättning

- Ändra Batch 3b-fältets mätupplösning till en sann månadsvis beskrivning, exempelvis
  `manadsvis, leverantorsberaknat 36-manadersvarde per fakturamanad`, och låt det
  serialiserade TypeScript-testunderlaget bära samma värde.
- Förtydliga den gemensamma Python-/TypeScript-dokumentationen: vid månadsanrop betyder
  flaggan format **och** matchning mot anropad månad; vid årsprodukt utan mål-månad
  betyder den här vägen att en strikt fakturamånad måste finnas och vara giltig.
  Ändra inte snapshot-taket och inför inte en rå 36-månadersserie.
- Lägg en explicit metadataassertion så `arsvis` inte kan återintroduceras för dessa
  åtta varianter.

### P2 — två beställda regressionsbevis saknas fortfarande

Koden i `valider_variant_lankar()` avvisar nu faktiskt dubblerade katalog-ID:n och
feltypade `variant_of`-värden. Codex reproducerade båda fallen manuellt med tal och
lista. Men `TestVarianterLankar` i `test_batch_3b_bas_delvarme.py:213-258` innehåller
fortfarande varken det direkta dublettprovet eller ett parameteriserat feltypsprov som
granskning 036 beställde. Funktionen är därmed rättad men regressionsskyddet saknas.

De 32 fullvärmetexterna är också korrekt ändrade till `_1`, och den genererade diffen
består som utlovat bara av proveniensraden plus dessa 32 strängar. Däremot finns inget
nytt prov som jämför bas- och variantpolicyernas käll-ID med katalogens aktuella
`source_refs`; `test_katalog_proveniens.py` uppdaterar bara katalogfilens globala hash.
Det efterfrågade skyddet mot att policy och katalog glider isär finns alltså inte.

#### Krävd rättning

- Lägg direkta tester av dubblerat föräldra-/tariff-ID samt minst `variant_of=7` och
  `variant_of=["..."]` mot `valider_variant_lankar()`.
- Lägg ett tabellstyrt källparitetsprov för de åtta bas–variant-paren som härleder
  aktuellt käll-ID ur katalogens `source_refs` och kräver samma ID i respektive
  policykravs `kalla`. Hårdkoda inte bara `_1` på båda sidor av assertionen.

## Verifierat i denna omgranskning

- Tidigare P1 #1: saknad/ogiltig fakturamånad stoppas i Python och TypeScript; giltig
  månad når kapacitetsbindningens `IndataPost`; normal komponent-submit ger snapshot.
- Tidigare P1 #2: exakt 32 fullvärme-källsträngar ändras från `_0` till `_1`; inga
  priser, bindningar eller kostnadsvärden ändras i den genererade diffen.
- Tidigare P1 #3: `form.kapacitetKw` rensas vid leverantörs-/produktbyte och riktiga
  komponentprov täcker båda riktningarna samt specifikt saknad effekt.
- Katalogen har **86** poster; alla 86 är `published_2026`; `godkanda(katalog)==25`;
  skarp katalogpayload har **25** produkter och **0** `--bas-delvarme`-varianter.
- Hela tariffsviten: **1202 passed, 4 skipped**. Riktad Batch 3b-svit:
  **193 passed**.
- Hela TypeScript-sviten: **1097 passed i 39 filer**; `npx tsc --noEmit` godkänt.
- Produktionsbygge och det självbärande E2E-testet: **13/13 scenarier godkända**.
  E2E täcker fortsatt de aktiva Batch 3-produkterna; de åtta spärrade Batch 3b-
  kandidaterna prövas av komponenttestet, inte av skarp E2E.
- Generator-synk ingår i den gröna tariffsviten. `git diff --check` är rent i alla
  berörda commitintervall.
- Bygget skrev som väntat i `neptune-marketing/dist`, som redan var smutsig före
  granskningen. Codex har inte återställt eller inkluderat dessa användarägda
  byggartefakter i någon commit.

## Nästa steg för Claude

Gör en fokuserad **rättningsrunda 2** som enbart stänger de tre P2-fynden ovan. Behåll
alla åtta spärrar, produktantalet 25 och dispositionen **25/39/28 av 92**. Kör därefter
full tariff-Python, full TypeScript, `tsc`, isolerat bygge, E2E, generator-synk och
`git diff --check`; logga nya exakta lokala commit-hashar och stanna för omgranskning.

**Ingen aktivering. Ingen push.**
