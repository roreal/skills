# Batchplan v2.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-08 av Claude. Ersätter `batchplan-v1.md` i sin helhet, som svar på Codex
kodgranskning [2026-09-08-001](../conversations/reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md).
Bygger på dispositionerna i [`tariffinventering-v2.md`](tariffinventering-v2.md) §4.1 (46
produkter). Ingen batch är påbörjad — detta är ett förslag till Codex granskning och Roberts
prioritering.

**Vad som är nytt i v2:** ordningen följer nu överlämningens regel rakt av (återstående
Familj 4 FÖRE Sundsvalls rena energitariff hade varit fel — men Sundsvall Indal har noll
kund-/prospektprioritet och noll ny motorkod, så det placeras ändå FÖRST som ett medvetet,
separat, oberoende beslut: ren aktivering av en redan byggd mekanism är inte
"Familj 4-arbete" och konkurrerar inte om samma granskningskapacitet). Kraftringen är
flyttad till samma batch som E.ON/Navirum (samma ej implementerade motortyp,
`supply_temperature_adjusted_flow` — v1 satte den fel i "inget nytt motorarbete"-gruppen).
Alla tariff-ID:n skrivs ut fullständigt, ingen förkortning.

## Gemensamt för samtliga batcher (Sandviken-mallen)

Oförändrat från v1 — se granskningarna `2026-09-06-004` till `2026-09-07-003` för den fullt
utarbetade mallen (katalogändring → `Tariffpolicy` med `minvarde`/`heltal` → produktsidans
`kontraktsgatadPolicy`/`KontraktBlockerat`/`energyProvenance` återanvänd rakt av → kr/schablon
blockerade → golden-/gräns-/kontraktsfasad-/produktadapter-/diff-/momstest i båda språk →
tre fokuserade lokala commits, Codex-granskning, push i ordningen skills → enkey-agents →
neptune_academy).

## Batch 1 — Sundsvall Indal, Liden och Lucksta (1 tariff, minst risk)

- **Tariff:** `sundsvall-energi-indal-liden-och-lucksta-2026`.
- **Modell:** ren energitariff, `capacity: {"type": "not_applicable"}`. Ingen ny motorkod —
  mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp
  1–4 (2026-09-04), bara inte aktiverad mot en riktig katalograd.
- **Obligatorisk indata:** ingen utöver energimängd (MWh).
- **Filer:** katalog-JSON, `godkanda()`-testet i `test_katalog.py` (räknaren 7→8).
- **Teststrategi:** regressionstest att `grind()` godkänner raden, golden-värde mot
  100,8 öre/kWh, verifiera att en ren energitariff utan kapacitetsfält går på legacy-vägen
  utan kontraktskrav.
- **Visas för användaren:** mwh, kr och schablon — alla tre.

## Batch 2 — Familj 4-resten + Telge (5 tariffer)

- **Tariffer:** `karlstads-energi-karlstad-2026`,
  `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`,
  `vanerenergi-mariestad-och-toreboda-2026`, `ovik-energi-ornskoldsvik-2026`,
  `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`.
- **Modell:** Sandviken-mönstret. Ingen ny motorkod — samtliga fält (effekt,
  `temperature_difference`, `low_utilization`, `incremental_return_temperature`) finns
  redan i `JUSTERINGSTYPER`.
- **Avvikande regler:** Övik behöver katalogrättelse (`fixed`, `monthly_proration`) FÖRE
  aktivering. Telge behöver TRE obligatoriska fält (effekt, normalårskorrigerad energi,
  returtemperatur), inte ett. Södertörn: bara SFAB:s rekommenderade effekt + returtemp-
  avvikelse aktiveras — kundvald effekt med överuttagsavgift är specialvariant 2 i
  inventeringens §5, egen framtida batch.
- **Obligatorisk indata:** debiterbar effekt (kW) för alla fem; Telge dessutom
  normalårskorrigerad energi (MWh) och returtemperatur (°C); Södertörn dessutom
  returtemperaturavvikelse (°C).
- **Filer:** 5× katalograd, `policyregister.py` (5 nya policyer).
- **Teststrategi:** en `test_familj4_resten_kontrakt.py`, golden-värden mot respektive
  prislista, gränstest vid varje bands golv/tak, Telges tre fälts blockering testad separat.
- **Visas för användaren:** mwh-läge med tariffspecifika obligatoriska fält; kr/schablon
  blockerade.

## Batch 3 — Delad flödeskorrigeringsmotor: E.ON, Navirum, Kraftringen (9 tariffer)

**Rättat i v2:** Kraftringen använder SAMMA ej implementerade justeringstyp
(`supply_temperature_adjusted_flow`) som de åtta E.ON/Navirum-tarifferna och hör därför i
samma batch — v1 satte den felaktigt bland tarifferna utan nytt motorarbete.

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
  denna batch — E.ON/Navirums 36-månadersmetod är specialvariant 1 i §5, egen delbatch.
  Kraftringens Brunnshög är specialvariant 3, blockerad tills källunderlag finns.
- **Obligatorisk indata:** debiterbar effekt, medelframledningstemperatur `Tf` (°C), flöde
  (m³) — samtliga tre för samtliga nio tariffer.
- **Filer:** katalograder ×9, EN delad motorformel i `justeringar.py`/`adjustments.ts`,
  `policyregister.py` (parametriserad policyfunktion, likt `_stockholm_exergi_policy`).
- **Teststrategi:** golden-värde mot minst en orts publicerade räkneexempel, gränstest för
  flödesformelns temperaturberoende, `noggrannhet: snapshot`-regressionstest, kontraktsfasad-
  test i båda språk. `okand_justering`-regressionstest att `supply_temperature_adjusted_flow`
  nu är känd men fortfarande blockerar tariffer som saknar `Tf`/flöde.
- **Visas för användaren:** mwh-läge, tre obligatoriska fält; resultat märkt uppskattning
  (snapshot); kr/schablon blockerade.

## Batch 4 — Egna flödesformler: Eskilstuna, Jämtkraft, Umeå (5 tariffer)

**Nytt i v2** (v1 saknade denna batch helt — dessa fem klassades felaktigt som "inget nytt
motorarbete" i leverantörsvärde-gruppen).

- **Tariffer:** `eskilstuna-energi-och-miljo-eskilstuna-2026` (`network_flow_difference`),
  `jamtkraft-ostersund-froson-as-2026`, `jamtkraft-brunflo-och-opevagen-2026`,
  `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
  (samtliga tre `flow_difference`), `umea-energi-umea-enkel-2026`
  (`asymmetric_flow_difference`, med statisk `reference_m3_per_MWh` — TILL SKILLNAD från
  Vattenfalls dynamiska, blockerade variant av samma typnamn).
- **Modell:** TRE separata nya justeringstyper i `justeringar.py`/`adjustments.ts` —
  `network_flow_difference`, `flow_difference`, `asymmetric_flow_difference`. Alla tre har
  kompletta, statiska formler i katalogens `adjustments`-poster redan i dag; ingen väntar på
  ett leverantörsbesked.
- **Avvikande regler:** Eskilstunas referens
  (`monthly_mean_for_customers_covered_by_flow_tariff`) måste verifieras som ett stabilt
  katalogvärde eller en uttryckligen redovisad fakturapost innan aktivering — annars ska
  raden flyttas till `blocked_external_info` i stället.
- **Obligatorisk indata:** debiterbar effekt + flöde (m³, okt–apr) för samtliga fem.
- **Filer:** katalograder ×5, tre nya motorformler, `policyregister.py` ×5.
- **Teststrategi:** golden-värde per tariff, gränstest för respektive formels
  temperatur-/referensberoende, `okand_justering`-regression att de tre nya typerna inte av
  misstag öppnar upp Vattenfalls eller Sundsvall Matforss BLOCKERADE varianter av samma
  typnamn (särskilt `asymmetric_flow_difference` — dela INTE kod som antar en statisk
  referens med Vattenfalls dynamiska variant utan en explicit typkontroll).
- **Visas för användaren:** mwh-läge, effekt + flöde; kr/schablon blockerade.

## Batch 5a — Leverantörsvärde, enkla fall (11 tariffer)

Inget nytt motorarbete. Effekt/band är leverantörens/fakturans värde, ingen ytterligare
justeringspost.

- **Tariffer:** `borlange-energi-borlange-2026` (effektgrupp, automatisk gruppindelning vid
  501 kW blockerad), `c4-energi-kristianstad-2026` (effektgrupp, 500 kW blockerad),
  `falu-energi-vatten-falun-2026`, `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
  (spärr: endast 0–500 kW), `habo-energi-habo-2026`,
  `mjolby-svartadalen-energi-mjolby-2026`,
  `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` (ingen kapacitetsdel — fast
  årsavgift, energi, säsongsflöde i m³ okt–apr; `volume`-justeringens `months`-hänsyn måste
  verifieras innan aktivering, se batch 5b:s anmärkning),
  `skovde-energi-skovde-2026`, `trollhattan-energi-trollhattan-2026`,
  `kils-energi-kil-2026` (kategorital ELLER effektvärde, kunden väljer),
  `tekniska-verken-katrineholm-katrineholm-2026`.
- **Obligatorisk indata:** debiterbar effekt/band (Mälarenergi 2–4 lgh: fast avgift +
  energi + säsongsflöde i stället för effekt).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5a_kontrakt.py`/`.ts`, golden-värde
  per tariff, Falu ytterorters >500 kW-spärr testad explicit, Mälarenergi 2–4 lgh:s
  `volume`+`months`-semantik testad separat (se anmärkning i batch 5b).
- **Visas för användaren:** mwh-läge, obligatorisk indata; kr/schablon blockerade.

## Batch 5b — Leverantörsvärde med säsongsflöde eller känd metod (12 tariffer)

**Rättat i v2:** `volume`-justeringen i dagens motor använder ETT årsflöde och beaktar inte
postens `months` (Codex granskning `2026-09-08-001`, P1). Samtliga tariffer nedan har
säsongsbegränsad flödesavgift (okt–apr, 7 månader) i katalogen. Ett årsflöde får INTE
appliceras på fel månader — kräver verifierad säsongsindata och motorsemantik i
`faktura.py`/`fjarrvarme.ts` INNAN aktivering, inte bara ett synligt flödesfält som v1 antog.

- **Tariffer:** `lulea-energi-lulea-2026`, `nevel-gimo-osterbybruk-och-osthammar-2026`,
  `oresundskraft-helsingborg-normal-2026`,
  `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`,
  `oresundskraft-angelholm-normal-2026`, `piteenergi-pitea-centrala-natet-2026`,
  `piteenergi-norrfjarden-och-sjulnas-2026`, `tekniska-verken-linkoping-linkoping-2026`
  (lågtemperaturvariant = specialvariant 4, blockerad separat),
  `jonkoping-energi-jonkoping-och-granna-2026` (accessavgift = specialvariant 6, blockerad
  separat), `partille-energi-partille-2026` (returtemperaturavvikelse, redan stödd typ —
  inget `volume`/`months`-arbete för denna, med i batchen av gruppindelningsskäl),
  `soderhamn-nara-soderhamn-taxa-11-och-12-2026`, `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`.
- **Motorarbete:** verifiera/bygg `months`-hänsyn för `volume`-justeringen (påverkar ALLA
  volume-tariffer i katalogen, inte bara denna batch — regressionstesta mot de redan
  implementerade legacy-tarifferna med `volume`, t.ex. Mölndal).
- **Obligatorisk indata:** debiterbar effekt + säsongsflöde (m³, okt–apr) för
  flödestarifferna; Partille effekt + returtemperaturavvikelse (inget flöde).
- **Teststrategi:** som 5a, plus ett regressionstest att `months`-hänsynen inte ändrar
  redan pushade legacy-tariffers resultat.
- **Visas för användaren:** som 5a.

## Batch 6 — Nya kapacitetsformer (2 tariffer, störst motorarbete)

- **Tariffer:** `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
  (`heterogeneous_bands`, Wn/Q-grupper, PLUS `optional_environmental_addon` som ett synligt
  kundval — v1 nämnde bara kapacitetsformen), `finspangs-tekniska-verk-finspang-2026`
  (`piecewise_polynomial` PLUS `conditional_flow`, TVÅ separata nya motordelar — v1 nämnde
  bara kapacitetsformen).
- **Avvikande regler:** Borås — automatisk gruppindelning blockeras, leverantören/kunden
  anger grupp; miljötillägget byggs som en kryssruta i samma batch (se öppen fråga 2 i
  inventeringens §8). Finspång — spetsvärmetillägget är specialvariant 5, egen delbatch
  efter grundformeln.
- **Obligatorisk indata:** Borås: prisgrupp + `Wn`/`Q` + valfritt miljötillägg. Finspång:
  `P`-värde + returtemperatur (för `conditional_flow`s villkor).
- **Filer:** ny kapacitetsformelkod + två nya justeringstyper i `justeringar.py`/
  `fjarrvarme.ts`, katalograder, policyer.
- **Teststrategi:** golden-värde per formel, gränstest vid gruppgränserna, regressionstest
  att kapacitetsformsutökningen inte påverkar `selected_band_affine`-tarifferna.
- **Visas för användaren:** mwh-läge, tariffspecifik obligatorisk indata; kr/schablon
  blockerade.

## Batch 7 — Stockholm Exergis årsprodukt (1 produkt, egen kontraktsväg)

**Nytt i v2** (rättat disposition, se inventeringens §4.1). Skiljer sig från övriga batcher:
`monthly_invoice`-kontraktet är redan implementerat och fakturavaliderat — bara ÅRSVÄGEN
saknar motsvarande bindning.

- **Tariff:** `stockholm-exergi-stockholm-exergi-normal-2026` (representerar samma produkt
  som leverantörsfilens `stockholm-exergi-2025`/`-2026`).
- **Modell:** bygg ett källverifierat årsreferensfall för `annual_forward`, motsvarande
  Sandvikens granskningskedja (`2026-09-06-004`→`2026-09-07-003`). Gör kall energi och
  returtemperatur till synlig, obligatorisk indata för årsvägen.
- **Avvikande regler:** rör INTE det redan godkända `monthly_invoice`-kontraktet.
- **Teststrategi:** eget källverifierat referensfall (inte bara Åkermannen-fixturens
  månadsdata återanvänd rakt av för ett annat ändamål), kontraktsfasadtest för
  `annual_forward`, regressionstest att `monthly_invoice`-vägen är oförändrad.
- **Visas för användaren:** mwh-läge med obligatoriska fält; kr/schablon-status beror på om
  en verifierad invers/schablonmodell byggs samtidigt eller inte — avgörs vid
  implementation.

## Batch 8 — Vattenfall (12 tariffer, kontingent)

**Codex svar (granskning `2026-09-08-001`, öppen fråga 1):** hela gruppen förblir `blocked`
tills flödesreferensen (3.3, `asymmetric_flow_difference`) är löst. Bygg INGA osynliga
delkomponenter (3.1/3.2/3.4) i förväg. Denna batch schemaläggs alltså inte förrän ett
leverantörssvar finns — tas inte med i implementationsordningen ovan.

## Ej batchade — `blocked_external_info` (25 produkter)

Väntar på leverantörssvar via processen i
[`todo-godkanna-fler-fjarrvarmetariffer.md` §7](todo-godkanna-fler-fjarrvarmetariffer.md).

## Ej batchade — kända specialvarianter (7, se inventeringens §5)

Fyra väntar på en formulerad leverantörsfråga eller ett Robert-beslut (Södertörns
överuttag, Kraftringens Brunnshög, Tekniska Verken Linköpings lågtemperaturvariant,
Jönköpings accessavgift). Tre är `ready_to_implement` som egna, mindre delbatcher EFTER
respektive grundformel (E.ON/Navirums 36-månadersmetod, Finspångs spetsvärmetillägg,
Borås miljötillägg — det sistnämnda byggs redan i batch 6, se ovan).

## Sammanfattning

| Batch | Tariffer | Ny motorkod? | Risk |
|---|---:|---|---|
| 1 — Sundsvall Indal | 1 | Nej (aktivering av befintlig mekanism) | Minst |
| 2 — Familj 4 + Telge | 5 | Nej (Sandviken-mönstret) | Låg |
| 3 — E.ON/Navirum/Kraftringen | 9 | Ja (delad flödeskorrigering) | Medel |
| 4 — Eskilstuna/Jämtkraft/Umeå | 5 | Ja (tre nya justeringstyper) | Medel |
| 5a — Leverantörsvärde, enkla | 11 | Nej | Låg |
| 5b — Leverantörsvärde, säsongsflöde | 12 | Ja (`volume`+`months`-semantik) | Låg–medel |
| 6 — Nya kapacitetsformer | 2 | Ja (två nya kapacitetsformer + två justeringstyper) | Högst |
| 7 — Stockholm Exergi årsprodukt | 1 | Nej (kontraktsbindning, ingen ny formel) | Låg–medel |
| 8 — Vattenfall | 12 | Kontingent, ej schemalagd | Ej schemalagd |
| **Summa batchade (1–7)** | **46** | | |
| Blockerade (ej batchade) | 25 | | |
| Redan implementerade | 7 | | |
| **Totalt (tariffprodukter)** | **78** | | |

Specialvarianterna (7) är inte inräknade i totalen — de tillkommer när de bryts ut som egna
poster i en framtida inventeringsversion (se inventeringens §5).
