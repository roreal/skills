---
session_id: "2026-09-14-002"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Codex granskning 2026-09-14-012: changes required före aktivering; exact-statusväg, UI-/drift-/bandtest, Kil-proveniens och levande dokumentation ska rättas. Ingen aktivering eller push; 37/27/28 består."
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
  katalogens lagrade 2026-priser, band och momsgrund ordagrant (inklusive
  C4:s fortsatt tvetydiga 500 kW-gräns, Kils moms-inklusive-status via
  Skövdes vat_conversion-källfigurer 628/458/200 och 1 605 kr/kW/år).

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
- `remaining_information_requests`: R05, R12 flyttade till
  `resolved_information_requests` med en explicit not att frågorna inte är
  externt besvarade men inte längre produktblockerande, och att den exakta
  C4-gränsen vid 500 kW INTE är verifierad. R13 helt borttagen (Söderhamns
  egen rad hade ingen kvarvarande hängande referens att flytta separat).
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

**Verifiering:** Python full svit **1410 passed, 4 skipped** (var 1392+4).
TypeScript full svit **1335 passed** i 45 filer (var 1271). `npx tsc --noEmit`:
rent. Mekaniskt: katalog 86 poster, `godkanda(katalog)`==37, isolerad kopia med
åtta spärrar rensade ger 45. Disposition oförändrad **37/27/28 av 92**.

Ingen aktivering, ingen push. Stannar för Codex omgranskning.
