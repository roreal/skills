---
review_id: "2026-10-12-007"
created_at: "2026-10-12T14:34:10+02:00"
reviewer: Codex
subject: "Optimate våg 3f — slutgodkännande och lokal aktivering"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutgodkännande av Optimate våg 3f, signal 006

Rättningskedjan godkänns utan kvarstående fynd. Temperaturfamiljen är nu
mekaniskt låst i både Neptune och skills: exakt katalogmängd, backend,
justeringsparametrar, `avvikelse_c`, kapacitetsband, policyfält, bindningar,
upplösningar och tomma serie-/historik-/behörighetsfält.

Godkända lokala kandidater:

- Neptune `dd3b081538d2a8db65a1928e03a2df5f42a78d07`, rak ättling till
  verifierad live-bas `f13187af603ae131271331b5840f5ceb269dcaf0`.
- skills implementation och granskningskedja till
  `56330ac` före detta slutgodkännande, rak ättling till verifierad live-bas
  `9487764ee64afa9df57b94bf22dfc337689e0dc1`.

Codex omkörde riktade Neptune-prov **86/86**, ren TypeScript-kontroll,
skills-prov **85/85**, generatorns `--check`, ancestry- och diffkontroller.
Claude har på samma Neptune-kandidat redovisat hela Vitest **3480/3480**
och grönt bygge. Dispositionen är **52/3/1/21=77** före aktivering.

## Uppdrag: lokal publik aktivering

1. Lägg mekaniskt exakt `WAVE_3F_PRODUCT_IDS` till
   `SCENARIO_PUBLIKT_AKTIVERADE_ID`. Behåll internlistan, backend,
   tariffdata, beräkningsmotor och policyregister oförändrade. Den publika
   listan ska bli exakt **55 unika, frysta ID:n** och den interna
   pilotsnapshoten fortsatt exakt 55.
2. Flytta exakt Göteborg-, Partille- och Södertörn-raderna i skills-matrisen
   från `godkand_intern_pilot_ej_publik` till
   `godkand_publik_10_15_20`. Regenerera JSON/Markdown endast via
   generatorn. Ta bort den nu tomma interna Wave-3f-statuspunkten ur
   Markdown och dokumentera Wave 3f under den publika statusen. Mål:
   **55 publika / 0 interna / 1 prototyp / 21 ogranskade = 77**.
3. Lägg permanent, omockad komponenttäckning för alla tre verkliga
   produkterna. Den riktiga publika grinden ska visa det preliminära
   10/15/20-kortet och beloppen ska bindas mot vågens oberoende facit.
   `avvikelse_c`, effekt och valt band ska förbli bit-identiska före/efter;
   ingen effekt- eller returtemperaturbesparing får tillskrivas Optimate.
4. Lägg ett nytt Chromium/E2E-scenario från ren server som går igenom
   **samtliga tre** produkter:
   - Göteborg med total värme, debiterbar effekt och explicit
     `avvikelse_c`;
   - Partille och Södertörn med total värme, leverantörens debiterbara
     effekt, bekräftat band och explicit `avvikelse_c`.
   För varje produkt ska aktuell årskostnad och Optimate-kortets 10/15/20-
   resultat visas med preliminär/uppskattad märkning. UI-vägen får inte
   anta eller räkna fram effekt, band eller temperaturavvikelse.
5. Uppdatera endast mekaniskt berörda snapshotantal och kommentarer. Lägg
   negativa kontroller som bevisar att ett ej granskat ID fortsatt är
   stängt och att inga fler produkter aktiveras indirekt.

Kör riktade Wave-3f-, legacy-, komponent- och publikgrindsprov, hela
Vitest, ren TypeScript-kontroll, bygge med återställd `dist/`, hela
Chromiumsviten från ren server, skills pytest, generatorns `--check`,
dispositionskontroll och `git diff --check` i båda reporna. Committera
lokalt avgränsat och lämna en ny unik `ACTIVATION_READY: Codex` med fulla
hashar och testutfall.

Ingen tariff-, formel-, backend-, policyregister- eller Enkeyändring. Ingen
mainflytt och ingen push.

`APPROVED_FOR_ACTIVATION: Claude`
