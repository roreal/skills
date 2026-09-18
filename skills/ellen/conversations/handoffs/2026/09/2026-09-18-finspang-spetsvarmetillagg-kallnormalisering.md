---
handoff_id: "2026-09-18-042"
created_at: "2026-09-18T12:36:39+02:00"
from: Codex
to: Claude
status: ready-for-implementation
requested_by: Robert
approved_by: Codex
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "finspang-2026-spetsvarmetillagg-source-normalization-and-disposition-tests-only"
tariff_activation_allowed: false
catalog_change_allowed: false
product_code_change_allowed: false
push_allowed: false
force_push_allowed: false
published_history_rewrite_allowed: false
required_skills_parent: "ab1432883bd42aacbf34a3613e20da88e042f3cc"
required_enkey_origin_main: "47fdc67386b9db990d63c910069700b75301f743"
protected_enkey_local_main: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
required_neptune_main: "92226dbf16d705365cf9d9d3b52e763dadfad1b5"
---

# Uppdrag till Claude: normalisera Finspångs spetsvärmetillägg för 2026

## Källbeslut

Läs den committade, sanitiserade bedömningen
[`2026-09-18-bedomning-finspang-spetsvarmetillagg.md`](../../../../Fjarrvarmetariffer/Svar%20på%20frågor/2026-09-18-bedomning-finspang-spetsvarmetillagg.md)
fullständigt. Finspångs Tekniska Verk har bekräftat att något
spetsvärmetillägg inte har debiterats kunder 2026 och att det saknas en
tillämpad debiteringsmodell. Den ej materialiserade variantposten
`finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg` ska därför flyttas
från `blocked_external_info`/`external_answer_required` till
`not_applicable` för 2026.

Detta är en käll- och dispositionsnormalisering, inte en tariffimplementation.
Konstruera inte ett 20-procentigt påslag. Finspångs redan implementerade
bastariff ska vara helt oförändrad.

## Tillåtet ändringsscope

1. Uppdatera `Fjarrvarmetariffer/variantfragor-ej-materialiserade-2026.md`:
   stäng A5, klassificera rad 4 som `not_applicable`, länka den sanitiserade
   bedömningen och skriv att inget nytt leverantörssvar behövs för 2026.
2. Lägg daterade, tydliga nulägesrättelser i
   `Fjarrvarmetariffer/tariffinventering-v22.md` och
   `Fjarrvarmetariffer/batchplan-v22.md`. Bevara historiska baslinjer som
   historik. §5:s maskinparsade Finspångsrad ska däremot få den aktuella
   dispositionen `not_applicable`, och §8a:s aktuella status ska synkas.
3. Uppdatera endast
   `tools/tariffer/tests/test_dispositionsgrind_inventering.py` i
   `enkey-agents` så att den skarpa grinden bevisar
   **74 implemented / 2 ready / 15 blocked / 1 not_applicable av 92**.
   Pinna uttryckligen Finspångs variant-ID till `not_applicable`. Revidera
   berörda historiska/projicerade summeringar så att `not_applicable` räknas
   med i totalen i stället för att 92 felaktigt kräver att alla poster ligger
   i endast tre klasser.
4. Lägg daterad leveransbokföring i
   `conversations/sessions/2026/09/2026-09-17-blockerade-tariffer.md` och en
   ny unik, committad toppsignal `REVIEW_READY: Codex` i
   `conversations/index.md`.

Ändra inte råmejlet, katalog-JSON, katalog-SHA, generatorer, motor, policy,
React/TypeScript, Neptune, Finspångs bastariff, prisdata eller agentbryggan.
Ingen ny fysisk katalograd eller produkt får skapas.

## Enkey-isolering är obligatorisk

Lokala `enkey-agents/main@2e30bb2` innehåller en bevarad, ännu opushad och
tariffoberoende Milesight-commit ovanpå `origin/main@47fdc67`. Checka inte ut,
flytta, återställ eller skriv om denna lokala `main`, och lägg inte
tarifftestcommitten ovanpå den.

Gör i stället teständringen på en separat lokal kandidatbranch/worktree med
exakt bas `47fdc67386b9db990d63c910069700b75301f743`. Bevara lokala `main@2e30bb2`
orörd. Rapportera kandidatref och commit i nästa signal. Ingen ref får pushas
i detta steg.

## Acceptanskriterier

- exakt 92 dispositions-ID:n består: 78 bas + 14 variant;
- skarp disposition är exakt `74 / 2 / 15 / 1` i ordningen implemented,
  ready, blocked, not_applicable;
- varianten `--spetsvarmetillagg` är exakt den enda flytten och blir
  `not_applicable`;
- Finspångs bastariff är fortsatt implementerad och byte-oförändrad i
  katalogen;
- fysiska katalogmått är oförändrade: 86 rader, 73 godkända och 75
  produkter;
- den riktade dispositionsgrinden och full `tools/tariffer`-svit är gröna;
- råmejlet förblir ospårat och inga personuppgifter tas in i git;
- `git diff --check` är rent för det tillåtna scopet.

Stanna efter en committad `REVIEW_READY: Codex`. Ingen aktivering eller push.
