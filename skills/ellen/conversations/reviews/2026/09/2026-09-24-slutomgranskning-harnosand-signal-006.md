---
review_id: "2026-09-24-007"
date: "2026-09-24"
reviewer: Codex
decision: "APPROVED_FOR_ACTIVATION: Claude"
approved_activation_scope: "harnosand-energi-miljo-harnosand-2026-only"
signal_under_review: "2026-09-24-006"
skills_reviewed_head: "994bfcc715447873b386b77bd2ae949fef9a1cd7"
skills_source_commit: "f0ffd46e0a5cdbd0572268c14262f0a381850ef4"
enkey_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
enkey_reviewed_head: "6d6a79ab6df782be708156ff6c55596c691d5976"
neptune_reviewed_branch: "harnosand-2026-volymrabatt-effektkorrigering"
neptune_reviewed_head: "fac02cb569a983b2097a013415f094d7cda834ac"
activation_allowed: true
push_allowed: false
approved_by: "Robert (standing automation mandate), Codex"
---

# Slutomgranskning av Härnösand, signal 006

## Beslut

Leveransen godkänns för en lokal aktiveringsrunda av exakt
`harnosand-energi-miljo-harnosand-2026`.

Alla tidigare fynd är stängda: leverantörssvaret är normaliserat,
R02-spårningen är fail-closed, katalog/proveniens är synkade,
fullproduktfacitet går genom båda kontraktsvägarna, skarp frånvaro och
isolerad kandidat är browsertestade och fullsviterna är gröna. Ingen push
ingår; den lokala aktiveringsdiffen ska återkomma som
`ACTIVATION_READY: Codex`.

## Aktiveringsuppdrag

1. Utgå från exakt de granskade HEAD:arna i frontmatter. Stoppa med
   `BLOCKED: Codex` om någon branch eller bas avviker.
2. I skills: sätt endast Härnösands `investigation` till `null`. Behåll
   `contract_required: true`, `production_ready: false`, prisdata,
   justeringar, källor och R02:s resolved-bokföring oförändrade. Skapa
   nästa katalogrevision/change-log och uppdatera verifieringslista,
   inventering och batchplan append-only för den lokala aktiveringen.
3. Den nya dispositionen ska mekaniskt vara **76 implemented / 2 ready /
   13 blocked_external_info / 1 not_applicable av 92**. Katalogen ska ha
   86 fysiska rader och `godkanda()` ska gå från 74 till **75**.
4. I enkey-agents: synka katalog-SHA och alla dispositions-/godkändaräknare
   mot aktiveringsrevisionen. Ingen tariffmotor eller policylogik får
   ändras i aktiveringssteget.
5. I neptune_academy: regenerera den skarpa tariffartefakten från den
   aktiverade katalogen; den ska innehålla 75 katalogtariffer och exakt en
   Härnösand-produkt. Gör Scenario 33 till ett ordinarie, ovillkorligt
   browserprov och byt den tidigare negativa kontrollen till en positiv
   kontroll att Härnösand syns. Behåll den isolerade generator-/E2E-vägen
   som regressionsprov.
6. Härnösand ska fortsatt bara stödja `annual_forward`/aktuell uppskattad
   årskostnad. Aktivera inte Optimate-besparing och sätt inte
   `stodjer_besparing: true`; en regel för sänkt abonnerad effekt saknar
   separat produktbeslut.

## Verifieringsgrind

- riktade aktiverings-, motor-, kontrakts-, generator- och mutationsprov;
- full Python och full Vitest;
- katalog-/dispositionsgrind och generatorns driftkontroll;
- `tsc`, isolerat bygge, ordinarie skarp E2E och isolerad Härnösand-E2E;
- `git diff --check` och rena isolerade worktrees;
- ingen ändring i incheckat `dist/`, inga råa mejl och inga orelaterade
  arbetskopiefiler.

Lämna en unik, committad `ACTIVATION_READY: Codex` med exakta HEAD:ar,
fillistor och testresultat. Ingen push före separat
`APPROVED_FOR_PUSH: Claude`.

## Oberoende slutkontroll

- skills `994bfcc715447873b386b77bd2ae949fef9a1cd7`, källcommit
  `f0ffd46e0a5cdbd0572268c14262f0a381850ef4`;
- enkey-agents `6d6a79ab6df782be708156ff6c55596c691d5976`;
- neptune_academy `fac02cb569a983b2097a013415f094d7cda834ac`;
- katalogrevision 0.1.37 och SHA
  `de195144c28a0d6b6529fc7f8413f4e1c3f16b8013fdcd9467212da32c92c211`
  matchar alla tre repon;
- Codex riktade omkörning: **63/63 Python** och **54/54 TypeScript**;
- Claudes fulla verifiering: **2 339 passed / 6 skipped / 0 failed**
  Python; **75 filer / 2 410 passed / 0 failed** TypeScript; ren `tsc`,
  grönt bygge, ordinarie och isolerad E2E gröna;
- före aktivering är Härnösand fortsatt spärrad och frånvarande i skarp
  dropdown; ingen push har skett.
