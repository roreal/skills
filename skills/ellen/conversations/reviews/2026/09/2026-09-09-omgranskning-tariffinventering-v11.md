---
review_id: "2026-09-09-002"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v11.md
  - Fjarrvarmetariffer/batchplan-v11.md
  - skills commits 02c50aae48af034e5e870ec480441e2461a9c4d3 and 136d9cd5b841b753bb5081a4de29797e9203441d
reviewed_heads:
  skills: "136d9cd5b841b753bb5081a4de29797e9203441d"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-001"
---

# Omgranskning av tariffinventering v11 och batchplan v11

## Bedömning

V11 löser flera viktiga delar av V10-granskningen. Rått React-state är nu skilt från den
parsade domän-DTO:n, numeriska enumvärden och band-ID:n har olika typer, en separat
årsresultatgren saknar besparingsfält, kapaciteten har fått en gemensam indatabyggare och
adapterkontrollens reverse-nyckel bevarar provideridentiteten.

Planen är ändå inte implementeringsklar. Parsern returnerar ett `saknat`-fel som inte finns
i den deklarerade felunionen och mappar samtidigt saknad indata till den ogiltiga
felkanalen. Den nya förvalidatorn täcker inte de befintliga `minVarde`-/`maxVarde`-/
`heltal`-regler som annars fortfarande kastar generiska fel, och `maxvarde: null` förs
igenom till TypeScript utan den null-normalisering övriga valfria fält har. Generatorns
`bygg_ts()` får en tom katalog men ett icke-tomt produktionsregister och måste därför kasta
i preflightens första riktning, vilket dokumentet självt först medger och senare påstår att
ett test ska motbevisa. Produktdispatchen har dessutom två källor till `onskadTyp`, en
odefinierad `argsFranInputs`-väg och ingen förmågemodell för legacytariffer; den nya
besparingsgrenen anropas inte av den verkliga sidwrapper som planen visar.

Det krävs därför en avgränsad V12-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — parserns saknat-kontrakt finns inte i den deklarerade feltypen

V11 §6a.2 rad 1938–1953 anger returtypen
`PolicyInputValue | PolicyValideringsFel`, avvisar tomma skalärfält som "saknat värde" och
returnerar för en delvis tom serie orsaken `'saknat'`. Den deklarerade
`PolicyValideringsFel`-unionen på rad 2069 innehåller emellertid bara `'typ' | 'numerik' |
'kardinalitet' | 'okant_val'`. Den beskrivna parsern kan alltså inte implementeras mot sin
egen returtyp.

Rad 1961–1962 mappar dessutom varje parserfel till `ogiltigaFalt`, medan rad 2072–2077
kräver att legitimt saknad kundindata ska gå genom den separata `saknadeFalt`-vägen. Ett
tomt råfält är särskilt vanligt om formulärstatet initialiseras med en tom sträng per
metadatafält. Samma kundlucka blir då `ogiltigaFalt` om nyckeln finns i statet men
`saknadeFalt` om nyckeln saknas helt.

**Begärd rättning:** definiera ett enda diskriminerat parserresultat som skiljer
`parsed`, `missing` och `invalid`, eller utöka feltypen och ange en konsekvent mappning.
Tomt/blankt obligatoriskt skalärfält och tomt obligatoriskt serieelement ska få samma
stabila fältnära klassning oavsett hur React-statet initialiserades; explicit texten `"0"`
ska fortfarande bli talet `0`. Testa både frånvarande state-nyckel, tom skalärsträng,
blanksteg, delvis tom serie, felaktig numerik och explicit noll i den riktiga sidan.

### P1 — förvalidatorn och `maxvarde`-transporten är inte slutna över policyreglerna

V11 rad 2054–2070 inför rätt sorts förvalideringspunkt, men den uppräknade kontrollen täcker
bara värdetyp, seriekardinalitet, allow-list och banduppslag. Dagens verkliga
`harledResultatstatus` kontrollerar också `heltal` och `minVarde`; V11 inför dessutom
`maxVarde`. Om en direkt produktanropare skickar exempelvis ett decimalt heltalskrav eller
ett värde utanför min/max kommer förvalidatorn enligt planen att godkänna värdet och den
efterföljande kontraktsvalidatorn fortsätter kasta ett generiskt `Error`. Det bryter V11:s
eget löfte att fel som kan pekas ut på ett användarinmatat fält ska bli
`ogiltigaFalt`/`numerik`.

Planen säger också "för `band_id_val` specifikt" i en funktion som bara tar
`Tariffpolicy`, prispost och `IndataPost`. `band_id_val` är ett UI-metadataläge, inte ett
värde i `KravPost.vardetyp`. Den körbara domänregeln måste därför identifiera bandfältet via
`vardetyp === 'band_id'` och den statiska bindningen, inte via en metadataegenskap
validatorn inte får som argument.

Slutligen anger mappningstabellen på rad 1745 `maxVarde: k.maxvarde`. Python-dataklassen
serialiserar standardvärdet `None` som JSON `null`; till skillnad från exempelvis
`antalVarden: k.antal_varden ?? undefined` normaliseras detta inte. Eftersom
`policyFranGenererad()` läser `k` som `any` fångar kompilatorn inte felet, och en strikt
`skapaKravPost` kommer att se `null` som ett närvarande, icke-numeriskt maxvärde. Då kan
alla policyer utan maxgräns blockeras redan vid deserialisering.

**Begärd rättning:** låt förvalidatorn i både Python och TypeScript täcka samtliga
kundvärdesregler innan den kastande fasaden nås: ändlighet, värdetyp, `minVarde`,
`maxVarde`, `heltal`, seriekardinalitet, allow-list och banduppslag. Identifiera bandfält
från domänpolicyn. Ändra transporten till `maxVarde: k.maxvarde ?? undefined` och testa
både `null`, frånvarande fält och ett faktiskt maxvärde. Lägg direkta produktanrop för
under min, över max och brutet heltalskrav som måste ge typade användarfel, inte `Error`.

### P1 — `bygg_ts()`-preflighten är fortfarande logiskt omöjlig med produktionsregistret

Pseudokoden på rad 2416–2418 skickar `{"tariffs": []}` tillsammans med det verkliga,
icke-tomma `ADAPTERREGISTER`. Preflightens första riktning itererar varje adapterpost och
slår upp dess katalog-ID i just `rak_katalog["tariffs"]`. Stockholms post kan därför inte
hittas och funktionen måste kasta `"finns inte i katalogen"` innan reverse-kontrollen ens
nås.

V11 medger exakt detta på rad 2437–2444 och säger att `bygg_ts()` inte används för en
katalogberoende adapter. Samtidigt säger rad 2445–2447 att funktionen förblir korrekt för
leverantörsfiler utan markör, trots att den första riktningen kastar på det globala
registret oavsett vilka leverantörsfiler som byggs. Rad 2696–2699 kräver sedan motsatsen:
`bygg_ts()` med produktionsregistret och Stockholms markör ska passera utan kast och ge
samma reverse-kontroll som katalogvägen. Alla tre påståendena kan inte vara sanna.

**Begärd rättning:** välj ett verkligt anropskontrakt. Det enklaste är att låta
`bygg_ts()` ta en rå katalog när ett icke-tomt adapterregister används och köra exakt samma
tvåvägspreflight som `bygg_ts_fran_katalog()`. Om standalone-vägen i stället ska sakna
katalog måste den ha uttryckligen avgränsad semantik och får inte beskrivas som en full
bijektionskontroll. Behåll den provider-specifika reverse-nyckeln, injicera alla register
konsekvent och skriv tester vars förväntade utfall överensstämmer med pseudokoden. Rätta
också rad 2451: `_bearbeta_leverantorsfil()` får policyn från `policyregister.py` via
`_policy_till_json()`, inte från katalog-JSON.

### P1 — sidans årsproduktdispatch saknar ett entydigt, nåbart kontrakt

V11 rad 2595–2598 kallar `beraknaArsprodukt` den enda produktentryn för en
kontraktsgated tariff. Rad 2624 säger samtidigt att `calcResult` inte ska ändras, och
wrappern på rad 2634–2644 anropar `beraknaArsprodukt` bara för
`aktuell_arskostnad`; besparing går direkt till det oförändrade `calcResult(inputs)`.
Dagens verkliga `calcResult` anropar `beraknaBesparingsvarde` tre gånger och känner inte
till `beraknaArsprodukt`. Den nya `{typ:'besparing'}`-grenen är därmed inte den väg den
riktiga sidan använder för Sandviken, trots att batchplan rad 595–596 påstår det.

Det finns ytterligare tre körbarhetsluckor:

1. `onskadTyp` läggs enligt rad 2647 i `KalkylatorInputs`, men wrappern tar samma val som en
   separat parameter. Det finns två potentiellt motstridiga sanningskällor.
2. Wrapperns aktuella-kostnadsgren anropar den kontraktsgated `beraknaArsprodukt` för
   godtyckliga `KalkylatorInputs`, men planen definierar ingen förmågefunktion eller
   fail-closed-gren för legacytariffer och icke-fjärrvärmesystem. UI:t kan därför inte
   maskinellt veta när valet stöder en eller båda produkttyperna, trots rad 2649–2651.
3. `argsFranInputs(inputs)` finns inte i dagens kod och specificeras inte. Det är just där
   samma `energyScope`-uppskalning, `paverkbarMwh`, `energyProvenance`, MWh-only-grind och
   kapacitetsregler måste återanvändas. Dessutom säger gren 2 att
   `byggKontraktIndata` körs före den befintliga kärnan, men dagens
   `beraknaBesparingsvardeKontrakt` tar ingen färdig indatakarta och bygger själv sin karta.

**Begärd rättning:** välj en sanningskälla för `onskadTyp`, definiera en explicit
produktförmåga per vald prispost och ange fail-closed-beteendet för legacytariffer,
kontraktsgated tariffer och andra energisystem. Visa en faktisk extraherad hjälpfunktion
som bygger beräkningsargumenten från `KalkylatorInputs` med samma scope-/proveniensregler
som dagens `calcResult`. Välj sedan antingen att verkligen routa besparing genom
`beraknaArsprodukt`, eller dokumentera att den befintliga besparingsvägen är en separat
avsiktlig entry och ta bort påståendet om en enda entry. Specificera också om den
befintliga kontraktskärnan ska ta en färdig `indata`-karta eller själv äga den gemensamma
byggaren, så kartan inte byggs och valideras i två oförenliga lager. Testa verklig sida och
direktanrop för Stockholm aktuell kostnad, Stockholm förbjuden besparing, Sandviken
besparing, Sandviken aktuell kostnad, en legacytariff samt ett icke-fjärrvärmesystem.

## P2-fynd

- V11 beskriver flera nya tester i förfluten form, exempelvis "Testat identiskt" på rad
  2088, trots att leveransen endast ändrar dokumentation och gränssnitten ännu inte finns.
  Skriv "ska testas" fram till en verifierad kodleverans och skilj planerade acceptanstest
  från faktiskt körda tester.
- V11 ska vara självbärande men batchplan rad 50 hänvisar till
  `tariffinventering-v10.md`, inventeringen rad 1896 till `batchplan-v10.md` och rad 2794
  till samma gamla batchplan för aktuella fillistor/tabeller. Historiska jämförelser med
  V10 är riktiga, men normativa korsreferenser ska peka på V11.
- Batchplan rad 117–118 säger både att `KalkylatorInputs.policyFalt` dispatchar till
  `beraknaArsprodukt` och att den fullständiga besparingsvägen är oförändrad. Synkronisera
  fillistan med det dispatchbeslut som väljs i P1-rättningen ovan.

## Verifieringar

- `skills@02c50aa` och tidskorrigeringen `136d9cd` ändrar bara dokumentation och
  konversationslogg. Ingen produktkod, tariffdata, genererad frontendfil eller aktivering
  ändrades.
- `git diff --check ab38b79..136d9cd` är rent. `136d9cd` ligger direkt ovanpå
  `02c50aa`, vars verifierbara committid är `2026-09-09T07:20:05+02:00`.
- Produktrepoerna är rena och oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`. Den verkliga generatorn, resultatvalidatorn,
  produktadaptern, `calcResult` och resultatsidan lästes som granskningsbas.
- V11 innehåller fortsatt 78 bastariffrubriker och redovisar kontrollmängden 78 bas + 14
  varianter = 92 samt dispositionen 7 implementerade, 55 redo och 30 blockerade. Inget
  sakstatusfynd i V11-deltat motiverar en flytt i denna runda.
- Lokal `main` är 15 commits före `origin/main` och inte efter. V11 är inte godkänd för
  push.
- Inga fulla produkttester kördes eftersom V11 endast ändrar planeringsdokumentation och
  de beskrivna nya gränssnitten ännu inte finns i kod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v12.md` och `batchplan-v12.md`; ändra inte V11 i efterhand.
2. Gör parserresultatet typkorrekt och skilj konsekvent saknad från ogiltig råindata utan
   att tappa skillnaden mellan tomt och explicit noll.
3. Låt förvalidatorn täcka alla kundvärdesregler (`min`, `max`, `heltal`, ändlighet,
   värdetyp, serie, allow-list och band) före den kastande fasaden; rätta
   `maxvarde: null`-transporten.
4. Ge `bygg_ts()` ett anropskontrakt som faktiskt kan uppfylla preflighten, och synkronisera
   pseudokod, förklaring och tester. Behåll provider + tariff + katalograd i bijektionen.
5. Gör produktdispatchen entydig: en källa till `onskadTyp`, explicit
   produktförmågemodell, verklig argumentbyggare och överensstämmelse mellan wrapper,
   `calcResult`, `beraknaArsprodukt` och befintlig kontraktskärna.
6. Rätta P2-proveniens, tempus och normativa V11-korsreferenser.
7. Behåll V11:s lösta råstate/DTO-uppdelning, numerisk enum/band-ID-uppdelning,
   kapacitetsdelning, diskriminerade sidresultat, etikettkälla, provider-specifika
   reverse-nyckel samt dispositionerna 7/55/30 om ingen sakstatus ändras.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `136d9cd`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
