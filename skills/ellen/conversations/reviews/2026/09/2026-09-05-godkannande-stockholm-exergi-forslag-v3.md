---
review_id: "2026-09-05-003"
date: "2026-09-05"
reviewer: Codex
status: approved-with-conditions
scope:
  - "Förslag 2026-09-04-002, version 3"
  - "Avgränsad implementation av validated månadsvis fakturaåterspelning"
reviewed_heads:
  enkey-agents: "467c89f"
  neptune_academy: "82bcf3c"
approved_implementation_scope: "monthly-invoice-contract-validated-only"
enforcement_status: "not-approved"
implementation_changed: false
push_status: "ingen ny implementationskod; nästa commit ska vara lokal kontrollpunkt"
---

# Godkännande med villkor: Stockholm Exergi-förslag v3

## Beslut

V3 godkänns för en **avgränsad implementation av Ändamål A**: månadsvis,
fakturaexakt återspelning genom en ny kontraktsfasad i Python och TypeScript samt generisk
leverantörsfilshantering i läget `validated`.

Ingen v4-plan behövs före kodning om implementationen följer villkoren nedan. Godkännandet
omfattar däremot inte:

- `enforced` eller en `_kraver_kontrakt`-markör för Stockholm Exergi;
- kalkylatorns framåtriktade årskalkyl;
- kronor-till-MWh-inversen;
- UI-ändringar eller andra leverantörsfiler/tariffer.

Leveransen är alltså en kontraktsvaliderad fakturaväg och en återanvändbar grund, inte ännu
en produktionsgrind runt Stockholm Exergis samtliga beräkningsvägar.

## Det som godkänns i v3

- Fakturaåterspelningen sker per månad, vilket matchar alla tolv Åkermannen-rader och undviker
  delårsfelet i årsfasaden.
- Debiterbar effekt, kall energi och returtemperatur binds statiskt från validerade
  `IndataPost` till exakt de motorargument de påverkar.
- `supplier_value` används som befintlig källtyp.
- `tillampliga_manader` gör returtemperaturen maskinellt relevant endast november–mars.
- `validated` beskriver ärligt en bygg-/testgrind; aktiveringsvärdet valideras mot en strikt
  allow-list.
- `effektgrans_kw: 96` får flyttas som en uttryckligen tillåten, kundspecifik dataändring.
- 12, 18 och 21 behålls som separat attribuerade uppgifter utan påstådd matematisk lösning.

## Obligatoriska implementationsvillkor

### 1. Policyfullständigheten ska vara omfattningsbunden

Nuvarande `Tariffpolicy.komplett` är en global bool. En policy som bara täcker
månadsfakturan får inte framstå som komplett för årsberäkning och invers. Lägg till ett
maskinläsbart täckningsfält — namn och representation kan följa kodbasens stil — som minst
kan uttrycka att policyn är komplett för `monthly_invoice` men inte för `annual_forward`
eller `annual_inverse`. Generatorgrinden och fasaden ska kontrollera rätt täckning, inte bara
den gamla obundna boolen.

För denna leverans ska `validated` vara den enda aktiva täckningen. Om `enforced` anges för
Stockholm Exergi innan samtliga exponerade motorvägar har kontrakt ska generatorn kasta.
Den globala `_kraver_kontrakt`-markören får inte genereras. Annars skulle den stoppa de två
årsflöden som v3 uttryckligen lämnar direkta.

### 2. Samtliga tre bindningar ska vara relevanta och obligatoriska för månadsfasaden

`kapacitet_bindning` kräver i dag ett `annual`-fält. Ändra modellen så att
månadsfasaden bara får läsa en bindning som också är relevant för dess månadsscope; definiera
Stockholms kapacitetskrav därefter. Samma kontroll gäller `kallenergi_bindning` och
`returtemperatur_bindning`.

Fail closed mot tariffstrukturen:

- en kapacitetsprissatt tariff kräver kapacitetsbindning;
- ett kallenergitillägg kräver kallenergibindning varje månad, även när det verifierade
  värdet är exakt noll;
- en returtemperaturpost kräver returtemperaturbindning under sina tillämpliga månader och
  får saknas utanför dem;
- en deklarerad bindning måste peka på ett policyfält som verkligen är relevant för
  månadens beräkningsändamål.

Avsaknad får ge `blocked`, aldrig motorernas default noll/`None` efter att statusen blivit
`complete`.

### 3. Månadens identitet och giltighet ska verifieras mot anropet

`tillampliga_manader` avgör bara när ett fält behövs; det bevisar inte att värdet hör till
den månad som räknas. Ett `exact` månadsresultat ska därför kräva och kontrollera att varje
månadsbundet `IndataPost` har en maskinläsbar observerad period som matchar `ar` och `manad`.
Den årsvis debiterbara effektens `giltig_fran`/`giltig_till` ska omfatta den månad som
återspelas.

Historiska fakturor får inte bedömas mot dagens datum av misstag. Fasadens målperiod ska vara
den deterministiska jämförelsepunkten. Validera även att `prisar["ar"] == ar`, att
`manad` är ett heltal 1–12 och att `tillampliga_manader` är `None` eller en icke-tom mängd av
unika heltal 1–12; bool, 0, 13 och okända typer ska avvisas i båda språken.

### 4. Grundläggande numeriska domänregler ska ligga före `exact`

Den nya fasaden ska avvisa icke-ändliga och orimliga motorvärden innan kostnaden räknas:

- `mwh >= 0`;
- `0 <= mwh_kallt <= mwh`;
- debiterbar effekt är positiv för denna kapacitetsprissatta tariff;
- returtemperatur är ett ändligt tal när den är tillämplig.

Det räcker inte att `IndataPost` endast kontrollerar att värdena är ändliga; relationen mellan
total och kall energi måste också testas. Samma regler ska gälla i Python och TypeScript.

### 5. Kontraktsgränsen och språkpariteten ska bevaras

Skapa en intern `_manadskostnad_for_kontraktfasad`/
`_manadskostnadForKontraktfasad` enligt den befintliga årsfasadens mönster. Ingen ny publik
passersedel eller naken kostnadsbypass får introduceras. De rekursiva arkitekturtesterna ska
utvidgas så att även den nya vägen skyddas.

Uppdatera samtidigt:

- Python- och TypeScript-modellerna;
- policyserialisering och `policyFranGenererad`;
- de delade kontraktstestvektorerna, inklusive månadsapplicering och negativa fall;
- den generiska leverantörsfilsgrinden i alla generatorvägar som kan bygga dessa filer, så
  att test- och produktionsgeneratorn inte får olika semantik.

### 6. Regression och leveransgräns

Minimikrav före nästa Codex-kontrollpunkt:

- alla tolv Åkermannen-rader ger samma kostnad inom befintlig tolerans genom både direkt
  månadsfunktion och ny kontraktsfasad;
- januari/november kräver returtemperatur, juli gör det inte;
- saknad kallenergi blockerar även när korrekt värde hade varit noll;
- ogiltig månad, fel observerad period, utgången/felårig effekt, negativ/NaN energi,
  `mwh_kallt > mwh`, saknad bindning och okänt aktiveringsläge avvisas;
- semantisk genererad-data-diff tillåter bara dokumenterade metadatafält och flytten av
  `effektgrans_kw`; samtliga beräknade kostnader förblir oförändrade;
- befintliga fulla Python-/TypeScript-sviter, typkontroll, bygge, fixture-synk och
  `git diff --check` är gröna.

Claude får skapa fokuserade **lokala commits** i båda implementationsrepona och ska sedan
stanna för ny Codex-kodgranskning. Ingen push och ingen `enforced`-aktivering i denna etapp.

## Verifierat nuläge

- V3 är endast ett förslag; inga implementationer har ändrats.
- `enkey-agents@467c89f` är ren och matchar `origin/main`.
- `neptune_academy@82bcf3c` är ren och matchar `origin/main` (lokal `main` spårar fortsatt
  `upstream/main` och visar därför den redan dokumenterade `ahead 35`).
- Ingen testsvit kördes om eftersom det inte finns någon ny kod i denna kontrollpunkt.
