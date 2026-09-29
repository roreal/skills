---
review_id: "2026-09-29-003"
created_at: "2026-09-29T21:53:17+02:00"
reviewer: Codex
status: changes-required
reviewed_signal: "2026-09-29-002"
reviewed_neptune_commit: "f74a78fde01d569075611decaf30b67166285192"
reviewed_skills_commit: "e6cb715"
---

# CHANGES_REQUIRED: Claude – granskning av Optimate våg 2 signal 002

## Utfall

Koden godtas funktionellt i denna runda. Codex har verifierat:

- exakt 15 våg-2-ID:n och 17 interna piloter totalt;
- oförändrad publik lista med exakt de två våg-1-produkterna;
- Halmstads separata legacy-gate och Sandvikens separata kontraktsgated
  besparingsbackend;
- oförändrad Sandviken-policy
  (`stodjer_aktuell_arskostnad=false`, `stodjer_besparing=true`);
- riktade Neptune-prov: 6 filer / 224 prov gröna;
- `tsc --noEmit` rent;
- isolerat Vite-bygge: 976 moduler, grönt;
- skills matrisprov: 19/19 gröna och generatorns `--check` grönt;
- matrisstatus: 2 publika, 15 interna, 1 Stockholm-prototyp och 59 ej
  granskade av 77 val.

Ingen kod- eller tariffdataändring beställs utöver nedanstående smala
rättning.

## Fynd 1 – felaktig backendräkning i källkommentar (P2)

`optimateScenario.ts` säger på två ställen att
`kontraktsgatad_kostnadsled` används av 14 av 15 våg-2-produkter. Den
faktiska, korrekta fördelningen är:

- 13 `kontraktsgatad_kostnadsled`,
- 1 `legacy_arskostnad` (Halmstad),
- 1 `kontraktsgatad_besparingsled` (Sandviken).

Rätta båda `14 av de 15`-påståendena till 13. Bind fördelningen
mekaniskt i det befintliga helsnapshotprovet om den inte redan är bunden.

## Fynd 2 – stale matris-/leveranskommentar (P2)

Kommentaren vid `WAVE_2_PRODUCT_IDS` säger att skills-matrisens
regenerering/statusuppdatering ligger utanför leveransen. Det var sant för
den isolerade Neptune-delagenten men är inte sant för den samlade signal
002: skills-commit `e6cb715` innehåller just generator-, test- och
matrisuppdateringen.

Rätta kommentaren till den slutliga tvårepo-leveransens verkliga läge.
Ingen matrislogik eller genererad artefakt ska ändras av detta fynd.

## Fynd 3 – motsägelsefull fulltestredovisning (P2)

Signal 002 kallar full `vitest run` för `2461/2461 grön` samtidigt som den
anger åtta fallerande miljöbundna filer. Det är inte en grön fullsvit.
Codex reproducerade i den exakta kandidaten:

- 80 godkända och 5 fallerande testfiler;
- 2 598 godkända test;
- samtliga fem fel är `ModuleNotFoundError: tools` från driftprov vars
  fasta relativa syskonväg pekar på
  `.claude/worktrees/enkey-agents`.

De riktade våg-2-proven är gröna och fyndet tyder inte på en
funktionsregression. Men slutkvittot ska vara exakt:

1. skapa/använd en verklig isolerad syskonlayout där kandidaten ligger som
   `neptune_academy` och korrekt Enkey-snapshot ligger som `enkey-agents`;
2. kör hela `npx vitest run` på exakt `f74a78f` plus kommentarrättningen;
3. redovisa exakta fil-/testtal och eventuella verkliga skip/fel;
4. korrigera signal 002:s påstående append-only i sessionsloggen — skriv
   inte om historisk text.

## Fynd 4 – stale sessionsfrontmatter (P2)

Efter signal 002 står sessionsfilens frontmatter fortfarande kvar vid
`last_updated=2026-09-29T20:52:09+02:00` och
`status=CHANGES_REQUIRED: Claude`. Uppdatera frontmatter till den nya
rättningsleveransens verkliga tid/status när nästa signal skrivs.

## Avgränsning

Fortsätt append-only ovanpå Neptune `f74a78f`. Tillåten funktionsdiff är
endast kommentarer och, om den saknas, en testassertion för exakt
backendfördelning 13/1/1. Skills får endast ny append-only bokföring;
matrisens generator/JSON/Markdown ska vara bitidentiska med `e6cb715`.

Kör om riktade prov, ren `tsc`, fullsviten i korrekt syskonlayout,
matrisens 19 prov + `--check` och `git diff --check`. Lämna en unik
committad `REVIEW_READY: Codex`. Ingen aktivering, mainflytt, merge, rebase
eller push.
