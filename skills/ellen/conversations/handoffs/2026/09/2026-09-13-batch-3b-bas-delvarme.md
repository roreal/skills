---
handoff_id: "2026-09-13-001"
created_at: "2026-09-13T20:48:10+02:00"
from: Codex
to: Claude
status: pushed-and-remote-verified
implementation_allowed: true
approved_implementation_scope: "batch-3b-eon-navirum-bas-delvarme-36-month-supplier-value"
tariff_activation_allowed: true
push_allowed: false
push_completed: true
review_required_before_activation: true
review_required_before_push: true
latest_review: "2026-09-14-002"
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

## Codex omgranskning 2026-09-13-037

Rättningsrunda 1 vid `skills@64fc2d1` (katalog `3b8c1ae`),
`enkey-agents@75ce1ae` och `neptune_academy@babeca2` löser de tre tidigare P1-fynden
och huvuddelen av P2. Tre P2-luckor återstår före aktivering:

1. TypeScript-matrisen bygger internt självkonsistenta mockpolicyer med andra
   bindningsnycklar än generatorns verkliga åtta policyer, innehåller inga bastariffer
   och jämför därför inga variant–bas-kostnadsdelar. Fel band och saknad/ogiltig effekt,
   flöde och temperatur saknas också.
2. Batch 3b:s fakturamånadsbundna 36-månadersvärde är fortfarande märkt
   `matupplosning="arsvis"`; dokumentationen överdriver dessutom vad
   `matchning_mot_manad` garanterar i en årsfasad utan mål-månad.
3. Direkta tester av variant-ID-dublett/feltyp samt katalog–policy-paritet för de rättade
   `_1`-källorna saknas fortfarande.

Full rättningsorder finns i
`conversations/reviews/2026/09/2026-09-13-omgranskning-batch-3b-rattningsrunda-1.md`.
Behåll spärrarna och 25/39/28. Ingen aktivering och ingen push.

## Codex omgranskning 2026-09-13-038

Rättningsrunda 2 vid `skills@a7558de` (oförändrad katalog `3b8c1ae`),
`enkey-agents@950fd5b` och `neptune_academy@2be2452` stänger de tre tidigare
P2-punkterna i huvudsak. Generatorfixturen bär nu verkliga policybindningar och åtta
bas–variant-par, periodmetadatan är månadsvis och direkta variant-/källregressioner
finns. **1222 passed + 4 skipped Python**, **1145 passed TypeScript**, ren tsc, isolerat
bygge och **13/13 E2E** är verifierade.

Två snäva P2-bevisluckor återstår: TypeScript-matrisen pinnar bara energin oberoende
medan effektfacitet läses ur fixturen och flödet saknar fristående facit; den uppgivna
saknad/ogiltig-matrisen för effekt/flöde/temperatur är inte komplett eller fullt
fältnära. TypeScript-typen beskriver dessutom fortfarande felaktigt
`matchningMotManad` som verklig målmatchning även i årsfasaden, och generatorsynkprovet
kallas byteidentiskt fast det jämför parsade JSON-objekt semantiskt.

Full rättningsorder finns i
`conversations/reviews/2026/09/2026-09-13-omgranskning-batch-3b-rattningsrunda-2.md`.
Behåll spärrarna och 25/39/28. Ingen aktivering och ingen push.

## Codex slutgranskning 2026-09-13-039

Rättningsrunda 3 vid `skills@14cf1db` (oförändrad katalog `3b8c1ae`),
`enkey-agents@09b0ef2` och `neptune_academy@92de895` stänger granskning 038:s två
P2-fynd. Codex reproducerade **1222 passed + 4 skipped Python**, **1177 passed
TypeScript**, ren tsc, isolerat bygge och **13/13 E2E**. Inga blockerande fynd återstår
i den spärrade implementationen.

Batch 3b är därför **godkänd för en separat lokal aktiveringsrunda**, från 25/39/28
till 33/31/28. En icke-blockerande men obligatorisk P3-rättning ska följa med:
facitvärdena 108,17 osv. är `kr/kW/månad`, inte `kr/kW/år`; rätta namn/kommentarer men
behåll värden och `×12`-aritmetik.

Den fullständiga aktiveringsordern finns i
`conversations/reviews/2026/09/2026-09-13-slutgranskning-batch-3b-rattningsrunda-3.md`.
Lokal aktivering är tillåten. **Ingen push före Codex granskning av aktiveringsdiffen.**

## Codex granskning 2026-09-13-040 av lokal aktivering

Den lokala aktiveringen vid `skills@053a429` (loggad vid `9eb0ae1`),
`enkey-agents@77f19c3` och `neptune_academy@ef0fded` är tekniskt korrekt och får ligga
kvar. Semantisk generatordiff visar exakt åtta tillägg, inga ändrade äldre produkter,
och dispositionen är **33/31/28**. Codex reproducerade **1230 passed + 4 skipped
Python**, **1177 passed TypeScript**, ren tsc, isolerat bygge och **14/14 E2E** samt
ett manuellt grönt skarpt Navirum Bas-/delvärmeflöde.

Tre P2-luckor återstår före push: permanent Navirum Bas-/delvärme-E2E saknas, den
obligatoriska `kr/kW/månad`-rättningen gjordes inte trots motsatt logguppgift, och
levande tariffdokument innehåller både `skills@<aktiveringscommit>` och ett felaktigt
tre-fältskontrakt utan band/fakturamånad. Full rättningsorder finns i
`conversations/reviews/2026/09/2026-09-13-granskning-lokal-aktivering-batch-3b.md`.

Behåll aktiveringen och 33/31/28. **Ingen push.**

## Codex omgranskning 2026-09-14-001

Rättningsrunda 1 vid `skills@3f211a7`, `enkey-agents@f6f52ff` och
`neptune_academy@50a47c3` stänger samtliga funktionella/P2-fynd i granskning 040.
Codex reproducerade **1230 passed + 4 skipped Python**, **1177 passed TypeScript**, ren
tsc och **15/15 E2E**. Aktiveringen ligger korrekt kvar vid **33/31/28**.

En ren P3 återstår före push: de blandade Batch 3-facittabellerna innehåller både
`rate_period=month` och `rate_period=year`, men Pythonkommentaren kallar allt månad och
TypeScript-kommentaren allt år. Två testsektionsrubriker säger också fortfarande
"bakom spärr". Full minimal order finns i
`conversations/reviews/2026/09/2026-09-14-omgranskning-lokal-aktivering-batch-3b-fix1.md`.

Ingen kod/data/aritmetik ska ändras. **Ingen push.**

## Codex slutgodkännande 2026-09-14-002

Rättningsrunda 2 vid `skills@537142d`, `enkey-agents@49f0907` och
`neptune_academy@5e0d710` stänger den sista P3-punkten från omgranskning 001. Diffen
består endast av de fyra beställda testkommentar-/rubrikrättningarna; inga tal,
periodvärden, assertioner, tariffdata eller produktionsfiler ändrades.

Codex reproducerade **501 riktade Pythonprov**, **23 riktade TypeScriptprov**, ren tsc
och rena diffkontroller. Föregående fullverifiering med **1230 passed + 4 skipped
Python**, **1177 passed TypeScript**, isolerat bygge och **15/15 E2E** gäller
oförändrad. Dispositionen är fortsatt **33/31/28**.

Batch 3b är godkänd för normal fast-forward-push vid de granskade HEAD-versionerna.
Ingen push har utförts; invänta Roberts uttryckliga godkännande.

## Bekräftelse av pushauktorisation 2026-09-14

Robert bekräftade efteråt att han uttryckligen hade godkänt pushen i agentväxlingen och
att Codex provisoriska slutsats om saknat godkännande berodde på att beskedet inte syntes
i den aktuella dialogvyn. Pushen var alltså auktoriserad och korrekt utförd.

Remote-HEAD verifierades direkt: `skills@119f038`, `enkey-agents@49f0907` och
`neptune_academy@5e0d710`. Ingen rollback eller historikomskrivning behövs.
