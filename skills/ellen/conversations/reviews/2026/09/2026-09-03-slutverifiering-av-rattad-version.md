---
review_id: "2026-09-03-004"
date: "2026-09-03"
reviewer: Codex
status: completed
scope:
  - Claudes rättningar efter verifiering 003
  - enkey-agents prisårsgrind
  - neptune_academy kalkylatorns felhantering och kronor-invers
reviewed_heads:
  enkey-agents: "545f1e0"
  neptune_academy: "ce47d58"
remote_verified: true
---

# Slutverifiering av rättad version

## Bedömning

Den rättade versionen fungerar i den nuvarande webbprodukten och jag hittar
inget nytt lanseringsblockerande fel i ändringarna. Det tidigare dolda
fixpunktsfelet visas nu som ett tydligt formulärfel utan ohanterat
webbläsarfel. Prisårsgrinden accepterar bara 2026, och Gotlands krav på
föregående kalenderårs MWh finns nu även i TypeScripts domännära
fjärrvärmewrapper.

Två av verifiering 003:s fynd är därmed helt stängda. Det tredje är stängt
för React-flödet och den rekommenderade TypeScript-wrappern, men inte för
alla lågnivågränssnitt: Pythons publika `mwh_fran_arskostnad` och
TypeScripts lägre `mwhFranArskostnad` behåller uttryckligen approximationen
när fältet saknas. Det är dokumenterat och påverkar inte dagens webbflöde,
men är fortfarande en kontraktsrisk för en framtida direktintegration från
Ellen.

## Bekräftade rättningar

### P1 stängd — fixpunktsfelet är synligt och handlingsbart

`KalkylatorPage` fångar nu alla avsiktliga `Error` från fjärrvärmens
kronor-väg och använder motorns feltext när det specialiserade
kapacitetsmeddelandet inte matchar:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:273`

Det tidigare reproduktionsfallet kördes om med Playwright: Göteborg Energi,
10 000 m², 1 000 000 kr/år och ingen debiterbar effekt. Resultatet blev ett
synligt `role="alert"` med instruktion att ange debiterbar effekt, inget
resultat och inget `pageerror` eller konsolfel. Gotlands MWh-läge och
kronor-läget med ett ifyllt föregående-årsvärde fortsatte samtidigt att ge
resultat.

### P2 stängd — prisåret måste vara exakt 2026

Kataloggrinden jämför nu `price_year` med heltalet 2026:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:227`

Regressionstestet binder `2025`, `2027`, strängen `"2026"`, `True` och
`-1` som ogiltiga värden:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/tests/test_katalog.py:288`

### P2 stängd i produktvägen — Gotlandskravet finns i TypeScript-domänen

`mwhFranArskostnadForFjarrvarme` kontrollerar nu tariffens deklarerade
indatafält och kastar ett tydligt domänfel när
`foregaende_ars_mwh` krävs men saknas:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts:262`

Tre nya enhetstester verifierar saknat värde, explicit värde och en tariff
som inte har kravet:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.test.ts:474`

`rawEnergyFranArskostnad` anropar denna wrapper, så både den domännära
funktionen och React-sidan är skyddade. Webbläsartestet bekräftade dessutom
att Gotland taxa 21 utan fältet stoppas med ett begripligt formulärfel och
att samma beräkning fungerar när fältet fylls i.

## Kvarstående, inte lanseringsblockerande

### P2 — Python- och lågnivåinverserna kräver fortfarande inget explicit val

Pythons `mwh_fran_arskostnad` använder fortfarande årets prövade energi som
fallback när `falt.foregaende_ars_mwh` saknas. Beteendet är dokumenterat och
testas uttryckligen:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:795`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/tests/test_invers_tvetydighet.py:133`

Det är acceptabelt som ett medvetet lågnivåbeteende för nuvarande produkt,
men formuleringen att "varje anropare" är skyddad gäller bara anropare av
TypeScript-wrappern. Innan Ellen eller ett API använder Pythonmotorn direkt
bör motsvarande domännära wrapper införas där, alternativt bör
approximationen kräva ett explicit opt-in.

### Testskuld — UI-regressionen är verifierad manuellt men inte permanent

De tre nya Vitest-testerna täcker motorgränsen, men det finns fortfarande
inget komponent- eller incheckat Playwright-test som binder att
`KalkylatorPage` visar icke-konvergensfelet och inte skapar ett `pageerror`.
Den manuella Playwright-verifieringen är grön i denna granskning, men ett
permanent test skulle hindra att just den tidigare P1-regressionen kommer
tillbaka.

## Verifiering

- `enkey-agents` tariffsvit: 176 tester godkända.
- `enkey-agents` bredare relevanta svit: 223 tester godkända.
- `neptune-marketing`: 217 tester godkända.
- TypeScript: `npx tsc --noEmit` godkänd.
- Produktionsbygge: `npm run build` godkänt; endast den befintliga
  bundle-storleksvarningen rapporterades.
- Riktade Playwright-fall: Göteborgs icke-konvergens, Gotlands spärr,
  Gotland med explicit föregående-årsvärde och Gotlands MWh-läge godkända.
- `git diff --check` för rättningscommitten gav inga whitespace-fel.
- `enkey-agents` HEAD `545f1e0` matchar GitHubs `origin/main`.
- `neptune_academy` HEAD `ce47d58` matchar GitHubs `origin/main`.
- Båda implementationsrepona var rena efter tester och återställning av
  genererade `dist`-filer.

Inga implementationsfiler ändrades under verifieringen.
