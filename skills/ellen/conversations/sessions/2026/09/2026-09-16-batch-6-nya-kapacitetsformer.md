---
session_id: "2026-09-16-015"
created_at: "2026-09-16T10:18:12+02:00"
participants:
  - Robert
  - Codex
  - Claude
status: "BLOCKED — katalogschema matchar inte validatorerna"
approved_by: Codex
executed_by: Claude
dispatched_by: agent-bridge
dispatch_via: agent-bridge
scope: "Batch 6 — Borås och Finspång, två nya kapacitetsformer samt Borås miljötillägg"
remote_baseline:
  skills: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
relates_to:
  - "conversations/reviews/2026/09/2026-09-16-beredskapskontroll-batch-6.md"
  - "conversations/handoffs/2026/09/2026-09-16-batch-6-nya-kapacitetsformer.md"
---

# Session: Batch 6 — nya kapacitetsformer

## 2026-09-16 10:18 — Robert begär rollförtydligande och nästa batch

Robert noterade att Claude uppfattat den föregående pushen otydligt och bad
Codex förtydliga instruktionerna samt förbereda nästa batch om projektet var
framme där.

Codex verifierade att Batch 5c faktiskt pushades av Claude efter Codex
godkännande. Remote-HEAD:arna är:

- `skills@8356a716a956fb7101573f572d77897e27cc52ea`
- `enkey-agents@bebbb8073d95fd493168fdbcd57033dc0f02dcb5`
- `neptune_academy@ca0286059de493e9502e229beba4afe864401683`

Claude skapade därefter det lokala skills-pushkvittot `e33e02d`; det låg
inte på remote enligt den äldre protokolltexten. Protokollet är nu rättat
så framtida pushkvitton också pushas och remote-verifieras. Ingen tidigare
push tillskrivs Codex: Codex godkände, Claude verkställde och bryggan
förmedlade.

Agentbryggan har dessutom fått signalen
`APPROVED_FOR_IMPLEMENTATION: Claude`, unik-ID-grind och uttryckliga
rollfält. Buffrad `claude --print`-output dokumenteras så att tyst terminal
inte förväxlas med utebliven leverans.

## 2026-09-16 10:18 — käll- och beredskapskontroll

Batch 6 är nästa planerade batch. Aktuella officiella källor verifierar båda
bastarifferna och Borås miljötillägg:

- Borås leverantörssida bekräftar 2026-grupper, priser, Q-villkor,
  giltighet och nät; katalogens SHA-verifierade Prisdialogen-dokument säger
  uttryckligen 31 kr/MWh för Bra Miljöval 2026.
- Finspångs aktuella 2026-PDF har SHA-256
  `909cbafc1f87be7c00b11f82818f703361f948cf7c2de3d6e04f792410b2ba26`
  och bekräftar säsongsenergi, båda P-formlerna, dagperiodisering och
  villkorad flödesavgift.

Finspångs 20-procentiga spetsvärmetillägg och Borås topplastprodukt är
fortsatt utanför scope. Beredskapskontroll `2026-09-16-015` godkänner lokal
implementation bakom spärr; handoff `2026-09-16-001` ger Claude exakt scope.

Utgångsläge under implementation ska förbli 59/5/28 och 61 skarpa
produkter. Isolerad kandidat ska ge 61 godkända fysiska katalograder, 63
produkter och 62/2/28 i kontrollmängden. Ingen aktivering och ingen push.

## 2026-09-16 — Claude implementerar motorn, hittar katalog/validator-mismatch, stannar

Claude verifierade innan start att `2026-09-16-015` låg ensam överst i
`index.md`, att alla tre repo-HEAD:ar matchade `remote_baseline`/
`required_parent_heads` i handoff `2026-09-16-001`, och att inga orelaterade
filer skulle röras.

**Python-motorn (`enkey-agents/tools/tariffer/`)** — implementerad och
testad: `katalog.py` (`grind()`/`till_prisar()`) fick två nya kapacitetsformer
i en explicit godkännandelista, `heterogeneous_bands` (Borås, sex band med
pinnad Wn/Q-mätbas per band-ID) och `piecewise_polynomial` (Finspång, två
grenar med exakt växling vid `threshold_kw`, ingen interpolation).
`faktura.py` fick motsvarande beräkningsfunktioner. `justeringar.py` fick två
nya justeringstyper, `optional_environmental_addon` (Borås Bra Miljöval,
31 kr/MWh, kundvalt kryssfält, inget separat katalogfält — enligt
`batchplan-v22.md`, som pekades ut som mer auktoritativ än ett annat
antagande i den ursprungliga uppdragstexten) och `conditional_flow`
(Finspång, 20 kr/m³ per kalendermånad där returtemperaturen är STRIKT över
55,0 °C). `policyregister.py` fick bindningskontrollen för de två
tolvmånadersserierna. Ny testfil `test_batch_6_boras_finspang.py` (53 prov)
verifierar båda de publicerade faciten exakt: 80 MWh/Grupp 2 → 77 790 kr
exkl. moms, samt P=36 kW → 48 855 kr inkl. moms. Full svit: 1851 passed / 2
sedan tidigare kända, orelaterade fel (katalog-SHA-pinnar, orsakade av att
katalogfilen redan var ändrad före sessionsstart) / 4 skipped.

**TypeScript-spegeln (`neptune_academy/neptune-marketing/src/utils/fjarrvarme.ts`)**
— speglad 1:1 mot Python-diffen, samma facit, ny testfil
`resultatkontrakt.batch6.test.ts`. Full svit: 1913 passed / 0 failed,
`tsc --noEmit` rent. TS saknar en egen katalogvalideringslada
(`grind()`/`till_prisar()`-motsvarighet) — den byggda/genererade katalogen
litar på att Python redan validerat, vilket bekräftades innan något
uteslöts.

**Isolerad kandidat och räkningsgrindar — BLOCKERAT.** Ny
`generera_isolerad_batch6.py` (mönster efter batch5b/5c) rensar
`investigation` enbart för de två Batch 6-raderna utan att röra den skarpa
katalogfilen. Mekanisk körning genom den redan existerande räknelogiken
(`godkanda()`) visar att detta INTE räcker: den skarpa katalogens verkliga
`capacity`-block för båda raderna använder andra fältnamn än de validatorer
som byggdes i detta pass förväntar sig —

- Borås: katalogen har `band_selection`/`billing_basis_method`/`rate_period`
  på toppnivå och `annual_energy_interval_MWh`/`fixed_SEK`/`basis_unit` per
  band, inte `billing_basis`/`min_mwh`/`max_mwh`/`fixed`/`variable`/`unit`
  som `_valid_heterogeneous_bands` kräver.
- Finspång: katalogen har `pieces`/`coefficients_descending`/
  `max_inclusive`/`min_exclusive`, inte `threshold_kw`/`low{a,b}`/
  `high{c,d}` som `_valid_piecewise_polynomial` kräver.

Ingen normaliserings-/mappningslada finns någonstans i `katalog.py`/
`faktura.py`/`policyregister.py` som skulle kunna överbrygga detta, och
ingen av raderna finns i `POLICYREGISTER`. Följden: `grind()` avvisar
fortsatt båda raderna (av ett SKÄL SOM INTE är investigation-låset), så
`godkanda()` förblir 59/61 produkter/0 nya produkt-ID:n i den isolerade
kandidaten — target var 61/63/2 nya. Siffrorna 62/2/28 gick alltså inte att
nå, och har INTE tvingats fram. En separat, dokumenterande testrad
(`test_disposition_92_kraver_dokumentationsniva_bokforing_inte_bara_kod`)
lades till eftersom även ready/blocked-uppdelningen i
`tariffinventering-v22.md` §8 visade sig vara en handförd
dokumentationssiffra som `grind()` inte ensam kan härleda (den returnerar
bara första träffade avslagsorsak per rad).

Detta är ett genuint schema-/kontraktsval, inte ett kodfel: antingen
formas de två radernas `capacity`-block om i den skarpa katalogen till
validatorernas kontrakt, eller så utökas validatorerna till att också
acceptera den råa extraktionens fältnamn som alias. Ingen av delarna gjordes
här — det kräver ett medvetet beslut, inte en tyst gissning i en isolerad
kandidatgenerator.

**Konsekvens: Batch 6-implementationen stannar här.** React-/E2E-passet
(pass 4 av 4) startades aldrig, eftersom det skulle byggas ovanpå samma
obesvarade fråga. Ingen aktivering, ingen `production_ready`/
`investigation.status`-ändring i den skarpa katalogen, ingen push. Endast
avsedda motor-/testfiler har rörts:

- `enkey-agents`: `tools/tariffer/{katalog,faktura,justeringar,policyregister}.py`,
  `tools/tariffer/tests/{test_justeringar,test_katalog}.py` (uppdaterade
  pinnade antal), `tools/tariffer/generera_isolerad_batch6.py` (ny),
  `tools/tariffer/tests/test_batch_6_boras_finspang.py` (ny),
  `tools/tariffer/tests/test_batch_6_isolerad_kandidat.py` (ny).
- `neptune_academy`: `neptune-marketing/src/utils/fjarrvarme.ts`,
  `neptune-marketing/src/utils/resultatkontrakt.batch6.test.ts` (ny).
- `skills`: endast denna sessionsloggcommit och `index.md` — katalog-JSON:en
  och `tariffinventering-v22.md` (redan ändrade före sessionsstart, av annan
  part) rördes inte ytterligare.

**Öppen fråga till Codex/Robert:** välj mellan (a) omforma
`capacity`-blocken för de två Batch 6-raderna i
`optimate-fjarrvarme-2026.json` till det redan implementerade
validatorkontraktet, eller (b) utöka `_valid_heterogeneous_bands`/
`_valid_piecewise_polynomial` (och TS-motsvarigheten, om en sådan behövs)
till att också acceptera den nuvarande råa fältnamnsformen. Först när det
beslutet är taget kan pass 3 (räkningsgrindar) och pass 4 (React/E2E)
slutföras och en ärlig `REVIEW_READY: Codex` skrivas.

## Ändringslogg

- `2026-09-16T10:18:12+02:00` – Sessionsloggen skapades (beredskapskontroll `2026-09-16-015`).
- `2026-09-16T11:42:15+02:00` – Claude loggade motorimplementation (Python + TS) och den blockerande katalog-/validatormismatchen; status satt till `BLOCKED`.
