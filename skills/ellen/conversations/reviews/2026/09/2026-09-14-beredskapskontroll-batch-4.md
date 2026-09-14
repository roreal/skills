---
review_id: "2026-09-14-003"
date: "2026-09-14"
reviewer: Codex
status: approved-for-local-implementation-behind-gate
scope:
  - "Batch 4 i Fjarrvarmetariffer/batchplan-v22.md"
  - "Tre Jämtkrafttariffer med flow_difference"
  - "Umeå Energi Enkel med asymmetric_flow_difference och leverantörsvärdet B"
baseline_heads:
  skills: "8b12daa9cbdb3f392bc6a5d20a32ae6f89f6c2b3"
  enkey_agents: "49f09078e6ed0acb0a7c05a104694110cf59b3e2"
  neptune_academy: "5e0d710f993b1058cf39c652eb45d171ca766406"
implementation_changed_by_reviewer: false
implementation_status: approved-locally-behind-existing-investigation-gates
activation_status: not-approved
push_status: not-approved
tariff_disposition_before: "33 implemented / 31 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "33 implemented / 31 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "37 implemented / 27 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-4-jamtkraft-umea.md"
---

# Beredskapskontroll: Batch 4 — Jämtkraft och Umeå

## Beslut

**Godkänd för lokal implementation bakom befintliga `investigation.status="utreds"`-spärrar.**
Källunderlaget räcker för uppskattad årskostnad i MWh-läge för exakt fyra produkter:

1. `jamtkraft-ostersund-froson-as-2026`
2. `jamtkraft-brunflo-och-opevagen-2026`
3. `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
4. `umea-energi-umea-enkel-2026`

Ingen extern leverantörsfråga behöver lösas före implementationen. Ingen av de fyra får
aktiveras och inget repo får pushas i denna etapp. Efter fokuserade lokala commits ska
Claude stanna för Codex kodgranskning.

## Källbedömning

Jämtkrafts officiella prisändringsmodell 2026–2028 anger 2026 års energi- och
effektpriser, debiterbar effekt som medelvärdet av de tre högsta dygnsmedeleffekterna samt
flödeskomponenten för oktober–april. Referensen är 19 m³/MWh och priset 3 kr/m³. Det
publicerade exemplet med 118 MWh och Q/W 17 ger 708 kr bonus, vilket överensstämmer med
`3 × (Q − 19 × W)` när bonus bokförs som en negativ justering.

Katalogens `15_0` pekar däremot på ett historiskt 2025-dokument trots att de lagrade
priserna är 2026 års värden. Implementationen ska därför frysa den officiella
2026–2028-PDF:en som en ny, oföränderlig källa `15_1`, med verklig SHA-256,
hämtningstidpunkt och verifierade sidreferenser. `15_0` ska bevaras historiskt men inte
längre vara priskälla för de tre 2026-raderna.

Umeå Energis officiella Enkel-sida och prisvillkor anger `(k × A + m) × B`, de sju
effektbanden, energiavgifterna, B-intervallet och en årsvis flödespremie för hela perioden
1 oktober–30 april. Referensen är 17 m³/MWh; lägre flöde ger 3 kr/m³ bonus och högre flöde
7 kr/m³ avgift. Katalogens aktuella officiella webbkällor
`web-review-umea-enkel` och `web-review-umea-terms` kan behållas, men deras
hämtning/proveniens ska återverifieras i leveransen. Kalkylatorn ska ta leverantörens redan
beräknade `B`, inte försöka beräkna normalårskorrigerad `U`.

## Arkitekturvillkor

- Lägg till de två justeringstyperna snävt i Python och TypeScript. Flödet är ett enda
  aggregerat m³-värde för oktober–april; energin summeras endast över månaderna
  `[1,2,3,4,10,11,12]`.
- Jämtkraft kräver tre policyfält: leverantörens debiterbara effekt, bekräftat band-ID och
  flöde 1 oktober–30 april. Batchplanens äldre tvåfältsformulering får inte användas för
  att kringgå katalogens `band_selection`.
- Umeå kräver fyra policyfält: leverantörens årseffekt `A`, bekräftat band-ID, flöde
  1 oktober–30 april och leverantörens faktor `B` inom `[0,93; 1,401]`.
- `kapacitet_multiplikator_bindning` finns redan i policytypen men måste transporteras
  till den verkliga kapacitetsmotorn i båda språken. Endast Umeås deklarerade
  `post_multiplier` får konsumera värdet.
- Den nakna `grind()` ska förbli strikt. `godkanda()` får göra det avgränsade tvåpass som
  beskrivs i V22: kvittera endast det exakta multiplikatoravslaget efter statisk
  policykontroll, ta bort endast `post_multiplier` i en kopia och kör hela ordinarie grind
  igen. Okänd issue, okänd justering eller annan multiplikator ska fortsatt blockera.
- `kontrollera_kompositgrind()` kontrollerar struktur, inte kundvärdet. `B=14` ska stoppas
  av kontraktsförkontrollen/`harled_resultatstatus`; den motsägande raden i
  `tariffinventering-v22.md` ska rättas.
- Vattenfalls blockerade `asymmetric_flow_difference` med dynamisk
  `reference_m3_per_MWh="network_average"` får inte öppnas av Umeås statiska formel.

## Räknings- och leveransgrind

Katalogen har redan 86 fysiska poster efter Batch 3b. Under denna etapp ska:

- `godkanda(katalog)` fortsatt ge exakt 33 katalogprodukter;
- den skarpa genererade leverantörslistan fortsatt ha 35 produkter totalt: 33 från
  katalogen och 2 befintliga leverantörsfiler;
- inga av de fyra Batch 4-ID:na finnas i den skarpa payloaden;
- en isolerad katalogkopia där exakt de fyra spärrarna rensas ge 37 katalogprodukter;
- dispositionen förbli 33/31/28 av 92.

Den fullständiga implementerings- och acceptansordern finns i handoffen ovan.
