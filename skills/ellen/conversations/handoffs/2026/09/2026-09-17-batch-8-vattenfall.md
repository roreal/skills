---
handoff_id: "2026-09-17-010"
created_at: "2026-09-17T10:03:40+02:00"
from: Codex
to: Claude
status: ready-for-implementation
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "batch-8-vattenfall-12-public-calculator-estimates-behind-gate"
tariff_activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
review_required_before_activation: true
review_required_before_push: true
required_parent_heads:
  skills: "55491dbfd92fcae2caf896f9a9457f1582d834c8"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "5c1bd8821cc288204b5a7bfb466b918ff61403a5"
tariff_disposition_before: "62 implemented / 2 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "62 implemented / 2 ready / 28 blocked av 92"
tariff_disposition_after_future_activation: "74 implemented / 2 ready / 16 blocked av 92"
relates_to:
  - "conversations/reviews/2026/09/2026-09-17-beredskapskontroll-batch-8-vattenfall.md"
  - "conversations/proposals/2026/09/2026-09-17-blockerade-tariffer-kallrevision.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 8 och daterad rättelse 2026-09-17"
  - "Fjarrvarmetariffer/tariffinventering-v22.md §8a"
---

# Uppdrag till Claude: Batch 8 — Vattenfalls tolv uppskattade årsprodukter

## Mandat och stoppunkt

Robert har gett fria händer att lösa de blockerade energibolagen. Codex
godkänner nu lokal implementation av de tolv Vattenfall-raderna bakom
deras befintliga spärr.

Läs beredskapskontroll `2026-09-17-010` fullständigt; den är bindande
för källmodell, tekniskt kontrakt, begränsningar, tester,
arbetskopieundantag och repo-HEAD:ar. Implementera hela det avgränsade
scopet, committa fokuserat i berörda repon och avsluta med en unik,
committad toppost `REVIEW_READY: Codex`.

**Aktivera inte de tolv raderna, pusha inte, skriv inte om historik och
ändra inte agentbryggan.** `investigation.status="utreds"` och
`production_ready=false` ska stå kvar på samtliga tolv rader. Stanna
efter granskningssignalen.

## Leveransens minsta innehåll

1. Rätta katalogmetadata och Vattenfallskällor enligt
   beredskapskontrollen. Bevara tidigare texter i daterad historik.
2. Skapa separata motorformer för sju månaders volymrabatt och
   kategoriskt flödesestimat. Återanvänd inte befintliga typer med annan
   semantik.
3. Bind abonnemangseffekt, Standard/Spetsig-behörighet, profil och
   flödesval genom en komplett `annual_forward`-policy per tariff.
4. Låt Vattenfalls profilval styra motorns faktiska tolvmånadersserie i
   båda språken. Bevisa 100-procentssumma och språkparitet.
5. Märk resultatet `estimated` och visa att kalkylestimatet utesluter
   överuttag och tillverkningsindustriavdrag samt använder 4 kr/m³ på
   båda sidor trots prislistans verkliga 4/6-regel.
6. Behåll `stodjer_aktuell_arskostnad=True` och
   `stodjer_besparing=False`; kr-läge och schablon får inte kringgå
   kontraktet.
7. Kör hela acceptansmatrisen, inklusive det oberoende Uppsala-facitet,
   isolerad tolvradsprojektion och fulla regressioner.

Råa mejl/PDF:er, kund- eller kontaktuppgifter och de lokala
Vattenfallkopiorna ska inte committas. Den sanitiserade bedömningen av
Sundsvallssvaret är redan dokumenterad men ligger utanför Batch 8:s
produktdiff.

## Leveranssignal

Sessionsposten ska redovisa exakta slut-HEAD:ar, varje ändrad fil,
testantal, den isolerade räkningen och bevarade arbetskopieundantag. Den
ska uttryckligen säga:

> Batch 8 är implementerad lokalt bakom spärr för tolv Vattenfall-
> produkter. Ingen tariff är aktiverad, inget är pushat och ingen
> historik är omskriven. approved_by: Codex; executed_by: Claude;
> dispatched_by: agent-bridge. Väntar på Codex kodgranskning.
