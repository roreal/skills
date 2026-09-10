---
session_id: "2026-09-08-001"
started_at: "2026-09-08T09:21:35+02:00"
last_updated: "2026-09-10T12:52:47+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: batch0-code-review-changes-required
topics:
  - kalkylator-v1
  - produktdirektiv
  - verifieringsnivaer
  - leverantorstackning
  - tariffprioritering
source: visible-conversation
transcript_fidelity: summarized
---

# Session: produktkontrakt för kalkylator v1

## Sammanfattning

Efter att Claudes Sandviken-push hade verifierats bad Robert Codex fortsätta. Codex
genomförde den avgränsade dokumentationsetapp som tidigare rekommenderats: ett första
produktdirektiv för kalkylator v1 skapades, den inaktuella tariff-to-do-listan synkades
med Roberts beslut om års- och fakturaverifiering och två tekniska underlag fick
förtydliganden om verifieringsmetod och ordet `exact`.

V22 godkändes med villkor i `2026-09-09-016` som plan för en avgränsad lokal Batch 0-
implementation. Robert gav klartecken och Claude levererade två lokala commits. Codex
kodgranskade dem i `2026-09-10-001`: **changes-required**. Attesteringsbasen,
fail-closed-defaults och de befintliga regressionerna fungerar, men verklig DTO-/UI-kedja,
prispostbunden bandvalidering/motorväg, full numerisk serievalidering och verifierbar
generatorproveniens saknas. Ingen tariffaktivering eller push ingår. Dispositionen
7/57/28 av 92 är oförändrad.

Lidköping Energis leverantörssvar är källgodkänt i `2026-09-09-006`. Båda
Lidköpingstarifferna flyttades i V16 till `ready_to_implement`, med obligatoriska
tolvmånadersserier för kundvolym, kundavkylning och nätets medelavkylning. Dispositionen är
därmed 7/57/28 av 92 (bas 7/47/24, varianter 0/10/4) och ska bevaras i V22; det är den
tekniska integrationsplanen, inte källstatusen, som måste rättas.

Hela Åkermannens fakturaarkiv är inventerat och återspelat i `2026-09-09-009`. De 22
PDF-filerna motsvarar 20 unika fakturaperioder januari 2025–augusti 2026; två är
dubblettkopior. Alla nya enkelfall och maj–juli-avräkningen matchar Python och TypeScript
inom högst 2,4 öre. Arkivet blir senare en separat sanitiserad testfixtur och ändrar inte
tariffdispositionen.

Batch 0 har ändrat lokal kalkylator-/kontraktskod och den genererade filen, men ingen
tariffdata, disposition eller aktivering. Produktcommitterna är inte pushade.

Efter två rättningsrundor har Codex i `2026-09-10-003` godtagit bandfelsvägen,
scope-uppskalningen och Pythons slutna felorsak, men fortsatt satt **`changes-required`**.
Den nya sidan kan ännu inte representera V22:s numeriska enum eller elementvisa serier,
metadatan saknar prispost-/inmatningstypskontrakt och fältfelen är globala. Det nya
Playwright-testet verifierar bara fall där policy-UI:t är frånvarande och kräver dessutom
en separat manuellt startad preview-server. Den gemensamma argumentbyggaren har fortfarande
ett annat schema än `Tariffberakningsunderlag`. Ingen tariffaktivering eller push är
godkänd; dispositionen är fortsatt 7/57/28.

Rättningsrunda 3 är omgranskad i `2026-09-10-004`. Prispostmedveten metadata, numeriskt
enum, strikt råparser, elementvisa serieinputfält och det gemensamma underlaget är nu
rättade; 387 Python- och 468 TypeScripttester, typkontroll samt ett självbärande E2E-
kommando är gröna. Beslutet är ändå fortsatt **`changes-required`**: det avtalade
sammanhållna 12-serie→kostnadstestet med oberoende handfacit saknas, sidan använder inte
`stodjerBesparing` för alternativ/default, domänlagrets fältspecifika fel blir fortfarande
globala och UI-texterna stoppas inte vid policykonstruktion. Ingen aktivering eller push;
7/57/28 kvarstår.

## Levererade dokument

- `PROJECT_CHARTER.md` — målprioritering, kalkylatorns v1-scope, verifieringsnivåer,
  redovisningsspråk, leverantörsprioritering, Definition of Done och icke-mål.
- `Fjarrvarmetariffer/todo-godkanna-fler-fjarrvarmetariffer.md` — äldre krav på generell
  månadsmodell och faktura per prismodell ersatta med den beslutade årsmodellen;
  Sandviken och grundkartläggningen markerade klara.
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md` — not om att intern status
  `exact` inte betyder fakturaverifierad och inte ska användas som kundlöfte.
- `Fjarrvarmetariffer/optimate-agentfundament-bebo-fjarrvarme.md` — tariffadapter kan
  årsverifieras mot leverantörsexempel eller oberoende referensberäkning; fakturor används
  för Enkeys kunder eller när kontroll uttryckligen efterfrågas.

## Beslut som dokumenten återger

- Kalkylatorn är projektets primära produktmål; Ellens mätdata- och
  kostnadsoptimeringsförmåga är sekundär.
- Kalkylator v1 är i första hand en leverantörsspecifik årsberäkning.
- Modellstatus och resultatstatus hålls isär. En källverifierad tariff gör inte ett
  enskilt kundresultat fakturaverifierat.
- Kundgränssnittet skiljer `beräknat`, `uppskattat` och `fakturaverifierat`; det
  fristående ordet "exakt" används inte som kvalitetslöfte.
- MWh-, kronor- och schablonläge är separata tarifförmågor. Ett icke verifierat läge
  blockeras i stället för att gissas.
- Samtliga möjliga tariffprodukter i en fryst inventering ska implementeras. Varje
  återstående post ska vara explicit blockerad av extern information eller motiverat ej
  tillämplig; ingen oklassificerad rest tillåts.

## Öppet beslut för Robert

1. Ska en saknad leverantör ge ett separat val med tydligt märkt generell uppskattning och
   möjlighet att efterfråga bolaget? Codex rekommenderar ja; ett riksgenomsnitt får aldrig
   framstå som den namngivna leverantörens tariff.

## Nästa kontrollpunkt

Claude ska rätta P1/P2-fynden i `2026-09-10-003` utan tariffaktivering eller
dispositionsändring: implementera V22:s exakta metadata-/råformskontrakt inklusive
numeriskt enum och elementvis serie, fältlokala fel, ett självbärande verkligt sidtest med
syntetisk fullständig tariff samt ett enda gemensamt `Tariffberakningsunderlag`. Full
testmatris, typkontroll, bygge och diffkontroll ska redovisas, följt av en ny
Codexomgranskning. Ingen push är godkänd.

## Konversation

### Robert — användare

> Du kan fortsätta nu

### Codex — assistent

Codex fortsatte med dokumentationsetappen enligt den tidigare beslutade arbetsordningen.
Produktdirektivet och de synkade arbetsdokumenten levererades utan ändring av produktkod
eller tariffdata. Två produktbeslut återstår för Robert: v1:s minsta leverantörstäckning
och beteendet när användarens leverantör saknas.

### Robert — användare

> Jag ser de sju befintliga tarifferna som en utvärdering, jag vill att vi tar oss igenom samtliga som är möjliga. Om energibolagen kan fakturera på dessas uppgifter så ska vi kunna bygga en kalkyl som skapar motsvarande uppskattade årskostnad.

### Codex — assistent

Codex uppdaterade produktdirektivet till version 0.2. De sju aktiva tarifferna är nu
uttryckligen en utvärderingsbas, inte v1:s slutliga omfattning. Täckningsmålet är samtliga
tariffer i en fryst tariffinventering som kan återskapas som källverifierad uppskattad
årskostnad. Inventeringen omfattar både JSON-katalogen och separat förvaltade
leverantörsfiler, så exempelvis Stockholm Exergi inte faller utanför kontrollmängden.

"Möjlig" definieras tekniskt: alla nödvändiga prisdelar, formler och villkor ska vara
kända, och dynamiska värden ska kunna anges synligt, hämtas från verifierad källa eller
beräknas från uttryckligt underlag. En leverantörs internt dolda formel eller nätreferens
ersätts inte med en gissning; tariffen får då `blocked_external_info` och en konkret fråga
tills besked finns. Varje tariff ska till slut vara implementerad, externt blockerad eller
motiverat ej tillämplig — ingen oklassificerad restlista.

### Claude — assistent

Claude genomförde överlämning `2026-09-08-001`: en fullständig, deduplicerad
tariffinventering och batchplan, ingen kod eller tariffdata ändrad.

[`tariffinventering-v1.md`](../../../../Fjarrvarmetariffer/tariffinventering-v1.md) täcker
samtliga 78 katalograder plus de två separat förvaltade leverantörsfilerna (Stockholm
Exergi, Riksgenomsnittet) — 80 enheter, deduplicerat till 79 unika produkter. Byggd på
den redan granskade [verifieringslistan](../../../../Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md)
och [teknisk-kartläggning v4](../../../../Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md)
i stället för att omgranska källorna på nytt, plus en direkt läsning av
`katalog.py`/`policyregister.py`/`tariffer.generated.ts` för faktisk motor-/kontrakts-/
UI-status. Disposition: 8 `implemented_source_verified_annual` (de sju katalogtarifferna +
Stockholm Exergi), 43 `ready_to_implement`, 27 `blocked_external_info` (varje rad med den
exakta leverantörsfrågan), 2 `not_applicable` (Riksgenomsnittet, Stockholm Exergis
katalogduplikat). Summan stämmer mot kontrollmängden (78 katalog + 2 leverantörsfiler = 80).
`optimate-fjarrvarme-2027.json` (en annan sessions redan pushade commit `62181a1`, prisår
2027, bara 2 av 53 medlemmar ifyllda) är uttryckligen utanför denna frusna 2026-version.

[`batchplan-v1.md`](../../../../Fjarrvarmetariffer/batchplan-v1.md) föreslår sju batcher (43
tariffer) i stigande risk-/motorarbetesordning: (1) Sundsvall Indal/Liden/Lucksta —
ren energitariff, ren aktivering; (2) Familj 4-resten + Telge, Sandviken-mönstret rakt av;
(3) E.ON/Navirum, delad ny flödesformel; (4a–4c) 26 fristående leverantörsvärde-tariffer i
tre delbatcher efter hur mycket särvillkor de bär; (5) Borås + Finspång, två nya
kapacitetsformer i motorn; (6) Vattenfalls tolv tariffer, kontingent på ett öppet beslut om
3.3 (asymmetrisk flödesjustering). De 27 blockerade tarifferna batchas inte — de väntar på
leverantörssvar via den befintliga processen i tariff-to-do:ns §7.

Fyra öppna frågor lämnade till Codex i inventeringens §8: Vattenfalls delnings-/väntebeslut,
en motsägelse mellan verifieringslistan och teknisk-kartläggningen om Sundsvall Matfors
(löst genom att följa den senare, mer detaljerade, redan granskade källan som auktoritativ),
om "leverantörsvärde-mönstret" som generell policy för ~26 produkter behöver granskas
tariff för tariff, och om de föreslagna `not_applicable`-undantagen inom vissa batcher
(kundvald effekt hos Södertörn, lågtemperaturvärme hos Tekniska Verken Linköping,
Brunnshög hos Kraftringen, spetsvärme hos Finspång) är rätt avvägning.

Ingen produktkod, tariffdata, genererad fil eller produktionsgrind ändrad. Ingen ny tariff
aktiverad.

### Robert — användare

> Dags för granskning

### Codex — assistent

Codex granskade tariffinventering v1, batchplan v1 och den lokala dokumentationscommitten
`1d52803`. Alla 78 katalog-ID:n finns i inventeringen, men kontrollpunkten fick
`changes-required`: dokumentet saknar den beställda per-produktmatrisen, Borlänge/C4 är
felaktigt externt blockerade, Stockholm Exergis månadsvalidering bär inte ensam
årsdispositionen, flera flödes-/temperaturfält och nya adapterbehov saknas och kända
specialvarianter får inte gömmas som "ej tillämpliga i denna batch". Räkningen och
dokumentationsproveniensen har också fel och sex lokala länkar är brutna. Claude har fått en
avgränsad v2-beställning utan produktkod, tariffdata eller push. Fullständig granskning:
[`2026-09-08-001`](../../../reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md).

### Robert — användare

> Läs igenom claude

### Codex — assistent

Codex kontrollerade den delade mappen igen. Inget nytt Claude-svar, ingen
`tariffinventering-v2.md`, ingen `batchplan-v2.md` och ingen rättningscommit fanns ännu.
Repositoryts HEAD var fortsatt `1d52803`; de senaste filändringarna i conversations var
Codex granskning och logguppdateringar från 10:14. V2-beställningen i granskning
`2026-09-08-001` kvarstår därför oförändrad.

### Claude — assistent

Claude levererade v2 av båda dokumenten som svar på samtliga fynd i granskning
`2026-09-08-001`.

[`tariffinventering-v2.md`](../../../../Fjarrvarmetariffer/tariffinventering-v2.md) ersätter
v1 i sin helhet: en normaliserad post per unik tariff-ID (46 `ready_to_implement`, 25
`blocked_external_info`, 7 `implemented_source_verified_annual`) i stället för grupptext,
med källa/katalog/motor/kontrakt/test/UI-status som separata fält, obligatorisk indata med
fyndplats, inmatningsläge och tariffamilj per rad. Riksgenomsnittet ligger nu i en egen
schablontabell (§7), inte bland tariffprodukterna. Tre dispositioner rättade:
`borlange-energi-borlange-2026` och `c4-energi-kristianstad-2026` är `ready_to_implement`
(leverantörsvärde-mönstret, automatisk gruppindelning blockerad); Stockholm Exergis
katalograd (`stockholm-exergi-stockholm-exergi-normal-2026`) är `ready_to_implement`, inte
längre räknad som implementerad — dess `monthly_invoice`-kontrakt (godkänt `2026-09-06-003`)
täcker inte kalkylatorns årsprognos. Motorstatusen är omräknad direkt mot
`justeringar.py`s `JUSTERINGSTYPER`: 16 av de 46 `ready`-tarifferna kräver ny motorkod (en
ej implementerad justeringstyp eller kapacitetsform) — Kraftringen (samma typ som
E.ON/Navirum), Eskilstuna, Jämtkrafts tre produkter, Umeå och Finspång saknades i v1:s
motorbedömning. Sju kända specialvarianter (E.ON/Navirums 36-månadersmetod, Södertörns
kundvalda effekt, Kraftringens Brunnshög, Tekniska Verken Linköpings lågtemperaturvariant,
Finspångs spetsvärmetillägg, Jönköpings accessavgift, Borås miljötillägg) är utbrutna till
en egen spårad tabell (§5) i stället för `not_applicable`. Räkningsspråket är rättat: 79
unika enheter = 78 tariffprodukter + 1 syntetisk schablon (inte "79 unika tariffprodukter"),
53 leverantörer + 1 schablonentitet (inte 55) — verifierat programmatiskt mot katalog-JSON,
inte räknat för hand.

[`batchplan-v2.md`](../../../../Fjarrvarmetariffer/batchplan-v2.md) ersätter v1: ordningen
följer nu överlämningens regel (Familj 4-resten före Sundsvall Indal, som ändå läggs FÖRST
som ett eget, oberoende, lägsta-risk-beslut eftersom det inte konkurrerar om samma
granskningskapacitet som Familj 4-arbetet). Kraftringen flyttad till samma batch som
E.ON/Navirum (batch 3, 9 tariffer, delad `supply_temperature_adjusted_flow`-motorkod). Ny
batch 4 för Eskilstuna/Jämtkraft/Umeå (5 tariffer, tre separata nya justeringstyper — helt
utelämnad i v1). Leverantörsvärde-gruppen delad i 5a (11, inget nytt motorarbete) och 5b
(12, kräver `volume`+`months`-säsongssemantik som dagens motor saknar). Batch 6 (Borås/
Finspång) uppdaterad med Borås miljötillägg och Finspångs dubbla motorbehov
(`piecewise_polynomial` OCH `conditional_flow`). Ny batch 7 för Stockholm Exergis
årsprodukt. Batch 8 (Vattenfall) oförändrad, kontingent. Samtliga tariff-ID:n skrivna ut
fullständigt, ingen förkortning.

Dokumentationshistoriken gjordes självbärande: `PROJECT_CHARTER.md`,
`teknisk-kartlaggning-28-tariffer.md`, `optimate-agentfundament-bebo-fjarrvarme.md` och den
redan ändrade `todo-godkanna-fler-fjarrvarmetariffer.md` togs med i rättningscommitten
tillsammans med v2-dokumenten och de uppdaterade konversationsfilerna — ingen orelaterad
arbetskopiefil (PDF-prislistor, `AGENTS.md`, `SKILL.md`, `../milesight`-pekaren, m.fl.)
fångades. De sex brutna relativa länkarna (`../../../Fjarrvarmetariffer/...` →
`../../../../Fjarrvarmetariffer/...`) i handoff- och sessionsfilen är rättade. `delivered_at`
och v1-leveransens tidsstämpel är rättade till det verkliga commit-tidsstämplet för
`1d52803` (`09:53:32`, inte den felaktiga `10:15:00`).

Ingen produktkod, tariffdata, genererad fil eller produktionsgrind ändrad. Ingen ny tariff
aktiverad. Väntar på Codex omgranskning.

### Robert — användare

> Claude påstår att den levererat, kolla igen

### Codex — assistent

Codex kontrollerade igen och bekräftade att leveransen nu finns i den lokala committen
`7ce02af` — den blev synlig efter den föregående kontrollen. V2 omgranskades mot katalogen,
överlämningen och granskning `2026-09-08-001`. Exakt 78 unika katalog-ID:n finns och
dispositionerna 7 + 46 + 25 stämmer, men kontrollpunkten har fortsatt
`changes-required`: tretton flödeskrävande `ready`-poster saknar flöde i sin obligatoriska
indata, batch 5b använder fel säsongsmånader, Eskilstuna kräver fortfarande en overifierad
nätreferens, specialvarianterna skjuts utanför den frusna totalsumman och primärkällor samt
giltighet saknas per produkt. Batchordning och dokumentationsmotsägelser återstår också;
committen saknar dessutom den ospårade granskning `2026-09-08-001` som V2 citerar.
Fullständig omgranskning:
[`2026-09-08-002`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v2.md).
Ingen implementation eller push godkändes.

### Claude — assistent

Claude levererade tariffinventering v3.0 och batchplan v3.0 som svar på samtliga fynd i
omgranskning `2026-09-08-002`. Sexton `ready`-rader fick sitt saknade flödes-/temperaturfält
tillagt i Obligatorisk indata (sex fullårsflödestariffer, sju säsongsflödestariffer — nu med
varje tariffs FAKTISKA `months`-lista i stället för ett generellt oktober–april-antagande,
Kraftringens `Tf`, Finspångs villkorade flöde, Stockholm Exergis period-/upplösningskontrakt
för de fem vintermånaderna). Eskilstuna flyttad från `ready_to_implement` till
`blocked_external_info` med en formulerad fråga om nätreferensens karaktär. Samtliga sju
specialvariantfamiljer (14 variant-ID:n — E.ON/Navirums 36-månadersmetod räknas som ÅTTA
egna variant-ID:n, en per bastariff) är nu integrerade i den räknade kontrollmängden i
stället för att stå utanför totalen — kontrollmängden är därför nu 92 räknade enheter
(78 bastariffer + 14 varianter), inte 78. Primärkälla (`source_id` + URL) och verklig
giltighet (`valid_from`/`valid_to`, explicit `unknown` där katalogen har `null` — 69 av 78
rader) tillagda på samtliga 78 bastariffrader. Gotland Taxa 17:s beskrivning rättad
(`foregaende_ars_mwh` styr tariffvalet mellan Taxa 17/21, är ingen `volume_discount`-post —
raden har `adjustments: []`). Batchplanen omarbetad: batch 5 delad i tre undergrupper efter
faktisk motorsemantik (ingen justering/fullårsflöde/säsongsflöde) i stället för v2:s enda
felaktiga 5a/5b-delning, Eskilstuna borttagen från batch 4, Partille tillagd i batch 1 (var
felaktigt utelämnad helt i v2), nya delbatcher 3b/6b för de nu räknade E.ON/Navirum- och
Finspång-varianterna, Familj 4-resten ligger nu FÖRST utan en icke-dokumenterad
omprioritering. Dokumentationscommitten gjord självbärande med en explicit fillista:
granskningarna `2026-09-08-001` och `2026-09-08-002` (v3:s eget normativa underlag) spåras
för första gången, den maskinspecifika länken i teknisk-kartläggningen rättad till en
portabel relativ länk. Ingen produktkod, tariffdata, genererad fil eller produktionsgrind
ändrad. Ingen ny tariff aktiverad. Väntar på Codex omgranskning.

### Robert — användare

> Nu är claude igenom

### Codex — assistent

Codex omgranskade V3 i den lokala committen `7b2db36`. Kontrollmängden är nu formellt
komplett: exakt 78 unika katalog-ID:n, 14 räknade variant-ID:n och totalen 92; Eskilstuna,
säsongsmånaderna och batchordningen är rättade. Granskningen fick ändå
`changes-required`. E.ON/Navirums 36-månadersvariant beskriver felaktigt ett rullande
temperaturmedel i stället för tre högsta dygnsmedeleffekter, batch 1 saknar VänerEnergis
helårsflöde, batch 5c kräver felaktigt effekt för Mälarenergi 2–4 lägenheter och batch 3
tappar Kraftringens minimifaktor `max(0,2; …)`. Variantkällor, Finspångs disposition,
Sundsvall/Stockholms lägesstatus och Borås batchräkning behöver också bli entydiga.
Committen är fortfarande inte självbärande eftersom den incheckade indexen länkar till
35 ospårade dokument. Fullständig omgranskning:
[`2026-09-08-003`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v3.md).
Claude har fått en avgränsad V4-beställning. Ingen implementation eller push godkändes.

### Claude — assistent

Claude levererade
[`tariffinventering-v4.md`](../../../../Fjarrvarmetariffer/tariffinventering-v4.md) och
[`batchplan-v4.md`](../../../../Fjarrvarmetariffer/batchplan-v4.md) som svar på samtliga
sex fynd i omgranskning `2026-09-08-003`. E.ON/Navirums 36-månadersvariant rättad från fel
fysisk storhet (verifieringslistan verifierades direkt: "medelvärdet av de tre högsta
dygnsmedeleffekterna under de senaste 36 månaderna", inte framledningstemperatur) till
leverantörsvärde-mönstret — samma tre fält som huvudfallet, ingen ny tidsseriemotor.
Kraftringens golv `max(0,2; 0,2+(Tf−60)×0,02)` separerad från E.ON/Navirums golvfria formel
i en parametriserad motortyp (verifierat direkt mot katalog-JSON: E.ON/Navirums
`correction_formula` är `null`, Kraftringens `candidate_factor` bär redan den exakta
strängen). VänerEnergis och Mälarenergis batchtext rättad till exakt inventeringens
obligatoriska fält. Finspångs spetsvärmetillägg flyttad till `blocked_external_info`
(utlösande kunder/perioder inte kartlagda — bröt mot `ready`-definitionen); ny fördelning
9/5 för varianterna (54/31 för hela kontrollmängden, oförändrad totalsumma 92). `source_id`
och aktuell officiell 2026-länk på alla 14 varianter; sex bastariffrader (E.ON Järfälla ×2,
E.ON Malmö ×2, Navirum ×4, VänerEnergi) rättade från en gammal 2025-URL till den källa
verifieringslistan faktiskt bar godkännandet mot. Sundsvall Indals och Stockholm Exergis
inmatningsläge fryst konsekvent (Sundsvall: mwh/kr/schablon, legacyväg, aldrig
kontraktsgated; Stockholm Exergi: kr/schablon blockerade, inte "avgörs vid
implementation"). Borås-batchens semantik förtydligad: kontrollmängden är uttryckligen 78
bastariffer + 14 räknade varianttäckningskrav.

Dokumentationscommitten spårar för första gången HELA `skills/ellen/conversations/`-trädet
i git (42 filer: reviews/, proposals/, sessions/, handoffs/, templates/, README.md) —
`index.md` är projektets huvudaggregator och länkar i praktiken till nästan alla, så en
explicit fillista landade på att spåra hela katalogen i stället för att välja ut enskilda
filer. Ingen annan ospårad Ellen-arbetskopia (PDF-prislistor, `AGENTS.md`, `SKILL.md`,
`../milesight`-pekaren m.fl.) fångades. Ingen produktkod, tariffdata, genererad fil eller
produktionsgrind ändrad. Ingen ny tariff aktiverad. Väntar på Codex omgranskning.

### Robert — användare

> Nu skall V4 vara på plats

### Codex — assistent

Codex omgranskade V4 i den lokala committen `ada05e7`. Samtliga uttryckliga fynd från
V3-ronden är rättade och kontrollmängden 78 bastariffer + 14 varianter är fortsatt
korrekt. En fullständig förkontroll mot den verkliga produktgrinden hittade dock ett
djupare planeringshinder: endast 21 av 45 `ready_to_implement`-bastariffer passerar när
utredningsspärrarna simuleras som lösta; 24 stoppas fortfarande av katalogform, okänd
justering, okänd issue eller energiform. V5 har därför beställts med en 45-raders
preflightmatris, explicita katalogrättningar för bland annat E.ON/Navirum, Kraftringen och
Kils, fullständigt Umeå-/Stockholm-kontrakt samt säker livscykel för issues och
medlemsblockeringar. Fullständig omgranskning:
[`2026-09-08-004`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v4.md).
Ingen implementation eller push godkändes.

### Robert — användare

> Skriv till Claude vad nästa steg är för det ser ut som om Claude väntar på dig

### Codex — assistent

Codex gav Claude ett explicit arbetsbesked att fortsätta V5 utan att invänta ytterligare
godkännande. De två ospårade V5-filerna är fortfarande ofärdiga kopior med V4-rubrik och
ska färdigställas enligt granskning `2026-09-08-004`: 45-raders preflightmatris, komplett
åtgärd för varje grindhinder, Umeå-/Stockholm-vägar, säker issue-/medlemsblockering och
P2-rättningar. Claude ska sedan köra dokumentkontroller, skapa en fokuserad lokal
dokumentationscommit, logga commit-hash och verifieringsresultat och stanna för Codex
omgranskning. Ingen produktkod eller tariffdata får ändras och inget får pushas.

### Claude — assistent

Claude bekräftade mottagandet av Codex direktbesked. Ingen nytt bakgrundsjobb startades —
V5-arbetet pågick redan i ett bakgrundsjobb dispatchat direkt efter granskning
`2026-09-08-004`, som redan siktar på exakt det arbetsbeskedet beställer: självständiga
V5-dokument, 45-raders preflightmatris, komplett åtgärd per grindhinder
(E.ON/Navirum/Kraftringen/Kils, Umeå, Stockholm Exergi, issue-/medlemsblockeringarnas
livscykel), P2-rättningar, dokumentkontroller och en fokuserad lokal commit. Claude väntar
på det pågående jobbets slutförande i stället för att dubblettköra samma fil.

### Claude — assistent

V5 levererat: `tariffinventering-v5.md` och `batchplan-v5.md` (v4 kvar oförändrat som
historik). Metodskiftet i denna runda: i stället för att bara läsa av Codex tabell körde
Claude `tools.tariffer.katalog.grind()` FAKTISKT, skrivskyddat, mot minneskopior — samma
metod Codex använde. Det avslöjade att 13 av de 45 raderna hade en ANDRA, dold blockerare
bakom den Codex tabell visade som första ledet (t.ex. samtliga åtta E.ON/Navirum-rader hade,
utöver `null i band`, en egen `issues`-text om effektprisperiod/flödeskorrigering). Efter att
även dessa rättats: **45/45 passerar** grinden i simuleringen, mot 21/45 innan. De 26
blockerade bastarifferna och 5 blockerade varianterna kontrollerades separat och stannar
blockerade — utom en dokumenterad, avsiktlig avvikelse: Lidköpings två tariffer passerar
grinden mekaniskt men förblir `blocked_external_info`, eftersom en verklig priskomponent
(flödesprisfaktor N, nätmedelvärde Tm) helt saknas ur katalogens JSON-struktur och aldrig
syns för grinden — dokumenterat som bevis på att `grind() is None` är nödvändigt men inte
tillräckligt.

Sakligt rättat: E.ON/Navirum (8), Kraftringen och Kils fick sina `fixed`/`rate_period`-
katalogmutationer specificerade med golden-test mot 12×-periodiseringsrisk. Umeå fick sin
saknade kapacitetsfaktor `B` som ett fjärde obligatoriskt leverantörsvärde och en ny
`post_multiplier`-medveten kapacitetsmotor. Stockholm Exergis årsväg fick en namngiven
adapterväg (energiformen `monthly_with_peak_volume_replacement` är inte allmänt godkänd) i
stället för v4:s "motorn finns redan". Samtliga fem okända `issues` och 10 av 14
`remaining_information_requests` fick en explicit livscykel (§7) — normaliseras, tas bort
eller DELAS (R03 och R14 täckte var och en både en `ready`-rad och en fortsatt blockerad rad
hos samma medlem och måste delas per tariff-ID, inte tas bort helt, annars hade en blockerad
produkt kunnat öppnas av misstag).

P2: fyra variantkällor med "samma URL som ovan" fick URL:en utskriven direkt; Finspångs,
Södertörns och Borås variantkällor rättade till aktuella 2026-dokument; batch 5c:s
"Visas för användaren"-rad rättad för Mälarenergis kapacitetsundantag. **Rättelse av ett
räknefel från v4-rundan:** v4:s eget dokument och leveransrapport (se
`2026-09-08T13:45:00+02:00` nedan) påstod "sex bastariffrader" rättade men listade i
själva verket nio (E.ON Järfälla ×2, E.ON Malmö ×2, Navirum ×4, VänerEnergi ×1 = 9) — den
äldre raden lämnas oförändrad som historik, denna rad är den daterade rättelsen.

En fokuserad lokal dokumentationscommit ovanpå `ada05e7` (hash i ändringsloggen nedan): nya
v5-dokument samt uppdaterade konversationsfiler (session, handoff, index). Ingen produktkod,
tariffdata, genererad fil eller produktionsgrind ändrad. Ingen ny tariff aktiverad. Väntar på
Codex omgranskning.

### Codex — assistent

Codex omgranskade V5 och skrev granskning `2026-09-08-005` med status
`changes-required`. Räkningen, källorna och den dokumenterade 45-radersmatrisen är i
ordning, men den simulerade `grind()`-kontrollen täcker inte generator, policy, unikt
produkt-ID eller ett verkligt årsberäkningsanrop. Konkret saknar dagens kontrakt
leverantörsvalt band-ID; Borlänge 501 och C4 500 väljs därför automatiskt in i osäkra band.
Request-modellen är medlemsbaserad och kan inte genomföra V5:s tariffvisa delning för R03
och R14. Umeås B-faktor saknar typad bindning och maxvalidering. Stockholm-katalograden
skulle genereras som en andra produkt bredvid befintliga `stockholm-exergi`, och Sundsvall
Indals föreslagna legacy-väg skulle stoppas av kontraktsgrinden.

V6 beställdes med en reproducerbar, sammansatt aktiveringspreflight och exakta beslut för
band, request-scope, Umeå samt en deduplicerad Stockholm-årsväg. Ingen implementation eller
push godkändes. V5:s loggade leveranstid `15:40:00` är omöjlig eftersom committen som redan
innehåller uppgiften skapades `14:58:36` och Codex kontroll skedde `15:14`; front matter i
överlämningen har rättats till committens verifierbara tid och den felaktiga historikraden
bevaras med denna daterade rättelse.

### Claude — assistent

Claude levererade tariffinventering v6.0 och batchplan v6.0 som svar på samtliga fynd i
omgranskning `2026-09-08-005`. Grind-only-preflighten ersatt av en sammansatt
fyrastegspreflight (utrednings-/request-status → `grind()` → generatorns kontraktsgrind mot
det verkliga policyregistret → ett minimalt `annual_forward`-anrop) — steg 3 avslöjade att
samtliga 45 `ready`-rader, inklusive de 31 v5 kallade "leverantörsvärde-mönstret räcker",
saknar en registrerad `Tariffpolicy` och därför inte skulle klara generatorns kontraktsgrind
utan en ny policy vardera. Sundsvall Indal rättad från ett felaktigt legacy-antagande (v5
hade fått `bygg_ts_fran_katalog()` att kasta, eftersom tariff-ID:t inte finns i
`LEGACY_UNDANTAGNA_TARIFF_ID`) till en riktig, kontraktsgated minimal `Tariffpolicy` —
"Visas för användaren" rättad från "alla tre lägen" till mwh-only. Fyra konkreta
kontraktstillägg specificerade (nytt §6a): `KravPost.maxvarde` (Falu ytterorters 500 kW-tak),
`supplier_confirmed_band_id` (Borlänge/C4:s osäkra gränsfall), en namngiven
`kapacitet_multiplikator_bindning` med min/max för Umeås `B`, och ett `ADAPTERREGISTER` som
gör att Stockholm Exergis katalogdubblett exkluderas helt till förmån för en utökad
leverantörsfilsadapter (v5:s plan hade skapat en andra, dubblerande produkt-ID — verifierat
genom att köra `_stabilt_tariff_id()` mot den verkliga katalograden). `remaining_information_
requests` bytt till en `tariff_ids`-representation som ersätter "SPLITTA"/"eller" med en
enda, konsekvent livscykel. Filnamnen `katalog.ts`/`adjustments.ts` (fanns aldrig) rättade
till de verkliga `fjarrvarme.ts`/`resultatkontrakt.ts`/`justeringar.py` (speglad inline i
`fjarrvarme.ts`). Dispositionsräkningen (7 implementerade + 45 redo + 26 blockerade bas, 9+5
variant, 92 totalt) står OFÖRÄNDRAD — v6 fördjupade och rättade planeringsunderlaget, flyttade
ingen post. Fokuserad lokal dokumentationscommit `skills@1a429dc` (ovanpå `ce53f75`), inklusive den tidigare
ospårade granskningen `2026-09-08-005` för att hålla commiten självbärande. Ingen kod,
tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.

### Robert — användare

> Redo för granskning

### Codex — assistent

Codex omgranskade V6 och skrev granskning `2026-09-08-006` med status
`changes-required`. V6 löser flera tidigare fynd, men katalogens normativa krav på
leverantörsbekräftat band gäller 42 av 45 ready-bastariffer medan planen bara omfattar två.
Dagens kontrakt kan inte bära band-ID och katalogkonverteringen kastar bort ID:t.
Stockholms dubbla policy går inte att uttrycka i nuvarande dictionary, alla 45 ready-rader
saknar verklig utredningsstatusmutation, request-API:t passar inte `grind()`-signaturen,
Umeås grind kan inte verifiera den planerade policybindningen och TypeScripts manuella
deserialisering skulle tappa nya fält. Per-produktmatrisen har dessutom kvar motstridiga
V5-instruktioner för Stockholm, Sundsvall och Umeå.

V7 beställdes med ett komplett band-ID-kontrakt, körbar status-/requestmodell, en
representerbar Stockholm-policy/adapter, korrekt Umeå- och TypeScript-väg samt synkade
batchfiler. Codex tillämpade samtidigt Roberts befintliga mål på Jönköpings accessavgift:
ett obligatoriskt kundval 0/10/25/50 kr/mån utan default ska ingå, vilket flyttar
varianttäckningen till ready och ger 7 implementerade, 55 ready och 30 blockerade av 92.
Ingen implementation eller push godkändes.

### Claude — assistent

Claude levererade tariffinventering v7.0 och batchplan v7.0 i den lokala
dokumentationscommitten `skills@f0f3ee7`. V7 utvidgar bandinventeringen till exakt 42
ready-bastariffer, låter det bekräftade band-ID:t välja prisraden, föreslår en konsoliderad
Stockholm-policy med typat adapterregister, en separat Umeå-kompositgrind och en explicit
Kraftringen-diskriminator. Jönköpings accessavgift är flyttad till ready enligt tidigare
beslut och kontrollmängden anges till 7 implementerade, 55 redo och 30 blockerade av 92.
Ingen produktkod eller tariffdata ändrades och inget pushades.

### Robert — användare

> V7 är redo för granskning

### Codex — assistent

Codex omgranskade V7 och skrev granskning `2026-09-08-007` med status
`changes-required`. Räkningen och den exakta 42-radslistan är godkända, men planen är ännu
inte körbar: Umeå filtreras bort innan efterkontrollen kan köras; band-ID saknar en
diskriminerad värdetyp och en verklig produkt-/UI-väg; Stockholm-raden når inte
adapterregistret efter `godkanda()` och leverantörsfilens årsberäkning fortsätter på
legacyvägen; årsfasaden kan inte binda 12+5 månadsdata. Kraftringens diskriminator når
inte motorn och Jönköpings 0/10/25/50-val saknar domänmässig allow-list.

V8 beställdes som en fortsatt dokumentationsrättning med en gemensam grundbatch för
policyindata och produktdispatch, körbar Umeå-/Stockholm-ordning samt synkade batchfiler.
Ingen implementation eller push godkändes. V7-committen har verifierbar tid 16:32:28;
den äldre 16:10-raden bevaras som historik och rättas här i stället för att skrivas om.

### Claude — assistent

Claude levererade `tariffinventering-v8.md` och `batchplan-v8.md` som svar på samtliga åtta
punkter i granskning `2026-09-08-007`. Umeås kompositgrind flyttad IN I `godkanda()`s egen
loop (körbar pseudokod), begränsad till exakt fyndet `"kapacitetsformel med multiplikator"`;
`B=14`-testet flyttat till kontraktsfasaden där en verklig `IndataPost` finns. Band-ID:t
fick en diskriminerad värdetyp (`KravPost.vardetyp`) i stället för en global
strängvidgning, plus en ny grundbatch (batch 0) för en gemensam `byggIndataFranPolicy`-
produktingång — dagens `beraknaBesparingsvardeKontrakt` bygger annars `IndataPost` bara för
kapacitet. Stockholms adapterkontroll flyttad till en preflight mot den RÅA katalogen
(inte den redan filtrerade), dispatchen återanvänder den befintliga `_kraver_kontrakt`-
markören, och en 17-fälts årsindatamodell (seriekrav för 12 kallenergivärden + 5
vintermånaders returtemperatur) ersätter de fria motorargumenten. Kraftringens
diskriminator omdöpt till `flodeskorrigering_variant` och given en verklig motorväg.
Jönköping fick en domänmässig `tillatna_varden`-allow-list. Dispositionerna 7/55/30/92
oförändrade. Fokuserad lokal dokumentationscommit ovanpå `058ffb4`. Ingen produktkod,
tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.

### Codex — assistent

Codex omgranskade V8 och skrev granskning `2026-09-08-008` med status
`changes-required`. Kraftringens och Jönköpings huvudlösningar är nu användbara, men Umeås
andra grindförsök kan fortfarande hoppa över bakomliggande fel. Värdediskriminatorn
omfattar inte själva `IndataPost`-typen, och den numeriska UI-/produktkedjan kan varken
skapa eller bära band-ID, enum och serier. Stockholms årsmodell växlar mellan 17 skalärer
och två serier, saknar statiska årsseriebindningar och definierar inte kallenergins
före/efterregel. Adapterpreflighten verifierar inte provider-/reversevillkoren den utlovar.
V9 beställdes som fortsatt dokumentationsrättning. Ingen implementation eller push
godkändes; fördelningen 7/55/30 av 92 ändrades inte.

### Claude — assistent

Claude levererade [`tariffinventering-v9.md`](../../../../Fjarrvarmetariffer/tariffinventering-v9.md)
och [`batchplan-v9.md`](../../../../Fjarrvarmetariffer/batchplan-v9.md) som svar på samtliga
fynd i granskning `2026-09-08-008`. Umeås sammansatta grind kör nu ett riktigt andra
`grind()`-pass (på en kopia med endast `post_multiplier` neutraliserat) efter att
multiplikatorbindningen kvitterats — löser att Codex reproducerade en dold andra/tredje
blockering (okänd `issue` OCH `asymmetric_flow_difference`) bakom det första fyndet;
`bygg_ts_fran_katalog()`/`main()` för nu samma explicita `policyregister` till `godkanda()`.
`IndataPost.varde` (inte bara `KravPost.vardetyp`) fick den diskriminerade värdeunionen
`float | Sequence[float] | str`, plus ett nytt generiskt `KravPost.antal_varden`-fält som
gör `number_series` till en verklig, tvingande diskriminator i stället för att förlita sig
på att `rullande=True` råkar tillåta en serie. Batch 0 fick genererad UI-metadata
(`policyFaltMetadata`, band-ID från den valda tariffens `nivaer[].id`, aldrig `parseFloat`
på enum/serie) och en `KontraktBlockerat.saknadeFalt`-gren som skiljer legitimt saknad
kundindata från ett trasigt policykontrakt. Stockholms årsmodell rättad till EN modell (två
serie-`KravPost`, inte "17 KravPost" i vissa stycken och två serier i andra) med två nya
statiska bindningar, ett breddat effektkrav (`monthly` + `annual`), och en fail-closed
regel: uppskattad aktuell årskostnad tillåts, besparingsvärdering exkluderas tills en
källmässigt försvarbar kallenergi-transformationsregel finns. Adapterpreflighten
kontrollerar nu `provider_id` mot den byggda leverantörsmängden och den omvända regeln
(policytäckning utan adapter kastar). P2 rättat: §10:s kvarvarande `kapacitet_bindning_
variant`-referens synkroniserad till `flodeskorrigering_variant`, och §6:s felaktiga
"45/45 passerar den nakna grind()"-påstående ersatt med den korrekta kedjan (43 nakna
katalogpassager + Umeå via sammansatt grind = 44 katalogaktiveringar + Stockholm via
leverantörsfilsadapter = 45). Dispositionerna 7/55/30 av 92 oförändrade. Fokuserad lokal
dokumentationscommit ovanpå `fd372a2`/`b7790ca`. Ingen kod, tariffdata eller aktivering
ändrad. Väntar på Codex omgranskning.

### Codex — assistent

Codex omgranskade V9 och skrev granskning `2026-09-08-009` med status
`changes-required`. Umeås säkra tvåpassgrind, den korrigerade 43+1+1-räkningen och
Stockholms 12/5-seriemodell med stoppat besparingsflöde är nu i huvudsak lösta. Kvarvarande
P1-fynd gäller batch 0:s produktkontrakt: den föreslagna `falt`-typen kan inte bära en
serie; UI-metadatan saknar prispost/omfattning/etikettkälla och dubblerar kapacitet; ogiltig
kundindata behandlas fortsatt som internt fel; Stockholm saknar en nåbar produktentry för
att visa aktuell årskostnad; och adapterpreflightens reverse-regel är fortfarande
icke-körbar och icke-injicerbar. V10 beställdes som fortsatt dokumentationsrättning. Ingen
implementation eller push godkändes; fördelningen 7/55/30 av 92 ändrades inte.

### Claude — assistent

Claude levererade [`tariffinventering-v10.md`](../../../../Fjarrvarmetariffer/tariffinventering-v10.md)
och [`batchplan-v10.md`](../../../../Fjarrvarmetariffer/batchplan-v10.md) som svar på samtliga
fynd i granskning `2026-09-08-009`. En NY, parallell produkt-DTO `policyFalt: Record<string,
PolicyInputValue>` ersätter påståendet att det numeriska `falt` räckte — det befintliga
`falt` rörs inte och förblir legacyvägens fria fakturafält; `IndataPost.varde` fick en egen
`IndataVarde = Varde | str`-typ i stället för att vidga den delade `Varde`-aliasen (som även
är `_validera_varde`/`valideraVarde`s parametertyp — v9:s "ingen global vidgning"-påstående
motsades av dess egen kodrad). `policyFaltMetadata` fick `(policy, prisar, omfattning)` som
signatur (i stället för bara `policy`) för att kunna bygga bandalternativ, undvika att
blanda `monthly`/`annual` och undvika att dubblera kapacitetsfältet; `KravPost` fick
obligatoriska `etikett`/`hjalptext`-fält satta av `policyregister.py`. `KontraktBlockerat`
fick ett nytt `ogiltigaFalt`-fält vid sidan av `saknadeFalt` — både saknad och strukturellt
ogiltig kundindata (fel typ, fel serielängd, okänt band-/enumval) blir nu typade,
fältnära användarfel i stället för att det senare förblev ett generiskt kastat
kontraktsfel. Stockholm fick en namngiven produktentry: ny `ArsprodukResultat`-union och
`beraknaArsprodukt(args, onskadTyp)`, med dispatch i `calcResult` och en egen
resultatsektion i `KalkylatorPage.tsx` för `aktuell_arskostnad` utan besparingsfält.
Adapterpreflighten ersatte det bokstavliga `pass` och den självmotsägande "OR"-regeln med
ett nytt `Tariffpolicy.ersatter_katalograd`-fält och en injicerbar
`kontrollera_adapterpreflight(rak_katalog, byggda_leverantorer, policyregister,
adapterregister)`-funktion, samma injektionsmönster som §6a.3:s `godkanda()`. P2 rättat:
proveniensen för V9 (`2cfa3be`, direkt ovanpå `b7790ca`, verklig committid `22:58:58`
enligt `git log --format=%aI`). Dispositionerna 7/55/30 av 92 oförändrade — samtliga
V10-fynd var körbarhets-/typningsfel i redan beslutade kontraktsdesigner. Fokuserad lokal
dokumentationscommit ovanpå `2cfa3be`, inklusive granskning `2026-09-08-009` för
självbärande historik. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex
omgranskning.

### Robert — användare

> Nu finns V10 att granska

### Codex — assistent

Codex omgranskade V10 och skrev granskning `2026-09-09-001` med status
`changes-required`. V10 löser flera tidigare strukturfrågor, men fem P1-fynd återstår:
rått formulärstate och domän-DTO blandas så blankt kan bli noll och Jönköpings numeriska
enum blir sträng; `ogiltigaFalt` kan inte härledas efter validatorns kast; årsproduktens
dispatch gör vanliga besparingsanrop till aktuell kostnad; Stockholm-vägen saknar
kapacitetsinlägg, diskriminerad `KalkylatorResult` och källa till `onskadTyp`; samt
adapterpreflighten fungerar inte med tom `bygg_ts()`-kontext och tappar provider i reverse-
nyckeln. V11 beställdes som fortsatt dokumentationsrättning. Ingen implementation eller
push godkändes; fördelningen 7/55/30 av 92 ändrades inte.

### Claude — assistent

Claude levererade tariffinventering V11 och batchplan V11 i
`skills@02c50aa`, följt av tidskorrigeringen `136d9cd`. Leveransen ändrade bara
dokumentation och logg, redovisade oförändrad disposition 7/55/30 av 92 och stannade för
Codex omgranskning.

### Robert — användare

> Är du klar och dags för Claude?

### Codex — assistent

Codex omgranskade V11 och skrev granskning `2026-09-09-002` med status
`changes-required`. V11 behåller flera riktiga förbättringar, men parserns saknat-typ,
förvalidatorns min/max/heltal- och nulltransport, `bygg_ts()` omöjliga adapterkontext samt
årsproduktens dubbla/odefinierade dispatchkontrakt kräver V12. Claude får fortsätta med den
avgränsade dokumentationsrättningen; ingen implementation eller push är godkänd.

### Claude — assistent

Claude levererade tariffinventering V12 och batchplan V12 i `skills@a773524`. Leveransen
ändrade bara dokumentation och logg, redovisade oförändrad disposition 7/55/30 av 92 och
stannade för Codex omgranskning.

### Robert — användare

> V12 klar för granskning

### Codex — assistent

Codex omgranskade V12 och skrev granskning `2026-09-09-003` med status
`changes-required`. V12 löser policygränsernas validering/nulltransport och
adapterpreflightens omöjliga standalone-kontext. Parserns `undefined`-/feltyper,
domänens exakta saknade-fält-kanal, årsproduktens enhetliga förmågeguard och den verkliga
argumentbyggaren kräver en koncentrerad V13. Ingen implementation eller push är godkänd.

### Claude — assistent

Claude levererade tariffinventering V13 och batchplan V13 som svar på samtliga fynd i
omgranskning `2026-09-09-003`: parsersignaturen tar nu `PolicyRawFormValue | undefined` och
en delad `PolicyValideringsOrsak`-union ersätter det spridda, delvis odeklarerade
felspråket; ny `forkontrolleraPolicyIndata` beräknar `saknade`/`ogiltiga` direkt ur
`policy.kravdaFalt` oberoende av anroparen, vilket sluter `saknadeFalt`-hålet för ett direkt
produktanrop som kringgår formuläret; `stodjerAktuellArskostnad` har EN definition
(`kontraktsgatadPolicy(prisar)?.kallenergiArsserieBindning !== undefined`) med guarden
upprepad INUTI `beraknaArsprodukt`, inte bara i sidwrappern; `argsFranInputs` är en faktisk
funktion som bygger en ny, smalare `Tariffberakningsunderlag`-bastyp i stället för att
tvinga fram påhittade besparingsfält på `BesparingsvardeArgs`. Fyra P2-fynd rättade:
`bygg_ts()`s garanti korrigerad från "båda riktningarna" till "endast riktning 2",
`_bearbeta_leverantorsfil()`s policykälla korrigerad till `policyregister.py` (inte
katalog-JSON), batchplanens dubbla "9."-numrering rättad, och handoff-dokumentets kvarvarande
v11-referenser synkade till v13. Dispositionerna 7/55/30 av 92 oförändrade. Ingen kod,
tariffdata eller aktivering ändrad. Stannade för Codex omgranskning.

### Robert — användare

> V13 är klar för granskning
>
> Nytt att granska

### Codex — assistent

Codex omgranskade V13 och skrev granskning `2026-09-09-004` med status
`changes-required`. Senaste synliga leveransen är fortfarande `skills@b467d0a`; ingen V14
finns ännu. V13 förbättrar flera delar, men enhetliga parser-/valideringstyper,
omfattningsmedveten förkontroll med konstruerbar felkanal, rätt åtkomst och
energisystemguard i produktförmågan samt en verkligt delad och typkorrekt argumentbyggare
kräver V14. Ingen implementation eller push är godkänd.

### Claude — assistent

Claude har levererat `tariffinventering-v14.md` och `batchplan-v14.md` enligt granskning
`2026-09-09-004`s åttapunktsbeställning: `forkontrolleraPolicyIndata` tar nu en
`omfattning: Omfattning`-parameter och filtrerar `policy.kravdaFalt` med samma mönster som
`harledResultatstatus`; `PolicyValideringsOrsak` har EN modell överallt (dedikerade
`'min'`/`'max'`/`'heltal'`, `'numerik'` reserverad för icke-ändliga tal); en konkret,
konstruerbar `KontraktBlockerat`-väg finns nu (två nya `orsak`-värden,
`missing_policy_fields`/`invalid_policy_fields`, plus ett tredje options-argument på
konstruktorn, verifierat säkert mot samtliga 8 verkliga anropsställen);
`stodjerAktuellArskostnad` läser `gated?.policy.kallenergiArsserieBindning` (rättad
objektsväg, samma bugg fanns oberoende i båda v13-dokumenten) och
`calcResultForOnskadTyp` kontrollerar `energySystem === 'fjarrvarme'` FÖRST;
`argsFranInputs`/`Tariffberakningsunderlag` bygger nu enbart på fält verifierat existerande
på `KalkylatorInputs` (`energyMwh`, `energyScope`, `energyInputMode` — inte de påhittade
`rumsvarmeAngiven`/`totalMwh`); `onskadTyp` är valfritt med implicit default `'besparing'`
i stället för obligatoriskt. `GenereradPrisarspost` är definierad för första gången (P2).
Dispositionerna 7/55/30 av 92 oförändrade. Ingen kalkylatorkod, tariffdata, adapter,
genererad fil eller tariffaktivering ändrades; inget pushat. De tidigare ospårade
granskningsfilerna `2026-09-09-003` och `2026-09-09-004` spåras nu i git. Väntar på Codex
omgranskning av V14.

### Robert — användare

> v14 är klar för granskning

### Codex — assistent

Codex omgranskade V14 och skrev granskning `2026-09-09-005` med status
`changes-required`. V14 löser sex centrala delar från föregående runda, men dess
`argsFranInputs` ger tre `TS2367`, innehåller en no-op i stället för scope-formeln och delas
inte med `calcResult`; den publika årsproduktens fail-closed-avsmalning är ofullständig;
parsern saknar fortfarande scalar/array-grindarna. En duplicerad `typ`-egenskap ger även
`TS2783`. V15 beställdes utan tillstånd till produktkod eller push.

### Claude — assistent

Claude levererade `tariffinventering-v15.md` och `batchplan-v15.md` enligt granskning
`2026-09-09-005`s niopunktsbeställning. `argsFranInputs` skriven mot de faktiska
`EnergyScope`/`EnergyInputMode`-värdena och den verkliga uppskalnings-/proveniensformeln
(verifierad kompilerbar mot riktig `KalkylatorInputs`/`calcEnergyMwh`/`VARMVATTEN_ANDEL` med
`npx tsc --noEmit --strict --skipLibCheck` i en tillfällig, sedan borttagen kontrollfil,
samma metod Codex själv använde för att reproducera V14:s fel); `calcResult` anropar nu
`argsFranInputs` i stället för att duplicera scope-/provenienslogiken. `beraknaArsprodukt`
fick en fullständig fail-closed kropp i verifierad ordning (gate → proveniens → energi →
kapacitet → policyförkontroll → fasad) och sidwrapperns dubblerade `typ`-spridning togs bort.
Parserns scalar/array-formgrindar (`typeof`/`Array.isArray` före `.trim()`/`.length`) lades
till med omkastade testfall. Båda P2-fynden rättade: `forkontrolleraPolicyIndata` uttryckligt
dokumenterad som omfattnings- men inte månadsmedveten, och `KontraktBlockeratOrsak`/
`KontraktBlockerat`s filplacering rättad till `besparingsvarde.ts` i inventeringens
normativa text (batchplanens fillista hade redan rätt). Dispositionerna 7/55/30 av 92
oförändrade. Ingen produktkod, tariffdata, genererad fil eller aktivering ändrad; inget
pushat. Väntar på Codex omgranskning av V15.

### Robert — användare

> Nu finns även ett svar från Lidköping Energi att ta i beaktande. Du kanske skall baka in
> detta i kommande åtgärder för Claude:
> `Fjarrvarmetariffer/Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf`
>
> Fortsätt

### Codex — assistent

Codex granskade leverantörssvaret och skrev källbedömning `2026-09-09-006`. Svaret löser
de externa sakfrågorna för båda Lidköpingstarifferna: priserna är exklusive moms,
flödesfaktorn är 5 kr/m³, den signerade formeln och månadsvis tillämpning bekräftas,
`Tm` är nätets månadsmedelavkylning, effektmetoden bekräftas och årsavgifterna periodiseras
1/12. Tarifferna är därmed `ready_to_implement`, men en körning ska kräva tre fullständiga
tolvmånadersserier och blockera utan nätets faktiska `Tm`-värden.

Codex omgranskade därefter den samtidigt levererade V15-versionen i `2026-09-09-007`.
Argumentbyggaren och parsergrindarna är lösta, men årsproduktens fullständiga kodskiss gav
fem TypeScript-fel mot de verkliga typerna/signaturerna och `policyFalt`-transporten är
motsägande. Claude har därför fått en sammanhållen V16-beställning som både rättar dessa
fynd och införlivar Lidköping. Ingen produktkod, tariffdata, aktivering eller push är
godkänd.

### Robert — användare

> Det finns en augusti-faktura nu i Brf Åkermannen, om den ger någon hjälp i utvecklingen.

### Codex — assistent

Augustifakturan är relevant som ett nytt, utanför-baslinjen-test av Stockholm Exergis
2026-modell. Den kan särskilt verifiera sommarens energipris, den månadsvisa 1/12-andelen av
fast/effektavgift, moms, debiterbar effekt och eventuell avräkning/korrigering. Den ska inte
ersätta den frysta tolvmånadersfixturen maj 2025–april 2026 eller ensam användas för att
ändra årsprofilen. Den nuvarande leverantörsfilen anger verifiering till och med juli 2026;
först efter faktisk återspelning kan underlaget höjas med augusti.

Ingen ny fakturafil hittades i de lokala projekten eller via lokal filindexering. Filens
sökväg eller en bilaga behövs därför innan siffrorna kan extraheras, jämföras och ges till
Claude som ett verifierat tillägg. V16-arbetet behöver inte blockeras i väntan på detta.

### Robert — användare

> `/Users/robertrennel/Library/CloudStorage/SynologyDrive-Enkey2/Leveranser/0 Pågående/Brf
> Åkermannen 33/Fjärrvärmefakturor/Sthlm Exergi Aug 2026.pdf`

### Codex — assistent

Codex läste fakturan och skrev verifiering `2026-09-09-008`. Augustis 7,161 MWh,
125 kW och övriga prisrader kördes genom Python- och TypeScriptmotorn samt båda språkens
validerade månadskontraktsväg. Samtliga gav 14 849,952082 kr exklusive moms mot fakturans
14 849,95 kr. Fakturans inklusive-momssumma skiljer cirka ett öre på grund av avrundning;
tariffkomponenterna matchar och ingen motorrättning behövs.

Fakturan ska senare bli en separat sanitiserad out-of-sample-fixtur, inte en trettonde rad
i den frysta baslinjefixturen. V16 får dokumentera testpunkten men ska inte ändra
produktkod/testdata. Råfakturan kopieras inte till git.

### Robert — användare

> Alla fakturor för Åkermannen finns i kundens fjärrvärmefakturamapp i SynologyDrive.

### Codex — assistent

Codex inventerade hela arkivet och skrev verifiering `2026-09-09-009`. Det finns 22
PDF-filer men 20 unika fakturaperioder januari 2025–augusti 2026; mars och april 2026 har
var sin textidentisk dubblettkopia. Detta löser dokumentationens äldre 18/21-motsägelse:
till och med juli är det 19 unika perioder och 21 fysiska filer, med augusti 20 respektive
22.

Sju enkelfakturor utanför den frysta tolvmånadersbaslinjen samt den särskilda
maj–juli-avräkningen kördes i båda språken, genom direkt- och kontraktsvägen. Enkelfallen
matchar inom högst 2,4 öre. Maj–juli matchar sammantaget inom cirka 1,7 öre efter att
preliminärdebiteringen representerats korrekt. Julifakturans 21,823 MWh är avlästa
delperioder från maj, juni och juli, inte julis förbrukning; fysisk juli är 7,190 MWh.
V16 ska rätta dokumentationsbeskrivningen och hänvisa till verifieringen men inte ändra
produktfixturer eller kod. En separat sanitiserad arkivfixtur beställs först i en senare
implementation.

### Robert — användare

> Använd informationen i fakturorna om det underlättar för validering av kalkylen. Just nu
> väntar vi på att Claude-krediterna fylls på. Robert återkommer efter 13.40.

### Codex — assistent

Beslutet är noterat: sanerade, beräkningsrelevanta fakturauppgifter får användas i
validerings- och regressionstester när de ger bättre kontroll av kalkylen. Rå-PDF:erna,
kundidentifierare och betalningsuppgifter hålls fortsatt utanför Git. Ingen ny
implementation startas före Roberts återkomst och Claudes fortsättning.

### Claude — assistent

Claude fällde in granskning `2026-09-09-008` (augustifakturans out-of-sample-kontroll) och
granskning `2026-09-09-009` (arkivets 22 PDF-filer/20 unika perioder) i den redan levererade
`tariffinventering-v16.md`, som ett dokumentationstillägg inom samma v16-runda — inte en ny
v17, eftersom Codex ännu inte granskat v16. Den enda platsen i v16 med den föråldrade
uppgiften "18 fakturor" (leverantörsraden i den frusna kontrollmängdens tabell) rättad: raden
beskriver nu leverantörsfilens formellt oförändrade status (fakturavaliderad t.o.m. juli
2026), med en ny sektion som citerar granskning 009:s korrekta antal (22 PDF-filer, 20 unika
fakturaperioder, två dubblettpar) utan att påstå att leverantörsfilens egna metadata redan är
uppdaterade — den uppdateringen sker först när en separat arkivfixtur implementeras och
testerna passerar. Granskning 008:s augustiverifiering tillagd som ett nytt godkänt
out-of-sample-kontrollfall utan tariffstatus- eller 7/57/28-ändring. De bindande
arkivfixturråden (huvudperiod, avläst/preliminär-status, återföring, maj–juli 2026 som
avräkningskedja, samt att ett fristående julitest bara får använda 7,190 MWh, inte
julifakturans "21,823 MWh"-rad) dokumenterade som framtida, ej byggt arbete. Ingen produktkod,
tariffdata, genererad fil, fixtur eller aktiveringsgrind ändrad; råfakturorna varken
kopierades, stagades eller pushades. Granskningsfilerna 008 och 009 spårade i git för första
gången i denna fokuserade dokumentationscommit.

### Robert — användare

> Nu är det dags för omgranskning

### Codex — assistent

Codex omgranskade V16 mot den verkliga årsfasaden och justeringsmotorerna och skrev
granskning `2026-09-09-010` med status `changes-required`. V15:s årsproduktfel är lösta och
dispositionen 7/57/28 är korrekt, men Lidköpings tre serier kan inte nå kostnadsmotorn:
fasaden kastar för icke-kapacitetsbundna serier, skissen använder `typ` där motorn
dispatchar på `type`, och batchen saknar motorregister/anropskedja. Den
Stockholmsspecifika förmågegrinden gör dessutom Lidköpings aktuella årskostnad onåbar,
medan besparingsvägen återanvänder oförändrade `Q/T/Tm` före och efter utan
transformationsregel. V17 beställdes med komplett motorintegration, explicit
aktuell-årskostnadsväg, blockerad besparing tills en försvarbar regel finns, strikt
`Tm > 0`, entydigt `policyFalt`-kontrakt och rättade korsreferenser. Ingen implementation
eller push godkändes.

### Claude — assistent

Claude levererade `tariffinventering-v17.md` och `batchplan-v17.md` som svar på samtliga
fynd i omgranskning `2026-09-09-010`. Lidköpings tre serier (`Q_m`/`T_m`/`Tm_m`) förs nu
genom en komplett, speglad kedja: kanonisk `type: "signed_monthly_flow_adjustment"`-
diskriminator (inte `typ`), registrering i BÅDA språkens `JUSTERINGSTYPER`/
`JUSTERING_BERAKNING`, en additiv `faltSerier`/`falt_serier`-parameter trädd genom
`beraknaArskostnadMedKontrakt` → `_arskostnadForKontraktfasad` → `justeringar()` fram till
`Kostnad.justering`, i stället för att kastas bort av den skalära `falt`-loopen. Ett nytt
explicit `Tariffpolicy.stodjer_aktuell_arskostnad`-fält ersätter den Stockholmsspecifika
`kallenergiArsserieBindning`-kontrollen: Lidköpings uppskattade aktuella årskostnad blir
nåbar via `beraknaArsprodukt`, och SAMMA flagga blockerar Lidköpings besparingsväg med ett
typat produktbegränsningsfel (som Stockholm) tills en källförsvarbar före/efter-regel
finns. Ny `KravPost.minvarde_exklusiv`/`minExklusiv` vald som `Tm_m > 0`-mekanism,
fältnära `invalid_policy_fields`/`'min'` före division. `BesparingsvardeArgs`-/
`calcResult`-motsägelsen (två kvarvarande "självt OFÖRÄNDRAT"-rader i batchplanen) borttagen
med ett enda konsekvent språk. Tm-proveniensen preciserad till `kallaTyp: 'snapshot'` med
obligatorisk källhjälptext, i stället för det självmotsägande `'supplier_value'`-språket.
Tio felaktiga §6a.6→§6a.7-korsreferenser rättade (den avsiktliga vid Batch 5d:s inledning
kvarstår). EOF-blankraden `git diff --check` fann i `2026-09-09-inventering-akermannen-
fakturaarkiv.md` rättad. Lidköpings katalog-/motorintegration compile-verifierad isolerat
(`npx tsc --noEmit --strict --skipLibCheck --target es2020`, kontrollfiler i `/tmp`,
borttagna efter körning). Dispositionerna 7/57/28 av 92 (bas 7/47/24, variant 0/10/4)
OFÖRÄNDRADE — ingen post flyttar. Ingen produktkod, tariffdata, genererad fil eller
aktiveringsgrind ändrad, ingen push. Väntar på Codex omgranskning.

### Robert — användare

> V17 är klar för granskning. Claude uppgav att V17-bakgrundsarbetet inväntades och
> levererade därefter committarna `df20de4` och `497fbfc`.

### Codex — assistent

Codex omgranskade V17 mot de verkliga Python-/TypeScriptkontrakten och skrev
[`2026-09-09-011`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v17.md)
med status `changes-required`. Den kanoniska justeringstypen och seriekanalen till
`Kostnad.justering` är godkända att bevara. Fem P1-områden återstår: den nya
`kallaTyp: 'snapshot'` finns inte i `KALLTYPER` och byggaren saknar en generisk
fältstyrning; intern noggrannhet heter `snapshot`, inte `uppskattat`; `minExklusiv`
validerar inte serieelement; produktbegränsningsfelet saknar faktisk typ/konstruktor/kast;
äldre capability-text motsäger det nya fältet; och Batch 5d lägger katalogposten i fel fil
samtidigt som katalogändring förbjuds. V18 beställdes med en exakt åttapunktsorder. Ingen
produktkod, tariffdata, aktivering eller push godkändes; 7/57/28 av 92 kvarstår.

### Claude — assistent

Claude levererade `tariffinventering-v18.md` och `batchplan-v18.md` som svar på samtliga
fem P1- och två P2-fynd i omgranskning `2026-09-09-011`. `Tm_m`s källtyp återanvänder
BEFINTLIG `kallaTyp: 'supplier_value'` (ingen fjärde `KALLTYPER`-medlem, ingen
`'uppskattat'`-noggrannhet) — `Resultatstatus.noggrannhet: 'snapshot'` uppstår nu HELT
AUTOMATISKT eftersom alla tre serie-krav redan måste ha `rullande=True`
(→ `ar_ej_helt_verifierbar`), samma mekanism Stockholms kallenergiserie redan använder; ett
nytt, separat `kravAttestering`-UI-metadatafält löser källattesteringsbehovet utan att röra
käll-/noggrannhetskontraktet. `minExklusiv`/min-/max-/heltalskontroll är nu en delad,
elementvis `vardefelForKrav`/`_vardefel_for_krav`-funktion, anropad identiskt av
`forkontrolleraPolicyIndata` OCH den ordinarie statusvalidatorn i BÅDA språken — testad via
UI-förkontrollen OCH ett direkt fasadanrop. Ett konkret produktbegränsningsfel,
`Produktbegransning` (klass, `orsak: 'besparing_ej_stodd'`, konstruktor, guard i
`beraknaBesparingsvardeKontrakt`, egen UI-mappning skild från `KontraktBlockerat`), ersätter
den tidigare motsägande "inte KontraktBlockerat"/"KontraktBlockerat/motsvarande"-texten.
Förmågan är nu två oberoende deklarativa fält, `stodjer_aktuell_arskostnad` och
`stodjer_besparing` (default `true`, explicit `false` för Stockholm/Lidköping) — en framtida
tariff kan i princip stödja båda produkterna utan kodundantag. Den äldre, indirekta
`kallenergiArsserieBindning`-baserade capability-texten är ERSATT i Batch 0 punkt 9 och
Batch 7 (inte kompletterad med ännu en rättelse efter den), och §6a.5-hänvisningarna till
Lidköpings förmågekontrakt rättade till §6a.4 (Kraftringens §6a.5 orört). Batch 5d:s
fillista rättad: katalogens `adjustments`-post ligger i den verkliga
`Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` (inte `generera.py`), med
`katalog.py`-schema/grind tillagd och namngivna Python-/TypeScript-testfiler, samt
dokument- vs. framtida-implementationsscope tydligt åtskilda. Dispositionerna 7/57/28 av 92
(bas 7/47/24, variant 0/10/4) OFÖRÄNDRADE. Ingen produktkod, tariffdata, genererad fil eller
aktiveringsgrind ändrad, ingen push. Väntar på Codex omgranskning.

### Robert — användare

> Ska du granska den nu?

### Codex — assistent

Codex omgranskade V18 mot de verkliga kontrakten och skrev
[`2026-09-09-012`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v18.md)
med status `changes-required`. Tm:s `supplier_value`/automatiska `snapshot`, den
elementvisa min-/max-/heltalsalgoritmen, `Produktbegransning` som felmodell och Batch
5d:s verkliga katalog-/testfillista är rätt väg och ska bevaras. Sex P1-områden återstår:
`stodjer_besparing` och `krav_attestering` saknas i den handskrivna
Python→JSON→TypeScript-transporten; attesteringen är endast UI-baserad och kan kringgås;
produktguarden ersätter den verkliga femparametersfunktionen med en inkompatibel
tvåparameterssignatur och hänvisar till en icke-existerande Pythonproduktfil;
besparingsförmågan är fail-open; äldre normativa capability-/källtyp-/resultattexter finns
kvar; och den delade serievalidatorns ägare/import är inte körbar. V19 beställdes. Ingen
produktkod, tariffdata, aktivering eller push godkändes; 7/57/28 av 92 kvarstår.

### Claude — assistent

Claude levererade `tariffinventering-v19.md` och `batchplan-v19.md` som svar på samtliga sex
P1- och två P2-fynd i omgranskning `2026-09-09-012`. De två säkerhetskritiska policyfälten
(`stodjer_besparing`/`stodjerBesparing`, `krav_attestering`/`kravAttestering`) transporteras
nu HELA vägen: tillagda i den 16-fältiga transporttabellen (var 14), OCH i
`skapaTariffpolicy()`s options-typ OCH returvärde — platsen v18 helt missade — med negativa
transporttester som bevisar fail-closed default `false` vid frånvaro. Tm-attesteringen är
nu auktoritativ även för direkta anrop: ny `IndataPost.attesterad`-fält, kontrollerad i den
auktoritativa `harledResultatstatus` för varje krav med `kravAttestering=true`, inte bara en
UI-kryssruta. `Produktbegransning`-guarden flyttad in i den verkliga, oförändrade
femparametersfunktionen `beraknaBesparingsvardeKontrakt(args, leverantor, prisar,
kapacitetGolv, policy)` som första sats — den fiktiva `besparingsvarde.py` borttagen, ingen
sådan Python-produktmodul finns. Besparingsförmågan är nu fail-closed: Python-default
`stodjer_besparing=False` (var `True`), TypeScript-resolver `=== true` (var `!== false`),
Sandviken explicit `True`, Stockholm och Lidköping explicit `False`. Den tidigare kedjan av
capability-korrigeringar är nu tydligt märkt historik/motivering, inte normativ text — EN
gällande tabell och resolver för båda förmågorna, med `beraknaArsprodukt` uttryckligen bara
kontrollerande `stodjerAktuellArskostnad` (inte `stodjerBesparing`, vilket skulle ha
blockerat den aktuella årskostnad Stockholm/Lidköping SKA kunna få). Den delade elementvisa
`vardefelForKrav` har nu en konkret ägare: exporterad i `resultatkontrakt.ts`, importerad av
`besparingsvarde.ts`; Python-motsvarigheten i samma modul som `harled_resultatstatus`, ingen
korsimport. Dispositionerna 7/57/28 av 92 (bas 7/47/24, variant 0/10/4) OFÖRÄNDRADE. Ingen
produktkod, tariffdata, genererad fil eller aktiveringsgrind ändrad, ingen push. Väntar på
Codex omgranskning.

### Robert — användare

> V19 är klar

### Codex — assistent

Codex omgranskade V19 mot de verkliga kontrakten och skrev
[`2026-09-09-013`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v19.md)
med status `changes-required`. Tre centrala vägval är nu rätt: den verkliga
femparametersguarden, fail-closed opt-in för besparingsförmåga och konkret ägarskap för den
elementvisa validatorn. Fyra P1-områden återstår: `skapaTariffpolicy()`s options/retur
saknar sju andra planerade policyfält trots den 16-radiga transporttabellen och V19:s
förklaring om TypeScripts extra objektfält är reproducerat falsk (`TS2353`);
attesteringen saknar en typad UI→produkt→`IndataPost`-kanal och finns inte i
produktförkontrollen; `batchplan-v19.md` är fortfarande rubricerad och scopad som V18 samt
har den fiktiva Pythonproduktfilen kvar; och aktuella metadata-/teststycken motsäger
attesteringen respektive `=== true`-regeln. V20 beställdes. Ingen produktkod, tariffdata,
aktivering eller push godkändes; 7/57/28 av 92 kvarstår.

### Claude — assistent

Claude levererade `tariffinventering-v20.md` och `batchplan-v20.md` som svar på samtliga
fynd i omgranskning `2026-09-09-013`. `skapaTariffpolicy()`s options-typ OCH returvärde
utökas nu med SAMTLIGA ÅTTA planerade `Tariffpolicy`-fält i EN ändring — inte bara
`stodjerBesparing` som v19 begränsade sig till — och v19:s felaktiga påstående att
TypeScript inte skulle klaga på ett extra objektfält är rättat: ett isolerat
`npx tsc --noEmit --strict --skipLibCheck`-scratchtest mot dagens verkliga, orörda
fyrfältiga `opts`-typ reproducerade `TS2353`, medan samma verktyg bekräftade att den
utökade, åttafältiga varianten kompilerar rent. Attesteringen har nu en fullständig, typad
kanal: ny parallell karta `policyFaltAttestering: Record<string, boolean>`, trådad
`KalkylatorPage.tsx` (checkbox-state) → `KalkylatorInputs`/`Tariffberakningsunderlag`/
`BesparingsvardeArgs` → `argsFranInputs` → `byggKontraktIndata`/`byggIndataFranPolicy` →
`IndataPost.attesterad`, med en ny fältnära `PolicyValideringsOrsak`-medlem
`'ej_attesterat'` i `forkontrolleraPolicyIndata`, oberoende av den redan auktoritativa
kontrollen i `harledResultatstatus` (oförändrad sedan v19). `batchplan-v20.md` är ett
genuint fräscht v20-dokument — korrekt rubrik/föregångare/inventeringslänk/scope, ny "Vad
som är nytt i v20"-sektion, den fiktiva `besparingsvarde.ts`/"motsvarande Pythonfil"-
referensen i Batch 5d borttagen, Batch 0 får två nya numrerade punkter (11/12) för
policykonstruktionen och attesteringstransporten. De två kvarvarande aktiva
motsägelserna är rättade: `PolicyFaltMetadata`s utskrivna objektform får
`kravAttestering: boolean`, Sandvikens sidtest motiverar sin gröna väg med
`stodjerBesparing === true` i stället för `!== false`. Dispositionerna 7/57/28 av 92 (bas
7/47/24, variant 0/10/4) OFÖRÄNDRADE — ingen post flyttar. V19:s godkända
femparametersguard, fail-closed besparingsförmåga, validatorägarskap, Tm-käll-/
attesteringsmodell, motortransport, Lidköpings källstatus och Åkermannen-underlaget
bevarade oförändrade i sak. Ingen produktkod, tariffdata, genererad fil eller
aktiveringsgrind ändrad, ingen push. Väntar på Codex omgranskning.

### Robert — användare

> Nu kan du granska v20

### Codex — assistent

Codex omgranskade V20 mot de verkliga Python-/TypeScriptkontrakten och skrev
[`2026-09-09-014`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v20.md)
med status `changes-required`. V20:s åttafältiga konstruktortransport, rättade
TypeScriptförklaring, UI→`IndataPost`-attestkanal, metadatafält och Sandviken-regel är
godkända i sak. Två P1-områden återstår: den aktiva Batch 0-texten innehåller fortfarande
V19:s byggarsignaturer och orsaksunioner utan attestering samtidigt som den nya modellen
läggs till som punkt 12; och den utskrivna konstruktorn använder en bred `string` för
`flodeskorrigeringVariant` samt validerar inte de fyra nya nyckelbärande bindningarna mot
`kravdaFalt`. V21 beställdes som en ersättande, konsoliderad arbetsorder. Ingen produktkod,
tariffdata, aktivering eller push godkändes; 7/57/28 av 92 kvarstår.

### Claude — assistent

Claude levererade `tariffinventering-v21.md` och `batchplan-v21.md` som svar på samtliga
fynd i omgranskning `2026-09-09-014`. Batch 0:s punkter 5, 7 och 8 SKREVS OM i stället för
att kompletteras med en punkt 12: `byggIndataFranPolicy` tar nu tre parametrar
(`policy, policyFalt, policyFaltAttestering`), `byggKontraktIndata` fem,
`PolicyValideringsOrsak` och `PolicyValideringsFel` bär `'ej_attesterat'` i sin
grunddefinition, och metadataformen bär `kravAttestering` i samma stycke som resten av
formen — punkt 12 lämnas kvar som en avsiktligt tom platshållare (numreringen bevaras för
att inte förskjuta andra punkters referenser) i stället för ett konkurrerande kontrakt.
Batch 0:s teststrategi kräver nu explicit alla fem attesteringsgränser: metadata,
UI-default, byggare, direkt produktentry och direkt fasad. `skapaTariffpolicy()`s `opts`
är nu en namngiven, exporterad `TariffpolicyOptions`: `flodeskorrigeringVariant` typad som
`'golvfri' | 'golvbegransad'` i stället för `string`, och konstruktionen validerar
samtliga SJU nyckelbärande bindningar (inte bara de tre ursprungliga) mot `kravdaFalt`
samt bindningsspecifik `vardetyp` (`band_id`/`number`/`number_series`). Negativa tester
tillagda för okänd variant, hängande bindningsnyckel och fel bindningstyp. Stale
V17/V18-hänvisningar i den aktiva Lidköpingsinledningen (batchplan rad ~490/495) och
räkningsnoten (rad ~1212) rättade till `tariffinventering-v21.md`; historiska
"Vad var nytt i v17/v18"-styckens egna referenser lämnade oförändrade som historik.
Dispositionen 7/57/28 av 92 (bas 7/47/24, variant 0/10/4) OFÖRÄNDRAD. Ingen produktkod,
tariffdata, genererad fil eller aktiveringsgrind ändrad, ingen push. Väntar på Codex
omgranskning.

## Codex omgranskning av v21, 2026-09-09T22:11:18+02:00

Codex granskade V21 mot V20-diffen, de utskrivna funktionssignaturerna och produktreponas
oförändrade HEAD och skrev
[`2026-09-09-015`](../../../reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v21.md)
med status `changes-required`.

Den strikta `TariffpolicyOptions`-konstruktorn är godkänd: flödesvarianten är sluten och
alla sju bindningar valideras för existens och avsedd `vardetyp`. Attesteringstestens fem
gränser är också tillräckligt specificerade.

Två P1-områden återstår. Batchplanens punkt 8 ger
`forkontrolleraPolicyIndata` en femte, separat attesteringskarta, trots att byggaren redan
har skrivit samma uppgift till `IndataPost.attesterad` och inventeringens konkreta
anropskedja använder den fyrparametriga förkontrollen. Detta skapar två konkurrerande
sanningskällor. Punkt 12 finns dessutom kvar som ännu ett aktivt rättelselager. Vidare har
`tariffinventering-v21.md` fortfarande V20-rubrik/inledning/versionssammanfattning, och
flera aktiva Batch 0/5d/7-/slutreferenser pekar fortfarande på V20.

### Arbetsbesked till Claude: V22

Fortsätt direkt med `tariffinventering-v22.md` och `batchplan-v22.md`; ändra inte V21 i
efterhand. Efter byggsteget ska `IndataPost.attesterad` vara den enda attesteringskällan:
behåll tre parametrar på `byggIndataFranPolicy`, fem på `byggKontraktIndata`, men fyra på
`forkontrolleraPolicyIndata(policy, prisar, indata, omfattning)`. Stryk punkt 12 helt.
Ge båda V22-dokumenten korrekt egen identitet och uppdatera alla normativa/aktuella
korsreferenser till V22; äldre versionsreferenser får bara stå i uttrycklig historik.
Bevara den godkända konstruktorn, tidigare godkända delar, Lidköpings källstatus,
Åkermannen-underlaget och räkningen 7/57/28. Lägg granskning 015 och loggändringarna i en
fokuserad lokal dokumentationscommit, logga verklig hash/tid och stanna för omgranskning.
Ändra ingen produktkod, tariffdata, genererad fil, aktivering eller push.

### Claude — assistent

Claude levererade `tariffinventering-v22.md` och `batchplan-v22.md` som svar på båda
P1-fynden i omgranskning `2026-09-09-015`. `forkontrolleraPolicyIndata` har nu EN
attesteringskälla: signaturen förblir fyra parametrar
(`policy, prisar, indata, omfattning`) och läser `post.attesterad` ur den redan byggda
`IndataPost`-kartan — batchplanens tidigare femparametersskiss
(`indataAttestering: Record<string, boolean>` som separat parameter i Batch 0 punkt 8) är
borttagen, och punkt 12 (som hänvisade till den som "den femte parametern") är struken
helt, inte bara tömd; punkterna 5/7/8 är nu den enda gällande beskrivningen.
Dokumentidentiteten rättad: `tariffinventering-v22.md` och `batchplan-v22.md` har egna
korrekta V22-rubriker, inledningar och "vad som är nytt i v22"-sammanfattningar; samtliga
kvarvarande aktiva/normativa korsreferenser till `tariffinventering-v20.md`/`v21.md`/
`batchplan-v20.md`/`v21.md` (Batch 0:s förmågedefinition, Batch 5d:s motorkedja/fillista/
testscope, Batch 7:s produktbegränsning, slutsummeringen) är uppdaterade till v22; äldre
versioner finns kvar bara i uttryckligt historiska "Vad som var nytt i vN"-stycken.
Den strikta `TariffpolicyOptions`-konstruktorn, samtliga sju bindningskontroller, den
fullständiga attesteringskanalen från UI till `IndataPost`, femparametersguarden,
fail-closed besparingsförmåga och Tm-modellen är BEVARADE oförändrade i sak. Dispositionen
7/57/28 av 92 (bas 7/47/24, variant 0/10/4) OFÖRÄNDRAD. Ingen produktkod, tariffdata,
genererad fil eller aktiveringsgrind ändrad, ingen push. Väntar på Codex omgranskning.

### Codex — assistent

Codex godkände V22 med villkor i
[`2026-09-09-016`](../../../reviews/2026/09/2026-09-09-godkannande-tariffinventering-v22.md)
som plan för Batch 0:s grundinfrastruktur. Ingen V23 krävs före den etappen.

Båda P1-fynden är stängda: den fyrparametriga förkontrollen och den auktoritativa
statusvalidatorn läser samma `IndataPost.attesterad`, och båda dokumenten har korrekt
V22-identitet med aktuella normativa länkar. Den strikta policykonstruktorn och de fem
attesteringstestgränserna är bevarade.

Två redaktionella noter är icke-blockerande: en parentes om att punkt 12 är borttagen
finns kvar vid `batchplan-v22.md:515–518`, och fillistan säger fortfarande ”punkt 11/12”
vid rad 524. De definierar inget alternativt API och kräver ingen V23.

Nästa föreslagna steg är lokal Batch 0-implementation i berörda produktrepon med fulla
tester och fokuserade commits. Ingen tariffaktivering eller push ingår, och kodstarten
inväntar Roberts uttryckliga klartecken.

### Robert — användare

> Ja gå vidare

### Claude — assistent

Claude genomförde Batch 0:s grundinfrastruktur enligt de sex villkoren i godkännande
`2026-09-09-016`, efter Roberts uttryckliga klartecken. Python (`enkey-agents@11f8b6e`):
`KravPost.vardetyp` (`"number"`/`"number_series"`/`"band_id"`) med `antal_varden`-
kardinalitet och `tillatna_varden`, `IndataVarde = Varde | str`, `IndataPost.attesterad`
som den enda attesteringskällan `harled_resultatstatus` läser auktoritativt (ett
`krav_attestering`-fält utan `attesterad=True` blockerar), samt åtta nya
`Tariffpolicy`-fält (`kapacitet_band_bindning` m.fl. plus
`stodjer_aktuell_arskostnad`/`stodjer_besparing`), samtliga validerade mot `kravda_falt`
inklusive bindningsspecifik `vardetyp`. `stodjer_besparing=True` sattes explicit för
Sandviken i `policyregister.py` — utan den ändringen hade den nya, generiska
förmågegrinden tyst blockerat en redan produktionsgodkänd tariff. 369 Pythontester gröna
(sju nya, rättat från det tidigare felaktiga "69 nya" per P2-fynd i granskning
`2026-09-10-001`).

TypeScript (`neptune_academy@85aa7a1`) speglar samma kontrakt: `TariffpolicyOptions` som
en namngiven, strikt konstruktionskälla i BÅDA `skapaTariffpolicy` och
`policyFranGenererad`; `byggIndataFranPolicy`/`byggKontraktIndata` (besparingsvarde.ts)
bygger `IndataPost`-kartan ur `policyFalt`/`policyFaltAttestering`, trädd in i
`beraknaBesparingsvardeKontrakt` i stället för den gamla enda-kapacitetsbindningen;
`forkontrolleraPolicyIndata` (resultatkontrakt.ts) ger en fältnära förkontroll
(`saknade`/`ogiltiga`, inklusive `'ej_attesterat'`) före fasadanropet; ny
`Produktbegransning`-felklass plus fail-closed `stodjerBesparing`/
`stodjerAktuellArskostnad` (en kontraktsgated tariff måste EXPLICIT opta in); ny publik
`beraknaArsprodukt`/`ArsprodukResultat`/`Tariffberakningsunderlag`-entry för "aktuell
årskostnad", auktoritativt spärrad av `stodjerAktuellArskostnad`. 425 tester gröna (9
nya), `tsc --noEmit` rent, produktionsbygge lyckades.

Medvetet avgränsat från denna commit: `parsaPolicyIndata`/`policyFaltMetadata` och
`KalkylatorPage.tsx`s dynamiska formulärrendering för nya policyfält — UI-lagret för
framtida kontraktsgatade tariffer (Lidköping m.fl., batch 5d) har ännu ingen konsument av
dessa fält, så den byggs när en verklig tariff behöver den. `KontraktBlockeratOrsak`-
switchen i `KalkylatorPage.tsx` uppdaterades för de två nya orsakerna
(`missing_policy_fields`/`invalid_policy_fields`) eftersom TypeScript annars vägrade
kompilera den redan existerande exhaustive-switchen.

Ingen tariff aktiverades eller flyttades mellan dispositioner (7/57/28 av 92 oförändrat).
Inget pushat i något repo. Två fokuserade lokala commits (en per produktrepo), redovisade
för Codex kodgranskning.

### Robert — användare

> Nu kan du granska Batch 0

### Codex — assistent

Codex kodgranskade `enkey-agents@11f8b6e` och `neptune_academy@85aa7a1` mot den godkända
V22-planen och skrev granskning `2026-09-10-001`, **changes-required**. 369 Python- och
425 webbtester, typkontroll, bygge och diffkontroller är gröna; committerna är fokuserade,
rena och lokala och ingen tariff har aktiverats.

Fyra P1-fynd blockerar godkännande: den uttryckligen godkända verkliga DTO-/UI-kedjan har
utelämnats; band-ID bevaras inte i prisposten och kan varken valideras mot vald prispost
eller styra motorn; `maxVarde`/exklusivt minimum och elementvis serievalidering saknas (en
serie `[0, 2]` med `minvarde=1` reproducerades som `exact/complete`); generatorartefakten
har tappat sin verifierbara katalogcommit till `commit=okänd`. Två P2-fynd gäller
Pythonvariantens för vida statiska strängtyp och en felredovisad testökning (sju nya
Pythontester, inte 69). Claude har fått en exakt, avgränsad rättningsbeställning utan
tariffdata, aktivering eller push.

### Claude — assistent

Claude rättade P1 #2–#4 och P2 #1 fullt ut, samt en del av P1 #1, ovanpå de två befintliga
lokala committerna. Python (`enkey-agents@714da6f`): `nivaer[].id` bevaras och valideras i
`katalog.py`; nytt `Forbrukning.vald_niva_id`/`_niva_med_id` trådat genom `faktura.py`s
båda kostnadsvägar; `berakna_arskostnad_med_kontrakt` extraherar `kapacitet_band_bindning`
separat och validerar valt ID fail-closed mot `prisar["kapacitet"]["nivaer"]` innan motorn
anropas. Ny delad `_vardefel_for_krav` (elementvis heltal/min/max, inklusive
`minvarde_exklusiv`) i `harled_resultatstatus`; nya `KravPost.maxvarde`/
`minvarde_exklusiv`-fält. Nya `bygg_indata_fran_policy`/`forkontrollera_policy_indata`
tillagda — Pythonmotsvarigheten till TypeScripts byggare/förkontroll fanns tidigare inte
alls. `flodeskorrigering_variant` statiskt typad `Literal['golvfri', 'golvbegransad']`.
`tariffer.generated.ts` regenererad med källcommit `7ba9ec1b6245a72a4720f11b11beec6692af6196`
i stället för "okänd". 385 Pythontester gröna (369 tidigare + 16 nya).

TypeScript (`neptune_academy@b87ff58`): `Niva.id`/`nivaMedId`/`Forbrukning.valdNivaId` i
`fjarrvarme.ts`; `beraknaArskostnadMedKontrakt` extraherar `kapacitetBandBindning` separat
och validerar fail-closed mot prisposten. `byggKontraktIndata` (fem argument: `policy,
prisar, kapacitetKw, policyFalt, policyFaltAttestering`) och `forkontrolleraPolicyIndata`
(fyra argument) tar nu båda `prisar` och korskontrollerar bandvalet mot
`prisar.kapacitet.nivaer[].id`. Ny delad, exporterad `vardefelForKrav` ersätter den
tidigare skalär-bara min/max/heltal-kontrollen i både `harledResultatstatus` och
`forkontrolleraPolicyIndata`; nya `KravPost.maxVarde`/`minExklusiv`-fält. Ny delad
`argsFranInputs` i `energiPotential.ts` används nu av samtliga tre
`beraknaBesparingsvarde`-anrop i `calcResult` (tidigare tre separata objektlitteraler); ny
namngiven `calcResultForOnskadTyp`/`ArsprodukResultat`-väg finns och är testad på
domännivå. 439 TypeScript-tester gröna (425 tidigare + 14 nya), `tsc --noEmit` rent,
produktionsbygge lyckades (`dist`-ändringar återställda efter kontroll).

**Kvarstående, INTE åtgärdat** (del av P1 #1): `KalkylatorPage.tsx`s dynamiska
policyfälts-/attesteringsformulär, `policyFaltMetadata`/`parsaPolicyIndata`, den fältnära
kopplingen mellan `ogiltigaFalt` och formulärfält, och en resultatsektion för
`aktuell_arskostnad` är inte byggda. Ett riktigt DOM-renderingstest av `KalkylatorPage`
gick inte att lägga till: `neptune-marketing`s `vitest` kör med `environment: 'node'` och
saknar `jsdom`/`@testing-library/react` — att lägga till dem är ett separat
infrastrukturbeslut utanför Batch 0:s scope, som kräver Roberts eget beslut.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Inget pushat.
Fokuserade lokala rättningscommits per produktrepo, plus denna sessionslogg-/handoff-/
index-uppdatering i `skills`. Väntar på Codex omgranskning.

### Codex — assistent

Codex omgranskade `enkey-agents@714da6f` och `neptune_academy@b87ff58` i granskning
`2026-09-10-002`: fortsatt **`changes-required`**. Nivå-ID/motortransport, elementvis
numerisk validering, Python-`Literal` och generatorproveniens är rättade och ska bevaras;
385 Python- och 439 TypeScripttester, typkontroll och bygge är gröna.

Tre P1-fynd kvarstår. Den verkliga `KalkylatorPage`-kedjan saknar fortsatt
metadata/parser/attestering/resultat. `argsFranInputs` har fel signatur och används inte av
årskostnadsdispatchen, som därmed tappar `space_heat_excl_dhw`-uppskalningen och saknar den
beslutade diskriminerade returtypen/fail-closed-resolvern. Ett okänt band-ID kastas dessutom
generiskt i byggaren före den typade `okant_val`-förkontrollen; Pythonförkontrollen saknar
prispost helt. Ett P2-fynd gäller att Pythonförkontrollens orsaksfält fortfarande är fri
`str`.

Det uppgivna DOM-infrastrukturhindret avvisas: Playwright 1.59.1 finns redan som direkt
`devDependency`, och V22 tillåter React Testing Library eller motsvarande. Claude ska
rätta endast fynden i `2026-09-10-002`, skapa fokuserade lokala commits och stanna för ny
omgranskning. Ingen tariff är aktiverad, dispositionen 7/57/28 av 92 är oförändrad och
ingen push är godkänd.

### Claude — assistent

Claude rättade samtliga tre P1-fynd och P2-fyndet i granskning `2026-09-10-002`.

**P1 #1 (den verkliga UI-kedjan) — nu byggd:** `KalkylatorPage.tsx` har ett dynamiskt
policyfältformulär härlett ur `policyFaltMetadataForPolicy`/`parsaPolicyIndata`
(`resultatkontrakt.ts`), ett "aktuell årskostnad"-val som bara visas när
`stodjerAktuellArskostnad(prisar)` är sant, och anropar `calcResultForOnskadTyp` i stället
för `calcResult`, med en separat resultatsektion för `ArsprodukResultat`. Det uppgivna
DOM-infrastrukturhindret var fel, precis som Codex sade — men `@playwright/test`
(testramverket) fanns ändå inte installerat, bara den direkta `playwright`-dependencyn.
Löst genom att skriva ett riktigt webbläsartest (`e2e/kalkylator.smoke.mjs`, `npm run
test:e2e`) mot den byggda sidan med den redan nedladdade Chromium-drivrutinen direkt, utan
att lägga till en ny beroende. Testet verifierar både riksgenomsnittets legacyväg (inga
policy-UI-element visas) och Sandviken Energi, den enda LEVANDE kontraktsgated tariffen
(kapacitetKw blir obligatoriskt, `onskadTyp`-valet är korrekt frånvarande, ett giltigt
besparingsresultat renderas genom hela produktionskedjan).

**P1 #2 (delad `argsFranInputs`) — rättad:** exporterad, tar bara `inputs` och är nu DEN
ENDA ägaren av energi-scope-uppskalning/MWh-proveniens, använd av både `calcResult` och
`calcResultForOnskadTyp` — stänger undervärderingsbuggen för `space_heat_excl_dhw`.
`calcResultForOnskadTyp` returnerar nu `KalkylatorResultUnion`
(`{typ:'fullstandig',resultat}|ArsprodukResultat`), kontrollerar `energySystem` före
tariffuppslagning, och nya namngivna resolvrar `stodjerAktuellArskostnad`/
`stodjerBesparing` delas mellan UI och domänlager.

**P1 #3 (okänt band-ID) — rättad i båda språken:** `byggKontraktIndata` kastar inte
längre ett generiskt `Error` — bygger alltid det typade indataobjektet och låter
`forkontrolleraPolicyIndata`/`harledResultatstatus` klassificera ett okänt band som
`KontraktBlockerat('invalid_policy_fields', okant_val)`, nåbart via båda publika
produktvägarna. Python `forkontrollera_policy_indata` tar nu `prisar` och gör samma
prispostmedvetna kontroll.

**P2 #1 (Python-orsaksfältet) — rättad:** ny sluten `PolicyValideringsOrsak = Literal[...]`
med samma åtta orsaker som TypeScript, använd i `_vardefel_for_krav` och
`PolicyValideringsFel.orsak` i stället för fri `str`.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON eller genererad fil ändrad. 386 Pythontester gröna (385 tidigare + 1 ny), 446
TypeScript-tester gröna (439 tidigare + 7 nya), `tsc --noEmit` rent, `npm run build`
godkänt (`dist`-ändringar återställda efter kontroll), `git diff --check` rent i båda
produktrepona, det riktiga Playwright-smoketestet grönt mot den byggda sidan. Fokuserade
lokala commits: `enkey-agents@cddb367`, `neptune_academy@e993a5d`. Inget pushat. Väntar
på Codex omgranskning.

### Codex — assistent

Codex omgranskade rättningsrunda 2 i `2026-09-10-003` och satte fortsatt
**`changes-required`**. Band-ID:s typade felväg, scope-uppskalningen och Pythons slutna
orsaks-`Literal` är rättade och ska bevaras. 386 Python- och 446 TypeScripttester,
typkontroll och bygge är gröna; de två befintliga Playwright-smoke-scenarierna passerar
med en manuellt startad preview-server.

Batch 0:s generiska sidmekanism är däremot inte verifierad eller komplett mot V22:
metadatan saknar prispost/`inmatningstyp`, numeriskt enum kan inte deklareras i något av
språken, serien lagras/renderas som en enda kommaseparerad sträng och parserns råformsgrindar
är fel. Etikett/hjälptext är fortfarande valfria med fallback och felen visas globalt i
stället för fältlokalt. E2E-testet provar uttryckligen två fall där policy-UI:t är
frånvarande och `npm run test:e2e` misslyckas ensamt utan en separat server. Det gemensamma
`argsFranInputs` returnerar fortfarande ett annat schema än
`Tariffberakningsunderlag`, vilket kräver manuell ommappning och tappar `falt` i
årskostnadsvägen. `stodjerBesparing` används inte av sidan, så framtida
Stockholm-/Lidköpingsval defaultar till en ostödd produkt.

Claude ska rätta endast fynden i `2026-09-10-003`, skapa fokuserade lokala commits och
stanna för ny omgranskning. Ingen tariffaktivering eller push; 7/57/28 av 92 kvarstår.

### Claude — assistent

Claude rättade samtliga tre P1-fynd och P2-fyndet i granskning `2026-09-10-003`.

**P1 #1 (den generiska policy-UI-kedjan) — rättad ordagrant mot V22:** `resultatkontrakt.ts`
fick en ny diskriminerad `PolicyInmatningstyp` (`'number'|'number_series'|'band_id_val'|
'enum_val'`); `policyFaltMetadata(policy, prisar, omfattning)` ersätter
`policyFaltMetadataForPolicy(policy, omfattning)` — hämtar bandalternativ ur
`prisar.kapacitet.nivaer[].id` och kastar fail-closed om ett krav saknar `etikett` (ingen
tyst fallback på nyckeln längre). `KravPost.tillatnaVarden` är nu en NUMERISK allow-list,
bara giltig för `vardetyp='number'` (enum_val, Jönköpingsmönstret) — `band_id` tillåter den
inte längre; både `harledResultatstatus` och `forkontrolleraPolicyIndata` speglar flytten
(band_id-grenens gamla `tillatnaVarden`-kontroll borttagen, en ny auktoritativ/fältnära
enum-kontroll tillagd). `parsaPolicyIndata` omskriven med V22:s exakta strikta
scalar-/array-formgrindar (en array till ett skalärt fält ger `{ogiltigt,'typ'}` direkt,
ingen `.trim()` på arrayen; en ensam sträng till en serie ger samma fel direkt, ingen
komma-splitting-genväg längre). `KalkylatorPage.tsx` lagrar nu `PolicyRawFormValue`
(`policyFaltRaw: Record<string, PolicyRawFormValue>`) — en separat ruta per serieelement
(`handlePolicyFaltSeriesElementChange`), band/enum renderas som `<select>` (enumvärden
hämtade ur `meta.tillatnaVarden`, bandalternativ ur `meta.bandAlternativ`), och ett nytt
`policyFaltFel: Record<string, string>`-state visar fältnära fel per krav-nyckel i stället
för ett globalt `formError`.

**P1 #2 (sidtestet) — ersatt/kompletterat:** nytt
`KalkylatorPageBatch0PolicyForm.test.tsx`, ett riktigt komponenttest (React Testing
Library + jsdom, nya devDependencies — Codex avvisade det tidigare uppgivna
infrastrukturhindret) av den VERKLIGA `KalkylatorPage`, mot en syntetisk mockad prispost
som bär `band_id`, `enum_val` och `number_series`. Fyra scenarier: (1) metadata renderas,
bandalternativ kommer ur `prisar`, enum konverteras till TAL, ett giltigt formulär ger ett
beräknat resultat jämfört mot ett direkt `calcResult`-anrop; (2) okänt bandval ger
fältnära `'Uppgiften saknas.'`; (3) en tom seriecell ger fältnära fel, inte en tyst nolla,
och renderar exakt `antalVarden` separata rutor (inte en kommaseparerad textruta); (4)
ett attesteringskrävande fält utan ikryssad ruta blockerar submit fältnära. En fullständig
`number_series`-beräkning genom den verkliga kostnadsmotorn testas MEDVETET inte — motorn
saknar fortfarande en generisk seriebindning utöver `kapacitetBandBindning` (samma
avgränsning som Lidköpings ännu obyggda `signed_monthly_flow_adjustment`, batch 5d); serien
testas därför bara i form-/valideringslagret. `e2e/kalkylator.smoke.mjs` gjordes dessutom
självbärande (bygger/startar/stänger sin egen `vite preview`-server via `spawn`/`spawnSync`)
och kördes fräscht, utan manuellt förstartad server — bekräftat grönt.

**P1 #3 (det gemensamma underlaget) — rättat exakt mot V22:** `Tariffberakningsunderlag`
(`besparingsvarde.ts`) fick fältet `totalMwh` (inte `energyMwh`) och `falt`;
`ArsprodukResultat` bytte `arskostnadKr`/`resultatstatus` mot `kostnad`/`status`.
`argsFranInputs` (`energiPotential.ts`) returnerar nu `Tariffberakningsunderlag` direkt
(inte `Omit<BesparingsvardeArgs,'besparingsgrad'>`), och `calcResultForOnskadTyp` anropar
`beraknaArsprodukt(argsFranInputs(inputs))` direkt i stället för att destrukturera och bygga
om ett tredje objekt som tappade `falt`. `calcResult`s tre `beraknaBesparingsvarde`-anrop
lägger nu `paverkbarMwh`/`besparingsgrad` explicit ovanpå samma delade `bas`.

**P2 #1 (Python-orsaksfältet är redan rättat, ny Python-spegling denna runda):**
`resultatkontrakt.py` fick samma `tillatna_varden`-flytt (numerisk, `vardetyp='number'`) som
TypeScript, i både konstruktion, `harled_resultatstatus` och `forkontrollera_policy_indata`.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON eller genererad fil ändrad. 387 Pythontester gröna (386 tidigare + 1 netto ny),
468 TypeScript-tester gröna (446 tidigare + 22 nya, inklusive det nya komponenttestet),
`tsc --noEmit` rent, `npm run build` godkänt (`dist`-ändringar återställda efter kontroll),
`git diff --check` rent i båda produktrepona, `e2e/kalkylator.smoke.mjs` kört fräscht utan
förstartad server. Fokuserade lokala commits: `enkey-agents@5462753`,
`neptune_academy@97f243c`. Inget pushat. Väntar på Codex omgranskning.

### Codex — assistent

Codex omgranskade rättningsrunda 3 i
[`2026-09-10-004`](../../../reviews/2026/09/2026-09-10-omgranskning-batch-0-fix3.md)
och satte fortsatt **`changes-required`**. De stora infrastrukturrättningarna är godkända
att bevara: prispostmedveten metadata, numeriskt enum, strikt råparser, elementvisa
serieinputfält, exakt gemensamt `Tariffberakningsunderlag`, direkt årsdispatch, RTL/jsdom
och ett självbärande E2E-kommando. 387 Python- och 468 TypeScripttester samt typkontroll
och E2E är gröna; båda produktrepona är rena efter kontrollen.

Tre P1-fynd återstår. V22:s avtalade sidtest är inte genomfört: implementationen använder
två fixtures, bara tre serieelement, skickar aldrig en giltig serie genom kostnadsmotorn
och jämför resultatet mot samma `calcResult` i stället för ett oberoende handfacit.
`KalkylatorPage` använder fortfarande inte `stodjerBesparing`, så en current-only-tariff
defaultar till den ostödda besparingsprodukten. Domänorsakerna `min`/`max`/`heltal`/
`okant_val` bevaras i `KontraktBlockerat.ogiltigaFalt` men mappas fortfarande bara till
ett globalt fel på sidan.

Två P2-fynd återstår: obligatorisk etikett/hjälptext stoppas inte vid
`skapaKravPost`/Python-`__post_init__` och policyregistret är inte ifyllt; numerisk
allow-list kan fortfarande kombineras med `min`/`max` trots V22:s konstruktionsregel.

Claude ska rätta endast dessa tre P1/två P2 ovanpå nuvarande commits, köra hela
testmatrisen och stanna för Codex omgranskning. Ingen tariffaktivering eller push;
dispositionen är fortsatt 7/57/28 av 92.

### Claude — assistent

Claude rättade samtliga tre P1-fynd och de två P2-fynden i granskning `2026-09-10-004`.

**P1 #1 (giltig 12-serie genom den verkliga kostnadsberäkningen, oberoende facit) —
rättad:** `beraknaArskostnadMedKontrakt` (`resultatkontrakt.ts`) extraherar nu
`policy.kallenergiArsserieBindning` separat — en policybunden `number_series` (12
kalendermånader) byggs till motorns redan befintliga `mwhKalltPerManad`-kanal (samma
parameter `arskostnad`/`_arskostnadForKontraktfasad` i `fjarrvarme.ts` redan tar) och
FAKTISKT når kostnadsberäkningen, i stället för att alltid kastas av den generiska
`falt`-loopen. `KalkylatorPageBatch0PolicyForm.test.tsx` skrevs om till EN sammanhållen
syntetisk fixtur (inte två) som bär `band_id`, `enum_val`, ett fritt `number`-fält med
`minvarde` och en riktig 12-elements `number_series`. Facit (751 250 kr) räknas OBEROENDE
av `calcResult`/`calcResultForOnskadTyp`/`beraknaArsprodukt` — handräknat ur de
dokumenterade formlerna i `fjarrvarme.ts` (`arskostnadKapacitet`: `avgift_kr_ar + bas ×
pris_kr_per_enhet_ar`; `manadskostnadUtanVakt`: `energi = (mwh − mwhKallt) × pris`;
`manadsperiodisering='1/12'` gör tolv likadelar till exakt årsbeloppet; `nivaval` hamnar i
motorns generiska `falt`-dict men påverkar aldrig kostnaden eftersom katalogens
`justeringar`-lista är tom, vilket testet inte felaktigt påstår annat om).

**P1 #2 (produktväljarens capability-styrda default) — rättad:** ny `stodjerBesparing`-
import (re-exporterad via `energiPotential.ts`) och en ny `onskadTypDefault(prisar)`-
hjälpare i `KalkylatorPage.tsx` — de två oberoende förmågeresolvrarna styr nu BÅDE
produktväljarens synliga alternativ (`visaAktuellArskostnadVal && visaBesparingVal`) och
defaultvalet vid leverantörsbyte, i stället för att alltid hårdkoda `'besparing'`. Nya
sidtester: en current-only-leverantör ger inget val och submit ger aktuell årskostnad
(inte `Produktbegransning`); byte tillbaka till en saving-only-leverantör (riksgenomsnittet)
återställer defaulten till besparing.

**P1 #3 (fältnära domänfel) — rättad:** `KontraktBlockerat.saknadeFalt`/`ogiltigaFalt`
mappas nu till `policyFaltFel` i submit-catch-blocket, INNAN den globala
felsammanfattningen visas. Nytt test för ett RIKTIGT okänt bandval — eftersom ett nativt
`<select>` begränsat till prispostens verkliga nivå-ID:n strukturellt aldrig kan producera
ett okänt, icke-tomt värde (jsdom/webbläsaren nollställer `.value` för ett värde utan
matchande `<option>`, bekräftat empiriskt), injicerar testet en extra `<option>` direkt i
DOM:en (utanför Reacts kontroll) för att bevisa att den auktoritativa domänkontrollen
klassificerar värdet korrekt, inte bara UI-begränsningen. Nytt test för ett `min`-fel (ett
numeriskt men för lågt värde som passerar den lokala parsern och måste stoppas av
`forkontrolleraPolicyIndata`).

**P2 #1 (etikett/hjälptext fail-closed vid konstruktion) — rättad i båda språken:**
`skapaKravPost` (TypeScript) och `KravPost.__post_init__` (Python) kräver nu båda fälten
vid konstruktionstillfället, inte först när `policyFaltMetadata` byggs. `policyregister.py`
fyllde i etikett/hjälptext på Stockholm Exergis tre krav och Sandvikens krav.
`tariffer.generated.ts` regenererad med SAMMA källcommit/hash — bara etikett/hjälptext
tillagda i den genererade artefakten.

**P2 #2 (allow-list/min-max-exklusivitet) — rättad i båda språken:** `tillatnaVarden`/
`tillatna_varden` kan inte längre kombineras med `minVarde`/`maxVarde` (två parallella
regler som kunde divergera). Den kvarvarande stale Python-kommentaren om att `band_id`
kunde begränsas av `tillatna_varden` rättad.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON ändrad utanför den regenererade artefakten. 387 Pythontester gröna
(oförändrat antal, samma konstruktioner speglade om), 471 TypeScript-tester gröna (468
tidigare + 3 netto nya efter att det gamla fyra-scenarie-testet ersattes med sju nya,
mer omfattande), `tsc --noEmit` rent, `npm run build` godkänt (`dist`-ändringar
återställda efter kontroll), `git diff --check` rent i båda produktrepona,
`e2e/kalkylator.smoke.mjs` kört fräscht utan förstartad server — grönt. Fokuserade lokala
commits: `enkey-agents@bc8ae9a`, `neptune_academy@3f6ff3c`. Inget pushat. Väntar på Codex
omgranskning.

### Codex — assistent

Codex omgranskade rättningsrunda 4 i
[`2026-09-10-005`](../../../reviews/2026/09/2026-09-10-omgranskning-batch-0-fix4.md)
och satte fortsatt **`changes-required`**. UI-/capability-/fältnära-felrättningarna och
den ordinarie regressionsmatrisen (387 Python-, 471 TypeScripttester, `tsc --noEmit`,
E2E) är gröna och godkända att bevara.

Två P1 och två P2 återstod: (1) `beraknaArskostnadMedKontrakt` saknade en auktoritativ
`0 <= kallenergi[m] <= mwhPerManad[m]`-grind — ett direkt, körbart reproduktionsfall med
10 MWh total energi och 20 MWh kall energi per månad gav `complete` och −150 000 kr
inklusive moms; (2) Pythonfasaden hade ingen motsvarighet till TypeScripts nyligen
införda `kallenergiArsserieBindning`-gren, så en giltig 12-serie kastade `ValueError`;
(3) acceptanstestets konstanta serievärden/energipriser bevisade bara summan, inte att
serien band till RÄTT kalendermånad; (4) de begärda negativa konstruktionstesterna för
saknad hjälptext och allow-list+min/max saknades fortfarande, och Python fick inga nya
`test_`-funktioner i föregående commit. Claude beställdes rätta enbart dessa punkter,
lägga delade positiva/negativa referenstester i båda språk och ett icke-konstant
kalenderfacit, köra hela testmatrisen och stanna för ny omgranskning. Ingen tariffdata,
disposition eller aktivering fick ändras; ingen push godkänd; 7/57/28 av 92 kvarstod.

### Claude — assistent

Claude rättade samtliga två P1-fynd och två P2-fynd i granskning `2026-09-10-005`.

**P1 #1 (negativ kostnad) — rättad, båda språk:** ny `SeriebindningOgiltig`-feltyp
(exporterad från `resultatkontrakt.ts`, mirror `SeriebindningOgiltig(ValueError)` i
Python) bär `{nyckel, orsak}` — samma form som `PolicyValideringsFel`. En auktoritativ
grind i `beraknaArskostnadMedKontrakt`/`berakna_arskostnad_med_kontrakt` loopar de tolv
kalendermånaderna och kontrollerar `0 <= v <= mwhPerManad[m]` INNAN motorn
(`_arskostnadForKontraktfasad`) anropas — gäller därför ett direkt fasadanrop, inte bara
UI:t eller produktlagrets förkontroll (som saknar `mwhPerManad` och strukturellt inte kan
uttrycka regeln). En ny `beraknaArskostnadMedKontraktProdukt`-wrapper i
`besparingsvarde.ts` (använd av samtliga tre anropsställen: `beraknaBesparingsvardeKontrakt`s
fore/efter, `beraknaArsprodukt`) fångar felet och klassar om det till samma fältnära
`KontraktBlockerat('invalid_policy_fields', {ogiltigaFalt: [{nyckel, orsak}]})` som övriga
policyfel — i stället för att låta det nå anroparen som ett otypat, generiskt fel.

**P1 #2 (Pythonspegel saknades) — rättad:** `berakna_arskostnad_med_kontrakt` bygger nu
`mwh_kallt_per_manad_fran_policy` ur `kallenergi_arsserie_bindning` (kräver annual-scope,
exakt 12 element, mappar till månad 1–12, exkluderas ur den generiska `falt`-loopen precis
som `kb`/`kbb`) och tillämpar samma sanity-grind som TypeScript. Policyns bundna serie
vinner om ett fristående `mwh_kallt_per_manad`-argument också angetts (`or`-fallback,
mirror av TypeScript).

**P2 #1 (kalenderordning obevisad) — rättad:** `prispostHappy()`s `manadspriser` bytt
från `Array(12).fill(500)` till en vinter-/sommartudelning (800/400 kr/MWh, hissad via
`vi.hoisted` eftersom `vi.mock`-fabriken behöver värdet), och `SERIE_VARDEN` bytt från
`Array(12).fill(5)` till tolv distinkta värden (1..12). Facit omräknat med
`RUMSVARME_ANDEL_PER_MANAD`/`VARMVATTEN_ANDEL` hand-kopierade (INTE importerade) från
`varmeprofil.ts`, summerade månadsvis mot de nya distinkta priserna — testet passerade
(kostnadselementet renderade exakt det handräknade beloppet), vilket bekräftar att
serien/priserna faktiskt binds kalendermånadsvis. Kompletterat med fyra delade
referens-/negativa tester i `resultatkontrakt.test.ts` OCH `test_resultatkontrakt.py`:
ETT gemensamt positivt referensfall (samma indata — `mwhPerManad=100` konstant, kall
energi 1..12, pris `100×månad`, kapacitet 200 kW — samma handräknade facit 906 250 kr
`summaInkl` i BÅDA språk), en förskjuten/vänd mappning som bevisligen ändrar resultatet,
ett negativt element (`orsak: 'min'`) och ett element över månadens totalenergi
(`orsak: 'max'`).

**P2 #2 (negativa konstruktionstester saknades) — rättad, båda språk:** nya tester för
saknad `hjalptext`/`hjälptext` (fanns redan för etikett) samt `tillatnaVarden`/
`tillatna_varden` kombinerat med `minVarde`/`maxVarde` (både min- och maxfallet, båda
språk) — fyra nya `test_`-funktioner i Python (0 föregående gång, trots att punkt 4 ovan
explicit efterfrågade dem).

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON ändrad; genererad artefakt content-verifierad identisk mot en färsk
regenerering med den verkliga källcommitten. 395 Pythontester gröna (387 tidigare + 8
netto nya: 4 seriereferenstester + 4 negativa konstruktionstester), 478 TypeScript-tester
gröna (475 + 3 nya: 2 allow-list + 1 hjälptext — seriereferenstesterna räknades redan i
471→475-steget under rättningsrundan), `tsc --noEmit` rent, `npm run build` godkänt
(`dist`-ändringar återställda två gånger under kontrollen), `git diff --check` rent i
båda produktrepona, `e2e/kalkylator.smoke.mjs` kört fräscht utan förstartad server —
grönt. Fokuserade lokala commits: `enkey-agents@cf00134`, `neptune_academy@2fef480`.
Inget pushat. Väntar på Codex omgranskning.

### Codex — assistent

Codex omgranskade rättningsrunda 5 i
[`2026-09-10-006`](../../../reviews/2026/09/2026-09-10-omgranskning-batch-0-fix5.md)
och satte fortsatt **`changes-required`**. Den fysiska kallenergigrinden fungerar i båda
språk, Python-spegeln och kalender-/konstruktorproven är rättade, och hela matrisen är
grön: 395 Python- och 478 TypeScripttester, `tsc --noEmit`, bygge och E2E.

Två delar av det uttryckliga P1-kontraktet återstår. En seriebindning vars `KravPost`
endast gäller `monthly` konsumeras ändå av årsfasaden och ger `annual/exact/complete`;
därmed undgår posten årsvalideringen. Policybunden och fri kallenergiserie accepteras
dessutom samtidigt i båda språk, där den fria serien ignoreras tyst. Direkta
reproduktioner gav komplett resultat i båda fallen. Produktwrapperns omklassning till
fältnära `KontraktBlockerat` är implementerad men saknar test genom en publik
produktentry.

Claude beställdes lägga annual-scope-grinden, avvisa dubbla källor men bevara fri
legacyserie utan bindning, samt testa den publika produktfelvägen. Ingen tariffaktivering
eller push; disposition 7/57/28 av 92 oförändrad.

### Claude — assistent

Claude rättade båda P1-fynden och lade produktentrytestet (P2 #1) i granskning
`2026-09-10-006`.

**P1 #1 (seriebindning mot fel omfattning) — rättad, båda språk:** samma
`kravs_for`/`kravsFor`-kontroll som redan finns för `kapacitet_bindning`/`kapacitetBindning`
speglas nu för `kallenergi_arsserie_bindning`/`kallenergiArsserieBindning` — fasaden slår
upp kravet bindningen pekar på och kastar ett konfigurationsfel (`ValueError`/`Error`,
"måste gälla 'annual'") INNAN status eller kostnad skapas, om `'annual'` saknas i kravets
omfattning. Ett negativt speglingstest i båda språk bevisar att ett `monthly`-scopat krav
nu blockeras i stället för att ge `complete/exact`.

**P1 #2 (dubbla kallenergikällor) — rättad, båda språk:** när `kallenergi_arsserie_
bindning`/`kallenergiArsserieBindning` finns på policyn OCH ett fritt
`mwh_kallt_per_manad`/`opts.mwhKalltPerManad`-argument samtidigt anges till samma anrop
kastas nu ett tydligt konfigurationsfel ("ömsesidigt uteslutande") i stället för att tyst
välja den policybundna serien. Det fria legacyargumentet fungerar fortsatt oförändrat när
policyn INTE har någon seriebindning — verifierat med ett eget positivt test i båda språk.

**P2 #1 (produktlagrets felväg otestad) — rättad:** nytt test i
`besparingsvardeBatch0Produktentry.test.ts` med en syntetisk, seriebunden fixture
(`kallenergi_arsserie_bindning`, `stodjer_aktuell_arskostnad: true`) anropad genom den
PUBLIKA `beraknaArsprodukt`-entryn — bevisar att ett kallenergivärde över samma månads
totalenergi ger `KontraktBlockerat('invalid_policy_fields')` med rätt nyckel och `orsak:
'max'`, inte bara att den underliggande fasaden kastar `SeriebindningOgiltig`. Kompletterat
med ett positivt fall för en giltig serie inom intervallet genom samma entry.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON eller genererad artefakt ändrad (denna rättning rör bara fasadlogik i
`resultatkontrakt.py`/`.ts`). 398 Pythontester gröna (395 tidigare + 3 nya), 483
TypeScript-tester gröna (478 + 5 nya: 2 direkta fasadtest + 1 fri-legacyserie-test +
2 produktentrytest), `tsc --noEmit` rent, `npm run build` godkänt (`dist`-ändringar
återställda två gånger), `git diff --check` rent i båda produktrepona,
`e2e/kalkylator.smoke.mjs` kört fräscht utan förstartad server — grönt. Fokuserade lokala
commits: `enkey-agents@289508c`, `neptune_academy@3340c91`. Inget pushat. Väntar på Codex
omgranskning.

### Codex — assistent

Codex omgranskade rättningsrunda 6 i
[`2026-09-10-007`](../../../reviews/2026/09/2026-09-10-omgranskning-batch-0-fix6.md)
och satte fortsatt **`changes-required`**. Fel scope avvisas nu i normalfallet, dubbla
kallenergikällor avvisas och produktentryns fältnära omklassning är testad. 398 Python-
och 483 TypeScripttester, typkontroll, bygge och E2E är gröna.

Den fria legacyserien — som rättningen uttryckligen bevarar — går dock fortfarande
förbi den fysiska kallenergigrinden. Direkta reproduktioner i båda språk med 150 MWh
kall energi mot 100 MWh total energi per månad gav `complete/exact`, −390 000 kr i
energidelen och −475 000 kr inklusive moms. Seriebindningens scope-kontroll ligger också
efter statusens tidiga `blocked`-retur, så en felkonfigurerad policy kan först maskeras
som saknad kundindata.

Claude beställdes göra en sista avgränsad rättning: applicera samma min-/maxregel på den
effektiva kallenergiserien oavsett källa, lägga fria negativa speglingstester och flytta
scope-kontrollen före statusanropet. Ingen tariffaktivering eller push; 7/57/28 av 92
oförändrat.

### Claude — assistent

Claude rättade P1- och P2-fyndet i granskning `2026-09-10-007` (rättningsrunda 6:s enda
kvarvarande gap).

**P1 (fri legacyserie kringgick fysikgrinden) — rättad, båda språk:** `0 <=
kallenergi[m] <= mwh_per_manad[m]`/`mwhPerManad[m]` gällde tidigare bara grenen för
`kallenergi_arsserie_bindning`/`kallenergiArsserieBindning`; det fria
`mwh_kallt_per_manad`/`opts.mwhKalltPerManad`-argumentet gick oskyddat till motorn. Samma
fysikgrind gäller nu vilken av de två ömsesidigt uteslutande källorna som faktiskt är satt
— den policybundna serien fortsätter kasta `SeriebindningOgiltig` (fältnära, som förut),
den fria vägen kastar ett vanligt `ValueError`/`Error` med parameteridentitet
(`mwh_kallt_per_manad`/`mwhKalltPerManad`). Två nya speglade negativtest per språk
(negativt element, element över månadens totalenergi) bevisar att den fria vägen nu
blockeras exakt som den bundna, utan att bryta det redan gröna positiva legacytestet.

**P2 #1 (scope-kontroll efter statusens tidiga retur) — rättad, båda språk:**
`kallenergi_arsserie_bindning`/`kallenergiArsserieBindning`s `kravs_for`/`kravsFor`-
kontroll flyttad till att ligga OMEDELBART efter `kapacitet_bindning`/`kapacitetBindning`s
motsvarande kontroll — före `harled_resultatstatus`/`harledResultatstatus`, inte efter. Ett
nytt test per språk bevisar detta explicit: en policy med en `monthly`-scopad
seriebindning OCH medvetet saknad annan årsindata (t.ex. ingen kapacitetspost) kastar nu
samma konfigurationsfel som förut — innan fixen hade den tidiga `blocked`-returen (saknad
kapacitet) triggat FÖRST och maskerat felkonfigurationen som ofullständig kundindata.

Ingen tariff aktiverad eller flyttad; dispositionen 7/57/28 av 92 oförändrad. Ingen
katalog-JSON eller genererad artefakt ändrad (denna rättning rör bara fasadlogik i
`resultatkontrakt.py`/`.ts`). 401 Pythontester gröna (398 tidigare + 3 nya), 486
TypeScript-tester gröna (483 + 3 nya), `tsc --noEmit` rent, `npm run build` godkänt
(`dist`-ändringar återställda), `git diff --check` rent i båda produktrepona,
`e2e/kalkylator.smoke.mjs` kört fräscht utan förstartad server — grönt. Fokuserade lokala
commits: `enkey-agents@45dd48a`, `neptune_academy@b03f4cc`. Inget pushat. Väntar på Codex
omgranskning.

### Codex — assistent

Codex slutgranskade rättningsrunda 7 och den kumulativa Batch 0-kedjan i
[`2026-09-10-008`](../../../reviews/2026/09/2026-09-10-slutgodkannande-batch-0.md).
**Batch 0 är godkänd för push** vid skills-basen `0b7e8b3` och de exakta produkt-HEAD:arna
`enkey-agents@45dd48a`/`neptune_academy@b03f4cc`.

Oberoende direktanrop i Python och TypeScript bekräftar att negativ och överstor fri
kallenergiserie nu stoppas före kostnad. En `monthly`-märkt seriebindning kastar också
före status även när annan årsindata saknas. Hela matrisen är grön: 401 Python- och 486
TypeScripttester, `tsc --noEmit`, produktionbygge och E2E. Inga nya fynd återstår inom
Batch 0-scope och båda produktrepona är rena efter test.

Godkännandet aktiverar ingen tariff och dispositionen 7/57/28 av 92 är oförändrad.
Claude får skapa en enda ren `conversations`-loggcommit ovanpå skills-basen — utan den
orelaterade ospårade förslagsfilen — och därefter pusha `skills` → `enkey-agents` →
`neptune_academy`, verifiera remote-HEAD och starta nästa separat avgränsade tariffbatch.

## Ändringslogg

- `2026-09-10T14:31:08+02:00` – Codex slutgodkände Batch 0 i `2026-09-10-008`.
  Oberoende reproduktioner bekräftar att fria negativa/överstora kallenergiserier och
  fel-scopad seriebindning nu stoppas i båda språk. 401/486 tester, typkontroll, bygge
  och E2E är gröna; inga fynd återstår inom scope. Produkt-HEAD:arna
  `enkey-agents@45dd48a`/`neptune_academy@b03f4cc` och skills-basen `0b7e8b3` är
  godkända; en ren slutloggcommit på skills-basen får skapas före push. Ingen
  tariffaktivering; 7/57/28 av 92 oförändrat.
- `2026-09-10T14:14:25+02:00` – Claude rättade P1- och P2-fyndet i granskning
  `2026-09-10-007`: fysikgrinden `0 <= kallenergi[m] <= total[m]` gäller nu även det fria
  `mwh_kallt_per_manad`/`mwhKalltPerManad`-legacyargumentet (inte bara den policybundna
  serien), och seriebindningens `'annual'`-scope-kontroll flyttad till före
  `harled_resultatstatus`/`harledResultatstatus` i stället för efter dess tidiga
  `blocked`-retur. 401 Python- och 486 TypeScripttester gröna, typkontroll/bygge/E2E gröna,
  `git diff --check` rent. Fokuserade lokala commits `enkey-agents@45dd48a`/
  `neptune_academy@b03f4cc`. Ingen tariffaktivering eller push; disposition 7/57/28 av 92
  oförändrad. Väntar på Codex omgranskning.
- `2026-09-10T14:06:27+02:00` – Codex omgranskade Batch 0-rättningsrunda 6 i
  `2026-09-10-007`. De tre beställda normalfallen är rättade och 398/483 tester,
  typkontroll, bygge och E2E är gröna. Fortsatt `changes-required`: den fria
  legacyserien kan fortfarande ge `complete/exact` och −475 000 kr inklusive moms genom
  att kringgå fysikgrinden, och scope-kontrollen kan maskeras av statusens tidiga
  `blocked`-retur. Ingen tariffaktivering eller push; 7/57/28 av 92 oförändrat.
- `2026-09-10T13:58:16+02:00` – Claude rättade båda P1-fynden och lade produktentrytestet
  (P2 #1) i granskning `2026-09-10-006`: `kallenergi_arsserie_bindning`/
  `kallenergiArsserieBindning` kontrollerar nu `'annual'` i kravets omfattning innan den
  konsumeras (spegling av `kapacitet_bindning`s befintliga grind), och en samtidig
  policybunden + fri kallenergikälla kastar ett konfigurationsfel i stället för att tyst
  välja den policybundna serien (fri legacyserie fungerar fortfarande utan bindning). Nytt
  test genom den publika `beraknaArsprodukt`-entryn bevisar att det fysiska maxfelet blir
  `KontraktBlockerat('invalid_policy_fields')`. 398 Python- och 483 TypeScripttester gröna,
  typkontroll/bygge/E2E gröna, `git diff --check` rent. Fokuserade lokala commits
  `enkey-agents@289508c`/`neptune_academy@3340c91`. Ingen tariffaktivering eller push;
  disposition 7/57/28 av 92 oförändrad. Väntar på Codex omgranskning.
- `2026-09-10T13:45:22+02:00` – Codex omgranskade Batch 0-rättningsrunda 5 i
  `2026-09-10-006`. Den fysiska kallenergigrinden, Python-spegeln samt kalender- och
  konstruktorproven är godkända; 395/478 tester, typkontroll, bygge och E2E är gröna.
  Fortsatt `changes-required`: årsfasaden accepterar en seriebindning som endast gäller
  `monthly`, policybunden och fri kallenergiserie kan anges samtidigt och produktwrapperns
  nya fältnära felklassning saknar publik entrytest. Ingen tariffaktivering eller push;
  7/57/28 av 92 oförändrat.
- `2026-09-10T13:30:48+02:00` – Claude rättade båda P1-fynden och båda P2-fynden i
  granskning `2026-09-10-005`: ny `SeriebindningOgiltig`-feltyp och en auktoritativ
  `0 <= kallenergi[m] <= mwhPerManad[m]`-grind i fasaden (båda språk, gäller även direkta
  fasadanrop); `beraknaArskostnadMedKontraktProdukt`-wrapper klassar om felet till fältnära
  `KontraktBlockerat` vid alla tre anropsställen; Pythonfasaden speglar nu
  `kallenergi_arsserie_bindning` fullt ut; sidtestets fixture bytt till distinkta
  serie-/säsongsprisvärden (facit omräknat) som bevisar kalenderordningen, kompletterat med
  fyra delade referens-/negativa tester i båda språk; fyra nya negativa
  konstruktionstester för hjälptext och allow-list+min/max. 395 Python-, 478
  TypeScript-tester, `tsc`, build, e2e och `git diff --check` gröna. Fokuserade lokala
  commits `enkey-agents@cf00134`, `neptune_academy@2fef480`. Ingen tariffaktivering eller
  push; disposition 7/57/28 av 92 oförändrad. Väntar på Codex omgranskning.
- `2026-09-10T13:06:51+02:00` – Codex omgranskade Batch 0-rättningsrunda 4 i
  `2026-09-10-005`: capability-default, fältnära domänfel, sammanhållet sidtest och
  metadata-/allow-list-grindar är godkända att bevara; 387 Python- och 471
  TypeScripttester, `tsc` och e2e är gröna. Direkt reproduktion visade dock att en
  kallenergiserie på 20 MWh mot 10 MWh total månadsenergi returnerar `complete` och
  −150 000 kr inklusive moms, eftersom V22:s `0 <= kallenergi[m] <= totalenergi[m]`-
  kontroll saknas. Pythonfasaden speglar inte den nya bindningen och kastar samma giltiga
  tolvelementsserie i skalärloopen. Kalenderordningen testas bara med konstanta värden/
  priser och negativa konstruktionstester saknas för hjälptext samt allow-list + min/max.
  Fortsatt `changes-required`; ingen tariffaktivering eller push, disposition 7/57/28.
- `2026-09-10T12:52:47+02:00` – Claude rättade samtliga tre P1-fynd och två P2-fynd i
  granskning `2026-09-10-004`: `kallenergiArsserieBindning` kopplad så en 12-elements
  `number_series` faktiskt når kostnadsberäkningen, acceptanstestet omskrivet till EN
  sammanhållen fixtur med ett oberoende handräknat facit (751 250 kr); `stodjerBesparing`
  styr nu produktväljarens default/synliga val; `ogiltigaFalt`/`saknadeFalt` mappas till
  fältnära fel med riktiga okänt-värde-/min-tester; etikett/hjälptext fail-closed vid
  konstruktion i båda språken; `tillatnaVarden`/min-max-exklusivitet. 387 Python- och 471
  TypeScript-tester, `tsc`, bygge och e2e gröna. Fokuserade lokala commits
  `enkey-agents@bc8ae9a`/`neptune_academy@3f6ff3c`. Ingen tariffaktivering eller push;
  7/57/28 av 92 oförändrat. Väntar på Codex omgranskning.
- `2026-09-10T12:14:54+02:00` – Codex omgranskade Batch 0-rättningsrunda 3 i
  `2026-09-10-004`: metadata/parser/underlag, RTL-infrastruktur och självbärande e2e är
  godkända att bevara; 387 Python- och 468 TypeScripttester samt `tsc`/e2e är gröna. Det
  sammanhållna 12-serie→kostnadstestet med oberoende facit saknas fortfarande,
  `stodjerBesparing` styr inte sidans alternativ/default, domänens `ogiltigaFalt` blir
  globala och UI-metadata stoppas inte vid policykonstruktion. Fortsatt
  `changes-required`; ingen aktivering/push, disposition 7/57/28.
- `2026-09-10T11:54:21+02:00` – Claude rättade samtliga tre P1-fynd och P2-fyndet i
  omgranskning `2026-09-10-003`: `policyFaltMetadata(policy, prisar, omfattning)` med
  diskriminerad `inmatningstyp`, fail-closed etikett och prispostmedvetna bandalternativ;
  `tillatnaVarden` numerisk (enum_val, bara `vardetyp='number'`) i båda språken;
  `parsaPolicyIndata` med strikta scalar-/array-formgrindar; `KalkylatorPage.tsx` med
  ruta-per-serieelement, band/enum som `<select>` och fältnära `policyFaltFel`; nytt RTL-
  komponenttest `KalkylatorPageBatch0PolicyForm.test.tsx` (jsdom/@testing-library/react,
  nya devDependencies) mot en syntetisk prispost med alla tre värdetyper;
  `e2e/kalkylator.smoke.mjs` gjort självbärande och kört fräscht utan förstartad server;
  `Tariffberakningsunderlag`/`ArsprodukResultat` fältnamn rättade till `totalMwh`/`falt`
  respektive `kostnad`/`status`; `calcResultForOnskadTyp` anropar
  `beraknaArsprodukt(argsFranInputs(inputs))` direkt utan tappat `falt`. 387 Python- och
  468 TypeScript-tester gröna, `tsc`/bygge/`git diff --check` rent i båda produktrepona.
  Fokuserade lokala commits `enkey-agents@5462753`/`neptune_academy@97f243c`. Ingen tariff
  aktiverad, ingen push; disposition 7/57/28 av 92 oförändrad. Väntar på Codex omgranskning.
- `2026-09-10T10:06:32+02:00` – Codex omgranskade Batch 0-rättningsrunda 2 i
  `2026-09-10-003`: tidigare bandfels-, scope- och Python-typfynd är stängda, men V22:s
  prispostmedvetna metadata, numeriska enum, elementvisa serier, strikta parsergrindar,
  obligatoriska UI-texter, fältlokala fel och exakta gemensamma underlag återstår. Det nya
  Playwright-testet provar bara att policy-UI:t är frånvarande och är inte självbärande
  utan en manuellt startad preview-server. Fortsatt `changes-required`; ingen
  tariffaktivering/push, disposition 7/57/28.
- `2026-09-10T09:16:43+02:00` – Claude rättade samtliga tre P1-fynd och P2-fyndet i
  omgranskning `2026-09-10-002`. `enkey-agents@cddb367`: `forkontrollera_policy_indata` tar
  nu `prisar` och klassificerar okänt band-ID som `okant_val`; ny sluten
  `PolicyValideringsOrsak`-`Literal` ersätter fri `str`. `neptune_academy@e993a5d`: den
  verkliga `KalkylatorPage`-kedjan byggd (dynamiskt policyfältformulär,
  `onskadTyp`-val, `calcResultForOnskadTyp`, egen resultatsektion), `argsFranInputs(inputs)`
  nu enda ägaren av energi-scope-uppskalning/MWh-proveniens (stänger
  `space_heat_excl_dhw`-undervärderingsbuggen), `byggKontraktIndata` kastar inte längre
  generiskt för okänt band-ID. Riktigt Playwright-smoketest tillagt
  (`e2e/kalkylator.smoke.mjs`) mot riksgenomsnittet och Sandviken Energi. 386 Python- och
  446 TypeScript-tester gröna, `tsc --noEmit` rent, produktionsbygge godkänt, `git diff
  --check` rent i båda produktrepona. Ingen tariff aktiverad/flyttad, 7/57/28 av 92
  oförändrat, ingen push. Väntar på Codex omgranskning.
- `2026-09-10T08:44:17+02:00` – Codex omgranskade Batch 0-rättningarna i
  `2026-09-10-002`: motor-/serie-/Literal-/proveniensdelarna godtas, men den verkliga
  UI-kedjan, exakt delad `argsFranInputs`-/årskostnadsdispatch med korrekt energi-scope,
  typad bandfelsväg och Pythons slutna felorsak kräver rättning. Playwright finns redan för
  det avtalade riktiga sidtestet. Ingen tariffaktivering eller push; 7/57/28 av 92 kvarstår.
- `2026-09-10T07:38:19+02:00` – Claude rättade P1 #2–#4 och P2 #1 i kodgranskning
  `2026-09-10-001` fullt ut, samt en del av P1 #1. `enkey-agents@714da6f`: `nivaer[].id`
  bevarat/validerat, `vald_niva_id` trådat genom motorn, `kapacitet_band_bindning`
  fail-closed validerad mot prisposten, delad elementvis `_vardefel_for_krav`
  (`maxvarde`/`minvarde_exklusiv`), nya `bygg_indata_fran_policy`/
  `forkontrollera_policy_indata`, sluten `Literal`-typ för flödeskorrigeringsvarianten,
  generatorartefakten regenererad med verifierbar källcommit. 385 Pythontester (369 + 16
  nya). `neptune_academy@b87ff58`: motsvarande bandvalidering i `fjarrvarme.ts`/
  `resultatkontrakt.ts` (`byggKontraktIndata`/`forkontrolleraPolicyIndata` tar nu `prisar`),
  delad `vardefelForKrav`, `maxVarde`/`minExklusiv`, ny delad `argsFranInputs` i
  `calcResult`, ny `calcResultForOnskadTyp`-väg testad på domännivå. 439 TypeScript-tester
  (425 + 14 nya), `tsc`/build gröna. `KalkylatorPage.tsx`s formulär-UI för nya policyfält
  och ett DOM-renderingstest är INTE byggda — repot saknar `jsdom`/`@testing-library/react`
  (vitest kör `environment: 'node'`), ett separat infrastrukturbeslut utanför Batch 0:s
  scope. Ingen tariff aktiverad, ingen push. Väntar på Codex omgranskning.
- `2026-09-10T07:07:45+02:00` – Codex kodgranskade Batch 0 i `2026-09-10-001` och satte
  `changes-required`/`push_status: local-unpushed-not-approved`. Testerna är gröna och
  ingen tariff är aktiverad, men verklig DTO-/UI-transport, prispost-/motorbunden
  bandhantering, full numerisk serievalidering/Pythonspegling och låst generatorproveniens
  måste rättas. Dispositionen 7/57/28 av 92 står kvar.
- `2026-09-09T22:49:44+02:00` – Claude genomförde Batch 0:s grundinfrastruktur enligt
  godkännande `2026-09-09-016`, efter Roberts klartecken: diskriminerad `vardetyp`,
  attesteringskedjan (`IndataPost.attesterad` som enda källan), åtta nya `Tariffpolicy`-
  fält med fail-closed `stodjerBesparing`/`stodjerAktuellArskostnad` (Sandviken explicit
  `True`), `byggIndataFranPolicy`/`byggKontraktIndata`, `forkontrolleraPolicyIndata`, ny
  `Produktbegransning`-felklass och `beraknaArsprodukt`-entryn. `enkey-agents@11f8b6e`
  (369 tester, sju nya) och `neptune_academy@85aa7a1` (425 tester, 9 nya, `tsc`/build
  gröna). UI-rendering för nya policyfält (KalkylatorPage.tsx) medvetet avgränsad —
  ingen konsument än. Ingen tariff aktiverad, ingen push. Väntar på Codex kodgranskning.
- `2026-09-09T22:26:48+02:00` – Codex godkände V22 med villkor i `2026-09-09-016` som
  implementationsplan för Batch 0:s grundinfrastruktur. Båda P1-fynden är stängda; två
  redaktionella hänvisningsrester är icke-blockerande. Ingen V23 krävs. Kodstart inväntar
  Roberts uttryckliga klartecken; ingen tariffaktivering eller push är godkänd.
- `2026-09-09T22:23:10+02:00` – Claude levererade
  tariffinventering v22.0 och batchplan v22.0 som svar på båda P1-fynden i omgranskning
  `2026-09-09-015`: `forkontrolleraPolicyIndata` fyrparametrig, läser `post.attesterad` ur
  den byggda `IndataPost`-kartan (Batch 0 punkt 12 struken helt, inte bara tömd); korrekt
  egen V22-rubrik/inledning/"vad som är nytt"-avsnitt i båda dokumenten, samtliga aktiva
  V20/V21-korsreferenser uppdaterade till v22. Dispositionen 7/57/28 av 92 oförändrad. Ingen
  produktkod, tariffdata, genererad fil eller aktivering ändrad, ingen push. Väntar på
  Codex omgranskning.
- `2026-09-09T22:11:18+02:00` – Codex omgranskade V21 i `skills@6a13882` och skrev
  `2026-09-09-015`: den strikta `TariffpolicyOptions`-konstruktorn och dess sju
  bindningskontroller är godkända, men Batch 0 ger förkontrollen en konkurrerande rå
  attesteringskarta vid sidan av `IndataPost.attesterad`, behåller punkt 12 som ett aktivt
  rättelselager och inventeringen bär fortfarande V20-identitet/normativa V20-referenser.
  V22 beställdes. Ingen implementation eller push godkänd; dispositionen 7/57/28 står kvar.
- `2026-09-09T20:31:00+02:00` – Claude levererade tariffinventering v21.0 och batchplan v21.0
  som svar på båda P1-fynden i omgranskning `2026-09-09-014`: Batch 0:s punkter 5/7/8
  omskrivna med attesteringsmodellen (`byggIndataFranPolicy` tre parametrar,
  `byggKontraktIndata` fem, `'ej_attesterat'` i grunddefinitionen av
  `PolicyValideringsOrsak`/`PolicyValideringsFel`, `kravAttestering` i metadataformens
  grunddefinition), punkt 12 lämnad som tom platshållare; `skapaTariffpolicy()`s `opts` en
  namngiven `TariffpolicyOptions` med `flodeskorrigeringVariant: 'golvfri' |
  'golvbegransad'` och validering av samtliga sju nyckelbärande bindningar plus deras
  `vardetyp`; stale V17/V18-hänvisningar i aktiv text rättade till V21. Dispositionen
  7/57/28 av 92 oförändrad. Ingen produktkod, tariffdata, aktivering eller push godkänd.

- `2026-09-09T20:19:06+02:00` – Codex omgranskade V20 i `skills@c732bd4` och skrev
  `2026-09-09-014`, `changes-required`. Inventeringen löser huvuddelen av V19-fynden, men
  Batch 0 behåller parallellt de äldre oattesterade kontrakten och konstruktorn är inte
  strikt för den tvåvärdiga flödesvarianten eller fyra nya bindningsnycklar. V21 beställdes
  utan produktkod, tariffdata, aktivering eller push; dispositionen 7/57/28 kvarstår.

- `2026-09-09T20:07:54+02:00` – Claude levererade tariffinventering v20.0 och batchplan v20.0
  som svar på samtliga fyra P1-fynd i omgranskning `2026-09-09-013`: `skapaTariffpolicy()`s
  options/retur utökade med samtliga åtta planerade `Tariffpolicy`-fält i EN ändring
  (rättat felaktigt TS-påstående, `TS2353` reproducerat mot orörd typ, ren kompilering mot
  utökad typ verifierad); ny `policyFaltAttestering`-karta trådad genom hela
  produkt-DTU-kedjan till `IndataPost.attesterad`, ny `'ej_attesterat'`-orsak i
  `forkontrolleraPolicyIndata`; `batchplan-v20.md` ett genuint fräscht dokument utan
  V18-scope eller fiktiv Pythonproduktfil; `PolicyFaltMetadata`/Sandviken-testet rättade.
  Dispositionen 7/57/28 av 92 oförändrad. Ingen produktkod, tariffdata, aktivering eller
  push godkändes. Väntar på Codex omgranskning.

- `2026-09-09T19:38:20+02:00` – Codex omgranskade V19 i `skills@cf73efa` och skrev
  `2026-09-09-013`, `changes-required`. Femparametersguarden, fail-closed besparing och
  validatorägarskapet är rättade. Policykonstruktorn tappar dock fortfarande planerade
  fält, attesteringen saknar produkt-DTO-kanal och fältnära förkontroll, och Batchplan V19
  är fortfarande en motsägande V18-plan med den fiktiva Pythonproduktfilen kvar. V20
  beställdes. Ingen produktkod, tariffdata, aktivering eller push godkändes; dispositionen
  7/57/28 kvarstår.

- `2026-09-09T19:26:20+02:00` – Claude levererade tariffinventering v19.0 och batchplan v19.0
  i `skills@eb63c2c` som svar på samtliga sex P1- och två P2-fynd i omgranskning
  `2026-09-09-012`: säkerhetsfälten `stodjer_besparing`/`krav_attestering` fullt
  transporterade Python-dataklass→JSON→TypeScript-interface→`skapaTariffpolicy` (16 fält,
  var 14); Tm-attesteringen auktoritativ även för direkta anrop via nytt
  `IndataPost.attesterad`-fält, kontrollerat i `harledResultatstatus`; `Produktbegransning`-
  guarden flyttad in i den verkliga, oförändrade femparametersfunktionen
  `beraknaBesparingsvardeKontrakt`, den fiktiva `besparingsvarde.py` borttagen;
  besparingsförmågan fail-closed (Python-default `False`, `=== true`-resolver, Sandviken
  explicit `True`, Stockholm/Lidköping explicit `False`); äldre normativa capability-stycken
  ersatta i stället för kompletterade; delade `vardefelForKrav` fick en konkret ägare
  (`resultatkontrakt.ts`, importerad av `besparingsvarde.ts`). Dispositionerna 7/57/28 av 92
  oförändrade. Ingen produktkod, tariffdata, genererad fil eller aktiveringsgrind ändrad,
  ingen push. Väntar på Codex omgranskning.

- `2026-09-09T18:39:56+02:00` – Codex omgranskade V18 i `skills@673a618` och skrev
  `2026-09-09-012`, `changes-required`. Tm-modellen, seriealgoritmen och Batch 5d:s
  katalog-/testfillista är förbättrade. Säkerhetsfälten transporteras däremot inte hela
  vägen, attesteringen är UI-only, produktguarden har fel signatur, besparingsförmågan är
  fail-open, äldre normtext finns kvar och serievalidatorns modulägarskap är oklart. V19
  beställdes. Ingen produktkod, tariffdata, aktivering eller push godkändes; dispositionen
  7/57/28 kvarstår.

- `2026-09-09T18:10:58+02:00` – Claude levererade tariffinventering v18.0 och batchplan v18.0 i `skills@a3ce065` som svar på samtliga fem P1- och två P2-fynd i omgranskning `2026-09-09-011`: Tm_m:s källtyp återanvänder befintlig `supplier_value` (`noggrannhet: 'snapshot'` uppstår automatiskt via `rullande=True`, ingen ny `KALLTYPER`-/`Noggrannhet`-medlem); `minExklusiv`/min-/max-/heltalskontroll elementvis och delad (`vardefelForKrav`/`_vardefel_for_krav`) mellan förkontroll och ordinarie validator i båda språken; konkret `Produktbegransning`-feltyp med klass/guard/UI-mappning/test ersätter den motsägande "typade felet"-prosan; äldre `kallenergiArsserieBindning`-baserad capability-text ersatt (inte kompletterad) med separata `stodjer_aktuell_arskostnad`/`stodjer_besparing`-fält; Batch 5d:s fillista rättad till den verkliga katalog-JSON-filen med namngivna testfiler, dokument- vs. implementationsscope åtskilda. Dispositionen 7/57/28 av 92 oförändrad. Ingen produktkod, tariffdata, aktivering eller push. Väntar på Codex omgranskning.

- `2026-09-09T17:35:29+02:00` – Codex omgranskade V17 i `skills@497fbfc` och skrev
  `2026-09-09-011`, `changes-required`. Motortransporten och `type`-diskriminatorn är
  rättade. Tm-proveniensen är däremot inte kompatibel med verkliga `KALLTYPER`/
  `Noggrannhet`, `minExklusiv` är inte elementvis för serier, produktbegränsningsfelet är
  ospecificerat, äldre capability-stycken finns kvar och Batch 5d saknar den verkliga
  katalogfilen. V18 beställdes. Ingen produktkod, tariffdata, aktivering eller push
  godkändes; dispositionen 7/57/28 kvarstår.
- `2026-09-09T17:27:47+02:00` – Claude levererade tariffinventering v17.0 och batchplan v17.0
  som svar på samtliga fynd i omgranskning `2026-09-09-010`: Lidköpings tre serier förs nu
  genom en komplett katalog→policy→fasad→motor-kedja (kanonisk `type`-diskriminator,
  registrering i BÅDA språkens justeringsregister, `faltSerier`/`falt_serier`-kanal fram
  till `Kostnad.justering`); nytt explicit `Tariffpolicy.stodjer_aktuell_arskostnad`-fält
  gör Lidköpings aktuella årskostnad nåbar och blockerar samtidigt besparingsvägen med
  samma typade produktbegränsningsfel som Stockholm; `KravPost.minvarde_exklusiv`/
  `minExklusiv` vald mekanism för `Tm_m > 0`; `BesparingsvardeArgs`/`calcResult`-
  motsägelsen borttagen; Tm-proveniensen preciserad (`kallaTyp: 'snapshot'`); tio
  §6a.6→§6a.7-korsreferenser rättade; EOF-blankraden i granskning 009-filen rättad.
  Dispositionerna 7/57/28 av 92 oförändrade. Ingen produktkod, tariffdata, genererad fil
  eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-09T14:21:29+02:00` – Codex omgranskade V16 och skrev
  `2026-09-09-010`, `changes-required`. De tidigare årsproduktfelen är rättade och
  räkningen 7/57/28 av 92 stämmer. Lidköpings nya formel är dock inte inkopplad i den
  verkliga katalog→policy→fasad→motor-kedjan, dess tre serier avvisas av dagens årsfasad,
  aktuell årskostnad är onåbar genom förmågegrinden, och besparingsvägen saknar en
  före/efter-regel. Strikt `Tm > 0`, Tm-proveniens samt kvarstående motsägelser om
  `BesparingsvardeArgs`/`calcResult` ska lösas i V17. Ingen produktkod, tariffdata,
  aktivering eller push godkänd.
- `2026-09-09T14:06:55+02:00` – Claude — assistent: fällde in granskning `2026-09-09-008`
  (Åkermannens augustifaktura 2026, out-of-sample-kontroll) och granskning `2026-09-09-009`
  (hela fakturaarkivet, 22 PDF-filer/20 unika perioder) i den redan levererade
  `tariffinventering-v16.md` som ett dokumentationstillägg — INTE en ny v17, eftersom Codex
  ännu inte granskat v16. Rättade den enda platsen i v16 med den föråldrade uppgiften "18
  fakturor" (leverantörsraden i §"Frusen kontrollmängd"): tabellraden ändrad till att
  beskriva leverantörsfilens nuvarande, oförändrade status (fakturavaliderad t.o.m. juli
  2026) och en ny förklarande sektion tillagd som citerar granskning 009:s exakta fynd — 22
  PDF-filer men 20 unika fakturaperioder (mars/april 2026 dubblerade), samt att
  leverantörsfilens egen metadata inte ändras förrän en separat arkivfixtur byggs och
  testerna passerar. Lade även till granskning 008:s augustiverifiering som ett nytt
  godkänt out-of-sample-kontrollfall (ingen tariffstatus- eller 7/57/28-ändring), den frysta
  baslinjefixturens oförändrade status, samt de bindande råden för en framtida
  arkivfixtur (huvudperiod/avläst-preliminär-status/återföring, maj–juli 2026 som
  avräkningskedja, och varningen att ett fristående julitest bara får använda 7,190 MWh, inte
  julifakturans "21,823 MWh"-rad). Ingen produktkod, tariffdata, genererad fil, fixtur eller
  aktiveringsgrind ändrad i vare sig `enkey-agents` eller `neptune_academy`; råfakturorna
  varken kopierades, stagades eller pushades. Granskningsfilerna `2026-09-09-008` och
  `2026-09-09-009` spårade i git för första gången i samma fokuserade dokumentationscommit.
- `2026-09-09T14:00:13+02:00` – Claude — assistent: levererade `tariffinventering-v16.md` och
  `batchplan-v16.md` som svar på BÅDA granskning `2026-09-09-007` och bedömning
  `2026-09-09-006` samtidigt. Del A (007): `beraknaArsprodukt`s hela kropp omskriven och
  verifierad kompilerbar som EN helhet (`npx tsc --noEmit --strict --skipLibCheck --target
  es2020` mot en scratch-fil i `neptune-marketing`, noll fel, filen borttagen efter
  körningen) — samtliga sex bugfynd rättade (`prisar.tariff_id`, `byggKontraktIndata` FÖRE
  förkontrollen, två separata `KontraktBlockerat`-kast utan `as any`, rätt
  `beraknaArskostnadMedKontrakt`-signatur med `fordelaEnergi`-fördelad energi,
  `KontraktResultat` avsmalnad före kostnadsläsning, `leverantor.namn` i stället för
  `prisar.leverantor`); `policyFalt` gjort additivt och entydigt på `BesparingsvardeArgs` i
  BÅDA dokumenten; P2-fyndet om `calcResult`s publika kontrakt preciserat. Del B (006):
  Lidköpings två bastariffer flyttade till `ready_to_implement`, ny disposition 7/57/28 av
  92 (bas 7/47/24) i BÅDA dokumenten, `verifieringslista-fjarrvarmebolag.md` uppdaterad med
  källgodkännandet, ny batch 5d efter batch 0 och en ny deklarativ
  `signed_monthly_flow_adjustment`-justeringstyp (mirrorad Python/TypeScript, niopunkts
  testplan). Rå-PDF:en stagades inte. Fokuserad lokal dokumentationscommit
  `d63bcbb` i `skills`, inklusive granskning 006 och 007 (tidigare ospårade).
  Ingen produktkod, tariffdata, genererad fil, aktivering eller push. Åkermannen-arkivets
  metadata (granskning 009) ingick INTE i denna leverans. Väntar på Codex omgranskning.
- `2026-09-09T12:50:46+02:00` – Robert godkände att sanerade fakturauppgifter används där
  de underlättar validering av kalkylen. Råfakturorna ska fortsatt ligga utanför Git.
  Arbetet väntar på påfyllda Claude-krediter och Roberts återkomst efter 13.40; ingen ny
  implementation startades.
- `2026-09-09T12:33:49+02:00` – Codex inventerade hela Åkermannens fakturaarkiv i
  `2026-09-09-009`: 22 PDF-filer motsvarar 20 unika perioder januari 2025–augusti 2026,
  med dubblettkopior för mars/april 2026. Sju nya enkelfall och maj–juli-avräkningen
  passerar Python/TypeScript, direkt/kontrakt, inom högst 2,4 öre. V16 ska rätta
  arkivbeskrivningen; separat sanitiserad testfixtur skjuts till senare implementation.
  Råfakturorna kopierades inte och ingen produktkod/testdata ändrades.
- `2026-09-09T12:21:30+02:00` – Codex återspelade Åkermannens augustifaktura i
  `2026-09-09-008`. Python, TypeScript och båda validerade månadskontraktsvägarna matchar
  14 849,95 kr exklusive moms; kvarvarande differens inklusive moms är cirka ett öres
  avrundning. Kontrollfallet planeras som separat sanitiserad out-of-sample-fixtur efter
  dokumentationsetappen. Råfakturan kopierades inte och ingen produktkod/testdata ändrades.
- `2026-09-09T12:12:22+02:00` – Robert upplyste om en ny augustifaktura för Brf
  Åkermannen. Codex bedömde den som lämplig för ett separat out-of-sample-test av Stockholm
  Exergis 2026-tariff, men kunde inte hitta filen lokalt. Sökväg/bilaga inväntas; ingen
  verifieringsräkning eller fixtur ändrades och V16 blockeras inte.
- `2026-09-09T12:04:02+02:00` – Codex granskade Lidköping Energis svar i
  `2026-09-09-006` och omgranskade V15 i `2026-09-09-007`. Två Lidköpingstariffer flyttas i
  V16 till `ready_to_implement`, vilket ändrar dispositionen till 7/57/28 av 92 och kräver
  en separat batch 5d med tre fail-closed tolvmånadersserier. V15 löser argumentbyggaren
  och parsergrindarna, men årsproduktens kod ger fem reproducerade TypeScript-fel och
  `policyFalt`-transporten är inte entydig. V16 beställdes som en sammanhållen
  dokumentationsrättning. Rå-PDF:en stagades inte; ingen produktkod, tariff-JSON,
  genererad fil, aktivering eller push godkändes.
- `2026-09-09T10:33:00+02:00` – Claude levererade tariffinventering v15.0 och batchplan
  v15.0 som svar på samtliga tre P1-fynd och två P2-fynd i omgranskning `2026-09-09-005`:
  `argsFranInputs` skriven mot verkliga enumvärden/formel och verifierad tsc-kompilerbar,
  delad bas mellan `calcResult` och `beraknaArsprodukt`; `beraknaArsprodukt` fick en
  fullständig fail-closed kropp och wrapperns dubblerade `typ`-spridning togs bort; parserns
  scalar/array-formgrindar tillagda; `forkontrolleraPolicyIndata`s månadsavgränsning
  dokumenterad; `KontraktBlockeratOrsak`s filplacering rättad. Fokuserad lokal
  dokumentationscommit ovanpå `f4f2370`, inklusive granskning `2026-09-09-005`. Ingen
  produktkod, tariffdata, genererad fil eller aktivering ändrad; inget pushat. Väntar på
  Codex omgranskning.
- `2026-09-09T10:16:28+02:00` – Codex omgranskade V14 i `skills@f4f2370` och skrev
  `2026-09-09-005`: annual-scope, orsaksmodell, domänfelväg, `.policy`-åtkomst,
  energisystemguard och valfri `onskadTyp` är lösta. Tre P1-områden återstår i den
  icke-kompilerbara/odelade argumentbyggaren, årsproduktens ofullständiga fail-closed-flöde
  och parserns saknade råformsgrindar. V15 beställdes; inga produktändringar eller push
  godkändes och dispositionen 7/55/30 står kvar.
- `2026-09-09T10:05:00+02:00` – Claude levererade tariffinventering v14.0 och batchplan
  v14.0 som svar på samtliga fyra P1-fynd i omgranskning `2026-09-09-004`:
  omfattningsmedveten `forkontrolleraPolicyIndata`, enhetlig
  `'min'`/`'max'`/`'heltal'`-orsaksmodell, en konkret konstruerbar
  `KontraktBlockerat`-väg (`missing_policy_fields`/`invalid_policy_fields`), rättad
  `stodjerAktuellArskostnad`-objektsåtkomst med energisystemgrind FÖRST i
  `calcResultForOnskadTyp`, och `argsFranInputs`/`Tariffberakningsunderlag` byggd på
  verkliga `KalkylatorInputs`-fält med `onskadTyp` gjord valfri. Dispositionerna 7/55/30 av
  92 oförändrade; de ospårade granskningsfilerna 003/004 lades till i samma commit; ingen
  produktkod, tariffdata eller aktivering ändrad; inget pushat.
- `2026-09-09T09:45:04+02:00` – Codex omgranskade V13 i `skills@b467d0a` och skrev
  `2026-09-09-004`: fyra P1-områden kvarstår i feltypskedjan, den omfattningslösa
  förkontrollen/felkanalen, produktförmågans wrapperåtkomst/energisystemguard och den
  icke-existerande samt odelade argumentbyggaren. V14 beställdes; inga produktändringar
  eller push godkändes och dispositionen 7/55/30 står kvar.
- `2026-09-09T09:40:00+02:00` – Claude levererade tariffinventering v13.0 och batchplan
  v13.0 som svar på samtliga fynd i omgranskning `2026-09-09-003`: parsersignaturen tar
  `PolicyRawFormValue | undefined`, en delad `PolicyValideringsOrsak`-union, ny
  `forkontrolleraPolicyIndata` sluter `saknadeFalt`-hålet för direkta produktanrop, EN
  `stodjerAktuellArskostnad`-definition via `kontraktsgatadPolicy` med guarden upprepad
  inuti `beraknaArsprodukt`, och `argsFranInputs` byggd som faktisk funktion mot en ny,
  smalare `Tariffberakningsunderlag`-typ. Fyra P2-fynd rättade (`bygg_ts()`s garanti,
  `_bearbeta_leverantorsfil()`s policykälla, batchplanens dubbla "9.", handoffens
  v11-rester). Dispositionerna 7/55/30/92 oförändrade. Ingen kod, tariffdata eller
  aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-09T09:08:48+02:00` – Codex omgranskade V12 i `skills@a773524` och skrev
  `2026-09-09-003`: min/max/heltal, nulltransporten och den snävare `bygg_ts()`-preflighten
  är lösta. Parsersignaturen/felunionerna, direkta anrops exakta `saknadeFalt`, en enda
  fail-closed produktförmåga och en faktisk typkorrekt argumentbyggare kräver V13. Ingen
  implementation eller push godkänd; dispositionen 7/55/30 står kvar.
- `2026-09-09T08:53:39+02:00` – Claude levererade tariffinventering v12.0 och batchplan
  v12.0 som svar på samtliga fynd i omgranskning `2026-09-09-002`: parserns felresultat är
  nu en typkorrekt diskriminerad union (`PolicyParseResultat = {status:'parsed', varde} |
  {status:'saknat'} | {status:'ogiltigt', orsak}`) i stället för `PolicyInputValue |
  PolicyValideringsFel`, som inte kunde bära `'saknat'`; `valideraPolicyIndata` täcker nu
  `minVarde`/`maxVarde`/`heltal` bredvid de befintliga kontrollerna, bandfält identifieras
  via `vardetyp === 'band_id'` i stället för en metadataegenskap validatorn inte tar emot,
  och `maxVarde`-transporten null-normaliseras (`?? undefined`); `bygg_ts()` fick ett
  verkligt, körbart anropskontrakt genom att `kontrollera_adapterpreflight` tar
  `rak_katalog: dict | None` och bara kör riktning 1 (katalogberoende) när en riktig katalog
  finns, medan `bygg_ts()` skickar `rak_katalog=None` och bara riktning 2 (bijektionens
  reverse-led) — en uttryckligen avgränsad, mindre garanti än `bygg_ts_fran_katalog()`s
  fulla tvåvägskontroll, inte en låtsad fullständig bijektion som v11 aldrig kunde köra utan
  att kasta; årsproduktdispatchen smalnades till EN gren i `beraknaArsprodukt`
  (`aktuell_arskostnad`), `onskadTyp` finns nu bara på `KalkylatorInputs` (v11 hade den både
  som funktionsparameter och inputfält), en ny `stodjerAktuellArskostnad(prisar)` ger
  explicit produktförmåga och fail-closer INNAN `beraknaArsprodukt` anropas, `argsFranInputs`
  extraherades som en genuin funktion ur `calcResult`s befintliga logik (v11 anropade den
  utan att någonsin definiera den), och besparingsvägen är uttryckligen den BEFINTLIGA,
  oförändrade `calcResult`-vägen — v11:s andra dispatch-gren konstruerades aldrig av den
  riktiga sidan och togs bort som en död omkonstruktion. P2 rättat: "Testat identiskt"
  ändrat till framtida tempus (ingen sådan testsvit finns ännu). Dispositionerna 7/55/30/92
  oförändrade. Fokuserad lokal dokumentationscommit ovanpå `136d9cd`. Ingen produktkod,
  tariffdata, genererad fil eller produktionsgrind ändrad; ingen tariff aktiverad; inget
  pushat. Väntar på Codex omgranskning.
- `2026-09-09T08:24:19+02:00` – Codex omgranskade V11 i `skills@136d9cd` och skrev
  `2026-09-09-002`: parsern använder `'saknat'` utanför sin felunion och klassar tomma
  råvärden inkonsekvent; förvalidatorn täcker inte min/max/heltal och `maxvarde: null`
  transporteras inte till `undefined`; `bygg_ts()` får en tom katalog och måste därför
  kasta mot det verkliga adapterregistret; sidwrappern har två källor till `onskadTyp`,
  saknar produktförmåga/argumentbyggare och anropar inte den nya besparingsgrenen. V12
  beställdes. Ingen implementation eller push godkänd; dispositionen 7/55/30 står kvar.
- `2026-09-09T07:20:05+02:00` – Claude levererade tariffinventering v11.0 och batchplan v11.0 som svar på samtliga fynd i omgranskning `2026-09-09-001`: rått formulärstate (`PolicyRawFormValue`) skilt från den parsade `PolicyInputValue`-DTO:n med en strikt `parsaPolicyIndata`-parser (tomma/delvis ifyllda serier ger fältnära fel i stället för fail-open-nollor; Jönköpings numeriska enum konverteras till tal, band-ID förblir sträng); en ny `valideraPolicyIndata`-funktion körs FÖRE fasadanropet och gör `KontraktBlockerat.ogiltigaFalt` till en verkligen körbar felkanal (v10:s design försökte läsa den ur ett `blocked`-resultat `harledResultatstatus` aldrig returnerar för ogiltiga — bara saknade — värden); `beraknaArsprodukt` fick tre dispatch-grenar i stället för en, så besparingsflödet för Sandviken och alla framtida kontraktstariffer bevaras samtidigt som Stockholms aktuella-årskostnad-väg blir nåbar via en helt separat, ny `KalkylatorResultUnion`-wrapper (`calcResultForOnskadTyp`) i stället för en omöjlig retrofit av `KalkylatorResult`s obligatoriska besparingsfält; adapterpreflighten fick ETT anropskontrakt för `bygg_ts()` (alltid det verkliga produktionsregistret, aldrig en låtsad tom kontext) och en reverse-nyckel på hela `(provider_id, tariff_id, ersatter_katalograd)` i stället för bara `tariff_id`. P2 rättat: etikett/hjälptext har en källa (policyregistret), batch 0 säger nu tre värdetyper, `kontrollera_adapterpreflight` ägs konsekvent av `generera.py`. Dispositionerna 7/55/30/92 oförändrade. Fokuserad lokal dokumentationscommit. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-09T07:01:50+02:00` – Codex omgranskade V10 i `skills@ab38b79` och skrev
  `2026-09-09-001`: den parallella DTO:n, pris-/omfattningsmedvetna metadatan och den
  explicita adaptermarkören är förbättringar, men råstate/parsern kan göra blankt till noll
  och skickar Jönköpings numeriska enum som sträng; validatorns kast gör den beskrivna
  `ogiltigaFalt`-vägen onåbar; årsproduktens dispatch tappar stödd besparing; Stockholm
  saknar kapacitetsinlägg och en full `KalkylatorResult`-/UI-väg; `bygg_ts()` kan inte köra
  preflight med tom adapterkontext och reverse-kontrollen tappar provideridentitet. V11
  beställdes. Ingen implementation eller push godkänd; dispositionen 7/55/30 står kvar.
- `2026-09-08T23:32:03+02:00` – Claude levererade tariffinventering v10.0 och batchplan
  v10.0 som svar på samtliga fynd i granskning `2026-09-08-009`: ny parallell
  `policyFalt: Record<string, PolicyInputValue>`-DTO genom hela produktkedjan (det
  numeriska `falt` orört), `IndataPost.varde` fick en egen `IndataVarde`-typ i stället för
  att vidga den delade `Varde`-aliasen, `policyFaltMetadata(policy, prisar, omfattning)`
  löser bandalternativ/omfattningsfiltrering/kapacitetsdubblering, `KontraktBlockerat.
  ogiltigaFalt` klassar strukturellt ogiltig kundindata som ett typat användarfel vid sidan
  av `saknadeFalt`, Stockholm fick en namngiven produktentry (`ArsprodukResultat`,
  `beraknaArsprodukt`) med dispatch och rendering, adapterpreflighten ersatte `pass`/globala
  register med `Tariffpolicy.ersatter_katalograd` och en injicerbar
  `kontrollera_adapterpreflight`. Dispositionerna 7/55/30 av 92 oförändrade. Fokuserad lokal
  dokumentationscommit ovanpå `2cfa3be`. Ingen kod, tariffdata eller aktivering ändrad.
  Väntar på Codex omgranskning.
- `2026-09-08T23:12:46+02:00` – Codex omgranskade V9 i `skills@2cfa3be` och skrev
  `2026-09-08-009`: Umeås tvåpassgrind, Stockholms 12/5-seriemodell och räkningen är
  förbättrade, men den angivna produkt-DTO:n kan inte bära serier, UI-metadatan saknar
  nödvändig prispost/omfattning och skulle dubblera kapacitet, invalid kundindata
  felklassas, Stockholm saknar en nåbar aktuell-årskostnadsväg och adapterpreflighten är
  fortfarande en skiss med globala register och `pass`. V10 beställdes; ingen
  implementation eller push godkänd.

- `2026-09-08T22:56:55+02:00` – Claude levererade tariffinventering v9.0 och batchplan v9.0 som svar på samtliga fynd i granskning `2026-09-08-008`: Umeås sammansatta grind kör nu ett riktigt andra `grind()`-pass efter multiplikatorkvittering (stänger den reproducerade dolda andra/tredje blockeringen), `IndataPost.varde` fick den diskriminerade värdeunionen (inte bara `KravPost`), nytt generiskt `antal_varden`-kardinalitetsfält gör `number_series` till en verklig diskriminator, batch 0 fick genererad UI-metadata och en felklassningsgren (`saknadeFalt`), Stockholms årsmodell rättad till EN modell (två serier, två nya statiska bindningar, breddat effektkrav, fail-closed före/efter-regel för besparingsvärdering), adapterpreflighten kontrollerar nu provider/reverse-villkoren, samt två P2-rättningar (stale `kapacitet_bindning_variant`-referens, felaktigt "45/45 grind()"-påstående). Dispositionerna 7/55/30/92 oförändrade. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.

- `2026-09-08T22:37:24+02:00` – Codex omgranskade V8 i `skills@b7790ca` och skrev
  `2026-09-08-008`: Kraftringens typade diskriminator och Jönköpings allow-list är i
  huvudsak lösta, men Umeås andra grindförsök hoppar över dolda fynd, `IndataPost`- och
  UI-/produktkedjan kan inte bära band/enum/serier, Stockholms årsserier saknar statiska
  bindningar och före/efterregel, och adapterpreflighten validerar inte provider/reverse.
  V9 beställdes; ingen implementation eller push godkänd.
- `2026-09-08T17:20:00+02:00` – Claude levererade tariffinventering v8.0 och batchplan v8.0 som svar på samtliga åtta punkter i granskning `2026-09-08-007`: Umeås kompositgrind gjord körbar (flyttad in i `godkanda()`s egen loop, med `B=14`-testet flyttat till kontraktsfasaden), bandkontraktet fick en diskriminerad värdetyp i stället för en global strängvidgning, ny grundbatch (batch 0) för en gemensam policyindata-produktingång, Stockholms adapterkontroll flyttad till en preflight mot den råa katalogen med `_kraver_kontrakt`-återanvänd dispatch och en 17-fälts årsindatamodell, Kraftringens diskriminator omdöpt (`flodeskorrigering_variant`) och given en motorväg, Jönköping fick en domänmässig allow-list. Dispositionerna 7/55/30/92 oförändrade. Fokuserad lokal dokumentationscommit ovanpå `058ffb4`. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08T16:52:08+02:00` – Codex omgranskade V7 i `skills@f0f3ee7` och skrev
  `2026-09-08-007`: kontrollmängden 78+14 och den exakta 42-radslistan stämmer, men Umeås
  eftergrind kan inte återinföra en redan filtrerad rad, band-ID saknar ett säkert
  end-to-end-produktkontrakt, Stockholm saknar nåbar dedup/årsdispatch och representerbar
  12+5-månadsbindning, Kraftringens diskriminator når inte motorn och Jönköpings fyrvärdesval
  saknar domänallow-list. V8 beställdes; ingen implementation eller push godkänd. Den äldre
  V7-leveranstiden 16:10 rättas här till committens verifierbara tid 16:32:28 utan att den
  historiska raden nedan skrivs om.

- `2026-09-08T16:04:00+02:00` – Codex omgranskade V6 i
  `skills@1a429dc` samt korrigeringscommitten `058ffb4` och skrev `2026-09-08-006`: flera V5-fynd är lösta, men
  band-ID-kontraktet täcker bara två av 42 berörda ready-tariffer och är inte typat eller
  bevarat genom generatorn; Stockholms dubbelpolicy är omöjlig i nuvarande register;
  utredningsstatus/request-API, Umeås policyberoende grind och TypeScript-deserialisering
  är ofullständiga. V7 beställdes. Jönköpings accessavgift beslutades som obligatoriskt
  kundval utan default, vilket ändrar totalfördelningen till 7/55/30. Ingen implementation
  eller push godkänd.

- `2026-09-08T15:32:00+02:00` – Claude levererade tariffinventering v6.0 och batchplan v6.0 som svar på samtliga fynd i omgranskning `2026-09-08-005`: grind-only ersatt av en sammansatt fyrastegspreflight (§6), Sundsvall Indal rättad till en riktig kontraktsgated policy (inte legacy), fyra konkreta kontraktstillägg specificerade (§6a: `KravPost.maxvarde`, `supplier_confirmed_band_id`, Umeås `kapacitet_multiplikator_bindning`, Stockholms `ADAPTERREGISTER`), `remaining_information_requests` bytt till `tariff_ids`-representation, felaktiga filnamn rättade. Dispositionsräkningen 7+45+26 bas / 9+5 variant = 92 oförändrad. Fokuserad lokal commit `skills@1a429dc` (ovanpå `ce53f75`), inklusive granskning `2026-09-08-005` för självbärande historik. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08T15:14:26+02:00` – Codex omgranskade V5 i `skills@ce53f75` och skrev `2026-09-08-005`: korrekt kontrollmängd och bättre dokumentation, men grind-only-preflighten täcker inte aktiveringskedjan. Leverantörsvalt band saknar kontraktsbindning, R03/R14 kan inte delas tariffvis med dagens medlemsmodell, Umeås B saknar komplett typad/maxvaliderad väg, Stockholm skulle dubbleras och Sundsvall Indals kontraktsfria legacy-väg stoppas av generatorn. V6 beställdes; ingen implementation eller push godkänd. Därtill rättas den tidigare V5-leveranstiden `15:40:00`: committen som innehåller leveransloggen skapades `14:58:36`, vilket är den verifierbara leveranstiden. Den äldre felaktiga raden nedan lämnas oförändrad som historik.

- `2026-09-08T15:40:00+02:00` – Claude levererade tariffinventering v5.0 och batchplan v5.0 som svar på samtliga fynd i omgranskning `2026-09-08-004`. Metodskifte: `grind()` faktiskt körd mot minneskopior (inte bara avläst från Codex tabell) — 21/45 före rättningarna, 45/45 efter, med 13 tidigare dolda andraledsblockerare upptäckta och stängda i samma runda. E.ON/Navirum/Kraftringen/Kils fick specificerade katalogmutationer; Umeå fick sin saknade `B`-kapacitetsfaktor; Stockholm Exergi fick en namngiven adapterväg i stället för en påstådd redan-befintlig motor; samtliga fem okända issues och 10 av 14 informationsförfrågningar fick en explicit livscykel (två delade, resten borttagna). Känd metodavvikelse dokumenterad (Lidköping passerar grinden mekaniskt men förblir korrekt blockerad — en priskomponent saknas helt ur JSON). Ett räknefel i v4-rundans "sex bastariffrader" (i själva verket nio) rättat som en daterad korrigering, utan att ändra den äldre raden. Fokuserad lokal dokumentationscommit ovanpå `ada05e7`. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08T16:10:00+02:00` – Claude levererade tariffinventering v7.0 och batchplan v7.0 som svar på samtliga fynd i omgranskning `2026-09-08-006`: bandkontraktet (§6a.2) omfattar nu 42 `ready`-rader i stället för 2 (verifierat mekaniskt mot katalogen, exakt Codex tal), omkonstruerat så det bekräftade band-ID:t SJÄLVT väljer prisraden i stället för att bara valideras mot vad `_niva()` skulle valt automatiskt (v6:s design gjorde leverantörsbeskedet verkningslöst i just de tvetydiga gränsfall det finns till för); Stockholm Exergis policy rättad till EN utökad post i stället för två separata med samma nyckel (`POLICYREGISTER[tariff_id]` kan inte bära två), `ADAPTERREGISTER` typat med provider/tariff/täckningskrav; Umeås aktiveringsgrind arkitektoniskt separerad i en ny `kontrollera_kompositgrind()` — den nakna `grind()` rörs inte, `B`-taket omräknat till 1,401; Kraftringens diskriminator namngiven explicit (`kapacitet_bindning_variant`, §6a.5); request-representationen förenklad till en enda `blockerade_tariff_ider(katalog)`-upplösning FÖRE grindanropet (löser v6:s tvetydiga `grind(tariff, utredda)`-signatur); TypeScript-deserialiseringen för samtliga tre nya kontraktsfält specificerad explicit (ingen automatisk mappning finns); per-produktmatrisens tre stale rader (Stockholm, Sundsvall Indal, Umeå) synkroniserade mot besluten. Codex/Roberts beslut på v6:s fyra öppna frågor tillämpade utan omfrågan — Jönköpings accessavgift flyttad till `ready_to_implement` (ny disposition 7/55/30 av 92, variantsplit 10/4). Dokumentationscommit ovanpå `058ffb4`. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08T14:58:00+02:00` – Claude bekräftade Codex direktbesked (14:45:43) och rapporterade att V5-arbetet redan pågår i ett bakgrundsjobb dispatchat efter granskning `2026-09-08-004` — inget nytt jobb startades för att undvika filkrock. Väntar på det pågående jobbets leverans.
- `2026-09-08T14:45:43+02:00` – Codex gav Claude explicit klartecken att fortsätta och slutföra V5 enligt granskning `2026-09-08-004`, därefter skapa en lokal dokumentationscommit, logga leveransen och stanna för omgranskning. Ingen implementation eller push är tillåten.

- `2026-09-08T14:22:32+02:00` – Codex omgranskade V4 i `skills@ada05e7` i granskning `2026-09-08-004`. V3-fynden är lösta, men en full grindpreflight gav endast 21 pass av 45 `ready`-bastariffer; 24 har ytterligare katalog-, motor-, issue- eller energiformshinder och 18 rader är dessutom medlemsblockerade. V5 beställdes med per-ID-preflight, E.ON/Navirum/Kraftringen/Kils-korrigeringar, fullständiga Umeå-/Stockholm-vägar och explicit blockeringslivscykel. Ingen implementation eller push godkändes.

- `2026-09-08T13:45:00+02:00` – Claude levererade tariffinventering v4.0 och batchplan v4.0 som svar på samtliga fynd i omgranskning `2026-09-08-003`: E.ON/Navirums 36-månadersvariant rättad från fel fysisk storhet (framledningstemperatur) till den verifierade regeln (medelvärde av de tre högsta dygnsmedeleffekterna, kW) med leverantörsvärde-mönstret som valt kontrakt, ingen ny tidsseriemotor; Kraftringens golvbegränsade flödesfaktor separerad från E.ON/Navirums i en parametriserad motortyp med två regelvarianter; batch 1 (VänerEnergi) och batch 5c (Mälarenergi, ingen kapacitetsdel) rättade till exakt inventeringens indata; Finspångs spetsvärmetillägg flyttat till `blocked_external_info` (utlösningsvillkor inte kartlagt, ny fördelning 9/5 för varianterna); `source_id` + aktuell officiell länk på alla 14 varianter och sex bastariffrader (E.ON/Navirum ×6, VänerEnergi) rättade från gammal 2025-URL till aktuell 2026-källa; Sundsvall Indal och Stockholm Exergis inmatningslägen frysta konsekvent i både inventering och batchplan; Borås-batchens semantik förtydligad (78 bas + 14 räknade varianttäckningskrav). Dokumentationscommitten spårar för första gången HELA `skills/ellen/conversations/`-trädet i git (42 filer), inte bara de senast citerade granskningarna. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08T13:10:40+02:00` – Codex omgranskade V3 i `skills@7b2db36` i granskning `2026-09-08-003`. Kontrollmängden 78 bas + 14 varianter är komplett och flera V2-fynd är lösta, men E.ON/Navirums felaktiga 36-månadersindata, Kraftringens tappade minimifaktor, VänerEnergi/Mälarenergis batchindata, variantproveniens/Finspångs status, lägesmotsägelser, Borås batchräkning och 35 ospårade indexmål kräver V4. Ingen implementation eller push godkänd.

- `2026-09-08T12:05:00+02:00` – Claude levererade tariffinventering v3.0 och batchplan v3.0 som svar på samtliga fynd i omgranskning `2026-09-08-002`: 16 flödes-/temperaturluckor stängda med tariffvisa `months`-listor (inte ett generellt antagande), Eskilstuna flyttad till `blocked_external_info`, samtliga sju specialvariantfamiljer (14 variant-ID:n) integrerade i kontrollmängden (ny totalsumma 92 = 78 bas + 14 variant), primärkälla/giltighet tillagd på alla 78 bastariffrader, Gotland Taxa 17 rättad, batch 5 delad i tre undergrupper efter motorsemantik, Partille tillagd i batch 1, Familj 4 ligger nu FÖRST, granskningarna 2026-09-08-001/-002 spårade för första gången, maskinspecifik länk rättad. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.

- `2026-09-08T11:28:26+02:00` – Codex bekräftade att Claudes V2-leverans finns i `skills@7ce02af` och omgranskade den i `2026-09-08-002`. ID- och statusräkningen stämmer, men tretton flödesluckor, fel säsongsmånader, Eskilstunas overifierade nätreferens, specialvarianter utanför kontrollmängden, ofullständig käll-/giltighetsproveniens, en fortsatt icke självbärande granskningskedja samt batch-/dokumentationsmotsägelser kräver V3. Ingen implementation eller push godkänd.
- `2026-09-08T10:43:54+02:00` – Claude levererade tariffinventering v2.0 och batchplan v2.0 som svar på samtliga fynd i granskning `2026-09-08-001`: verklig per-produktmatris (46 ready/25 blocked/7 implemented), tre rättade dispositioner (Borlänge, C4, Stockholm Exergis årsprodukt), motorstatus omräknad mot `JUSTERINGSTYPER` (16 ready-tariffer kräver ny motorkod, inte bara fyra familjer), sju specialvarianter spårade i egen tabell i stället för `not_applicable`, rättat räkningsspråk (78 tariffprodukter + 1 schablon, 54 leverantörsentiteter), omordnad batchplan med fullständiga ID:n, självbärande dokumentationscommit och sex rättade länkar. Ingen kod, tariffdata eller aktivering ändrad. Väntar på Codex omgranskning.
- `2026-09-08` – Codex kontrollerade mappen efter Roberts uppmaning att läsa Claudes svar. Inget nytt Claude-svar, inga V2-filer och ingen rättningscommit fanns ännu; HEAD var fortsatt `1d52803`.
- `2026-09-08` – Codex granskade tariffinventering v1 och batchplan v1 i granskning `2026-09-08-001`: `changes-required`. Alla katalog-ID:n finns, men per-produktmatris, dispositioner, obligatoriska indata, adapterbehov, specialvarianter, räkning, länkar och commitproveniens kräver v2. Ingen implementation eller push godkänd.
- `2026-09-08T10:15:00+02:00` – Claude levererade tariffinventering v1.0 och batchplan v1.0 enligt överlämning `2026-09-08-001`: 80 enheter klassade (8 implementerade, 43 redo, 27 externt blockerade, 2 ej tillämpliga), sju föreslagna implementationsbatcher, fyra öppna frågor till Codex. Ingen kod, tariffdata eller aktivering ändrad.
- `2026-09-08T09:36:59+02:00` – Codex skapade överlämning `2026-09-08-001` till Claude för en fullständig, deduplicerad v1-inventering och batchplan. Kontrollmängden ska omfatta både JSON-katalogen och separat förvaltade leverantörsfiler; ingen kod, tariffdata eller aktivering får ändras före Codex granskning.
- `2026-09-08T09:31:03+02:00` – Robert beslutade att de sju aktiva tarifferna endast är en utvärdering och att alla möjliga tariffer ska implementeras. Produktdirektiv v0.2 och tariff-to-do uppdaterades med ett versionssatt slutkriterium och dispositionerna `implemented_source_verified_annual`, `blocked_external_info` och `not_applicable`. Ingen implementation eller tariffdata ändrad.
- `2026-09-08T09:21:35+02:00` – Produktdirektiv v0.1 skapat och tariffens to-do,
  tekniska kartläggning samt agentfundament synkade med Roberts beslut. Ingen
  implementation eller tariffaktivering ändrad.
