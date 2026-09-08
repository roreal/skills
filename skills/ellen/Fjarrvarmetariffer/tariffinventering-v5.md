# Tariffinventering v5.0 — fullständig kontrollmängd för kalkylator v1

Upprättad 2026-09-08 av Claude. Ersätter `tariffinventering-v4.md` i sin helhet (v4 ändras
INTE i efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-08-004](../conversations/reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v4.md)
(`status: changes-required`, supersedes `2026-09-08-003`) av v4. Ingen produktkod, tariffdata
eller genererad fil är ändrad av detta dokument.

**Vad som är nytt i v5, i korthet** (se granskning `2026-09-08-004` för fullständig
motivering till varje punkt):

1. **Grindpreflight FAKTISKT KÖRD, inte bara påstådd** (§6): `tools.tariffer.katalog.grind()`
   kördes mot en minneskopia av alla 45 `ready`-rader. Före v5:s rättningar: 21/45 passerar
   (identiskt med Codex tabell). Efter v5:s föreslagna rättningar: 45/45 passerar. 13 av de
   45 raderna hade en ANDRA, tidigare dold blockerare bakom den Codex tabell visade som
   första ledet — upptäckt genom att faktiskt köra grinden på nytt efter varje delrättning,
   inte bara läsa av det första stoppet.
2. **Katalogrättelser specificerade för E.ON/Navirum (8), Kraftringen och Kils**: `fixed:
   null`/`rate_period: null` → explicita värden (`fixed: 0`, `rate_period: "month"` för
   E.ON/Navirum, `"year"` för Kraftringen), med golden-test mot en 12×-periodiseringsrisk.
3. **Umeå fick sin saknade kapacitetsfaktor `B`**: v4 nämnde bara den nya flödesjusteringen.
   `B` (leverantörens egna piecewise-multiplikator) blir ett fjärde obligatoriskt
   leverantörsvärde, med en ny `post_multiplier`-medveten kapacitetsmotor — `grind()` avvisar
   annars posten oavsett övriga fält.
4. **Stockholm Exergis årsväg fick en namngiven adapter**, inte bara "motorn finns redan":
   `monthly_with_peak_volume_replacement` är ingen allmänt godkänd energiform — lösningen
   binder katalog-ID:t explicit till den redan fakturavaliderade leverantörsspecifika
   beräkningsvägen.
5. **Livscykel för samtliga fem okända `issues` och 10 av 14 `remaining_information_requests`**
   (§7): varje normaliseras, tas bort eller DELAS — två förfrågningar (R03, R14) täckte
   tidigare både en `ready`-rad och en fortsatt blockerad rad hos samma medlem och måste
   delas per tariff-ID, inte tas bort helt.
6. **Känd metodavvikelse dokumenterad:** Lidköpings två tariffer (`blocked_external_info`)
   passerar `grind()` mekaniskt redan idag, men förblir korrekt blockerade — en verklig
   priskomponent (flödesprisfaktor N, nätmedelvärde Tm) saknas helt ur JSON-strukturen och
   syns därför aldrig för grinden. `grind() is None` är nödvändigt men inte tillräckligt.
7. **`source_id` + direkt officiell länk på samtliga 14 varianter** (§5) — fyra rader som
   tidigare skrev "samma URL som ovan" har nu URL:en utskriven direkt; Finspångs, Södertörns
   och Borås variantkällor rättade från 2025- till 2026-dokument.
8. **Räknefel rättat:** v4:s egen text påstod "sex bastariffrader" rättade men listade i
   själva verket nio (E.ON Järfälla ×2, E.ON Malmö ×2, Navirum ×4, VänerEnergi ×1 = 9) —
   samma miskategorisering fanns i leveransrapporten. Denna sida är den korrigerade
   källan; sessionsloggens äldre felskrivning lämnas oförändrad som historik med en daterad
   rättelse i dess ändringslogg, i stället för att tystas ändras i efterhand.
9. **Dokumentationscommitten görs självbärande** mot den incheckade `index.md`: båda
   tariffgranskningarna (`2026-09-08-003`, `2026-09-08-004`) spåras nu i git.

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
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
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
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py/adjustments.ts innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
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
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py/adjustments.ts innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
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
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py/adjustments.ts innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
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
- **Obligatorisk indata:** Debiterbar effekt (kW), förbrukningsvägd MÅNADSMEDEL-framledningstemperatur `Tf` (°C, fakturan/nätdata — formeln själv använder `Tf` varje månad, inte bara flödet) OCH flöde (m³, fakturan). Formeln `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)` känd (katalog); Brunnshögs nätdel är en EGEN VARIANT, se särfallstabellen — endast ordinarie nät ingår här.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Kraftringen — samma motortyp som E.ON/Navirum
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` — SAMMA ej implementerade motortyp som de åtta E.ON/Navirum-tarifferna. Bör byggas i SAMMA batch/commit som dem, inte separat i "leverantörsvärde utan nytt motorarbete" som v1 felaktigt antog. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1): `fixed: null` och `rate_period: null` — verifieringslistan anger redan `fixed: 0`, `rate_period: "year"`; sätt båda explicit. Golden-test: ett handräknat helår bekräftar att kapacitetsdelen inte periodiseras om (year, ingen ×12) och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Nätavgränsning, effektprisperiod och flödeskorrektion behöver bekräftas..." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden.
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
- **Obligatorisk indata:** `monthly_invoice`-kontraktet (kall energi, returtemp, debiterbar effekt) är redan implementerat och fakturavaliderat (18 fakturor, granskning `2026-09-06-003`) MED ett explicit period-/upplösningskontrakt: returtemperatur krävs bara november–mars (5 vintermånader, `tillampliga_manader`), kall energi krävs samtliga 12 månader. Kalkylatorns ÅRSPROGNOS saknar dock motsvarande kontraktsbindning idag och anropar motorn utan dessa värden alls. VALT KONTRAKT (rättat i v5, granskning 2026-09-08-004, P1): namngiven adapter, INTE en generell motorutökning för `monthly_with_peak_volume_replacement` — energiformen är unik för Stockholm Exergi i hela katalogen, så en generell motorkapacitet skulle byggas för en enda tariff. `annual_forward`-fasaden binds explicit till samma redan fakturavaliderade leverantörsspecifika beräkningsväg (`_stockholm_exergi_policy`-mönstret i `policyregister.py`) i stället för den generella `selected_band_affine`-katalogmotorn — grinden får ett namngivet undantag för just detta katalog-ID, inte en ny godkänd energiform i `FAS1_ENERGIFORMER`.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Stockholm Exergi — egen kontraktsväg via namngiven adapter, ej Sandviken-mönstret och ej den generella katalogmotorn
- **Kvarstående arbete (preciserat i v5):** Berörda filer: `resultatkontrakt.py`/`.ts` (ny `berakna_arskostnad_med_kontrakt`-anropspunkt för denna adapter), `policyregister.py` (utöka `_stockholm_exergi_policy` med `annual_forward` i `tackning`), `katalog.py` (namngivet undantag för `stockholm-exergi-stockholm-exergi-normal-2026` som kringgår den generella energiforms-kontrollen och i stället kräver adaptern). Årsindata: kall energi 12 månader, returtemp nov–mar (5 månader), debiterbar effekt — samma tre fält och period-/upplösningskontrakt som `monthly_invoice`. Bygg ett eget källverifierat årsreferensfall för `annual_forward` (motsvarande Sandvikens granskningskedja `2026-09-06-004`→`2026-09-07-003`). Regressionstest: `monthly_invoice`-kontraktet och dess 18 fakturarader rörs inte och ger identiskt resultat före/efter adapterns tillägg. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering (nästa blockerare bakom `energiform`, inte synlig i granskning 2026-09-08-004:s förstaledsanalys): `issues`-texten "Förtydligande av prisvillkor 2026 finns. Tvådelad prognos och alternativa vinterregler återstår..." är redan självlöst — texten medger själv att "leverantörens effektvärde och -3 °C-gränsen kan användas som kundindata", samma leverantörsvärde-mönster adaptern redan bygger på. TA BORT issue-raden.
- **Disposition:** `ready_to_implement`


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
- **Inmatningslägen:** mwh, kr OCH schablon — alla tre (rättat i v4, granskning 2026-09-08-003, P2: denna tariff aktiveras via den befintliga `EJ_TILLAMPLIG_KAPACITETSFORM`-mekanismen, INTE Sandviken-kontraktsmönstret — den blir aldrig kontraktsgated (`_kraver_kontrakt` sätts inte), utan går på samma legacy-väg som de sex redan godkända legacy-tarifferna i §3, som redan stödjer alla tre lägen. §2:s generella regel om blockerat kr/schablon gäller bara `ready_to_implement`-tariffer som BLIR kontraktsgated via `POLICYREGISTER` — inte denna.)
- **Tariffamilj/adapter:** Ren energitariff — engångsjustering, legacy-väg (ej kontraktsgated)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1: medlemsomfattande informationsförfrågan saknade livscykel):** Sätt `capacity.type: "not_applicable"` på katalograden. Mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp 1–4 (2026-09-04), bara inte aktiverad mot denna rad. INFORMATIONSFÖRFRÅGAN R14 (medlem `sundsvall-energi`) SKA DELAS, INTE TAS BORT: dess text ("Leveransvillkor för abonnemang från 2000 kW i Sundsvall/Matfors") gäller uttryckligen bara `sundsvall-energi-sundsvall-normal-2026` och `sundsvall-energi-matfors-och-kvissleby-normal-2026` (båda `blocked_external_info`, Matfors hålls blockerad per granskning 2026-09-08-003 följd av teknisk-kartläggning v4) — INTE Indal/Liden/Lucksta. Omskopa R14 till just de två Sundsvall/Matfors-tariffernas ID:n (eller lägg till ett `tariff_ids`-fält i stället för det medlemsomfattande `member_ids`) så `utredda_medlemmar` aldrig felaktigt fångar denna rad. Grindtest: `grind()` på Indal/Liden/Lucksta ska passera med tom `utredda`-mängd EFTER denna omskopning, medan Sundsvall-normal/Matfors fortsatt ger `utreds (medlem)`.
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
- **Obligatorisk indata (rättat i v5, granskning 2026-09-08-004, P1: v4 saknade kapacitetsfaktorn helt):** Debiterbar effekt (kW), flöde okt–apr (m³, fakturan, `asymmetric_flow_difference`), OCH kapacitetsfaktorn `B` — katalogens `post_multiplier` är en piecewise-formel av kvoten `U = normalårskorrigerad_energi_dec_jan_feb / energi_sep_apr`, men bolagets normalårskorrigering är INTE publicerad, så `U` kan inte räknas ut ur rå mätdata. Valt kontrakt: leverantörens EGET redan beräknade `B`-värde (fakturan/leverantörsbesked) tas emot som ett fjärde obligatoriskt leverantörsvärde — INGEN kalkylatorberäkning av `U`/`B` från energidata. `Tariffpolicy.kapacitet_bindning` binder `billing_basis` (leverantörens årseffekt, samma effektsignaturmönster som huvudfallets `A`), och `B` binds som en separat, ny multiplikatorbindning.
- **Inmatningslägen:** mwh (samtliga fyra fält krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Umeå — ny motortyp `asymmetric_flow_difference` OCH en ny, typad `post_multiplier`-medveten kapacitetsmotor (till skillnad från Vattenfall: statisk flödesreferens, men Vattenfall saknar denna kapacitetskomplikation helt)
- **Kvarstående arbete (utökat i v5):** (1) `asymmetric_flow_difference` finns INTE i JUSTERINGSTYPER — byggs separat från Vattenfalls blockerade variant av samma typnamn (Umeås formel är komplett och byggbar, Vattenfalls är det inte). (2) NY kapacitetsmotor som accepterar `post_multiplier` som ett bundet leverantörsvärde `B` i stället för att grinden avvisar posten (`kapacitetsformel med multiplikator`) — `grind()` måste ändras så en tariff med `post_multiplier` GODKÄNNS när `B` är deklarerat som ett obligatoriskt, källkänt `Tariffpolicy`-fält, inte en dold motorgissning. (3) Handräknade testfall för minst tre `U`-intervall (piecewise-gränserna 0,300/0,500/0,800) som bevisar att kalkylatorn ALDRIG härleder `B` själv utan alltid använder det inmatade leverantörsvärdet. (4) YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Hela effektkostnaden multipliceras med B; gränser och normalårskorrigering måste mappas. Andra avtalsalternativ ingår inte." är fullt löst av A/B-leverantörsvärdekontraktet ovan — TA BORT issue-raden.
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
| `jonkoping-energi-jonkoping-och-granna-2026--accessavgift` | `jonkoping-energi-jonkoping-och-granna-2026` | `16_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Jonkoping-Energi-2025-till-2026-Prisandringsmodell.pdf) | Avtalsberoende accessavgift (0/10/25/50 kr/mån) — beror på det enskilda avtalet, inte en publicerad allmän regel | Okänt tills Robert beslutar om kundformulärfält eller permanent uteslutning | samtliga blockerade | Ej batchad | `blocked_external_info` — VÄNTAR PÅ ROBERT-BESLUT (produktbeslut, inte källfråga): ska accessavgiften bli ett kundformulärfält (kunden anger sitt avtalade belopp) eller uteslutas permanent ur produkten? Claude får inte avgöra detta själv. |
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026--miljotillagg` | `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | `borasem-2026` (https://borasem.se/webb/foretag/fjarrvarme/priserochvillkor2026.4.3b2618bc1976272a99c471fd.html) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 | Miljötillägget "Bra Miljöval" (31 SEK/MWh) — ett kundvalt UI-tillval, inte en automatisk prisdel | Kryssruta/kundval i UI, inget nytt fält utöver bastariffens | mwh; kr/schablon blockerade | 6 (samma batch som grundformeln — se §8:s räkningsnot om hur denna variant räknas separat trots att den byggs i samma commit) | `ready_to_implement` |

**14 variant-ID:n totalt, rättat i v4:** 9 `ready_to_implement` (åtta E.ON/Navirum-varianter,
Borås tillägg), 5 `blocked_external_info` (Södertörn, Kraftringen Brunnshög, Tekniska Verken
Linköping lågtemperatur, Jönköping accessavgift, Finspångs spetsvärmetillägg — flyttad från
`ready` i v4). Jönköpings variant väntar uttryckligen på ett Robert-BESLUT, inte bara ett
leverantörssvar — se öppen fråga 1 nedan.

## 6. Grindpreflight — samtliga 45 `ready`-ID:n (granskning 2026-09-08-004, P1)


Verifierat genom att FAKTISKT KÖRA `tools.tariffer.katalog.grind()` (enkey-agents@fd8f8da) mot en minneskopia av varje rad, med `investigation.status` simulerat löst och en tom `utredda`-mängd — samma metod Codex använde i granskning `2026-09-08-004`. Ingen katalogfil eller kod ändrades; detta är en läsning, inte en aktivering.


**Resultat FÖRE v5:s föreslagna rättningar: 21/45 passerar** (identiskt med Codex tabell). **Resultat EFTER v5:s föreslagna rättningar, applicerade på en skrivskyddad minneskopia: 45/45 passerar.** De 26 blockerade bastarifferna och de 5 blockerade varianterna kontrollerades separat (oförändrade, utan v5:s rättningar) och ger fortsatt grindstopp — UTOM en känd, avsiktlig avvikelse: se anmärkningen efter tabellen.


| Tariff-ID | Dagens grindorsak (första ledet) | Planerad åtgärd | Berörd fil | Förväntad slutstatus |
|---|---|---|---|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | kapacitetsform | Ny kapacitetsform `heterogeneous_bands` + ny justeringstyp `optional_environmental_addon` (kundvalt UI-tillval) | katalog.py (grind), justeringar.py/.ts, KalkylatorPage.tsx (kryssruta) | grind() None |
| `borlange-energi-borlange-2026` | okänd issue (501 kW) | Normalisera issue till känd typ; TA BORT R04 | katalog-JSON (issues), remaining_information_requests | grind() None |
| `c4-energi-kristianstad-2026` | okänd issue (500 kW) | Normalisera issue till känd typ; TA BORT R05 | katalog-JSON (issues), remaining_information_requests | grind() None |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | null i band | fixed:0, rate_period:month; TA BORT normaliserad issue; ny `supply_temperature_adjusted_flow`-motor; SPLITTA R10 | katalog-JSON, justeringar.py/.ts, policyregister.py, remaining_information_requests | grind() None |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | null i band | Samma som Järfälla bostäder | samma | grind() None |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | null i band | Samma + Malmö/Burlöv −15→−8 °C rättelse (redan i v4) | samma | grind() None |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | null i band | Samma | samma | grind() None |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | okänd issue (>500 kW) | Normalisera issue (fail-closed cap); SPLITTA R15 (behåll för falu-ytterorter borttagen, ej relevant för Falun) | katalog-JSON, remaining_information_requests | grind() None |
| `falu-energi-vatten-falun-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `finspangs-tekniska-verk-finspang-2026` | kapacitetsform | Ny kapacitetsform `piecewise_polynomial` + ny justeringstyp `conditional_flow` | katalog.py, justeringar.py/.ts | grind() None |
| `habo-energi-habo-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | okänd justeringstyp | Ny justeringstyp `flow_difference` | justeringar.py/.ts | grind() None |
| `jamtkraft-brunflo-och-opevagen-2026` | okänd justeringstyp | Samma | samma | grind() None |
| `jamtkraft-ostersund-froson-as-2026` | okänd justeringstyp | Samma | samma | grind() None |
| `jonkoping-energi-jonkoping-och-granna-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `karlstads-energi-karlstad-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `kils-energi-kil-2026` | null i band | fixed:0 på alla fyra band; TA BORT normaliserad issue | katalog-JSON | grind() None |
| `kraftringen-kraftringen-2026` | null i band | fixed:0, rate_period:year; TA BORT normaliserad issue; delad `supply_temperature_adjusted_flow` MED golv | katalog-JSON, justeringar.py/.ts, policyregister.py | grind() None |
| `lulea-energi-lulea-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `mjolby-svartadalen-energi-mjolby-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | null i band | Samma som E.ON | samma | grind() None |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | null i band | Samma | samma | grind() None |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | null i band | Samma | samma | grind() None |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | null i band | Samma | samma | grind() None |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `oresundskraft-angelholm-normal-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `oresundskraft-helsingborg-normal-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `ovik-energi-ornskoldsvik-2026` | null i band | fixed:0 på alla band, monthly_proration→kalenderdagsviktning (redan i v4); TA BORT normaliserad issue | katalog-JSON | grind() None |
| `partille-energi-partille-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `piteenergi-norrfjarden-och-sjulnas-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `piteenergi-pitea-centrala-natet-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `skovde-energi-skovde-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `stockholm-exergi-stockholm-exergi-normal-2026` | energiform | Namngiven adapter (ej generell motor); TA BORT normaliserad issue; eget källverifierat årsreferensfall | resultatkontrakt.py/.ts, policyregister.py, katalog.py (namngivet undantag) | grind() None via adapter |
| `sundsvall-energi-indal-liden-och-lucksta-2026` | kapacitetsform | `capacity.type: "not_applicable"` (redan byggd mekanism); SPLITTA R14 (behåll för Sundsvall-normal/Matfors) | katalog-JSON, remaining_information_requests | grind() None |
| `tekniska-verken-katrineholm-katrineholm-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `tekniska-verken-linkoping-linkoping-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | okänd issue (inaktuell) | TA BORT issue helt (redan besvarad); TA BORT R11 | katalog-JSON, remaining_information_requests | grind() None |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | okänd issue | Normalisera issue; TA BORT R12 | katalog-JSON, remaining_information_requests | grind() None |
| `trollhattan-energi-trollhattan-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |
| `umea-energi-umea-enkel-2026` | kapacitetsformel med multiplikator | Ny `post_multiplier`-medveten kapacitetsmotor, A/B leverantörsvärde; TA BORT normaliserad issue; ny `asymmetric_flow_difference` | katalog.py (grind), faktura.py/fjarrvarme.ts, justeringar.py/.ts, policyregister.py | grind() None |
| `vanerenergi-mariestad-och-toreboda-2026` | passerar redan idag | Ingen — leverantörsvärde-mönstret räcker (bekräftat: grind() None redan med investigation.status simulerat löst och tom utredda-mängd) | policyregister.py (ny policy, inget motorarbete) | grind() None (oförändrat) |

**Metodnot, upptäckt av v5:s egen körning (inte synlig i Codex förstaledsanalys):** att lösa den FÖRSTA grindorsaken avslöjar ibland en ANDRA, tidigare dold bakomliggande orsak — 13 av de 45 raderna hade en YTTERLIGARE `okänd issue`- eller `okänd justeringstyp`-blockering bakom den förstnämnda (t.ex. samtliga åtta E.ON/Navirum-rader hade, utöver `null i band`, en andra issue-text om effektprisperiod/flödeskorrigering). v5:s per-tariffrader ovan (§4.1) och tabellen här är uppdaterade för BÅDA ledden, inte bara det Codex tabell råkade visa som första stopp.


**Känd avvikelse (Lidköping, INTE en del av de 45):** `lidkoping-energi-lidkoping-041-kw-2026` och `-42-kw-2026` (`blocked_external_info`, §4.2) passerar MEKANISKT `grind()` redan idag när `investigation.status` simuleras löst — deras `issues`-texter matchar redan kända, godkända mönster. De förblir ändå korrekt blockerade i denna inventering: den publika källan saknar HELT 2026 års flödesprisfaktor N och nätmedelvärde Tm — ett verkligt prissättande fält som aldrig kodats som en `adjustments`-post i katalogen och som grinden därför strukturellt inte kan upptäcka. Detta visar att `grind() is None` är NÖDVÄNDIGT men INTE TILLRÄCKLIGT för `ready_to_implement` — en tariff kan mekaniskt passera grinden medan en verklig priskomponent saknas helt ur JSON-strukturen. Lidköping stannar `blocked_external_info` av detta skäl, ett mänskligt omdöme grinden inte kan ersätta.


## 7. Livscykel för `remaining_information_requests` som berör `ready`-raderna (granskning 2026-09-08-004, P1)


Katalogen har 14 `remaining_information_requests` totalt. De 10 nedan berör minst en av de 45 `ready`-raderna — övriga 4 (R02, R07, R08, R09) gäller enbart redan `blocked_external_info`-tariffer och rörs inte av denna etapp.


| ID | Medlem(mar) | Fråga | Disposition | Motivering |
|---|---|---|---|---|
| R03 | `malarenergi` | Vilka nät hör sidans två olika tabeller till? Bekräfta fast avgift 2217/2117 för 25–79 kW samt sommarperiod/flödesvillkor. | **DELAS** | Gäller uttryckligen `storre-fastigheter`/`gruppanslutna-smahus` (båda `blocked_external_info`), inte `24-lagenheter` (ingen kapacitetsdel, ingen effekt-/avgiftstvetydighet). Omskopa till de två övriga Mälarenergi-ID:n. |
| R04 | `borlange-energi` | Bekräfta september–oktober 559 kr/MWh och vilken effektgrupp exakt 501 kW tillhör. | **TAS BORT** | Höstpriset är verifierat (källgranskad); 501 kW-gränsen löses av den normaliserade issue-texten (leverantörens fakturavärde, ej automatisk gruppindelning). |
| R05 | `c4-energi` | Vilken prisgrupp gäller exakt 500 kW? | **TAS BORT** | Löses av den normaliserade issue-texten (leverantörens fakturavärde för gränsfall). |
| R06 | `kraftringen` | Hur används temperaturens korrigeringsfaktor på flödespriset? Behöver explicit slutformel samt effektprisets tidsenhet och periodisering. | **TAS BORT** | Formeln är källverifierad (verifieringslistan, golv vid 0,2) och effektprisperioden rättas i katalogen (`rate_period: year`) — frågan är besvarad. |
| R10 | `e-on-jarfalla, e-on-malmo, navirum-energi-norrkoping-och-soderkoping, navirum-energi-orebro-kumla-och-hallsberg` | Aktuell prisbilaga och särskilda prisvillkor: effektprisets periodisering och temperaturkorrigerat flödespris. | **TAS BORT** | Samtliga fyra medlemmars enda tariffer är `ready_to_implement`; periodiseringen rättas i katalogen (`rate_period: month`) och flödesformeln är källverifierad (§4.1, batch 3). Ingen delning behövs — alla berörda produkter blir redo samtidigt. |
| R11 | `telge-nat` | Fullständig villkorsbilaga som gäller tillsammans med 2026 års prislista, alternativt bekräftelse att tillsvidarevillkoren i 2025-bilagan fortsatt gäller. | **TAS BORT** | Verifieringslistan bekräftar redan att tillsvidarevillkoren gäller — frågan är redan besvarad, katalogens kontroll-issue är inaktuell. |
| R12 | `temab-fjarrvarme` | Kategorital och historik bakom debiteringseffekten, om Optimate ska beräkna den själv; annars räcker leverantörens debiterbara effekt. | **TAS BORT** | Löses av den normaliserade issue-texten (leverantörens fakturavärde används, ingen egen beräkning). |
| R13 | `soderhamn-nara` | Byggnadstypens omräkningsindex, om Optimate ska beräkna effekten själv; annars leverantörens debiterbara effekt. | **TAS BORT** | Tariffen passerar redan grinden idag (dess enda issue matchar ett känt mönster) — leverantörens debiterbara effekt används, ingen egen beräkning. |
| R14 | `sundsvall-energi` | Leveransvillkor för abonnemang från 2000 kW i Sundsvall/Matfors. Krävs endast för kunder i dessa grupper. | **DELAS** | Gäller uttryckligen `sundsvall-normal`/`matfors-och-kvissleby` (båda `blocked_external_info`, Matfors hålls blockerad per teknisk-kartläggning v4), inte `indal-liden-och-lucksta` (ren energitariff, ingen effektdel alls). Omskopa till de två övriga Sundsvall-ID:n. |
| R15 | `falu-energi-vatten` | Prisgrupp över 500 kW i Bjursås, Grycksbo, Sundborn eller Svärdsjö, endast om sådana kunder ingår. | **TAS BORT** | Löses av den normaliserade issue-texten på ytterorternas rad (fail-closed >500 kW). Falun berörs inte och har ingen egen öppen fråga. |

**Sammanfattning:** 7 förfrågningar (`R04, R05, R06, R11, R12, R13, R15`) TAS BORT helt — deras frågor är redan besvarade av verifieringslistan eller löses av den normaliserade issue-texten på respektive rad. 2 förfrågningar (`R03, R14`) DELAS — de täcker i dag BÅDE en `ready`-rad och en eller flera fortsatt `blocked_external_info`-rader hos samma medlem; omskopning krävs så `utredda_medlemmar()` aldrig råkar öppna en produkt som ska förbli blockerad. `R10` TAS BORT utan delning eftersom samtliga fyra berörda medlemmars enda tariffer blir redo samtidigt.


## 8. Räkningskontroll

| Disposition | Bastariffer (§3–4) | Varianter (§5) | Summa |
|---|---:|---:|---:|
| `implemented_source_verified_annual` | 7 | 0 | 7 |
| `ready_to_implement` | 45 | 9 | 54 |
| `blocked_external_info` | 26 | 5 | 31 |
| `not_applicable` | 0 | 0 | 0 |
| **Summa** | **78** | **14** | **92** |

Rättat i v4 (granskning `2026-09-08-003`, P1/P2): Finspångs spetsvärmetillägg flyttad från
`ready_to_implement` till `blocked_external_info` (utlösningsvillkoret inte kartlagt, se §5)
— varianternas fördelning ändras från 10/4 till 9/5, men totalen 14 variant-ID:n är
oförändrad. Verifierat: 7 + 54 + 31 = 92, och 78 (bas) + 14 (variant) = 92.

**Oförändrat i v5 (granskning `2026-09-08-004`):** dispositionsräkningen ovan står kvar — v5 lade till en verklig, körd grindpreflight (§6), en livscykel för medlemsomfattande informationsförfrågningar (§7) och fördjupade obligatorisk-indata-/motorbedömningar för 16 av de 45 `ready`-raderna, men flyttade ingen post mellan dispositioner.

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

1. **Jönköpings accessavgift** (variant `jonkoping-energi-jonkoping-och-granna-2026--accessavgift`,
   §5): avtalsspecifik, inte en generell katalogregel. Behöver ett Robert-BESLUT (inte en
   källfråga): ska den bli ett kundformulärfält (kunden anger sitt avtalade belopp, 0/10/25/50
   kr/mån) eller uteslutas permanent ur produkten? Claude avgör inte detta själv — hålls
   `blocked_external_info` tills beslutet finns.
2. **E.ON/Navirums 36-månadersvarianter** (batch 3b, §5): föreslås som en egen, mindre
   delbatch EFTER batch 3:s grundformel. Bekräfta ordningen, eller flagga om den i stället
   ska in i SAMMA batch som grundformeln. (Finspångs spetsvärmetillägg är flyttat till
   `blocked_external_info` i v4 — inte längre en batchordningsfråga, se §5.)
3. **Batch 5-uppdelningen** (5a/5b/5c i `batchplan-v4.md`) grupperar nu efter faktisk
   motorsemantik (ingen justering / fullårsflöde / säsongsflöde) i stället för v2:s enda
   felaktiga 5a/5b-delning. Bekräfta att denna gruppering är rätt nivå av granularitet,
   eller om fler undergrupper behövs.
4. **Kraftringens golvbegränsade faktor** (batch 3, granskning `2026-09-08-003` P1): v4
   beskriver nu en parametriserad motortyp med två verifierade regelvarianter (E.ON/Navirum
   utan golv, Kraftringen med golv vid 0,2). Bekräfta att denna modellering är tillräcklig,
   eller om ytterligare separation krävs innan kodning.

Samtliga övriga öppna frågor från v1–v3 är besvarade av Codex i granskningarna
`2026-09-08-001`, `2026-09-08-002` och `2026-09-08-003` och tillämpade rakt av i denna v4:
Vattenfall helt `blocked` som grupp (batch 8), Sundsvall Matfors följer teknisk-kartläggning
v4, leverantörsvärde-mönstret kräver tariffvis kontroll av VARJE prisdel (genomfört i §4 för
samtliga 45 `ready`-bastariffer), kända specialvarianter får aldrig bli `not_applicable`
(genomfört i §5 — alla sju integrerade i den räknade kontrollmängden), och E.ON/Navirums
36-månadersmetod är nu korrekt beskriven som ett dygnsmedeleffekt-leverantörsvärde, inte en
temperaturberäkning (§5).
