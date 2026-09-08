---
review_id: "2026-09-08-008"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v8.md
  - Fjarrvarmetariffer/batchplan-v8.md
  - skills commits fd372a237fc4bdd5dc95782c6ebb57b77411292b and b7790ca354659ef26f89c79f26a38ab6b4559ece
reviewed_heads:
  skills: "b7790ca354659ef26f89c79f26a38ab6b4559ece"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-007"
---

# Omgranskning av tariffinventering v8 och batchplan v8

## Bedömning

V8 löser flera viktiga delar av V7-granskningen. Kraftringens regelvariant har nu ett
domänriktigt namn, en serialiseringsrad och en beskriven motorparameter. Jönköpings
0/10/25/50-val har fått en riktig domänregel i stället för enbart UI-val. Stockholm ska
dispatchas via den befintliga `_kraver_kontrakt`-mekanismen och adapterkontrollen har
flyttats till den råa katalogen. Kontrollmängden är fortsatt sammanhängande: 78
bastariffer, 14 varianttäckningskrav och fördelningen 7 implementerade, 55 redo samt 30
blockerade.

Planen är ändå inte implementeringsklar. Umeås andra grindförsök kan förbruka den första
avslagsorsaken utan att kontrollera fel som låg dolda bakom den. `KravPost.vardetyp`
diskriminerar kravet, men `IndataPost.varde` kan fortfarande inte typmässigt bära ett
band-ID och seriegrenen är inte strikt. Den föreslagna produktingången saknar både
serieindata och den UI-metadata som behövs för att skapa band-, enum- och seriefält.
Stockholms årsmodell växlar dessutom mellan 17 skalärer och två serier, saknar statiska
motorbindningar och definierar inte hur kallenergin förändras mellan kalkylens före- och
efterfall. Adapterpreflighten använder inte sitt `provider_id` och kan inte utföra två av
de tester planen utlovar.

Det krävs därför en avgränsad V9-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — Umeås andra försök hoppar över bakomliggande grindfel

V8 §6a.3 låter `godkanda()` anropa `grind()` och, endast när dess första returvärde är
`"kapacitetsformel med multiplikator"`, lägga till raden om
`kontrollera_kompositgrind()` godkänner multiplikatorbindningen. Dagens `grind()` returnerar
det första fyndet. Kontrollen av `post_multiplier` ligger före kontrollen av `issues` och
`okand_justering()`. En Umeå-rad med korrekt B-bindning men kvarvarande okänd issue eller
okänd `asymmetric_flow_difference` läggs därför till utan att dessa senare kontroller
någonsin körs. Det motsäger V8:s kommentar att varje annat fynd faller igenom och förblir
blockerat.

Pseudokoden introducerar samtidigt `godkanda(katalog, policyregister=POLICYREGISTER)`, men
V8 säger att `bygg_ts_fran_katalog()` inte behöver ändras. Generatorn har redan ett
injekterbart `policyregister` och anropar i dag `godkanda(katalog)` utan registret. Den
sammansatta grinden skulle då läsa det globala registret, medan den efterföljande
`kontrollera_aktiveringsgrind(..., register=policyregister)` läser det injicerade. Ett
testregister och produktregistret får två olika sanningar.

**Begärd rättning:** konsumera endast multiplikatorfyndet och kör därefter samtliga
återstående strukturella kontroller, exempelvis genom en capability-medveten grind eller
genom att återköra grinden på en säker kopia där endast den verifierade
`post_multiplier`-spärren är kvitterad. `bygg_ts_fran_katalog()` och `main()`s räkning ska
föra samma explicita policyregister till `godkanda()`. Testa att Umeå passerar först när
issue-rättelsen, den kända justeringstypen och B-bindningen alla finns; lägg tillbaka en
okänd issue respektive justering och bevisa att båda blockerar. Testa även ett injicerat
register skilt från det globala.

### P1 — värdediskriminatorn är inte ett komplett typkontrakt

V8 avvisar med rätta en oreglerad global strängvidgning, men den föreslagna lösningen
ändrar bara `KravPost`. `IndataPost.varde` är fortfarande typad med `Varde`, som i dagens
Python är `float | Sequence[float]` och i TypeScript `number | readonly number[]`. En
`band_id`-post med strängvärde kan alltså inte konstrueras typkorrekt utan att även ändra
indatapostens typ.

`number_series` är inte heller en verklig diskriminator enligt den beskrivna valideringen.
V8 säger att `number` och `number_series` använder den befintliga valideringen oförändrad.
Den accepterar både skalär och serie; dagens `rullande=True` tillåter en serie men kräver
inte en. Ett fält märkt `number_series` kan därför fortfarande få ett skalärt tal, medan
ett `number`-fält först avvisar en serie genom en separat `rullande`-kontroll. Det finns
inte heller ett deklarativt kardinalitetsfält för Stockholms exakt 12 respektive 5 värden.

**Begärd rättning:** specificera en diskriminerad `IndataPost`/värdeunion i båda språk,
inte bara ett fält på `KravPost`. Korsvalideringen ska kräva exakt skalärt ändligt tal för
`number`, en icke-tom serie av ändliga tal för `number_series` och en icke-tom sträng för
`band_id`. Lägg ett generiskt kardinalitetskontrakt, exempelvis `antal_varden`, på
seriekrav; undvik fältnamns- eller Stockholm-hårdkodning i valideraren. Behåll stöd för
E.ON/Navirums rullande men skalära leverantörseffekt genom att modellera det som
`vardetyp="number", rullande=True`, inte genom att låta `number_series` acceptera skalär.
Testa alla korsade feltyper och serialiseringsrundturen.

### P1 — produktingången har ingen genererad UI-väg för policykraven

V8 §6a.2 utgår från att kalkylatorsidan redan samlar tariffspecifik indata i ett fritt
`falt`-objekt. Det stämmer bara för dagens numeriska `indatafalt`. Dessa genereras av
`indatafalt_for()` från kända justeringar och kapacitetsformen `kWh/day`; UI:t renderar
varje post som `type="number"` och bygger `Record<string, number>` via `parseFloat`.
`KalkylatorInputs.falt` och `BesparingsvardeArgs.falt` är också numeriska.

Det finns därför ingen källa till ett band-ID-val för de 41 aktiverade
bandbastarifferna, ingen generell väg för obligatoriska policyfält som inte redan skapar
`indatafalt`, inget enum-val för Jönköping och ingen kontroll för Stockholms två serier.
Den föreslagna `byggIndataFranPolicy(policy, falt: Record<string, string | number>)`
hanterar dessutom bara `number` och `band_id`, inte `number_series`. Ett saknat policyfält
ger visserligen `blocked` i kontraktsfasaden, men dagens produktadapter klassar varje
sådant `blocked` efter kapacitetskontrollen som ett oväntat konfigurationsfel; V8 anger
ingen användarfelstyp eller UI-text för ett legitimt saknat obligatoriskt fält.

**Begärd rättning:** välj en enda typad produktindata-DTO genom
`KalkylatorPage` → `energiPotential` → `besparingsvarde` → `IndataPost`. Ange hur
policykrav blir genererad UI-metadata med minst inmatningstyp, etikett, hjälptext,
obligatoriskhet, tillåtna alternativ och seriekardinalitet. Bandalternativen ska komma
från just den valda tariffens bevarade `nivaer[].id`; enum och serie får inte parsas som
ett tal. Uppdatera de faktiska TypeScript-signaturerna och utskrifts-/återskapandevägen.
Skilj saknad/ogiltig kundindata från ett trasigt policykontrakt i
`KontraktBlockerat`/UI:t. Batch 0 ska ha ett syntetiskt end-to-end-test som faktiskt
renderar, fyller och beräknar number + band-ID + enum + serie, inte bara anropar en
hjälpfunktion.

### P1 — Stockholms årsmodell är motsägelsefull och saknar statiska bindningar

V8 kallar modellen både "17 nya `KravPost`" och den rekommenderade lösningen en enda
12-elements kallenergipost plus en 5-elements returtemperaturpost. Batchplanen upprepar
"17 nya `KravPost`" samtidigt som den namnger två seriekrav. Det är två olika API:n med
olika UI-, validerings- och bindningsbehov; implementationen kan inte lämnas att välja
mellan dem.

Även den rekommenderade tvåseriemodellen saknar två `Tariffpolicy`-bindningar som talar om
vilken validerad post som ska bli `mwh_kallt_per_manad` respektive
`returtemp_c_per_manad`. De befintliga `kallenergi_bindning` och
`returtemperatur_bindning` pekar på månadsfasadens skalära fält. Utan nya annual-bindningar
träffar serierna årsfasadens generella `falt`-loop, som uttryckligen kastar för serier.
Att skriva att "Stockholm-motsvarigheten" läser vissa nycklar är inte ett statiskt,
generiskt kontrakt och skulle bryta dokumentets egen regel mot tariff-ID-/fältnamns-
hårdkodning. Det befintliga effektkravet är dessutom märkt endast `monthly`; planen måste
uttryckligen lägga `annual` på samma unika effektpost om den ska användas av årsfasaden.

Slutligen används samma `IndataPost`-karta i dagens besparingsadapter för både före- och
efterkostnaden, medan de syntetiska månadsmängderna minskar i efterfallet. V8 säger inte
hur de 12 kallenergimängderna ska förändras. Oförändrad kallenergi kan bli större än en
eftermånads total-MWh; dagens motor räknar då en negativ mängd normal energi. En
årsprodukt som ska värdera besparing behöver en explicit, källmässigt försvarbar regel
för före/efter eller ska blockeras från besparingsvärderingen.

**Begärd rättning:** välj den enda rekommenderade modellen (två serier), lägg generiska
annual-seriebindningar och kardinalitet i policyn, låt effektposten gälla båda relevanta
omfattningarna och exkludera de två bundna serierna från det numeriska `falt`-objektet.
Definiera och testa `0 <= kallenergi[m] <= totalenergi[m]` samt hur kallenergin behandlas i
efterfallet. Om ingen verifierbar transformationsregel finns ska Stockholm kunna ge
uppskattad aktuell årskostnad men inte ett påhittat besparingsbelopp. Testa 12/5-längd,
månadsordning, gränser, före/efter och oförändrad `monthly_invoice`.

### P1 — Stockholm-preflighten validerar inte den adapter den beskriver

V8:s pseudokod slår upp katalog-ID och målpolicy, men använder aldrig
`AdapterEntry.provider_id` och kontrollerar inte den redan byggda `leverantorer`-mängden.
Ett felaktigt provider-ID kan därför inte kasta, trots att testlistan uttryckligen lovar
det. En loop över befintliga `ADAPTERREGISTER`-poster kan inte heller bevisa det omvända
påståendet "policytäckning utan adapter kastar"; en saknad post itereras aldrig.

**Begärd rättning:** preflighten ska verifiera en ett-till-ett-kedja från rå katalograd
till existerande leverantör, existerande prisårspost under just den leverantören,
matchande tariff-ID och policy med krävd täckning. Definiera även den omvända regeln som
gör att en leverantörsfilspolicy avsedd att ersätta en katalogdublett inte får
`annual_forward` utan motsvarande adapterpost. Gör adapterregistret injicerbart i tester
och bevisa fel provider, fel tariff, saknat mål, saknad/stale/redundant mapping samt exakt
ett UI-val.

## P2-fynd

- §6 säger att 45/45 ready-rader efter rättningar passerar den nakna `grind()`. Det kan
  inte stämma med V8:s egen design: Stockholm ska fortsatt stoppas av `utreds`/`energiform`
  och Umeå ska fortsatt ge `kapacitetsformel med multiplikator` i den nakna grinden. Rätt
  beviskedja är 43 nakna katalogpassager + Umeå genom en säker sammansatt grind = 44
  katalogaktiveringar, samt Stockholm via en separat leverantörsfilsadapter = 45 ready-
  bastariffer.
- `tariffinventering-v8.md`, `batchplan-v8.md`, sessionen och överlämningen blandar
  "17 fält", "17 nya KravPost" och två serieposter. Använd ett enda antal och ett enda
  schema genom samtliga dokument.
- V8-committen `fd372a2` ligger direkt ovanpå `f0f3ee7`, inte `058ffb4` som sessionen och
  överlämningen anger. Leveranstiden är 17:20:42 enligt committen; korrigeringscommitten
  `b7790ca` uppdaterade endast överlämningens metadata, inte de båda kvarvarande
  leveransraderna.

## Verifieringar

- `skills@b7790ca` består inom granskningsomfånget av dokumentation och konversationslogg;
  ingen produktkod, tariffdata eller genererad frontendfil ändrades av V8.
- `git diff --check f0f3ee7..b7790ca` är rent. Lokal `main` är tio commits före
  `origin/main`; V8 är inte godkänd för push.
- Inventeringen har 78 unika produktrubriker och räkningskontrollen anger fortsatt
  78 bas + 14 varianttäckningskrav = 92, fördelat 7/55/30.
- Relativa länkar i V8 pekar på befintliga filer.
- `katalog.py`, `generera.py`, `policyregister.py`, `resultatkontrakt.py`, `faktura.py`,
  TypeScript-spegeln, produktadaptern, `energiPotential.ts`, `fjarrvarme.ts` och
  kalkylatorsidan lästes på de pinnade produkt-HEAD:arna.
- Umeås katalograd bär samtidigt `post_multiplier`, en ännu okänd issue och
  `asymmetric_flow_difference`; dagens grind returnerar multiplikatorfyndet före de två
  senare kontrollerna. TypeScript har fortsatt `Varde = number | readonly number[]`,
  numeriska `falt`-signaturer och en kalkylatorsida som renderar alla genererade
  `indatafalt` som `type="number"`.
- Inga fulla produkttester kördes eftersom V8 endast ändrar planeringsdokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v9.md` och `batchplan-v9.md`; ändra inte V8 i efterhand.
2. Gör Umeås sammansatta grind fullständig efter att multiplikatorfyndet kvitterats och
   använd samma injicerade policyregister genom hela generatorvägen.
3. Specificera ett verkligt diskriminerat `IndataPost`-kontrakt för skalär, serie och
   band-ID, inklusive generisk seriekardinalitet och serialiseringsrundtur.
4. Gör batch 0 till ett riktigt produkt-/UI-kontrakt med genererad metadata, typad DTO,
   korrekt felklassning och end-to-end-test för number, band-ID, enum och serie.
5. Välj exakt två annual-serieposter för Stockholm, lägg statiska bindningar, annual-
   effektomfattning och en fail-closed före/efterregel för kallenergin.
6. Slutför adapterpreflightens provider-/tariff-/reversekontroller och tester.
7. Behåll V8:s Kraftringen- och Jönköpingslösningar samt dispositionerna 7/55/30 om ingen
   sakstatus ändras; rätta P2-räkningen och commitproveniensen.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `b7790ca`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
