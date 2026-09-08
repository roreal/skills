---
review_id: "2026-09-06-006"
date: "2026-09-06"
reviewer: Codex
status: approved-with-conditions
scope:
  - "Förslag 2026-09-06-001, version 3"
  - "Sandviken Energi Helleverans, annual_forward och MWh-only"
reviewed_heads:
  enkey-agents: "2dd62a2"
  neptune_academy: "e64c3de"
approved_implementation_scope: "sandviken-helleverans-annual-forward-mwh-only"
inverse_status: "not-approved"
implementation_changed: false
push_status: "ingen ny implementationskod; nästa kontrollpunkt ska vara lokal kodgranskning"
---

# Godkännande med villkor: Sandviken-förslag v3

## Beslut

V3 godkänns för en **avgränsad lokal implementation** av Sandviken Energi —
Helleverans i kalkylatorns framåtriktade årskalkyl med faktiskt angiven MWh och
leverantörens debiterbara effekt.

Ingen v4-plan behövs före kodning om implementationen följer villkoren nedan. Claude får
skapa tre fokuserade lokala commits, en per repo, och ska därefter stanna för Codex
kodgranskning. Godkännandet omfattar inte push, kronor→MWh-invers, schablonberäkning,
Delleverans eller någon annan ny tariff.

## Det som godkänns i v3

- Katalogpolicy placeras per prisår, på samma strukturella nivå som
  `_kraver_kontrakt` och Stockholm Exergis befintliga policy.
- Produktadaptern styrs av den exakta kontraktsmarkören, inte av allmän policyförekomst.
- Stockholm Exergis `validated`-policy utan markör ska förbli helt utanför den nya
  årsadaptern.
- Blockering hanteras som ett förväntat domänfel, inte som ett partiellt numeriskt
  `KalkylatorResult`.
- Momsinklusive `summaInkl` bevaras.
- Sandvikens inmatade effekt förs oförändrad till kontraktet; decimaler och värden under
  tariffens publicerade minimum avvisas i stället för att avrundas eller klämmas.
- Både kronorläge och schablonläge hålls utanför piloten.
- Policyns exakta `KravPost`, `annual_forward`-täckning och statiska
  kapacitetsbindning är specificerade.
- Aktuella 2026-webbkällor, Helleveransidentitet och
  `days_in_month/days_in_year` ingår i katalogdiffen.
- Den ospårade katalogen ska checkas in och knytas till generatorartefakten med
  innehållshash och Git-version.

## Bindande implementationsvillkor

### 1. Kontraktsgrinden ska vara helt fail-closed

V3 rad 62 får inte returnera `undefined` när `_kraver_kontrakt === true` men policyn
saknar `annual_forward`. Markör + saknad policy, ogiltig policy eller saknad täckning är
ett konfigurationsfel och ska kasta innan någon naken motorväg nås. Endast avsaknad av
markör får returnera "ingen kontraktsadapter".

Den delade hjälpen måste vara faktiskt åtkomlig för de konsumenter v3 namnger, antingen
som en exporterad och testad kapabilitetsresolver eller genom ett annat gemensamt publikt
gränssnitt. Duplicera inte rå `_kraver_kontrakt`-/policytolkning i React-sidan.

Minimikrav:

- markör saknas + `validated`-policy → befintlig årsprognos och invers oförändrade;
- markör sann + policy saknas/är trasig/saknar `annual_forward` → tydligt
  konfigurationsfel, aldrig naken fallback;
- markör sann + `annual_forward` men utan `annual_inverse` → MWh-vägen tillåts och
  kronorvägen blockeras som förväntat användarfall.

### 2. Lyckade resultat ska bära status; alla felvägar ska vara typade

`KontraktBlockerat` är rätt modell för att hindra ett partiellt resultat från att nå
`calcResult`. V3 säger samtidigt att `Besparingsvarde` lämnas helt orört, vilket skulle
kasta bort fasadens status på ett lyckat resultat. Lägg därför till ett typat
`resultatstatus` på det kompletta kontraktsresultatet, exempelvis som ett valfritt fält på
`Besparingsvarde` så legacy-vägarna förblir kompatibla. Före- och efteranropets status ska
kontrolleras; ett blockerat fasadanrop får aldrig derefereras med `!`.

Domänfelet behöver en maskinläsbar orsak, minst:

- `missing_capacity`;
- `invalid_capacity`;
- `unsupported_input_mode`.

Annars skulle decimalen 49,4 kW visas som "effekt måste anges" trots att användaren
faktiskt angav ett värde. Både den tidiga kronorvägens catch och catch-blocket kring
`calcResult` ska översätta domänfelet till korrekt svensk användartext. Den interna
strängen `KONTRAKT_BLOCKERAT:<id>` får inte bli det synliga kronorfelet.

Före- och efterkostnad ska fortsätta använda `kostnad.summaInkl`. Lägg en explicit
momsregression så `summaExkl` inte kan återinföras.

### 3. Effekten ska valideras i domänlagret och förbli oförändrad

Sandvikens kontraktsväg ska kräva:

```text
Number.isFinite(kw) && Number.isInteger(kw) && kw >= 3
```

Det godkända värdet ska föras byte-/talidentiskt till `IndataPost.varde` med
`kallaTyp: "supplier_value"`; ingen `normaliseraKapacitet`, `Math.round`, golvklämning
eller annan dold omvandling får förekomma. Den befintliga normaliseringen för legacy-
tariffer lämnas oförändrad.

UI:t ska dessutom markera fältet som obligatoriskt för Sandviken och använda dynamiskt
`required`, `min=3` och `step=1`, men domänkontrollen är fortfarande auktoritativ så andra
anropare inte kan kringgå kravet. Testa acceptans för 3, 49, 50, 199 och 200 samt
blockering för saknat värde, 2, 2,9, 49,4/49,5/49,6, 199,9, 200,1, `NaN` och oändlighet.

### 4. MWh-only betyder ett faktiskt positivt MWh-värde

Det räcker inte att `energyInputMode === "mwh"`; dagens formulär faller tillbaka på
areabaserad schablon om MWh-fältet är tomt eller inte ger ett positivt `knownEnergy`.
När Sandviken är vald ska därför även tomt, ogiltigt, noll eller negativt MWh-värde
blockeras före `calcResult`. Det får aldrig tyst bli schablon.

Kronor- och schablonläge ska blockeras med tydlig text så snart användaren försöker
beräkna. Den auktoritativa spärren ska dessutom finnas i produkt-/domänlagret; UI-
förkontrollen är bara användarhjälp.

### 5. Använd en explicit etikettregel och bevara stabila ID:n

V3:s föreslagna generella villkor på rad 153–158 godkänns **inte som skrivet**. Codex
kontrollerade det mot den riktiga katalogen: det skulle även byta visningsnamn för tre
befintliga ensamt godkända tariffer till bland annat `Göteborg Energi — Göteborg`,
`Halmstads Energi och Miljö — Halmstad` och
`Mölndal Energi — Mölndal, Kållered och Lindome`. Påståendet att ingen befintlig medlem
påverkas är alltså fel.

Använd i stället en explicit opt-in för produktnamn, eller en lika snäv regel som endast
gäller nya kontraktsstyrda katalogtariffer och har ett regressionstest för samtliga
befintliga namn. Sandvikens verkliga genererade visningsnamn ska bli exakt
`Sandviken Energi — Helleverans` utan leverantörshårdkodning i produktkoden.

Säkerställ samtidigt att Sandvikens leverantörs-ID inte byter betydelse eller försvinner
den dag ytterligare en Sandvikenprodukt godkänns. En lämplig väg är att alltid använda
det stabila tariffbaserade ID:t för nya, icke-legacy katalogtariffer och bevara befintliga
legacy-ID:n oförändrade.

### 6. Katalogmetadata och proveniens ska vara reproducerbara

`investigation: null`, `issues: []`, `network_or_product: "Helleverans"`, de två
`pages: null`-referenserna och den fullständiga policyn godkänns. Att låta
`production_ready: false`, `calculation_status` och `component_completeness` ligga kvar är
acceptabelt i denna kontrollpunkt eftersom den separata, granskade adaptern och
aktiveringsgrinden uttryckligen begränsar omfattningen.

Komplettera dock katalogändringen med:

- nytt `as_of` och `retrieved_on` för kontrolltillfället;
- en `change_log`-post som anger Sandviken Helleverans, källorna, effektkravet,
  periodiseringen och aktiveringsomfattningen;
- schema-/revisionsuppdatering om en ny explicit etikettmarkör införs.

Lägg endast till den avsedda katalogfilen i `skills`-committen; använd inte `git add .` i
den nuvarande arbetskopian med många andra ospårade Ellen-filer.

Hashpinnen ska jämföras mot exakt kataloginnehåll. V3:s hänvisning till
`test_synk.py:s _FORVANTAD_SHA256` är fel: den befintliga motsvarigheten finns i
`test_resultatkontrakt_vektorer.py`. Kataloghash och katalogrepots commit-ID ska matas
deterministiskt till ett spårat manifest eller generatorhuvud; låt inte vanliga
fixture-anrop dynamiskt fråga Git efter aktuell arbetskopia.

### 7. Regressions- och leveransgränsen

Före nästa Codex-kontrollpunkt ska minst följande vara grönt:

- kataloggrinden går från exakt 6 till 7 godkända tariffposter;
- samtliga **6** befintliga legacy-tariffer, riksgenomsnittet och Stockholm Exergis två
  prisår behåller tidigare ID, etiketter och beräkningsresultat;
- Sandvikens policy och markör ligger tillsammans på rätt prisårspost;
- riktig katalog → generator → genererad data → produkt → UI verifieras, inte bara en
  mock;
- faktiskt MWh + giltig rå heltalseffekt ger momsinklusive före-/efterkostnad och bär
  `complete`-status;
- saknad/ogiltig effekt samt kr/schablon/tomt MWh blockeras med rätt orsak och text;
- endast avsedda Sandviken-/proveniensfält skiljer sig i genererad data;
- Python- och TypeScript-sviter, typkontroll, produktionsbygge, katalog-/fixture-synk och
  `git diff --check` är gröna.

Claude får därefter redovisa de tre lokala commit-hasharna och testresultaten. Ingen push
före ny Codex-kodgranskning och Roberts beslut.

## Verifierat nuläge

- V3 är endast ett förslag; ingen implementationskod eller katalogdata har ändrats.
- `enkey-agents@2dd62a2` och `neptune_academy@e64c3de` är de tidigare granskade och
  pushade heads; implementationsarbetskopiorna är rena.
- Katalogen innehåller 78 poster och grinden ger 6 godkända.
- De sex befintliga katalogtariffernas verkliga medlems-/produktnamn kontrollerades; v3:s
  generella etikettvillkor skulle ändra Göteborg, Halmstad och Mölndal.
- Det tidigare fokuserade produktentry-testet är fortsatt relevant; ingen ny testsvit
  kördes eftersom v3 inte innehåller kod.

Codex ändrade ingen implementation, katalogdata, genererad fil eller commit under denna
granskning.
