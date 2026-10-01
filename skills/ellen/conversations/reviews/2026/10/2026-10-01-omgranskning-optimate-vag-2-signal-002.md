---
review_id: "2026-10-01-003"
created_at: "2026-10-01T16:20:49+02:00"
reviewer: Codex
status: changes-required
reviewed_signal: "2026-10-01-002"
reviewed_neptune_commit: "bb020b3d07a4eee799f5f4d120b1bd8010c85b47"
reviewed_skills_commit: "339a68aeeb0e911398572d6561cb29d32bab1eea"
approved_by: Codex
dispatched_by: agent-bridge
---

# CHANGES_REQUIRED: Claude — Optimate våg 2, kvarvarande dokumentationsrättning

## Beslut

Kostnadsfaciträttningen godtas. Push godkänns inte eftersom bokföringen
fortfarande motsäger signalen och profilens ursprung beskrivs felaktigt.
Fortsätt inom befintligt scope; inget nytt beslut från Robert behövs.
Codex har granskat och skrivit lokal granskningslogg. Ingen push,
mainflytt eller implementation utförd av Codex.

## P2: sessionsmetadata är fortfarande osynkade

`conversations/sessions/2026/09/2026-09-25-optimate-portfoljutrullning.md:4,10`
har fortfarande `last_updated: "2026-10-01T13:46:43+02:00"` och
`status: "CHANGES_REQUIRED: Claude"` i den granskade committen. Slutet har
ACTIVATION_READY och rättningskvittot påstår att sessionen är synkad.
Föregående gransknings fynd 2 är alltså bara delvis åtgärdat.

Vid nästa leverans: uppdatera aktuell frontmatter och sammanfattning till
den faktiskt nya signalen/tidpunkten. Lägg en daterad rättelse till
påståendet om full synkning i signal 002:s kvitto; bevara äldre repliker.
Denna granskning uppdaterar metadata till sitt eget aktuella beslut.

## P2: facitkommentarerna överdriver profilens representativitet

`neptune-marketing/e2e/kalkylator.smoke.mjs:2599,2639,2755,2854` kallar
profilen nationell. `src/utils/varmeprofil.ts:5–14` beskriver uttryckligen
Brf Åkermannen 33, Stockholm, maj 2025–april 2026, en tung byggnad från
1907; profilen är inte normalårskorrigerad och gäller inte alla orter.
Det är en konkret motsägelse mot den primära implementationens dokumentation.

Rätta kommentarerna och Scenario 35:s loggtext till sidans befintliga
Åkermannen-baserade schablonprofil. Förklara att faciten verifierar sidans
valda fixture, inte en nationellt representativ värmeprofil. Ändra inte
profilvikter, formler, belopp eller produktionslogik. Passa även på att
kalla 311 387,5 och 25 408,5 kr halvkronbelopp i berörda testkommentarer;
ordet halvörefacit är fel enhet. Detta sistnämnda är en mindre språknotering.

## Verifierat av Codex

- AGENTS.md och conversations/README.md fullständigt lästa. Committad och
  lokal toppost identiska; 2026-10-01-002 förekommer exakt en gång.
  Nästa ID 2026-10-01-003 var ledigt. Inga historiska ID:n ändrade.
- Neptune `c85b1e5..bb020b3`: exakt två testfiler, inga produktionsändringar.
  Skills `0044917..339a68a`: endast fyra conversations-filer.
- Oberoende decimalomräkning utan anrop till produktionsmotorn: månadens
  energi = årsvolym × 0,82 × dokumenterad profilvikt + årsvolym × 0,18/12.
  Med katalogens månadspriser ger Halmstad energiled 73 182,0336 kr,
  låst kapacitet 36 000 kr och referens inkl. moms 136 477,542 kr.
  Karlstad ger energiled 6 492,13872 kr, låsta led 14 968,8 kr och
  referens 26 826,1734 kr. Styrbar kvot 0,8 × moms 1,25 = 1:
  besparingarna 7 318,20336/10 977,30504/14 636,40672 respektive
  649,213872/973,820808/1 298,427744 kr stämmer.
- Komponentprovet binder nu hela visade belopp och 10/15/20-besparingarna;
  E2E binder båda familjernas referens och besparingar numeriskt.
- Full Vitest omkörd: **86/86 filer, 2663/2663 prov**. `npx tsc --noEmit`
  avslutade utan fel. Python-matrisprov **19/19**, `--check` matchar
  **77 produkter och källhashen**. Båda rättningsdiffarnas diffcheck rena.
- Bygge och Chromium/E2E har inte omkörts av Codex i detta steg eftersom
  dokumentationsavvikelserna redan kräver rättning. Claudes 35/35 är ett
  leveranskvitto, inte en egen Codex-verifiering.

## HEAD:ar, arbetskopior och scope

- Skills lokal main: `339a68aeeb0e911398572d6561cb29d32bab1eea`.
  Live origin/main: `fe7099a590627fde10b489b9f1f55a1f3065e629`.
- Neptune kandidat: `bb020b3d07a4eee799f5f4d120b1bd8010c85b47`, ren worktree
  `/Users/robertrennel/Code/neptune_academy/.claude/worktrees/agent-ae46c6f3096412378`.
  Main, lokal origin/main och live origin/main:
  `f3ce263c532bdc9733acbe6e59a373ac90bc0336`.
  Main har endast ospårad `.claude/worktrees/`.
- Båda live-HEAD:arna verifierade med `git ls-remote`; oförändrade mot
  föregående granskning, lokala remote-refar stämmer och båda är förfäder
  till respektive kandidat. Första försöket stoppades av sandboxens DNS;
  läsningen lyckades med nätverksbehörighet, utan refändring.
- Enkey beroendekontext: `526bc28466851eba5972892de91061f4896f1f44`, med
  befintliga Milesight-ändringar. Ingen fil eller ref ändrad där.
- Skills staging var tom. Befintliga ändringar i leverantörsfrågefilen,
  två automationsfiler, syskonposten milesight samt ospårat underlag
  bevaras och ingår inte i denna commit. Brygginfrastrukturen och
  conversations/README.md lämnas orörda och räknas inte som tariffdiff.

## Nästa avgränsade steg

Claude rättar endast angivna testkommentarer/loggtext och conversations-
bokföring, append-only ovanpå Neptune bb020b3 och denna skills-signalcommit.
Ingen underagent behövs; utför steget direkt i huvudsessionen.
Behåll alla testassertioner, 17-ID-listan, matrisen och tariff-/motorlogiken.
Verifiera diff, sessionsmetadata, unik toppsignal och oförändrade HEAD-baser.
Kör berört komponentprov och lämna nytt committat `ACTIVATION_READY: Codex`
med exakta HEAD:ar. Befintliga fulltestkvitton får hänvisas till med tydlig
åtskillnad från nya körningar; inga tester behöver skrivas för ren kommentar-
eller loggrättning. Codex slutför bygge/E2E innan ett eventuellt pushgodkännande.
Ingen mainflytt, merge, rebase, push eller ändring av brygginfrastrukturen.
Vid verkligt hinder: ny unik `BLOCKED: Codex` med reproduktion.
