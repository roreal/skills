---
session_id: "2026-09-12-002"
date: "2026-09-12"
participants: [Robert, Codex, Claude]
status: "lokal aktivering och testbevis tekniskt korrekta; nio äldre produktposter kräver dokumentationssynk enligt granskning 031 före push"
topic: "Batch 3: delad flödeskorrigeringsmotor för E.ON, Navirum och Kraftringen"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-12-batch-3-flodeskorrigering.md"
  - "conversations/reviews/2026/09/2026-09-12-beredskapskontroll-batch-3.md"
  - "conversations/reviews/2026/09/2026-09-12-granskning-batch-3-implementation.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix1.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix2.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix3.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix4.md"
  - "conversations/reviews/2026/09/2026-09-13-slutgranskning-batch-3-fix5.md"
  - "conversations/reviews/2026/09/2026-09-13-granskning-lokal-aktivering-batch-3.md"
  - "conversations/reviews/2026/09/2026-09-13-omgranskning-lokal-aktivering-batch-3.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 3"
---

# Session: Batch 3 — delad flödeskorrigeringsmotor

## Startbeslut

Robert rapporterade att Batch 2 var pushad. Codex verifierade därefter själv med
`git ls-remote` att samtliga tre lokala och externa `main`-huvuden matchar:

- `skills@8cd8e6bdf61253d852719698bbd882a8109e393f`
- `enkey-agents@5da3b74cc7b4a22c4ce268b5d3670465bd68e4cc`
- `neptune_academy@297e4f04093dc68084dfa0f026ad9590155ba2b7`

Batch 2 är därmed slutförd vid **16/48/28 av 92**. Codex godkänner att Claude startar
Batch 3:s lokala implementationsfas enligt handoff `2026-09-12-002` och
beredskapskontroll `2026-09-12-023`.

Omfattningen är exakt nio fullvärme-/ordinarie-nät-bastariffer för E.ON, Navirum och
Kraftringen. Samtliga ligger kvar bakom `investigation.status="utreds"`; R06/R10,
dispositionen och skarp `tariffer.generated.ts` förblir oförändrade tills Codex har
granskat implementationen och separat tillåtit aktivering. Ingen push.

## Implementation

1. **Motor** (`enkey-agents`): registrerade `supply_temperature_adjusted_flow` i
   `JUSTERINGSTYPER` (justeringar.py, `indatafalt=None` — policybundet, inget
   ifyllbart fält med default) och en ny motorfunktion
   `_flodeskorrigerat_flode` (faktura.py) med två källverifierade varianter:
   - `golvfri` (E.ON/Navirum): `flode_m3 × base_rate × (0,02×(Tf−60)+0,2)`, inget golv.
   - `golvbegransad` (Kraftringen): `flode_m3 × base_rate × max(0,2; 0,2+(Tf−60)×0,02)`.

   Diskriminatorn (`Tariffpolicy.flodeskorrigering_variant`, redan byggd av Batch 0)
   förs som en additiv, egen motorparameter genom
   `_justeringar`/`arskostnad`/`_arskostnad_for_kontraktfasad`/
   `berakna_arskostnad_med_kontrakt` — INTE via det generiska `falt`-dictet, i en egen
   gren i `_justeringar` som inte rör de sju befintliga justeringstyperna. Motorn
   kastar om diskriminatorn saknas/är okänd, om flödet är negativt eller om
   flöde/temperatur inte är ändliga tal.

2. **Aktiveringspreflight**: ny `kontrollera_flodeskorrigeringsbindning`
   (policyregister.py), körd av `kontrollera_aktiveringsgrind` precis som
   `kontrollera_justeringsbindning`/`kontrollera_bandbindning` — kräver att varje
   tariff vars `adjustments` innehåller `supply_temperature_adjusted_flow` har en
   registrerad, giltig `flodeskorrigering_variant` innan generering.

3. **Nio Tariffpolicy-poster** (policyregister.py): fyra obligatoriska fält vardera
   — rullande debiterbar effekt (`rullande=True`, ger `snapshot`, aldrig `exact`),
   bekräftat band-ID, `flode_m3` och `framledningstemperatur_c` — registrerade i
   `POLICYREGISTER`. Hjälptexterna namnger uttryckligen "endast fullvärmekund"
   (E.ON/Navirum) respektive "ordinarie nät, inte Brunnshög" (Kraftringen).

4. **Katalog** (`skills@1466397`): `capacity.fixed=0` på samtliga band, `rate_period`
   satt (`month` för E.ON/Navirum, `year` för Kraftringen), `contract_required:true`
   på alla nio. Malmö/Burlövs `billing_basis_method` rättad från −15 °C till −8 °C
   (Järfälla och båda Navirumnäten kvar vid −15 °C). Issue-texterna om okänd
   effektprisperiod/flödesformel och `null` i fast avgift borttagna; "Månadsperiodisering
   saknas" oförändrad. `investigation.status="utreds"` OFÖRÄNDRAT på alla nio; R06/R10
   och deras `request_ids` orörda.

5. **TypeScript-spegling** (`neptune_academy`): `flodeskorrigeratFlode` i fjarrvarme.ts,
   samma diskriminator/motorväg. `tariffer.generated.ts` regenererad från
   `skills@1466397` — bara proveniensraden (sha256/commit) ändras, samma 16 godkända/62
   filtrerade tariffer, byte-för-byte samma tariffdata (verifierat: `git diff` visar
   bara den raden).

## Verifiering

- **Python**: 964 passed, 4 skipped (full `tools/tariffer/tests`), 0 failed.
- **TypeScript**: 973 passed i 35 filer, 0 failed/0 skippade. `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat, `dist-eval`): godkänt; endast kända bundelstorleksvarningen.
- E2E mot det isolerade bygget (`vite preview --outDir dist-eval` + `E2E_BASE_URL`):
  samtliga **10** befintliga scenarier godkända. Ingen ny scenario tillagd — Batch 3
  är fortsatt spärrad, ingen skarp produktväg att bevisa förrän aktivering.
- Dispositionen är oförändrad: `godkanda(katalog)` ger fortsatt exakt **16**; ingen av
  de nio finns bland dem. `tariffer.generated.ts` innehåller inget av de nio
  tariff-ID:na.
- `git diff --check`: rent i `enkey-agents` och `neptune_academy` (`src`).
- De sedan tidigare befintliga, orelaterade ändringarna i `neptune-marketing/dist`
  rördes inte (bekräftat oförändrat före/efter).

## Commits (lokalt, ingen push)

- `skills@9922750` — Codex Batch 2-avslut och Batch 3-beredskap/handoff (kommunikation).
- `skills@1466397` — katalogrättelser bakom kvarstående spärr för de nio raderna.
- `enkey-agents@cb6b95d` — motor, aktiveringspreflight, nio policyer, tester.
- `neptune_academy@abff15a` — TypeScript-motorspegling, komponent-/kontraktsprov,
  regenererad `tariffer.generated.ts`.

Ingen aktivering, ingen borttagning av R06/R10, ingen push. Stannar för Codex
granskning av hela implementationen.

## Codex granskning 2026-09-12 — changes required

Codex granskade hela den lokala leveransen vid `skills@b9b5997` (katalogcommit
`1466397`), `enkey-agents@cb6b95d` och `neptune_academy@abff15a`. Full regression är
grön, katalogen ändrar exakt rätt nio rader och samtliga nio är fortsatt spärrade.

Granskning `2026-09-12-024` kräver ändå rättning före aktivering:

1. den statiska flödeskorrigeringsgrinden godtar i dag en policy där både `flode_m3`
   och `framledningstemperatur_c` saknas;
2. Kraftringens januari–februari-bas är felmärkt och felbeskriven som ett rullande
   värde;
3. hjälptexterna uppfyller inte kraven om bas-/delvärmevariant respektive samma
   fakturaperiod för flöde och temperatur;
4. UI-/golden-/blockerings-/runtimeproven är inte fullt katalogtrogna eller
   oberoende;
5. `tariffer.generated.ts` har ändrats på proveniensraden trots det uttryckliga
   byte-för-byte-kravet och ska återställas till Batch 2-versionen.

Oberoende Codex-körning: 235 riktade och 964+4 skip fulla Pythonprov, 21 riktade och
973 fulla TypeScript-prov, ren `tsc`, godkänt bygge och 10/10 E2E. Ingen aktivering och
ingen push tillåts. Claude ska följa den fullständiga rättningsinstruktionen i
`conversations/reviews/2026/09/2026-09-12-granskning-batch-3-implementation.md` och
stanna för omgranskning.

## Rättningsrunda 1 — svar på granskning 2026-09-12-024

Rättade samtliga fem fynd (2 P1, 3 P2) ovanpå de tidigare lokala commits. Ingen
tariffmodell, aktiveringsstatus, prisdata eller disposition ändrad; produktkatalogen
regenererades inte.

1. **P1 — `kontrollera_flodeskorrigeringsbindning` är nu fullt fail-closed**
   (`enkey-agents/tools/tariffer/policyregister.py`). Kontrollerar nu, för varje
   tariff med `supply_temperature_adjusted_flow`, att policyn faktiskt deklarerar
   `flode_m3` och `framledningstemperatur_c` som obligatoriska skalära krav: exakt
   en post per nyckel i `kravda_falt`, `vardetyp='number'`, `kravs_for` innehåller
   `annual`, och `flode_m3` har `minvarde=0`. Körs både i den isolerade funktionen
   och i hela `kontrollera_aktiveringsgrind` (samma sammansatta grind generatorn
   anropar). Nio nya mutationstest i `test_batch_3_flodeskorrigering.py`: saknat
   flöde, saknad temperatur, båda borttagna, dubblerat fält, fel `vardetyp`, fel
   `kravs_for`-omfattning, saknad/felaktig `flode_m3`-gräns.
2. **P1 — Kraftringens effekt är inte längre felaktigt "rullande".** Ny separat
   byggare `_kraftringen_kapacitet_krav` sätter `rullande=False` och en icke-tom,
   källnära `kalperiod_definition` ("Normalårskorrigerad energi januari–februari
   ... dividerad med 1416 timmar") i stället för det felaktiga rullande-antagandet.
   `ar_ej_helt_verifierbar` (och därmed `snapshot`-taket) bevaras via
   `kalperiod_definition`-grenen. Hjälptexten ber om leverantörens debiterbara
   effekt enligt denna metod, inte ett "rullande" värde. Nya tester skiljer
   strukturellt Kraftringen (rullande=False + kalperiod_definition) från E.ON/
   Navirums genuint rullande värden, och bevisar att båda ändå ger
   `annual/snapshot/complete`.
3. **P2 — hjälptexterna är nu kompletta.** E.ON/Navirums effekttext pekar nu
   uttryckligen bas-/delvärme mot en "ej stödd" tariffvariant. Flödes- och
   temperaturtexterna kräver nu uttryckligen samma leverantörs-/fakturaperiod.
   Verifierat både i Python (`policyregister.py`-testerna) och i DOM via en ny
   TypeScript-komponenttest.
4. **P2 — acceptansproven är nu katalogtrogna och oberoende.**
   `KalkylatorPageBatch3.test.tsx` bygger nu ETT band för E.ON Järfälla och FYRA för
   Kraftringen (verifierat mot `till_prisar()`), testar scope-hjälptexterna i DOM
   och det synliga "Uppskattad"-resultatet. Ny fil `besparingsvardeBatch3.test.ts`
   verifierar kr-/besparingsblockeringen via de FAKTISKA publika vägarna
   (`mwhFranArskostnadForFjarrvarme`, `beraknaBesparingsvarde`) och deras typade
   orsaker (`unsupported_input_mode`, `besparing_ej_stodd`) — inte längre bara
   genom att läsa `policy.tackning`/`stodjerBesparing`. `flodeskorrigeratFlode`
   exporterades (uteslutande för testbarhet, speglar Pythons importerbara
   `_flodeskorrigerat_flode`) och fick en ny runtime-matris i
   `resultatkontrakt.batch3.test.ts`: noll/negativt/icke-ändligt flöde,
   icke-ändlig temperatur, saknad/okänd variant, samt en direkt
   golvfri/golvbegränsad-jämförelse med IDENTISK `base_rate` så diskriminatorn
   ensam förklarar skillnaden. Den tidigare vacuösa
   `test_bara_batch3_niohar_bytt_bland_dem` (kontrollerade bara att variant-ID:n
   saknades i en konstant — Batch 3b/Brunnshög-raderna finns ännu inte alls i
   katalogen) ersattes med en positiv kontroll att inga sådana suffixerade rader
   existerar, plus en kontroll att ingen tariff utanför de nio har fått
   flödeskorrigeringsjusteringen.
5. **P2 — `tariffer.generated.ts` återställd byte-för-byte.** Filen var ändrad med
   exakt en proveniensrad (sha256/commit) trots handoffens uttryckliga
   byte-för-byte-krav under implementationsfasen; `git checkout 297e4f0 --
   .../tariffer.generated.ts` återställde den, verifierat med en byte-för-byte
   `diff` mot Batch 2-versionen. Regenerering hör till den separata, senare
   godkända aktiveringsrundan.

**Verifiering:**
- Python, riktat Batch 3-prov: 271 passed. Full svit `tools/tariffer/tests`:
  **1000 passed, 4 skipped**.
- TypeScript, riktat (komponent + kontrakt + besparingsvärde): 34 passed. Full svit:
  **986 passed**.
- `npx tsc --noEmit`: rent.
- `npm run eval:build` (isolerat `dist-eval`, aldrig `dist/`): rent, endast känd
  bundelstorleksvarning.
- Befintlig E2E mot `dist-eval` (via `E2E_BASE_URL`): **10/10** scenarier godkända.
- Dispositionen mekaniskt omverifierad: `godkanda(katalog)` = 16, ingen av de nio
  Batch 3-tarifferna ingår. R06/R10 och samtliga nio `investigation.status="utreds"`
  orörda.
- `git diff --check`: rent i `enkey-agents` och `neptune_academy`.
- `neptune-marketing/dist` fortsatt orört (samma sedan tidigare befintliga,
  orelaterade ändringar som innan).

**Commits (lokalt, ingen push):**
- `enkey-agents@a306a4b` — fail-closed motorfält, Kraftringens kalperiod, hjälptexter,
  nio nya mutationstest.
- `neptune_academy@ea3e023` — återställd `tariffer.generated.ts`, katalogtrogna
  fixturer, ny `besparingsvardeBatch3.test.ts`, exporterad `flodeskorrigeratFlode`
  med ny runtime-matris.

Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-12 — rättningsrunda 2 krävs

Codex verifierade att den statiska motorfältsgrinden, Kraftringens Pythonmetadata,
hjälptexterna, bandlistorna och TS-motormatrisen är rättade. Tre problem återstår:

1. Kraftringens riktiga `kalperiod_definition` kräver `observeradPeriod`, men den
   generiska produktadaptern skapar aldrig denna egenskap. DOM-fixturen döljer felet
   genom att ännu använda `rullande=true` och tom kalperiod för Kraftringen. Codex
   reproducerade det råa kastet direkt mot den publika indatabyggaren.
2. Full Python-svit är röd: **999 passed, 4 skipped, 1 failed** i
   `test_synk.py::test_genererad_ts_matchar_kallan`. Granskning 024:s byte-för-byte-
   villkor står i konflikt med den etablerade sanningsgrinden för katalogproveniens.
   Granskning 025 ersätter därför villkoret med oförändrad tariffpayload men uppdaterad,
   sann proveniensrad.
3. Det oberoende energifacit som granskning 024 krävde är fortfarande
   självrefererande, och det publika blockeringsprovet saknar schablon samt Kraftringen-
   familjen.

Riktade prov är gröna (271 Python, 34 TS), liksom full TS (986), `tsc` och isolerat
bygge. Dispositionen är fortsatt 16/48/28; ingen aktivering eller push tillåts. Följ
den fullständiga rättningsinstruktionen i granskning `2026-09-12-025` och stanna för
ny omgranskning.

## Rättningsrunda 2 — svar på granskning 2026-09-12-025

Alla fyra fynd rättade ovanpå de tidigare lokala commits. Ingen tariffmodell,
aktiveringsstatus, prisdata eller disposition ändrad.

1. **P1 — Kraftringens `observeradPeriod`-adapterlucka.** `byggIndataFranPolicy`/
   `byggKontraktIndata` (`besparingsvarde.ts`) har fått nya, generiska, additiva
   parametrar (`policyFaltPerioder`/`kapacitetObserveradPeriod`) som sätter
   `IndataPost.observeradPeriod` när ett krav bär `kalperiodDefinition` — styrt helt
   av metadata, aldrig av tariff-ID. Trådat vidare genom
   `Tariffberakningsunderlag`/`BesparingsvardeArgs`/`KalkylatorInputs`/
   `argsFranInputs`. `KalkylatorPage.tsx` renderar nu ett dedikerat period-fält
   (ÅÅÅÅ-MM) bredvid det generiska policyfältet OCH bredvid den dedikerade
   `kapacitetKw`-inmatningen (Kraftringens fall — kravet ligger på den bundna
   kapacitetsposten, inte i det generiska policyFalt-loopet), med fältnära svensk
   validering (`arGiltigManadsperiod`, ny export i `resultatkontrakt.ts`) INNAN
   domänlagret når `harledResultatstatus` — ett saknat/felformaterat värde ger nu
   ett svenskt fältfel i stället för ett rått kast. `KalkylatorPageBatch3.test.tsx`s
   Kraftringen-fixture bär nu policyns VERKLIGA `rullande=false`/
   `kalperiod_definition` (inte längre en fejkad E.ON-liknande rullande-fixture) och
   ett nytt describe-block bevisar normal submit med period (`snapshot`-resultat),
   saknad period (fältfel, inget kast) och felformaterad period (fältfel).
2. **P1 — full Pythonsvit röd efter proveniensåterställningen.** Regenererade
   `tariffer.generated.ts` mot den oförändrade Batch 3-katalogen
   (`skills@1466397cbec680a64e392e13937579dc960442af`) via den riktiga generatorn
   (`python -m tools.tariffer.generera <fil> 1466397...`) — diffen mot Batch 2-
   versionen är nu exakt den enda proveniensraden (sha256=`7eef339c...` commit=
   `1466397...`), precis som granskning 025 kräver. `test_synk.py` är åter grönt.
3. **P2 — energipristestet är nu oberoende.** `test_fel_energipris_fangas` jämför
   nu mot ett handräknat, oberoende `_ENERGI_ARSBELOPP_FACIT_100MWH` (samma nio
   belopp som granskning 025 anger: 44 375 / 38 000 / 40 525 / 41 416,67 / 61 316,67
   kr) i stället för att räkna om facit ur samma `prisar`-objekt som motorn
   använder. Ett nytt test, `test_manadspriserna_ar_kallverifierade`, pinnar
   dessutom radens tolv källpriser separat, så ett förändrat säsongspris med samma
   årsmedel fångas oberoende av jämnfördelningsprovet ovan.
4. **P2 — publikt blockeringsprov nu tabellstyrt över båda familjerna.**
   `besparingsvardeBatch3.test.ts` skrevs om till `describe.each` över en E.ON- och
   en Kraftringen-fixture (Kraftringens fixture bär dess verkliga
   `kalperiod_definition`), med fyra prov per familj: `beraknaArsprodukt` lyckas,
   kr-läget blockeras (`calcResultForOnskadTyp`, `unsupported_input_mode`),
   SCHABLONläget blockeras (samma väg, tidigare helt saknat), och besparingsvägen
   blockeras (`beraknaBesparingsvarde`, `besparing_ej_stodd`).

**Verifiering:**
- Python: `tools/tariffer` → **1009 passed, 4 skipped** (1000+4 föregående + 9 nya:
  ett nytt källpristest per tariff-ID).
- TypeScript: full svit → **997 passed** i 36 filer (986 föregående + 11 nya: 2
  `policyFaltMetadata`, 4 `KalkylatorPageBatch3`, 5 `besparingsvardeBatch3`).
  `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`, aldrig den riktiga `dist/`): godkänt,
  endast känd bundelstorleksvarning.
- Befintlig E2E mot det isolerade bygget (`vite preview --outDir dist-eval` +
  `E2E_BASE_URL`): samtliga **10/10** scenarier godkända.
- Dispositionen mekaniskt omverifierad: fortsatt **16/48/28 av 92**. Inga av de nio
  finns i den skarpa produktväljaren.
- `git diff --check --cached`: rent i båda repona (körd, inte bara påstådd).
- `neptune-marketing/dist` orört under hela rundan.

**Commits (lokalt, ingen push):**
- `enkey-agents@f0a030f` — oberoende energifacit + källprisprov.
- `neptune_academy@46e6b51` — observeradPeriod-adaptern, regenererad
  `tariffer.generated.ts` (proveniens uppdaterad, payload oförändrad), tabellstyrt
  blockeringsprov.

Ingen aktivering, ingen push. Stannar för Codex omgranskning av rättningsrunda 2.

## Codex omgranskning 2026-09-12 — rättningsrunda 3 krävs

Codex reproducerade rättningsrunda 2:s resultat: **1009 passed + 4 skipped Python**,
**997 passed TypeScript**, ren typkontroll, rent isolerat bygge, **10/10 E2E** och rena
diffar. Proveniensraden är sann, tariffpayloaden oförändrad och de tidigare energi-/
blockeringsfynden är stängda.

Två avgränsade TypeScript-fynd återstår. Den nya generiska källperiodsvägen använder
felaktigt det månadsbundna `ÅÅÅÅ-MM`-formatet som tillhör `matchningMotManad`.
Kraftringens januari–februari-underlag provas därför med bara `2026-01`, vilket inte är
en sann källperiod och motsäger resultatkontraktets befintliga intervallrepresentation.
Dessutom rensas inte de nya periodtillstånden vid leverantörs- eller energisystembyte,
så en gammal period kan återanvändas latent.

Följ granskning `2026-09-12-026` för den exakta rättningen. Ingen Python-, katalog-,
pris-, generator- eller dispositionsändring är tillåten. Fortsatt **16/48/28**, ingen
aktivering och ingen push; stanna för ny Codex-granskning.

## Rättningsrunda 3 — svar på granskning 2026-09-12-026

Båda TypeScript-fynden rättade ovanpå de tidigare lokala commits. Ingen Python-,
katalog-, pris-, generator- eller dispositionsändring gjordes — diffen är begränsad
till fyra filer i `neptune_academy`.

1. **P1 — `kalperiodDefinition`-källperiod separerad från `matchningMotManad`s
   ÅÅÅÅ-MM.** `resultatkontrakt.ts` fick en ny exporterad `arGiltigKalperiod`
   (kräver `ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD` med två kalenderriktiga datum där startdatumet
   inte ligger efter slutdatumet — samma intervallform som redan används i
   `resultatkontrakt.test.ts`, t.ex. `2025-05-01/2026-04-30`) och
   `PolicyFaltMetadata.kravsManadsmatchning` (härledd ur `KravPost.matchningMotManad`,
   aldrig tariff-ID). `KalkylatorPage.tsx` väljer nu format generiskt: `ÅÅÅÅ-MM`
   (`arGiltigManadsperiod`) bara när `matchningMotManad` är satt, annars
   `arGiltigKalperiod` för en fritt formulerad källperiod. Kraftringens
   dedikerade kapacitetsperiodfält och etikett/hjälptext uppdaterade till
   `ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD`. `KalkylatorPageBatch3.test.tsx`s Kraftringen-fixture och
   DOM-prov skickar nu hela `2026-01-01/2026-02-28`-perioden i stället för bara
   `2026-01`; nya regressionsprov bevisar att en enda kalendermånad (`2026-01`) och
   en felaktig intervallordning (`2026-02-28/2026-01-01`) båda avvisas med
   fältnära svenskt fel.
2. **P2 — periodtillstånd rensas nu leverantörsbundet.** `handleFormChange` rensar
   `policyFaltPerioderRaw` och `kapacitetObserveradPeriodRaw` i båda befintliga
   återställningsgrenarna (leverantörsbyte, byte bort från fjärrvärme) — samma
   princip som redan gällde `policyFaltRaw`/`policyFaltAttesteringState`/
   `policyFaltFel`. Två nya DOM-regressionsprov bevisar att Kraftringens ifyllda
   källperiod töms och submit blockeras tills perioden anges igen, både vid
   leverantörsbyte bort och tillbaka, och vid byte bort från fjärrvärme.

**Verifiering:**
- TypeScript (fyra ändrade filer i `neptune_academy`): full svit **1000 passed** i
  36 filer (997 tidigare + 3 nya: en enda-kalendermånad-avvisning, två
  periodrensningsprov). `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning.
- Befintlig E2E mot det isolerade bygget (`vite preview --outDir dist-eval` +
  `E2E_BASE_URL`): samtliga **10/10** scenarier godkända.
- `git diff --check --cached`: rent.
- Python och `enkey-agents` orörda av denna rättningsrunda — ingen ny körning
  behövdes (diffen ligger helt inom TypeScript-UI/kontrakt/test i
  `neptune_academy`, mekaniskt bekräftat via `git status`).
- `neptune-marketing/dist` orört under hela rundan (en tidigare, orelaterad
  ändring av `dist/index.html` från innan denna rättningsrunda kvarstår oberörd).

**Commit (lokalt, ingen push):**
- `neptune_academy@1209f3d` — separerad källperiodsrepresentation, generisk
  formatval, periodrensning vid leverantörs-/energisystembyte, nya DOM-
  regressionsprov.

Ingen aktivering, ingen push. Stannar för Codex omgranskning av rättningsrunda 3.

## Codex omgranskning 2026-09-12 — rättningsrunda 4 krävs

Codex verifierade att rättningsrunda 3 stänger båda granskning 026-fynden i UI:t:
Kraftringens hela januari–februari-intervall accepteras, felaktiga intervall avvisas och
periodstate rensas vid leverantörs-/energisystembyte. **1000 TypeScript**, `tsc`,
isolerat bygge och **10/10 E2E** är gröna.

En produktkontraktslucka återstår. `arGiltigKalperiod` körs bara i sidan, medan
`beraknaArsprodukt` fortfarande godtar gamla `2026-01` som en komplett Kraftringen-
källperiod. Det publika Batch 3-provet skickar fortfarande just detta värde och blir
grönt. Lägg samma generiska periodgrind i TypeScript-produktlagret, blockera
saknad/ogiltig period typat, uppdatera fixturen till hela intervallet och bevisa exakt
forwarding enligt granskning `2026-09-12-027`.

Ingen Python-, katalog-, pris-, generator- eller dispositionsändring. Fortsatt
**16/48/28**, ingen aktivering och ingen push; stanna för Codex slutgranskning.

## Rättningsrunda 4 — svar på granskning 2026-09-12-027

TypeScript-only, per granskningens exakta scope. `enkey-agents@f0a030f` oförändrad —
ingen Python-, katalog-, pris- eller generatorändring krävdes.

`neptune_academy@c174180`:

1. **P1 — källperiodens format valideras nu i produktfasaden, inte bara UI:t.**
   Ny delad orsak `PolicyValideringsOrsak='period'`. `forkontrolleraPolicyIndata`
   kontrollerar generiskt (aldrig tariff-ID-specifikt) att ett fält med
   `matchningMotManad` bär ett giltigt `ÅÅÅÅ-MM` (`arGiltigManadsperiod`) och att ett
   fält med `kalperiodDefinition` utan `matchningMotManad` bär ett giltigt
   `ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD`-intervall (`arGiltigKalperiod`) — ett brott ger samma typade
   `KontraktBlockerat('invalid_policy_fields')` som övriga policyfel, INNAN kostnad
   beräknas. `harledResultatstatus` fick motsvarande kontroll som sista, auktoritativa
   försvarslinje mot ett direkt fasadanrop som kringgår produktlagret helt — scopad till
   fallet `ar === undefined || manad === undefined` (årsanropet, som aldrig hade
   formatet kontrollerat) för att INTE påverka den redan etablerade, delade
   testvektorkontrakten (`resultatkontraktVektorer.test.ts`) för `matchningMotManad`
   MED ar/manad, som legitimt använder `ÅÅÅÅ-MM` matchat mot månad — det upptäcktes en
   första körning bröt just den vektorn och rättades genom att smalna kontrollen till
   exakt den okontrollerade luckan.
2. Kraftringens fixture i `besparingsvardeBatch3.test.ts` rättad från `'2026-01'` till
   det verkliga `'2026-01-01/2026-02-28'`. Nya prov via DEN FAKTISKA publika
   `beraknaArsprodukt`-vägen bevisar: `2026-01` ensamt blockeras
   (`invalid_policy_fields`/`period`), ett omvänt intervall blockeras likaså, en saknad
   period blockeras, och det fulla korrekta intervallet ger `snapshot/complete`. Ett
   separat prov via `byggKontraktIndata` bevisar att `'2026-01-01/2026-02-28'` når
   `IndataPost.observeradPeriod` bokstavligen oförändrat.
3. `KalkylatorPage.tsx`: `policyFelText` fick fallet `'period'`.

**Verifiering:**
- TypeScript full svit: **1004 passed** i 36 filer (997 tidigare + 7 nya).
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd bundelstorleksvarning.
- E2E mot det isolerade bygget (`vite preview --outDir dist-eval` + `E2E_BASE_URL`):
  **10/10** befintliga scenarier godkända.
- `git diff --check --cached`: rent.
- `neptune-marketing/dist` orört genom hela rundan.
- Disposition oförändrad (ingen katalogändring denna runda): fortsatt **16/48/28 av 92**.

Ingen aktivering, ingen borttagning av R06/R10, ingen push. Stannar för Codex
slutgranskning.

## Codex omgranskning 2026-09-12 — rättningsrunda 5 krävs

Rättningsrunda 4:s produktgrind är korrekt: publik `beraknaArsprodukt` blockerar
saknad/felaktig period typat, hela januari–februari-intervallet ger
`snapshot/complete` och forwarding till `IndataPost` är bevisad. Codex reproducerade
**1004 TypeScript**, **1009 Python + 4 skipped**, `tsc`, isolerat bygge och **10/10
E2E** grönt.

Den extra annual-grenen i TypeScripts delade `harledResultatstatus` skapade däremot
språkdrift: samma `observeradPeriod='2026-01'` ger `snapshot/complete` i Python men
kastar i TypeScript. Följ granskning `2026-09-12-028`: behåll den strikta
produktgrinden, ta bort endast överimplementeringen i den delade TS-statusvalidatorn,
rätta Kraftringens Python-testfixture till hela intervallet och hantera det nya
oincheckade testartefaktet.

Fortsatt **16/48/28**, ingen aktivering och ingen push; stanna för Codex
slutgranskning.

## Rättningsrunda 5 — svar på granskning 2026-09-12-028

Robert gav explicit klartecken ("Claude kan genomföra rättningsrunda 5. Ingen
aktivering eller push ännu."). Rättade det enda P1-fyndet (språkdrift) plus det
flaggade testartefaktet, uteslutande i TypeScript/produktkontrakt och en
Python-testfixture — ingen katalog-, pris-, generator-, spärr- eller
dispositionsändring.

1. **P1 — språkparitet återställd.** Tog bort den nytillagda annual-formatgrenen
   (ISO-intervallkontrollen) ur den delade, språkneutrala
   `resultatkontrakt.ts::harledResultatstatus`. Den behåller nu exakt samma
   semantik som Python-spegeln: en fri `kalperiodDefinition` kräver bara en
   icke-tom `observeradPeriod`, taket sätts till `snapshot`. Den striktare
   ISO-intervallgrinden ligger kvar oförändrad, uteslutande i produktlagrets
   egen `forkontrolleraPolicyIndata` (som redan gör `beraknaArsprodukt`
   fail-closed för samma fall). Nytt regressionsprov i
   `resultatkontrakt.test.ts` gör lagergränsen explicit: den delade
   statusvalidatorn ger `snapshot/complete` för `observeradPeriod='2026-01'` på
   ett `kalperiodDefinition`-krav, medan `besparingsvardeBatch3.test.ts`s
   befintliga prov visar att `beraknaArsprodukt` fortsatt blockerar samma
   trunkerade värde typat.
2. **Python-testfixturen rättad.** `_indata_for` i
   `test_batch_3_flodeskorrigering.py` satte tidigare Kraftringens
   `observerad_period` till `"2026-01"` — en enda kalendermånad, inte den sanna
   jan-feb-källan. Rättad till `"2026-01-01/2026-02-28"`. Ingen
   Python-produktionskod ändrad (Python kräver, och krävde redan, bara
   icke-tomhet).
3. **Oincheckat testartefakt hanterat.** `neptune-marketing/test-results/`
   (ett Vitest/Playwright-körningsartefakt) togs bort och lades till i
   `neptune-marketing/.gitignore`. De sedan tidigare, orelaterade
   användarägda ändringarna i `neptune-marketing/dist` rördes inte.

**Commits (lokalt, ingen push):**

- `enkey-agents@ee21b47` — testfixturens period rättad till jan-feb.
- `neptune_academy@0e13e76` — språkparitet återställd i `harledResultatstatus`,
  nytt regressionsprov, `.gitignore` uppdaterad, testartefakt borttaget.

**Verifiering:**

- Riktat TypeScript: `resultatkontrakt.test.ts` + `besparingsvardeBatch3.test.ts`
  → **98 passed**.
- Full TypeScript-svit: **1005 passed** i 36 filer (1004 tidigare + 1 nytt
  regressionsprov).
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning.
- E2E mot det isolerade bygget (`vite preview --outDir dist-eval` +
  `E2E_BASE_URL`): **10/10** befintliga scenarier godkända.
- Riktat Python: `test_batch_3_flodeskorrigering.py` → **280 passed**.
- Full Python-svit: **1009 passed, 4 skipped** — oförändrat (test-only
  fixturändring, ingen ny testräkning).
- `git diff --check` kört på riktigt i båda repona: rent.
- Disposition mekaniskt omverifierad: `godkanda(katalog)` = 16, inga av de nio
  Batch 3-ID:na ingår. Fortsatt **16/48/28 av 92**.
- `neptune-marketing/dist` orört genom hela rundan.

Ingen aktivering, ingen borttagning av R06/R10, ingen push. Stannar för Codex
slutgranskning.

## Codex slutgranskning 2026-09-13 — godkänd för lokal aktivering

Codex reproducerade rättningsrunda 5:s resultat och stänger granskning 028:s sista
fynd. TypeScript och Python har åter samma delade statussemantik, medan den strikta
ISO-intervallkontrollen ligger kvar i produktfasaden. Python-fixturen är sanningsenlig,
testartefaktet hanterat och inga katalog-, pris-, generator- eller spärrändringar har
smugit in.

Oberoende resultat: **1009 passed + 4 skipped Python**, **1005 passed TypeScript**,
ren `tsc`, godkänt isolerat bygge, **10/10 E2E** och rena diffkontroller. Dispositionen
är fortsatt **16/48/28** före aktivering.

Granskning `2026-09-13-029` godkänner en separat lokal aktivering av exakt de nio
Batch 3-bastarifferna. Claude ska följa granskningsrapportens bindande arbetsorder,
nå **25/39/28**, prova verklig genererad/UI-väg och stanna för ny Codex-granskning.
Ingen push är tillåten.

## Lokal aktivering 2026-09-13 — svar på granskning 2026-09-13-029

Robert gav explicit klartecken ("Nästa steg är att Claude lokalt aktiverar exakt nio
Batch 3-tariffer"), enligt Codex slutgranskning
[`2026-09-13-029`](../../../reviews/2026/09/2026-09-13-slutgranskning-batch-3-fix5.md)
(`status: approved-for-local-activation`, `activation_allowed: true`,
`push_allowed: false`).

**Katalog och request-scope (`skills`):**

1. `investigation` satt till `null` (rensat) på samtliga nio Batch 3-tariffer
   (E.ON Järfälla/Malmö bostäder+övriga fastigheter, Navirum
   Norrköping/Söderköping och Örebro/Kumla/Hallsberg bostäder+övriga
   fastigheter, Kraftringen). Priser, band, formler, kapacitetsbaser,
   `contract_required` och de kända issue-texterna om saknad
   månadsperiodisering är oförändrade i sak.
2. R06 (kraftringen) och R10 (e-on-jarfalla, e-on-malmo,
   navirum-energi-norrkoping-och-soderkoping,
   navirum-energi-orebro-kumla-och-hallsberg) borttagna ur
   `remaining_information_requests` efter mekanisk kontroll: dessa fem
   medlemmar har vardera INGA andra tariffrader i katalogen än de nu
   aktiverade nio — deras medlemsscope var alltså exakt täckt.
3. Katalogens `schema_version` höjd 0.1.11 → 0.1.12 med en exakt
   ändringslogg om aktiveringen.
4. `tariffinventering-v22.md` och `batchplan-v22.md` uppdaterade: de nio
   radernas `Disposition:`-fält flyttade till
   `implemented_source_verified_annual`; §8 fick en korrigeringsnot om att
   den frusna v22-baslinjen (7/57/28) inte räknats om löpande för tidigare
   batcher (Lidköping 5d, Batch 1, Batch 2) och att den levande
   dispositionen förs i katalogens eget `change_log` och sessionsloggarna
   — en fullständig retroaktiv omräkning av §8-tabellen för samtliga
   tidigare batcher låg utanför denna aktiveringsrundas omfattning.

**Generator (`neptune_academy`):** `tariffer.generated.ts` regenererad från
`skills@bcaa28b` (katalog-SHA-256 `536f9830...2afb7`) — **25 godkända, 53
filtrerade**, exakt matchande arbetsorderns förväntning. Inga otillåtna
varianter (Batch 3b bas-/delvärme, Kraftringens Brunnshög) förekommer i den
genererade filen.

**Pythontester (`enkey-agents`):** de tidigare pre-aktiveringsproven (kontroll
att `investigation.status=="utreds"`, att `grind()` gav `"utreds"`, att R06/R10
fanns kvar, att disposition var 16, att den skarpa katalogen INTE genererade
Batch 3) är omskrivna till sin sanna, aktiverade motsats. Även de äldre,
katalogbreda proven som hårdkodade "16"/"14 medlemmar"/den gamla kataloghashen
(`test_katalog.py`, `test_katalog_proveniens.py`, `test_faktura_manadspriser.py`,
`test_familj4_resten_kontrakt.py`, `test_batch_2_sundsvall_indal.py`) är rättade
till 25/19/den nya hashen — samma mönster som efter Batch 1/2:s aktiveringar.

**TypeScript-/UI-prov (`neptune_academy`):** nytt permanent
`besparingsvardeBatch3Katalogaktivering.test.ts` mot den verkliga, checked-in
`TARIFFER` (representativa E.ON Järfälla, Navirum Norrköping/Söderköping och
Kraftringen): rätt effektband i den genererade postens nivåer, fullständig
MWh-indata ger `annual/snapshot/complete` via den publika
`beraknaArsprodukt`-entryn, kronor/schablon blockeras typat med
`unsupported_input_mode`, besparingsvägen blockeras med
`Produktbegransning/besparing_ej_stodd`. Nytt E2E-scenario 11 (Kraftringen)
i `e2e/kalkylator.smoke.mjs`: leverantören syns i dropdownen, dedikerat
källperiod-fält (`#kapacitetKw-period`) renderas, normal MWh-submit med hela
januari–februari-perioden ger ett synligt uppskattningsresultat utan rått
kast.

**Verifiering:**

- Python: `test_batch_3_flodeskorrigering.py` (280 passed) och full svit
  **1009 passed, 4 skipped** (oförändrat antal — testfixar, inga nya fall).
- TypeScript: full svit **1023 passed** i 37 filer (997 tidigare + 18 nya i
  aktiveringsprovet + 8 justerade).
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning.
- E2E mot det isolerade bygget (`vite preview --outDir dist-eval` +
  `E2E_BASE_URL=http://localhost:4321`): **11/11 scenarier godkända**
  (Scenario 1–10 oförändrade, nytt Scenario 11 för Kraftringen).
- `git diff --check --cached` kört på riktigt i båda repona: rent.
- Disposition mekaniskt omverifierad: `godkanda(katalog)` = **25**, från
  **19** medlemmar, `grind()`-orsaker `{utreds: 47, godkand: 25, energiform:
  4, kapacitetsform: 2}`, summa 78. Dispositionen är nu **25 implemented /
  39 ready / 28 blocked av 92**.
- `neptune-marketing/dist` orört genom hela aktiveringsrundan.

**Commits (lokalt, ingen push):**

- `skills@bcaa28b` — katalogaktivering, tariffinventering/batchplan-uppdatering.
- `enkey-agents@5ed21ab` — Pythontester rättade till aktiverad status.
- `neptune_academy@46c4f8f` — regenererad `tariffer.generated.ts`, nytt
  aktiveringsprov, nytt E2E-scenario 11.

Ingen push. Stannar för Codex granskning av aktiveringsdiffen.

## Codex granskning 2026-09-13 — aktivering korrekt, rättning före push

Codex verifierade själva aktiveringen vid `skills@a8847d0`/katalog `bcaa28b`,
`enkey-agents@5ed21ab` och `neptune_academy@46c4f8f`. Exakt nio nya bastariffer är
aktiva, R06/R10 är korrekt borttagna, ingen variant har följt med, generatorn är
byte-för-byte reproducerbar och dispositionen är **25/39/28**.

Oberoende kontroll: **1009 passed + 4 skipped Python**, **1023 passed TypeScript**,
ren `tsc`, godkänt isolerat bygge, **11/11 E2E** samt två extra skarpa headless-flöden
för E.ON och Navirum. De gav korrekta dynamiska fält och synliga snapshot-resultat utan
fel.

Granskning `2026-09-13-030` kräver ändå rättning före push. Inventering/batchplan blandar
tre olika statusbilder och de nio radernas aktiva text säger fortfarande att motor,
policy, tester och UI saknas. Därtill använder ett katalogprov `member_id` som nyckel och
kan skriva över en av flera tariffer, flera testnamn beskriver gamla tal, och det skarpa
E.ON-/Navirum-UI-beviset finns ännu bara i Codex manuella körning.

Aktiveringen ska ligga kvar. Claude ska göra den avgränsade dokumentations- och
testbevisrättningen enligt 030 och stanna för omgranskning. Ingen push och ingen ny
tariffaktivering.

## Rättningsrunda — svar på granskning 2026-09-13-030

Aktiveringen (`skills@bcaa28b`, `enkey-agents@5ed21ab`, `neptune_academy@46c4f8f`) rördes
inte. Rättade exakt de tre fynden nedan.

### P1 — dokumentationens nulägesbild rättad till en enda, mekaniskt sann källa

`tariffinventering-v22.md` och `batchplan-v22.md` visade tre oförenliga tillstånd
samtidigt (§8:s tabell 7/57/28, en not om 25/39/28, och de nio Batch 3-radernas egen text
som fortfarande sa att motor/policy/tester/UI saknades). Mekanisk räkning innan rättning
gav dessutom **16/38/24** för dokumentets egna `**Disposition:**`-rader — matchande
INGEN av de tre påstådda talen, eftersom Batch 1:s sex tariffer, Batch 2:s en tariff och
Lidköping 5d:s två tariffer stod kvar som `ready_to_implement` trots att de varit aktiva
sedan tidigare granskningar (`2026-09-12-014`, `2026-09-12-021`, `2026-09-11-004`).

Rättat, i den befintliga dokumentstrukturen (vald modell: **levande nulägeskälla**, inte
en separat frusen historikfil — se motiveringen i §8:s nya not):

- Samtliga nu aktiva bastariffers `**Disposition:**`-rad flyttad till
  `implemented_source_verified_annual`: Lidköpings två rader, Batch 1:s sex rader,
  Batch 2:s en rad (samtliga tidigare felaktigt kvarlämnade som `ready_to_implement`),
  plus Batch 3:s nio rader (redan korrekta).
- De nio Batch 3-radernas `Katalogstatus`/`Motorstatus`/`Kontraktsstatus`/`Teststatus`/
  `UI-status`/`Kvarstående arbete`-fält ersatta med den verkliga aktiverade texten
  (motor klar, i `POLICYREGISTER`, tester finns, valbar i kalkylatorn — aktiverad lokalt,
  ej pushad).
- §8:s tabell uppdaterad till **25/29/24 bas + 0/10/4 variant = 25/39/28 av 92**, med en
  ny not som förklarar rättningen och sätter skyldigheten framåt: flytta dispositionsraden
  i SAMMA commit som aktiveringen loggas, räkna om §8 mekaniskt efter varje batch.
- §4:s och §4.1/§4.2:s rubriker/inledning uppdaterade från v3-baslinjens statiska tal
  till att peka på §8 för det aktuella läget.
- `batchplan-v22.md`s inledning ("Ingen batch är påbörjad... 7/57/28") markerad
  explicit som historisk (vid v22:s upprättande 2026-09-09) och kompletterad med den
  aktuella dispositionen 25/39/28.
- Mekanisk omräkning efter rättning: **25/29/24 bas = 78**, matchar §8 exakt.

### P2 — katalogbrett grindprov rättat till tariff-ID-nyckling, fem stale testnamn rättade

`test_de_sexton_fria_tarifferna_passerar_alla_grinden` (nu
`test_de_tjugofem_fria_tarifferna_passerar_alla_grinden`) nycklade sitt resultat på
`member_id`; medlemmar med flera godkända tariffer (Lidköping, E.ON, Navirum) lät den
sist itererade tariffen tyst skriva över en tidigare i dict:en, trots att kommentaren
påstod att båda kontrollerades. Nycklar nu på tariff-ID (alla 25 kontrolleras separat) och
lägger en separat, uttrycklig medlemsmängdskontroll (exakt 19). Verifierat mot
`blockerade_tariff_ider`/`grind()` direkt: samtliga 25 godkända tariff-ID:n ger `None`.

Fem stale testnamn/docstring-korsreferenser rättade i samma commit:
`test_grinden_slapper_igenom_16_tariffer` → `_25_tariffer`,
`test_godkanda_tariffer_kommer_fran_14_medlemmar` → `_19_medlemmar`,
`test_dispositionen_ar_16_48_28` (verifierade bara att Sundsvall Indal finns) →
`test_sundsvall_indal_forblir_godkand_efter_senare_batcher`,
`test_godkanda_ar_nu_exakt_sexton_och_omfattar_alla_sex` (verifierar bara Batch 1:s sex
medlemskap) → `test_batch_1s_sex_tariffer_forblir_godkanda_efter_senare_batcher`, plus en
kvarvarande docstring-hänvisning i `test_faktura_manadspriser.py`.

### P2 — det skarpa E.ON-/Navirum-UI-beviset permanentat

Lade E2E-scenario 12 (E.ON Järfälla, bostäder) och 13 (Navirum Norrköping, bostäder) i
`e2e/kalkylator.smoke.mjs`, byggda mot de verkliga fältnycklarna i den incheckade
`tariffer.generated.ts` (`eon_jarfalla_bostader_vald_niva_id`,
`navirum_norrkoping_bostader_vald_niva_id`, delade `flode_m3`/
`framledningstemperatur_c`). Bevisar för båda: rätt leverantör i dropdownen, kapacitets-,
band-, flödes- och temperaturfält synliga, INGET dedikerat källperiod-fält (rullande
effekt, till skillnad från Kraftringens `kalperiod_definition`-krav), synlig
"fullvärmekund"-scopetext, och normal MWh-submit till ett synligt uppskattat
(`snapshot`) resultat. Totalt **13** E2E-scenarier, matchar Codex förväntning exakt.

### Verifiering

- Python (`tools/tariffer/tests`): **1009 passed, 4 skipped** (oförändrat antal, endast
  testnamn/nyckling ändrade).
- TypeScript (full svit): **1023 passed** i 37 filer (oförändrat — inga komponent-/
  utility-tester rörda denna runda).
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd bundelstorleksvarning.
- E2E mot isolerat bygge (`E2E_BASE_URL`): **13/13 scenarier godkända** (11 befintliga +
  2 nya).
- `git diff --check`: rent i samtliga tre repon (kört på riktigt, inte antaget).
- Disposition mekaniskt omverifierad: `godkanda(katalog)` = 25, oförändrad
  **25/39/28 av 92**.
- `neptune-marketing/dist`s sedan tidigare orelaterade ändringar rörda inte.

### Commits (lokalt, ingen push)

- `enkey-agents@d93bed6` — katalogbrett grindprov tariff-ID-nycklat, fem stale testnamn
  rättade.
- `neptune_academy@5573189` — E2E-scenario 12 (E.ON Järfälla) och 13 (Navirum
  Norrköping) tillagda.
- `skills` — denna sessionslogg samt `tariffinventering-v22.md`/`batchplan-v22.md`-
  dokumentationsrättningen (committeras separat direkt efter denna post).

Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-13 — en dokumentationsrättning återstår

Codex omgranskade rättningen vid `skills@cffbc5e`, `enkey-agents@d93bed6` och
`neptune_academy@5573189`. Det tariff-ID-nycklade katalogprovet är rättat och de nya
omockade E.ON-/Navirum-scenarierna passerar. Oberoende verifiering gav **1009 passed + 4
skipped Python**, **1023 passed TypeScript**, ren `tsc`, godkänt isolerat bygge,
**13/13 E2E**, byte-för-byte reproducerad genererad katalog och rena diffkontroller.

Granskning `2026-09-13-031` håller ändå push stängd. Lidköping 5d:s två, Batch 1:s sex
och Batch 2:s en redan aktiva tariff har fått en avvikande dispositionsetikett i stället
för den enhetliga `**Disposition:**`-raden. Samma nio block säger fortfarande
`investigation.status: utreds`, att policy/tester saknas och att UI inte är valbart.
Dokumentets påstående om en mekanisk 25/29/24-räkning och en enda nulägesbild är därför
ännu inte sant. Även en stale parentes om det gamla testnamnet sexton återstår.

Claude ska endast synkronisera dessa nio produktposter och rätta kommentaren, verifiera
den exakta 25/29/24 + 0/10/4-räkningen, logga och stanna för slutomgranskning. Själva
aktiveringen ska ligga kvar. Ingen ny tariffaktivering och ingen push.
