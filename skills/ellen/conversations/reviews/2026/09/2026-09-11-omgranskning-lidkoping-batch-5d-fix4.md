---
review_id: "2026-09-11-001"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 4"
  - "Samtliga fynd och acceptansbevis i granskning 2026-09-10-012"
reviewed_heads:
  skills: "904655cef52288d9e8c68a6eff5cc45d5843bd91"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "0a85eba59e1e89680d1404dcf13fb5aef813da9a"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-10-012"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 4

## Beslut

**Changes required.** De tre beställda P2-rättningarna är levererade: en normal
knappsubmit når nu Lidköpings svenska, fältnära kapacitetsfel; den tvåtariffade
sidmatrisen finns och är grön; de publika domänproven jämför exakt felorsak; och
TypeScript använder fasta momsfacit. Den valda lösningen, `noValidate` på hela
beräkningsformuläret, har däremot öppnat en ny **P1-regression**: övriga HTML-validerade
fält kan nu passera till beräkningen med ogiltiga värden utan motsvarande
applikationsvalidering.

Ingen tariff är aktiverad och inget repo är pushat. Produktionsurvalet är fortsatt sju
tariffer och dispositionen 7 implementerade / 57 redo / 28 blockerade av 92 är
oförändrad.

## Fynd

### P1 — global `noValidate` låter ogiltig MWh och antal undercentraler ge ett motsägelsefullt resultat

Rättningen lägger `noValidate` på kalkylatorns hela huvudformulär. Det löser just
kapacitetsfältets konflikt, men kopplar samtidigt bort webbläsarens skydd för samtliga
andra `min`/`max`-/`step`-fält. `handleCalculate` speglar inte alla dessa regler.

Codex reproducerade följande i riktig headless Chromium mot den levande kalkylatorn:

1. area `10 000`, energiläge MWh, årsenergi `-5`, undercentraler `21`;
2. `#energyMwh.checkValidity() === false` eftersom `min=1` och
   `#substations.checkValidity() === false` eftersom `max=20`;
3. normal klickning på **Beräkna energipotential** gav trots detta inget fel och
   renderade ett färdigt resultat;
4. resultatet räknade energin från schablon men redovisade samtidigt energikällan som
   **”Angiven av användaren (-5 MWh/år)”**, samt visade **21 undercentraler**.

Roten är konkret: MWh-grenen accepterar det parsade värdet `-5`, men båda
rimlighetskontrollerna körs bara för värden större än noll. `knownEnergy` blir därför
`undefined` och motorn faller tillbaka till schablon, medan `energySourceLabel` behåller
`-5`. `substationsNum` har bara ett lokalt golv via `Math.max(1, ...)`, inget tak vid 20.
Före `noValidate` stoppade webbläsaren båda värdena före submit.

Detta är inte bara en felmeddelandefråga: kalkylatorn levererar en beräkning på annan
energi än den användaren matade in och beskriver ändå den ogiltiga siffran som källa.
Samma globala förändring berör även övriga huvudformsfält med HTML-gränser och ska därför
hanteras som en valideringsägarskapsfråga för hela formuläret.

## Bekräftade rättningar

- En verklig Chromium-klickning med Sandviken, `min=3` och värdet 2 når nu React:
  `aria-invalid="true"`, `aria-describedby="kapacitetKw-fel"`, synlig svensk text
  ”Värdet är för lågt.”, två `role=alert` och inget resultat.
- Sidtestet har båda tariff-fixturerna och provar 0–41-produktens 2/3/41/42 kW samt
  42+-produktens 41/42 kW via `requestSubmit()`. HTML-gränser, svensk fälttext och ARIA
  verifieras; giltiga gränser når resultat med explicit valt band-ID.
- De publika gränsproven jämför nu hela
  `ogiltigaFalt=[{nyckel:'lidkoping_debiterbar_effekt_kw', orsak:'min'|'max'}]`.
- TypeScripts momstester jämför direkt mot 17 947,50 respektive 90 057,50 kr och det
  missvisande äldre `invalid_energy`-testnamnet är rättat till saknad MWh-proveniens.
- Kontaktformulären är oförändrade.

## Oberoende verifiering

- Riktade Lidköpingstester: **3 testfiler, 70 tester passerade**.
- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **507 passed**.
- `npm test -- --run`: **21 testfiler, 569 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: godkänd för befintliga riksgenomsnitts- och Sandvikenscenarier;
  `dist` återställd.
- Två riktiga Chromiumprov: kapacitetsrättningen verifierad positivt och
  helformulärsregressionen reproducerad enligt P1-fyndet.
- `git diff --check` är rent och produktrepona är rena. Sedan tidigare orelaterade filer
  i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Gör rättningsrunda 5, begränsad till valideringsregressionen ovan:

1. Ta bort den globala `noValidate`-lösningen om inte samtliga huvudformsbegränsningar
   speglas av applikationsvalidering. Rekommenderad liten lösning är att bevara native
   constraint validation för resten av formuläret och hantera just `kapacitetKw` via en
   riktad `onInvalid`-väg som sätter samma svenska fälttext, `aria-invalid`,
   `aria-describedby` och global sammanfattning. Föregående granskning tillät uttryckligen
   detta alternativ. En annan lösning är acceptabel bara om hela formulärets
   valideringskontrakt blir explicit och testat.
2. Lägg regressionstest med normal knappsubmit för minst negativ MWh och fler än 20
   undercentraler. Båda ska stoppas utan resultat; kalkylatorn får aldrig falla tillbaka
   till schablon och samtidigt redovisa den ogiltiga MWh-siffran som användarkälla.
   Kontrollera samtidigt övriga `min`/`max`-/`step`-fält som påverkas av vald lösning.
3. Bevara de sex nya tvåtariffade kapacitetsfallen och verifiera i riktig
   browser-/E2E-väg att 2 kW fortsatt ger svensk fälttext och ARIA för en levande
   kontraktsgated tariff.

Kör hela Python-/TypeScriptmatrisen, `tsc --noEmit`, bygge, självbärande E2E och
`git diff --check`. Gör en fokuserad lokal commit och rapportera exakta HEAD-hashar.
Aktivera ingen tariff, ändra inte 7/57/28 och pusha inget repo. Stanna därefter för ny
Codex-omgranskning.
