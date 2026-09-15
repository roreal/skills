---
session_id: "2026-09-15-018"
created_at: "2026-09-15T21:08:00+02:00"
participants:
  - Robert
  - Codex
  - Claude
status: "Implementerad lokalt bakom spärr, INTE aktiverad, INTE pushad. skills@c5d499d, enkey-agents@d08fd5e, neptune_academy@36c1ed0. Väntar på Codex kodgranskning."
scope: "Batch 5c — åtta tariffer med säsongsvis flödesavgift"
remote_baseline:
  skills: "df41660620f572b5b22d7dd27332c68b1be62049"
  enkey_agents: "5eaca3c4f3eafb3c7065319803592abe062f49ae"
  neptune_academy: "28ae62945ed50b23cffadd5a7b3070cc2d5c41ae"
relates_to:
  - "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5c.md"
  - "conversations/handoffs/2026/09/2026-09-15-batch-5c-sasongsflode.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5c"
---

# Session: Batch 5c — säsongsflöde

## 2026-09-15 21:08 — Codex förbereder nästa steg

Robert meddelade att Claude verifierat Batch 5b-pushen och bad Codex
förbereda nästa steg.

Codex verifierade att lokala huvuden matchar `origin/main`:

- `skills@df41660620f572b5b22d7dd27332c68b1be62049`
- `enkey-agents@5eaca3c4f3eafb3c7065319803592abe062f49ae`
- `neptune_academy@28ae62945ed50b23cffadd5a7b3070cc2d5c41ae`

`enkey-agents` och `neptune_academy` är rena. `skills` innehåller sedan
tidigare orelaterade ändringar/otaggade filer; de ingår inte i detta uppdrag
och ska lämnas orörda.

Beredskapskontroll `2026-09-15-018` godkänner lokal implementation av
Batch 5c bakom spärr. Handoff `2026-09-15-002` ger Claude ett bindande
uppdrag för exakt åtta tariffer.

Det centrala beslutet är att säsongsflöde ska bäras som en 12-elements
kalendermånadsserie i befintliga `number_series`/`falt_serier`, varefter
motorn summerar exakt varje `volume`-posts egna `months`. Därmed kan 5, 6,
7 och 9 debiteringsmånader bevisas mekaniskt och ett exkluderat månadsflöde
garanteras ge noll kostnadsbidrag.

Sju tariffer kräver leverantörens effekt + bekräftat band + flödesserie.
Mälarenergi 2–4 lägenheter saknar kapacitetsdel och kräver bara energi och
flödesserie utöver sin fasta årsavgift. R03 ska scopesäkras till de två
andra fortsatt blockerade Mälarenergi-raderna; frågan är inte besvarad.

Utgångsläge och grind:

- skarpt under implementation: 51/13/28, 53 produkter;
- isolerat med exakt åtta spärrar rensade: 59/5/28, 61 produkter;
- ingen aktivering och ingen push före Codex granskning och Roberts senare
  uttryckliga beslut.

## 2026-09-15 22:05 — Claude implementerar Batch 5c lokalt bakom spärr

Implementationen följer handoff `2026-09-15-002` och beredskapskontroll
`2026-09-15-018` punkt för punkt.

### Python (enkey-agents)

- `justeringar.py`: ny `_valid_volume()` — sluten schemakontroll av
  katalogens `volume`-post (exakt nycklarna `type/rate/unit/months`,
  `unit="SEK/m3"`, ändligt positivt `rate`, icke-tom lista av unika
  heltalsmånader 1–12), inkopplad i `okand_justering()`.
- `faktura.py`: `_flodesavgift()` läser postens egen `months` — exakt
  `{1..12}` behåller den skalära helårsvägen (`falt["flode_m3"]`/MWh-
  reserv, oförändrad), en riktig delmängd summerar
  `falt_serier["flode_m3"][m]` för postens egna månader och kastar om
  serien saknas — aldrig MWh/FLODE_DELTA_T-reserven för en säsongspost.
- `policyregister.py`: `kontrollera_volymbindning()` utökad att kräva
  `vardetyp='number_series'`, `antal_varden=12`, `rullande=False`,
  `takad_till_snapshot=True` för en säsongspost (oförändrat
  `vardetyp='number'` för helår), plus en ny generisk "exakt en
  volume-post"-kontroll. Ny delad byggare `_sasongsflode_krav()`. Åtta
  nya `Tariffpolicy`-objekt registrerade (Luleå, Öresundskraft
  Helsingborg/Ängelholm, Piteå centrala/Norrfjärden-Sjulnäs, Nevel,
  Tekniska verken Linköping, Mälarenergi 2–4 lägenheter utan
  `kapacitet_bindning`/`kapacitet_band_bindning`).
- Ny fil `generera_isolerad_batch5c.py` (speglar
  `generera_isolerad_batch5b.py`) för den isolerade kandidatgenereringen.
- Ny testfil `tests/test_leverantorsvarde_batch5c_kontrakt.py`: 85 prov
  — oberoende handräknat golden-facit för alla åtta (inkl. Nevels
  publicerade referensfall med båda avrundningsvarianterna dokumenterade
  och tydligt åtskilda), delta-prov (+100 m³ i inkluderad/exkluderad
  månad), serie-felmatris (saknad/skalär/11/13/sträng/negativ/NaN),
  postens egen schemakontroll (dubblerad/malformad `volume`-post), R03-
  scopesäkring, regressionsprov för Batch 5b/VänerEnergi (skalärt
  helårsflöde oförändrat) och Mölndals icke-kontraktsstyrda legacyreserv,
  samt mekaniska räkningsgrindar (skarpt 51/53, isolerat 59/61 med
  exakt åtta nya ID:n och oförändrade 53 gamla).
- `tests/test_katalog_proveniens.py`: `_FORVANTAD_KATALOG_SHA256`
  uppdaterad till katalogens nya sha256 efter `contract_required`/R03-
  ändringarna.

### Katalog (skills)

- `contract_required: true` på exakt de åtta kandidaterna;
  `production_ready: false` och `investigation.status="utreds"`
  oförändrat för alla åtta.
- `R03` rättad från `member_ids: ["malarenergi"]` till en tariff-scopad
  `tariff_ids`-lista mot de två andra Mälarenergi-raderna (större
  fastigheter, gruppanslutna småhus); borttagen ur 2–4-lägenheters
  `investigation.request_ids`. Requestens fråga och `status="utreds"`
  oförändrade — en scopesäkring, inte ett externt svar.
- Källprovenienstexterna (URL:er, avgränsningar) i handoffen är redan
  återgivna i Python-policyernas `kalla`-fält (`_sasongsflode_krav`/
  `_familj4_kapacitet_krav`); katalogens egna `source_refs`/`sources`-
  poster för dessa åtta rördes INTE i denna omgång — endast
  `contract_required` och R03-scopet ändrades i katalogfilen. Detta är
  en medveten avgränsning: de exakta källcitaten står redan i
  handoffen/beredskapskontrollen och i policyernas `kalla`-fält, och en
  ändring av `source_refs`/`sources` skulle inte påverka någon
  beräkning eller grind. Flaggas explicit för Codex granskning i stället
  för att antas vara i scope.
- `billing_basis_method` för de sju kapacitetstarifferna lämnades
  OFÖRÄNDRAD (ingen av källorna gav en fullt styrkt, maskinellt
  omsatt formel att skriva om till) — samtliga sju effektfält är
  `takad_till_snapshot=True` i policyn i stället, exakt som handoffen
  kräver när sammanvägningen inte är fullt styrkt.

### TypeScript (neptune_academy/neptune-marketing)

- `fjarrvarme.ts`: `flodesavgift()` fick samma months-diskriminering
  och `faltSerier`-läsning som Python-sidan, med identisk kastvakt.
- Ny testfil `resultatkontrakt.batch5c.test.ts`: 58 prov, samma golden-
  facit-tal som Python-sidan, samma delta-/felmatris, plus ett
  regressionsprov för Mölndals skalära reservväg.
- `tariffer.generated.ts` regenererad från den oförändrade skarpa
  katalogen — fortfarande EXAKT 53 produkter, bara källkatalogens
  sha256/commit-provenienslinje ändrades.
- `kalkylator.smoke.mjs`: nya Scenario 21 (Luleå, effekt/band/tolv-
  rutors serie) och Scenario 22 (Mälarenergi 2–4 lägenheter utan
  kapacitetsfält), gated bakom `E2E_ISOLERAD_BATCH5C` — hoppas
  avsiktligt över i den ordinarie skarpa sviten. Samtidigt upptäcktes
  och rättades en latent bräcklighet i Scenario 19: dess
  `getByRole('option', {name: 'Öresundskraft'})` skulle ha fått en
  falsk träff (3 alternativ) så snart Batch 5c:s två nya
  Öresundskraft-produkter disambiguerar namnet — bytt till en regex
  som håller för båda namnformerna.
- Ny fil `e2e/batch5c-isolated-e2e.mjs` (speglar
  `batch5b-isolated-e2e.mjs` exakt: arkiverad `git archive`-kopia, egen
  port 4175, processunik `vantaPaViteRedo`) samt npm-scriptet
  `test:e2e:batch5c-isolated`. En separat portkonfliktsregression
  byggdes INTE för Batch 5c — den underliggande `vantaPaViteRedo`-
  mekanismen är oförändrad och redan permanent regressionstestad av
  Batch 5b:s `batch5b-isolated-e2e.port-conflict.test.mjs`; flaggas för
  Codex att bekräfta att detta är tillräckligt.

### Testresultat (samtliga körda efter slutlig commit)

- Python: **1691 passed, 4 skipped** (`pytest tools/tariffer/tests`).
- TypeScript: **1701 passed** i 52 testfiler (`npm test -- --run`).
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt, 971 moduler.
- Ordinarie `npm run test:e2e`: Scenario **1–20 gröna**, 21–22 korrekt
  överhoppade (loggat).
- `npm run test:e2e:batch5c-isolated`: Scenario **1–22 gröna** i den
  arkiverade, isolerade kopian (Luleå + Mälarenergi omockat, mot en
  riktig byggd sida).
- `git diff --check` rent i alla tre repon.

### Mekanisk räkningsverifiering

- Skarpt (oförändrat under implementationen): `godkanda(katalog)` = 51,
  `blockerade_tariff_ider(katalog)` = 21 fysiska rader, 86 fysiska
  katalograder totalt (disposition **51/13/28 av 92**, oförändrad —
  ingen av de åtta kandidaternas kategori flyttades). 53 skarpa
  produkter (51 katalog + 2 leverantörsfiler), oförändrat.
- Isolerat (exakt de åtta spärrarna rensade, ALDRIG den skarpa
  katalogen): `godkanda(isolerad)` = 59 — exakt de åtta nya ID:na
  tillkommer, de tidigare 51 oförändrade (disposition **59/5/28 av
  92**). 61 produkter i den isolerade genereringen.

### Commit-hashar

- `skills@c5d499d2b8c25d0ffb0a0f1e637fbc326f0908a7` — katalog:
  `contract_required` + R03-scopesäkring.
- `enkey-agents@d08fd5e6a830cc967831aa1cef7e0d7d7c2d8a9c` — motor/
  policy/test.
- `neptune_academy@36c1ed0f63b2c22851543a0096e1f46eb3f915ed` — TS-
  motor/test/E2E (två commits: implementation + en liten E2E-
  namnmatchningsrättning).

### Slutsats

Batch 5c är implementerad bakom spärr. Ingen tariff är aktiverad och
inget är pushat. Väntar på Codex kodgranskning.
