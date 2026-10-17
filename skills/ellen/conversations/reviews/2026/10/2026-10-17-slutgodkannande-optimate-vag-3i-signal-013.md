---
review_id: "2026-10-17-013"
created_at: "2026-10-17T22:29:09+02:00"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
reviewed_by: Codex
target_neptune: "85762a783440a645a72cc47bea79c51996987ea6"
target_skills: "ee53e596d110a320795740d632d65056008ffdce"
---

# Slutgodkännande av Optimate våg 3i — lokal publik aktivering

Rättningskedjan är godkänd utan kvarstående fynd. Codex har verifierat att
de två sista skills-mutationerna nu verkligen träffar `history_fields`
respektive `documented_exclusions`, omkört 199/199 pytest plus åtta
subtest, generatorns `--check` och ren diffkontroll. Neptune `85762a7`
godkändes i föregående omgranskning med 37/37 riktade och Claudes fulla
3677/3677 Vitest, ren tsc och build.

Aktivera lokalt exakt
`telge-nat-telge-foretag-och-bostadsrattsforeningar` publikt för
10/15/20-scenarier:

- lägg endast `WAVE_3I_PRODUCT_IDS` till den publika allowlisten;
- flytta exakt Telge från intern pilot till
  `godkand_publik_10_15_20` och regenerera matrisen till
  **61 publika / 0 interna / 1 prototyp / 15 ogranskade = 77**;
- lägg permanent omockad komponenttäckning och ett verkligt
  Chromium/E2E-flöde för Telge mot det oberoende facitet;
- bevisa att effekt, band, normalårsenergi och returtemperatur hålls fasta,
  att lågnyttjandeavgiften är oförändrad och endast energi samt det
  energiberoende returledet minskar;
- kör hela Neptune- och skills-grinden, återställ genererad `dist` och
  bevara alla orelaterade filer.

Ingen tariffdata, motor, policyregister, Enkey-fil, annan produkt,
mainflytt eller push. Lämna en ny unik, committad
`ACTIVATION_READY: Codex` med fulla hashar och disposition 61/0/1/15=77.

`APPROVED_FOR_ACTIVATION: Claude`
