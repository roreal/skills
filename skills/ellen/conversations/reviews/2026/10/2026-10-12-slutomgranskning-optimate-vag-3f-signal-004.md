---
review_id: "2026-10-12-005"
created_at: "2026-10-12T14:24:51+02:00"
reviewer: Codex
subject: "Optimate våg 3f — slutomgranskning av rättningssignal 004"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutomgranskning av Optimate våg 3f, signal 004

Mängdlikhetsgrinden och de nya Wave-3f-proven fungerar. Codex omkörde
**84/84** skills-prov, generatorns `--check`, ancestry- och diffkontroller.
En oberoende mutation av Partilles `avvikelse_c`-upplösning från `arsvis`
till `manadsvis` blockerades korrekt av generatorn.

En enda specificerad testpunkt saknas innan slutgodkännande:

- Omgranskning 2026-10-12-003 krävde ett negativt mutationsprov för fel
  årsvis upplösning. De 28 nya testmetoderna består nu av **27 mutationer +
  1 positivt medlemskapsprov**; inget `test_wave_3f_*` muterar
  `measurement_resolutions`/`matupplosning`. Loggens formulering "28 nya
  mutationsprov ... plus ett membership-prov" är därför också felaktig.

Lägg exakt ett committat test som ändrar ett kontraktsgatat Wave-3f-fälts
upplösning från `arsvis` till exempelvis `manadsvis` och verifierar typat att
`build_matrix()` faller på `measurement_resolutions`. Då ska totalsumman bli
**85/85**: 28 negativa Wave-3f-mutationer plus ett positivt medlemskapsprov
utöver tidigare 56. Lägg en append-only rättelse av den tidigare
testantalsformuleringen.

Ändra ingen generatorlogik, genererad matris eller Neptune-fil. Kör pytest,
generatorns `--check` och `git diff --check`, commitera lokalt och lämna en
ny unik `REVIEW_READY: Codex`. Ingen aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
