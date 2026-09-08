---
review_id: "2026-09-08-006"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v6.md
  - Fjarrvarmetariffer/batchplan-v6.md
  - skills commit 1a429dce29d10c59c626721705556bc0445ec76b
  - skills correction commit 058ffb4ca0022813abd6e745ccff0ece6cce31fd
reviewed_heads:
  skills: "058ffb4ca0022813abd6e745ccff0ece6cce31fd"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-005"
---

# Omgranskning av tariffinventering v6 och batchplan v6

## Bedömning

V6 rättar flera viktiga V5-fel. Sundsvall Indal behandlas nu som en kontraktsgated
MWh-produkt, Stockholm-katalograden ska inte skapa ett andra UI-val, Falu får ett planerat
maxkrav och request-livscykeln har fått ett valt tariff-ID-spår. Kontrollmängden är fortsatt
formellt komplett: 78 bastariffer och 14 varianttäckningar, totalt 92. V6-committen är
avgränsad till dokumentation och `git diff --check ce53f75..058ffb4` är rent.

Planen kan ändå inte godkännas för implementation. Den största kvarvarande luckan är att
katalogens eget integrationskontrakt kräver leverantörsbekräftat band för 42 av de 45
`ready_to_implement`-bastarifferna, medan V6 bygger bandkontraktet endast för Borlänge och
C4. Dagens konvertering kastar dessutom bort källans band-ID:n, och V6:s föreslagna
jämförelse låter den osäkra automatiska intervalltolkningen överpröva leverantörens besked.
Stockholm-planen försöker samtidigt lägga två policyer med samma nyckel i ett vanligt
`dict`, request-planen passar inte den angivna `grind()`-signaturen och alla 45 ready-rader
står fortfarande kvar som `investigation.status: utreds` utan en faktisk mutationsplan.

Det krävs därför en avgränsad V7-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — bandkontraktet måste omfatta 42 ready-tariffer, inte två

Katalogens normativa integrationskontrakt säger: "Originalintervall bevaras. Välj
`supplier_confirmed_band_id`; intervallsträngar får inte automatiskt parsas till
produktionsgränser." Maskinell kontroll visar att 73 av 78 katalograder och **42 av de 45
ready-raderna** bär `band_selection: supplier_confirmed_band_id_required`. De enda tre
ready-undantagen är Finspång, Mälarenergi 2–4 lägenheter och Sundsvall Indal.

V6 §6a.2 använder däremot det nya bandfältet endast för Borlänge och C4 och säger att
"övriga 40" bara behöver en ny policy. Det skulle åter aktivera automatisk bandtolkning
för nästan hela kontrollmängden i strid med katalogkontraktet.

Dagens data- och motorväg kan inte heller genomföra den valda lösningen:

- Python `Varde` är `float | Sequence[float]` och TypeScript `Varde` är
  `number | readonly number[]`; `IndataPost` kan alltså inte bära ett strängformat band-ID.
- `till_prisar()` omvandlar `capacity.bands` till `nivaer` med endast `min`, `max`, fast
  avgift och rörligt pris. Källans `bands[].id` bevaras inte, trots att V6 vill validera mot
  `prisar.kapacitet.nivaer[].id`.
- V6 vill först bekräfta band-ID och sedan kasta om det inte överensstämmer med vad
  `_niva()` själv väljer. Det gör leverantörsbeskedet verkningslöst i exakt de tvetydiga
  gränsfallen: den automatiska parsern väljer i dag Borlänge band 5 vid 501 kW och C4 band
  6 vid 500 kW. Om leverantören bekräftar angränsande band skulle V6 blockera det korrekta
  beskedet i stället för att använda det.

**Begärd rättning:** V7 ska inventera och ange band-ID-kontraktet för samtliga 42 berörda
ready-rader. Bevara källans band-ID genom `katalog.py`/`till_prisar`, generator och båda
motorerna. Lägg till en typad sträng-/enumväg i Python, TypeScript, UI och serialisering.
Det bekräftade bandet ska direkt välja den prisrad som används; en automatiskt parsad
intervallsträng får inte överpröva valet. Om numerisk rimlighetskontroll önskas måste den
bygga på källverifierade normaliserade gränser och uttryckligen hantera öppna
gränspunkter, inte återinföra parsern som sanningskälla. Saknat eller okänt band-ID ska
blockera.

### P1 — Stockholm kan inte ha två policyer med samma tariff-ID i dagens register

V6 föreslår en ny separat `Tariffpolicy` för `stockholm-exergi-2026` med
`annual_forward`, vid sidan av den befintliga policyn för `monthly_invoice`.
`POLICYREGISTER` är emellertid `dict[str, Tariffpolicy]`: två poster med samma nyckel kan
inte samexistera; den ena skriver över den andra. Den befintliga Stockholm-policyn har
dessutom bara månadskrav (`kravs_for=("monthly",)`) och täckningen `monthly_invoice`.

Det planerade `ADAPTERREGISTER: dict[str, str]` bevisar inte heller att någon årsadapter
finns. Det mappar bara katalog-ID till ett annat **tariff-ID** och används för att hoppa
över katalograden. V6 kallar felaktigt `stockholm-exergi-2026` leverantörsfils-ID; filens
leverantörs-ID är `stockholm-exergi`, medan `stockholm-exergi-2026` är tariff-ID:t.
Leverantörsfilens nuvarande `validated`-grind kräver endast `monthly_invoice`, så ett rent
dedupliceringshopp skulle kunna passera utan `annual_forward`-täckning eller årsadapter.

**Begärd rättning:** välj en faktiskt representerbar modell. Rekommenderad väg är en enda
sammanhållen policy för `stockholm-exergi-2026` med båda täckningsändamålen och
ändamålsspecifika krav, alternativt en genomgående registermodell nycklad på
`(tariff_id, ändamål)`. Adapter-/dedupliceringsposten ska typat ange katalog-ID,
`provider_id: stockholm-exergi`, `tariff_id: stockholm-exergi-2026`, obligatorisk
`annual_forward`-täckning och den adapter som produktdispatch faktiskt anropar. Generatorn
får hoppa över katalogdubbletten först när exakt en målprodukt samt policy och årsadapter
är verifierade; saknad eller stale mapping ska kasta. Preflighten ska redovisa 44
katalogaktiveringar plus en leverantörsfilsaktivering, inte låtsas att alla 45 går genom
samma `grind()`-väg.

### P1 — faktisk utredningsstatus och request-API saknas fortfarande

Maskinell kontroll av de 45 ready-raderna visar:

- 45/45 har fortfarande `investigation.status: utreds`;
- 45/45 har `production_ready: false`;
- 45/45 saknar `contract_required`.

V6:s steg 1 kräver att status inte längre är `utreds`, men dokumentet anger ingen konkret
tariffvis mutation (`lost`, `null` eller annan beslutad representation). Därmed skulle
samtliga ready-rader fortfarande stoppas före den planerade policygrinden.

Request-API:t är också ofullständigt. V6 föreslår `oppna_tariff_ider(katalog)` men behåller
en `grind(tariff, utredda)` som bara får tariffen och en enda mängd. Den kan inte själv
anropa den nya katalogfunktionen eller skilja tariff-ID:n från medlem-ID:n på det sätt
texten beskriver.

**Begärd rättning:** definiera en exakt statusövergång och katalogmutation för varje av de
44 katalograder som verkligen ska aktiveras; Stockholm-dubbletten redovisas separat.
Ange samtidigt `contract_required: true`, kvarvarande `issues` och request-ID-livscykel per
rad. Välj sedan ett enda körbart request-kontrakt och följ det genom schema, laddning,
`godkanda()`, `grind()` och tester. En robust modell är att först lösa varje öppen request
till en mängd blockerade tariff-ID:n och endast låta `grind(tariff, blockerade_tariff_ider)`
jämföra tariff-ID; medlemsomfattande requests expanderas uttryckligt vid laddning.

### P1 — Umeås grind/policykoppling är inte implementeringsbar som beskriven

V6 säger att `grind()` endast ska acceptera `post_multiplier` när den namngivna
`kapacitet_multiplikator_bindning` finns i tariffens policy. Samma dokument konstaterar
korrekt att `grind()` saknar policyparameter eller registeråtkomst. Ingen arkitektur väljs
för hur kontrollen då ska göras, vilket lämnar valet mellan fortsatt blockering och ett
hårdkodat/allmänt undantag.

**Begärd rättning:** skilj den strukturella kataloggrinden från den sammansatta
aktiveringsgrinden, eller ge en uttryckligt typad capability-/policyberoende kontroll till
en ny aktiveringsfunktion. Den nakna grinden får inte godkänna okända multiplikatorer.
Beskriv hur `post_multiplier` bevaras genom `till_prisar`, binds till `B` och används av
båda motorerna.

Intervallet behöver också korrigeras innan kodning. Den publicerade mellanformeln
`1,34×U+0,330` ger `1,40066` vid `U=0,799`; ett absolut tak `maxvarde=1,4` kan därför
avvisa ett legitimt leverantörsvärde beroende på leverantörens avrundning. V7 ska utgå från
den faktiska precision leverantören redovisar eller använda hela det formelhärledda
intervallet med dokumenterad avrundningsregel — inte anta ett exakt 1,4-tak.

### P1 — TypeScript-serialiseringen är uttryckligen fel beskriven

V6 §6a.1 säger att `policyFranGenererad` inte behöver ändras eftersom
`dataclasses.asdict` serialiserar `maxvarde`. Det gäller bara Python-JSON-sidan.
TypeScripts `policyFranGenererad()` mappar fälten manuellt och läser i dag `minvarde` och
`heltal`, men inte `maxvarde`. Utan en explicit `maxVarde: k.maxvarde`-mappning tappas
Falu-gränsen tyst i frontend. Detsamma gäller den nya
`kapacitet_multiplikator_bindning`, som måste läsas in uttryckligen till
`kapacitetMultiplikatorBindning`.

**Begärd rättning:** lägg alla Python-/TypeScript-fält, JSON-namn, deserialisering,
validering och negativa tester i V7:s fil- och kontraktsplan. Inga nya genererade fält får
förlita sig på automatisk TypeScript-mappning som inte finns.

### P1 — per-produktmatrisen motsäger V6:s egna beslut

Minst tre rader är kvar från V5 och skulle ge fel arbetsorder:

- Stockholm-raden säger fortfarande namngivet kataloggrindundantag och ändring i
  `katalog.py`, trots §6a.4:s leverantörsfilsväg där katalograden ska förbli blockerad.
- Sundsvall Indal säger fortfarande `mwh, kr och schablon` samt legacy utan kontrakt,
  trots batch 2:s korrekta beslut om kontraktsgated MWh-only.
- Umeå-raden beställer fortfarande test av tre `U`-intervall, trots §6a.3:s beslut att
  motorn bara tar emot leverantörens `B`.

**Begärd rättning:** synkronisera varje berörd produktrad, §6/§6a, varianttabellen och
batchplanen till en enda normativ arbetsorder. Sök dessutom alla 42 bandtariffer så att
ingen rad fortsätter beskriva automatiskt effektband eller enbart numerisk effekt.

## P2-fynd

- V6 säger att `POLICYREGISTER` innehåller "de 7 redan implementerade + Sandviken".
  Registret har i verkligheten tre poster: Stockholm 2025, Stockholm 2026 och Sandviken.
  De sex övriga legacyprodukterna saknar policy. Slutsatsen att nya katalogprodukter
  behöver policy är riktig, men nulägesbeskrivningen ska rättas.
- Batchfillistorna är inte färdigräknade trots sammanfattningen: batch 1 tar bort R11 men
  saknar requestfilen; batch 5a tar bort R05/R12/R13 men saknar requestfilen och nämner
  inte R13 konsekvent; batch 5b tar bort R04/R15 utan requestfil; batch 5c omskopar R03
  utan requestfil. Batch 4 använder åter den icke existerande förkortningen
  `justeringar.py/.ts`; de verkliga filerna är `justeringar.py` och inlinekod i
  `fjarrvarme.ts`.
- V6:s innehållscommit är `1a429dc`; HEAD `058ffb4` rättar självreferensen i loggen. Den
  senare korrigeringen saknas i sessionsloggens ändringshistorik och `last_updated` står
  kvar på 15:32, före båda committarna. Nästa leverans ska logga hela granskade
  commitintervallet utan att skriva om äldre historik.

## Beslut på V6:s öppna frågor

1. **Jönköpings accessavgift:** Roberts redan beslutade mål innebär att en fakturerbar,
   källkänd och kundkänd avtalsuppgift ska kunna ingå. Modellera därför avgiften som ett
   synligt obligatoriskt val på Jönköpings basprodukt med de verifierade värdena
   0/10/25/50 kr per månad; inget standardvärde och okänt val ska blockera. Exponera inte
   en dubblettprodukt. Varianttäckningen flyttas till `ready_to_implement`, vilket ändrar
   variantfördelningen till 10 ready/4 blocked och totalsumman till 7 implementerade,
   55 ready och 30 blockerade av 92.
2. **E.ON/Navirum:** batch 3b efter grundformeln är godkänd som ordning.
3. **Batch 5:** indelningen 5a/5b/5c är godkänd som arbetsstorlek, men först efter att det
   gemensamma band-ID-kontraktet för samtliga berörda produkter är specificerat.
4. **Kraftringen:** en parametriserad motortyp är godkänd om regelvarianten är en explicit,
   typad discriminator och okänd/saknad variant blockerar. Den får inte härledas implicit
   från leverantörs-ID.

## Verifieringar

- `skills@1a429dc` och korrigeringscommitten `058ffb4` ändrar endast dokumentation; ingen produktkod, tariffdata eller
  genererad frontendfil ingår.
- `git diff --check ce53f75..058ffb4` är rent. Lokal `main` är inte pushad; `origin/main`
  ligger fortsatt på `62181a1` vid granskningen.
- Inventeringen innehåller exakt 78 unika katalog-ID:n, varianttabellen 14 ID:n och
  preflighttabellen exakt de 45 ready-ID:na.
- Strukturerad kontroll mot katalog-JSON gav 45/45 ready med `status: utreds`, 45/45 med
  `production_ready: false`, 45/45 utan `contract_required` och 42/45 med
  `supplier_confirmed_band_id_required`.
- `POLICYREGISTER`, `katalog.py`, `generera.py`, `resultatkontrakt.py`, `faktura.py` och
  TypeScript-spegeln lästes på de pinnade produkt-HEAD:arna ovan.
- Ändrade dokuments relativa länkar och dispositionsmängder kontrollerades; inga brutna
  länkar eller dubbletter hittades.
- Inga fulla produkttester kördes eftersom V6 enbart ändrar dokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v7.md` och `batchplan-v7.md`; ändra inte V6 i efterhand.
2. Gör band-ID till ett riktigt end-to-end-kontrakt för alla 42 berörda ready-bastariffer,
   inklusive strängtyp, bevarade ID:n, direkt bandval, UI, serialisering och negativa test.
3. Ange verklig utrednings-/request-/`contract_required`-mutation samt ett körbart
   request-API för var och en av de 44 katalogaktiveringarna.
4. Ersätt Stockholms omöjliga dubbelpolicy med en representerbar ändamålsmodell och en
   typad, fail-closed adapter-/dedupliceringsgrind för leverantörsfilens årsprodukt.
5. Slutför Umeås policyberoende aktiveringsgrind, multiplikatorflöde och källriktiga
   B-gräns/avrundning; rätta TypeScript-deserialiseringen för alla nya fält.
6. Synkronisera hela per-produktmatrisen och batchernas verkliga fillistor med besluten.
7. Tillämpa besluten ovan, särskilt Jönköpings accessavgift och den nya 55/30-fördelningen.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `058ffb4`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
