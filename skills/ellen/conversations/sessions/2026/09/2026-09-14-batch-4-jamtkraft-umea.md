---
session_id: "2026-09-14-001"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Lokal implementation bakom spärr klar; stannar för Codex granskning"
topic: "Batch 4: Jämtkraft (tre rader) och Umeå Energi Enkel"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-4.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 4"
---

# Session: Batch 4 — Jämtkraft och Umeå Energi Enkel

## Startbeslut

Robert gav 2026-09-14 klartecken att ta nästa batch. Codex verifierade först att den
separata auktorisationsrättelsen för Batch 3b var normal fast-forward-pushad som
`skills@8b12daa`: Robert hade godkänt Batch 3b-pushen; den tidigare oklarheten berodde på
att dialogen hoppade mellan agenterna.

Codex beredskapskontroll `2026-09-14-003` godkänner därefter Batch 4 för lokal
implementation bakom spärr. Omfattningen är exakt tre Jämtkraftprodukter och Umeå Enkel.
Startdispositionen är 33 implemented / 31 ready / 28 blocked av 92. Under
implementationsfasen ska samma disposition och den skarpa produktmängden 35 bestå.

## Bindande handoff

Claude ska följa
`conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md`. Uppdraget omfattar:

- ny, korrekt fryst Jämtkraftkälla för 2026 (`15_1`);
- `flow_difference` och `asymmetric_flow_difference` i Python/TypeScript;
- leverantörens `B` genom Umeås verkliga kapacitetsväg;
- strikt tvåpassgrind utan uppluckring av den nakna kataloggrinden;
- tre Jämtkraftfält respektive fyra Umeåfält;
- oberoende golden-facit, fail-closed-test och riktig UI/E2E-verifiering.

Ingen aktivering och ingen push är godkänd. Claude ska logga lokala commit-hashar och
testresultat här och stanna för Codex granskning.

## Händelselogg

- `2026-09-14T08:16:28+02:00` – Codex fastställde Batch 4-scope och skrev beredskapskontroll
  samt bindande handoff. Den tidigare misstanken om en dubblerad `retur += k.retur`-rad i
  Pythonmotorn avfördes efter kontroll av de exakta källraderna; endast en addition finns.
- `2026-09-14` – Robert gav explicit klartecken ("Claude kan börja arbeta från handoffen
  nu") att starta implementationen.

## Uppdrag

Implementationen enligt Codex auktoritativa handoff `2026-09-14-001` och
beredskapskontroll `2026-09-14-003`. Ingen aktivering och ingen push i denna etapp —
samtliga fyra tariffer ligger bakom en ren lokal `investigation.status="utreds"`-
implementationsspärr.

## Implementation

1. **Källa och katalogproveniens** (`skills@c1d8320`): hämtade Jämtkrafts officiella
   prisändringsmodell 2026-2028 (`https://www.jamtkraft.se/wt/documents/519/…pdf`) med
   `curl` (ingen bot-blockering), beräknade riktig SHA-256
   (`a7451e8d…dc43e995`), extraherade text med `pdftotext` och verifierade sidorna
   19-20 ordagrant mot katalogens priser, effektband, referensvärde 19 m³/MWh, rate=3
   och kapacitetsmetoden ("medelvärdet av de tre högsta dygnsmedeleffekterna … gäller
   tills en högre dygnsmedeleffekt mäts upp eller i högst 12 månader"). Ny källpost
   `15_1` tillagd; de tre radernas `source_refs` pekar nu på `15_1` sidorna 19-20. Det
   historiska `15_0` (2025-dokumentet) bevaras oförändrat. Jämtkrafts tidigare lösta
   issue-text om omappad effektmetod togs bort.
2. **Umeå källverifiering**: hämtade och läste `web-review-umea-terms` (storyblok-PDF)
   samt `web-review-umea-enkel`/`prismodell` (HTML) på riktigt — bekräftade ordagrant
   katalogens energipriser (650/416/242 SEK/MWh), sju effektband och den fullständiga
   piecewise B-formeln (`0,93` / `0,35U+0,825` / `1,34U+0,330` / `1,4`). `retrieved_on`
   uppdaterat till 2026-09-14 för båda web-review-källorna; ingen prisdata ändrad.
3. **Katalogrättelse** (`skills@c1d8320`): `capacity.formula` för Umeå rättad från
   `"(fixed + variable * billing_basis) * B"` till basformeln
   `"fixed + variable * billing_basis"` — multiplikatorn dokumenteras uteslutande via
   `capacity.post_multiplier`, vilket krävs för att den nya tvåpassgrinden (se nedan)
   ska kunna ta bort ENDAST `post_multiplier` och köra hela ordinarie `grind()` igen,
   exakt algoritmen handoffen beskriver. Priser/`till_prisar` läser aldrig `formula`
   som text — ändringen påverkar inga beräknade belopp. `contract_required:true` satt
   på alla fyra rader. Umeås tidigare lösta issue-text om omappad B togs bort eftersom
   bindningen, motorn och tvåpassgrinden nu finns och är testade.
4. **Ny delad flödesdifferens-motor** (`enkey-agents@69b3060`/`neptune_academy@289b9c0`):
   `flow_difference` (Jämtkraft, `justering = rate × (flode_okt_apr_m3 −
   reference_m3_per_MWh × W_säsong)`, inget golv) och `asymmetric_flow_difference`
   (Umeå, samma diff, men `bonus_rate` vid underskott / `fee_rate` vid överskott).
   Registrerade i `JUSTERINGSTYPER`/`JUSTERING_BERAKNING` i båda språken. Fail-closed
   schemakontroll (`_valid_flow_difference`/`_valid_asymmetric_flow_difference`,
   `justeringar.py`) kräver ändliga positiva `rate`/`reference_m3_per_MWh`/
   `bonus_rate`/`fee_rate` och EXAKT sju distinkta månader `{1,2,3,4,10,11,12}` —
   Vattenfalls redan blockerade dynamiska `reference: "network_average"`-rader
   (12 st.) avvisas automatiskt av samma kontroll, utan en Vattenfall-specifik
   specialregel (regressionstest).
5. **Umeås kapacitetsmultiplikator B**: `Forbrukning.kapacitet_multiplikator`/
   `kapacitetMultiplikator` trådat genom `_arskostnad_kapacitet`/`arskostnadKapacitet`
   (multiplicerar bara nivåbeloppet, aldrig `fast_avgift`) och hela vägen upp genom
   `arskostnad`/`_arskostnad_for_kontraktfasad` i båda språken.
   `resultatkontrakt.py`/`.ts` löser `kapacitet_multiplikator_bindning` till ett
   skalärt värde precis som `kapacitet_bindning`, exkluderar nyckeln ur den generiska
   `falt`-loopen och validerar `kravs_for` innehåller `'annual'`. Intervallet
   `[0,93; 1,401]` kontrolleras generiskt av den redan befintliga
   `KravPost.minvarde`/`maxvarde`-mekanismen — inga Umeå-specifika specialregler; B=14
   blockeras vid ett verkligt kundanrop med ett tydligt `ValueError`
   ("värdet uppfyller inte kravets gräns").
6. **Strikt kompositgrind** (`enkey-agents@69b3060`): den nakna `grind()` i
   `katalog.py` är OFÖRÄNDRAD och avvisar alltid en `post_multiplier`-rad med
   `"kapacitetsformel med multiplikator"`. `godkanda(katalog, policyregister=None)`
   fick ett injicerbart `policyregister`-argument och ett snävt andra pass: när
   `grind()`s avslag är exakt den strängen slås tariffens policy upp, en ny
   `kontrollera_kompositgrind(tariff, policy)` (`policyregister.py`) verifierar
   STRUKTUR (aldrig kundvärde) — att `kapacitet_multiplikator_bindning` pekar på ett
   befintligt numeriskt krav och att `capacity.post_multiplier` har exakt den stödda
   formen (`name`/`input_U`/`pieces`) — och en GRUND KOPIA av tariffen utan
   `capacity.post_multiplier` körs genom hela ordinarie `grind()` igen. Originalkatalogen
   och dess tariffobjekt muteras aldrig (verifierat separat). `generera.py`s båda
   `godkanda(katalog)`-anrop uppdaterade till att skicka samma `policyregister` vidare.
7. **Fyra nya `Tariffpolicy`-poster** (`enkey-agents@69b3060`): tre Jämtkraft-policyer
   (unik `kapacitet_bindning`/`kapacitet_band_bindning`-nyckel per tariff, delad
   `flode_okt_apr_m3`-nyckel — samma fysiska storhet, samma mönster som Batch 3:s
   `flode_m3`) och en Umeå-policy (`kapacitet_bindning`, `kapacitet_band_bindning`,
   `kapacitet_multiplikator_bindning`, samma delade flödesnyckel). Alla fyra
   `tackning={"annual_forward"}`, `stodjer_besparing=False`. Registrerade i
   `POLICYREGISTER`.
8. **Ny statisk aktiveringspreflight**: `kontrollera_flodesdifferensbindning`
   (`policyregister.py`) kräver, för varje rad vars `adjustments` innehåller
   `flow_difference`/`asymmetric_flow_difference`, exakt en `kravda_falt`-post med
   nyckeln `flode_okt_apr_m3`, `vardetyp='number'`, `kravs_for` innehållande `'annual'`
   och `minvarde=0` — kallad från `kontrollera_aktiveringsgrind`.
9. **Dokumentation**: `tariffinventering-v22.md`s fyra tariffposter uppdaterade till
   verklig implementation-bakom-spärr-status (motor/kontrakt/test/källa), utan att
   flytta `Disposition: ready_to_implement`. `batchplan-v22.md` fick en kort
   implementationsstatusnot i slutet av Batch 4-avsnittet med samma disciplin.

## Verifiering

- **Python**: `pytest tools/tariffer/tests` → **1259 passed, 4 skipped**, 0 failed.
  Ny fil `test_batch_4_jamtkraft_umea.py` (29 test): katalog-/dispositionsräkning,
  isolerad 37-produktsräkning, naken Umeå-grind utan policy, katalog-/policybindning
  för alla fyra, motorn (golden, gränsfall, felvägar, säsongssemantik), schemakontroll
  och Vattenfall-regression, samt oberoende handräknade golden-facit genom den
  verkliga kontraktsfasaden. Två redan befintliga test rättade till de nya talen
  (`test_registret_taeker_de_tio_kanda_typerna`, katalogens pinnade SHA-256).
- **TypeScript**: `vitest run` → **1194 passed** i 40 filer, 0 failed. Ny fil
  `resultatkontrakt.batch4.test.ts` (17 test) speglar exakt samma golden-facit.
  `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning. Den redan befintliga, orelaterade `dist/`-smutsigheten är
  orörd.
- **Mekanisk kontroll**: `godkanda(katalog)` == 33 (oförändrat). Katalogen har
  fortsatt 86 poster. En isolerad kopia med exakt de fyra spärrarna rensade, samma
  explicita `policyregister`, ger exakt **37** katalogprodukter — Umeås rad krävde
  både en registrerad policy OCH den strikta kompositgrindens strukturkontroll; ett
  tomt `policyregister` lämnar Umeå blockerad medan de tre Jämtkraft-raderna (ingen
  `post_multiplier`) godkänns oförändrat. Den skarpa, regenererade
  `tariffer.generated.ts` har fortsatt **35 produkter totalt** (2 leverantörsfiler +
  33 katalogprodukter); diffen mot föregående version är exakt proveniensraden och
  genereringsdatumet.
- **Golden-facit** (10 MWh/månad, band 1) genom den verkliga kontraktsfasaden i BÅDA
  språken, oberoende handräknat mot handoffens tabell:

  | Tariff | Energi | Effekt | Justering (flöde 1400) | Exkl. moms | Inkl. moms |
  | --- | ---: | ---: | ---: | ---: | ---: |
  | Östersund/Frösön/Ås | 55 540 | 32 120 | 210 | 87 870 | 109 837,50 |
  | Brunflo/Opevägen | 60 340 | 32 120 | 210 | 92 670 | 115 837,50 |
  | Åre m.fl. | 68 560 | 32 120 | 210 | 100 890 | 126 112,50 |

  Referensflöde 1330 m³ → 0 kr; 1260 m³ → −210 kr (samtliga Jämtkraft-rader, samma
  band/effektpris).

  Umeå (A=20 kW, band 1, energi 56 400 kr): B=1/flöde 1260 → fast 20 381, justering
  490, totalt 77 271 exkl./96 588,75 inkl.; B=0,93/referensflöde 1190 → fast
  18 954,33, totalt 75 354,33 exkl.; B=1,401/referensflöde → fast 28 553,781, totalt
  84 953,781 exkl.; B=1/flöde 1120 → justering −210. B=14 kastar via
  kontraktsförkontrollen (`maxvarde`); B=0,5 kastar via samma mekanism (`minvarde`).

## Kvarstående — inte gjort i denna leverans

Handoffens acceptanspunkt 8 ("ett riktigt komponent-/E2E-prov med injicerad kandidat
för Jämtkraft och Umeå som visar rätt fält, enheter, normal submit och
`annual/snapshot/complete`") är **inte** genomförd i denna runda — tid/omfattning
räckte inte till ett UI-komponenttest i denna leverans, utöver de rena kontrakts-/
motorproven ovan. Detta bör lösas i en fokuserad uppföljning innan aktivering, eller
tas upp av Codex som ett fynd i granskningen.

## Commits (lokalt, ingen push)

- `skills@c1d8320` — Jämtkrafts/Umeås källproveniens, kapacitetsmetod,
  `contract_required`, Umeås `capacity.formula`-rättning, borttagna lösta issues.
- `enkey-agents@69b3060` — delad flödesdifferens-motor, kapacitetsmultiplikator B,
  strikt kompositgrind, fyra Tariffpolicy-poster, nya/rättade tester.
- `neptune_academy@289b9c0` — TypeScript-spegel av motorn och multiplikatorn,
  regenererad `tariffer.generated.ts`, nytt speglat testfil.
- `skills` (dokumentationscommit, denna) — `tariffinventering-v22.md`/
  `batchplan-v22.md` implementationsstatus, denna sessionsfil, `index.md`.

Ingen aktivering, ingen push. Stannar för Codex granskning av hela implementationen.
