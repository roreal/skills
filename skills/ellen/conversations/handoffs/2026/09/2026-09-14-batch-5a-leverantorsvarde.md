---
handoff_id: "2026-09-14-002"
created_at: "2026-09-14T20:53:08+02:00"
from: Codex
to: Claude
status: ready-for-local-implementation
implementation_allowed: true
approved_implementation_scope: "batch-5a-eight-supplier-capacity-and-confirmed-band-tariffs"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
baseline_remote_heads:
  skills: "13b2a4ffc4520b7ebaca10eaa2efe0eb548259ff"
  enkey_agents: "5d498cfab3f968af42ba60751b5143c6f96536e0"
  neptune_academy: "ebe4d621ff800cab1f8248cd8e4e07ba042064fd"
tariff_disposition_before: "37 implemented / 27 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "37 implemented / 27 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "45 implemented / 19 ready / 28 blocked av 92"
relates_to:
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-5a.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5a"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §6a.2 och §7"
  - "Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md"
---

# Uppdrag till Claude: Batch 5a — åtta leverantörsvärdestariffer

## Mål och stoppunkt

Implementera lokalt exakt dessa åtta `annual_forward`-produkter bakom deras
befintliga `investigation.status="utreds"`-spärrar:

1. `c4-energi-kristianstad-2026`
2. `kils-energi-kil-2026`
3. `skovde-energi-skovde-2026`
4. `trollhattan-energi-trollhattan-2026`
5. `tekniska-verken-katrineholm-katrineholm-2026`
6. `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`
7. `soderhamn-nara-soderhamn-taxa-11-och-12-2026`
8. `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`

Kalkylen ska skapa en uppskattad årskostnad från tolv MWh-värden, leverantörens
debiterbara effekt/effektsignatur och leverantörens bekräftade band/taxa.
Resultatstatus ska vara `annual/snapshot/complete`, aldrig `exact`.

Detta är endast implementation bakom spärr. **Rensa inte spärrarna, regenerera
inte in kandidaterna i skarp payload och pusha inte.** Commitera fokuserat
lokalt i berörda repon, dokumentera hash/tester och stanna för Codex
kodgranskning.

## 1. Aktuella officiella källor och katalogproveniens

Verifiera källorna på riktigt och låt varje 2026-rad referera en aktuell
officiell källa som bär priset. Bevara historiska `_0`/2025-poster som historik,
men använd dem inte ensamma som bevis för 2026.

| Tariff | Aktuell officiell källa | Krav |
| --- | --- | --- |
| C4 | `https://www.c4energi.se/foretag/fjarrvarme/priser-och-villkor/` (redirect till katalogens nuvarande URL) | Uppdatera `web-review-c4-current.retrieved_on`; sidan anger 427/612, alla band och den fortsatt oklara 500 kW-gränsen. |
| Kil | `https://bolag.kil.se/download/18.1b9e2707199c916c9d91010c/1761112730710/Fj%C3%A4rrv%C3%A4rmeavgifter%202026%20normalprislista.pdf` | Uppdatera/frys den officiella PDF-posten med SHA-256 `d8bb87ca07f92ea90a7165d4453384be32ac84cc99e60c8a0a9705caf5bb6e32`; samma bytes som användarfilen. |
| Skövde | `https://skovdeenergi.se/fjarrvarme/priser-avgifter/taxa-fjarrvarme-2026-inklusive-moms/` | Lägg aktuell leverantörswebbkälla och referera den; bevara `35_0` historiskt. |
| Trollhättan | `https://www.trollhattanenergi.se/foretag/fjarrvarme/` | Uppdatera `web-review-trollhattan-final.retrieved_on` och använd den som 2026-priskälla. |
| Katrineholm | `https://tekniskaverken.se/foretag/fjarrvarme/priser` | Lägg aktuell leverantörswebbkälla/referens för 2026; bevara `40_0`, vars metadata i dag är missvisande. |
| Öresundskraft | `https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/` | Uppdatera `oresund-web.retrieved_on`; sidan anger målgruppen, `(A×C)+B`, fakturans A och energisäsongerna. |
| Söderhamn | `https://www.soderhamnnara.se/sidor/fjarrvarme/foretagskunder/priser-foretag.html` | Uppdatera `web-review-soderhamn-final.retrieved_on`; använd den som 2026-priskälla. |
| TEMAB | `https://temab.tierp.se/download/18.7fa3d20319a7bbd966d1fe/1763023016779/Taxa%20f%C3%B6r%20Fj%C3%A4rrv%C3%A4rmeleveranser%202026.pdf` | Frys `web-review-temab-final` med SHA-256 `c4a1ac3bc559bb3befcd4c5d3a45ef8331c5a1d3f69abda16924475dbcb1a5e8` och korrekta sidor 3–4. |

Rå-PDF:er ska inte committas. Använd riktig bytehash, riktig
`retrieved_on=2026-09-14` och beskrivande titlar/kind. Uppdatera
verifieringslistan och inventeringens levande kandidatrader så att de inte
fortsätter kalla en historisk 2025-post för ensam primärkälla.

## 2. Katalogrättelser bakom spärr

Sätt `contract_required:true` på samtliga åtta. Bevara
`production_ready:false` och varje `investigation.status="utreds"` under hela
denna etapp.

- **C4:** ersätt den okända 500 kW-issuen med den redan godkända inledningen
  `Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd
  leverantörens fakturavärde ...`. Bevara månadsperiodiseringsissuen. Ta bort
  R05 ur `remaining_information_requests`, eftersom produktkontraktet kräver
  leverantörens band och aldrig härleder gränsen.
- **Kil:** sätt `fixed:0` på alla fyra band. Ta bort den därmed inaktuella
  `null i fast avgift`-issuen. Normalisera effektmetodens issue till samma
  kända inledning och bevara månadsperiodiseringsissuen. Bevara
  `vat_basis="included"` och `vat_confirmation`; konvertera inte de
  publicerade beloppen en gång till.
- **TEMAB:** normalisera kategoritalsissuen till den kända inledningen och
  bevara `monthly_proration="days_in_month/365"`. Ta bort R12; kalkylatorn
  tar TEMAB:s debiteringseffekt/anslutningsvärde och räknar inte kategorital.
- **Söderhamn:** ta bort R13; kalkylatorn tar leverantörens anslutningseffekt
  och räknar inte byggnadsindexet.
- **Övriga fyra:** ändra inte pris, band, formel, momsgrund eller kvarvarande
  månadsperiodiseringsissue annat än verklig proveniens och
  `contract_required:true`.

Dokumentera R05/R12/R13-borttagningarna i katalogens `change_log`: frågorna
är inte externt besvarade, men de är inte längre produktblockerande när ett
obligatoriskt leverantörsvärde används. Påstå inte att den exakta C4-gränsen
har verifierats.

## 3. Exakt två policyfält per tariff

Bygg åtta separata `Tariffpolicy`-poster. Alla ska ha
`tackning=frozenset({"annual_forward"})`,
`stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False`, en numerisk
`kapacitet_bindning` och en `kapacitet_band_bindning` av typen `band_id`.
Nycklarna ska vara produktunika så att ett leverantörs-/produktbyte inte kan
återanvända värden tyst.

| Tariff | Numerisk nyckel / min | Bandnyckel | Synlig betydelse |
| --- | --- | --- | --- |
| C4 | `c4_debiterbar_effekt_kw` / 3 | `c4_vald_niva_id` | Högsta dygnsmedeleffekt senaste 12 månaderna + leverantörens grupp |
| Kil | `kil_debiterbar_effekt_kw` / 8 | `kil_vald_niva_id` | Avtalad/leverantörsberäknad effekt + leverantörens grupp |
| Skövde | `skovde_debiterbar_effekt_kw` / 5 | `skovde_vald_niva_id` | Leverantörens prisgrundande effekt + band 1 |
| Trollhättan | `trollhattan_debiterbar_effekt_kw` / 0 | `trollhattan_vald_niva_id` | Rullande högsta dygnsmedeleffekt + leverantörens grupp |
| Katrineholm | `katrineholm_effektsignatur_kw` / 5 | `katrineholm_vald_niva_id` | Leverantörens effektsignatur + leverantörens grupp |
| Öresund Totalvärme | `oresund_totalvarme_effekt_kw` / 0 | `oresund_totalvarme_vald_niva_id` | Fakturans A-värde + leverantörens grupp |
| Söderhamn | `soderhamn_anslutningseffekt_kw` / 0 | `soderhamn_vald_taxa_id` | Leverantörens anslutningseffekt + taxa 10/11/12/13 |
| TEMAB | `temab_debiteringseffekt_kw` / 0 | `temab_vald_taxa_id` | TEMAB:s debiteringseffekt/anslutningsvärde + taxa 1/2/3 |

De numeriska kraven är `supplier_value`, årsvisa och ändliga. Bandfälten ska
hämta sin allow-list från respektive skarp prispost; lägg inte en parallell
manuell lista i policyn. Etikett och hjälptext krävs på svenska och engelska
enligt nuvarande konstruktor, och ska säga att båda värdena läses på
faktura/avtal eller bekräftas av leverantören.

### Normativ bandsemantik

Alla åtta har redan
`capacity.band_selection="supplier_confirmed_band_id_required"`.
`kapacitet_band_bindning` ska därför använda den befintliga direkta
ID-uppslagningen. Lägg **inte** till en kontroll som kräver att numerisk effekt
ligger inom parserns tolkning av `source_interval`. C4 vid exakt 500 kW är
acceptansfallet som bevisar detta:

- utan band-ID: blocked;
- med okänt ID: fältnära `okant_val`/blocked;
- med ett av leverantören bekräftat känt ID: använd exakt det bandet, även om
  en automatisk intervalltolkning skulle ha valt det angränsande bandet.

## 4. Motor- och UI-scope

Ingen ny motorkod förväntas. Åtta katalograder använder redan
`selected_band_affine`, tolv energipriser, `adjustments:[]` och stödd
momsbehandling. Ändra inte `_niva()`, intervallparsern, momsformlerna eller
generella kostnadsformler för att få batchen att passera. Om ett verkligt
motorhinder upptäcks: stanna, logga ett reproducerbart fall och invänta ny
granskning i stället för att bredda scope.

UI:t ska genereras från policyfältmetadata: MWh-läge plus de två
tariffspecifika fälten. Kronor och schablon ska ge
`unsupported_input_mode`; besparing ska ge `besparing_ej_stodd`. Saknad,
icke-ändlig eller under-minimum effekt samt saknat/tomt/okänt band ska ge
fältnära `saknadeFalt`/`ogiltigaFalt` före motoranrop. Produktbyte i samma
sidladdning ska rensa både effekt och band, även mellan två Batch 5a-produkter.

## 5. Oberoende golden-facit

Använd gemensamt 10 MWh i var och en av årets tolv månader och 10 kW. Använd
band-ID enligt tabellen. Facit är handräknat från publicerade tal och får inte
genereras genom `till_prisar`, `arskostnad`, `calcResult` eller
`beraknaArsprodukt` i testets expected-gren.

| Tariff | Band | Energi i katalogens prisbas | Effekt/fast i samma prisbas | Summa exkl. moms | Summa inkl. moms |
| --- | --- | ---: | ---: | ---: | ---: |
| C4 | `2` | 60 490 | 13 260 | 73 750 | 92 187,50 |
| Kil (`vat_basis=included`) | `1` | 103 200 inkl. | 11 577,90 inkl. | 91 822,32 | 114 777,90 |
| Skövde | `1` | 44 576 | 12 840 | 57 416 | 71 770,00 |
| Trollhättan | `1` | 63 510 | 13 915 | 77 425 | 96 781,25 |
| Katrineholm | `1` | 73 080 | 11 905 | 84 985 | 106 231,25 |
| Öresund Totalvärme | `1` | 48 130 | 12 621,90 | 60 751,90 | 75 939,875 |
| Söderhamn | `10` | 92 040 | 8 001 | 100 041 | 125 051,25 |
| TEMAB | `1` | 99 840 | 6 557 | 106 397 | 132 996,25 |

Pinna i både Python och TypeScript minst energi, fast/kapacitet,
`summa_exkl` och `summa_inkl`. Testa dessutom varje bands båda ändar där
källan är entydig och bevis att valt band-ID — inte `_niva()` — styr satsen.

## 6. Test- och synkkrav före aktivering

1. Ny samlad Pythonfil
   `tools/tariffer/tests/test_leverantorsvarde_batch5a_kontrakt.py` med rå
   katalogstatus, policystruktur, alla band, golden/felmatris och
   requestlivscykel.
2. Motsvarande TypeScript-kontraktstest med samma oberoende facit. Om en
   fixture behövs ska den exporteras/maskinellt jämföras mot Pythons verkliga
   `till_prisar()`; skapa inte en oberoende "auktoritativ" kopia som kan drifta.
3. Riktat UI-komponentprov med den isolerade genererade kandidatposten:
   rätt två fält, fältnära fel, giltig submit och produktbytesrensning.
4. Aktiveringspreflight ska bevisa att alla åtta har korrekt bandbindning och
   policy. Ett saknat/feltypat bandkrav ska stoppa generering.
5. Katalogproveniens/SHA-test och generatorsynk ska uppdateras mekaniskt, inte
   försvagas eller tas bort.
6. Full Python- och TypeScript-svit samt `npx tsc --noEmit` ska vara gröna.
   Isolerat `npm run eval:build` körs om frontendlager/genererad fixture ändras.

## 7. Leveransgrind och stopp

Före återlämning ska följande vara mekaniskt visat:

- katalogen har 86 fysiska poster;
- alla åtta rader har `contract_required:true`, men fortfarande
  `production_ready:false` och `investigation.status="utreds"`;
- `godkanda(katalog, policyregister=POLICYREGISTER)` är fortsatt 37;
- skarp genererad payload är fortsatt 39 produkter och innehåller inget av de
  åtta ID:na;
- isolerad kopia med exakt åtta spärrar rensade ger 45 katalogprodukter och
  klarar samma generatorpreflight;
- dispositionen är fortsatt 37/27/28 under implementationen.

Commitera fokuserat lokalt i `skills`, `enkey-agents` och vid behov
`neptune_academy`. Logga exakta hashar och testantal i Batch 5a-sessionen.
**Ingen aktivering och ingen push. Stanna för Codex granskning.**

Efter godkänd implementation följer en separat lokal aktiveringsrunda för
exakt åtta rader. Dess mål är 45/19/28 och 47 skarpa produkter; den diffen
kräver ny Codex-granskning och därefter Roberts uttryckliga pushbesked.
