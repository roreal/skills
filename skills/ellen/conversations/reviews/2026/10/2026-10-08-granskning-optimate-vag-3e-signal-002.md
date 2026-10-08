---
review_id: "2026-10-08-003"
created_at: "2026-10-08T09:25:37+02:00"
reviewer: Codex
subject: "Optimate våg 3e — granskning av intern Umeå-pilot"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Granskning av Optimate våg 3e, signal 002

Beräkningsfacit, bonus→avgift-brytpunkten, den oförändrade
kapacitetskostnaden, intern/publik separation och dispositionen
**51/1/1/24=77** ser riktiga ut. Codex omkörde Wave-3e-proven
**37/37 gröna**, skills-proven **51/51 gröna**, matrisgeneratorns
`--check` samt `git diff --check` i båda reporna.

Leveransen kan ändå inte godkännas ännu. Tre bindande delar av handoff
2026-10-08-001 är inte mekaniskt bevisade.

## P1 — hela katalogmängden är inte låst

`WAVE_3E_PRODUCT_IDS` ska vara exakt hela katalogmängden med
`asymmetric_flow_difference`. Generatorn itererar bara den namngivna listan
vid `generera_besparingspotential_tackningsmatris.py:619`; den bygger aldrig
motsvarande mängd ur samtliga matrisrader, trots kommentaren ovanför
konstanten. Neptune-provet kontrollerar på samma sätt bara att Umeå-raden har
typen, inte att ingen annan katalograd har den.

Codex reproducerade felet genom att låta en andra katalograd
(`partille-energi-partille`) rapportera
`adjustment_types=['asymmetric_flow_difference']`: `build_matrix()` slutfördes
ändå med 77 produkter (`GLOBAL_SET_FAIL_OPEN`).

Rätta båda sidor så att den härledda katalogmängden jämförs exakt med
`WAVE_3E_PRODUCT_IDS`, och lägg ett negativt prov där en andra produkt får
typen.

## P1 — de råa policybindningarna är fail-open

Matrisgrinden jämför härledda `required_policy_fields` och `history_fields`,
men läser inte de tre råa policybindningarna. Codex muterade var och en av

- `policy.kapacitet_bindning`,
- `policy.kapacitet_band_bindning`, och
- `policy.kapacitet_multiplikator_bindning`

till `fel_nyckel`; `build_matrix()` accepterade samtliga mutationer
(`BINDING_FAIL_OPEN`). Neptune-proven binder A och band vid
`optimateScenarioVag3e.test.ts:187–188` och `:324–325`, men saknar helt en
assertion för `kapacitet_multiplikator_bindning`. Att B finns bland
`kravda_falt` är inte samma sak som att kapacitetsmotorn binder till B.

Låt skills-grinden kontrollera exakt de tre råa bindningarna och lägg ett
negativt mutationsprov för var och en. Bind även Neptune-provet explicit
till B-nyckeln. Lås samtidigt B-fältets råa kontrakt till `vardetyp=number`,
`matupplosning=arsvis` och det slutna intervallet `[0.93, 1.401]`.

## P1 — obligatoriska typade blockeringar saknas

Handoffens scenariogrind kräver typad blockering för saknat **och** ogiltigt
flöde, A, band, B och observerad period. Nuvarande prov täcker flöde, A och
ogiltigt band, men inte:

- saknat band;
- saknat eller ogiltigt B, inklusive värden utanför båda intervallgränserna;
- saknad eller ogiltig `kapacitetObserveradPeriod`.

Hjälparen `underlagMed()` lägger dessutom alltid till den giltiga perioden
när `kapacitetKw` finns, så dagens prov kan inte uttrycka de två sista
periodfallen. Utöka fixturen eller bygg de negativa underlagen explicit och
verifiera exakta typade orsaker/fält. Produktionen behöver bara ändras om
proven visar ett verkligt fail-open-beteende.

## Rättningsscope

1. Stäng de tre luckorna ovan med minimala generator-/teständringar.
2. Regenerera JSON/Markdown enbart om generatorns avsedda utdata ändras;
   dispositionen ska fortsatt vara **51/1/1/24=77**.
3. Kör riktade Wave-3e-prov, hela Vitest, ren TypeScript-kontroll, bygge med
   återställd `dist/`, skills pytest, generatorns `--check` och
   `git diff --check` i båda reporna.
4. Committera lokalt och lämna en ny unik `REVIEW_READY: Codex` med fulla
   hashar och testutfall.

Ingen tariff-, motor-, policyregister-, UI- eller Enkeyändring, ingen publik
aktivering, ingen mainflytt och ingen push.

`CHANGES_REQUIRED: Claude`
