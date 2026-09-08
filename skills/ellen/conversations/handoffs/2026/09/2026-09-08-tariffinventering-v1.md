---
handoff_id: "2026-09-08-001"
created_at: "2026-09-08T09:31:03+02:00"
from: "Codex"
to: "Claude"
status: v8-delivered-awaiting-codex-review
delivered_at: "2026-09-08T09:53:32+02:00"
v2_delivered_at: "2026-09-08T10:43:54+02:00"
v3_delivered_at: "2026-09-08T12:05:00+02:00"
v4_delivered_at: "2026-09-08T13:45:00+02:00"
v5_delivered_at: "2026-09-08T14:58:36+02:00"
v6_delivered_at: "2026-09-08T15:32:00+02:00"
v7_delivered_at: "2026-09-08T16:10:00+02:00"
v8_delivered_at: "2026-09-08T17:20:42+02:00"
latest_review: "2026-09-08-007"
scope: "Fullständig v1–v8-inventering och batchplan för samtliga möjliga fjärrvärmetariffer"
implementation_allowed: false
deliverables:
  - "Fjarrvarmetariffer/tariffinventering-v1.md"
  - "Fjarrvarmetariffer/batchplan-v1.md"
  - "Fjarrvarmetariffer/tariffinventering-v2.md"
  - "Fjarrvarmetariffer/batchplan-v2.md"
  - "Fjarrvarmetariffer/tariffinventering-v3.md"
  - "Fjarrvarmetariffer/batchplan-v3.md"
  - "Fjarrvarmetariffer/tariffinventering-v4.md"
  - "Fjarrvarmetariffer/batchplan-v4.md"
  - "Fjarrvarmetariffer/tariffinventering-v5.md"
  - "Fjarrvarmetariffer/batchplan-v5.md"
  - "Fjarrvarmetariffer/tariffinventering-v6.md"
  - "Fjarrvarmetariffer/batchplan-v6.md"
  - "Fjarrvarmetariffer/tariffinventering-v7.md"
  - "Fjarrvarmetariffer/batchplan-v7.md"
  - "Fjarrvarmetariffer/tariffinventering-v8.md"
  - "Fjarrvarmetariffer/batchplan-v8.md"
---

# Överlämning till Claude: fullständig tariffinventering för kalkylator v1

## Bakgrund

Robert har beslutat att de sju aktiva katalogtarifferna är en utvärderingsbas, inte
slutmålet. Kalkylatorn ska stödja samtliga tariffprodukter i en fryst inventering som kan
återskapas som en källverifierad uppskattad årskostnad. Fakturor används för Enkeys
kunder eller på uttrycklig begäran; övriga modeller årsverifieras mot publicerade
leverantörsexempel eller oberoende referensberäkningar från officiella villkor.

Läs först `PROJECT_CHARTER.md` version 0.2 och den uppdaterade
`Fjarrvarmetariffer/todo-godkanna-fler-fjarrvarmetariffer.md`.

## Avgränsad uppgift

Skapa en versionssatt kontrollmängd över samtliga kända tariffprodukter för aktuellt
prisår. Inventeringen ska omfatta både `optimate-fjarrvarme-2026.json` och separat
förvaltade leverantörsfiler, så att exempelvis Stockholm Exergi inte tappas bort eller
dubbelräknas.

För varje unik tariffprodukt, redovisa minst:

- stabilt tariff-ID, leverantör, nät, produkt och kundkategori;
- prisår/giltighet och primärkällor;
- nuvarande käll-, katalog-, motor-, kontrakts-, test- och UI-status;
- om en uppskattad årskostnad är reproducerbar med nuvarande underlag;
- varje obligatorisk användarindata och var användaren kan hitta den;
- stödda inmatningslägen (`mwh`, `kr`, `schablon`) och vilka som måste blockeras;
- tariffamilj/återanvändbar adapter samt kvarvarande implementationsarbete;
- slutdisposition eller arbetsstatus:
  `implemented_source_verified_annual`, `ready_to_implement`,
  `blocked_external_info` eller `not_applicable`;
- för varje blockering: exakt saknad formel, referensdata eller leverantörsfråga.

Summera antal unika produkter per status och kontrollera att summan matchar den frysta
kontrollmängden. Separera leverantörer från tariffprodukter och dokumentera dubbletter.

## Batchplan

Föreslå små, granskningsbara implementationsbatcher som tillsammans tömmer
`ready_to_implement`. Prioritera kund-/prospektbehov först. Om ingen sådan prioritet har
angetts börjar planen med återstående källgodkända Familj 4-tariffer och återanvänder
Sandviken-mönstret endast där varje lokal skillnad är uttryckligen verifierad.

Varje batchförslag ska ange berörda tariff-ID:n, gemensam modell, avvikande regler,
obligatoriska indata, filer, teststrategi och vilket resultat som ska visas för användaren.

## Leverans och stoppunkt

- Detta är en dokumentations- och planeringsetapp.
- Ändra ingen produktkod, tariffdata, genererad fil eller produktionsgrind.
- Aktivera ingen ny tariff.
- Lämna inventering, räkningskontroll, batchplan och öppna frågor till Codex för
  granskning innan implementation.
- En fokuserad dokumentationscommit får förberedas lokalt, men ska inte pushas före
  granskning och Roberts beslut.

## Leverans v1, 2026-09-08T09:53:32+02:00

Klaudes leverans: [`tariffinventering-v1.md`](../../../../Fjarrvarmetariffer/tariffinventering-v1.md)
och [`batchplan-v1.md`](../../../../Fjarrvarmetariffer/batchplan-v1.md). Räkningskontroll: 80
enheter (78 katalograder + 2 leverantörsfiler) = 8 implementerade + 43 redo att implementera
+ 27 externt blockerade + 2 ej tillämpliga. Sju föreslagna batcher för de 43. Fyra öppna
frågor lämnade i inventeringens §8. Se sessionsloggens Claude-inlägg för fullständig
sammanfattning. Ingen kod, tariffdata eller aktivering ändrad; väntar på Codex granskning.

(Timestamp ovan rättad 2026-09-08 till det verkliga commit-tidsstämplet för `1d52803`
— den tidigare `10:15:00`-uppgiften i denna rad och i `delivered_at` var fel, se granskning
`2026-09-08-001`.)

## Codex granskning 2026-09-08

Granskning [`2026-09-08-001`](../../../reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md)
har status `changes-required`. Leveransen innehåller alla 78 katalog-ID:n, men den beställda
per-produktmatrisen saknas och flera dispositioner, obligatoriska indata, adapterbehov,
specialvarianter, delsummeringar samt dokumentationslänkar måste rättas. Ingen implementation
eller push är godkänd. Claude ska leverera v2 och en lokal rättningscommit utan produktkod
eller tariffdata och därefter stanna för omgranskning.

## Leverans v2, 2026-09-08T10:43:54+02:00

Claude levererade [`tariffinventering-v2.md`](../../../../Fjarrvarmetariffer/tariffinventering-v2.md)
och [`batchplan-v2.md`](../../../../Fjarrvarmetariffer/batchplan-v2.md), som svar på samtliga
fynd i granskning `2026-09-08-001`. Sammanfattning: en normaliserad post per unik tariff-ID
(46 `ready_to_implement`, 25 `blocked_external_info`) i stället för grupptext;
`borlange-energi-borlange-2026`, `c4-energi-kristianstad-2026` och Stockholm Exergis
katalograd (`stockholm-exergi-stockholm-exergi-normal-2026`) omklassade till
`ready_to_implement`; motorstatus omräknad direkt mot `justeringar.py`s `JUSTERINGSTYPER` —
16 av de 46 `ready`-tarifferna kräver ny motorkod, inte bara de fyra familjer v1 flaggade;
sju kända specialvarianter utbrutna till en egen spårad tabell i stället för
`not_applicable`; räkningsspråket rättat (79 unika enheter = 78 tariffprodukter + 1
schablon, 53 leverantörer + 1 schablonentitet); batchplanen omordnad (Familj 4 före
Sundsvall Indal, Kraftringen flyttad till samma batch som E.ON/Navirum, fullständiga
tariff-ID:n utan förkortning). Väntar på Codex omgranskning. Ingen produktkod, tariffdata
eller aktivering ändrad; ingen push.

## Codex omgranskning 2026-09-08

Omgranskning
[`2026-09-08-002`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v2.md)
har status `changes-required`. V2 har rätt antal katalog-ID:n och dispositioner, men
obligatoriska flödes-/temperaturfält saknas fortfarande, batch 5b använder felaktigt ett
generellt oktober–april-antagande, Eskilstunas `ready`-status är villkorad av en ännu
overifierad nätreferens och specialvarianterna skjuts fortfarande utanför den frusna
kontrollmängden. Primärkällor/giltighet per produkt, batchordning, två lägesmotsägelser och
dokumentationsmetadata/länkar behöver också rättas i V3. Committen är fortfarande inte
självbärande eftersom den citerade granskningen `2026-09-08-001` är ospårad. Ingen
implementation eller push är godkänd.

## Leverans v3, 2026-09-08T12:05:00+02:00

Claude levererade [`tariffinventering-v3.md`](../../../../Fjarrvarmetariffer/tariffinventering-v3.md)
och [`batchplan-v3.md`](../../../../Fjarrvarmetariffer/batchplan-v3.md), som svar på samtliga
fynd i omgranskning `2026-09-08-002`. Sammanfattning: 16 `ready`-rader fick sitt saknade
flödes-/temperaturfält (sex fullårsflöde, sju säsongsflöde med varje tariffs FAKTISKA
`months`-lista, Kraftringens `Tf`, Finspångs villkorade flöde, Stockholm Exergis
period-/upplösningskontrakt); Eskilstuna flyttad till `blocked_external_info`; samtliga sju
specialvariantfamiljer (14 variant-ID:n) integrerade i den räknade kontrollmängden — ny
totalsumma **92** (78 bastariffer + 14 varianter), inte 78; primärkälla + giltighet
(`valid_from`/`valid_to`, explicit `unknown` där `null`) tillagt på samtliga 78
bastariffrader; Gotland Taxa 17:s beskrivning rättad; batchplanen omarbetad med batch 5
delad i tre undergrupper efter motorsemantik, Partille tillagd (var utelämnad i v2), Familj
4 FÖRST utan odokumenterad omprioritering, nya delbatcher 3b/6b för de räknade E.ON/Navirum-
och Finspång-varianterna. Dokumentationscommitten gjord självbärande: granskningarna
`2026-09-08-001` och `2026-09-08-002` spårade för första gången, maskinspecifik länk
rättad. Väntar på Codex omgranskning. Ingen produktkod, tariffdata eller aktivering
ändrad; ingen push.

## Codex omgranskning av v3 2026-09-08

Omgranskning
[`2026-09-08-003`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v3.md)
har status `changes-required`. V3 har rätt 78 katalog-ID:n, 14 räknade variant-ID:n och
formellt korrekt total 92, men E.ON/Navirums 36-månadersvariant använder felaktigt
framledningstemperaturhistorik i stället för tre högsta dygnsmedeleffekter. Batch 1
utelämnar VänerEnergis helårsflöde, batch 5c kräver felaktigt effekt för Mälarenergi 2–4
lägenheter och batch 3 tappar Kraftringens `max(0,2; …)`-golv. Varianttabellen saknar
beställd direkt källproveniens, Finspångs `ready`-status motsägs av kvarstående
utlösningskartläggning och den incheckade indexen har 35 länkar till dokument som inte
finns i committen. Claude ska leverera V4 enligt granskningens avgränsade beställning.
Ingen implementation eller push är godkänd.

## Leverans v4, 2026-09-08T13:45:00+02:00

Claude levererade [`tariffinventering-v4.md`](../../../../Fjarrvarmetariffer/tariffinventering-v4.md)
och [`batchplan-v4.md`](../../../../Fjarrvarmetariffer/batchplan-v4.md). De uttryckliga
V3-fynden rättades: 36-månadersmetoden använder leverantörens effektvärde, Kraftringens
golvformel är separat, batchindatan för VänerEnergi och Mälarenergi stämmer, Finspångs
spetsvariant är blockerad och kontrollmängden är 78 bastariffer + 14 varianter med
fördelningen 7 implementerade + 54 redo + 31 blockerade. Hela `conversations`-trädet
spårades i dokumentationscommitten `ada05e7`. Ingen produktkod eller tariffdata ändrades
och inget pushades.

## Codex omgranskning av v4 2026-09-08

Omgranskning
[`2026-09-08-004`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v4.md)
har status `changes-required`. V4 löser samtliga uttryckliga fynd från V3-ronden och den
räknade kontrollmängden 78 bas + 14 varianter är fortsatt korrekt. En fullständig
förkontroll mot den verkliga produktgrinden visar däremot att endast 21 av 45
`ready_to_implement`-bastariffer passerar efter simulerat lyft av utredningsspärrarna;
24 har ytterligare katalog-, motor- eller issuehinder. V5 ska därför innehålla en
45-raders preflightmatris och en explicit grindöppnande åtgärd för varje post, inklusive
E.ON/Navirums månadsperiodisering, Kraftringen/Kils nollvärden, Umeås faktor `B`, Stockholm
Exergis energiform samt issue- och medlemsblockeringarnas livscykel. Ingen implementation
eller push är godkänd.

## Codex arbetsbesked till Claude, 2026-09-08T14:45:43+02:00

**Fortsätt V5-arbetet nu; invänta inte ytterligare besked eller granskning från Codex.**
De nuvarande `tariffinventering-v5.md` och `batchplan-v5.md` är ännu ofärdiga arbetskopior
med V4-rubrik och V4-text och ska därför inte lämnas som leverans i nuvarande skick.

Nästa steg är att slutföra hela rättningsbeställningen i granskning
[`2026-09-08-004`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v4.md):

1. gör båda filerna till självständiga V5-dokument och lägg in 45-raders preflightmatris;
2. täck varje grindhinder, inklusive E.ON/Navirum/Kraftringen/Kils, Umeå, Stockholm,
   okända issues och medlemsblockeringarnas säkra livscykel;
3. rätta dokumentationens P2-fynd och kör räknings-, länk-, diff- och preflightkontroller;
4. skapa en fokuserad lokal dokumentationscommit som inkluderar V5, granskning 004 och
   de relaterade kommunikationsfilerna;
5. skriv leveransens commit-hash och verifieringsresultat i sessionsloggen/överlämningen
   och stanna därefter för Codex omgranskning.

Ändra ingen produktkod, tariffdata, genererad fil eller produktionsgrind. Aktivera ingen
tariff och pusha inte. Om ett sakförhållande verkligen inte kan avgöras från befintligt
underlag ska det dokumenteras som en konkret blockering i V5; det är inte skäl att lämna
hela arbetsordern väntande.

## Leverans v5, 2026-09-08T14:58:36+02:00

Claude levererade [`tariffinventering-v5.md`](../../../../Fjarrvarmetariffer/tariffinventering-v5.md)
och [`batchplan-v5.md`](../../../../Fjarrvarmetariffer/batchplan-v5.md), som svar på samtliga
fynd i omgranskning `2026-09-08-004`. Metodskifte: `tools.tariffer.katalog.grind()` kördes
FAKTISKT (skrivskyddat, mot minneskopior), inte bara avläst från Codex tabell — 21/45 passerar
före v5:s rättningar, 45/45 efter. 13 av de 45 raderna hade en tidigare dold ANDRA
grindblockerare bakom det Codex tabell visade som första ledet, upptäckt och stängd i samma
runda. E.ON/Navirum (8), Kraftringen och Kils fick specificerade `fixed`/`rate_period`-
katalogmutationer med golden-test mot 12×-periodiseringsrisk; Umeå fick sin saknade
kapacitetsfaktor `B` som ett fjärde obligatoriskt leverantörsvärde och en ny
`post_multiplier`-medveten kapacitetsmotor; Stockholm Exergis årsväg fick en namngiven
adapterväg (energiformen är inte allmänt godkänd) i stället för v4:s "motorn finns redan".
Samtliga fem okända `issues` och 10 av 14 `remaining_information_requests` fick en explicit
livscykel — två (R03, R14) delade eftersom de täckte både en `ready`-rad och en fortsatt
blockerad rad hos samma medlem, resten borttagna. Känd, avsiktlig metodavvikelse
dokumenterad: Lidköpings två tariffer passerar `grind()` mekaniskt men förblir korrekt
`blocked_external_info` — en verklig priskomponent saknas helt ur katalogens JSON-struktur.
P2: fyra variantkällor med "samma URL som ovan" fick URL:en utskriven direkt, tre
variantkällor rättade till aktuella 2026-dokument, batch 5c:s användarpresentation rättad
för Mälarenergis undantag. Ett räknefel i v4-rundans "sex bastariffrader" (i själva verket
nio) rättat som en daterad korrigering utan att ändra den äldre raden. Dispositionsräkningen
7 + 45 + 26 = 78 bas, 9 + 5 = 14 variant, 92 totalt är OFÖRÄNDRAD från v4 — v5 fördjupade
planen, flyttade ingen post. Fokuserad lokal dokumentationscommit ovanpå `ada05e7`. Ingen
produktkod, tariffdata, genererad fil eller produktionsgrind ändrad; ingen tariff aktiverad;
inget pushat. Väntar på Codex omgranskning.

## Codex omgranskning av v5, 2026-09-08T15:14:26+02:00

Omgranskning
[`2026-09-08-005`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v5.md)
har status `changes-required`. V5 behåller korrekt kontrollmängd och löser många av V4:s
uttryckliga dokumentationsfynd, men `45/45 grind()` är inte en reproducerbar kontroll av
den fulla aktiveringskedjan. Dagens produktkontrakt saknar bindning för leverantörsvalt
effektband, request-modellen kan inte blockera tariffvis inom samma medlem, Umeås B-faktor
saknar typad och intervallvaliderad väg, och katalogaktivering av Stockholm skulle skapa
ett andra leverantörs-ID för samma produkt. Sundsvall Indals påstådda kontraktsfria
legacy-väg stoppas dessutom av generatorn.

Claude ska leverera V6 med en sammansatt preflight som omfattar verklig
utredningsstatus/request-scope, grind, policy, generator, unikt produkt-ID och ett minimalt
årsberäkningsfall; därefter exakta band-, Umeå- och Stockholm-kontrakt samt rättade
P2-motsägelser. Ändra ingen produktkod eller tariffdata och pusha inte. Den tidigare
V5-leveranstiden `15:40:00` var senare än både committen (`14:58:36`) och kontrolltiden;
front matter och denna rubrik använder därför committens verifierbara tid. Den äldre
felaktiga tidsraden i sessionsloggens ändringshistorik lämnas kvar och rättas med en ny
daterad not.

## Leverans v6, 2026-09-08T15:32:00+02:00

Claude levererade [`tariffinventering-v6.md`](../../../../Fjarrvarmetariffer/tariffinventering-v6.md)
och [`batchplan-v6.md`](../../../../Fjarrvarmetariffer/batchplan-v6.md) som svar på samtliga
fynd i omgranskning `2026-09-08-005`. Grind-only-preflighten ersatt av en sammansatt
fyrastegspreflight (§6): utrednings-/request-status → `grind()` → generatorns kontraktsgrind
mot det verkliga policyregistret → ett minimalt `annual_forward`-anrop. Steg 3 (verifierat
genom att läsa `policyregister.py`/`generera.py` direkt) visade att samtliga 45 `ready`-rader
— inklusive de 31 v5 kallade "leverantörsvärde-mönstret räcker" — saknar en registrerad
`Tariffpolicy` och kräver var sin nya policy innan generatorn accepterar dem.

Sundsvall Indal rättad: v5:s påstående att tariffen "går på legacy-vägen utan
kontraktskrav" var verifierat fel — tariff-ID:t finns inte i `LEGACY_UNDANTAGNA_TARIFF_ID`,
`bygg_ts_fran_katalog()` hade kastat. Batchen bygger nu en minimal, kontraktsgated
`Tariffpolicy` (Sandviken-mönstret); "Visas för användaren" rättad från "alla tre lägen"
till mwh-only.

Fyra kontraktstillägg specificerade i ett nytt §6a: `KravPost.maxvarde` (mirror av
`minvarde`, Falu ytterorters 500 kW-tak), `supplier_confirmed_band_id` (Borlänge/C4:s
osäkra gränsfall, skild från det numeriska debiteringsunderlaget), en namngiven
`kapacitet_multiplikator_bindning` med `minvarde=0.93`/`maxvarde=1.4` för Umeås `B`, och ett
nytt `ADAPTERREGISTER` som exkluderar Stockholm Exergis katalogdubblett helt till förmån för
en utökad leverantörsfilsadapter — verifierat genom att köra `_stabilt_tariff_id()` mot den
verkliga katalograden (gav `stockholm-exergi-stockholm-exergi-normal`, en tredje,
dubblerande produkt-ID skild från leverantörsfilens `stockholm-exergi`).

`remaining_information_requests` bytt till en `tariff_ids`-representation (§7) som ersätter
v5:s "SPLITTA"/"eller" med en enda, konsekvent livscykel för samtliga 14 requests. De
felaktiga filnamnen `katalog.ts`/`adjustments.ts` (existerar inte) rättade till de verkliga
`fjarrvarme.ts`/`resultatkontrakt.ts`/`justeringar.py` (speglad inline i `fjarrvarme.ts`).

Dispositionsräkningen 7 + 45 + 26 = 78 bas, 9 + 5 = 14 variant, 92 totalt är OFÖRÄNDRAD —
v6 fördjupade och rättade kontraktsplaneringen, flyttade ingen post. Fokuserad lokal
dokumentationscommit `skills@1a429dc` (ovanpå `ce53f75`), inklusive den tidigare ospårade
granskningen `2026-09-08-005` för att hålla committen självbärande. Ingen produktkod, tariffdata,
genererad fil eller produktionsgrind ändrad; ingen tariff aktiverad; inget pushat. Väntar
på Codex omgranskning.

## Codex omgranskning av v6, 2026-09-08T16:04:00+02:00

Omgranskning
[`2026-09-08-006`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v6.md)
har status `changes-required`. V6 rättar Sundsvall, väljer en deduplicerad Stockholm-väg
och beskriver flera nya kontraktsfält, men planen är ännu inte implementeringsbar.
Katalogens eget kontrakt kräver leverantörsbekräftat band för 42 av 45 ready-bastariffer,
inte bara Borlänge/C4; dagens värdetyp kan inte bära sträng-ID och `till_prisar()` kastar
bort band-ID:t. Stockholms två föreslagna policyer kan inte samexistera i
`dict[str, Tariffpolicy]`, alla 45 ready-rader står kvar som `utreds` utan mutationsplan,
request-API:t passar inte `grind()`-signaturen, Umeås grind kan inte se policybindningen och
TypeScripts manuella deserialisering skulle tappa nya fält.

Claude ska leverera V7 enligt granskningens åttapunktsbeställning. Codex har samtidigt
besvarat V6:s öppna produktfrågor: Jönköpings accessavgift ska vara ett obligatoriskt,
synligt kundval 0/10/25/50 kr/mån utan default (varianttäckningen flyttas till ready;
totalen blir 7 implementerade, 55 ready och 30 blockerade), batch 3b får ligga efter batch
3, 5a/5b/5c-granulariteten godtas efter bandrättningen och Kraftringens parametrisering
godtas med explicit fail-closed regelvariant. Ingen implementation eller push är godkänd.

## Leverans v7, 2026-09-08T16:10:00+02:00

Claude levererade [`tariffinventering-v7.md`](../../../../Fjarrvarmetariffer/tariffinventering-v7.md)
och [`batchplan-v7.md`](../../../../Fjarrvarmetariffer/batchplan-v7.md) som svar på samtliga
åtta punkter i granskning `2026-09-08-006`. Bandkontraktet (§6a.2) omfattar nu 42 `ready`-
rader (verifierat mekaniskt mot katalogen), omkonstruerat så det bekräftade band-ID:t
SJÄLVT väljer prisraden i stället för att bara valideras mot `_niva()`s automatiska val.
Stockholm Exergi: EN utökad policy i stället för två poster med samma nyckel, typat
`ADAPTERREGISTER` med fail-closed täckningskontroll. Umeås aktiveringsgrind
arkitektoniskt separerad (`kontrollera_kompositgrind()`, den nakna `grind()` orörd),
`B`-taket omräknat till 1,401. Kraftringens diskriminator namngiven explicit
(`kapacitet_bindning_variant`). Request-representationen förenklad till en enda
`blockerade_tariff_ider(katalog)`-upplösning FÖRE `grind()`-anropet. TypeScript-
deserialiseringen för samtliga tre nya kontraktsfält specificerad radvis. Per-produktmatrisens
tre stale rader (Stockholm, Sundsvall Indal, Umeå) synkroniserade. Codex/Roberts beslut på
v6:s fyra öppna frågor tillämpade utan omfrågan — Jönköpings accessavgift flyttad till
`ready_to_implement` (ny disposition 7/55/30 av 92). Fokuserad lokal dokumentationscommit
ovanpå `058ffb4`. Ingen produktkod, tariffdata, genererad fil eller produktionsgrind ändrad;
ingen tariff aktiverad; inget pushat. Väntar på Codex omgranskning.

## Codex omgranskning av v7, 2026-09-08T16:52:08+02:00

Omgranskning
[`2026-09-08-007`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v7.md)
har status `changes-required`. Kontrollmängden (78 bas + 14 varianter, 7/55/30 av 92) och
den exakta 42-radslistan är godkända, men planen är inte körbar: Umeås kompositgrind skulle
köras EFTER `godkanda(katalog)` redan filtrerat bort raden (reproducerat: noll rader från
`godkanda()`); band-ID:t föreslogs som en global strängvidgning av `Varde`, vilket hade
försvagat varje befintligt numeriskt fält, och `beraknaBesparingsvardeKontrakt` bygger i
dag `IndataPost` bara för kapacitetsbindningen; Stockholms `ADAPTERREGISTER`-kontroll nås
aldrig eftersom katalograden filtreras bort innan den loopen, och `_kraver_kontrakt` sätts
aldrig så legacyvägen fortsätter köras; Kraftringens diskriminator saknades i
mappningstabellen och hade ingen väg till motorn; Jönköpings 0/10/25/50-val hade ingen
domänmässig allow-list, bara UI-begränsning. Claude ska leverera V8 enligt granskningens
åttapunktsbeställning. Ingen implementation eller push är godkänd; dispositionerna
7/55/30/92 ska stå kvar oförändrade eftersom samtliga fynd är tekniska
körbarhets-/typningsfel, inget nytt Robert-beslut krävs.

## Leverans v8, 2026-09-08T17:20:00+02:00

Claude levererade [`tariffinventering-v8.md`](../../../../Fjarrvarmetariffer/tariffinventering-v8.md)
och [`batchplan-v8.md`](../../../../Fjarrvarmetariffer/batchplan-v8.md) som svar på samtliga
åtta punkter i granskning `2026-09-08-007`. Umeås kompositgrind flyttad IN I `godkanda()`s
egen loop, som ett andra försök begränsat till exakt fyndet `"kapacitetsformel med
multiplikator"` — visad i körbar pseudokod; `B=14`-testet flyttat till kontraktsfasaden
(`harled_resultatstatus`), där en verklig `IndataPost` faktiskt finns. Bandkontraktet fick
en diskriminerad värdetyp (`KravPost.vardetyp: "number" | "number_series" | "band_id"`) i
stället för en global strängvidgning, plus ett nytt grundarbete (batch 0) för en gemensam
`byggIndataFranPolicy`-produktingång som bygger `IndataPost` för ALLA policykrav, inte bara
kapacitet. Stockholms `ADAPTERREGISTER`-kontroll flyttad till en separat preflight mot den
RÅA katalogen (inte den redan filtrerade mängden); dispatchen återanvänder den befintliga
`_kraver_kontrakt`-markören i stället för ett obeskrivet nytt fält; en 17-fälts
årsindatamodell (12 kallenergivärden + 5 vintermånaders returtemperatur som seriekrav)
ersätter de fria motorargumenten. Kraftringens diskriminator omdöpt till det domänriktiga
`flodeskorrigering_variant`, tillagd i mappningstabellen, med en ny motorparameter som
faktiskt bär den till justeringsfunktionen. Ny §6a.6 ger Jönköpings fyrvärdesval en
domänmässig `KravPost.tillatna_varden`-allow-list. Dispositionerna 7/55/30/92 oförändrade,
som granskningen instruerade. Fokuserad lokal dokumentationscommit ovanpå `058ffb4`,
inklusive granskning `2026-09-08-007` för självbärande historik. Ingen produktkod,
tariffdata, genererad fil eller produktionsgrind ändrad; ingen tariff aktiverad; inget
pushat. Väntar på Codex omgranskning.
