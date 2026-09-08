---
review_id: "2026-09-03-003"
date: "2026-09-03"
reviewer: Codex
status: completed
scope:
  - Claudes slutrapport efter omgranskning 002
  - enkey-agents tariffmotor
  - neptune_academy kalkylator och kronor-flöde
reviewed_heads:
  enkey-agents: "37dd7cd"
  neptune_academy: "4777176"
remote_verified: true
---

# Verifiering av Claudes slutrapport

## Bedömning

Slutrapportens huvuduppgifter stämmer. Gotlands taxa 21 stoppas nu i
kalkylatorns kronor-läge när föregående kalenderårs MWh saknas, ett ifyllt
värde ger resultat och MWh-läget påverkas inte. Texten om standardvärden är
rättad, MWh-värdet följer med i energikällan, och valuta samt saknat prisår
stoppas i kataloggrinden. De rapporterade commit-id:na ligger på GitHubs
`origin/main`.

Testningen hittade dock ett separat P1-fel i samma kronor-flöde: för vissa
helt rimliga belopp ger den befintliga fixpunktslösaren avsiktligt upp med
ett begripligt domänfel, men sidan kastar felet vidare i stället för att
visa det. Jag ser också två mindre kontraktsluckor: prisåret valideras bara
med sanningsvärde och Gotlands nya krav finns bara i React-sidan, inte i de
exporterade motorgränssnitten.

## Fynd

### P1 — Förväntade fixpunktsfel blir osynliga sidfel i kronor-läget

När debiterbar effekt saknas försöker
`mwhFranArskostnadForFjarrvarme` lösa det cirkulära sambandet mellan energi
och uppskattad kapacitet. Om loopen inte konvergerar inom 20 varv kastar den
ett avsiktligt och handlingsbart fel som säger att användaren ska ange
debiterbar effekt:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts:303`

Kalkylatorsidan översätter däremot bara fel som matchar
`kapacitetsfelText`. Alla andra motorfel kastas vidare ur submit-hanteraren:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:263`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:1014`

Reproducerat end-to-end med Playwright:

1. Area 10 000 m², fjärrvärme och Göteborg Energi.
2. Välj kronor per år och ange 1 000 000 kr.
3. Lämna debiterbar effekt tom och beräkna.

Resultatet blir ingen resultatvy och inget `role="alert"`. Webbläsaren
rapporterar i stället ett ohanterat `pageerror` med motorns text om att
fixpunktsloopen inte konvergerade. Formuläret ligger kvar och ser ut som om
knappen inte gjorde något.

Ett direkt test av motorn över en kostnadsserie visade samma fel för
Göteborg vid 1,0, 1,5, 2,0, 3,0 och 5,0 miljoner kr samt för Mölndal vid
1,5, 2,0 och 5,0 miljoner kr. Det är alltså inte ett enstaka syntetiskt
hörnfall. Rundturer som började med en beräknad 500 MWh-faktura fungerade
däremot för samtliga sju leverantörsalternativ.

Rekommendation: använd typade domänfel och visa åtminstone
icke-konvergensfelet i `formError`, med fokus på fältet för debiterbar
effekt. Lägg ett komponent- eller Playwright-test som kräver synligt fel och
inget ohanterat `pageerror`. På längre sikt bör man pröva om den sammansatta
energi/kapacitetsfunktionen kan lösas robustare än med dagens fixpunktsloop.

### P2 — Prisårsgrinden accepterar godtyckliga sanningsvärdiga värden

Den nya kontrollen är:

```python
if not tariff.get("price_year"):
    return "saknar prisår"
```

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:219`

Det stoppar `None`, saknad nyckel och noll, vilket slutrapporten uttryckligen
lovar. Men ett riktat prov visar att `2025`, `2027`, strängen `"2026"`,
`True` och `-1` alla passerar `grind()`. Testet binder bara `None`:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/tests/test_katalog.py:278`

Eftersom samma tariff samtidigt måste ha
`price_status="published_2026"` bör prisåret vara ett heltal som
överensstämmer med statusens år, inte bara ett värde som är sant i Python.

Rekommendation: kräv för dagens katalog `type(price_year) is int and
price_year == 2026`, eller härled tillåtet år från en versionssatt status.
Bind fel år, sträng, booleskt värde och negativt år i parametriserade tester.

### P2 — Gotlands nya krav skyddar UI:t men inte de exporterade motoranropen

Spärren ligger i `KalkylatorPage.handleCalculate` och är korrekt för dagens
webbflöde:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:231`

`rawEnergyFranArskostnad`, `mwhFranArskostnadForFjarrvarme`, TypeScripts
lägre invers och Pythons `mwh_fran_arskostnad` accepterar fortfarande en
Gotlandstariff utan `foregaende_ars_mwh`. Då återkommer exakt den
självrefererande approximation som gav föregående gransknings felvärden.

Detta påverkar inte den nuvarande React-sidan, men domäninvarianten kan
kringgås av ett annat UI, ett API eller den planerade Ellen-integrationen.

Rekommendation: flytta eller duplicera kravet i den domännära wrappern och
returnera ett typat fel när tariffen har `volume_discount` men basfältet
saknas. Om låg-nivåfunktionen ska behålla approximationen bör det krävas ett
explicit val, inte aktiveras av ett utelämnat argument.

## Bekräftade delar av slutrapporten

- Gotland taxa 21 utan föregående-årsvärde ger nu ett tydligt formulärfel i
  kronor-läget och visar inget resultat.
- Samma flöde ger resultat när föregående-årsvärdet fylls i.
- Gotlands MWh-läge fungerar utan att fältet görs obligatoriskt.
- Samtliga sju leverantörsalternativ klarade en MWh → beräknad faktura →
  kronor → MWh-rundtur i den riktade webbläsarkontrollen; taxa 21 fick då
  ett explicit föregående-årsvärde.
- Formulärtexten använder nu "neutralt eller härlett standardvärde".
- MWh-lägets energikälletext innehåller den numeriska energin.
- Kontaktunderlaget redovisar statiska defaulttal och markerar dynamiska
  värden som härledda.
- `currency` måste nu vara exakt `SEK`; saknat eller falskt `price_year`
  avvisas.

## Verifiering

- `enkey-agents` tariffsvit: 175 tester godkända.
- `enkey-agents` bredare relevanta svit (`tests` och
  `tools/tariffer/tests`): 222 tester godkända.
- `neptune-marketing`: 214 tester godkända.
- TypeScript: `npx tsc --noEmit` godkänd.
- Produktionsbygge: `npm run build` godkänt; bara den befintliga varningen
  om en stor JavaScript-bundle rapporterades.
- Riktade Playwright-tester kördes mot den lokala Vite-applikationen.
- `enkey-agents` HEAD `37dd7cd` matchar GitHubs `origin/main`.
- `neptune_academy` HEAD `4777176` matchar GitHubs `origin/main`.
- Båda implementationsrepona var rena efter tester och återställning av
  genererade `dist`-filer.
- Inga implementationsfiler ändrades under verifieringen.

Ett helt ospårat `pytest` från repositoryroten är inte grönt i den här
miljön: insamlingen stannar på 13 befintliga Milesight-fel, främst saknat
`pymodbus` och importkrockar för `tests.*`. Det påverkar inte de 175
tarifftesterna eller de 222 uttryckligen valda relevanta testerna, men
innebär att "hela Python-repositoryt är grönt" inte är verifierat.

## Fortsatt öppet enligt slutrapporten

Följande är korrekt redovisade som uppskjutna och betraktas därför inte som
nya upptäckter i denna verifiering:

- strukturerade datakvalitetsorsaker och korrekta etiketter för varje väg,
- återstående enhets-, formel- och periodfält i kataloggrinden,
- tariff-id/version och källmarkering per fält i kontaktunderlaget,
- spårbar validering av `NaN`, okända nycklar och klampad direktindata.

Det separata säkerhetsfyndet om den tidigare pushade autentiseringsuppgiften
kvarstår tills uppgiften har roterats och historiken hanterats enligt en
godkänd plan.
