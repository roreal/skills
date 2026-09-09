---
review_id: "2026-09-09-011"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v17.md
  - Fjarrvarmetariffer/batchplan-v17.md
  - skills commits df20de40df095bc5b4ff47ea5956a23363719867 and 497fbfcc07a4cbaa40739a7788b888f80e7db318
reviewed_heads:
  skills: "497fbfcc07a4cbaa40739a7788b888f80e7db318"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-010"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v17 och batchplan v17

## Bedömning

V17 löser huvuddelen av V16:s integrationsproblem. Den kanoniska diskriminatorn
`type: "signed_monthly_flow_adjustment"` är vald, de två justeringsregistren och en
speglad `faltSerier`/`falt_serier`-transport till `Kostnad.justering` är specificerade,
och Lidköping har fått en explicit aktuell-årskostnadsförmåga. V17 har också rättat de
beställda Lidköpingsreferenserna och EOF-felet. `git diff --check d75ea6b..497fbfc` är rent.

Planen är ändå inte implementeringsklar. Den nya Tm-källtypen accepteras inte av det
befintliga resultatkontraktet, det strikta minimumet jämför en hel serie som om den vore
ett tal, och det utlovade produktbegränsningsfelet är fortfarande bara prosa. Batchplanen
har dessutom kvar två äldre, normativa versioner av förmågekontraktet samt en fillista som
placerar katalogändringen i fel fil och samtidigt säger att katalogen inte ska ändras.
V18 krävs före produktkod, tariffdata, aktivering eller push.

## P1-fynd

### P1 — `kallaTyp: 'snapshot'` är varken en giltig eller komplett transport

V17 rad 4004–4013 säger att `byggIndataFranPolicy` ska märka just `Tm_m` med
`kallaTyp: 'snapshot'` och att resultatets interna `noggrannhet` blir `'uppskattat'`.
Det kan inte implementeras mot nuvarande kontrakt:

- TypeScript har exakt `KALLTYPER = ['supplier_value', 'calculated', 'estimated']` och
  Python samma tre värden. Båda konstruktorerna avvisar andra källtyper.
- `NOGGRANNHETER` är `exact | snapshot | estimated`; `'uppskattat'` är UI-språk, inte ett
  internt enumvärde.
- den generiska byggaren är fortfarande specificerad vid rad 2331–2338 att märka varje
  post som `supplier_value`; ingen policyegenskap berättar för byggaren att just Tm ska
  få en annan källa. Ett hårdkodat Lidköpingsnyckelnamn i byggaren vore fel lösning.
- Batch 5d nämner inte en utökning av `KALLTYPER`, tillåtna källor, serialisering,
  statusregler eller testvektorer. V17 kallar dessutom värdet ”nytt, tredje” trots att
  tre källtyper redan finns.

**Begärd rättning:** återanvänd helst den befintliga modellen. Ett av användaren
transkriberat, namngivet leverantörs-/fakturavärde kan vara `supplier_value`, medan
kravets kvalitet/rullande källperiod gör resultatets `noggrannhet: 'snapshot'`. Lägg till
en obligatorisk källattestering/hjälptext och blockera fältet om användaren inte intygar
faktura eller direkt besked. Om en fjärde källtyp verkligen behövs måste V18 i stället
utöka hela speglade unionen, konstruktionsvalideringen, policykällorna, byggaren,
serialiseringen, statushärledningen och testerna. Använd aldrig `'uppskattat'` som internt
`Noggrannhet`-värde.

### P1 — `minExklusiv` validerar inte elementen i `number_series`

V17 rad 1987–2001 och 3981–3997 byter kontrollen till uttryck som jämför
`post.varde` direkt med `f.minvarde`. För Tm är `post.varde` däremot en tolvmånadersserie.
I den verkliga `harledResultatstatus` körs dagens min-/heltalskontroll bara innanför
`if (!arSerie(post.varde))` (TypeScript rad 412–421); Python har samma avgränsning vid
rad 436–445. V17:s egen generiska förkontroll säger samtidigt korrekt att min, max och
heltal ska kontrolleras på samtliga serieelement.

En rak implementation av den nya texten ger alltså en ogiltig array–tal-jämförelse eller
olika beteende mellan UI-förkontrollen och ett direkt fasadanrop.

**Begärd rättning:** definiera samma elementvisa kontroll i BÅDA validatorerna och BÅDA
språken, exempelvis `varden = arSerie(varde) ? varde : [varde]`. Kör min, max och heltal
över varje numeriskt element. För exklusivt minimum är brottet `varde <= min`; för
inkluderande minimum `varde < min`. Testa också ett direkt fasadanrop så att spärren inte
bara bevisas via produktsidans förkontroll.

### P1 — produktbegränsningsfelet saknar typ, konstruktor och verkligt kast

V17 rad 3051–3053 säger uttryckligen att begränsningen inte är `KontraktBlockerat`, men
testfall 12 vid rad 4061–4064 säger `KontraktBlockerat`/motsvarande. I varken V17 eller
Batch 5d finns en klass, orsakstyp, konstruktor, guardrad eller UI-mappning för det
”typade produktbegränsningsfelet”. Den verkliga produktkoden har i dag bara
`KontraktBlockerat`, och `beraknaBesparingsvardeKontrakt` saknar denna guard.

**Begärd rättning:** välj exakt en maskinläsbar modell. Skriv ut typen och dess fält,
den konkreta guarden i `beraknaBesparingsvardeKontrakt`, hur UI:t visar den och tester för
både Stockholm och Lidköping. Använd inte samtidigt ”inte `KontraktBlockerat`” och
”`KontraktBlockerat`/motsvarande”.

### P1 — äldre förmågetext är fortfarande normativ och motsäger V17-beslutet

Batchplan rad 271–347 beskriver fortfarande `stodjerAktuellArskostnad` som en kontroll av
`policy.kallenergiArsserieBindning` som bara är sann för Stockholm. Samma gamla definition
upprepas vid rad 935–952. Fillistan rad 371 kallar hela `calcResult`-vägen oförändrad trots
att samma dokument säger att dess interna argumentbyggnad ändras.

Inventeringen har motsvarande äldre funktionskropp vid rad 3150–3168 följd av den nya
rättelsen, kallar `beraknaArsprodukt` ”den enda produktentrypunkten för Stockholm” vid rad
3222–3225 och motiverar Sandvikens `false` med den gamla bindningen vid rad 3620. Två nya
Lidköpingshänvisningar vid rad 4027 och 4061 pekar dessutom på §6a.5 fast förmågekontraktet
ligger i §6a.4.

**Begärd rättning:** ersätt den gamla normativa texten i stället för att lägga en ny
rättelse efter den. Överallt ska förmågan läsas från det explicita policyfältet, Lidköping
ska ingå i tabeller och produkttester, och ”oförändrad” får bara avse det publika
returkontraktet/resultatbeteendet.

### P1 — Batch 5d saknar den verkliga katalogfilen och motsäger sitt genomförandescope

Batchplan rad 461 placerar ”katalogens `adjustments`-post” i `generera.py`. Posten bor i
`Fjarrvarmetariffer/optimate-fjarrvarme-2026.json`; `katalog.py` läser den och
`generera.py` serialiserar redan dataklassen. Nästa rad säger samtidigt att katalog-JSON
inte ändras av etappen. Det är sant om meningen avser den nuvarande dokumentationscommitten,
men falskt för den framtida implementationsbatch som fillistan beskriver: motortypen kan
inte nås utan en katalogpost.

**Begärd rättning:** skilj tydligt den dokument-only V17/V18-committen från den framtida
Batch 5d-implementationen. Lägg den verkliga katalog-JSON-filen, eventuella
`katalog.py`-schema-/grindändringar och explicita Python-/TypeScripttester i fillistan.
Aktivering ska fortfarande ske först efter granskad kod och gröna tester, i en fokuserad
senare commit.

## P2-fynd

- `stodjer_aktuell_arskostnad` används i V17 även som negationen av
  ”stöder besparing”. Det råkar fungera för Stockholm och Lidköping i dag men låser en
  framtida tariff som kan stödja båda produkterna. V18 bör skilja förmågorna deklarativt,
  exempelvis med ett separat `stodjer_besparing` eller `besparingsmodell`.
- Batch 5d bör namnge de konkreta testfilerna: Pythonregistrering/exakt typmängd,
  justeringsberäkning, TypeScriptparitet, direkt fasadvalidering, produktbegränsning och
  katalog→policy→fasad→motor→`Kostnad.justering`.

## Godkända delar och verifieringar

- Den föreslagna seriekanalen är arkitekturellt rimlig: justeringen körs årsvis och hela
  tolvmånadersserien kan föras i ett anrop till justeringsmotorn.
- Kanonisk `type`-diskriminator, Pythonregistrering och TypeScript-/Pythontransporten till
  `Kostnad.justering` ska bevaras i V18.
- Ett explicit policyfält för aktuell årskostnad är rätt väg, även om det behöver skiljas
  från besparingsförmågan.
- Lidköpings två produkter förblir källgodkända och `ready_to_implement`. Ingen Tm-serie
  får gissas eller hårdkodas.
- Dispositionen förblir 7 implementerade, 57 redo och 28 externt blockerade av totalt 92.
- Committerna `df20de4` och `497fbfc` ändrar endast dokumentation. Produktrepoerna står
  kvar på `enkey-agents@fd8f8da` och `neptune_academy@f1df177`; ingen tariff är aktiverad.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v18.md` och `batchplan-v18.md`; ändra inte V17 i efterhand.
2. Gör Tm-proveniensen kompatibel med det verkliga käll-/noggrannhetskontraktet och lägg
   till en maskinläsbar källattestering; behåll intern `noggrannhet: 'snapshot'`.
3. Gör min/max/heltalsvalidering elementvis och identisk i förkontroll och ordinarie
   statusvalidator i båda språken; testa direkta fasadanrop.
4. Definiera och använd ett enda konkret produktbegränsningsfel med UI-mappning och test.
5. Ersätt alla äldre normativa capability-/”oförändrad”-stycken och rätta §6a.4-
   hänvisningarna; lägg till Lidköping i tabeller och produkttester.
6. Rätta Batch 5d-fillistan med den verkliga katalog-JSON-filen, schema/grind vid behov
   och namngivna testfiler. Skilj dokumentationsscope från framtida implementation.
7. Separera aktuell-årskostnadsförmåga från besparingsförmåga så att framtida tariffer kan
   stödja båda utan kodundantag.
8. Bevara V17:s godkända motortransport, Lidköpings källstatus, räkningen 7/57/28 och
   Åkermannen-underlaget. Lägg denna granskning i en fokuserad lokal dokumentationscommit,
   logga verklig hash/tid och stanna för omgranskning. Ändra ingen produktkod,
   tariffaktivering eller push.
