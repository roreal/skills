---
review_id: "2026-09-23-001"
date: "2026-09-23"
reviewer: Codex
decision: "APPROVED_INTERNAL_PILOT"
approved_scope: "scenario-provenance-physical-invariant-and-public-gate-correction"
neptune_reviewed_head: "605bddd5c39a0663ca01ab8ad88acd25013a9aa0"
neptune_parent: "0958f616b19029d3903dda763d674437a1f1615d"
skills_head_before_review_log: "b8feac8f4b67efe5a3c2aecd95c75e917da40636"
enkey_untouched_head: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
activation_allowed: false
push_allowed: false
---

# Slutomgranskning av Optimate-scenariomotorns rättningsrunda

## Beslut

Rättningsrundan i Neptune `0958f61..605bddd` godkänns för den avgränsade
**interna Sundsvall-piloten**. Inga kvarstående fynd finns inom
granskning 009:s tre rättningspunkter. Detta är inte ett godkännande för
publik UI-aktivering, tariffaktivering eller push.

## Stängda fynd

1. Rumsvärmeserien har nu obligatorisk proveniens. Varje hypotetiskt
   efterläge har egen `status: 'preliminar'`, antagandelista och kan inte
   presenteras med `exact` noggrannhet. Den befintliga referenskostnadens
   status lämnas oförändrad.
2. Ackumulerat rumsvärmeöverskott avvisas på årsnivå och övrig last kläms
   till lägst noll som sista skydd. Gränsfallet där varje månad låg inom
   toleransen men årssumman blev negativ är testat.
3. Intern pilot och publik förmåga är separerade. Sundsvall är tillåten i
   den interna beräkningspiloten, medan
   `stodjerOptimateScenarioPubliktAktiverad` är fail-closed med tom
   publik allowlist.

Diffen innehåller exakt två filer:

- `neptune-marketing/src/utils/optimateScenario.ts`
- `neptune-marketing/src/utils/optimateScenario.test.ts`

Ingen UI-anropare, katalogpost, `stodjer_besparing`-flagga eller annan
tariff har ändrats.

## Oberoende verifiering

- riktade scenariotest inklusive Stockholm-regression: **26/26** gröna;
- full Vitest: **2 292/2 292** gröna i 69 filer;
- `npx tsc --noEmit`: rent;
- `npm run eval:build`: grönt, endast befintlig chunkstorleksvarning;
- täckningsmatrisens kontroll och sex Python-test: gröna;
- `git diff --check`: rent och Neptune-arbetskopian ren.

Browser-E2E kördes inte om för den här tvåfilsrättningen: ingen
produktionsanropare importerar scenariomotorn och den föregående
granskningen körde samtliga UI-scenarier 1–29 gröna mot samma bas.

## Senare grindar

Före publik integration ska UI-kontraktet även bära proveniens för den
totala månadsprofilen när den kan vara skattad. Effekt-/flödesfamiljer
kräver dessutom fryst debiteringshistorik och finare prisledssemantik.
De frågorna ligger utanför denna rättningsrunda och hindrar inte den
godkända interna Sundsvall-piloten.
