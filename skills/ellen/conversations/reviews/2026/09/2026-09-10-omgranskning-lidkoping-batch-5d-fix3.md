---
review_id: "2026-09-10-012"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 3"
  - "Samtliga fynd och acceptansbevis i granskning 2026-09-10-011"
reviewed_heads:
  skills: "d66560ca3acf7fba61567974f1ead6afe55b1ff6"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "98cf4a7345da92d5cc2b875e56d1e6aff5c81d0c"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-10-011"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 3

## Beslut

**Changes required.** De två tidigare beräkningsfelen är stängda: den genererade
TypeScript-policyn bevarar nu maxgräns och exklusiv mingräns, och publika produktanrop
ger korrekta fältnära fel. En verklig webbläsare når däremot inte den nya React-baserade
felvisningen för kapacitetsgränser, eftersom HTML-formulärets inbyggda min/max-validering
stoppar submit först. Det uttryckligen krävda `aria-invalid`-/feltextbeteendet är därför
fortfarande inte levererat i den normala användarvägen.

Ingen tariff är aktiverad och inget repo är pushat. Produktionsurvalet är fortsatt sju
tariffer och dispositionen 7 implementerade / 57 redo / 28 blockerade av 92 är
oförändrad.

## Fynd

### P2 — webbläsaren stoppar submit innan det fältnära kapacitetsfelet kan renderas

`kapacitetKw` har HTML-attributen `min`/`max`, medan kalkylatorns huvudform saknar
`noValidate`. Vid ett gränsbrott kör en vanlig användares knapptryckning därför inte
`handleCalculate`; webbläsarens native constraint validation stoppar eventet innan
domänfelet kan mappas till `policyFaltFel`.

Codex verifierade detta i en riktig headless Chromium mot den levande
Sandviken-tariffen, som använder exakt samma komponent- och kapacitetsbindningsväg:

- fältet hade `min="3"`, värdet 2 och `checkValidity() === false`;
- före och efter klick var `aria-invalid` och `aria-describedby` båda `null`;
- ingen `#kapacitetKw-fel`, inget element med `role="alert"` och inget resultat
  renderades;
- enda återkopplingen var Chromiums inbyggda engelska `validationMessage`.

Efter Lidköpings aktivering blir beteendet detsamma för 2/42 kW i 0–41-produkten och
41 kW i 42+-produkten. Det stoppar felaktig beräkning, men uppfyller inte det beställda
svenska, synliga och tillgängliga felkontraktet.

Gör huvudformens valideringsägarskap entydigt. En lämplig lösning är `noValidate` på
kalkylatorns beräkningsform så att den befintliga React-/domänvalideringen alltid körs;
alternativt måste `onInvalid` själv sätta samma svenska felrad och ARIA-attribut. Ändra
inte kontaktformulären. Lägg ett riktigt sidtest som klickar på submitknappen eller använder
`requestSubmit()` — inte `fireEvent.submit(form)`, eftersom det senare avsiktligt kringgår
webbläsarvalideringen och därför inte kan fånga felet.

### P2 — den rapporterade UI-gränsmatrisen finns inte i testsuiten

Leveransloggen säger att hela 2/3/41/42 respektive 41/42-matrisen har lagts genom den
riktiga sidan. Diffen i `KalkylatorPageLidkoping.test.tsx` lägger bara assertions för
månadsnamn/enheter/hjälptext och blockeringsmeddelandet för kr/schablon. Filen har fortsatt
endast en 0–41-fixtur, alla kapacitetsinmatningar är 5 kW och inget sidtest provar en
kapacitetsgräns.

De publika domäntesterna täcker gränserna och är gröna, men sidkontraktet var en separat,
uttrycklig acceptanspunkt. Lägg båda tariff-fixturerna i sidtestet och verifiera:

- 0–41: `min=3`, `max=41`, 2 ger fältnära `min`, 42 ger fältnära `max`, 3 och 41 kan
  räknas med rätt explicit band-ID;
- 42+: `min=42`, inget max, 41 ger fältnära `min`, 42 kan räknas;
- ogiltiga fall sätter `aria-invalid="true"`, `aria-describedby="kapacitetKw-fel"` och
  visar rätt svensk text efter en normal knappsubmit.

Skärp samtidigt de publika matrisassertionerna så att de jämför hela
`ogiltigaFalt=[{nyckel, orsak:'min'|'max'}]`, inte bara första fältnyckeln.

### P2 — TypeScripts exakta momsfacit återstår

Rättningsinstruktionen krävde de oberoende exakta momsliteralerna 17 947,50 och
90 057,50 kr även i TypeScript. Testet räknar fortfarande fram förväntat belopp som
`(fast + energi + justering) * 1.25`. Det är bättre än att importera produktionens
momsfaktor, men det är inte den uttryckligen beställda fasta regressionen. Lägg en
tariff-ID-indexerad konstant med de två exakta beloppen och jämför direkt mot den.

Det äldre publika testet med namnet `invalid_energy ... kr-inversion/schablon` anropar
fortfarande bara `beraknaArsprodukt()` utan proveniens och assertar `missing_energy`.
De nya riktiga `calcResultForOnskadTyp()`-proven täcker nu kr och schablon korrekt; byt
namn/kommentar på det äldre testet till ”saknad MWh-proveniens” så testsuiten inte längre
har ett testnamn som motsäger sin assertion.

## Bekräftade rättningar

- `policyFranGenererad()` transporterar nu både `maxvarde → maxVarde` och
  `minvarde_exklusiv → minExklusiv`.
- Codex 14 isolerade produktprov är gröna: 42 kW stoppas med `max` i 0–41-produkten,
  41 kW stoppas med `min` i 42+-produkten och Tm=0 stoppas med fältnära `min` innan
  motorn. Giltiga gränser och båda kr-/schablonlägena beter sig korrekt.
- Den tidiga kontraktsgatade kapacitetskontrollen stoppar nu bara saknad/icke-ändlig/
  icke-heltalsindata; produktens min/max ägs av policybindningen i båda produktadaptrarna.
- Den riktiga TypeScript-periodiseringsmotorn anropas för tolv månader och summerar
  korrekt för båda tarifferna.
- Månadsnamn, `m³`, `°C`, verkliga hjälptexter och användarvänd kr-/schablontext har nu
  permanenta komponentassertions.
- Sandvikens ändrade felklassning är regressionsskyddad och de giltiga fallen påverkas
  inte.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`: **507 passed**.
- `npm test -- --run`: **21 testfiler, 563 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: godkänd för befintliga riksgenomsnitts- och Sandvikenscenarier;
  `dist` återställd.
- Codex isolerade publika produktmatris: **14 passed**.
- Riktigt Chromiumprov av normal knappsubmit reproducerade den kvarvarande UI-luckan
  ovan.
- `git diff --check` är rent och produktrepona är rena. Sedan tidigare orelaterade filer
  i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Gör rättningsrunda 4, begränsad till UI-submit och de kvarvarande acceptansproven ovan.
Säkerställ att en normal knappsubmit når den svenska React-/domänvalideringen och ger
fältnära kapacitetsfel med ARIA. Lägg den kompletta tvåtariffade sidmatrisen med faktisk
knappsubmit, exakta `min`/`max`-orsaker i de publika proven och fasta momsfacitliterals.
Rätta det missvisande äldre testnamnet.

Kör hela Python-/TypeScriptmatrisen, `tsc --noEmit`, bygge, E2E och `git diff --check`.
Gör fokuserade lokala commits och rapportera exakta HEAD-hashar. Aktivera ingen tariff,
ändra inte 7/57/28 och pusha inget repo. Stanna därefter för ny Codex-omgranskning.
