---
review_id: "2026-09-10-009"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "Lokal Batch 5d-implementation för Lidköping Energi 0–41 kW och 42+ kW"
  - "Katalog, Pythonmotor, TypeScriptmotor, produktentry, UI och acceptansbevis"
reviewed_heads:
  skills: "0dbba6a"
  skills_product_commit: "d7eb655f2962d057b5d3ebdc2dbf45bfac3729a4"
  enkey-agents: "25b97acb3bfe45858a8ce4ee9e343352d8c8c083"
  neptune_academy: "760bf766b49f978d98a1e486bac5a7a5ea23558a"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_handoff: "2026-09-10-001"
---

# Kodgranskning av Lidköping Batch 5d

## Beslut

**Changes required.** Den signerade månadsjusteringen är korrekt kopplad genom de nya
Python- och TypeScriptmotorerna i huvudfallet, men Batch 5d är inte redo för aktivering
eller push. Två kostnadskritiska P1-fynd och tre P2-fynd återstår.

Ingen tariff har aktiverats och inga produktrepon har pushats. Dispositionen ska ligga
kvar på 7 implementerade / 57 redo / 28 blockerade av 92.

## Fynd

### P1 — katalogens minsta debiteringsgrund tappas och produktgränserna är inte auktoritativa

Katalogen anger `minimum_billing_basis: 3` för båda Lidköpingsposterna, men
`till_prisar()` transporterar inte fältet. Den delade Lidköpingspolicyn sätter samtidigt
`minvarde=0`, och TypeScripts `kapacitetsGolv()` härleder bara golvet från det lägsta
bandets `min`. För produkten 0–41 kW blir golvet därför 0 i stället för 3.

Oberoende reproduktion genom den publika `beraknaArsprodukt`-entryn, med en isolerad
testinjektion av den ännu inaktiva tariffposten, accepterade både 0 och 1 kW som
`complete`. Pythonfasaden accepterade 1 kW och räknade 6 734 kr exklusive moms i stället
för att blockera eller använda minsta debiteringsgrund. Samma delade policy accepterade
även 5 kW för produkten 42+ vid ett direkt fasadanrop och gav 23 317 kr exklusive moms.

Rättningen ska bevara och tillämpa katalogens minsta debiteringsgrund genom hela kedjan
och samtidigt sätta tariffspecifika produktgränser:

- 0–41 kW: min 3, max 41;
- 42+ kW: min 42.

Det bekräftade band-ID:t ska fortsatt vara auktoritativt; rättningen ska inte börja
gissa eller räkna om bandet från effekttalet. Lägg gränstester genom Pythonfasaden,
TypeScripts publika produktentry och det verkliga formuläret: 2/3/41/42 kW för den första
produkten samt 41/42 kW för den andra.

### P1 — den nya justeringstypens payload passerar grinden utan schemavalidering

`okand_justering()` verifierar bara att strängen
`signed_monthly_flow_adjustment` finns i registret. Den kontrollerar inte `faktor_n` eller
de tre fältnamnen. En oberoende katalogmutation med `faktor_n=0` passerade grinden och gav
`complete` med noll i justering, alltså ett tyst för lågt pris.

Grinden ska för denna typ kräva ett ändligt positivt numeriskt `faktor_n` samt tre
icke-tomma strängnycklar för volym, kundavkylning och nätavkylning. Kontrollera även att
bindningarna kan kopplas till rätt obligatoriska `number_series`-krav och att ändringen
speglas där generator-/TypeScriptkontraktet behöver det. Lägg negativa mutationstester
för saknad/feltypad/noll/icke-ändlig faktor och saknade eller ogiltiga fältnamn. Felaktig
katalogdata ska avvisas före kostnadsberäkning.

### P2 — det uttryckligen beställda produkt- och UI-beviset saknas

Den nya TypeScripttestfilen dokumenterar själv att den inte anropar
`beraknaArsprodukt`, besparingsprodukten eller `KalkylatorPage`. I stället testas den lägre
motorn och två capability-hjälpare mot en syntetisk prispost. Det uppfyller inte handoffens
krav på den verkliga produkt- och UI-kedjan.

Att tarifferna ska förbli inaktiva är inte ett tekniskt hinder för testen. Codex
reproducerade P1-felet ovan genom att injicera en testlokal katalogpost i den importerade
genererade datastrukturen, utan att ändra eller aktivera produktionskatalogen. Använd samma
princip, alternativt en temporärt genererad testartefakt från en katalogkopia.

Acceptansproven ska visa att:

- `beraknaArsprodukt` ger aktuell uppskattad årskostnad i bekräftat MWh-läge för båda
  produkterna;
- kr-inversion och schablon blockeras och besparingsvägen kastar `Produktbegransning`;
- den riktiga `KalkylatorPage` renderar tre tolvmånadersserier januari–december med rätt
  enheter och hjälptexter, kräver attestering av nätets `Tm`, visar fältnära fel och inte
  kan kringgå de blockerade lägena.

### P2 — bara 0–41 kW har goldenfall och flera avtalade gränsbevis saknas

Både Python- och TypeScripttestet hårdkodar endast tariff-ID:t och priserna för 0–41 kW.
Leveransrapportens uppgift om ett handräknat goldenfall *per tariff* stämmer därför inte.
Testerna verifierar inte heller total inklusive moms, 1/12-periodiseringen eller ett
icke-ändligt serieelement, trots att samtliga ingick i acceptanslistan.

Lägg ett katalogbundet, handräknat goldenfall för vardera tariffen och spegla samma
referensfall i TypeScript. För nuvarande provdata (1 MWh, 10 m³, T=30 °C och Tm=40 °C i
varje månad) är faciten:

- 0–41 kW, 5 kW, band 1: fast 9 530, energi 4 678, justering 150, summa exkl. moms
  14 358 och summa inkl. moms 17 947,50 kr;
- 42+ kW, 42 kW, band 1: fast 66 984, energi 4 912, justering 150, summa exkl. moms
  72 046 och summa inkl. moms 90 057,50 kr.

Verifiera dessutom att kapacitetsdelen verkligen fördelas med 1/12 per månad och summerar
till årsbeloppet, samt att `NaN`/oändlighet i var och en av de tre serietyperna blockeras
fältnära i båda språk.

### P2 — katalogens status- och källmetadata motsäger den implementerade modellen

De båda katalogposterna säger fortfarande att månadsperiodisering saknas, samtidigt som
`monthly_proration` nu är satt till `1/12`. Nya `faktor_n=5`, den tvåsidiga formeln och
periodiseringsbeskedet hänvisar dessutom bara till `source_id: 20_1`, som är
Normalprislista 2025. Den leverantörssvarskälla som faktiskt löste frågorna den
9 september 2026 finns bara i konversationsgranskningen.

Rensa den inaktuella periodiseringsfrågan ur `issues` och `conditions_sv` när dess test är
på plats. Behåll den relevanta upplysningen att leverantörens debiterbara effekt måste
användas. Lägg till en icke-känslig, katalogbunden proveniens för 2026-priserna och
leverantörssvaret (datum, SHA-256 och gransknings-ID räcker för den privata källan) och
knyt båda tariffposterna till den. Den råa e-post-PDF:en får fortsatt inte committas.
`investigation.status` ska ligga kvar på `utreds` som aktiveringsspärr under
rättningsrundan.

## Det som är godkänt i sak

- Formeln `5 × Q_m × (1 − T_m/Tm_m)` räknas månadsvis och summeras till
  `Kostnad.justering` i båda motorerna.
- Positiv avgift, noll och negativ kreditering fungerar utan nollklämning.
- Saknad serie, fel kardinalitet, `Tm <= 0`, saknad attestering och okänt band-ID stoppas
  i de provade motorvägarna.
- Det oberoende referensfallet för 0–41 kW gav samma delbelopp i Python och TypeScript.
- Ingen tariff är aktiverad; den genererade produktionsartefakten innehåller fortsatt sju
  godkända tariffer.

Detta är delgodkännanden av beteenden, inte ett slutgodkännande av commitkedjan.

## Oberoende verifiering

- Python: `414 passed`; endast sandboxrelaterad pytestcache-varning.
- TypeScript: 18 testfiler och `497 passed`.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; befintlig bundle-varning, genererade `dist`-ändringar
  återställda.
- `npm run test:e2e`: godkänd för de två befintliga scenarierna riksgenomsnittet och
  Sandviken; provet omfattar inte Lidköping.
- Oberoende Pythonanrop verifierade båda korrekta goldenbeloppen, 1 kW-felet,
  42+-produktens 5 kW-lucka och att `faktor_n=0` passerar.
- Oberoende TypeScriptprov genom den publika `beraknaArsprodukt`-entryn verifierade att
  0 och 1 kW accepteras för 0–41-produkten.
- `git diff --check` är rent för de granskade commitintervallen. Produktrepona är rena;
  sedan tidigare orelaterade filer i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Rätta endast de fem fynden ovan på de nu granskade lokala commitkedjorna. Aktivera ingen
tariff, regenerera inte in Lidköping i produktionsurvalet och pusha inget repo. Gör
fokuserade commits per berört repo, kör hela Python-/TypeScriptmatrisen, typkontroll,
produktionbygge, självbärande E2E och `git diff --check`, och rapportera exakta nya HEAD-
hashar i Batch 5d-sessionen. Stanna därefter för ny Codex-omgranskning.
