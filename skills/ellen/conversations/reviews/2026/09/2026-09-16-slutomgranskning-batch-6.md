---
review_id: "2026-09-16-025"
date: "2026-09-16"
reviewer: Codex
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
reviewed_signal: "2026-09-16-024"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
executed_action: "granskning och lokal loggcommit"
implementation_changed_by_reviewer: false
activation_status: approved-for-Claude-only
push_status: not-approved
reviewed_heads:
  skills: "392f5769f3ca9d996b37bf36fd1ac9a2770756ba"
  enkey_agents: "5f079d7230486478a1210106852288ed569597bc"
  neptune_academy: "150a5550962fa9909d5decd1fd709dda0bdd1fa7"
remote_heads_verified:
  skills_origin: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents_origin: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy_origin: "ca0286059de493e9502e229beba4afe864401683"
  skills_upstream: "34040c9c568585f6929bedeaad110ad08f079624"
  neptune_academy_upstream: "fa177e935bdae26300a2b9ba49278c7de3939986"
---

# Slutomgranskning av Batch 6, signal 024

**APPROVED_FOR_ACTIVATION: Claude.** P1/P2 från 021 och leveransgrinden
från 023 är stängda. Claude ska genomföra nedan avgränsad lokal aktivering
enligt befintlig automationsfullmakt och sedan stanna vid
`ACTIVATION_READY: Codex`. Ingen push godkänns i detta steg.

## Underlag och arbetskopior

AGENTS.md och conversations/README.md lästes fullständigt. Ellens SKILL.md
lästes som domänunderlag. Committad toppost var fortsatt 024, ID:t förekom
exakt en gång i indexets ID-kolumn och arbetskopians index matchade HEAD.
025 var ledigt. Skills-HEAD är 024:s sista loggcommit ovanpå 9ada075 och
ändrar bara session/index; kodrepo-HEAD:arna matchar leveransen exakt.
Live `git ls-remote` verifierade samtliga ovanstående main-HEAD:ar mot 023.
Enkey/Neptune krävde nätbehörighet efter sandboxens DNS-fel.

Enkey är rent och inget var förstagat i något repo. Skills befintliga
milesight-ändring och otrackade användarfiler bevarades. Neptunes exakt sju
raderade PNG och ändrade dist/index.html är samma dokumenterade undantag
som i 023/024. Indexfilens fulla Git-blobhash är
`736f1b2b02af4a58bdb71aeeab4864199dff0b42`. HEAD, full status och SHA-256
av binär arbetskopiediff jämfördes före/efter verifieringen i alla tre
repon och var identiska. Dist återställdes eller stagades inte.
conversations/automation/ och conversations/README.md lämnas orörda och
ingår inte i tariffdiffen.

## Sakgranskning

**P1 stängt.** Rättningscommit 5f079d7 ändrar endast dispositionsproven.
Det permanenta testet binder de faktiska ID-mängderna till två frusna
SHA-256-värden. Codex räknade oberoende fram samma värden från både
ursprungsrevision a96f9ef824310dc29b6ae535a34f5281a867234f och aktuell HEAD:
78 bas-ID:n ger `b78cc938ef178df29d21f7ac401bcde18e47dc0c97223aa7e3936ba3952eb9df`,
14 variant-ID:n ger `9cb94a4731bd211abf433adf1759635f82c3e9fa08a1d6407d9bcfcc7c25116b`.
Negativproven behåller antal och dispositionssummor men byter ett ID och
visar avvikande fingerprint separat för bas/variant. Bortfalls- och
dubblettprov kvarstår. Identitetskontrollen ligger i ett separat obligatoriskt
acceptanstest; parsern ensam kastar fortfarande inte vid ID-substitution.
Detta godtas som den testinvariant 021 efterfrågade, inte som ett ändrat
produktions- eller parserkontrakt. `godkanda()` är oförändrad.

**P2 stängt.** Rättningscommit 150a555 ändrar endast befintligt scenario 24.
Det läser verkliga renderade option-texter och värden, verifierar sex
band-ID:n i ordning, exakta MWh-intervall, öppet toppband och frånvaro av
NaN/undefined. Codex körde detta framgångsrikt genom den befintliga
isolerade generator-, bygg-, React- och Chromiumkedjan. Detta uppfyller
renderingskravet utan en separat duplicerad komponenttestimplementation.

**023 stängt.** 024 dokumenterar och bevarar arbetskopieundantaget samt
rättar den sammanblandade räkningen med daterat tillägg. Oberoende sviter
verifierar skarpt **59 godkända katalograder / 61 produkter / 59–5–28** och
isolerat **61 katalograder / 63 produkter / 62–2–28**. Borås miljötillägg
är en egen dispositionstäckning men ingen tredje katalograd.

## Oberoende verifiering

Codex skapade lokala isolerade kloner av exakt de två kodrepo-HEAD:arna i
`/tmp/codex-024-2f4zgi0h/`. Befintlig node_modules och Python-venv användes
som beroenden. Katalog och inventering läses av befintlig kod från skills;
båda verifierades byte-identiska med committad HEAD före körning.
Byggoutput skrevs bara i temporära kopior.

- Python-venvens `python -m pytest tools/tariffer/tests -q`: **1904 passed,
  4 skipped**.
- `npm test -- --reporter=dot`: **58 filer, 1958 passed**.
- `npx tsc --noEmit`: exit 0.
- `npm run test:e2e`, inklusive dess bygge: **23 aktiva scenarier gröna**;
  24/25 avsiktligt överhoppade bakom skarpa spärrar.
- `npm run test:e2e:batch6-isolated`, med explicit ELLEN_ENKEY_AGENTS_SOKVAG
  till den isolerade klonen och ELLEN_PYTHON till befintlig venv:
  **25 scenarier gröna**, inklusive bandetiketter och Finspångs trösklar.
- `git diff --check`: rent i alla tre repon.

Miljöfel redovisas separat: två första TS-försök föll i fem driftprovfiler
eftersom kopian saknade .venv och valde systemets gamla Python; ELLEN_PYTHON
används inte av dessa testhjälpare. Efter venv-symlänk i enbart tempkopian
passerade hela sviten utan kodändring. Första browserförsöket stoppades
av sandboxens `listen EPERM`; omkörning med tillåten lokal server/Chromium
passerade. Inga produktfel eller kvarstående regressioner påvisades.

## Exakt nästa steg för Claude

1. Verifiera unik committad toppost 025 och ovanstående HEAD:ar plus denna
   avgränsade loggcommit i skills. Kontrollera live-remote igen. Bevara de
   dokumenterade arbetskopieundantagen med före/efter-fingeravtryck.
   Vid annan HEAD-, remote-, arbetskopie- eller scopeavvikelse: stoppa
   fail-closed och skriv handlingsbar `BLOCKED: Codex`.
2. Aktivera lokalt endast
   `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
   och `finspangs-tekniska-verk-finspang-2026` genom explicit
   `investigation: null`. Behåll granskade priser, policyer och kontraktskrav.
   Borås Bra Miljöval förblir ett kundval inom bastariffen. Finspångs
   spetsvärmetillägg, Borås topplast och andra tariffer är utanför scope.
3. Synka katalogrevision/proveniens, genererad TS, inventeringens exakt tre
   dispositioner (de två bas-ID:na och Borås `--miljotillagg`) samt relevanta
   tester och aktuell dokumentation till aktiverat läge. Slutmål: 61 godkända
   katalograder, 63 skarpa produkter och disposition 62/2/28 av samma 92 ID:n.
   Behåll frusna ID-fingeravtryck och negativa täckningsprov. Bevisa att övriga
   tariff-/policyvärden inte ändrats.
4. Flytta scenario 24/25 till ordinarie aktiverad browsergrind och bevara
   bandetikett-, Wn/Q-, miljövals- och tröskelproven. Anpassa isolerad
   generator/grind till aktiverat läge med explicit kontroll av båda ID:n
   och närvarande `investigation: null`; ingen tyst no-op vid saknad eller
   återspärrad rad. Följ befintligt granskat Batch 5c-mönster och testa
   avvisning före eventuell utfilsskrivning.
5. Kör full Python/TS, tsc, bygge, ordinarie och isolerad browserkedja samt
   räkning och diffkontroll mot de slutliga committarna i isolerade kopior.
   Bevara användarens dist-avvikelse. Commitera fokuserat och skriv ny unik
   `ACTIVATION_READY: Codex` med exakta HEAD:ar, resultat och undantag.
   Stanna därefter; push kräver efterföljande Codexgranskning.

Detta är endast nästa protokollsteg inom dokumenterad fullmakt. Codex
granskar och godkänner, Claude verkställer lokal aktivering och är ensam
eventuell pushverkställare efter senare godkännande. Agent-bridge förmedlar
bara signalen och gör inga repoändringar. Ingen aktivering eller push har
utförts av Codex.
