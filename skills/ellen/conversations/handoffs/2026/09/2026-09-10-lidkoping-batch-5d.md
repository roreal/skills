---
handoff_id: "2026-09-10-001"
created_at: "2026-09-10T15:08:01+02:00"
from: "Codex"
to: "Claude"
status: fix-round-1-delivered-awaiting-review
implementation_allowed: true
approved_implementation_scope: "batch-5d-lidkoping-local-implementation-only"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
latest_review: "2026-09-10-009"
fix_round_1_delivered_at: "2026-09-10T17:51:55+02:00"
baseline:
  skills_local: "f1d4d1d"
  enkey_agents: "fbacd83"
  neptune_academy: "c4e1a26"
tariff_ids:
  - "lidkoping-energi-lidkoping-041-kw-2026"
  - "lidkoping-energi-lidkoping-42-kw-2026"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5d"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §4.2 och §6a.7"
  - "conversations/reviews/2026/09/2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md"
  - "conversations/reviews/2026/09/2026-09-10-slutgodkannande-batch-0.md"
  - "conversations/proposals/2026/09/2026-09-09-maximal-tarifftackning-efter-batch-0.md"
---

# Nästa uppdrag till Claude: lokal implementation av Lidköping Batch 5d

## Beslut och mål

Batch 0 är slutgodkänd och pushad i produktrepona. Nästa separat avgränsade steg är
**Batch 5d** enligt den godkända V22-planen: gör de två källgodkända
Lidköpingstarifferna tekniskt färdiga för en senare aktiveringskontroll.

Implementera lokalt och stanna därefter för Codex kod-, käll- och UI-granskning. Denna
runda tillåter nödvändiga katalog-, policy-, motor-, produkt-, UI-, generator- och
teständringar för exakt de två angivna tariff-ID:na. Den tillåter **inte** att tarifferna
görs produktionsvalbara, att deras disposition flyttas till implementerad eller att något
repo pushas.

## Bindande avgränsning

1. Följ den redan godkända specifikationen i `batchplan-v22.md` Batch 5d och
   `tariffinventering-v22.md` §6a.7. Starta inte en ny arkitekturrevision och skapa inte
   V23 om inte en konkret motsägelse mot den nu pushade koden gör planen omöjlig.
2. Arbeta endast med:
   - `lidkoping-energi-lidkoping-041-kw-2026`
   - `lidkoping-energi-lidkoping-42-kw-2026`
3. Batch 1, leverantörsmejl och övriga 55 redo-poster ligger utanför denna leverans.
4. Bevara den skriftligt bekräftade modellen exakt:
   `5 × Q_m × (1 − T_m/Tm_m)` per kalendermånad, summerad över 12 månader, exklusive
   moms. Resultatet är tvåsidigt: positiv avgift eller negativ kreditering, utan
   nollklämning. Fasta avgifter periodiseras 1/12 enligt leverantörssvaret.
5. `Q_m`, `T_m` och nätvärdet `Tm_m` är tre separata obligatoriska tolvmånadersserier.
   `Tm_m` ska vara strikt större än noll och kräver en faktisk, transporterad attestering
   av att värdet kommer från faktura eller leverantörsbesked. Inget standardvärde och
   ingen dold uppskattning får införas.
6. Båda produkterna ska stödja **aktuell uppskattad årskostnad** i MWh-läget.
   Kr-inversion och schablon ska blockeras. Besparingsprodukten ska fortsatt blockeras med
   `Produktbegransning` tills en källförsvarbar före/efter-regel för serierna finns.
7. Lägg den deklarativa justeringen i den verkliga katalogen och transportera den genom
   hela kedjan katalog → policy → fasad → motor → `Kostnad.justering` i både Python och
   TypeScript. Återanvänd Batch 0:s generiska serie-, metadata-, attestering- och
   felkontrakt; hårdkoda inte Lidköpingsfält i de generiska byggarna.
8. Låt `production_ready`/aktiveringsstatus vara avstängd. Under denna lokala
   implementationsrunda ska den styrande dispositionen därför vara kvar på
   **7 implementerade / 57 redo / 28 blockerade av 92**. Efter en separat, godkänd
   aktivering blir måltalet 9/55/28 — inte före den kontrollpunkten.

## Arbetsordning

1. Verifiera först repo-HEAD och arbetskopior. `skills@bac6f7f` ligger lokalt en commit
   före `origin/main@ca96a9a`; skillnaden är endast Claudes avslutande pushlogg för Batch 0.
   Bevara committen och skriv inte om den. Produktbaserna är
   `enkey-agents@45dd48a` och `neptune_academy@b03f4cc`.
2. Gör en kort gapkontroll mot den verkliga Batch 0-koden. Delar som redan finns ska
   återanvändas, inte implementeras en gång till. Om V22:s namn eller pseudokod avviker
   mekaniskt från det nuvarande API:t, följ det nuvarande API:t men bevara kontraktets
   semantik och dokumentera avvikelsen i leveransrapporten.
3. Implementera den kompletta Batch 5d-fillistan i de tre repona. Gör speglade
   Python-/TypeScriptändringar där motorn är dubblerad och regenerera endast härledda
   artefakter från den granskade katalogbasen.
4. Gör fokuserade lokala commits per repo. Staga inte befintliga orelaterade modifierade
   eller ospårade filer, ändra inte rå-PDF:n med leverantörssvaret och ta inte med det
   separata Codex-förslaget om maximal täckning av misstag.
5. Stanna efter lokal verifiering. Ingen push och ingen tariffaktivering.

## Minsta acceptansbevis före överlämning till Codex

- Ett oberoende handräknat goldenfall per tariff, med tydligt redovisade katalogpriser,
  effektband, energi, fasta avgifter, månadsserier, signerad justering och moms. Förväntat
  värde får inte genereras med funktionen som testas.
- Gemensamt referensfall visar samma delbelopp och totalsumma i Python och TypeScript.
- Minst ett positivt och ett negativt justeringsfall visar att kreditering inte kläms till
  noll, plus nollfallet `T_m = Tm_m`.
- Saknad serie, fel kardinalitet, icke-ändligt värde, `Tm_m <= 0`, saknad attestering och
  felaktigt effektbands-ID blockeras fältnära före division/kostnadsberäkning.
- Ett riktigt integrationsprov når `Kostnad.justering` via katalog → policy → fasad →
  motor; ett separat produktprov visar aktuell årskostnad och ett visar att
  besparingsvägen ger `Produktbegransning`.
- UI-prov på den riktiga kalkylatorsidan visar tre seriefält i januari–december-ordning,
  korrekta enheter/hjälptexter, obligatorisk attestering av `Tm_m`, fältnära fel och att
  otillåtna inmatnings-/produktlägen inte kan kringgås.
- Befintliga regressioner för de sju aktiva tarifferna är gröna och deras resultat är
  oförändrade. Kör full Python- och TypeScript-svit, `tsc --noEmit`, produktionsbygge,
  självbärande E2E samt `git diff --check`.

## Leveransrapport

Skriv resultatet i sessionen
`conversations/sessions/2026/09/2026-09-10-lidkoping-batch-5d.md` och länka det från
indexet. Rapportera:

- exakta lokala commit-hashar och baser i alla tre repon;
- ändrade filer och varför;
- handräknade facit och utfall per testlager;
- fulla testantal samt resultat för typkontroll, bygge och E2E;
- bekräftelse att ingen tariff är aktiverad, inget är pushat och 7/57/28 är oförändrat;
- eventuella kvarstående avvikelser eller blockerare utan att vidga scope.

När detta är levererat gör Codex en oberoende omgranskning. Aktivering/push kräver därefter
en ny kontrollpunkt. Nästa köade kodbatch efter godkänd Lidköping är Batch 1: sex
leverantörer enligt V22.

## Codex — granskning 2026-09-10-009 och nästa rättningsrunda

Batch 5d är **inte godkänd ännu**. Den fullständiga granskningen finns i
[`2026-09-10-009`](../../../reviews/2026/09/2026-09-10-kodgranskning-lidkoping-batch-5d.md).
Kärnformeln fungerar i båda språk, men Claude ska rätta följande avgränsade punkter på de
redan levererade lokala commitkedjorna:

1. Transportera och tillämpa `minimum_billing_basis` genom katalogformat, generator,
   policy, publik produktentry och formulär. Kräv 3–41 kW för 0–41-produkten och minst
   42 kW för 42+-produkten. Det leverantörsbekräftade band-ID:t ska fortsatt väljas
   explicit och inte härledas ur kW-talet.
2. Lägg fail-closed-validering av `signed_monthly_flow_adjustment`-payloaden: ändligt
   positivt `faktor_n`, tre obligatoriska icke-tomma fältnycklar och kopplingsbarhet till
   rätt obligatoriska tolvmånaderskrav. Lägg negativa katalogmutationstester.
3. Lägg riktiga produktprov genom `beraknaArsprodukt` och besparingsentryn samt ett
   renderingstest av den verkliga `KalkylatorPage`. Använd en isolerad testinjektion eller
   temporär genererad katalogpost; aktivera inte tariffen i produktionsdata. Proven ska
   omfatta MWh-only, blockerad kr-inversion/schablon, `Produktbegransning`, tre
   januari–december-serier, enheter/hjälptexter, obligatorisk Tm-attestering, fältnära fel
   och produktgränserna ovan.
4. Gör testmatrisen verkligt tvåtariffad. Lägg oberoende golden för 42+ och verifiera båda
   totalsummorna inklusive moms, faktisk 1/12-periodisering samt NaN/oändlighet i alla tre
   serier i både Python och TypeScript. Facit finns i granskningen.
5. Rätta katalogens interna motsägelse om saknad periodisering och lägg en icke-känslig
   katalogproveniens för 2026-prissidan och leverantörssvaret (datum/hash/gransknings-ID).
   Behåll den relevanta upplysningen om leverantörens debiterbara effekt. Den råa PDF:en
   ska inte committas.

Kör full Python- och TypeScript-svit, `tsc --noEmit`, produktionbygge, självbärande E2E
och `git diff --check`. Gör fokuserade lokala commits per repo och rapportera exakta nya
HEAD-hashar i sessionen. `investigation.status` ska vara kvar som aktiveringsspärr,
ingen tariff får göras produktionsvalbar, inget repo får pushas och dispositionen
7/57/28 av 92 ska förbli oförändrad. Stanna därefter för ny Codex-omgranskning.
