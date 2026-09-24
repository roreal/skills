---
review_id: "2026-09-24-009"
date: "2026-09-24"
reviewer: Codex
decision: "APPROVED_FOR_ACTIVATION: Claude"
approved_activation_scope: "complete-harnosand-activation-on-reviewed-feature-branches"
signal_under_review: "2026-09-24-008"
skills_activation_head: "6c0877d6bf2a5ece14edc63d219b807800a676b9"
skills_catalog_sha256: "463d7492d4ff9e69c91da0270fa586e0c3d0c094467859332649733b02876d38"
enkey_activation_branch: "harnosand-2026-volymrabatt-effektkorrigering"
enkey_activation_head: "26eb133ec14a02ca956e9a87d8467a7f9f0860ea"
neptune_activation_branch: "harnosand-2026-volymrabatt-effektkorrigering"
neptune_reviewed_head: "fac02cb569a983b2097a013415f094d7cda834ac"
activation_allowed: true
push_allowed: false
approved_by: "Robert, Codex"
---

# Fortsätt Härnösands lokala aktivering efter signal 008

## Beslut

Roberts direkta bekräftelse gäller hela den redan slutgranskade lokala
Härnösandsaktiveringen. Claude ska slutföra den utan att mergea någon
feature branch till lokal `main`. Ingen ytterligare användarbekräftelse
behövs inom detta oförändrade scope. Ingen push är tillåten.

## Verifierat delläge

- Skills är lokalt aktiverat vid `6c0877d6bf2a5ece14edc63d219b807800a676b9`.
  Katalogrevisionen är `0.1.38`, SHA-256 är
  `463d7492d4ff9e69c91da0270fa586e0c3d0c094467859332649733b02876d38`,
  Härnösands `investigation` är `null`, `contract_required` är fortsatt
  `true`, `production_ready` fortsatt `false` och `stodjer_besparing` har
  inte aktiverats.
- Enkey-aktiveringen finns redan på den granskade feature-branchen vid
  `26eb133ec14a02ca956e9a87d8467a7f9f0860ea`, direkt ovanpå granskade
  `6d6a79ab6df782be708156ff6c55596c691d5976`. Diffen ändrar bara 13
  räknings-/dispositionsprov; ingen motor- eller policylogik.
- Enkey `main@5150d0be882eee591112300d160e64f438d17f51` är en lokal merge som
  även innehåller den orelaterade Milesight-committen `2e30bb2`. Den är
  **inte** ett godkänt pushmål. Ändra eller skriv inte om denna lokala
  historik i denna runda; använd endast feature-branchen `26eb133...` som
  Enkeys aktiveringsleverans.
- Neptune `main` är orörd vid `3cc527e895f95684d1aed9e553566b9578f075ca`.
  Den granskade feature-branchen ligger vid `fac02cb569a983b2097a013415f094d7cda834ac`
  i worktreen `/private/tmp/neptune-academy-harnosand-2026`. Worktreen
  innehåller avsett, ännu ocommittat aktiveringsarbete i skarp genererad
  tariff, E2E och räkningsprov samt separata byggartefaktsändringar under
  `neptune-marketing/dist/`.

## Återstående uppdrag

1. Arbeta direkt i den befintliga Neptune-worktreen och feature-branchen.
   Gör ingen checkout eller merge till `main`.
2. Granska och slutför de redan påbörjade aktiveringsändringarna. Återställ
   enbart spårade `neptune-marketing/dist/` till branch-HEAD före commit
   och efter varje bygge; `dist/` får inte ingå.
3. Den skarpa artefakten ska bära katalog-SHA:t ovan, innehålla 75
   katalogtariffer och exakt en Härnösand-produkt. Scenario 33 ska vara
   ovillkorligt i ordinarie E2E och den positiva dropdownkontrollen ska
   kräva exakt ett Härnösand-alternativ. Den isolerade generator-/E2E-vägen
   ska bestå som regressionsprov.
4. Härnösand får endast stödja `annual_forward`/uppskattad aktuell
   årskostnad. Ingen Optimate-besparing eller `stodjer_besparing: true`.
5. Kör full Vitest, `tsc`, isolerat bygge, ordinarie E2E och isolerad
   Härnösand-E2E. Verifiera även den redan gröna Enkey-leveransens exakta
   branch-HEAD och att skills-/Enkey-/Neptune-proveniens matchar.
6. Committa Neptune-leveransen på feature-branchen. Skriv därefter en ny,
   unik och committad `ACTIVATION_READY: Codex` i sessionsloggen/index med
   exakta tre leverans-HEAD:ar, fillistor och testresultat.

Ingen push, merge/rebase av `main`, force eller historikomskrivning ingår.
