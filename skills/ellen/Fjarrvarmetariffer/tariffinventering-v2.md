# Tariffinventering v2.0 — fullständig kontrollmängd för kalkylator v1

Upprättad 2026-09-08 av Claude. Ersätter `tariffinventering-v1.md` i sin helhet, som svar på
Codex kodgranskning [2026-09-08-001](../conversations/reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md)
(`status: changes-required`) av v1 och den ursprungliga överlämningen
[2026-09-08-001](../conversations/handoffs/2026/09/2026-09-08-tariffinventering-v1.md)
från Codex. Ingen produktkod, tariffdata eller genererad fil är ändrad av detta dokument.

**Vad som är nytt i v2, i korthet** (se granskningen för fullständig motivering till varje
punkt):

1. En verklig, normaliserad post per unik tariffprodukt (§3–4) i stället för grupptext —
   Riksgenomsnittet ligger nu i en egen tabell (§7) för syntetiska schabloner.
2. Tre dispositioner rättade: `borlange-energi-borlange-2026` och
   `c4-energi-kristianstad-2026` är nu `ready_to_implement` (leverantörsvärde-mönstret,
   samma som Borås effektgrupp); Stockholm Exergis ANNUAL-produkt
   (`stockholm-exergi-stockholm-exergi-normal-2026`) är `ready_to_implement`, inte
   `implemented_source_verified_annual` — dess `monthly_invoice`-kontrakt (godkänt
   `2026-09-06-003`) täcker inte kalkylatorns årsprognos.
3. Motorstatusen är omräknad direkt mot `justeringar.py`s `JUSTERINGSTYPER`-register
   (den faktiska godkännandelistan för justeringstyper) — 16 av de 46 `ready`-tarifferna
   kräver NY motorkod (en ej implementerad justeringstyp eller kapacitetsform), inte bara
   E.ON/Navirum/Borås/Finspång som v1 flaggade. Se §4 för samtliga.
4. Sju kända specialvarianter är utbrutna till en egen spårad tabell (§5) i stället för
   `not_applicable`.
5. Räkningsspråket är rättat: 79 unika enheter = **78 tariffprodukter + 1 syntetisk
   schablon** (inte "79 unika tariffprodukter"), 53 leverantörer + 1 schablonentitet
   (inte 55).
6. Batchplanen (`batchplan-v2.md`) följer överlämningens ordning (Familj 4-resten före
   Sundsvalls rena energitariff), skriver ut alla ID:n fullständigt, och flyttar
   Kraftringen till samma batch som E.ON/Navirum (samma ej implementerade motortyp).

## Frusen kontrollmängd (proveniens)

| Källa | Version/commit | Antal produkter i denna inventering |
|---|---|---|
| `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` | `schema_version 0.1.3`, `skills`-repo commit `7ba9ec1b6245a72a4720f11b11beec6692af6196` (sha256 `a35fc95b741c6af9a3d1462dbd3e23c12577e2f1f1b75bd05b6ab6f484b52bcd`) | 78 katalograder (53 leverantörer) |
| `enkey-agents/skills/ellen/leverantor-stockholm-exergi.md` | fakturavaliderad mot 18 fakturor, Brf Åkermannen 33 (`monthly_invoice`-kontraktet, granskning `2026-09-06-003`) | Samma produkt som katalogens `stockholm-exergi-stockholm-exergi-normal-2026` — räknas EN gång, se §4 |
| `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md` | Nils Holgersson-rapporten 2025 | 1 syntetisk schablon, egen tabell §7 — inte ett tariffprodukt |

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
- **Sandviken och varje `ready_to_implement`-tariff nedan:** mwh-läge kräver den
  obligatoriska indatan; kr och schablon blockeras tills en egen, verifierad
  invers/schablonmodell byggs och godkänns separat.

## 3. Redan implementerade (7 produkter)


#### `goteborg-energi-goteborg-2026`
- **Leverantör / nät / kundkategori:** Göteborg Energi — Göteborg — näring/brf
- **Prisår/giltighet:** 2026, legacy-tariff sedan uppgift 7 (2026-09-03)
- **Källstatus:** godkänd | **Katalogstatus:** legacy, `contract_required` ej satt | **Motorstatus:** klar (`temperature_difference`, redan i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated (legacy) | **Teststatus:** i generella regressions-/godkanda-sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja, redan i produktion
- **Obligatorisk indata:** Returtemperaturavvikelse har ett neutralt default (0 °C); ingen indata är formellt obligatorisk för legacy-vägen
- **Inmatningslägen:** mwh, kr, schablon — alla tre
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-17-under-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 17, under 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (ingen kapacitetsdel, `capacity: null`) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** föregående kalenderårs energi krävs för kr-läget (volymrabattens band)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 21, över 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`cooling_deadband`, `volume_discount`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** föregående kalenderårs energi (volymrabatt); avkylning har neutralt default
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `halmstads-energi-och-miljo-halmstad-2026`
- **Leverantör / nät / kundkategori:** Halmstads Energi och Miljö — Halmstad — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (inga justeringar) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** ingen
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `molndal-energi-molndal-kallered-och-lindome-2026`
- **Leverantör / nät / kundkategori:** Mölndal Energi — Mölndal, Kållered och Lindome — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`volume`, kWh/dygn-kapacitetsform, redan stödd) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** flöde och högsta dygnsenergi har dynamiska gissningsdefault (`ar_gissning: true`) — kan anges för exakthet men är inte formellt obligatoriska
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `norrenergi-norrenergi-2026`
- **Leverantör / nät / kundkategori:** Norrenergi — Norrenergi — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`low_utilization`, `incremental_return_temperature`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** normalårskorrigerad energi och returtemperatur har dynamiska default (egen uppskattad förbrukning respektive 30 °C-tröskeln)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `sandviken-energi-sandviken-normal-2026`
- **Leverantör / nät / kundkategori:** Sandviken Energi — Helleverans — näring/brf
- **Prisår/giltighet:** 2026 | **Källstatus:** godkänd, granskning `2026-09-07-003` | **Katalogstatus:** `contract_required: true` | **Motorstatus:** klar (ingen kapacitetsdel utöver effekt) | **Kontraktsstatus:** `POLICYREGISTER`, `annual_forward`, `minvarde=3`/`heltal=True` | **Teststatus:** `test_sandviken_kontrakt.py`, `besparingsvardeSandviken.test.ts` | **UI-status:** valbar, pushad `origin/main`
- **Årsreproducerbar:** Ja, i produktion | **Obligatorisk indata:** debiterbar effekt (kW, fakturan), heltal ≥3 kW
- **Inmatningslägen:** mwh (obligatorisk effekt); kr och schablon blockerade (`unsupported_input_mode`/`missing_energy`/`invalid_energy`)
- **Disposition:** `implemented_source_verified_annual`

## 4. Per-produktmatris — samtliga 71 icke-implementerade tariffprodukter

En normaliserad post per unik tariff-ID (inte grupptext). 46 är `ready_to_implement` (§4.1),
25 är `blocked_external_info` (§4.2). Fälten följer exakt vad överlämning `2026-09-08-001`
begärde: leverantör, nät, produkt, kundkategori, prisår/giltighet+källa, käll-/katalog-/
motor-/kontrakts-/test-/UI-status separat, årsreproducerbarhet, obligatorisk indata med
fyndplats, inmatningsläge, tariffamilj/adapter, kvarstående arbete, disposition.

### 4.1 Redo att implementera (46 produkter)


#### `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
- **Leverantör / nät / kundkategori:** Borås Energi och Miljö — Borås, Sjömarken, Sandared, Dalsjöfors, Fristad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** Ingen ny motorkod. `Tariffpolicy` med leverantörsvärde-krav, samma mönster som redan godkända leverantörsvärde-tariffer.
- **Disposition:** `ready_to_implement`


#### `c4-energi-kristianstad-2026`
- **Leverantör / nät / kundkategori:** C4 Energi — Kristianstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** Ingen ny motorkod. `Tariffpolicy` med leverantörsvärde-krav, samma mönster som redan godkända leverantörsvärde-tariffer.
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. E.ON Järfälla (bostäder).
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. E.ON Järfälla (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. E.ON Malmö (bostäder, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. E.ON Malmö (övriga fastigheter, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `eskilstuna-energi-och-miljo-eskilstuna-2026`
- **Leverantör / nät / kundkategori:** Eskilstuna Energi och Miljö — Eskilstuna — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (network_flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH kundens flöde (m³, fakturan). Referensen är `monthly_mean_for_customers_covered_by_flow_tariff` — nätets egen genomsnittsflöde per MWh för flödestariffkunder, inte kundens eget värde; måste verifieras som ett stabilt katalogvärde eller en uttryckligen redovisad fakturapost innan aktivering.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Eskilstuna — ny motortyp `network_flow_difference`
- **Kvarstående arbete:** `network_flow_difference` finns INTE i JUSTERINGSTYPER. Samma typnamn som Sundsvall Matforss blockerade post, men Eskilstunas referens är (till skillnad från Matfors) beskriven i källan — kräver ändå ny motorkod och en verifierad referens innan `ready` kan bli `implemented`.
- **Disposition:** `ready_to_implement`


#### `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Bjursås, Grycksbo, Sundborn, Svärdsjö — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `falu-energi-vatten-falun-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Falun — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `finspangs-tekniska-verk-finspang-2026`
- **Leverantör / nät / kundkategori:** Finspångs Tekniska Verk — Finspång — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE — ny kapacitetsform `piecewise_polynomial` + conditional_flow
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens P-värde (kapacitetsformelns bas) OCH returtemperatur varje månad (för `conditional_flow`s villkor >55 °C, flöde-m³). Spetsvärmetillägget (20 %) är en EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Finspång — ny kapacitetsform + ny motortyp
- **Kvarstående arbete:** `piecewise_polynomial` (ny kapacitetsform) OCH `conditional_flow` (ny justeringstyp, villkorad på månatlig returtemperatur) — TVÅ separata nya motordelar, större arbete än enbart kapacitetsformen som v1 angav.
- **Disposition:** `ready_to_implement`


#### `habo-energi-habo-2026`
- **Leverantör / nät / kundkategori:** Habo Energi — Habo — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Åre, Järpen, Mörsil, Duved, Kall, Hallen, Krokom, Nälden, Föllinge — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `karlstads-energi-karlstad-2026`
- **Leverantör / nät / kundkategori:** Karlstads Energi — Karlstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `kraftringen-kraftringen-2026`
- **Leverantör / nät / kundkategori:** Kraftringen — Kraftringen — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde (m³, fakturan). Formeln `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)` känd (katalog); Brunnshögs nätdel är en EGEN VARIANT, se särfallstabellen — endast ordinarie nät ingår här.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Kraftringen — samma motortyp som E.ON/Navirum
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` — SAMMA ej implementerade motortyp som de åtta E.ON/Navirum-tarifferna. Bör byggas i SAMMA batch/commit som dem, inte separat i "leverantörsvärde utan nytt motorarbete" som v1 felaktigt antog.
- **Disposition:** `ready_to_implement`


#### `lulea-energi-lulea-2026`
- **Leverantör / nät / kundkategori:** Luleå Energi — Luleå — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, 2–4 lägenheter — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen kapacitetsdel. Fast årsavgift (katalog), energi (MWh, kund anger), säsongens verkliga flöde i m³ (flow, okt–apr) — fakturans flödesvärde, INTE härlett ur MWh×antagen ΔT.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Mälarenergi, ren energitariff (2–4 lgh)
- **Kvarstående arbete:** `volume`-justeringen finns i motorn men appliceras i dag på ett enda årsflöde, inte postens `months` (okt–apr). Kräver månadssemantik i faktura.py/fjarrvarme.ts innan aktivering — annars prissätts fel månader.
- **Disposition:** `ready_to_implement`


#### `mjolby-svartadalen-energi-mjolby-2026`
- **Leverantör / nät / kundkategori:** Mjölby Svartådalen Energi — Mjölby — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. Navirum Norrköping/Söderköping (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. Navirum Norrköping/Söderköping (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. Navirum Örebro/Kumla/Hallsberg (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. Navirum Örebro/Kumla/Hallsberg (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `nevel-gimo-osterbybruk-och-osthammar-2026`
- **Leverantör / nät / kundkategori:** Nevel — Gimo, Österbybruk och Östhammar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-angelholm-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Ängelholm normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg Totalvärme, central installerad före 2024 — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** Katalogrättelse krävs FÖRE aktivering: `fixed: null`→0, `monthly_proration`→kalenderdagsviktning.
- **Disposition:** `ready_to_implement`


#### `partille-energi-partille-2026`
- **Leverantör / nät / kundkategori:** Partille Energi — Partille — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `piteenergi-pitea-centrala-natet-2026`
- **Leverantör / nät / kundkategori:** PiteEnergi — Piteå centrala nätet — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `skovde-energi-skovde-2026`
- **Leverantör / nät / kundkategori:** Skövde Energi — Skövde — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** `monthly_invoice`-kontraktet (kall energi, returtemp, debiterbar effekt) är redan implementerat och fakturavaliderat (18 fakturor, granskning `2026-09-06-003`). Kalkylatorns ÅRSPROGNOS saknar dock motsvarande kontraktsbindning idag och anropar motorn utan kall energi-/returtemperaturvärden.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Stockholm Exergi — egen kontraktsväg, ej Sandviken-mönstret
- **Kvarstående arbete:** Bygg ett eget källverifierat årsreferensfall för `annual_forward` (motsvarande Sandvikens granskningskedja `2026-09-06-004`→`2026-09-07-003`), gör kall energi/returtemp till synlig, obligatorisk indata för årsvägen, och sätt rätt inmatningslägesspärrar. `monthly_invoice`-kontraktet rörs inte — det är redan klart och stannar som det är.
- **Disposition:** `ready_to_implement`


#### `sundsvall-energi-indal-liden-och-lucksta-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Indal, Liden och Lucksta — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen utöver energimängd (MWh).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Ren energitariff — engångsjustering
- **Kvarstående arbete:** Sätt `capacity.type: "not_applicable"` på katalograden. Mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp 1–4 (2026-09-04), bara inte aktiverad mot denna rad.
- **Disposition:** `ready_to_implement`


#### `tekniska-verken-katrineholm-katrineholm-2026`
- **Leverantör / nät / kundkategori:** Tekniska Verken - Katrineholm — Katrineholm — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** Ingen ny motorkod. `volume` gäller bara säsongsmånaderna (okt–apr) i katalogen — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik innan aktivering, inte bara ett synligt flödesfält.
- **Disposition:** `ready_to_implement`


#### `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`
- **Leverantör / nät / kundkategori:** Telge Nät — Telge företag och bostadsrättsföreningar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Kvarstående arbete:** Alla tre justeringstyper redan i JUSTERINGSTYPER. `Tariffpolicy` med tre bundna fält, ingen ny motorkod.
- **Disposition:** `ready_to_implement`


#### `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`
- **Leverantör / nät / kundkategori:** TEMAB Fjärrvärme — Tierp, Karlholmsbruk och Örbyhus — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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


#### `trollhattan-energi-trollhattan-2026`
- **Leverantör / nät / kundkategori:** Trollhättan Energi — Trollhättan — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (asymmetric_flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). `reference_m3_per_MWh: 17`, `bonus_rate: 3`, `fee_rate: 7` är REDAN statiska katalogvärden (till skillnad från Vattenfalls `reference: "network_average"`, som är dynamisk och blockerande).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Umeå — ny motortyp `asymmetric_flow_difference` (till skillnad från Vattenfall: statisk referens)
- **Kvarstående arbete:** `asymmetric_flow_difference` finns INTE i JUSTERINGSTYPER. Måste byggas separat från Vattenfalls blockerade variant av samma typnamn — Umeås formel är komplett och byggbar, Vattenfalls är det inte (se Vattenfall-raderna).
- **Disposition:** `ready_to_implement`


#### `vanerenergi-mariestad-och-toreboda-2026`
- **Leverantör / nät / kundkategori:** VänerEnergi — Mariestad och Töreboda — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
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

### 4.2 Blockerade av extern information (25 produkter)

Endast produkter där prisbestämningen själv är tvetydig, motsägs, eller där en obligatorisk
prisdel helt saknar publicerat värde. Frågan i sista fältet är den som ska skickas till
leverantören (ordagrant eller nästan ordagrant från verifieringslistan/teknisk-kartläggningen
— inte omformulerad här).


#### `gavle-energi-gavle-2026`
- **Leverantör / nät / kundkategori:** Gävle Energi — Gävle — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
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

## 5. Kända specialvarianter — spårade, inte gömda i `not_applicable`

Enligt granskning `2026-09-08-001` (P1, "möjliga specialvarianter får inte döljas som
'ej tillämpliga i denna batch'"): dessa sju fall är verkliga, källkända produktvarianter
som INTE ingår i huvuddispositionen ovan för sin bastariff. Ingen av dem får slutstatus
`not_applicable` bara för att den skjuts ur en batch — varje rad nedan har antingen en
egen preliminär disposition eller väntar uttryckligen på ett Robert-beslut. Det slutliga
antalet tariffprodukter i en framtida inventeringsversion blir sannolikt större än 78 när
dessa delas ut som egna rader.

| # | Basprodukt | Variant | Vad den kräver | Preliminär disposition | Väntar på |
|---|---|---|---|---|---|
| 1 | E.ON/Navirum (8 tariffer) | 36-månadersmetoden för kunder med annan bas-/delvärmekälla än fullvärme | Egen formel, källverifierad enligt verifieringslistan, men inte kartlagd i detalj i teknisk-kartläggning v4 (som bara behandlar fullvärme) | `ready_to_implement`, egen mindre delbatch efter fullvärmebatchen | Robert: bekräfta att delbatchen ska schemaläggas separat, inte samtidigt |
| 2 | `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | Kundvald effekt (i stället för SFAB:s rekommenderade) med egen överuttagsavgift | Överuttagsformeln är inte kartlagd i detalj; skiljer sig från `capacity_overrun`-typen som redan finns i katalogschemat för andra leverantörer | `blocked_external_info` — exakt fråga saknas ännu, måste formuleras | Robert/Codex: formulera frågan till Södertörns Fjärrvärme |
| 3 | `kraftringen-kraftringen-2026` | Brunnshögs nätdel | Egen prisstruktur, inte kartlagd — bara ordinarie nät är verifierat i denna inventering | `blocked_external_info` — källunderlag för Brunnshög saknas i denna omgång | Robert: hämta Brunnshögs egen prislista |
| 4 | `tekniska-verken-linkoping-linkoping-2026` | Lågtemperaturleverans | Egen tariffstruktur enligt källan, inte kartlagd i detalj | `blocked_external_info` — källunderlag för lågtemperaturvarianten saknas i denna omgång | Robert: hämta lågtemperaturprislistan |
| 5 | `finspangs-tekniska-verk-finspang-2026` | Spetsvärmetillägg (20 %) | Känt procentvillkor, men inte kartlagt vilka kunder/perioder som utlöser det | `ready_to_implement`, egen liten delbatch efter grundformeln | Robert: bekräfta att spetsvärmetillägget ska byggas som en synlig tilläggspost |
| 6 | `jonkoping-energi-jonkoping-och-granna-2026` | Avtalsberoende accessavgift (0/10/25/50 kr/mån) | Beror på det enskilda avtalet, inte på en publicerad allmän regel | `blocked_external_info` — kräver avtalsspecifik uppgift per kund, inte en generell katalogregel | Robert: bekräfta om accessavgiften ska vara ett kundformulärfält eller uteslutas permanent |
| 7 | `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | Miljötillägget "Bra Miljöval" (31 SEK/MWh, valfritt) | Ett kundvalt tillägg, inte en automatisk prisdel — kräver ett UI-produktval, inte bara ett indatafält | `ready_to_implement`, som ett tillval i samma batch som grundformeln | — (kan byggas direkt som en kryssruta i samma batch) |

Bastariffernas dispositioner ovan (§3–4) gäller det ORDINARIE/FULLVÄRME-fallet i varje
rad. Ingen av de sju varianterna ovan är räknad in i 78-summan i §6 — de tillkommer när de
bryts ut som egna, spårade poster i en framtida inventeringsversion.
## 6. Räkningskontroll

| Disposition | Antal |
|---|---:|
| `implemented_source_verified_annual` | 7 |
| `ready_to_implement` | 46 |
| `blocked_external_info` | 25 |
| `not_applicable` | 0 |
| **Summa (tariffprodukter)** | **78** |

Stämmer exakt mot de 78 katalograderna: 7 + 46 + 25 + 0 = 78 (verifierat programmatiskt mot
`optimate-fjarrvarme-2026.json`, inte räknat för hand).

**Härledning av totalen 79 unika enheter / 80 råa kontrollposter:** 78 katalograder + 1
separat förvaltad leverantörsfil (Stockholm Exergi) + 1 separat förvaltad schablonfil
(Riksgenomsnittet) = 80 råa kontrollposter. Stockholm Exergis katalograd
(`stockholm-exergi-stockholm-exergi-normal-2026`) OCH dess leverantörsfil beskriver SAMMA
produkt (samma leverantör, nät, kundkategori — leverantörsfilen bär bara det redan
fakturavaliderade `monthly_invoice`-kontraktet som en extra, mer detaljerad datakälla för
just den raden, inte en andra produkt). Efter den dedupliceringen: **79 unika enheter = 78
tariffprodukter + 1 syntetisk schablon** (Riksgenomsnittet, som aldrig var ett
tariffprodukt att implementera, se §7).

**Leverantörer vs. tariffprodukter:** katalogens 53 `members`-poster inkluderar redan
Stockholm Exergi (leverantörsfilen lägger inte till en 54:e leverantör). Det är alltså
**53 fjärrvärmeleverantörer + 1 syntetisk schablonentitet** (Riksgenomsnittet, inte en
fjärrvärmeleverantör) = 54 unika leverantörsentiteter, inte 55. 78 tariffprodukter fördelat
på 53 leverantörer — flera (Vattenfall, E.ON, Navirum, PiteEnergi, Öresundskraft, Skellefteå
Kraft, Hässleholm Miljö, Tekniska Verken, Jämtkraft, Falu Energi & Vatten, Gotlands Energi)
har mer än en produkt (nät/ort/produktvariant).

**Dubbletter funna:** exakt en — Stockholm Exergis katalograd mot dess leverantörsfil
(hanterad genom att räkna den EN gång, som `ready_to_implement`, se §4.1). Inga andra
katalograder beskriver samma leverantör+nät+produkt+kundkategori två gånger.

## 7. Syntetiska schabloner (separat tabell, inte tariffprodukter)

| Post | Källa | Vad den är | Motivering till `not_applicable` |
|---|---|---|---|
| Riksgenomsnittet | `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md`, Nils Holgersson-rapporten 2025 | Syntetisk nationell schablon som används när ingen namngiven leverantör är vald eller känd | Inte ett tariffprodukt att implementera — en beräkningsmekanism för det generiska fallet. Se produktdirektivets öppna beslut ([PROJECT_CHARTER §8](../PROJECT_CHARTER.md)) om hur den ska presenteras när en namngiven leverantör saknas: som ett tydligt märkt separat val, inte tyst som om den vore leverantörens egen tariff. |

## 8. Öppna frågor till Codex

1. **E.ON/Navirums 36-månadersmetod och Finspångs spetsvärmetillägg** (specialvariant 1
   och 5 i §5) föreslås som `ready_to_implement`, egna mindre delbatcher EFTER
   grundformlerna i respektive familjebatch. Om det anses fel prioritering — att de i
   stället ska vänta tills en framtida omgång eller läggas i SAMMA batch som grundformeln —
   säg till innan batchplanen genomförs.
2. **Borås miljötillägg** (specialvariant 7) föreslås byggt direkt i samma batch som Borås
   grundformel, som ett kundvalt UI-tillägg. Om det bedöms som ett för stort scope-tillägg
   för batch 5 (som redan har högst risk pga två nya kapacitetsformer), bör det brytas ut
   till en egen, separat, mindre batch — flagga om så är fallet.
3. **Tre specialvarianter saknar fortfarande en formulerad leverantörsfråga** (Södertörns
   överuttagsavgift, Kraftringens Brunnshög, Tekniska Verken Linköpings lågtemperaturvariant
   — specialvariant 2–4 i §5). Robert/Codex behöver antingen formulera dessa frågor eller
   bekräfta att de kan vänta obestämt utan att blockera huvudtariffens `ready_to_implement`
   -status, vilket de gör i denna v2.
4. **Jönköpings accessavgift** (specialvariant 6) är avtalsspecifik, inte en generell
   katalogregel — föreslagen `blocked_external_info` tills Robert bestämmer om den ska bli
   ett kundformulärfält (ett värde kunden själv anger, inte katalogdata) eller uteslutas
   permanent ur produkten. Det är en produktbeslutsfråga, inte en ren källfråga, så den
   flaggas separat här.

Öppna frågorna 1–4 från v1 (Vattenfall helt blockerad, Sundsvall Matfors följer
teknisk-kartläggning v4, leverantörsvärde-mönstret kräver tariffvis kontroll, kända
specialvarianter får inte bli `not_applicable`) är redan besvarade av Codex i granskning
`2026-09-08-001` och tillämpade rakt av i denna v2 — se §1 punkt 3–4 och §5.
