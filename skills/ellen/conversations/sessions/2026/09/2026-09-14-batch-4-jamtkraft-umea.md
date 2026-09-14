---
session_id: "2026-09-14-001"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Slutgodkänd enligt Codex 2026-09-14-008 för separat lokal aktivering av exakt fyra Batch 4-tariffer till 37/27/28; push ej tillåten"
topic: "Batch 4: Jämtkraft (tre rader) och Umeå Energi Enkel"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-4.md"
  - "conversations/reviews/2026/09/2026-09-14-granskning-batch-4-implementation.md"
  - "conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-1.md"
  - "conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-2.md"
  - "conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-3.md"
  - "conversations/reviews/2026/09/2026-09-14-slutgranskning-batch-4-fixrunda-4.md"
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
- `2026-09-14` – Codex granskade leveransen vid `skills@e8341ce` (katalog
  `skills@c1d8320`), `enkey-agents@69b3060` och `neptune_academy@289b9c0`. Beslut:
  **changes required före aktivering** enligt granskning `2026-09-14-004`. Reproducerade
  blockerare är en odubbelriktad multiplikatorbindning som kan multiplicera en
  Jämtkraftkostnad, en kompositgrind som accepterar godtycklig multiplikatorstruktur,
  flödesvalidatorer som ignorerar enhet/formel samt det saknade verkliga UI-/E2E-provet.
  Fullsviterna är gröna (1259+4 skip Python, 1194 TypeScript, tsc och isolerat bygge), men
  spärrarna och 33/31/28 ligger kvar; ingen aktivering eller push är godkänd.

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
`annual/snapshot/complete`") var **inte** genomförd i denna runda — tid/omfattning
räckte inte till ett UI-komponenttest i denna leverans, utöver de rena kontrakts-/
motorproven ovan. Codex tog upp detta som P1 #4 i granskning 2026-09-14-004; stängt
i rättningsrunda 1 nedan.

## Commits (lokalt, ingen push)

- `skills@c1d8320` — Jämtkrafts/Umeås källproveniens, kapacitetsmetod,
  `contract_required`, Umeås `capacity.formula`-rättning, borttagna lösta issues.
- `enkey-agents@69b3060` — delad flödesdifferens-motor, kapacitetsmultiplikator B,
  strikt kompositgrind, fyra Tariffpolicy-poster, nya/rättade tester.
- `neptune_academy@289b9c0` — TypeScript-spegel av motorn och multiplikatorn,
  regenererad `tariffer.generated.ts`, nytt speglat testfil.
- `skills` (dokumentationscommit) — `tariffinventering-v22.md`/
  `batchplan-v22.md` implementationsstatus, denna sessionsfil, `index.md`.

Ingen aktivering, ingen push. Stannade för Codex granskning av hela implementationen
— se granskning `2026-09-14-004`.

## Rättningsrunda 1 — svar på granskning 2026-09-14-004

Alla fyra bindande fynden (tre P1, ett P2) rättade. Katalogen, tariffdata, priser och
tariffspärrar oförändrade — samtliga fyra `investigation.status="utreds"` och
dispositionen fortsatt **33/31/28 av 92**.

1. **P1 — dubbelriktad multiplikatorbindning** (`enkey-agents@dd51562`).
   `till_prisar` (katalog.py) transporterar nu en explicit
   `kapacitet.multiplikator_typ`-markör till `prisar`, satt bara när
   `capacity.post_multiplier` matchar exakt en post i den nya, källpinnade
   `policyregister._KANDA_MULTIPLIKATORER`. Motorn (`_arskostnad_kapacitet` i
   faktura.py, `arskostnadKapacitet` i fjarrvarme.ts) vägrar nu en
   `kapacitet_multiplikator` om denna markör saknas — även vid ett direkt
   motoranrop som kringgår hela aktiveringsgrinden. `kontrollera_aktiveringsgrind`
   kör dessutom `kontrollera_kompositgrind` för VARJE tariff vars policy eller
   katalograd nämner en multiplikator, i båda riktningarna. Codex reproduktion (en
   syntetisk `kapacitet_multiplikator_bindning` på en Jämtkraft-policy, som saknar
   `post_multiplier` helt) kastar nu `ValueError` i stället för att halvera
   kapacitetskostnaden tyst — verifierat manuellt mot exakt Codex reproduktion.
2. **P1 — kompositgrinden accepterade godtycklig struktur** (samma commit).
   `kontrollera_kompositgrind` kräver nu att `capacity.post_multiplier` matchar
   exakt en av `_KANDA_MULTIPLIKATORER` (Umeås enda källverifierade B-formel:
   `name="B"`, exakt `input_U` och fyra exakta `pieces`). Codex reproduktionsstruktur
   (`{"name":"X","input_U":"anything","pieces":[...]}`) avvisas nu.
3. **P1 — justeringsschemat ignorerade unit/formula** (samma commit).
   `_valid_flow_difference`/`_valid_asymmetric_flow_difference` (justeringar.py)
   validerar nu en sluten nyckelmängd, ett pinnat `unit="SEK/m3"` och (för
   `flow_difference`) ett `formula` härlett från postens egna `rate`/
   `reference_m3_per_MWh`. Codex reproduktion (byt båda fälten till `"WRONG"`)
   avvisas nu för båda typerna; en injicerad, källmässigt obefintlig
   `formula`-nyckel på `asymmetric_flow_difference` avvisas som en oväntad nyckel.
4. **P1 — saknat verkligt UI-/produktbytesprov** (`neptune_academy@dd0ebaf`).
   Ny `KalkylatorPageBatch4.test.tsx`: injicerar en Umeå- och två Jämtkraft-
   kandidater via `vi.mock('../data/tariffer.generated')`, bevisar korrekta
   fält/enheter/etiketter för båda familjerna, en normal MWh-submit till ett
   synligt uppskattat resultat, samt produktbyte Jämtkraft↔Jämtkraft och
   Jämtkraft↔Umeå som INTE tyst återanvänder effekt (`#kapacitetKw`), band eller
   det MEDVETET delade `flode_okt_apr_m3`-fältet — `handleFormChange` nollställer
   hela `policyFaltRaw`-objektet vid varje leverantörsbyte, oavsett nyckelnamn.
5. **P2 #4 — generatorns sluträkning** (`enkey-agents@dd51562`).
   `generera.py:main()` skickar nu explicit `policyregister=POLICYREGISTER` till
   den avslutande `godkanda(katalog)`-räkningen, samma register
   `bygg_ts_fran_katalog` de facto redan använde.

**Nya commit-hashar:**
- `enkey-agents@dd51562` — multiplikatorbindning, kompositgrind, justeringsschema,
  generatorns explicita register, sju nya negativa test.
- `neptune_academy@dd0ebaf` — motorförsvar mot multiplikator utan markör, ny
  `KalkylatorPageBatch4.test.tsx` (10 test).

**Verifiering:**
- Python: `tools/tariffer/tests` → **1266 passed, 4 skipped** (1259+4 skip baslinje +
  7 nya).
- TypeScript: `vitest run` → **1207 passed** i 41 filer (1194 baslinje + 13 nya:
  3 direkta motorförsvarsprov, 10 i `KalkylatorPageBatch4.test.tsx`).
  `npx tsc --noEmit`: godkänt (efter borttagning av två oanvända testkonstanter).
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning.
- `node e2e/kalkylator.smoke.mjs` mot det isolerade bygget: samtliga **15/15**
  befintliga scenarier godkända (inget nytt Batch 4-scenario — de fyra raderna är
  fortfarande spärrade och kommer omockas i den senare aktiveringsrundan).
- Generatorsynk: en fristående regenerering av `tariffer.generated.ts` mot
  `skills@c1d83200c08903610e28ac20c504d748dd067081` är **byte-för-byte identisk**
  med den incheckade filen — fortsatt 35 produkter totalt (33 katalog + 2
  leverantörsfiler), inga Batch 4-ID:n läckta.
- Mekanisk kontroll: `godkanda(katalog)` == 33, katalogen har fortsatt 86 poster.
  Dispositionen är oförändrad **33/31/28 av 92**.
- `git diff --check` rent i båda repona (endast Python-/TypeScript-källfiler och
  denna sessionsfil ändrade — inget katalog-/prisdata, inga orelaterade filer,
  ingen befintlig `dist/`-smuts rörd).

Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-14-005

Codex omgranskade rättningsrunda 1 vid `skills@2ea4ae2`, `enkey-agents@dd51562` och
`neptune_academy@dd0ebaf`. Beslut: **changes required före aktivering**. Jämtkraftvägen,
flödesjusteringsschemat och produktbytet är stängda, men multiplikatorn accepterar fortfarande
extra struktur, fel policyintervall, ett godtyckligt typ-ID och direkt `B=14`. Kandidat-UI-
provet behöver pinna de enheter/status/fältnära fel som det påstår, två andra-pass-prov
saknas och verifieringslistan/inventeringen/batchplanen är fortfarande osynkade.

Full verifiering är grön: 1266+4 skip Python, 1207 TypeScript, tsc, isolerat bygge, 15/15
E2E och byte-identisk 35-produktsgenerator. Det ändrar inte det reproducerade P1-fyndet.
Bindande rättningsordning finns i
`conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-1.md`. Spärrarna och
33/31/28 ligger kvar; ingen aktivering eller push är godkänd.

**Rättelse av rättningsrunda 1:s slutsats** (granskning 2026-09-14-005): rubriken
"Alla fyra bindande fynden (tre P1, ett P2) rättade" ovan var för stark. Granskning
004 hade fyra P1-rubriker (multiplikatorbindning, kompositgrindstruktur,
justeringsschema-validering, saknat UI-/produktbytesprov) plus en sammansatt P2
(dokumentationssynk). Multiplikatorbindningen visade sig INTE vara fullt stängd —
se rättningsrunda 2 nedan — och dokumentationssynken var öppen. Behåll ovanstående
punkter 1–3 som en beskrivning av VAD som ändrades i den commiten, inte som ett
påstående att alla fynd då var stängda.

## Rättningsrunda 2 — svar på granskning 2026-09-14-005

Två kvarvarande fynd stängda. Katalog, tariffdata, priser och tariffspärrar
oförändrade — samtliga fyra `investigation.status="utreds"` och dispositionen
fortsatt **33/31/28 av 92**.

1. **P1 — multiplikatorns "exakta" deskriptor och direkta motorvakt var fortfarande
   öppna** (`enkey-agents@5a56c27`, `neptune_academy@8e5bb96`). `multiplikator_typ()`
   extraherade tidigare en REDUCERAD kandidat och kastade tyst bort okända nycklar
   på toppnivå och i varje `pieces`-post — båda extra-nyckelfallen matchade
   fortfarande. Kompositgrinden krävde inte att policyfältets `minvarde`/`maxvarde`
   var EXAKT det källpinnade `[0.93, 1.401]`. Motorn (Python och TypeScript)
   kontrollerade bara att `multiplikator_typ` RÅKADE vara en sträng och att talet
   var ändligt — accepterade därför både ett påhittat typ-ID och ett värde utanför
   intervallet.

   Rättat: `_KANDA_MULTIPLIKATORER` bär nu `{"shape": …, "interval": …}`, där
   `interval` kommer från en enda ny konstant `MULTIPLIKATOR_GRANSVARDEN`
   (`faktura.py` — den lägsta modulen i importgrafen, för att undvika en cirkulär
   import mot `policyregister.py`, som i sin tur importerar den för sin
   intervallkontroll). `multiplikator_typ()` kräver nu EXAKTA nyckelmängder
   (`set(...) != {...}` avvisar direkt) för både `post_multiplier` och varje
   `pieces`-post. `kontrollera_kompositgrind` korsvaliderar policyfältets
   `minvarde`/`maxvarde` mot samma `MULTIPLIKATOR_GRANSVARDEN[typ]`. Motorn
   (`_arskostnad_kapacitet`/`arskostnadKapacitet`) kräver nu att typ-ID:t finns i
   `MULTIPLIKATOR_GRANSVARDEN` OCH att värdet ligger inom dess intervall — även vid
   ett direkt anrop. Reproducerat och bekräftat blockerat: giltig Umeåmarkör +
   direkt `B=14` (gav tidigare 285 334 kr) och `multiplikator_typ="arbitrary"` +
   `B=0.5` (gav tidigare 10 190,50 kr) kastar nu båda. Gränserna 0,93/1,401 själva
   fungerar fortfarande.
2. **P2 — kandidat-UI-provet gjorde inte alla påstådda assertioner**
   (`neptune_academy@8e5bb96`). `KalkylatorPageBatch4.test.tsx` räknar nu exakt antalet
   synliga policyfält (2 för Jämtkraft, 3 för Umeå, utöver `#kapacitetKw`), pinnar
   etiketter/enheter, och har fältspecifika `-fel`-prov för saknat/ogiltigt band,
   flöde, B samt ogiltig (negativ) effekt — inte bara "inget resultat visas" för de
   fall det inte har någon dedikerad fältnära text (helt tomt `#kapacitetKw` hoppar
   över den tidiga UI-genvägen och faller igenom utan egen `-fel`-sträng, samma
   etablerade mönster som Umeås ursprungliga "saknad B"-test). Statusdimensionen
   `annual/snapshot/complete` bevisas EXPLICIT i `resultatkontrakt.batch4.test.ts`
   (redan befintliga assertions mot `res.status.*`) — nya kommentarer i båda
   filerna pekar korsvis på varandra så det är tydligt vilken del som bevisar
   vilken statusdimension, i stället för att komponentprovets svaga
   "uppskattad"-textsträng felaktigt påstods bevisa den.
3. **P2 — beställda andra-pass-regressioner och levande dokumentationssynk**
   (`enkey-agents@5a56c27`, `skills@2716a0f`). Två nya tester
   (`test_kompositgrindens_andra_pass_avvisar_dold_okand_issue`/`..._justering`)
   bevisar att en giltig multiplikatorbindning inte kan dölja en okänd `issue`
   eller okänd justeringstyp för `godkanda()`s andra pass. `verifieringslista-
   fjarrvarmebolag.md` (Jämtkraft ×3 och Umeå) är omskriven till sant nuläge: `15_1`
   sidorna 19–20 i stället för `15_0` s.18–19, "implementerat bakom spärr" i stället
   för "måste mappas", och Umeå-blocket säger nu explicit "direkt A och direkt B,
   aldrig U" i stället för "leverantörens A och B/U". `tariffinventering-v22.md`
   (rad ~804/823/842) och `batchplan-v22.md` (rad ~918) är rättade till TRE
   tariffspecifika Jämtkraft-fält (effekt, bekräftat band-ID, flöde), inte två.

Riktad Batch 4-svit: **47 Python** (41 tidigare + 6 nya), **29 TypeScript**
(23 tidigare + 6 nya). Full Python: **1271 passed, 4 skipped**. Full TypeScript:
**1218 passed** i 41 filer. `npx tsc --noEmit`: rent. Disposition mekaniskt
omverifierad: `godkanda(katalog)` fortsatt 33, katalogen 86 poster, dispositionen
**33/31/28 av 92**. Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-14-006

Codex omgranskade rättningsrunda 2 vid `skills@62b0bc9`, `enkey-agents@5a56c27` och
`neptune_academy@8e5bb96`. Beslut: **changes required före aktivering**. Den exakta
multiplikatorbindningen, motorintervallet, andra-pass-regressionerna, produktbytet och
statusbeviset är stängda. Rättningsrundan skrev däremot felaktigt om Jämtkrafts verifierade
12-månadersregel till E.ON/Navirums 36-månadersregel inklusive fakturamånad i alla tre
verifieringsposter. UI-proven medger fortfarande att tom obligatorisk effekt saknar
kalkylatorns fältnära `#kapacitetKw-fel`, och de påstådda `kW`-/`m³`-assertionerna testar
inte enheterna. Ett direkt Python-motoranrop accepterar dessutom
`kapacitet_multiplikator=True` som B=1 medan TypeScript och kontraktslagret avvisar bool.

Oberoende verifiering: 1271+4 skip i tariffsviten, 1218 TypeScript, tsc, produktions- och
eval-bygge samt 15/15 E2E är gröna. Katalogen har 86 poster, `godkanda()` 33, inga Batch
4-ID:n är aktiva och generatorsynken består. Bindande rättningsordning finns i
`conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-2.md`. Spärrarna
och 33/31/28 ligger kvar; ingen aktivering eller push är godkänd.

## Rättningsrunda 3 — svar på granskning 2026-09-14-006

Rättade det ena P1-fyndet och de tre P2-fynden.

1. **P1 — Jämtkrafts felaktiga 36-månadersregel rättad till den verifierade
   12-månadersregeln.** `verifieringslista-fjarrvarmebolag.md` rad 135/140/145 sa
   felaktigt att debiteringseffekten byggde på "de senaste 36 månaderna inklusive
   fakturamånaden" och krävde en bekräftad fakturamånad — detta var E.ON/Navirums
   Batch 3b-regel, inte Jämtkrafts. Jämtkrafts officiella prisändringsmodell
   2026–2028 (tryckt sida 11/20) samt den redan implementerade
   `_jamtkraft_kapacitet_krav`-policyn (`policyregister.py:942-959`, `kalperiod_definition=""`,
   inget `kravsObserveradPeriod`) anger båda 12 månader utan fakturamånadskrav.
   Koden var alltid korrekt — bara dokumentationstexten (kopierad in av misstag från
   fel tariffamilj i en tidigare runda) var fel. Rättade alla tre rader till "de
   senaste 12 månaderna" utan fakturamånad/tidsserie.
2. **P2 — tom obligatorisk effekt ger nu kalkylatorns fältnära svenska fel.**
   `KalkylatorPage.tsx` skippade tidigare all validering för ett HELT tomt
   `#kapacitetKw` (bara guarded av `!== ''`) och föll igenom till domänlagrets
   `KontraktBlockerat('missing_capacity')`, som inte sätter `saknadeFalt` — bara den
   generiska HTML-`required`-blockeringen skyddade fältet. Lade en explicit
   `else`-gren för tomt värde (för kontraktsgatade tariffer) som sätter
   `#kapacitetKw-fel`, `aria-invalid` och `aria-describedby`, precis som band/flöde.
   Uppdaterade båda Batch 4-testen (Jämtkraft och Umeå) att assertera detta explicit
   i stället för bara "inget resultat visas".
3. **P2 — enhetsproven pinnar nu faktiskt `kW`/`m³`.** Testet sökte tidigare bara
   delar av hjälptexten. Lade explicita assertioner på de fullständiga etiketterna
   `Debiterbar effekt (kW)`, `Debiterbar årseffekt A (kW)` och
   `Flöde 1 oktober–30 april (m³)`.
4. **P2 — Pythons bool-glipa i den direkta motorvakten stängd.** `math.isfinite()`
   godtog `bool` (int-underklass i Python) som `kapacitet_multiplikator`; ett direkt
   anrop med `True` gav 20 381 kr i stället för att kastas. Avvisar nu bool explicit
   före isfinite-kontrollen. TypeScript var redan korrekt
   (`Number.isFinite(true)===false`) — lade en explicit bekräftande TS-test.

**Commit-hashar:**
- `enkey-agents@fcecc48` — `faktura.py`s bool-avvisning + direkt Pythonregressionstest.
- `neptune_academy@fa872c4` — `KalkylatorPage.tsx`s tom-effekt-fältfel, Batch 4-testens
  fältnära/enhets-/bool-assertioner.
- (skills-commit för denna post och `verifieringslista-fjarrvarmebolag.md` följer.)

**Verifiering:** riktad Python 42 passed (Batch 4-filen), full Python **1272 passed,
4 skipped**. Riktad TypeScript 42 passed, full TypeScript **1219 passed** i 41 filer.
`npx tsc --noEmit`: rent. Isolerat `npm run eval:build`: godkänt, endast känd
bundelstorleksvarning. E2E mot isolerat bygge: **15/15** scenarier godkända (Batch 4
förblir spärrad, avsiktligt inget nytt scenario). Generatorsynk: 2 passed. Mekaniskt
verifierat: katalogen har 86 poster, `godkanda(katalog)`==33, inga Batch 4-ID:n bland
de godkända. Disposition oförändrad **33/31/28 av 92**. `git diff --check`: rent i alla
tre repon (bortsett från den sedan tidigare orelaterade `../milesight`-submodulpekaren
och `neptune-marketing/dist`, ingen av vilka rörts). Ingen aktivering, ingen push.
Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-14-007

Codex omgranskade rättningsrunda 3 vid `skills@910a3fc`, `enkey-agents@fcecc48` och
`neptune_academy@fa872c4`. De fyra fynden i granskning 006 är stängda och oberoende
verifierade. Beslutet är ändå **changes required före aktivering** eftersom Umeås
komponentkandidat inte motsvarar den verkliga serialiserade policyn: testet sätter tom
`kalperiod_definition`, `rullande:true` och en fabricerad etikett, medan
`POLICYREGISTER`/generatorn ger en treårig kalenderdefinition, `rullande:false` och
`Debiterbar årseffekt (A)`. Testets normal-submit slipper därför det verkliga obligatoriska
`#kapacitetKw-period`-fältet och kan bli falskt grönt.

Oberoende verifiering: 1272+4 skip i tariffsviten, 1219 TypeScript, tsc, eval-bygge,
15/15 E2E och två generatorsynkprov är gröna. Katalogen har 86 poster, `godkanda()` 33,
inga Batch 4-ID:n är aktiva och 33/31/28 består. Bindande rättningsordning finns i
`conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-3.md`. Ingen
aktivering och ingen push är godkänd.

## Rättningsrunda 4 — svar på granskning 2026-09-14-007

Rättade exakt det enda P1-fyndet: Umeås testfixtur i
`KalkylatorPageBatch4.test.tsx` fick sin kapacitetskravsobjekt ändrat till att
källverifierat, ordagrant matcha den riktiga `policyregister.py:_umea_kapacitet_krav`
(icke-tom treårig `kalperiod_definition`, `rullande=false`, etiketten
`Debiterbar årseffekt (A)`). Literalen upprepas i testfilen (inte delad via en
modulnivåkonstant) för att undvika samma `vi.mock`-TDZ-fälla filens övriga
literaler redan dokumenterar.

Lade fyra nya/utökade prov:

1. period-renderingsprov: `#kapacitetKw-period` visas med korrekt etikett
   ("Källperiod debiterbar effekt avser (ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD)") och den
   fullständiga hjälptexten ur den riktiga `kalperiod_definition`.
2. saknad period blockerar submit fältnära via `#kapacitetKw-fel`/ARIA, delat
   med kapacitetsfältets felyta (samma mönster som övriga period-krav i
   `KalkylatorPage.tsx`).
3. ogiltigt periodformat blockerar submit fältnära med rätt felbeskrivning
   (`ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD`).
4. normal submit med giltig treårsperiod (`2023-01-01/2025-12-31`) ger ett
   synligt uppskattat resultat.
5. produktbytesprov: perioden visas (tom) efter byte Jämtkraft→Umeå, och
   försvinner helt (inte bara töms) efter byte Umeå→Jämtkraft — även om
   användaren byter tillbaka till Umeå igen.

De fem tidigare Umeå-submit-testen (B utanför intervall, saknad B, saknat band,
saknat flöde) fyller nu även periodfältet innan submit, eftersom perioden annars
skulle blockera FÖRE de fält testet faktiskt avser att pröva (kapacitets-/
periodkontrollen i `KalkylatorPage.tsx` körs innan den generiska
policyfält-loopen).

**Commit:** `neptune_academy@dfe4b9f` — enda ändrade fil:
`neptune-marketing/src/pages/KalkylatorPageBatch4.test.tsx`. `skills` och
`enkey-agents` oförändrade denna runda.

**Verifiering:** riktad TypeScript (Batch 4-filen) **20 passed** (18 tidigare + 2
nya). Full TypeScript-svit **1221 passed** i 41 filer (1219 + 2 nya). `npx tsc
--noEmit`: rent. Full Python-svit oförändrad **1272 passed, 4 skipped** (ingen
produktionskod rörd denna runda). Isolerat `npm run eval:build`: godkänt, endast
känd bundelstorleksvarning. E2E mot isolerat bygge: **15/15** scenarier godkända
(Batch 4 förblir spärrad, avsiktligt inget nytt scenario). Generatorsynk: 2
passed. Mekaniskt verifierat: katalogen har 86 poster, `godkanda(katalog)`==33,
disposition oförändrad **33/31/28 av 92**. `git diff --check`: rent (bortsett
från den sedan tidigare orelaterade `neptune-marketing/dist`, som inte rörts).
Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex slutgranskning 2026-09-14-008

Codex slutgranskade fix-runda 4 vid `skills@a0d9f75`, oförändrat
`enkey-agents@fcecc48` och `neptune_academy@dfe4b9f`. Det sista P1-fyndet är stängt:
Umeåmocken speglar nu den verkliga treåriga kalenderdefinitionen, `rullande:false`, exakt
etikett/hjälptext och periodfältets renderings-, fel-, submit- och produktbytesvägar.

Codex reproducerade 20 riktade komponentprov, 1221 TypeScriptprov, ren tsc, 1272+4 skip
Python, grönt eval-bygge, 15/15 E2E och två generatorsynkprov. Katalogen har fortfarande
86 poster, `godkanda()` 33, inga Batch 4-ID:n är aktiva och dispositionen är 33/31/28.

Batch 4 är därmed **godkänd för en separat lokal aktiveringsrunda** av exakt tre
Jämtkraftprodukter och Umeå Enkel. Bindande aktiveringsorder finns i
`conversations/reviews/2026/09/2026-09-14-slutgranskning-batch-4-fixrunda-4.md`. Målet är
37/27/28 och 39 skarpa produkter. **Ingen push före ny Codex-granskning av
aktiveringsdiffen.**
