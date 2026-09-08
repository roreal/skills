---
review_id: "2026-09-06-005"
date: "2026-09-06"
reviewer: Codex
status: changes-required
scope:
  - "Förslag 2026-09-06-001 version 2: Sandviken Energi Helleverans"
  - "Katalog, policyplacering, produktadapter, UI-spärr och proveniens"
reviewed_heads:
  enkey-agents: "2dd62a2"
  neptune_academy: "e64c3de"
implementation_changed: false
push_status: "ingen ny implementation finns"
---

# Omgranskning: Sandviken-förslag v2

## Bedömning

V2 rättar viktiga delar av v1: piloten är nu avgränsad till Helleverans,
`annual_forward` och MWh-läge; kronor-inversen hålls utanför; ett faktiskt
leverantörsvärde för effekten ska krävas; de aktuella 2026-källorna och
kalenderdagsperiodiseringen namnges; och katalogen ska bli versionshanterad.

Förslaget är ändå **inte implementationsklart**. Produktadaptern kopplar policyn på fel
nivå och skulle samtidigt bryta Stockholm Exergis redan pushade `validated`-flöde.
Blockeringsreturen passar inte kalkylatorns nuvarande typer eller anropskedja, och
`summaExkl` ändrar den etablerade momssemantiken. V2 fortsätter dessutom att ändra det
inmatade leverantörsvärdet med en overifierad avrundning och löser fortfarande inte den
faktiska dropdownetiketten.

Status är därför **changes-required**. Claude ska skriva ett kort v3-förslag och stanna
före kodning.

## Fynd

### P1 — policyn läses från fel nivå och grenen fångar fel tariff

V2 rad 50–53 och 83–85 använder `prisar.policy` och låter förekomsten av vilken policy
som helst aktivera årsadaptern respektive kronor-spärren.

Det stämmer inte med kataloggeneratorns faktiska form:

- för en ny katalogtariff lägger `bygg_ts_fran_katalog` policyn på
  **leverantörsobjektet** som `entry["policy"]`, medan `_kraver_kontrakt` ligger i
  prisårsposten;
- Stockholm Exergis redan pushade `validated`-pilot har däremot `policy` i
  **prisårsposten**, men policyn täcker bara `monthly_invoice` och sätter inte
  `_kraver_kontrakt`.

V2 skulle alltså missa Sandvikens policy, falla vidare till den nakna `arskostnad` och
kasta `KontraktKravs`. Samtidigt skulle `if (policy)` fånga Stockholm Exergi, försöka köra
dess årsprognos genom en policy som saknar `annual_forward` och blockera ett befintligt
produktionsflöde. Samma felaktiga kontroll skulle även stänga Stockholms nuvarande
kronorflöde, trots att v2 säger att det ska vara oförändrat.

**Krav på v3:** välj en kanonisk policyplacering per prisår. Det renaste är att även
kataloggeneratorn lägger policyn på den genererade prisårsposten, på samma plats som
Stockholms policy. Årsadaptern får ändå inte grena på enbart `policy`: den ska aktiveras
endast när `_kraver_kontrakt === true`, kräva en parsebar policy med
`annual_forward`-täckning och kasta ett tydligt konfigurationsfel om markör och policy inte
hänger ihop. En `validated`-policy utan markören ska lämna befintlig årsprognos och invers
orörda. Kronor-spärren ska på motsvarande sätt styras av den kontraktsmarkerade tariffens
saknade `annual_inverse`, inte av allmän policyförekomst.

### P1 — blockeringsreturen går inte genom dagens produktkedja och momsen blir fel

V2 rad 64–71 föreslår att `beraknaBesparingsvarde` returnerar ett
`resultatBlockerat`-objekt och i normalfallet använder `summaExkl`.

Dagens `Besparingsvarde` kräver åtta numeriska/resultatfält. `calcResult` anropar
`beraknaBesparingsvarde` tre gånger och läser omedelbart bland annat `andelAvNotan`,
`besparingKr` och `kapacitetUppskattad`. Ett partiellt blockeringsobjekt kan därför inte
bara visas av `KalkylatorPage`; det måste först modelleras och föras genom hela
`energiPotential.ts`-kedjan. Annars blir det antingen ett typfel eller `undefined`/`NaN`
i offertlogiken.

Dessutom använder den befintliga produktvägen uttryckligen `summaInkl`. Kronorlägets
argument heter `krInkl`, UI:t jämför med kundens faktiska faktura och nuvarande tester
pinnar momsinklusive belopp. Att byta till `summaExkl` skulle sänka de redovisade
Sandvikenbeloppen med 20 procent jämfört med samma momsinklusive faktura.

**Krav på v3:** definiera antingen en diskriminerad union som förs hela vägen genom
`calcResult` till UI, eller ett särskilt förväntat domänfel som bär `Resultatstatus` och
fångas i formuläret. Ett blockerat kontraktsresultat får aldrig ge ett partiellt
`KalkylatorResult`. Ett komplett resultat ska bära den härledda statusen och fortsätta
använda `kostnad.summaInkl` för både före och efter.

### P1 — ett leverantörsvärde ändras och märks därefter felaktigt som verifierat

V2 rad 55–60 och 108–134 kör användarens fakturavärde genom
`normaliseraKapacitet`, alltså `Math.round` och golvklämning, innan posten märks
`supplier_value`/`verified`. Då är det lagrade värdet inte längre det leverantörsvärde
användaren skrev in.

Detta var uttryckligen förbjudet i granskning 004. Att en regel redan används av legacy-
tariffer gör den inte källverifierad för Sandviken. Tester av `Math.round` bevisar bara
JavaScripts beteende, inte Sandviken Energis avtalsregel. Förslaget beskriver dessutom
felaktigt `Math.round` som "runda till jämnt"; JavaScript rundar positiva halvtal uppåt.

Bandtesterna är inte heller språkidentiska på den nivå som betyder något:
`_niva`/`nivaFor` väljer första bandet vars max räcker, medan TypeScript-produktens yttre
normalisering exempelvis gör 49,4 till 49 före nivåval. Utan normalisering går 49,4 vidare
till nästa band. Att normalisera testvärdet i båda testerna skulle bara bygga in det
overifierade antagandet i facit.

**Krav på v3:** välj en verkligt fail-closed delmängd. Utan nytt leverantörsbesked kan
piloten acceptera endast ändliga heltal som redan ligger entydigt i de publicerade banden
(lägst 3 kW), föra exakt det oförändrade talet till `IndataPost` och avvisa decimaler och
värden under 3. Alternativet är att implementera och kräva leverantörens band-ID. Den
delade legacy-normaliseringen får lämnas orörd, men får inte användas på Sandvikens
kontraktsväg. Gränstester ska acceptera 3, 49, 50, 199 och 200 samt avvisa decimalfallen,
inte ange vilket band ett okänt avrundningsfall "borde" få.

### P1 — Helleveransetiketten och MWh-avgränsningen är fortfarande inte genomförda

Att ändra `network_or_product` enligt v2 rad 31–36 räcker inte. Generatorn använder bara
det fältet när **flera godkända tariffer för samma medlem** finns. När Sandviken blir den
enda godkända raden visar dagens generator fortfarande bara `Sandviken Energi`.
Sätts hela texten `Sandviken Energi — Helleverans` i fältet och en andra tariff senare
godkänns riskerar nuvarande prefixlogik dessutom ett dubblerat bolagsnamn.

V2 spärrar kronorläget men säger inget om formulärets tredje läge, `schablon`. Där kan
Sandviken fortfarande väljas och årsenergin uppskattas ur area. Det motsvarar inte den
deklarerade avgränsningen till MWh-läge och kan ge en kontraktsstatus grundad endast på
effekten trots att energin är uppskattad.

**Krav på v3:** specificera generatorändringen som verkligen ger den genererade etiketten
`Sandviken Energi — Helleverans`, gärna med katalogvärdet `Helleverans` och en explicit
visningsnamnsregel. Om piloten ska vara MWh-only ska både `kr` och `schablon` blockeras för
Sandviken och ett positivt, faktiskt MWh-värde krävas. Om schablon ska tillåtas måste scope
och resultatstatus i stället revideras sanningsenligt. Testa den riktiga genererade
dropdownen, inte bara katalogfältet.

### P2 — katalog- och policyändringen är ännu inte en fullständig semantisk diff

De nya källorna, effektmetoden och `days_in_month/days_in_year` är korrekta. Följande
behöver dock preciseras:

- `investigation.status: "kall_verifierad"` är ett nytt, odefinierat statusvärde. Dagens
  grind blockerar bara exakt `"utreds"`, så varje felskrivning passerar på samma sätt.
  Lägg en strikt allow-list/explicit godkänd status i grinden eller använd ett redan
  definierat, entydigt avslutskontrakt.
- V2 ändrar `component_completeness` men nämner inte den kvarvarande
  `production_ready: false`, katalogens `coverage_summary`, `as_of`, `schema_version` eller
  `change_log`. Ange vilka som ska ändras och varför; lämna inte motstridiga metadata.
- De två källorna är HTML-sidor och har inga PDF-sidor. `source_refs[].pages` bör vara
  `null`, inte `[1]`.
- `network_or_product` bör beskriva produkten (`Helleverans`), inte upprepa bolagsnamnet.
- Eftersom v2 ersätter v1 måste den även ange den fullständiga nya
  `POLICYREGISTER`-posten: tariff-ID, `KravPost` för `debiterbar_effekt_kw`,
  `kravs_for=("annual",)`, endast `supplier_value`, `rullande=False`,
  `tackning={"annual_forward"}` och `kapacitet_bindning`.

### P2 — regressionsbaslinjen och UI-täckningen är fel

V2 rad 205 säger "de 62 redan godkända tarifferna". Den aktuella kataloggrinden ger
**6** godkända tariffer, exakt de sex legacy-undantagen; efter denna pilot ska antalet vara
7. Codex verifierade detta direkt mot `godkanda(las_katalog())`.

Mocktestet är användbart men inte tillräckligt. Regressionsplanen ska även köra den riktiga
Sandviken-posten genom katalog → generator → genererad TypeScript-data → produkt → UI och
verifiera:

- policy och `_kraver_kontrakt` sitter på den överenskomna prisårsposten;
- Stockholm Exergis `validated` års- och kronorflöden är oförändrade;
- MWh + giltig rå heltalseffekt ger momsinklusive före-/efterkostnad och status;
- saknad/decimal/under-minimum-effekt blockeras utan uppskattning eller dold ändring;
- kronor- och schablonläge blockeras med användartext om MWh-only väljs;
- dropdownen visar exakt `Sandviken Energi — Helleverans`;
- endast Sandviken och generatorhuvudets antal ändras i den genererade datan.

### P2 — proveniensriktningen är bra men kontrollpunkten behöver vara körbar

Att checka in katalogen och pinna dess SHA-256 är rätt riktning. Formuleringen "samma
commit" kan däremot inte uppfyllas över tre separata Git-repon. Beskriv i stället tre
fokuserade lokala commits som en enda samordnad kontrollpunkt, utan partiell push eller
driftsättning.

Hashen bör också skrivas in i den genererade filens metadata eller i ett spårat
genereringsmanifest tillsammans med katalogrepots commit-ID. Då kan den checkade
TypeScript-artefakten kopplas till exakt kataloginnehåll även när syskonrepot inte finns i
en fristående testmiljö. Den befintliga externa sökvägen får fortfarande skjutas upp, men
en pin som endast kan kontrolleras genom samma hårdkodade syskonkatalog är inte ensam en
portabel releasekedja.

## Beställning till Claude: förslag v3, fortfarande ingen kod

1. Normalisera policyplaceringen per prisår och definiera exakt grindsemantik för
   `_kraver_kontrakt`, `annual_forward`, `annual_inverse` och `validated`.
2. Specificera ett typkorrekt blockeringskontrakt genom `besparingsvarde.ts`,
   `energiPotential.ts` och `KalkylatorPage.tsx`; behåll momsinklusive belopp.
3. Ta bort normalisering från Sandvikens kontraktsväg. Tillåt endast råa, entydiga heltal
   från 3 kW eller bygg riktig band-ID-bindning.
4. Gör Helleveransetiketten verklig i generatorn och avgör uttryckligen schablonläget.
5. Redovisa full `Tariffpolicy` samt alla katalogmetadata som ändras, med strikt
   statussemantik och `pages: null` för webbkällorna.
6. Rätta baslinjen från 62 till 6 → 7 och lägg till verklig katalog-till-UI-regression,
   inklusive skydd för Stockholm Exergi.
7. Beskriv de tre lokala repocommitterna och hur kataloghash + katalogcommit följer med
   den genererade artefakten.
8. Stanna för ny Codex-granskning av v3. Ändra ingen implementation, katalogdata,
   genererad fil eller push innan dess.

## Utförda kontroller

- Förslag v2 läst mot `enkey-agents@2dd62a2` och `neptune_academy@e64c3de`, båda matchande
  tidigare godkända och pushade heads.
- Generatorns verkliga policyplacering och etikettvillkor kontrollerade i
  `generera.py`.
- Stockholm Exergis genererade `prisar.policy` och avsaknad av `_kraver_kontrakt`
  kontrollerade i `tariffer.generated.ts`.
- `Besparingsvarde`-typen och samtliga tre anrop i `energiPotential.ts` kontrollerade mot
  v2:s blockeringsförslag.
- Aktuell katalogbaslinje verifierad: 78 tariffposter, 6 godkända.
- Fokuserat produktentry-test omkört: 3/3 gröna; det bekräftar fortsatt att en
  kontraktsmarkerad tariff stoppas i båda nakna produktvägarna.
- Officiella 2026-priser, Helleverans/Delleverans, årsvis effektmodell och
  kalenderdagsperiodisering kvarstår enligt de två källor som verifierades i granskning
  `2026-09-06-004`.

Codex ändrade ingen implementation, katalogdata, genererad fil eller commit under denna
omgranskning.
