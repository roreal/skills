---
review_id: "2026-09-04-010"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit 8ea1fbb
  - neptune_academy commit 1082bd8
  - rättningar efter granskning 2026-09-04-009
reviewed_heads:
  enkey-agents: "8ea1fbb"
  neptune_academy: "1082bd8"
implementation_changed: false
push_status: local-unpushed
---

# Omgranskning av policybindning och produktgrind

## Bedömning

Claude har nu rättat datum-, kvalitets- och numerikfynden korrekt. Bindningen har också
flyttats från varje beräkningsanrop till `Tariffpolicy`, och odeklarerade extrafält kan inte
längre påverka `falt`. De ordinarie testsviterna, typkontrollen och produktionsbygget är gröna.
Inga riktiga tariffer eller policyer har aktiverats och committerna är lokala.

Kontrollpunkten är ändå **inte godkänd för push eller nästa tariffbatch**. Den nya bindningen
valideras bara mot att nyckeln förekommer någonstans i policyn; den kontrolleras inte mot
beräkningens omfattning, värdeform eller prisobjektets verkliga kapacitetsdel. Därför kan ett
`exact/complete`-resultat fortfarande få fel eller noll kapacitetskostnad, och två andra
former kraschar först efter att statusen redan blivit `complete`. Produktgrinden är dessutom
fortfarande opt-in och hash-pinnen synkroniserar inte två oberoende repon.

## Fynd

### P1 — policybindningen kan fortfarande nollställa eller krascha kapacitetsdelen

`Tariffpolicy.__post_init__`/`skapaTariffpolicy` kräver bara att
`kapacitet_bindning`/`kapacitetBindning` finns bland samtliga kravnycklar
(`resultatkontrakt.py:162–170`, `resultatkontrakt.ts:127–135`). Fasaden kontrollerar inte att
bindningen är relevant för årsberäkningen eller att ett prisobjekt med kapacitetspris faktiskt
har en bindning. Den förutsätter dessutom att en validerad kapacitet aldrig är en serie, trots
att statusfunktionen uttryckligen tillåter serier för rullande fält.

Codex reproducerade tre fall på `8ea1fbb`; TypeScript-spegeln har samma kontrollordning:

```text
prisobjekt med 100 kr/kW/år + annual effekt=50 + kapacitet_bindning=None
=> exact/complete, fast kostnad 0 kr

kapacitet_bindning pekar på ett krav som bara gäller monthly, annual-indata saknas
=> annual exact/complete; fasaden kraschar därefter med KeyError("effekt")

rullande annual kapacitetsfält med en validerad serie om 12 tal
=> snapshot/complete; fasaden kraschar därefter med TypeError vid float(list)
```

Det första fallet finns till och med som ett positivt regressionstest mot ett prisobjekt som
har en riktig kapacitetsnivå (`test_resultatkontrakt.py:368–376` och TypeScript rad 294–300).
Testets antagande att `None` alltid betyder ett medvetet "ingen kapacitetsdel" stämmer inte
med prisobjektet som faktiskt prissätts. För övriga relevanta fält hoppas en serie tyst över
när `falt` byggs, trots att statusen kan vara `complete` (`resultatkontrakt.py:360–364`).

**Begärd rättning:**

1. Gör kapacitetsrollen explicit, utan ett tvetydigt standard-`None`/`undefined`: antingen en
   namngiven årsrelevant kravnyckel eller en uttrycklig `not_applicable`-variant.
2. Jämför rollen mot `prisar` i fasaden. Ett prisobjekt med kapacitetsnivå/formel måste ha en
   kapacitetsbindning; `not_applicable` får bara användas när prisobjektet saknar
   kapacitetskomponent.
3. Kräv att bindningens `KravPost` gäller `annual` före årsberäkning och att det faktiska
   motorvärdet är skalärt. En serie utan implementerad reduceringsregel ska ge `blocked` eller
   ett tydligt strukturfel före `complete`, aldrig hoppas över eller krascha efter statusen.
4. Modellera motorfält som uttryckliga, namngivna bindningar i stället för att implicit skicka
   alla skalära årsrelevanta krav. Då kan metadatafält och framtida serier inte oavsiktligt
   blandas ihop med motorns `falt`.
5. Lägg de tre reproduktionerna ovan samt ett serieformat `falt` i båda språkens tester.

### P1 — `contract_required` är fortfarande ett frivilligt fält, inte en aktiveringsgrind

`till_prisar` kopierar nu ett sanningsvärdigt `contract_required` till
`_kraver_kontrakt`, vilket är användbar plumbing. Men ingen katalogpost har fältet, ingen
policyregistry finns och ingen generator- eller produktväg kräver att fältet finns för de nya
tarifferna. Om det glöms bort utelämnar `till_prisar` uttryckligen spärren och råmotorn fortsätter
att fungera (`katalog.py:610–626`; det beteendet testas positivt i
`test_resultatkontrakt.py:513–535`). `grind()` validerar inte heller fältets typ eller koppling
till en komplett `Tariffpolicy`.

Passersedeln minskar risken för ett oavsiktligt `True`, men är inte modulprivat i TypeScript:
`KONTRAKT_PASSERSEDEL` exporteras från `fjarrvarme.ts:178` och används som ett vanligt publikt
argument på `arskostnad`. I Python kan motsvarande understrukna singleton också importeras.
Det är en internkonvention, inte den begärda strukturella produktgrinden.

**Begärd rättning:** lägg ett tariff-ID-indexerat policyregister i katalog-/generatorflödet.
En tariff som hör till den nya kontraktsstyrda gruppen ska avvisas av aktiveringsgrinden om
`contract_required is not True`, komplett policy saknas eller tariff-ID:n inte matchar.
Generatorn ska bära både markör och policy till TypeScript. Lägg ett end-to-end-test från
katalogfixture via grind/generator till den publika beräkningsentryn. Flytta den ovaktade
motorn och passersedeln bakom en verkligt intern modulgräns eller samlokalisera fasaden med
den privata motorfunktionen, så konsumenter inte får ett exporterat bypassargument.

### P2 — två lokala hash-pinnar kan fortfarande glida isär med gröna tester

De två fixturekopiorna är byte-identiska nu (`sha256
089d812e289e3b2471318d3b64001d4274a08afcd28ee0eb99a530dd6187707f`). Men varje repo
jämför bara sin egen fixture mot sin egen hårdkodade konstant. Om Pythonfixturen och dess
Pythonkonstant ändras tillsammans passerar Python; den gamla TypeScriptfixturen och dess gamla
TypeScriptkonstant passerar samtidigt där. Ingen testprocess ser att de två gröna hashvärdena
är olika. Den enda verkliga korsrepojämförelsen är fortfarande hemkatalogbunden och hoppas
över när sidorepot saknas.

**Begärd rättning:** använd en gemensam kanonisk artefakt eller en CI-kontroll som faktiskt
checkar ut och jämför båda repona, där saknad motpart är ett fel. Alternativt dokumentera den
lokala direkta jämförelsen som en utvecklarhjälp och flytta den verkliga konformitetsgarantin
till ett gemensamt, versionsstyrt testpaket. Två oberoende konstanter ska inte kallas
synkspärr.

## Godkända delar i denna runda

- endast policydeklarerade årsrelevanta skalärfält kan nu nå `falt`,
- `NaN`, oändlighet, bool, sträng och tom/icke-numerisk serie avvisas,
- TypeScript avvisar nu omöjliga kalenderdatum på samma sätt som Python,
- endast `verified` kan bidra till `exact`; saknad/`unverified` kvalitet ger högst `snapshot`,
- en enkel boolesk bypass stoppas,
- `not_applicable`- och tidigare tariffmotorändringar är fortsatt regressionsgröna,
- inga tariffposter, policyinstanser eller genererade produktdata har aktiverats.

## Avgränsad rättningsbeställning till Claude

Rätta endast grundetappen och håll commitserierna lokala:

1. stäng de tre kapacitetsbindningsfallen och tyst bortfall av serieformat motorfält,
2. gör kontraktskravet obligatoriskt och tariff-ID-kopplat i aktiverings-/generatorgrinden,
3. ersätt den exporterade bypassvägen med en intern motorgräns,
4. inför en verklig korsrepo- eller kanonisk fixturesynk,
5. kör hela Python- och TypeScript-sviten, `tsc --noEmit`, produktionsbygget och nya negativa
   end-to-end-tester.

Aktivera inga tariffer och rör inte Familj 4, Telge, E.ON/Navirum, Sundsvall Matfors eller
Vattenfall. Redovisa nya lokala commit-hashar och invänta ny Codex-kontroll före push.

## Utförda kontroller

- `enkey-agents@8ea1fbb`: 266/266 tariff-pytest passerar i projektets `.venv`.
- `neptune_academy@1082bd8`: 292/292 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda committerna.
- Båda implementationsarbetskopiorna är rena; committerna är lokala och opushade.
- Fixturekopiorna och deras lokala hashkonstanter matchar i Roberts nuvarande klonlayout.
- Riktade Pythonanrop reproducerade nollkostnad utan bindning, årsbindning mot endast
  månadsrelevant krav samt serieformad kapacitetsbindning.
- Sökning utanför tester bekräftade att ingen faktisk katalogpost, policyregistry, generator-
  eller produktkonsument ännu upprätthåller `contract_required`.

Codex ändrade ingen implementation, tariffdata, commit eller push under granskningen.
