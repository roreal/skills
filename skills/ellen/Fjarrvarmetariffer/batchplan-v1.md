# Batchplan v1.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-08 av Claude, i svar på överlämning
[2026-09-08-001](../conversations/handoffs/2026/09/2026-09-08-tariffinventering-v1.md).
Bygger på dispositionerna i [`tariffinventering-v1.md`](tariffinventering-v1.md) §4 (43
produkter). Ingen batch är påbörjad — detta är ett förslag till Codex granskning och Roberts
prioritering, se [PROJECT_CHARTER §4](../PROJECT_CHARTER.md).

Ingen kund-/prospektprioritet är angiven ännu (tier 1 i produktdirektivets
prioriteringsprincip). Ordningen nedan följer i stället tier 3–4: minsta risk och mest
återanvändbar adapter först, med Familj 4-resten som Sandviken-mönstrets naturliga
fortsättning.

## Gemensamt för samtliga batcher (Sandviken-mallen)

Varje batch nedan som använder "leverantörsvärde-mönstret" ska följa exakt samma struktur
som Sandviken-etappen (granskningarna `2026-09-06-004` till `2026-09-07-003`), inte
återuppfinnas per batch:

1. Katalogändring: `contract_required: true` + `display_produktnamn` där tillämpligt, källor
   och `as_of`/ändringslogg uppdaterade.
2. `Tariffpolicy` i `policyregister.py`: `tackning: {"annual_forward"}`,
   `kapacitet_bindning` (eller motsvarande) med `minvarde`/`heltal` satt enligt tariffens
   egna nivåer/golv — INTE hårdkodat i motorn, i policyn (granskning `2026-09-07-001`, P1).
3. Generatorn (`generera.py`) kräver ingen ändring om policyplaceringen redan följer
   Stockholm Exergi/Sandviken-mönstret (prisårspostens `policy`-fält).
4. Produktsidan (`besparingsvarde.ts`/`energiPotential.ts`/`KalkylatorPage.tsx`): återanvänd
   `kontraktsgatadPolicy`, `KontraktBlockerat`, `energyProvenance: 'confirmed_mwh'` rakt av
   — bygg INGEN ny per-tariff-kopia av den logiken.
5. Kr- och schablonläge blockeras (`unsupported_input_mode`/`missing_energy`/
   `invalid_energy`), exakt som Sandviken, om inte tariffen uttryckligen saknar en
   obligatorisk indata (se batch 1, ren energitariff).
6. Tester: golden-värde mot leverantörens eget exempel/prislista, gränsvärden vid varje
   bandkant, kontraktsfasadtest (Python OCH TypeScript, samma gränser i båda — inte bara i
   produktadaptern, se granskning `2026-09-07-001` P1 #3), produktadaptertest, genererad
   diff-kontroll, momskontroll (`summaInkl`, aldrig `summaExkl`).
7. Tre fokuserade lokala commits (skills → enkey-agents → neptune_academy), Codex-granskning,
   rättningsrundor tills `approved-for-push`, push i den ordningen.

## Batch 1 — Sundsvall Indal/Liden/Lucksta (1 tariff, minst risk)

**Varför först:** ingen kapacitetsdel alls (ren energitariff), ingen ny obligatorisk
kundindata, inget nytt kr-/schablonblock behövs (inget effektberoende värde att gissa på).
Mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är redan byggd och testad mot en fixture sedan
etapp 1–4 (2026-09-04) — bara inte aktiverad mot en riktig katalograd.

- **Tariff:** `sundsvall-energi-indal-liden-och-lucksta-2026`.
- **Modell:** ren energitariff, `energi.type: monthly`, `capacity: {"type": "not_applicable"}`.
- **Avvikande regler:** inga.
- **Obligatorisk indata:** ingen utöver energimängd (MWh).
- **Filer:** katalog-JSON (sätt `capacity.type`, ta bort `investigation`), `godkanda()`-testet
  i `test_katalog.py` (räknaren 7→8).
- **Teststrategi:** regressionstest att `grind()` nu godkänner raden; golden-värde mot
  100,8 öre/kWh; INGET kontraktskrav behövs (ingen obligatorisk effekt) — kan gå på den
  befintliga legacy-vägen precis som de sex ursprungliga, om produktlagret tillåter en
  ren energitariff utan kapacitetsfält (verifiera det antagandet i implementationen).
- **Visas för användaren:** mwh-, kr- och schablonläge — alla tre, eftersom inget värde
  behöver gissas eller kontraktsgatas.

## Batch 2 — Familj 4-resten + Telge (5 tariffer)

**Varför näst:** exakt samma mönster som redan är byggt, testat och pushat för Sandviken.
Lägst implementationsrisk av de kontraktsgatade batcherna.

- **Tariffer:** `karlstads-energi-karlstad-2026`, `sodertorns-fjarrvarme-...-2026`,
  `vanerenergi-mariestad-och-toreboda-2026`, `ovik-energi-ornskoldsvik-2026`,
  `telge-nat-...-2026`.
- **Modell:** Sandviken-mönstret (§ ovan), en `Tariffpolicy` per tariff.
- **Avvikande regler:** Övik behöver katalogrättelse (`fixed`, `monthly_proration`) FÖRE
  aktivering. Telge behöver ett extra obligatoriskt fält (`normalarskorrigerad_energi_mwh`)
  utöver effekt. Södertörn: kundvald effekt (med överuttagsavgift) är uttryckligen
  `not_applicable` i denna batch — bara SFAB:s rekommenderade effekt aktiveras.
- **Obligatorisk indata:** debiterbar effekt (kW) för alla fem; Telge dessutom
  normalårskorrigerad energi.
- **Filer:** 5× katalograd, `policyregister.py` (5 nya policyer, kan samlas i en commit),
  generator/produktlager oförändrat (mönstret återanvänds).
- **Teststrategi:** en `test_<tariff>_kontrakt.py`-fil per tariff eller en samlad
  `test_familj4_resten_kontrakt.py`, golden-värden mot respektive prislista,
  gränstest vid varje bands golv/tak, Telges extra fälts blockering testad separat.
- **Visas för användaren:** mwh-läge, obligatorisk effekt (+ Telges extra fält); kr/schablon
  blockerade.

## Batch 3 — E.ON/Navirum rullande högutväxling (8 tariffer)

**Varför efter Familj 4:** ny, delad adapter (`supply_temperature_adjusted_flow`) som
samtliga åtta återanvänder — större motorarbete än batch 1–2 men bara en gång.

- **Tariffer:** de fyra E.ON/Navirum-paren i §4.2 i inventeringen (Järfälla, Malmö,
  Norrköping/Söderköping, Örebro/Kumla/Hallsberg — bostäder + övriga fastigheter vardera).
- **Modell:** ny formeltyp i katalogschemat (`correction_formula`) + motsvarande
  `kallenergi_bindning`/`returtemperatur_bindning`-liknande bindning i `Tariffpolicy` för
  flödeskorrigeringen (`Tf`, `flode_m3`), utöver kapacitetsbindningen (effekt).
  `noggrannhet: snapshot` (aldrig `exact`) med ett enskilt leverantörseffektvärde, per
  teknisk-kartläggning v4.
- **Avvikande regler:** Malmö/Burlöv `-15→-8 °C` katalogrättelse. Endast fullvärmekunder i
  denna batch — 36-månadersmetoden för bas-/delvärme är källverifierad men egen, mindre
  delbatch.
- **Obligatorisk indata:** debiterbar effekt, `Tf` (medelframledningstemperatur), `flode_m3`.
- **Filer:** katalograder ×8, ny motorformel i `faktura.py`/`fjarrvarme.ts` (delad, en
  implementation för alla åtta), `policyregister.py` (en policyfunktion parametriserad per
  ort, likt `_stockholm_exergi_policy`).
- **Teststrategi:** golden-värde mot minst en orts publicerade räkneexempel, gränstest för
  flödesformelns temperaturberoende, `noggrannhet: snapshot`-regressionstest (aldrig
  `exact`), kontraktsfasadtest i båda språk.
- **Visas för användaren:** mwh-läge, tre obligatoriska fält (effekt, `Tf`, flöde); resultat
  märkt uppskattning (snapshot), inte beräknat med `exact`-kvalitet; kr/schablon blockerade.

## Batch 4a — Leverantörsvärde, enkla fall utan effekt-nyans (7 tariffer)

Inget särskilt villkor utöver "använd leverantörens/fakturans effekt".

- **Tariffer:** `eskilstuna-...`, `falu-energi-vatten-falun-2026`,
  `falu-energi-vatten-bjursas-...-2026` (spärr >500 kW), `habo-energi-habo-2026`,
  `mjolby-svartadalen-energi-mjolby-2026`,
  `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`,
  `skovde-energi-skovde-2026`, `trollhattan-energi-trollhattan-2026`.
- **Modell:** Sandviken-mönstret, inget nytt motorarbete (redan stödd `selected_band_affine`
  + säsongsenergi).
- **Obligatorisk indata:** debiterbar effekt/band.
- **Teststrategi:** en samlad `test_leverantorsvarde_batch4a_kontrakt.py`/`.ts`, golden-värde
  per tariff, Falun ytterorters >500 kW-spärr testad explicit.
- **Visas för användaren:** mwh-läge, obligatorisk effekt; kr/schablon blockerade.

## Batch 4b — Leverantörsvärde med känd beräkningsmetod (9 tariffer)

Källan anger en specifik `billing_basis_method` (medelvärde av N högsta dygns-/
timmedeleffekter) som ska mappas i katalogen, inte bara "leverantörens värde" utan metod.

- **Tariffer:** `jamtkraft-ostersund-froson-as-2026`, `jamtkraft-brunflo-och-opevagen-2026`,
  `jamtkraft-are-...-2026`, `jonkoping-energi-jonkoping-och-granna-2026`,
  `nevel-gimo-osterbybruk-och-osthammar-2026`, `partille-energi-partille-2026`,
  `piteenergi-pitea-centrala-natet-2026`, `piteenergi-norrfjarden-och-sjulnas-2026`,
  `soderhamn-nara-soderhamn-taxa-11-och-12-2026`.
- **Avvikande regler:** Jönköpings accessavgift (0/10/25/50 kr/mån) hör INTE till kärntariffen
  — dokumentera som avsiktligt exkluderad, inte glömd.
- **Obligatorisk indata:** debiterbar effekt (leverantörens fastställda värde, metoden
  dokumenteras i katalogen men beräknas inte automatiskt av motorn i denna batch).
- **Teststrategi:** som 4a, plus ett test per tariff som verifierar att
  `billing_basis_method`-texten är korrekt mappad (inte bara att effekten går att mata in).
- **Visas för användaren:** som 4a.

## Batch 4c — Leverantörsvärde med särskilt villkor (10 tariffer)

Varje tariff har ett eget extra villkor utöver ren effektindata — grupperas ihop eftersom
vart och ett är litet men kräver egen uppmärksamhet i granskningen.

- **Tariffer och villkor:**
  - `kils-energi-kil-2026` — kategorital ELLER effektvärde, användaren väljer vilket den har.
  - `kraftringen-kraftringen-2026` — flödesformel `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)`;
    Brunnshög `not_applicable`.
  - `lulea-energi-lulea-2026` — leverantörens fakturavärde, ingen automatisk metod alls.
  - `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` — kategorital eller
    anslutningsvärde.
  - `tekniska-verken-katrineholm-katrineholm-2026`,
    `tekniska-verken-linkoping-linkoping-2026` — effektsignatur/-grupp; Linköpings
    lågtemperaturvärme `not_applicable`.
  - `umea-energi-umea-enkel-2026` — leverantörens A- och B/U-värden (tre obligatoriska fält).
  - `oresundskraft-helsingborg-normal-2026`,
    `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`,
    `oresundskraft-angelholm-normal-2026` — fakturans effektvärde.
- **Teststrategi:** eget test per tariff (inte en samlad fil, eftersom villkoren skiljer sig
  åt) plus samma gränsvärdes-/momskontroller som övriga batcher.
- **Visas för användaren:** mwh-läge med tariffens specifika obligatoriska fält; kr/schablon
  blockerade.

## Batch 5 — Nya kapacitetsformer, Del B (2 tariffer, störst motorarbete)

- **Tariffer:** `boras-energi-och-miljo-...-2026` (`heterogeneous_bands`, Wn/Q-grupper),
  `finspangs-tekniska-verk-finspang-2026` (`piecewise_polynomial`).
- **Modell:** två NYA kapacitetsformer i motorn (`FAS1_KAPACITETSFORM` utökas eller en
  parallell typ läggs till) — större ändring än övriga batcher, motiverar egen granskning.
- **Avvikande regler:** Borås — automatisk gruppindelning vid exakta MWh-gränser blockeras,
  leverantören/kunden anger grupp. Finspång — spetsvärmetillägget (20 %) `not_applicable` i
  denna batch, bara ordinarie fullvärmeleverans.
- **Obligatorisk indata:** Borås: prisgrupp + `Wn`/`Q`. Finspång: `P`.
- **Filer:** ny kapacitetsformelkod i `faktura.py`/`fjarrvarme.ts`, katalograder, policyer.
- **Teststrategi:** golden-värde per formel, gränstest vid gruppgränserna (dokumenterat som
  "leverantören väljer" snarare än motorns egen gissning), regressionstest att
  `FAS1_KAPACITETSFORM`-utökningen inte påverkar `selected_band_affine`-tarifferna.
- **Visas för användaren:** mwh-läge, tariffspecifik obligatorisk indata; kr/schablon
  blockerade.

## Batch 6 — Vattenfall, villkorad (12 tariffer, kontingent på öppen fråga 1)

**Inte redo att schemaläggas förrän Codex/Robert svarat på öppen fråga 1 i
[inventeringen §8](tariffinventering-v1.md).** Två alternativ:

- **6a (hel grupp, väntar):** hela gruppen förblir `blocked` tills 3.3
  (`asymmetric_flow_difference`) är löst — ingen implementation påbörjas förrän ett
  leverantörssvar finns.
- **6b (delad, om beslutad):** bygg och testa 3.1 (produktval Standard/Spetsig), 3.2
  (säsongsbunden volymrabatt) och 3.4 (`capacity_overrun`-spärr) internt nu, men aktivera
  INGEN av de tolv tarifferna i kalkylatorn förrän 3.3 också är löst — exakt som
  teknisk-kartläggning v4 föreslår som möjligt. Kräver ett explicit Robert-beslut att göra
  det interna arbetet i förväg, eftersom det inte ger ett synligt resultat än.

Tas inte med i batch 1–5:s implementationsordning förrän det beslutet är fattat.

## Ej batchade — `blocked_external_info` (27 produkter)

Väntar på leverantörssvar via processen i
[`todo-godkanna-fler-fjarrvarmetariffer.md` §7](todo-godkanna-fler-fjarrvarmetariffer.md).
Ingen implementation påbörjas för dessa förrän Robert sparat ett verifierat svar och Codex
uppdaterat statusen.

## Sammanfattning

| Batch | Tariffer | Ny motorkod? | Risk |
|---|---:|---|---|
| 1 | 1 | Nej (aktivering av befintlig mekanism) | Minst |
| 2 | 5 | Nej (Sandviken-mönstret) | Låg |
| 3 | 8 | Ja (delad flödesformel) | Medel |
| 4a | 7 | Nej | Låg |
| 4b | 9 | Nej | Låg |
| 4c | 10 | Nej (men fler särfall att granska) | Låg–medel |
| 5 | 2 | Ja (två nya kapacitetsformer) | Högst |
| 6 | 12 | Kontingent på öppen fråga 1 | Ej schemalagd |
| **Summa batchade** | **43** | | |
| Blockerade (ej batchade) | 27 | | |
| Redan implementerade | 8 | | |
| Ej tillämpliga | 2 | | |
| **Totalt** | **80** | | |
