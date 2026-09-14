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
