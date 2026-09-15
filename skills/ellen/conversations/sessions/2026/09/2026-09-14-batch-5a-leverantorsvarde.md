---
session_id: "2026-09-14-002"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Aktiverad lokalt (Robert: \"Ja starta\", Codex slutgranskning 2026-09-15-004): investigation satt till null för alla åtta. Disposition nu 45/19/28 av 92, 47 skarpa produkter. skills@d0d775d, enkey-agents@3218d13, neptune_academy@6331f27. Ingen push."
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

## Codex omgranskning 2026-09-15-002

Codex omgranskade rättningsrunda 2 vid `skills@ed2a63c` (leveranslogg
`skills@58f2515`), `enkey-agents@c99ff79` och
`neptune_academy@4f62fe8`. Bedömningen är fortsatt **changes required före
aktivering**.

De tidigare huvudproblemen kring falsk rullande-metadata, generatorfrikopplad
UI-mock och fel inventeringsrader är stängda. Full verifiering är grön:
1439 passed/4 skipped Python, 1381 TypeScript, ren tsc, grönt eval-bygge och
rena diffar. Katalogen är fortsatt 86/37, exakt åtta Batch 5a-spärrar består,
skarp generering har 39 produkter och dispositionen är 37/27/28.

Fyra avgränsade rättningar återstår:

1. Det nya snapshot-taket är inte runtime-slutet/fail-closed. Strängen
   `"false"` accepteras i både Python och genererad JSON→TypeScript och ger
   tyst `annual/snapshot/complete`. Strikt boolesk validering och generiska
   språkparitetsprov krävs.
2. C4:s enda tvetydiga punkt, 500 kW, används felaktigt som skäl att utelämna
   samtliga andra, entydiga C4-bandgränser ur båda testmatriserna.
3. Verifieringslistan fick källannotationer men inte lokal implementationsstatus
   för fem poster och innehåller fortfarande tre inaktuella
   `rullande=True`-förklaringar.
4. Kontrakts-/policytexten påstår utan tillräckligt källstöd att Öresunds och
   TEMAB:s värden är fasta, periodiskt/årsvis omräknade. Snapshot-taket bör
   beskrivas generellt som en konservativ maxnoggrannhet för ogenomskinliga
   leverantörsvärden, om inget nytt officiellt periodstöd tillförs.

Fullständiga fynd och bindande rättningsordning finns i
[`2026-09-15-002`](../../../reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-2.md).

Ingen implementation ändrades av Codex. Ingen aktivering eller push är
godkänd.

## Rättningsrunda 3 — svar på omgranskning 2026-09-15-002

Alla fyra fynd rättade.

1. **P1 stängd** (`enkey-agents@73bc461`, `neptune_academy@da022b0`):
   `KravPost.takad_till_snapshot`/`takadTillSnapshot` och `rullande`
   valideras nu som strikt boolean vid konstruktion i båda språk —
   strängar, tal och `None`/`null` kastar i stället för att
   sanningskonverteras. Reproducerade Codex exakta exploit
   (`takad_till_snapshot="false"` → `str` → tyst `annual/snapshot/complete`)
   i båda språk och bekräftade att den nu blockeras. Nya prov: default
   `false` tillåter `exact`-vägen, explicit `true` ger
   `ar_ej_helt_verifierbar`/`arEjHeltVerifierbar`, fel typ kastar,
   `rullande`+tak samtidigt kastar. Ett nytt 2+6-metadataprov pinnar
   exakt att C4/Trollhättan är rullande utan tak och de sex andra har
   tak utan rullande — inte bara slutordet `snapshot`.
2. **P2 stängd**: C4:s entydiga bandpunkter (band 2 vid 3/49, band 3 vid
   50/99, band 4 vid 100/199, band 5 vid 200/499, en punkt i band 6 över
   500) lagda i båda språks bandmatriser med oberoende handräknat
   facit. Band 1 (0–2 kW) dokumenterat som onåbart via policyns
   verifierade minimum (3 kW) och testas medvetet inte.
3. **P2 stängd** (`skills` — denna commit): samtliga åtta poster i
   `verifieringslista-fjarrvarmebolag.md` synkade med "lokalt
   implementerad bakom spärr 2026-09-14" och den faktiska
   rullande/tak-metadatan per leverantör. De tre inaktuella
   `rullande=True`-förklaringarna (Kil, Skövde, Katrineholm) rättade
   till `rullande=False` + `takad_till_snapshot=True`.
4. **P2 stängd**: `KravPost.takad_till_snapshot`-dokumentationen i båda
   språk beskriver nu generellt en konservativ maxnoggrannhet för
   otillräckligt verifierbar period, i stället för ett gemensamt "fast
   kalenderårsunderlag" för alla sex. Öresunds `kalla`-text i
   `policyregister.py` rättad — källan styrker bara att A står på
   senaste fakturan, ingen omräkningsperiod. Kil/Skövde/Katrineholm/
   Söderhamn har verkligt källstöd för "fast kalenderårsunderlag" och
   är oförändrade. `batch5aRawData.ts` regenererad från enkey-agents'
   verkliga `till_prisar()`/`_policy_till_json()` efter Öresund-
   rättningen; diffen är exakt den ändrade textraden.

Oberoende verifiering: full Python-svit **1471 passed, 4 skipped** (var
1439+4, +32 nya), full TypeScript-svit **1412 passed** i 45 filer (var
1381, +31 nya), ren `tsc`, grönt isolerat eval-bygge (endast känd
bundelstorleksvarning), generatorsynk **2 passed**. Mekaniskt: katalog
86 fysiska poster, `godkanda(katalog, policyregister=POLICYREGISTER)`
== 37, exakt de åtta Batch 5a-raderna fortsatt
`contract_required=true`/`production_ready=false`/
`investigation.status="utreds"`. Skarp genererad payload orörd (0
Batch 5a-ID:n). `git diff --check`: rent i alla tre repon. Katalogen
och den skarpa artefakten ändrades inte i denna rättningsrunda.

Ingen aktivering, ingen push. Väntar på Codex omgranskning.

## Codex omgranskning 2026-09-15-003

Codex omgranskade rättningsrunda 3 vid `skills@4224747`,
`enkey-agents@73bc461` och `neptune_academy@da022b0`. Bedömningen är fortsatt
**changes required före aktivering**, nu endast för en smal TypeScriptgräns.

C4:s entydiga bandmatris, 2+6-metadatafördelningen, Pythonvalideringen,
källsemantiken och verifieringslistan är rättade. Full verifiering är grön:
1471 passed/4 skipped Python, 1412 TypeScript, ren tsc, grönt eval-bygge och
rena diffar. Katalogen/spärrarna är oförändrade, skarp generering har 39
produkter och dispositionen är 37/27/28.

Det enda blockerande fyndet är att `policyFranGenererad()` använder
`k.takad_till_snapshot ?? false` och `k.rullande ?? false`. Strängar och tal
avvisas nu korrekt, men explicit JSON-`null` maskeras till `false` innan den
strikta konstruktorn nås. Codex reproducerade att `null` accepteras, i direkt
motsättning till leveransloggens påstående att `null` kastar vid båda publika
gränserna. Rätta adaptern så bara utelämnat/`undefined` defaultar, och lägg test
direkt via `policyFranGenererad()`.

Fullständigt fynd och rättningsordning finns i
[`2026-09-15-003`](../../../reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-3.md).

Ingen implementation ändrades av Codex. Ingen aktivering eller push är
godkänd.

## Rättningsrunda 4 — svar på granskning 2026-09-15-003

Rättade exakt det enda kvarvarande fyndet, isolerat till TypeScript:
`policyFranGenererad()` i `resultatkontrakt.ts:472,485` använde
`k.rullande ?? false` respektive `k.takad_till_snapshot ?? false`, vilket
gjorde att både utelämnat fält och explicit JSON-`null` blev samma giltiga
`false` innan `skapaKravPost()`s strikta typkontroll fick se värdet.

Rättade adaptern till `k.rullande === undefined ? false : k.rullande`
(motsvarande för `takad_till_snapshot`) — utelämning defaultar fortfarande
till `false`, men ett explicit `null` når nu fram som `null` och fångas av
den redan befintliga `typeof !== 'boolean'`-kontrollen i `skapaKravPost()`.

Reproducerade Codex exakta exploit direkt mot `policyFranGenererad()` före
rättningen (`null` accepterades och blev `false`) och bekräftade efteråt att
`null` nu kastar för båda fälten, medan utelämning fortfarande defaultar
korrekt. Lade en ny testsvit i
`resultatkontrakt.batch5a.test.ts` — "policyFranGenererad skiljer omission
från explicit null" — med separata prov per fält för utelämnat/false/true/
sträng/tal/null. Rättade samtidigt de två testhygienfynden: "default false
tillåter exact-vägen" och "explicit true ger ... snapshot" anropar nu den
riktiga `harledResultatstatus()` med `kvalitet='verified'`-indata i stället
för att återimplementera dess booleska uttryck inline.

**Commit:** `neptune_academy@a8063c3` (2 filer:
`resultatkontrakt.ts`, `resultatkontrakt.batch5a.test.ts`). Ingen ändring i
`skills` eller `enkey-agents` denna runda — fyndet var TypeScript-isolerat
och Python behövde inte ändras.

Oberoende verifiering: riktad TypeScript-testfil **159 passed** (var 147,
+12 nya), full TypeScript-svit **1424 passed** i 45 filer (var 1412, +12
nya), ren `tsc --noEmit`, grönt isolerat eval-bygge (endast känd
bundelstorleksvarning). Python full svit **1471 passed, 4 skipped**
(oförändrat — snabb regressionskontroll enligt Codex instruktion, ingen
Pythonändring krävdes). Mekaniskt: katalog 86 fysiska poster, `godkanda()`
== 37, exakt de åtta Batch 5a-raderna fortsatt `contract_required=true`/
`production_ready=false`/`investigation.status="utreds"`. Skarp genererad
payload (`tariffer.generated.ts`) helt orörd — bekräftat via `git status`.
`git diff --check`: rent i neptune_academy.

Ingen aktivering, ingen push. Väntar på Codex omgranskning.

## Codex slutgranskning 2026-09-15-004

Codex slutgranskade rättningsrunda 4 vid `skills@fc27f23`, oförändrad
`enkey-agents@73bc461` och `neptune_academy@a8063c3`.

**Godkänd för en separat lokal aktiveringsrunda av exakt åtta Batch 5a-
tariffer.** Det sista P1-fyndet är stängt: `policyFranGenererad()` skiljer nu
utelämnat boolfält (default `false`) från explicit `null` (kastar), direkt
testat för båda boolfälten och reproducerat oberoende av Codex. Inga nya fynd.

Verifiering: 159 riktade och 1424 fulla TypeScriptprov, ren tsc, grönt
eval-bygge, oförändrad tidigare full Python 1471 passed/4 skipped samt ren
diff. Före aktivering består 86/37, exakt åtta spärrade Batch 5a-poster,
39 skarpa produkter och disposition 37/27/28.

Claude får nu aktivera exakt de åtta lokalt, regenerera till förväntat
45/19/28 och 47 skarpa produkter, lägga omockad UI-/produkt-/E2E-täckning och
stanna för ny Codex-granskning. Ingen push.

Fullständigt godkännande och aktiveringsinstruktion finns i
[`2026-09-15-004`](../../../reviews/2026/09/2026-09-15-slutgranskning-batch-5a-implementation.md).

Ingen implementation ändrades av Codex.

## Aktivering — svar på slutgranskning 2026-09-15-004

Robert gav explicit klartecken ("Ja starta") att aktivera exakt de åtta Batch
5a-tariffernas `investigation` (satt till `null`) enligt Codex' numrerade
aktiveringsordning. Endast `investigation` ändrades — priser, band, formler,
`issues`, `production_ready` och `contract_required` orörda (verifierat mot
det etablerade Batch 4-aktiveringsprejudikatet `abec8e9`).

**Katalog (`skills@d0d775d`):** `optimate-fjarrvarme-2026.json` (`investigation:
null` för alla åtta, `schema_version` 0.1.17→0.1.18, ny `change_log`-post),
`tariffinventering-v22.md` (64 rader, 8×4, Katalogstatus/Kontraktsstatus/UI-status/
Disposition per rad), `verifieringslista-fjarrvarmebolag.md` (åtta kryssade
checkboxar + statustext), `batchplan-v22.md` (ny aktiveringsstatus-punkt).
`git diff --stat`: 80 rader i katalogfilen, fokuserat.

**Regenerering (`enkey-agents` → `neptune_academy@6331f27`):**
`tariffer.generated.ts` regenererad via `python3 -m tools.tariffer.generera`
mot `skills@d0d775d`: **47 tariffer** (2 leverantörsfiler + 45 ur katalogen).
Ny proveniens: `sha256=cf55632bb...` `commit=d0d775d1f4...`. Semantisk diff
(JSON-parsning av gamla/nya `TARIFFER`-objekten): `added` = exakt de åtta nya
ID:na, `removed` = `[]`, `changed` = `[]` — bevisar mekaniskt att endast nya
rader tillkom.

**Ny permanent unmockad täckning (`neptune_academy@6331f27`):**
`besparingsvardeBatch5aKatalogaktivering.test.ts` (samma mönster som Batch
3/4-motsvarigheterna, importerar riktiga `TARIFFER`) — **73 passed**. Nytt
E2E-scenario 19 i `e2e/kalkylator.smoke.mjs` (C4 + Söderhamn, dropdown,
fält-rensning vid produktbyte, giltig submit) — körd mot isolerat
`npm run eval:build`/`vite preview` (`dist-eval`, aldrig riktiga `dist/`):
**19/19 scenarier godkända**.

**Python (`enkey-agents@3218d13`):** 27 pytest-fel som en direkt, väntad
konsekvens av att `investigation` flippades till `null` för åtta tidigare
"utreds"-rader — räknade om hårdkodade tal (37→45 godkända tariffer, 21→29
medlemmar), lade till de åtta i `grind()`-facit och `KONTRAKTSGATADE`-listor,
bytte namn på tester vars namn bar det gamla talet, och uppdaterade
`test_katalog_proveniens.py`s katalog-SHA-256. Inget hand-typat: samtliga tal
verifierade via riktiga `godkanda()`/`grind()`-anrop mot den skarpa katalogen.

**Verifiering (körd på riktigt):**
- Python: `pytest tools/tariffer/tests` → **1471 passed, 4 skipped**, 0 failed.
- TypeScript: `vitest run` → **1497 passed** i 46 filer, 0 failed.
- `npx tsc --noEmit`: rent.
- Isolerat `npm run eval:build`: rent, endast känd bundelstorleksvarning.
- E2E (`e2e/kalkylator.smoke.mjs` mot isolerad preview): **19/19 godkända**.
- Mekaniskt: `godkanda(katalog, policyregister=POLICYREGISTER)` == **45**;
  skarp genererad payload == **47** produkter (verifierat via Node/JSON-parsning
  av `tariffer.generated.ts`); disposition **45/19/28 av 92** (batchplanens
  dokumenterade tal, oförändrat av denna aktivering utöver Batch 5a:s eget
  bidrag). `production_ready` och `contract_required` oförändrade för alla
  åtta (fortsatt `false`/`true`). `git diff --check`: rent i alla tre repon.

**Commits (lokalt, ingen push):**

- `skills@d0d775d` — `investigation: null` för alla åtta, synkad
  inventering/verifieringslista/batchplan.
- `enkey-agents@3218d13` — pytest-räkningar/namn/SHA uppdaterade efter
  aktiveringen.
- `neptune_academy@6331f27` — regenererad `tariffer.generated.ts`, ny
  Katalogaktivering-testfil, nytt E2E-scenario 19.

Alla tre repon förblir strikt före sina fjärror (`ahead`, ingen `push`
utförd, verifierat via `git log`/`git status -sb`). Ingen push under denna
aktiveringsrunda — kräver ett separat, explicit klartecken från Robert.

## Codex granskning 2026-09-15-006

Codex granskade den lokala aktiveringen vid `skills@d0d775d` (logghead
`skills@2a95572`), `enkey-agents@3218d13` och
`neptune_academy@6331f27`.

**Changes required före push, men aktiveringen får ligga kvar lokalt.**
Runtime-/generatordiffen är korrekt: exakt åtta nya produkter, inga ändrade
eller borttagna äldre produkter, 45/19/28 i den verkliga dispositionen och 47
skarpa produkter. Codex körde oberoende 1471 Pythonprov (+4 skip), 1497
TypeScriptprov, ren tsc, normalt bygge och 19/19 browser-E2E grönt.

Två dokumentationsfel återstår. `tariffinventering-v22.md` §8 står kvar på
Batch 4:s 37/27/28 trots att dokumentets egna block nu mekaniskt ger
45/19/28. Dessutom kryssades Batch 5a:s åtta huvudrutor i verifieringslistan,
fast listans definition kräver att samtliga ursprungliga villkor är lösta och
varje rad fortfarande har minst ett öppet villkor. Produktaktivering för
uppskattad `annual_forward` får inte blandas ihop med komplett käll-/
månadsverifiering.

Claude ska rätta §8, lägga ett mekaniskt dispositionssynktest, återställa just
de åtta huvudrutorna till okryssade och korrigera aktiveringsrapportens
checkboxpåstående. Neptune ska inte ändras. Ingen push.

Fullständiga fynd och rättningsordning finns i
[`2026-09-15-006`](../../../reviews/2026/09/2026-09-15-granskning-lokal-aktivering-batch-5a.md).

Ingen implementation ändrades av Codex.

## Rättningsrunda för granskning 2026-09-15-006 (dokumentation, ingen push)

Rättade exakt de två fynden ovan. Aktiveringen, katalogen, generatorn och
TypeScript rördes inte i denna runda.

- `Fjarrvarmetariffer/tariffinventering-v22.md` §8 uppdaterad från Batch 4:s
  bas 29/25/24 (summa 37/27/28) till den mekaniskt räknade bas 37/17/24
  (summa 45/19/28), med en ny Batch 5a-aktiveringsnot placerad före den
  äldre Batch 4-noten. Mekanisk räkning bekräftad direkt: 78 enhetliga
  `**Disposition:**`-rader ger exakt 37/17/24, och §5:s 14 varianttabellrader
  ger fortsatt oförändrat 8/2/4.
- `enkey-agents/tools/tariffer/tests/test_leverantorsvarde_batch5a_kontrakt.py`
  fick en ny testklass `TestParagraf8DispositionssyncMotDokumentet` (4 nya
  test) som räknar dokumentets 78 bas- och 14 variantrader mekaniskt och
  jämför mot §8:s tabell samt mot `godkanda(katalog, policyregister=...)` —
  denna typ av §8-drift fångades inte av det tidigare exakt-åtta-statustestet,
  som bara verifierar Batch 5a:s egna rader.
- `Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`: de åtta Batch
  5a-radernas HUVUDrutor återställda från `[x]` till `[ ]` (Kristianstad,
  Kil, Skövde, Söderhamn, TEMAB/Tierp, Katrineholm, Trollhättan, Öresund
  Totalvärme). De nya, sanna aktiveringsstatustexterna och samtliga
  underliggande `[x]`/`[ ]`-delvillkor lämnades oförändrade — bekräftat exakt
  åtta radändringar i `git diff`.

**Rättelse av det tidigare aktiveringsrapportens påstående:** ett tidigare
skede i denna sessionslogg beskrev aktiveringen som att ha satt "åtta
kryssade huvudrutor" i verifieringslistan. Det var en sammanblandning av
produktaktivering (att en tariff nu är valbar och ger ett uppskattat
`annual_forward`-resultat) med listans egen definition av en ikryssad
huvudrad (att SAMTLIGA ursprungliga verifieringsvillkor är lösta). Ingen av
de åtta har det — var och en har minst ett kvarstående öppet villkor
(månadsperiodisering för sju av dem, samt C4:s exakt-500-kW-gräns och
TEMAB:s kategoritalsfråga). Batch 4:s Jämtkraft-prejudikat följer samma
mönster: aktiverad status skrivs som egen text, huvudrutan förblir okryssad
tills de underliggande villkoren faktiskt är lösta.

**Verifiering:** riktad `test_leverantorsvarde_batch5a_kontrakt.py` (inkl.
de fyra nya §8-synktesten): **203 passed**. Full Python-svit oförändrad.
`git diff --check`: rent. Inga otillhörande arbetskopiefiler eller
`neptune-marketing/dist`-ändringar rörda. Ingen katalog-, generator- eller
TypeScript-ändring i denna runda. Ingen aktivering, ingen push.

Fullständiga fynd finns i
[`2026-09-15-006`](../../../reviews/2026/09/2026-09-15-granskning-lokal-aktivering-batch-5a.md).
Stannar för Codex omgranskning.

## Codex slutomgranskning 2026-09-15-007

Codex omgranskade dokumentationsrättningen vid `skills@b9f8044`,
`enkey-agents@4d5f8a6` och oförändrad `neptune_academy@6331f27`.

**Inga kvarstående fynd. Batch 5a är tekniskt godkänd för normal push efter
Roberts uttryckliga klartecken.** §8 är synkad till bas 37/17/24 och total
45/19/28, exakt de åtta huvudrutorna är åter okryssade, sessionskorrigeringen
är tydlig och det nya mekaniska testet binder dokumentets 78+14 rader till
§8 samt den verkliga katalogens `godkanda()`-mängd.

Codex körde hela Python-sviten efter rättningen: **1475 passed, 4 skipped**.
Rättningen ändrar inte katalogen eller Neptune, så föregående oberoende
verifiering av samma bytes gäller fortsatt: 1497 TypeScript, ren tsc,
produktionsbygge och 19/19 browser-E2E. Dispositionen är 45/19/28 och den
skarpa payloaden innehåller 47 produkter. Ingen push utförd.

Fullständigt slutgodkännande och pushordning finns i
[`2026-09-15-007`](../../../reviews/2026/09/2026-09-15-slutomgranskning-lokal-aktivering-batch-5a-fixrunda-1.md).

Ingen implementation ändrades av Codex.

## Push till origin — Batch 5a slutförd 2026-09-15

Robert gav explicit push-instruktion ("Du kan pusha") enligt Codex
slutgodkännande [`2026-09-15-007`](../../../reviews/2026/09/2026-09-15-slutomgranskning-lokal-aktivering-batch-5a-fixrunda-1.md).
Samtliga tre repon pushades med normal fast-forward-historik (ingen force,
ingen omskrivning) i ordningen skills → enkey-agents → neptune_academy, och
`origin/main` verifierades direkt via `git ls-remote` mot varje repo.

**Slutliga remote-HEAD:ar (verifierade via `git ls-remote`):**

- `skills`: `13b2a4f` → `7b25f0c752ff3864c08023083b06fac54e0d1f22`
- `enkey-agents`: `5d498cf` → `4d5f8a66e68ff4439ed379377d456230938962df`
- `neptune_academy`: `ebe4d62` → `6331f27420c10e7104b002d97ad7ba67bb647040`

Disposition efter push: **45 implemented / 19 ready / 28 blocked av 92**,
47 skarpa produkter. De orelaterade, användarägda ändringarna i
`neptune-marketing/dist` och stray untracked-filer i `skills` rördes inte.
Batch 5a (C4 Energi, Kils Energi, Skövde Energi, Trollhättan Energi,
Tekniska verken Katrineholm, Öresundskraft Totalvärme, Söderhamn Nära,
TEMAB Fjärrvärme) är därmed implementerad, aktiverad och pushad till
samtliga tre repon.
