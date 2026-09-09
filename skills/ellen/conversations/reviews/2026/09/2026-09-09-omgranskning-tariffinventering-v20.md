---
review_id: "2026-09-09-014"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v20.md
  - Fjarrvarmetariffer/batchplan-v20.md
  - skills commits 7270b6ea808858dd74bfef14fdbdde3925e34fac and c732bd4af76efa15a317646db9b801a44e4aa8df
reviewed_heads:
  skills: "c732bd4af76efa15a317646db9b801a44e4aa8df"
  enkey-agents: "17c859908f938e419bf3ce92a8daf11282f63878"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-013"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v20 och batchplan v20

## Bedömning

V20 löser huvuddelen av V19-fynden i inventeringen. Den planerade
`skapaTariffpolicy()`-vägen bär nu alla åtta nya policyfält, TypeScripts excess-property-
förklaring är rättad, och attesteringen har en namngiven kanal från formulärstate genom
produkt-DTO:erna till `IndataPost.attesterad`. Metadataformen innehåller
`kravAttestering`, förkontrollen får orsaken `'ej_attesterat'`, och den ordinarie
statusvalidatorn förblir en oberoende spärr. Den fiktiva Pythonproduktfilen är också
borttagen ur Batch 5d.

Planen är ändå inte implementeringsklar. Den aktiva Batch 0-texten innehåller fortfarande
det äldre, oattesterade kontraktet samtidigt som två nya punkter läggs sist, och den
utskrivna policykonstruktorn försvagar en typad diskriminator samt lämnar de nya
bindningarna utanför konstruktionsvalideringen. V21 krävs innan produktkod, tariffdata,
aktivering eller push.

## P1-fynd

### P1 — Batch 0 har två samtidiga kontrakt för samma typer och funktioner

`batchplan-v20.md:232–253` anger fortfarande den gamla tvåparametersbyggaren
`byggIndataFranPolicy(policy, policyFalt)` och fyrparametersanropet
`byggKontraktIndata(..., args.policyFalt ?? {})`. Samma aktiva avsnitt anger vid rad
264–268 en `PolicyValideringsOrsak` utan `'ej_attesterat'`, vid rad 287–309 en
`PolicyValideringsFel` utan samma orsak, och metadatauppräkningen vid rad 254–263 saknar
`kravAttestering`.

Punkt 12 vid rad 428–438 lägger därefter till attestkartan och `'ej_attesterat'`, men
ersätter inte de äldre definitionerna. En implementerare kan därför följa punkt 5/7/8 och
bygga exakt den V19-väg som aldrig kan attestera Lidköping, eller följa punkt 12 och få ett
annat API. Batch 0:s teststrategi vid rad 461–471 testar inte heller uttryckligen
attesteringens fem nödvändiga gränser: metadata, UI-default, byggare, direkt produktentry
och direkt fasad.

Detta är samma strukturella problem som V19-granskningen bad V20 att lösa genom en genuint
aktuell batchplan. Den mekaniska jämförelsen visar också att V20-planen är V19 plus 99 och
minus 31 rader, och den aktiva Lidköpingsinledningen pekar fortfarande på
`tariffinventering-v18.md` vid rad 489/494 medan räkningsnoten pekar på V17 vid rad 1211.
Historik får referera äldre versioner, men en aktuell arbetsorder får inte använda dem som
normativ designkälla.

**Begärd rättning:** skriv om Batch 0:s punkter 5–8 i stället för att lägga en korrigering
som punkt 12. Det enda gällande kontraktet ska innehålla
`policyFaltAttestering` i `KalkylatorInputs`, `Tariffberakningsunderlag` och
`BesparingsvardeArgs`, i båda byggarna, i den delade orsaksunionen och i metadataformen.
Testlistan ska uttryckligen kräva:

- metadata med `kravAttestering: true` för rätt fält;
- oikryssad eller saknad UI-state som ett fältnära `'ej_attesterat'`-fel;
- `false`/saknad respektive `true` bevarat till `IndataPost.attesterad`;
- direkt produktentry som kastar `invalid_policy_fields` med rätt nyckel; och
- direkt fasad som blir `blocked` utan attestering men går vidare med attestering, givet
  övrig giltig indata.

Uppdatera samtidigt Batch 5d:s och räkningsnotens normativa länkar till V21. Äldre
versionshänvisningar får stå kvar endast i tydligt märkta historikstycken.

### P1 — den ”kompletta” policykonstruktorn är inte strikt för de nya fälten

Inventeringens konstruktor vid `tariffinventering-v20.md:2258–2293` transporterar nu de
åtta fälten, vilket är en riktig förbättring. Men två delar gör den fortfarande olämplig
som den ”kompletta, ensamma konstruktionskällan” som dokumentet säger att den är:

1. `flodeskorrigeringVariant?: string` vid rad 2268 motsäger det normativa kontraktet vid
   rad 4098–4099: bara `'golvfri' | 'golvbegransad'` är tillåtet. Den breda strängtypen
   släpper igenom ett okänt variantnamn till en sen motorgrind i stället för att göra
   ogiltig policy omöjlig eller omedelbart avvisad.
2. Konstruktorskissen säger vid rad 2276–2278 att bara den befintliga
   bindningsnyckelkontrollen ska bevaras oförändrad och kallar den dessutom felaktigt
   ”fyra ursprungliga bindningsfält”; dagens verkliga konstruktor validerar tre. De fyra
   nya nyckelbärande bindningarna (`kapacitetBandBindning`,
   `kapacitetMultiplikatorBindning`, `kallenergiArsserieBindning`,
   `returtemperaturArsserieBindning`) lämnas därmed utanför samma existenskontroll, trots
   att §6a.2–§6a.4 kräver att var och en pekar på en deklarerad `KravPost`.

De föreslagna direkta/genererade testerna vid rad 2319–2322 bevisar bara transport, inte
att en okänd variant, en hängande bindningsnyckel eller fel `vardetyp` stoppas.

**Begärd rättning:** definiera en enda namngiven `TariffpolicyOptions` med samma exakta
fältformer som `Tariffpolicy`. Typa flödesvarianten som den tvåvärdiga unionen och använd
samma typ i Python, JSON-mappning och TypeScript. Låt konstruktionen validera samtliga sju
nyckelbärande bindningar mot `kravdaFalt`; kontrollera dessutom bindningsspecifik
`vardetyp` där kontraktet kräver det (`band_id`, `number` respektive `number_series`).
Lägg negativa direkt- och genereringstester för okänd variant, hängande bindning och fel
bindningstyp, utöver de redan beställda transporttesten.

## Godkända delar och verifieringar

- Alla åtta nya policyfält finns nu i options och returobjekt; V19:s `TS2353`-förklaring
  är korrekt rättad.
- Inventeringen beskriver en sammanhängande attestkanal genom UI, produkt-DTO:er,
  `argsFranInputs`, båda byggarna och `IndataPost`; förkontroll och auktoritativ validator
  har skilda, rimliga roller.
- `PolicyFaltMetadata` innehåller nu `kravAttestering`, och Sandviken-testet använder
  korrekt explicit `stodjerBesparing === true`.
- Den verkliga femparametersguarden, fail-closed besparingsförmågan,
  `vardefelForKrav`-ägarskapet, Tm:s `supplier_value`/`snapshot`-modell,
  motortransporten och Batch 5d:s verkliga katalogfil ska bevaras.
- Lidköpings två produkter förblir källgodkända och `ready_to_implement`. Dispositionen
  förblir 7 implementerade, 57 redo och 28 externt blockerade av totalt 92.
- `git diff --check cf73efa..c732bd4` är rent. V20-committarna ändrar endast dokumentation
  och logg. Produktrepoerna står kvar på `enkey-agents@17c8599` och
  `neptune_academy@f1df177`; ingen tariffimplementation ingår i leveransen.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v21.md` och `batchplan-v21.md`; ändra inte V20 i efterhand.
2. Ersätt Batch 0:s äldre punkt 5–8-kontrakt med den fullständiga attestmodellen. Lägg inte
   ännu ett rättelselager sist i listan.
3. Gör `TariffpolicyOptions` exakt typad och låt konstruktorn validera alla gamla och nya
   bindningsnycklar samt deras avsedda värdetyper. Lägg negativa konstruktionstester.
4. Gör teststrategin explicit för hela attesteringskedjan: metadata, UI, byggare, direkt
   produktentry och direkt fasad, både negativ och positiv väg.
5. Uppdatera aktuella Batch 0/5d-/räkningsreferenser till V21. Historiska referenser får
   vara kvar endast i tydligt historiska avsnitt.
6. Bevara alla godkända V20-delar, Lidköpings källstatus, Åkermannen-underlaget och
   räkningen 7/57/28. Lägg denna granskning och loggändringarna i en fokuserad lokal
   dokumentationscommit, logga verklig hash/tid och stanna för omgranskning. Ändra ingen
   produktkod, tariffdata, genererad fil, aktivering eller push.
