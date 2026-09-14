---
review_id: "2026-09-14-011"
date: "2026-09-14"
reviewer: Codex
status: approved-for-local-implementation-behind-gate
scope:
  - "Batch 4:s avslut och faktiska remote-huvuden"
  - "Batch 5a i Fjarrvarmetariffer/batchplan-v22.md"
  - "Åtta annual_forward-tariffer med leverantörens effekt och bekräftade band"
baseline_heads:
  skills: "13b2a4ffc4520b7ebaca10eaa2efe0eb548259ff"
  enkey_agents: "5d498cfab3f968af42ba60751b5143c6f96536e0"
  neptune_academy: "ebe4d621ff800cab1f8248cd8e4e07ba042064fd"
implementation_changed_by_reviewer: false
implementation_status: approved-locally-behind-existing-investigation-gates
activation_status: not-approved
push_status: not-approved
tariff_disposition_before: "37 implemented / 27 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "37 implemented / 27 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "45 implemented / 19 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
---

# Beredskapskontroll: Batch 5a — leverantörens effekt och band

## Beslut

**Batch 4 är stängd och Batch 5a är godkänd för lokal implementation bakom de
åtta befintliga `investigation.status="utreds"`-spärrarna.** Alla tre faktiska
remote-huvuden verifierades med `git ls-remote`: `skills@13b2a4f`,
`enkey-agents@5d498cf` och `neptune_academy@ebe4d62`.

Batch 5a omfattar exakt:

1. `c4-energi-kristianstad-2026`
2. `kils-energi-kil-2026`
3. `skovde-energi-skovde-2026`
4. `trollhattan-energi-trollhattan-2026`
5. `tekniska-verken-katrineholm-katrineholm-2026`
6. `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`
7. `soderhamn-nara-soderhamn-taxa-11-och-12-2026`
8. `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`

Ingen ny beräkningsformel behövs. Befintlig `selected_band_affine`, tolv
energipriser, momsbehandling och band-ID-bindning räcker. Implementationen ska
ge uppskattad årskostnad i MWh-läge (`annual/snapshot/complete`), inte exakt
faktura, månadsfakturagaranti, kronor, schablon eller besparing.

## Källbedömning 2026-09-14

Aktuella officiella 2026-sidor/dokument verifierar de lagrade prisbeloppen:

- C4:s sida, uppdaterad 4 september 2026, visar 427/612 kr/MWh,
  effektformlerna och fortfarande den tvetydiga gränsen `200–499`/`>500`.
- Kils officiellt länkade femsidiga 2026-PDF är byteidentisk med användarens
  underlag (SHA-256 `d8bb87ca…b6e32`) och dess flerbostadsexempel bekräftar
  `fixed=0` samt `variable × E`; katalogens dokumenterade momsbesked ska
  fortsatt styra `vat_basis="included"`.
- Skövdes aktuella sida anger priser inklusive moms; katalogens värden är
  exakt dessa belopp dividerade med 1,25.
- Trollhättan, Tekniska verken Katrineholm, Öresundskraft Totalvärme och
  Söderhamn visar direkt de lagrade 2026-priserna och effektformlerna.
- TEMAB:s officiella 2026-PDF (SHA-256 `c4a1ac3b…a5e8`) anger juridiska
  personers priser exklusive moms, de tre taxorna, 832 kr/MWh och
  kalenderdagsperiodisering.

Historiska 2025-källposter får bevaras som historik men ska inte ensamma bära
proveniensen för 2026-värden. Handoffens källtabell anger vilka aktuella
officiella källor som ska frysas eller uppdateras innan aktivering.

## Rättad bandregel

V22 innehöll en lokal motsägelse som är rättad i samma dokumentationscommit.
Samtliga åtta katalograder har
`capacity.band_selection="supplier_confirmed_band_id_required"`. Därmed ska:

- ett känt, bekräftat band-ID välja prisraden direkt;
- saknat, tomt eller okänt ID blockera;
- `_niva()` och maskinellt tolkade `source_interval` aldrig överpröva
  leverantörens bandbesked.

Det sista är särskilt viktigt vid C4:s 500 kW: bindningen finns för att ett
leverantörsbesked ska kunna lösa en publicerad gränstvetydighet. Att kräva att
bandet samtidigt matchar parserns egen tolkning skulle återinföra den
automatiska gissning som §6a.2 uttryckligen avskaffade.

## Räknings- och leveransgrind

Under implementationen ska katalogen fortsatt ha 86 fysiska poster,
`godkanda(katalog, policyregister=POLICYREGISTER)` vara 37 och den skarpa
payloaden ha 39 produkter totalt. Ingen Batch 5a-produkt får läcka ut.

En isolerad kopia med exakt de åtta spärrarna rensade, R05/R12/R13 hanterade
enligt handoffen och de åtta nya policyerna ska ge 45 katalogprodukter. Den
framtida, separat granskade aktiveringen ska ge **45/19/28 av 92** och 47
skarpa produkter totalt. Ingen aktivering och ingen push är godkänd nu.

Den bindande implementerings- och testordern finns i handoff
`2026-09-14-002`.
