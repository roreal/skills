---
handoff_id: "2026-09-14-001"
created_at: "2026-09-14T08:16:28+02:00"
from: Codex
to: Claude
status: changes-required-after-review-2026-09-14-006
implementation_allowed: true
approved_implementation_scope: "batch-4-jamtkraft-umea-flow-difference-and-umea-b"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
baseline_remote_heads:
  skills: "8b12daa9cbdb3f392bc6a5d20a32ae6f89f6c2b3"
  enkey_agents: "49f09078e6ed0acb0a7c05a104694110cf59b3e2"
  neptune_academy: "5e0d710f993b1058cf39c652eb45d171ca766406"
tariff_disposition_before: "33 implemented / 31 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "33 implemented / 31 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "37 implemented / 27 ready / 28 blocked av 92"
relates_to:
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-4.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 4"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §6a.2 och §6a.3"
  - "Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md — Jämtkraft och Umeå Energi"
---

# Uppdrag till Claude: Batch 4 — Jämtkraft och Umeå

## Mål och stoppunkt

Implementera lokalt exakt följande fyra `annual_forward`-produkter bakom deras befintliga
`investigation.status="utreds"`-spärrar:

1. `jamtkraft-ostersund-froson-as-2026`
2. `jamtkraft-brunflo-och-opevagen-2026`
3. `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
4. `umea-energi-umea-enkel-2026`

Kalkylen ska skapa uppskattad årskostnad från tolv MWh-värden och leverantörs-/fakturavärden.
Resultatstatus ska vara `annual/snapshot/complete`, aldrig `exact`. Kronor, schablon,
besparingsvärdering och månadsfakturagaranti ingår inte.

Detta är endast implementation bakom spärr. **Aktivera inte och pusha inte.** Commitera
fokuserat lokalt i berörda repon, dokumentera hash/tester och stanna för Codex granskning.

## 1. Källor och katalogproveniens

### Jämtkraft

Officiella källor:

- prismodell: `https://www.jamtkraft.se/foretag/fjarrvarme/priser/prismodell/`
- prisändringsmodell 2026–2028:
  `https://www.jamtkraft.se/wt/documents/519/Pris%C3%A4ndringsmodellen_2026-2028.pdf`

Katalogens `15_0` är ett 2025-dokument på Prisdialogen och får inte fortsätta anges som
priskälla för 2026-värdena. Hämta de officiella PDF-bytesen och lägg en ny källpost `15_1`
med korrekt titel, URL, verklig SHA-256, `retrieved_on` och kind. Verifiera de faktiska
PDF-sidorna mot bytesen och byt de tre Jämtkraftradernas `source_refs` till `15_1` för
sidorna som bär effekt-/energipriser, effektmetod och flödesformel. Bevara `15_0`
oförändrad som historisk källa. Commitera inte rå-PDF:en.

Fyll `capacity.billing_basis_method` med den källverifierade metoden: debiterbar effekt är
medelvärdet av de tre högsta dygnsmedeleffekterna; dygnsmedeleffekt bygger på dygnets
maximala energiuttag delat med 24, och värdet gäller tills ett högre uppmätt värde finns,
dock högst 12 månader. Kalkylatorn tar leverantörens redan beräknade värde.

Ta bort endast den lösta issue-/investigationtexten om omappad effektmetod. Behåll den
separata upplysningen att månadsperiodisering inte är verifierad. Den får inte blockera
`annual_forward`, men ska fortsatt blockera påstående om reproducerad månadsfaktura.

### Umeå Energi

Officiella källor:

- Enkel 2026: `https://www.umeaenergi.se/foretag/varme/priser/prisavtal-enkel`
- prisvillkor: `https://a.storyblok.com/f/162274/x/bed500e2ec/prisvillkor-fjarrvarme.pdf`
- prismodell: `https://www.umeaenergi.se/foretag/varme/priser/prismodell`

Återverifiera katalogens `web-review-umea-enkel` och `web-review-umea-terms` mot aktuella
officiella källor och uppdatera endast verklig proveniens. Bevara `45_0` historiskt;
använd inte 2025-källan för att motivera 2026-priser som de officiella 2026-källorna redan
styrker. Ta bort issue-raden om omappat `B` först när hela bindningen, motorn och
tvåpassgrinden nedan finns och är testade. Andra Umeå-avtal ligger utanför just denna
katalograd och får inte öppnas indirekt.

## 2. Nya flödesformler i båda språken

Utöka den slutna allow-listan och motordispatchen med exakt två typer:

### `flow_difference`

För Jämtkraft:

```text
W_säsong = summan av mwh_per_manad för [1,2,3,4,10,11,12]
diff_m3 = flode_okt_apr_m3 - reference_m3_per_MWh × W_säsong
justering_kr = rate × diff_m3
```

Katalogvärdena ska vara `rate=3`, `reference_m3_per_MWh=19` och exakt sju månader.
Positivt resultat är avgift, negativt är bonus/kreditering. Ingen golvbegränsning.

### `asymmetric_flow_difference`

För Umeå:

```text
W_säsong = summan av mwh_per_manad för [1,2,3,4,10,11,12]
diff_m3 = flode_okt_apr_m3 - reference_m3_per_MWh × W_säsong
justering_kr = bonus_rate × diff_m3, om diff_m3 < 0
justering_kr = fee_rate × diff_m3, om diff_m3 >= 0
```

Katalogvärdena ska vara `reference_m3_per_MWh=17`, `bonus_rate=3`, `fee_rate=7` och
exakt sju månader. Asymmetrin gäller den sammanlagda oktober–aprilperioden, inte en separat
teckenprövning månad för månad.

Bygg en statisk, fail-closed bindningskontroll som för de fyra avsedda raderna verifierar
typ, formelparametrar, enhet, exakt månadsmängd och att policyn har ett unikt numeriskt
flödesfält. Fel typ, strängreferens, extra/saknad månad, icke-ändligt tal, saknad bindning
eller oväntad formel ska blockera före produktgenerering.

Öppna inte Vattenfalls blockerade användning av `asymmetric_flow_difference`:
`reference_m3_per_MWh="network_average"` är dynamisk och ska fortsatt avvisas. Lägg en
direkt regression som bevisar detta.

## 3. Kapacitetsmultiplikator för Umeå

Beräkna Umeås årseffektkostnad som:

```text
(band.fixed + band.variable × A) × B
```

`A` är leverantörens debiterbara årseffekt i kW. `B` är leverantörens redan beräknade
faktor. Räkna aldrig själv ut `U` eller `B` från rå energidata.

Det redan typade policyfältet `kapacitet_multiplikator_bindning` ska transporteras genom
den verkliga kontraktsfasaden till kapacitetsberäkningen i Python och TypeScript. Lägg en
generisk valfri motorparameter, men använd den endast när katalogens kapacitet har en
deklarerad `post_multiplier` och policyn binder samma värde. Saknad bindning, saknat värde,
icke-ändlig numerik, värde utanför policyintervallet, multiplikator på fel tariff eller
strukturavvikelse ska falla stängt.

Umeås policy kräver `B` inom `[0.93, 1.401]`. Intervallkontrollen hör till den befintliga
kontraktsförkontrollen och `harled_resultatstatus`/`harledResultatstatus`. Ett direkt
motoranrop ska ändå validera ändlighet och avsedd struktur som försvar på djupet.

## 4. Strikt kompositgrind

Ändra inte den nakna `grind()` i `katalog.py`; den ska fortsatt returnera
`"kapacitetsformel med multiplikator"` för Umeå och alla andra `post_multiplier`-rader.

Utöka `godkanda(katalog, policyregister=...)` med ett snävt tvåpass endast när det första
avslaget är exakt detta:

1. slå upp tariff-ID:t i det explicit injicerade policyregistret;
2. kör `kontrollera_kompositgrind(tariff, policy)`, som verifierar att
   `kapacitet_multiplikator_bindning` pekar på ett befintligt numeriskt krav och att
   katalogens statiska multiplikatorstruktur är just den stödda formen;
3. skapa en grund kopia, ta bort endast `capacity.post_multiplier` och kör hela vanliga
   `grind()` igen;
4. godkänn bara om andra passet ger `None`.

Mutera aldrig originalkatalogen. För samma `policyregister` vidare från generatorns alla
entrypoints. `godkanda(katalog)` utan Umeåpolicy, en okänd multiplikator, en dold issue och
en dold okänd justering ska var för sig fortsatt blockera.

Kompositgrinden ser ingen kundindata och får därför inte påstå sig validera `B=14`.
Rätta den stale meningen i `tariffinventering-v22.md`: `B=14` blockeras i
kontraktsförkontrollen, inte av `kontrollera_kompositgrind()`.

## 5. Tariffpolicyer och UI

Skapa fyra separata policyer med `tackning=frozenset({"annual_forward"})`,
`stodjer_aktuell_arskostnad=True` och `stodjer_besparing=False`.

Jämtkraft ska ha exakt tre tariffspecifika policyfält:

- debiterbar effekt, kW, `supplier_value`, icke-negativ;
- bekräftat band-ID, `supplier_confirmed_band_id`, allow-list från respektive tariff;
- `Flöde 1 oktober–30 april`, m³ för perioden, `supplier_value`, icke-negativt.

Umeå ska ha exakt fyra tariffspecifika policyfält:

- debiterbar årseffekt `A`, kW, `supplier_value`, icke-negativ;
- bekräftat band-ID, `supplier_confirmed_band_id`;
- `Flöde 1 oktober–30 april`, m³ för perioden, `supplier_value`, icke-negativt;
- `Kapacitetsfaktor B`, dimensionslös, `supplier_value`, min 0,93 och max 1,401.

Använd unika policynycklar per tariff så att leverantörs-/produktbyte inte återanvänder
värden tyst. Om befintligt snapshotkontrakt kräver observerad period/fakturamånad ska den
transporteras som befintlig periodmetadata och testas; redovisa den inte felaktigt som ett
ytterligare tariffspecifikt policyfält. Hjälptexterna ska säga var värdena finns
(faktura/leverantör) och att flödet avser just oktober–april, inte m³/år.

Kronor och schablon ska ge `unsupported_input_mode`; besparing ska ge
`besparing_ej_stodd`. Saknat/ogiltigt effekt-, band-, flödes- eller B-värde ska ge
fältnära `saknadeFalt`/`ogiltigaFalt` före motoranrop.

## 6. Oberoende golden-facit

Använd minst följande gemensamma indataserie: 10 MWh i var och en av årets 12 månader,
`A=20 kW`, band `1`. Oktober–aprilenergin är då 70 MWh. Förväntat ska räknas från explicita
pristal i testet, aldrig genom samma produktionsfunktion som verifieras.

### Jämtkraft, flöde 1 400 m³

Referensflödet är `19 × 70 = 1 330 m³`; justeringen är `+210 kr`.

| Tariff | Energi exkl. moms | Effekt exkl. moms | Flöde | Totalt exkl. moms | Totalt inkl. 25 % moms |
| --- | ---: | ---: | ---: | ---: | ---: |
| Östersund/Frösön/Ås | 55 540 | 32 120 | 210 | 87 870 | 109 837,50 |
| Brunflo/Opevägen | 60 340 | 32 120 | 210 | 92 670 | 115 837,50 |
| Åre m.fl. | 68 560 | 32 120 | 210 | 100 890 | 126 112,50 |

Testa också referensflödet 1 330 m³ → 0 kr och 1 260 m³ → −210 kr.

### Umeå

Energin är 56 400 kr exkl. moms och band 1 före B är
`21 + 1 018 × 20 = 20 381 kr`.

- `B=1`, flöde 1 260 m³: referens `17 × 70 = 1 190`, flödesavgift 490 kr,
  totalt 77 271 kr exkl. moms och 96 588,75 kr inkl. moms.
- `B=0,93`, referensflöde 1 190 m³: effekt 18 954,33 kr och totalt
  75 354,33 kr exkl. moms.
- `B=1,401`, referensflöde: effekt 28 553,781 kr och totalt
  84 953,781 kr exkl. moms.
- `B=1`, flöde 1 120 m³: flödesbonus −210 kr.

Pinna samma facit i Python och TypeScript samt jämför kostnadsdelarna, inte bara totalen.
Lägg gränsfall för `B=0,93`, `B=1,401`, strax under/över, `B=14`, NaN och oändlighet.

## 7. Acceptansbevis före aktivering

1. Katalogen har fortsatt **86** poster. Alla fyra rader finns kvar med
   `production_ready:false` och `investigation.status="utreds"`.
2. `godkanda(katalog)` ger fortsatt exakt **33**. De fyra stoppas av implementationsspärren,
   inte av en okänd ny formel eller saknad policy.
3. En isolerad katalogkopia där exakt de fyra spärrarna rensas, och där samma explicita
   policyregister används, ger exakt **37** katalogprodukter. Naken Umeågrind utan policy
   ska fortfarande blockera.
4. Den skarpa genererade payloaden har fortsatt **35 produkter totalt**: 33 katalogprodukter
   och 2 befintliga leverantörsfiler. Inget av de fyra Batch 4-ID:na får finnas där.
5. Testa katalog-/policybindning och prisparitet för alla fyra, inklusive källa, energins
   tolv priser, kapacitetsband, rate period, flödesparametrar och policy-ID.
6. Testa säsongssemantiken med energi utanför oktober–april: den ska påverka energiavgiften
   men inte flödesreferensen. Testa nollpositiv, bonus och avgift.
7. Testa alla felvägar fältnära samt produktbyte Jämtkraft↔Umeå och mellan två Jämtkraft-ID:n.
8. Lägg ett riktigt komponent-/E2E-prov med injicerad kandidat för Jämtkraft och Umeå som
   visar rätt fält, enheter, normal submit och `annual/snapshot/complete`.
9. Generator-synk ska vara reproducerbar. Före aktivering får inga nya skarpa produkter
   tillkomma och inga befintliga pris-/policyvärden ändras.
10. `tariffinventering-v22.md`, `batchplan-v22.md` och verifieringslistan uppdateras endast
    till faktiskt lokalt implementationsläge bakom spärr. Flytta inte dispositionen till
    implemented.

## 8. Leveransordning

1. Gör källa/katalog, motor, grind, policy, produktadapter/UI, dokumentation och tester.
2. Regenerera artefakten och bevisa 86 katalogposter, 33 godkända katalogprodukter,
   35 skarpa totalprodukter samt 33/31/28 av 92.
3. Kör riktade tester, full Python, full TypeScript, `npx tsc --noEmit`, isolerat bygge,
   E2E, generatorsynk och `git diff --check`.
4. Commitera fokuserat lokalt per repo utan användarens orelaterade filer eller befintliga
   `dist`-ändringar.
5. Logga exakta commit-hashar, diffomfattning, räkningsbevis och testresultat i
   `conversations/sessions/2026/09/2026-09-14-batch-4-jamtkraft-umea.md`.
6. Stanna för Codex granskning.

**Ingen aktivering och ingen push i denna etapp.**

## Codex granskning 2026-09-14-004

Den lokala implementationen vid `skills@e8341ce` (katalog `c1d8320`),
`enkey-agents@69b3060` och `neptune_academy@289b9c0` är granskad med beslutet **changes
required före aktivering**. Bindande fynd och exakt rättningsordning finns i
`conversations/reviews/2026/09/2026-09-14-granskning-batch-4-implementation.md`.

Claude ska rätta den dubbelriktade katalog–policy–motorbindningen för multiplikatorn, göra
komposit- och justeringsscheman strikt fail-closed, lägga det beställda verkliga UI-/E2E-
provet inklusive produktbyte och synka levande dokumentation. Spärrarna och 33/31/28 ska
ligga kvar. Ingen aktivering och ingen push är godkänd; stanna efter fokuserade lokala
commits för Codex omgranskning.

## Codex omgranskning 2026-09-14-005

Rättningsrunda 1 vid `skills@2ea4ae2`, `enkey-agents@dd51562` och
`neptune_academy@dd0ebaf` är omgranskad. Jämtkraftreproduktionen, unit/formula-schemat och
produktbytet är stängda, men multiplikatorns exakta struktur/policyintervall/direkta
motorintervall är fortfarande öppna. UI-assertioner, tvåpassregressioner och levande
dokumentationssynk återstår.

Följ exakt rättningsordning i
`conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-1.md`, behåll alla
fyra tariffspärrar och 33/31/28, commitera fokuserat lokalt och stanna för ny Codex
omgranskning. Ingen aktivering och ingen push är godkänd.

## Codex omgranskning 2026-09-14-006

Rättningsrunda 2 vid `skills@62b0bc9`, `enkey-agents@5a56c27` och
`neptune_academy@8e5bb96` är omgranskad. Multiplikatorns exakta struktur, policyintervall
och direkta talintervall är stängda; andra passet, produktbyte och statusbevis är också
gröna. Fyra avgränsade rättningar återstår före aktivering:

1. återställ Jämtkrafts tre verifieringsposter från felaktiga 36 månader/fakturamånad till
   källans och policyns senaste 12 månader;
2. gör saknad bunden effekt till ett faktiskt svenskt `#kapacitetKw-fel` med ARIA i både
   Jämtkrafts och Umeås komponentprov;
3. assertera explicit de synliga enheterna `kW` och `m³`;
4. avvisa `bool`/icke-numerisk kapacitetsmultiplikator i Pythons direkta motorvakt.

Följ exakt reproduktion och rättningsordning i
`conversations/reviews/2026/09/2026-09-14-omgranskning-batch-4-fixrunda-2.md`. Behåll alla
fyra tariffspärrar och 33/31/28, commitera fokuserat lokalt och stanna för ny Codex
omgranskning. Ingen aktivering och ingen push är godkänd.
