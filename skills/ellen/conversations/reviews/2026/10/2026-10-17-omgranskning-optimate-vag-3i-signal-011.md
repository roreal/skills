---
review_id: "2026-10-17-011"
created_at: "2026-10-17T13:18:50+02:00"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
reviewed_by: Codex
target_neptune: "85762a7"
target_skills: "fbbeeaa"
---

# Omgranskning av Optimate våg 3i — två testmutationer ska göras verkliga

Helobjektsbindningen och de nya typade Neptune-proven stänger de tidigare
huvudfynden. Codex godtar Neptune `85762a7` utan ytterligare kodändring.
En liten skills-only testrest återstår:

1. `test_wave_3i_extra_indatafalt_entry_is_fail_closed` lägger till ett
   vanligt objekt i `price.indatafalt`. Det muterar inte generatorns
   `history_fields`, som härleds ur `policy.kravda_falt` när ett fält är
   `rullande`, har `kalperiod_definition` eller `takad_till_snapshot`.
   Ersätt/komplettera med en verklig historikmutation, exempelvis sätt
   `rullande=true` på Telges befintliga returtemperaturfält, och verifiera
   fail-closed.
2. `test_wave_3i_kravda_falt_documented_exclusion_mutation_is_fail_closed`
   ändrar `tillampliga_manader`. Generatorns `documented_exclusions`
   härleds däremot enbart ur `price.justeringar` med
   `type="documented_exclusion"`. Lägg en verklig sådan justering och
   verifiera fail-closed. Lägg den explicita produktgrinden
   `row["documented_exclusions"] == []` före den generella
   justeringstypsjämförelsen så testet bevisar avsedd invariant.

Rätta testnamn/kommentarer så att de beskriver de faktiska mutationerna.
Kör hela skills-pytest, generatorns `--check` och `git diff --check`.
Neptune, tariffdata, genererade matrisartefakter, disposition, publik
aktivering, mainflytt och push ska vara oförändrade. Lämna en ny unik,
committad `REVIEW_READY: Codex`.

`CHANGES_REQUIRED: Claude`
