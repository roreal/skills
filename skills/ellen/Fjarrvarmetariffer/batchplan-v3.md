# Batchplan v3.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-08 av Claude. Ersätter `batchplan-v2.md` i sin helhet (v2 ändras INTE i
efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-08-002](../conversations/reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v2.md).
Bygger på dispositionerna i [`tariffinventering-v3.md`](tariffinventering-v3.md) §4.1 (45
bastariffer) och §5 (10 `ready_to_implement`-varianter). Ingen batch är påbörjad — detta är
ett förslag till Codex granskning och Roberts prioritering.

**Vad som är nytt i v3** (se granskning `2026-09-08-002` för fullständig motivering):

1. Batch 5 delad i TRE undergrupper efter faktisk motorsemantik, inte v2:s enda felaktiga
   5a/5b-delning som blandade "ingen justering", "fullårsflöde" och "säsongsflöde" i samma
   grupp och angav fel säsongsmånader (v2 antog blankt oktober–april för alla tolv rader i
   5b — katalogens faktiska `months`-listor varierar från 5 till 9 månader per tariff).
2. Eskilstuna borttagen från batch 4 (flyttad till `blocked_external_info`,
   se inventeringens §4.2) — batch 4 krymper från fem till fyra tariffer.
3. Två nya delbatcher (3b, 6b) för de nu räknade E.ON/Navirum- och Finspång-varianterna
   (inventeringens §5), som tidigare stod helt utanför batchplanen.
4. Familj 4-resten ligger FÖRST (batch 1), exakt enligt överlämningens ordningsregel — v2:s
   motivering för att sätta Sundsvall Indal först ("ett medvetet, separat, oberoende beslut")
   var inte ett dokumenterat Robert-beslut och är borttagen.
5. Samtliga tariff-ID:n skrivna ut fullständigt, ingen förkortning.
6. Varje batch redovisar EXAKT samma obligatoriska indata som motsvarande rader i
   `tariffinventering-v3.md` §4 — inklusive de 16 raderna som fick ett tillagt flödes-/
   temperaturfält i v3.

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
- **Obligatorisk indata:** debiterbar effekt (kW) för alla sex; Telge dessutom
  normalårskorrigerad energi (MWh) och returtemperatur (°C); Södertörn och Partille dessutom
  returtemperaturavvikelse (°C).
- **Filer:** 6× katalograd, `policyregister.py` (6 nya policyer).
- **Teststrategi:** en `test_familj4_resten_kontrakt.py`, golden-värden mot respektive
  prislista, gränstest vid varje bands golv/tak, Telges tre fälts blockering testad separat.
- **Visas för användaren:** mwh-läge med tariffspecifika obligatoriska fält; kr/schablon
  blockerade.

## Batch 2 — Sundsvall Indal, Liden och Lucksta (1 tariff, minst risk)

- **Tariff:** `sundsvall-energi-indal-liden-och-lucksta-2026`.
- **Modell:** ren energitariff, `capacity: {"type": "not_applicable"}`. Ingen ny motorkod —
  mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp
  1–4 (2026-09-04), bara inte aktiverad mot en riktig katalograd.
- **Obligatorisk indata:** ingen utöver energimängd (MWh).
- **Filer:** katalog-JSON, `godkanda()`-testet i `test_katalog.py` (räknaren 7→8).
- **Teststrategi:** regressionstest att `grind()` godkänner raden, golden-värde mot
  100,8 öre/kWh, verifiera att en ren energitariff utan kapacitetsfält går på legacy-vägen
  utan kontraktskrav.
- **Visas för användaren:** mwh, kr och schablon — alla tre (ren energitariff utan
  kapacitetsdel, samma legacy-invers som redan godkända rena energitariffer; INGEN
  motsägelse mot den generella `ready`-regeln nedan, eftersom denna tariff aldrig blir
  kontraktsgated).

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
- **Modell:** NY motorkod: `supply_temperature_adjusted_flow` i `justeringar.py`/
  `adjustments.ts` — formeln `volym × base_rate × (0,02×(Tf−60)+0,2)` är känd (katalogens
  `correction_formula`-fält för E.ON/Navirum resp. Kraftringens `candidate_factor`), men
  inte kodad. `noggrannhet: snapshot` (aldrig `exact`) när effekten är ett enskilt
  leverantörsvärde — effekten är en rullande 12-månadersserie i källan.
- **Avvikande regler:** Malmö/Burlöv `-15→-8 °C` katalogrättelse. Endast fullvärmekunder i
  denna batch — E.ON/Navirums 36-månadersmetod byggs som EGNA variant-ID:n i batch 3b, INTE
  samtidigt. Kraftringens Brunnshög är en egen, blockerad variant
  (`kraftringen-kraftringen-2026--brunnshog`), inte del av denna batch.
- **Obligatorisk indata:** debiterbar effekt, medelframledningstemperatur `Tf` (°C), flöde
  (m³) — samtliga tre för samtliga nio tariffer. Kraftringens `Tf` är den
  FÖRBRUKNINGSVÄGDA månadsmedelframledningstemperaturen (fakturan/nätdata) — samma fält som
  E.ON/Navirums, inte ett separat krav.
- **Filer:** katalograder ×9, EN delad motorformel i `justeringar.py`/`adjustments.ts`,
  `policyregister.py` (parametriserad policyfunktion, likt `_stockholm_exergi_policy`).
- **Teststrategi:** golden-värde mot minst en orts publicerade räkneexempel, gränstest för
  flödesformelns temperaturberoende, `noggrannhet: snapshot`-regressionstest, kontraktsfasad-
  test i båda språk. `okand_justering`-regressionstest att `supply_temperature_adjusted_flow`
  nu är känd men fortfarande blockerar tariffer som saknar `Tf`/flöde.
- **Visas för användaren:** mwh-läge, tre obligatoriska fält; resultat märkt uppskattning
  (snapshot); kr/schablon blockerade.

## Batch 3b — E.ON/Navirums 36-månadersmetod (8 variantrader, EFTER batch 3)

- **Tariffer:** de åtta variant-ID:n i inventeringens §5
  (`<bas-id>--bas-delvarme`, en per E.ON/Navirum-bastariff i batch 3).
- **Modell:** egen formel för kunder med bas-/delvärmekälla i stället för fullvärme,
  källverifierad i verifieringslistan men inte kartlagd i detalj i teknisk-kartläggning v4
  (som bara behandlar fullvärme) — kräver en egen, mindre kartläggningsrunda innan kodning.
- **Obligatorisk indata:** debiterbar effekt, 36 månaders rullande medelvärde av
  framledningstemperatur (avtalet), flöde.
- **Filer:** 8× ny variant-`Tariffpolicy`, delad 36-månadersformel.
- **Teststrategi:** eget golden-värde för 36-månadersformeln, regressionstest att den inte
  påverkar fullvärme-batchens `snapshot`-resultat.
- **Visas för användaren:** mwh-läge, samma tre fält som batch 3 plus det rullande
  36-månadersvärdet; kr/schablon blockerade.

## Batch 4 — Egna flödesformler: Jämtkraft, Umeå (4 tariffer)

**Eskilstuna borttagen i v3** (flyttad till `blocked_external_info`, se inventeringens §4.2
— nätreferensen `monthly_mean_for_customers_covered_by_flow_tariff` är inte verifierad som
ett stabilt katalogvärde eller en fakturapost, till skillnad från Umeås statiska referens).

- **Tariffer:** `jamtkraft-ostersund-froson-as-2026`, `jamtkraft-brunflo-och-opevagen-2026`,
  `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
  (samtliga tre `flow_difference`), `umea-energi-umea-enkel-2026`
  (`asymmetric_flow_difference`, med statisk `reference_m3_per_MWh: 17` — TILL SKILLNAD från
  Vattenfalls dynamiska, blockerade variant av samma typnamn).
- **Modell:** TVÅ separata nya justeringstyper i `justeringar.py`/`adjustments.ts` —
  `flow_difference` (Jämtkraft, formel `3×(flöde_m3 − 19×energi_MWh)`, referensvärdet 19
  m³/MWh redan statiskt i katalogen) och `asymmetric_flow_difference` (Umeå, `bonus_rate: 3`,
  `fee_rate: 7`, `reference_m3_per_MWh: 17`, allt statiskt). Ingen väntar på leverantörsbesked.
- **Avvikande regler:** `okand_justering`-regression att `asymmetric_flow_difference` inte av
  misstag öppnar upp Vattenfalls BLOCKERADE variant av samma typnamn (Vattenfalls referens är
  `"network_average"`, dynamisk — Umeås är ett statiskt tal; koden får inte dela logik som
  antar det ena för det andra utan en explicit typkontroll).
- **Obligatorisk indata:** debiterbar effekt + flöde oktober–april (m³, samtliga fyra
  tariffer har `months: [1,2,3,4,10,11,12]`, 7 månader).
- **Filer:** katalograder ×4, två nya motorformler, `policyregister.py` ×4.
- **Teststrategi:** golden-värde per tariff, gränstest för respektive formels
  referensberoende, `okand_justering`-regression mot Vattenfalls/Sundsvall Matforss
  BLOCKERADE varianter av samma typnamn.
- **Visas för användaren:** mwh-läge, effekt + flöde; kr/schablon blockerade.

## Batch 5a — Leverantörsvärde, ingen ytterligare justeringspost (8 tariffer)

Effekt/band är leverantörens/fakturans enda obligatoriska värde. Katalogens
`adjustments: []` för samtliga åtta — verifierat direkt mot JSON, inte antaget.

- **Tariffer:** `c4-energi-kristianstad-2026`, `kils-energi-kil-2026`,
  `skovde-energi-skovde-2026`, `trollhattan-energi-trollhattan-2026`,
  `tekniska-verken-katrineholm-katrineholm-2026`,
  `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`,
  `soderhamn-nara-soderhamn-taxa-11-och-12-2026`,
  `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`.
- **Obligatorisk indata:** debiterbar effekt/band (fakturan) — automatisk gruppindelning
  BLOCKERAS för C4 (500 kW-gränsen).
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
  fakturan/avtalet) för samtliga sex.
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
  tabellen ovan anger, för respektive tariff.
- **Filer:** 8× katalograd, `months`-semantik i motorn (delad), `policyregister.py` (8 nya
  policyer).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5c_sasongsflode.py`/`.ts` med ETT
  testfall per tariffs `months`-lista (inte ett delat antagande), regressionstest att
  helårs-`volume`-legacytariffer är oförändrade.
- **Visas för användaren:** mwh-läge, effekt/band + säsongsflöde; kr/schablon blockerade.

## Batch 6 — Nya kapacitetsformer (2 tariffer, störst motorarbete)

- **Tariffer:** `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
  (`heterogeneous_bands`, Wn/Q-grupper — miljötillägget byggs som en kryssruta i SAMMA batch,
  se §5-varianten `--miljotillagg`), `finspangs-tekniska-verk-finspang-2026`
  (`piecewise_polynomial` PLUS `conditional_flow`, TVÅ separata nya motordelar).
- **Avvikande regler:** Borås — automatisk gruppindelning blockeras, leverantören/kunden
  anger grupp. Finspångs spetsvärmetillägg (20 %) är en egen variant
  (`finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg`) i delbatch 6b, EFTER
  grundformeln.
- **Obligatorisk indata:** Borås: prisgrupp + `Wn`/`Q` + valfritt miljötillägg (kundvalt
  UI-tillval, inget separat katalogfält). Finspång: `P`-värde, returtemperatur varje månad
  (avgör om `conditional_flow`s villkor >55 °C utlöses) OCH, när villkoret utlöses, månadens
  flöde i m³ (multipliceras med 20 kr/m³).
- **Filer:** ny kapacitetsformelkod + två nya justeringstyper i `justeringar.py`/
  `fjarrvarme.ts`, katalograder, policyer.
- **Teststrategi:** golden-värde per formel, gränstest vid gruppgränserna, regressionstest
  att kapacitetsformsutökningen inte påverkar `selected_band_affine`-tarifferna. Finspångs
  villkorade flöde testat både under och över 55 °C-tröskeln.
- **Visas för användaren:** mwh-läge, tariffspecifik obligatorisk indata; kr/schablon
  blockerade.

## Batch 6b — Finspångs spetsvärmetillägg (1 variantrad, EFTER batch 6)

- **Tariff:** `finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg`.
- **Modell:** 20-procentigt tillägg, känt procentvillkor men INTE kartlagt vilka
  kunder/perioder som utlöser det — kräver en kort kompletterande kartläggning innan kodning,
  inte bara en flagga på grundformeln.
- **Obligatorisk indata:** samma som batch 6:s Finspång-rad, plus bekräftelse av
  utlösningsvillkoret.
- **Teststrategi:** golden-värde med och utan tillägget aktivt.
- **Visas för användaren:** mwh-läge; kr/schablon blockerade.

## Batch 7 — Stockholm Exergis årsprodukt (1 produkt, egen kontraktsväg)

Skiljer sig från övriga batcher: `monthly_invoice`-kontraktet är redan implementerat och
fakturavaliderat — bara ÅRSVÄGEN saknar motsvarande bindning.

- **Tariff:** `stockholm-exergi-stockholm-exergi-normal-2026` (representerar samma produkt
  som leverantörsfilens `stockholm-exergi-2025`/`-2026`).
- **Modell:** bygg ett källverifierat årsreferensfall för `annual_forward`, motsvarande
  Sandvikens granskningskedja (`2026-09-06-004`→`2026-09-07-003`). Gör kall energi och
  returtemperatur till synlig, obligatorisk indata för årsvägen — MED samma period-/
  upplösningskontrakt som det redan godkända `monthly_invoice`-kontraktet: kall energi
  samtliga tolv månader, returtemperatur bara november–mars (5 vintermånader).
- **Avvikande regler:** rör INTE det redan godkända `monthly_invoice`-kontraktet.
- **Teststrategi:** eget källverifierat referensfall (inte bara Åkermannen-fixturens
  månadsdata återanvänd rakt av för ett annat ändamål), kontraktsfasadtest för
  `annual_forward` med period-/upplösningskontraktet, regressionstest att
  `monthly_invoice`-vägen är oförändrad.
- **Visas för användaren:** mwh-läge med obligatoriska fält; kr/schablon-status beror på om
  en verifierad invers/schablonmodell byggs samtidigt eller inte — avgörs vid
  implementation.

## Batch 8 — Vattenfall (12 tariffer, kontingent)

**Codex svar (granskning `2026-09-08-001`, öppen fråga 1, bekräftat i `2026-09-08-002`):**
hela gruppen förblir `blocked` tills flödesreferensen (3.3, `asymmetric_flow_difference`) är
löst. Bygg INGA osynliga delkomponenter (3.1/3.2/3.4) i förväg. Denna batch schemaläggs
alltså inte förrän ett leverantörssvar finns — tas inte med i implementationsordningen ovan.

## Ej batchade — `blocked_external_info` (26 bastariffer + 4 variantrader)

Väntar på leverantörssvar (26 bastariffer, inkl. Eskilstuna) eller ett formulerat
leverantörssvar/Robert-beslut (4 variantrader: Södertörns överuttag, Kraftringens
Brunnshög, Tekniska Verken Linköpings lågtemperaturvariant, Jönköpings accessavgift — den
sistnämnda väntar specifikt på ett PRODUKTBESLUT från Robert, inte en källfråga) via
processen i [`todo-godkanna-fler-fjarrvarmetariffer.md` §7](todo-godkanna-fler-fjarrvarmetariffer.md).

## Sammanfattning

| Batch | Tariffer/varianter | Ny motorkod? | Risk |
|---|---:|---|---|
| 1 — Familj 4 + Telge + Partille | 6 | Nej (Sandviken-mönstret) | Låg |
| 2 — Sundsvall Indal | 1 | Nej (aktivering av befintlig mekanism) | Minst |
| 3 — E.ON/Navirum/Kraftringen | 9 | Ja (delad flödeskorrigering) | Medel |
| 3b — E.ON/Navirum 36-mån | 8 | Nej (egen formel, delad grundmotor) | Medel (kräver egen kartläggning) |
| 4 — Jämtkraft/Umeå | 4 | Ja (två nya justeringstyper) | Medel |
| 5a — Leverantörsvärde, ingen justering | 8 | Nej | Låg |
| 5b — Leverantörsvärde, fullårsflöde | 6 | Nej (bara nytt fält) | Låg |
| 5c — Leverantörsvärde, säsongsflöde | 8 | Ja (`volume`+`months`-semantik) | Medel |
| 6 — Nya kapacitetsformer | 2 | Ja (två nya kapacitetsformer + två justeringstyper) | Högst |
| 6b — Finspångs spetsvärmetillägg | 1 | Nej | Låg (kräver kort kartläggning) |
| 7 — Stockholm Exergi årsprodukt | 1 | Nej (kontraktsbindning, ingen ny formel) | Låg–medel |
| 8 — Vattenfall | 12 | Kontingent, ej schemalagd | Ej schemalagd |
| **Summa batchade (1–7, 3b, 6b)** | **55** | | |
| Blockerade bastariffer (ej batchade) | 26 | | |
| Blockerade variantrader (ej batchade) | 4 | | |
| Redan implementerade | 7 | | |
| **Totalt (bastariffer + varianter)** | **92** | | |

Stämmer mot inventeringens §6: 7 implementerade + 55 redo (batchade ovan) + 30 blockerade
(26 bas + 4 variant) = 92.
