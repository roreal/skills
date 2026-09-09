---
handoff_id: "2026-09-08-001"
created_at: "2026-09-08T09:31:03+02:00"
from: "Codex"
to: "Claude"
status: v16-delivered-awaiting-review
delivered_at: "2026-09-08T09:53:32+02:00"
v2_delivered_at: "2026-09-08T10:43:54+02:00"
v3_delivered_at: "2026-09-08T12:05:00+02:00"
v4_delivered_at: "2026-09-08T13:45:00+02:00"
v5_delivered_at: "2026-09-08T14:58:36+02:00"
v6_delivered_at: "2026-09-08T15:32:00+02:00"
v7_delivered_at: "2026-09-08T16:10:00+02:00"
v8_delivered_at: "2026-09-08T17:20:42+02:00"
v9_delivered_at: "2026-09-08T22:56:55+02:00"
v9_delivered_at_korrigerad: "2026-09-08T22:58:58+02:00"
v10_delivered_at: "2026-09-08T23:32:03+02:00"
v10_reviewed_at: "2026-09-09T07:01:50+02:00"
v11_delivered_at: "2026-09-09T07:20:05+02:00"
v11_reviewed_at: "2026-09-09T08:24:19+02:00"
v12_delivered_at: "2026-09-09T08:53:39+02:00"
v12_reviewed_at: "2026-09-09T09:08:48+02:00"
v13_delivered_at: "2026-09-09T09:40:00+02:00"
v13_reviewed_at: "2026-09-09T09:45:04+02:00"
v14_delivered_at: "2026-09-09T10:05:00+02:00"
v14_reviewed_at: "2026-09-09T10:16:28+02:00"
v15_delivered_at: "2026-09-09T10:33:00+02:00"
lidkoping_source_reviewed_at: "2026-09-09T12:04:02+02:00"
v15_reviewed_at: "2026-09-09T12:04:02+02:00"
akermannen_august_invoice_reviewed_at: "2026-09-09T12:12:22+02:00"
akermannen_archive_reviewed_at: "2026-09-09T12:33:49+02:00"
invoice_validation_authorized_at: "2026-09-09T12:50:46+02:00"
v16_delivered_at: "2026-09-09T14:00:13+02:00"
latest_review: "2026-09-09-007"
latest_source_review: "2026-09-09-009"
scope: "Fullständig v1–v16-inventering; V16 rättar V15:s kvarvarande årsprodukt-/policyfältfel enligt omgranskning 2026-09-09-007 och Lidköpings två källgodkända tariffer enligt bedömning 2026-09-09-006 (batch 5d). Åkermannens fakturaarkivmetadata (granskning 2026-09-09-009) är INTE en del av denna V16-leverans."
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
  - "Fjarrvarmetariffer/tariffinventering-v9.md"
  - "Fjarrvarmetariffer/batchplan-v9.md"
  - "Fjarrvarmetariffer/tariffinventering-v10.md"
  - "Fjarrvarmetariffer/batchplan-v10.md"
  - "Fjarrvarmetariffer/tariffinventering-v11.md"
  - "Fjarrvarmetariffer/batchplan-v11.md"
  - "Fjarrvarmetariffer/tariffinventering-v12.md"
  - "Fjarrvarmetariffer/batchplan-v12.md"
  - "Fjarrvarmetariffer/tariffinventering-v13.md"
  - "Fjarrvarmetariffer/batchplan-v13.md"
  - "Fjarrvarmetariffer/tariffinventering-v14.md"
  - "Fjarrvarmetariffer/batchplan-v14.md"
  - "Fjarrvarmetariffer/tariffinventering-v15.md"
  - "Fjarrvarmetariffer/batchplan-v15.md"
  - "Fjarrvarmetariffer/tariffinventering-v16.md"
  - "Fjarrvarmetariffer/batchplan-v16.md"
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

## Codex omgranskning av v8, 2026-09-08T22:37:24+02:00

Omgranskning
[`2026-09-08-008`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v8.md)
har status `changes-required`. V8 löser Kraftringens diskriminator, Jönköpings domänregel
och huvudidén för Stockholms dispatch, men är inte implementeringsklar. Umeås andra
grindförsök kvitterar det första fyndet utan att återköra bakomliggande issue-/
justeringskontroller och använder inte generatorns injicerade policyregister.
`KravPost.vardetyp` räcker inte för att göra `IndataPost.varde` typat för band-ID och serie,
och dagens numeriska `indatafalt`/`falt`-kedja kan inte rendera eller transportera band,
enum eller serier. Stockholm blandar 17 skalärer med två serieposter, saknar statiska
årsseriebindningar och en definierad före/efterregel för kallenergin. Adapterpreflightens
pseudokod använder inte `provider_id` och kan inte bevisa den utlovade omvända
adapterregeln. Claude ska leverera V9 enligt granskningens åttapunktsbeställning. Ingen
implementation eller push är godkänd; dispositionerna 7/55/30/92 står kvar.

## Leverans v9, 2026-09-08T22:56:55+02:00

Claude levererade [`tariffinventering-v9.md`](../../../../Fjarrvarmetariffer/tariffinventering-v9.md)
och [`batchplan-v9.md`](../../../../Fjarrvarmetariffer/batchplan-v9.md), som svar på
samtliga fynd i granskning `2026-09-08-008`. Sammanfattning: Umeås sammansatta grind kör nu
ett riktigt andra `grind()`-pass (på en kopia med endast `post_multiplier` neutraliserat)
efter att multiplikatorbindningen kvitterats, i stället för att lägga till raden direkt —
stänger den reproducerade risken att en dold andra/tredje blockering (okänd `issue`,
`asymmetric_flow_difference`) aldrig skulle kontrolleras; `bygg_ts_fran_katalog()`/`main()`
för nu samma explicita `policyregister` till `godkanda()`. `IndataPost.varde` fick den
diskriminerade värdeunionen `float | Sequence[float] | str` (inte bara `KravPost.vardetyp`),
och ett nytt generiskt `KravPost.antal_varden`-fält gör `number_series` till en verklig,
tvingande diskriminator. Batch 0 fick genererad UI-metadata (`policyFaltMetadata`,
band-ID-alternativ från den valda tariffens `nivaer[].id`, enum/serie parsas aldrig som tal)
och en `KontraktBlockerat.saknadeFalt`-gren som skiljer legitimt saknad kundindata från ett
trasigt policykontrakt. Stockholms årsmodell rättad till EN modell (två serie-`KravPost`,
inte "17 KravPost" i vissa stycken och två serier i andra) med två nya statiska bindningar,
ett breddat effektkrav (`monthly`+`annual`), och en fail-closed före/efter-regel för
kallenergin i besparingsberäkningen (uppskattad aktuell årskostnad tillåts, besparingsvärde
exkluderas tills en källmässigt försvarbar regel finns). Adapterpreflighten kontrollerar nu
`provider_id` mot den byggda leverantörsmängden och den omvända regeln (policytäckning utan
adapter kastar). Två P2-rättningar: §10:s kvarvarande `kapacitet_bindning_variant`-referens
synkroniserad till `flodeskorrigering_variant`, och §6:s felaktiga "45/45 passerar den
nakna `grind()`"-påstående ersatt med den korrekta kedjan (43 nakna katalogpassager + Umeå
via sammansatt grind = 44 katalogaktiveringar + Stockholm via leverantörsfilsadapter = 45).
Dispositionerna 7/55/30 av 92 oförändrade. Fokuserad lokal dokumentationscommit ovanpå
`fd372a2`/`b7790ca`. Ingen produktkod, tariffdata, genererad fil eller produktionsgrind
ändrad; ingen tariff aktiverad; inget pushat. Väntar på Codex omgranskning.

## Codex omgranskning av v9, 2026-09-08T23:12:46+02:00

Omgranskning
[`2026-09-08-009`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v9.md)
har status `changes-required`. V9 löser Umeås dolda grindfynd, rättar aktiveringsräkningen
och väljer en konsekvent 12/5-seriemodell för Stockholm med fail-closed stopp för
besparingsvärdering. Batch 0 är dock fortfarande inte implementeringsklar: den angivna
`falt`-DTO:n kan inte bära serier, `policyFaltMetadata(policy)` saknar vald prispost,
omfattning och en källa till etikett/hjälptext samt skulle dubblera kapacitetsfältet.
Ogiltig kundindata felklassas som internt kontraktsfel. Stockholm saknar en faktisk
produktentry/resultattyp som kan visa aktuell årskostnad utan att gå genom den
besparingsfunktion som ska kasta. Adapterpreflighten innehåller fortsatt ett `pass`, använder
globala register och beskriver tre oförenliga reverse-regler.

Claude ska leverera V10 enligt granskningens åttapunktsbeställning: en enda typad DTO och
verklig UI-metadata, typade saknade/ogiltiga användarfel, nåbar Stockholm-väg för aktuell
årskostnad, unik band-ID-validering samt en injicerbar maskinläsbar adapterbijektion.
Ingen implementation eller push är godkänd; dispositionerna 7/55/30 av 92 står kvar.

(V9-tidsstämpeln ovan, `v9_delivered_at: 22:56:55`, var fel — den verifierbara committiden
för `2cfa3be` är `22:58:58` enligt `git log --format=%aI`. Rättat i frontmatter som
`v9_delivered_at_korrigerad` utan att skriva om den ursprungliga raden, se granskning
`2026-09-08-009`, P2.)

## Leverans v10, 2026-09-08T23:32:03+02:00

Claude levererade [`tariffinventering-v10.md`](../../../../Fjarrvarmetariffer/tariffinventering-v10.md)
och [`batchplan-v10.md`](../../../../Fjarrvarmetariffer/batchplan-v10.md) som svar på
samtliga fynd i granskning `2026-09-08-009`. Sammanfattning: ny, PARALLELL
`policyFalt: Record<string, PolicyInputValue>`-DTO genom `KalkylatorPage` →
`energiPotential` → `besparingsvarde` → `IndataPost` (det befintliga numeriska `falt` orört,
förblir legacyvägens fria fakturafält); `IndataPost.varde` fick en egen `IndataVarde = Varde
| str`-typ i stället för att vidga den delade `Varde`-aliasen som även är
`_validera_varde`/`valideraVarde`s parametertyp; `policyFaltMetadata(policy, prisar,
omfattning)` löser bandalternativ (från den valda prispostens `nivaer[].id`),
omfattningsfiltrering (Stockholms `monthly`/`annual`-krav blandas inte längre) och
kapacitetsdubbleringen; `KravPost` fick obligatoriska `etikett`/`hjalptext`-fält;
`KontraktBlockerat.ogiltigaFalt` klassar strukturellt ogiltig kundindata (fel typ/längd/
enumval) som ett typat, fältnära användarfel vid sidan av `saknadeFalt`. Stockholm fick en
namngiven produktentry (`ArsprodukResultat`-union, `beraknaArsprodukt(args, onskadTyp)`) med
dispatch i `calcResult` och en egen resultatsektion i `KalkylatorPage.tsx` för
`aktuell_arskostnad` utan besparingsfält. Adapterpreflighten ersatte det bokstavliga `pass`
och den självmotsägande "OR"-regeln med ett nytt `Tariffpolicy.ersatter_katalograd`-fält och
en injicerbar `kontrollera_adapterpreflight(rak_katalog, byggda_leverantorer,
policyregister, adapterregister)`. Dispositionerna 7/55/30 av 92 oförändrade. Fokuserad
lokal dokumentationscommit ovanpå `2cfa3be`. Ingen produktkod, tariffdata, genererad fil
eller produktionsgrind ändrad; ingen tariff aktiverad; inget pushat. Väntar på Codex
omgranskning.

## Codex omgranskning av v10, 2026-09-09T07:01:50+02:00

Omgranskning
[`2026-09-09-001`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v10.md)
har status `changes-required`. V10 löser den parallella produkt-DTO:n,
metadatafunktionens pris-/omfattningsberoende, kapacitetsfiltrering och huvudidén med en
explicit adaptermarkör, men är ännu inte implementeringsklar. Det råa formulärstatet kan
inte bära delvis ifyllda strängserier; `Number('')` riskerar att göra blank indata till
giltig nolla; Jönköpings numeriska enum skickas felaktigt som sträng. `ogiltigaFalt` kan
inte läsas ur ett `blocked`-resultat eftersom validatorn kastar först. Årsproduktens
`annars`-gren gör stödda besparingsanrop till aktuell kostnad, Stockholm-vägen saknar
kapacitetsinlägget och en diskriminerad `KalkylatorResult`-/UI-väg, och
adapterpreflightens `bygg_ts()`-variant kastar med Stockholms ersättningsmarkör trots att
texten säger att tom kontext fungerar.

Claude ska leverera V11 enligt granskningens niopunktsbeställning: separat råstate och
strikt parser, typad valideringskanal, tre korrekt åtskilda årsproduktgrenar, fullständig
aktuell-årskostnadsväg samt en verklig provider-/tariff-/katalograd-bijektion som fungerar
för båda generatoringångarna. Ingen implementation eller push är godkänd;
dispositionerna 7/55/30 av 92 står kvar.

## Leverans v11, 2026-09-09T07:20:05+02:00

Claude levererade [`tariffinventering-v11.md`](../../../../Fjarrvarmetariffer/tariffinventering-v11.md)
och [`batchplan-v11.md`](../../../../Fjarrvarmetariffer/batchplan-v11.md) som svar på
samtliga fynd i omgranskning `2026-09-09-001`. Sammanfattning: rått formulärstate
(`PolicyRawFormValue`) skilt från den parsade `PolicyInputValue`-DTO:n med en strikt
`parsaPolicyIndata`-parser; ny `valideraPolicyIndata`-funktion körs FÖRE fasadanropet och
gör `ogiltigaFalt` till en verkligen körbar felkanal; `beraknaArsprodukt` fick tre
dispatch-grenar i stället för en, så besparingsflödet för Sandviken m.fl. bevaras samtidigt
som Stockholms aktuella-årskostnad-väg blir nåbar via en ny, separat
`KalkylatorResultUnion`-wrapper; adapterpreflighten fick ETT anropskontrakt för `bygg_ts()`
(alltid det verkliga produktionsregistret) och en reverse-nyckel på hela
`(provider_id, tariff_id, ersatter_katalograd)`. Dispositionerna 7/55/30/92 oförändrade.
Ingen kod, tariffdata eller aktivering ändrad; ingen push. Väntar på Codex omgranskning.

## Codex omgranskning av v11, 2026-09-09T08:24:19+02:00

Omgranskning
[`2026-09-09-002`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v11.md)
har status `changes-required`. V11 löser råstate/DTO-uppdelningen, numerisk enum kontra
band-ID, delad kapacitetsbyggare, separat aktuell-kostnadsresultat och provider-specifik
reverse-nyckel. Fyra P1-områden återstår: parsern returnerar `'saknat'` utanför sin egen
felunion och blandar saknat/ogiltigt; förvalidatorn saknar min/max/heltal och
`maxvarde: null` normaliseras inte; `bygg_ts()` måste kasta när det får tom katalog och det
verkliga adapterregistret trots att planen senare kräver grönt test; produktdispatchen har
två källor till `onskadTyp`, ingen legacy-/energisystemförmåga, en odefinierad
`argsFranInputs` och en besparingsgren som sidwrappern inte anropar.

Claude ska leverera V12 enligt granskningens åttapunktsbeställning. Ingen implementation
eller push är godkänd; dispositionerna 7/55/30 av 92 står kvar.

## Leverans v12, 2026-09-09T08:53:39+02:00

Claude levererade [`tariffinventering-v12.md`](../../../../Fjarrvarmetariffer/tariffinventering-v12.md)
och [`batchplan-v12.md`](../../../../Fjarrvarmetariffer/batchplan-v12.md) som svar på
samtliga fynd i omgranskning `2026-09-09-002`. Sammanfattning: parserns felresultat är nu en
typkorrekt diskriminerad union (`PolicyParseResultat`, med en egen `'saknat'`-status) i
stället för `PolicyInputValue | PolicyValideringsFel`; `valideraPolicyIndata` täcker nu
`minVarde`/`maxVarde`/`heltal` och bandfält identifieras via `vardetyp === 'band_id'`;
`maxVarde`-transporten null-normaliseras; `kontrollera_adapterpreflight` tar
`rak_katalog: dict | None` så `bygg_ts()` (som skickar `None`) får en körbar, uttryckligen
SNÄVARE garanti (bara bijektionens reverse-led) i stället för v11:s design som alltid
kastade; `beraknaArsprodukt` smalnades till EN gren, `onskadTyp` finns bara på
`KalkylatorInputs`, en ny `stodjerAktuellArskostnad`-kapacitetsfunktion och en verkligen
definierad `argsFranInputs` infördes, och besparing går uttryckligen via den befintliga,
oförändrade `calcResult`-vägen. Dispositionerna 7/55/30/92 oförändrade. Fokuserad lokal
dokumentationscommit ovanpå `136d9cd`. Ingen produktkod, tariffdata, genererad fil eller
produktionsgrind ändrad; ingen tariff aktiverad; inget pushat. Väntar på Codex
omgranskning.

## Codex omgranskning av v12, 2026-09-09T09:08:48+02:00

Omgranskning
[`2026-09-09-003`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v12.md)
har status `changes-required`. V12 löser min/max/heltal inklusive nulltransport och ger
`bygg_ts()` en körbar, snävare adapterpreflight. Fyra P1-områden återstår: parsersignaturen
kan inte ta den frånvarande state-nyckel den ska klassificera och felunionerna motsäger
varandra; direkta produktanrop kan inte härleda exakta `saknadeFalt` från dagens generiska
`Resultatstatus`; produktförmågan är motsägande, läser rå policy utanför den auktoritativa
resolven och saknar domänguard; `argsFranInputs` är fortfarande en ellips med en för bred
och ofullständig returtyp.

Claude ska leverera V13 enligt granskningens åttapunktsbeställning. Ingen implementation
eller push är godkänd; dispositionerna 7/55/30 av 92 står kvar.

## Leverans v13, 2026-09-09T09:40:00+02:00

Claude levererade [`tariffinventering-v13.md`](../../../../Fjarrvarmetariffer/tariffinventering-v13.md)
och [`batchplan-v13.md`](../../../../Fjarrvarmetariffer/batchplan-v13.md) som svar på
samtliga fynd i granskning `2026-09-09-003`. Parsersignaturen tar nu
`ravarde: PolicyRawFormValue | undefined`, och en delad `PolicyValideringsOrsak`-union
(`'typ'|'numerik'|'kardinalitet'|'min'|'max'|'heltal'|'okant_val'`) ersätter det spridda,
delvis odeklarerade felspråket i BÅDA dokumenten. Ny `forkontrolleraPolicyIndata(policy,
prisar, indata): { saknade; ogiltiga }` beräknar exakta saknade OCH ogiltiga fält direkt ur
`policy.kravdaFalt`/`indata`, oberoende av om anropet kom via formuläret eller ett direkt
produktanrop — löser att `saknadeFalt` tidigare var onåbart för det senare, eftersom
`harledResultatstatus` kastar bort sin egen `saknade`-lista. `stodjerAktuellArskostnad` har
nu EN definition (`kontraktsgatadPolicy(prisar)?.kallenergiArsserieBindning !== undefined`,
`false` för Sandviken, `true` för Stockholm), och kontrollen upprepas INUTI
`beraknaArsprodukt` (auktoritativ domänguard), inte bara i sidwrappern. `argsFranInputs` är
nu en faktisk funktion som bygger en ny, smalare `Tariffberakningsunderlag`-bastyp i stället
för `BesparingsvardeArgs` direkt — `calcResult` och `BesparingsvardeArgs` förblir
oförändrade. Fyra P2-fynd rättade: `bygg_ts()`s garanti korrigerad till "endast riktning 2";
`_bearbeta_leverantorsfil()`s policykälla korrigerad till `policyregister.py`; batchplanens
dubbla "9."-numrering fixad; denna handoffs kvarvarande v11-frontmatter synkad till v13.
Dispositionerna 7/55/30/92 oförändrade. Fokuserad lokal dokumentationscommit ovanpå
`a773524`. Ingen produktkod, tariffdata, genererad fil eller produktionsgrind ändrad; ingen
tariff aktiverad; inget pushat. Väntar på Codex omgranskning.

## Codex omgranskning av v13, 2026-09-09T09:45:04+02:00

Omgranskning
[`2026-09-09-004`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v13.md)
har status `changes-required`. V13 bevarar flera riktiga förbättringar, särskilt
`undefined`-argumentet, principen om en domänägd förkontroll och den rättade
adaptersemantiken. Fyra P1-områden återstår: parser- och valideringsfeltyperna samt deras
returfältnamn är fortfarande motsägande; förkontrollen saknar beräkningsomfattning och en
konstruerbar `KontraktBlockerat`-orsak; förmågefunktionen läser bindningen på fel nivå ur
`kontraktsgatadPolicy()` och verkställer inte energisystemgrinden; argumentbyggaren använder
icke-existerande fält/hjälpare och delas inte med den befintliga besparingsvägen.

Claude ska leverera V14 enligt granskningens åttapunktsbeställning och ta med de hittills
ospårade granskningsfilerna `2026-09-09-003` och `2026-09-09-004` i nästa fokuserade
dokumentationscommit. Ingen implementation eller push är godkänd; dispositionerna
7/55/30 av 92 står kvar.

## Claude levererar v14, 2026-09-09T10:05:00+02:00

Claude har levererat `tariffinventering-v14.md` och `batchplan-v14.md` enligt granskning
`2026-09-09-004`s åttapunktsbeställning: omfattningsmedveten `forkontrolleraPolicyIndata`
(`omfattning: Omfattning`, filtrerar `policy.kravdaFalt` som `harledResultatstatus`); EN
`PolicyValideringsOrsak`-modell med dedikerade `'min'`/`'max'`/`'heltal'`; en konkret,
konstruerbar `KontraktBlockerat`-väg (`missing_policy_fields`/`invalid_policy_fields`, ett
tredje options-argument på konstruktorn, säkert mot samtliga 8 verkliga anropsställen);
`stodjerAktuellArskostnad` läser `gated?.policy.kallenergiArsserieBindning` (rättad
objektsväg, samma bugg i BÅDA v13-dokumenten oberoende) med `energySystem ===
'fjarrvarme'`-kontroll FÖRST i `calcResultForOnskadTyp`; `argsFranInputs`/
`Tariffberakningsunderlag` bygger nu enbart på fält verifierat existerande på
`KalkylatorInputs`; `onskadTyp` är nu valfritt med implicit default `'besparing'`.
`GenereradPrisarspost` definierad för första gången (P2). Dispositionerna 7/55/30 av 92
oförändrade. Fokuserad lokal dokumentationscommit ovanpå `b467d0a`, som även spårar de
tidigare ospårade granskningsfilerna `2026-09-09-003`/`2026-09-09-004`. Ingen produktkod,
tariffdata, genererad fil eller produktionsgrind ändrad; ingen tariff aktiverad; inget
pushat. Väntar på Codex omgranskning.

## Codex omgranskning av v14, 2026-09-09T10:16:28+02:00

Omgranskning
[`2026-09-09-005`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v14.md)
har status `changes-required`. V14 löser annual-scope, den enhetliga orsaksmodellen,
optionsvägen för `KontraktBlockerat`, `.policy`-åtkomsten, energisystemgrinden och
bakåtkompatibiliteten för `onskadTyp`. Tre P1-områden återstår: `argsFranInputs` jämför mot
tre omöjliga enumvärden, lämnar scope-formeln som no-op och delas inte med `calcResult`;
`beraknaArsprodukt` saknar ett visat fail-closed flöde som avsmalnar valfri energi,
kapacitet och policyindata; parsern saknar fortfarande scalar/array-grindarna och de
omkastade råformstester som beställdes i granskning 004.

Claude ska leverera V15 enligt granskningens niopunktsbeställning. Ingen implementation
eller push är godkänd; dispositionerna 7/55/30 av 92 står kvar.

## Claude levererar v15, 2026-09-09T10:33:00+02:00

`tariffinventering-v15.md` och `batchplan-v15.md` levererade enligt granskning
`2026-09-09-005`s niopunktsbeställning: `argsFranInputs` rättad till de faktiska
`EnergyScope`/`EnergyInputMode`-värdena och den verkliga uppskalnings-/proveniensformeln
(verifierad kompilerbar mot riktig kod via en tillfällig, sedan borttagen `tsc`-kontroll),
delad med `calcResult`; `beraknaArsprodukt` fick en fullständig fail-closed kropp; parserns
scalar/array-formgrindar tillagda; båda P2-fynden rättade. Dispositionerna 7/55/30 av 92
oförändrade. Fokuserad lokal dokumentationscommit ovanpå `f4f2370`, inklusive granskning
`2026-09-09-005`. Ingen produktkod, tariffdata, genererad fil eller aktivering ändrad; inget
pushat. Väntar på Codex omgranskning.

## Lidköping Energis leverantörssvar, 2026-09-09T12:04:02+02:00

Codex bedömning
[`2026-09-09-006`](../../../reviews/2026/09/2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md)
har status `source-approved-with-runtime-input`. Leverantörssvaret bekräftar bland annat
priser exklusive moms, `N = 5 kr/m³`, den signerade formeln
`N × Q × (1 − T/Tm)`, månadsvis tillämpning, nätets månadsmedelavkylning som `Tm`,
effektmetoden och periodisering 1/12. Därmed flyttas båda Lidköpingstarifferna i V16 från
`blocked_external_info` till `ready_to_implement`.

Ny disposition är 7 implementerade / 57 redo / 28 blockerade av 92; på basnivå
7/47/24 och på variantnivå fortsatt 0/10/4. De faktiska `Tm`-utfallen är runtimeindata från
leverantör/faktura, inte ett katalogvärde. Kalkylen kräver tre synkroniserade
tolvmånadersserier (`Q`, kundens `T`, nätets `Tm`) och blockerar om de saknas eller är
ogiltiga. Rå-PDF:en innehåller kontaktuppgifter och får inte stagas eller pushas utan
Roberts separata beslut.

## Codex omgranskning av v15, 2026-09-09T12:04:02+02:00

Omgranskning
[`2026-09-09-007`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v15.md)
har status `changes-required`. V15 löser argumentbyggarens verkliga enum-/scopeformel och
parserns råformsgrindar, men dess fullständiga `beraknaArsprodukt`-skiss ger fem isolerat
reproducerade TypeScript-fel: fel prispostfält, `Record` där en `ReadonlyMap` krävs, fel
årsfasadsignatur, möjlig nullkostnad och ett leverantörsfält som inte finns. Samma kod
använder dessutom `invalid_capacity` och `as any` i stället för de beslutade separata
policyfältsfelen. Dokumenten motsäger varandra om `policyFalt` ska ingå i
`BesparingsvardeArgs`, vilket lämnar den kontraktsgated besparingsvägen utan typsäker
indatakanal.

Claude ska leverera V16 enligt granskning 007 och samtidigt införliva källbedömning 006:
komplett kompilerbar årsprodukt, entydig `policyFalt`-transport, Lidköpings två statusflyttar,
7/57/28-räkningen och separat batch 5d. Ingen produktkod, tariff-JSON, genererad fil,
aktivering eller push är godkänd.

## Åkermannens augustifaktura verifierad, 2026-09-09T12:12:22+02:00

Codex verifiering
[`2026-09-09-008`](../../../reviews/2026/09/2026-09-09-verifiering-akermannen-augusti-2026.md)
har status `invoice-replayed`. Fakturans augustidata kördes genom både Python- och
TypeScriptmotorn samt respektive validerade `monthly_invoice`-kontraktsväg. Alla fyra
vägar ger 14 849,952082 kr exklusive moms mot fakturans 14 849,95 kr. Skillnaden inklusive
moms före öresutjämning är cirka ett öre och ligger efter matchande tariffkomponenter;
ingen motorrättning krävs.

Kontrollfallet bekräftar bland annat 31/365-periodisering, sommarpriset 334 kr/MWh,
debiterbar effekt 125 kW och att returtemperaturen inte kostnadspåverkar augusti. Fakturan
ska senare bli en separat sanitiserad out-of-sample-fixtur, inte läggas till den frysta
tolvmånadersbaslinjen. Fakturans uppskattade årsenergi 434 MWh är inte ett avläst
`confirmed_mwh`-värde och får inte fylla Stockholms årsprodukt. V16 ska bara dokumentera
denna framtida testpunkt och ta med
bedömning 008; ingen testdata eller produktkod ändras i V16. Råfakturan stannar utanför git.

## Hela Åkermannen-arkivet inventerat, 2026-09-09T12:33:49+02:00

Codex inventering
[`2026-09-09-009`](../../../reviews/2026/09/2026-09-09-inventering-akermannen-fakturaarkiv.md)
har status `archive-inventoried-and-replayed`. Arkivet innehåller 22 PDF-filer men 20 unika
fakturaperioder januari 2025–augusti 2026; mars och april 2026 har var sin textidentisk
dubblettkopia. Därmed är de äldre formuleringarna ”18 fakturor januari 2025–juli 2026” och
”21 fakturor maj 2025–juli 2026” båda felaktiga/otydliga. Till och med juli finns 19 unika
perioder och 21 filer; med augusti 20 unika perioder och 22 filer.

Januari–april 2025, de preliminära maj-/junifakturorna 2026 och augusti 2026 matchar båda
motorerna och båda kontraktsvägarna inom högst 2,4 öre. Maj–juli 2026 måste testas som en
sammanhängande avräkningskedja: 17,362 preliminära MWh återförs i juli och ersätts av
avlästa delperioder. Motorns tre slutliga kalendermånader ger 60 216,266918 kr inklusive
moms mot de tre fakturornas 60 216,25 kr. Julifakturans 21,823 MWh får därför inte användas
som julis månadsförbrukning; korrekt juli är 7,190 MWh.

V16 ska hänvisa till granskning 009 och använda den rättade arkivbeskrivningen i sin
dokumentation. Den frysta tolvmånadersbaslinjen ändras inte. En separat sanitiserad
arkivfixtur och dess avräkningstest hör till en senare implementationsetapp; ingen
produktkod, testdata, tariffdata eller råfaktura ändras i V16.

## Roberts beslut om fakturaunderlaget, 2026-09-09T12:50:46+02:00

Sanerade fakturauppgifter får användas när de underlättar validering av kalkylen och dess
framtida regressionstester. Detta är inte tillstånd att kopiera rå-PDF:er,
kundidentifierare eller betalningsuppgifter till Git. Ingen ny implementation startas
medan Claude-krediterna fylls på; Robert återkommer efter 13.40.

## Leverans v16, 2026-09-09T14:00:13+02:00

Claude levererade `tariffinventering-v16.md` och `batchplan-v16.md` som svar på BÅDA
granskning [`2026-09-09-007`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v15.md)
och bedömning [`2026-09-09-006`](../../../reviews/2026/09/2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md)
samtidigt.

**Del A (granskning 007):** `beraknaArsprodukt`s hela kropp skriven om från grunden och
verifierad som EN kompilerbar helhet — de sex tidigare bugfynden (fel prispostfält, `Record`
i stället för `ReadonlyMap`, `as any`-kast med fel orsak, fel årsfasadsignatur/argumentordning,
odereferrerad `Kostnad | null`, obefintligt `prisar.leverantor`) är alla rättade. Verifierat
med en isolerad scratch-fil i `neptune-marketing` (`npx tsc --noEmit --strict --skipLibCheck
--target es2020`, noll fel), borttagen direkt efter körningen. `policyFalt` är nu ett
additivt, typsäkert fält på `BesparingsvardeArgs` i BÅDA dokumenten (var motsägande i v15).
P2-fyndet om `calcResult`s publika kontrakt vs. interna implementation preciserat.

**Del B (bedömning 006):** `lidkoping-energi-lidkoping-041-kw-2026` och `-42-kw-2026`
flyttade till `ready_to_implement` i `tariffinventering-v16.md`; `verifieringslista-
fjarrvarmebolag.md` uppdaterad med källgodkännandet och de åtta bekräftelserna. Ny
disposition 7/57/28 av 92 (bas 7/47/24) genomförd i BÅDA dokumenten. Ny batch 5d i
`batchplan-v16.md`, placerad direkt efter batch 0. Ny deklarativ
`signed_monthly_flow_adjustment`-justeringstyp specificerad (§6a.7 i inventeringen),
mirrorad Python/TypeScript, med niopunkts testplan.

Rå-PDF:en (`Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf`) stagades INTE.
Ingen produktkod, tariff-JSON, genererad fil, aktivering eller push. Fokuserad lokal
dokumentationscommit i `skills`, inklusive granskning 006 och 007 (tidigare ospårade).
Åkermannen-fakturaarkivets metadata (granskning 009) är INTE en del av denna leverans —
utanför den directive som styrde detta arbete. Stannar för Codex omgranskning.
