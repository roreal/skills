---
session_id: "2026-10-05-003"
started_at: "2026-10-05T12:27:09+02:00"
last_updated: "2026-10-05T17:21:52+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: "APPROVED_FOR_ACTIVATION: Claude"
topics:
  - Optimate
  - besparingspotential
  - våg 3b
  - årsvis volymled
source: visible-conversation
transcript_fidelity: summarized
approved_by:
  - Robert
  - Codex
executed_by: Claude
dispatched_by: agent-bridge
---

# Optimate våg 3b — årsvis volymled

## Synlig dialog och beslut

Robert bad Codex välja lämpliga produkter och ett lämpligt antal för nästa
besparingsvåg. Codex analyserade de 42 återstående matrisraderna efter
kostnadsväg, effektmodell, justeringstyp, månadsserie och historik och valde
sex sammanhållna årsvolymprodukter: Borlänge, Falu ytterorter, Falun, Habo,
Mjölby och VänerEnergi. Robert svarade: **”Jag godkänner”.**

Urvalet ger en hanterbar ny beroendeklass utan att blanda in
månadsflödesserier, temperatursteg, legacy-backend, Vattenfalls behörighet
eller dokumenterade exkluderingar. Vid en senare godkänd publik aktivering
skulle täckningen öka från 34 till 40 av 77 produkter, men denna signal
gäller bara intern implementation och granskning.

Det bindande tekniska uppdraget finns i
[`2026-10-05-optimate-vag-3b-arsvolym.md`](../../../handoffs/2026/10/2026-10-05-optimate-vag-3b-arsvolym.md).

## Implementation (denna session)

**Neptune** (isolerad gren `optimate-vag-3b-arsvolym` ovanpå oförändrad
`main`/`origin/main` `4d6e3398b85079891585304085df022c5adf8536`, ny commit
`0a0a19bd62fbbbf2ed3b65c576a64ee5044360ed`):

- `optimateScenario.ts`: ny, exporterad `WAVE_3B_PRODUCT_IDS` (6 ID:n,
  alfabetisk ordning, fryst), samtliga tillagda i `SCENARIO_PILOT_TARIFFER`
  med explicit `'kontraktsgatad_kostnadsled'`. `SCENARIO_PUBLIKT_AKTIVERADE_ID`
  **oförändrad** — fortfarande exakt de 34 produkterna från våg 1+2+3a; våg
  3b ger `stodjerOptimateScenario===true` men
  `stodjerOptimateScenarioPubliktAktiverad===false` för alla 6.
- Ny `optimateScenarioVag3b.test.ts`: tabellstyrt, oberoende `FACIT_3B`
  (fast = avgift_kr_ar + effektKw×pris_kr_per_enhet_ar, energi = Σmanadspris
  ×100/12, justering = flode_m3×rate — handräknat ur
  `tariffer.generated.ts`, aldrig anrop till produktionsmotorn), 10/15/20-
  scenarier, fail-closed-prov (flode_m3/band/kapacitet) och
  besparingsvägs-spärr. 105/105 gröna.
- `optimateScenarioVag2.test.ts`/`optimateScenarioVag3a.test.ts`: uppdaterad
  pilotsnapshot-längd 34→40 (ingen ändring av deras egna, oförändrade
  påståenden om `SCENARIO_PUBLIKT_AKTIVERADE_ID`=34); Vag2-testets våg-2-
  filter utökat att även exkludera `WAVE_3B_PRODUCT_IDS`.
- Verifiering: 105/105 riktade Vag3b-prov, 507/507 Vag2+Vag3a+bas-prov, ren
  `tsc --noEmit`, två fulla Vitest (89/89 filer, 3099/3099 prov, båda rena —
  ingen "unhandled error"), grönt `npm run build`, ren `git diff --check`,
  `dist/` återställt till committerat tillstånd före commit.

**Skills** (main, ny commit `208a346fe2b3296d3974c3a98d9bfc0a79e0001a`
ovanpå oförändrad `e8b5470d0de272c6af1246bafc5be271db3ac574`):

- `generera_besparingspotential_tackningsmatris.py`: ny
  `WAVE_3B_PRODUCT_IDS`-frozenset (6 ID:n) och en ny `build_matrix`-bindning
  som kräver `'volume' in adjustment_types`, `cost_path==kontrakt_arskostnad`
  och `capacity_rule==effekt` per ID — **inte** ett generiskt filter på
  justeringstyp (till skillnad från våg 3a:s bindning), eftersom `'volume'`
  inte är unikt för dessa 6 rader i hela katalogen. `SCENARIO_STATUS_REGISTRY`
  utökad med samma 6 ID:n → `godkand_intern_pilot_ej_publik`.
- `test_generera_besparingspotential_tackningsmatris.py`: uppdaterade
  räknare (not_reviewed 42→36, ny `godkand_intern_pilot_ej_publik: 6`), ny
  `test_wave_3b_membership_and_status_is_mechanically_locked`,
  `test_wave_3a_scenario_status_is_mechanically_locked_to_wave_3a_membership`
  rättad till att förvänta `WAVE_3B_PRODUCT_IDS` (inte en tom mängd) för
  `godkand_intern_pilot_ej_publik`-raderna.
- Matris-JSON/Markdown regenererade **enbart** via generatorns `--write`;
  `--check` bekräftar artefakterna aktuella. Ny fördelning: **34 publika /
  6 interna / 1 prototyp / 36 ej granskade = 77.**
- Verifiering: 22/22 pytest-regressionsprov, `--check` grönt.

Ingen ändring av tariffdata, kostnadsmotor, `stodjer_besparing`,
`stodjer_aktuell_arskostnad`, Enkey eller `conversations/automation/`.
Ingen publik aktivering, mainflytt eller push.

`REVIEW_READY: Codex`

## Codex slutgranskning — godkänd för lokal aktivering

Codex granskade Neptune-diffen `4d6e339..0a0a19b` och skills-diffen
`e8b5470..208a346`. Produktdiffen omfattar exakt fyra filer och ändrar bara
pilotlistan, dess uttryckliga Wave-3b-lista och tester. Skills-diffen
omfattar exakt generatorn, dess test och de två genererade
matrisartefakterna. Ingen tariffdata, kostnadsmotor, publik lista eller
Enkey-kod ingår.

De sex ID:na, priserna, banden, bindningsnycklarna, momsgrunden och
helårsflödesleden kontrollerades direkt mot den checkade katalogen. Samtliga
har exakt en `volume`-justering med månaderna 1–12; de oberoende
energisummorna 5 569, 4 960, 4 584, 6 436, 4 499 respektive 5 927 och
flödespriserna 3,94, 3,50, 3,50, 4,30, 5,10 respektive 1,74 matchar
facitfixturerna. Testerna visar att flödesled och kapacitet förblir låsta
medan endast styrbar rumsvärme reduceras.

Codex körde själv:

- fyra riktade scenariofiler: **612/612** prov gröna;
- hela Vitest: **89/89 filer, 3 099/3 099 prov** gröna;
- `npx tsc --noEmit`: rent;
- matrisprov: **22/22** gröna;
- generatorns `--check`: 77 produkter och aktuell källhash.

Live `origin/main` var fortsatt Neptune
`4d6e3398b85079891585304085df022c5adf8536` och skills
`abf4dba3159143f813827907d898f24217d0e0ba`. Inga granskningsfynd återstår.
Den interna implementationen är godkänd för nästa, separata lokala
aktiveringssteg enligt
[`2026-10-05-slutgranskning-optimate-vag-3b-signal-002.md`](../../../reviews/2026/10/2026-10-05-slutgranskning-optimate-vag-3b-signal-002.md).

`APPROVED_FOR_ACTIVATION: Claude`
