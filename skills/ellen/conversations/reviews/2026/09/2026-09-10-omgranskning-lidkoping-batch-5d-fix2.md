---
review_id: "2026-09-10-011"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 2"
  - "Samtliga fynd och acceptansbevis i granskning 2026-09-10-010"
reviewed_heads:
  skills: "e769eec0764bd0c07d53ed380de2cd9673be702f"
  enkey-agents: "6293e2a7e1c234062af4badd5ce199545e17eabc"
  neptune_academy: "b5d8466c75cb5e64407e924c5e17ca67560d2627"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-10-010"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 2

## Beslut

**Changes required.** Katalog-/generatorrättningarna och den officiella källproveniensen
är korrekta, men den genererade policyn tappar två säkerhetskritiska gränsattribut när den
läses in i TypeScript. Det gör att ett effektvärde utanför produktens intervall faktiskt
kan räknas och att ett otillåtet nollvärde för nätets Tm når motorn som ett otypat fel.

Ingen tariff är aktiverad och inget repo är pushat. Produktionsurvalet är fortsatt sju
tariffer och dispositionen 7 implementerade / 57 redo / 28 blockerade av 92 är
oförändrad.

## Fynd

### P1 — genererad policy tappar `maxvarde` och `minvarde_exklusiv`

Python-generatorn skriver båda attributen i den snake_case-formade policyn, men
`policyFranGenererad()` transporterar bara `minvarde`. Den skickar varken
`maxVarde: k.maxvarde` eller `minExklusiv: k.minvarde_exklusiv` till
`skapaKravPost()` (`resultatkontrakt.ts`, omkring rad 410–432).

Codex reproducerade detta genom samma genererade råform som den nya permanenta
produktfixturen använder:

- råpolicyn bar `maxvarde: 41`, men den inlästa policyn fick
  `maxVarde === undefined`;
- `beraknaArsprodukt()` accepterade därefter **42 kW i 0–41 kW-produkten** och
  returnerade `complete`;
- råpolicyn bar `minvarde_exklusiv: true` för nätets Tm, men den inlästa policyn fick
  `minExklusiv === undefined`;
- en Tm-serie med tolv nollor passerade därför den fältnära förkontrollen och nådde
  justeringsmotorn, som kastade ett vanligt `Error` med `Tm_m måste vara > 0` i stället
  för `KontraktBlockerat('invalid_policy_fields')` med fältnyckel och orsaken `min`.

Detta är ett produktfel inför aktiveringen, inte bara en testlucka. Lägg den saknade
transporten i `policyFranGenererad()` och ett genererat-policytest som bevisar att minst
`minvarde`, `minvarde_exklusiv`, `maxvarde`, `heltal`, `vardetyp`, kardinalitet och
attestering överlever snake_case → domänobjekt. Det publika Lidköpingstestet ska därefter
bevisa både maxfelet och Tm=0 som fältnära, typade domänfel innan kostnad räknas.

### P1 — 42+-produktens nedre gräns stoppas före den fältnära policyn

`beraknaArsprodukt()` kontrollerar `kapacitetKw < kapacitetsGolv(prisar)` och kastar
`KontraktBlockerat('invalid_capacity')` innan `byggKontraktIndata()` och
`forkontrolleraPolicyIndata()` körs (`besparingsvarde.ts`, omkring rad 581–597).

Codex verifierade att 41 kW för 42+-produkten visserligen stoppas, men felet saknar
`ogiltigaFalt`. React-sidan mappar endast `saknadeFalt`/`ogiltigaFalt` till
`policyFaltFel`; det dedikerade `kapacitetKw`-fältet får därför varken den nya synliga
felraden eller `aria-invalid`. Samma problem finns i den kontraktsgatade
besparingsadapterns tidiga kapacitetskontroll, även om Lidköpings besparingsprodukt i sig
är avstängd.

Låt den tidiga kontrollen endast stoppa verkliga typ-/numerikfel (saknat, icke-ändligt,
icke-heltal) och låt policybindningens `minVarde`/`maxVarde` vara enda auktoritativa
produktgräns, eller bifoga motsvarande fältnära detaljer i det tidiga felet. Normalfallet
ska vara en och samma väg för 0–41 och 42+ så att `min`/`max` alltid kan visas vid
`kapacitetKw`.

### P2 — acceptansproven går fortfarande runt de två felaktiga produktvägarna

De lägre gränstesterna i `resultatkontrakt.lidkoping.test.ts` bygger policyn direkt med
camelCase och ser därför inte felet i `policyFranGenererad()`. Den nya publika
produktfixturen använder rätt råform men provar bara giltiga 5 respektive 42 kW. UI-testet
har endast 0–41-fixturen och provar inga effektgränser. Därmed uppfylls ännu inte den
beställda matrisen 2/3/41/42 respektive 41/42 genom publik entry och riktig sida.

Följande uttryckliga luckor finns dessutom kvar:

- testet som påstår kr-/schablonblockering anropar bara `beraknaArsprodukt()` utan
  `energyProvenance`; det väljer varken `energyInputMode='kr'` eller `'schablon'`, och
  testnamnet säger `invalid_energy` medan assertionen kräver `missing_energy`;
- sidproven kör kr och schablon men kontrollerar bara att resultat saknas, inte den synliga
  blockeringsorsaken;
- Python har nu ett riktigt 1/12-anrop, men TypeScript-sviten har fortfarande inget
  Lidköpingsprov som anropar `manadskostnad()`/motsvarande periodiseringsmotor och
  verifierar tolv delar samt årssumman;
- UI-testet räknar rutorna men assertar inte januari–december-etiketterna, `°C` eller de
  verkliga hjälptexterna. Koden ser riktig ut, men regressionsbeviset saknas.

Lägg separata `calcResultForOnskadTyp()`-prov för kr och schablon med
`unsupported_input_mode`, kontrollera samma användarvända feltext i sidprovet, och gör
gräns-/månads-/enhets-/hjälptextmatrisen verkligt exekverad. Använd exakta literalsiffror
även för TypeScripts momsfacit 17 947,50 och 90 057,50 kr.

## Bekräftade rättningar

- En felskriven men syntaktiskt giltig serienyckel stoppas nu av generatorpreflighten och
  når inte artefakten.
- `minimum_billing_basis` avvisar sträng, bool, noll, negativt och icke-ändligt tal i
  kataloggrinden; TypeScriptmotorn har också en fail-closed runtimekontroll.
- Pythons riktiga 1/12-prov ger 794,166666… kr per månad och exakt 9 530 kr per år för
  0–41-goldenfallet; Python använder nu oberoende momsbelopp för båda tarifferna.
- De två giltiga publika årskostnadsfallen blir `complete`, och besparingsentryn kastar
  `Produktbegransning('besparing_ej_stodd')`.
- Månadsnamn renderas i sidkoden och kapacitetsfältet läser policyobjektets min/max; felet
  är att två av attributen inte når detta objekt och att den tidiga spärren saknar
  fältdetaljer.
- Officiella 2026-sidan finns som källa `20_3`; medlemmen och båda tarifferna refererar
  `20_2` och `20_3`. Kataloghashen och den genererade artefaktens källcommit
  `skills@e769eec` stämmer bitvis.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`: **507 passed**.
- `npm test -- --run`: **21 testfiler, 544 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: godkänd för de befintliga riksgenomsnitts- och
  Sandvikenscenarierna; `dist` återställd.
- Codex isolerade produktprov: **14 passed** och reproducerade samtidigt exakt de två
  tappade policyattributen, det felaktigt godkända 42 kW-fallet, det otypade Tm=0-felet,
  42+-produktens globala fel utan fältdetaljer samt korrekta typade kr-/schablonfel när
  den verkliga `calcResultForOnskadTyp()`-vägen anropas.
- Katalogens SHA-256 är
  `f1db6e63107f458faa5ce331b6e38ff33f62e14f07e6d3c5cbc18559d33e90e0`, identisk med
  både proveniensprovet och den genererade artefaktens header.
- `git diff --check` är rent för samtliga granskade commitintervall. Produktrepona är
  rena; sedan tidigare orelaterade filer i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Gör rättningsrunda 3, endast för fynden ovan. Transportera `maxvarde` och
`minvarde_exklusiv` genom `policyFranGenererad()`, och se till att kontraktsgatade
kapacitetsgränser ger `KontraktBlockerat('invalid_policy_fields')` med
`ogiltigaFalt=[{nyckel: kapacitetBindning, orsak: 'min'|'max'}]` i stället för ett tidigt
globalt fel.

Lägg permanenta regressionsprov genom den genererade råpolicyformen, båda publika
produkterna och den riktiga sidan för 2/3/41/42 respektive 41/42, Tm=0, båda faktiska
kr-/schablonlägena, TypeScripts verkliga 1/12-motor samt januari–december, enheter och
hjälptexter. Kör hela Python-/TypeScriptmatrisen, `tsc --noEmit`, bygge, E2E och
`git diff --check`. Gör fokuserade lokala commits och rapportera exakta HEAD-hashar.

Aktivera ingen tariff, ändra inte 7/57/28 och pusha inget repo. Stanna därefter för en ny
Codex-omgranskning.
