# Teknisk kartläggning: de 27 kapacitetstariffer + 1 ren energitariff (v4)

> **Terminologi efter produktbeslut 2026-09-08:** dokumentets interna status `exact`
> betyder att beräkningsmotorn har fullständiga verifierade indata för angivet scope. Den
> betyder inte att resultatet har verifierats mot en kundfaktura och ska inte visas som
> "exakt" i kundgränssnittet. Se [produktdirektivet](../PROJECT_CHARTER.md).

Upprättad 2026-09-04 av Claude. **v4 — reviderad efter omgranskning
[2026-09-04-005](../conversations/reviews/2026/09/2026-09-04-omgranskning-teknisk-kartlaggning-v3.md)
(Codex, `status: changes-required`).** v3 löste huvuddelen av v2:s åtta fynd men hade själv
sex kvarstående problem: ett datakontrakt som blandade tariffkrav, kundindata och
resultatstatus i samma objekt (och dessutom införde en fjärde, odefinierad statusnivå); två
fall (E.ON/Navirum, Vattenfall) där ett ofullständigt eller ögonblicksbildsbaserat resultat
kunde visas som `exact_annual`; neutrala temperaturdefault som fortfarande behandlades som
verifierad noll i stället för okänt värde; en självmotsägande text om vilka
justeringar som faktiskt byggs kontra blockeras; en familjeaggregerad matris i stället för en
per-tariffmatris; och en Vattenfall-uppdateringsfrekvens märkt "ej bekräftad" trots att
källan redan säger mer. Alla sex är rättade nedan. Ingen kod är ändrad av detta dokument.

## Vad som ändrats sedan v3, i korthet

1. **Kontraktet är nu tre separata objekt**, inte ett: tariffens krav (`required_input`),
   den faktiska indata som matats in (`supplied_input`), och resultatets status
   (`result_metadata`). `supplier_value_snapshot` är borttaget som en fjärde
   indatakälla — "snapshot" är nu en `accuracy`-egenskap på RESULTATET, inte en
   mätvärdeskälla.
2. **Ingen totalsumma får `accuracy: exact` när en kostnadskomponent saknas eller bygger på
   ett enda icke-rullande värde.** E.ON/Navirum med ett leverantörseffektvärde ger
   `accuracy: snapshot`. Vattenfall med blockerad flödespost ger `completeness: blocked` för
   HELA tariffen, inte bara den enskilda posten.
3. **Neutrala temperaturdefault (Södertörn, Telge) är nu obligatorisk indata för `exact`,
   inte tyst accepterad noll.** Samma sak gällde redan VänerEnergis `flode_m3` i v3 och är
   oförändrad.
4. **Byggpåståendet är nu specifikt:** E.ON/Navirums flödesjustering byggs (formeln är känd
   och kan skrivas som strukturerad katalogdata). Sundsvall Matfors och Vattenfalls
   flödespost byggs INTE i denna batch — de är blockerande, inte årsposter med
   redovisningsmässig fördelning.
5. **Per-tariffmatrisen är nu två normaliserade tabeller**, inte en familjeaggregerad: en
   familjetabell för gemensam algoritm och en tabell med alla 27 tariff-ID rakt av, en rad
   per tariff, med `ej publicerat` där en uppgift genuint saknas.
6. **Vattenfalls uppdateringsfrekvens** för debiteringseffekten anges nu som bekräftad
   (beräknas en gång per år, meddelas för nästkommande år) — enligt Codex granskning av den
   lokalt sparade officiella prislistan (`2026-09-04-005`), inte enligt en egen ny
   PDF-läsning i detta dokument. Se källhänvisning i tabellen.

---

## Det reviderade datakontraktet (tre separata objekt)

```text
Tariffmetadata / required_input        (en post per tariff och fält, statisk katalogdata)
  key                       # t.ex. "flode_m3", "Tf", "avvikelse_c"
  unit
  required_for[]            # lista: "annual" och/eller "monthly" — samma fält kan krävas för båda
  allowed_basis_types[]     # vilka supplied_input.basis_type som får uppfylla kravet
  cadence                   # hur ofta värdet normalt ändras (t.ex. "årsvis", "rullande månadsvis")
  measurement_resolution    # t.ex. "dygn", "timme", "månad", "ej publicerad"
  source_period_definition  # t.ex. "föregående 1 maj–30 april", "juli–juni"
  applicability             # när fältet gäller (t.ex. bara fullvärmekunder)
  source_reference          # källreferens i verifieringslistan/katalogen

Körningsindata / supplied_input        (en post per fält och beräkning, kundens/fakturans värde)
  key
  value | series
  basis_type                # supplier_value | calculated | estimated
  observed_period
  valid_from / valid_to
  source_reference
  quality

Resultatmetadata                       (en post per beräknat resultat)
  scope                     # annual | monthly
  accuracy                  # exact | snapshot | estimated
  completeness              # complete | partial | blocked
```

**Regler som följer direkt av uppdelningen:**

- Ett kundvärde lagras ALDRIG i `required_input` — bara vad som krävs, aldrig vad som angetts.
- `required_for` är en lista: ett fält kan krävas för `annual` men inte `monthly`, eller båda.
- `accuracy: snapshot` sätts på RESULTATET när en `required_input` med
  `cadence: "rullande månadsvis"` bara uppfylldes av ett enda, icke-rullande `supplied_input`
  (E.ON/Navirums effektvärde är typexemplet).
- `completeness: blocked` sätts på HELA tariffens resultat, inte bara den enskilda posten, så
  fort en obligatorisk `required_input` för den efterfrågade `scope` saknar ett giltigt
  `supplied_input` ELLER saknar en verifierad formel att räkna med. En tariff med
  `completeness: blocked` exponeras inte i kalkylatorn som ett valbart, färdigt resultat.

---

## Rättad exakthets-/fullständighetsstatus per familj

| Familj/tariff | `accuracy` | `completeness` | Motivering |
|---|---|---|---|
| Familj 4 (Karlstad, Sandviken, Södertörn, VänerEnergi, Övik) | `exact` OM samtliga obligatoriska fält (effekt, ev. flöde/temperatur — se nedan) är `supplier_value` | `complete` när fälten finns, annars `blocked` | Ingen rullande komponent, ingen blockerad extern data |
| Telge | Samma som ovan, plus `normalarskorrigerad_energi_mwh` obligatoriskt | `complete`/`blocked` | Ingen rullande komponent |
| Sundsvall Indal/Liden/Lucksta | `exact` (ren energitariff, inget kapacitetsberoende fält) | `complete` | Berörs inte av effekthindret alls |
| E.ON/Navirum (8) | **`snapshot`**, inte `exact`, när effekten är ett enda leverantörsvärde (rättat P1-2) | `complete` OM `flode_m3`/`Tf` finns, annars `blocked` | Effekten är en rullande 12-månadersserie; ett enda värde är en ögonblicksbild, inte en rekonstruktion av tolv debiterade värden |
| Sundsvall Matfors/Kvissleby | — (byggs inte i denna batch) | `blocked` | `network_m3_per_MWh` saknas helt som katalogdata; posten är inte en årsjustering med redovisningsmässig fördelning, den är obyggbar tills referensdatan finns |
| Vattenfall (12) | — (hela tariffen) | **`blocked`** tills flödesposten kan beräknas, oavsett om övriga delkomponenter (volymrabatt, produktval, `capacity_overrun`-spärr) är klara och testade | En totalsumma där en obligatorisk prispost saknas är inte exakt och får inte exponeras som produktionsklar, även om de andra tre delproblemen (3.1, 3.2, 3.4) är lösta internt |

---

## Vad som faktiskt byggs kontra blockeras i denna batch (rättar P1-4)

**Byggs (formel känd, kan skrivas som strukturerad katalogdata):**

- E.ON/Navirums `supply_temperature_adjusted_flow` — formeln
  `volym × base_rate × (0,02 × (Tf − 60) + 0,2)` är känd (verifieringslistans prosa), saknar
  bara att skrivas in i katalogens `correction_formula`-fält. `Tf` och `flode_m3` blir
  obligatorisk indata, inget default.
- Vattenfalls säsongsbundna volymrabatt (3.2) — källan anger redan
  `selected_rate_applies_to_all_purchased_energy_in_months` och basperioden (föregående 1
  maj–30 april).
- Vattenfalls produktvalsbekräftelse (3.1, kundbekräftat Standard/Spetsig) och
  `capacity_overrun`-spärren (3.4, `ej_tillämplig` vid rekommenderad effekt, blockerande vid
  eget val).
- Det gemensamma datakontraktet (ovan) i Python-registret, `till_prisar`, TypeScript-spegeln
  och React-formuläret.
- Sundsvall Indal/Liden/Luckstas periodiseringssentinel.
- Katalogrättelserna i Familj 4, Telge och E.ON Malmö (`-15 → -8 °C`).

**Byggs INTE i denna batch (blockerande, saknar verifierad formel eller källdata):**

- Sundsvall Matfors/Kvisslebys `network_flow_difference` — `network_m3_per_MWh` saknas helt.
- Vattenfalls `asymmetric_flow_difference` (3.3) — nätreferensen är inte verifierad som ett
  statiskt katalogvärde; källan beskriver den som beräknad för aktuell månad.

Vattenfalls tre byggbara delproblem (3.1, 3.2, 3.4) FÅR implementeras och testas internt —
men hela tariffens resultat förblir `completeness: blocked` och alltså inte valbar i
kalkylatorn förrän 3.3 också är löst. Detta är en medveten skillnad mot att bygga delarna och
sedan av misstag exponera en ofullständig tariff.

---

## Neutrala temperaturdefault är obligatorisk indata för `exact` (rättar P1-3)

Södertörns `avvikelse_c` (typ `temperature_difference`) och Telges `returtemperatur_c` (typ
`incremental_return_temperature`) har redan existerande `Indatafalt`-default (0 °C
respektive 30 °C) som ger posten värdet noll — men noll är bara KORREKT om kundens faktiska
värde också råkar ge noll. Ett saknat värde är okänt, inte verifierat noll.

**Rättelse:** dessa två fält läggs till i `required_input` med `required_for: ["annual"]` för
de tariffer som har typen. Saknas ett giltigt `supplied_input` blir resultatets `accuracy`
`estimated` (med en tydlig markering att en faktisk avvikelse skulle kunna ändra beloppet),
aldrig tyst `exact` med ett antaget nollbidrag. Samma regel gäller redan VänerEnergis
`flode_m3` (v3, oförändrad) och gäller nu även Sandvikens/Karlstads/Övik/Sydtörns/Telges
effektfält enligt det gemensamma datakontraktet ovan.

De tre justeringstypernas KOD-nivå-defaultar (`justeringar.py`: 0/43/30 °C) ändras INTE — de
förblir korrekta säkerhetsvärden för anrop som inte går via kalkylatorns UI (t.ex. en
framtida direkt motoranrop). Det är bara kalkylatorns eget resultatkontrakt som nu kräver ett
riktigt värde för att sätta `accuracy: exact`.

---

## Familjetabell — gemensam algoritm (kompletterar per-tariffmatrisen nedan)

| Familj | Katalogtyp | Byggs i denna batch | Delade byggstenar |
|---|---|---|---|
| E.ON/Navirum (8) | `supply_temperature_adjusted_flow` | Ja | `_mwh_for_manader`-mönstret återanvänds inte (ingen `months`-begränsning på denna typ — gäller alla 12 månader) |
| Sundsvall Matfors (1) | `network_flow_difference` | Nej — blockerad | — |
| Vattenfall (12) | `volume_discount` (utökad basperiod+tillämpning), `capacity_overrun` (spärr), `asymmetric_flow_difference` (blockerad) | Delvis (3.1/3.2/3.4 ja, 3.3 nej) | `_mwh_for_manader` återanvänds för 3.2/3.3:s 7-månadersbegränsning när/om 3.3 någonsin byggs |
| Familj 4 (5) + Telge | Befintliga typer (`temperature_difference`, `low_utilization`, `incremental_return_temperature`) eller ingen typ alls | Ja (katalogrättelser + datakontrakt) | Inga nya typer |
| Sundsvall Indal (1) | Ingen (ren energitariff) | Ja (periodiseringssentinel) | — |

## Per-tariffmatris — samtliga 27 kapacitetstariffer, ett tariff-ID per rad

`ej publicerat` betyder: uppgiften saknas i både katalogens JSON och verifieringslistans
prosa och kräver antingen en ny primärkälla eller en direkt leverantörsförfrågan — den är
INTE uppskattad här.

| Tariff-ID | Metod | Referenstemp | Historikperiod | Dagurval | Reservregel | Avrundning | Uppdateringsfrekvens | Källa |
|---|---|---|---|---|---|---|---|---|
| `karlstads-energi-karlstad-2026` | Medel tre högsta dygnseffekter | Kvalificerande kyla −16 till −10 °C | Löpande, nov–mar | ej publicerat | Annars föregående värde | ej publicerat | Nov–mar vid kvalificering | Katalog `capacity.billing_basis_method` |
| `sandviken-energi-sandviken-normal-2026` | Effektsignatur | −16 °C | Föregående vinter okt–apr | ej publicerat | Medel två senaste årens toppdygn | ej publicerat | Årlig | Katalog + verifieringslista |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | Effektsignatur ELLER egenvald, min 5 kW | ej publicerat | ej publicerat | ej publicerat | ej publicerat | ej publicerat | ej publicerat | Katalog |
| `vanerenergi-mariestad-och-toreboda-2026` | Medel två signaturer | −13,5 °C | Jan–mar | Vardagar | R²<0,6 → tre högsta dygn, min 5 kW | ej publicerat | Årlig | Katalog |
| `ovik-energi-ornskoldsvik-2026` | Signatur ELLER tre högsta dygnsenergier, leverantörens val | ej publicerat | ej publicerat | ej publicerat | Leverantören väljer metod | ej publicerat | ej publicerat | Katalog |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | Dygnsmedeleffekt | −11 °C | Juli–juni | Vardagar | Alternativa historikregler, ej detaljerat | Heltal | Årsrevision 1 jan | Katalog |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | Effektsignatur, rullande | −15 °C | Månad 13 till månad 2 före fakturamånad | Vardagar under 15 °C | Medel tre högsta dygn nov–mar; alt. 36-mån bas-/delvärme | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | Samma som ovan | −15 °C | Samma | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | Effektsignatur, rullande | **−8 °C** (katalogrättelse) | Samma som Järfälla | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | Samma som ovan | **−8 °C** | Samma | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | Effektsignatur, rullande | −15 °C | Samma som Järfälla | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Månadsvis | Katalog + verifieringslista |
| `sundsvall-energi-matfors-och-kvissleby-normal-2026` | Högsta dygnsmedel | Dygn <−10 °C exkluderas | Okt–mars föregående säsong | ej publicerat | ej publicerat | ej publicerat | Fastställs april, gäller följande jan–dec | Katalog |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-standard-2026` | Regression, ej strukturerad i katalog | −14 °C | Okt–apr | Vardagar | Tre högsta dygn, tre senaste hela kalenderår | ej publicerat | **Årlig, beräknas en gång och meddelas för nästkommande år** | Verifieringslista + Codex granskning 005 (lokalt sparad 2026-prislista) |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-spetsig-2026` | Samma | −14 °C | Samma | Samma | Samma | ej publicerat | Samma | Samma |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-standard-2026` | Samma | −14 °C | Samma | Samma | Samma | ej publicerat | Samma | Samma |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-spetsig-2026` | Samma | −14 °C | Samma | Samma | Samma | ej publicerat | Samma | Samma |
| `vattenfall-motala-och-askersund-motala-och-askersund-standard-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Samma (ej separat verifierad för denna ort) | Verifieringslista |
| `vattenfall-motala-och-askersund-motala-och-askersund-spetsig-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-nykoping-nykoping-standard-2026` | Samma | −14 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-nykoping-nykoping-spetsig-2026` | Samma | −14 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-uppsala-uppsala-standard-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-uppsala-uppsala-spetsig-2026` | Samma | −15 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-vanersborg-vanersborg-standard-2026` | Samma | −12,5 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |
| `vattenfall-vanersborg-vanersborg-spetsig-2026` | Samma | −12,5 °C | Samma | Samma | Samma | ej publicerat | Samma | Verifieringslista |

**Om uppdateringsfrekvensen (P2-2):** Codex granskning `2026-09-04-005` verifierade mot den
lokalt sparade officiella prislistan för Haninge/Tyresö/Älta/Gustavsberg att den
rekommenderade effekten beräknas en gång per år och meddelas för nästkommande år. Detta
dokument har inte självständigt läst PDF-sidan om igen — raden ovan är attribuerad till
Codex granskning, inte en ny, egen primärkälleläsning. För Motala/Askersund, Nyköping,
Uppsala och Vänersborg finns motsvarande bekräftelse ännu bara i verifieringslistans
allmänna beskrivning, inte i en egen granskad PDF per ort — markerat separat i tabellen i
stället för att anta att alla fem områdenas prislistor säger exakt samma sak.

**Vattenfalls tre separata effektbegrepp, för tydlighetens skull ännu en gång:** raden ovan
avser den REKOMMENDERADE DEBITERINGSEFFEKTEN (kapacitetsformelns bas). Tariffvalskvoten (3.1,
medel av tre högsta TIMmedeleffekter föregående maj–april) och `capacity_overrun`s
DYGNSmedeleffekt (3.4) är andra storheter och ingår inte i denna tabell.

---

## Övriga sektioner, oförändrade från v3 i sak

Följande delar av v3 stod inte under kritik i granskning `2026-09-04-005` och är därför
oförändrade i sak (bara ordnade om runt de nya kontraktsobjekten ovan):

- Familj 2 (Sundsvall Matfors) och Familj 3:s (Vattenfall) delproblem 3.1–3.4, inklusive
  `capacity_overrun`s `ej_tillämplig`-modell.
- Familj 5, Sundsvall Indal/Liden/Luckstas periodiseringssentinel.
- Fas A/Fas B-uppdelningen och Sandviken som föreslagen första automatiseringspilot.

## Sammanfattning: rekommenderad ordning, v4

1. **Lås det tredelade datakontraktet** (`required_input`/`supplied_input`/
   `result_metadata`) i Python-registret, `till_prisar`, TypeScript-spegeln och
   React-formuläret.
2. **Sundsvall Indal/Liden/Lucksta** — oberoende, `exact`/`complete` direkt.
3. **Familj 4 + Telge** (6 tariffer) — katalogrättelser, temperaturfälten som obligatorisk
   indata för `exact`, `accuracy: exact`/`completeness: complete` när fälten finns.
4. **E.ON/Navirum** (8 tariffer) — bygg `supply_temperature_adjusted_flow`, resultat ger
   `accuracy: snapshot` med ett leverantörseffektvärde, `completeness: complete` när
   `Tf`/`flode_m3` finns.
5. **Vattenfalls tre byggbara delproblem** (3.1, 3.2, 3.4) implementeras och testas, men hela
   tariffgruppens resultat förblir `completeness: blocked` tills 3.3 är löst — INTE exponerad
   som valbar i kalkylatorn under tiden.
6. **Sundsvall Matfors** och **Vattenfalls flödespost (3.3)** — byggs inte i denna batch;
   kvar som blockerande tills extern data/leverantörsbesked finns.
7. **Fas B-pilot (Sandviken)** kan påbörjas parallellt när Robert vill ha en automatisk
   effektmotor.

Skickas till Codex för ny granskning innan Robert väljer första implementationsbatchen.
Inget implementerat.
