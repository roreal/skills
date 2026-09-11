---
review_id: "2026-09-11-002"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 5"
  - "P1-valideringsregressionen och browserbeviset i granskning 2026-09-11-001"
reviewed_heads:
  skills: "fcf68eadd09a59d08d65dab5f685080bad90093d"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "35026399d4436ba889e1af7ffa03c6cc5fd23a99"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-11-001"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 5

## Beslut

**Changes required.** De två exakt reproducerade värdena från föregående granskning är
stängda: negativ MWh och 21 undercentraler stoppas nu före beräkning, och Sandvikens
fältnära kapacitetsfel fungerar fortsatt i riktig Chromium. Rättningen behåller emellertid
global `noValidate` och har inte gjort det utlovade **fulla** formulärkontraktet explicit.
Bråktal i heltalsfält och leverantörsspecifika fakturafält utanför sina kataloggränser
passerar fortfarande och ger resultat. Det permanenta browser-/E2E-beviset som beställdes
finns inte heller i committen.

Ingen tariff är aktiverad och inget repo är pushat. Produktionsurvalet är fortsatt sju
tariffer och dispositionen 7 implementerade / 57 redo / 28 blockerade av 92 är
oförändrad.

## Fynd

### P1 — `parseInt` accepterar 1,5 undercentraler och beräknar som 1

`#substations` har heltalssteget 1 genom HTML:s standard för `type="number"`, men den nya
JS-kontrollen använder `parseInt(form.substations, 10)`. Därför blir `1.5` till `1` och
klarar intervallet 1–20.

Codex reproducerade i riktig Chromium:

- `#substations.value === "1.5"`, `checkValidity() === false` och
  `validity.stepMismatch === true`;
- normal klickning gav inget fel och renderade ett färdigt resultat;
- kalkylen använde en undercentral via `substationsNum`, medan resultattabellen visade
  användarens råvärde **”1.5 st”**.

Det är samma typ av motsägelsefulla resultat som rättningsrundan skulle stänga. Tolka
värdet med `Number`, kräv ändlighet och `Number.isInteger`, och använd därefter samma
validerade heltal i beräkning och redovisning.

### P1 — fakturafältens kataloggränser kringgås och motorn klämmer värdet tyst

De dynamiska fälten under ”Förfina med värden från din faktura” renderas med katalogens
`min_varde`, `max_varde` och `step`, men `handleCalculate` validerar dem inte.
`faltForBerakning` skickar varje ändligt tal vidare. Motorns `resolveraFalt` klämmer sedan
värdet till sin gräns, medan kontaktunderlaget fortfarande beskriver råvärdet som
”från fakturan”.

Codex reproducerade detta med den levande Göteborgstariffens `avvikelse_c`:

- fältets tillåtna intervall var −10…10 °C;
- värdet `999` gav `checkValidity() === false` och `validity.rangeOverflow === true`;
- normal knappsubmit gav inget fel och renderade ett resultat;
- beräkningen fick råvärdet 999, vilket `resolveraFalt` tyst klämde till 10 °C, samtidigt
  som kontaktunderlaget skulle redovisa **999 °C (från fakturan)**.

Validera alla ifyllda `valdIndatafalt` mot just den valda prispostens metadata innan
beräkning: ändligt tal, min/max och heltal när `heltal=true`. Ett uttryckligt fel ska ge
inget resultat; användarinmatning får inte klämmas till en annan beräkningssiffra och ändå
redovisas som om den faktiskt användes.

### P2 — beställt permanent browser-/E2E-bevis saknas

Commit `3502639` ändrar bara `KalkylatorPage.tsx` och jsdom-testfilen. Sessionsloggen säger
uttryckligen att Chromiumproven kördes som temporära script och inte committades. Det
befintliga `e2e/kalkylator.smoke.mjs` provar fortfarande bara två giltiga scenarier och
kan därför inte upptäcka att `noValidate` åter öppnar en invalid-submit-regression.

Lägg de kritiska fallen i den självbärande E2E-sviten med normal knappklickning. jsdom-
proven är bra komponentprov men ersätter inte det uttryckligen beställda browserbeviset.

## Bekräftade rättningar

- Riktig Chromium, MWh `-5` med giltigt antal undercentraler: svenskt fel och inget
  resultat.
- Riktig Chromium, 21 undercentraler: svenskt fel och inget resultat.
- Riktig Chromium, levande Sandviken med 2 kW: ”Värdet är för lågt.”,
  `aria-invalid="true"`, `aria-describedby="kapacitetKw-fel"` och inget resultat.
- En giltig riksgenomsnittsberäkning i MWh-läge är fortsatt grön i komponenttestet.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **507 passed**.
- `npm test -- --run`: **21 testfiler, 572 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: godkänd för de två befintliga giltiga scenarierna; sviten saknar
  fortsatt invalid-submit-fallen, `dist` återställd.
- Egna Chromiumprov bekräftade de tre rättade fallen och reproducerade de två kvarvarande
  P1-fallen ovan.
- `git diff --check` är rent och produktrepona är rena. Sedan tidigare orelaterade filer
  i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Gör rättningsrunda 6 utan att ändra tariffmotorernas avsiktliga skydd för direkta anrop:

1. Ersätt `parseInt`-valideringen av undercentraler med en gemensam, validerad numerisk
   representation som kräver ändligt heltal 1–20. `1.5`, 0 och 21 ska stoppas; giltiga
   gränser 1 och 20 ska räknas och redovisas med samma värde.
2. Validera varje ifyllt `valdIndatafalt` mot dess `min_varde`, `max_varde` och `heltal`
   före beräkning. Lägg komponentprov för minst Göteborg `avvikelse_c=999` och ett
   `heltal=true`-fält med decimal; båda ska ge synligt svenskt fel och inget resultat.
3. Inventera återstående numeriska huvudformsfält (`area`, MWh, kr, eget energipris och
   kapacitet) och gör HTML-attribut och JS-/domänregler medvetet samstämmiga. Om decimaler
   är giltiga, sätt ett uttryckligt lämpligt `step`; om heltal krävs, validera det. Lägg en
   tabellstyrd komponentmatris för gränserna så att ”fullt formulärkontrakt” blir bevisat,
   inte bara beskrivet i kommentar.
4. Utöka det committade `e2e/kalkylator.smoke.mjs` med normal knappsubmit för minst
   negativ MWh, `1.5` undercentraler, ett utanför-gräns-fakturafält och Sandviken 2 kW.
   Ogiltiga fall ska ge inget resultat; Sandviken ska dessutom ge den svenska fälttexten
   och korrekta ARIA-attribut.

Kör hela Python-/TypeScriptmatrisen, `tsc --noEmit`, bygge, självbärande E2E och
`git diff --check`. Gör en fokuserad lokal commit och rapportera exakta HEAD-hashar.
Aktivera ingen tariff, ändra inte 7/57/28 och pusha inget repo. Stanna därefter för ny
Codex-omgranskning.
