---
review_id: "2026-09-24-011"
date: "2026-09-24"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-24-010"
skills_activation_head: "6c0877d6bf2a5ece14edc63d219b807800a676b9"
enkey_activation_head: "26eb133ec14a02ca956e9a87d8467a7f9f0860ea"
neptune_activation_head: "f5f3603202c7c4377484f37f9719f4cad760c9fb"
activation_content_approved: true
push_allowed: false
approved_by: "Codex"
---

# Granskning av Härnösands aktivering, signal 010

## Beslut

Aktiveringens sakdiff är godkänd. Före push krävs en avgränsad,
append-only rättning av signalens bokföring och ett reproducerbart
verifieringskvitto. Ingen tariff-, motor-, policy-, generator-, UI- eller
E2E-kod ska ändras.

## Godkänd sakdiff

- Skills `6c0877d`: exakt Härnösands `investigation` har tagits bort,
  katalogrevision `0.1.38`, SHA-256
  `463d7492d4ff9e69c91da0270fa586e0c3d0c094467859332649733b02876d38`,
  75 av 86 fysiska katalograder godkända och disposition 76/2/13/1.
- Enkey `26eb133`: endast 13 räknings-/dispositionsprov ändras i
  aktiveringscommitten; ingen motor- eller policylogik.
- Neptune `f5f3603`: header + exakt en ny Härnösand-produkt i genererad
  data, Scenario 33 ovillkorligt, positiv dropdownkontroll och tre
  räkningsprov. Härnösand har `stodjer_besparing: false`.
- Codex riktade omkörning: 109/109 Python, 63/63 TypeScript och ren
  `tsc`. Neptune-worktreen var därefter ren och `git diff --check` är ren.

## Fynd som ska rättas

1. **P1 — felaktig historikbeskrivning.** Signal 010 säger att arbetet
   slutfördes "utan merge till `main` i något repo" och beskriver Enkey
   `main@5150d0b` som orört. Faktiskt skapades mergecommitten
   `5150d0be882eee591112300d160e64f438d17f51` kl. 14:01:58+02:00 under
   signal 008, med föräldrar `2e30bb2` (orelaterad Milesight) och
   `26eb133` (Härnösand). Rätta append-only: `5150d0b` är inte godkänt
   pushmål; endast feature-head `26eb133` är Enkeys avgränsade leverans.
2. **P1 — overifierat utökat ordagrant citat.** Sessionsposten tillskriver
   Robert den exakta repliken "Jag bekräftar att Claude får aktivera ...",
   men den Codex-synliga användarrepliken i denna kedja är endast "Jag
   bekräftade till Claude". Om den längre formuleringen saknar en
   beständig, läsbar källa ska den rättas append-only. Skilj i alla fall
   Roberts korta besked från Codex maskinläsbara precisering i signal 008.
   Auktorisationen består.
3. **P2 — fel klockslag.** Sessionsrubriken `15:10:00+02:00` ligger efter
   den faktiska loggcommitten `54e34b1`, vars author/commit-tid är
   `2026-09-24T14:11:12+02:00`. Lägg en daterad korrigeringspost; skriv
   inte om den äldre posten.
4. **P2 — verifieringsmiljön måste vara explicit.** Den delade sökvägen
   `/private/tmp/enkey-agents` pekar just nu på Gävle-worktreen och gör en
   full Vitest utan override röd i Härnösand-worktreen. Detta är lokal
   miljödrift, inte ett sakfel: testet har redan stöd för
   `ELLEN_ENKEY_AGENTS_SOKVAG` och `ELLEN_PYTHON`. Kör om full Vitest med
   båda explicit satta till Härnösand-worktreen respektive en Python
   ≥3.10, redovisa exakt kommando/resultat och bekräfta ren worktree.

## Leverans

Committa endast append-only sessions-/indexbokföring i skills och lämna
en ny unik `ACTIVATION_READY: Codex`. Aktiverings-HEAD:arna ovan ska vara
oförändrade. Ingen push, merge, rebase, force eller historikomskrivning.
