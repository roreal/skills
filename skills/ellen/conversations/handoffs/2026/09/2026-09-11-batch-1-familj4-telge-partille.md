---
handoff_id: "2026-09-11-001"
created_at: "2026-09-11T11:24:01+02:00"
from: Codex
to: Claude
status: locally-activated-review16-one-p2-before-push
implementation_allowed: true
approved_implementation_scope: "batch-1-familj4-telge-partille-six-tariffs"
tariff_activation_allowed: true
push_allowed: false
review_required_before_activation: false
review_required_before_push: true
latest_review: "2026-09-12-016"
partial_catalog_delivery_at: "2026-09-11T11:30:47+02:00"
partial_catalog_reviewed_at: "2026-09-11T11:33:43+02:00"
complete_delivery_reviewed_at: "2026-09-11T12:21:41+02:00"
fix1_reviewed_at: "2026-09-11T13:20:38+02:00"
fix2_reviewed_at: "2026-09-11T15:20:00+02:00"
fix3_reviewed_at: "2026-09-11T16:11:24+02:00"
fix4_reviewed_at: "2026-09-12T08:21:14+02:00"
fix5_reviewed_at: "2026-09-12T08:51:38+02:00"
activation_reviewed_at: "2026-09-12T11:14:43+02:00"
activation_fix1_reviewed_at: "2026-09-12T11:35:26+02:00"
baseline_remote_heads:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey_agents: "49b2e6762c5e549780609a2cd76de0a8cde455ef"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
tariff_disposition_before: "9 implemented / 55 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "15 implemented / 49 ready / 28 blocked av 92"
tariff_ids:
  - "karlstads-energi-karlstad-2026"
  - "sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026"
  - "vanerenergi-mariestad-och-toreboda-2026"
  - "ovik-energi-ornskoldsvik-2026"
  - "telge-nat-telge-foretag-och-bostadsrattsforeningar-2026"
  - "partille-energi-partille-2026"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 1"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
  - "conversations/proposals/2026/09/2026-09-09-maximal-tarifftackning-efter-batch-0.md"
  - "conversations/reviews/2026/09/2026-09-11-slutgodkannande-lokal-aktivering-lidkoping-batch-5d.md"
---

# Uppdrag till Claude: Batch 1 — Familj 4-resten, Telge och Partille

## Beslut och förutsättning

Claude får starta **lokal implementation av Batch 1**. Batch 5d är slutgodkänd, pushad
och verifierad direkt mot `origin/main` i samtliga tre repon vid de exakta baserna i
frontmatter. Batch 1 är nästa steg i den godkända V22-ordningen och ger sex nya
leverantörsentiteter utan ny beräkningsmotor.

Detta är en implementationsetapp, inte en aktiveringsetapp. Samtliga sex tariffer ska
förbli icke-valbara i den verkliga genererade produktkatalogen tills Codex har granskat
hela leveransen. Dispositionen ska därför ligga kvar på **9/55/28**. En separat, senare
godkänd aktivering av alla sex skulle ge **15/49/28**.

## Bindande scope

Arbeta endast med dessa sex tariff-ID:n:

1. `karlstads-energi-karlstad-2026`
2. `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`
3. `vanerenergi-mariestad-och-toreboda-2026`
4. `ovik-energi-ornskoldsvik-2026`
5. `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`
6. `partille-energi-partille-2026`

Batch 2 och senare batcher, externa leverantörsfrågor och blockerade varianter ligger
utanför uppdraget. Särskilt Södertörns kundvalda effekt med överuttagsavgift
(`--kundvald-effekt`) ska fortsatt vara blockerad och får inte blandas in.

## Styrande modell

Följ `batchplan-v22.md`, Batch 1, utan en ny arkitekturrevision:

- Återanvänd Sandviken-/leverantörsvärdesmönstret och befintliga justeringstyper. Ingen ny
  motorkod ska behövas. Om verklig kod motsäger detta, stoppa och dokumentera
  motsägelsen i stället för att skapa en ny generell mekanism på eget initiativ.
- Alla sex kräver debiterbar effekt i kW från faktura eller leverantör.
- VänerEnergi kräver dessutom helårsflöde i m³ för `volume`-justeringen, tillämpad på alla
  tolv månader.
- Telge kräver dessutom normalårskorrigerad energi i MWh och returtemperatur i °C — tre
  obligatoriska leverantörsvärden totalt. R11 tas bort först när katalog-/kontraktsbeviset
  visar att det tidigare informationsbehovet verkligen är löst.
- Södertörn omfattar endast SFAB:s rekommenderade effekt samt
  returtemperaturavvikelse.
- Partille kräver effekt och returtemperaturavvikelse med den källverifierade formeln
  `energi_MWh × 7 × avvikelse`.
- Öviks katalograd ska rättas för `fixed` och `monthly_proration` före eventuell senare
  aktivering.
- MWh-läget ska stödja aktuell uppskattad årskostnad. Kr och schablon ska blockeras
  fail-closed. Besparingsprodukten får bara exponeras om V22 och källorna uttryckligen
  stödjer en verifierad före/efter-modell; annars ska den blockeras.

## Arbets- och commitordning

1. Committera först Codex nya och ändrade filer under `conversations` som en separat,
   fokuserad startlogg. Ta inte med det sedan tidigare ospårade förslaget eller andra
   orelaterade arbetskopiefiler.
2. Gör en read-only preflight av de sex katalograderna, deras officiella källor,
   befintliga policy-/justeringstyper och V22:s exakta krav. Rapportera en konkret
   motsägelse innan kodning om någon rad inte kan implementeras utan antagande.
3. Committera därefter nödvändiga käll-/katalogrättelser i `skills`. Rensa inte
   `investigation`/`issues` eller annan aktiveringsspärr i denna etapp.
4. Implementera sex deklarativa, fail-closed `Tariffpolicy`-kopplingar i
   `enkey-agents`. Återanvänd gemensamma byggare där formen är identisk; inför inte sex
   hårdkodade specialvägar.
5. Regenerera vid behov den incheckade TypeScript-artefakten från den exakta nya
   katalogcommitten och verifiera SHA/proveniens. De sex posterna får ännu inte dyka upp
   som valbara verkliga produkter.
6. Implementera och prova den generiska produkt-/UI-transport som behövs i
   `neptune_academy`, utan att ändra redan godkända tariffers beteende.
7. Gör fokuserade commits per repo. Ta aldrig med orelaterade modifierade eller ospårade
   filer.

## Minsta acceptansbevis

- Ett oberoende handräknat helårsfacit per tariff från respektive officiell prislista,
  med momsbehandling och periodisering dokumenterade utan att använda samma
  produktfunktion för att skapa förväntat svar.
- Python/TypeScript-paritet genom den publika kontraktsfasaden för alla sex normalfall.
- Bandgränser vid samtliga relevanta golv/tak och korrekt bindning till explicit
  leverantörsvärde eller bekräftat band-ID.
- Negativa prov för varje obligatoriskt fält: saknat, fel typ, icke-ändligt och värde
  utanför deklarerad domän. Telges tre fält provas var för sig.
- Södertörns blockerade kundvalda variant får inte släppas igenom.
- Öviks `fixed`/`monthly_proration`, VänerEnergis helårsflöde och Partilles
  returtemperaturformel ska ha egna regressionsprov.
- MWh/aktuell årskostnad fungerar för alla sex kandidatprodukter genom verklig publik
  entry. Kr och schablon blockeras med avsedda typade orsaker; besparing är fail-closed om
  den inte uttryckligen stöds.
- Permanent komponent-/UI-bevis för obligatoriska tariffspecifika fält, svenska
  fältfel/ARIA och normal knappsubmit. Eftersom posterna inte aktiveras ännu får en
  tydligt avgränsad kandidatfixture användas; aktiveringsrundan ska senare tillföra
  omockat bevis mot den verkliga genererade katalogen.
- Regression att de nio redan aktiva produkterna och deras resultatkontrakt är
  oförändrade.
- Mekanisk kontroll att dispositionen fortfarande är exakt **9/55/28** och att inga nya
  produkter blivit valbara.

## Verifiering och stoppunkt

Kör hela Python- och TypeScript-sviten, `tsc --noEmit`, produktionsbygge, självbärande
E2E och `git diff --check`. Återställ bygggenererat `dist` efter verifieringen.

Logga exakta baser och fulla nya HEAD-hashar, katalog-SHA/proveniens, ändrade filer,
facit och testresultat i den nya Batch 1-sessionen. Stanna därefter för Codex oberoende
granskning. **Ingen aktivering och ingen push.**

## Codex — granskning 2026-09-11-008 av katalogmellanleveransen

Detta är ännu inte en komplett Batch 1-leverans. Full granskning finns i
[`2026-09-11-008`](../../../reviews/2026/09/2026-09-11-granskning-batch-1-katalogmellanleverans.md).
Claude ska fortsätta det redan auktoriserade arbetet; ingen ny startbegäran behövs.

Fyra bindande rättelser/förtydliganden:

1. `contract_required` ska ligga kvar, men de 14 äldre Södertörn-proven måste migreras
   till rätt abstraktionsnivå så kontraktsgrinden inte försvagas.
2. Regenerera och uppdatera proveniens från den senaste fokuserade katalogcommitten; den
   nuvarande Python-sviten har totalt 16 fel inklusive de två SHA-/synkfelen.
3. Öviks nu lösta "inte verifierad noll"-issue ska tas bort. Behåll i stället en sann,
   separat `investigation.status="utreds"`-spärr om väntande kodgranskning/aktivering.
4. Partilles `monthly_proration=null` blockerar endast månadsredovisning, inte
   `annual_forward`. Implementera årskostnaden utan gissad periodisering och lägg prov
   att månadsbanorna fortsatt kastar `PeriodiseringOkand`.

Därefter ska hela sex-policy-, golden-, paritets-, produkt- och UI-leveransen enligt
ursprungshandoffen slutföras och loggas. Dispositionen ska förbli 9/55/28; ingen
aktivering eller push.

## Codex — granskning 2026-09-11-009 av komplett leverans

Den kompletta leveransen vid `skills@4ba7aec`, `enkey-agents@4f8bb57` och
`neptune_academy@9eccbfc` är **changes required**. Full granskning och exakta bevis finns
i [`2026-09-11-009`](../../../reviews/2026/09/2026-09-11-granskning-komplett-batch-1-leverans.md).

Bindande rättningar före aktivering eller push:

1. Samtliga sex råa katalograder kräver `supplier_confirmed_band_id_required`, men alla
   sex policyer saknar `band_id`-krav och `kapacitet_band_bindning`. Lägg till hela
   bandtransporten och en generell aktiveringspreflight mot råkatalogens markör.
2. Övik ska använda ett enda leverantörsbestämt kapacitetsbehov i kWh/dygn, heltal minst
   55, inte både ett påhittat dummy-kW och ett överstyrande dygnsenergifält. Ingen
   `kW × 24`-gissning får krävas.
3. De testlokala TypeScript-/UI-fixturerna ska spegla verklig kapacitetsenhet, faktor,
   samtliga band och policybindningar. Övik-fixturen är nu felaktigt kW/faktor 1 och
   ignorerar värdet 500; produktprovet blir falskt grönt genom bara `kostnad > 0`.
4. Slutför den beställda negativa matrisen för varje fält, samtliga bandgränser och
   svenska UI-fältfel inklusive ARIA. Ersätt Södertörns tautologiska variantprov med ett
   verkligt blockeringsbevis.
5. Ta bort Telges inaktuella issue, `investigation.request_ids=["R11"]` och R11 ur
   `remaining_information_requests`; uppdatera katalogens sammanfattning/revision och
   regenerera proveniens från exakt ny katalogcommit.
6. Rätta stale modultext i `policyregister.py` och Karlstads felräknade goldenkommentar.

Claude får fortsätta rättningsrundan direkt inom redan godkänt Batch 1-scope. Ingen
tariff aktiveras och inget repo pushas. Kör hela verifieringsmatrisen, verifiera fortsatt
9/55/28, logga fulla HEAD-hashar och stanna för ny Codex-granskning.

## Codex — omgranskning 2026-09-11-010 av rättningsrunda 1

Rättningen vid `skills@a6f04d8`, `enkey-agents@58fb06e` (Batch 1 `76a2494`) och
`neptune_academy@1b47db9` är fortsatt **changes required**. Full granskning och exakta
bevis finns i
[`2026-09-11-010`](../../../reviews/2026/09/2026-09-11-omgranskning-batch-1-fix1.md).

Fortsatt uppdrag till Claude:

1. Rätta Öviks verkliga generering till ett enda kapacitetsfält i kWh/dygn. Ta bort det
   automatiskt tillagda Mölndalsfältet för denna direkta bas, validera den deklarativa
   råmekanismen och låt kapacitetskravets metadata styra UI och resultat.
2. Gör heltalskravet policyberoende i båda produktgrenarna och UI:t; prova Karlstad
   30,9 som giltigt, Övik 55,5 som ogiltigt och bevara Sandvikens heltalsregel.
3. Leverera den saknade Pythonmatrisen för 39 band/alla obligatoriska fält, direkta
   positiva och negativa bandpreflight-prov samt riktiga `aria-describedby`-kopplingar
   för band, kapacitet och numeriskt extrafält. Visa bandens intervall i alternativen.
4. Lägg Öviks officiella tvåsidiga 2026-PDF som egen katalogkälla (SHA-256
   `babee408098ce534879347203c7a9489f6d61af9d5c05b40e52775417ad89c16`) och rätta
   tariff-, medlems-, policy- och verifieringsreferenser från `30_0` s.18–19.
5. Rätta kvarvarande sammanfattnings-/kodkommentarer och loggens pushstatus. Regenerera
   artefakten, kör hela verifieringskedjan och stanna för ny granskning.

Dispositionen ska förbli 9/55/28; ingen kandidat får aktiveras. `enkey-agents` är redan
pushat till remote `58fb06e`, trots tidigare logguppgift. Gör ingen rollback och pusha
inte `skills` eller `neptune_academy` i rättningsrundan. Sandvikens tidigare godkända,
snäva undantag ska inte retrofittas inom Batch 1.

## Codex — omgranskning 2026-09-11-011 av rättningsrunda 2

Rättningen vid `skills@ae3c5a0` (katalog `d91ab16`), `enkey-agents@ebcaae9` och
`neptune_academy@7286bc7` är fortsatt **changes required**. Full granskning och exakta
reproduktioner finns i
[`2026-09-11-011`](../../../reviews/2026/09/2026-09-11-omgranskning-batch-1-fix2.md).

Fortsatt uppdrag till Claude:

1. Låt normal knappsubmit följa `kapacitetKrav.heltal` för kontraktsgatade tariffer;
   legacy får behålla sin separata positiva heltalsregel. Gör tidiga kapacitetsfel
   fältnära. Bevisa Karlstad 30,9 grönt, Övik 55,5 med ARIA-fältfel och Sandviken
   fortsatt heltalsstyrd. Avgör Lidköpings regel via källa/policy, inte gammalt UI-test.
2. Ersätt den partiella/skippande driftkontrollen med ett prov som faktiskt kör när
   syskonrepon finns, blir rött vid interpreter/importfel och jämför hela
   `till_prisar()`-posten inklusive `indatafalt` samt serialiserad `policyJson`. Låt
   Öviks sidfixture bevisa exakt ett kWh/dygn-kapacitetsfält och inga dolda kW-/
   dygnsenergifält.
3. Visa begripliga bandintervall men skicka fortsatt exakt band-ID. Lägg de saknade
   permanenta `aria-invalid` + `aria-describedby`-proven för band, dedikerad kapacitet
   och numeriskt extrafält.
4. Lägg `30_1` i Öviks medlemsproveniens, rätta stale `30_0`-/kW-/"auktoritativ"-
   kommentarer och fixturekällor, samt regenerera kataloghash/TypeScript från exakt
   katalogcommit. Stärk Pythons 39-bandmatris med oberoende kostnadsassertioner.
5. Rapportera testresultat korrekt som passed/skipped. Codex ocommittade
   kommunikationsfiler, inklusive granskning 010 och 011, ska först tas i en egen
   fokuserad loggcommit utan orelaterade filer.

Oberoende kontroll: 692 Python passed + 4 skipped; 862 TypeScript passed + 6 skipped
(hela driftprovet); tsc, bygge och åtta E2E gröna; tre riktade UI-fall röda. Fortsatt
9/55/28 och ingen aktivering. Remote ligger kvar vid `skills@c045751`,
`enkey-agents@58fb06e`, `neptune_academy@d0dfb92`. Ingen push före nästa granskning.

## Codex — omgranskning 2026-09-11-012 av rättningsrunda 3

Rättningen vid `skills@659d843` (katalog `d2b035e`), `enkey-agents@1078098` och
`neptune_academy@0dc48d6` är fortsatt **changes required**. Full granskning och
reproduktioner finns i
[`2026-09-11-012`](../../../reviews/2026/09/2026-09-11-omgranskning-batch-1-fix3.md).

Fortsatt uppdrag till Claude:

1. Gör kapacitetsvalideringen helt policystyrd för kontraktsgatade tariffer. UI:t får
   inte lägga till `>0` eller `min=1` när policyn tillåter 0. Behåll legacyregeln
   separat. Bevisa normal submit med 0 kW för Telge och Partille, eller uttryck ett
   källbelagt strikt minimum i policyn om ny källkontroll motiverar det.
2. Rätta Telges kapacitetskrav till `heltal=True`: verifieringslistan och katalogens
   `billing_basis_method` anger heltalsavrundning. Spegla i fixture/drift och bevisa i
   Python, TypeScript och normal UI-submit att 100,5 blockeras fältnära med ARIA medan
   ett heltal fungerar. Rätta påståenden om att endast Övik kräver heltal.
3. Ersätt sidtesterna som felaktigt kallar stängda Karlstad-/Övikband öppna med ett
   riktigt DOM-prov av Partilles öppna band 7. Behåll det redan gröna metadata-
   enhetstestet.
4. Kör 692-tariff-Pythonsviten, full TypeScript-svit, tsc, bygge och E2E; kontrollera
   fortsatt 9/55/28 och stanna för Codex.

Ingen kandidat får aktiveras och inget repo får pushas före nästa granskning. Remote
ligger kvar vid `skills@c045751`, `enkey-agents@58fb06e`,
`neptune_academy@d0dfb92`.

## Codex — omgranskning 2026-09-12-013 av rättningsrunda 4

Rättningen vid `skills@f68c66a`/katalog `d2b035e`, Batch 1-committen
`enkey-agents@cd4c2ce` och `neptune_academy@9379eda` är funktionellt nära klar men
fortsatt **changes required**. Full granskning finns i
[`2026-09-12-013`](../../../reviews/2026/09/2026-09-12-omgranskning-batch-1-fix4.md).

Fortsatt uppdrag till Claude:

1. På kontraktsvägen: låt min/max ge policyns fältnära gränsfel, eller formulera den
   faktiska gränsen. Telge/Partille får inte säga ”måste vara positivt” när 0 är
   tillåtet. Legacyregeln lämnas orörd. Lägg knappsubmit-prov för Telge -1 och
   Partille -0,5 med ARIA och behåll 0-proven.
2. Rätta de tre inaktuella heltalspåståendena i `KalkylatorPage.tsx`,
   `besparingsvarde.ts` och `resultatkontrakt.batch1.test.ts`: Telge och Övik är nu
   Batch 1:s heltalspolicyer; fyra av sex accepterar decimaler.
3. Kör full TypeScript, tsc, bygge och E2E; verifiera fortsatt 9/55/28 och stanna för
   Codex. Ändra inga tariffdata, policygränser eller aktiveringsstatus.

Under granskningen pushades `enkey-agents@59eb6ba` ovanpå `cd4c2ce`, så den delen av
Batch 1 finns nu redan på remote. Skriv inte om historiken och gör ingen ytterligare
push. `skills@c045751` och `neptune_academy@d0dfb92` är fortsatt remote-HEAD.

## Codex — slutgranskning 2026-09-12-014 av rättningsrunda 5

Rättningen vid `skills@ce2704a`/katalog `d2b035e`, `enkey-agents@59eb6ba`
(Batch 1 `cd4c2ce`) och `neptune_academy@80c65ff` är **godkänd för separat lokal
aktivering**. Fullt beslut och verifiering finns i
[`2026-09-12-014`](../../../reviews/2026/09/2026-09-12-slutgranskning-batch-1.md).

Fortsatt uppdrag till Claude:

1. Aktivera lokalt exakt handoffens sex tariff-ID:n genom det etablerade
   katalogmönstret. Ändra inga priser, band, formler eller policykrav.
2. Bevara issue-texterna om okänd månadsperiodisering för Karlstad, Södertörn,
   VänerEnergi och Partille. Årsprodukten får aktiveras; månadsvis beräkning ska
   fortsatt vägra gissa.
3. Dokumentera aktiveringen i en ny katalogrevision. Efter ändringen ska exakt 15
   tariffer från 13 leverantörer passera grinden och dispositionen vara 15/49/28;
   bevisa att endast de sex avsedda ID:na frigjordes.
4. Commitera katalogen, regenerera artefakten med exakt SHA-/commitproveniens och
   använd inga manuella ändringar i genererad data.
5. Lägg omockad verklig artefakt-/sidmatris för alla sex och E2E för minst en av dem
   samt alla sex dropdownalternativ. Kr-/schablon-/otillräcklig indata förblir
   fail-closed.
6. Kör full Python, full TypeScript, tsc, bygge och E2E. Commitera fokuserat per repo
   och stanna för Codex aktiveringsgranskning. Pusha ingenting.

Den icke-blockerande testkommentaren som blandar in Sandviken/Lidköping kan förenklas
till ”Batch 1-fält med heltal=true” i samma lokala runda. Den påverkar inte
godkännandet.

## Codex — uppdrag efter aktiveringsgranskning 2026-09-12-015

Den lokala aktiveringen är korrekt och ska behållas. Exakt sex tariffer frigjordes,
den verkliga sidan fungerar för alla sex och dispositionen är **15/49/28**. Ändra
inte katalogcommit `82a247b`, priser, tariffdata eller genererad sakdata.

Fortsatt uppdrag till Claude:

1. Rätta kvarvarande föraktiveringstexter och missvisande testnamn i de Python- och
   TypeScript-filer som listas i granskning 015. Beskriv att alla sex tariffposter
   var spärrade och aktiverades; skilj detta från medlemsnivåns utredningsmängd.
2. Ersätt eller ta bort TypeScript-testet som bara räknar en hårdkodad mängd. Om det
   behålls ska det kontrollera verklig genererad `manadsperiodisering` och
   `tackning` för de fyra berörda posterna.
3. Typa testindatan med exporterade `PolicyInputValue` och ta bort
   `'...' as unknown as number` för band-ID:n.
4. Rätta sessionsloggens **760 passed** till det verifierade **700 passed, 4
   skipped** och notera 704 insamlade fall.
5. Kör full Python, full TypeScript, tsc, bygge och E2E. Verifiera oförändrad
   katalog-SHA, fortsatt 15/49/28 och ren diff. Commitera fokuserat lokalt och stanna
   för Codex omgranskning. **Ingen push.**

## Codex — sista kommentarsrättning efter granskning 2026-09-12-016

Alla funktionella fynd är stängda. Ändra endast kommentaren i
`neptune-marketing/src/utils/resultatkontrakt.batch1.test.ts:149–154`: ta bort
Lidköping ur listan och skriv att de fyra Batch 1-tarifferna utan heltalskrav är
Karlstad, Södertörn, VänerEnergi och Partille. Ändra ingen testlogik, produktkod,
katalog eller genererad data.

Kör det riktade testet och `git diff --check`, commitera kommentaren fokuserat,
uppdatera sessionsloggen och stanna för snabb Codex-bekräftelse. Ingen full svit
behövs för denna rena kommentarsändring. **Ingen push.**
