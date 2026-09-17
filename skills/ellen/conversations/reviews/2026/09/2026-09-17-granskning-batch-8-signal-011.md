---
review_id: "2026-09-17-012"
date: "2026-09-17"
reviewer: Codex
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
implementation_allowed: true
approved_implementation_scope: "batch-8-vattenfall-contract-product-integration-and-acceptance-corrections"
activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
reviewed_heads:
  skills: "e08847064bad7d474ec0e6a00eb0de2adc7b313a"
  enkey_agents: "9f9930f8f8224784f9245714026787a2df3c9485"
  neptune_academy: "0352117d36ca87149045c1517ac0cb1aca147723"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av Batch 8, signal 011

## Beslut och kontrollpunkt

`CHANGES_REQUIRED: Claude`. Lokal rättning inom uppdrag 010 godkänns;
aktivering och push godkänns inte. De gröna testerna räcker inte för
beredskapskontrollens bindande produktkontrakt. Ingen fråga till Robert
behövs för nedanstående rättningar inom redan beslutat scope.

AGENTS.md och conversations/README.md är lästa fullständigt. Signal
`2026-09-17-011` var översta post i både arbetskopia och HEAD:s index,
förekom exakt en gång som sessions-ID och var committad i `e088470`.
Produkt-HEAD:arna matchade signalen exakt. Granskade produktdiffar är
`6059d5e..9f9930f` respektive `5c1bd882..0352117`; skills leveransdiff
är `d047e79..e088470`. Live `origin/main` verifierades med `git ls-remote`
i alla tre repon och matchade 010:s kontrollpunkt. Den kända
publiceringsasymmetrin och Batch 7-spärren kvarstår utanför detta scope.

enkey-agents och neptune_academy hade rena arbetskopior. Skills hade
befintliga lokala ändringar/ospårade filer, inklusive frågedokument,
råunderlag, AGENTS.md/SKILL.md, automation och milesight. Dessa bevaras.
Bryggfilerna och README-protokollet ingår inte i tariffdiffen och ändras inte.

## Blockerande fynd

### P1 — profil och behörighet når inte den verkliga webbprodukten

`src/utils/besparingsvarde.ts:751` använder fortfarande
`fordelaEnergi(underlag.totalMwh)` för aktuell årskostnad. Sökning i src
visar att `fordelaEfterProfil` och `vattenfallBehorighetUppfylld` endast
anropas av den nya testfilen, inte av produktflödet. Den handbyggda
TS-fixturen provar den nakna motorn och saknar faktisk katalog-/policytransport.
Att visa generiska policyfält räcker därför inte: valt profilvärde
kommer inte att styra webbproduktens månadsserie vid framtida aktivering.

Rätta den befintliga produkt-/kontraktsvägen och generatortransporten
så att profilregistret, policyfältet och katalogens behörighetsregel är
statiskt bundna och används i båda språken. Behåll spärrarna på disk.
Visa i isolerad genererad kandidat att samtliga tre profilval faktiskt
ändrar motorns serie och kostnad samt att Standard/Spetsig kontrolleras.

### P1 — ogiltig produktbehörighet returnerar komplett kostnad

`tools/tariffer/vattenfall_arsprodukt.py:116` dokumenterar uttryckligen
att kostnaden beräknas oavsett behörighetsfel; `:169` returnerar felet
vid sidan av ett separat KontraktResultat. Oberoende reproduktion med
Uppsala Standard, 1000 MWh, 300 kW och behörighetsindata 100 MWh/250 kW
ger kvoten 0,4 och ett felmeddelande, men samtidigt
`fullstandighet='complete'`, `noggrannhet='estimated'` och kostnaden
1 073 430 kr exkl. moms.

Tekniskt beslut på leveransens fråga 1: behörigheten ska blockera
kostnad auktoritativt i kontrakts-/domänvägen, även för direkta anrop.
En separat valideringsfunktion är tillåten, men dess utfall får inte
vara ett valfritt sidomeddelande som UI kan ignorera. Återanvänd typad
fel-/blockeringskanal och testa under/på/över 1,2 genom verklig fasad.

### P1 — uppskattningen kan felaktigt märkas snapshot

`policyregister.py:_VATTENFALL_PROFIL_KRAV` tillåter både customer_value
och estimated. Endast Pythonhjälparens manuella val av estimated gör
goldenfallet uppskattat. Oberoende prov med samma giltiga kontraktsindata,
men profilens tillåtna `kalla_typ='customer_value'`, ger
`noggrannhet='snapshot'`, `fullstandighet='complete'`.

Gör estimatklassningen till en egenskap hos denna kalkylprodukt som
överlever direktanrop och genererad TS-transport. Kundens profilval
får inte omklassificera modellen till en snapshotkostnad. Visa även
överuttag/industriavdrag och 4/6-kronorsbegränsningen i resultatets
användarflöde. Att documented_exclusion är en känd, överhoppad
motorpost bevisar inte att användaren får informationen.

### P2 — exakt rabattgräns ger språkberoende pengar

Oberoende exekvering av TS-funktionerna visar att 249 MWh med profil 1
summerar till 249.00000000000006 och ger -1108,05 kr rabatt, där
Python och det beslutade gränsfacitet ger 0 kr. Den nya TS-testfilens
248.999 i stället för 249 undviker felet; det är inte ett godkänt undantag.

Rätta den nya säsongstypens bandval med entydig kontinuerlig
gränssemantik och stabilt årsunderlag. Testa de exakta beslutade
gränserna och värden på båda sidor i båda språken, inklusive fraktionell
MWh. Ändra inte äldre tariffers bandsemantik oavsiktligt.

## Återstående beslut och avgränsad rättningsrunda

Leveransens fråga 2: ett enda kapacitetsband kan härledas från katalogen,
men hjälpvägen får inte fabricera en kundspecifik leverantörsattestering.
Bind valet statiskt till det verifierade enda bandet och transportera
dess verkliga proveniens; alternativt kräv faktisk attestering genom
befintlig kontraktsväg. Behåll felstopp för felaktigt/manipulerat band.

Leveransens fråga 3: React- och browserprov var uttryckliga acceptanskrav
i 010. De skjuts inte till efter aktivering. Testa den verkliga sidan
mot isolerad genererad tolvradskandidat: profilval, behörighetsfel,
estimated, synliga exkluderingar, saknade/ogiltiga fält och spärrat
kr-/besparingsläge. Kör ordinarie browser-E2E och bygge utan att ändra
befintligt dist. Utöka mutationsprov för statiska bindningar och
profilernas vikter/etiketter, inte bara register mot en separat konstant.

Tillåtna beröringsytor är Batch 8:s katalogmetadata, befintliga motorer,
policy-/resultatkontrakt, generator, befintlig produktfasad/UI och deras
relevanta tester samt granskningsloggar. Gör minsta sammanhängande
rättning; skapa ingen ny parallell beräkningsväg. Regenerera med
spårbar katalogproveniens (nuvarande TS-huvud anger `commit=okänd`).
Dokumentera ändrade filer och slut-HEAD:ar, exakt isolerad räkning
73 godkända/75 produkter och projektionen 74/2/16, samtidigt som skarpt
läge förblir 86/61/63 och 62/2/28.

Claude ska verifiera dessa produkt-HEAD:ar och skills granskningscommit
med `e088470` som förälder före rättning. Stoppa vid ny avvikelse.
Avsluta med en ny unik, committad `REVIEW_READY: Codex` och stanna.
Ingen aktivering, push, historikomskrivning eller ändring av automation
eller protokoll ingår. Orelaterade arbetskopiefiler ska bevaras.

## Oberoende validering i detta granskningssteg

- Full Python: **2053 passed, 4 skipped**, inga fel.
- Full TypeScript: **2060 passed**, 64 filer; `tsc --noEmit` grönt.
- Uppsala-goldenfall och befintlig isolerad grindprojektion ingår i
  dessa tester. De bevisar inte den saknade produktintegrationen.
- Separata läsande reproduktioner bekräftar behörighetsfelet,
  snapshot-klassningen och rabattfelet ovan.
- `git diff --check` rent i alla tre repon före loggändringen.
- Nytt bygge, Reactprov för Vattenfall och browser-E2E har inte körts
  av Codex i detta steg; de konstaterade blockerarna kvarstår oavsett
  äldre regressioners utfall.

Codex utför endast granskning och loggcommit här. Claude är mottagare
för rättningen; agent-bridge förmedlar signalen. Ingen push har utförts.
