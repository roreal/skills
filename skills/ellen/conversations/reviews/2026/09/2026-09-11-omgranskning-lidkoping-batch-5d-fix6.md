---
review_id: "2026-09-11-003"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 6"
  - "Samtliga P1/P2-krav i granskning 2026-09-11-002"
reviewed_heads:
  skills: "6760da167fb7214560292222febc0a7ab072ac2b"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "0ed23b37cf38d0caf65d2f4f92fbbe4a658f7f0e"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-11-002"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 6

## Beslut

**Changes required.** Rättningsrunda 6 stänger de två tidigare P1-felen: undercentraler
trunkeras inte längre och fakturafält inom den normala numeriska representationsvägen
valideras mot prispostens metadata före slutresultat. Det permanenta browserbeviset är nu
incheckat och samtliga sex E2E-scenarier passerar.

Den uttryckligen beställda synkroniseringen av **alla** numeriska huvudformsfält är dock
inte färdig. `step="any"` har lagts till, men HTML:s `min=1` och JavaScripts gräns `>0`
är fortfarande olika för area och MWh. Den beställda tabellstyrda komponentmatrisen för
area/MWh/kr/eget pris/kapacitet saknas helt. Global `noValidate` gör avvikelserna
funktionella: HTML-ogiltiga värden kan fortfarande ge ett färdigt resultat.

Ingen tariff är aktiverad och inget repo är pushat. Produktionsurvalet är fortsatt sju
tariffer och dispositionen 7 implementerade / 57 redo / 28 blockerade av 92 är
oförändrad.

## Fynd

### P2 — HTML- och JS-gränserna är fortfarande osynkroniserade

Codex reproducerade två fall i riktig headless Chromium mot `neptune_academy@0ed23b3`:

- `area=0.5`: fältet har `min=1` och `checkValidity() === false`, men normal knappklickning
  gav inget fel och renderade ett resultat;
- `area=10`, MWh-läge och `energyMwh=0.5`: även detta fält har `min=1` och
  `checkValidity() === false`, men knappklickningen gav inget fel och renderade ett
  resultat.

Orsaken är att JS fortsatt bara avvisar `area <= 0` respektive `rawEnergy <= 0`.
`step="any"` gör decimaler över och under 1 steg-giltiga, men ändrar inte `min=1`.
Samma kodgranskning visar motsvarande kontraktsfråga för `energyKr` och
`energyPriceCustom` (`min=1` i HTML, bara `>0` i JS), medan ett icke-kontraktsgatat
`kapacitetKw` har `min=0` i HTML men den nya JS-kontrollen kräver ett positivt heltal.

Det är acceptabelt att besluta att positiva decimaler under 1 är giltiga eller att
gränsen är 1 — men HTML, JavaScript, feltext och test måste ange samma sak. Nu gör de inte
det.

### P2 — den beställda numeriska komponentmatrisen saknas

Rättningsinstruktionen krävde en tabellstyrd komponentmatris för `area`, MWh, kr, eget
energipris och kapacitet. Diffen lägger fem testfall, men de gäller bara `1.5`
undercentraler, undercentralsgränsen 20 och tre fakturafältsfall. Ingen assertion provar
de nya `step="any"`-attributen eller JS-/HTML-gränserna för de fem namngivna fälten.

Utan matrisen upptäcker sviten inte de två Chromiumfallen ovan. Lägg verkliga
komponent-submitprov för beslutad nedre gräns, ett värde precis under den och ett giltigt
decimalvärde där decimaler stöds. Kapacitet ska dessutom täcka 0, decimal och positivt
heltal i både legacy- och kontraktsgatad väg.

### P2 — icke-ändligt fakturavärde kan fortfarande behandlas som tomt

Valideringen itererar över `faltForBerakning`, som redan har filtrerat bort allt som inte
är ändligt. I Chromium gav `avvikelse_c=1e999` ett nummerfält med
`validity.badInput === true`, tomt DOM-värde och inget fel; normal knappklickning gav ett
resultat med tariffens standardvärde. Med `noValidate` måste bad-input-status antingen
fångas via formulärkontrollens `validity` eller förhindras genom en annan lösning. Det
räcker inte att kontrollera bara värden som överlevt filtret.

Fakturafältskontrollen ligger dessutom efter kr-lägets anrop till
`rawEnergyFranArskostnad`, som redan konsumerar `faltForBerakning`. Flytta kontrollen före
varje beräkningskonsument så att ”valideras före beräkning” gäller även kroninversen.

## Bekräftade rättningar

- `parsaHeltal` använder `Number`, ändlighetskontroll och `Number.isInteger`; 1,5
  undercentraler stoppas och 20 redovisas/räknas konsekvent.
- Ifyllda, representerbara fakturatal kontrolleras mot `min_varde`, `max_varde` och
  `heltal`, med svensk fälttext och korrekta ARIA-attribut. Göteborgs `999 °C` stoppas.
- Kapacitetsfältet har nu en explicit positiv-heltalskontroll i JS.
- `step="any"` är infört för area, MWh, kr och eget energipris, vilket löser den tidigare
  implicita heltalsstegregeln för decimaler som ligger inom tillåtet intervall.
- `e2e/kalkylator.smoke.mjs` innehåller nu sex permanenta scenarier. De fyra nya provar
  negativ MWh, 1,5 undercentraler, Göteborg 999 °C och Sandviken 2 kW via normal
  knappklickning mot en riktig produktionsbuild.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **507 passed**.
- `npm test -- --run`: **21 testfiler, 577 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: **alla sex scenarier passerade** mot en ny produktionsbuild;
  `dist` återställd.
- Egna Chromiumprov bekräftade de levererade rättningarna och reproducerade area/MWh-
  avvikelserna samt `validity.badInput`-fallet ovan.
- `git diff --check` är rent och produktrepona är rena. Sedan tidigare orelaterade filer
  i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Gör rättningsrunda 7, begränsad till det kvarvarande numeriska formulärkontraktet:

1. Definiera en entydig nedre gräns för `area`, `energyMwh`, `energyKr` och
   `energyPriceCustom`, och använd samma gräns i HTML, JS och svensk feltext. Sätt
   icke-kontraktsgatad kapacitets `min` i linje med dess positiva-heltalsregel.
2. Validera fakturafältens råa/bad-input-status och metadata före **alla** konsumenter,
   inklusive `rawEnergyFranArskostnad` i kr-läget. Ett icke-ändligt/bad-input-värde får
   inte omtolkas som tomt och falla tillbaka på standardvärde.
3. Lägg den redan beställda tabellstyrda komponentmatrisen för area, MWh, kr, eget pris
   och kapacitet: under gräns, exakt gräns och giltig decimal där decimaler tillåts;
   kapacitet även 0/decimal/heltal i legacy- och kontraktsgatad väg. Assert både
   HTML-attribut/`checkValidity()` och normal `requestSubmit()`-utfall.
4. Utöka E2E med minst ett av de hittills otäckta under-1-fallen och ett bad-input-fall
   om browsern kan representera det stabilt. Bevara samtliga sex befintliga scenarier.

Ett säkrare alternativ till fortsatt dubblering är att behålla native validering för
övriga kontroller och använda ett riktat `onInvalid` för kapacitet; permanent Chromium-
E2E finns nu och kan vara sanningskälla även om jsdom inte modellerar alla invalid-event
perfekt. Oavsett implementation ska ovanstående observerbara kontrakt uppfyllas.

Kör hela Python-/TypeScriptmatrisen, `tsc --noEmit`, bygge, självbärande E2E och
`git diff --check`. Gör en fokuserad lokal commit och rapportera exakta HEAD-hashar.
Aktivera ingen tariff, ändra inte 7/57/28 och pusha inget repo. Stanna därefter för ny
Codex-omgranskning.
