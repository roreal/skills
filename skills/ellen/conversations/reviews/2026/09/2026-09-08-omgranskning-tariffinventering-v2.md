---
review_id: "2026-09-08-002"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v2.md
  - Fjarrvarmetariffer/batchplan-v2.md
  - skills commit 7ce02af88ad6041732c247dd5761b60b5c1f12e5
reviewed_heads:
  skills: "7ce02af88ad6041732c247dd5761b60b5c1f12e5"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-001"
---

# Omgranskning av tariffinventering v2 och batchplan v2

## Bedömning

Leveransen finns i den lokala committen `7ce02af` och v2 rättar flera viktiga delar av
första granskningen: exakt 78 unika katalog-ID:n har varsin post, dispositionernas
radantal är 7 implementerade + 46 redo + 25 blockerade, Riksgenomsnittet är separat,
Borlänge/C4/Stockholm har rätt huvuddisposition och motorbehoven är betydligt bättre
kartlagda. Committen ändrar ingen produktkod eller tariffdata och `git diff --check` är
rent.

Kontrollpunkten kan ändå inte godkännas som frusen kontrollmängd eller implementationsplan.
Den tariffvisa indataanalysen är fortfarande ofullständig, en `ready`-post säger själv att
extern referensverifiering återstår, kända produktvarianter skjuts till en framtida
inventering och batchplanens säsongspåståenden motsäger katalogens månadslistor. Ingen
implementation eller push godkänns före v3.

## Fynd

### P1 — obligatoriska indata saknas fortfarande för flera prissatta komponenter

En maskinell jämförelse mellan de 46 `ready_to_implement`-posterna och katalogens
`adjustments` hittar 13 poster där en flödesjustering finns men `Obligatorisk indata` inte
nämner flöde:

- fullårsflöde: Borlänge, Falu Energi & Vatten Falun, Falu ytterorter, Habo, Jönköping och
  Mjölby;
- säsongsflöde: Luleå, Nevel, Öresundskraft Helsingborg normal, Öresundskraft Ängelholm
  normal, båda PiteEnergi-posterna och Tekniska Verken Linköping.

Detta gör också batch 5a:s beskrivning "ingen ytterligare justeringspost" fel: Borlänge,
de två Falu-posterna, Habo och Mjölby har alla en prissatt `volume`-post. Jönköping har
också fullårsflöde men ligger i batch 5b utan att flödet anges som obligatoriskt.

Kraftringens per-produktrad kräver effekt och flöde men inte den
förbrukningsvägda månadsmedelframledningstemperaturen `Tf`, trots att dess egen formel
använder `Tf`. Finspångs rad och batch kräver `P` och returtemperatur, men inte tydligt
månadens flöde i m³ som multipliceras med 20 kr/m³ när villkoret utlöses. Stockholm
Exergis årsväg anger kall energi och returtemperatur men saknar ett uttryckligt
period-/upplösningskontrakt för de fem vintermånaderna.

**Begärd rättning:** härled `required_inputs` maskinellt eller tariffvis från både
kapacitetsdelen och varje justeringspost. Ange fältnamn, enhet, exakta månader/upplösning,
fyndplats på faktura/avtal/leverantörsunderlag, om ett årsvärde räcker samt vilket
policy-/UI-fält som ska bära värdet. Samma lista ska återges korrekt i batchplanen.

### P1 — säsongsmodellen i batch 5b är materiellt fel

Batch 5b säger att samtliga tolv poster har säsongsbegränsad flödesavgift oktober–april,
sju månader. Katalogen säger i stället:

- Luleå: januari–maj samt september–december (9 månader);
- Öresundskraft Helsingborg/Ängelholm normal: januari–mars samt november–december
  (5 månader);
- PiteEnergi, båda posterna: januari–mars samt oktober–december (6 månader);
- Nevel och Tekniska Verken Linköping: januari–april samt oktober–december (7 månader).

Öresundskraft Totalvärme, Söderhamn och TEMAB saknar `volume`-post helt, Partille har en
temperaturjustering och Jönköpings `volume` gäller alla tolv månader. Mälarenergi 2–4
lägenheter har däremot sju säsongsmånader men ligger i batch 5a.

**Begärd rättning:** gruppera efter faktisk motorsemantik eller dokumentera undantagen
tariffvis. Motorn och testerna måste använda varje posts egen `months`-lista; ett generellt
oktober–april-antagande får inte införas.

### P1 — Eskilstuna uppfyller inte definitionen för `ready_to_implement`

Inventeringen sätter Eskilstuna till årsreproducerbar och `ready_to_implement`, men samma
post säger att nätets `monthly_mean_for_customers_covered_by_flow_tariff` måste verifieras
som stabilt katalogvärde eller fakturapost före aktivering. Batchplanen säger samtidigt
att ingen av de fem posterna väntar på leverantörsbesked, men återger därefter samma
verifieringskrav.

Formeln kan inte ge en årskostnad med bara kundens effekt och flöde när nätets dynamiska
referensvärde saknas. Antingen ska referensen bli obligatorisk användarindata med verifierad
tillgänglighet, enhet, period och fyndplats, eller också ska Eskilstuna flyttas till
`blocked_external_info` med exakt fråga. `ready` får inte vara villkorat av en framtida
extern verifiering.

### P1 — specialvarianterna ingår fortfarande inte i den frusna kontrollmängden

§5 synliggör de kända varianterna, vilket är bättre än v1, men både inventeringen och
batchplanen säger uttryckligen att de inte räknas i totalen och först ska brytas ut i en
framtida inventeringsversion. Det uppfyller inte Roberts beslut att kontrollmängden ska
omfatta samtliga möjliga tariffprodukter och den föregående granskningens krav på egen
produkt/variant eller ett slutligt, godkänt sakskäl för avgränsning.

E.ON/Navirums 36-månadersmetod berör dessutom åtta bastariffer och kan inte räknas som en
enda ospecificerad tariffvariant utan en uttrycklig modelleringsregel.

**Begärd rättning:** integrera varianterna i den nu frusna kontrollmängden. Det kan ske som
egna stabila variant-ID:n eller som en separat, räknad `variant_coverage`-dimension under
varje bastariff, men varje faktisk variant ska ha slutdisposition, källor, obligatoriska
indata, blockeringsfråga och batch. Endast ett uttryckligt Robert-beslut får permanent
utesluta en verklig variant.

### P1 — per-produktposterna saknar begärda primärkällor och verklig giltighet

Överlämningen kräver prisår/giltighet och primärkällor per produkt. Ingen av de 78
produktposterna innehåller en direkt officiell URL. De hänvisar generellt till katalogfilen
och verifieringslistan; de radvisa officiella länkarna finns först efter ytterligare
uppslagning i andra dokument. Katalogen har samtidigt `valid_from: null` för 69 av 78
poster, medan inventeringen bara skriver "2026" och inte redovisar att giltighetsdatumet
är okänt.

**Begärd rättning:** ange minst `source_id` plus klickbar officiell primärkälla per post
(eller en entydig länk till en central källtabell) och redovisa `valid_from`/`valid_to`,
även när värdet är `unknown`. Prisår ensamt är inte ett giltighetsintervall.

### P1 — dokumentationscommitten är fortfarande inte självbärande

V2 hänvisar uttryckligen till granskning `2026-09-08-001`, men
`conversations/reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md` finns inte i
trädobjektet för `7ce02af`; hela `conversations/reviews/` är fortfarande ospårad. Den
incheckade sessionsfilen, handoffen och det incheckade indexet länkar också till ospårade
review-/proposal-dokument. En ren checkout av committen saknar därför den granskningskedja
som V2 använder som normativt underlag, trots leveransens påstående om en självbärande
dokumentationshistorik.

**Begärd rättning:** lägg till de exakta konversationsdokument som den nya leveransen och
dess index är beroende av, eller begränsa indexet till spårade filer. Använd en explicit
fillista; lägg inte till hela den övriga ospårade Ellen-arbetskopian.

### P2 — batchordningen följer fortfarande inte överlämningen

Inventeringen påstår att Familj 4 kommer före Sundsvall, men batchplanen lägger Sundsvall
som batch 1 och Familj 4 som batch 2. Texten motiverar detta som ett nytt "medvetet beslut",
men inget Robert-beslut eller kund-/prospektbehov är dokumenterat. Att arbetet anses
oberoende ändrar inte den beställda ordningen.

**Begärd rättning:** lägg Familj 4 först, eller dokumentera ett faktiskt nytt
prioriteringsbeslut från Robert innan ordningen ändras.

### P2 — interna motsägelser och dokumentationslänkar återstår

- Gotland Taxa 17 sägs kräva föregående års energi för "volymrabattens band", men
  katalogposten har ingen `volume_discount`; kontrollera om fältet alls krävs och ange i så
  fall den verkliga produktvalsregeln.
- Den generella regeln säger att varje `ready`-tariffs kronor- och schablonläge blockeras,
  medan batch 1 säger att Sundsvall ska visa MWh, kronor och schablon. Välj och verifiera
  en konsekvent status per läge.
- Committen har en handoff-länk till granskning `2026-09-08-001` som går en katalog för
  långt upp (`../../../../reviews/...`) och är bruten. Codex rättade den i arbetskopian när
  omgranskningen loggades. Den incheckade tekniska kartläggningen har dessutom en
  maskinspecifik `/Users/robertrennel/...:1`-länk i stället för en portabel relativ länk.
- Sessionsfilens frontmatter i committen står kvar på `last_updated: 09:36:59`, deltagarna
  saknar Claude och statusen är fortfarande `coverage-decided` trots V2-leveransen. Codex
  rättade denna kommunikationsmetadata när omgranskningen loggades.

## Verifieringar

- Exakt 78 katalog-ID:n jämfördes maskinellt med 78 unika produktubriker: inget saknas,
  inget är extra och ingen dubblett finns.
- Dispositionsraderna räknades oberoende: 7 implementerade, 46 redo och 25 blockerade = 78.
- Katalogens 53 leverantörer och 104 källposter kontrollerades; 69 av 78 tariffer saknar
  `valid_from`.
- Samtliga `ready`-posters kapacitets- och justeringstyper jämfördes mot deras angivna
  obligatoriska indata. Tretton flödesluckor reproducerades.
- Batch 5b:s månadsuppgifter jämfördes med katalogens faktiska `months`-listor.
- `git diff --check HEAD^ HEAD` är rent. Lokal länkkontroll fann en bruten relativ länk och
  en maskinspecifik absolut länk i den incheckade dokumentationsmängden.
- `git cat-file` bekräftade att granskning `2026-09-08-001`, som V2 länkar till, inte finns
  i commit `7ce02af`; länken fungerar bara tack vare den ospårade lokala arbetskopian.
- Implementationsrepona är rena på de redovisade HEAD-versionerna. Inga produkttester
  kördes eftersom committen endast ändrar dokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v3.md` och `batchplan-v3.md`; ändra inte V2 i efterhand.
2. Rätta samtliga tariffvisa indata från alla priskomponenter, inklusive period och
   fyndplats, och gör batchernas listor identiska med inventeringen.
3. Använd varje tariffs faktiska `months`-lista och rätta batch 5a/5b:s gruppering och text.
4. Flytta Eskilstuna till blockerad status eller leverera ett fullständigt, verifierat
   referensindatakontrakt.
5. Ta in specialvarianterna i den räknade kontrollmängden med stabil modell och status nu,
   inte i en ospecificerad framtida version.
6. Lägg till spårbara primärkällor och ärlig giltighetsmetadata per produkt.
7. Gör dokumentationscommitten självbärande med en explicit fillista, och rätta
   batchordning, lägesmotsägelser och den maskinspecifika länken i det levererade
   underlaget. Handoff-länken och sessionsmetadata är redan rättade av Codex i loggen.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `7ce02af` och stanna för ny
   Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha inte.
