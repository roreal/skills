---
review_id: "2026-09-09-013"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v19.md
  - Fjarrvarmetariffer/batchplan-v19.md
  - skills commits eb63c2ceaf9a44714a8c494f7e4710338c80d2f2 and cf73efad63f244b3298b72b6bd73cbd7491f366b
reviewed_heads:
  skills: "cf73efad63f244b3298b72b6bd73cbd7491f366b"
  enkey-agents: "17c859908f938e419bf3ce92a8daf11282f63878"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-012"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v19 och batchplan v19

## Bedömning

V19 rättar den verkliga femparametersguarden, väljer fail-closed opt-in för
besparingsförmågan och ger den elementvisa validatorn ett konkret, cykelfritt ägarskap.
Inventeringen beskriver också ett auktoritativt `IndataPost.attesterad`-krav. Dessa vägval
är rätt och ska bevaras.

Planen är ändå inte implementeringsklar. Den uttryckliga policykonstruktorn kan fortfarande
inte bära huvuddelen av de planerade `Tariffpolicy`-fälten, och V19:s påstående om att
TypeScript skulle acceptera extra objektfält är fel. Attesteringen saknar samtidigt en
faktisk kanal från formulär-/produktindatan till `IndataPost`, så ett normalt
Lidköpingsanrop kan inte bli attesterat. `batchplan-v19.md` är dessutom fortfarande en
selektivt ändrad V18-plan med V18-rubrik, V18-scope och den fiktiva Pythonproduktfil som
V19 säger sig ha tagit bort. V20 krävs före produktkod, tariffdata, aktivering eller push.

## P1-fynd

### P1 — `skapaTariffpolicy()` är fortfarande en flaskhals och V19:s TypeScriptpåstående är fel

Transporttabellen vid `tariffinventering-v19.md:2153–2170` listar sexton fält, men den
”kompletta konstruktionskedjan” vid rad 2203–2225 utökar `skapaTariffpolicy()`s options och
returvärde med endast `stodjerBesparing`. Den verkliga konstruktorn har i dag bara
`tackning`, `kapacitetBindning`, `kallenergiBindning` och `returtemperaturBindning`.

Följande planerade policyfält saknas därför fortfarande i den uttryckliga options-/retur-
kedjan:

- `kapacitetBandBindning`,
- `kapacitetMultiplikatorBindning`,
- `flodeskorrigeringVariant`,
- `kallenergiArsserieBindning`,
- `stodjerAktuellArskostnad`,
- `returtemperaturArsserieBindning`,
- `ersatterKatalograd`, och
- `stodjerBesparing` finns beskrivet, men måste ingå i samma kompletta modell som de andra.

Detta är inte bara risk för tyst bortfall. V19 rad 2221–2224 säger att TypeScripts
strukturella typning inte klagar på extra fält i ett direkt objektliteral om
`exactOptionalPropertyTypes` inte används. Det är fel: en isolerad körning med projektets
TypeScript (`npx tsc --noEmit --strict --skipLibCheck`) gav `TS2353: Object literal may only
specify known properties`. Kontrollfilen låg i `/private/tmp` och togs bort efter testet.
Om typen kringgås med `any` tappar det nuvarande returobjektet i stället fälten.

Konsekvensen är bland annat att `stodjerAktuellArskostnad` inte kan nå resolvern och att
adapter-/motorbindningar kan försvinna, även om `policyFranGenererad()` läser JSON-raden.

**Begärd rättning:** definiera ett enda komplett `TariffpolicyOptions`-/konstruktionskontrakt
med samtliga befintliga och planerade fält, visa hela returobjektet och låt
`policyFranGenererad()` använda exakt samma kontrakt. Testa både direkt konstruktion och
genererad policy för varje fält. Rätta förklaringen om TypeScripts excess-property-check.

### P1 — attesteringen når inte `byggIndataFranPolicy` eller produktvägarna

V19 rad 4304–4335 gör `IndataPost.attesterad` till en auktoritativ domänmarkör, men ingen
typad produktkanal matar markören:

- `byggIndataFranPolicy(policy, policyFalt)` vid rad 2540–2545 tar bara
  `Record<string, PolicyInputValue>` och bygger endast `varde` och `kallaTyp`,
- `KalkylatorInputs`, `Tariffberakningsunderlag` och `BesparingsvardeArgs` saknar ett
  attesteringsfält i de utskrivna kontrakten vid rad 3686–3731 och 3775–3784,
- `argsFranInputs()` transporterar därför ingen attestering,
- den normativa `PolicyFaltMetadata`-formen vid rad 2578–2580 saknar fortfarande
  `kravAttestering`, trots att rad 2229–2231 säger att egenskapen läggs till, och
- `forkontrolleraPolicyIndata` vid rad 2670–2692 kontrollerar inte attestering.

Med den utskrivna V19-designen skapar UI-/produktvägen alltså varje `IndataPost` utan
`attesterad:true`; Lidköping blockeras alltid i den senare statusvalidatorn. Samtidigt
passerar en icke attesterad karta produktens förkontroll och blir därefter det generiska
”oväntat konfigurationsfel” som den verkliga `beraknaBesparingsvardeKontrakt` använder för
ett senare `blocked`-resultat, inte ett fältnära användarfel.

**Begärd rättning:** välj ett enda typat end-to-end-kontrakt, exempelvis ett strukturerat
`PolicyInputPost` med `varde` och `attesterad`, eller en separat
`policyFaltAttestering: Record<string, boolean>`. För det genom
`KalkylatorPage` → `KalkylatorInputs` → `argsFranInputs` →
`Tariffberakningsunderlag`/`BesparingsvardeArgs` → `byggKontraktIndata`/
`byggIndataFranPolicy` → `IndataPost`. Låt även `forkontrolleraPolicyIndata` ge ett typat,
fältnära utfall för ett närvarande men icke attesterat krav, och låt den ordinarie
statusvalidatorn vara den oberoende auktoritativa spärren. Testa UI, direkt produktentry
och direkt fasad i båda relevanta språken.

### P1 — `batchplan-v19.md` är fortfarande V18 och motsäger V19-leveransen

Filen heter `batchplan-v19.md`, men rad 1–13 har rubriken ”Batchplan v18.0”, säger att den
ersätter V17, bygger på `tariffinventering-v18.md` och beskriver vad V18 gör. Det finns
ingen sektion ”Vad som är nytt i v19”. En mekanisk jämförelse mot V18 visar bara 39
tillagda och 23 borttagna rader i en fil på 1 158 rader.

De kvarvarande skillnaderna är funktionella, inte kosmetiska:

- Batch 0 rad 202–233 specificerar bara `policyFalt`-värden och metadata utan den nya
  attesteringstransporten,
- Batch 0:s förkontroll vid rad 257–297 saknar icke-attesterad-indata som fältnära fel,
- Batch 5d rad 485–539 beskriver fortfarande ”denna dokumentationscommit” och fillistan som
  V18, länkar testplanen till V18 och säger att ingen kod ändras av V18-dokumenten,
- rad 516 behåller `besparingsvarde.ts`/”motsvarande Pythonfil”, trots att V19:s inventering
  uttryckligen fastslår att Pythonfilen inte finns och ska tas bort, och
- Batch 5d:s fillista nämner `kravAttestering`-metadata men inte den nödvändiga
  `IndataPost.attesterad`- och produkt-DTO-transporten.

**Begärd rättning:** bygg `batchplan-v20.md` från den gällande V19/V20-modellen, med rätt
rubrik, föregångare, inventeringslänk och dokumentationsscope. Spegla hela
attesteringskedjan och det kompletta policykonstruktionskontraktet i Batch 0/5d, ta bort den
fiktiva Pythonfilen och uppdatera test-/fillistor samt slutlig räkningsnot till aktuell
version.

### P1 — två aktuella normstycken motsäger de nya fälten

Även inventeringen har två kvarvarande aktiva motsägelser:

- `PolicyFaltMetadata`-objektet vid rad 2578–2580 saknar `kravAttestering`, trots den senare
  nya definitionen, och
- sidtestet vid rad 3878–3881 motiverar fortfarande Sandvikens gröna väg med
  `stodjerBesparing !== false`, trots att V19:s gällande kontrakt är explicit
  `stodjerBesparing === true`.

De historiska avsnitten får stå kvar när de tydligt är märkta historik, men aktuella typer,
tester och fillistor måste uttrycka exakt samma modell.

**Begärd rättning:** ersätt de två aktiva styckena och kör en mekanisk sökning efter
`!== false`, den fiktiva Pythonfilen, V18-scope och metadataformer utan attestering innan
V20 levereras.

## Godkända delar och verifieringar

- `Produktbegransning`-guarden ligger nu korrekt först i den verkliga, oförändrade
  femparameterssignaturen och använder den redan upplösta `policy`-parametern.
- `stodjerBesparing` är rätt fail-closed i resolvern: endast explicit `true` öppnar en
  kontraktsgatad tariff; Sandviken ska opta in och Stockholm/Lidköping ska förbli spärrade.
- `vardefelForKrav` ägs nu konkret av `resultatkontrakt.ts` och importeras i befintlig
  beroenderiktning av `besparingsvarde.ts`; Pythonmotsvarigheten kan bo i samma modul som
  båda validatorerna.
- `IndataPost.attesterad` plus ett generiskt `KravPost.kravAttestering` är en rimlig
  domänmodell när den kopplas till en verklig produkt-DTO och båda validatorerna.
- Tm:s `supplier_value`/automatiska `snapshot`-modell, den elementvisa seriealgoritmen,
  motortransporten och den verkliga katalogfilen ska bevaras.
- Lidköpings två produkter förblir källgodkända och `ready_to_implement`. Dispositionen
  förblir 7 implementerade, 57 redo och 28 externt blockerade av totalt 92.
- `git diff --check 673a618..cf73efa` är rent. V19-committarna ändrar endast dokumentation
  och logg. `neptune_academy` står kvar på `f1df177`; `enkey-agents@17c8599` innehåller en
  orelaterad paus av LR260-jobb efter den tidigare granskningspunkten, ingen tariffkod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v20.md` och `batchplan-v20.md`; ändra inte V19 i efterhand.
2. Gör `skapaTariffpolicy()`s options och retur till en fullständig, ensam
   konstruktionskälla för samtliga planerade `Tariffpolicy`-fält; rätta TypeScriptpåståendet
   och lägg direkta samt genererade transporttester.
3. Definiera och transportera faktisk attestering genom hela produkt-DTO-kedjan till
   `IndataPost`; kontrollera den både fältnära i `forkontrolleraPolicyIndata` och
   auktoritativt i `harledResultatstatus`/Pythonmotsvarigheten.
4. Ersätt Batchplanens V18-huvud/scope/referenser och spegla V20:s fullständiga
   konstruktor-, attestering-, filliste- och testkontrakt. Ta bort den fiktiva
   Pythonproduktfilen överallt i aktuell normtext.
5. Rätta aktuella metadata-/teststycken till `kravAttestering` respektive explicit
   `stodjerBesparing === true`; historik ska vara tydligt avskild från norm.
6. Bevara den rättade femparametersguarden, fail-closed besparingsförmåga,
   validatorägarskap, Tm-modell, motortransport, Lidköpings källstatus, räkningen 7/57/28
   och Åkermannen-underlaget. Lägg denna granskning och loggändringarna i en fokuserad lokal
   dokumentationscommit, logga verklig hash/tid och stanna för omgranskning. Ändra ingen
   produktkod, tariffdata, aktivering eller push.
