---
review_id: "2026-10-14-003"
created_at: "2026-10-14T19:49:44+02:00"
reviewer: Codex
subject: "Optimate våg 3g — slutgodkännande och lokal aktivering"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutgodkännande av Optimate våg 3g, signal 002

Rättningskedjan godkänns utan kvarstående fynd. Skills-grinden binder nu
Lidköpings två produkter fail-closed mot exakt fem unika råa policyfält,
hela kapacitets- och bandkontraktet, justeringen och Q/T/Tm-serierna.
Booleska värden kan inte längre passera som numeriska nollor eller ettor,
och båda produkternas bandtabeller mutationsprovas var för sig.

Godkända lokala kandidater:

- Neptune `f2c57c3f9b92febb8256b8a05ef59d716a790421`, rak ättling till
  verifierad live-bas `3f3d6ca97493df90a16b5d095724a42d5b126d33`.
- skills implementation och granskningskedja till
  `4247684dcf4d4950d4c2456441c2c03906951648` före detta
  slutgodkännande, rak ättling till verifierad live-bas
  `9a9fe40171b392372b73a940daec1ce3964bd1df`.

Codex omkörde skills **128/128** plus fyra gröna subtest,
generatorns `--check`, Wave-3g-proven **69/69**, ren TypeScript-kontroll,
ancestry- och diffkontroller samt samtliga sex oberoende mutationer från
omgranskningen. Neptune-worktreen är ren. På samma oförändrade
Neptune-kandidat är den tidigare fullkörningen **3563/3563** grön.
Dispositionen är **55/2/1/19=77** före aktivering.

## Uppdrag: lokal publik aktivering

1. Lägg mekaniskt exakt `WAVE_3G_PRODUCT_IDS` till
   `SCENARIO_PUBLIKT_AKTIVERADE_ID`. Behåll internlistan, backend,
   tariffdata, beräkningsmotor och policyregister oförändrade. Den publika
   listan ska bli exakt **57 unika, frysta ID:n** och den interna
   pilotsnapshoten fortsatt exakt 57.
2. Flytta exakt Lidköping 0–41 kW och 42+ kW i skills-matrisen från
   `godkand_intern_pilot_ej_publik` till
   `godkand_publik_10_15_20`. Regenerera JSON/Markdown endast via
   generatorn och uppdatera endast mekaniskt berörda prov/kommentarer.
   Måldisposition: **57 publika / 0 interna / 1 prototyp / 19 ogranskade =
   77**.
3. Lägg permanent, omockad komponenttäckning för båda verkliga
   produkterna. Den riktiga publika grinden ska visa det preliminära
   10/15/20-kortet och beloppen ska bindas mot vågens oberoende facit.
   Debiterbar effekt, valt band och samtliga tre Q/T/Tm-serier ska vara
   bit-identiska före/efter. Ingen effektbesparing, bandväxling,
   volymminskning eller förbättrad avkylning får tillskrivas Optimate.
4. Lägg ett nytt Chromium/E2E-scenario från ren server som går igenom
   **båda** produkterna med handoffens gemensamma 120 MWh-fixtur:
   - 0–41 kW: debiterbar effekt 20 kW, bekräftat band 2;
   - 42+ kW: debiterbar effekt 100 kW, bekräftat band 1;
   - Q `[10,20,...,120]`, T `[20,22,...,42]`, Tm tolv gånger 40 och
     uttrycklig attestering av Tm.
   Verifiera aktuell årskostnad samt Optimate-kortets 10/15/20-resultat
   mot det oberoende facit som redan är låst i Wave-3g-proven. UI-vägen
   får inte uppskatta eller ersätta effekt, band, Q, T eller Tm.
5. Lägg en publik fail-closed UI-kontroll: saknad Tm-attestering eller
   ofullständig serie ska inte ge ett besparingsresultat. Behåll ett
   genuint ogranskat ID och `riksgenomsnitt` stängda och bevisa att inga
   ytterligare produkter aktiveras indirekt.

Kör riktade Wave-3g-, komponent- och publikgrindsprov, hela Vitest, ren
TypeScript-kontroll, bygge med återställd `dist/`, hela Chromiumsviten från
ren server, skills pytest, generatorns `--check`, dispositionskontroll och
`git diff --check` i båda reporna. Committera lokalt avgränsat och lämna
en ny unik `ACTIVATION_READY: Codex` med fulla hashar och testutfall.

Ingen tariff-, formel-, backend-, policyregister- eller Enkeyändring.
Ingen mainflytt och ingen push.

`APPROVED_FOR_ACTIVATION: Claude`
