---
review_id: "2026-09-09-006"
date: "2026-09-09"
reviewer: Codex
status: source-approved-with-runtime-input
scope:
  - Fjarrvarmetariffer/Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf
  - Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md
  - lidkoping-energi-lidkoping-041-kw-2026
  - lidkoping-energi-lidkoping-42-kw-2026
reviewed_head:
  skills: "f4f23702eccf8480022eab177a0aee6b9a20224c"
source_sha256: "93b47766933ba2cd6c841db982cc0981a4b44ec39fe08ff543b3c707746e8f34"
implementation_changed: false
push_status: local-unpushed-not-approved
supplements_review: "2026-09-09-005"
feeds_next_review: "2026-09-09-007"
---

# Bedömning av Lidköping Energis leverantörssvar 2026

## Beslut

Lidköping Energis skriftliga svar den 9 september 2026 löser de externa sakfrågor som
blockerade båda företagstarifferna. Följande två bastariffer ska i nästa inventering flyttas
från `blocked_external_info` till `ready_to_implement`:

- `lidkoping-energi-lidkoping-041-kw-2026`
- `lidkoping-energi-lidkoping-42-kw-2026`

Beslutet betyder källmässigt redo, inte redan implementerad eller fakturaverifierad. Den
månadsvisa flödeskomponenten kräver fortfarande verklig beräkningsindata. Saknas den ska
beräkningen blockeras; den får inte ersättas med noll eller ett uppskattat standardvärde.

Dispositionen ändras därmed från 7/55/30 till **7 implementerade / 57 redo / 28
blockerade**, fortfarande 92 totalt. På basnivå blir fördelningen 7/47/24; varianterna är
oförändrade 0/10/4.

## Källan

Lokalt arkiverat e-postsvar:
`Fjarrvarmetariffer/Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf`.

- Avsändare: Lidköping Energis värmenätschef.
- Svarsdatum: 2026-09-09 10:07.
- Relevanta sidor: 1–2.
- SHA-256:
  `93b47766933ba2cd6c841db982cc0981a4b44ec39fe08ff543b3c707746e8f34`.
- PDF:en är tre sidor. Sida 3 innehåller bara namnet på en separat bilaga,
  `prismodell komersiella.pdf`; bilagan är inte inbäddad i den arkiverade PDF:en.

Råfilen innehåller kontaktuppgifter och ska inte läggas till i git eller pushas utan
Roberts uttryckliga beslut. Denna granskningsanteckning bevarar de tekniska svaren utan
kontaktuppgifterna och binder dem till originalfilens hash.

## Bekräftade tariffvillkor

Leverantörssvaret bekräftar följande för 2026:

1. De publicerade företagspriserna ska läsas **exklusive moms**. Påståendet ”inklusive
   moms” på den ena webbsidan är fel. Katalogens nuvarande `vat_basis: "excluded"` är
   därmed korrekt.
2. Flödesavgift eller flödespremie gäller samtliga kommersiella kunder i prisgrupp 2–5,
   vilket täcker båda katalogprodukterna ovan.
3. Flödesprisfaktorn är `N = 5 kr/m³`.
4. Formeln är fortsatt `N × Q × (1 − T/Tm)`.
5. `Tm` är nätets månadsvisa medel av samtliga anläggningars
   `T_in − T_ut`, alltså nätets månadsmedelavkylning.
6. Komponenten gäller alla månader och debiteras eller krediteras månadsvis.
7. Debiterbar effekt bestäms i första hand med en effektsignatur vid −10 °C, byggd av
   dygnsvärden december–februari under de två senaste vintrarna, och i andra hand av högsta
   uppmätta dygnsmedeleffekt. Den redan beslutade säkra produktvägen kan fortsatt kräva
   leverantörens fastställda effekt i stället för att försöka återskapa signaturen.
8. De publicerade fasta årsavgifterna och effektavgifterna periodiseras med en tolftedel per
   månad.

## Beräkningskontrakt för implementation

Lidköping passar inte i batch 5b:s enkla `volume`-modell. Den behöver en egen liten batch,
förslagsvis **batch 5d — Lidköping nätmedelavkylning**, efter batch 0:s serie- och
policyindatastöd.

Den statiska tariffparametern är `N = 5 SEK/m³` exklusive moms. För varje månad `m` ska
motorn beräkna en signerad justering:

```text
flödesjustering_m = 5 × Q_m × (1 − T_m / Tm_m)
årsjustering = summan för månad 1–12
```

Här är:

- `Q_m`: kundens uppmätta fjärrvärmevolym i m³ för månaden;
- `T_m`: kundens månadsmedelavkylning `T_in − T_ut` i °C;
- `Tm_m`: Lidköpingsnätets månadsmedelavkylning i °C, som leverantörsvärde.

Alla tre serierna ska ha exakt 12 värden och samma kalenderordning. `Q_m` ska vara ändlig
och minst noll; `T_m` ska vara ändlig; `Tm_m` ska vara ändlig och strikt större än noll så
division med noll aldrig kan ske. Formeln ska inte klämmas till noll: positivt belopp är
avgift och negativt belopp är premie/kreditering enligt den bekräftade tvåsidiga modellen.

Övrig obligatorisk produktindata är bekräftad energi i MWh, leverantörens debiterbara
effekt och det bekräftade effektband som den redan planerade
`selected_band_affine`-mekanismen kräver. Om någon obligatorisk serie eller kapacitetsuppgift
saknas ska tariffen ge ett typat, fältnära blockerat resultat.

E-postsvaret anger hur `Tm` bestäms men innehåller inte de tolv faktiska månadsutfallen och
bekräftar inte att de alltid visas på kundfakturan. Det är därför ett **runtimekrav**, inte
ett statiskt katalogvärde. Kalkylatorn får använda värden från faktura eller direkt
leverantörsbesked; utan dem ska Lidköpings fullständiga tariff inte räknas. Resultatet ska
visas som `uppskattat` tills ett konkret kundfall har fakturaverifierats.

## Tillägg till Claudes V16-beställning

V15 levererades medan denna källbedömning pågick. V16 ska därför svara på både
omgranskning `2026-09-09-007` och denna källbedömning:

1. Uppdatera `verifieringslista-fjarrvarmebolag.md`: markera båda Lidköpingstariffernas
   externa källunderlag godkänt 2026-09-09 och återge de åtta bekräftelserna ovan. Skilj
   källgodkännande från kvarstående implementation/fakturavalidering.
2. Flytta båda raderna till `ready_to_implement` i `tariffinventering-v16.md`, ersätt den
   gamla texten om saknade `N`/`Tm` och ange den nya lokala källans hash/proveniens.
3. Ändra räkningskontrollen till 7/57/28 av 92 och basfördelningen till 7/47/24;
   variantfördelningen 0/10/4 är oförändrad.
4. Lägg en separat batch 5d med de två Lidköpingstarifferna i `batchplan-v16.md`; justera
   batchsumman från 55 till 57 och de ej batchade bastarifferna från 26 till 24.
5. Specificera en ny, deklarativ justeringstyp för den signerade månadsformeln ovan,
   speglad i Python och TypeScript, samt tre 12-värdesserier med tydliga enheter,
   kalendermånader och fail-closed-validering. Återanvänd batch 0:s
   `number_series`-/policyfältmekanism.
6. Planera katalogens framtida källpost, `adjustments`-post, lösta
   `investigation`-villkor, `POLICYREGISTER`, generering, UI och golden-/gräns-/negativtester.
   Ändra inte JSON eller produktkod i den här dokumentationsrundan.
7. Testplanen ska omfatta positiv avgift (`T < Tm`), noll (`T = Tm`), negativ premie
   (`T > Tm`), `Tm = 0`, fel serielängd, saknad månad, moms och 1/12-periodisering.
8. Bevara V15:s korrekta rättningar av argumentbyggaren och parsergrindarna och rätta dess
   återstående årsprodukt-/`policyFalt`-fynd enligt granskning `2026-09-09-007`; Lidköping
   är ett tillägg, inte en ersättning för dem.
9. Lägg till denna granskningsanteckning och omgranskning `2026-09-09-007` i den fokuserade
   dokumentationscommitten. Staga
   inte den råa e-post-PDF:en utan separat beslut från Robert. Ingen produktkod,
   tariffdata, tariffaktivering eller push är godkänd.
