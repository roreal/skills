---
review_id: "2026-09-06-001"
date: "2026-09-06"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit 670efa7
  - neptune_academy commit 68543a4
  - implementation efter godkännande 2026-09-05-003
reviewed_heads:
  enkey-agents: "670efa7"
  neptune_academy: "68543a4"
implementation_changed: false
push_status: local-unpushed-not-approved
---

# Kodgranskning: Stockholm Exergis månadsvisa resultatkontrakt

## Bedömning

Leveransen är väl avgränsad till `validated` månadsvis fakturaåterspelning. Den nya
månadsfasaden återspelar samtliga tolv Åkermannen-rader med samma kostnad som den befintliga
direkta vägen, täckningen är separerad mellan `monthly_invoice`, `annual_forward` och
`annual_inverse`, och ingen `_kraver_kontrakt`-markör eller produktändring har införts.
Test-, typ-, bygg- och diffkontrollerna är gröna inom tariffprojektets avtalade omfattning.

Kontrollpunkten får ändå **`changes-required` före push**. Två bindande säkerhetsvillkor kan
fortfarande kringgås och ge `exact/complete` med en felaktigt beräknad fakturakostnad. En
mindre språkparitetslucka och några uttryckligen beställda negativtester återstår också.

## Fynd

### P1 — kallenergi- och returtemperaturbindningarna är inte fail-closed mot tariffstrukturen

Månadsfasaden korskontrollerar enbart kapacitetsstrukturen. Den verifierar att en **befintlig**
`kallenergi_bindning` eller `returtemperatur_bindning` pekar på ett `monthly`-fält, men den
kräver aldrig att bindningen finns när prisobjektet faktiskt har `energi.tillagg` respektive
en tillämplig `returtemperatur`-post
(`resultatkontrakt.py:622–650`, `resultatkontrakt.ts:613–640`). Därefter ersätts saknade
bindningar med motorernas standardvärden `0` och `None`/`null`
(`resultatkontrakt.py:662–664`, `resultatkontrakt.ts:651–653`).

Codex reproducerade detta på januari 2026 genom att behålla alla tre verifierade
`IndataPost` men skapa en kopia av den registrerade policyn utan en bindning:

- utan `kallenergi_bindning`: status blev `monthly/exact/complete`, men energikostnaden blev
  64 608,486 kr i stället för 65 580,451 kr;
- utan `returtemperatur_bindning`: status blev `monthly/exact/complete`, men returposten blev
  0 kr i stället för −28,9076 kr.

Detta är exakt den tysta noll/`None`-väg som villkor 2 förbjöd. Nuvarande registrerade
Stockholm-policy innehåller visserligen rätt bindningar, men den publika fasaden och den
generiska policyn säger sig upprätthålla kontraktet och måste därför stänga felaktig eller
framtida policydata maskinellt.

**Begärd rättning:** korskontrollera även kallenergi och returtemperatur mot prisobjektets
faktiska struktur i både Python och TypeScript. `energi.tillagg` ska kräva en relevant
kallenergibindning varje månad. En returtemperaturpost ska kräva en relevant bindning när
målmånaden ingår i tariffpostens månader; utanför dem får den saknas. Kontrollera också att
det bundna policyfältets `tillampliga_manader` verkligen omfattar målmånaden. Lägg negativa
tester för saknad kallenergi- och returtemperaturbindning samt för bindning vars policyfält
inte är tillämpligt den aktuella månaden. Resultatet får blockeras eller kasta före motorn,
men får aldrig bli `complete` med standardvärde.

### P1 — effektens giltighet bevisar inte att den omfattar hela fakturamånaden

Fasaden väljer månadens första dag som enda `berakningsdatum`
(`resultatkontrakt.py:652–658`, `resultatkontrakt.ts:642–646`). Statuskontrollen jämför sedan
de valfria gränserna `giltig_fran`/`giltig_till` enbart mot denna punkt
(`resultatkontrakt.py:397–409`, `resultatkontrakt.ts:400–414`). Därmed kan `exact` uppnås
utan något giltighetsintervall alls, eller med en effekt som bara gäller den första dagen.

Codex reproducerade båda fallen för januari 2026:

- en effektpost helt utan `giltig_fran` och `giltig_till` gav `exact/complete` och kostnad;
- `giltig_fran: 2026-01-01`, `giltig_till: 2026-01-01` gav också `exact/complete` och kostnad.

Villkor 3 kräver att den årsvis debiterbara effekten **omfattar månaden**, inte bara
månadens första dag.

**Begärd rättning:** gör giltighetsintervallet obligatoriskt för det årsvisa
kapacitetsfältet i månadsfasaden och kontrollera att det täcker både månadens första och
sista kalenderdag. Spegla kontrollen i båda språken. Lägg tester för saknade gränser,
start mitt i månaden, slut mitt i månaden, exakt heltäckande intervall och skottårets
februari. Historiska månader ska fortsatt jämföras mot målmånaden, aldrig dagens datum.

### P2 — TypeScript tillåter dubblerade `tillampligaManader`

`skapaKravPost` kräver en icke-tom lista och heltal 1–12 men jämför inte listans längd med
en `Set` (`resultatkontrakt.ts:130–139`). `[1, 1, 2]` accepteras alltså trots villkor 3:s
uttryckliga krav på unika månader. Pythonmodellen använder `frozenset`, men den delade
vektorbyggaren konverterar rålistan till `frozenset` innan konstruktion och skulle därför
tyst dölja samma fel i en testvektor (`test_resultatkontrakt_vektorer.py:76–84`).

**Begärd rättning:** avvisa dubbletter i TypeScript och lägg ett negativtest. Om fallet läggs
i den delade vektorfilen måste Pythonharnessen kontrollera rålistans unikhet före
`frozenset`-konverteringen så testet verkligen är symmetriskt.

### P2 — två beställda negativtester saknas

Acceptansvillkor 6 begärde uttryckliga negativa tester för **saknad bindning** och **okänt
aktiveringsläge**. Bindningsfallet saknas och döljer P1-felet ovan. Själva
`kontrollera_leverantorsfilsgrind` har en korrekt strikt allow-list, men testet under rubriken
”aktiveringslage strikt allow-list” kontrollerar endast att de riktiga posterna innehåller
`validated`; ingen felskrivning eller fel typ provas.

**Begärd rättning:** lägg de saknade bindningstesterna enligt P1 och isolerade generator-/
grindtester för exempelvis `"validted"`, `None`, tal och objekt. Verifiera fortsatt att
`enforced` avvisas med dagens endast-`monthly_invoice`-policy och att `_kraver_kontrakt`
aldrig genereras för `validated`.

### P3 — några modulkommentarer beskriver fortfarande grundetappen

Pythonmodulens inledning nämner fortfarande `komplett=True`, endast kapacitetsbindning,
endast årsfasaden och att inga tariffpolicyer instansieras (`resultatkontrakt.py:10–23,
49–50`). `KontraktKravs`-texten nämner på motsvarande sätt bara årsfasaden. Rätta detta i
samma lilla uppföljningscommit så dokumentationen beskriver `tackning`, tre bindningar,
månadsfasaden och Stockholm-piloten.

## Godkända delar

- `Tariffpolicy.tackning` skiljer de tre beräkningsändamålen och årsfasaden blockeras av en
  policy som bara täcker `monthly_invoice`.
- Leverantörsfilen använder `validated`, inte `enforced`; båda prisåren har separata
  tariff-ID:n och ingen global kontraktsmarkör genereras.
- Månad, prisår, ändlig numerik, `0 <= mwh_kallt <= mwh`, positiv effekt och
  observerad-period-matchning valideras.
- Januari kräver returtemperatur, juli gör det inte, och saknad kall energi som indata
  blockerar även när rätt värde är noll.
- Alla tolv fakturarader matchar den direkta månadsfunktionen i båda språken.
- Den interna månadskostnadswrappern följer årsfasadens mönster och de rekursiva
  arkitekturtesterna skyddar båda interna funktionsnamnen.
- Generatorns båda vägar delar leverantörsfilsbehandling; fixturekopiorna och genererad data
  är synkade. Den faktiska git-diffen innehåller bara kontraktsmetadata, policydata och den
  godkända flytten av `effektgrans_kw` i Stockholm-materialet.
- Kalkylatorns årsprognos, kronor-till-MWh-invers, UI och övriga tariffer är orörda.

## Rättningsbeställning till Claude

1. Stäng de två saknade bindningskontrollerna mot tariffstrukturen och månadstillämpligheten
   i båda språken.
2. Kräv och verifiera att effektens giltighetsintervall täcker hela målmånaden.
3. Avvisa dubblerade `tillampligaManader` i TypeScript och gör testet språkparitetssäkert.
4. Lägg de saknade negativa testen för bindningar och okänt aktiveringsläge.
5. Rätta de inaktuella modulkommentarerna.
6. Kör tariffsviten, Vitest, `tsc --noEmit`, produktionsbygget, fixture-synken och
   `git diff --check`; skapa fokuserade lokala rättningscommits och stanna för omgranskning.

Ändra inte `validated` till `enforced`, lägg inte till `_kraver_kontrakt`, ändra inte
årsprognos/invers/UI/andra tariffer och pusha inte före nästa Codex-kontroll.

## Utförda kontroller

- `enkey-agents@670efa7`: 330/330 tester under `tools/tariffer/tests` passerar.
- `neptune_academy@68543a4`: 347/347 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda committerna.
- Båda implementationsarbetskopiorna är rena efter kontrollen; inget har pushats.
- Ett oavgränsat `pytest` från hela `enkey-agents` stannar i insamlingen på 13 orelaterade
  Milesight-fel (bland annat saknat `pymodbus`). Den avtalade och tidigare redovisade
  tariffsviten är komplett och grön.
- Codex körde fyra extra reproduktionsfall som bekräftade falskt `exact/complete` vid borttagen
  kallenergi-/returtemperaturbindning samt ofullständig eller saknad effektgiltighet.

Codex ändrade ingen implementation, tariffdata, commit eller push under granskningen.
