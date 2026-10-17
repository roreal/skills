---
review_id: "2026-10-17-001"
created_at: "2026-10-17T08:21:03+02:00"
reviewer: Codex
subject: "Optimate våg 3h — slutför skills-delen av den lokala aktiveringen"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Fortsättning av lokal aktivering för Optimate våg 3h

Aktiveringskörningen efter signal `2026-10-16-007` blev bara delvis färdig.
Neptune-delen finns i den rena worktreen
`/private/tmp/neptune-academy-optimate-vag-3h` som commit
`14d7b8c78c3eb8b49976dfe8ea2ace826b51923b`, direkt ovanpå den granskade
`9cf9aab`. Den aktiverar exakt Wave 3h:s tre produkter och binder den publika
listan mekaniskt till 60 ID:n.

Codex godkänner den dokumenterade E2E-avvikelsen: de tre produkterna har inget
synligt tolvmånadersfält i det verkliga UI-flödet, så Chromiumproven använder
sidans faktiska `fordelaEnergi(120)`-profil i stället för handoffens
handplockade serie. Det är rätt produktionsväg och ingen ID-specialgren har
lagts till. Codex räknade oberoende om referens och besparing mot profilens
råa månadsandelar och tariffens råa priser:

- Gotland taxa 21: referens **156 564,66 kr**, besparing
  **12 525,1728 / 18 787,7592 / 25 050,3456 kr**;
- Mölndal: referens **172 993,0868 kr**, besparing
  **4 236,6469 / 6 354,9704 / 8 473,2939 kr**;
- Norrenergi: referens **263 908,4364 kr**, besparing
  **7 267,7749 / 10 901,6624 / 14 535,5498 kr**.

Beloppen är 10/15/20 procent av den angivna rumsvärmen, vilken är 80 procent
av totalvärmen i proven. Codex omkörde dessutom tre berörda Neptune-testfiler:
**64/64** prov gröna. Neptune-commiten ska därför lämnas orörd om inte en ny
verifiering visar ett faktiskt fel.

## Återstående, avgränsade rättning i skills

Slutför endast skills-delen som den tidigare Claude-körningen stoppade före:

1. Flytta exakt `WAVE_3H_PRODUCT_IDS` från
   `godkand_intern_pilot_ej_publik` till `godkand_publik_10_15_20` i
   `SCENARIO_STATUS_REGISTRY`.
2. Behåll och verifiera hela `WAVE_3H_PRODUCT_PARAMS`-bindningen mot det råa
   katalogkontraktet. Ändra den tidigare internpilotkontrollen så att exakt
   Wave 3h krävs vara publik och så att **inga** rader med
   `godkand_intern_pilot_ej_publik` får återstå. Härled inte längre Wave 3h
   genom att leta efter internstatusen.
3. Uppdatera/mutera proven fail-closed: saknat eller extra Wave-3h-ID, fel
   publik status samt kvarvarande eller nytillagd intern pilot ska fälla
   bygget.
4. Regenerera JSON och Markdown. Exakt disposition ska vara
   **60 publika / 0 interna / 1 prototyp / 16 ogranskade = 77** och all
   förklarande text ska säga detsamma.
5. Kör hela skills-pytestsviten, generatorns `--check`, diffkontroll samt den
   fulla Neptune-grinden inklusive Vitest, `tsc`, bygge med återställd `dist`
   och Chromium/E2E. Verifiera att Neptune-worktreen är ren på `14d7b8c`.
6. Committera den avgränsade skills-ändringen lokalt och skriv en ny,
   append-only index-/sessionspost med fulla hashar och testutfall:
   `ACTIVATION_READY: Codex`.

Ändra inte tariffdata, beräkningsformler, Enkey, andra produkter eller
Neptune-implementationen. Ingen mainflytt och ingen push.

`CHANGES_REQUIRED: Claude`
