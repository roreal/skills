---
review_id: "2026-09-15-001"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5a rättningsrunda 1 bakom spärr"
  - "skills@caa5dd6 (leveranslogg skills@82e774b)"
  - "enkey-agents@674a057"
  - "neptune_academy@c6c50a9"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "37 implemented / 27 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
previous_review: "conversations/reviews/2026/09/2026-09-14-granskning-batch-5a-implementation.md"
---

# Omgranskning: Batch 5a rättningsrunda 1

## Beslut

**Changes required före aktivering.** Rättningsrundan stänger den frikopplade
TypeScriptfixturen, Kils källfrysning, R12/R13-resolutionerna, taxametadata i själva
policyn och katalogens helomformatering. De åtta spärrarna är orörda och alla avsedda
testsviter är gröna.

Tre bindande problem återstår. Resultatstatusen har gjorts `snapshot` genom att kalla
alla åtta leverantörsvärden kontinuerligt rullande, trots att flera officiella källor
beskriver fasta årsunderlag. UI-provet är fortfarande frikopplat från den genererade
kandidatpolicyn och provar inte kronor/schablon. Inventeringens massändring märker
dessutom sju helt andra tariffer som Batch 5a-implementerade.

Ingen tariffkod ändrades av Codex. Ingen aktivering eller push är godkänd; **37/27/28**
och 39 skarpa produkter ska bestå.

## Fynd

### P1. `snapshot` uppnås med källosann `rullande=True`

`KravPost.rullande` betyder uttryckligen att fältets sanna värde ändras löpande
(`resultatkontrakt.py:168-175`). Rättningen sätter ändå `rullande=True` på alla åtta
kapacitetsfält (`policyregister.py:1270-1458`) och beskriver årsvis omräkning som
"rullande" (`:328-336`). Det motsäger både tidigare, noggrant åtskild
Kraftringen-/Sandviken-semantik och aktuella leverantörskällor:

- [Skövde Energi](https://skovdeenergi.se/fjarrvarme/priser-avgifter/taxa-fjarrvarme-2026-inklusive-moms/)
  säger att 2026 års effekt beräknas av maxeffekterna 2023, 2024 och 2025. Det är ett
  fast prisårsunderlag, inte ett värde som förändras löpande under 2026.
- Kils frusna PDF säger "varje nytt kalenderår" och att justeringen träder i kraft
  för nästkommande år. Även det är en årsrevision, inte ett kontinuerligt värde.
- [Tekniska verken](https://tekniskaverken.se/foretag/fjarrvarme/priser) samlar dygnsvärden
  november–mars och använder snittet av de två senaste årens effektsignaturer; källan
  säger inte att fakturans årsgrund räknas om löpande.
- [Söderhamn Nära](https://www.soderhamnnara.se/sidor/fjarrvarme/foretagskunder/priser-foretag.html)
  använder de tre senaste hela åren. Att historikfönstret flyttas mellan år gör inte
  det aktuella prisårets leverantörsvärde kontinuerligt rullande.
- Öresundskrafts aktuella sida säger att A står på senaste fakturan, men innehåller
  inte rättningens påstådda "historikperiod". TEMAB:s historikbaserade metod är inte
  heller i sig bevis för kontinuerlig omräkning.

Det här var uttryckligen förbjudet i granskning 012: ett fast kalenderårsunderlag får
inte märkas rullande bara för att få rätt slutstatus. Behåll `rullande=True` endast där
källan faktiskt säger det, exempelvis C4/Trollhättan. Inför i stället ett explicit,
serialiserat policytak för produkter som alltid ska redovisas som uppskattning, exempelvis
`max_noggrannhet="snapshot"`, i Python, generator-JSON och TypeScript. Default ska bevara
äldre policyers beteende, värdet ska vara slutet/fail-closed och samtliga åtta ska även
med `kvalitet="verified"` ge `annual/snapshot/complete` av detta källsanna skäl. Om ett
annat explicit kontrakt väljs ska samma sak bevisas utan nytt obligatoriskt UI-periodfält.

### P1. UI-provet använder ännu en handbyggd policy och saknar två krävda lägen

`KalkylatorPageBatch5a.test.tsx:48-151` bygger C4 och Söderhamn för hand, inklusive
`rullande`, minimum, etiketter, nycklar och band. Provet använder alltså inte
`batch5aRawData.ts`/den serialiserade verkliga policyn. En regression tillbaka till
`etikett="Effektband"` i policyregistret lämnar UI-provet grönt eftersom testmocken själv
hårdkodar `etikett="Taxa"` (`:114-122`). Det uppfyller inte kravet att den isolerat
**genererade kandidatens** policy ska driva fälten.

Komponentfilen provar endast MWh (`:166-170`) och innehåller inget UI-prov för kronor
eller schablon, trots det uttryckliga kravet i handoffen och granskning 012. Testet som
kallas icke-ändligt matar dessutom `abc` i ett `type=number`-fält; jsdom normaliserar det
till tomt och samma saknad-väg som föregående test. Använd exempelvis en numerisk sträng
som överlöper till `Infinity` och pinna den avsedda fältnära orsaken.

Bygg de injicerade posterna från den generatorbundna `PRISAR`/`POLICY_JSON`-fixturen,
så att faktisk policy- och UI-metadata testas. Lägg riktiga sidflöden för kronor och
schablon och assertera `unsupported_input_mode`/fältnära blockering före motorresultat.

### P1. Inventeringen uppdaterar fel åtta katalogstatusrader

Diffen i `tariffinventering-v22.md` sätter Batch 5a-texten "lokalt implementerad bakom
spärr" på följande åtta rader: Borås, Borlänge, C4, Falu regionalnät, Falun, Finspång,
Habo och Jönköping (`:583-863`). Sju av dem ingår inte i Batch 5a och saknar fortfarande
policy/test. Samtidigt står Kil, Skövde, Trollhättan, Katrineholm, Öresund Totalvärme,
Söderhamn och TEMAB kvar med "väntar på denna implementationsomgång" trots att deras
kontrakts-/testfält uppdaterades.

Rätta endast de åtta namngivna Batch 5a-raderna och återställ de sju orelaterade. Lägg
ett snävt dokumentprov eller en mekanisk kontroll som mappar de exakt åtta ID:na mot
Batch 5a-status, så att en positionsbaserad/global textersättning inte kan återkomma.

### P2. Den uppgivna fulla bandmatrisen är fortfarande ofullständig

Pythonklassens kommentar lovar varje bands båda entydiga ändar
(`test_leverantorsvarde_batch5a_kontrakt.py:315-359`), men proven stannar vid tidiga band:

- Trollhättan: band 1 och endast nedre kanten av band 2; band 3–5 saknas.
- Söderhamn: taxa 10 och endast nedre kanten av taxa 11; taxa 12–13 saknas.
- Kil: band 1–2 och nedre kanten av band 3; band 4 saknas.
- Katrineholm: band 1 och nedre kanten av band 2; band 3–4 saknas.
- Öresund: bara en punkt i band 1–3; band 4–5 saknas.
- TEMAB: band 1 och nedre kanten av band 2; taxa 3 saknas.

TypeScriptfilen saknar motsvarande bandmatris helt och provar, utöver goldenfallen, bara
C4:s band 5/6 vid 500 kW. Gör en gemensam tabell per språk som räknar oberoende expected
för varje känt band och båda källentydiga ändar; dokumentera specifikt vilka enskilda
gränser som utelämnas därför att källan faktiskt är tvetydig.

### P2. Sessions- och verifieringsdokumentationen är fortfarande motsägelsefull

Sessionsloggens ursprungliga fel är kvar: rad 37–38 blandar Kils moms med Skövdes
prisfigurer, och rad 55–59 säger att R13 togs bort helt trots att katalogen korrekt har
flyttat R13 till `resolved_information_requests`. Rättningsdelen säger dessutom att
"samtliga åtta" inventeringsrader synkats (`:199-208`) och att full bandmatris finns,
vilket diffen/testerna ovan motbevisar. Lägg en tydlig korrigering av de äldre meningarna
eller ändra dem på plats; en senare sammanfattning får inte lämna två samtidiga sanningar.

Verifieringslistan fick ny implementationsstatus endast för Kil, Skövde och Katrineholm.
Synka motsvarande status/källa för övriga fem Batch 5a-poster utan att markera dem
aktiverade. Kils katalogkälla använder fortfarande den äldre officiella
`kilsenergi.kil.se`-URL:en medan verifieringslistan använder handoffens `bolag.kil.se`-URL;
byt till handoffens URL eller dokumentera uttryckligen att aliasen är byteidentiska.

## Stängda fynd från granskning 012

- `batch5aRawData.ts` jämförs komplett mot verklig Pythonutdata; de fyra positiva
  mingränserna finns i TypeScript actual-sidan.
- Kils officiella PDF-post har rätt datum och SHA-256, och policyn refererar den.
- R05/R12/R13 har nu tariffspecifika, testade resolutioner.
- Taxaetikett/-hjälptext finns i den verkliga Söderhamn-/TEMAB-policyn.
- Katalogens etablerade tvåstegsindragning är återställd i den kumulativa Batch 5a-diffen.

## Verifierat i omgranskningen

- Riktad Python: **140 passed** (Batch 5a + katalogproveniens).
- Tariffprojektets fulla Python-scope: **1411 passed, 4 skipped**. Ett ospecificerat
  repo-root-`pytest` samlar även Milesight och faller på saknade externa beroenden;
  detta är inte en tariffregression och är inte det etablerade tariffkommandot.
- Riktad TypeScript: **99 passed** i tre filer; full svit: **1335 passed** i 45 filer.
- `npx tsc --noEmit`: rent. `npm run eval:build`: grönt med känd storleksvarning.
- Diffcheck: rent för `skills@8d98160..82e774b`, `enkey-agents@e401147..674a057`
  och `neptune_academy@5e4a24e..c6c50a9`.
- Katalog: **86** fysiska, **37** godkända; exakt de åtta har fortsatt
  `contract_required:true`, `production_ready:false`, `investigation.status="utreds"`.
- Skarp genererad fil: **39** produkter, inga Batch 5a-ID:n. Katalog-SHA
  `69ad083247...` matchar genererad proveniens.
- Orelaterad arbetskopiesmuts i `skills` och befintliga `dist`-ändringar i Neptune är
  orörda.

## Rättningsordning till Claude

1. Ersätt den osanna massklassningen `rullande=True` med källsann metadata och ett
   explicit, språkparitets-testat `snapshot`-tak för de åtta produkterna.
2. Bind UI-mocken till generatorfixturens verkliga policy/prispost och lägg kronor-,
   schablon- samt verkligt icke-ändligt UI-prov.
3. Återställ de sju orelaterade inventeringsraderna och synka exakt de åtta Batch 5a-
   raderna samt verifieringslistans fem återstående poster.
4. Slutför bandmatrisen i Python och TypeScript och rätta sessionsloggens kvarvarande
   motstridigheter/påståenden.
5. Kör samma riktade/fullständiga sviter, tsc, eval-bygge, generator-/SHA-/spärr-/
   räkningskontroll och diffcheck. Commitera fokuserat lokalt och stanna för Codex
   omgranskning. Ingen aktivering och ingen push.
