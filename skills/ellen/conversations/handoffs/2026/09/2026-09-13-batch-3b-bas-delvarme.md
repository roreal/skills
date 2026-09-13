---
handoff_id: "2026-09-13-001"
created_at: "2026-09-13T20:48:10+02:00"
from: Codex
to: Claude
status: changes-required-after-local-implementation
implementation_allowed: true
approved_implementation_scope: "batch-3b-eon-navirum-bas-delvarme-36-month-supplier-value"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
latest_review: "2026-09-13-036"
baseline_remote_heads:
  skills: "19c68fe95e52492b58cc24965ef39a1083a655c8"
  enkey_agents: "4b1d4b6d78c010a4722f54df833ab7903431e9dc"
  neptune_academy: "55731894428d7fe43be00b9ddf36dad2597e8098"
tariff_disposition_before: "25 implemented / 39 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "25 implemented / 39 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "33 implemented / 31 ready / 28 blocked av 92"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 3b"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §5, §6a.2 och §6a.5"
  - "Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md — E.ON/Navirum"
  - "conversations/reviews/2026/09/2026-09-13-beredskapskontroll-batch-3b.md"
---

# Uppdrag till Claude: Batch 3b — E.ON/Navirum bas-/delvärme

## Mål

Implementera lokalt exakt åtta separata bas-/delvärmeprodukter för E.ON och Navirum.
Kalkylatorn ska använda leverantörens redan beräknade debiterbara effekt för
fakturamånaden: medelvärdet av de tre högsta uppmätta dygnsmedeleffekterna under de
föregående 36 månaderna inklusive fakturamånaden.

Bygg **ingen** rå 36-månadersserie, topp-tre-algoritm eller ny kostnadsmotor. Årspriset
räknas med den redan pushade Batch 3-motorn och samma energi-, effekt- och golvfria
flödespriser som respektive bastariff.

Detta är en implementationsfas. **Ingen variant aktiveras och inget repo pushas.**

## Exakt tariffomfattning

1. `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026--bas-delvarme`
2. `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026--bas-delvarme`
3. `e-on-malmo-malmo-och-burlov-bostader-2026--bas-delvarme`
4. `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026--bas-delvarme`
5. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026--bas-delvarme`
6. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026--bas-delvarme`
7. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026--bas-delvarme`
8. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026--bas-delvarme`

Varje variant ska bära `variant_of` med exakt motsvarande ID utan
`--bas-delvarme`. Ändra inte Kraftringens `--brunnshog`-variant eller någon annan batch.

Bygg en liten generisk `variant_of`-validering i katalogvägen och anropa den från
`godkanda()`: föräldern ska vara ett befintligt, unikt katalog-ID, får inte vara samma rad
eller själv vara en variant och ska ha samma `member_id` och `price_year`. Saknat/feltypat
ID, kedja eller avvikelse ska kasta före produktgenerering. Lägg negativa tester för varje
fall; härled inte föräldern från suffixet.

## Katalog och källproveniens bakom spärren

1. Lägg in de åtta variantposterna i
   `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json`, nära respektive bastariff.
2. Kopiera följande prissättande fält byte-/värdemässigt från bastariffen:
   `member_id`, `customer_scope`, `price_year`, giltighet, `price_status`, `vat_basis`,
   `currency`, `energy`, kapacitetsband/priser/enheter/periodisering, `adjustments` och
   källkoppling. Den enda avsiktliga kapacitetsskillnaden är
   `billing_basis_method`, som ska beskriva 36-månadersregeln ovan.
3. Sätt `contract_required:true`. Lägg varje ny rad bakom en ren lokal
   `investigation.status="utreds"`-implementationsspärr utan koppling till en extern
   informationsförfrågan. Behåll den kända månadsperiodiserings-issuen; den blockerar
   månadsprodukt, inte framtida `annual_forward`.
4. Gör produktnamnen entydiga: befintlig bastariff får suffixet `Fullvärme`; motsvarande
   variant får `Bas-/delvärme`. Ändra inga befintliga produkt-ID:n eller kostnadsvärden.
5. Lägg till de fyra nya 2026-källposterna `03_1`, `04_1`, `25_1`, `26_1` enligt
   beredskapskontroll 035. Hämta de officiella PDF-bytesen, lagra verklig SHA-256 och
   `retrieved_on`, lägg käll-ID:t i rätt medlemsrad och byt de åtta bastariffernas samt de
   åtta varianternas `source_refs` till rätt `_1`-källa med sidorna 1–2. Bevara `_0`
   oförändrade som historiska källor. Inga rå-PDF:er ska committas.
6. Höj schema-/katalogrevisionen och uppdatera levande omfattningsmetadata från 78 till
   **86 katalogposter = 78 bastariffer + 8 materialiserade varianter**. Detta ändrar inte
   projektets fasta kontrollmängd 92 eller dispositionen under implementationsfasen.
   Dokumentera samtidigt `variant_of`-relationen i katalogens `integration_contract`.
7. Uppdatera bara levande 78-räkningsassertioner/kommentarer som faktiskt avser
   `len(katalog["tariffs"])`; bevara historiska designdokument som uttryckligen beskriver
   den ursprungliga 78-raderskatalogen.

## Generatorns stabila variant-ID

Utöka `_stabilt_tariff_id` generiskt så att:

- `...-2026` fortsätter bli `...`;
- `...-2026--bas-delvarme` blir `...--bas-delvarme`;
- variantsuffixet aldrig tappas;
- andra år och omkastad katalogordning ger samma deterministiska regel;
- en basprodukt och dess variant aldrig kan kollidera eller skriva över varandra.

Lägg isolerade positiva och negativa generatorprov. Hårdkoda inte de åtta ID:na i själva
ID-algoritmen.

## Tariffpolicyer

Bygg åtta egna `Tariffpolicy`-poster, gärna via en parametriserad Batch 3b-byggare:

- `tackning=frozenset({"annual_forward"})`;
- `stodjer_aktuell_arskostnad=True`;
- `stodjer_besparing=False`;
- `flodeskorrigering_variant="golvfri"`;
- skalär debiterbar effekt via en unik `kapacitet_bindning` per variant;
- bekräftat nivå-ID via en unik `kapacitet_band_bindning` per variant, även om raden har
  ett enda band;
- befintliga policybundna `flode_m3` och `framledningstemperatur_c`;
- endast `supplier_value`, `rullande=True`, icke-negativ effekt och metadata/hjälptext som
  uttryckligen anger bas-/delvärme, tre högsta dygnsmedeleffekter, föregående 36 månader,
  inklusive fakturamånaden och att värdet ska läsas från faktura/leverantör;
- inget fält för råa 36 månaders mätvärden och ingen intern beräkning av topp tre.

Källperioden/observerad period ska vara fakturamånaden i det befintliga
snapshot-kontraktet. Samma fyra kontraktsfält som fullvärmeprodukten visas: debiterbar
effekt, bekräftat band, flöde och medelframledningstemperatur. Formuleringen i Batchplan
V22 om "tre fält, ingen fjärde" förbjuder ett separat 36-månadersfält; den tar inte bort
det generiska band-ID-kravet som redan gäller dessa katalograder.

## Paritet och skydd mot katalogdrift

Lägg ett tabellstyrt test över samtliga åtta variant–bastariff-par som bevisar att:

- alla prisbärande data är lika: tolv energipriser, kapacitetsbandens ID/intervall/fasta
  och rörliga belopp, rate period, enhet, fast avgift, moms och flödesjustering;
- medlem, kundscope, prisår och officiell 2026-källa är lika;
- endast effektmetod, ID, etikett, `variant_of` och spärrstatus skiljer;
- den nya policyn pekar på variant-ID:t och inte på bastariffen;
- fullvärmepolicyns hjälptext/nycklar och kostnadsresultat inte skrivs över.

Testet ska använda explicita tillåtna skillnader och falla på en oväntad avvikelse, inte
normalisera bort hela objektfält som senare kan börja bära priser.

## Acceptansbevis före aktivering

1. Alla åtta varianter finns i katalogen men `godkanda(katalog)` är fortsatt exakt **25**.
   Med 86 katalogposter ska grindens avslag räknas om medvetet; åtta nya poster ska
   stoppas av implementationsspärren, inte av okänd formel eller saknad policy.
   Variantvalideringen ska samtidigt acceptera exakt åtta giltiga föräldrakopplingar och
   kasta på okänd förälder, självreferens, variantkedja samt fel medlem/prisår.
2. En isolerad katalogkopia där exakt Batch 3b-spärrarna rensas ska generera exakt åtta
   nya, unika, årsoberoende produkt-ID:n och totalt 33 katalogprodukter. Den skarpa
   incheckade tariffpayloaden ska under denna fas inte innehålla något
   `--bas-delvarme`-ID.
3. Tabellstyrda Python- och TypeScript-goldenprov ska täcka alla åtta. Vid samma MWh,
   effekt, band, flöde och temperatur ska variant och bastariff ge samma kostnadsdelar;
   facit ska samtidigt pinna publicerade priser oberoende av motorn som testas.
4. Resultatstatus är `annual/snapshot/complete`, aldrig `exact`. Saknad eller ogiltig
   effekt, observerad period, band, flöde eller temperatur ska blockera/fela fältnära
   enligt befintligt kontrakt.
5. Kronor och schablon ska blockeras med `unsupported_input_mode`; besparing med
   `besparing_ej_stodd`. Ingen månadsfaktura ska godkännas.
6. Ett riktigt komponenttest med injicerad kandidat ska visa ett entydigt
   `Bas-/delvärme`-val, exakt de fyra policyfälten, 36-månadershjälptext, normal submit och
   snapshot-resultat. Ett syskontest ska visa det separata `Fullvärme`-valet och att dess
   hjälptext fortfarande beskriver fullvärmemetoden.
7. Testa produktbyte mellan fullvärme och bas-/delvärme så att effekt, band och
   observerad period inte återanvänds tyst under fel policynyckel. Flöde/temperatur får
   bara återanvändas om befintlig generisk state-policy uttryckligen gör det och testet
   visar att periodkravet fortfarande är uppfyllt.
8. Uppdatera `tariffinventering-v22.md`/`batchplan-v22.md` endast med faktisk
   implementation bakom spärr. Flytta inte de åtta `ready_to_implement`-dispositionerna
   till implemented före den separata aktiveringsrundan.

## Leveransordning

1. Gör katalog-, källa-, policy-, generator-, dokumentations- och teständringarna ovan.
2. Regenerera artefakten med korrekt katalogproveniens. Före aktivering får diffen bara
   ändra proveniens och de åtta befintliga produkternas `Fullvärme`-etiketter; produktmängd,
   produkt-ID:n och alla pris-/policyvärden ska vara oförändrade. Inget
   `--bas-delvarme`-ID får finnas i den skarpa payloaden ännu.
3. Kör full Python, full TypeScript, `npx tsc --noEmit`, isolerat bygge, E2E,
   generator-synk och `git diff --check` i relevanta repon.
4. Redovisa exakt att katalogen har 86 poster, `godkanda(katalog)==25`, skarp payload har
   25 katalogprodukter och projektets disposition är **25/39/28 av 92**.
5. Commitera fokuserat lokalt per repo, logga exakta commit-hashar och testresultat i
   `conversations/sessions/2026/09/2026-09-13-batch-3b-bas-delvarme.md` och stanna för
   Codex granskning.

**Ingen aktivering och ingen push i denna etapp.** Rör inte användarens orelaterade
arbetskopiefiler eller byggartefakter.

## Codex granskning 2026-09-13-036

Den första lokala leveransen vid `skills@e712cea` (katalog `2af09b2`),
`enkey-agents@f237ef1` och `neptune_academy@6ce65e8` kräver rättning före aktivering.
Den bindande rättningsordern finns i
`conversations/reviews/2026/09/2026-09-13-granskning-batch-3b-implementation.md`.

Sammanfattat ska Claude återställa fakturamånaden som obligatorisk observerad period,
stoppa återanvändning av effekt vid produktbyte, rätta fullvärmepolicyernas stale
`_0`-källor, lägga verkliga TypeScript-goldenprov över alla åtta, synkronisera den
levande 86-radersräkningen och stärka paritets-/fail-closed-proven. De åtta
implementationsspärrarna och 25/39/28 ska ligga kvar. Ingen aktivering och ingen push.
