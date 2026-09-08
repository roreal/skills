# Batchplan v6.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-08 av Claude. Ersätter `batchplan-v5.md` i sin helhet (v5 ändras INTE i
efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-08-005](../conversations/reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v5.md)
(supersedes `2026-09-08-004`). Bygger på dispositionerna i
[`tariffinventering-v6.md`](tariffinventering-v6.md) §4.1 (45 bastariffer) och §5 (9
`ready_to_implement`-varianter), samt §6/§6a:s sammansatta aktiveringspreflight och §7:s
`tariff_ids`-baserade livscykel för informationsförfrågningar. Ingen batch är påbörjad —
detta är ett förslag till Codex granskning och Roberts prioritering.

**Vad som är nytt i v6** (se granskning `2026-09-08-005` för fullständig motivering):

1. **Batch 2 (Sundsvall Indal) omskriven i grunden.** v5 påstod att tariffen "går på
   legacy-vägen utan kontraktskrav" — VERIFIERAT FEL: tariff-ID:t
   `sundsvall-energi-indal-liden-och-lucksta-2026` finns inte i `LEGACY_UNDANTAGNA_TARIFF_ID`
   (bara sex ursprungliga uppgift-7-tariffer), så `bygg_ts_fran_katalog()` hade kastat om
   batchen byggts som skriven. Batchen kräver nu en riktig `Tariffpolicy`
   (Sandviken-mönstret, `contract_required: true`), vilket gör tariffen kontraktsgated —
   "Visas för användaren" rättad från "mwh, kr och schablon" till mwh-only, kr/schablon
   blockerade, konsekvent med den generella regeln.
2. Batch 4 (Umeå): `B`-bindningen namngiven konkret som `kapacitet_multiplikator_bindning`
   med `minvarde=0.93`/`maxvarde=1.4` (nytt kontraktsfält, se inventeringens §6a.3) i
   stället för v5:s ospecificerade "A/B leverantörsvärde".
3. Batch 1 (Borlänge/C4, om de flyttas hit senare) och Falu-raden i 5b: hänvisar nu till
   inventeringens §6a.1/§6a.2 (`KravPost.maxvarde`, `supplier_confirmed_band_id`) i stället
   för att bara säga "normalisera issue-texten".
4. Batch 7 (Stockholm Exergi): omskriven till EXKLUDERING av katalograden och en utökad
   leverantörsfilsadapter (inventeringens §6a.4) — v5:s "namngiven adapter" band fortfarande
   katalog-ID:t, vilket hade skapat en andra, dubblerande produkt-ID (verifierat:
   `_stabilt_tariff_id` ger `stockholm-exergi-stockholm-exergi-normal`, skilt från
   leverantörsfilens `stockholm-exergi`).
5. Samtliga batchers filistor och "TA BORT"/"tariff_ids sätts"-rader räknade om mot den
   nya §7 i inventeringen — inget "SPLITTA" kvar.
6. Batch 6 och Borås-semantiken skriven om till "2 bastariffer + 1 varianttäckning" konsekvent
   med räkningsmodellen i inventeringens §8 (v5:s batchsumma 54 i stället för 55 berodde på
   att Borås miljötillägg räknades otydligt).

## Gemensamt för samtliga batcher (Sandviken-mallen)

Oförändrat — se granskningarna `2026-09-06-004` till `2026-09-07-003` för den fullt
utarbetade mallen (katalogändring → `Tariffpolicy` med `minvarde`/`heltal` → produktsidans
`kontraktsgatadPolicy`/`KontraktBlockerat`/`energyProvenance` återanvänd rakt av → kr/schablon
blockerade → golden-/gräns-/kontraktsfasad-/produktadapter-/diff-/momstest i båda språk →
tre fokuserade lokala commits, Codex-granskning, push i ordningen skills → enkey-agents →
neptune_academy).

## Batch 1 — Familj 4-resten + Telge + Partille (6 tariffer)

Ligger FÖRST enligt överlämningens ordningsregel (ingen kund-/prospektprioritet är angiven).

- **Tariffer:** `karlstads-energi-karlstad-2026`,
  `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`,
  `vanerenergi-mariestad-och-toreboda-2026`, `ovik-energi-ornskoldsvik-2026`,
  `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`,
  `partille-energi-partille-2026`.
- **Modell:** Sandviken-mönstret. Ingen ny motorkod — samtliga fält (effekt,
  `temperature_difference`, `low_utilization`, `incremental_return_temperature`) finns
  redan i `JUSTERINGSTYPER`. Partille tillagd i v3 (samma `temperature_difference`-mönster
  som Göteborg/Södertörn; v1/v2 utelämnade felaktigt att den har ett obligatoriskt
  temperaturfält, granskning `2026-09-08-001`).
- **Avvikande regler:** Övik behöver katalogrättelse (`fixed`, `monthly_proration`) FÖRE
  aktivering. Telge behöver TRE obligatoriska fält (effekt, normalårskorrigerad energi,
  returtemperatur), inte ett. Södertörn: bara SFAB:s rekommenderade effekt +
  returtemperaturavvikelse aktiveras — kundvald effekt med överuttagsavgift är en egen,
  blockerad variant (`sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026--kundvald-effekt`,
  inventeringens §5), inte del av denna batch. Partille: effekt + returtemperaturavvikelse,
  formeln `energi_MWh×7×avvikelse`, redan känd typ.
- **Obligatorisk indata:** debiterbar effekt (kW) för alla sex; VänerEnergi dessutom
  helårsflöde i m³ (fakturan, `volume`-justering, gäller alla 12 månader — rättat i v4,
  granskning 2026-09-08-003, P1: v3:s batchtext saknade detta fält trots att inventeringens
  rad och katalogens `adjustments` redan hade det); Telge dessutom normalårskorrigerad
  energi (MWh) och returtemperatur (°C); Södertörn och Partille dessutom
  returtemperaturavvikelse (°C).
- **Filer:** 6× katalograd, `policyregister.py` (6 nya policyer).
- **Teststrategi:** en `test_familj4_resten_kontrakt.py`, golden-värden mot respektive
  prislista, gränstest vid varje bands golv/tak, Telges tre fälts blockering testad separat.
- **Visas för användaren:** mwh-läge med tariffspecifika obligatoriska fält; kr/schablon
  blockerade.

## Batch 2 — Sundsvall Indal, Liden och Lucksta (1 tariff, minst risk)

- **Tariff:** `sundsvall-energi-indal-liden-och-lucksta-2026`.
- **Modell:** ren energitariff, `capacity: {"type": "not_applicable"}`. `EJ_TILLAMPLIG_
  KAPACITETSFORM`-mekanismen (byggd och testad mot fixture sedan etapp 1–4, 2026-09-04) tar
  bort ALLA grindstopp relaterade till kapacitetsformen. Det räcker DÄREMOT INTE för
  aktivering — se rättelsen nedan.
- **RÄTTAD (granskning 2026-09-08-005, P1): tariffen kräver en riktig `Tariffpolicy`, inte
  legacy-vägen.** v5 påstod felaktigt att en ren energitariff "går på legacy-vägen utan
  kontraktskrav". Verifierat direkt mot `policyregister.py`:
  `sundsvall-energi-indal-liden-och-lucksta-2026` finns INTE i `LEGACY_UNDANTAGNA_TARIFF_ID`
  (frozensetten innehåller uteslutande de sex tariffer som redan var produktionsgodkända
  INNAN resultatkontraktet fanns — Sundsvall Indal är inte en av dem). Generatorns
  `bygg_ts_fran_katalog()` kräver därför `contract_required: true` OCH en registrerad,
  komplett `Tariffpolicy` för denna rad, precis som för Sandviken — annars `raise`:er den.
  Batchen bygger alltså en MINIMAL policy: `capacity_bindning=None` (ingen kapacitetsdel
  att binda), `kravda_falt` bara energi (ingen effekt), `tackning={"annual_forward"}`. Samma
  mönster Sandviken redan bevisat, ingen ny mekanism.
- **Obligatorisk indata:** ingen utöver energimängd (MWh) — men eftersom tariffen nu blir
  kontraktsgated gäller den generella regeln (§2): kr och schablon blockeras tills en egen
  `annual_inverse`-fasad finns, inte "alla tre lägen" som v5 påstod.
- **Filer:** katalog-JSON (`contract_required: true`), `policyregister.py` (ny minimal
  policy), `godkanda()`-testet i `test_katalog.py` (räknaren 7→8), `remaining_information_
  requests` (R14 får `tariff_ids` satt till de två fortsatt blockerade Sundsvall-tarifferna
  — se inventeringens §7 — INTE en "delning" av `member_ids`, som datastrukturen inte
  stödjer idag).
- **Teststrategi:** regressionstest att `grind()` godkänner raden, golden-värde mot
  100,8 öre/kWh via KONTRAKTSFASADEN (inte naket `arskostnad`-anrop), test att
  `bygg_ts_fran_katalog()` INTE kastar för denna rad, kr/schablon-blockeringstest (samma
  mönster som Sandvikens `unsupported_input_mode`).
- **Visas för användaren:** mwh-läge endast, med källverifierat energipris. Kr och schablon
  blockerade — RÄTTAT från v5:s "mwh, kr och schablon, alla tre", som byggde på det felaktiga
  legacy-antagandet ovan.

## Batch 3 — Delad flödeskorrigeringsmotor: E.ON, Navirum, Kraftringen (9 tariffer)

- **Tariffer:** `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`,
  `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`,
  `e-on-malmo-malmo-och-burlov-bostader-2026`,
  `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`,
  `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`,
  `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`,
  `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`,
  `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`,
  `kraftringen-kraftringen-2026`.
- **Modell (rättat i v4, granskning 2026-09-08-003, P1):** NY motorkod:
  `supply_temperature_adjusted_flow` i `justeringar.py` (speglad inline i `fjarrvarme.ts`) som en
  PARAMETRISERAD motortyp med TVÅ verifierade regelvarianter, inte en enda odelad formel —
  v3:s odelade formel skulle underdebitera Kraftringen vid `Tf < 60 °C`:
  - **E.ON/Navirum** (8 tariffer): `volym × base_rate × (0,02×(Tf−60) + 0,2)`, INGET golv.
    Källverifierad i verifieringslistan (`03_0`/`04_0`/`25_0`/`26_0`) — katalogens egna
    `correction_formula`-fält är `null` för samtliga åtta rader (verifierat direkt mot
    JSON), formeln är alltså INTE katalognativ.
  - **Kraftringen** (1 tariff): `volym × 10,40 × max(0,2; 0,2 + (Tf−60)×0,02)` — MED golv
    vid 0,2. Katalogens `candidate_factor`-fält bär redan denna exakta sträng.
  `noggrannhet: snapshot` (aldrig `exact`) när effekten är ett enskilt leverantörsvärde —
  effekten är en rullande 12-månadersserie i källan.
- **Avvikande regler:** Malmö/Burlöv `-15→-8 °C` katalogrättelse. Endast fullvärmekunder i
  denna batch — E.ON/Navirums 36-månadersmetod byggs som EGNA variant-ID:n i batch 3b, INTE
  samtidigt. Kraftringens Brunnshög är en egen, blockerad variant
  (`kraftringen-kraftringen-2026--brunnshog`), inte del av denna batch.
- **Obligatorisk indata:** debiterbar effekt, medelframledningstemperatur `Tf` (°C), flöde
  (m³) — samtliga tre för samtliga nio tariffer. Kraftringens `Tf` är den
  FÖRBRUKNINGSVÄGDA månadsmedelframledningstemperaturen (fakturan/nätdata) — samma fält som
  E.ON/Navirums, inte ett separat krav.
- **Filer:** katalograder ×9, EN delad motorformel i `justeringar.py` (speglad inline i
  `fjarrvarme.ts`), `policyregister.py` (parametriserad policyfunktion, likt
  `_stockholm_exergi_policy`), `remaining_information_requests` (R06 TAS BORT, R10 TAS
  BORT — se inventeringens §7).
- **Teststrategi:** golden-värde mot minst en orts publicerade räkneexempel, gränstest för
  flödesformelns temperaturberoende, `noggrannhet: snapshot`-regressionstest, kontraktsfasad-
  test i båda språk. `okand_justering`-regressionstest att `supply_temperature_adjusted_flow`
  nu är känd men fortfarande blockerar tariffer som saknar `Tf`/flöde. MINST ETT
  gränstest per regelvariant (rättat i v4): E.ON/Navirum vid `Tf` under/vid/över 60 °C utan
  golv, och Kraftringen specifikt vid `Tf < 60 °C` som bevisar att golvet 0,2 tillämpas i
  stället för att formeln tillåts gå under det.
- **Visas för användaren:** mwh-läge, tre obligatoriska fält; resultat märkt uppskattning
  (snapshot); kr/schablon blockerade.

## Batch 3b — E.ON/Navirums 36-månadersvariant (8 variantrader, EFTER batch 3)

**Rättat i v4 (granskning 2026-09-08-003, P1):** v3 krävde felaktigt ett "36 månaders
rullande medelvärde av framledningstemperatur" som obligatorisk indata. Den verifierade
regeln (verifieringslistan) gäller i stället medelvärdet av de TRE HÖGSTA
DYGNSMEDELEFFEKTERNA (kW) — effekt, inte temperatur — under de senaste 36 månaderna
inklusive fakturamånaden. Valt kontrakt: leverantörens egna 36-månadersberäkning tas emot
som leverantörsvärde (SAMMA mönster som batch 3:s huvudfall, vars effekt också kommer från
leverantörens beräkning, inte en kalkylatorregression). Ingen ny 36-månaders tidsseriemotor
byggs i kalkylatorn — v3:s formulering "plus det rullande 36-månadersvärdet" var
självmotsägande (tre fält, sedan ett fjärde).

- **Tariffer:** de åtta variant-ID:n i inventeringens §5
  (`<bas-id>--bas-delvarme`, en per E.ON/Navirum-bastariff i batch 3).
- **Modell:** leverantörsvärde-mönstret för kunder med bas-/delvärmekälla i stället för
  fullvärme — ingen ny beräkningsmotor, bara en ny `Tariffpolicy`-variant per bastariff där
  källan till effektfältet är leverantörens 36-månadersberäkning i stället för
  -15 °C-regressionen.
- **Obligatorisk indata:** debiterbar effekt (kW, fakturan — leverantörens
  36-månadersberäkning), medelframledningstemp `Tf` (°C, fakturan) OCH flöde (m³, fakturan)
  — SAMMA tre fält som batch 3:s huvudformel, ingen fjärde.
- **Filer:** 8× ny variant-`Tariffpolicy` (leverantörsvärde-mönstret, samma kod som redan
  används för Sandviken/batch 5). INGEN ny formelkod i `justeringar.py` (speglad inline i `fjarrvarme.ts`).
- **Teststrategi:** kontraktsfasadtest att debiterbar effekt tas emot rakt av som
  leverantörsvärde utan intern 36-månadersberäkning, regressionstest att bas-/
  delvärmevarianten inte påverkar fullvärme-batchens `snapshot`-resultat.
- **Visas för användaren:** mwh-läge, SAMMA tre fält som batch 3 (debiterbar effekt, `Tf`,
  flöde) — bara källan till effektvärdet skiljer sig; kr/schablon blockerade.

## Batch 4 — Egna flödesformler: Jämtkraft, Umeå (4 tariffer)

**Eskilstuna borttagen i v3** (flyttad till `blocked_external_info`, se inventeringens §4.2
— nätreferensen `monthly_mean_for_customers_covered_by_flow_tariff` är inte verifierad som
ett stabilt katalogvärde eller en fakturapost, till skillnad från Umeås statiska referens).

- **Tariffer:** `jamtkraft-ostersund-froson-as-2026`, `jamtkraft-brunflo-och-opevagen-2026`,
  `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
  (samtliga tre `flow_difference`), `umea-energi-umea-enkel-2026`
  (`asymmetric_flow_difference` OCH en ny `post_multiplier`-medveten kapacitetsmotor — se
  nedan, rättat i v5, granskning 2026-09-08-004, P1: v4 saknade kapacitetsdelen helt).
- **Modell:** TVÅ separata nya justeringstyper i `justeringar.py` (speglad inline i `fjarrvarme.ts`) —
  `flow_difference` (Jämtkraft, formel `3×(flöde_m3 − 19×energi_MWh)`, referensvärdet 19
  m³/MWh redan statiskt i katalogen) och `asymmetric_flow_difference` (Umeå, `bonus_rate: 3`,
  `fee_rate: 7`, `reference_m3_per_MWh: 17`, allt statiskt). DESSUTOM för Umeå ENSAM: en ny
  kapacitetsmotor som accepterar `post_multiplier` som ett bundet leverantörsvärde `B` —
  `grind()` avvisar i dag varje post med `post_multiplier` (`kapacitetsformel med
  multiplikator`); ändringen gör att en tariff GODKÄNNS när `B` är bundet via det NYA,
  namngivna `Tariffpolicy`-fältet `kapacitet_multiplikator_bindning` (se inventeringens
  §6a.3) — INTE ett generellt undantag som öppnar `post_multiplier` för alla tariffer.
  `B` valideras mot `minvarde=0.93`/`maxvarde=1.4` (katalogens egna `pieces`-brytpunkter,
  samma `minvarde`/`maxvarde`-mekanism som §6a.1). Kalkylatorn räknar ALDRIG själv ut
  `U = normalårskorrigerad_energi_dec_jan_feb / energi_sep_apr` (bolagets normalårskorrigering
  är inte publicerad) — bara det redan beräknade `B`. Ingen väntar på leverantörsbesked.
- **Avvikande regler:** `okand_justering`-regression att `asymmetric_flow_difference` inte av
  misstag öppnar upp Vattenfalls BLOCKERADE variant av samma typnamn (Vattenfalls referens är
  `"network_average"`, dynamisk — Umeås är ett statiskt tal; koden får inte dela logik som
  antar det ena för det andra utan en explicit typkontroll). Umeås `issues`-text ("Hela
  effektkostnaden multipliceras med B...") TAS BORT — löst av A/B-kontraktet.
- **Obligatorisk indata:** Jämtkraft (tre tariffer): debiterbar effekt + flöde oktober–april
  (m³, `months: [1,2,3,4,10,11,12]`, 7 månader). Umeå (rättat i v5): debiterbar effekt, flöde
  okt–apr, OCH kapacitetsfaktorn `B` (leverantörens eget redan beräknade värde) — TRE
  obligatoriska fält, inte två.
- **Filer:** katalograder ×4, `justeringar.py`/`.ts` (två nya formler), `katalog.py`
  (`grind()`-ändring för `post_multiplier`), `faktura.py`/`fjarrvarme.ts` (ny
  kapacitetsberäkning för Umeå), `policyregister.py` ×4.
- **Teststrategi:** golden-värde per tariff, gränstest för respektive formels
  referensberoende, `okand_justering`-regression mot Vattenfalls/Sundsvall Matforss
  BLOCKERADE varianter av samma typnamn, samt Umeås `B`-intervall (golden-värden vid
  `B=0.93`, `B=1.4` och en mellanliggande punkt; ett negativt test för `B=14` utanför
  intervallet ska blockera) — kallat `B-intervall`, inte "U-intervall", eftersom motorn
  aldrig räknar `U`.
- **Visas för användaren:** mwh-läge; Jämtkraft: effekt + flöde; Umeå: effekt + flöde + `B`;
  kr/schablon blockerade för alla fyra.

## Batch 5a — Leverantörsvärde, ingen ytterligare justeringspost (8 tariffer)

Effekt/band är leverantörens/fakturans enda obligatoriska värde. Katalogens
`adjustments: []` för samtliga åtta — verifierat direkt mot JSON, inte antaget.

- **Tariffer:** `c4-energi-kristianstad-2026`, `kils-energi-kil-2026`,
  `skovde-energi-skovde-2026`, `trollhattan-energi-trollhattan-2026`,
  `tekniska-verken-katrineholm-katrineholm-2026`,
  `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`,
  `soderhamn-nara-soderhamn-taxa-11-och-12-2026`,
  `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`.
- **Obligatorisk indata:** debiterbar effekt/band (fakturan) — för C4 dessutom det NYA
  `supplier_confirmed_band_id`-fältet (inventeringens §6a.2): exakt 500 kW är den
  uttryckligen osäkra gränsen (band 5 `200–499` vs band 6 `>500`), så automatisk
  bandvalsautomatik (`_niva()`) accepteras INTE — kunden bekräftar band-ID direkt, och
  motorn validerar att det bekräftade ID:t faktiskt täcker det angivna kW-talet innan
  beräkning. KATALOGRÄTTELSE: C4, Kils (`kils-energi-kil-2026`, dessutom `fixed:0` på alla
  fyra band) och TEMAB (`temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`) har var
  sin `issues`-text som INTE matchar grindens godkännandelista — normaliseras till den
  redan kända typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad;
  använd leverantörens fakturavärde" (se inventeringens §6). Informationsförfrågningarna
  R05 (c4-energi), R12 (temab-fjarrvarme) TAS BORT — se inventeringens §7.
- **Filer:** 8× katalograd, `policyregister.py` (8 nya policyer, samma mönster).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5a_kontrakt.py`/`.ts`, golden-värde
  per tariff, C4:s 500 kW-gränsblockering testad explicit.
- **Visas för användaren:** mwh-läge, obligatorisk indata; kr/schablon blockerade.

## Batch 5b — Leverantörsvärde, fullårsflöde (6 tariffer)

**Rättat i v3:** dessa sex har en prissatt `volume`-post som gäller ALLA TOLV månader
(katalogens `months: [1..12]`) — v2 utelämnade flödet som obligatorisk indata för dem helt
(Codex granskning `2026-09-08-002`, P1). Ingen `months`-semantik saknas i motorn för dessa
(hela året, ingen säsongsgräns att missa) — bara ett nytt synligt fält, ingen ny motorkod.

- **Tariffer:** `borlange-energi-borlange-2026` (effektgrupp + flöde, 501 kW-gränsen
  blockerad), `falu-energi-vatten-falun-2026`,
  `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`, `habo-energi-habo-2026`,
  `mjolby-svartadalen-energi-mjolby-2026`,
  `jonkoping-energi-jonkoping-och-granna-2026` (accessavgiften är en egen, blockerad
  variant — `jonkoping-energi-jonkoping-och-granna-2026--accessavgift`, väntar på
  Robert-beslut, INTE del av denna batch).
- **Obligatorisk indata:** debiterbar effekt/band + prissatt flöde i m³ (hela året,
  fakturan/avtalet) för samtliga sex. Borlänge behöver DESSUTOM det NYA
  `supplier_confirmed_band_id`-fältet (§6a.2, samma mekanism som C4 i batch 5a): källan
  skriver `>501` och 501 kW är den uttryckligen osäkra gränsen mellan band 4 (`251–500`) och
  band 5 (`>501`). Falu ytterorter behöver DESSUTOM `KravPost.maxvarde=500` (§6a.1): dess
  publicerade prisgrupper går bara till 500 kW — ett mekaniskt maxkrav ersätter att bara
  förlita sig på att `_niva()` råkar kasta `ValueError` för värden utan täckande band.
  KATALOGRÄTTELSE: båda har var sin `issues`-text som inte matchar grindens
  godkännandelista — normaliseras (se inventeringens §6). Informationsförfrågningarna R04
  (borlange-energi) TAS BORT; R15 (falu-energi-vatten) TAS BORT (löst mekaniskt av
  `maxvarde`, inte av request-processen) — se inventeringens §7.
- **Filer:** 6× katalograd, `policyregister.py` (6 nya policyer med två bundna fält).
- **Teststrategi:** som 5a, plus golden-värde som inkluderar flödesavgiften för varje rad.
- **Visas för användaren:** mwh-läge, effekt/band + flöde; kr/schablon blockerade.

## Batch 5c — Leverantörsvärde, säsongsflöde (8 tariffer, kräver `months`-motorsemantik)

**Rättat i v3:** v2:s batch 5b påstod att samtliga tolv rader hade oktober–april (7
månader) — fel för nio av dem. De faktiska `months`-listorna varierar 5–9 månader per
tariff (verifierat direkt mot katalog-JSON):

| Tariff | `months` | Antal |
|---|---|---:|
| `lulea-energi-lulea-2026` | jan–maj + sep–dec | 9 |
| `oresundskraft-helsingborg-normal-2026` | jan–mar + nov–dec | 5 |
| `oresundskraft-angelholm-normal-2026` | jan–mar + nov–dec | 5 |
| `piteenergi-pitea-centrala-natet-2026` | jan–mar + okt–dec | 6 |
| `piteenergi-norrfjarden-och-sjulnas-2026` | jan–mar + okt–dec | 6 |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | jan–apr + okt–dec | 7 |
| `tekniska-verken-linkoping-linkoping-2026` (lågtemperaturvariant är en egen, blockerad variant, inte del av denna batch) | jan–apr + okt–dec | 7 |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` (ingen kapacitetsdel — fast årsavgift + energi + säsongsflöde) | jan–apr + okt–dec | 7 |

- **Motorarbete:** bygg `months`-hänsyn för `volume`-justeringen i `faktura.py`/
  `fjarrvarme.ts` — motorn och testerna MÅSTE använda varje posts EGEN `months`-lista, inget
  generellt antagande. Detta motorarbete delas av alla åtta rader men skrivs EN gång.
  Regressionstesta mot redan implementerade legacy-tariffer med `volume` (t.ex. Mölndal,
  helårs-`volume`) för att bevisa att helårsfallet inte påverkas.
- **Obligatorisk indata:** debiterbar effekt/band + säsongsflöde i m³, exakt de månader
  tabellen ovan anger, för SJU av åtta tariffer. **Undantag, rättat i v4 (granskning
  2026-09-08-003, P1):** `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` har
  INGEN kapacitetsdel i katalogen (`capacity: null`) — v3:s batchtext krävde felaktigt
  effekt/band för alla åtta. Mälarenergi behöver i stället bara ENERGI (MWh) + säsongsflöde
  (m³, jan–apr + okt–dec) utöver katalogens fasta årsavgift; ingen effekt/band-fält alls.
- **Filer:** 8× katalograd, `months`-semantik i motorn (delad), `policyregister.py` (8 nya
  policyer — Mälarenergis policy binder INGEN kapacitetsnyckel, till skillnad från övriga
  sju).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5c_sasongsflode.py`/`.ts` med ETT
  testfall per tariffs `months`-lista (inte ett delat antagande), regressionstest att
  helårs-`volume`-legacytariffer är oförändrade.
- **Visas för användaren (rättat i v5, granskning 2026-09-08-004, P2):** mwh-läge. SJU av åtta: effekt/band + säsongsflöde. Mälarenergi 2–4 lägenheter (ENDA undantaget): energi (MWh) + säsongsflöde — INGEN effekt/band, tariffen saknar kapacitetsdel helt. kr/schablon blockerade för alla åtta.

## Batch 6 — Nya kapacitetsformer (2 bastariffer + 1 varianttäckning, störst motorarbete)

**Räkningsmodell förtydligad i v4 (granskning 2026-09-08-003, P2):** denna batch bygger 2
BASTARIFFER (Borås, Finspång) plus Borås miljötillägg som en RÄKNAD VARIANTTÄCKNING
(`--miljotillagg`, inventeringens §5) i samma commit — inte en tredje fristående tariff.
Räknas som "2 + 1" i Sammanfattningen nedan, inte "2" eller "3".

**Finspångs spetsvärmetillägg borttaget från denna batch i v4** (flyttad till
`blocked_external_info` i inventeringens §5 — utlösande kunder/perioder är inte kartlagda,
vilket bröt mot `ready`-definitionen). Grundformeln (`piecewise_polynomial` +
`conditional_flow`, UTAN spetsvärmetillägget) byggs ändå i denna batch; tillägget läggs på
senare, se "Ej batchade" nedan.

- **Tariffer:** `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
  (`heterogeneous_bands`, Wn/Q-grupper — miljötillägget byggs som en kryssruta i SAMMA batch,
  se §5-varianten `--miljotillagg`), `finspangs-tekniska-verk-finspang-2026`
  (`piecewise_polynomial` PLUS `conditional_flow`, TVÅ separata nya motordelar — utan
  spetsvärmetillägget, som är blockerat).
- **Avvikande regler:** Borås — automatisk gruppindelning blockeras, leverantören/kunden
  anger grupp.
- **Obligatorisk indata:** Borås: prisgrupp + `Wn`/`Q` + valfritt miljötillägg (kundvalt
  UI-tillval, inget separat katalogfält). Finspång: `P`-värde, returtemperatur varje månad
  (avgör om `conditional_flow`s villkor >55 °C utlöses) OCH, när villkoret utlöses, månadens
  flöde i m³ (multipliceras med 20 kr/m³). Spetsvärmetillägget byggs INTE i denna batch.
- **Filer:** ny kapacitetsformelkod (`heterogeneous_bands`, `piecewise_polynomial`) i
  `faktura.py`/`fjarrvarme.ts`, `katalog.py` (`grind()` utökad med de nya
  kapacitetsformerna i sin godkännandelista — Python-sidans grind, ingen TS-tvilling),
  två nya justeringstyper (`optional_environmental_addon`, `conditional_flow`) i
  `justeringar.py` (speglade inline i `fjarrvarme.ts`), katalograder, policyer.
- **Teststrategi:** golden-värde per formel, gränstest vid gruppgränserna, regressionstest
  att kapacitetsformsutökningen inte påverkar `selected_band_affine`-tarifferna. Finspångs
  villkorade flöde testat både under och över 55 °C-tröskeln.
- **Visas för användaren:** mwh-läge, tariffspecifik obligatorisk indata; kr/schablon
  blockerade.

## Batch 7 — Stockholm Exergis årsprodukt (1 produkt, utökad leverantörsfilsadapter)

Skiljer sig från övriga batcher: `monthly_invoice`-kontraktet är redan implementerat och
fakturavaliderat — bara ÅRSVÄGEN saknar motsvarande bindning. **Katalograden aktiveras
INTE** (rättat i v6, granskning 2026-09-08-005, P1 — se inventeringens §6a.4 för fullständig
motivering).

- **Produkt:** leverantörsfilens redan verifierade `stockholm-exergi-2026` (INTE
  katalogens `stockholm-exergi-stockholm-exergi-normal-2026`).
- **RÄTTAD väg (v5:s "namngivna adapter" band fortfarande katalog-ID:t — VERIFIERAT FEL):**
  `_stabilt_tariff_id()` kördes mot den verkliga katalograden och gav
  `stockholm-exergi-stockholm-exergi-normal` — ett TREDJE, aldrig tidigare existerande
  produkt-ID, skilt från leverantörsfilens `stockholm-exergi`. Att binda adaptern till
  katalog-ID:t (v5:s plan) hade alltså skapat TVÅ valbara alternativ i UI för samma
  underliggande normalprodukt. Den nya planen: (1) leverantörsfilens `stockholm-exergi-2026`
  får en ANDRA, separat `Tariffpolicy` med `tackning: {"annual_forward"}` (vid sidan av den
  befintliga `{"monthly_invoice"}`-policyn — samma tariff-ID, två täckningsområden); (2) ett
  nytt `ADAPTERREGISTER`-register i `policyregister.py` mappar katalog-ID:t
  `stockholm-exergi-stockholm-exergi-normal-2026` → leverantörsfils-ID:t
  `stockholm-exergi-2026`; (3) `bygg_ts_fran_katalog()` läser registret och HOPPAR ÖVER
  katalograden helt (explicit dedup i generatorn, inget rått ID-undantag i `katalog.py`).
  `katalog.py`/`grind()` rörs INTE — katalograden fortsätter korrekt visa `energiform` som
  avslagsorsak.
- **Modell:** kall energi och returtemperatur blir synlig, obligatorisk indata för
  årsvägen — MED samma period-/upplösningskontrakt som det redan godkända
  `monthly_invoice`-kontraktet: kall energi samtliga tolv månader, returtemperatur bara
  november–mars (5 vintermånader). Bygg ett källverifierat årsreferensfall, motsvarande
  Sandvikens granskningskedja (`2026-09-06-004`→`2026-09-07-003`).
- **Avvikande regler:** rör INTE det redan godkända `monthly_invoice`-kontraktet.
- **Filer:** `resultatkontrakt.py`/`.ts` (ny anropspunkt), `policyregister.py` (utökad
  `_stockholm_exergi_policy` + nytt `ADAPTERREGISTER`), `generera.py` (läser registret,
  hoppar över katalogduplikatet).
- **Teststrategi:** eget källverifierat referensfall (inte bara Åkermannen-fixturens
  månadsdata återanvänd rakt av för ett annat ändamål), kontraktsfasadtest för
  `annual_forward` med period-/upplösningskontraktet, regressionstest att
  `monthly_invoice`-vägen är oförändrad, OCH ett nytt test att generatorn producerar EXAKT
  ETT UI-val för Stockholm Exergi (inte två) efter `ADAPTERREGISTER`-hoppet.
- **Visas för användaren:** mwh-läge med obligatoriska fält, under leverantörs-ID:t
  `stockholm-exergi`; kr och schablon BLOCKERADE (frusen status, samma som inventeringens
  rad och §2:s generella regel).

## Batch 8 — Vattenfall (12 tariffer, kontingent)

**Codex svar (granskning `2026-09-08-001`, öppen fråga 1, bekräftat i `2026-09-08-002`):**
hela gruppen förblir `blocked` tills flödesreferensen (3.3, `asymmetric_flow_difference`) är
löst. Bygg INGA osynliga delkomponenter (3.1/3.2/3.4) i förväg. Denna batch schemaläggs
alltså inte förrän ett leverantörssvar finns — tas inte med i implementationsordningen ovan.

## Ej batchade — `blocked_external_info` (26 bastariffer + 5 variantrader)

Väntar på leverantörssvar (26 bastariffer, inkl. Eskilstuna) eller ett formulerat
leverantörssvar/Robert-beslut (5 variantrader, rättat i v4 — Finspångs spetsvärmetillägg
tillagt: Södertörns överuttag, Kraftringens Brunnshög, Tekniska Verken Linköpings
lågtemperaturvariant, Jönköpings accessavgift — den sistnämnda väntar specifikt på ett
PRODUKTBESLUT från Robert, inte en källfråga — samt Finspångs spetsvärmetillägg, väntar på
en kartläggning av utlösande kunder/perioder) via processen i
[`todo-godkanna-fler-fjarrvarmetariffer.md` §7](todo-godkanna-fler-fjarrvarmetariffer.md).

## Sammanfattning

| Batch | Tariffer/varianter | Ny motorkod? | Risk |
|---|---:|---|---|
| 1 — Familj 4 + Telge + Partille | 6 | Nej (Sandviken-mönstret) | Låg |
| 2 — Sundsvall Indal | 1 | Nej (motorn `EJ_TILLAMPLIG_KAPACITETSFORM` finns; ny minimal `Tariffpolicy` krävs, rättat i v6) | Minst |
| 3 — E.ON/Navirum/Kraftringen | 9 | Ja (parametriserad flödeskorrigering, två regelvarianter) | Medel |
| 3b — E.ON/Navirum 36-mån (variant) | 8 | Nej (leverantörsvärde, ingen ny motorkod) | Låg |
| 4 — Jämtkraft/Umeå | 4 | Ja (två nya justeringstyper) | Medel |
| 5a — Leverantörsvärde, ingen justering | 8 | Nej | Låg |
| 5b — Leverantörsvärde, fullårsflöde | 6 | Nej (bara nytt fält) | Låg |
| 5c — Leverantörsvärde, säsongsflöde | 8 | Ja (`volume`+`months`-semantik) | Medel |
| 6 — Nya kapacitetsformer (2 bas + 1 variant) | 2 + 1 | Ja (två nya kapacitetsformer + två justeringstyper) | Högst |
| 7 — Stockholm Exergi årsprodukt | 1 | Nej (kontraktsbindning, ingen ny formel) | Låg–medel |
| 8 — Vattenfall | 12 | Kontingent, ej schemalagd | Ej schemalagd |
| **Summa batchade (1–7, 3b)** | **54** | | |
| Blockerade bastariffer (ej batchade) | 26 | | |
| Blockerade variantrader (ej batchade, inkl. Finspång) | 5 | | |
| Redan implementerade | 7 | | |
| **Totalt (bastariffer + varianter)** | **92** | | |

Stämmer mot inventeringens §8: 7 implementerade + 54 redo (batchade ovan) + 31 blockerade
(26 bas + 5 variant) = 92.
