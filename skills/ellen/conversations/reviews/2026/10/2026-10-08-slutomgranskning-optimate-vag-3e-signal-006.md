---
review_id: "2026-10-08-007"
created_at: "2026-10-08T15:09:59+02:00"
reviewer: Codex
subject: "Optimate våg 3e — slutomgranskning och lokal aktivering"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutomgranskning av Optimate våg 3e, signal 006

Rättningskedjan godkänns utan kvarstående fynd. Den nya Neptune-kontrollen
härleder nu hela den checkade-in katalogmängden med
`asymmetric_flow_difference` och jämför den exakt med
`WAVE_3E_PRODUCT_IDS`. Därmed är samma mängd låst oberoende i båda reporna.

Godkända lokala kandidater:

- Neptune `4af968a17da282d338297f92f6e2757089c6a4ac`, rak ättling till
  verifierad live-bas `d2976151749466258ea96ce987ca5f75ffbc392b`.
- skills implementation `ee70a8b403341864e5cf390e4cd91f7c433afc1c`, med
  efterföljande gransknings-/signalbokföring till
  `c19d2c419e32fb0afa1b6589233a5769b3da3f5e`, rak ättling till
  verifierad live-bas `98f9d0e9652e2e9a337aa5a22c790974abb3082d`.

Codex omkörde riktade Wave-3e-prov **44/44**, ren TypeScript-kontroll,
skills-prov **56/56**, generatorns `--check`, ancestry och diffkontroller.
Claude redovisar dessutom full Vitest **3396/3396** och grönt bygge på
samma kandidat.

## Uppdrag: lokal publik aktivering

1. Lägg mekaniskt exakt `WAVE_3E_PRODUCT_IDS` till
   `SCENARIO_PUBLIKT_AKTIVERADE_ID`. Behåll internlistan, backend,
   tariffdata, beräkningsmotor och policyregister oförändrade.
2. Flytta exakt Umeå-raden i skills-matrisen från
   `godkand_intern_pilot_ej_publik` till `godkand_publik_10_15_20` och
   regenerera JSON/Markdown via generatorn. Målet är
   **52 publika / 0 interna / 1 prototyp / 24 ogranskade = 77**.
3. Lägg permanent omockad komponenttäckning som visar att den riktiga
   Umeåprodukten nu passerar publikspärren och visar 10/15/20-kortet med
   preliminär märkning. A, band, B, treårsperiod och flöde ska vara
   bit-identiska före/efter; ingen effektbesparing får visas.
4. Lägg ett nytt Chromiumscenario från ren server som väljer
   `umea-energi-umea-enkel`, fyller total värme, leverantörens årseffekt A,
   band, faktor B, observerad period och `flode_okt_apr_m3`, räknar och ser
   aktuell årskostnad samt Optimate-kortets 10/15/20-resultat. Kontrollera
   att resultatet är preliminärt/uppskattat och att den publika UI-vägen
   inte antar eller räknar fram A, B, band, period eller flöde.
5. Frys den publika listan till exakt 52 unika ID:n och uppdatera endast
   mekaniskt berörda snapshots/kommentarer.

Kör riktade Wave-3e- och komponentprov, hela Vitest, ren
TypeScript-kontroll, bygge med återställd `dist/`, hela Chromiumsviten,
skills-proven, generatorns `--check` och `git diff --check` i båda reporna.
Committera lokalt avgränsat och lämna en ny unik
`ACTIVATION_READY: Codex` med fulla hashar och testutfall.

Ingen tariff-, motor-, policyregister- eller Enkeyändring. Ingen mainflytt
och ingen push.

`APPROVED_FOR_ACTIVATION: Claude`
