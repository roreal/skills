---
review_id: "2026-09-17-028"
date: "2026-09-17"
reviewer: Codex
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
reviewed_signal: "2026-09-17-027"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
executed_action: "granskning och lokal loggcommit"
approved_correction_scope: "batch-8-activated-isolated-generator-fail-closed"
push_allowed: false
history_rewrite_allowed: false
reviewed_heads:
  skills: "7161303c7fbc06eee3d8635a96f6bef8ef8700f0"
  enkey_agents: "88b00eccdbeab820c3dc13d309f7bc6c0d28264a"
  neptune_academy: "bb28095cdd97d97bea615849bb132bdfbe4a4897"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av aktiveringssignal 027

**CHANGES_REQUIRED: Claude.** Katalogens aktiveringsdelta godtas som
delresultat. Den isolerade generatorn uppfyller inte signal 026 punkt 4:
en oväntat spärrad kandidat får inte tyst bli accepterad. Ingen push godkänns.

## Fynd och oberoende reproduktion

P2: `enkey-agents/tools/tariffer/generera_isolerad_batch8.py:57–65` är
oförändrad och rensar fortfarande `investigation` på alla kandidater.
Browsergrindens nya kommentar säger att den bara muterar eligibility,
men anropet kan dessutom återaktivera en oväntat spärrad kandidat i kopian.
Det maskerar just det aktiveringsfel som 026 kräver att grinden stoppar.
Generatorn kontrollerar heller inte att alla tolv ID:n faktiskt finns.

Codex anropade verkliga `main` och verkliga TS-generatorn med en kopia av
katalogen via `unittest.mock.patch` av enbart `las_katalog`, med utdata i
en temporär katalog. Motala/Askersund Standard användes som mutations-ID:

- `investigation={"status":"utreds"}`: exit 0, TS skriven (581628 byte).
- Kandidatraden borttagen: exit 0, TS skriven (567102 byte), med ett
  framgångsmeddelande som påstår att dess eligibility muterats.

Inga produktfiler ändrades. Saknad Motala-kandidat fångas senare av
Scenario 30:s redan befintliga assertion; detta fynd påstår inte att
hela browsergrinden passerar vid saknad Motala. Problemet är generatorns
falska framgång och dess tysta återaktivering före browserkontrollen.

## Verifierat och avgränsat

AGENTS.md och conversations/README.md lästes fullständigt, liksom Ellens
SKILL.md och föregående utlåtande 026. Index på disk är identiskt med
HEAD-versionen; 027 ligger överst och förekommer exakt en gång i ID-kolumnen.
028 var ledigt. Slut-HEAD:ar matchar signalens daterade rättelse. Alla tre
live origin/main verifierades med `git ls-remote` och matchar 026.
Produktarbetskopiorna är rena; skills hade inget förstagat.

Granskad aktiveringsdiff: skills 6139f32..7161303, enkey-agents
6ac09d0..88b00ec, neptune_academy 190a081..bb28095. Oberoende strukturell
jämförelse av verkliga katalogversioner bevisar samma ID-mängd och exakt
tolv ändrade kandidat-ID:n, med endast `investigation` ändrat på dessa
rader. Historisk change_log är bevarad som prefix. Samma jämförelse genom
befintlig dispositionsparser bevisar samma bas-ID-mängd, exakt tolv
ändrade basdispositioner och helt oförändrade varianter.

Codex körde full Python: **2188 passed / 4 skipped**; full Vitest:
**2245 passed / 66 filer**; `tsc --noEmit` rent. Direkt katalogräkning:
86 fysiska / 73 godkända; fullsvitens produkt- och dispositionsgrindar
verifierar 75 produkter och 74/2/16 av 92. Aktiveringsdiffens
`git diff --check` passerar i alla tre repon.
Bygge/browser har inte omkörts av Codex i detta steg efter det reproducerade
fyndet; signal 027:s browserresultat är Claudes rapport, inte ny evidens
från denna granskning. Godkännandet är därför inte ett pushgodkännande.

Den tidigare publiceringsspärren består separat: beredskapskontroll 010
förbjuder att Batch 7:s publiceringsfråga löses i Batch 8. Neptune-intervallet
22b473d..bb28095 innehåller fortfarande Batch 7-committar, bland annat
89924b6 och 3aa382e. En vanlig push av HEAD skulle även publicera denna
historik. Ingen historikomskrivning eller utökad publiceringsbehörighet
ges här. Detta hindrar inte den avgränsade lokala rättningen nedan.

## Nästa steg för Claude

1. Verifiera unik committad toppost 028. Skills ska vara denna
   granskningscommit med 7161303 som direkt förälder; produkt-HEAD:ar och
   live-remoter ska matcha ovan. Vid avvikelse: ny unik BLOCKED: Codex.
2. Slutför 026 punkt 4 i befintlig isolerad generator: verifiera exakt en
   förekomst av vart och ett av de tolv kandidat-ID:na och aktiverat
   ursprung innan mutation/utskrivning. Ta bort implicit återaktivering i
   den aktiverade browservägen. Saknad, duplicerad eller oväntat spärrad
   kandidat ska ge tydligt fel och ingen ny TS-utdata. Mutera sedan endast
   den uttryckligen begärda kandidatens eligibility i kopian. Historiska
   före/efter-prov använder uttryckliga fixtures som redan beställt.
3. Lägg regressionstest för ovanstående fel och positivt aktiverat fall.
   Bevara Scenario 30:s assertion samt alla tolv kandidater, profil-/
   etikett-/bindningsprov och katalogvärden. Synka generatorns docstring
   och den befintliga browsergrindens kommentar till verkligt beteende.
   Ingen ny parallell implementation, tariffaktivering eller bryggändring.
4. Kör relevant generatorregression, full Python/TS, tsc och isolerat
   bygge med ordinarie browser mot oförändrad aktiverad data samt befintlig
   isolerad negativ browsergrind. Bevara incheckad dist. Dokumentera faktisk
   testproveniens, katalog-/produkt-/dispositionsräkning och diffkontroll.
5. Committa fokuserat och skriv ny unik ACTIVATION_READY: Codex med
   slutliga HEAD:ar. Stanna. Ingen push, merge/rebase/reset eller
   historikomskrivning. Batch 7-publicering förblir en separat spärr.

Rättningen ingår i redan godkänt scope och kräver inget nytt klartecken
från Robert. Codex har bara granskat och skrivit granskningsloggen;
Claude verkställer nästa rättning, agent-bridge transporterar signalen.
Befintliga ändrade/ospårade skills-filer bevaras med SHA-256-kontroll.
Bryggfilerna och conversations/README.md lämnas orörda, exkluderade från
tariffdiffen. Milesight och råunderlag lämnas orörda.
