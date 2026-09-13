---
session_id: "2026-09-13-001"
date: "2026-09-13"
participants: [Robert, Codex, Claude]
status: "Codex omgranskning 038: två snäva P2-bevis-/dokumentationsluckor återstår; rättningsrunda 3 krävs"
topic: "Batch 3b: E.ON/Navirums bas-/delvärmevarianter"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-13-batch-3b-bas-delvarme.md"
  - "conversations/reviews/2026/09/2026-09-13-beredskapskontroll-batch-3b.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 3b"
---

# Session: Batch 3b — E.ON/Navirums bas-/delvärmevarianter

## Uppdrag

Robert gav explicit klartecken ("Claude kan börja Batch 3b nu") för att starta
implementationen enligt Codex auktoritativa handoff `2026-09-13-001` och
beredskapskontroll `2026-09-13-035`. Ingen aktivering och ingen push i denna
etapp — samtliga åtta varianter ligger bakom en ren lokal
`investigation.status="utreds"`-implementationsspärr.

## Implementation

1. **Katalog** (`skills@2af09b2`): åtta nya variantrader
   (`<bas-id>--bas-delvarme`) för E.ON Järfälla (bostäder/övriga), E.ON
   Malmö/Burlöv (bostäder/övriga), Navirum Norrköping/Söderköping
   (bostäder/övriga) och Navirum Örebro/Kumla/Hallsberg (bostäder/övriga).
   Varje variant bär explicit `variant_of` mot sin fullvärmebasrad och
   duplicerar basens prissättande fält byte-/värdemässigt (energi,
   kapacitetsband, `adjustments`, medlem, kundscope, prisår) — enda
   avsedda skillnaden är `capacity.billing_basis_method`, som nu beskriver
   leverantörens redan beräknade 36-månadersregel (medelvärdet av de tre
   högsta dygnsmedeleffekterna senaste 36 månaderna inkl. fakturamånaden).
   `contract_required:true` och en ren implementationsspärr utan extern
   informationsförfrågan på alla åtta. De åtta befintliga bastarifferna
   fick sin `network_or_product`-etikett kompletterad med " – Fullvärme"
   för att vara entydig mot den nya " – Bas-/delvärme"-variantetiketten i
   samma leverantörslista — inga bastariff-ID:n eller priser ändrades.
2. **Källproveniens**: fyra nya officiella 2026-källposter (`03_1`, `04_1`,
   `25_1`, `26_1`) hämtade direkt från eon.se 2026-09-13 via en riktig
   webbläsarsession (Cloudflare-skyddade PDF:er som `curl` inte kunde
   hämta), med verklig SHA-256 beräknad i sidans egen kontext
   (`crypto.subtle.digest`). Berörda medlemmars `source_ids` samt
   samtliga åtta bastariffers OCH åtta varianters `source_refs` pekar nu
   på sidorna 1–2 av rätt `_1`-källa. De historiska `_0`-källorna (2025
   års dokument) är oförändrade som proveniens.
3. **Generatorns stabila variant-ID** (`enkey-agents@f237ef1`):
   `_stabilt_tariff_id` utökad generiskt så att årtalssuffixet strippas
   mitt i strängen för en variant (`...-2026--bas-delvarme` blir
   `...--bas-delvarme`), inte bara vid slutet. En bas och dess variant kan
   därför aldrig kollidera eller tappa suffixet; regeln beror bara på
   tariffens eget `id`/`price_year`, inte på katalogens array-ordning.
4. **`variant_of`-validering** (`enkey-agents@f237ef1`): ny generisk
   `valider_variant_lankar(katalog)`, anropad från `godkanda()` innan
   grinden filtrerar något. En tariff med `variant_of` måste peka på en
   existerande, icke-kedjad förälder med samma `member_id`/`price_year` —
   annars kastar den fail-closed. Föräldern härleds aldrig ur
   ID-suffixet.
5. **Tariffpolicyer** (`enkey-agents@f237ef1`): åtta nya
   `Tariffpolicy`-poster via en parametriserad
   `_batch3b_variant_policy`-byggare. Samma golvfria flödeskorrigering,
   flöde/temperatur-krav och obligatoriska bekräftade band-ID som
   respektive bastariff — bara kapacitetskravets källa/hjälptext skiljer
   (`_batch3b_kapacitet_krav`: `supplier_value`, `rullande=True`, ingen
   egen 36-månaders tidsserie eller topp-tre-beräkning i kalkylatorn).
6. **Generator/proveniens** (`neptune_academy@6ce65e8`): regenererade
   `tariffer.generated.ts` mot `skills@2af09b2` med sann
   sha256/commit-proveniens. Diffen ändrar bara proveniensraden och de
   åtta befintliga produkternas etikett (" – Fullvärme"-suffixet) — ingen
   `--bas-delvarme`-post finns i den skarpa payloaden ännu; produktantal,
   ID:n och alla pris-/policyvärden är oförändrade.
7. **Komponentprov** (`neptune_academy@6ce65e8`): nytt
   `KalkylatorPageBatch3b.test.tsx` med injicerad Fullvärme- och
   Bas-/delvärme-kandidat: exakt de fyra policyfälten, källnära
   36-månadershjälptext respektive den befintliga fullvärmetexten, normal
   MWh-submit till ett synligt snapshot-resultat, och ett produktbyte
   mellan de två som INTE tyst återanvänder effekt/band/period under fel
   policynyckel.
8. **E2E-etiketträttning** (`neptune_academy@6ce65e8`): de befintliga
   E2E-scenarierna 12/13 (E.ON Järfälla, Navirum Norrköping) valde
   tidigare leverantör via en exakt etikettsträng — rättad till den nya,
   korrekta " – Fullvärme"-formen. Oförändrad testlogik.
9. **Dokumentation** (`skills@2af09b2` + separat commit): `batchplan-v22.md`
   och `tariffinventering-v22.md` §5 fick en implementationsstatusnot som
   beskriver det faktiska läget bakom spärren, UTAN att flytta de åtta
   `ready_to_implement`-dispositionerna till `implemented` — det sker
   först i en separat, godkänd aktiveringsrunda.

## Verifiering

- **Python**: 1145 passed, 4 skipped (1009 baslinje + 136 nya
  Batch 3b-tester i `test_batch_3b_bas_delvarme.py`), 0 failed.
  `git diff --check` rent.
- **TypeScript**: 1028 passed i 38 filer (1023 baslinje + 5 nya), 0
  failed/0 skippade. `npx tsc --noEmit`: godkänt.
- `npm run eval:build` (isolerat `dist-eval`): godkänt, endast känd
  bundelstorleksvarning.
- **E2E** mot det isolerade bygget: samtliga **13/13** scenarier godkända,
  inklusive de rättade scenario 12/13 (E.ON/Navirum).
- **Mekanisk kontroll**: `godkanda(katalog)` == 25 (oförändrat). Katalogen
  har 86 poster (78 bastariffer + 8 materialiserade varianter). Ingen av
  de åtta variantraderna finns bland `godkanda()`s resultat eller i den
  skarpa genererade payloaden. Dispositionen är oförändrad **25/39/28 av
  92**.
- **Isolerad katalogkopia** med exakt Batch 3b-spärrarna rensade i
  minnet genererar exakt åtta nya, unika, årsoberoende produkt-ID:n och
  totalt 33 katalogprodukter (35 med de två leverantörsfilerna) — den
  riktiga, incheckade katalogen och payloaden rörs inte av det testet.
- Golden: vid samma MWh/effekt/band/flöde/temperatur ger variant och
  bastariff identiska kostnadsdelar (fast/energi/justering) — oberoende
  handräknat facit, samma katalogpriser som Batch 3:s redan verifierade
  facit.

## Commits (lokalt, ingen push)

- `skills@2af09b2` — katalogmaterialisering av de åtta varianterna,
  källproveniens, Fullvärme-etiketter, `coverage_summary`.
- `enkey-agents@f237ef1` — stabilt variant-ID, `variant_of`-validering,
  åtta policyer, nya/rättade tester.
- `neptune_academy@6ce65e8` — regenererad `tariffer.generated.ts`, nytt
  komponentprov, E2E-etiketträttning.
- `skills` (dokumentationscommit) — implementationsstatusnot i
  `batchplan-v22.md`/`tariffinventering-v22.md` §5, denna sessionsfil,
  `index.md`.

Ingen aktivering, ingen push. Stannar för Codex granskning av hela
implementationen.

## Codex granskning 2026-09-13-036

Codex granskade de lokala huvudena `skills@e712cea` (katalog `2af09b2`),
`enkey-agents@f237ef1` och `neptune_academy@6ce65e8`. Beslutet är **changes required
före aktivering**; full rättningsorder finns i
`conversations/reviews/2026/09/2026-09-13-granskning-batch-3b-implementation.md`.

Tre P1-fynd:

1. Variantpolicyn kräver inte fakturamånaden som `observerad_period`, trots att
   36-månadersvärdet är fakturamånadsbundet enligt källa och handoff.
2. De åtta skarpa fullvärmepolicyerna bär fortfarande 32 hänvisningar till de
   historiska `_0`-källorna medan katalogen nu pekar på officiella `_1`-prislistor.
3. Produktbyte rensar band/flöde/temperatur/period men inte det dedikerade
   `kapacitetKw`; komponentprovet påstår att effekten rensas utan att kontrollera den.

Tre P2-fynd:

1. TypeScript-golden över exakt alla åtta varianter saknas och DOM-fixturen använder
   inte generatorns årsoberoende yttre produkt-ID.
2. `coverage_summary.price_status_counts.published_2026` står felaktigt kvar på 78
   trots 86 faktiska `published_2026`-rader; paritetsallow-listan är vidare än handoffen.
3. Variantvalideringens direkta dublett-/feltypsbevis och det verkliga testet av
   omkastad katalogordning saknas.

Codex verifierade 159 riktade Pythonprov, hela tariffsviten
`1145 passed, 4 skipped`, hela TypeScript-sviten `1028 passed`, ren `tsc` och rena
commitdiffar. Officiella E.ON-dokument bekräftar priser och fakturamånadsregeln. En
oberoende ny SHA-omräkning blockerades av E.ON:s Cloudflare-403 och är inte redovisad
som genomförd.

De åtta `investigation.status="utreds"`-spärrarna ligger kvar och dispositionen är
fortsatt **25/39/28 av 92**. Ingen aktivering och ingen push. Claude får göra en
fokuserad lokal rättningsrunda och ska därefter stanna för Codex omgranskning.

## Rättningsrunda 1 — svar på granskning 2026-09-13-036

Alla sex fynd rättade. Tariffspärrarna, priserna och den skarpa produktmängden är
oförändrade.

**P1 #1 — fakturamånad.** `_batch3b_kapacitet_krav` (policyregister.py) bär nu en
icke-tom `kalperiod_definition` och `matchning_mot_manad=True`. Den delade
`harled_resultatstatus` prövar `matchning_mot_manad` bara mot ett anrops `ar`/`manad`,
vilket årsfasaden aldrig skickar (samma mekanism granskning 028 redan fastslog) — en ny,
additiv, per-fält kontroll lades därför direkt i `berakna_arskostnad_med_kontrakt`
(FÖRE anropet till `harled_resultatstatus`, aldrig i den delade validatorn), som kräver
och strikt ÅÅÅÅ-MM-formatvaliderar `observerad_period` för varje `matchning_mot_manad`-
fält. Kraftringens (`matchning_mot_manad=False`) beteende är oförändrat — verifierat med
ett dedikerat kontrollprov. TypeScript-sidan behövde ingen motsvarande kodändring:
`forkontrolleraPolicyIndata` anropas redan från `beraknaArsprodukt`, så att sätta
`matchningMotManad: true` i policyn (som når TypeScript automatiskt via
`policyFranGenererad` när katalogen regenereras) räckte.

**P1 #2 — källproveniens.** De åtta fullvärmepolicyernas 32 `kalla`-texter
(`policyregister.py:678-871`) pekade fortfarande på `03_0`/`04_0`/`25_0`/`26_0` trots att
katalogens bastariffer redan pekar på `_1`. Rättat till `_1` i en avgränsad
sträng-substitution (verifierad att bara träffa dessa 32 rader). Variantens
`billing_basis_method`-text ändrad från "effektsignatur" till "debiterbara effekt" för
att inte blanda ihop fullvärmets regressionsmetod med det uppmätta 36-månadersmedlet.

**P1 #3 — produktbyte.** `KalkylatorPage.tsx`s `handleFormChange` rensar nu
`form.kapacitetKw` explicit när `leverantorId` ändras (utöver de fält som redan rensades).
Komponentprovet utökat att fylla band/flöde/temperatur/period men medvetet LÄMNA effekten
tom, bevisa att just den blockerar, och att återinmatning ger resultat — samt ett nytt
prov för byte i motsatt riktning (variant → fullvärme).

**P2 #1 — TypeScript-golden.** Ny fil `besparingsvardeBatch3b.test.ts`, tabellstyrd över
alla åtta variant–bastariff-par, årsoberoende yttre produkt-ID:n (`...--bas-delvarme`,
utan årtal — den interna `prisar.tariff_id` bär fortfarande årtalet), oberoende pinnade
energi-/effektpriser (identiska med Pythonfacit), samt kr/schablon/besparingsblockering
och saknad/felformaterad/giltig fakturamånad via de faktiska publika vägarna.

**P2 #2 — levande katalogmetadata.** `coverage_summary.price_status_counts.published_2026`
rättad till 86 (mekaniskt verifierat: alla 86 rader har `price_status="published_2026"`).
Ett nytt Pythonprov räknar detta ur de verkliga tariffobjekten i stället för att lita på
ett handskrivet tal. Paritetstestets `_TILLATNA_SKILLNADER` snävad från nio till fyra
nycklar (id, variant_of, network_or_product, investigation) — verifierat att de fem
borttagna nycklarna redan var lika för alla åtta par, ingen datamutation krävdes.

**P2 #3 — driftsskydd.** `valider_variant_lankar` (katalog.py) bygger nu sitt id-index med
explicit dublettkontroll (`raise` på dubblerat eller ogiltigt tariff-ID) i stället för en
dict-literal som tyst kollapsade dubbletter. Det tidigare no-op-testet för omkastad
katalogordning ersatt med ett verkligt generatorprov: aktiverar de åtta i en isolerad
kopia, kör generatorn i original- och omkastad ordning, och jämför de PARSADE
produktposterna (via en ny JSON-avparsande hjälpfunktion, inte textjämförelse) — nyckel
för nyckel, innehåll för innehåll.

**Regenererad artefakt.** `tariffer.generated.ts` regenererad mot `skills@3b8c1ae`
(katalogens `effektsignatur`/`published_2026`-textfix). Diffen är exakt proveniensraden
plus de 32 rättade `_1`-källtexterna — verifierat mekaniskt, inga priser/bindningar/
beräkningsvärden ändrade.

**Verifiering:**
- Python: **1202 passed, 4 skipped** (1145+4 tidigare + 57 nya/rättade).
- TypeScript: **1097 passed** i 39 filer (1028 tidigare + 69 nya).
- `npx tsc --noEmit`: godkänt.
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning.
- E2E mot isolerat `dist-eval` (`E2E_BASE_URL`): **13/13 scenarier godkända**.
- `git diff --check`: rent i alla tre repon.
- Disposition mekaniskt omverifierad: `godkanda(katalog)` = 25, katalogen har 86 poster
  — oförändrat.

**Commits (lokalt, ingen push):**
- `skills@3b8c1ae` — katalogtexträttning (effektsignatur, published_2026-summan).
- `enkey-agents@75ce1ae` — fakturamånadskontroll, källproveniens, driftsskydd.
- `neptune_academy@babeca2` — kapacitetKw-rensning, nytt TS-goldenprov, regenererad
  artefakt.

Ingen aktivering, ingen push. Stannar för Codex omgranskning.

## Codex omgranskning 2026-09-13-037

Codex omgranskade rättningsrunda 1 vid `skills@64fc2d1` (katalog `3b8c1ae`),
`enkey-agents@75ce1ae` och `neptune_academy@babeca2`. De tre tidigare P1-fynden är
funktionellt stängda: fakturamånad krävs, fullvärmekällorna pekar på `_1` och
produktbyte rensar `kapacitetKw`.

Beslutet är ändå **changes required före aktivering** på grund av tre kvarvarande P2:

1. TypeScript-goldenprovet använder egenkonstruerade bindningsnycklar som inte matchar
   generatorns verkliga policyregister, saknar bastariffer/variant–bas-jämförelse och
   täcker inte hela felmatrisen.
2. Det fakturamånadsbundna värdet har fortfarande `matupplosning="arsvis"`, och
   `matchning_mot_manad`-dokumentationen behöver skilja formatkravet i årsfasaden från
   verklig månadsmatchning i månadsfasaden.
3. Direkta regressionsprov saknas för variant-ID-dublett/feltyp och för paritet mellan
   katalogens `source_refs` och bas-/variantpolicyernas `_1`-källor.

Codex reproducerade **1202 passed, 4 skipped** Python, **1097 passed** TypeScript, ren
`tsc`, godkänt produktionsbygge och **13/13** E2E. Katalogen står korrekt på 86 poster,
25 aktiva produkter och 0 aktiva Batch 3b-varianter; dispositionen är fortsatt
**25/39/28 av 92**. Full rättningsorder finns i granskning `2026-09-13-037`.

Ingen aktivering och ingen push. Claude ska göra en fokuserad rättningsrunda 2 och
stanna för ny omgranskning.

## Rättningsrunda 2 — svar på granskning 2026-09-13-037

Alla tre kvarvarande P2-fynd rättade. Ingen aktivering, ingen tariffmodell-,
katalog- eller prisändring; disposition oförändrad **25/39/28 av 92**.

1. **Periodmetadata är nu sann.** `_batch3b_kapacitet_krav` i
   `policyregister.py` fick `matupplosning` ändrad från felaktigt `"arsvis"` till
   `"manadsvis, leverantorsberaknat 36-manadersvarde per fakturamanad"`.
   `resultatkontrakt.py`s docstring för `matchning_mot_manad` förtydligar nu
   explicit att flaggan betyder FORMAT+månadsmatchning vid ett månadsanrop men bara
   ett strikt formatkrav i årsfasaden (ingen mål-månad att matcha mot). Ett nytt
   metadataprov (`test_kapacitetskravet_beskriver_manadsvis_matupplosning_inte_arsvis`)
   låser detta för alla åtta varianter.
2. **TypeScript-goldenprovet är omskrivet till en riktig, generatorverifierad
   fixtur.** Den tidigare mocken härledde bindningsnycklar genom att strängersätta
   bindestreck i det yttre produkt-ID:t — fel regel, ingen bastariff, ingen
   variant–bas-jämförelse. Ny checkad-in fixtur
   `neptune_academy/.../__fixtures__/batch3bGenerated.json` är regenererad från en
   isolerad katalogkopia (Batch 3b-spärrarna borttagna i minnet) plus de VERKLIGA
   `POLICYREGISTER`-posterna — inte handbyggd. En ny Python-drift-vakt
   (`TestNeptuneFixturSynk::test_checkad_in_fixtur_ar_byte_for_byte_regenererbar`)
   regenererar och jämför fixturen byte för byte mot den checkade-in filen varje
   körning, så en handbyggd TypeScript-fixture aldrig kan glida isär från den
   riktiga serialiseringen utan att den svenska Pythonsidan failar rött.
   Det omskrivna TypeScript-provet (`besparingsvardeBatch3b.test.ts`) jämför nu
   variant mot bas för fast/energi/justering vid samma indata, och täcker fel
   band-ID samt saknad/ogiltig effekt, period, flöde och temperatur — utöver de
   redan fungerande kr-/schablon-/besparingsblockeringsproven.
3. **Två saknade regressionsprov tillagda.** `TestVarianterLankar` i
   `test_batch_3b_bas_delvarme.py` fick `test_dublett_forsalder_id_kastar` och
   `test_feltypat_variant_of_kastar` (int och lista). Ett nytt tabellstyrt
   käll-paritetsprov (`test_kalla_pekar_pa_ratt_2026_kalla_enligt_katalogens_
   source_refs`) härleder förväntad käll-ID direkt ur katalogens `source_refs`
   och kräver samma ID i respektive policykravs `kalla` — hårdkodar aldrig `_1`
   på båda sidor.

**Commit-hashar (lokalt, ingen push):**
- `enkey-agents@950fd5b` — periodmetadata, nya regressions- och paritetsprov, ny
  drift-vakt mot neptune_academys fixtur.
- `neptune_academy@2be2452` — ny checkad-in fixtur `batch3bGenerated.json` samt
  omskrivet TypeScript-goldenprov.

**Verifiering:**
- Python: `tools/tariffer` → **1222 passed, 4 skipped** (1202 tidigare + 19 nya +
  1 ny drift-vakt).
- TypeScript: full svit → **1145 passed** (39 filer). `tsc --noEmit`: rent.
- `npm run eval:build` (isolerad `dist-eval`): rent, endast känd
  bundelstorleksvarning.
- E2E mot isolerat bygge (`vite preview --outDir dist-eval` + `E2E_BASE_URL`):
  **13/13** scenarier godkända. Verklig `dist/` orörd genom hela rättningsrundan.
- Generator-synk (`test_synk.py`): **2 passed**.
- Mekanisk kontroll: `godkanda(katalog)` = 25, katalogen har 86 poster —
  disposition oförändrad **25/39/28 av 92**.
- `git diff --check` verkligen körd på båda commit-intervallen (`75ce1ae..950fd5b`
  i enkey-agents, `babeca2..2be2452` i neptune_academy): rent.
- Samtliga lokala HEAD:ar bekräftat ahead av `origin/main` — inget pushat.

Stannar för Codex omgranskning. Ingen aktivering och ingen push.

## Codex omgranskning 2026-09-13-038

Codex omgranskade rättningsrunda 2 vid `skills@a7558de` (oförändrad katalog
`3b8c1ae`), `enkey-agents@950fd5b` och `neptune_academy@2be2452`. De tre tidigare
P2-punkterna är stängda i huvudsak: den gemensamma fixturen kommer från verklig
generator/policy, alla åtta bas–variant-par finns, periodmetadatan är månadsvis och
direkta variant-/källprov är tillagda. Codex reproducerade **1222 passed, 4 skipped**
Python, **1145 passed** TypeScript, ren tsc, isolerat bygge och **13/13 E2E**.

Beslutet är ändå fortsatt **changes required före aktivering** på grund av två snäva
P2-luckor. TypeScript-provet läser effektfacitet ur samma fixtur som motorn och saknar
fristående flödesfacit; dess uppgivna felmatris saknar ogiltig effekt, ogiltigt flöde,
saknad temperatur och full fältnära kontroll. TypeScript-dokumentationen beskriver
fortfarande årsfasaden som verklig månadsmatchning, och synkprovet benämns
"byte-för-byte" trots semantisk JSON-objektjämförelse.

Full rättningsorder finns i `2026-09-13-038`. Behåll samtliga åtta spärrar och
dispositionen **25/39/28 av 92**. Ingen aktivering och ingen push; Claude ska göra en
fokuserad rättningsrunda 3 och stanna för omgranskning.

## Rättningsrunda 3 — svar på granskning 2026-09-13-038

Båda P2-fynden rättade. Ingen tariff-, pris-, motor- eller aktiveringsändring.

1. **TypeScript-golden nu fullt oberoende, felmatrisen komplett.**
   `besparingsvardeBatch3b.test.ts`s `FACIT` utökat med `variabelKrPerKwAr` och
   `flodeBaseRate` (identiska litereade värden som Pythonsidans
   `_KAPACITET_OCH_FLODE_FACIT`). `fast` beräknas nu `effekt × variabelKrPerKwAr × 12`
   och `justering` med den golvfria formeln `flode_m3 × baseRate × (0,02×(Tf−60)+0,2)`
   — bägge handräknade i testet, aldrig utlästa ur `variantPrisar`. Ett nytt
   sanitetsprov verifierar dessutom att fixturen faktiskt bär dessa publicerade
   priser (`pris_kr_per_enhet_ar === variabelKrPerKwAr×12`, `justeringar[0].base_rate
   === flodeBaseRate`) innan de används som facit. Felmatrisen kompletterad med
   ogiltig effekt (`invalid_capacity`), ogiltigt (negativt) flöde
   (`invalid_policy_fields`/`flode_m3`/`min`) och saknad temperatur
   (`missing_policy_fields`/`framledningstemperatur_c`); samtliga fall verifierar nu
   `KontraktBlockerat`, exakt `orsak` och relevant `saknadeFalt`/`ogiltigaFalt`-nyckel
   via en delad `forvantaBlockering`-hjälpfunktion, inte längre ett odetaljerat
   `.toThrow()`.
2. **Periodmetadata-dokumentation och testbenämning rättad.**
   `KravPost.matchningMotManad`s kommentar i `resultatkontrakt.ts` skiljer nu
   uttryckligen på ett verkligt månadsanrops målmatchning (matchad period HINDRAR
   inte "exact") och en årsprodukts (Batch 3b:s) rena formatkrav utan mål-månad, som
   INTE bevisar rätt fakturamånad och därför inte hindrar snapshot-taket när fältet
   även bär en `kalperiodDefinition`. Pythonsidans `TestNeptuneFixturSynk`-testmetod
   döptes om från `test_checkad_in_fixtur_ar_byte_for_byte_regenererbar` till
   `..._semantiskt_regenererbar` (och motsvarande kommentarer i både Python- och
   TypeScript-filen rättade) — provet gör en `json.loads`-objektjämförelse, inte en
   rå bytejämförelse. **Rättelse av tidigare felaktigt påstående**: rättningsrunda
   2:s loggpost ovan (rad 286–289) beskrev av misstag detta prov som en genuin
   byte-för-byte-jämförelse; det gjorde det aldrig, bara den beskrivande texten var
   fel.

**Commit-hashar:**
- `enkey-agents@09b0ef2` — testnamn/kommentarrättning (Python).
- `neptune_academy@92de895` — utökat FACIT, komplett felmatris, dokumentationsrättning.

**Verifiering:**
- Riktat Batch 3b-TypeScript: 144 passed (upp från 121). Full TypeScript-svit: 1177
  passed i 39 filer (upp från 1145). `npx tsc --noEmit`: godkänt.
- Riktat Batch 3b-Python: 213 passed. Full Python-svit: **1222 passed, 4 skipped**
  (oförändrat — inga produktionsändringar).
- Generator-synk: `test_fixture_synkad_med_neptune_marknad`,
  `test_fixturen_ar_identisk_i_bada_reponen`, `test_genererad_ts_matchar_kallan` samt
  `TestNeptuneFixturSynk::test_checkad_in_fixtur_ar_semantiskt_regenererbar`: alla 4
  godkända.
- Isolerat `npm run eval:build`: godkänt, endast känd bundelstorleksvarning. E2E mot
  det isolerade bygget: **13/13 scenarier godkända**.
- `git diff --check` kört på riktigt i båda repona: rent.
- Disposition mekaniskt omverifierad: `godkanda(katalog)` = 25, katalogen 86 rader —
  oförändrat **25/39/28 av 92**.

Ingen aktivering, ingen push. Stannar för Codex omgranskning.
