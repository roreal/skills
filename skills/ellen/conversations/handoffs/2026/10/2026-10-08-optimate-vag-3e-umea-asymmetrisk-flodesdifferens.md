---
handoff_id: "2026-10-08-001"
created_at: "2026-10-08T08:57:54+02:00"
status: approved-for-implementation
signal: "APPROVED_FOR_IMPLEMENTATION: Claude"
requested_by: Robert
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
---

# Optimate våg 3e — Umeå Energis asymmetriska flödesdifferens

Robert har efter den fjärrverifierade Wave 3d-leveransen sagt **"OK dags
för nästa batch"**. Nästa minsta sammanhållna beroendeklass är exakt den
enda kvarvarande produkten med `asymmetric_flow_difference`:

- `umea-energi-umea-enkel`

Implementera den först som **intern, ej publik 10/15/20-pilot**. Den får
inte läggas i `SCENARIO_PUBLIKT_AKTIVERADE_ID` i denna etapp.

## Verifierad bas

- Neptune live `origin/main`:
  `d2976151749466258ea96ce987ca5f75ffbc392b`.
- skills live `origin/main`:
  `98f9d0e9652e2e9a337aa5a22c790974abb3082d`.
- Nuvarande disposition:
  **51 publika / 0 interna / 1 prototyp / 25 ogranskade = 77**.

Skapa en ny isolerad Neptune-worktree och gren direkt från den verifierade
live-basen. Återanvänd inte en äldre Wave 3-worktree.

## Tillåten implementation

1. Lägg ett fryst, namngivet `WAVE_3E_PRODUCT_IDS` med exakt ID:t ovan.
2. Lägg produkten explicit i den interna backendkartan som
   `kontraktsgatad_kostnadsled`.
3. Håll den helt utanför den publika allowlisten. Publik lista ska fortsatt
   vara exakt 51 unika, frysta ID:n; intern pilotsnapshot blir 52.
4. Flytta exakt Umeå-raden i skills-matrisen från `not_reviewed` till
   `godkand_intern_pilot_ej_publik`. Regenerera JSON/Markdown enbart via
   generatorn. Mål: **51/1/1/24=77**.

Ingen tariff-, motor-, policyregister-, UI-, Enkey- eller
produktkatalogändring tillåts. Den befintliga kostnadsmotorn och
kontraktsfasaden ska återanvändas oförändrade.

## Bindande scenariokontrakt

Endast månadens köpta energi och total MWh får ändras i efterfallen.
Följande referensvärden ska återanvändas identiskt i samtliga scenarier:

- leverantörens årseffekt `A`/`kapacitetKw`;
- bekräftat effektband;
- leverantörens kapacitetsfaktor `B`;
- den treåriga observerade kalenderperioden för `A`;
- `flode_okt_apr_m3`;
- övriga policyfält och produkt-ID.

Kapacitetsledet `(band.fast + band.rörlig × A) × B` ska därför vara
bit-identiskt före/efter. Ingen effektbesparing får tillskrivas Optimate.
Flödet hålls fast, men det asymmetriska kostnadsledet ska räknas om mot
efterfallets lägre oktober–aprilenergi:

```text
diff = flode_okt_apr_m3 − 17 × MWh_okt_apr
justering = 3 × diff när diff < 0
justering = 7 × diff när diff >= 0
```

Motorn får aldrig anta eller räkna fram `A`, `B`, band, period eller flöde.

## Oberoende brytpunktsfacit

Använd minst följande tabellstyrda fixture, där facit skrivs som literaler
och **inte** genereras genom `beraknaOptimateScenario`,
`beraknaArsprodukt` eller annan produktionsfunktion:

- Månadsenergi januari–december:
  `[18,16,14,10,6,3,2,3,6,10,14,18]` MWh, totalt 120 MWh.
- Styrbar rumsvärme: 80 procent av varje månad.
- `A=20 kW`, band `1`, `B=1,1`, observerad period
  `2023-01-01/2025-12-31`.
- `flode_okt_apr_m3=1600`.
- Energipriser:
  `[650,650,650,416,416,242,242,242,416,416,650,650]` kr/MWh.
- Effektled:
  `(21 + 1 018 × 20) × 1,1 = 22 419,10 kr`, oförändrat.

Förväntat exklusive moms:

| Scenario | Energi | MWh okt–apr | diff m³ | Flödesled | Totalt exkl. |
| --- | ---: | ---: | ---: | ---: | ---: |
| Referens | 67 248,00 | 100 | −100 | −300,00 | 89 367,10 |
| 10 % | 61 868,16 | 92 | 36 | 252,00 | 84 539,26 |
| 15 % | 59 178,24 | 88 | 104 | 728,00 | 82 325,34 |
| 20 % | 56 488,32 | 84 | 172 | 1 204,00 | 80 111,42 |

Förväntat inklusive moms: referens **111 708,875 kr** och besparing
**6 034,80 / 8 802,20 / 11 569,60 kr** vid 10/15/20 procent.

Fixturen är avsiktligt vald så att referensen använder bonusgrenen och
alla tre efterfall använder avgiftsgrenen. Ett fel som återanvänder
referensjusteringen, använder samma sats på båda sidor eller prövar tecken
månad för månad ska därför falla.

## Fail-closed-grindar

Bind både Neptune- och skills-sidan till exakt:

- `adjustment_types == ['asymmetric_flow_difference']` och inga extra led;
- justeringsparametrar `reference_m3_per_MWh=17`, `bonus_rate=3`,
  `fee_rate=7`, exakt månader `[1,2,3,4,10,11,12]`;
- `cost_path == 'kontrakt_arskostnad'`;
- `capacity_rule == 'effekt'`, exakt sju band;
- `required_policy_fields` exakt
  `{flode_okt_apr_m3, umea_enkel_arseffekt_a_kw,
  umea_enkel_kapacitetsfaktor_b, umea_enkel_vald_niva_id}`;
- `history_fields == ['umea_enkel_arseffekt_a_kw']`;
- `series_fields == []` och samtliga fyra fält `arsvis`;
- policybindningarna exakt A-, band- och B-nycklarna ovan;
- `B` inom det befintliga slutna intervallet `[0,93; 1,401]`.

Lägg negativa mutationsprov som minst fäller extra/fel justeringstyp,
fel/missad A-/band-/B-/flödesbindning, fel historikfält, extra seriefält,
fel upplösning och fel bandantal. Bevisa även att `WAVE_3E_PRODUCT_IDS`
är exakt hela katalogmängden med `asymmetric_flow_difference`; ingen annan
produkt får öppnas indirekt.

Scenario-/adapterproven ska typat blockera saknat eller ogiltigt flöde,
A, band, B och observerad period. Umeå ska vara sann i den interna grinden
men falsk i den publika.

## Leveransgrind

Kör minst:

- riktade Wave-3e-prov med det oberoende facit ovan;
- hela Vitest;
- `npx tsc --noEmit`;
- `npm run build`, därefter återställ enbart genererad `dist/`-smuts;
- skills pytest;
- matrisgeneratorns `--check`;
- `git diff --check` i båda reporna.

Committera lokalt, avgränsat. Ingen publik aktivering, mainflytt eller push.
Lämna en ny unik `REVIEW_READY: Codex` med fulla hashar, ancestry,
testutfall och disposition **51/1/1/24=77**.

`APPROVED_FOR_IMPLEMENTATION: Claude`
