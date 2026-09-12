---
review_id: "2026-09-12-023"
date: "2026-09-12"
reviewer: Codex
status: approved-for-local-implementation
scope: "Batch 3 — delad flödeskorrigeringsmotor för E.ON, Navirum och Kraftringen"
baseline_remote_heads:
  skills: "8cd8e6bdf61253d852719698bbd882a8109e393f"
  enkey_agents: "5da3b74cc7b4a22c4ce268b5d3670465bd68e4cc"
  neptune_academy: "297e4f04093dc68084dfa0f026ad9590155ba2b7"
implementation_allowed: true
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
expected_after_future_approved_activation: "25 implemented / 39 ready / 28 blocked av 92"
---

# Beredskapskontroll för Batch 3

## Beslut

Batch 2 är oberoende remote-verifierad och avslutad. Batch 3 är godkänd att starta som
en **lokal implementationsfas** enligt den separata arbetsordern
`conversations/handoffs/2026/09/2026-09-12-batch-3-flodeskorrigering.md`.

Godkännandet omfattar kod, katalogrättelser bakom kvarvarande spärr och tester för exakt
nio bastariffer. Det omfattar inte aktivering, regenerering av den skarpa
produkttariffilen eller push.

## Verifierat nuläge

- `git ls-remote origin refs/heads/main` matchar lokala HEAD i alla tre repon:
  `skills@8cd8e6b`, `enkey-agents@5da3b74`, `neptune_academy@297e4f0`.
- Batch 2-loggen är pushad; den avslutande `skills`-committen är verifierad separat av
  Codex mot remote.
- Aktuell disposition är **16/48/28 av 92**.
- De nio Batch 3-raderna är källgranskade och ligger i `ready_to_implement`; inget nytt
  leverantörsbesked krävs före implementation.
- Batch 0 har redan byggt den typade
  `flodeskorrigering_variant`/`flodeskorrigeringVariant`-diskriminatorn och det generiska
  policyformuläret. Batch 1 har byggt den obligatoriska band-ID-vägen. Batch 3 ska koppla
  dessa befintliga kontrakt till den nya motorn, inte skapa parallella specialvägar.
- Katalogens nio rader har fortfarande de avsiktliga luckorna `fixed:null`,
  `rate_period:null`, implementationsspärr och R06/R10. Malmö/Burlövs två rader har
  dessutom den felaktiga beräkningstemperaturen −15 °C i texten; den ska vara −8 °C.

## Avgränsningar som inte får tappas

- E.ON/Navirums åtta bastariffer gäller endast fullvärmekunder. De åtta
  bas-/delvärmevarianterna hör till Batch 3b och ändras inte nu.
- Kraftringens rad gäller endast ordinarie nät. Brunnshögs variant förblir blockerad.
- E.ON/Navirum använder den golvfria faktorn. Kraftringen använder den golvbegränsade
  faktorn; leverantörs-ID får aldrig användas som implicit regelval.
- En enda leverantörseffekt representerar den rullande grunden och ska därför ge
  `snapshot`, aldrig `exact`. Resultatet är uppskattad årskostnad.
- Endast bekräftad MWh stöds. Kronor, schablon och besparing förblir blockerade.

## Fasordning

1. Implementera lokalt och håll samtliga nio `investigation.status="utreds"`.
2. Codex granskar implementationen och de syntetiska/isoleringstestade produktvägarna.
3. Endast efter ett nytt uttryckligt godkännande får exakt nio spärrar samt R06/R10
   tas bort, skarp tariffdata regenereras och omockade UI/E2E-prov läggas till.
4. En ny Codex-granskning krävs före push.

Detta fasbeslut ersätter Batchplan V22:s otydliga placering av borttagningen av R06/R10:
de ska ligga kvar under implementationsfasen så att ingen tariff kan passera grinden av
misstag och inga `investigation.request_ids` blir hängande referenser.
