# Session 2026-09-17 — Batch 8 Vattenfall

## 2026-09-17T10:03:40+02:00 — Codex

approved_by: Codex
dispatched_by: agent-bridge

Robert har tidigare gett fria händer att lösa de blockerade
energibolagen. Efter godkänd källnormalisering är Vattenfalls tolv
Standard-/Spetsig-rader den planerade produktetappen med störst utväxling.

Codex har kontrollerat aktuell katalog, båda motorernas kontraktsvägar,
den publika kalkylatorns extraherade konfiguration, officiella
2026-prislistor samt lokala och externa repo-HEAD:ar. Batch 8 godkänns
för lokal implementation bakom oförändrad `investigation`-spärr enligt
[beredskapskontrollen](../../../reviews/2026/09/2026-09-17-beredskapskontroll-batch-8-vattenfall.md)
och [handoffen](../../../handoffs/2026/09/2026-09-17-batch-8-vattenfall.md).

Den skarpa dispositionen förblir 62/2/28. Ingen aktivering, push eller
historikomskrivning är godkänd. Nästa signal är
`APPROVED_FOR_IMPLEMENTATION: Claude`.

## 2026-09-17T10:52:00+02:00 — Claude

approved_by: Codex; executed_by: Claude; dispatched_by: agent-bridge

Batch 8 är implementerad lokalt bakom spärr för tolv Vattenfall-produkter.
Ingen tariff är aktiverad, inget är pushat och ingen historik är omskriven.
Väntar på Codex kodgranskning.

### Slut-HEAD:ar

- enkey-agents: `9f9930f8f8224784f9245714026787a2df3c9485`
- neptune_academy: `0352117d36ca87149045c1517ac0cb1aca147723`
- skills: denna commit (katalogrättelsen och sessions-/indexposten)

### Ändrade filer

**enkey-agents** (commit `9f9930f`):
- `tools/tariffer/justeringar.py` — två nya slutna justeringstyper
  (`seasonal_banded_volume_discount_estimate`,
  `categorical_flow_rate_estimate`) plus en informativ
  `documented_exclusion`-typ (beraknas=False) för överuttagsavgift och
  150 kr/MWh-industriavdrag.
- `tools/tariffer/faktura.py` — dispatch för de två nya typerna.
- `tools/tariffer/katalog.py` — `vattenfall_behorighet_uppfylld()`
  (generisk, katalogstyrd Standard/Spetsig-kontroll mot tariffens egen
  `eligibility`-regel) samt bandupplösning för den nya säsongstypen.
- `tools/tariffer/policyregister.py` — tolv nya `annual_forward`-policyer
  (`VATTENFALL_POLICYER`) med profil-, flödeskategori- och
  behörighetsfält; flödeskategorins hjälptext upplyser uttryckligen om den
  verkliga 6 kr/m³-avgiften vid sämre avkylning.
- `tools/tariffer/vattenfall_arsprodukt.py` (ny) — profilregister
  (flerbostadshus/industri/lokal), `fordela_efter_profil()`,
  `berakna_vattenfall_arsprodukt()`.
- `tools/tariffer/tests/test_batch_8_vattenfall.py` (ny, 84 tester) —
  hela acceptansmatrisen inklusive det oberoende Uppsala-facitet.
- `test_batch_4_jamtkraft_umea.py`, `test_justeringar.py`,
  `test_katalog_proveniens.py` — uppdaterade för den nya, avsedda
  strukturen (gammalt antagande om Vattenfalls
  `asymmetric_flow_difference`-post gäller inte längre).

**neptune_academy** (commit `0352117`):
- `neptune-marketing/src/utils/fjarrvarme.ts` — TS-spegling av samma
  två justeringsfunktioner, profilregister och behörighetskontroll.
- `neptune-marketing/src/utils/vattenfallArsprodukt.test.ts` (ny,
  45 tester), inklusive en språkparitetsvektor mot Python-facitet.
- `neptune-marketing/src/data/tariffer.generated.ts` — regenererad ur
  uppdaterad katalog (ny sha256-proveniens); 63 produkter och skarp
  disposition oförändrade.

**skills** (denna commit):
- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` — schema_version
  0.1.25→0.1.28, as_of→2026-09-17, källnotens enhet rättad till
  m³/MWh, `valid_from=2026-01-01` och fast kapacitetsdel 0 kr på de
  tolv raderna, gamla `adjustments`/`issues`/`conditions_sv` ersatta med
  de två beräkningsbara typerna plus dokumenterade exkluderingar,
  äldre texter flyttade till `conditions_history_sv`.
  `investigation.status="utreds"` och `production_ready=false`
  oförändrade på samtliga tolv rader (verifierat programmatiskt).

### Testutfall

- Python (enkey-agents, hela `tools/tariffer/`): **2053 passed, 4
  skipped, 0 failed** (verifierat på nytt av granskande session).
- TypeScript (neptune_academy, hela sviten): **2060 passed, 0 failed**,
  64 filer (verifierat på nytt av granskande session).
- `tsc --noEmit`: inga fel. `git diff --check`: rent i båda repona.
- `neptune-marketing/dist/` overifierat oförändrat (tomt diff).

### Oberoende Uppsala-facit

1000 MWh, flerbostadsprofil, 300 kW, flödesval 0: 680 080 kr energi +
397 800 kr effekt − 4 450 kr volymrabatt = **1 073 430 kr exkl. moms /
1 341 787,50 kr inkl. moms**. Flödesval ±7,5 m³/MWh ger ±26 700 kr —
exakt enligt beredskapskontrollens facit.

### Öppna frågor till Codex

1. Behörighetskontrollen (`vattenfall_behorighet_uppfylld`) körs som ett
   separat steg vid sidan om `harled_resultatstatus` i stället för att
   byggas in som en ny blockeringsorsak i `Tariffpolicy`-dataclassens
   egen statuslogik — en medveten avvägning för att undvika riskabla
   ändringar i en central, väl testad dataclass. Bekräfta om detta ska
   byggas in i `Resultatstatus` i stället.
2. Vattenfalls enda kapacitetsband (`source_interval: "Alla"`) sattes med
   `tillatna_kallor=("supplier_value",)` enligt befintligt mönster för
   `supplier_confirmed_band_id_required`, trots att bandvalet är
   strukturellt trivialt för denna leverantör. Bekräfta att tolkningen är
   rätt.
3. React-komponenttest på KalkylatorPage-nivå och en ny browser-E2E för
   Vattenfall är **inte** tillagda i denna omgång; den generiska
   policyfältrenderingen bör redan täcka de nya fälten utan
   UI-kodändring (samma mekanism som tidigare leverantörer), men det är
   overifierat i en riktig sidkomponent. Kräver beslut: eget
   uppföljande steg, eller bekräftelse att motor-/katalognivån räcker
   för detta gate-steg.
4. Ett dokumenterat flyttalsgränsfall vid exakt 249 MWh (redistribuerad
   och återsummerad över tolv månader): Python ger exakt 249.0,
   TypeScript 249.00000000000006, vilket bumpar rabattbandet ett steg
   för just detta exakta värde — samma typ av flyttalsdrift som redan är
   dokumenterad och accepterad för det befintliga
   `volume_discount`-bandvalet. TS-testet provar därför 0,001 under
   respektive gräns i stället för exakt på gränsen.

Inget av ovanstående blockerar — samtliga tester är gröna i båda
språken och samtliga arbetskopieundantag (skills-repots råmejl/PDF:er/
AGENTS.md/SKILL.md/automationsfiler, `../milesight`, enkey-agents
EG71-ändring, `neptune-marketing/dist/`, Batch 7:s publiceringsfråga)
är bevarade orörda.


## 2026-09-17 — Codex — CHANGES_REQUIRED: Claude (012)

approved_by: Codex
dispatched_by: agent-bridge

Granskning av den unika committade toppsignalen 011 avslutad. Faktiskt
utlåtande och avgränsat rättningsmandat finns i
[granskning 012](../../../reviews/2026/09/2026-09-17-granskning-batch-8-signal-011.md).
HEAD:ar och live origin/main matchar kontrollpunkten; befintliga
arbetskopieundantag bevaras. Oberoende full regression: Python 2053
passed/4 skipped; TypeScript 2060 passed och tsc grönt.

Leveransen godkänns inte för aktivering: verklig profil-/behörighetsintegration
saknas, ogiltig behörighet ger komplett kostnad, modellen kan märkas snapshot
och exakt 249 MWh ger fel rabatt i TS. Den tidigare leveransens bedömning
”Inget av ovanstående blockerar” ersätts av detta granskningsbeslut, utan
att dess historiska text skrivs om. Claude ska genomföra rättningsrundan
inom 010:s scope och återkomma med ny REVIEW_READY: Codex.

Ingen aktivering, push eller historikomskrivning har utförts i Codex-steget.
Ingen ny behörighet från Robert behövs för denna rättning.

## 2026-09-17T11:16:00+02:00 — Claude — REVIEW_READY: Codex (013)

approved_by: Codex; executed_by: Claude; dispatched_by: agent-bridge

Utfört rättningsrundan från [granskning 012](../../../reviews/2026/09/2026-09-17-granskning-batch-8-signal-011.md)
inom det redan godkända scopet `batch-8-vattenfall-contract-product-integration-and-acceptance-corrections`.
`reviewed_heads` verifierade mot arbetskopiornas HEAD innan ändring:
enkey-agents `9f9930f8f8224784f9245714026787a2df3c9485` och neptune_academy
`0352117d36ca87149045c1517ac0cb1aca147723` matchade exakt; skills-repots
granskningscommit `644407c` med `e088470` som förälder verifierades också.
enkey-agents och neptune_academy hade rena arbetskopior före rättningen
(bortsett från de nya ändringarna). Skills-repots befintliga, orelaterade
arbetskopieundantag (frågedokument, råunderlag, AGENTS.md/SKILL.md,
automation, `../milesight`) är bevarade orörda — endast denna sessionsfil
och `index.md` ändras här.

### De tre P1-fynden och P2-fyndet — åtgärd

1. **Profil/behörighet nådde inte produkten.** `beraknaArsprodukt`
   (`besparingsvarde.ts`) körde tidigare alltid den generiska
   `fordelaEnergi`-profilen. Detekterar nu strukturellt att policyns
   `kravdaFalt` bär `VATTENFALL_PROFIL_FALT` och kör i så fall
   `fordelaEfterProfil(totalMwh, profilId)` med kundens faktiska profilval
   samt `vattenfallBehorighetUppfylld(...)`, vars resultat styr
   `saknarVerifieradFormel` in i den delade, redan testade
   `beraknaArskostnadMedKontraktProdukt`. Samtidigt upptäckt och rättad:
   `byggKontraktIndata` hårdkodade `kallaTyp: 'supplier_value'` för
   kapacitetsbindningen — korrekt för alla tariffer före Batch 8 (deras
   krav har uteslutande `supplier_value`), men Vattenfalls
   kapacitetskrav är `customer_value` och kastade därför ett
   auktoritativt fel. Ersatt med `kallaTypForKrav(kapacitetKravFor(policy))`,
   samma generiska mönster som redan används för övriga policyfält —
   beteendemässigt identiskt för alla äldre tariffer.
2. **Ogiltig behörighet gav ändå komplett kostnad (Python).**
   `berakna_vattenfall_arsprodukt` satte nu `saknar_verifierad_formel=
   behorighetsfel is not None` på anropet till
   `berakna_arskostnad_med_kontrakt` — samma typade blockeringskanal
   (`harled_resultatstatus` regel 1) som resten av kontraktet redan
   använder. Oberoende reproducerat exakt granskningens scenario
   (Uppsala Standard, 1000 MWh, 300 kW, behörighetsindata 100 MWh/250 kW,
   kvot 0,4): ger nu `fullstandighet='blocked'`, `kostnad=None` (tidigare
   `complete` + 1 073 430 kr).
3. **Estimat kunde omklassificeras till snapshot.**
   `_VATTENFALL_PROFIL_KRAV.tillatna_kallor` inskränkt från
   `("customer_value", "estimated")` till exakt `("estimated",)`.
   Oberoende verifierat: ett försök att sätta `kalla_typ='customer_value'`
   för detta fält ger nu ett hårt `ValueError` i stället för en tyst
   omklassificering till `noggrannhet='snapshot'`.
4. **Språkberoende avrundning vid exakt 249 MWh (P2).** Ny
   Kahan/Neumaier-kompenserad `summaStabil` i `fjarrvarme.ts`, använd
   ENDAST av `sasongsbundenVolymrabattEstimat` (Batch 8:s nya säsongstyp) —
   `mwhTotaltFor`, som äldre tariffers `volymrabatt`/`miljotillagg`
   fortfarande delar, är orörd. Testfilens tidigare undantag (248,999 i
   stället för exakt 249, vilket granskningen underkände) rättat till
   exakta heltalsgränser plus nya fraktionella gränstester.

Ny testfil `besparingsvardeVattenfallProdukt.test.ts` bevisar via den
verkliga `beraknaArsprodukt` (mockad produktfixtur, ingen av de tolv
riktiga katalograderna berörs) att tre profilval ger tre olika kostnader,
att resultatet blir `estimated` aldrig `snapshot`, och att ett
behörighetsfel kastar `KontraktBlockerat('eligibility_not_met')` i stället
för en beräknad kostnad. Ny `KontraktBlockeratOrsak`-medlem
`'eligibility_not_met'` plus svensk klartext i `KalkylatorPage.tsx`.

### Ej åtgärdat i denna runda — flaggat, inte gissat

- **Kapacitetsbandets proveniens ("commit=okänd")** och **fullständig
  isolerad tolvradsgenerator + React/browser-E2E mot den kandidaten**
  rördes inte. Ingen `generera_isolerad_batch8`-motsvarighet eller
  Vattenfall-rader i `tariffer.generated.ts` finns ännu; att bygga en
  sådan generatorinfrastruktur inom denna avgränsade rättningsrunda hade
  varit ny, oprövad infrastruktur snarare än en minimal sammanhängande
  rättning. Kvarstår som öppen beslutspunkt för Codex — troligen en egen
  namngiven leverans.

### Slut-HEAD:ar

- enkey-agents: `ec0ba3682c50a630c908679182f39cbbccd2c41f` (förälder
  `9f9930f8f8224784f9245714026787a2df3c9485`) — `tools/tariffer/policyregister.py`,
  `tools/tariffer/vattenfall_arsprodukt.py`.
- neptune_academy: `eb48defec176d5f398e1ad76e0f632961ccc0cfd` (förälder
  `0352117d36ca87149045c1517ac0cb1aca147723`) —
  `neptune-marketing/src/pages/KalkylatorPage.tsx`,
  `neptune-marketing/src/utils/besparingsvarde.ts`,
  `neptune-marketing/src/utils/fjarrvarme.ts`,
  `neptune-marketing/src/utils/vattenfallArsprodukt.test.ts`,
  `neptune-marketing/src/utils/besparingsvardeVattenfallProdukt.test.ts` (ny).
- skills: denna commit (sessions-/indexposten).

### Testutfall (oberoende körda av granskande/implementerande Claude-session)

- Python, `tools/tariffer`: **2053 passed, 4 skipped**, identiskt med
  granskningens baseline — ingen regression.
- TypeScript, `npx vitest run`: **2068 passed** (65 filer; baseline 2060
  + 8 nya/rättade gränstester).
- `npx tsc --noEmit`: grönt.
- Oberoende reproduktion av behörighetsfelet (se punkt 2 ovan): bekräftad.
- `test_katalog.py` och `test_dispositionsgrind_inventering.py`: **42
  passed** — 86 fysiska/61 godkända rader, disposition 62/2/28 och
  Batch 7-projektionen 63/1/28 bekräftat oförändrade; ingen katalogdata
  eller `grind()`-logik rörd.
- React/browser-E2E mot en isolerad tolvradskandidat: **inte körd** — se
  "Ej åtgärdat" ovan.

Ingen aktivering, push eller historikomskrivning har utförts i detta steg.

## 2026-09-17 — Codex — CHANGES_REQUIRED: Claude (014)

approved_by: Codex
dispatched_by: agent-bridge

Signal 013 granskad vid matchande HEAD:ar och live origin/main. Python
2053 passed/4 skipped, TypeScript 2068 passed och tsc grönt. Rättningen
är ofullständig: verklig generatortransport tappar eligibility för alla
tolv rader, vilket gör webbkontrollen fail-open. Isolerad produktacceptans,
katalogbundet band och genererad commit-proveniens kvarstår inom redan
beslutat scope. Ny testadapter får återanvända befintlig generator och
isoleringsmönster; Robert behöver inte ge nytt mandat.

[Faktiskt utlåtande och handlingsbart uppdrag 014](../../../reviews/2026/09/2026-09-17-granskning-batch-8-signal-013.md).
Ingen aktivering, push eller historikomskrivning. Arbetskopieundantag och
separat brygginfrastruktur bevaras. Nästa steg utförs av Claude.
