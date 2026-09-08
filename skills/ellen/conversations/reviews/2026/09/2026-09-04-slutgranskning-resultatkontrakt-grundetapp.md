---
review_id: "2026-09-04-009"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit b4d355c
  - neptune_academy commit ee5f041
  - rättningar efter granskning 2026-09-04-008
reviewed_heads:
  enkey-agents: "b4d355c"
  neptune_academy: "ee5f041"
implementation_changed: false
push_status: local-unpushed
---

# Slutgranskning av resultatkontraktets grundetapp

## Bedömning

Claude har rättat flera av föregående rundas problem korrekt. Tariff-ID kontrolleras nu,
fria `kapacitet`/`falt`-argument är borttagna från kontraktsfasaden, rullande och
källperiodsbundna fält kan inte längre bli `exact`, Python accepterar samma råa JSON-lista
som TypeScript och `not_applicable` är stängd mot motsägande prisfält. Omfattningen är fortsatt
ren: inga tariffer eller tariffpolicyer har aktiverats och committerna är lokala.

Kontrollpunkten är ändå **inte godkänd för push eller nästa tariffbatch**. Fem P1-luckor
återstår i den centrala garantin att `exact/complete` bara får beskriva den indata som faktiskt
prissätts. En P2-lucka innebär dessutom att fixturekopiornas nya lokala synktest fortfarande
inte är en portabel eller CI-upprätthållen synkspärr.

## Fynd

### P1 — motorbindningen väljs fortfarande fritt och kan peka ut ovaliderad indata

`kapacitet_nyckel`/`kapacitetNyckel` är ett fritt anropsargument, inte en verifierad del av
`Tariffpolicy`. Fasaden kontrollerar inte att nyckeln motsvarar en relevant `KravPost`. Den
kan också utelämnas trots att policyn kräver ett effektfält. Dessutom byggs `falt` av **alla**
skalära poster i indatamappen, även extrafält som policyn aldrig har validerat
(`resultatkontrakt.py:323–337`, `resultatkontrakt.ts:305–323`).

Codex reproducerade på `b4d355c` med en komplett policy vars enda krav var
`effekt=50`:

```text
kapacitet_nyckel="annan", ovaliderat extrafält annan=100
=> exact/complete, fast kostnad 10 000 kr

kapacitet_nyckel utelämnad
=> exact/complete, fast kostnad 0 kr
```

Kontraktet validerar alltså fortfarande ett värde men kan prissätta ett annat. Samma lucka
gäller tariffspecifika `falt`.

**Begärd rättning:** gör motorbindningen till statisk, validerad policydata i stället för ett
fritt anropsval. Varje bindning ska peka på exakt en relevant kravpost med förväntad enhet och
motorroll (`kapacitet` eller en namngiven `falt`-nyckel). Bygg endast motorvärden från dessa
bundna kravposter. Avvisa saknad, extra, duplicerad eller omfattningsfrämmande bindning. Lägg
negativa tester för fel nyckel, utelämnad kapacitetsbindning och ett ovaliderat extrafält som
försöker påverka kostnaden i båda språken.

### P1 — numeriska värden valideras inte innan de märks `exact` och prissätts

`IndataPost.varde` typas men valideras inte vid körning som ändligt tal eller serie av ändliga
tal. I Python gav en obligatorisk kapacitet med `float("nan")` både
`Resultatstatus(exact, complete)` och en verklig `Kostnad` vars `fast` och `summa_inkl` var
`NaN`. TypeScript har motsvarande avsaknad av `Number.isFinite`.

**Begärd rättning:** validera varje relevant och motorbundet värde före statusbeslutet. Ett
skalärt värde ska vara ett ändligt tal (inte bool i Python); en serie ska vara icke-tom och
innehålla enbart ändliga tal. Ogiltig numerik ska kasta ett tydligt strukturfel eller ge
`blocked`, men aldrig `exact/complete`. Lägg delade vektorer för `NaN`/oändlighet där formatet
tillåter det och språkegna tester för runtimefallen.

### P1 — TypeScript accepterar omöjliga kalenderdatum som Python avvisar

Python använder `date.fromisoformat`, men TypeScript använder regex plus `Date.parse`
(`resultatkontrakt.ts:145–150`). JavaScript normaliserar flera omöjliga kalenderdatum i
stället för att avvisa dem. Codex verifierade:

```text
2026-02-29 -> 2026-03-01
2026-02-30 -> 2026-03-02
2026-04-31 -> 2026-05-01
```

Det gör att samma indata kan kasta i Python men passera datumvalideringen i TypeScript,
trots löftet om samma kontrakt i båda språken.

**Begärd rättning:** validera kalenderdatum utan normalisering, exempelvis genom att parsa
år/månad/dag och kontrollera en UTC-rundtur mot exakt ursprungsdatum. Lägg de omöjliga datumen
ovan, inklusive ett icke-skottårs 29 februari och ett giltigt skottårsdatum, i den gemensamma
konformitetsmängden.

### P1 — `unverified` och saknad kvalitet kan fortfarande ge `exact`

Allow-listan avvisar nu okända strängar, men både `None`/`null` ("inte bedömt") och det
uttryckliga värdet `unverified` behandlas på samma sätt som `verified`. Codex reproducerade
att båda ger `exact/complete` för ett annars enkelt krav. Det löser inte föregående krav att
okänd eller ej verifierbar kvalitet ska vara fail-closed eller högst en ögonblicksbild.

**Begärd rättning:** definiera kvalitetsnivåernas effekt på resultatstatus. Endast
`verified` bör kunna bidra till `exact`; `unverified` och saknad kvalitet ska ge högst
`snapshot` eller `blocked`, enligt ett dokumenterat val som speglas i båda språken och i de
delade testvektorerna.

### P1 — produktspärren är fortfarande frivillig och publikt kringgångbar

Sökning utanför tester visar fortfarande inga tariffpolicyinstanser och ingen
produktionskonsument av kontraktsfasaden. Ingen katalogpost eller generator sätter
`_kraver_kontrakt`; det är en frivillig, muterbar nyckel på prisobjektet. Den påstått interna
bypassflaggan är samtidigt ett vanligt argument på samtliga exporterade motorfunktioner
(`_via_kontraktfasad=True` i Python och `viaKontraktfasad=true` i TypeScript). Codex kunde
anropa den markerade Pythonmotorn direkt med flaggan och få en kostnad.

Testerna visar därför bara att spärren fungerar när anroparen frivilligt sätter markören och
inte frivilligt sätter bypassflaggan. De visar inte att en av de nya katalogtarifferna
maskinellt måste ha en komplett policy och gå genom fasaden.

**Begärd rättning:** gör kontraktskravet härlett och obligatoriskt i
katalog-/generator-/aktiveringsgrinden för varje tariff i den nya batchen; det får inte vara
en lös nyckel en konsument kan glömma. Gör bypassvägen modulprivat eller använd en intern
motorfunktion som bara fasaden anropar, utan en publik boolesk genväg. Lägg ett test från den
verkliga produktentryn/generatorn som bevisar att en ny tariff utan komplett policy eller
obligatorisk indata inte kan ge en kostnad. Befintliga sex legacytariffer kan fortsatt vara
uttryckligt undantagna.

### P2 — SHA-256-kontrollen är lokal och hoppas över i isolerade kloner

Fixturefilerna är byte-identiska nu (`sha256
d51c8063b3bfe61954f01502a316147a16050b8507be37e63783c57047f0ad70`). Testet söker dock
motparten via den användarspecifika sökvägen `~/Code/neptune_academy/...` och kör
`pytest.skip` när den saknas (`test_resultatkontrakt_vektorer.py:27–30, 73–84`). En vanlig CI-
körning eller annan klonlayout kan därför godkänna en ändrad Pythonfixture utan att
TypeScriptkopian finns eller jämförs. Kopieringen är fortfarande manuell.

**Begärd rättning:** välj en kanonisk fixture med deterministisk generering/kopiering, eller
lägg en gemensam CI-kontroll som checkar ut båda repona och där saknad motpart är ett fel.
Repoernas ordinarie tester ska vara portabla och inte bero på Roberts hemkatalog.

## Godkända delar i denna runda

- tariff-ID kontrolleras före beräkning,
- fria separata `kapacitet`/`falt`-värden är borttagna,
- rullande eller källperiodsbundna fält får högst `snapshot`,
- rå JSON-lista och Python-tuple behandlas lika strukturellt,
- `not_applicable` avvisar samtidiga kapacitetsprisfält och översätter inga band,
- `giltig_fran` och `giltig_till` beaktas; okända kvalitetssträngar blockeras,
- inga tariffer eller tariffpolicyer har aktiverats.

## Avgränsad rättningsbeställning till Claude

Rätta endast grundetappen och håll commitserierna lokala:

1. flytta motorbindningen från fritt anropsargument till validerad policy och använd endast
   bundna, relevanta kravposter,
2. validera ändlig numerik och kvalitetens faktiska statusverkan,
3. gör ISO-datumvalideringen kalenderriktig och identisk i Python/TypeScript,
4. gör produktspärren obligatorisk via katalog/generator/produktentry och ta bort publik
   boolesk bypass,
5. ersätt den hemkatalogbundna, hoppbara fixturekontrollen med en portabel deterministisk
   synk-/konformitetsmekanism,
6. kör hela Python- och TypeScript-sviten, `tsc --noEmit`, produktionsbygget och nya negativa
   integrationstester.

Aktivera inga tariffer och rör inte Familj 4, Telge, E.ON/Navirum, Sundsvall Matfors eller
Vattenfall. Redovisa nya lokala commit-hashar och invänta en ny Codex-kontroll före push.

## Utförda kontroller

- `enkey-agents@b4d355c`: 239/239 tariff-pytest passerar i projektets `.venv`.
- `neptune_academy@ee5f041`: 268/268 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda committerna.
- Båda implementationsarbetskopiorna är rena; committerna är lokala och opushade.
- Fixturekopiornas SHA-256 är identisk i Roberts nuvarande klonlayout.
- Riktade Pythonanrop verifierade fri/utelämnad kapacitetsbindning, `NaN`-kostnad,
  `unverified`/saknad kvalitet samt den publika bypassflaggan.
- Riktat JavaScriptanrop verifierade `Date.parse`-normalisering av omöjliga kalenderdatum.
- Sökning utanför tester verifierade att ingen katalog-/generator-/produktväg använder
  kontraktsfasaden eller sätter kontraktsmarkören.

Codex ändrade ingen implementation, tariffdata, commit eller push under granskningen.
