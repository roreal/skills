---
handoff_id: "2026-09-17-036"
created_at: "2026-09-17T18:28:11+02:00"
from: Codex
to: Claude
status: ready-for-implementation
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "local-neptune-main-ref-replacement-with-preserved-backup"
branch_replacement_allowed: true
push_allowed: false
force_push_allowed: false
tariff_activation_allowed: false
published_history_rewrite_allowed: false
required_heads:
  skills: "55f7f44c4ef8e1da1a309dd68fd33465c81bc967"
  enkey_agents: "47fdc67386b9db990d63c910069700b75301f743"
  neptune_main_before: "bb28095cdd97d97bea615849bb132bdfbe4a4897"
  neptune_candidate: "92226dbf16d705365cf9d9d3b52e763dadfad1b5"
required_live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
required_backup_ref: "refs/heads/neptune-batch7-history-original-backup"
operational_pause_at: "2026-09-18T08:00:00+02:00"
safe_mutation_cutoff: "2026-09-18T07:45:00+02:00"
relates_to:
  - "conversations/reviews/2026/09/2026-09-17-granskning-neptune-historiksanering-signal-034.md"
  - "conversations/handoffs/2026/09/2026-09-17-neptune-historiksanering-kandidat.md"
---

# Uppdrag till Claude: lokal Neptune-mainflytt till sanerad historik

## Uttryckligt mandat och stoppunkt

Robert godkände Codex exakta fråga om att skapa en lokal säkerhetsref vid
`bb28095` och flytta lokala Neptune `main` till den tekniskt godkända,
sanerade kandidaten `92226db`, fortfarande utan push.

Läs granskning 035 fullständigt. Verifiera samtliga obligatoriska HEAD:ar,
rena produktarbetskopior och live-remoter på nytt innan någon ref ändras.
Stoppa fail-closed med `BLOCKED: Codex` vid minsta avvikelse.

Utför sedan endast följande i `neptune_academy`:

1. Skapa den nya lokala säkerhetsrefen
   `refs/heads/neptune-batch7-history-original-backup` exakt vid
   `bb28095cdd97d97bea615849bb132bdfbe4a4897`. Refnamnet ska vara ledigt
   före operationen; skriv inte över en befintlig ref.
2. Verifiera åter säkerhetsrefen, kandidatrefen och identiska slutträd.
3. Flytta atomiskt endast lokala `refs/heads/main` från förväntat gammalt
   värde `bb28095cdd97d97bea615849bb132bdfbe4a4897` till exakt
   `92226dbf16d705365cf9d9d3b52e763dadfad1b5`, med det gamla värdet som
   compare-and-swap-villkor. Ingen reset eller checkout med filändringar.
4. Verifiera att `HEAD` fortfarande är `main`, att dess nya commit är
   `92226db`, att index och arbetskopia är rena, och att slutträdet är
   oförändrat. Bevara både kandidatrefen och säkerhetsrefen.

**Pusha inte någon ref, använd inte force-push, ändra inte remoter, aktivera
inga tariffer och ändra inte Enkey, produktfiler, katalogdata eller
agentbryggan.** Avsluta med en unik, committad toppost
`REVIEW_READY: Codex` som redovisar före/efter-refvärden och nya
live-remotekontroller. Branchflytten är en lokal förberedelse, inte ett
pushgodkännande.

## Planerad paus den 18 september

Robert sätter datorn i viloläge omkring **2026-09-18 08:00 Europe/Stockholm**.
Detta korta refsteg ska slutföras och lämnas vid en committad kontrollpunkt
nu. Ingen mutation eller push får påbörjas efter säkerhetsgränsen 07:45.
Om uppdraget av någon anledning inte kan vara helt avslutat före gränsen,
stoppa utan ytterligare repoändring och skriv en committad
`BLOCKED: Codex`.

Viloläge får aldrig tolkas som att en pågående körning är klar. Efter
återupptagande ska HEAD:ar, arbetskopior, remoter och senaste unika signal
verifieras innan automationen återstartas. Agentbryggan är lokal runtime
och antas inte ha överlevt viloläget.
