---
review_id: "2026-10-08-005"
created_at: "2026-10-08T15:01:47+02:00"
reviewer: Codex
subject: "Optimate våg 3e — omgranskning av rättningsrunda signal 004"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Omgranskning av Optimate våg 3e, signal 004

De tre reproducerade fail-open-felen i granskning 003 är stängda:

- extra `asymmetric_flow_difference`-produkt blockeras nu av
  skills-generatorn;
- fel rå A-, band- eller B-bindning blockeras;
- B-kontraktet och de typade negativa scenarioproven för band, B och
  observerad period finns och går grönt.

Codex omkörde **43/43** Wave-3e-prov, ren TypeScript-kontroll,
**56/56** skills-prov, grön generator-`--check`, ancestry och
`git diff --check`. De tidigare reproduktionsskripten skriver nu
`GLOBAL_SET_BLOCKED` samt `BINDING_BLOCKED` för samtliga tre bindningar.

## P1 — den Neptune-sidiga globala katalogbindningen saknas fortfarande

Granskning 003 instruerade uttryckligen: ”Rätta båda sidor så att den
härledda katalogmängden jämförs exakt med `WAVE_3E_PRODUCT_IDS`”.
Skills-sidan gör nu detta korrekt. Neptune-sidan kontrollerar däremot
fortfarande bara:

- att `WAVE_3E_PRODUCT_IDS == ['umea-energi-umea-enkel']`; och
- att just Umeå-raden har `asymmetric_flow_difference`.

Inget Neptune-prov itererar alla poster i `TARIFFER` och jämför mängden
produkter som har justeringstypen med `WAVE_3E_PRODUCT_IDS`. Kommentarens
påstående att typen är unik i hela katalogen är därför fortfarande inte
bevisat i den repo där allowlisten används.

## Avgränsad rättning

1. Lägg ett Neptune-prov som härleder samtliga produkt-ID:n i den verkliga,
   checkade-in `TARIFFER`-snapshoten med
   `asymmetric_flow_difference` och jämför mängden exakt med
   `WAVE_3E_PRODUCT_IDS`.
2. Ändra ingen produktionskod, tariffdata, matris eller status.
3. Kör riktade Wave-3e-prov, hela Vitest, ren TypeScript-kontroll, bygge med
   återställd `dist/`, skills generator-`--check` samt diffkontroller.
4. Committera det enda testtillägget lokalt och lämna en ny unik
   `REVIEW_READY: Codex`.

Ingen aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
