---
review_id: "2026-09-12-016"
date: "2026-09-12"
reviewer: Codex
status: changes-required-before-push
scope:
  - "Rättning av P2-fynden i aktiveringsgranskning 2026-09-12-015"
  - "Slutgranskning av lokal Batch 1-aktivering före push"
reviewed_heads:
  skills: "257bb463eb5de85029ee2d8d6a5626dfaff2fc95"
  skills_catalog_commit: "82a247bbf028dfb8ed7b23ef976f1909256d0e92"
  enkey-agents: "a4cfdb297ea9079864e70c1e2d85c73a191e8c57"
  neptune_academy: "5eae7ce291682b1df96b6326a3c4bfe096278750"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
local_activation_status: correct-and-retained
push_allowed: false
tariff_disposition: "15 implemented / 49 ready / 28 blocked av 92"
follows_review: "2026-09-12-015"
---

# Slutgranskning av Batch 1-aktivering — rättningsrunda 1

## Beslut

**Changes required före push för en enda kvarvarande P2-kommentar.** Själva
aktiveringen, katalogdatan, beräkningsvägarna och de permanenta proven är korrekta.
Alla fyra sakfynd från granskning 015 är funktionellt stängda.

## P2 — Lidköping ligger fortfarande felaktigt i Batch 1-kommentaren

`neptune-marketing/src/utils/resultatkontrakt.batch1.test.ts:149–154` har fått rätt
testnamn, men kommentaren säger fortfarande att
”Karlstad, Södertörn, VänerEnergi, **Lidköping**, Partille” saknar heltalskravet.
`describe.each(BATCH1)` innehåller inte Lidköping. De fyra Batch 1-tariffer som saknar
kravet är Karlstad, Södertörn, VänerEnergi och Partille.

Detta var uttryckligen en del av granskning 015:s instruktion att inte blanda in
Sandviken/Lidköping i detta Batch 1-prov. Ersätt exakt kommentaren med exempelvis:

> de fyra Batch 1-tarifferna (Karlstad, Södertörn, VänerEnergi och Partille)
> som saknar kravet.

Ingen produktkod, katalog, genererad data eller testlogik ska ändras. Eftersom
rättningen bara är en kommentar behövs ingen ny full testkörning; kör riktat
TypeScript-test och `git diff --check`, logga den exakta diffen och stanna för en
snabb Codex-bekräftelse. Ingen push före den bekräftelsen.

## Stängda fynd från granskning 015

- Alla föraktiveringspremisser är omskrivna till korrekt dåtid.
- Alla sex tariffposter beskrivs nu korrekt som tariffgatade före aktiveringen;
  Telges medlemsnivåstatus blandas inte längre ihop med tariffstatusen.
- Direktprovet heter korrekt ”produkt-entryn” och påstår inte längre DOM-rendering.
- Månadsperiodiseringsprovet läser verklig genererad data och bekräftar både
  `manadsperiodisering === null` och `tackning=['annual_forward']` för de fyra.
- Band-ID:n använder `PolicyInputValue`; samtliga dubbla casts är borta.
- Sessionsloggen anger korrekt **700 passed, 4 skipped** och 704 insamlade fall.
- Katalogen är byteidentisk med `skills@82a247b`, SHA-256
  `b47502f1d02ccc483a99d20fb47ba866c8326197ef64051c36c51b024bc50f26`.

## Oberoende verifiering

- Python: **700 passed, 4 skipped**, 0 failed.
- TypeScript: **934 passed** i 28 filer, 0 failed/0 skipped.
- `npx tsc --noEmit`: godkänt.
- `npm run build`: godkänt; endast befintlig bundlevarning.
- E2E: samtliga **9** scenarier godkända.
- Katalogdisposition: fortsatt **15/49/28 av 92**.
- `git diff --check`: rent i samtliga tre repon.
- Genererade byggfiler återställda; produktrepona rena.
- Remote-HEAD är oförändrade; inget i denna aktiveringsrunda är pushat.

