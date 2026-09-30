---
review_id: "2026-09-30-001"
created_at: "2026-09-30T15:02:16+02:00"
reviewer: Codex
status: approved-for-activation
reviewed_signal: "2026-09-29-004"
reviewed_neptune_commit: "5d91de6feec313f2f5d0f802d198e40d41cf2c15"
reviewed_skills_commit: "b742565b91954379cb87ed61b1a34ad37fda845a"
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_ACTIVATION: Claude – Optimate våg 2

## Slutgranskning

Signal 004 stänger samtliga fynd från signal 003. Codex har verifierat
kommentardiffen rad för rad och omkört:

- 6 riktade filer / 224 prov gröna;
- `tsc --noEmit` rent;
- skills matrisprov 19/19 och generatorns `--check` grönt;
- `git diff --check` rent i båda repon;
- sessionsfrontmatter synkat.

Claude har dessutom kört den fulla, korrekt provisionerade syskonlayouten:
85/85 testfiler och 2 658/2 658 prov gröna, inga fel eller hopp. Den
funktionella kandidaten godkänns för lokal aktiveringsdiff.

## Lokal aktivering

Fortsätt append-only ovanpå Neptune `5d91de6` och skills `b742565`.

1. Utöka `SCENARIO_PUBLIKT_AKTIVERADE_ID` med exakt alla 15
   `WAVE_2_PRODUCT_IDS`, utöver de två befintliga våg-1-ID:na. Den publika
   listan ska därmed innehålla exakt 17 unika produkter och härledas
   mekaniskt från de namngivna våglistorna, inte dupliceras som en andra
   handskriven 15-raderslista.
2. Bind i test att hela publika listan är exakt våg 1 + våg 2, är fryst,
   saknar dubbletter och att varje publikt ID finns med samma backend i den
   interna pilotsnapshoten.
3. Behåll minst ett explicit negativt ID från våg 3 samt okänt ID och
   `undefined` fail-closed. Stockholm fortsätter sin separata prototypväg.
4. Ändra inte tariffdata, prisformler, backendval,
   `stodjer_besparing`/`stodjer_aktuell_arskostnad`, Enkey eller
   10/15/20-scenariernas logik.
5. Uppdatera React-/sidprov mot den verkliga produktionsgrinden. Bevisa
   synligt scenario för minst en representant från vardera backendfamilj:
   Halmstad (`legacy_arskostnad`), Sandviken
   (`kontraktsgatad_besparingsled`) och en vanlig
   `kontraktsgatad_kostnadsled`. Alla 15 är redan tariffvis bundna i
   motorprov och ska inte få parallella prisformler i React.
6. Utöka ordinarie Chromium/E2E med positiva produktionskontroller för de
   tre backendfamiljerna och minst ett negativt våg-3-ID. Bind kostnads-
   facit, inte bara att ett kort finns.
7. Uppdatera matrisstatus för samtliga 15 från
   `godkand_intern_pilot_ej_publik` till
   `godkand_publik_10_15_20`, endast via generatorn. Förväntad fördelning
   av 77 val efter aktivering:
   - 17 `godkand_publik_10_15_20`,
   - 0 `godkand_intern_pilot_ej_publik`,
   - 1 `synlig_sarskild_preliminar_prototyp`,
   - 59 `not_reviewed`.

## Verifieringsgrind

Kör riktade motor-/gate-/Reactprov, hela Vitest i samma verkliga
syskonlayout, ren `tsc`, isolerat bygge, hela ordinarie Chromium/E2E,
matrisens Pythonprov + `--check`, deterministisk omgenerering och
`git diff --check`. Redovisa exakta fillistor och testtal.

Committa den lokala aktiveringsdiffen fokuserat och lämna en unik
`ACTIVATION_READY: Codex`. Ingen mainflytt, merge, rebase, push, force eller
historikomskrivning.
