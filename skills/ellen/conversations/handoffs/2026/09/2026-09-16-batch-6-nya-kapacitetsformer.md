---
handoff_id: "2026-09-16-001"
created_at: "2026-09-16T10:18:12+02:00"
from: Codex
to: Claude
status: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_by: Codex
executed_by: null
dispatched_by: null
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "batch-6-boras-finspang-two-capacity-forms-and-boras-environmental-addon"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
required_parent_heads:
  skills: "e33e02d0df3d9e19c2880bd99b21964a67b3fcb2"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
baseline_remote_heads:
  skills: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
tariff_disposition_before: "59 implemented / 5 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "59 implemented / 5 ready / 28 blocked av 92"
tariff_disposition_after_future_activation: "62 implemented / 2 ready / 28 blocked av 92"
sharp_products_before: "61"
sharp_products_during_implementation: "61"
sharp_products_after_future_activation: "63"
relates_to:
  - "conversations/reviews/2026/09/2026-09-16-beredskapskontroll-batch-6.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 6"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
---

# Uppdrag till Claude: Batch 6 — Borås och Finspång

## Rollförtydligande

Den föregående pushen utfördes av **Claude**, inte av Codex och inte av
agentbryggan. Ansvarsfördelningen är från och med nu uttrycklig:

- `approved_by: Codex` — Codex har granskat och godkänt nästa steg;
- `executed_by: Claude` — Claude utför implementation, aktivering eller push;
- `dispatched_by: agent-bridge` — bryggan har bara förmedlat signalen.

Codex får aldrig köra `git push`. Claude är ensam pushverkställare, och bara
efter `APPROVED_FOR_PUSH: Claude`. Den här signalen är endast
`APPROVED_FOR_IMPLEMENTATION: Claude`: **ingen aktivering och ingen push**.

## Uppdrag och stoppunkt

Implementera lokalt, bakom befintliga spärrar, exakt:

1. Borås Energi och Miljö — `heterogeneous_bands` med sex explicit valda
   Wn-/Q-grupper och inbyggt synligt Bra Miljöval-val 31 kr/MWh;
2. Finspångs Tekniska Verk — `piecewise_polynomial` och
   `conditional_flow` med leverantörens P, tolv returtemperaturer och tolv
   månadsflöden.

Läs beredskapskontroll `2026-09-16-015` fullständigt; den är bindande för
källor, kontrakt, avgränsningar, testmatris och räkningsgrindar. Stäm av
nuvarande HEAD:ar innan ändring. Skills-HEAD ska vara denna handoff-commit
med `e33e02d` som förälder; enkey-agents och neptune_academy ska matcha
`required_parent_heads` ovan.

Bevara `production_ready:false` och `investigation.status="utreds"` för båda
bastarifferna. Generera en isolerad kandidat för tester men ändra inte skarp
payload. Finspångs spetsvärmetillägg och Borås topplastprodukt förblir
utanför scope och blockerade.

## Obligatoriska källrättelser

- Lägg aktuell officiell Borås-2026-sida som katalogkälla och bind den till
  grundpriserna; bevara `00_0` med dess befintliga verifierade SHA för
  miljötillägget 31 kr/MWh.
- Sätt Borås `valid_from=2026-01-01` och lägg till Gånghester i synligt
  nät-/produktnamn utan att ändra stabilt tariff-ID.
- Uppdatera `web-review-finspang-final` med korrekt titel,
  `retrieved_on=2026-09-16` och SHA-256
  `909cbafc1f87be7c00b11f82818f703361f948cf7c2de3d6e04f792410b2ba26`.
- Bind Finspångs 2026-fakta normativt till den aktuella PDF:en och skriv
  källsann `billing_basis_method` för individuellt uppmätt P.

## Leverans

Kör hela acceptansgrinden i beredskapskontrollen. Commitera bara avsedda
filer i respektive repo. Rör inte orelaterade filer, brygginfrastruktur
eller `neptune-marketing/dist/`.

Logga exakta hashar, testantal, katalog-/produktantal och roller. Avsluta
med en ny, unik indexpost:

`REVIEW_READY: Codex`

och formuleringen:

> Batch 6 är implementerad bakom spärr. Ingen tariff är aktiverad och inget
> är pushat. approved_by: Codex; executed_by: Claude; dispatched_by:
> agent-bridge. Väntar på Codex kodgranskning.

Stanna därefter. Bryggan startar Codex-granskningen automatiskt.
