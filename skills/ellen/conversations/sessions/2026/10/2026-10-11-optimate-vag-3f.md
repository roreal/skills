---
session_id: "2026-10-11-002"
started_at: "2026-10-11T19:47:10+02:00"
last_updated: "2026-10-11T19:47:10+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
  - Claude
status: active
topics:
  - Optimate
  - besparingspotential
  - våg 3f
  - Göteborg Energi
  - Partille Energi
  - Södertörns Fjärrvärme
  - temperaturdifferens
source: visible-conversation
transcript_fidelity: summarized
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3f — temperaturdifferens

## Start och beslut

Efter att våg 3e pushats, kvitterats och fjärrverifierats instruerade
Robert: **"Välj och starta nästa våg"**.

Codex inventerade de 24 återstående `not_reviewed`-produkterna. Tolv hör
till Wave 3 och tolv till den mer osäkra Vattenfall-familjen i Wave 4.
Nästa avgränsning blir exakt hela den återstående
`temperature_difference`-familjen:

- `goteborg-energi`;
- `partille-energi-partille`;
- `sodertorns-fjarrvarme-sodertorns-fjarrvarme`.

Gruppen är tekniskt sammanhållen genom samma befintliga tariffjustering,
men backendvalet förblir explicit: Göteborg använder den befintliga
legacy-årskostnadsvägen, Partille och Södertörn kontraktsmotorn. Endast
styrbar rumsvärme minskas; effekt, band och `avvikelse_c` låses. Det
prognostiseras alltså ingen separat returtemperatur- eller effektbesparing.

Live-baser före start:

- Neptune `origin/main=f13187af603ae131271331b5840f5ceb269dcaf0`;
- skills `origin/main=9487764ee64afa9df57b94bf22dfc337689e0dc1`.

Startdispositionen är **52 publika / 0 interna / 1 prototyp / 24
ogranskade = 77**. Målet för den interna, ej publika pilotleveransen är
**52/3/1/21=77**.

Se [implementeringshandoffen](../../../handoffs/2026/10/2026-10-11-optimate-vag-3f-temperaturdifferens.md).

Ingen publik aktivering, tariff-/formel-/UI-/Enkeyändring, mainflytt eller
push ingår i detta steg.

`APPROVED_FOR_IMPLEMENTATION: Claude`
