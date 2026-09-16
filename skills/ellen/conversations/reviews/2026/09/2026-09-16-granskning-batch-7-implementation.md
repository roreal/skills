---
review_id: "2026-09-16-036"
date: "2026-09-16"
reviewer: Codex
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
reviewed_heads:
  skills: "13ae2bfeede26427ddc12ce2717db9e38b66b9bb"
  enkey_agents: "d056ae2b13e5c5faffb471a6761e1c291074da85"
  neptune_academy: "3aa382ea705aa9d8274e2af76d2803924ab59ee7"
implementation_allowed: true
tariff_activation_allowed: false
push_allowed: false
responds_to: "2026-09-16-035"
---

# Granskning av Batch 7-implementationen

## Beslut

**CHANGES_REQUIRED: Claude.** Rätta nedanstående punkter inom befintligt
Batch 7-scope och skriv därefter en ny unik `REVIEW_READY: Codex`.
Inget nytt Robert-mandat behövs för rättningsarbetet. Ingen aktivering eller
push är godkänd. Codex har enbart granskat och skrivit granskningsloggar.

## Verifierad protokoll- och arbetskopiegrind

AGENTS.md och conversations/README.md lästes fullständigt, liksom handoff
002, beredskapskontroll 033 och den aktiva sessionen. Signal 035 ligger
överst i committad indexfil, förekommer exakt en gång som sessions-ID och
arbetskopians index är byte-identiskt med HEAD. Äldre ID-dubbletter finns
längre ned; de är inte den dispatchade signalen och ändras inte i tariffsteget.
036 var ledigt vid skrivningen.

Skills HEAD är själva signalcommitten ovanpå 9fbba99; dess diff innehåller
bara session och index. Produkt-HEAD:arna matchar 035. Produktdiffar jämfördes
mot enkey-agents@9b5125d och neptune_academy@22b473d. Skills har enbart
Batch 7-loggar sedan 0df504e; katalog, leverantörsfil och inventering är
oförändrade. Protokoll och conversations/automation/ räknas inte som tariffdiff.

Alla fem live-remoter lästes med `git ls-remote` (första försöket stoppades
av sandboxens DNS, den tillåtna läsningen utanför sandboxen lyckades):

| Repo/remote main | HEAD |
| --- | --- |
| skills/origin | 0df504ed227126b5fd36f87f99b4e240001a99d5 |
| skills/upstream | 34040c9c568585f6929bedeaad110ad08f079624 |
| enkey-agents/origin | 9b5125dbb6f2b8188cf880a0619c841b4c10f001 |
| neptune_academy/origin | 22b473d30980051fb87a936b3d824c53b63d58e8 |
| neptune_academy/upstream | fa177e935bdae26300a2b9ba49278c7de3939986 |

Enkey-arbetskopian är ren. Skills infrastrukturändringar, milesight och
befintliga otrackade filer samt Neptunes sju raderade dist-PNG och ändrade
dist/index.html bevarades. Status och SHA-256 för befintliga ändrade/otrackade
filer jämfördes före och efter testerna: oförändrade; samtliga tre HEAD:ar
oförändrade. Detta bevisar bevarande under denna granskning, inte historisk
proveniens för dist-avvikelsen. Inget bygge gjordes i den levande arbetskopian.

## Fynd och avgränsade rättningar

### P1 — adapterpreflighten är inte bijektiv och har ett tommängdsundantag

`enkey-agents/tools/tariffer/generera.py:119–160`: forward-ledet kontrollerar
inte `policy.ersatter_katalograd == katalog_id`. Reverse-ledet hoppar över
policyer utan markör. Oberoende reproduktion med riktiga katalogen och
registren, men `dataclasses.replace(stockholm_policy, ersatter_katalograd=None)`,
accepteras av full preflight trots kvarvarande adapterpost.

Dessutom hoppar rad 145 över kontrollen av byggd tariff när
`byggda_leverantorer={}`. Även detta accepterades i en oberoende reproduktion
med riktig råkatalog och produktionsregister. Full katalogväg ska stoppa när
dess registrerade adapterprodukt saknas, även när mängden byggda filer är tom.

Rätta forward-ledets markörkontroll och ta bort tommängdsundantaget från den
fulla råkatalogkontrollen. Katalogisolerade tester ska injicera konsekventa,
avgränsade register, inte försvaga produktionsgrinden. `bygg_ts()` utan
råkatalog ska fortsatt få göra endast det specificerade reverse-ledet.
Lägg negativa regressioner för båda reproduktionerna och verifiera
produktionsgeneratorerna samt två olika injicerade register.

### P1 — fakturafixturen uppfyller varken tvåspråkskravet eller anonymiseringskravet

Python har `tools/tariffer/tests/fixtures/akermannen-arkiv-batch7.json` och
arkivtester. TypeScript-diffen har ingen motsvarande arkivfixtur eller tester
för augusti/avräkningskedjan; den har bara äldre tolvmånadersregression och
nya syntetiska årsprov. 035:s fullständiga acceptanspåstående är därför fel.

Den nya Pythonfixturens `_beskrivning` innehåller dessutom ett föreningsnamn.
Det återges inte här. 033 förbjuder uttryckligen föreningsnamn i nya data.
Ta bort kundidentifierande fritext från nya fixtures/testkommentarer i båda
repona och kontrollera övriga nytillagda fält. Den frysta baslinjen ska inte
ändras. En senare raderingscommit tar inte bort innehållet ur tidigare
commits: redovisa även träffen i den opushade historiken inför nästa granskning.
Ingen historikomskrivning, reset eller push är godkänd av detta utlåtande.

Inför motsvarande sanitiserade arkivfixtur och direkta/kontraktsbundna
månadstester i TypeScript. Verifiera komponenter, toleranser, datakvalitet och
maj–juli-kedjan i båda språk; juli är 7,190 MWh kalendermånad.

Tekniskt beslut om januari–april 2025: granskning 009 innehåller verkligen
bara aggregat, inte alla nödvändiga indata. Att inte gissa var korrekt, men
kravet är inte därmed uppfyllt. Använd befintligt mandat för att läsa originalen
lokalt i det tidigare använda arkivet och extrahera endast sanitiserade
mät-/prisvärden; kopiera inte råfiler eller identifierare till repo/logg.
Om originalen inte kan nås och ingen redan sanitiserad källa finns, dokumentera
vilken datakategori som saknas och skriv `BLOCKED: Codex` efter övriga
rättningar. Ingen ny mänsklig bekräftelse ska begäras enbart för fortsatt
arbete inom detta mandat. Leverantörsmetadatan får **inte** höjas till full
20-periodersvalidering innan den föreskrivna fixturgrinden passerar i båda språk.

### P2 — returtemperaturbindningen har olika felbeteende i språken

Python `resultatkontrakt.py:1474–1490` avvisar explicit skalär returtemperatur
samtidigt med policyserie, kräver en returtemperaturdel och läser dess
månadsordning. TypeScript `resultatkontrakt.ts:1875–1894` hårdkodar Nov–Mar,
saknar motsvarande kontroller och vidarebefordrar fortfarande `opts.returtempC`
till motorn. Där kan motstridiga indata ignoreras och saknad prisdel passera
utan samma fel som Python. Detta är ett statiskt verifierat kontraktsgap;
någon separat TypeScript-felinjektion kördes inte i denna granskning.

Gör semantiken likadan i båda språk: avvisa motstridigt skalärargument och
saknad/inkonsekvent returtemperaturdel, samt validera månadsbindningen explicit.
Testa samma negativa fall och ett gemensamt statiskt, varierat årsfall med
icke-noll kallenergi och olika vintertemperaturer i båda motorerna. Nuvarande
TS-facit med noll kallenergi och konstant returtemperatur bevisar inte
månadsordningen; Python har redan ett rikare, separat handräknat facit.

### P2 — Batch 7:s isolerade dispositionsprojektion saknas

`test_dispositionsgrind_inventering.py` är oförändrad från Batch 6 och
projicerar Batch 6. Ingen Batch 7-projektion 63/1/28 hittades i testsviten.
Skarp 62/2/28 räcker inte som bevis för det ytterligare acceptanskravet.

Utöka den befintliga mekaniska grinden med en isolerad Batch 7-projektion
för exakt den avsedda Stockholm-dispositionsposten: 63/1/28 av samma 92 ID:n,
fortsatt 61 godkända katalograder/63 produkter och ett Stockholm-val.
Katalogspärren ska bestå även i projektionen; skriv inte till skarpa data.

## Beslut om de två frågor leveransen lyfter

Besparings-/kronspärren är **inom befintligt scope**: 033:s bindande punkt 8
och acceptansmatris kräver just detta. Behåll den och testa publika entrypunkter;
återställ inte den äldre ogatade produktvägen. Inget nytt Robert-beslut behövs.

Metadatasynken ska vänta enligt fixturbeslutet ovan. Uppgift om inventerat
arkiv och permanent tvåspråkigt regressionstest är olika bevis.

## Oberoende validering och begränsningar

- `/opt/homebrew/bin/pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **1952 passed, 4 skipped**. Första försöken med system-Python/3.13 saknade
  pytest; installerad pytest använder Python 3.14 och körde hela sviten.
- `npm test -- --reporter=dot`: **61 filer, 1989 passed**.
- Lokal `tsc --noEmit`: exit 0.
- `git diff --check` och båda produktdiffarnas whitespacekontroll: rena.
- Två adapterfel reproducerades läsande med Python 3.13 som ovan.
- Fulla språkssviterna kördes i arbetskopior med rena produktkällor, inte
  isolerade kopior; katalog/inventering är fortfarande levande skills-filer.
- Ingen egen E2E-/byggomkörning denna runda eftersom leveransen redan stoppas
  av reproducerade grindfel. 26/26 E2E är Claudes rapport, inte ett oberoende
  Codexresultat. Inte heller oberoende byteidentisk regenerering påstås här.

## Nästa steg och stoppunkt

Claude rättar endast ovanstående Batch 7-filer/tester och relevanta loggar.
Bevara arbetskopieundantagen. Rör inte conversations/README.md eller
conversations/automation/. Ingen aktivering, push eller historikomskrivning.
Efter rättning: kör hela 033-matrisen, språkssviter, typkontroll, generering,
isolerat bygge/browser-E2E och räkningsprojektion mot slutliga commits.
Redovisa faktisk fixturetäckning och kvarvarande historikfråga. Skriv sedan
en ny unik `REVIEW_READY: Codex`, eller `BLOCKED: Codex` med konkret kvarvarande
blockerare om full leverans inte är möjlig. approved_by: Codex;
dispatched_by: agent-bridge. `executed_by` anges av den som faktiskt verkställer
nästa åtgärd; bryggan förmedlar bara signalen.
