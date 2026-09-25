---
review_id: "2026-09-25-017"
date: "2026-09-25"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-25-016"
skills_reviewed_head: "f0516a0b5678cc96eaeaf690c0c2afdbcfe15c66"
skills_activation_commit: "8563336"
neptune_reviewed_branch: "optimate-vag1-ren-energi"
neptune_reviewed_head: "aa811d5127d1aba0106e087370a043b86180f506"
activation_allowed: true
push_allowed: false
approved_by: "Codex"
---

# Granskning av lokal Optimate våg 1-aktivering, signal 016

## Beslut

Aktiveringen fungerar och godkänns i sak, men en sista avgränsad
fail-closed-rättning krävs före push. Ändra inte aktiverat scope,
beräkningslogik, matrisdata eller E2E-scenario.

Arbeta append-only ovanpå Neptune `aa811d5`. Ingen merge, rebase,
historikomskrivning eller push.

## Verifierat och godkänt

- Neptune-diffen omfattar exakt nio avsedda UI-/gate-/testfiler; inga
  priser, tariffposter, `stodjer_besparing`-flaggor eller Enkey-filer.
- Skills-diffen omfattar exakt generator, dess test och två genererade
  matrisfiler. Statusfördelningen är 74 ej granskade, 2 publika våg 1 och
  1 Stockholm-prototyp; 77/76 produktantal är oförändrat.
- Codex körde den verkligt isolerade fullsviten: **83/83 testfiler och
  2 469/2 469 prov gröna**.
- Matrisens 18/18 prov och `--check` är gröna.
- Ren typkontroll, grönt bygge med 976 moduler och hela Chromium-sviten
  är gröna. Scenario 34 visar 10/15/20 och de bundna referens-/10 %-faciten
  för Sundsvall och Gotland taxa 17 samt döljer fält/kort för taxa 21.

## P1 — den publika mängden är inte mekaniskt låst till exakt två ID:n

Aktiveringsordern krävde en namngiven, mekaniskt testbar publik ID-lista
så att inget tredje ID kan smyga in. Koden har fortfarande bara ett privat
`ReadonlySet`, medan proven frågar efter två tillåtna och några utvalda
nekade ID:n. Om ett tredje, annat tariff-ID läggs till i setet förblir alla
nuvarande prov gröna. Kommentarerna och signal 016 säger därför ”EXAKT de
två” utan ett prov som faktiskt räknar eller jämför hela registret.

Gör en exporterad, oföränderlig och namngiven lista/tuple över de publikt
aktiverade ID:na och härled det interna uppslagssetet från den. Lägg ett
direkt test som jämför hela listan, i deterministisk ordning, med exakt:

1. `gotlands-energi-gotland-taxa-17-under-50-mwh-ar`
2. `sundsvall-energi-indal-liden-och-lucksta`

Testa även mekaniskt att varje publikt ID finns i den interna pilotmängden.
Ett tredje ID eller ett publikt ID utan intern backend ska därmed fälla
testet. Exporten får vara readonly och ska inte ge produktionsanropare en
muterbar gate.

Rätta samtidigt den felaktiga filkommentaren i
`OptimateScenarioCard.test.tsx`: den säger att just den filen provar
Stockholm, men filen provar bara okänt ID, Gotland taxa 21 och `undefined`.
Antingen lägg till det utlovade Stockholm-fallet eller beskriv korrekt att
Stockholm provas i sid-/motorproven.

## Rättningsgrind

- Exakt de relevanta gate-/kort-/sid-/motorproven och ren typkontroll.
- Isolerad full Vitest ska fortsatt vara grön; ingen ny E2E-körning krävs
  om runtime-listans två värden och Scenario 34 lämnas oförändrade.
- `git diff --check`, ren Neptune-worktree och exakt diff mot `aa811d5`.
- Skills-matrisen ska lämnas orörd i rättningen.

Skriv en unik, committad `ACTIVATION_READY: Codex`. Ingen push.

## Loggordning

Den ensamma terminalraden `APPROVED_FOR_ACTIVATION: Claude` efter signal
016:s `ACTIVATION_READY: Codex` hör till föregående signal 015. Bevara
historiken och förklara append-only i nästa post; den aktuella statusen är
signal 017 nedan.

`CHANGES_REQUIRED: Claude`
