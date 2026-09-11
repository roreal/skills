---
handoff_id: "2026-09-11-001"
created_at: "2026-09-11T11:24:01+02:00"
from: Codex
to: Claude
status: partial-delivery-changes-required
implementation_allowed: true
approved_implementation_scope: "batch-1-familj4-telge-partille-six-tariffs"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
latest_review: "2026-09-11-008"
partial_catalog_delivery_at: "2026-09-11T11:30:47+02:00"
partial_catalog_reviewed_at: "2026-09-11T11:33:43+02:00"
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
