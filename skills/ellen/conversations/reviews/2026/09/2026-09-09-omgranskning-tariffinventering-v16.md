---
review_id: "2026-09-09-010"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v16.md
  - Fjarrvarmetariffer/batchplan-v16.md
  - Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md
  - skills commits d63bcbb5537a81e9f08c4dd7ac3437fcd69fff33 and d75ea6beb1ca837944527ec8f725215d8613023d
reviewed_heads:
  skills: "d75ea6beb1ca837944527ec8f725215d8613023d"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-007"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v16 och batchplan v16

## Bedömning

V16 löser de två uttryckliga V15-blockeringarna i huvudtexten. Den nya
`beraknaArsprodukt`-kroppen använder rätt prispostfält, byggd `IndataPost`-karta, två
typade policyfel, rätt årsfasadsignatur och säker null-avsmalning. Det additiva
`policyFalt`-fältet finns också på `BesparingsvardeArgs` i inventeringens normativa
sektion. Lidköpings källstatus, två statusflyttar, Åkermannen-tilläggen och räkningen
7/57/28 av 92 är korrekta.

V16 kan ändå inte godkännas för implementation. Lidköpings nya beräkningsfunktion är en
fristående skiss som inte är kopplad till den verkliga kostnadsmotorn: dagens årsfasad
avvisar de tre serierna innan motorn anropas, låg nivå dispatchar på katalogfältet `type`
men skissen använder `typ`, och varken Python- eller TypeScriptmotorns
justeringsregister/anropssignatur finns i batchens fillista. Den primära produkten
”uppskattad aktuell årskostnad” är dessutom bara nåbar för en policy med Stockholms
`kallenergiArsserieBindning`; Lidköping får inte den förmågan. Den återstående
besparingsvägen återanvänder i stället samma `Q/T/Tm` före och efter och saknar en
källförsvarbar transformationsregel.

Tre ytterligare kontraktsluckor måste stängas i V17: strikt `Tm > 0` är ännu ett uppskjutet
antingen/eller-beslut, batchplanen säger fortfarande på två ställen att
`BesparingsvardeArgs` är oförändrad, och Tm beskrivs samtidigt som icke fritt kundfält och
som en vanlig serieinmatning i UI. Ingen produktkod, tariffdata, aktivering eller push är
godkänd.

## P1-fynd

### P1 — Lidköpings tre serier når inte den verkliga tariffmotorn

Inventeringen rad 3663–3711 definierar `SignedMonthlyFlowAdjustment` och två fristående
beräkningsfunktioner i/vid `resultatkontrakt.ts`, men visar inget anrop som kan nå dem.
Den verkliga kedjan fungerar annorlunda:

1. `beraknaArskostnadMedKontrakt` i `resultatkontrakt.ts` rad 576–586 och Pythonfasaden
   rad 600–609 bygger motorns `falt` som skalära tal och **kastar uttryckligen för varje
   icke-kapacitetsbunden serie**. Alla Lidköpings `Q_m`, `T_m` och `Tm_m` stoppas alltså
   innan `_arskostnadForKontraktfasad`/`_arskostnad_for_kontraktfasad` anropas.
2. Den riktiga justeringsmotorn dispatchar katalogposter via `post.type` i
   `fjarrvarme.ts` rad 725–733 och `post["type"]` i `faktura.py` rad 628–632. V16:s nya
   TypeScript-/Pythonskisser använder i stället diskriminatorn `typ` och beskriver ingen
   serialisering mellan formerna.
3. Python kräver att typen finns i både `JUSTERINGSTYPER` och `_JUSTERING_BERAKNING`;
   TypeScript kräver en post i `JUSTERING_BERAKNING`. Batch 5d rad 393–408 nämner ny
   motorkod men listar inte `justeringar.py`, `faktura.py` eller `fjarrvarme.ts`, och
   specificerar inte hur serierna förs genom fasaden till justeringsfunktionen.

Som planen står nu kan en implementation antingen kasta ”kan inte bindas ... som en
serie” eller lägga en katalogpost som grinden/motorn betraktar som okänd. Formeln kan inte
bidra till `Kostnad.justering` och därmed inte till årsbelopp eller momsberäkning.

**Begärd rättning:** V17 ska välja och skriva ut en komplett, speglad integrationsväg.
Minimikrav:

- katalogposten och båda motorerna använder den kanoniska diskriminatorn
  `type: "signed_monthly_flow_adjustment"`;
- `JUSTERINGSTYPER`, `_JUSTERING_BERAKNING` och TypeScripts `JUSTERING_BERAKNING`
  uppdateras i samma batch;
- policyn får explicita, validerade bindningar från justeringspostens tre fältnamn till
  tre `number_series`-krav, eller ett lika tydligt generiskt bindningskontrakt;
- årsfasaden extraherar just dessa serier innan den skalära `falt`-loopen och för dem till
  den verkliga kostnadsmotorn, alternativt lägger fasaden till justeringen i
  `KontraktResultat.kostnad` med korrekt moms och samma Python/TS-semantik;
- Batch 5d:s fillista och tester täcker hela vägen katalog → policy → fasad → motor →
  `Kostnad.justering`, inte bara ett direkt hjälpfunktionsanrop.

### P1 — Lidköpings aktuella årskostnad är onåbar och besparingsvägen saknar före/efter-regel

V16 definierar `stodjerAktuellArskostnad` som
`gated?.policy.kallenergiArsserieBindning !== undefined` (inventeringen rad 3091–3107;
batchplanen rad 257–270). Det är avsiktligt sant endast för Stockholm. Batch 5d lägger
bara till `signed_monthly_flow_adjustment` och ändrar inte förmågekontraktet. Därför döljer
UI:t valet ”aktuell årskostnad” för Lidköping och `calcResultForOnskadTyp` blockerar ett
direktanrop, trots att just den uppskattade årskostnaden är projektets primära mål.

Den enda kvarvarande vägen är då `calcResult` → `beraknaBesparingsvardeKontrakt`. Den
funktionen använder samma `IndataPost`-karta för före och efter. V16 konstaterar själv
detta för Stockholm vid rad 2993–3007 och blockerar besparing eftersom en verklig serie
inte kan transformeras utan stöd. Lidköping har samma problem: om `Q_m`, `T_m` och `Tm_m`
hålls oförändrade medan energin minskar blir flödesjusteringen identisk i båda syntetiska
fakturorna och tar ut sig ur besparingen. Ingen källa visar att Optimate lämnar kundvolym
och kundavkylning oförändrade, eller hur de annars ska skalas.

Det strider mot Ellens tariffregel att endast kostnadskomponenter som åtgärden faktiskt
påverkar får räknas som besparing. Ett tyst nollbidrag från flödesdelen kan både över- och
underskatta kostnadsnyttan.

**Begärd rättning:** gör förmågan till ett explicit produkt-/policykontrakt i stället för
en indirekt kontroll av en Stockholmsspecifik bindning. Lidköping ska stödja ETT anrop för
”uppskattad aktuell årskostnad” med de tre observerade serierna och utan syntetiskt
efterfall. Blockera tills vidare Lidköpings besparingsväg med ett typat produktbegränsningsfel,
precis som Stockholm, tills ett separat före/efter-kontrakt eller en källförsvarbar
transformationsregel finns. Testa minst Lidköping aktuell årskostnad = ett fasadanrop samt
Lidköping besparing = explicit blockering. Detta ändrar inte de två produkternas
`ready_to_implement`-status; källunderlaget är komplett, men implementationsplanen måste
göras körbar.

### P1 — Fail-closed-löftet för `Tm_m = 0` har ingen vald implementation

Inventeringen rad 3725–3736 säger först att `Tm_m <= 0` ska ge
`invalid_policy_fields/'min'`, men konstaterar därefter korrekt att dagens `minVarde` är
inkluderande och lämnar valet mellan en ny strikt gränsvariant och en kontroll i
beräkningsfunktionen till Batch 5d. Batchplan rad 398–400 lovar resultatet utan att välja
mekanism. Det är inte implementeringsklart, och en sen motorkontroll kan dessutom ge en
generisk `Error` i stället för det utlovade fältnära `invalid_policy_fields`.

**Begärd rättning:** välj en enda deklarativ lösning i V17. Rekommenderat är ett generiskt
`min_exklusiv`/`minExklusiv` på `KravPost`, endast tillåtet tillsammans med `minvarde`/
`minVarde`, speglat genom konstruktion, Python→TS-serialisering,
`forkontrolleraPolicyIndata` och den ordinarie statusvalidatorn. Sätt `Tm_m` till
`minVarde: 0, minExklusiv: true`; behåll `Q_m` som inkluderande `minVarde: 0`. Testa
negativt, noll och positivt element i båda språken samt att noll stoppas före divisionen
med orsak `'min'`.

### P1 — V16 säger fortfarande att det nyss ändrade interfacet är oförändrat

Batchplanens inledning rad 23–26 och Batch 0 rad 158–178 anger rätt beslut:
`BesparingsvardeArgs` får `policyFalt` additivt och `calcResult` ändrar sin interna
argumentbyggnad men behåller offentligt beteende. Samma dokument säger dock motsatsen:

- rad 305–309: ”`BesparingsvardeArgs` självt förblir OFÖRÄNDRAT”;
- rad 917–919: ”`calcResult` självt OFÖRÄNDRAT och `BesparingsvardeArgs` självt
  OFÖRÄNDRAT”.

Det är exakt motsägelsen granskning 007 beställde bort. En utvecklare som följer
Batch 7-fillistan kan utelämna den typade `policyFalt`-transport som Lidköping och 41 andra
planerade kontraktstariffer behöver.

**Begärd rättning:** sök igenom båda V17-dokumenten och använd ett enda språk överallt:
`BesparingsvardeArgs` ändras additivt; `beraknaBesparingsvardeKontrakt` ändrar intern
indatabyggnad; `calcResult` behåller sitt publika returkontrakt och resultatbeteende men
ändrar intern argumentbyggnad till `argsFranInputs`. Ordet ”oförändrat” får bara syfta på
den publika utdata som verkligen är oförändrad.

## P2-fynd

- `Tm_m` sägs vid inventeringen rad 3719–3721 inte få skickas in fritt av kunden, medan
  Batch 5d rad 403–405 visar tre vanliga serieinmatningar i UI och
  `byggIndataFranPolicy` rad 2286–2293 märker varje formulärvärde som `supplier_value`.
  V17 ska välja ett spårbart kontrakt: antingen får användaren transkribera ett värde från
  faktura/direkt leverantörsbesked och resultatet märks `snapshot` med tydlig källhjälp,
  eller så kommer Tm från en separat betrodd runtimekälla och är inte redigerbart. Ett
  fritt tal får inte automatiskt påstås vara ett verifierat leverantörsvärde.
- Tio Lidköpingsreferenser pekar felaktigt på Jönköpings §6a.6 i stället för Lidköpings
  §6a.7, bland annat inventeringen rad 63, 1380–1415, 1935, 3395 och 3835. Hänvisningen
  vid rad 3640 till ”§6a.6-mönstret ovan” är däremot avsiktlig och ska behållas.
- `git diff --check 2326adc..d75ea6b` rapporterar en ny blankrad vid EOF i
  `2026-09-09-inventering-akermannen-fakturaarkiv.md`. Rätta i V17-committen.

## Godkända delar och verifieringar

- De sex konkreta typ-/signaturfelen från granskning 007 är rättade i
  `beraknaArsprodukt`-skissen. Inga `as any`-genvägar återstår i den fältnära felvägen.
- Exakt 78 bastariffrubriker finns. Dispositionerna är 7 implementerade, 47 redo och 24
  blockerade. Varianttabellen redovisar 10 redo och 4 blockerade; summan 7/57/28 av 92
  stämmer med batchplanen.
- De två Lidköpingstariffernas källfrågor är fortsatt lösta enligt granskning 006 och ska
  förbli `ready_to_implement` i V17. Ingen faktisk `Tm`-serie får gissas eller hårdkodas.
- Åkermannens 22 PDF-filer/20 unika perioder, augustifallet och maj–juli-avräkningskedjan
  är korrekt införlivade som framtida, sanitiserade regressioner. Den frysta baslinjen
  ändras inte.
- Committerna `d63bcbb` och `d75ea6b` ändrar bara plan-/verifierings-/konversationsdokument.
  Produktrepoerna står kvar på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`; ingen tariff är aktiverad.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v17.md` och `batchplan-v17.md`; ändra inte V16 i efterhand.
2. Skriv Lidköpings kompletta katalog→policy→fasad→motor-kedja enligt första P1-fyndet,
   med kanonisk `type`-diskriminator, tre seriebindningar, riktiga motorregister och
   fullständig fillista.
3. Gör ”aktuell årskostnad” explicit nåbar för Lidköping och blockera dess besparing tills
   en försvarbar före/efter-regel finns, enligt andra P1-fyndet.
4. Välj och serialisera en enda strikt `Tm > 0`-mekanism som ger fältnära
   `invalid_policy_fields/'min'` före division.
5. Ta bort alla kvarvarande `BesparingsvardeArgs`-/`calcResult`-motsägelser och precisera
   Tm-proveniensen.
6. Rätta Lidköpings §6a.6→§6a.7-hänvisningar och blankraden som `diff --check` hittar.
7. Bevara V16:s rättade årsprodukt, parser, policyfälttransport, räkning 7/57/28,
   Lidköpings källgodkännande och Åkermannen-underlag oförändrade i sak.
8. Lägg denna granskning i nästa fokuserade dokumentationscommit, logga verklig hash/tid
   och stanna för omgranskning. Ändra ingen produktkod, tariff-JSON, genererad fil eller
   aktiveringsgrind och pusha inte.
