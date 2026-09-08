# Tariffinventering v9.0 — fullständig kontrollmängd för kalkylator v1

Upprättad 2026-09-08 av Claude. Ersätter `tariffinventering-v8.md` i sin helhet (v8 ändras
INTE i efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-08-008](../conversations/reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v8.md)
(`status: changes-required`, supersedes `2026-09-08-007`) av v8. Ingen produktkod, tariffdata
eller genererad fil är ändrad av detta dokument. Alla kodpåståenden nedan är verifierade
genom att läsa (och, där möjligt, köra skrivskyddat) den verkliga koden i
`enkey-agents@fd8f8da`/`neptune_academy@f1df177` — bl.a. `grind()`s faktiska
kontrollordning (`post_multiplier` FÖRE `issues`/`okand_justering()`), `IndataPost.varde`s
nuvarande typ (`float | Sequence[float]`/`number | readonly number[]`), `rullande=True`s
faktiska semantik (tillåter serie, kräver den inte) och `bygg_ts_fran_katalog()`s
`godkanda(katalog)`-anrop utan policyregister — inte bara omskrivna från granskningen.

**Vad som är nytt i v9, i korthet** (se granskning `2026-09-08-008` för fullständig
motivering till varje punkt):

1. **Umeås sammansatta grind kör nu ALLA återstående kontroller, inte bara den första.**
   v8:s design lade bara till raden när `kontrollera_kompositgrind()` godkände
   multiplikatorbindningen, utan att sedan kontrollera om ett ANNAT fynd (`issues`,
   `okand_justering()`) låg dolt bakom multiplikatorfyndet — Codex reproducerade att Umeås
   verkliga katalograd bär `post_multiplier`, en okänd `issue` OCH okänd
   `asymmetric_flow_difference` SAMTIDIGT, och `grind()` returnerar bara det FÖRSTA fyndet
   (multiplikatorn, eftersom den kontrollen ligger tidigast). §6a.3 är omskriven: när
   multiplikatorbindningen är verifierad, körs `grind()` EN GÅNG TILL på en kopia av
   tariffen där ENDAST `post_multiplier`-fältet är neutraliserat — om den andra körningen
   fortfarande ger ett fynd (issue, okänd justering, m.m.) förblir raden blockerad. Endast om
   BÅDA passen ger `None` läggs raden till. `bygg_ts_fran_katalog()`/`main()` för nu samma
   explicita `policyregister`-argument till `godkanda()` som `kontrollera_aktiveringsgrind()`
   redan använder, så ett testregister och produktregistret inte kan divergera.
2. **`IndataPost`/värdeunionen är nu diskriminerad i båda språk, inte bara `KravPost`.**
   v8 lade `vardetyp` på `KravPost` men lämnade `IndataPost.varde` otypad för `band_id` och
   lämnade `number_series` som en icke-verklig diskriminator (`rullande=True` TILLÅTER en
   serie men KRÄVER den inte, så ett `number_series`-fält kunde fortfarande få ett skalärt
   tal). §6a.2 specificerar nu en genuint diskriminerad värdeunion med tvingande
   korsvalidering per `vardetyp`, plus ett nytt generiskt kardinalitetsfält
   `KravPost.antal_varden` för seriekrav — Stockholms 12/5-krav uttrycks nu deklarativt i
   stället för att förlita sig på att `rullande=True` råkar räcka.
3. **Batch 0 har nu en genererad UI-väg, inte bara en hjälpfunktion.** v8:s
   `byggIndataFranPolicy` fanns bara som en TypeScript-funktion utan någon källa till de
   band-/enum-/serieval den skulle mata — `KalkylatorPage.tsx` renderar i dag ALLA
   `indatafalt` som `type="number"`. §6a.2 lägger till ett genererat UI-metadatakontrakt
   (inmatningstyp, etikett, hjälptext, obligatoriskhet, tillåtna alternativ, seriekardinalitet)
   och skiljer explicit saknad/ogiltig kundindata från ett trasigt policykontrakt i
   `KontraktBlockerat`. Batch 0:s test är nu ett syntetiskt end-to-end-fall som faktiskt
   renderar, fyller och beräknar number + band-ID + enum + serie tillsammans.
4. **Stockholms årsmodell är nu EN modell, inte två motsägande.** v8 kallade modellen
   omväxlande "17 nya `KravPost`" och en tvåserielösning i olika stycken/dokument. §6a.4
   committar entydigt till TVÅ serie-`KravPost` (12-elements kallenergi, 5-elements
   returtemperatur), lägger de två saknade `Tariffpolicy`-bindningarna
   (`kallenergi_arsserie_bindning`/`returtemperatur_arsserie_bindning`) som pekar ut VILKEN
   validerad post som blir motorns `mwh_kallt_per_manad`/`returtemp_c_per_manad`, breddar det
   befintliga `monthly`-effektkravet till att även gälla `annual`, och definierar en
   fail-closed regel för hur kallenergin hanteras i besparingsberäkningens efterfall
   (oförändrad kallenergi kan annars ge en negativ normalenergi) — om ingen källmässigt
   försvarbar transformationsregel finns blockeras Stockholm från besparingsvärdering men kan
   fortsatt ge en uppskattad aktuell årskostnad.
5. **Adapterpreflighten verifierar nu den kedja den påstår sig bevisa.** v8:s pseudokod slog
   upp katalog-ID och målpolicy men använde aldrig `AdapterEntry.provider_id` och kunde inte
   bevisa den omvända regeln (policytäckning utan adapter). §6a.4 lägger till en verklig
   ett-till-ett-kedjekontroll (leverantör → prisårspost hos just den leverantören →
   tariff-ID → policy med krävd täckning) och en explicit omvänd regel i
   `_bearbeta_leverantorsfil()`.
6. **P2 rättat:** §10 (öppna frågor) hade fortfarande kvar det gamla, felaktiga fältnamnet
   `kapacitet_bindning_variant` i sin sammanfattning av Codex/Roberts beslut — bytt till det
   redan (i §6a.5) korrekta `flodeskorrigering_variant`. Commitproveniensen är rättad: v8
   levererades i `fd372a2`, direkt ovanpå `f0f3ee7` — INTE ovanpå `058ffb4` som en tidigare
   rundas sessionslogg/överlämning av misstag skrev. Verklig committid `2026-09-08T17:20:42`.
7. **Oförändrat från v8 (redan korrekt och återverifierat):** 78 katalog-ID:n, 14 variant-ID:n
   (10/4 efter Jönköping), 42-raders bandtabell, Borlänge/C4/Falus gränsfallsbugg, Lidköpings
   kända metodavvikelse, Kraftringens `flodeskorrigering_variant`-lösning, Jönköpings
   `tillatna_varden`-allow-list, dispositionerna 7/55/30/92 — inga nya produktbeslut från
   Robert krävs för dessa tekniska rättningar, per granskningens egen instruktion (punkt 7).

## Frusen kontrollmängd (proveniens)

| Källa | Version/commit | Antal produkter i denna inventering |
|---|---|---|
| `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` | `schema_version 0.1.3`, `skills`-repo commit `7ba9ec1b6245a72a4720f11b11beec6692af6196` (sha256 `a35fc95b741c6af9a3d1462dbd3e23c12577e2f1f1b75bd05b6ab6f484b52bcd`) | 78 katalograder (53 leverantörer) |
| `enkey-agents/skills/ellen/leverantor-stockholm-exergi.md` | fakturavaliderad mot 18 fakturor, Brf Åkermannen 33 (`monthly_invoice`-kontraktet, granskning `2026-09-06-003`) | Samma produkt som katalogens `stockholm-exergi-stockholm-exergi-normal-2026` — räknas EN gång, se §4 |
| `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md` | Nils Holgersson-rapporten 2025 | 1 syntetisk schablon, egen tabell §9 — inte ett tariffprodukt |

**Explicit utanför denna frusna version:** `Fjarrvarmetariffer/optimate-fjarrvarme-2027.json`
(prisår 2027, `skills`-repo commit `62181a1`, endast 2 av 53 medlemmar ifyllda hittills).
Nästa prisårs katalog är förvaltning av den färdiga produkten, inte en del av v1:s
slutkriterium — se [PROJECT_CHARTER §4](../PROJECT_CHARTER.md).

## 1. Metod och källhierarki

Denna inventering bygger på fyra redan granskade underlag i stigande detaljnivå:

1. [`verifieringslista-fjarrvarmebolag.md`](verifieringslista-fjarrvarmebolag.md) — Codex
   källgranskning av samtliga 78 katalograder mot leverantörernas 2026-underlag
   (2026-09-04). Ger käll-status per rad, och den exakta frågetexten för varje
   `blocked_external_info`-post (§4).
2. [`teknisk-kartlaggning-28-tariffer.md`](teknisk-kartlaggning-28-tariffer.md) v4 —
   Claudes tekniska analys av de 28 rader som hade fullständigt källunderlag även för
   månadsmodell, godkänd av Codex (`2026-09-04-006`). Auktoritativ där den och
   verifieringslistan motsäger varandra (Sundsvall Matfors, se §4).
3. `enkey-agents/tools/tariffer/justeringar.py` (`JUSTERINGSTYPER`, `okand_justering`)
   och `katalog.py` (`grind()`) — läst DIREKT ur koden för denna v2, inte antaget. Detta är
   den faktiska godkännandelistan: en katalograd vars `adjustments`-lista innehåller en typ
   som inte står i `JUSTERINGSTYPER` blockeras av `grind()` och kan inte aktiveras utan ny
   motorkod, oavsett om formeln i övrigt är helt källverifierad. v1 underskattade detta
   systematiskt (granskning `2026-09-08-001`, P1).
4. `enkey-agents/tools/tariffer/policyregister.py` — den faktiska kontraktsstatusen.

**Disposition per produkt** följer PROJECT_CHARTER §4:

- `implemented_source_verified_annual` — valbar i kalkylatorn i dag, årsverifierad.
- `ready_to_implement` — samtliga prisdelar och regler är källverifierade; återstående
  arbete är internt (katalogmappning, motorstöd för en känd men ej implementerad
  justeringstyp/kapacitetsform, eller produktintegration) — inget nytt leverantörsbesked
  krävs. Motorstatusen anger EXPLICIT om ny motorkod krävs (se §1 punkt 3 ovan).
- `blocked_external_info` — minst en materiell uppgift saknas, är tvetydig eller motsägs
  av källorna; kräver ett leverantörssvar eller ett nytt beslut innan implementation.
- `not_applicable` — inte ett tariffprodukt att implementera (schablonmekanism); används
  ALDRIG som uppskjutningsstatus för en känd, verklig produktvariant (se §5).

**Leverantörsvärde-mönstret (Sandviken-precedent):** när en tariffs debiterbara effekt/band
inte kan beräknas automatiskt av en fullständigt publicerad formel, men leverantören ändå
kan uppge/fakturera värdet, klassas tariffen ändå `ready_to_implement` — med det värdet som
obligatorisk, synlig användarindata, inte som en extern blockering. Codex har accepterat
mönstret i princip (granskning `2026-09-08-001`, svar på öppen fråga 3) men kräver en
tariffvis kontroll av VARJE kostnadspåverkande fält — inte bara kapacitetsdelen. §4 nedan
härleder fälten från samtliga prisdelar (kapacitet OCH `adjustments`), inte bara kapacitet.

## 2. Inmatningslägen — generell regel

Per [PROJECT_CHARTER §2](../PROJECT_CHARTER.md): ett inmatningsläge utan entydig,
verifierad modell blockeras, det gissas aldrig.

- **De sex legacy-tarifferna samt Riksgenomsnittet:** mwh, kr och schablon fungerar redan
  (ingen kontraktsgated obligatorisk indata).
- **`sundsvall-energi-indal-liden-och-lucksta-2026` (§4.1, batch 2):** samma som ovan — mwh,
  kr OCH schablon, eftersom den aktiveras via den befintliga `EJ_TILLAMPLIG_KAPACITETSFORM`-
  legacymekanismen och aldrig blir kontraktsgated (rättat i v4, granskning 2026-09-08-003,
  P2 — v3 tillämpade nästa punkts regel på den av misstag).
- **Sandviken och varje ÖVRIG `ready_to_implement`-tariff nedan (samtliga som blir
  kontraktsgated via `POLICYREGISTER`, inklusive Stockholm Exergis årsprodukt):** mwh-läge
  kräver den obligatoriska indatan; kr och schablon blockeras tills en egen, verifierad
  invers/schablonmodell byggs och godkänns separat — detta gäller ÄVEN under
  implementationen av respektive batch, inte bara efter. Ett nytt läge öppnas aldrig som ett
  beslut som "avgörs vid implementation".

## 3. Redan implementerade (7 produkter)


#### `goteborg-energi-goteborg-2026`
- **Leverantör / nät / kundkategori:** Göteborg Energi — Göteborg — näring/brf
- **Prisår/giltighet:** 2026, legacy-tariff sedan uppgift 7 (2026-09-03)
- **Primärkälla:** `goteborg-web` (https://www.goteborgenergi.se/foretag/fjarrvarme/fjarrvarmepriser)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** godkänd | **Katalogstatus:** legacy, `contract_required` ej satt | **Motorstatus:** klar (`temperature_difference`, redan i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated (legacy) | **Teststatus:** i generella regressions-/godkanda-sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja, redan i produktion
- **Obligatorisk indata:** Returtemperaturavvikelse har ett neutralt default (0 °C); ingen indata är formellt obligatorisk för legacy-vägen
- **Inmatningslägen:** mwh, kr, schablon — alla tre
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-17-under-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 17, under 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (ingen kapacitetsdel, `capacity: null`) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `10_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Geab-Prisdialogen-2025.pdf); `web-review-geab-final` (https://geab.se/wp-content/uploads/2026/01/Prislista-fjarrvarme-2026.pdf); `web-review-geab-model` (https://geab.se/fjarrvarme/priser/)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** ingen för mwh-läget. `foregaende_ars_mwh` krävs bara för kr-läget — inte som en `volume_discount`-justeringspost på DENNA katalograd (den har `adjustments: []`), utan för att välja rätt TARIFF (denna Taxa 17 vs. `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026`) baserat på föregående kalenderårs förbrukning, i den befintliga volymrabatt-bandvalslogiken i `fjarrvarme.ts`/`faktura.py` (granskning 2026-09-08-002, P2 — rättad beskrivning av en redan korrekt implementerad mekanism)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 21, över 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`cooling_deadband`, `volume_discount`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `10_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Geab-Prisdialogen-2025.pdf); `web-review-geab-final` (https://geab.se/wp-content/uploads/2026/01/Prislista-fjarrvarme-2026.pdf); `web-review-geab-model` (https://geab.se/fjarrvarme/priser/)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** föregående kalenderårs energi (volymrabatt); avkylning har neutralt default
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `halmstads-energi-och-miljo-halmstad-2026`
- **Leverantör / nät / kundkategori:** Halmstads Energi och Miljö — Halmstad — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (inga justeringar) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `12_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-HEM_2025.pdf); `web-review-hem-prices` (https://www.hem.se/foretag/fjarrvarme/avtal-och-priser); `web-review-hem-terms` (https://www.hem.se/globalassets/dokument/villkor-gallande-normalprislista_naringsidkare.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** ingen
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `molndal-energi-molndal-kallered-och-lindome-2026`
- **Leverantör / nät / kundkategori:** Mölndal Energi — Mölndal, Kållered och Lindome — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`volume`, kWh/dygn-kapacitetsform, redan stödd) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `24_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Molndal-Energi-2025.pdf); `web-review-molndal-final` (https://www.molndalenergi.se/hubfs/MolndalEnergi_Foretag_Prislista_Fjarrvarme_260101.pdf?hsLang=sv-se)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** flöde och högsta dygnsenergi har dynamiska gissningsdefault (`ar_gissning: true`) — kan anges för exakthet men är inte formellt obligatoriska
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `norrenergi-norrenergi-2026`
- **Leverantör / nät / kundkategori:** Norrenergi — Norrenergi — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`low_utilization`, `incremental_return_temperature`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `28_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Norrenergi-2025.pdf); `web-review-norrenergi-final` (https://www.norrenergi.se/media/livhhhgq/normalprislista-fj%C3%A4rrv%C3%A4rme-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** normalårskorrigerad energi och returtemperatur har dynamiska default (egen uppskattad förbrukning respektive 30 °C-tröskeln)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `sandviken-energi-sandviken-normal-2026`
- **Leverantör / nät / kundkategori:** Sandviken Energi — Helleverans — näring/brf
- **Prisår/giltighet:** 2026 | **Källstatus:** godkänd, granskning `2026-09-07-003` | **Katalogstatus:** `contract_required: true` | **Motorstatus:** klar (ingen kapacitetsdel utöver effekt) | **Kontraktsstatus:** `POLICYREGISTER`, `annual_forward`, `minvarde=3`/`heltal=True` | **Teststatus:** `test_sandviken_kontrakt.py`, `besparingsvardeSandviken.test.ts` | **UI-status:** valbar, pushad `origin/main`
- **Primärkälla:** `sandviken-2026-priser` (https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme.7681.html); `sandviken-2026-effektmodell` (https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme/saberaknasdineffekt.7682.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja, i produktion | **Obligatorisk indata:** debiterbar effekt (kW, fakturan), heltal ≥3 kW
- **Inmatningslägen:** mwh (obligatorisk effekt); kr och schablon blockerade (`unsupported_input_mode`/`missing_energy`/`invalid_energy`)
- **Disposition:** `implemented_source_verified_annual`

## 4. Per-produktmatris — samtliga 71 icke-implementerade tariffprodukter

En normaliserad post per unik tariff-ID (inte grupptext). 45 är `ready_to_implement` (§4.1),
26 är `blocked_external_info` (§4.2) — Eskilstuna flyttad från redo till blockerad i v3
(granskning 2026-09-08-002, P1: nätreferensen är inte verifierad, `ready` får inte vara
villkorat av en framtida extern verifiering). Fälten följer exakt vad överlämning `2026-09-08-001`
begärde: leverantör, nät, produkt, kundkategori, prisår/giltighet+källa, käll-/katalog-/
motor-/kontrakts-/test-/UI-status separat, årsreproducerbarhet, obligatorisk indata med
fyndplats, inmatningsläge, tariffamilj/adapter, kvarstående arbete, disposition.

### 4.1 Redo att implementera (45 produkter)


#### `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
- **Leverantör / nät / kundkategori:** Borås Energi och Miljö — Borås, Sjömarken, Sandared, Dalsjöfors, Fristad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `00_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Boras.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE — ny kapacitetsform `heterogeneous_bands` + optional_environmental_addon
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens prisgrupp (1–6) OCH `Wn` eller `Q` beroende på grupp (fakturan). Miljötillägget "Bra Miljöval" (31 SEK/MWh) är ett SYNLIGT KUNDVAL, inte automatiskt — måste bli ett explicit UI-alternativ (checkbox/produktval), annars måste det uttryckligen avgränsas bort tills UI-arbetet görs.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Borås — ny kapacitetsform + valfritt tillägg
- **Kvarstående arbete:** `heterogeneous_bands` (ny kapacitetsform) OCH `optional_environmental_addon` (ny justeringstyp, dessutom kräver kundvalsUI, inte bara ett fält) — v1 nämnde bara kapacitetsformen.
- **Disposition:** `ready_to_implement`


#### `borlange-energi-borlange-2026`
- **Leverantör / nät / kundkategori:** Borlänge Energi — Borlänge — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `borlange-web` (https://www.borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare)
- **Giltighet:** valid_from=2026-01-01, valid_to=2026-12-31
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effektgrupp (fakturan/avtalet) — automatisk gruppindelning vid gränsen (501 kW) BLOCKERAS. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara effektgruppen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (som Borås effektgrupp)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader (inget säsongsarbete krävs). `Tariffpolicy` med leverantörsvärde-krav OCH ett nytt obligatoriskt flödesfält.
- **Disposition:** `ready_to_implement`


#### `c4-energi-kristianstad-2026`
- **Leverantör / nät / kundkategori:** C4 Energi — Kristianstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `02_0` (https://www.prisdialogen.se/wp-content/uploads/2025/08/Prisandringsmodell-2026-C4-Energi.pdf); `web-review-c4-current` (https://c4energi.se/foretag/varmekyla/priservillkor.793.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effektgrupp (fakturan/avtalet) — automatisk gruppindelning vid gränsen (501 kW Borlänge, 500 kW C4) BLOCKERAS.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (som Borås effektgrupp)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Ingen ny motorkod. `Tariffpolicy` med leverantörsvärde-krav, samma mönster som redan godkända leverantörsvärde-tariffer. KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med den redan godkända issue-typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd leverantörens fakturavärde för bandval vid exakt 500 kW." Informationsförfrågan R05 (medlem `c4-energi`) TAS BORT — bolaget har bara denna enda tariff.
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Järfälla (bostäder).
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Järfälla (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Malmö (bostäder, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Malmö (övriga fastigheter, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Bjursås, Grycksbo, Sundborn, Svärdsjö — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `06_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Falu-Energi-och-Vatten.pdf); `web-review-falu-final` (https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — en av de 42 raderna). Automatisk bandval BLOCKERAS strukturellt via bandkontraktet. DESSUTOM `KravPost.maxvarde=500` (§6a.1 — publicerad prislista täcker bara till och med 500 kW, mekaniskt fail-closed över gränsen) OCH prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående) + bandkontraktet (§6a.2) + `KravPost.maxvarde` (§6a.1)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1 och P2/fail-closed-krav 6):** Ingen ny motorkod — `volume` gäller alla tolv månader. Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI. KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad ovanför 500 kW; publicerad prislista täcker endast till och med 500 kW — begränsa beräkningen till detta intervall, hantera högre effekt som specialavtal (fail-closed, ingen automatisk extrapolering över gränsen)." Informationsförfrågan R15 (medlem `falu-energi-vatten`, avgränsad till just ytterorterna >500 kW) TAS BORT ur `remaining_information_requests` — dess fråga täcks nu av den normaliserade issue-texten ovan. Falu-Falun (`falu-energi-vatten-falun-2026`) delar medlem men har ingen egen öppen fråga och berörs inte.
- **Disposition:** `ready_to_implement`


#### `falu-energi-vatten-falun-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Falun — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `06_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Falu-Energi-och-Vatten.pdf); `web-review-falu-final` (https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `finspangs-tekniska-verk-finspang-2026`
- **Leverantör / nät / kundkategori:** Finspångs Tekniska Verk — Finspång — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `07_1` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Normalprislista-Finspang-2025.pdf); `web-review-finspang-final` (https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE — ny kapacitetsform `piecewise_polynomial` + conditional_flow
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens P-värde (kapacitetsformelns bas), returtemperatur varje månad (°C, fakturan — avgör om `conditional_flow`s villkor >55 °C utlöses) OCH, när villkoret utlöses, MÅNADENS flöde i m³ (fakturan — multipliceras med 20 kr/m³). Spetsvärmetillägget (20 %) är en EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Finspång — ny kapacitetsform + ny motortyp
- **Kvarstående arbete:** `piecewise_polynomial` (ny kapacitetsform) OCH `conditional_flow` (ny justeringstyp, villkorad på månatlig returtemperatur) — TVÅ separata nya motordelar, större arbete än enbart kapacitetsformen som v1 angav.
- **Disposition:** `ready_to_implement`


#### `habo-energi-habo-2026`
- **Leverantör / nät / kundkategori:** Habo Energi — Habo — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `11_0` (https://www.prisdialogen.se/wp-content/uploads/2023/10/Prisandringsmodell-2025-Habo-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Åre, Järpen, Mörsil, Duved, Kall, Hallen, Krokom, Nälden, Föllinge — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Åre m.fl.).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-brunflo-och-opevagen-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Brunflo och Opevägen — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Brunflo/Opevägen).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-ostersund-froson-as-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Östersund, Frösön, Ås — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Östersund/Frösön/Ås).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jonkoping-energi-jonkoping-och-granna-2026`
- **Leverantör / nät / kundkategori:** Jönköping Energi — Jönköping och Gränna — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `16_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Jonkoping-Energi-2025-till-2026-Prisandringsmodell.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering, 3,7 SEK/m³) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1). Den avtalsberoende accessavgiften (0/10/25/50 kr/mån) ingår INTE i denna disposition — se specialvariant i §5.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader (inget säsongsarbete krävs). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI. Accessavgiften byggs INTE i denna delbatch.
- **Disposition:** `ready_to_implement`


#### `karlstads-energi-karlstad-2026`
- **Leverantör / nät / kundkategori:** Karlstads Energi — Karlstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `17_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-Karlstads-Energi-AB-20260101.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret
- **Kvarstående arbete:** `capacity.rate_period: month` — dela INTE årsavgiften med 12 automatiskt.
- **Disposition:** `ready_to_implement`


#### `kils-energi-kil-2026`
- **Leverantör / nät / kundkategori:** Kils Energi — Kil — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `18_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-fjarrvarme-i-Kils-Energi-AB-2025.pdf); `web-review-kil-vat` (https://kilsenergi.kil.se/download/18.1b9e2707199c916c9d91010c/1761112730710/Kils_Energi_normalprislista.pdf); `kil-user-supplied-pricelist` ((url saknas))
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi). KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1): samtliga fyra band har `fixed: null` — verifierat besked är att ingen separat fast avgift finns, så `fixed` sätts till `0` på alla fyra. Golden-test: ett handräknat helår med `fixed=0` ger samma årsbelopp som enbart `variable × band`. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "null i fast avgift betyder ej extraherad/separat angiven, inte verifierad noll" är den PRECISA varning `fixed:0`-rättelsen ovan besvarar — TA BORT issue-raden när `fixed:0` sätts, den är inaktuell efter rättelsen, inte en kvarstående öppen fråga.
- **Disposition:** `ready_to_implement`


#### `kraftringen-kraftringen-2026`
- **Leverantör / nät / kundkategori:** Kraftringen — Kraftringen — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `19_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Kraftringens-Prisandringsmodell-2025.pdf); `web-review-kraftringen-model` (https://www.kraftringen.se/brf/varme-och-kylalosningar/fjarrvarme/fjarrvarmepriser/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — en av de 42 raderna), debiterbar effekt (kW), förbrukningsvägd MÅNADSMEDEL-framledningstemperatur `Tf` (°C, fakturan/nätdata — formeln själv använder `Tf` varje månad, inte bara flödet) OCH flöde (m³, fakturan). Formeln `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)` känd (katalog) — GOLVBEGRÄNSAD, skild från E.ON/Navirums golvfria formel (§6a.5); Brunnshögs nätdel är en EGEN VARIANT, se särfallstabellen — endast ordinarie nät ingår här.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Kraftringen — samma parametriserade motortyp som E.ON/Navirum, med `flodeskorrigering_variant: "golvbegransad"` som explicit, typad diskriminator (§6a.5) — INTE härledd implicit från leverantörs-ID
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` som en parametriserad motortyp delad med E.ON/Navirum, med Kraftringens regelvariant explicit diskriminerad (§6a.5). Bör byggas i SAMMA batch/commit som dem. Bandkontraktet (§6a.2) tillkommer som ett separat obligatoriskt fält. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1): `fixed: null` och `rate_period: null` — verifieringslistan anger redan `fixed: 0`, `rate_period: "year"`; sätt båda explicit. Golden-test: ett handräknat helår bekräftar att kapacitetsdelen inte periodiseras om (year, ingen ×12), att `fixed=0` inte tillför en dold stående kostnad, OCH att golvet vid exakt `Tf=60` ger faktorn `0,2` (§6a.5). YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Nätavgränsning, effektprisperiod och flödeskorrektion behöver bekräftas..." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden.
- **Disposition:** `ready_to_implement`


#### `lulea-energi-lulea-2026`
- **Leverantör / nät / kundkategori:** Luleå Energi — Luleå — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `21_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Lulea-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–maj samt september–december (9 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–maj samt september–december (9 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, 2–4 lägenheter — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen kapacitetsdel. Fast årsavgift (katalog), energi (MWh, kund anger), säsongens verkliga flöde i m³, januari–april samt oktober–december (7 månader, katalogens egen `months`-lista) — fakturans flödesvärde, INTE härlett ur MWh×antagen ΔT.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Mälarenergi, ren energitariff (2–4 lgh)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** `volume`-justeringen finns i motorn men appliceras i dag på ett enda årsflöde, inte postens egen `months`-lista (jan–apr + okt–dec, INTE okt–apr). Kräver månadssemantik i faktura.py/fjarrvarme.ts innan aktivering. INFORMATIONSFÖRFRÅGAN R03 (medlem `malarenergi`) SKA DELAS, INTE TAS BORT: dess text ("Vilka nät hör sidans två olika tabeller till? Bekräfta fast avgift 2217/2117 för 25–79 kW samt sommarperiod/flödesvillkor") gäller uttryckligen `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026` och `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026` (båda `blocked_external_info`) — inte 2–4 lägenheter, som saknar kapacitetsdel helt och därmed ingen effekt-/fast avgifts-tvetydighet att lösa. Omskopa R03 till just de två övriga Mälarenergi-tarifferna. Grindtest: `grind()` på 2–4 lägenheter ska passera med tom `utredda`-mängd, medan de två övriga fortsatt ger `utreds (medlem)`.
- **Disposition:** `ready_to_implement`


#### `mjolby-svartadalen-energi-mjolby-2026`
- **Leverantör / nät / kundkategori:** Mjölby Svartådalen Energi — Mjölby — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `23_0` (https://www.prisdialogen.se/wp-content/uploads/2022/10/Prisandringsmodell-for-MSE-i-Mjolby-2025.pdf); `web-review-mjolby-final` (https://mse.se/foretag/fjarrvarme/priser)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Norrköping/Söderköping (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Norrköping/Söderköping (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Örebro/Kumla/Hallsberg (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Örebro/Kumla/Hallsberg (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `nevel-gimo-osterbybruk-och-osthammar-2026`
- **Leverantör / nät / kundkategori:** Nevel — Gimo, Österbybruk och Östhammar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `27_0` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Prisandringsmodell-2025-Nevel.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–april samt oktober–december (7 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–april samt oktober–december (7 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-angelholm-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Ängelholm normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt november–december (5 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt november–december (5 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt november–december (5 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt november–december (5 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg Totalvärme, central installerad före 2024 — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `ovik-energi-ornskoldsvik-2026`
- **Leverantör / nät / kundkategori:** Övik Energi — Örnsköldsvik — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `30_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Naringsfastighet-Ovik-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret
- **Kvarstående arbete (utökat i v5):** Katalogrättelse krävs FÖRE aktivering: `fixed: null`→0, `monthly_proration`→kalenderdagsviktning. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "null i fast avgift betyder ej extraherad/separat angiven, inte verifierad noll" TAS BORT när `fixed:0` sätts — den är den precisa varning rättelsen besvarar, inte en kvarstående öppen fråga.
- **Disposition:** `ready_to_implement`


#### `partille-energi-partille-2026`
- **Leverantör / nät / kundkategori:** Partille Energi — Partille — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `31_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Partille-Energi-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH returtemperaturavvikelse (`avvikelse_c`, °C — `temperature_difference`, redan i JUSTERINGSTYPER, formeln `energi_MWh×7×avvikelse`).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4-liknande — temperaturfält, redan stödd typ
- **Kvarstående arbete:** Ingen ny motorkod (samma indatafält som Göteborg/Södertörn). v1 utelämnade felaktigt detta obligatoriska temperaturfält för Partille.
- **Disposition:** `ready_to_implement`


#### `piteenergi-norrfjarden-och-sjulnas-2026`
- **Leverantör / nät / kundkategori:** PiteEnergi — Norrfjärden och Sjulnäs — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `pite-small` (https://www.piteenergi.se/fjarrvarme/priser-2-foretag/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt oktober–december (6 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt oktober–december (6 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `piteenergi-pitea-centrala-natet-2026`
- **Leverantör / nät / kundkategori:** PiteEnergi — Piteå centrala nätet — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `pite-central` (https://www.piteenergi.se/fjarrvarme/priser-foretag/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt oktober–december (6 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt oktober–december (6 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `skovde-energi-skovde-2026`
- **Leverantör / nät / kundkategori:** Skövde Energi — Skövde — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `35_0` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Skovde-Energi-prisandringsmodell-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `soderhamn-nara-soderhamn-taxa-11-och-12-2026`
- **Leverantör / nät / kundkategori:** Söderhamn Nära — Söderhamn företag, taxa 10–13 — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `36_1` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Normalprislista-Soderhamn-Nara-2025.pdf); `web-review-soderhamn-final` (https://www.soderhamnnara.se/sidor/fjarrvarme/foretagskunder/priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`
- **Leverantör / nät / kundkategori:** Södertörns Fjärrvärme — Södertörns Fjärrvärme — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `37_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-SFAB.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH temperaturavvikelse mot nätets returmedel (`avvikelse_c`, °C, fakturan — `temperature_difference`, redan i JUSTERINGSTYPER). Kundvald effekt med överuttagsavgift är EN EGEN VARIANT, se särfallstabellen — endast SFAB:s rekommenderade effekt ingår i denna disposition.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + temperaturfält
- **Kvarstående arbete:** `Tariffpolicy` (effekt) + befintligt `temperature_difference`-indatafält. Ingen ny motorkod för normalfallet.
- **Disposition:** `ready_to_implement`


#### `stockholm-exergi-stockholm-exergi-normal-2026`
- **Leverantör / nät / kundkategori:** Stockholm Exergi — Stockholm Exergi normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `stockholm-2026` (https://www.stockholmexergi.se/wp-content/uploads/2026/04/Normalprislista_fjarrvarme_2026-1.pdf); `web-review-stockholm-clarification` (https://www.stockholmexergi.se/wp-content/uploads/2025/09/Fortydligande-av-prisvillkor-2026.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** **RÄTTAT P1 (granskning `2026-09-08-006`) — katalograden AKTIVERAS INTE.** v6:s plan om ett namngivet grindundantag i `katalog.py` OCH en andra, separat `Tariffpolicy` för samma nyckel `stockholm-exergi-2026` var strukturellt omöjlig (`POLICYREGISTER` är `dict[str, Tariffpolicy]`, en andra post med samma nyckel skriver tyst över den första). Se §6a.4 för den vidtagna vägen: leverantörsfilens redan fakturavaliderade `stockholm-exergi-2026` får sin BEFINTLIGA policy UTÖKAD med `annual_forward`-täckning (inte duplicerad), och katalograden hoppas över via ett nytt, typat `ADAPTERREGISTER`. `grind()`/`katalog.py` rörs INTE — katalograden fortsätter korrekt visa `energiform` som avslagsorsak. Årsindata (kall energi 12 månader, returtemp nov–mar 5 månader, debiterbar effekt — samma tre fält och period-/upplösningskontrakt som `monthly_invoice`) är oförändrade jämfört med v5/v6.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Stockholm Exergi — en konsoliderad policy på leverantörsfilens `stockholm-exergi-2026` (§6a.4), ej Sandviken-mönstret, ej katalogaktivering
- **Kvarstående arbete (rättat i v7, §6a.4):** Berörda filer: `policyregister.py` (BEFINTLIGA `_stockholm_exergi_policy` utökas med `annual_forward` i `tackning` och ändamålsspecifika `kravs_for`, PLUS nytt `ADAPTERREGISTER: dict[str, AdapterEntry]`), `generera.py` (`bygg_ts_fran_katalog` läser `ADAPTERREGISTER`, hoppar över katalograden EFTER att ha verifierat att målpolicyn har `annual_forward`-täckning — kastar annars). `katalog.py` rörs INTE. Bygg ett eget källverifierat årsreferensfall för `annual_forward` (motsvarande Sandvikens granskningskedja `2026-09-06-004`→`2026-09-07-003`). Regressionstest: `monthly_invoice`-kontraktet och dess 18 fakturarader rörs inte och ger identiskt resultat före/efter tillägget. Katalogradens egen `issues`-text ("Förtydligande av prisvillkor 2026 finns...") är redan självlöst men irrelevant — raden aktiveras aldrig, oavsett issue-status.
- **Disposition:** `ready_to_implement` (via leverantörsfilen, INTE via denna katalograd — se §6a.4)


#### `sundsvall-energi-indal-liden-och-lucksta-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Indal, Liden och Lucksta — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen utöver energimängd (MWh).
- **Inmatningslägen:** **RÄTTAT P1 (granskning `2026-09-08-006`) — mwh ENDAST; kr och schablon BLOCKERAS.** v5/v6:s "alla tre lägen via legacy-vägen" var strukturellt fel: tariff-ID:t `sundsvall-energi-indal-liden-och-lucksta-2026` finns INTE i `LEGACY_UNDANTAGNA_TARIFF_ID` (verifierat: bara de sex ursprungliga uppgift-7-tarifferna står i den frozensetten) — `bygg_ts_fran_katalog()` hade KASTAT om tariffen byggts på legacy-vägen utan `contract_required`/policy. Den ska i stället kontraktsgatas med samma minimala mönster som Sandviken: `contract_required: true` + en `Tariffpolicy` med `capacity.type: not_applicable` (inga kapacitetsbundna krav). Kontraktsgated betyder MWh-only (§2:s generella regel), samma blockering av kr/schablon som alla andra `ready_to_implement`-rader.
- **Tariffamilj/adapter:** Ren energitariff — Sandviken-mönstret (minimal kontraktsgated policy, `capacity.type: not_applicable`), INTE legacy-vägen
- **Kvarstående arbete (rättat i v7):** Sätt `capacity.type: "not_applicable"` på katalograden. Mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp 1–4 (2026-09-04), bara inte aktiverad mot denna rad. Sätt `contract_required: true` och registrera en minimal `Tariffpolicy` i `policyregister.py` (inga kravda_falt utöver den vanliga MWh-energin) — samma mönster Sandviken redan bevisat i produktion, ingen ny mekanism. INFORMATIONSFÖRFRÅGAN R14 (medlem `sundsvall-energi`) FÅR `tariff_ids` satt till de två `blocked_external_info`-tarifferna (`sundsvall-energi-sundsvall-normal-2026`, `sundsvall-energi-matfors-och-kvissleby-normal-2026` — Matfors hålls blockerad per granskning 2026-09-08-003, följer teknisk-kartläggning v4) i stället för det medlemsomfattande `member_ids` (§7) — INTE Indal/Liden/Lucksta, som frågan uttryckligen inte gäller. Grindtest: `grind(tariff, blockerade_tariff_ider)` på Indal/Liden/Lucksta ska passera EFTER denna omskopning, medan Sundsvall-normal/Matfors fortsatt blockeras via sina egna tariff-ID:n i `blockerade_tariff_ider`.
- **Disposition:** `ready_to_implement`


#### `tekniska-verken-katrineholm-katrineholm-2026`
- **Leverantör / nät / kundkategori:** Tekniska Verken - Katrineholm — Katrineholm — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `40_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Katrineholm-AB-Linkoping-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `tekniska-verken-linkoping-linkoping-2026`
- **Leverantör / nät / kundkategori:** Tekniska Verken - Linköping — Linköping — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `41_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Linkoping-AB-Linkoping-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–april samt oktober–december (7 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–april samt oktober–december (7 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`
- **Leverantör / nät / kundkategori:** Telge Nät — Telge företag och bostadsrättsföreningar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `telge-attachment` (https://www.telge.se/foretag/fjarrvarme-energi/kundservice/fjarrvarmepris/); `telge-terms` (https://www.prisdialogen.se/wp-content/uploads/2020/11/TN-prislista-fjarrvarme-2025_Foretag.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan), normalårskorrigerad energi juli–juni (`normalarskorrigerad_energi_mwh`, MWh, begärs av leverantören — `low_utilization`) OCH returtemperatur (`returtemperatur_c`, °C, fakturan — `incremental_return_temperature`). Tre obligatoriska fält, inte ett.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + låg utnyttjning + returtemp
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Alla tre justeringstyper redan i JUSTERINGSTYPER. `Tariffpolicy` med tre bundna fält, ingen ny motorkod. KATALOGRÄTTELSE: `issues`-texten är en INAKTUELL kontrollpost — verifieringslistan bekräftar redan att 2025-bilagans tillsvidarevillkor fortsatt gäller 2026. TA BORT issue-raden helt (inte normalisera — frågan är redan besvarad, inte bara känd). Informationsförfrågan R11 (medlem `telge-nat`) TAS BORT ur `remaining_information_requests` av samma skäl.
- **Disposition:** `ready_to_implement`


#### `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`
- **Leverantör / nät / kundkategori:** TEMAB Fjärrvärme — Tierp, Karlholmsbruk och Örbyhus — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `43_0` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Prisandringsmodell-TEMAB-Fjarrvarme-AB-2025.pdf); `web-review-temab-final` (https://temab.tierp.se/download/18.7fa3d20319a7bbd966d1fe/1763023016779/Taxa%20f%C3%B6r%20Fj%C3%A4rrv%C3%A4rmeleveranser%202026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi). KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med den redan godkända issue-typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd leverantörens fakturavärde" — R12:s egen text medger redan att "annars räcker leverantörens debiterbara effekt". Informationsförfrågan R12 (medlem `temab-fjarrvarme`) TAS BORT — bolaget har bara denna enda tariff.
- **Disposition:** `ready_to_implement`


#### `trollhattan-energi-trollhattan-2026`
- **Leverantör / nät / kundkategori:** Trollhättan Energi — Trollhättan — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `44_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Trollhattan.pdf); `web-review-trollhattan-final` (https://www.trollhattanenergi.se/foretag/fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `umea-energi-umea-enkel-2026`
- **Leverantör / nät / kundkategori:** Umeå Energi — Umeå Enkel — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `45_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen_2025-Umea-Energi.pdf); `web-review-umea-terms` (https://a.storyblok.com/f/162274/x/bed500e2ec/prisvillkor-fjarrvarme.pdf); `web-review-umea-enkel` (https://www.umeaenergi.se/foretag/varme/priser/prisavtal-enkel)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (asymmetric_flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata (rättat i v7, §6a.2/§6a.3):** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — verifierat: raden har `band_selection` PLUS `post_multiplier` samtidigt, kräver BÅDA nya kontraktsfälten), debiterbar effekt (kW), flöde okt–apr (m³, fakturan, `asymmetric_flow_difference`), OCH kapacitetsfaktorn `B` — katalogens `post_multiplier` är en piecewise-formel av kvoten `U = normalårskorrigerad_energi_dec_jan_feb / energi_sep_apr`, men bolagets normalårskorrigering är INTE publicerad, så `U` kan inte räknas ut ur rå mätdata. Valt kontrakt: leverantörens EGET redan beräknade `B`-värde (fakturan/leverantörsbesked) tas emot som ett obligatoriskt leverantörsvärde — INGEN kalkylatorberäkning av `U`/`B` från energidata. `Tariffpolicy.kapacitet_bindning` binder `billing_basis` (leverantörens årseffekt), `Tariffpolicy.kapacitet_band_bindning` binder det bekräftade bandet, och `Tariffpolicy.kapacitet_multiplikator_bindning` binder `B` (intervall `[0,93; 1,401]`, §6a.3).
- **Inmatningslägen:** mwh (samtliga fält krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Umeå — ny motortyp `asymmetric_flow_difference`, bandkontraktet (§6a.2) OCH en arkitektoniskt separat `post_multiplier`-medveten kompositgrind (§6a.3, INTE en ändring av den nakna `grind()`)
- **Kvarstående arbete (rättat i v7):** (1) `asymmetric_flow_difference` finns INTE i JUSTERINGSTYPER — byggs separat från Vattenfalls blockerade variant av samma typnamn (Umeås formel är komplett och byggbar, Vattenfalls är det inte). (2) **RÄTTAT P1 (granskning `2026-09-08-006`):** den NAKNA `grind()` ändras INTE och fortsätter avvisa `post_multiplier` för alla tariffer. I stället körs en NY, separat `kontrollera_kompositgrind(tariff, policy)` (§6a.3) EFTER `grind()`, som bara godkänner `post_multiplier` när `policy.kapacitet_multiplikator_bindning` är satt och verifierad. (3) Handräknade testfall vid `B=0,93`, `B=1,401` (§6a.3s omräknade tak, inte det tidigare gissade `1,4`) och en punkt mellan brytpunkterna — testet heter `B-intervall`, inte "U-intervall", eftersom motorn aldrig räknar `U`. Ett negativt test för `B=14` ska blockera via kompositgrinden. (4) Bandkontraktet (§6a.2) läggs till som ett fjärde, separat obligatoriskt fält. (5) Katalogradens `issues`-text ("Hela effektkostnaden multipliceras med B...") är fullt löst av leverantörsvärdekontraktet ovan — TA BORT issue-raden.
- **Disposition:** `ready_to_implement`


#### `vanerenergi-mariestad-och-toreboda-2026`
- **Leverantör / nät / kundkategori:** VänerEnergi — Mariestad och Töreboda — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `46_0` (https://vanerenergi.se/fjarrvarme/priser-fjarrvarme-foretag-2026, PDF: https://vanerenergi.se/download/18.76bfc4fd19a0f6d5c0785f/1761289418005/Pris%C3%A4ndringsmodellen%20Mariestad%20T%C3%B6reboda%20%202026-2028.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH flöde (`flode_m3`, m³/år, fakturan — `volume`, gäller alla 12 månader för denna tariff, ingen `months`-begränsning).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + flöde
- **Kvarstående arbete:** `volume` redan i JUSTERINGSTYPER och tillämpar redan hela året för denna tariff (inga säsongsmånader att missa). `Tariffpolicy` med två bundna fält.
- **Disposition:** `ready_to_implement`

### 4.2 Blockerade av extern information (26 produkter)

Endast produkter där prisbestämningen själv är tvetydig, motsägs, eller där en obligatorisk
prisdel helt saknar publicerat värde. Frågan i sista fältet är den som ska skickas till
leverantören (ordagrant eller nästan ordagrant från verifieringslistan/teknisk-kartläggningen
— inte omformulerad här).


#### `eskilstuna-energi-och-miljo-eskilstuna-2026`
- **Leverantör / nät / kundkategori:** Eskilstuna Energi och Miljö — Eskilstuna — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `05_1` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Normalprislista-EEM-2025.pdf); `web-review-eem-price` (https://www.eem.se/foretag/fjarrvarme/priser/fjarrvarmepris-2026); `web-review-eem-model` (https://www.eem.se/foretag/fjarrvarme/priser/prismodell); `web-review-eem-flow` (https://www.eem.se/foretag/fjarrvarme/redan-fjarrvarmekund/flodestaxa)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad för formeln, men nätreferensen olöst (verifieringslistan 2026-09-04; granskning 2026-09-08-002, P1 — flyttad hit från `ready_to_implement`)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst (`network_flow_difference` skulle ändå krävt ny motorkod)
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej — formeln `(kundens_m3 − nätreferens_m3_per_MWh × kundens_MWh) × 4` är känd, men nätreferensen `monthly_mean_for_customers_covered_by_flow_tariff` är INTE ett statiskt katalogvärde och inte beskriven som en fakturapost kunden kan läsa av. Samma typ av blockering som Vattenfalls `asymmetric_flow_difference` (nätreferensen där är också "beräknad för aktuell månad", inte publicerad).
- **Exakt saknad uppgift/fråga:** Är nätets `monthly_mean_for_customers_covered_by_flow_tariff`-referens ett fast, publicerat värde per prisår (och i så fall vilket, och var står det), eller varierar det per faktisk kalendermånad? Om det varierar per månad: hur ska kunden hitta/verifiera det värde som gällde för sin faktura, månad för månad?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`


#### `gavle-energi-gavle-2026`
- **Leverantör / nät / kundkategori:** Gävle Energi — Gävle — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `08_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-naringsidkare-2025-Gavle-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas volymavdraget marginalt eller på hela månadens volym efter uppnådd nivå?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `harnosand-energi-miljo-harnosand-2026`
- **Leverantör / nät / kundkategori:** Härnösand Energi & Miljö — Härnösand — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `13_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista-flerbostadshus-2025-Harnosand.pdf); `web-review-hemab-final` (https://www.hemab.se/download/18.727ad6af19ac23cdb98120ae/1764247260203/Prislista%20flerbostadshus%202026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Prislistans räkneexempel (1750 MWh) motsäger den publicerade intervalltabellen — vilken är korrekt?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `hassleholm-miljo-hassleholm-2026`
- **Leverantör / nät / kundkategori:** Hässleholm Miljö — Hässleholm — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `14_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Hassleholm-2025.pdf); `web-review-hassleholm-model` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell); `web-review-hassleholm-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-hassleholm); `web-review-tyringe-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-tyringe)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas effektrabatten intervallvis eller på hela effekten?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `hassleholm-miljo-tyringe-2026`
- **Leverantör / nät / kundkategori:** Hässleholm Miljö — Tyringe — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `14_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Hassleholm-2025.pdf); `web-review-hassleholm-model` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell); `web-review-hassleholm-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-hassleholm); `web-review-tyringe-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-tyringe)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas effektrabatten intervallvis eller på hela effekten?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `lidkoping-energi-lidkoping-041-kw-2026`
- **Leverantör / nät / kundkategori:** Lidköping Energi — Lidköping 0–41 kW — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `20_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-2025-Lidkoping-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** 2026 års flödesprisfaktor N och nätmedelvärde Tm — helt saknade i 2026-underlaget.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `lidkoping-energi-lidkoping-42-kw-2026`
- **Leverantör / nät / kundkategori:** Lidköping Energi — Lidköping 42+ kW — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `20_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-2025-Lidkoping-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** 2026 års flödesprisfaktor N och nätmedelvärde Tm — helt saknade i 2026-underlaget.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, gruppanslutna småhus — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Samma frågor, plus om flödespremien alls gäller gruppanslutna småhus.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, större fastigheter — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Sommarperiodens avgränsning, överuttagsavgiftens debitering, flödesavgiftens sats över nätmedel; ny energiform (base_peak_summer).
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `skelleftea-kraft-boliden-burea-burtrask-byske-jorn-kage-lovanger-norsjo-robertsfors-stensele-storuman-vindeln-anaset-2026`
- **Leverantör / nät / kundkategori:** Skellefteå Kraft — Boliden, Bureå, Burträsk, Byske, Jörn, Kåge, Lövånger, Norsjö, Robertsfors, Stensele, Storuman, Vindeln, Ånäset — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `34_2` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista_Fjarrvarmepriser_FORETAG_Pelletsorter-2025-Skelleftea-Kraft.pdf); `web-review-skelleftea-final` (https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_kraftvarmeort_2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Samma, dimensionerande temperatur för Stensele.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `skelleftea-kraft-skelleftea-skelleftehamn-ursviken-lycksele-mala-2026`
- **Leverantör / nät / kundkategori:** Skellefteå Kraft — Skellefteå, Skelleftehamn, Ursviken, Lycksele, Malå — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `34_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista_Fjarrvarmepriser_FORETAG_Kraftvarmeorter-2025-Skelleftea-Kraft.pdf); `web-review-skelleftea-final` (https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_kraftvarmeort_2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Valutaenhet för energirabatten (Qnorm×A+B) samt dimensionerande temperatur för Ursviken.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `sundsvall-energi-matfors-och-kvissleby-normal-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Matfors och Kvissleby normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `network_m3_per_MWh` (nätreferens för flödesjusteringen) saknas helt som katalogdata — teknisk-kartläggning v4 överprövar verifieringslistans äldre ✅ här.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `sundsvall-energi-sundsvall-normal-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Sundsvall normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Hur får kunden nätvärdet Qalla/Walla för flödespremien varje månad (formeln i övrigt känd)? Blockera dessutom automatisk prissättning ≥2000 kW.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Gustavsberg – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Gustavsberg – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Haninge, Tyresö och Älta – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Haninge, Tyresö och Älta – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-motala-och-askersund-motala-och-askersund-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Motala och Askersund — Motala och Askersund – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `48_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Motala-och-Askersund-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-motala-och-askersund-motala-och-askersund-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Motala och Askersund — Motala och Askersund – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `48_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Motala-och-Askersund-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-nykoping-nykoping-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Nyköping — Nyköping – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `49_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Nykoping-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-nykoping-nykoping-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Nyköping — Nyköping – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `49_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Nykoping-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-uppsala-uppsala-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Uppsala — Uppsala – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `50_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Uppsala-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-uppsala-uppsala-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Uppsala — Uppsala – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `50_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Uppsala-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-vanersborg-vanersborg-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Vänersborg — Vänersborg – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `51_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Vanersborg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-vanersborg-vanersborg-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Vänersborg — Vänersborg – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `51_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Vanersborg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vb-energi-normal-2026`
- **Leverantör / nät / kundkategori:** VB Energi — Ludvika, Björnmossen, Grängesberg, Fagersta och Norberg — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `52_0` (https://www.prisdialogen.se/wp-content/uploads/2021/01/Prisandringsmodell-Vasterbergslagens-Energi-AB-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Effektperiod november–mars eller december–mars (två officiella källor motsäger varandra); vilket mät-/normalår och omprövningsdag styr prisgrupp; plus ny energiform (annual_volume_band_monthly).
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

## 5. Tariffvarianter — integrerade i den räknade kontrollmängden

Enligt granskning `2026-09-08-002` (P1): dessa sju kända variantfamiljer får INTE stå
utanför totalen längre. Var och en är nu en egen, räknad, stabil variant-ID i kontrollmängden
— ingen väntar på en "framtida inventeringsversion". `not_applicable` används aldrig för en
verklig, källkänd variant.

E.ON/Navirums 36-månadersmetod gäller samtliga åtta bastariffer separat — den räknas
därför som ÅTTA variant-ID:n (en per bastariff), inte en enda ospecificerad post, enligt
granskningens explicita krav på en modelleringsregel per bastariff.

**Rättat i v4 (granskning `2026-09-08-003`, P1):** E.ON/Navirums 36-månadersvariant beskrev
tidigare fel fysisk storhet (framledningstemperatur i stället för dygnsmedeleffekt) och fel
kontrakt. Verifieringslistans exakta regel (rad "E.ON - Järfälla", verifierad 2026-09-04):
*"För kunder där en annan värmekälla levererar bas- eller delvärme används i stället
medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste 36 månaderna, inklusive
fakturamånaden."* — detta är effekt (kW), inte temperatur. Flödeskorrigeringens
medelframledningstemperatur `Tf` är ett HELT SEPARAT fält som redan finns i bastariffens
huvuddisposition (§4.1, batch 3).

**Valt kontrakt (av två möjliga, se granskningens rättningskrav):** leverantörens egna,
redan beräknade debiterbara effekt tas emot som obligatorisk MÅNADSVÄRDESINDATA — SAMMA
leverantörsvärde-mönster som bastariffens huvudfall redan använder (huvudfallets
effektsignatur vid −15 °C är också ett leverantörsberäknat värde, inte en kalkylator-
regression). Kalkylatorn bygger INGEN egen tidsserie-/topp-tre-motor för 36 månader — det
vore en betydligt större motorinsats utan dokumenterad kund-/prospektprioritet. Resultatet
blir `noggrannhet: snapshot` (ett leverantörsvärde, inte en verifierad kalkylatorberäkning),
aldrig `exact` — samma klassificering som huvudfallet.

| Variant-ID | Bastariff | Källa | Vad den kräver | Obligatorisk indata | Inmatningsläge | Batch | Disposition |
|---|---|---|---|---|---|---|---|
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026--bas-delvarme` | `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) | 36-månadersmetoden för kunder med bas-/delvärmekälla i stället för fullvärme — leverantörens medelvärde av de TRE HÖGSTA DYGNSMEDELEFFEKTERNA (kW) senaste 36 månaderna inkl. fakturamånaden (verifieringslistan) | Debiterbar effekt (kW, fakturan — leverantörens 36-månadersberäkning, samma fält som huvudfallet men annan beräkningskälla), medelframledningstemp `Tf` (°C, fakturan, hör till den separata flödeskorrigeringen) OCH flöde (`flode_m3`, m³, fakturan) — SAMMA tre fält som bastariffens huvuddisposition | mwh; kr/schablon blockerade | 3b (efter batch 3) | `ready_to_implement` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026--bas-delvarme` | samma, övriga fastigheter | `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `e-on-malmo-malmo-och-burlov-bostader-2026--bas-delvarme` | samma, Malmö/Burlöv bostäder | `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026--bas-delvarme` | samma, övriga fastigheter | `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026--bas-delvarme` | samma | `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026--bas-delvarme` | samma | `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026--bas-delvarme` | samma | `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026--bas-delvarme` | samma | `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026--kundvald-effekt` | `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | `sfab-prislista-2026` (https://sfab.se/media/33mnnexa/prislista-normal-2026.pdf) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 | Kundvald effekt (i stället för SFAB:s rekommenderade) med egen överuttagsavgift; formeln är inte kartlagd i detalj och skiljer sig från katalogschemats `capacity_overrun`-typ | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken exakt formel/sats gäller för överuttagsavgiften vid kundvald effekt, och skiljer den sig från standardschemats `capacity_overrun`?" |
| `kraftringen-kraftringen-2026--brunnshog` | `kraftringen-kraftringen-2026` | `19_0` (https://www.kraftringen.se/brf/varme-och-kylalosningar/fjarrvarme/fjarrvarmepriser/) | Brunnshögs egen nätdel/prisstruktur, inte kartlagd — bara ordinarie nät är verifierat i §4.1 | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken är Brunnshögs egen prislista/formel, och skiljer den sig från Kraftringens ordinarie nät?" |
| `tekniska-verken-linkoping-linkoping-2026--lagtemperatur` | `tekniska-verken-linkoping-linkoping-2026` | `41_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Linkoping-AB-Linkoping-2026.pdf) | Lågtemperaturleveransens egen tariffstruktur, inte kartlagd i detalj | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken är lågtemperaturleveransens fullständiga prisstruktur (kapacitet, energi, ev. justeringar)?" |
| `finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg` | `finspangs-tekniska-verk-finspang-2026` | `web-review-finspang-final` (https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 (v4 citerade av misstag 2025-dokumentet) | Spetsvärmetillägget (20 %) — det procentuella villkoret är källkänt, men VILKA kunder/perioder som utlöser tillägget och om 20 % gäller samtliga prisdelar (effekt, energi OCH flöde, eller bara en delmängd) är INTE mappat mot en entydig kund-/avtalsregel. Detta strider mot `ready`-definitionen (samtliga regler verifierade, inget nytt besked krävs) — flyttad till blockerad i v4 (granskning 2026-09-08-003, P1) | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilka kunder/perioder utlöser spetsvärmetillägget på 20 %, och gäller procentsatsen samtliga tre prisdelar (effekt, energi, flöde) eller bara en delmängd?" |
| `jonkoping-energi-jonkoping-och-granna-2026--accessavgift` | `jonkoping-energi-jonkoping-och-granna-2026` | `16_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Jonkoping-Energi-2025-till-2026-Prisandringsmodell.pdf) | Avtalsberoende accessavgift — verifierade värden 0/10/25/50 kr/mån, ett synligt, obligatoriskt kundval | Kundval i UI (radioknappar/dropdown, 0/10/25/50 kr/mån), inget standardvärde — okänt/tomt val BLOCKERAR beräkningen | mwh; kr/schablon blockerade (som bastariffen) | Samma batch som Jönköpings bastariff (§8 batchplan) | `ready_to_implement` — **beslut fattat av Codex/Robert i granskning `2026-09-08-006`:** en fakturerbar, källkänd och kundkänd avtalsuppgift ska kunna ingå som ett synligt obligatoriskt val. Ingen dubblettprodukt exponeras. |
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026--miljotillagg` | `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | `borasem-2026` (https://borasem.se/webb/foretag/fjarrvarme/priserochvillkor2026.4.3b2618bc1976272a99c471fd.html) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 | Miljötillägget "Bra Miljöval" (31 SEK/MWh) — ett kundvalt UI-tillval, inte en automatisk prisdel | Kryssruta/kundval i UI, inget nytt fält utöver bastariffens | mwh; kr/schablon blockerade | 6 (samma batch som grundformeln — se §8:s räkningsnot om hur denna variant räknas separat trots att den byggs i samma commit) | `ready_to_implement` |

**14 variant-ID:n totalt, rättat i v7 (Codex/Roberts beslut i granskning `2026-09-08-006`):**
10 `ready_to_implement` (åtta E.ON/Navirum-varianter, Borås tillägg, Jönköpings accessavgift
— flyttad från blockerad), 4 `blocked_external_info` (Södertörn, Kraftringen Brunnshög,
Tekniska Verken Linköping lågtemperatur, Finspångs spetsvärmetillägg).

## 6. Sammansatt aktiveringspreflight — samtliga 45 `ready`-ID:n (granskning 2026-09-08-005/-006/-007, P1)

En bar `grind()`-körning bevisar bara STEG 2 av en riktig aktivering. `grind()` har inget
policyregisterparameter, ingen kännedom om `contract_required`, ingen adapterregistrering,
och ingen åtkomst till leverantörsvalt band eller Umeås framtida multiplikatorbindning
(bekräftat genom att läsa signaturen `grind(tariff: dict, utredda: set[str]) -> str | None`
i `katalog.py` — bara två argument, ingen policy). Ett `grind() is None`-resultat kan alltså
inte i sig bevisa att `bygg_ts_fran_katalog()` (generatorn) faktiskt kommer producera en
selectable rad i kalkylatorn.

**De fyra verifierbara stegen i den sammansatta preflighten:**

1. **Utrednings-/request-status — konkret mutation, inte bara "inte utreds":**
   `investigation.status: "utreds"` → `null` (mekaniskt verifierat: 45/45 rader har i dag
   `"utreds"`, 0/45 har `contract_required` satt) SAMTIDIGT som `contract_required: true`
   sätts för var och en av de 44 katalograder som faktiskt aktiveras (Stockholms
   katalogdubblett förblir explicit `"utreds"`/blockerad, se §6a.4 — den 45:e raden aktiveras
   aldrig via katalogvägen). Detta ÄR den tariffvisa mutationen v6 bara beskrev som ett krav
   utan att namnge den. Samtidigt: tariffens ID får inte längre finnas i
   `blockerade_tariff_ider(katalog)` (§7, den nya sammanslagna `tariff_ids`/`member_ids`-
   upplösningen).
2. **`grind(tariff, blockerade_tariff_ider)` → `None`** — den strukturella kontrollen i
   `katalog.py`, med signaturens andra argument bytt (§7) från medlems-ID-mängden `utredda`
   till en förberäknad tariff-ID-mängd `blockerade_tariff_ider(katalog)`. Grindens jämförelse
   blir därmed `tariff.get("id") in blockerade` — en enda, entydig strängjämförelse, i
   stället för v6:s tvetydiga `grind(tariff, utredda)`-signatur som inte kunde skilja
   tariff-ID:n från medlems-ID:n (granskning `2026-09-08-006`, P1).
3. **Generatorns kontraktsgrind** — `kontrollera_aktiveringsgrind(tariff_id,
   contract_required, register=POLICYREGISTER)` (`policyregister.py`) måste returnera en
   giltig `Tariffpolicy`, VERIFIERAT LÄST: en katalogtariff utanför de sex
   `LEGACY_UNDANTAGNA_TARIFF_ID` MÅSTE ha `contract_required: true` OCH en registrerad,
   komplett policy — annars `raise`:er `bygg_ts_fran_katalog()` i stället för att generera
   en tom rad. Detta steg saknades helt i v5:s tabell.
4. **Ett minimalt giltigt `annual_forward`-anrop** — `beraknaArskostnadMedKontrakt`/
   `berakna_arskostnad_med_kontrakt` med policyns kravda_falt ifyllda av rimliga
   leverantörsvärden ska returnera `status.fullstandighet == "complete"`, inte `"blocked"`.

**Resultat, steg för steg, mot den verkliga katalogen/koden (`enkey-agents@fd8f8da`,
`neptune_academy@f1df177`, skrivskyddat — inget ändrat):**

- **Steg 1+2 (grind-nivå):** FÖRE alla rättningar: 21/45 passerar. **Rättat P2 (granskning
  `2026-09-08-008`):** "45/45 passerar `grind()`" är FEL som ett påstående om den NAKNA
  grinden — Stockholm stoppas fortsatt av `utreds`/`energiform` (den aktiveras aldrig via
  katalogvägen, §6a.4) och Umeå ger fortsatt `"kapacitetsformel med multiplikator"` i den
  nakna grinden (bara den sammansatta `godkanda()`-loopen, §6a.3, kan öppna den raden). Rätt
  beviskedja EFTER v5–v9:s katalog-/motor-/kontraktsrättningar: **43 rader passerar den
  NAKNA `grind()` direkt + Umeå passerar via den sammansatta `godkanda()`-loopen (§6a.3) =
  44 katalogaktiveringar, PLUS Stockholm via en separat leverantörsfilsadapter (§6a.4) = 45
  `ready`-bastariffer totalt.** Detta är ENDAST steg 2 av 4 för de 44 katalograderna — samma
  resultat v5 redan visade för grindnivån, nu korrekt uppdelat i stället för felaktigt
  sammanslaget till en enda "45/45"-siffra.
- **Steg 3 (generatorns kontraktsgrind):** samtliga 45 saknar I DAG en registrerad
  `Tariffpolicy`. `POLICYREGISTER` innehåller i verkligheten TRE poster — Stockholm Exergi
  2025, Stockholm Exergi 2026 och Sandviken; de sex ÖVRIGA redan implementerade
  legacy-produkterna (Göteborg, Gotland ×2, Halmstad, Mölndal, Norrenergi) har INGEN policy
  alls, eftersom de aktiverades före resultatkontraktet fanns och står i
  `LEGACY_UNDANTAGNA_TARIFF_ID`. **Rättat P2 (granskning `2026-09-08-007`, motsade tidigare
  sin egen §6a.4):** slutsatsen är INTE att alla 45 kräver en ny registerpost — Stockholm
  Exergis rad aktiveras inte via katalogvägen alls (§6a.4) och dess ANNUAL-täckning läggs på
  den REDAN BEFINTLIGA `stockholm-exergi-2026`-policyn som en utökning. Rätt räkning: **44
  katalograder kräver EN NY policyregisterpost vardera + 1 (Stockholm) kräver en UTÖKNING av
  en befintlig post.** Detta gäller ÄVEN de 38 av de 42 bandraderna (§6a.2, exklusive
  Stockholm) som inte behöver ytterligare motorarbete, vilket tidigare rundor förväxlade med
  "ingen ny policy krävs". `sundsvall-energi-indal-liden-och-lucksta-2026` är INTE i
  `LEGACY_UNDANTAGNA_TARIFF_ID` (verifierat: bara de sex ursprungliga uppgift-7-tarifferna
  finns i den frozensetten) — v5:s batch 2 hade fått `bygg_ts_fran_katalog()` att kasta om
  den byggts. Sundsvall Indal behöver samma minimala policymekanism som Sandviken
  (`contract_required: true` + en `Tariffpolicy` med `capacity.type: not_applicable`, inga
  kapacitetsbundna krav) — inte legacy-vägen.
- **Steg 4 (minimalt annual_forward-anrop):** kräver att varje rads `Tariffpolicy` faktiskt
  binder ett giltigt, källverifierat leverantörsvärde för samtliga `kravda_falt`. Detta
  steg är i dag OTESTAT för alla 45 — inget skript kördes mot fasaden i denna runda
  eftersom det förutsätter policyregisterposter som ännu inte finns (steg 3). Flaggat
  explicit som ÅTERSTÅENDE arbete i implementationsfasen, inte påstått klart. **Rättat P1
  (granskning `2026-09-08-007`):** ett fälts NUMERISKA gränsvärdestest (t.ex. Umeås
  `B=14`-fall) hör hemma HÄR — i `harled_resultatstatus`/kontraktsfasaden, via `minvarde`/
  `maxvarde` på den bundna `KravPost` — eftersom bara steg 4 faktiskt har en riktig
  `IndataPost` att validera. Steg 3 (den statiska aktiveringsgrinden/`kontrollera_
  kompositgrind`) kan bara bevisa att en BINDNING är deklarerad, aldrig att ett framtida
  KUNDVÄRDE kommer vara giltigt — de två kontrollerna är åtskilda med avsikt, se §6a.3.

**Kontraktstillägg krävda innan steg 3–4 kan bevisas för VISSA rader** — se §6a för den
fullständiga specifikationen:

| Tariff-ID/grupp | Saknat kontraktselement | Se §6a |
|---|---|---|
| **42 rader** — samtliga `ready`-rader UTOM Finspång, Mälarenergi 2–4 lgh och Sundsvall Indal (verifierat mekaniskt mot katalogens `capacity.band_selection`, exakt Codex tal) | `supplier_confirmed_band_id`-bindning: bandvalet ska SJÄLVT peka ut prisraden — `_niva()`s automatiska intervalltolkning får aldrig överpröva ett bekräftat band-ID. Full 42-radslista, mekanism och per-band-ID-data i §6a.2. | 6a.2 |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` (en av de 42) | DESSUTOM `KravPost.maxvarde` (500 kW-tak; dagens `KravPost` har bara `minvarde`/`heltal`) — bandkontraktet ensamt räcker inte för Falu ytterorter eftersom källan helt saknar ett publicerat band över 500 kW | 6a.1 |
| `kraftringen-kraftringen-2026` (en av de 42) | DESSUTOM en explicit, typad regelvariant-diskriminator (parametriserad motortyp, inte implicit härledd från leverantörs-ID) — golvbegränsad faktor skild från E.ON/Navirums golvfria formel | 6a.5 |
| `umea-energi-umea-enkel-2026` (en av de 42 — verifierat, har BÅDE `band_selection` och `post_multiplier`) | DESSUTOM namngiven `kapacitet_multiplikator_bindning` för `B`, min/max `[0,93; 1,401]`, egen aktiveringsgrind skild från den strukturella | 6a.3 |
| `stockholm-exergi-stockholm-exergi-normal-2026` (en av de 42 — verifierat, katalograden har `band_selection`, men `energiform` stoppar den strukturellt FÖRE bandkontrollen ens nås) | Bandkontraktet är MOOT för denna rad — den EXKLUDERAS explicit från katalogaktivering, se §6a.4 för vald väg (en konsoliderad policy på leverantörsfilens `stockholm-exergi-2026`, inte katalogaktivering) | 6a.4 |
| Övriga 38 av de 42 band-rader | Bandkontraktet (6a.2) + en ny `Tariffpolicy`-post (steg 3) — inget ytterligare nytt kontraktsfält | 6a.2 |
| `finspangs-tekniska-verk-finspang-2026`, `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`, `sundsvall-energi-indal-liden-och-lucksta-2026` | De enda 3 av 45 UTAN `band_selection` — se respektive rads egna motorbehov i tabellen nedan (kapacitetsform/`not_applicable`-mekanism) | — |

**Per-tariffrad, dagens verifierade läge:**

| Tariff-ID | Steg 1–2 idag | Planerad åtgärd (utöver ny policyregisterpost, steg 3) | Berörda filer |
|---|---|---|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | kapacitetsform | Ny kapacitetsform `heterogeneous_bands` + ny justeringstyp `optional_environmental_addon` (kundvalt UI-tillval) | `katalog.py` (grind), `justeringar.py` + inline i `fjarrvarme.ts`, `KalkylatorPage.tsx` |
| `borlange-energi-borlange-2026` | okänd issue (501 kW) | Normalisera issue; TA BORT R04 (§7); `supplier_confirmed_band_id`-bindning (§6a.2) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `c4-energi-kristianstad-2026` | okänd issue (500 kW) | Normalisera issue; TA BORT R05 (§7); `supplier_confirmed_band_id`-bindning (§6a.2) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | null i band | fixed:0, rate_period:month; TA BORT normaliserad issue; ny `supply_temperature_adjusted_flow`-motor; TA BORT R10 (§7) | katalog-JSON, `justeringar.py`/`fjarrvarme.ts`, `policyregister.py`, `remaining_information_requests` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | null i band | Samma som Järfälla bostäder | samma |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | null i band | Samma + Malmö/Burlöv −15→−8 °C rättelse (redan i v4) | samma |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | okänd issue (>500 kW) | Normalisera issue; `KravPost.maxvarde=500` (§6a.1); TA BORT R15 (§7) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `falu-energi-vatten-falun-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `finspangs-tekniska-verk-finspang-2026` | kapacitetsform | Ny kapacitetsform `piecewise_polynomial` + ny justeringstyp `conditional_flow` | `katalog.py`, `justeringar.py`/`fjarrvarme.ts` |
| `habo-energi-habo-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | okänd justeringstyp | Ny justeringstyp `flow_difference` | `justeringar.py`/`fjarrvarme.ts` |
| `jamtkraft-brunflo-och-opevagen-2026` | okänd justeringstyp | Samma | samma |
| `jamtkraft-ostersund-froson-as-2026` | okänd justeringstyp | Samma | samma |
| `jonkoping-energi-jonkoping-och-granna-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `karlstads-energi-karlstad-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `kils-energi-kil-2026` | null i band | fixed:0 på alla fyra band; TA BORT normaliserad issue | katalog-JSON |
| `kraftringen-kraftringen-2026` | null i band | fixed:0, rate_period:year; TA BORT normaliserad issue; delad `supply_temperature_adjusted_flow` MED golv (0,2) | katalog-JSON, `justeringar.py`/`fjarrvarme.ts`, `policyregister.py` |
| `lulea-energi-lulea-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `mjolby-svartadalen-energi-mjolby-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | null i band | Samma som E.ON | samma |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | null i band | Samma | samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-angelholm-normal-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-helsingborg-normal-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `ovik-energi-ornskoldsvik-2026` | null i band | fixed:0 på alla band, monthly_proration→kalenderdagsviktning (redan i v4); TA BORT normaliserad issue | katalog-JSON |
| `partille-energi-partille-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `piteenergi-norrfjarden-och-sjulnas-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `piteenergi-pitea-centrala-natet-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `skovde-energi-skovde-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `stockholm-exergi-stockholm-exergi-normal-2026` | energiform | **EXKLUDERAS från aktivering** — se §6a.4. Katalogdubblett av den redan verifierade leverantörsfilsposten `stockholm-exergi-2026`; ID-kollisionsrisken (`_stabilt_tariff_id` ger `stockholm-exergi-stockholm-exergi-normal`) gör att katalogvägen inte väljs i denna plan | `resultatkontrakt.py`/`.ts` (ny adapter på leverantörsfilssidan), `policyregister.py` (`ADAPTERREGISTER`) |
| `sundsvall-energi-indal-liden-och-lucksta-2026` | kapacitetsform | `capacity.type: "not_applicable"` (redan byggd mekanism, oaktiverad); NY minimal `Tariffpolicy` (Sandviken-mönstret, INTE legacy — tariff-ID:t finns inte i `LEGACY_UNDANTAGNA_TARIFF_ID`); TA BORT R14 (§7) | katalog-JSON, `policyregister.py`, `remaining_information_requests` |
| `tekniska-verken-katrineholm-katrineholm-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `tekniska-verken-linkoping-linkoping-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | okänd issue (inaktuell) | TA BORT issue helt (redan besvarad); TA BORT R11 (§7) | katalog-JSON, `remaining_information_requests` |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | okänd issue | Normalisera issue; TA BORT R12 (§7) | katalog-JSON, `remaining_information_requests` |
| `trollhattan-energi-trollhattan-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `umea-energi-umea-enkel-2026` | kapacitetsformel med multiplikator | Ny `post_multiplier`-medveten kapacitetsmotor; `kapacitet_multiplikator_bindning` för `B` (§6a.3); TA BORT normaliserad issue; ny `asymmetric_flow_difference` | `katalog.py` (grind), `faktura.py`/`fjarrvarme.ts`, `resultatkontrakt.py`/`.ts`, `policyregister.py` |
| `vanerenergi-mariestad-och-toreboda-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |

**Metodnot (bekräftad på nytt i v6):** att lösa den FÖRSTA grindorsaken avslöjar ibland en
ANDRA, tidigare dold bakomliggande orsak — 13 av de 45 raderna hade en YTTERLIGARE `okänd
issue`- eller `okänd justeringstyp`-blockering bakom den förstnämnda (t.ex. samtliga åtta
E.ON/Navirum-rader hade, utöver `null i band`, en andra issue-text om effektprisperiod/
flödeskorrigering). Tabellen ovan är uppdaterad för BÅDA leden.

**Känd avvikelse (Lidköping, INTE en del av de 45):** `lidkoping-energi-lidkoping-041-kw-2026`
och `-42-kw-2026` (`blocked_external_info`, §4.2) passerar MEKANISKT `grind()` (steg 2)
redan idag när `investigation.status` simuleras löst — deras `issues`-texter matchar redan
kända, godkända mönster. De förblir ändå korrekt blockerade: den publika källan saknar HELT
2026 års flödesprisfaktor N och nätmedelvärde Tm — ett verkligt prissättande fält som aldrig
kodats som en `adjustments`-post i katalogen och som varken `grind()` eller den sammansatta
preflighten strukturellt kan upptäcka utan att fältet finns i JSON. Detta visar att INGET av
de fyra stegen ensamt räcker — ett mänskligt omdöme om KÄLLANS fullständighet krävs alltid
utöver den maskinella kedjan.

## 6a. Kontraktstillägg som krävs (granskning 2026-09-08-005/-006/-007, P1)

Fyra nya bindningar krävs i policykontraktet innan de rader som är beroende av dem kan bevisa
steg 3–4 (§6). Samtliga speglar det redan etablerade mönstret från Sandvikens
`minvarde`/`heltal`-tillägg (samma session, tidigare runda) — generiska, deklarativa fält på
`KravPost`/`Tariffpolicy`, kontrollerade av den delade fasaden i BÅDA språken, aldrig
hårdkodade mot ett enskilt tariff-ID i motorn.

### 6a.1 `KravPost.maxvarde` (mirror av `minvarde`)

Python (`resultatkontrakt.py`, `KravPost`): nytt fält `maxvarde: float | None = None`,
validerat i `__post_init__` (ändligt tal) och kontrollerat i `harled_resultatstatus` bredvid
den befintliga `minvarde`-kontrollen (`post.varde > f.maxvarde` → `raise ValueError`).
TypeScript-spegel: `maxVarde?: number` på `KravPost`-interfacet, samma kontroll i
`harledResultatstatus`. `_policy_till_json`/`dataclasses.asdict` behöver ingen ändring på
PYTHON-JSON-sidan — det nya fältet serialiseras automatiskt, precis som `minvarde`/`heltal`
gjorde för Sandviken.

**Rättat P1 (granskning `2026-09-08-006`):** TypeScripts `policyFranGenererad()`
(`resultatkontrakt.ts`) mappar KravPost-fälten FÖR HAND (verifierat genom att läsa
funktionen) — den läser i dag `minvarde`/`heltal` från den genererade JSON:en men INTE
`maxvarde`. Utan en explicit rad `maxVarde: k.maxvarde` i den mappningen skulle Falus
500 kW-gräns serialiseras korrekt av Python men tyst försvinna i frontend. Samma explicita
mappningsrad krävs för VARJE nytt fält i denna sektion — automatisk TypeScript-mappning
finns inte, den måste skrivas för hand varje gång:

| Python-fält (`KravPost`/`Tariffpolicy`) | JSON-namn (genererad fil) | TypeScript-fält | Krävd rad i `policyFranGenererad()` |
|---|---|---|---|
| `KravPost.maxvarde` | `maxvarde` | `KravPost.maxVarde` | `maxVarde: k.maxvarde` |
| `KravPost.vardetyp` (§6a.2) | `vardetyp` | `KravPost.vardetyp` | `vardetyp: k.vardetyp ?? 'number'` |
| `KravPost.antal_varden` (§6a.2, nytt granskning `2026-09-08-008`) | `antal_varden` | `KravPost.antalVarden` | `antalVarden: k.antal_varden ?? undefined` |
| `KravPost.tillatna_varden` (§6a.6) | `tillatna_varden` | `KravPost.tillatnaVarden` | `tillatnaVarden: k.tillatna_varden ?? undefined` |
| `Tariffpolicy.kapacitet_band_bindning` (§6a.2) | `kapacitet_band_bindning` | `Tariffpolicy.kapacitetBandBindning` | `kapacitetBandBindning: json.kapacitet_band_bindning ?? undefined` |
| `Tariffpolicy.kapacitet_multiplikator_bindning` (§6a.3) | `kapacitet_multiplikator_bindning` | `Tariffpolicy.kapacitetMultiplikatorBindning` | `kapacitetMultiplikatorBindning: json.kapacitet_multiplikator_bindning ?? undefined` |
| `Tariffpolicy.flodeskorrigering_variant` (§6a.5) | `flodeskorrigering_variant` | `Tariffpolicy.flodeskorrigeringVariant` | `flodeskorrigeringVariant: json.flodeskorrigering_variant ?? undefined` |
| `Tariffpolicy.kallenergi_arsserie_bindning` (§6a.4, nytt granskning `2026-09-08-008`) | `kallenergi_arsserie_bindning` | `Tariffpolicy.kallenergiArsserieBindning` | `kallenergiArsserieBindning: json.kallenergi_arsserie_bindning ?? undefined` |
| `Tariffpolicy.returtemperatur_arsserie_bindning` (§6a.4, nytt granskning `2026-09-08-008`) | `returtemperatur_arsserie_bindning` | `Tariffpolicy.returtemperaturArsserieBindning` | `returtemperaturArsserieBindning: json.returtemperatur_arsserie_bindning ?? undefined` |

Negativa test krävs för samtliga nio fält ovan: en genererad policy med fältet satt som TypeScript
läser tillbaka korrekt (inte `undefined`), och en policy UTAN fältet som fortsatt ger
`undefined` (inte t.ex. tomsträng eller `null` feltolkat som ett giltigt bandval).

**Används av:** `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
(`maxvarde=500` på dess `debiterbar_effekt_kw`-krav) — mekaniskt fail-closed i stället för
att förlita sig på att `_niva()` råkar kasta `ValueError` för värden utan täckande band.

### 6a.2 `supplier_confirmed_band_id`-bindning (omkonstruerad, granskning 2026-09-08-006, P1)

**Rättat designfel (P1):** v6:s design bekräftade ett band-ID och kastade sedan om det
INTE stämde med vad `_niva()` skulle ha valt automatiskt — vilket gör leverantörens besked
verkningslöst i EXAKT de tvetydiga gränsfall bindningen finns till för att lösa (dagens
autoväljare tar Borlänge band 5 vid 501 kW och C4 band 6 vid 500 kW; om leverantören
bekräftar ett ANGRÄNSANDE band skulle v6:s design felaktigt blockera det korrekta beskedet
i stället för att använda det). Det bekräftade band-ID:t ska i stället VÄLJA prisraden
direkt.

**Katalogens normativa kontrakt (ordagrant, `optimate-fjarrvarme-2026.json`s
integrationsanvisning):** *"Originalintervall bevaras. Välj `supplier_confirmed_band_id`;
intervallsträngar får inte automatiskt parsas till produktionsgränser."* — detta gäller inte
bara Borlänge/C4 utan samtliga rader vars `capacity.band_selection` är
`supplier_confirmed_band_id_required`.

**Omfattning, verifierad mekaniskt mot den checkade-in katalogen (skrivskyddat script,
`enkey-agents@fd8f8da`):** exakt **42 av de 45 `ready`-raderna** bär markören — de enda tre
undantagen är `finspangs-tekniska-verk-finspang-2026`,
`malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` (ingen kapacitetsdel) och
`sundsvall-energi-indal-liden-och-lucksta-2026` (ren energitariff). v6 specificerade bara
Borlänge/C4 och kallade detta "en ny policy räcker" för resten — fel, se §6-tabellen ovan.

**Diskriminerad värdetyp — INTE en global vidgning av `Varde` (rättat P1, granskning
`2026-09-08-007`):** v7:s `Varde = float | Sequence[float] | str` skulle ha försvagat VARJE
befintligt numeriskt fält samtidigt — verifierat att `_validera_varde`/`valideraVarde`
(resultatkontrakt.py/.ts) i dag avvisar varje sträng, att kontraktsfasaden gör
`float(post.varde)` för varje relevant skalär, att TypeScript lägger varje sådan post i
`Record<string, number>`, och att kalkylatorsidan konverterar med `parseFloat`. En global
strängtillåtelse hade tyst öppnat alla dessa vägar för ogiltig indata, inte bara bandfältet.

Nytt `KravPost`-fält `vardetyp: Literal["number", "number_series", "band_id"] = "number"`
(mirror `vardetyp?: 'number' | 'number_series' | 'band_id'` i TS, default `'number'` för
bakåtkompatibilitet med alla befintliga krav). `__post_init__`/`skapaKravPost` validerar:
`vardetyp == "band_id"` FÖRBJUDER `minvarde`/`maxvarde`/`heltal`/`tillatna_varden` (§6a.6) på
samma post — ett band-ID har ingen numerisk gräns.

**Rättat P1 (granskning `2026-09-08-008`) — `vardetyp` på `KravPost` räcker inte ensamt:**
`IndataPost.varde` (`resultatkontrakt.py`/`.ts`) är fortfarande typad `Varde = float |
Sequence[float]` (Python) / `number | readonly number[]` (TypeScript) — verifierat genom att
läsa typdefinitionen. En `band_id`-post med strängvärde kan alltså INTE konstrueras
typkorrekt utan att `IndataPost.varde`s egen typ också utökas. Fixet ändrar båda typerna,
inte bara kravkontraktet:

- Python: `Varde = float | Sequence[float] | str` PÅ `IndataPost.varde` ENSAMT — `KravPost`
  fortsätter sakna `str` i sin egen typannotering av vad ett krav KAN uttrycka numeriskt,
  eftersom kravet inte bär ett värde, bara en beskrivning av vilket värde det förväntar sig.
  TypeScript-spegel: `Varde = number | readonly number[] | string` på samma ställe.
- `harled_resultatstatus`/`harledResultatstatus` grenar på `f.vardetyp` INNAN den anropar
  `_validera_varde`/`valideraVarde`: för `"band_id"` kräver den att `post.varde` är en
  icke-tom `str` (kastar annars, kastar även om ett tal skickas som "band-ID") — bandkravet
  hamnar alltså ALDRIG i vägen för `_validera_varde`s numeriska kontroll. `_validera_varde`
  SJÄLV ändras INTE och fortsätter oförändrat avvisa `str` för ett fält vars `vardetyp` är
  `"number"`/`"number_series"` — den nya bredare `Varde`-unionen på `IndataPost` vidgar bara
  vad TYPSYSTEMET tillåter att KONSTRUERA, inte vad den KRAVSPECIFIKA valideringen accepterar.
- **`number_series` görs till en verklig diskriminator, inte bara en tillåten möjlighet
  (rättat P1, granskning `2026-09-08-008`):** verifierat att dagens `rullande=True` TILLÅTER
  en serie men INTE KRÄVER en — ett fält märkt `number_series` kunde alltså fortfarande få
  ett bart skalärt tal genom, medan `"number"` bara avvisade en serie via en separat
  `rullande`-kontroll på ANNAT håll i koden. `harled_resultatstatus`/`harledResultatstatus`
  kräver nu explicit, i samma `vardetyp`-gren: `"number"` → `post.varde` MÅSTE vara ett
  skalärt ändligt tal (kastar om det är en `Sequence`/array); `"number_series"` → `post.varde`
  MÅSTE vara en icke-tom `Sequence`/array av ändliga tal (kastar om det är ett bart skalärt
  tal). E.ON/Navirums rullande men SKALÄRA leverantörseffekt (ett enda tal, uppdaterat en
  gång per kalenderår — se `rullande=False`-kommentaren i `policyregister.py` från
  Sandviken-etappen) förblir korrekt modellerad som `vardetyp="number", rullande=True` — inte
  genom att låta `"number_series"` acceptera ett skalärt värde som en genväg.
- **Nytt kardinalitetsfält `KravPost.antal_varden: int | None = None`** (mirror
  `antalVarden?: number` i TS) — deklarativt, GENERISKT (ingen fältnamns- eller
  tariff-specifik hårdkodning i valideraren): satt bara meningsfullt tillsammans med
  `vardetyp="number_series"`, kastar i `__post_init__`/`skapaKravPost` om satt på
  `"number"`/`"band_id"`. `harled_resultatstatus`/`harledResultatstatus` kräver, när satt,
  `len(post.varde) == f.antal_varden` exakt — annars kastar (fel längd är ett strukturellt
  indatafel, inte ett "nästan rätt"-läge som ska accepteras). Stockholms kallenergiserie
  sätter `antal_varden=12`, returtemperaturserien `antal_varden=5` (§6a.4) — det generiska
  fältet uttrycker BÅDA utan att motorn känner till "Stockholm" eller "12"/"5" som
  hårdkodade konstanter någonstans i valideraren själv.

**Mekanism (Python `resultatkontrakt.py`/`katalog.py`/`faktura.py`, TS-speglar likadant):**

1. `till_prisar()` (`katalog.py`) bevarar källans `band["id"]` in i varje `nivaer`-post:
   `{"id": band.get("id"), "min": ..., "max": ..., "avgift_kr_ar": ..., "pris_kr_per_enhet_ar": ...}`
   — i dag tappas `id` helt (verifierat genom att läsa funktionen, se §4 P1-citaten).
2. Nytt `Tariffpolicy`-fält `kapacitet_band_bindning: str | None = None` (mirror
   `kapacitetBandBindning?: string` i TS) pekar ut vilket krävt fält (en NY, separat
   `KravPost`, t.ex. `nyckel="effektband_id"`, `vardetyp="band_id"`) som bär det
   leverantörsbekräftade band-ID:t. Skilt från det befintliga numeriska fältet bakom
   `kapacitet_bindning` — bandvalet och det numeriska debiteringsunderlaget är två oberoende
   krävda fält, och den delade fasadens `falt`-uppbyggnad SKA uttryckligen hoppa över
   `policy.kapacitet_band_bindning` när den bygger den numeriska `falt`-dictionaryn (samma
   mönster som den redan hoppar över `kb`/`policy.kapacitet_bindning` i dag) — ett
   band-ID får aldrig försöka bli `float(...)`.
3. Ny fasadparameter i den lågnivåkoden `arskostnad`/`manadskostnad`
   (`faktura.py`/`fjarrvarme.ts`): `vald_niva_id: str | None = None`. När satt, hoppar
   motorn över `_niva()`s automatiska intervall-uppslagning HELT och använder i stället
   `next(n for n in nivaer if n["id"] == vald_niva_id)` — kastar `ValueError` om ID:t inte
   finns bland `prisar.kapacitet.nivaer`. Kontraktsfasaden
   (`beräkna_arskostnad_med_kontrakt`/`beraknaArskostnadMedKontrakt`) läser
   `indata[policy.kapacitet_band_bindning].varde` och skickar det vidare som
   `vald_niva_id` när `kapacitet_band_bindning` är satt på policyn — annars oförändrat
   beteende (`_niva()` auto-väljer, som i dag, för de tre rader som saknar markören).
4. `_niva()` självt ändras INTE — den fortsätter vara den automatiska fallback-vägen för
   allt som inte har en `supplier_confirmed_band_id`-bindning.
5. Saknat, tomt eller okänt band-ID på en markerad tariff BLOCKERAR
   (`harled_resultatstatus` avvisar via samma mekanism som andra saknade obligatoriska
   fält) — gissas aldrig.

**Grundarbete: en gemensam produktingång för ALLA policykrav (nytt P1, granskning
`2026-09-08-007`) — inte bara kapacitet.** Verifierat genom att läsa
`beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts`): den bygger i dag `IndataPost` ENDAST
för `policy.kapacitetBindning`. Varje policy med ett band-, flödes-, temperatur-, B- eller
annat extra krav utöver kapacitet ger därför i dag ett `blocked`-resultat som (per den
befintliga felhanteringen där `beraknaBesparingsvardeKontrakt` tolkar ETT oväntat
`blocked`-fynd som ett konfigurationsfel) skulle kasta i stället för att räkna — detta gäller
ALLA 41 av de 45 `ready`-raderna som har mer än ett krävt fält, inte bara bandraderna.

Detta MÅSTE lösas som grundarbete FÖRE första tariffbatchen (ny batch 0, se
`batchplan-v9.md`), inte något Sandvikens nuvarande kapacitets-only-adapter redan täcker:

1. `KalkylatorPage.tsx` samlar redan tariffspecifik indata i ett fritt `falt`-objekt
   (`Record<string, string>` från formulärfält). Denna indata måste föras OFÖRÄNDRAD genom
   `energiPotential.ts` (`KalkylatorInputs.falt`) till `besparingsvarde.ts`
   (`BesparingsvardeArgs.falt`) — redan fallet för de befintliga fria fälten, ingen ändring
   där.
2. Ny hjälpfunktion i `besparingsvarde.ts`, t.ex. `byggIndataFranPolicy(policy: Tariffpolicy,
   falt: Record<string, string | number>): Map<string, IndataPost>`: itererar
   `policy.kravdaFalt`, slår upp varje `nyckel` i `falt`, och bygger en `IndataPost` per
   TRÄFF med `kallaTyp: 'supplier_value'` och rätt `varde`-typ enligt fältets `vardetyp`
   (`Number(...)` för `"number"`, oförändrad sträng för `"band_id"`, en array/serie
   ospridd — se punkt 6 nedan — för `"number_series"`). Ett policydeklarerat fält UTAN
   motsvarande `falt`-nyckel byggs INTE — det blir korrekt `saknade`/`blocked` i
   `harled_resultatstatus`, inte en tyst `undefined`. Ett `falt`-nyckel UTAN motsvarande
   policykrav IGNORERAS — extra, ovaliderad indata når aldrig motorn.
3. `beraknaBesparingsvardeKontrakt` anropar den nya funktionen i stället för att bara sätta
   ETT `Map`-inlägg för `kapacitetBindning` — kapacitetsbindningen (redan validerad separat
   ovanför i samma funktion, heltal/golv) läggs in i samma karta EFTER den generiska
   uppbyggnaden, så dess redan skärpta valideringsregler (§ befintlig kod) inte försvagas.
4. Python-sidans motsvarande produktväg (i dag bara Sandvikens direkta
   `berakna_arskostnad_med_kontrakt`-anrop i tester, ingen egen produktsida) får samma
   generiska byggfunktion `bygg_indata_fran_policy(policy, falt)` i förberedelse för framtida
   Python-produktkonsumenter, för att hålla mekanismen synkad i båda språken redan nu.
5. **Genererad UI-metadata (nytt P1, granskning `2026-09-08-008`):** v8:s
   `byggIndataFranPolicy` antog att `KalkylatorPage.tsx` REDAN hade en källa till band-/enum-
   /serieval att skicka in i `falt` — men verifierat genom att läsa den sidan och
   `indatafalt_for()` (`generera.py`): dagens `indatafalt` genereras BARA från kända
   justeringar och kapacitetsformen `kWh/day`, och UI:t renderar VARJE post som
   `type="number"` byggd via `parseFloat`. Det finns alltså i dag INGEN källa till ett
   band-ID-val, ett Jönköping-liknande enum-val, eller ett serieinmatningsfält. Ny
   TypeScript-typ `PolicyFaltMetadata` genereras från `Tariffpolicy.kravdaFalt` (samma
   generator-/policyregisterväg som redan bär de andra fälten i denna sektion) och exponeras
   via en ny funktion `policyFaltMetadata(policy: Tariffpolicy): PolicyFaltMetadata[]` i
   `resultatkontrakt.ts`, en post per `KravPost` med minst:
   `{ nyckel, inmatningstyp: 'number' | 'band_id_val' | 'enum_val' | 'number_series',
   etikett, hjalptext, obligatorisk: true, tillatnaVarden?, seriekardinalitet? }`. Band-ID-
   alternativen (`inmatningstyp: 'band_id_val'`) hämtas från DEN VALDA tariffens egen
   bevarade `prisar.kapacitet.nivaer[].id` (§6a.2 punkt 1) — INTE en global lista — så
   `KalkylatorPage.tsx` kan rendera exakt de band den aktuella leverantören faktiskt
   publicerar. Enum-alternativ (`inmatningstyp: 'enum_val'`) hämtas från `KravPost.
   tillatnaVarden` (§6a.6). Varken enum- eller bandvärden får någonsin passera
   `parseFloat` — de renderas och lagras som strängar/diskreta val genom hela
   `KalkylatorPage.tsx` → `falt`-kedjan.
6. **Felklassning (nytt P1, granskning `2026-09-08-008`):** ett saknat obligatoriskt
   policyfält ger korrekt `blocked` i `harled_resultatstatus`, men dagens
   `beraknaBesparingsvardeKontrakt` tolkar VARJE oväntat `blocked`-resultat (bortom det redan
   särskilda kapacitetsfallet) som ett konfigurationsfel och kastar en generisk `Error` —
   fel för en LEGITIMT saknad kundindata, som ska visas som ett vanligt formulärfel, inte en
   trasig policy. `KontraktBlockerat` (redan den delade felklassen från Sandviken-etappen)
   får ett nytt, valfritt fält `saknadeFalt?: string[]` — satt när `status.fullstandighet ===
   'blocked'` OCH varje saknat krävt fält faktiskt saknas i den byggda `falt`-mappen (dvs.
   användaren inte fyllt i det), skilt från fallet där `falt`-mappen har alla nycklar men ett
   VÄRDE är strukturellt ogiltigt (fel `vardetyp`, fel längd, okänt enum-/band-ID) — det
   senare förblir ett kastat kontraktsfel, eftersom det INTE är ett läge en vanlig
   användarinmatning kan råka i via det genererade UI:t (punkt 5), bara via ett direkt
   API-/fasadanrop som kringgår formuläret. `KalkylatorPage.tsx` visar `saknadeFalt` som en
   vanlig "fyll i dessa fält"-text i stället för det generiska felmeddelandet.

**Numerisk rimlighetskontroll (frivillig, källbaserad — inte `_niva()` återinförd som
sanningskälla):** om en tariffs källa publicerar entydiga, normaliserade gränser (t.ex.
Borlänges "band 5 gäller `>501` kW") kan policyn DESSUTOM kräva att det numeriska
kapacitetsvärdet ligger inom det bekräftade bandets `min`/`max` — men det bekräftade
band-ID:t vinner alltid över vad `_niva()` skulle valt; kontrollen finns bara för att fånga
en uppenbar felskrivning (t.ex. band-ID 3 ihopparat med ett kW-tal som uppenbart hör till
band 6), inte för att överpröva ett korrekt, tvetydigt gränsfallsbesked. Öppna gränspunkter
(">N" utan explicit övre gräns, "<N" utan explicit undre gräns) hanteras genom att helt
enkelt inte sätta den saknade gränsen — ingen implicit ±1-justering.

**De 42 berörda raderna** (tariff-ID, antal band, källans band-ID:n — verifierat mekaniskt):

| Tariff-ID | Band | Band-ID:n i källan |
|---|---:|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | 6 | 1–6 |
| `borlange-energi-borlange-2026` | 5 | 1–5 |
| `c4-energi-kristianstad-2026` | 6 | 1–6 |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | 1 | 1 |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | 1 | 1 |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | 1 | 1 |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | 1 | 1 |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | 4 | 1–4 |
| `falu-energi-vatten-falun-2026` | 7 | 1–7 |
| `habo-energi-habo-2026` | 1 | 1 |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | 5 | 1–5 |
| `jamtkraft-brunflo-och-opevagen-2026` | 5 | 1–5 |
| `jamtkraft-ostersund-froson-as-2026` | 5 | 1–5 |
| `jonkoping-energi-jonkoping-och-granna-2026` | 4 | 1–4 |
| `karlstads-energi-karlstad-2026` | 5 | 1–5 |
| `kils-energi-kil-2026` | 4 | 1–4 |
| `kraftringen-kraftringen-2026` | 4 | 1–4 |
| `lulea-energi-lulea-2026` | 7 | 1–7 |
| `mjolby-svartadalen-energi-mjolby-2026` | 4 | 1–4 |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | 1 | 1 |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | 1 | 1 |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | 1 | 1 |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | 1 | 1 |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | 3 | 1–3 |
| `oresundskraft-angelholm-normal-2026` | 5 | 1–5 |
| `oresundskraft-helsingborg-normal-2026` | 5 | 1–5 |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | 5 | 1–5 |
| `ovik-energi-ornskoldsvik-2026` | 16 | 1–16 |
| `partille-energi-partille-2026` | 7 | 1–7 |
| `piteenergi-norrfjarden-och-sjulnas-2026` | 4 | 1–4 |
| `piteenergi-pitea-centrala-natet-2026` | 4 | 1–4 |
| `skovde-energi-skovde-2026` | 1 | 1 |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | 4 | 10–13 |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | 4 | 1–4 |
| `stockholm-exergi-stockholm-exergi-normal-2026` | 5 | 1–5 (rad exkluderad, se §6a.4 — bandkontraktet moot) |
| `tekniska-verken-katrineholm-katrineholm-2026` | 4 | 1–4 |
| `tekniska-verken-linkoping-linkoping-2026` | 4 | 1–4 |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | 3 | 1–3 |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | 3 | 1–3 |
| `trollhattan-energi-trollhattan-2026` | 5 | 1–5 |
| `umea-energi-umea-enkel-2026` | 7 | 1–7 (dessutom `kapacitet_multiplikator_bindning`, §6a.3) |
| `vanerenergi-mariestad-och-toreboda-2026` | 4 | 1–4 |

**Ambiguösa exakta gränsfall (kräver leverantörsbekräftelse, inte bara ett vilket-som-helst
band-ID):** `borlange-energi-borlange-2026` (band 5, `>501`) och
`c4-energi-kristianstad-2026` (band 6, `>500`) är de två rader där ett exakt gränsvärde
(501 respektive 500 kW) är den uttryckligen osäkra punkten källan själv flaggar. De övriga
40 raderna har inte en känd tvetydig gräns i källan, men bandkontraktet gäller ändå
strukturellt för alla 42 — katalogens integrationskontrakt gör ingen skillnad mellan "känt
tvetydiga" och "inte kända som tvetydiga", och en framtida gränsförskjutning ska inte kunna
smyga sig förbi en rad som råkade vara icke-ambiguös vid detta skrivtillfälle.

### 6a.3 Umeås `kapacitet_multiplikator_bindning` — arkitektoniskt separerad grind (rättat P1, granskning 2026-09-08-007)

**Rättat ordningsfel (P1, granskning `2026-09-08-007`):** v7 påstod att
`kontrollera_kompositgrind(tariff, policy)` skulle köras EFTER steg 2+3 i §6 — men den
VERKLIGA generatorn (`bygg_ts_fran_katalog()` i `generera.py`) anropar
`ur_katalogen = godkanda(katalog)` FÖRST och itererar sedan BARA de rader `grind()` gav
`None` för. En kontroll som körs "efter" kan alltså aldrig återinföra en rad `godkanda()`
redan filtrerat bort — Codex reproducerade exakt detta: med Umeås status/issues
neutraliserade gav `grind(...)` fortsatt `"kapacitetsformel med multiplikator"` och
`godkanda()` returnerade noll rader.

Löst genom att flytta kompositkontrollen IN I `godkanda()`s egen loop, som ett andra försök
begränsat till EXAKT ett fynd — **rättat P1 (granskning `2026-09-08-008`):** v8:s version
lade till raden så fort `kontrollera_kompositgrind()` godkände multiplikatorbindningen, UTAN
att därefter kontrollera om ett ANNAT strukturellt fynd (okänd `issue`, okänd
`okand_justering()`) låg dolt bakom multiplikatorfyndet. `grind()` returnerar bara det FÖRSTA
fyndet den hittar, och kontrollen av `post_multiplier` ligger FÖRE kontrollen av `issues`/
`okand_justering()` — Codex reproducerade att Umeås verkliga katalograd har SAMTLIGA tre
problem samtidigt (`post_multiplier`, en ännu okänd `issue`, och `asymmetric_flow_difference`
som `okand_justering()` inte känner igen), så v8:s design skulle ha lagt till raden utan att
de två sistnämnda någonsin kontrollerades. Fixet: efter att multiplikatorbindningen är
verifierad, körs `grind()` EN GÅNG TILL på en kopia av tariffen där ENDAST det fynd som redan
är kvitterat (`post_multiplier`) är neutraliserat — alla andra fält, inklusive `issues` och
`adjustments`, är oförändrade. Bara om ÄVEN detta andra pass ger `None` läggs raden till:

```python
def _neutralisera_post_multiplier(tariff: dict) -> dict:
    """Returnerar en YTLIG kopia av tariffen där ENDAST det redan kvitterade
    post_multiplier-fyndet är borttaget — kapacitetsobjektet kopieras separat
    så den ursprungliga katalogposten aldrig muteras. Alla andra fält
    (issues, adjustments, investigation, m.m.) är OFÖRÄNDRADE, så grind()s
    andra pass fortsatt kan hitta och blockera på dem."""
    kapacitet = dict(tariff.get("capacity") or {})
    kapacitet.pop("post_multiplier", None)
    return {**tariff, "capacity": kapacitet}


def godkanda(katalog: dict, policyregister: dict = POLICYREGISTER) -> list[dict]:
    resultat = []
    blockerade = blockerade_tariff_ider(katalog)  # §7
    for t in katalog["tariffs"]:
        avslag = grind(t, blockerade)
        if avslag is None:
            resultat.append(t)
            continue
        # NYTT: kompositgrindens ENDA konsumerbara fynd. Varje annat fynd
        # ("null i band", "okänd issue", "energiform", ...) faller igenom
        # och tariffen förblir blockerad — ingen generell undantagsväg.
        if avslag == "kapacitetsformel med multiplikator":
            policy = policyregister.get(t["id"])
            if policy is not None and kontrollera_kompositgrind(t, policy) is None:
                # Multiplikatorfyndet är kvitterat — men grind() returnerade
                # bara DET FÖRSTA fyndet; kör grinden igen med bara det
                # kvitterade fältet neutraliserat, för att avslöja en
                # eventuell DOLD andra blockering (samma "metodnot"-mönster
                # som redan gällde 13 av de 45 raderna, §6).
                t_neutraliserad = _neutralisera_post_multiplier(t)
                if grind(t_neutraliserad, blockerade) is None:
                    resultat.append(t)
                # annars: fortfarande blockerad av ett dolt strukturellt fynd
        # annars: förblir blockerad (fortsätter loopen utan att lägga till t)
    return resultat
```

**Rättat P1 (registerdivergens, granskning `2026-09-08-008`):** v8:s pseudokod introducerade
`godkanda(katalog, policyregister=POLICYREGISTER)` men sa att `bygg_ts_fran_katalog()` inte
behövde ändras — verifierat att generatorn i dag anropar `godkanda(katalog)` UTAN registret,
medan den redan har ett injekterbart `policyregister`-argument som förs vidare till
`kontrollera_aktiveringsgrind(..., register=policyregister)` längre ner i samma funktion. Utan
en ändring skulle den sammansatta grinden läsa det GLOBALA registret medan resten av
generatorn läser det INJICERADE — ett testregister och produktregistret kunde då ge olika
svar. `bygg_ts_fran_katalog()` ändras därför till att uttryckligen föra sitt egna
`policyregister`-argument vidare till `godkanda(katalog, policyregister=policyregister)`, och
`main()`s räkningslogik (som anropar `godkanda()` separat för statistik) gör detsamma.

Detta ÄR den körbara ordningen — kompositkontrollen är en del av samma filtreringspassage
`godkanda()` redan gör, inte ett separat steg efteråt. `bygg_ts_fran_katalog()` behöver
föra sitt egna `policyregister`-argument uttryckligen vidare till `godkanda(katalog,
policyregister=policyregister)` (se ovan) — annars läser den sammansatta grinden det globala
`POLICYREGISTER` medan resten av funktionen kan läsa ett injicerat register. Utöver den ena
raden ligger hela fixet i `godkanda()` själv.

1. Den nakna `grind()` (`katalog.py`) ändras INTE — den fortsätter avvisa varje
   `capacity.post_multiplier` som `"kapacitetsformel med multiplikator"`, oförändrat för
   alla tariffer inklusive Umeå. Umeå passerar alltså ALDRIG steg 2 (§6) ensamt — bara den
   sammansatta `godkanda()`-loopen ovan kan öppna raden, och först efter att BÅDA
   grindpassen (det ursprungliga och det neutraliserade) gett `None`.
2. `kontrollera_kompositgrind(tariff: dict, policy: Tariffpolicy) -> str | None`
   (`policyregister.py`) tar policyn som explicit argument. Om
   `tariff["capacity"].get("post_multiplier") is not None`, kräver funktionen att
   `policy.kapacitet_multiplikator_bindning is not None` OCH att den bundna `KravPost`
   finns i `policy.kravda_falt` — annars avslagsorsak. Detta ÄR den explicita, typade
   capability-kontrollen v6 saknade; den nakna grinden godkänner aldrig en okänd
   multiplikator på egen hand, och kompositkontrollen kan bara YTTERLIGARE godkänna, aldrig
   ytterligare blockera, en rad `grind()` redan släppte igenom.
3. Motorn (`faktura.py`/`fjarrvarme.ts`) läser det bundna värdet som `B` och multiplicerar
   in det i kapacitetsformeln — motorn räknar ALDRIG `U` (normalårskorrigerat förhållande),
   bara `B` som ett direkt leverantörsvärde. Python: `kapacitet_multiplikator_bindning: str
   | None = None` på `Tariffpolicy`, validerat mot `kravda_falt` precis som
   `kapacitet_bindning`/`kallenergi_bindning`. TypeScript-spegel:
   `kapacitetMultiplikatorBindning?: string` — mappningsraden i §6a.1s tabell.

**Intervallkrav, omräknat:** den publicerade mellanformeln `1,34×U+0,330` ger `1,40066` vid
`U=0,799` (katalogens övre brytpunkt) — ett absolut, avrundat tak `maxvarde=1,4` hade därför
kunnat avvisa ett giltigt leverantörsvärde beroende på HUR leverantören själv avrundar sin
egen publicerade formel. Kravet sätts i stället till `minvarde=0.93`, `maxvarde=1.401` —
fyra värdesiffror, en (1) enhet extra marginal på sista decimalen mot den exakta
formelutledda gränsen `1,40066`, med regeln dokumenterad explicit i policykommentaren i
stället för att gissa ett exakt tak.

**Rättat P1 (granskning `2026-09-08-007`) — B-värdesvalideringen flyttad till rätt lager:**
`kontrollera_kompositgrind` tar bara `(tariff, policy)` — den kan bevisa att bindningen är
DEKLARERAD, men har ingen `IndataPost` att kontrollera det faktiska kundvärdet mot. Testet
för `B=14` (uppenbart utanför intervallet) hör därför INTE hemma i
`kontrollera_kompositgrind`, utan i `harled_resultatstatus`/kontraktsfasaden via den bundna
`KravPost`s `minvarde=0.93`/`maxvarde=1.401` — exakt samma mekanism som redan validerar
Sandvikens effektgolv. Test: golden-värden vid `B=0.93`, `B=1.401` och en punkt mellan
brytpunkterna (kontraktsfasaden, steg 4 i §6); ett negativt test för `B=14` blockerar via
`harled_resultatstatus` (INTE `kontrollera_kompositgrind`, som aldrig ser det faktiska
värdet); och ett separat test att Umeå UTAN bindningen fortsatt stoppas av
`kontrollera_kompositgrind` (steg 3, den statiska kontrollen) samt att en ANNAN tariff med
okänd multiplikator (ingen policy alls, eller policy utan bindningen) fortsatt stoppas av
samma funktion. Testet kallas `B-intervall`, inte "U-intervall" — motorn räknar aldrig `U`.

**Nya test (granskning `2026-09-08-008`, `godkanda()`s tvåpassdesign ovan):** Umeå läggs
till i `godkanda()`s resultat FÖRST när issue-rättelsen, den kända justeringstypen
(`asymmetric_flow_difference` registrerad) OCH B-bindningen samtliga finns; lägg tillbaka en
okänd `issue` (allt annat rättat) och bevisa att raden ändå blockeras av det andra
`grind()`-passet; lägg tillbaka en okänd justeringstyp (allt annat rättat) och bevisa samma
sak. Ett separat test kör `godkanda(katalog, policyregister=ett_annat_register)` och bevisar
att resultatet skiljer sig från `godkanda(katalog)` (globalt register) när det injicerade
registret saknar Umeås policy — bevisar att registret faktiskt förs igenom, inte bara läses
globalt av misstag.

**Används av:** `umea-energi-umea-enkel-2026` — enda tariffen med `post_multiplier` i dagens
kontrollmängd. Kräver BÅDE detta OCH bandkontraktet (§6a.2) — verifierat att raden har både
`band_selection` och `post_multiplier` samtidigt.

### 6a.4 Stockholm Exergi — nåbar adapterkontroll, verklig dispatch och en typad årsindatamodell (rättat P1, granskning 2026-09-08-007/-008)

**Rättat P1 #1 — adapterkontrollen var inte nåbar:** v7 beskrev `ADAPTERREGISTER` som
kontrollerat "när generatorn behandlar en katalogtariff" — men den VERKLIGA
`bygg_ts_fran_katalog()` gör `ur_katalogen = godkanda(katalog)` FÖRST och itererar sedan
BARA de rader som kom igenom. Stockholms katalograd har `investigation.status: utreds` OCH
stoppas av `energiform` (`monthly_with_peak_volume_replacement` finns inte i
`FAS1_ENERGIFORMER`) — den når alltså ALDRIG in i den filtrerade loopen där v7 tänkte sig
kontrollen. Löst genom att köra adapterkontrollen som en SEPARAT preflight mot den RÅA
`katalog["tariffs"]`-listan, direkt efter `ur_katalogen = godkanda(katalog)` i
`bygg_ts_fran_katalog()` — oberoende av om katalograden finns kvar i `ur_katalogen`:

```python
def bygg_ts_fran_katalog(katalog, ...):
    ur_katalogen = godkanda(katalog)
    # NYTT: kontrolleras mot RÅ katalog["tariffs"], inte ur_katalogen —
    # en adapterpost får peka på en katalograd grind()/godkanda() redan
    # (korrekt) filtrerat bort, eftersom hela poängen är att den raden
    # aldrig ska aktiveras via katalogvägen, bara via adapterhoppet.
    leverantorer = _bygg_leverantorer(filer, policyregister=policyregister)  # redan byggd tidigare i funktionen
    for katalog_id, entry in ADAPTERREGISTER.items():
        rad = next((t for t in katalog["tariffs"] if t["id"] == katalog_id), None)
        if rad is None:
            raise ValueError(f"ADAPTERREGISTER: {katalog_id} finns inte i katalogen")
        # RÄTTAT P1 (granskning 2026-09-08-008): v8 slog bara upp entry.tariff_id
        # i POLICYREGISTER men kontrollerade aldrig entry.provider_id mot den
        # redan byggda leverantorer-mängden — ett felaktigt provider_id kunde
        # då aldrig kastas, trots att testlistan lovade det.
        leverantor = leverantorer.get(entry.provider_id)
        if leverantor is None:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} anger provider_id={entry.provider_id!r}, "
                "men ingen sådan leverantörsfil är byggd"
            )
        prisarspost = next((p for p in leverantor["prisar"] if p.get("tariff_id") == entry.tariff_id), None)
        if prisarspost is None:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} anger tariff_id={entry.tariff_id!r} hos "
                f"{entry.provider_id!r}, men leverantören har ingen sådan prisårspost"
            )
        malpolicy = POLICYREGISTER.get(entry.tariff_id)
        if malpolicy is None or entry.kravd_tackning not in malpolicy.tackning:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} pekar på {entry.tariff_id}, men "
                f"målpolicyn saknas eller täcker inte {entry.kravd_tackning!r}"
            )
    # RÄTTAT P1 (omvänd regel, granskning 2026-09-08-008): en leverantörsfilspolicy
    # avsedd att ERSÄTTA en katalogdublett (dvs. en policy med annual_forward vars
    # tariff_id förekommer som mål i ADAPTERREGISTER) får inte existera UTAN en
    # motsvarande adapterpost — annars kunde en policy tyst få annual_forward-
    # täckning aktiverad utan att någon adapterkontroll någonsin körts för den.
    adapterade_mal = {entry.tariff_id for entry in ADAPTERREGISTER.values()}
    for leverantor in leverantorer.values():
        for prisarspost in leverantor["prisar"]:
            policy = prisarspost.get("policy")
            tariff_id = prisarspost.get("tariff_id")
            if policy and "annual_forward" in policy.get("tackning", []) and tariff_id not in adapterade_mal:
                # Undantag: en policy vars annual_forward-täckning INTE kom via
                # en katalogdublett (t.ex. en framtida, direkt leverantörsprodukt
                # utan någon katalogmotsvarighet) är tillåten — kontrollen gäller
                # bara poster som FAKTISKT förväntas nås via ett adapterhopp.
                # Stockholms fall bekräftas explicit ADAPTERAT via en positiv
                # medlemskapskontroll ovan, inte via denna negativa gissning.
                pass  # se produktionskoden för den fullständiga, testade regeln
    # ... resten av funktionen oförändrad; leverantörsfilerna (inkl.
    # stockholm-exergi-2026, nu med utökad policy) byggs som i dag i
    # _bygg_leverantorer(), FÖRE katalogloopen.
```

Kastar (`raise`) om registret pekar på en katalograd som inte finns, en leverantör/prisårspost
som inte finns, eller en målpolicy som saknas/inte täcker `annual_forward` — aldrig en tyst
utebliven rad. `godkanda()`/katalogloopen rörs INTE av detta — `ADAPTERREGISTER`-kontrollen
är en oberoende preflight, inte ett filter inuti den befintliga loopen.

**Omvänd regel, precist (ersätter pseudokodens skiss ovan):** en leverantörsfilspolicy får
INTE deklarera `annual_forward` i `tackning` om den samtidigt INTE är målet för någon
`ADAPTERREGISTER`-post ELLER inte redan var godkänd för `annual_forward` innan denna etapp
(dvs. reglen gäller framåtriktat, den ändrar inte redan pushad policydata retroaktivt). I
praktiken: `_bearbeta_leverantorsfil()` validerar, när den läser en prisårspost vars policy
har `annual_forward`, att exakt en `ADAPTERREGISTER`-post pekar på den (`provider_id` +
`tariff_id` matchar) — saknas den kastar generatorn. Testet bevisar båda riktningarna: (a)
en `ADAPTERREGISTER`-post utan matchande annual_forward-policy kastar (redan ovan), och (b)
en annual_forward-policy utan matchande `ADAPTERREGISTER`-post kastar (den nya kontrollen).

**Rättat P1 #2 — ingen verklig dispatch fanns:** v7 sa att leverantörsfilens prispost
"visserligen" får policyn bifogad men inte `_kraver_kontrakt` — så `kontraktsgatadPolicy()`
(`besparingsvarde.ts`) skulle fortsätta returnera `undefined` och `beraknaBesparingsvarde`
fortsätta på legacyvägen, HELT OAVSETT att policyn nu (via 6a.4 #1) har `annual_forward`.
Att bara lägga täckningen i policyn ändrar alltså inte vilken kod som faktiskt körs.

Lösningen ÅTERANVÄNDER den redan befintliga `_kraver_kontrakt`-markören — samma mekanism
som redan tvingar VARJE annan kontraktsgated tariff (Sandviken m.fl.) genom
`beräkna_arskostnad_med_kontrakt`-fasaden i stället för den nakna motorn — i stället för
att hitta på ett nytt, parallellt dispatch-fält: `_bearbeta_leverantorsfil()`
(`generera.py`) sätter `_kraver_kontrakt: True` på Stockholms prispost NÄR dess policy (efter
6a.4 #1s utökning) täcker `annual_forward`, precis som katalogvägens
`kontrollera_aktiveringsgrind` redan gör för nya katalogtariffer. Detta är den enda
ändringen som krävs för dispatch: `kontraktsgatadPolicy()` returnerar då policyn i stället
för `undefined`, och `beraknaBesparingsvarde` väljer automatiskt kontraktsgrenen — ingen ny
`AdapterEntry`-diskriminator eller `annual_inverse`-krav behövs för själva dispatchen (den
löser bara vilken KATALOGRAD som ska hoppas över, se #1 ovan).

**Rättat P1 #3 — årsindatan var inte representerad:** dagens årsfasad tar
`mwh_kallt_per_manad` och ETT enda `returtemp_c` som fria argument — ett tal används för
ALLA vintermånader, och `Tariffpolicy` förbjuder dubblerade `kravda_falt.nyckel`, så de
befintliga månadsvisa `kall_energi_mwh`/`returtemperatur_c`-kraven (redan bundna till
`monthly`-omfattningen) kan inte återanvändas rakt av för en ENDA årsvis samlad indata.

**Rättat P1 (granskning `2026-09-08-008`) — EN modell, inte två motsägande.** v8 kallade
modellen omväxlande "17 nya `KravPost`" (denna sektions rubrik) och rekommenderade samtidigt
tvåserielösningen nedan — batchplanen upprepade "17 nya KravPost" separat. Det är den
tvåskalar-plus-tolvskalar-modellen (17 enskilda `KravPost`) OCH tvåserielösningen som är TVÅ
OLIKA API:n med olika UI-/validerings-/bindningsbehov; de kan inte båda stå kvar som möjliga
val. **Vald modell, den enda: två serie-`KravPost`**, inte 17 skalära:

- `KravPost(nyckel="kall_energi_mwh_arsserie", vardetyp="number_series", antal_varden=12,
  rullande=True, kravs_for=("annual",))` — `IndataPost.varde` är en 12-elements
  `Sequence[float]` i kalenderordning (januari–december). `antal_varden=12` (§6a.2) gör
  längdkravet deklarativt i stället för att förlita sig på att `rullande=True` råkar tillåta
  serier.
- `KravPost(nyckel="returtemperatur_c_vintermanader", vardetyp="number_series",
  antal_varden=5, rullande=True, kravs_for=("annual",))` — exakt 5 element, ordnade
  november–mars (samma vintermånader som redan gäller för det befintliga `monthly`-kravet).
- Båda seriekraven valideras i `harled_resultatstatus` via `antal_varden` (§6a.2) INNAN de
  binds — en serie av fel längd BLOCKERAR, mappas aldrig till fel månad genom att bara
  zippa index.
- **Två nya statiska `Tariffpolicy`-bindningar (saknades helt i v8, P1):**
  `kallenergi_arsserie_bindning: str | None = None` och
  `returtemperatur_arsserie_bindning: str | None = None` (mirror
  `kallenergiArsserieBindning`/`returtemperaturArsserieBindning` i TS — mappningsraderna i
  §6a.1s tabell). Utan dessa skulle serierna träffa årsfasadens GENERELLA `falt`-loop, som
  uttryckligen kastar för seriepost — precis samma princip som `kapacitet_band_bindning`
  (§6a.2) och `kapacitet_multiplikator_bindning` (§6a.3): en bindning pekar UT vilket
  validerat fält som är motorns specialargument, den generiska `falt`-loopen hoppar
  uttryckligen över alla tre bindna fälten (`kb`, `kapacitet_band_bindning`,
  `kapacitet_multiplikator_bindning`, och nu `kallenergi_arsserie_bindning`/
  `returtemperatur_arsserie_bindning`) när den bygger den numeriska `falt`-dictionaryn.
- **Effektkravets omfattning breddad (saknades i v8, P1):** det befintliga
  `debiterbar_effekt_kw`-kravet (redan bundet via `kapacitet_bindning` för
  `monthly_invoice`) är i dag märkt ENDAST `kravs_for=("monthly",)`. Stockholms utökade
  policy lägger `"annual"` till SAMMA post (`kravs_for=("monthly", "annual")`) i stället för
  att duplicera ett nytt, separat effektkrav med en annan nyckel — samma leverantörsvärde
  gäller båda omfattningarna, och `Tariffpolicy` förbjuder ändå dubblerade nycklar.
- Kontraktsfasadens `berakna_arskostnad_med_kontrakt`-motsvarighet för Stockholm läser de
  två bundna serierna (via `kallenergi_arsserie_bindning`/`returtemperatur_arsserie_bindning`,
  ALDRIG genom att fritt läsa en hårdkodad nyckel eller "Stockholm-motsvarigheten läser vissa
  nycklar" — det generiska bindningsmönstret gäller identiskt för alla framtida tariffer med
  samma behov) och konstruerar `mwh_kallt_per_manad`/en NY
  `returtemp_c_per_manad: dict[int, float]`-parameter till den lågnivåkod som redan
  periodiserar per månad — det befintliga enskalär-`returtemp_c`-argumentet ANVÄNDS INTE
  för denna väg; `_arskostnad_for_kontraktfasad`/TS-motsvarigheten får en ny, valfri
  `returtemp_c_per_manad`-parameter som (när satt) används i stället för det enskalära
  argumentet för exakt de fem vintermånaderna. Inga parallella fria argument får kringgå
  policyn för denna tariff.

**Fail-closed regel för före/efter i besparingsberäkningen (saknades helt i v8, P1):**
`beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts`) använder i dag SAMMA `IndataPost`-
karta för både före- och efterkostnaden, medan de syntetiska månadsmängderna (`fordelaEnergi`)
KRYMPER i efterfallet med den påverkbara energins minskning. Om Stockholms 12 kallenergivärden
hölls OFÖRÄNDRADE mellan de två anropen skulle ett eftermånads totalenergi kunna bli MINDRE än
den ursprungliga kallenergin för samma månad — motorn skulle då räkna en NEGATIV mängd normal
(varm) energi, ett fysiskt orimligt resultat. Ingen leverantörskälla ger en verifierad regel
för hur kallenergin ska skalas om mellan ett fiktivt före- och eftertillstånd (kallenergin är
en fastighetsspecifik mätserie, inte en tariffparameter som kan härledas ur besparingsgraden).
**Beslut:** Stockholms årsprodukt kan ge en UPPSKATTAD AKTUELL årskostnad (ett enda
`beraknaArskostnadMedKontrakt`-anrop med de verkliga 12 kallenergivärdena, `noggrannhet:
snapshot`, ingen krympning inblandad), men EXKLUDERAS explicit från
besparingsvärderingsflödet (`kostnadFore`/`kostnadEfter`-paret i `beraknaBesparingsvarde`)
tills en källmässigt försvarbar transformationsregel finns — `beraknaBesparingsvardeKontrakt`
kastar ett tydligt, typat fel (inte `KontraktBlockerat` — detta är inte en kunddatalucka utan
en produktbegränsning) om anroparen efterfrågar en besparingsberäkning för en tariff vars
policy har `kallenergi_arsserie_bindning` satt. `0 <= kallenergi[m] <= totalenergi[m]`
valideras ändå för VARJE månad `m` i det enkla uppskattningsflödet, som ett generellt,
icke-Stockholm-specifikt sanity-krav på alla framtida `number_series`-bundna kallenergikrav.

**Preflighten (§6) rapporterar 44 katalogaktiveringar + 1 leverantörsfilsutökning** — inte
45 identiska `grind()`-vägar. Stockholms rad i §6:s per-tariffrad-tabell markeras
`EXKLUDERAS` (oförändrat), men mekanismen som gör den tillgänglig i UI:t ligger helt
utanför den katalogdrivna aktiveringskedjan.

**Bevisat genom körning:** `_stabilt_tariff_id()` på katalograden ger
`stockholm-exergi-stockholm-exergi-normal` — en tredje, aldrig tidigare existerande
produkt-ID skild från leverantörsfilens `stockholm-exergi-2026`. Utan
`ADAPTERREGISTER`-preflighten skulle en katalogaktivering (om den någonsin nådde grinden)
skapa TVÅ val i UI för samma underliggande normalprodukt, vilket bryter inventeringens
egen dedupliceringsregel (§1).

**Test (utöver v7:s lista, kompletterat granskning `2026-09-08-008`):** saknad/stale
`ADAPTERREGISTER`-mappning kastar; fel `provider_id` (leverantören finns inte i den byggda
leverantörsmängden) kastar; fel `tariff_id` (leverantören finns, men har ingen sådan
prisårspost) kastar; policytäckning UTAN adapter kastar (den omvända regeln); en
seriekrav-post med 11 eller 13 element (kall energi) resp. 4 eller 6 element (returtemp)
blockerar via `antal_varden`; effektkravets `kravs_for` innehåller nu `"annual"` OCH
`"monthly"` samtidigt (ett test per omfattning, samma `KravPost`); ett anrop till den
uppskattade årskostnaden med giltiga 12/5-serier ger `noggrannhet: snapshot`; ett anrop till
besparingsvärderingen för Stockholm kastar det nya typade felet (inte `KontraktBlockerat`);
`0 <= kallenergi[m] <= totalenergi[m]` blockerar för ett medvetet ogiltigt värde; oförändrad
`monthly_invoice`-väg (regressionstest att den befintliga fakturaåterspelningen inte
påverkas av utökningen); exakt ETT Stockholm-val genereras i UI:t (ingen katalogdublett).

### 6a.5 Kraftringens parametriserade motortyp — domänriktigt namn och en verklig motorväg (rättat P1, granskning 2026-09-08-007)

Codex/Roberts beslut i granskning `2026-09-08-006` (öppen fråga 4): en parametriserad
motortyp för E.ON/Navirums flödeskorrigering delad med Kraftringen är godkänd, UNDER
FÖRUTSÄTTNING att regelvarianten är en explicit, typad diskriminator — INTE implicit
härledd från leverantörs-ID.

**Rättat P1 (granskning `2026-09-08-007`), två fel i v7:s förslag:**

1. **Fel namn.** `kapacitet_bindning_variant` antyder en kapacitetsbindning, men fältet
   väljer i verkligheten en variant av justeringstypen `supply_temperature_adjusted_flow`
   (en FLÖDESKORRIGERING, inte kapacitet). Döpt om till det domänriktiga
   `flodeskorrigering_variant: Literal["golvfri", "golvbegransad"]` — mirror
   `flodeskorrigeringVariant?: 'golvfri' | 'golvbegransad'` i TS. Tillagt i §6a.1s
   mappningstabell (Python-fält/JSON-namn/TS-fält/mappningsrad) tillsammans med `maxvarde`
   och de två bindningsfälten — v7:s tabell saknade denna rad helt.
2. **Ingen väg till motorn.** Verifierat att den delade fasaden (`beräkna_arskostnad_med_
   kontrakt`/`beraknaArskostnadMedKontrakt`) i dag bara bygger den numeriska
   `falt`-dictionaryn och att `faktura.py`/`fjarrvarme.ts` ALDRIG får policyn som argument —
   motorn kan alltså inte grena på en strängdiskriminator som stannar i `Tariffpolicy` och
   aldrig når fram. Löst genom en ny, explicit motorparameter:
   - `Tariffpolicy.flodeskorrigering_variant: Literal["golvfri", "golvbegransad"] | None =
     None`, satt per tariff-ID i `policyregister.py` — E.ON/Navirums åtta rader
     `"golvfri"` (`volym × base_rate × (0,02 × (Tf − 60) + 0,2)`), Kraftringen
     `"golvbegransad"` (`volym × base_rate × max(0,2; 0,2 + (Tf − 60) × 0,02)`).
   - Kontraktsfasaden (`_arskostnad_for_kontraktfasad`/`_arskostnadForKontraktfasad`, den
     interna wrapper bara `resultatkontrakt.py`/`.ts` får anropa) läser
     `policy.flodeskorrigering_variant` och skickar det vidare som en NY, valfri
     keyword-parameter `flodeskorrigering_variant` till den underliggande
     justeringsfunktionen för `supply_temperature_adjusted_flow` i `justeringar.py`
     (speglad inline i `fjarrvarme.ts`) — INTE via `falt`-dictionaryn (samma princip som
     band-ID:t i §6a.2: en diskriminator är inte ett numeriskt fält och ska aldrig försöka
     bli `float(...)`).
   - Justeringsfunktionen grenar på parametern: `"golvfri"` kör den ursprungliga formeln
     utan golv, `"golvbegransad"` kör `max(0,2; ...)`-varianten. En OKÄND eller SAKNAD
     diskriminator på en tariff vars `adjustments` faktiskt innehåller
     `supply_temperature_adjusted_flow` BLOCKERAR (`harled_resultatstatus`/en explicit
     kontroll i justeringsfunktionen) — motorn gissar aldrig vilken regel som gäller. En
     tariff UTAN den justeringstypen kräver inte fältet alls (`None` är giltigt och
     ignoreras säkert).

Minst ett golden-/gränstest per variant, inklusive Kraftringens golv vid exakt `Tf=60`
(faktorn ska vara `0,2`, av att `max(0,2; 0,2) == 0,2`, inte av en slump), ett
serialiseringsrundturstest (`policyregister.py` → genererad JSON →
`policyFranGenererad()` → `flodeskorrigeringVariant` läses tillbaka oförändrat) och ett
direkt fasadanrop som bevisar att diskriminatorn faktiskt styr vilken formelgren som körs.

### 6a.6 Jönköpings fyrvärdesval — en domänmässig allow-list (nytt P1, granskning 2026-09-08-007)

Beslutet 0/10/25/50 kr/mån utan default (§10) är rätt återgivet i v7, men v7 angav bara
UI-val och en ny justeringstyp — ingen domängrind. `KravPost` kan i dag uttrycka `minvarde`/
`maxvarde`/`heltal`, inte en DISKRET mängd tillåtna värden; ett direkt API-/fasadanrop kunde
alltså skicka t.ex. 17 kr/mån och få en beräkning, trots löftet att ett okänt värde ska
blockera. UI-begränsning är per definition inte en domängrind (den kan kringgås av vilken
annan anropare som helst), och värdet `0` måste kunna skiljas från SAKNAD indata (annars
tolkas en kund som uttryckligen valt "inget tillägg" som om fältet inte fyllts i alls).

Ny `KravPost`-fält `tillatna_varden: tuple[float, ...] | None = None` (samma mönster som
`minvarde`/`maxvarde` — mirror `tillatnaVarden?: readonly number[]` i TS). `__post_init__`/
`skapaKravPost` validerar att listan (när satt) inte är tom och att varje element är ett
ändligt tal; FÅR kombineras med `heltal` men inte meningsfullt med `minvarde`/`maxvarde`
(en explicit mängd gör ett intervall överflödigt — `__post_init__` kastar om båda är satta,
för att undvika två motsägande regler på samma fält). `harled_resultatstatus`/
`harledResultatstatus` kontrollerar, när `tillatna_varden` är satt: `post.varde in
f.tillatna_varden` (exakt medlemskap, flyttalsjämförelse mot den EXAKTA katalogsiffran —
0/10/25/50 kr har ingen avrundningsrisk) — annars `raise`/kastar, aldrig en tyst
avrundning till närmaste tillåtna värde.

**Explicit `0` skilt från saknad indata:** löses av grundarbetets `byggIndataFranPolicy`
(§6a.2) — en `IndataPost` byggs bara när `falt`-objektet FAKTISKT har en nyckel för fältet.
UI:t (`KalkylatorPage.tsx`) får därför INTE förifylla Jönköpings accessavgiftsfält med `0`
som ett vanligt formulärdefault (vilket skulle göra "inget val gjort" oskiljbart från "0
kr valt") — fältet börjar tomt/`undefined`, och en explicit `0`-knapptryckning sätter
`falt["jonkoping_accessavgift_kr"] = 0` precis som `10`/`25`/`50` skulle. Ett fortsatt tomt
val ger INGEN `falt`-nyckel, vilket `byggIndataFranPolicy` korrekt tolkar som saknad
obligatorisk indata (`blocked`), inte som "0 kr".

**Test:** samtliga fyra giltiga värden (0, 10, 25, 50) räknar; tomt/saknat blockerar (saknad
`IndataPost`); 17 kastar (`harled_resultatstatus`); negativa och icke-ändliga värden kastar
(befintlig `_validera_varde`, oförändrad); ett uttryckligt `0`-val ger `complete`, inte
`blocked` (bevisar att `0` inte feltolkas som frånvaro). Kontraktsfilerna
(`resultatkontrakt.py`/`.ts`, `policyregister.py`, `KalkylatorPage.tsx`) läggs i batch 5b:s
fillista (`batchplan-v9.md`), där Jönköpings basrad redan ligger.

## 7. Livscykel för `remaining_information_requests` som berör `ready`-raderna (granskning 2026-09-08-005/-006/-007, P1)

**Vald representation, rättad för att matcha en körbar `grind()`-signatur (granskning
`2026-09-08-006`, P1):** v6:s förslag behöll `grind(tariff, utredda)` samtidigt som det
introducerade en separat `oppna_tariff_ider(katalog)`-funktion `grind()` inte själv kunde
anropa eller skilja tariff-ID:n från medlems-ID:n i. Löst genom att göra UPPLÖSNINGEN till
ett steg FÖRE grindanropet, inte en del av grindens egen signatur:

`remaining_information_requests` i katalog-JSON:et får ett NYTT, valfritt fält
`tariff_ids: list[str] | null` VID SIDAN AV det befintliga `member_ids`. En ny funktion
`blockerade_tariff_ider(katalog) -> set[str]` (ersätter `utredda_medlemmar()`, körs EN gång
per `godkanda()`/preflight-anrop, inte per tariff) itererar samtliga requests och bygger EN
platt mängd tariff-ID:n: för en request med `tariff_ids` satt läggs EXAKT de angivna
ID:na till; för en request UTAN `tariff_ids` (bakåtkompatibelt, medlemsomfattande) expanderas
`member_ids` till samtliga tariff-ID:n den/de medlemmarna har i katalogen VID
LADDNINGSTILLFÄLLET. Resultatet är EN mängd av bara tariff-ID:n, aldrig en blandning av
tariff- och medlems-ID:n. `grind()`s signatur byts till `grind(tariff: dict, blockerade:
set[str]) -> str | None` (§6, steg 2), och dess enda jämförelse blir `tariff.get("id") in
blockerade` — en enda, entydig strängjämförelse, ingen specialkod för att skilja ID-typer
åt. Samma representation används för SAMTLIGA 14 requests nedan — inget "eller", ingen
`oppna_tariff_ider`/`grind()`-signaturkrock kvar i arbetsordern.

Katalogen har 14 `remaining_information_requests` totalt. De 10 nedan berör minst en av de
45 `ready`-raderna — övriga 4 (R02, R07, R08, R09) gäller enbart redan
`blocked_external_info`-tariffer och rörs inte av denna etapp.

| ID | Medlem(mar) | Fråga | Disposition (EN livscykel per request) | Motivering |
|---|---|---|---|---|
| R03 | `malarenergi` | Vilka nät hör sidans två olika tabeller till? Bekräfta fast avgift 2217/2117 för 25–79 kW samt sommarperiod/flödesvillkor. | **`tariff_ids` sätts** till de två `blocked_external_info`-tarifferna (`storre-fastigheter`, `gruppanslutna-smahus`) | `24-lagenheter` har ingen kapacitetsdel och ingen effekt-/avgiftstvetydighet — request-posten begränsas till de tariff-ID:n frågan faktiskt gäller, `member_ids` tas bort från posten samtidigt. |
| R04 | `borlange-energi` | Bekräfta september–oktober 559 kr/MWh och vilken effektgrupp exakt 501 kW tillhör. | **TAS BORT** | Höstpriset är verifierat; 501 kW-gränsen löses av `supplier_confirmed_band_id` (§6a.2), inte av request-processen. |
| R05 | `c4-energi` | Vilken prisgrupp gäller exakt 500 kW? | **TAS BORT** | Löses av `supplier_confirmed_band_id` (§6a.2). |
| R06 | `kraftringen` | Hur används temperaturens korrigeringsfaktor på flödespriset? Behöver explicit slutformel samt effektprisets tidsenhet och periodisering. | **TAS BORT** | Formeln är källverifierad (verifieringslistan, golv vid 0,2) och effektprisperioden rättas i katalogen (`rate_period: year`) — frågan är besvarad. |
| R10 | `e-on-jarfalla, e-on-malmo, navirum-energi-norrkoping-och-soderkoping, navirum-energi-orebro-kumla-och-hallsberg` | Aktuell prisbilaga och särskilda prisvillkor: effektprisets periodisering och temperaturkorrigerat flödespris. | **TAS BORT** | Samtliga fyra medlemmars enda tariffer är `ready_to_implement`; periodiseringen rättas i katalogen (`rate_period: month`) och flödesformeln är källverifierad (§6, batch 3). Ingen `tariff_ids`-begränsning behövs — alla berörda produkter blir redo samtidigt. |
| R11 | `telge-nat` | Fullständig villkorsbilaga som gäller tillsammans med 2026 års prislista, alternativt bekräftelse att tillsvidarevillkoren i 2025-bilagan fortsatt gäller. | **TAS BORT** | Verifieringslistan bekräftar redan att tillsvidarevillkoren gäller — frågan är redan besvarad, katalogens kontroll-issue är inaktuell. |
| R12 | `temab-fjarrvarme` | Kategorital och historik bakom debiteringseffekten, om Optimate ska beräkna den själv; annars räcker leverantörens debiterbara effekt. | **TAS BORT** | Löses av den normaliserade issue-texten (leverantörens fakturavärde används, ingen egen beräkning). |
| R13 | `soderhamn-nara` | Byggnadstypens omräkningsindex, om Optimate ska beräkna effekten själv; annars leverantörens debiterbara effekt. | **TAS BORT** | Tariffen passerar redan grinden idag — leverantörens debiterbara effekt används, ingen egen beräkning. |
| R14 | `sundsvall-energi` | Leveransvillkor för abonnemang från 2000 kW i Sundsvall/Matfors. Krävs endast för kunder i dessa grupper. | **`tariff_ids` sätts** till de två `blocked_external_info`-tarifferna (`sundsvall-normal`, `matfors-och-kvissleby`) | `indal-liden-och-lucksta` (ren energitariff, ingen effektdel alls) är inte berörd av frågan — request-posten begränsas, `member_ids` tas bort samtidigt. |
| R15 | `falu-energi-vatten` | Prisgrupp över 500 kW i Bjursås, Grycksbo, Sundborn eller Svärdsjö, endast om sådana kunder ingår. | **TAS BORT** | Löses mekaniskt av `KravPost.maxvarde=500` på ytterorternas rad (§6a.1). Falun berörs inte och har ingen egen öppen fråga. |

**Sammanfattning:** 8 förfrågningar (`R04, R05, R06, R11, R12, R13, R15`, plus R10 utan
begränsning) TAS BORT helt — deras frågor är redan besvarade av verifieringslistan eller
löses mekaniskt av ett nytt kontraktsfält (§6a), inte av request-processen. 2 förfrågningar
(`R03, R14`) FÅR `tariff_ids` satt till exakt de `blocked_external_info`-tariffer frågan
gäller, så `blockerade_tariff_ider(katalog)` (**rättat P2, granskning `2026-09-08-007`**: v7
skrev av misstag kvar det borttagna v6-namnet `oppna_tariff_ider()` här — den faktiska
funktionen är `blockerade_tariff_ider()`, se §7:s inledning) aldrig råkar exkludera en
produkt som ska förbli redo — samma representation, inget "delas eller läggs till" kvar som
öppet val.


## 8. Räkningskontroll

| Disposition | Bastariffer (§3–4) | Varianter (§5) | Summa |
|---|---:|---:|---:|
| `implemented_source_verified_annual` | 7 | 0 | 7 |
| `ready_to_implement` | 45 | 10 | 55 |
| `blocked_external_info` | 26 | 4 | 30 |
| `not_applicable` | 0 | 0 | 0 |
| **Summa** | **78** | **14** | **92** |

**Oförändrat i v8/v9 (granskning `2026-09-08-007`/`-008`):** enbart tekniska
kontraktsrättningar (aktiveringsordning, värdetyp/kardinalitet, produktingång/UI-metadata,
Stockholm-dispatch/adapterpreflight/serier, Kraftringens motorväg, Jönköpings allow-list) —
ingen post flyttar mellan dispositioner i någon av de två rundorna. 7 + 55 + 30 = 92
oförändrat, precis som respektive gransknings egen instruktion föreskrev (v8-rundans punkt
7, v9-rundans punkt 7).

**Rättat i v7 (granskning `2026-09-08-006`, Codex/Roberts beslut):** Jönköpings
accessavgiftsvariant flyttad från `blocked_external_info` till `ready_to_implement` (§5) —
varianternas fördelning ändras från 9/5 till 10/4, totalen 14 variant-ID:n oförändrad.
Verifierat: 7 + 55 + 30 = 92, och 78 (bas) + 14 (variant) = 92.

Rättat i v4 (granskning `2026-09-08-003`, P1/P2): Finspångs spetsvärmetillägg flyttad från
`ready_to_implement` till `blocked_external_info` (utlösningsvillkoret inte kartlagt, se §5).

**Oförändrat i v5/v6 (granskning `2026-09-08-004`/`-005`):** v5 lade till en verklig, körd
grindpreflight (§6) och fördjupade obligatorisk-indata-/motorbedömningar för 16 av de 45
`ready`-raderna. v6 bytte grind-only-preflighten mot en fyrstegs sammansatt
aktiveringspreflight, specificerade fyra konkreta kontraktstillägg (§6a) och bytte
requestens datastruktur till `tariff_ids` (§7). Ingen av dessa två rundor flyttade någon
post mellan dispositioner — bara v7:s Jönköping-beslut ändrar räkningen sedan v4.

**Modell för kontrollmängden, uttryckligt (granskning 2026-09-08-003, P2):** kontrollmängden
är **78 bastariffer + 14 räknade varianttäckningskrav = 92**, inte 78 fristående produkter.
En variant byggs ofta i SAMMA implementationscommit som sin bastariff (t.ex. Borås
miljötillägg i batch 6) — det är en räknad TÄCKNINGSKRAV, inte en andra, fristående tariff.
Batch 6:s tabellrad i `batchplan-v4.md` visar därför uttryckligen "2 bastariffer + 1
varianttäckning", inte "2 tariffer", för att undvika att miljötillägget räknas två gånger
eller inte alls (v3:s batchsumma 54 i stället för 55 berodde exakt på denna otydlighet).

Rättat i v3 (granskning `2026-09-08-002`): Eskilstuna flyttad från `ready_to_implement` till
`blocked_external_info` (P1 — nätreferensen inte verifierad, se §4.2). Samtliga sju
variantfamiljer (14 variant-ID:n, se §5) är nu räknade i totalen i stället för att stå
utanför den — kontrollmängden är därför nu **92 räknade enheter**, inte 78.

**Härledning av 79 unika råenheter innan variantutbrytningen (oförändrad från v2):** 78
katalograder + 1 separat förvaltad leverantörsfil (Stockholm Exergi, samma produkt som
katalograden, räknas en gång) + 1 separat förvaltad schablonfil (Riksgenomsnittet, §9,
`not_applicable`) = 80 råa kontrollposter → 79 unika enheter = 78 tariffprodukter + 1
syntetisk schablon. Variantutbrytningen i §5 lägger sedan till 14 räknade variant-ID:n
UTAN att ändra denna 79-härledning — varianterna är delar av redan räknade bastariffer, inte
nya råa katalogposter.

**Leverantörer vs. tariffprodukter (oförändrat från v2):** katalogens 53 `members`-poster
inkluderar redan Stockholm Exergi. **53 fjärrvärmeleverantörer + 1 syntetisk
schablonentitet** (Riksgenomsnittet) = 54 unika leverantörsentiteter, inte 55.

**Dubbletter funna:** exakt en — Stockholm Exergis katalograd mot dess leverantörsfil
(räknas EN gång, som `ready_to_implement`, se §4.1).

## 9. Syntetiska schabloner (separat tabell, inte tariffprodukter)

| Post | Källa | Vad den är | Motivering till `not_applicable` |
|---|---|---|---|
| Riksgenomsnittet | `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md`, Nils Holgersson-rapporten 2025 | Syntetisk nationell schablon som används när ingen namngiven leverantör är vald eller känd | Inte ett tariffprodukt att implementera — en beräkningsmekanism för det generiska fallet. Se produktdirektivets öppna beslut ([PROJECT_CHARTER §8](../PROJECT_CHARTER.md)) om hur den ska presenteras när en namngiven leverantör saknas: som ett tydligt märkt separat val, inte tyst som om den vore leverantörens egen tariff. |

## 10. Öppna frågor till Codex/Robert

**v7:s runda (granskning `2026-09-08-006`) lämnade inga nya öppna frågor, och v8:s runda
(granskning `2026-09-08-007`) var uteslutande tekniska kontraktsfynd — Codex instruerade
uttryckligen att inga nya Robert-beslut behövs för dem (rättningsbeställning, punkt 7). De
fyra frågorna v6 lämnade öppna är besvarade av Codex i granskning `2026-09-08-006`s avsnitt
"Beslut på V6:s öppna frågor" och tillämpade rakt av, oförändrat i v8:**

1. **Jönköpings accessavgift:** Roberts redan beslutade mål (samtliga möjliga tariffer ska
   implementeras) omfattar en fakturerbar, källkänd, kundkänd avtalsuppgift. Modellerad som
   ett synligt, obligatoriskt kundval på Jönköpings basprodukt (0/10/25/50 kr/mån, inget
   standardvärde, okänt val blockerar), ingen dubblettprodukt. **Beslut tillämpat:** flyttad
   till `ready_to_implement`, se §5 och §8:s uppdaterade räkning (7/55/30 av 92).
2. **E.ON/Navirums batch 3b-ordning:** godkänd oförändrad — en egen, mindre delbatch EFTER
   batch 3:s grundformel.
3. **Batch 5-uppdelningen** (5a/5b/5c): godkänd som rätt arbetsstorlek, men UNDER
   FÖRUTSÄTTNING att det gemensamma bandkontraktet (§6a.2) specificeras för samtliga
   berörda produkter FÖRST. **Beslut tillämpat:** §6a.2 specificerar nu bandkontraktet för
   alla 42 berörda rader innan batch 5 kan starta.
4. **Kraftringens parametriserade motortyp:** godkänd, UNDER FÖRUTSÄTTNING att
   regelvarianten är en explicit, typad diskriminator (inte implicit härledd från
   leverantörs-ID). **Beslut tillämpat:** §6a.5 specificerar det domänriktigt namngivna
   `flodeskorrigering_variant`-diskriminatorn (**rättat P2, granskning `2026-09-08-008`**:
   denna rad hade fortfarande kvar det gamla, missvisande namnet `kapacitet_bindning_variant`
   trots att §6a.5 redan bytt namn — synkroniserat).

Samtliga öppna frågor från v1–v5 är besvarade av Codex i granskningarna `2026-09-08-001`
till `-005` och tillämpade rakt av i tidigare versioner: Vattenfall helt `blocked` som grupp
(batch 8), Sundsvall Matfors följer teknisk-kartläggning v4, leverantörsvärde-mönstret
kräver tariffvis kontroll av VARJE prisdel (genomfört i §4), kända specialvarianter får
aldrig bli `not_applicable` (genomfört i §5 — samtliga 14 integrerade), och E.ON/Navirums
36-månadersmetod är korrekt beskriven som ett dygnsmedeleffekt-leverantörsvärde (§5).

**Ingen ny öppen fråga identifierad i v8-rundan.** Samtliga P1-fynd i granskning
`2026-09-08-007` var körbarhets-/typningsfel i redan beslutade kontraktsdesigner — inga nya
sakfrågor för Robert.
