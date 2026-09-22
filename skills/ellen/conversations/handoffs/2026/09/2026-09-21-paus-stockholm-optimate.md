---
handoff_id: "2026-09-21-004"
created_at: "2026-09-21T16:08:49+02:00"
from: Codex
to: Robert och nästa arbetspass
status: paused
automatic_restart: false
push_allowed: false
force_push_allowed: false
skills_local_head: "a2a33acd250809bfb32a581e609365da65130fd0"
neptune_local_head: "a4eb519e06bed0eaaa62719b87ee9e330b071529"
---

# Paus: Stockholm Exergi och preliminär Optimate-potential

Robert bad 2026-09-21 att stoppa arbetet tills vidare och spara nuläge samt
det som återstår på Git. Ingen automatisk återstart eller bevakning har satts
upp för denna kalkylatorändring. Den isolerade förhandsvisningen på port 4174
är stoppad; ingen process lyssnade på porten vid pausens början.

## Bevarat läge

- Neptune-koden i `neptune-marketing/` innehåller två **opublicerade**
  deländringar ovanpå `main@a4eb519`: dels omfattningsrättningen så att
  enbart rumsvärme visas och summeras utan tappvarmvatten, dels den separata
  preliminära Optimate-vyn för Stockholm Exergi med 15/20/25 procent av
  styrbar rumsvärme och en villkorad effektkänslighet. Tariffens
  `stodjer_besparing=false` är oförändrad.
- Senaste verifiering: 2 270/2 270 TypeScript-tester, ren `tsc`, isolerat
  `dist-eval`-bygge och hela Chromium-E2E 1–29 gröna. `git diff --check`
  rent i både Neptune och skills. Spårad `dist/` är orörd.
- Metod och begränsningar står i
  `Fjarrvarmetariffer/stockholm-exergi-schablonunderlag-2026.md` och de
  opublicerade sessionsfilerna
  `2026-09-21-stockholm-rumsvarme.md` samt
  `2026-09-21-stockholm-optimate-potential.md`.
- Ingen commit, push, tariffaktivering eller ändring i Enkey har gjorts för
  dessa två deländringar.

## Git att göra vid återupptagning

1. Granska aktuell `git status` och diff på nytt; kontrollera att HEAD,
   beroenden och testresultat fortfarande gäller. Kör om relevanta tester
   om andra ändringar har tillkommit.
2. Gör en **avgränsad lokal Neptune-commit** med endast dessa åtta filer:
   `neptune-marketing/e2e/kalkylator.smoke.mjs`,
   `src/pages/KalkylatorPage.module.css`,
   `src/pages/KalkylatorPage.tsx`,
   `src/pages/KalkylatorPageStockholmBatch7.test.tsx`,
   `src/utils/stockholmExergiSchablon.ts`,
   `src/utils/stockholmExergiSchablon.test.ts`,
   `src/utils/stockholmOptimatePotential.ts` och
   `src/utils/stockholmOptimatePotential.test.ts` (alla `src/`-sökvägar
   relativt `neptune-marketing/`). Dela gärna i två commits: rumsvärmens
   omfattning och därefter besparingsvyn, men bara om diffarna går att
   separera utan att skapa ett mellanläge som inte bygger.
3. Gör en **avgränsad lokal skills-commit** med metodunderlaget, de två
   sessionsfilerna, denna handoff och de tre nya indexraderna. Kontrollera
   först att ingen rå kundidentifierare eller annan känslig uppgift har
   tillkommit. Håll separat från övriga ändringar i skills-arbetskopian.
4. Efter egen granskning och beslut om publicering: verifiera aktuella
   remoter och gör endast normal fast-forward-push av exakt godkända
   commits enligt projektets Git- och agentflöde. Ingen force-push.

**Ta inte med** orelaterade ändringar i `conversations/automation/`,
`Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`,
`skills/milesight`, ospårade PDF/EML/XLSX/källfiler, `AGENTS.md`,
`SKILL.md` eller spårad `neptune-marketing/dist/`. Dessa filer fanns redan
i arbetskopian och har inte hanterats inom kalkylatoruppdraget.

Nästa produktfråga efter publicering är validering mot verklig uppmätt
rumsvärme, dygns-/effektdata och komfortkrav. Nuvarande procentsatser är
endast scenarier, inte garanterade besparingar.

## Daterad statusrättelse 2026-09-22

Efter Roberts ”OK låter bra, kör!” återupptogs den avgränsade Git-uppgiften.
Exakt de åtta Neptune-filerna ovan är nu lokalt committade i
`86be35ae4c5e3f021c97c40d0473ab3d3427b127` efter 2 271 godkända
TypeScript-test, ren typkontroll, isolerat bygge och 29/29 Chromium-scenarier.
Neptunes arbetskopia var ren efter commit. Äldre text ovan beskriver det
verkliga läget **vid pausen**, inte det nuvarande Git-läget. Ingen push eller
tariffaktivering har gjorts. Aktuell portföljgranskning och fortsatt scope
finns i `conversations/reviews/2026/09/2026-09-22-arkitekturgranskning-besparingspotential-etapp-0.md`.
