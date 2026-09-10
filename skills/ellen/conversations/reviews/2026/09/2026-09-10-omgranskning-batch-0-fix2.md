---
review_id: "2026-09-10-003"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@cddb367594829d5ef708411ba0979e074e7e8c91"
  - "neptune_academy@e993a5d4a9f8e9c53dfda5f3b56721d2a4ea1a00"
  - "Rättningar mot omgranskning 2026-09-10-002"
base_heads:
  enkey-agents: "714da6fe12a8a6c171968e01eddefa50fedc0a0f"
  neptune_academy: "b87ff5853623b2c492cc56b91ba046920013caea"
reviewed_heads:
  enkey-agents: "cddb367594829d5ef708411ba0979e074e7e8c91"
  neptune_academy: "e993a5d4a9f8e9c53dfda5f3b56721d2a4ea1a00"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
supersedes_review: null
follows_review: "2026-09-10-002"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0, rättningsrunda 2

## Beslut

Rättningen får fortsatt **`changes-required`**. De konkreta scope-, bandfels- och
Python-typfelen från `2026-09-10-002` är i huvudsak rättade och ska bevaras. Den nya
sidkoden och dess smoke-test uppfyller däremot inte det godkända V22-kontrakt som Batch 0
ska etablera innan de 57 redo-tarifferna byggs ut.

Det avgörande problemet är att implementationen bara är grön för fall där den nya
generiska UI-mekanismen inte används. Den kan ännu inte representera Jönköpings numeriska
enum, rendera en riktig elementvis serie eller ge fältlokala fel. Det påstådda
end-to-end-testet verifierar uttryckligen att policy-UI:t är **frånvarande** i båda sina
scenarier. Det kan därför inte upptäcka de kontraktsavvikelser som redan finns i den nya
koden.

Ingen tariff får aktiveras och de lokala produktcommitterna är inte godkända för push.

## Fynd

### P1 #1 — Den generiska policy-UI-kedjan avviker på alla kritiska gränser från V22

V22 kräver `policyFaltMetadata(policy, prisar, omfattning)` med en diskriminerad
`inmatningstyp`, obligatorisk etikett/hjälptext, prispostens bandalternativ, numeriska
enumalternativ och seriekardinalitet (`batchplan-v22.md:287–324`,
`tariffinventering-v22.md:2801–2847`). Den implementerade
`policyFaltMetadataForPolicy(policy, omfattning)` tar inte `prisar`, har bara
`vardetyp`, saknar `obligatorisk`/`inmatningstyp` och kan inte skapa vare sig
`band_id_val` eller `enum_val` (`resultatkontrakt.ts:798–840`).

Det får följande konkreta följder:

- Bandalternativen läses direkt ur `valdPrisar` i React-sidan
  (`KalkylatorPage.tsx:813–823`) i stället för ur den prispostmedvetna metadatan.
- `KravPost.tillatnaVarden` är `readonly string[]` och tillåts bara för `band_id`
  (`resultatkontrakt.ts:145–147,191–200`). Python speglar samma fel med
  `tuple[str, ...]` och samma bandkrav (`resultatkontrakt.py:228–231,263–269`). V22:s
  Jönköpingskontrakt är i stället en **numerisk** allow-list på ett `number`-krav:
  `readonly number[]`/`tuple[float, ...]`, medan `band_id` hämtar sina giltiga ID:n ur
  prisposten och förbjuder `tillatnaVarden` (`tariffinventering-v22.md:2507–2511,
  2630–2634,4234–4253`). Jönköpings `0/10/25/50` kan alltså inte deklareras i dagens
  implementerade kontrakt.
- Sidans råstate är fortsatt `Record<string, string>`
  (`KalkylatorPage.tsx:116–117`), fast den deklarerade råtypen tillåter
  `readonly string[]`. Alla serier renderas som **en** kommaseparerad textruta
  (`KalkylatorPage.tsx:824–831`) i stället för exakt `antalVarden` separata råfält.
  Numeriska enumvärden renderas inte som val över huvud taget.
- Parsern accepterar en sträng i `number_series` och delar den på kommatecken
  (`resultatkontrakt.ts:871–876`), trots V22:s uttryckliga `Array.isArray`-grind. En array
  till ett skalärt fält klassas samtidigt som `saknat`, inte `{ogiltigt, typ}`
  (`resultatkontrakt.ts:867–869,885–889`). Det är motsatsen till de beslutade
  råformsgrindarna.
- `etikett`/`hjalptext` är fortfarande valfria i båda språk och metadatan faller tyst
  tillbaka till nyckeln/tom sträng (`resultatkontrakt.ts:148–151,829–832`;
  `resultatkontrakt.py:232–235`). V22 kräver att policyregistret är enda källa och att en
  kravpost utan etikett stoppas fail-closed. De existerande policyregisterposterna har
  följaktligen fortfarande inga sådana texter.
- Submit-förkontrollen samlar allt i ett enda globalt `formError`
  (`KalkylatorPage.tsx:427–454,919`) och kopplar inte `saknadeFalt`, `ogiltigaFalt` eller
  `ej_attesterat` till respektive input. Det uppfyller inte V22:s fältlokala felkrav och
  ger inte `aria-invalid`/fältanknuten feltext.

**Begärd rättning:** implementera V22:s metadata- och råformskontrakt ordagrant i båda
språk. Band-ID:n ska komma från vald prispost; `tillatnaVarden` ska vara numerisk allow-list
för `number`; `inmatningstyp` ska skilja `number`, `band_id_val`, `enum_val` och
`number_series`; etikett/hjälptext ska vara fail-closed och fyllas i i policyregistret.
Sidan ska lagra `PolicyRawFormValue`, rendera en ruta per serieelement, rendera numeriskt
enum som val, köra de strikta formgrindarna och visa fältlokala fel. Legacyfältet `falt`
ska förbli separat och oförändrat.

### P1 #2 — Sidtestet provar inte Batch 0-funktionen och är inte reproducerbart ensamt

Det nya `e2e/kalkylator.smoke.mjs` testar riksgenomsnittet och Sandviken. I båda fallen
assertar testet att `onskadTyp` och/eller policyfältformuläret är **frånvarande**
(`kalkylator.smoke.mjs:39–50,62–78`). Det fyller inget policyfält, väljer inget band-ID,
skapar ingen serie, provar inget enum, testar ingen attestering, inget fältlokalt fel och
ingen `aktuell_arskostnad`-resultatsektion. Sökning i `src/**/*test*` ger inga anrop alls
till `policyFaltMetadataForPolicy` eller `parsaPolicyIndata`.

V22 kräver i stället den verkliga `KalkylatorPage` med en syntetisk prispost som bär
samtliga tre värdetyper plus ett Jönköping-liknande enum, en 12-elementsserie med en tom
ruta som ska ge fältfel, attestering och ett resultat jämfört med handräknat facit
(`tariffinventering-v22.md:2840–2847`). De fem uttryckliga attesteringsgränserna i
`batchplan-v22.md:384–394` är inte heller kompletta: byggare, produktentry och fasad är
testade, men metadata- och verklig UI-gräns saknas.

Kommandot är dessutom inte självbärande. `package.json` definierar `test:e2e` som enbart
`node e2e/kalkylator.smoke.mjs`, medan skriptet förutsätter en redan startad server på
port 4173. Kört exakt som `npm run test:e2e` i ett rent läge slutar det med
`ERR_CONNECTION_REFUSED`. Med en separat manuellt startad `npm run preview` passerar de
två smoke-scenarierna, men täckningsproblemet ovan kvarstår.

**Begärd rättning:** ersätt eller komplettera smoke-testet med V22:s verkliga syntetiska
sidtest. Testkommandot ska själv bygga/starta/vänta på och stänga sin testserver, eller
vara ett vanligt komponenttest som inte kräver en extern server. Verifiera specifikt
metadata, alla inmatningslägen, tom seriecell, attestering, fältlokal felkoppling och
handräknat årsresultat.

### P1 #3 — Det beslutade gemensamma underlaget är fortfarande två olika scheman

Scope-felet från förra granskningen är funktionellt rättat: `argsFranInputs` äger nu
uppskalningen och den nya dispatchen använder dess `totalMwh`. Men V22:s uttryckliga
kontrakt är fortfarande inte implementerat.

V22 anger exakt `argsFranInputs(inputs): Tariffberakningsunderlag`, där
`Tariffberakningsunderlag` har `totalMwh`, `leverantorId`, `kapacitetKw`, `falt`,
`policyFalt`, `policyFaltAttestering` och proveniens
(`tariffinventering-v22.md:3935–3989`). Nu returnerar hjälparen i stället
`Omit<BesparingsvardeArgs, 'besparingsgrad'>` och inkluderar därmed även
`paverkbarMwh` (`energiPotential.ts:447–487`). Den verkliga
`Tariffberakningsunderlag` har i sin tur `energyMwh`, saknar `totalMwh` och saknar `falt`
(`besparingsvarde.ts:476–486`).

`calcResultForOnskadTyp` kan därför inte göra V22:s enda avsedda anrop
`beraknaArsprodukt(argsFranInputs(inputs))`. Den destrukturerar hjälparens retur och bygger
ett tredje objekt manuellt (`energiPotential.ts:716–726`), där `falt` tappas. Det lämnar
fortsatt två produkt-DTO:n som kan drifta isär när nästa tariff kräver ett befintligt
numeriskt fakturafält. Även årsresultatets fältnamn avviker från den beslutade unionen:
`arskostnadKr`/`resultatstatus` i stället för `kostnad`/`status`
(`besparingsvarde.ts:488–495`; V22 `tariffinventering-v22.md:4071–4096`).

**Begärd rättning:** gör V22:s `Tariffberakningsunderlag` till den gemensamma bastypen,
låt `argsFranInputs` returnera exakt den och låt besparingsvägen lägga på
`paverkbarMwh`/`besparingsgrad` vid anropet. Årskostnadsvägen ska skicka samma underlag
direkt utan ommappning eller tappade fält. Synka den diskriminerade unionens fältnamn och
tester med den godkända definitionen.

### P2 #1 — Produktväljaren använder bara den ena av de två förmågeresolvrarna

`stodjerBesparing(prisar)` är implementerad men har ingen produktkonsument; sökningen ger
bara dess definition. Sidan visar alltid både alternativen när
`stodjerAktuellArskostnad` är sann (`KalkylatorPage.tsx:789–801`) och återställer samtidigt
`onskadTyp` till `besparing` vid varje leverantörsbyte (`KalkylatorPage.tsx:210–215`).

För de planerade Stockholm-/Lidköpingspolicyerna är
`stodjerAktuellArskostnad=true` och `stodjerBesparing=false`. Deras förvalda knapptryckning
går därför till en uttryckligen ostödd produkt och ger `Produktbegransning`, trots att den
stödda årskostnadsprodukten finns bredvid. De två oberoende förmågorna ska styra både vilka
val som erbjuds och vilket giltigt default sidan använder.

## Rättningar som är godkända att bevara

- Okänt band-ID når nu `okant_val` genom de publika produktvägarna i TypeScript.
- Pythonförkontrollen tar prisposten och kontrollerar valt band mot dess verkliga nivå-ID:n.
- `PolicyValideringsOrsak` är nu en sluten åttaorsaks-`Literal` i Python.
- `argsFranInputs` äger nu den verkliga `space_heat_excl_dhw`-uppskalningen; det tidigare
  konkreta undervärderingsfelet är stängt och riktade dispatchtester är tillagda.
- Energisystemgrinden och den diskriminerade toppnivåunionen finns, och sidan anropar den
  nya dispatchen samt har en separat årskostnadssektion.
- Ingen tariff, katalogpost, disposition eller produktionsgrind har ändrats.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **386 passed**;
  endast en sandboxrelaterad pytestcache-varning.
- `npm test -- --run` i `neptune-marketing`: **15 testfiler, 446 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; byggskapade `dist`-ändringar återställdes efter kontrollen.
- Med manuellt startad preview-server: `npm run test:e2e` passerar sina två smoke-scenarier.
- Utan förhandsstartad server: samma dokumenterade kommando misslyckas med
  `ERR_CONNECTION_REFUSED` mot `http://localhost:4173/kalkylator`.
- `git diff --check 714da6f..cddb367` och `git diff --check b87ff58..e993a5d`: godkända.
- Båda produktrepona är rena efter granskningen.
- Statisk kontroll bekräftar att metadata/parser saknar tester, att E2E-testet aldrig
  renderar ett policyfält och att `stodjerBesparing` saknar produktanropare.

## Nästa kontrollpunkt för Claude

Rätta endast P1/P2-fynden ovan ovanpå befintliga commits. Ingen tariffdata, disposition
eller aktivering får ändras. Batch 0 ska kunna bevisa den framtida generiska mekanismen
med en syntetisk tariff **innan** någon av de 57 redo-posterna aktiveras; dagens frånvaro
av en levande tariff med alla fälttyper är skälet till fixturen, inte ett skäl att hoppa
över testet.

Skapa fokuserade lokala rättningscommits per produktrepo, kör hela testmatrisen inklusive
ett självbärande verkligt sidtest, typkontroll, bygge och diffkontroll, logga bas-/slut-HEAD
och stanna för Codex omgranskning. Ingen push.
