# Tariffinventering v1.0 — fullständig kontrollmängd för kalkylator v1

Upprättad 2026-09-08 av Claude, i svar på överlämning
[2026-09-08-001](../conversations/handoffs/2026/09/2026-09-08-tariffinventering-v1.md) från Codex.
Ingen produktkod, tariffdata eller genererad fil är ändrad av detta dokument. Detta är
underlaget produktdirektivets [§4](../PROJECT_CHARTER.md) och slutkriterium refererar till.

## Frusen kontrollmängd (proveniens)

| Källa | Version/commit | Antal produkter i denna inventering |
|---|---|---|
| `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` | `schema_version 0.1.3`, `skills`-repo commit `7ba9ec1b6245a72a4720f11b11beec6692af6196` (sha256 `a35fc95b741c6af9a3d1462dbd3e23c12577e2f1f1b75bd05b6ab6f484b52bcd`) | 78 katalograder (53 leverantörer) |
| `enkey-agents/skills/ellen/leverantor-stockholm-exergi.md` | senast ändrad enligt fil, fakturavaliderad mot 18 fakturor Brf Åkermannen 33 | 1 (2 prisår: 2025, 2026) |
| `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md` | Nils Holgersson-rapporten 2025 | 1 (syntetisk schablon, se nedan — räknas inte som ett tariffprodukt att implementera) |

**Explicit utanför denna frusna version:** `Fjarrvarmetariffer/optimate-fjarrvarme-2027.json`
(prisår 2027, commit `62181a1`, endast 2 av 53 medlemmar ifyllda hittills). Nästa prisårs
katalog är förvaltning av den färdiga produkten, inte en del av v1:s slutkriterium — se
[PROJECT_CHARTER §4](../PROJECT_CHARTER.md).

Total kontrollmängd i denna inventering: **80 unika enheter** — 78 katalograder + 2 separat
förvaltade leverantörsfiler (varav en, riksgenomsnittet, inte är ett tariffprodukt).
Deduplicerat till **79 unika tariffprodukter** (katalogens Stockholm Exergi-rad är samma
produkt som leverantörsfilen, se §5).

## 1. Metod och källhierarki

Denna inventering bygger på tre redan granskade underlag i stigande detaljnivå, utan att
upprepa deras innehåll i onödan:

1. [`verifieringslista-fjarrvarmebolag.md`](verifieringslista-fjarrvarmebolag.md) —
   Codex källgranskning av samtliga 78 katalograder mot leverantörernas 2026-underlag
   (2026-09-04). Ger käll-status per rad.
2. [`teknisk-kartlaggning-28-tariffer.md`](teknisk-kartlaggning-28-tariffer.md) v4 —
   Claudes tekniska analys av de 28 rader som hade fullständigt källunderlag även för
   månadsmodell, godkänd av Codex (`2026-09-04-006`). Ger motor-/kontraktsstatus för den
   delmängden — auktoritativ där den och verifieringslistan skulle motsäga varandra (se §4,
   Sundsvall Matfors).
3. `enkey-agents/tools/tariffer/katalog.py` (`godkanda()`, `grind()`,
   `FAS1_ENERGIFORMER`, `FAS1_KAPACITETSFORM`, `EJ_TILLAMPLIG_KAPACITETSFORM`) och
   `policyregister.py` — den faktiska motor-/kontraktsstatusen i dag, läst direkt ur koden,
   inte antagen.

**Disposition per produkt** följer PROJECT_CHARTER §4:

- `implemented_source_verified_annual` — valbar i kalkylatorn i dag, årsverifierad.
- `ready_to_implement` — samtliga prisdelar och regler är källverifierade; återstående
  arbete är internt (katalogmappning, motorstöd för en ny men känd formeltyp, eller
  produktintegration) — inget nytt leverantörsbesked krävs.
- `blocked_external_info` — minst en materiell uppgift saknas, är tvetydig eller motsägs
  av källorna; kräver ett leverantörssvar eller ett nytt beslut innan implementation.
- `not_applicable` — inte ett tariffprodukt att implementera (schablonmekanism eller
  duplicerad post), med motivering.

**Leverantörsvärde-mönstret (Sandviken-precedent):** när en tariffs debiterbara effekt/band
inte kan beräknas automatiskt av en fullständigt publicerad formel, men leverantören ändå
kan uppge/fakturera värdet, klassas tariffen ändå `ready_to_implement` — med det värdet som
obligatorisk, synlig användarindata (motsvarande Sandvikens `debiterbar_effekt_kw`), inte
som en extern blockering. Det är bara `blocked_external_info` när själva **prisbestämningen**
(vilken grupp/band, vilket formelkonstant, vilken periodgräns) är tvetydig i källan, eller
när en nödvändig prisdel helt saknar publicerat värde.

## 2. Inmatningslägen — generell regel

Per [PROJECT_CHARTER §2](../PROJECT_CHARTER.md) och `icke-mål`: ett inmatningsläge utan
entydig, verifierad modell blockeras, det gissas aldrig. Det ger två mönster i praktiken:

- **De sex legacy-tarifferna (Göteborg, Gotland ×2, Halmstad, Mölndal, Norrenergi) samt
  Riksgenomsnittet och Stockholm Exergi:** MWh-läge fungerar; kr-läge fungerar redan i dag
  via den generiska fixpunktsloopen (`mwhFranArskostnadForFjarrvarme`) eftersom ingen av dem
  kräver en kontraktsgated, obligatorisk indata; schablon fungerar (uppskattad effekt).
- **Sandviken och varje ny tariff som (liksom Sandviken) har en genuint obligatorisk,
  icke-härledbar användarindata** (effekt, band, kategorital, U-värde …): MWh-läge kräver
  den obligatoriska indatan, kr-läge och schablon blockeras tills en egen, verifierad
  invers/schablonmodell byggs och godkänns separat (`annual_inverse` är uttryckligen
  `not-approved` för Sandviken i dag, se granskning `2026-09-06-006`).

Nästan alla `ready_to_implement`-produkter nedan hör till det andra mönstret, eftersom det är
just en obligatorisk effekt-/bandindata som gör dem `ready_to_implement` i stället för redan
`implemented`. Undantag noteras per produkt i §3.

## 3. Redan implementerade (8 produkter)

| Tariff-ID | Leverantör | Nät/produkt | Källa | Motor | Kontrakt | UI | Lägen |
|---|---|---|---|---|---|---|---|
| `goteborg-energi-goteborg-2026` | Göteborg Energi | Göteborg | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `gotlands-energi-gotland-taxa-17-under-50-mwh-ar-2026` | Gotlands Energi | Taxa 17, <50 MWh/år | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026` | Gotlands Energi | Taxa 21, ≥50 MWh/år | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `halmstads-energi-och-miljo-halmstad-2026` | Halmstads Energi och Miljö | Halmstad | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `molndal-energi-molndal-kallered-och-lindome-2026` | Mölndal Energi | Mölndal, Kållered, Lindome | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `norrenergi-norrenergi-2026` | Norrenergi | Norrenergi | ✅ legacy | ✅ | Ej kontraktsgated | ✅ valbar | mwh, kr, schablon |
| `sandviken-energi-sandviken-normal-2026` | Sandviken Energi | Helleverans | ✅ granskning `2026-09-07-003` | ✅ | ✅ `POLICYREGISTER`, `annual_forward` | ✅ valbar | mwh (obligatorisk effekt ≥3 kW); kr/schablon blockerade |
| `stockholm-exergi-2025`/`-2026` | Stockholm Exergi | Normal | ✅ fakturavaliderad (18 fakturor, Brf Åkermannen 33) | ✅ | `validated`-policy, `monthly_invoice` (`2026-09-06-003`) | ✅ valbar (via legacy års-/kr-väg, inte kontraktsfasaden — se §4) | mwh, kr, schablon |

**Anmärkning Stockholm Exergi:** produktvägen i kalkylatorn i dag använder fortfarande den
legacy årsberäkningen (`beraknaBesparingsvarde` utan kontraktsgren), inte
`beraknaArskostnadMedKontrakt`. Det källgranskade `monthly_invoice`-kontraktet
(`2026-09-06-003`) piloterar bara fakturaexakt återspelning (Ändamål A), inte kalkylatorns
årsprognos (Ändamål B) eller kr-inversen (Ändamål C). Det gör inte resultatet fel — det är
en redan godkänd, medveten avgränsning — men det betyder att Stockholm Exergis
årsberäkningsväg tekniskt sett ÄR densamma legacy-mekanism som de sex ursprungliga
tarifferna, inte kontraktsfasaden. Ingen åtgärd krävs; noterat för fullständighet.

## 4. Redo att implementera (43 produkter)

Grupperat efter familj/adapter. `Indata` anger den föreslagna obligatoriska
leverantörsvärde-indatan (Sandviken-mönstret) där tillämpligt.

### 4.1 Familj 4-resten + Telge (5 produkter) — Sandviken-mönstret rakt av

Redan i detalj kartlagt i [teknisk-kartläggning v4](teknisk-kartlaggning-28-tariffer.md)
(Familj 4/Telge-raden i tabellen), källgranskat i verifieringslistan (alla ✅/[x]).

| Tariff-ID | Leverantör | Indata | Övrigt |
|---|---|---|---|
| `karlstads-energi-karlstad-2026` | Karlstads Energi | Debiterbar effekt (kW) | `capacity.rate_period: month`, ej dividera årsavgift med 12 |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | Södertörns Fjärrvärme | Debiterbar effekt (kW) | Kundvald effekt har egen överuttagsavgift — INTE med i denna batch, blockera det fallet explicit |
| `vanerenergi-mariestad-och-toreboda-2026` | VänerEnergi | Debiterbar effekt (kW) | Månadsperiodisering redan verifierad (1/12) |
| `ovik-energi-ornskoldsvik-2026` | Övik Energi | Debiterbar effekt (kW) | Katalogrättelse: `fixed: null`→0, `monthly_proration` → kalenderdagsviktning |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | Telge Nät | Debiterbar effekt (kW) + `normalarskorrigerad_energi_mwh` | Formeltext säger "effektpris" men enheten kräver `effektbehov` — katalogens tolkning är den dimensionsriktiga |

### 4.2 E.ON/Navirum — rullande högutväxling (8 produkter)

Gemensam adapter: `supply_temperature_adjusted_flow` (känd formel, `0,02×(Tf−60)+0,2`).
`accuracy: snapshot` (inte `exact`) med ett enda leverantörseffektvärde, per
[teknisk-kartläggning](teknisk-kartlaggning-28-tariffer.md).

| Tariff-ID | Leverantör | Indata |
|---|---|---|
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | E.ON Järfälla | Effekt, `Tf`, `flode_m3` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | E.ON Järfälla | Samma |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | E.ON Malmö | Samma (katalogrättelse −15→−8 °C) |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | E.ON Malmö | Samma |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | Navirum Norrköping/Söderköping | Samma |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | Navirum Norrköping/Söderköping | Samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | Navirum Örebro/Kumla/Hallsberg | Samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | Navirum Örebro/Kumla/Hallsberg | Samma |

Endast fullvärmekunder ingår i denna batch (regressionsmetoden); övriga värmekällor
(36-månadersmetoden) är källverifierade men kan tas i en egen, mindre delbatch.

### 4.3 Leverantörsvärde-mönstret — annars fristående tariffer (26 produkter)

Var och en har en egen, redan källgranskad prisstruktur (ingen delad formel utöver
motorns befintliga `selected_band_affine`/säsongsenergi), men effekten/bandet fastställs
med leverantörens eget värde i stället för en fullt publicerad automatisk beräkning.

| Tariff-ID | Leverantör | Indata / villkor |
|---|---|---|
| `eskilstuna-energi-och-miljo-eskilstuna-2026` | Eskilstuna Energi och Miljö | Prisgrundande effekt/band |
| `falu-energi-vatten-falun-2026` | Falu Energi & Vatten | — (fullt källverifierat, ingen effekt-osäkerhet) |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | Falu Energi & Vatten (ytterorter) | Spärr: endast 0–500 kW, stoppa över |
| `habo-energi-habo-2026` | Habo Energi | — |
| `jamtkraft-ostersund-froson-as-2026` | Jämtkraft | `billing_basis_method`: medel tre högsta dygnsmedeleffekter senaste 12 mån |
| `jamtkraft-brunflo-och-opevagen-2026` | Jämtkraft | Samma |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | Jämtkraft | Samma |
| `jonkoping-energi-jonkoping-och-granna-2026` | Jönköping Energi | `billing_basis_method`: medel tre av fem högsta dygnsmedeleffekter senaste 12 mån; accessavgift EJ med i kärntariffen |
| `kils-energi-kil-2026` | Kils Energi | Avtalets kategorital ELLER leverantörens effektvärde |
| `kraftringen-kraftringen-2026` | Kraftringen | Flödesformel `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)`; endast ordinarie nät (Brunnshög `not_applicable` i denna batch) |
| `lulea-energi-lulea-2026` | Luleå Energi | Leverantörens fakturavärde för debiterbar effekt |
| `mjolby-svartadalen-energi-mjolby-2026` | Mjölby Svartådalen Energi | — |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` | Mälarenergi | — (fast avgift, ej effektberoende) |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | Nevel | Fakturans E-värde |
| `partille-energi-partille-2026` | Partille Energi | Leverantörens band vid 2 500 kW-gränsen |
| `piteenergi-pitea-centrala-natet-2026` | PiteEnergi | Uppmätt effekt/band |
| `piteenergi-norrfjarden-och-sjulnas-2026` | PiteEnergi | Samma |
| `skovde-energi-skovde-2026` | Skövde Energi | — |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | Söderhamn Nära | Leverantörens anslutningseffekt |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | TEMAB Fjärrvärme | Kategorital eller anslutningsvärde |
| `tekniska-verken-katrineholm-katrineholm-2026` | Tekniska Verken Katrineholm | Leverantörens effektsignatur/-grupp |
| `tekniska-verken-linkoping-linkoping-2026` | Tekniska Verken Linköping | Samma; endast normal leverans (lågtemperaturvärme `not_applicable`) |
| `trollhattan-energi-trollhattan-2026` | Trollhättan Energi | — |
| `umea-energi-umea-enkel-2026` | Umeå Energi | Leverantörens A- och B/U-värden (normalårskorrigering ej publicerad — får aktiveras med leverantörens värden enligt källan själv) |
| `oresundskraft-helsingborg-normal-2026` | Öresundskraft | Fakturans effektvärde |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | Öresundskraft | Samma |
| `oresundskraft-angelholm-normal-2026` | Öresundskraft | Samma |

### 4.4 Motorarbete krävs — nya formeltyper (2 produkter, Del B)

| Tariff-ID | Leverantör | Motorarbete | Indata |
|---|---|---|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | Borås Energi och Miljö | Ny kapacitetsform (`heterogeneous_bands`, grupp 1–2 mot `Wn`, grupp 3–6 mot `Q`) | Leverantörens prisgrupp, `Wn` eller `Q`; automatisk gruppindelning vid exakta gränser (40/150/600/2000/7000 MWh) blockeras, leverantören väljer grupp |
| `finspangs-tekniska-verk-finspang-2026` | Finspångs Tekniska Verk | Ny kapacitetsformel (`piecewise_polynomial`, känd formel) | Leverantörens P-värde; spetsvärme-tillägget (20 %) `not_applicable`/uppskjutet i denna batch |

### 4.5 Ren energitariff — engångsjustering (1 produkt)

| Tariff-ID | Leverantör | Arbete |
|---|---|---|
| `sundsvall-energi-indal-liden-och-lucksta-2026` | Sundsvall Energi | Sätt `capacity.type: "not_applicable"` (`EJ_TILLAMPLIG_KAPACITETSFORM`) på den riktiga katalograden — mekanismen är redan byggd och testad mot en fixture (etapp 1–4, 2026-09-04), bara inte aktiverad mot denna rad |

## 5. Blockerade av extern information (27 produkter)

Endast produkter där prisbestämningen själv är tvetydig, motsägs, eller där en obligatorisk
prisdel helt saknar publicerat värde. Frågan i sista kolumnen är den som ska skickas till
leverantören.

| Tariff-ID | Leverantör | Exakt saknad uppgift/fråga |
|---|---|---|
| `borlange-energi-borlange-2026` | Borlänge Energi | Vilken effektgrupp gäller exakt vid 501 kW och intervallet direkt ovanför? |
| `c4-energi-kristianstad-2026` | C4 Energi | Vilken effektgrupp gäller exakt vid 500 kW? |
| `gavle-energi-gavle-2026` | Gävle Energi | Beräknas volymavdraget marginalt eller på hela månadens volym efter uppnådd nivå? |
| `harnosand-energi-miljo-harnosand-2026` | Härnösand Energi & Miljö | Prislistans räkneexempel (1 750 MWh) motsäger den publicerade intervalltabellen — vilken är korrekt? |
| `hassleholm-miljo-hassleholm-2026` | Hässleholm Miljö | Beräknas effektrabatten intervallvis eller på hela effekten? |
| `hassleholm-miljo-tyringe-2026` | Hässleholm Miljö (Tyringe) | Samma fråga |
| `lidkoping-energi-lidkoping-041-kw-2026` | Lidköping Energi | 2026 års flödesprisfaktor `N` och nätmedelvärde `Tm` — helt saknade i 2026-underlaget |
| `lidkoping-energi-lidkoping-42-kw-2026` | Lidköping Energi | Samma |
| `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026` | Mälarenergi | Sommarperiodens avgränsning, överuttagsavgiftens debitering, flödesavgiftens sats över nätmedel — plus ny energiform (`base_peak_summer`) i motorn |
| `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026` | Mälarenergi | Samma, plus om flödespremien alls gäller gruppanslutna småhus |
| `skelleftea-kraft-skelleftea-skelleftehamn-ursviken-lycksele-mala-2026` | Skellefteå Kraft | Valutaenhet för energirabatten (`Qnorm×A+B`) samt dimensionerande temperatur för Ursviken |
| `skelleftea-kraft-boliden-burea-burtrask-byske-jorn-kage-lovanger-norsjo-robertsfors-stensele-storuman-vindeln-anaset-2026` | Skellefteå Kraft | Samma, dimensionerande temperatur för Stensele |
| `sundsvall-energi-sundsvall-normal-2026` | Sundsvall Energi | Hur får kunden nätvärdet `Qalla/Walla` för flödespremien varje månad (formel i övrigt känd)? Blockera dessutom automatisk prissättning ≥2000 kW |
| `sundsvall-energi-matfors-och-kvissleby-normal-2026` | Sundsvall Energi | `network_m3_per_MWh` (nätreferens för flödesjusteringen) saknas helt som katalogdata — teknisk-kartläggning v4 överprövar verifieringslistans ✅ här, se dess P4-rättelse |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-standard-2026` | Vattenfall | `asymmetric_flow_difference` (3.3) — nätreferensen är inte verifierad som ett statiskt katalogvärde. Hela tariffgruppens resultat förblir `blocked` tills 3.3 löses, per teknisk-kartläggning v4 (medvetet, oavsett att 3.1/3.2/3.4 är byggbara) |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-spetsig-2026` | Vattenfall | Samma |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-standard-2026` | Vattenfall | Samma |
| `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-spetsig-2026` | Vattenfall | Samma |
| `vattenfall-motala-och-askersund-motala-och-askersund-standard-2026` | Vattenfall | Samma |
| `vattenfall-motala-och-askersund-motala-och-askersund-spetsig-2026` | Vattenfall | Samma |
| `vattenfall-nykoping-nykoping-standard-2026` | Vattenfall | Samma |
| `vattenfall-nykoping-nykoping-spetsig-2026` | Vattenfall | Samma |
| `vattenfall-uppsala-uppsala-standard-2026` | Vattenfall | Samma |
| `vattenfall-uppsala-uppsala-spetsig-2026` | Vattenfall | Samma |
| `vattenfall-vanersborg-vanersborg-standard-2026` | Vattenfall | Samma |
| `vattenfall-vanersborg-vanersborg-spetsig-2026` | Vattenfall | Samma |
| `vb-energi-normal-2026` | VB Energi | Effektperiod nov–mar eller dec–mar (två officiella källor motsäger varandra); vilket mät-/normalår och omprövningsdag styr prisgrupp; plus ny energiform (`annual_volume_band_monthly`) i motorn |

## 6. Ej tillämpligt (2 enheter)

| Post | Motivering |
|---|---|
| Riksgenomsnittet (`leverantor-riksgenomsnitt.md`) | Syntetisk nationell schablon för när leverantören är okänd — inte ett tariffprodukt att implementera. Se produktdirektivets öppna beslut (§8) om hur den ska presenteras när en namngiven leverantör saknas. |
| `stockholm-exergi-stockholm-exergi-normal-2026` (katalograd) | Duplikat av den redan implementerade, fakturavaliderade leverantörsfilen (§3). Katalogradens `energiform`-avvisning (`monthly_with_peak_volume_replacement`) kräver motorarbete för att katalogspåret ska kunna ersätta leverantörsfilen — inget som blockerar produkten, bara en framtida konsolidering om/när det prioriteras. Räknas inte som en egen implementationspost. |

## 7. Räkningskontroll

| Disposition | Antal |
|---|---:|
| `implemented_source_verified_annual` | 8 |
| `ready_to_implement` | 43 |
| `blocked_external_info` | 27 |
| `not_applicable` | 2 |
| **Summa** | **80** |

Stämmer mot kontrollmängden: 78 katalograder + 2 separat förvaltade leverantörsfiler = 80.
Deduplicerat till 79 unika PRODUKTER (Stockholm Exergis katalograd och leverantörsfil är
samma produkt, räknad en gång i §3, en gång som duplikat i §6).

**Leverantörer vs. tariffprodukter:** 53 leverantörer i katalogen + Stockholm Exergi +
Riksgenomsnittet = 55 unika leverantörsentiteter (varav riksgenomsnittet inte är en
fjärrvärmeleverantör). 80 tariffrader fördelat på dessa — flera leverantörer (t.ex.
Vattenfall, E.ON, Navirum, PiteEnergi, Öresundskraft, Skellefteå Kraft, Hässleholm Miljö,
Tekniska Verken, Jämtkraft) har mer än en produkt (nät/ort/produktvariant).

**Dubbletter funna:** exakt en — Stockholm Exergis katalograd mot dess leverantörsfil (§6).
Inga andra katalograder beskriver samma leverantör+nät+produkt+kundkategori två gånger.

## 8. Öppna frågor till Codex

1. **Vattenfalls disposition:** jag har följt teknisk-kartläggning v4:s redan granskade
   slutsats (`blocked` som HELA tariffgruppen tills 3.3 löses) rakt av, i stället för att
   själv ompröva den. Om Robert/Codex vill dela upp Vattenfall i en delbatch där 3.1/3.2/3.4
   byggs och testas internt medan 3.3 kvarstår blockerad (vilket teknisk-kartläggningen
   själv nämner som möjligt), bör det beslutas explicit — se batchplanen §3.3.
2. **Sundsvall Matfors-motsägelsen:** verifieringslistan (2026-09-04) markerar raden ✅,
   men teknisk-kartläggning v4 (samma datum, senare i sekvensen, Codex-godkänd) klassar den
   `blocked` på grund av saknad `network_m3_per_MWh`. Jag har följt teknisk-kartläggningen
   som auktoritativ eftersom den är den senare, mer detaljerade och redan granskade analysen
   — men flaggar den öppna motsägelsen mellan de två källdokumenten för synlighet.
3. **"Leverantörsvärde-mönstret" som generell policy:** jag har klassat ~26 produkter
   `ready_to_implement` enbart för att källan säger "använd leverantörens
   effekt-/bandvärde tills metoden implementerats" — samma mönster som Sandviken. Om Codex
   eller Robert anser att någon av dessa i praktiken kräver mer källverifiering innan den
   räknas som redo (t.ex. att leverantörens värde är svårt för en kund att själv hitta på
   fakturan), bör det flaggas per tariff i granskningen av denna inventering, inte antas
   löst av mig.
4. **Öresundskraft, Öviks m.fl. `not_applicable`-varianter** (kundvald effekt hos
   Södertörn, lågtemperaturvärme hos Tekniska Verken Linköping, Brunnshög hos Kraftringen,
   spetsvärme hos Finspång): jag har föreslagit att dessa specialfall lämnas explicit
   `not_applicable`/blockerade inom respektive batch snarare än att försena hela tariffen.
   Om det anses fel avvägning, säg till innan batchplanen genomförs.
