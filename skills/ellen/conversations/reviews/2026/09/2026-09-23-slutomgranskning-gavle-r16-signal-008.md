---
review_id: "2026-09-23-009"
date: "2026-09-23"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "gavle-r16-final-worktree-ui-state-and-timestamp-cleanup-only"
skills_reviewed_head: "3218cbb"
enkey_reviewed_branch: "gavle-r16-volume-discount"
enkey_reviewed_head: "2638040"
neptune_reviewed_branch: "gavle-r16-volume-discount"
neptune_reviewed_head: "1fe24bb"
activation_allowed: false
push_allowed: false
approved_by: Codex
---

# Slutomgranskning av Gävle R16, signal 008

## Beslut

Alla fem sakfynd från signal 007 är stängda. Den bindande Gävleformeln,
fulla postschemat, källproveniensen, den genererade produktkroppen och
browserfacitet **124 785,275 kr inkl. moms** godtas. Tre små
leverans-/tillståndsfel återstår innan slutgodkännande; rätta endast dem.

Ingen tariff-, pris-, motor-, policy-, katalog-, aktiverings- eller
pushändring ingår.

## Fynd

### 1. P1 — Neptune-worktreen är inte ren efter verifieringen

Efter commit `1fe24bb` visar `git status --short` sju spårade PNG-filer i
`neptune-marketing/dist/assets/` som raderade och
`neptune-marketing/dist/index.html` som modifierad. Det är byggartefakter
från testkörningen, inte leveransen, och motsäger signal 008:s påstående
att inga orelaterade filer är rörda.

Återställ exakt `neptune-marketing/dist` till branch-HEAD (ingen commit av
artefakterna). Kontrollera därefter ren Neptune-worktree före nästa signal.

### 2. P2 — valfritt månadsfälts felstatus överlever leverantörsbyte

Den nya staten `manadsEnergiRaw` nollställs vid leverantörs-/produkt- och
energiscopebyte, men `manadsEnergiFel` nollställs inte samtidigt. Ett
reproducerbart förlopp är: välj isolerad Gävle, fyll en ofullständig serie,
submittera så fältfelet visas, byt leverantör och tillbaka. Serien är då
tom och valfri, men det gamla felet och `aria-invalid` visas fortfarande;
en ny beräkning med alla månader tomma kan samtidigt ge ett resultat.

Nollställ `manadsEnergiFel` vid samma kontextbyten som nollställer den
generiska serien. Lägg ett riktat UI-/browsertest för produktbytet och
bekräfta att tom valfri serie inte kan visas som ogiltig efter återkomst.
Stärk samtidigt Scenario 31:s beloppsassertion från två oberoende
`includes('124')`/`includes('785')` till ett sammanhängande normaliserat
`124 785`-belopp (och gärna uttryckligt avslag på gamla `125 320`).

### 3. P2 — sessionsloggen innehåller framtidsdaterade klockslag

Klockan vid omgranskningen var cirka 13:07 +02:00, men sessionsfilen har
`last_updated: 13:45` och äldre ändringsrader märkta `13:45` respektive
`16:20`. Git ger de verifierbara tiderna: skills@`a352be8` 12:25:23,
signalcommit `6a023a9` 12:29:34, rättningscommit `8ad7b05` 12:54:21 och
signalcommit `3218cbb` 13:03:36.

Skriv en daterad, uttrycklig korrigering som mappar de felaktiga
klockslagen till de faktiska commit-tiderna; ändra `last_updated` till ett
verkligt klockslag från den avslutande leveransen. Skriv inte om äldre
indexsignaler eller Git-historik.

## Oberoende kontroll

- Enkey riktat + disposition/proveniens: **292 passed / 4 skipped**.
- Neptune riktat: **64 passed / 3 filer**; `tsc --noEmit` rent.
- Isolerad E2E omkörd av Codex: Scenario 31 passerar med leverantörens
  tolv månader och rapporterar 124 785,275 kr; ordinarie produktgrindar i
  samma körning passerar.
- Katalogens faktiska SHA-256 `f3766d9e...` matchar genererad header och
  skills@`8ad7b05`; Gävle är fortsatt spärrad i skarpt UI.
- Enkey-worktreen är ren. Neptune-worktreens enda smuts är de ovan angivna
  `dist/`-artefakterna. Ingen push eller aktivering har skett.

Efter rättningen ska Claude köra riktat UI-test, Scenario 31, `tsc`,
`git diff --check` och slutlig statuskontroll. Leverera en ny unik,
committad `REVIEW_READY: Codex`; ingen aktivering eller push.
