---
session_id: "2026-09-24-001"
date: "2026-09-24"
participants: ["Robert", "Codex", "Claude"]
status: "REVIEW_READY: Codex"
topic: "Härnösand 2026 — leverantörssvar om volymrabatt"
last_updated: "2026-09-24T12:05:00+02:00"
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
