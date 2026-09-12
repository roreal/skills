---
handoff_id: "2026-09-12-002"
created_at: "2026-09-12T18:57:05+02:00"
from: Codex
to: Claude
status: changes-required-after-implementation-review
implementation_allowed: true
approved_implementation_scope: "batch-3-eon-navirum-kraftringen-flow-adjustment"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
latest_review: "2026-09-12-026"
baseline_remote_heads:
  skills: "8cd8e6bdf61253d852719698bbd882a8109e393f"
  enkey_agents: "5da3b74cc7b4a22c4ce268b5d3670465bd68e4cc"
  neptune_academy: "297e4f04093dc68084dfa0f026ad9590155ba2b7"
tariff_disposition_before: "16 implemented / 48 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "16 implemented / 48 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "25 implemented / 39 ready / 28 blocked av 92"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 3"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §4.1, §6, §6a.2, §6a.5 och §7"
  - "conversations/reviews/2026/09/2026-09-12-beredskapskontroll-batch-3.md"
  - "conversations/reviews/2026/09/2026-09-12-granskning-batch-3-implementation.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix1.md"
  - "conversations/reviews/2026/09/2026-09-12-omgranskning-batch-3-fix2.md"
---

# Uppdrag till Claude: Batch 3 — E.ON, Navirum och Kraftringen

## Mål

Implementera lokalt en parametriserad `supply_temperature_adjusted_flow`-motor i Python
och TypeScript samt tariffpolicyer för exakt nio bastariffer. Målet är en uppskattad
årskostnad från bekräftad MWh, debiterbar effekt, bekräftat effektband, flöde och
framledningstemperatur.

Detta är en implementationsfas. **Ingen tariff aktiveras och inget pushas.**

## Exakt tariffomfattning

1. `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`
2. `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`
3. `e-on-malmo-malmo-och-burlov-bostader-2026`
4. `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`
5. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`
6. `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`
7. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`
8. `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`
9. `kraftringen-kraftringen-2026`

Ändra inte Batch 3b:s åtta `--bas-delvarme`-varianter och inte Kraftringens
`--brunnshog`-variant.

## Katalogrättelser bakom spärren

Gör följande i en fokuserad katalogrevision, men behåll
`investigation.status="utreds"` på samtliga nio rader:

- E.ON/Navirum ×8: sätt varje bands `fixed:0` och
  `capacity.rate_period:"month"`. Behåll `monthly_proration:null`; månadsprodukten är inte
  godkänd. Sätt `contract_required:true`.
- Malmö/Burlöv ×2: rätta `billing_basis_method` från −15 °C till −8 °C. Järfälla och
  båda Navirumnäten ligger kvar vid −15 °C.
- Kraftringen: sätt `fixed:0` på alla fyra band,
  `capacity.rate_period:"year"` och `contract_required:true`.
- Behåll alla publicerade energi-, effekt- och flödespriser oförändrade.
- Ta bort endast de issue-texter som rättelserna faktiskt löser: okänd
  effektprisperiod/flödesformel samt `null` i fast avgift. Behåll den kända issue-texten
  om saknad månadsperiodisering; den blockerar månadsvis redovisning men inte framtida
  `annual_forward`.
- R06 och R10 samt de nio tariffposternas requestreferenser ska ligga kvar tills en
  separat aktivering är godkänd. Lägg inte in en hängande requestreferens.
- Höj katalogrevisionen och beskriv exakt de bakom-spärren-rättelser som gjorts. Skriv
  inte att tarifferna är aktiverade.

Efter denna fas ska `godkanda(katalog)` fortfarande ge 16 och den genererade
**tariffpayloaden** vara oförändrad. Proveniensraden ska bära den aktuella
katalogfilens hash/commit så synktestet förblir sant och grönt. Detta ersätter det
tidigare byte-för-byte-villkoret enligt granskning `2026-09-12-025`; en diff med exakt
proveniensraden är tillåten men ingen Batch 3-tariff får finnas i payloaden.

## Motor och regelvarianter

Registrera `supply_temperature_adjusted_flow` som beräkningsbar typ i Python och
TypeScript. Använd en och samma motorfunktion med explicit diskriminator:

- `golvfri` för E.ON/Navirum:
  `flode_m3 × base_rate × (0,02 × (Tf − 60) + 0,2)`.
- `golvbegransad` för Kraftringen:
  `flode_m3 × base_rate × max(0,2; 0,2 + (Tf − 60) × 0,02)`.

För `flodeskorrigering_variant`/`flodeskorrigeringVariant` oförändrad från
`Tariffpolicy` genom kontraktsfasaden, den interna årskostnadsfasaden och
justeringsdispatchen. Lägg en additiv, valfri parameter med fail-closed kontroll; härled
aldrig varianten från leverantörs- eller tariff-ID.

När en tariff innehåller justeringstypen ska saknad eller okänd variant blockera innan
kostnad returneras. Lägg både statisk korsvalidering i aktiveringsgrinden och en
runtimevakt i motorn. Äldre tariffer utan justeringstypen ska vara oförändrade.

Använd gemensamma, policybundna skalärnycklar för flöde och `Tf`, konsekvent i båda
språken. Värdena måste vara ändliga; flöde får inte vara negativt. Inget neutralvärde
eller gissad standard får göra ett saknat obligatoriskt fält beräkningsbart.

## Tariffpolicyer och användarscope

Bygg nio policyer med befintlig Batch 0/1-infrastruktur:

- `tackning={"annual_forward"}`;
- `stodjer_aktuell_arskostnad=True`;
- `stodjer_besparing=False`;
- skalär debiterbar effekt bunden via `kapacitet_bindning`;
- bekräftat band-ID bunden via `kapacitet_band_bindning`, även för enbandsraderna;
- skalär `flode_m3` och framledningstemperatur `Tf`, båda från faktura/nätdata;
- `flodeskorrigering_variant="golvfri"` för åtta E.ON/Navirum och
  `"golvbegransad"` för Kraftringen.

Effektkravet ska bära den rullande/källperiodsmetadata som gör hela resultatet
`annual/snapshot/complete`, aldrig `exact`. Kronor och schablon ska blockeras typat med
`unsupported_input_mode`; besparingsvägen med `besparing_ej_stodd`.

Policyetiketter och hjälptexter ska vara kompletta och källnära:

- E.ON/Navirum måste tydligt säga **endast fullvärmekund** och hänvisa bas-/delvärme till
  en ännu ej stödd tariffvariant.
- Kraftringen måste tydligt säga **ordinarie nät, inte Brunnshög**.
- Flöde och `Tf` ska beskrivas som värden för samma leverantörs-/fakturaperiod. UI och
  resultat ska tydligt kalla utfallet en uppskattning (`snapshot`).

Skapa ingen tariff-ID-specifik UI-kod; det befintliga generiska policyformuläret ska
rendera tal- och bandfälten från genererad metadata.

## Obligatoriska tester före Codex-granskning

### Motor och paritet

- Python och TypeScript: `Tf` under, exakt och över 60 °C för båda varianterna.
- Ett under-60-fall ska uttryckligen bevisa skillnaden mellan golvfri och golvbegränsad,
  inte bara två positiva happy paths.
- Nollflöde, negativt flöde, icke-ändliga värden, saknad/okänd variant och oförändrade
  befintliga justeringstyper.
- Direkt fasadanrop ska bevisa att policyvarianten faktiskt når rätt motorgren.

### Verkliga katalograder bakom spärr

- En tabellstyrd matris över alla nio tariff-ID:n: katalogrättelser, rätt variant,
  samtliga obligatoriska fält/bindningar, riktiga band-ID:n och `snapshot/complete`.
- Oberoende handräknat goldenfacit per unik regel-/periodfamilj. För E.ON/Navirum ska
  effektpriset bevisligen multipliceras med 12; för Kraftringen får årsavgiften inte
  multipliceras med 12. `fixed:0` får inte skapa en dold stående kostnad.
- Minst ett tariffspecifikt facit för var och en av de nio raderna ska fånga fel energi-,
  effekt- eller flödespris. Förväntat värde får inte genereras av funktionen som testas.
- Kr/schablon/besparing blockeras för varje policyfamilj. Fel band-ID och saknade
  effekt-/flöde-/Tf-fält ska ge fältnära, typade fel.

### Generator och UI utan aktivering

- Kör generatorn mot isolerade katalogkopior där spärren tas bort i testminnet; bevisa
  att alla nio kan genereras med rätt policy och att originalkatalogen fortfarande
  filtrerar bort dem.
- Testa det generiska policyformuläret med representativa, verklighetstrogna genererade
  fixtures för minst E.ON/Navirum och Kraftringen: korrekt bandlista, alla tre numeriska
  uppgifter, scope-hjälptext, normal submit och `snapshot`-resultat.
- Kontrollera att den skarpa, incheckade `tariffer.generated.ts` har byte-för-byte
  oförändrad tariffpayload men sann proveniens för aktuell katalog. Enligt ändringen i
  granskning `2026-09-12-025` får diffen mot Batch 2 vara exakt proveniensraden;
  omockade verkliga produkt-/E2E-prov tillkommer först i en separat aktiveringsfas.

### Regression och leverans

- Kör riktade tester, full `tools/tariffer/tests`, full TypeScript, `npx tsc --noEmit`,
  `npm run eval:build`, befintlig E2E och `git diff --check` i alla berörda repon.
- Verifiera mekaniskt **16/48/28** och att ingen av de nio finns i den skarpa
  produktväljaren.
- Bevara de befintliga, orelaterade ändringarna i `neptune-marketing/dist`; återställ,
  bygg eller commitera dem inte. Använd fortsatt `dist-eval` för isolerat bygge.
- Commitera Codex nya kommunikationsfiler separat och därefter fokuserade lokala
  implementationcommits per repo. Logga bas/slut-HEAD, ändrade filer och exakta
  testresultat. Stanna sedan för Codex granskning.

**Ingen aktivering, ingen borttagning av R06/R10, ingen ändring av skarp genererad
tariffdata och ingen push.**

## Avgränsad rättningsrunda 3 efter granskning 026

Rättningsrunda 2 stänger granskning 025:s fyra ursprungliga fynd och dess fullsviter är
reproducerat gröna. Före aktivering återstår exakt två TypeScript-fynd:

1. skilj en generell `kalperiodDefinition`-källperiod från
   `matchningMotManad`-formatet `ÅÅÅÅ-MM`; Kraftringens period ska sanningsenligt täcka
   januari–februari och samma värde ska nå `IndataPost`;
2. rensa `policyFaltPerioderRaw` och `kapacitetObserveradPeriodRaw` vid leverantörsbyte
   och byte bort från fjärrvärme, med DOM-regressionsprov.

Följ granskning `2026-09-12-026` ordagrant. Ändra inte Python, katalog, priser,
generatorpayload, spärrar, R06/R10 eller disposition. Ingen aktivering och ingen push;
stanna för ny Codex-granskning.
