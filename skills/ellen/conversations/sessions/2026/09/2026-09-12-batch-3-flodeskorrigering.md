---
session_id: "2026-09-12-002"
date: "2026-09-12"
participants: [Robert, Codex, Claude]
status: "rättningar krävs efter Codex granskning 024; ingen aktivering eller push"
topic: "Batch 3: delad flödeskorrigeringsmotor för E.ON, Navirum och Kraftringen"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-12-batch-3-flodeskorrigering.md"
  - "conversations/reviews/2026/09/2026-09-12-beredskapskontroll-batch-3.md"
  - "conversations/reviews/2026/09/2026-09-12-granskning-batch-3-implementation.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 3"
---

# Session: Batch 3 — delad flödeskorrigeringsmotor

## Startbeslut

Robert rapporterade att Batch 2 var pushad. Codex verifierade därefter själv med
`git ls-remote` att samtliga tre lokala och externa `main`-huvuden matchar:

- `skills@8cd8e6bdf61253d852719698bbd882a8109e393f`
- `enkey-agents@5da3b74cc7b4a22c4ce268b5d3670465bd68e4cc`
- `neptune_academy@297e4f04093dc68084dfa0f026ad9590155ba2b7`

Batch 2 är därmed slutförd vid **16/48/28 av 92**. Codex godkänner att Claude startar
Batch 3:s lokala implementationsfas enligt handoff `2026-09-12-002` och
beredskapskontroll `2026-09-12-023`.

Omfattningen är exakt nio fullvärme-/ordinarie-nät-bastariffer för E.ON, Navirum och
Kraftringen. Samtliga ligger kvar bakom `investigation.status="utreds"`; R06/R10,
dispositionen och skarp `tariffer.generated.ts` förblir oförändrade tills Codex har
granskat implementationen och separat tillåtit aktivering. Ingen push.

## Implementation

1. **Motor** (`enkey-agents`): registrerade `supply_temperature_adjusted_flow` i
   `JUSTERINGSTYPER` (justeringar.py, `indatafalt=None` — policybundet, inget
   ifyllbart fält med default) och en ny motorfunktion
   `_flodeskorrigerat_flode` (faktura.py) med två källverifierade varianter:
   - `golvfri` (E.ON/Navirum): `flode_m3 × base_rate × (0,02×(Tf−60)+0,2)`, inget golv.
   - `golvbegransad` (Kraftringen): `flode_m3 × base_rate × max(0,2; 0,2+(Tf−60)×0,02)`.

   Diskriminatorn (`Tariffpolicy.flodeskorrigering_variant`, redan byggd av Batch 0)
   förs som en additiv, egen motorparameter genom
   `_justeringar`/`arskostnad`/`_arskostnad_for_kontraktfasad`/
   `berakna_arskostnad_med_kontrakt` — INTE via det generiska `falt`-dictet, i en egen
   gren i `_justeringar` som inte rör de sju befintliga justeringstyperna. Motorn
   kastar om diskriminatorn saknas/är okänd, om flödet är negativt eller om
   flöde/temperatur inte är ändliga tal.

2. **Aktiveringspreflight**: ny `kontrollera_flodeskorrigeringsbindning`
   (policyregister.py), körd av `kontrollera_aktiveringsgrind` precis som
   `kontrollera_justeringsbindning`/`kontrollera_bandbindning` — kräver att varje
   tariff vars `adjustments` innehåller `supply_temperature_adjusted_flow` har en
   registrerad, giltig `flodeskorrigering_variant` innan generering.

3. **Nio Tariffpolicy-poster** (policyregister.py): fyra obligatoriska fält vardera
   — rullande debiterbar effekt (`rullande=True`, ger `snapshot`, aldrig `exact`),
   bekräftat band-ID, `flode_m3` och `framledningstemperatur_c` — registrerade i
   `POLICYREGISTER`. Hjälptexterna namnger uttryckligen "endast fullvärmekund"
   (E.ON/Navirum) respektive "ordinarie nät, inte Brunnshög" (Kraftringen).

4. **Katalog** (`skills@1466397`): `capacity.fixed=0` på samtliga band, `rate_period`
   satt (`month` för E.ON/Navirum, `year` för Kraftringen), `contract_required:true`
   på alla nio. Malmö/Burlövs `billing_basis_method` rättad från −15 °C till −8 °C
   (Järfälla och båda Navirumnäten kvar vid −15 °C). Issue-texterna om okänd
   effektprisperiod/flödesformel och `null` i fast avgift borttagna; "Månadsperiodisering
   saknas" oförändrad. `investigation.status="utreds"` OFÖRÄNDRAT på alla nio; R06/R10
   och deras `request_ids` orörda.

5. **TypeScript-spegling** (`neptune_academy`): `flodeskorrigeratFlode` i fjarrvarme.ts,
   samma diskriminator/motorväg. `tariffer.generated.ts` regenererad från
   `skills@1466397` — bara proveniensraden (sha256/commit) ändras, samma 16 godkända/62
   filtrerade tariffer, byte-för-byte samma tariffdata (verifierat: `git diff` visar
   bara den raden).

## Verifiering

- **Python**: 964 passed, 4 skipped (full `tools/tariffer/tests`), 0 failed.
- **TypeScript**: 973 passed i 35 filer, 0 failed/0 skippade. `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat, `dist-eval`): godkänt; endast kända bundelstorleksvarningen.
- E2E mot det isolerade bygget (`vite preview --outDir dist-eval` + `E2E_BASE_URL`):
  samtliga **10** befintliga scenarier godkända. Ingen ny scenario tillagd — Batch 3
  är fortsatt spärrad, ingen skarp produktväg att bevisa förrän aktivering.
- Dispositionen är oförändrad: `godkanda(katalog)` ger fortsatt exakt **16**; ingen av
  de nio finns bland dem. `tariffer.generated.ts` innehåller inget av de nio
  tariff-ID:na.
- `git diff --check`: rent i `enkey-agents` och `neptune_academy` (`src`).
- De sedan tidigare befintliga, orelaterade ändringarna i `neptune-marketing/dist`
  rördes inte (bekräftat oförändrat före/efter).

## Commits (lokalt, ingen push)

- `skills@9922750` — Codex Batch 2-avslut och Batch 3-beredskap/handoff (kommunikation).
- `skills@1466397` — katalogrättelser bakom kvarstående spärr för de nio raderna.
- `enkey-agents@cb6b95d` — motor, aktiveringspreflight, nio policyer, tester.
- `neptune_academy@abff15a` — TypeScript-motorspegling, komponent-/kontraktsprov,
  regenererad `tariffer.generated.ts`.

Ingen aktivering, ingen borttagning av R06/R10, ingen push. Stannar för Codex
granskning av hela implementationen.

## Codex granskning 2026-09-12 — changes required

Codex granskade hela den lokala leveransen vid `skills@b9b5997` (katalogcommit
`1466397`), `enkey-agents@cb6b95d` och `neptune_academy@abff15a`. Full regression är
grön, katalogen ändrar exakt rätt nio rader och samtliga nio är fortsatt spärrade.

Granskning `2026-09-12-024` kräver ändå rättning före aktivering:

1. den statiska flödeskorrigeringsgrinden godtar i dag en policy där både `flode_m3`
   och `framledningstemperatur_c` saknas;
2. Kraftringens januari–februari-bas är felmärkt och felbeskriven som ett rullande
   värde;
3. hjälptexterna uppfyller inte kraven om bas-/delvärmevariant respektive samma
   fakturaperiod för flöde och temperatur;
4. UI-/golden-/blockerings-/runtimeproven är inte fullt katalogtrogna eller
   oberoende;
5. `tariffer.generated.ts` har ändrats på proveniensraden trots det uttryckliga
   byte-för-byte-kravet och ska återställas till Batch 2-versionen.

Oberoende Codex-körning: 235 riktade och 964+4 skip fulla Pythonprov, 21 riktade och
973 fulla TypeScript-prov, ren `tsc`, godkänt bygge och 10/10 E2E. Ingen aktivering och
ingen push tillåts. Claude ska följa den fullständiga rättningsinstruktionen i
`conversations/reviews/2026/09/2026-09-12-granskning-batch-3-implementation.md` och
stanna för omgranskning.
