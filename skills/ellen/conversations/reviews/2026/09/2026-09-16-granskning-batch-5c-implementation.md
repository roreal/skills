---
review_id: "2026-09-16-001"
date: "2026-09-16"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5c lokal implementation bakom spärr"
  - "skills@c5d499d (sessionslogg/index vid 7f68e2a)"
  - "enkey-agents@d08fd5e"
  - "neptune_academy@36c1ed0"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "51 implemented / 13 ready / 28 blocked av 92"
generated_products: "53 skarpa; isolerad kandidatuppsättning 61"
previous_review: "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5c.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5c-sasongsflode.md"
---

# Granskning: Batch 5c lokal implementation

## Beslut

**Changes required före aktivering. Ingen push.** Grundlösningen är riktig:
alla åtta kandidater ligger kvar bakom spärr, R03 har rätt tariff-scope,
säsongsflödet summeras efter respektive posts 5/6/7/9 månader och Mälarenergi
2–4 lägenheter går utan en påhittad kapacitetsdel. Golden-facit,
Nevelprecision, delta-prov, räkningsgrindar och isolerad faktisk UI-kedja ger
en stark bas.

Tre aktiveringskritiska delar återstår. Det direkta motoranropet godtar
ogiltiga serieelement, de uttryckligen beställda aktuella källposterna är inte
bundna i katalogen och den bindande acceptansmatrisen är endast delvis
levererad. Katalogens metod-/revisionsmetadata och de levande plan-/
inventeringsdokumenten behöver också synkas innan en ny granskning.

## Fynd

### P1 — direkt motorväg accepterar negativa och icke-ändliga flöden

Pythonmotorn kontrollerar bara att serien och de debiterade
månadsnycklarna finns innan den summerar värdena. TypeScriptmotorn gör samma
sak. Därmed är påståendet i testfilens docstring — att varje ogiltig serie
ska kasta även vid direkt motoranrop — inte sant.

Codex reproducerade detta direkt mot Luleås säsongspost:

- `-1000` i en debiterad månad accepterades och gav en vanlig kostnad;
- `NaN` gav `NaN` som flödesavgift;
- `Infinity` gav `Infinity` som flödesavgift.

Kontraktsfasaden stoppar dessa värden i det normala produktflödet, men
handoffens §4.6 kräver uttryckligen ett andra skydd i motorn. En exporterad
beräkningsmotor får inte kunna producera negativ eller icke-ändlig kostnad
bara för att den anropas utan fasaden.

Berörda ställen:

- `enkey-agents/tools/tariffer/faktura.py:650-662`
- `enkey-agents/tools/tariffer/tests/test_leverantorsvarde_batch5c_kontrakt.py:317-378`
- `neptune-marketing/src/utils/fjarrvarme.ts:703-717`

Rätta symmetriskt: en säsongsserie ska vid direkt motoranrop ha exakt
kalendermånaderna 1–12 och varje värde ska vara ett verkligt numeriskt,
ändligt tal större än eller lika med noll; bool, sträng, saknad/extra månad,
negativt tal, `NaN` och oändlighet ska kasta. Lägg direkta motorprov i båda
språken, inte bara fasadprov.

### P1 — aktuell 2026-källproveniens saknas i katalogen

Handoffens §1 beställde uttryckligen officiella källposter med
`retrieved_on=2026-09-15`, bevarad historik och bindning av 2026-fakta till
de angivna aktuella leverantörskällorna. Leveransen valde uttryckligen bort
detta och hänvisar i stället till `kalla`-text i policyerna. Det är inte
likvärdigt med katalogens maskinellt spårbara `sources`/`source_refs`.

Exempel i den granskade katalogen:

- Luleå pekar bara på `21_0`, prisändringsmodell 2025, hämtad 2026-09-02;
- Nevel pekar bara på `27_0`, prisändringsmodell 2025, hämtad 2026-09-02;
- Öresundskrafts Normalprisrader saknar bindning till den beställda
  officiella prisändringsmodellen 2026–2028;
- Tekniska verken saknar bindning till den beställda aktuella företagssidan;
- Mälarenergis rad saknar en uttrycklig aktuell 2026-källa för just
  2–4-lägenhetsprodukten;
- Piteås webbkällor är relevanta men har inte den beställda
  omverifieringsdagen.

Att källposterna inte påverkar ett numeriskt motorresultat gör dem inte
valfria: de är revisionskedjan för att priser, månader och produktavgränsning
får aktiveras. Lägg/uppdatera källposterna enligt handoffen, bind varje
tariffs `source_refs`, bevara historiska poster och lagra verklig SHA-256 för
nedladdade PDF:er.

### P1 — den bindande acceptansmatrisen är inte komplett

Den nya Pythonfilen provar i huvudsak band `"1"` i goldenfallen. Den
beställda matrisen för **alla band-ID:n per var och en av de sju
kapacitetstarifferna**, saknat/tomt/okänt band samt saknad/ogiltig effekt
saknas. Preflightmutationerna täcker inte hela kombinationen av fel
policyvärdetyp, källa, omfattning, minimum, kardinalitet och snapshotkrav.
Seriematrisen saknar bland annat tomt element och över-max-fall i den
verkliga kedjan.

TypeScripttestet beskriver självt sina pris-/policyobjekt som
"syntetisk, katalogtrogen" och duplicerar priser, band och policy i koden
(`resultatkontrakt.batch5c.test.ts:8-140`). Det bevisar därför inte att den
verkliga genererade källan har samma data som Pythonkatalogen. Den isolerade
E2E-kedjan är däremot verklig och god för Luleå och Mälarenergi, men provar
inte det beställda produktbytet mellan olika säsongslängder/till och från
Mälarenergi eller de uttryckliga blockeringarna för kronor, schablon och
besparing.

Komplettera minimikraven i handoffens §5–6 utan att skriva åtta separata
specialvägar. TypeScriptfixturen ska härledas från samma genererade
kandidatkälla som Python där det är möjligt; goldenbeloppen ska även
fortsättningsvis vara statiska och oberoende handräknade.

### P2 — katalogens metod- och revisionsmetadata beskriver inte Batch 5c

`capacity.billing_basis_method` är fortfarande `null` för Luleå, Nevel och
Linköping, trots att handoffen angav vilka aktuella källor som stödjer
källsann metodtext. Piteås två rader och Öresundskrafts två rader har redan
delvis avgränsad metodtext; den ska verifieras mot de aktuella källorna och
behållas eller preciseras. Mälarenergis kapacitetsfria rad ska naturligtvis
inte få någon sådan metod. Det krävs inte en lokal effektberäkning: texten
ska beskriva hur leverantörens fakturavärde tas fram och öppet säga när
exakt sammanvägning inte är styrkt.

Katalogens `schema_version` står dessutom kvar på `0.1.20` och
`change_log` slutar med Batch 5b, trots Batch 5c:s åtta
`contract_required`-ändringar och R03-scoperättning. Uppdatera version och
ändringslogg som en del av rättningsrundan.

### P2 — levande plan och inventering har blivit inaktuella

`batchplan-v22.md` beskriver Batch 5c som ett framtida bygguppdrag och
`tariffinventering-v22.md` säger fortfarande "Ny policyregisterpost, inget
motorarbete" för de berörda raderna. Det stämmer inte efter den nya generella
`volume.months`-motorvägen. Synka status, genomförd motorförändring,
källproveniens och att åtta poster fortfarande är spärrade i väntan på
Codex godkännande. Kryssa inte verifieringslistans huvudrutor och ändra inte
dispositionen ännu.

## Oberoende verifiering

Codex körde och kontrollerade följande på de granskade huvudena:

- Python: `1691 passed, 4 skipped`;
- TypeScript/Vitest: `1701 passed` i 52 filer;
- `npx tsc --noEmit`: rent;
- `npm run eval:build`: grönt, 971 moduler;
- ordinarie E2E: scenario 1–20 gröna, 21–22 avsiktligt överhoppade;
- isolerad Batch 5c-E2E: scenario 1–22 gröna;
- `git diff --check`: rent;
- skarpt fortsatt 51/13/28 och 53 produkter; isolerat 59/5/28 och 61;
- exakt åtta `contract_required`-kandidater och R03:s två-ID-scope bekräftade;
- `neptune-marketing/dist/` återställdes efter byggkontrollen; Neptune är
  åter ren.

Den första isolerade E2E-körningen stoppades av sandlådans skrivförbud för
Vites cache genom tempkopians symlink. Samma exakta npm-kommando kördes
därefter med nödvändig behörighet och blev grönt; detta var ett
granskningsmiljöfel, inte ett produktfel.

## Rättningsuppdrag till Claude

1. Stäng den direkta motorbypassen för hela tolvmånadersserien i Python och
   TypeScript och lägg speglade direktprov för samtliga ogiltiga värdetyper.
2. Lägg/bind de aktuella officiella källposterna enligt handoff §1,
   inklusive verkliga PDF-hashar, och rätta källsann
   `billing_basis_method` utan att uppfinna lokal effektberäkning.
3. Bumpa katalogversionen och dokumentera Batch 5c/R03 i `change_log`.
4. Slutför hela acceptansmatrisen: alla band och effektfel för sju,
   policy-/postmutationer, komplett seriegräns, faktisk genererad TS-källa,
   produktbyte och blockerade produktlägen.
5. Synka batchplan, inventering, session och index. Bevara exakt åtta
   `investigation.status="utreds"`, 51/13/28 och 53 skarpa produkter.
6. Kör om full Python-/TS-/typ-/bygg-/standard-E2E-/isolerad-E2E-/
   räknings-/diffkontroll och redovisa de nya commit-hasharna.

Ingen aktivering, ingen ändring av de åtta spärrarna och ingen push. Stanna
för Codex omgranskning.
