---
handoff_id: "2026-09-17-033"
created_at: "2026-09-17T16:17:16+02:00"
from: Codex
to: Claude
status: ready-for-implementation
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "isolated-neptune-unpushed-history-sanitization-candidate"
tariff_activation_allowed: false
branch_replacement_allowed: false
push_allowed: false
force_push_allowed: false
published_history_rewrite_allowed: false
isolated_candidate_history_reconstruction_allowed: true
enkey_or_skills_history_reconstruction_allowed: false
review_required_before_branch_replacement: true
review_required_before_push: true
required_heads:
  skills: "eb1c366f3945a0ae7ea8f15c7eb19675329052e4"
  enkey_agents: "47fdc67386b9db990d63c910069700b75301f743"
  neptune_academy: "bb28095cdd97d97bea615849bb132bdfbe4a4897"
required_live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
candidate_base: "22b473d30980051fb87a936b3d824c53b63d58e8"
candidate_tree_must_equal: "bb28095cdd97d97bea615849bb132bdfbe4a4897^{tree}"
expected_original_commits: 14
expected_candidate_commits: 13
relates_to:
  - "conversations/reviews/2026/09/2026-09-17-publiceringsgranskning-signal-031.md"
  - "conversations/sessions/2026/09/2026-09-17-batch-8-vattenfall.md"
---

# Uppdrag till Claude: isolerad sanerad Neptune-kandidat

## Mandat och absolut stoppunkt

Robert godkände uttryckligen Codex fråga om att låta Claude ta fram den
isolerade sanerade Neptune-kandidaten enligt publiceringsgranskning 032,
utan branchersättning eller push. Detta mandat gäller **endast** lokal
framtagning och verifiering av en kandidat för Neptunes ännu opushade
intervall
`22b473d30980051fb87a936b3d824c53b63d58e8..bb28095cdd97d97bea615849bb132bdfbe4a4897`.

Läs publiceringsgranskning 032 fullständigt innan arbetet börjar. Bevara
nuvarande branch, originalreferenser, originalcommits och arbetskopior.
Arbeta i en separat, isolerad worktree/kandidatref. En ny lokal kandidatref
är tillåten för att göra resultatet granskningsbart; aktuell branch får inte
flyttas eller ersättas.

**Stanna med en unik, committad toppost `REVIEW_READY: Codex`. Byt inte
aktuell branch, slå inte samman kandidaten, pusha inte någon ref, använd
inte force-push, aktivera inga tariffer och ändra inte Enkeys eller skills
produkthistorik.** Om en konflikt, oväntad patchrest eller annan avvikelse
kräver ett nytt tekniskt beslut ska arbetet stoppas fail-closed och signalen
vara `BLOCKED: Codex`.

## Exakt rekonstruktionskontrakt

Utgå från den verifierade Neptune-remotebasen `22b473d`. Rekonstruera de
14 lokala committarna i samma ordning och med samma sakliga patchar, med
endast följande historiksanering:

1. Lägg den redan granskade rättningen av de två kundidentifierande
   kommentarerna direkt i kandidatens motsvarighet till `89924b6`.
2. Lägg den redan granskade rättningen av den identifierande kommentaren i
   årsserietestet direkt i kandidatens motsvarighet till `eee1093`.
3. Bevara all exekverbar kod, alla facit och alla andra patchar.
4. Utelämna originalcommit `0bdb675` **endast om** hela dess patch därmed är
   absorberad och `git diff` visar att inget annat innehåll går förlorat.
5. Förväntat resultat är 14 originalcommits till 13 kandidatcommits. De nio
   senare sakpatcharna ska bevaras i ordning; deras hashar ändras naturligt
   genom de nya föräldrarna.

Originalordningen som ska mappas är:

1. `89924b6fb406466cd8c6624a462f217ee808bd28`
2. `3aa382ea705aa9d8274e2af76d2803924ab59ee7`
3. `eee10934ec3b16d26a6c2f271d0d337e797ee433`
4. `953f77a8fb9035cab4732bb842da5acbb6669054`
5. `0bdb6759bdbbb8785d0b716976b0483214282141` — förväntat absorberad
6. `5c1bd8821cc288204b5a7bfb466b918ff61403a5`
7. `0352117d36ca87149045c1517ac0cb1aca147723`
8. `eb48defec176d5f398e1ad76e0f632961ccc0cfd`
9. `f24333e413e997b5e34c1b1d62b15a5736ee8768`
10. `41dde169a789235f9ea38257196fa70fa10bde28`
11. `55069107a221e4eb4e6834b99d64e08ac30c96b1`
12. `190a0810d8b9d211df227039e406030238c59920`
13. `c29ae851850244e865b7ba10047f00dc2193c7c8`
14. `bb28095cdd97d97bea615849bb132bdfbe4a4897`

## Obligatorisk verifiering före leveranssignal

Leveransen ska minst redovisa och bevisa:

- full original–kandidat-mappning för samtliga 14 originalcommits, inklusive
  uttrycklig markering av den absorberade commiten;
- att kandidatens slutträd är byte-identiskt med trädet för `bb28095`;
- att varje kandidatsnapshot och varje kandidat-commitmeddelande har
  granskats mot de identifierande fragment som anges i 032, utan att dessa
  fragment återges i sessionsloggen;
- att originalbranchens namn och HEAD fortfarande är exakt `bb28095`, att
  originalcommits och remoter är bevarade och att ingen push har skett;
- full relevant TypeScript-, typkontroll-, build- och browsergrind för den
  isolerade kandidatens slutträd samt de externa katalog-/inventeringsprov
  som Neptune-flödet förutsätter;
- `git diff --check` för kandidatintervallet och rena produktarbetskopior;
- att disposition, katalogräkning och tariffaktiveringar är oförändrade.

Råa mejl/PDF:er, kund- eller kontaktuppgifter och befintliga orelaterade
arbetskopiefiler får inte läggas till, flyttas eller committas. Agentbryggans
filer får inte ändras.

Sessionsposten och topposten ska ange kandidatref och kandidat-HEAD, exakta
testresultat, mappningen och bevarade HEAD:ar. De ska uttryckligen säga att
kandidaten enbart väntar på Codex granskning och att branchersättning och
push fortfarande saknar tillstånd.
