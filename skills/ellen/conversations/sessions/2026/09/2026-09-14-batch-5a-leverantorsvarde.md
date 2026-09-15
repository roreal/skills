---
session_id: "2026-09-14-002"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Codex omgranskning 2026-09-15-001: changes required före aktivering; källosann rullande-metadata, frikopplat/ofullständigt UI-prov, fel inventeringsrader och ofullständig bandmatris ska rättas. Ingen aktivering eller push; 37/27/28 består."
topic: "Batch 5a: åtta leverantörsvärdestariffer (C4, Kil, Skövde, Trollhättan, Katrineholm, Öresundskraft Totalvärme, Söderhamn, TEMAB)"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-5a.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5a"
---

# Session: Batch 5a — åtta leverantörsvärdestariffer

## Uppdrag

Robert gav explicit klartecken ("Ja starta") att starta implementationen enligt
Codex auktoritativa handoff `2026-09-14-002` och beredskapskontroll
`2026-09-14-011`. Ingen aktivering och ingen push i denna etapp — samtliga åtta
tariffer ligger bakom en ren, redan befintlig `investigation.status="utreds"`-
implementationsspärr. Ingen ny motorkod: alla åtta rader använder redan
`selected_band_affine`.

## Källverifiering (utförd på riktigt, 2026-09-14)

- **Kil** och **TEMAB**: officiella PDF:er hämtade direkt med `curl` (ingen
  bot-blockering denna gång). Verkliga SHA-256 matchade exakt handoffens
  angivna hashar:
  - Kil: `d8bb87ca07f92ea90a7165d4453384be32ac84cc99e60c8a0a9705caf5bb6e32`
    (samma som den redan katalogförda `kil-user-supplied-pricelist`).
  - TEMAB: `c4a1ac3bc559bb3befcd4c5d3a45ef8331c5a1d3f69abda16924475dbcb1a5e8`;
    sidorna 3–4 kontrollerade ordagrant mot katalogens 832 kr/MWh, tre taxor
    (1 677/488, 4 193/433, 31 448/348) och kalenderdagsperiodisering.
- **C4, Skövde, Trollhättan, Katrineholm, Öresundskraft, Söderhamn**:
  aktuella officiella webbsidor hämtade via WebFetch. Samtliga bekräftade
  katalogens lagrade 2026-priser, band och momsgrund ordagrant, inklusive
  C4:s fortsatt tvetydiga 500 kW-gräns.
- **Rättelse (granskning 2026-09-15-001, P2 #2):** föregående mening
  blandade av misstag ihop Kils och Skövdes proveniens i en gemensam
  sats. Kils `vat_basis="included"` bekräftades mot Kils EGEN frusna
  officiella PDF (inte Skövdes källa). Skövdes `vat_conversion`-figurer
  (628/458/200 och 1 605 kr/kW/år) hör uteslutande till Skövdes egen
  webbsida och avser Skövdes prisomräkning, inte Kils momsstatus.

## Katalogrättelser bakom spärr (`skills@527c4bb`)

- `contract_required:true` satt på samtliga åtta.
- **C4**: 500 kW-issuen ersatt med den redan godkända inledningen
  ("Metod för debiterbar effekt/kapacitet är inte fullständigt mappad...").
  R05 borttagen ur `investigation.request_ids`.
- **Kil**: alla fyra band fick `fixed:0` (var `null`). Den inaktuella
  "null i fast avgift"-issuen borttagen. `vat_basis="included"` och
  `vat_confirmation` orörda — inga belopp konverterade om.
- **TEMAB**: kategoritalsissuen normaliserad till den kända inledningen.
  `monthly_proration="days_in_month/365"` orörd. R12 borttagen.
- **Söderhamn**: R13 borttagen ur `investigation.request_ids`.
- **Skövde, Trollhättan, Katrineholm, Öresundskraft**: endast
  `contract_required:true` och proveniens — inga pris-/band-/formel-/
  momsändringar.
- `remaining_information_requests`: R05, R12 OCH R13 flyttade till
  `resolved_information_requests` med en explicit, tariffkorrekt
  `resolution_sv` per ärende — det att frågorna inte är externt besvarade
  men inte längre produktblockerande, och att den exakta C4-gränsen vid
  500 kW respektive Söderhamns byggnadstypsindex INTE är verifierade.
  **Rättelse (granskning 2026-09-15-001, P2 #2):** en tidigare version av
  denna rad påstod felaktigt att R13 var "helt borttagen" — den ligger
  faktiskt kvar, korrekt flyttad till `resolved_information_requests`,
  precis som R05/R12.
- Källproveniens: `retrieved_on` uppdaterat till 2026-09-14 för
  `web-review-c4-current`, `web-review-trollhattan-final`,
  `web-review-soderhamn-final`, `web-review-temab-final` och `oresund-web`;
  `web-review-temab-final` fick sin verkliga SHA-256. Nya källposter
  `web-review-skovde-current` och `web-review-katrineholm-current`
  tillagda och kopplade till respektive rad. Historiska `_0`-poster
  oförändrade.
- `schema_version` `0.1.16` → `0.1.17`, ny `change_log`-post.

## Policyer (`enkey-agents@e401147`)

Åtta nya `Tariffpolicy`-poster via de befintliga delade byggarna
`_familj4_kapacitet_krav`/`_familj4_band_id_krav` (samma mönster som Batch 1):
exakt två tariffspecifika, produktunika policyfält per rad — debiterbar
effekt/effektsignatur/anslutningseffekt/debiteringseffekt och ett bekräftat
band-ID/taxa-ID. `tackning=frozenset({"annual_forward"})`,
`stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False` på alla åtta.
Bandfälten läser sin allow-list direkt ur den skarpa prispostens `nivaer`
(`_niva()`/automatisk intervalltolkning ersätter aldrig ett bekräftat
leverantörsband — se C4-provet nedan).

`test_katalog_proveniens.py`s `_FORVANTAD_KATALOG_SHA256` uppdaterad
mekaniskt till den nya katalogfilens hash.

## TypeScript-motsvarighet (`neptune_academy@5e4a24e`)

`resultatkontrakt.batch5a.test.ts` speglar Pythonfilen: samma facit mot en
syntetisk men katalogtrogen `prisar`/`Tariffpolicy`, vars fält (energipriser,
band-`nivaer`, moms) är hämtade ordagrant ur Pythons verkliga
`till_prisar()`-utskrift för dessa åtta rader — ingen oberoende,
handkonstruerad kopia som kan drifta.

`tariffer.generated.ts` regenererad mot `skills@527c4bb`: diffen är exakt
proveniensraden (sha256 + commit); fortsatt 39 skarpa produkter (37 katalog
+ 2 leverantörsfiler), inget av de åtta Batch 5a-ID:na finns där.

## Verifiering

- **Python**: full svit `tools/tariffer/tests` — **1392 passed, 4 skipped**,
  0 failed (1272 baslinje + 120 nya i
  `test_leverantorsvarde_batch5a_kontrakt.py`). `git diff --check` rent.
- **TypeScript**: full svit — **1271 passed** i 43 filer (1236 baslinje +
  35 nya), 0 failed. `npx tsc --noEmit`: rent.
- Isolerat `npm run eval:build` (`dist-eval`, aldrig den riktiga `dist/`):
  rent, endast känd bundelstorleksvarning.
- **Mekaniskt**: katalogen har 86 fysiska poster;
  `godkanda(katalog, policyregister=POLICYREGISTER)` == **37** — inget av
  de åtta Batch 5a-ID:na ingår. En isolerad kopia med exakt de åtta
  spärrarna rensade (samma explicita policyregister) ger **45**
  katalogprodukter, alla åtta inkluderade. Den skarpa genererade payloaden
  är fortsatt 39 produkter totalt.
- Goldenfacit (10 MWh/månad, 10 kW, band enligt handoffens tabell) matchar
  exakt i båda språken för alla åtta rader; C4:s bekräftade band 5 och 6 ger
  olika, korrekta kostnader vid exakt 500 kW utan att `_niva()` överprövar
  det bekräftade valet.

## Öppet fynd — flaggat, inte löst i denna leverans

Handoffens punkt 6.3 (ett riktat UI-komponentprov med den isolerade
genererade kandidatposten: rätt två fält, fältnära fel, giltig submit,
produktbytesrensning) är **inte byggt** i denna runda. Kontrakts-/
motornivåtesterna ovan (Python + TypeScript) bevisar att policyn, banden
och felvägarna är korrekta, men den riktiga sidkomponenten
(`KalkylatorPage.tsx`) mot en isolerad Batch 5a-kandidat är inte provad.
Flaggas explicit för Codex, som i Batch 4 flaggade motsvarande gap öppet
i stället för att tysta det.

## Commits (lokalt, ingen push)

- `skills@527c4bb` — katalogrättelser bakom spärr, källproveniens,
  request-livscykel, batchplan-implementationsnot.
- `enkey-agents@e401147` — åtta policyer, ny testfil, katalog-SHA-uppdatering.
- `neptune_academy@5e4a24e` — TypeScript-golden, regenererad
  `tariffer.generated.ts`.

Ingen aktivering, ingen push. Stannar för Codex granskning av hela
implementationen.

## Codex granskning 2026-09-14-012

Codex granskade den lokala leveransen vid `skills@527c4bb` (leveranslogg
`skills@8ef55d0`), `enkey-agents@e401147` och `neptune_academy@5e4a24e`.
Bedömningen är **changes required före aktivering**.

Det allvarligaste reproducerade fyndet är att samtliga åtta policyer returnerar
`annual/exact/complete` om de två leverantörsvärdena anges med
`kvalitet="verified"`. Handoffens produktkontrakt kräver alltid `snapshot`, aldrig
`exact`; leveransens golden blir snapshot endast därför att kvalitet lämnas tom.
Det riktiga UI-komponentprovet saknas som redan flaggat, och TypeScriptfixturen är
inte maskinellt bunden till Pythons verkliga kandidatdata samt använder fel
defaultminimum för fyra tariffer. Full band-/felmatris, Kil-PDF:ens officiella
källfrysning, de åtta levande inventeringsraderna och requestdokumentationen måste
också rättas. Katalogens oavsiktliga helomformatering ska återställas.

Oberoende verifiering: 1392+4 skip Python, 1271 TypeScript, ren tsc och grönt
eval-bygge. 86 katalogposter, 37 godkända katalogprodukter och 39 skarpa produkter
består; isolerad verklig generering med exakt de åtta spärrarna rensade lyckas och
ger 47 totalprodukter. Ingen implementation ändrades av Codex, ingen spärr rensades
och ingen push gjordes.

Fullständiga fynd och bindande rättningsordning finns i
[`2026-09-14-012`](../../../reviews/2026/09/2026-09-14-granskning-batch-5a-implementation.md).

## Rättningsrunda 1 — svar på granskning 2026-09-14-012

Alla tre P1-fynd, alla tre P2-fynd och P3-fyndet rättade.

1. **P1 — `exact`-buggen stängd för samtliga åtta.** `_familj4_kapacitet_krav`
   fick ett explicit, default-`False` `rullande`-parameter (samma
   gissar-inte-mönster som `heltal`). Källverifierat per leverantör och satt
   `True` för alla åtta: C4 och Trollhättan säger redan "senaste 12
   månaderna"/"rullande" i sin egen källtext; Skövde och Söderhamn är
   rullande 3-årsmedel som uppdateras årligen; Kils officiella normalprislista
   (bilaga 2, "Effektreglering", avsnittet "Övriga") anger uttryckligen att
   kundens abonnerade effekt omprövas varje kalenderår (verifierat direkt mot
   den lokala PDF-filen med `pdftotext`); Öresundskrafts källtext nämner en
   "historikperiod"; Katrineholms effektsignatur och TEMAB:s kategoritalsmetod
   är båda per definition regressions-/historikbaserade och recalculeras
   löpande. Nya Python- och TypeScript-prov ger explicit `verified`-kvalitet
   på alla fält och asserterar att utfallet ändå är `annual/snapshot/complete`.
2. **P1 — det riktiga UI-komponentprovet byggt.** Ny
   `KalkylatorPageBatch5a.test.tsx` (C4 + Söderhamn, 11 prov): rätt
   fält/enheter, tom/icke-ändlig/under-minimum-effekt, tomt/okänt band/taxa,
   giltig submit, produktbyte i båda riktningarna. Samma runda fixade
   `_familj4_band_id_krav`s hårdkodade `etikett="Effektband"` (nu ett explicit
   parametervärde, default oförändrat) — Söderhamn/TEMAB får nu `etikett="Taxa"`.
3. **P1 — TypeScriptfixturen bunden till källan.** Ny `batch5aRawData.ts`
   (VERBATIM export av `till_prisar()`/`_policy_till_json()`-utdata) plus
   `batch5aRawData.driftprov.test.ts` (samma mönster som Batch 1:s,
   `execFileSync` mot enkey-agents, `toEqual`). `resultatkontrakt.batch5a.test.ts`
   byggd om att konsumera fixturen via `policyFranGenererad` i stället för en
   handskriven, frikopplad kopia; golden-facit förblir oberoende handräknat.
4. **P2 — full band-/felmatris i båda språken.** Python: nya bandgränsprov för
   Kil, Katrineholm, Öresundskraft och TEMAB (utöver de redan gröna Trollhättan/
   Söderhamn); under-minimum-prov för C4/Kil/Skövde/Katrineholm;
   `test_kr_och_schablon_blockeras` anropar nu verkliga `harled_resultatstatus`
   med `annual_inverse`/`monthly_invoice` i stället för att bara läsa
   `policy.tackning`. TypeScript: samma icke-ändlig-/under-minimum-/
   kr-schablon-genom-riktig-väg-prov tillagda i den ombyggda testfilen.
5. **P2 — Kils källa fryst, dokumentation synkad.** Katalogens
   `web-review-kil-vat` fick riktig titel/kind/`retrieved_on=2026-09-14`/SHA-256
   (verifierad mot lokal PDF-fil); Kils policy pekar nu dit i stället för det
   historiska `18_0`/användarfilen. R12/R13 fick var sin tariffkorrekta
   `resolution_sv` (var kopierad C4-text); testnamnet rättat till
   "…r05_r12_r13_flyttade_till_resolved" med explicit R13-assertion. Samtliga
   åtta rader i `tariffinventering-v22.md` fick synkad Katalogstatus/
   Kontraktsstatus/Teststatus/UI-status; verifieringslistans Skövde-,
   Katrineholm- och Kil-poster uppdaterade med aktuell källa och
   implementationsstatus.
6. **P3 — katalogens formatering återställd.** Skrevs om via
   `json.dump(indent=2, ensure_ascii=False)`; diffen mot `cb55614` (basen före
   Batch 5a) är nu 176 rader, inte 23 000+.

**Verifiering:** Python full svit **1411 passed, 4 skipped** (var 1392+4, +19
nya prov). TypeScript full svit **1335 passed** i 45 filer (var 1271, +64 nya).
`npx tsc --noEmit`: rent. Isolerat `npm run eval:build`: godkänt, endast känd
bundelstorleksvarning. Mekaniskt: katalog 86 poster, `godkanda(katalog)`==37,
isolerad kopia med åtta spärrar rensade ger 45. Disposition oförändrad
**37/27/28 av 92**.

**Commits (lokalt, ingen push):**

- `skills@caa5dd6` — katalogets `rullande`-korrigering (samma
  investigation-spärrar), Kils frysta officiella källa, R12/R13-resolutioner,
  åtta synkade inventeringsrader, verifieringslistans Skövde/Katrineholm/Kil,
  återställd tvåstegsindentering.
- `enkey-agents@674a057` — `_familj4_kapacitet_krav`s `rullande`-parameter,
  `_familj4_band_id_krav`s `etikett`/`hjalptext`-parameter, full
  band-/felmatris, riktiga `harled_resultatstatus`-kr/schablon-prov,
  uppdaterad katalog-SHA-konstant.
- `neptune_academy@c6c50a9` — `batch5aRawData.ts`/`.driftprov.test.ts`,
  ombyggd `resultatkontrakt.batch5a.test.ts`, ny
  `KalkylatorPageBatch5a.test.tsx`, regenererad `tariffer.generated.ts`
  (diffen är exakt proveniensraden).

Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-15-001

Codex omgranskade rättningsrunda 1 vid `skills@caa5dd6` (slutlig logghead
`skills@82e774b`), `enkey-agents@674a057` och `neptune_academy@c6c50a9`.
Bedömningen är fortsatt **changes required före aktivering**.

Rundan stänger generatorbindningen för TypeScriptfixturen, Kils källfrysning,
R12/R13-resolutionerna, verklig taxaetikett i policyn och katalogens formatering.
Fyra huvudproblem återstår:

1. `snapshot` har framtvingats genom `rullande=True` på alla åtta, trots att Kil,
   Skövde, Katrineholm och Söderhamn uttryckligen bygger på fasta årsunderlag och
   övriga inte alla har källstöd för kontinuerlig omräkning. Källsann metadata och
   ett explicit policytak för uppskattad `snapshot` krävs.
2. UI-provet handbygger policy/prispost i stället för att använda den
   generatorbundna fixturen, saknar kronor-/schablonflöden och dess `abc`-fall
   normaliseras till tomt i `type=number` i stället för att bevisa icke-ändligt tal.
3. Inventeringen märker sju orelaterade tariffer som Batch 5a-implementerade och
   lämnar sju riktiga Batch 5a-raders katalogstatus stale.
4. Den uppgivna fulla bandmatrisen saknar fortfarande senare band i Python och
   motsvarande matris helt i TypeScript. Äldre motsägelsefulla sessionsmeningar och
   fem osynkade verifieringsposter återstår också.

Oberoende verifiering: 140 riktade Pythonprov; tariffprojektets fulla scope
1411 passed/4 skipped; 99 riktade och 1335 fulla TypeScriptprov; ren tsc, grönt
eval-bygge och rena commitdiffar. Katalogen är fortsatt 86/37, exakt de åtta
spärrarna består och den skarpa filen har 39 produkter utan Batch 5a. Ingen
implementation ändrades av Codex, ingen aktivering eller push godkändes.

Fullständiga fynd och bindande rättningsordning finns i
[`2026-09-15-001`](../../../reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-1.md).

## Rättningsrunda 2 — svar på omgranskning 2026-09-15-001

Nya commit-hashar: `skills@ed2a63c`, `enkey-agents@c99ff79`, `neptune_academy@4f62fe8`.

1. **P1 (falsk `rullande`):** infört ett nytt, additivt policytak
   `takad_till_snapshot: bool` (Python `KravPost`) / `takadTillSnapshot?: boolean`
   (TypeScript `KravPost`), ömsesidigt uteslutande med `rullande` och validerat i
   konstruktorn i båda språken. Ger samma `ar_ej_helt_verifierbar`/
   `arEjHeltVerifierbar`-effekt (tvingar `snapshot`) UTAN att kräva ett nytt
   obligatoriskt UI-periodfält. Satt på sex av åtta leverantörer (Kil, Skövde,
   Katrineholm, Öresund Totalvärme, Söderhamn, TEMAB) vars källor genuint
   beskriver en fast, periodiskt reviderad grund — INTE bara de fyra granskningen
   nämnde (Kil, Skövde, Katrineholm, Söderhamn); Öresund Totalvärme och TEMAB
   visade sig vid källgranskning ha samma egenskap. C4 och Trollhättan behåller
   `rullande=True` (källorna beskriver genuint rullande värden — granskningens
   egna exempel). Källtexten för Katrineholm och Öresund Totalvärme rättad i
   samma commit (tog bort felaktiga "uppdateras/omräknas löpande"-påståenden).
2. **P1 (UI-provet):** `KalkylatorPageBatch5a.test.tsx` bygger nu de injicerade
   testposterna direkt ur `PRISAR`/`POLICY_JSON` (den generatorbundna fixturen i
   `batch5aRawData.ts`) i stället för handbyggda literaler. Lagt till kr-/
   schablonblockeringstäckning. Granskningens förslag att byta det icke-ändliga
   testfallet mot `'1e400'` verifierades EMPIRISKT INTE fungera: jsdom saniterar
   varje sträng som överlöper till ett icke-ändligt tal till en TOM sträng vid
   DOM-värdetilldelning för `<input type="number">`, identiskt med ogiltiga
   strängar som `'abc'` (verifierat direkt mot jsdom; exakt brytpunkt `1e308`
   kvar/`1e309` blir tomt). Detta är en genuin DOM/jsdom-spec-begränsning, inte en
   produktbugg — testet behåller `'abc'`, omdöpt och kommenterat för att ärligt
   beskriva begränsningen, och pekar till det oberoende, DOM-förbigående
   icke-ändlighetsbeviset i `resultatkontrakt.batch5a.test.ts`.
3. **P1 (fel åtta rader):** `tariffinventering-v22.md` hade fått FEL åtta rader
   markerade (Borås, Borlänge, C4, Falu regionalnät, Falun, Finspång, Habo,
   Jönköping — sju av dessa hör inte till Batch 5a), medan sju av de åtta RIKTIGA
   Batch 5a-raderna (samtliga utom C4) hade lämnats med sin gamla
   föraktiveringstext. Rättat: de sju felaktiga raderna återställda till sin
   ursprungliga text, de sju missade riktiga raderna fick Batch 5a-statustexten.
   En permanent mekanisk kontroll (`TestLevandeInventeringssync`, tre testmetoder)
   lades till som parsar HELA dokumentet och verifierar att EXAKT de åtta riktiga
   Batch 5a-ID:na — och inga andra — bär statustexten.
4. **P2 (bandmatris):** ersatt de tidigare inkompletta, blandade
   parametriseringarna med en komplett matris per leverantör (Python) som täcker
   varje bands min- och maxgräns för samtliga sex icke-C4/icke-Skövde-leverantörer
   (44 parametriserade prov). Hittade och rättade i samma svep ett äkta testfel:
   Kils lägsta testpunkt använde `kw=0` (katalogbandets golv) men Kils policy har
   `minvarde=8`, vilket gav `ValueError` — rättat till `kw=8` med omräknat facit
   `9262.32`.
5. **P2 (sessions-/verifieringsdokumentation):** Kil-VAT/Skövde-meningen och
   R13-påståendet ovan i denna fil rättade (se `Rättelse`-noterna i
   Källverifiering- och Katalogrättelser-avsnitten). `verifieringslista-fjarrvarmebolag.md`
   fick de fem saknade "återverifierad 2026-09-14, Batch 5a"-annotationerna
   (C4, Söderhamn, TEMAB, Trollhättan, Öresundskraft). Katalogens Kil-VAT-källpost
   fick en dokumenterande `note` som bekräftar att handoffens `bolag.kil.se`-URL
   och katalogens `kilsenergi.kil.se`-URL är byteidentiska aliaser (matchande
   SHA-256) — ingen tariffdata ändrad, bara metadata; katalogens
   `_FORVANTAD_KATALOG_SHA256` uppdaterad i samma commit.

**Sidoeffekt upptäckt och rättad under verifiering:** det nya Python-fältet
`takad_till_snapshot` serialiseras av `dataclasses.asdict()` i ALLA policyer, inte
bara Batch 5a:s — vilket fick TVÅ redan incheckade generator-bundna
`neptune_academy`-fixturer att driva isär från sin källa (upptäckt mekaniskt av
deras egna driftprov). `batch3bGenerated.json` regenererad från den isolerade
katalogkopian (verifierad semantiskt identisk i övrigt). `batch1RawData.ts`
(handunderhållen) fick fältet tillagt i `Batch1KravRaw`-gränssnittet och
`KRAV_DEFAULT`. En mindre `tsc`-typfix krävdes också i `byggPost`s parametertyp
(`id: string` → `id: keyof typeof PRISAR`) efter UI-provets omskrivning.

**Verifiering (denna rättningsrunda, körd på riktigt):**
- Python: `pytest tools/tariffer/tests/` → **1439 passed, 4 skipped**.
- TypeScript: `vitest run` → **1381 passed** (45 filer).
- `tsc --noEmit`: rent.
- Isolerad `npm run eval:build` (dist-eval, aldrig den skarpa `dist/`): bygger rent.
- Katalog: 86 fysiska poster, `godkanda(katalog)` == 37.
- Samtliga åtta Batch 5a-rader: `investigation.status="utreds"`,
  `contract_required=True`, `production_ready=False`.
- Skarpa `tariffer.generated.ts`: 39 produkter, noll Batch 5a-ID:n.
- Disposition mekaniskt verifierad **37 implemented / 27 ready / 28 blocked av 92**
  (mekanisk tally av dokumentets 78 `**Disposition:**`-fält: 29/25/24, plus
  variant-tabellens 8/2/4 = 14 → 37/27/28 av 92 — oförändrad).
- `git diff --check`: rent i alla tre repon.

Ingen aktivering, ingen push. Väntar på Codex' nästa omgranskning.
