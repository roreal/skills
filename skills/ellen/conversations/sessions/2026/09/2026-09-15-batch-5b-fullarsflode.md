---
session_id: "2026-09-15-002"
date: "2026-09-15"
participants: [Robert, Codex, Claude]
status: "Codex granskning 2026-09-15-009: changes required före aktivering. INTE aktiverad, INTE pushad. skills@73f3035, enkey-agents@5f1529f, neptune_academy@3bd4d5d."
topic: "Batch 5b: sex leverantörsvärdestariffer med fullårsflöde (Borlänge, Falu tätort, Falu ytterorter, Habo, Mjölby) plus Jönköpings räknade accessavgift"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
  - "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5b.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5b"
---

# Session: Batch 5b — fullårsflöde och Jönköpings accessavgift

## Uppdrag

Robert gav explicit instruktion: läs handoff `2026-09-15-001` i sin
helhet och genomför Batch 5b exakt enligt uppdraget. Implementera och
committa lokalt bakom befintliga spärrar. Ingen tariffaktivering och
ingen push. Stanna därefter för Codex kodgranskning.

Baseline verifierad mot beredskapskontrollens angivna huvuden: `skills@
cd0bdb2` (plus en Batch 5a-pushlogg-commit ovanpå, ingen konflikt),
`enkey-agents@4d5f8a6`, `neptune_academy@6331f27`.

## Tre rättelser från beredskapskontroll 2026-09-15-008 som överstyr den
## gamla batchplanstexten

1. Samtliga sex katalograder har `capacity.band_selection=
   "supplier_confirmed_band_id_required"` — bekräftat band-ID krävs för
   ALLA SEX, inte bara Borlänge.
2. Varje policy behöver MINST tre kostnadsbärande krav: leverantörens
   effekt, bekräftat band och fakturans årsflöde `flode_m3`.
3. Habos leverantörsvärde är en FAST tvåårig normalårsmodell
   (`takad_till_snapshot`), INTE ett rullande värde — katalogens
   `capacity.billing_basis_method` innehöll tidigare fel formel.

## Källverifiering (utförd på riktigt, 2026-09-15, WebFetch mot aktuella
## officiella sidor)

- **Borlänge**: `borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare`
  — bekräftar priser och rullande 12-månaders effektspråk.
- **Falu tätort/ytterorter**: `fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html`
  — bekräftar priser och "omräknas 1 april varje år" (fast årsrevision).
- **Habo**: `haboenergi.se/varme-miljo-foretag/` — bekräftar den verkliga
  formeln (medel av två senaste kalenderårens normalårskorrigerade energi
  / 2200 eller 1700), inte den tidigare katalogtexten.
- **Mjölby**: `mse.se/foretag/fjarrvarme/priser` — bekräftar priser och
  tvåårsmedel (fast årsrevision).
- **Jönköping, priser**: `jonkopingenergi.se/foretag/fjarrvarme/fjarrvarme/priser`
  — bekräftar priser och accessavgiftens fyra nivåer (0/10/25/50 kr/
  central/månad).
- **Jönköping, effektmetod**: `jonkopingenergi.se/foretag/kundcenter/guider/vad-bestar-fjarrvarmekostnaden-av`
  — bekräftar "medel av de tre högsta av de fem högsta
  dygnsmedeleffekterna senaste tolv månaderna" (rullande).

## Katalogändringar bakom spärr (`skills@73f3035`)

- `contract_required: true` satt på samtliga sex kandidater;
  `investigation.status` kvarstår `"utreds"` — INGEN aktivering.
- Habos och Jönköpings `capacity.billing_basis_method` rättade till
  leverantörernas verkliga metoder (se källverifiering ovan).
- Jönköpings `adjustments` fick en ny sluten justeringspost:
  `{"type": "metered_access_fee", "unit": "SEK", "allowed_prices":
  [0, 10, 25, 50], "months": [1..12]}` — INGEN ny katalograd, ingen
  separat produkt.
- Borlänges och Falu ytterorters `issues`-texter normaliserade till
  grindens redan godkända formulering.
- R04 (Borlänge, 501 kW-gränsen) och R15 (Falu ytterorter, >500 kW)
  flyttade från `remaining_information_requests` till
  `resolved_information_requests`: inte externt besvarade i alla
  detaljer, men inte längre produktblockerande eftersom kontraktet
  kräver leverantörens bekräftade band-ID/värde i stället för att
  extrapolera automatiskt. Falu tätorts felaktiga medlemsvida koppling
  till R15 togs samtidigt bort (R15 gäller bara ytterorterna).
- Ny källproveniens: `haboenergi-web`, `jonkopingenergi-web-priser`,
  `jonkopingenergi-web-effekt`; `retrieved_on=2026-09-15` för
  `borlange-web`/`web-review-falu-final`/`web-review-mjolby-final`.
- `schema_version` `0.1.18` → `0.1.19`, ny `change_log`-post.
- Katalogen har fortsatt 86 fysiska poster; `godkanda(katalog)` förblir
  45.
- `batchplan-v22.md`/`tariffinventering-v22.md` synkade med de tre
  rättelserna ovan (en konsoliderad statusnotis över de sex
  per-tariffstyckena, som annars är oförändrade planeringssnapshots).

**Självrättning under arbetet:** Borlänge och Falu ytterorter
refererade fortfarande R04/R15 i sin `investigation.request_ids` efter
att frågorna flyttats till `resolved_information_requests` —
`test_grinden_slapper_igenom_45_tariffer` fångade detta omedelbart
("okänd informationsförfrågan: R04"). Fixat genom att tömma
`request_ids` för båda raderna, samma mönster som redan gällde Falu
tätort.

## Motor- och kontraktsimplementation (`enkey-agents@5f1529f`)

- **`resultatkontrakt.py`**: `KALLTYPER` fick `"customer_value"` (för
  kundangivna fält, till skillnad från leverantörsvärden). Nytt
  `Tariffpolicy.antal_undercentraler_bindning`-fält, med konstruktionstids-
  validering (`__post_init__`): måste peka på ett `vardetyp="number"`,
  `heltal=True`-krav vars `tillatna_kallor` innehåller `customer_value`.
- **`justeringar.py`**: ny justeringstyp `metered_access_fee` (ingen
  `indatafalt` — båda talen är obligatoriska policybundna fält, samma
  mönster som `flow_difference`). Ny payloadvalidator
  `_valid_metered_access_fee`: sluten nyckelmängd, `unit="SEK"`,
  `allowed_prices` exakt `[0, 10, 25, 50]`, `months` exakt alla tolv.
- **`faktura.py`**: ny motorfunktion `_accessavgift` (pris × 12 × antal,
  med runtime-vakter som är det ANDRA, aldrig det första, skyddet —
  aktiveringspreflighten nedan är det första). Registrerad i
  `_JUSTERING_BERAKNING["metered_access_fee"]`.
- **`policyregister.py`**: delad `_familj4_justeringsfalt_krav`
  återanvänd för `flode_m3` på alla sex (ingen ny byggare behövdes).
  Sex nya `Tariffpolicy`-objekt (`_BORLANGE_POLICY`,
  `_FALUN_TATORT_POLICY`, `_FALUN_YTTERORTER_POLICY` [`maxvarde=500` på
  effektfältet], `_HABO_POLICY` [`takad_till_snapshot=True`],
  `_MJOLBY_POLICY` [`takad_till_snapshot=True`], `_JONKOPING_POLICY`
  [`rullande=True`, plus de två nya accessfälten]). Två nya
  aktiveringspreflighter: `kontrollera_volymbindning` (varje
  `volume`-tariff måste ha exakt ett `flode_m3`-krav, `supplier_value`,
  `minvarde=0` — stänger `_flodesavgift`s äldre MWh/delta-T-reservväg för
  alla kontraktsgated `volume`-tariffer) och
  `kontrollera_accessavgiftsbindning` (accessprisfältets
  `tillatna_varden` måste vara exakt postens egen `allowed_prices`,
  källa `customer_value`; `antal_undercentraler_bindning` måste vara
  satt). Båda registrerade i `kontrollera_aktiveringsgrind`.
- **Ny testfil** `test_leverantorsvarde_batch5b_kontrakt.py` (52 test):
  strukturella prov (≥3 bundna fält, produktunika nycklar), räkningsgrind
  (45/47 oförändrat, isolerad aktiveringskopia ger 51/53), golden-facit
  för alla sex (oberoende handräknade från katalogens publicerade priser
  via `till_prisar`, INTE genererade av funktionen under test), saknat
  `flode_m3` ⇒ ofullständigt resultat, Falu ytterorters 500 kW-gräns
  (501 blockerar, 500 går igenom), Jönköpings fyra accessvärden
  (0/10/25/50, inkl. VAT-korrekt summa) samt att ett okänt/saknat
  accessvärde blockerar.
- Full Python-svit: **1527 passed, 4 skipped**.

## TypeScript-spegling (`neptune_academy@3bd4d5d`)

- **`resultatkontrakt.ts`**: `KALLTYPER` fick `'customer_value'`.
  `Tariffpolicy`/`TariffpolicyOptions` fick `antalUndercentralerBindning`,
  med samma konstruktionstidsvalidering som Python
  (`skapaTariffpolicy`). `policyFranGenererad` mappar
  `json.antal_undercentraler_bindning`.
- **`fjarrvarme.ts`**: ny `accessavgift`-funktion, registrerad i
  `JUSTERING_BERAKNING["metered_access_fee"]` (härleder automatiskt
  `JUSTERINGSTYPER_KANDA`).
- **Regenererade fixturer** (aldrig handredigerade): `tariffer.generated.ts`
  (via enkey-agents egen `python -m tools.tariffer.generera`, med
  `skills@73f3035` som proveniens-commit — 47 produkter, ingen Batch
  5b-läcka), `batch3bGenerated.json` (om via samma isolerade-kopia-mönster
  som testet självt använder), `batch1RawData.ts`/`batch5aRawData.ts`
  (det nya `antal_undercentraler_bindning: null`-fältet syns nu på ALLA
  redan serialiserade policyer, inte bara Batch 5b:s — mekaniskt en följd
  av att `dataclasses.asdict`/`_policy_till_json` är fullt generiska).
- Full TypeScript-svit: **1497 passed**. `tsc --noEmit`: rent.
  Produktionsbygge (`npm run eval:build`, isolerad `dist-eval`,
  efterstädad): OK. Browser-E2E (`npm run test:e2e`, 19 scenarier,
  Batch 1–5a): samtliga godkända.

**Känd begränsning, redovisad explicit:** `KalkylatorPage.tsx` (UI-
rendering av accessvalet, substations-injektion, fältfiltrering) är
INTE uppdaterad i denna omgång, och inget nytt E2E-scenario för Jönköping
finns — eftersom Batch 5b inte är aktiverad syns ingen av de sex
raderna i den riktiga genererade payloaden/dropdownen än, så ett äkta
scenario mot produktionsflödet kan inte byggas förrän en separat, godkänd
aktiveringsrunda. De 19 befintliga E2E-scenarierna (Batch 1–5a) är
oförändrat gröna. Detta är en medveten, redovisad scope-begränsning för
Codex att bedöma — inte ett dolt hål.

## Mekanisk räknings- och leveransverifiering

- `godkanda(katalog, policyregister=POLICYREGISTER)`: **45**, ingen av de
  sex Batch 5b-ID:na läcker in.
- Real skarp genererad payload (`bygg_ts_fran_katalog`): **47** produkter,
  ingen Batch 5b-produkt.
- Isolerad kopia med exakt de sex spärrarna rensade: **51** godkända
  katalogprodukter, **53** skarpa produkter (inkl. de två
  leverantörsfilsprodukterna) — disposition **52/12/28 av 92** (Jönköpings
  accessavgift räknas inte som en egen produkt, ingen
  räkningsmotsägelse).
- `git diff --check`: rent i samtliga tre repon.

## Hårda spärrar respekterade

Ingen aktivering (samtliga sex kvarstår `investigation.status="utreds"`).
Ingen push i något repo. `tariffer.generated.ts` aldrig handredigerad —
regenererad via den riktiga Pythongeneratorn. Inga orelaterade
arbetskopiefiler eller `neptune-marketing/dist`-ändringar rörda eller
committade. Handoffens frontmatter-`status` orörd (Codex jobb).

**Slutsats:** DONE_WITH_CONCERNS — kärnimplementationen (katalog, Python-
kontrakt/motor, TypeScript-spegling, tester, räkningsgrind) är fullständig
och verifierad, men `KalkylatorPage.tsx`-UI:t och ett äkta Jönköping-E2E-
scenario är uppskjutna till aktiveringsrundan (se begränsning ovan).
Stannar här för Codex kodgranskning.

## Codex granskning 2026-09-15T12:15:06+02:00

Granskning `2026-09-15-009`: **changes required före aktivering; ingen
push.** Motorformeln, spärrarna och räkningsgrindarna är i huvudsak rätt,
men begränsningen ovan kan inte skjutas till aktiveringsrundan. Den verkliga
produktadaptern märker båda nya `customer_value`-fälten som
`supplier_value`, transporterar inte globala `substations` och filtrerar
inte bort antalsbindningen från det generiska UI:t. Jönköping skulle därför
blockera och samtidigt visa ett dubblerat antal-fält.

Accessavgiftens deskriptor refererar inte explicit sina två fält och den
statiska preflighten korsvaliderar inte annual/1–20/exakt kundkälla för
antalet; Codex reproducerade att ett monthly/0–999/blandkällkontrakt
accepterades. Handoffens speglade TypeScript-/React-/E2E-/band-/felmatris
saknas också. Katalogens requesträkning och de levande inventeringsavsnitten
är osynkade.

Full verifiering: 1527 passed/4 skipped Python, 1497 TypeScript, ren tsc,
grönt isolerat bygge och 19/19 befintliga E2E; generatorn ger 45/47 och
isolerat 51/53 utan läckage. Grönt befintligt testläge stänger inte de
otestade/ej implementerade produktvägarna. Full rättningsorder finns i
`conversations/reviews/2026/09/2026-09-15-granskning-batch-5b-implementation.md`.
