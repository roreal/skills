---
review_id: "2026-09-25-006"
date: "2026-09-25"
reviewer: Codex
decision: "APPROVED_FOUNDATION"
signal_under_review: "2026-09-25-005"
skills_reviewed_head: "be8ef4d010debdb9867941ccb1021d37787e15a2"
neptune_reviewed_branch: "optimate-portfoljgrund-10-15-20"
neptune_reviewed_head: "1bfe1037063e1713dfbb54bfcc62d94b848b24f8"
activation_allowed: false
push_allowed: false
approved_by: "Codex"
---

# Slutomgranskning av Optimate-portföljgrunden, signal 005

## Beslut

Portföljgrunden godkänns. Den gemensamma motorn använder 10/15/20
procent, publik allowlist är tom och den regenererade matrisen beskriver
korrekt 76 verkliga produktval plus ett syntetiskt riksgenomsnitt.

Alla fynd i signal 004 är stängda:

- proveniensparsern avvisar nu både 41 hextecken och en giltig hash med
  efterföljande skräp;
- dubbla JSON-nycklar avvisas innan de kan skrivas över av parsern;
- okända status-ID:n och okända statusvärden avvisas;
- Stockholm-sluggen är konsekvent rättad till `sarskild`;
- JSON och Markdown visar samma per-produktstatus och statusfördelning.

Ingen publik aktivering eller push godkänns av detta beslut. Nästa
avgränsade steg är våg 1 enligt separat handoff 007.

## Oberoende kontroll

- Codex: **16/16** generatorprov gröna.
- `--check` och `git diff --check` gröna.
- Båda tidigare felaktigt accepterade provenienserna avvisas i direkt
  reproduktion.
- Matrisfacit oförändrat: 77 = 76 verkliga + 1 syntetiskt, 8/69 och
  vågor `1:2`, `2:15`, `3:48`, `4:12`.
- Neptune `1bfe103` är oförändrad. Codex fulla isolerade kontroll mot
  exakt `/private/tmp/enkey-agents-harnosand-2026` gav tidigare
  **75 testfiler / 2 410 test gröna** och gäller fortsatt eftersom
  rättningsrundan endast ändrade skills-matrisen.

## Bokföringsanmärkning

Sessionsrubriken `2026-09-25T09:35:00+02:00` i signal 005 är senare än
den verkliga commit-tiden. Den auktoritativa tiden för rättningscommitten
`be8ef4d` är `2026-09-25T09:26:26+02:00`. Den äldre raden skrivs inte om;
denna rättelse är append-only och ska användas i fortsatt bokföring.
