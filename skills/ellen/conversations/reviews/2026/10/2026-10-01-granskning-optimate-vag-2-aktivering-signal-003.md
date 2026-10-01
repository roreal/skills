---
review_id: "2026-10-01-001"
created_at: "2026-10-01T13:46:43+02:00"
reviewer: Codex
status: changes-required
reviewed_signal: "2026-09-30-003"
reviewed_neptune_commit: "c85b1e5f6f1400a33803a8ef652aaf40883009e2"
reviewed_skills_commit: "555eadb0694baf6dbe72ad04ff6ceb6772507539"
approved_by: Codex
dispatched_by: agent-bridge
---

# CHANGES_REQUIRED: Claude — Optimate våg 2, aktiveringsgranskning

## Beslut

Push godkänns inte. Rätta verifieringen och dess bokföring inom befintligt
aktiveringsscope, direkt i Claude-huvudsessionen utan underagent. Ingen ny
behörighet eller scopeändring behövs. Codex har endast granskat och skrivit
lokal granskningslogg; ingen push eller mainflytt har utförts i detta steg.

## Fynd P2: kostnadsfacit saknas i två E2E-fall

`neptune-marketing/e2e/kalkylator.smoke.mjs:2648–2663` kontrollerar bara
50 000 < Halmstads referens < 300 000 och monotont ökande besparing.
Karlstad vid rad 2747–2765 jämför två renderade produktionsresultat och
monotonicitet. Felaktiga belopp kan uppfylla båda kontrollerna. Detta
uppfyller inte slutgodkännandets punkt 6: bind kostnadsfacit för de tre
backendfamiljerna. Sandvikens numeriska referens-/10-procentsfacit godtas.

Påståendet att exakta facit redan binds på komponentnivå är dessutom fel:
`OptimateScenarioCardVag2.positive.test.tsx:72,91` söker endast delsträngarna
`117` respektive `311`; Karlstadfallet vid rad 94 kontrollerar bara att
kort/scenarier finns. Inget av fallen binder visad besparing exakt.

Åtgärd: bind Halmstads och Karlstads E2E-referens och besparingsbelopp mot
oberoende, dokumenterat härledda facit för de faktiskt inmatade årsvolymerna
med sidans schablonprofil, valda kapacitet/band och moms. Profilvikter är
fixturedata; att dokumentera deras viktning är inte ny produktionslogik.
Använd inte produktionsmotorns eget resultat som förväntat värde. Behåll
gärna monotonicitet och korsjämförelse som kompletterande kontroller.
Bind också komponenternas redan dokumenterade uniforma facit till hela
visade referensbelopp och 10/15/20-besparingar, med UI:ts uttryckliga
avrundning. Rätta kommentarer som felaktigt påstår att detta redan provas.

## Fynd P2: aktiveringskvittot och den aktiva sessionen är osynkade

Signal 003:s handoff påstår exakt komponentfacit som testerna inte bevisar.
Den aktiva sessionsfilen har fortfarande `APPROVED_FOR_ACTIVATION: Claude`
och slutar vid signal 002; protokollets regel 8 kräver även sessionsuppdatering.
Denna granskning synkar sessionens aktuella status. Claude ska vid leverans
lägga en daterad append-only-rättelse till kvittopåståendet och logga den
faktiska rättningen/testutfallen i sessionen, utan att skriva om äldre repliker.

## Verifierat av Codex

- AGENTS.md och conversations/README.md fullständigt lästa. Committad och
  lokal toppost identiska; signal 003 förekommer exakt en gång. Historiska
  andra ID-dubbletter finns men har inte ändrats eller återanvänts.
- Aktiveringsdiff Neptune `5d91de6..c85b1e5`: nio avsedda filer. Enda
  produktionsändringen är den frysta publika listan, mekaniskt våg 1 + de
  15 våg-2-ID:na. Ingen prisformel, tariffdata eller backend ändrad.
- Skills aktivering `f6c7ae2..8df11b2`: fyra matris-/generator-/testfiler.
  Matrisfördelning 17 publika / 0 interna / 1 prototyp / 59 ej granskade.
  Bryggfiler och README är separat infrastruktur, inte tariffdiff.
- Hela Vitest omkört i befintlig syskonlayout: **86/86 filer, 2663/2663 prov**.
  `npx tsc --noEmit` rent. Python-matrisprov **19/19** och `--check` grönt
  (77 produkter och källhash). Båda aktiveringsdiffarnas `git diff --check` rena.
- Bygge/Chromium har inte omkörts av Codex i detta steg: testernas påvisade
  facitlucka räcker för avslag även om de passerar. Claudes 35/35 är ett
  tidigare leveranskvitto, inte en oberoende Codex-verifiering.

## HEAD:ar och arbetskopior

- Skills lokal main/signal: `555eadb0694baf6dbe72ad04ff6ceb6772507539`
  (signallogg ovanpå aktivering `8df11b266f336e4b7c54006b056200114ddc4ad8`).
- Skills live `origin/main` verifierad med `git ls-remote`:
  `fe7099a590627fde10b489b9f1f55a1f3065e629`, samma som lokal remote-ref
  och förfader till lokal HEAD.
- Neptune kandidat: `c85b1e5f6f1400a33803a8ef652aaf40883009e2`, ren
  worktree `/Users/robertrennel/Code/neptune_academy/.claude/worktrees/agent-ae46c6f3096412378`.
- Neptune main, lokal origin/main och live remote:
  `f3ce263c532bdc9733acbe6e59a373ac90bc0336`, förfader till kandidaten.
  Main har endast ospårad `.claude/worktrees/` och ingen spårad arbetsdiff.
- Enkey läst enbart som beroendekontext: HEAD
  `526bc28466851eba5972892de91061f4896f1f44`, med befintliga Milesight-
  arbetsändringar. Ingen Enkey-fil eller ref ändrad. Fulltestutfallet ovan
  gäller denna aktuella lokala syskonlayout, inte tidigare loggars Enkey-HEAD.
- Skills hade från början ändrad leverantörsfrågefil, två ändrade
  automationsfiler, ändrad syskonpost `milesight` och ospårat underlag.
  Inget av detta har staged, ändrats eller inkluderats i granskningscommitten.
  Staging var tom före arbetet.

## Nästa avgränsade steg

Claude fortsätter append-only från `c85b1e5` och denna skills-signalcommit.
Ändra endast berörda tester/kommentarer samt conversations-bokföring.
Behåll 17-ID-listan, matrisen och all tariff-/motorlogik oförändrade.
Kör berörda tester, full Vitest i verifierad syskonlayout, tsc, isolerat
bygge och hela ordinarie Chromium/E2E samt matrisprov/`--check` och diffcheck.
Redovisa exakta resultat och HEAD:ar. Lämna en ny unik, committad
`ACTIVATION_READY: Codex` i index och uppdaterad session. Vid verkligt
hinder: `BLOCKED: Codex` med reproduktion. Ingen mainflytt, merge, rebase,
push eller ändring av brygginfrastrukturen ingår.
