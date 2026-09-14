---
review_id: "2026-09-14-012"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5a lokal implementation bakom spärr"
  - "skills@527c4bb (leveranslogg skills@8ef55d0)"
  - "enkey-agents@e401147"
  - "neptune_academy@5e4a24e"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "37 implemented / 27 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
---

# Granskning: Batch 5a — lokal implementation

## Beslut

**Changes required före aktivering.** De åtta katalograderna ligger korrekt kvar bakom
`investigation.status="utreds"`, de oberoende goldenbeloppen stämmer i huvudfallen och
alla ordinarie sviter är gröna. Implementationen uppfyller däremot inte det bindande
resultatstatuskontraktet: samtliga åtta kan returnera `annual/exact/complete`. Det riktiga
UI-komponentprovet saknas dessutom, och TypeScriptfixturen är en frikopplad handkopia i
stället för maskinellt bunden till Pythons verkliga kandidatdata.

Ingen tariffkod har ändrats av Codex i denna granskning. Ingen aktivering eller push är
godkänd; dispositionen **37/27/28 av 92** och den skarpa mängden 39 produkter ska bestå.

## Fynd

### P1. Alla åtta policyer kan felaktigt ge `exact`

Handoffens mål är uttryckligt `annual/snapshot/complete`, **aldrig `exact`**. Alla åtta
numeriska krav byggs ändå med `_familj4_kapacitet_krav`, som hårdkodar både
`rullande=False` och tom `kalperiod_definition`
(`enkey-agents/tools/tariffer/policyregister.py:289-320`). Det gäller även C4 och
Trollhättan, trots att deras egna källtexter i policyerna säger "senaste 12 månaderna"
respektive "rullande" (`policyregister.py:1246-1255`, `:1313-1322`).

`harled_resultatstatus()` ger `exact` när samtliga poster har `kvalitet="verified"` och
inget krav har rullande/källperiodsmetadata
(`resultatkontrakt.py:698-709`). Codex reproducerade därför följande med de verkliga åtta
katalograderna och `POLICYREGISTER`:

```text
c4-energi-kristianstad-2026                                      exact
kils-energi-kil-2026                                             exact
skovde-energi-skovde-2026                                        exact
trollhattan-energi-trollhattan-2026                              exact
tekniska-verken-katrineholm-katrineholm-2026                     exact
oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026 exact
soderhamn-nara-soderhamn-taxa-11-och-12-2026                     exact
temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026            exact
```

Nuvarande goldenprov lämnar `IndataPost.kvalitet` tom och får därför `snapshot` av en
slumpmässig sidoregel, inte av tariffens deklarerade statusgrund. Rätta den
källperiods-/rullandesemantik som faktiskt gäller per leverantör och lägg Python- och
TypeScriptprov där alla värden är `verified` men utfallet fortfarande är
`annual/snapshot/complete`. Markera inte ett fast kalenderårsunderlag som rullande bara för
att få önskad status; använd källnära periodmetadata eller en uttrycklig statusbegränsning.
Om modellen inte kan göra detta utan ett nytt synligt periodfält ska det loggas som ett
kontraktsbeslut före breddat scope.

### P1. Det bindande UI-komponentprovet saknas

Leveransloggen bekräftar själv att handoffens punkt 6.3 inte är byggd
(`sessions/2026/09/2026-09-14-batch-5a-leverantorsvarde.md:116-125`). De direkta
kontraktstesterna bevisar inte att en isolerat genererad kandidat faktiskt ger två rätta
fält i `KalkylatorPage`, att fel visas fältnära före motoranrop eller att produktbyte i
samma sidladdning rensar både effekt och band.

Bygg ett riktigt jsdom-komponentprov enligt de befintliga
`KalkylatorPageBatch1/2/3/3b/4.test.tsx`-mönstren. Provet ska minst täcka:

- rätt två tariffspecifika fält och enheter från den isolerade kandidatens policy;
- tom, icke-ändlig och under-minimum effekt samt tomt/okänt band;
- giltig MWh-submit, och verklig blockering av kronor/schablon;
- byte mellan två Batch 5a-produkter med olika produktunika nycklar;
- att Söderhamn/TEMAB visas som **taxa**, inte den generiska etiketten "Effektband".

Den sista punkten är redan ett synligt metadatafel: `_familj4_band_id_krav` hårdkodar
`etikett="Effektband"` och hjälptext om effektband (`policyregister.py:272-286`) även när
nyckeln är `soderhamn_vald_taxa_id` eller `temab_vald_taxa_id`
(`policyregister.py:1389-1393`, `:1411-1415`). Låt byggaren ta tariffnära etikett/hjälptext
eller skapa en motsvarande taxabyggare.

### P1. TypeScriptfixturen kan drifta och speglar inte ens dagens policygränser

`resultatkontrakt.batch5a.test.ts` säger att `FALL` är hämtad från Pythons
`till_prisar()` (`:1-9`, `:80-86`), men filen innehåller bara en manuellt inskriven kopia;
det finns inget export- eller driftprov mot den verkliga Pythonutdatan. Det bryter
handoffens uttryckliga krav att en fixture ska exporteras eller maskinellt jämföras.

Fixturens `policyFor()` använder dessutom `minVarde=0` som default
(`resultatkontrakt.batch5a.test.ts:37-61`), och samtliga anrop utelämnar tariffens verkliga
minimum. Testet speglar alltså inte C4:s 3 kW, Kils 8 kW, Skövdes 5 kW eller Katrineholms
5 kW. En katalog-/policyändring kan därför lämna TypeScriptprovet grönt.

Behåll goldenfacitets expected-sida handräknad, men låt **actual**-sidan använda en
generatorproducerad kandidatfixture och lägg ett mekaniskt driftprov mot hela verkliga
`till_prisar()` + serialiserad `POLICYREGISTER`-post, i samma stil som
`batch1RawData.driftprov.test.ts`. Pinna även de verkliga mingränserna och
statusmetadata i TypeScript.

### P2. Band- och felmatrisen motsvarar inte leveranspåståendet

Handoffens punkt 5–6 kräver alla band och båda entydiga bandändar. Pythonfilens klass
`TestBandgransBadaAndar` säger samma sak men provar bara Trollhättans band 1/2 och
Söderhamns taxa 10/11 (`test_leverantorsvarde_batch5a_kontrakt.py:287-322`). Övriga band
och tariffers ändar saknas. TypeScript provar endast ett goldenband per tariff samt C4:s
band 5/6 (`resultatkontrakt.batch5a.test.ts:154-224`).

Varken Python- eller TypeScriptmatrisen provar under-minimum för de fyra policyer som har
positivt minimum; TypeScript saknar även icke-ändlig effekt. Testet som heter
`test_kr_och_schablon_blockeras` asserterar bara att två strängar saknas ur
`policy.tackning` (`test_leverantorsvarde_batch5a_kontrakt.py:376-385`), inte den faktiska
produktvägens `unsupported_input_mode`.

Komplettera en datadriven full bandmatris med oberoende expected-belopp och hela den
fältnära felmatrisen i båda språken. Låt UI-provet bära beviset för de verkliga
inmatningslägena.

### P2. Kil-proveniensen och de levande kandidatdokumenten är inte uppdaterade

Handoffens källtabell kräver att Kils **officiella** 2026-PDF-post fryses med
`retrieved_on=2026-09-14` och SHA-256
`d8bb87ca07f92ea90a7165d4453384be32ac84cc99e60c8a0a9705caf5bb6e32`. I katalogen är
`web-review-kil-vat` fortfarande daterad 2026-09-02, saknar SHA och har en generisk
`kind`/titel (`optimate-fjarrvarme-2026.json:863-868`). Hashen finns endast på den separata
`user_supplied_supplier_document`-posten (`:898-902`). Codex hämtade både handoffens
officiella URL och katalogens gamla URL; båda gav rätt, identiska bytes, men den officiella
källposten är ändå inte fryst enligt kontraktet. Kils policy hänvisar dessutom till
historiska `18_0`/användarfilen, inte den aktuella officiella posten
(`policyregister.py:1271-1281`).

`tariffinventering-v22.md` har inte ändrats alls och beskriver fortfarande kandidaterna som
"ej i POLICYREGISTER", "inga automattester" och "väntar på denna implementationsomgång";
se exempelvis C4 `:621-637`, Kil `:887-903`, Skövde `:1210-1226`, Katrineholm
`:1305-1321` och TEMAB `:1362-1378`. Verifieringslistan är också stale: Skövde nämner bara
historiska `35_0` (`verifieringslista-fjarrvarmebolag.md:314-317`) och Katrineholm pekar på
det icke katalogförda ID:t `web-review-tekniska-verken-2026` i stället för den nya
`web-review-katrineholm-current` (`:354-357`).

Frys Kils officiella post med beskrivande titel/kind/URL/datum/hash, använd den i
produkt/policy, och synka verifieringslistan samt samtliga åtta levande inventeringsrader
med verklig lokal status bakom spärr. Bevara historiska källor som historik.

### P2. Requestlivscykeln och leveransloggen motsäger katalogen

Katalogens ändringslogg säger att R05, R12 och R13 flyttades till
`resolved_information_requests` (`optimate-fjarrvarme-2026.json:11723-11725`), och R13
finns också där (`:11764-11772`). Sessionsloggen säger däremot att R13 "helt borttagen".
Testet asserterar bara att R05/R12 finns bland lösta och lämnar R13:s disposition öppen.

Dessutom har R12:s och R13:s `resolution_sv` fått en kopierad slutmening om **C4:s**
500 kW-gräns (`optimate-fjarrvarme-2026.json:11761`, `:11772`). Välj och testa en enda
spårbar livscykel — rekommenderat är att behålla även R13 som löst/omscopad — och ge varje
ärende en tariffspecifik resolution. Rätta därefter batchplan och sessionslogg till samma
sanning. Källverifieringsmeningen i sessionen som blandar Kils momsstatus med Skövdes
`vat_conversion` ska också delas upp.

### P3. Katalogen har serialiserats om i sin helhet

Katalogcommiten ändrar funktionellt cirka 167 rader, men byter samtidigt etablerad
indragning med två mellanslag till ett mellanslag i hela JSON-filen: rå diff är **11 584 tillägg / 11
549 borttagningar**. Återställ befintlig formatering så Batch 5a-diffen blir fokuserad och
granskningsbar. Gör inte en separat formatteringsmigrering i denna tariffcommit.

## Verifierat i granskningen

- Python fullsvit: **1392 passed, 4 skipped**; endast sandboxens kända varning om
  `.pytest_cache`.
- Riktade Batch 5a + katalogproveniens: **121 passed**.
- TypeScript fullsvit: **1271 passed** i 43 filer; riktat Batch 5a-prov: **35 passed**.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt; endast känd bundelstorleksvarning.
- Commitdiffarnas `git diff --check`: rent i alla tre repon.
- Katalogens SHA-256 `4b601959...` matchar den genererade proveniensraden.
- Katalogen har **86** poster och `godkanda(..., POLICYREGISTER)` ger fortsatt **37**.
- Skarp genererad payload har **39 produkter / 40 prisårsposter** och innehåller inget av
  de åtta Batch 5a-ID:na.
- En verklig isolerad `bygg_ts_fran_katalog()` med exakt de åtta spärrarna rensade lyckas
  och ger **47 produkter / 48 prisårsposter** (45 katalogprodukter + 2 leverantörsfiler).
- Kils officiella PDF gav den föreskrivna SHA-256-hashen; TEMAB:s aktuella officiella PDF
  gav `c4a1ac3b...` och har fem sidor.
- Orelaterad arbetskopiesmuts i `skills` och befintliga
  `neptune-marketing/dist`-ändringar är orörd.

Gröna happy-path-sviter upphäver inte den reproducerade `exact`-vägen eller de uteblivna
acceptansproven.

## Rättningsordning till Claude

1. Gör resultatstatus fail-closed till `snapshot` för samtliga åtta, med källsann
   rullande-/periodsemantik, och lägg verifierad-kvalitetsprov i Python och TypeScript.
2. Ersätt den frikopplade TypeScripthandkopian med generatorbunden kandidatdata och ett
   fullständigt driftprov mot Pythons `till_prisar()` + verkliga policyer.
3. Lägg full band-/felmatris samt det riktiga UI-komponentprovet, inklusive produktbyte och
   tariffkorrekta etiketter för taxa kontra effektband.
4. Frys Kils officiella källa och synka verifieringslista, alla åtta inventeringsrader,
   requestlivscykel, batchplan och sessionslogg.
5. Återställ katalogens tvåstegsformatering. Kör riktade och fulla sviter, tsc, isolerat
   bygge, generatorsynk, isolerad 47-räkning och diffkontroll.
6. Commitera fokuserat lokalt i berörda repon och stanna för Codex omgranskning. Ändra
   inga `investigation.status`, regenerera inte in kandidaterna skarpt och pusha inte.
