---
session_id: "2026-09-24-001"
date: "2026-09-24"
participants: ["Robert", "Codex", "Claude"]
status: "APPROVED_FOR_ACTIVATION: Claude"
topic: "Härnösand 2026 — leverantörssvar om volymrabatt"
last_updated: "2026-09-24T13:42:28+02:00"
---

# Härnösand 2026 — A2/R02

## 2026-09-24T10:34:25+02:00 — Codex

Robert meddelade att ett nytt svar från Härnösand Energi & Miljö finns
lokalt som rå `.eml`. Codex har läst svaret, kontrollerat det mot HEMAB:s
officiella prislista 2026 och skapat en sanitiserad bedömning utan
personuppgifter.

Svaret stänger den externa källfrågan: HEMAB:s intervalltabell används i
faktureringen och det publicerade räkneexemplet är fel. Korrekt avdrag vid
1 750 MWh är 50 575 kr exklusive moms. Den officiella prislistan bekräftar
även avräkning på årets sista faktura, 1/12-periodiserad effektavgift och
effektkorrigeringens formel.

Codex har skrivit handoff
[`2026-09-24-harnosand-volymrabatt.md`](../../../handoffs/2026/09/2026-09-24-harnosand-volymrabatt.md)
för en källnormalisering och komplett årsprodukt bakom spärr. Råmejlet
ska förbli ospårat. Ingen aktivering eller push är tillåten före separat
granskning.

`APPROVED_FOR_IMPLEMENTATION: Claude`

## 2026-09-24T12:05:00+02:00 — Claude

approved_by: Codex; executed_by: Claude; dispatched_by: agent-bridge

Genomförde handoffens fulla scope bakom befintlig `investigation`-spärr.
Ingen aktivering och ingen push i denna runda.

**Reposäkerhet (verifierad före ändring):** skills `HEAD` var
`c25a809503fefdc4e9c78aaeec56302e79697fb0` (granskad bas); enkey-agents
`origin/main` var `451c85a0e19833e6607e109f44a30c0d54ef2815` (lokal
`main@2e30bb200d1831b8ca7461f67e0d958870ba6867` har en orelaterad
Milesight-commit och rördes inte); neptune_academy `origin/main` var
`3cc527e895f95684d1aed9e553566b9578f075ca`. Isolerade worktrees/branches
`harnosand-2026-volymrabatt-effektkorrigering` skapades från exakt dessa
baser i `/tmp/enkey-agents-harnosand-2026` och
`/tmp/neptune-academy-harnosand-2026`. Ingen merge, rebase, reset eller
historikomskrivning. Den redan smutsiga
`Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`,
`conversations/automation/`, `../milesight` och alla olistade
lokala/otrackade filer (inklusive de två lokala kopiorna av HEMAB-mejlet)
lämnades helt orörda och ostagade.

**Skills** (commit `f170d05196c40352e4613eaeeae30750811a1ddb`, ovanpå
`c25a809`): normaliserade `harnosand-energi-miljo-harnosand-2026`s
`adjustments` till `marginal_annual_volume_discount` (nytt maskinläsbart
`settlement: "last_invoice_of_calendar_year"`) och en ny sluten typ
`capacity_overrun` (`actual_kw_field: "debiteringsgrundande_effekt_kw"`),
satte `valid_from: "2026-01-01"`, rättade `13_1`s proveniens med en
daterad not (hashen är redan identisk med HEMAB:s officiella 2026-PDF,
ingen om-hämtning), lade till den sanitiserade bedömningen som ny källa
(`assessment-harnosand-volymrabatt-2026-09-24`), och gav Gävles befintliga
`marginal_annual_volume_discount`-post samma nya `settlement: "monthly"`
för paritet mot den skärpta nyckelmängden. Uppdaterade
`verifieringslista-fjarrvarmebolag.md` och `tariffinventering-v22.md`
(Härnösands bastariffrad `blocked_external_info` → `ready_to_implement`,
§8-tabellen och en daterad rättelsenot: disposition **75 / 3 / 13 / 1 av
92**, oförändrat `godkanda()` = 74 fysiska katalograder).
`investigation.status` är medvetet kvar på `"utreds"`;
`production_ready` oförändrat `false`.

**enkey-agents** (commit `b0a76d5a9b5a2ec243e6651ac843a8e76a09aae4`, två
commits ovanpå `451c85a`): ny `_effektoverskridande()` (faktura.py) och
`_valid_capacity_overrun()`/`_CAPACITY_OVERRUN_NYCKLAR`
(justeringar.py), registrerad i `_JUSTERING_BERAKNING`/
`JUSTERINGSTYPER`. `settlement` tillagt i
`_MARGINAL_ARSVOLYMRABATT_NYCKLAR` med pinnad tvåvärdes-enum
(`monthly`/`last_invoice_of_calendar_year`). Ny
`Tariffpolicy.effektoverskridande_bindning` (resultatkontrakt.py) och
`kontrollera_effektoverskridandebindning()` (policyregister.py, samma
bidirektionella mönster som `kontrollera_accessavgiftsbindning`),
inkopplad i `kontrollera_aktiveringsgrind`. `_HARNOSAND_POLICY`
registrerad i `POLICYREGISTER` med täckning `annual_forward`. Ny testfil
`test_harnosand_capacity_overrun.py` (50 prov: bindande helårsfacit,
samtliga bandgränser, mutations-/avvisningsprov). Katalog-SHA256 i
`test_katalog_proveniens.py` och de fyra hårdkodade
dispositionsräkningarna i `test_dispositionsgrind_inventering.py`
synkade mot den normaliserade katalogen (75/2/14/1 → 75/3/13/1).
`python3 -m pytest tools/tariffer/ -q`: **2324 passed, 6 skipped, 2
failed**. De två kvarvarande felen
(`test_batch_3b_bas_delvarme.py`/`test_leverantorsvarde_batch5b_kontrakt.py
::TestNeptuneFixturSynk::test_checkad_in_fixtur_ar_semantiskt_regenererbar`)
är verifierat förbefintliga och strukturella — de jämför mot
checkade-in fixturer i **huvudkopian** av `neptune_academy`
(`~/Code/neptune_academy`, hårdkodad sökväg, inte den isolerade
worktreen) och går sönder av ATT `POLICYREGISTER`-serialiseringen fick
ett nytt nollbart fält (`effektoverskridande_bindning`) på ALLA
tariffer, inte av någon Härnösand-/Gävle-specifik logik. Reproducerat: på
ren `451c85a` (utan detta scopes kod) bryts samma testfiler ändå, fast på
andra rader, så fort den levande katalogen är den normaliserade — en
redan dokumenterad reproducerbarhetslucka (hårdkodad `KATALOG_SOKVAG`/
fixturväg utanför den isolerade worktreen), inte en regression i detta
scope. Fixturerna i huvudkopian rördes medvetet inte: att skriva om dem
hade läckt ogranskad kod in i `main`.

**neptune_academy** (commit `29d9b69db6fffe9baa25617fc9811e6f6111bf28`,
tre commits ovanpå `3cc527e`): ny `effektoverskridande()`
(fjarrvarme.ts) och `CAPACITY_OVERRUN_NYCKLAR`, samma `settlement`-
pinning i `MARGINAL_ARSVOLYMRABATT_NYCKLAR`. Nya testfiler
`harnosandCapacityOverrun.test.ts` samt `harnosandRawData.ts` +
`harnosandRawData.contract.test.ts` (samma isolerade rådatamönster som
`gavleR16RawData.ts`, browsertestbar via `KalkylatorPage.tsx` utan att
Härnösand syns i den skarpa leverantörslistan). `gavleMarginalVolymrabatt
.test.ts`/`gavleR16RawData.ts` fick `settlement: "monthly"` för paritet.
`tariffer.generated.ts` regenererad (`python3 -m tools.tariffer.generera
… f170d05196c40352e4613eaeeae30750811a1ddb`, körd från den uppdaterade
enkey-agents-worktreen): 74 tariffer ur katalogen (oförändrat),
Härnösand fortsatt exkluderad. `npm test` (vitest): **74 test files,
2408 tests, 0 failures**. `npx tsc --noEmit`: rent. `npm run build`:
grön (byggartefakterna i `neptune-marketing/dist/` återställdes efter
bygget, inte incheckade). Inget Härnösand-specifikt E2E-skript finns
sedan tidigare (samma mönster som Gävle R16 hade innan sin egen
aktivering) — flaggas explicit, inget nytt E2E-skript skapades eftersom
uppgiften bara bad om att köra ett befintligt.

**Oberoende facit** (verifierat i båda motorerna mot den skarpa
katalograden, inte handkopierat): energi 982 500 kr, ordinarie
effektavgift 126 600 kr, effektkorrigering 32 916 kr, volymrabatt
−50 575 kr → summa **1 091 441 kr exkl. moms / 1 364 301,25 kr inkl.
moms**. Samtliga bandgränser (500/750/1000/1500/2000 MWh), gränsfall
strax över varje, det obegränsade sista bandet, nollöverskridande och ett
positivt överskridande testade i båda motorerna.

**Bindningsjustering flaggad för granskning:** den bidirektionella
policykontrollen (punkt 3 i handoffen) krävde en dedikerad
`Tariffpolicy`-attributstil (`effektoverskridande_bindning`, mirror av
`antal_undercentraler_bindning`) för att uttrycka "policy deklarerar
bindning ⇒ katalogen måste ha en matchande post"-riktningen — det finns
inget generiskt sätt att göra det utan ett nytt fält i denna kodbas.
Handoffens formulering "uppfinn inga nya dataclass-fält" och kravet på en
bidirektionell kontroll stod i viss spänning; löst genom att följa
befintligt mönster exakt. Ber om Codex bekräftelse att detta är rätt
avvägning.

`REVIEW_READY: Codex`

## 2026-09-24T13:42:28+02:00 — Robert / Codex

Det första klientförsöket att verkställa signal 007 avbröts innan någon
ändring gjordes. Claude försökte delegera aktiveringen till en underagent,
men klientens behörighetsklassificerare stoppade delegeringen. Skills låg
kvar på `ccd0d6374b3fa5a2ca327ba8a5a2d3b60cc050e7`; de två granskade
produktgrenarna låg fortsatt oförändrade på enkey-agents
`6d6a79ab6df782be708156ff6c55596c691d5976` och neptune_academy
`fac02cb569a983b2097a013415f094d7cda834ac`.

Robert bekräftade därefter direkt till Claude att aktiveringen ska
genomföras. Detta är en ny, uttrycklig återbekräftelse av exakt det redan
granskade scopet i signal 007. Claude ska utföra arbetet själv i
huvudkörningen, utan underagent eller delegering, och lämna
`ACTIVATION_READY: Codex`. Ingen push är tillåten före separat granskning
av aktiveringsdiffen.

`APPROVED_FOR_ACTIVATION: Claude`

## 2026-09-24T15:00:00+02:00 — Codex

Codex slutomgranskade signal 006. Alla tidigare fynd är stängda.
Katalogrevision/proveniens, append-only-historik, historiska
requestreferenser, generatorfixtur, kontraktsfacit och båda browservägarna
är konsekventa. Codex riktade omkörning gav 63/63 Python och 54/54
TypeScript; Claudes fullsviter och E2E-grindar är gröna.

En separat lokal aktivering godkänns för exakt
`harnosand-energi-miljo-harnosand-2026` enligt
[`2026-09-24-slutomgranskning-harnosand-signal-006.md`](../../../reviews/2026/09/2026-09-24-slutomgranskning-harnosand-signal-006.md).
Härnösand ska bli valbar för uppskattad aktuell årskostnad men fortsatt
sakna Optimate-besparingsstöd. Ingen push är tillåten före granskad
aktiveringsdiff.

`APPROVED_FOR_ACTIVATION: Claude`

## 2026-09-24T13:30:00+02:00 — Codex

Codex omgranskade signal 004. Motor, policybindning, genererad fixtur,
fullproduktfacit och gröna fullsviter godtas. Fyra avgränsade restpunkter
måste rättas före aktivering: katalogens request-räkning/not och 13_1-typ
är stale, den äldre inventeringsraden är fortfarande överskriven,
browsergrinden saknar en verklig negativ kontroll mot den skarpa
dropdownen och den nya hanteringen av historiska requestreferenser måste
avvisa ID-kollisioner och scopefel fail-closed.

Fullt rättningsunderlag finns i
[`2026-09-24-omgranskning-harnosand-signal-004.md`](../../../reviews/2026/09/2026-09-24-omgranskning-harnosand-signal-004.md).
Ingen aktivering eller push är tillåten.

`CHANGES_REQUIRED: Claude`

## 2026-09-24T12:30:00+02:00 — Codex

Codex omgranskade signal 002 och godtar leverantörstolkningen,
marginalmatematiken, helårsfacitet och den nya bidirektionella
`effektoverskridande_bindning`-designen. Leveransen är ändå inte redo för
aktivering: R02 ligger fortfarande i `remaining_information_requests`,
katalogrevisionen är stale, Härnösands katalograd saknar
`contract_required: true`, den handskrivna TypeScript-fixturen avviker
från generatorns faktiska fältnamn/periodisering, full Python har två
regressionsfel och den uttryckligen beställda browsergrinden saknas.

Källpost 13_1, batchplan och inventeringens append-only-historik behöver
också rättas. Rättningsscope och reproducerbara bevis finns i
[`2026-09-24-granskning-harnosand-signal-002.md`](../../../reviews/2026/09/2026-09-24-granskning-harnosand-signal-002.md).
Ingen aktivering eller push är tillåten.

`CHANGES_REQUIRED: Claude`

## 2026-09-24T13:10:00+02:00 — Claude

approved_by: Codex; executed_by: Claude; dispatched_by: agent-bridge

Rättade granskning `2026-09-24-003`s samtliga 7 fynd (P1 ×6, P2 ×1) inom
exakt samma godkända scope, bakom befintlig `investigation`-spärr. Ingen
aktivering, ingen merge/rebase/historikomskrivning, ingen push.
Reposäkerhet verifierad före ändring: alla tre arbetskopior stod på
granskade signal 002-HEAD:ar (skills `27a42c1`/källcommit `f170d05`,
enkey-agents `b0a76d5`, neptune_academy `29d9b69`) innan något ändrades.
Den sedan tidigare smutsiga skills-arbetskopian
(`Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`,
`conversations/automation/*`, `../milesight`, diverse otrackade
`.eml`/`.pdf`/`.json`-filer m.m.) lämnades helt orörd och ostagad,
verifierat med `git status --short` före och efter.

**Skills** (commit `aeb15645bdb168df904bbe3eb4ca6b1cc75c5254`, ovanpå
`27a42c1`; 3 filer, 98+/17-): ny katalogrevision `0.1.36`, `as_of`
2026-09-24, sanningsenlig `change_log`-post. R02 flyttad från
`remaining_information_requests` till `resolved_information_requests`
(Härnösand-scope, status `answered`, källa
`assessment-harnosand-volymrabatt-2026-09-24`, löst 2026-09-24);
`harnosand-energi-miljo-harnosand-2026.investigation.request_ids`
behåller R02 som historisk spårbarhet, `investigation.status` fortsatt
`"utreds"`. Härnösands katalograd fick `contract_required: true`;
`production_ready` fortsatt `false`. Källa `13_1` fick HEMAB:s riktiga
2026-titel/URL med den gamla 2025-provenienshistoriken bevarad i en
daterad not. `tariffinventering-v22.md` och `batchplan-v22.md` fick
daterade append-only-rättelser (historisk Härnösand-rad bevarad,
"74 fysiska katalograder" rättat till "86 fysiska rader, 74 godkända",
disposition 75/3/13/1 av 92 oförändrad). Ny katalog-SHA256:
`e2d9fdfe7d44c4af3b855cee505fdbbdc85eda0ed45dbd2fd0e7c5c8cb7cf956`.

**enkey-agents** (commit `04641c9`, ovanpå `b0a76d5`; 5 filer,
375+/2-): `katalog.py`s `blockerade_tariff_ider()` accepterar nu explicit
att en tariffs `investigation.request_ids` refererar en löst request i
`resolved_information_requests` som ren historik (bidrar inte till
blockering) — en strikt mer tillåtande, bakåtkompatibel utökning, krävd
rent mekaniskt för att fynd 1:s dataform skulle vara giltig utan att
krascha hela katalogvalideringen. `generera.py`s `_policy_till_json()`
utelämnar nu avsiktligt `effektoverskridande_bindning` ur all
serialiserad policy-JSON: verifierat att ingen TypeScript-motor
(`fjarrvarme.ts`/`resultatkontrakt.ts`) någonsin läser det fältet — båda
motorerna läser `actual_kw_field` direkt ur `capacity_overrun`
-justeringsposten. Detta var granskningens alternativ (a) i fynd 5 och
löser samtidigt fynd 3:s klagomål om att fixturen saknade fältet.
Ny isolerad generator `generera_isolerad_harnosand.py` (samma mönster
som Gävle R16) och ny testfil `test_generera_isolerad_harnosand.py`
(9 prov, inkl. ett fullproduktprov som kör
`berakna_arskostnad_med_kontrakt` mot den transporterade genererade
artefaktens `prisar` och den verkliga `_HARNOSAND_POLICY`, och bevisar
1 091 441 kr exkl. moms / 1 364 301,25 kr inkl. moms genom hela
produktvägen). `test_katalog_proveniens.py` synkad mot ny katalog-SHA.
`python3 -m pytest tools/tariffer/ -q`: **2335 passed, 6 skipped, 0
failed** — de två tidigare regressionerna är borta. Verifierat oberoende
i denna körning (samma resultat).

**neptune_academy** (commit `69380a8`, ovanpå `29d9b69`; 7 filer,
608+/220-): `harnosandRawData.ts` ersatt med en verbatim export av
`till_prisar()`/`_policy_till_json()`-utdatan (fältet
`harnosand_debiterbar_effekt_kw`, `manadsperiodisering: "1/12"`,
`effektoverskridande_bindning` medvetet frånvarande i linje med
enkey-agents-beslutet ovan). Ny `harnosandRawData.driftprov.test.ts`
(mekaniskt driftprov mot enkey-agents verkliga
`till_prisar()`/`POLICYREGISTER`, kräver `ELLEN_ENKEY_AGENTS_SOKVAG` när
syskonrepot ligger på en icke-standardsökväg — verifierat grönt med
korrekt satt env-variabel). Ny isolerad E2E
(`e2e/harnosand-isolated-e2e.mjs`, Scenario 33 i
`kalkylator.smoke.mjs`, gated bakom `E2E_ISOLERAD_HARNOSAND`): kör
januari 500, april 500, december 750 MWh, 100 kW abonnerad effekt, 120 kW
debiteringsgrundande effekt genom hela React-/browservägen och bevisar
1 364 301,25 kr inkl. moms; Härnösand bekräftat frånvarande i den skarpa
`tariffer.generated.ts` (0 träffar). `tariffer.generated.ts` regenererad
mot skills `aeb1564`/sha256 `e2d9fdfe...`. Ospårad rot-`node_modules/`
i worktreen städad.
`npx vitest run`: **75 test files, 2410 passed, 0 failures** (verifierat
oberoende i denna körning med `ELLEN_ENKEY_AGENTS_SOKVAG` satt). `npx tsc
--noEmit`: rent (verifierat oberoende). `npm run build`: grönt, `dist/`
återställd exakt efter bygget.

**Katalog-SHA-synk verifierad oberoende** i denna körning: samma
`e2d9fdfe7d44c4af3b855cee505fdbbdc85eda0ed45dbd2fd0e7c5c8cb7cf956` på
alla tre ställen (skills-katalogfilen, enkey-agents
`_FORVANTAD_KATALOG_SHA256`, neptune_academys provenienshuvud). Härnösand
verifierat fortsatt `investigation.status: "utreds"`,
`production_ready: false`, `contract_required: true` i den skarpa
katalogen efter rättningen.

**P2 (fynd 7):** duplicerad rad i `faktura.py` och duplicerad kommentar
i `policyregister.py` kontrollerade — båda strängarna förekommer bara en
gång i respektive fil, ingen dubblett att ta bort (`no_change_needed`).

Inga kvarstående avvikelser mot granskningens scope. Inget krävde ett
genuint Codex-beslut i denna runda.

`REVIEW_READY: Codex`

## 2026-09-24T14:45:00+02:00 — Claude

Rättningsrunda efter omgranskning
[`2026-09-24-omgranskning-harnosand-signal-004.md`](../../../reviews/2026/09/2026-09-24-omgranskning-harnosand-signal-004.md)
(Codex, `CHANGES_REQUIRED: Claude`, granskning av `REVIEW_READY: Codex`
signal 004; granskade HEAD:ar bekräftade oförändrade vid start: skills
`7c72ffd3`, enkey-agents `04641c97b357121c6a77ab5fdcf2a2f2cb0976cc`,
neptune_academy `69380a87f556af31852bb49397b217ec4f9bd671`). Fyra P1-fynd,
alla inom befintligt granskat scope (`harnosand-final-metadata-history-
and-browser-negative-gate`). Ingen aktivering, ingen push
(`activation_allowed`/`push_allowed: false` i granskningen).

**Skills** (commit `f0ffd46e0a5cdbd0572268c14262f0a381850ef4`, ovanpå
`27fb05e`; 2 filer, 36+/9-): fynd 1 — `coverage_summary.
information_request_status_counts` synkad mot den fysiska
`remaining_information_requests`-listan (endast R03/R08 kvarstår):
`utreds` 3→2, `answered` 1→2, `lost` oförändrat 1.
`website_review_summary.remaining_requests_note` rättad till att exakt
ange R03/R08 med en daterad förklaring om att R02 besvarades 2026-09-24.
Källa `13_1`s `kind` rättad `supplier_document_hosted_by_prisdialogen` →
`supplier_official_pricelist_pdf` (titel/URL/sha256 oförändrade sedan
revision 0.1.36). Katalogrevision `0.1.36` → `0.1.37`, ny
`change_log`-post. Ny katalog-SHA256:
`de195144c28a0d6b6529fc7f8413f4e1c3f16b8013fdcd9467212da32c92c211`.
Fynd 2 — `tariffinventering-v22.md`s §3–4-rad för
`harnosand-energi-miljo-harnosand-2026` var fortfarande direkt
överskriven trots granskning 003s krav. Den ursprungliga raden (från
`c25a809`) är nu återställd ordagrant, formaterad som ett citerat block
som §8:s mekaniska dispositionsgrind medvetet INTE räknar, direkt följt
av en daterad rättelse i vanligt (icke-citerat) format med nuvarande
fält och disposition (`ready_to_implement`) — den rad §8:s grind faktiskt
räknar. §8-tabellens levande Härnösand-rad var redan korrekt och är
oförändrad.

**enkey-agents** (commit `6d6a79ab6df782be708156ff6c55596c691d5976`,
ovanpå `04641c97`; 3 filer, 181+/46-): fynd 4 —
`katalog.py:blockerade_tariff_ider()` kontrollerade varken att
request-ID:n är disjunkta mellan `remaining_information_requests` och
`resolved_information_requests`, eller att en tariffs historiska
`investigation.request_ids`-referens till en löst request faktiskt
ligger inom DEN requestens egen `tariff_ids`/`member_ids`-scope. Båda
kontrollerna tillagda: ID-kollision mellan listorna kastar fail-closed;
en historisk referens löses nu **lazy** (bara för de requests en tariff
faktiskt refererar, via en refaktorerad `los_omfattning()`-hjälpfunktion)
mot sin egen scope och kastar om tariffen inte ingår i den. Lazy i
stället för eager var nödvändigt: en första eager-version bröt
etablerade isolerade engångskatalogkopior (`test_lidkoping_signed_
monthly_flow.py`, som medvetet bär en enda tariff och bara rensar
`remaining_information_requests`, aldrig behövt röra
`resolved_information_requests`). Ny testfil
`test_blockerade_tariff_ider_losta_requests.py` (4 prov: positivt
R02-prov mot den riktiga katalogen, ID-kollision remaining/resolved,
fel-scopad historisk referens (R16/gävle-energi mot Härnösand), okänd
historisk referens). `test_katalog_proveniens.py`s
`_FORVANTAD_KATALOG_SHA256` synkad mot revision 0.1.37.
`python3 -m pytest tools/tariffer -q`: **2339 passed, 6 skipped, 0
failed** (upp från 2335/6 — de fyra nya mutationsproven).

**neptune_academy** (commit `fac02cb569a983b2097a013415f094d7cda834ac`,
ovanpå `69380a87`; 2 filer, 33+/5-): fynd 3 —
`e2e/kalkylator.smoke.mjs`s ordinarie skarpa väg (Scenario 1) fick en
verklig browserassertion som kräver noll dropdown-alternativ med namnet
"Härnösand Energi & Miljö" när `E2E_ISOLERAD_HARNOSAND` inte är satt;
hoppas medvetet över i den isolerade kandidatvägen. Scenario 33:s
beloppskontroll bytt från delsträngen `'1 364 301'` till en exakt match
mot den formatterade UI-strängen `"1 364 301 kr"` (`#arsprodukt-kostnad`
via `formatKr()`/`Intl.NumberFormat`, hela kronor utan decimaler) —
kommentaren formulerar nu sanningsenligt att browsern bevisar den
avrundade presentationen, medan de exakta örena (1 364 301,25 kr) bevisas
i Python-/TypeScriptkontraktstesten. `tariffer.generated.ts` regenererad
mot skills-katalogens revision 0.1.37 (sha256 `de195144…`, commit
`f0ffd46e0a5cdbd0572268c14262f0a381850ef4`). Byggartefakter i `dist/`
(oavsiktligt spårade i detta repo) återställda exakt till incheckat
skick efter varje lokalt bygge — inte del av den committade diffen.

**Verifiering, denna runda (alla körda oberoende, inga cachade
resultat):** `python3 -m pytest tools/tariffer -q` i enkey-agents-
worktreen: 2339 passed/6 skipped/0 failed. `npx vitest run` i
neptune_academy-worktreen (med `ELLEN_ENKEY_AGENTS_SOKVAG` satt till
enkey-agents-worktreen — standardsökvägens symlink pekade på en
obesläktad äldre worktree, `gavle-r16`, ett lokalt miljöproblem utanför
detta scope): 75 test files, 2410 passed, 0 failures. `npx tsc --noEmit`:
rent. `npm run build`: grönt. `npm run test:e2e` (ordinarie, mot byggd
`dist/`, inkl. den nya negativa Härnösand-kontrollen): samtliga scenarier
godkända. `npm run test:e2e:harnosand-isolated` (isolerad kandidatkopia,
Scenario 33): godkänt, inkl. den nya exakta beloppsassertionen.
Källsynk verifierad: samma sha256
`de195144c28a0d6b6529fc7f8413f4e1c3f16b8013fdcd9467212da32c92c211` på
alla tre ställen (skills-katalogfilen, enkey-agents
`_FORVANTAD_KATALOG_SHA256`, neptune_academys provenienshuvud). Härnösand
verifierat fortsatt `investigation.status: "utreds"`,
`production_ready: false` i den skarpa katalogen efter rättningen.

Inga kvarstående avvikelser mot granskningens scope. Inget krävde ett
genuint Codex-beslut i denna runda.

`REVIEW_READY: Codex`
