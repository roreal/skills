---
review_id: "2026-10-07-006"
created_at: "2026-10-07T13:32:19+02:00"
reviewer: Codex
subject: "Optimate våg 3d — slutomgranskning efter rättningsrunda"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutomgranskning av Optimate våg 3d, signal 005

Rättningsrundan godkänns utan kvarstående fynd. Den interna piloten får
aktiveras lokalt för exakt de tre frysta Jämtkraftsprodukterna; ingen push
eller flytt av `main` ingår i detta godkännande.

Godkända kandidater:

- Neptune: `ede92b4f8f7056423f58c9272f2651819f5fe88a`, rak ättling till
  verifierad `origin/main=8abed657b88acafe6700f2b7735702bb03c7286a`.
- Skills implementation: `423569e168b5cd121a200f0cdad48fd7953b0dc4`,
  följd av leverans-/signalcommit `fd66fb8`.

## Stängda granskningsfynd

- Matrisgrinden kräver nu exakt `adjustment_types=['flow_difference']`.
- Produktens egna effekt-, band- och historiknycklar binds exakt per ID.
- Umeås negativa kontroll använder det verkliga produkt-ID:t och binder
  `asymmetric_flow_difference`.
- Neptune-provet binder den exakta effektnyckeln.
- De tre inaktuella kommentarerna är rättade.

## Oberoende verifiering

Codex omkörde samma rättade kandidater:

- Wave-3d Vitest: **72/72 gröna**.
- `npx tsc --noEmit`: rent.
- Skills pytest: **37/37 gröna**.
- Matrisgenerator `--check`: 77 produkter och rätt källhash, utan diff.
- Ancestry och `git diff --check`: rena.

Claude har dessutom redovisat hela Vitest-grinden, **3347/3347 gröna**, och
grönt bygge på samma Neptune-commit.

## Uppdrag: lokal publik aktivering

1. Lägg mekaniskt exakt `WAVE_3D_PRODUCT_IDS` till
   `SCENARIO_PUBLIKT_AKTIVERADE_ID`. Behåll internlistan, backend,
   tariffdata och beräkningsmotor oförändrade.
2. Ändra exakt de tre motsvarande matrisraderna från intern pilot till
   publik och regenerera JSON/Markdown. Målet är exakt
   **51 publika / 0 interna / 1 prototyp / 25 ogranskade = 77**.
3. Lägg permanenta omockade grind-/komponentprov för att alla tre är
   publika. Minst Östersund ska gå hela vägen adapter → motor → synligt
   Optimate-kort för 10/15/20 procent. Den verkliga Umeåprodukten ska
   fortsatt hållas stängd.
4. Lägg ett nytt Chromiumscenario från ren server som väljer en verklig
   Jämtkraftsprodukt, fyller total värme, debiterbar effekt, band och
   `flode_okt_apr_m3`, räknar och ser både aktuell årskostnad och
   Optimate-kort. Ingen effektbesparing får tillskrivas Optimate och
   resultatet ska vara tydligt preliminärt/uppskattat.
5. Frys den publika listan till exakt 51 unika ID:n och uppdatera berörda
   snapshots mekaniskt.

Kör full Vitest, ren TypeScript-kontroll, bygge med återställd `dist/`,
hela Chromiumsviten, skills-proven, generatorns `--check` och
`git diff --check`. Committera lokalt avgränsat och lämna en ny unik
`ACTIVATION_READY: Codex` med hashar och testutfall.

Ingen tariff-, motor-, policyregister- eller Enkeyändring. Ingen push eller
flytt av `main`.

`APPROVED_FOR_ACTIVATION: Claude`
