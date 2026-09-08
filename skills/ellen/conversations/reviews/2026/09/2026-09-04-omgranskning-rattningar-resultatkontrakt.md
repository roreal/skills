---
review_id: "2026-09-04-008"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commits 6f88ed7 och 005c6d9
  - neptune_academy commits abaca72 och 96f2d27
  - rättningar efter granskning 2026-09-04-007
reviewed_heads:
  enkey-agents: "005c6d9"
  neptune_academy: "96f2d27"
implementation_changed: false
push_status: local-unpushed
---

# Omgranskning av rättningarna i resultatkontraktet

## Bedömning

Claude har rättat två centrala delar korrekt:

- `capacity: null` plus saknad fast avgift avvisas åter; en ren energitariff kräver nu en
  explicit `capacity.type: "not_applicable"`-markör,
- en oinstansierad eller ofullständig `Tariffpolicy` blockerar genom ett explicit
  `komplett=False` som säkert standardvärde.

Omfattningen är fortfarande avgränsad. Inga riktiga tariffposter eller nya tariffamiljer har
aktiverats, båda arbetskopiorna är rena och committerna är lokala. De redovisade testsviterna
passerar även i Codex körning.

Kontrollpunkten är ändå **inte godkänd för push eller nästa tariffbatch**. Fyra P1-luckor
innebär fortfarande att ett resultat kan märkas `exact/complete` utan att kontraktet har
validerat de värden som faktiskt används i kostnadsberäkningen, rätt period och kvalitet eller
en verkligt täckande tidsserie. Den nya fasaden är dessutom ännu inte kopplad till någon
produktionsväg. Testvektorerna är identiska just nu men består av två manuella kopior utan
synkspärr.

## Fynd

### P1 — fasaden validerar ett värde men prissätter ett annat

I Python tar `berakna_arskostnad_med_kontrakt` emot `inrapporterad_indata`, `kapacitet` och
`falt` som tre oberoende argument. Statusen härleds ur det första, medan `arskostnad` får de
två senare oförändrade (`resultatkontrakt.py:324–368`). TypeScript gör samma sak
(`resultatkontrakt.ts:269–296`). Fasaden kontrollerar inte heller att
`policy.tariff_id`/`policy.tariffId` är samma tariff som `prisar.tariff_id`/`tariff_id`.

De nya integrationstesterna demonstrerar oavsiktligt luckan: kravposten `effekt` får värdet
123 men kostnaden räknas med separat `kapacitet=50` (`test_resultatkontrakt.py:229–238` och
`resultatkontrakt.test.ts:157–165`). Codex körde dessutom samma väg med
`policy.tariff_id="annan-tariff"`; resultatet blev fortfarande `exact/complete` och
kapacitetskostnaden beräknades från 50 kW.

Det går därför att uppfylla kontraktet med ett spårbart skenvärde och samtidigt prissätta en
annan, uppskattad eller felaktig siffra. Samma problem gäller tariffspecifika fält i `falt`.

**Begärd rättning:** gör de validerade `IndataPost`-objekten till kostnadsberäkningens enda
källa för de fält policyn omfattar, via en typad och testad bindning till `kapacitet` och
`falt`. Avvisa motsägande dubblettvärden. Kontrollera tariff-ID mellan policy och prisår innan
status kan bli komplett. Lägg negativa integrationstester för annan tariff och olika
kontrakts-/motorvärden i båda språken.

### P1 — period, giltighet och kvalitet kan fortfarande ge falskt `exact`

Implementationen erkänner uttryckligen att `observerad_period` inte jämförs med
`kalperiod_definition` (`resultatkontrakt.py:235–245`). Den kräver endast att värdet inte är
`None`; vilken sträng som helst, även tom sträng eller fel år, passerar. `giltig_fran` läses
aldrig, `giltig_till` jämförs som ovaliderad text och endast den exakta kvalitetssträngen
`"invalid"` blockeras (`resultatkontrakt.py:281–305`, TypeScript motsvarande rad 203–235).

Codex reproducerade följande på `005c6d9`, samtliga med `exact/complete`:

```text
kravets period: "2026", observerad_period: "2020"
kvalitet: "garbage"
giltig_fran: "2099-01-01", berakningsdatum: "2026-09-04"
```

Det är exakt det tidigare fyndets fall "observerad period 2020 trots krav 2026". Granskning
007 tillät uppskjuten full periodmodell bara om sådana fält under tiden inte kunde leda till
`exact`; den nuvarande närvarokontrollen är därför inte det begärda fail-closed-mellanläget.

**Begärd rättning:** inför maskinellt jämförbar period/täckning och en tillåten
kvalitetstaxonomi, eller låt okänd/ej verifierbar period och kvalitet ge `blocked` eller
`snapshot` tills modellen finns. Validera riktiga ISO-datum och båda giltighetsgränserna.
Tester ska minst täcka fel år, tom/ogiltig period, framtida `giltig_fran`, okänd kvalitet och
felaktigt datumformat.

### P1 — serielängd är inte tidsserietäckning och Python/TypeScript skiljer sig

Ett rullande fält får `exact` enbart när värdet råkar vara en Python-`tuple` eller
TypeScript-array med minst tolv element (`resultatkontrakt.py:297–303`,
`resultatkontrakt.ts:225–235`). Elementen saknar tidsstämplar/månadsidentitet, upplösning,
unikhetskontroll och numerisk kvalitetskontroll. Tolv `NaN` gav `exact/complete` i Codex
riktade körning.

Pythonkontraktet känner dessutom endast igen `tuple`, trots att JSON och TypeScript använder
listor/arrayer. Codex verifierade:

```text
icke-rullande Python-lista [1, 2]      => exact/complete
rullande Python-lista med 12 värden    => snapshot/complete
rullande Python-tuple med 12 värden    => exact/complete
TypeScript-array med 12 värden         => exact/complete
```

Den Python-adapter som kör de delade JSON-vektorerna konverterar listan till tuple före
testet (`test_resultatkontrakt_vektorer.py:26–33`) och döljer därmed språkavvikelsen i stället
för att fånga den.

**Begärd rättning:** använd samma JSON-nativa, strukturerade serierepresentation i båda
språken. En exakt serie måste bevisa förväntad upplösning och period, rätt antal unika och
sammanhängande datapunkter samt ändliga numeriska värden. Om det inte ska byggas i denna
grundetapp får en serie endast ge `snapshot`/`blocked`, aldrig `exact`. Kör samma råa JSON
utan språkunik normalisering i konformitetstesterna.

### P1 — ingen faktisk publik beräkningsväg använder skyddet

Sökning i båda kodbaserna visar att de nya fasaderna fortfarande endast anropas av sina egna
tester och den nya modulen. Generatorn och React-vägen har inte ändrats. Produktens
`besparingsvarde.ts:179–180` anropar fortsatt den exporterade `arskostnad` direkt, utan
`Tariffpolicy` eller `Resultatstatus`. Pythonfunktionerna `arskostnad` och
`mwh_fran_arskostnad` är på samma sätt fortsatt offentliga och omärkta.

Integrationstesterna bevisar alltså bara att fasaden blockerar **om någon väljer att anropa
den**. De bevisar inte acceptansvillkor 3 i granskning 006 eller rättningskrav 4 i granskning
007: att nya katalogtariffer inte kan nå ett omärkt kostnadsresultat genom den befintliga
produktvägen.

**Begärd rättning:** koppla den verkliga wrapper-/kalkylatorvägen till kontraktsfasaden, eller
inför en annan maskinellt upprätthållen spärr som gör råmotorn otillgänglig för de 28 nya
tarifferna. Märk och avgränsa äldre direktanrop som legacy. Lägg ett integrationstest från
den faktiska produktentryn som visar att en ny katalogtariff utan komplett policy eller
obligatorisk indata inte kan returnera en kostnad.

### P1 — `not_applicable` tillåter motsägande kapacitetsband

Den nya grindgrenen för `capacity.type == "not_applicable"` avvisar en samtidig fast avgift,
men kontrollerar inte att kapacitetsobjektet saknar band och övriga kapacitetsprisfält
(`katalog.py:277–287`). `till_prisar` läser fortfarande eventuella band innan sentinelen
sätts (`katalog.py:515–561`).

Codex lade ett vanligt kapacitetsband i den fristående rena-energifikturen. `grind()`
returnerade ändå `None` och prisårsobjektet bar bandet, medan sentinelen fick motorn att
redovisa noll kapacitetskostnad. En felaktig extraktion kan alltså samtidigt säga "ingen
kapacitet" och bära en verklig kapacitetsprislista; grinden väljer tyst den kostnadsfria
tolkningen.

**Begärd rättning:** definiera och validera den tillåtna objektsformen för
`not_applicable`. Avvisa åtminstone `bands`, `rate_period`, `basis_unit`, `formula` och
andra prissättande kapacitetsfält tillsammans med markören. Låt `till_prisar` uttryckligen
skapa tomma nivåer för markören i stället för att först översätta eventuella band. Lägg ett
regressionstest för den motsägande formen.

### P2 — testvektorerna är två manuella kopior, inte en synkspärr

De två fixturefilerna är byte-identiska i denna kontroll (`sha256
5c167076524ecf8921f75b354e212c9604565b2637123d95cac2e9043ebf7ff6`), men `_readme` säger
uttryckligen att de kopieras manuellt. Varje repository kör endast sin egen kopia. En ändring
av algoritm och facit i det ena repot kan därför passera lokalt utan att det andra repot ens
ser ändringen. Pythonadapterns list-till-tuple-konvertering visar dessutom att "samma JSON"
inte i sig betyder samma runtimefall.

**Begärd rättning:** välj en kanonisk fixture och en deterministisk kopierings-/generatorväg
med en kontroll som fallerar på avvikande genererat resultat, eller en faktisk
konformitetskontroll som jämför båda implementationerna mot samma fil. Lägg till
tariff-ID-/värdebindning, felperiod, okänd kvalitet och rå serierepresentation i facit.

## Avgränsad rättningsbeställning till Claude

Rätta bara grundetappen och håll båda commitserierna lokala:

1. bind kontrakterad indata till de värden som faktiskt skickas till kostnadsmotorn och
   kontrollera tariff-ID,
2. gör period, giltighet och kvalitet maskinellt verifierbara eller tydligt fail-closed,
3. ersätt längdbaserad tuple/array-status med en gemensam validerad serierepresentation eller
   blockera `exact` för serier tills den finns,
4. skydda den verkliga produktentryn för nya katalogtariffer, inte bara den valfria fasaden,
5. stäng `not_applicable`-schemat mot motsägande kapacitetsprisfält,
6. gör konformitetsvektorerna deterministiskt synkade och kör om samtliga kontroller.

Aktivera inga tariffer och rör inte Familj 4, Telge, E.ON/Navirum, Sundsvall Matfors eller
Vattenfall. Redovisa nya lokala commit-hashar och invänta en ny Codex-kontroll före push.

## Utförda kontroller

- `enkey-agents@005c6d9`: 221/221 tariff-pytest passerar i projektets `.venv`.
- `neptune_academy@96f2d27`: 252/252 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda nya committerna.
- Båda arbetskopiorna är rena och exakt två commits före respektive `origin/main`; ingen
  push har skett.
- De två lokala JSON-fixturekopiorna har samma SHA-256 i denna kontroll.
- Riktade Pythonanrop verifierade fel period, okänd kvalitet, framtida `giltig_fran`,
  icke-ändliga serievärden, list/tuple-avvikelsen, obundet tariff-ID/kapacitetsvärde samt
  motsägande `not_applicable` plus kapacitetsband.
- Sökning i produktkoden verifierade att fasaderna saknar produktionskonsumenter och att
  `besparingsvarde.ts` fortfarande använder `arskostnad` direkt.

Codex ändrade ingen implementation, tariffdata, commit eller push under omgranskningen.
