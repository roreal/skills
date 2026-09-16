---
handoff_id: "2026-09-15-002"
created_at: "2026-09-15T21:08:00+02:00"
from: Codex
to: Claude
status: "completed — pushad och remote-verifierad: skills@8356a71, enkey-agents@bebbb80, neptune_academy@ca02860"
implementation_allowed: true
approved_implementation_scope: "batch-5c-eight-seasonal-volume-tariffs"
tariff_activation_allowed: true
push_allowed: true
review_required_before_activation: true
review_required_before_push: true
baseline_remote_heads:
  skills: "df41660620f572b5b22d7dd27332c68b1be62049"
  enkey_agents: "5eaca3c4f3eafb3c7065319803592abe062f49ae"
  neptune_academy: "28ae62945ed50b23cffadd5a7b3070cc2d5c41ae"
tariff_disposition_before: "51 implemented / 13 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "51 implemented / 13 ready / 28 blocked av 92"
tariff_disposition_after_future_activation: "59 implemented / 5 ready / 28 blocked av 92"
sharp_products_before: "53"
sharp_products_during_implementation: "53"
sharp_products_after_future_activation: "61"
relates_to:
  - "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5c.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5c"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
---

# Uppdrag till Claude: Batch 5c — åtta säsongsflödestariffer

## Mål och stoppunkt

Implementera lokalt exakt följande åtta `annual_forward`-produkter bakom
deras befintliga `investigation.status="utreds"`-spärrar:

1. `lulea-energi-lulea-2026`
2. `oresundskraft-helsingborg-normal-2026`
3. `oresundskraft-angelholm-normal-2026`
4. `piteenergi-pitea-centrala-natet-2026`
5. `piteenergi-norrfjarden-och-sjulnas-2026`
6. `nevel-gimo-osterbybruk-och-osthammar-2026`
7. `tekniska-verken-linkoping-linkoping-2026`
8. `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`

Kalkylen ska skapa uppskattad årskostnad från tolv MWh-värden och tolv
kalendermånaders flöden. Sju produkter kräver dessutom leverantörens
debiterbara effekt och bekräftat band. Mälarenergi 2–4 lägenheter saknar
kapacitetsdel och får inte kräva eller visa effekt/band.

Resultatstatus ska vara `annual/snapshot/complete`, aldrig `exact`.

Detta är endast implementation bakom spärr. **Rensa inte `investigation`,
aktivera inte, pusha inte och lägg inte kandidatprodukterna i skarp
payload.** Commitera fokuserat lokalt, dokumentera hash/tester och stanna
för Codex granskning.

## 1. Aktuell källproveniens

Lägg eller uppdatera officiella källposter med `retrieved_on=2026-09-15`.
Bevara historiska källor som historik men bind 2026-fakta till aktuella
leverantörskällor:

- Luleå:
  `https://www.luleaenergi.se/produktion-och-infrastruktur/fjarrvarme/priser-och-avtalsvillkor/lulea-foretag-2026/`
- Öresundskraft Helsingborg/Ängelholm, företag Normalpris:
  `https://www.oresundskraft.se/globalassets/pdf/prisdialog/prisandringsmodell/prisandringsmodell-2026-2028.pdf`
- Piteå centrala:
  `https://www.piteenergi.se/fjarrvarme/priser-foretag/`
- Piteå Norrfjärden/Sjulnäs:
  `https://www.piteenergi.se/fjarrvarme/priser-2-foretag/`
- Nevel landningssida och 2026-prislista:
  `https://nevel.com/sv/fjarrvarme/gimo/`
  `https://nevel.com/wp-content/uploads/2025/10/Nevel_prislista_foretag_Osthammar_Gimo_Osterbybruk_2026.pdf`
- Tekniska verken företag:
  `https://tekniskaverken.se/foretag/fjarrvarme/priser`
- Mälarenergi 2–4 lägenheter:
  `https://www.malarenergi.se/fjarrvarme/pris-for-fjarrvarme/`

Källavgränsningar som ska synas i katalog/policyhjälp:

- Luleås flödespris gäller primäranslutning;
- Nevels standardprislista gäller full värmeleverans; delvärme har särskilda
  villkor och ingår inte;
- Linköpings normalpris 5,35 kr/m³ ska inte blandas ihop med den separata
  lågtemperaturvarianten 2,67 kr/m³;
- använd endast Öresundskrafts företags-/Normalprisvillkor, inte en
  konsumentprodukts avkylningsregel.

Rätta källsanna `billing_basis_method` där den aktuella sidan ger stöd, men
beräkna inte metoden lokalt i denna batch. Bind leverantörens fakturavärde:

- Luleå: aktuell dygnsmedeleffekt enligt leverantörens beskrivning;
- Piteå: dygnsmedeleffekter oktober–mars bestämmer nästa kalenderår;
- Linköping: leverantörens effektsignatur baserad på två års
  normalårskorrigerad energi och dimensionerande temperatur, med underlag
  november–mars;
- Nevel: leverantörens publicerade årsmetod/revisionsregel.

Finns exakt sammanvägning inte styrkt ska texten säga det och hänvisa till
leverantörens värde. Uppfinn inte automatisk effektberäkning.

## 2. Rätta Mälarenergis request-scope

`R03` blockerar i dag hela medlemmen `malarenergi`. Gör den tariffscopad:

```json
"tariff_ids": [
  "malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026",
  "malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026"
]
```

Ta bort `member_ids:["malarenergi"]` och ta bort `R03` från
2–4-lägenheters `investigation.request_ids`. Ändra inte R03:s fråga eller
`status="utreds"`; de två angivna tarifferna ska fortfarande blockeras.
Dokumentera att detta är korrigerad omfattning, inte ett externt svar.

## 3. Katalog och policyer bakom spärr

Sätt `contract_required:true` på exakt de åtta kandidaterna men bevara
`production_ready:false` och deras `investigation.status="utreds"`.

Varje policy ska ha `tackning={"annual_forward"}`,
`stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False` och exakt ett
obligatoriskt flödeskrav med:

- `nyckel="flode_m3"`;
- `vardetyp="number_series"` och `antal_varden=12`;
- `kravs_for=("annual",)`;
- `tillatna_kallor=("supplier_value",)`;
- `minvarde=0`, ändligt rimligt maxvärde;
- `matupplosning="manadsvis"`, `rullande=False` och
  `takad_till_snapshot=True`: serien är ett observerat faktura-/
  kalenderunderlag som används framåtriktat, inte ett löpande eller exakt
  framtidsvärde;
- etikett/hjälptext på svenska och engelska som säger att rutorna är
  januari–december och att endast tariffens namngivna flödesmånader
  debiteras.

Sju policyer ska dessutom ha tariffspecifikt numeriskt effektfält bundet
med `kapacitet_bindning` och tariffspecifikt `band_id` bundet med
`kapacitet_band_bindning`. Varje tariff använder
`supplier_confirmed_band_id_required`; beräkna aldrig bandet automatiskt.

Mälarenergis policy ska ha `kapacitet_bindning=None` och
`kapacitet_band_bindning=None`. Dess fasta årsavgift 7 884 kr exkl. moms,
energi 788/624/236 kr/MWh och flöde 1,60 kr/m³ är de exkl.-momsbelopp som
ska räknas. Ingen dold nolleffekt får användas för att simulera en
kapacitetsdel.

## 4. Implementera säsongssemantik generellt och fail-closed

Utöka `volume`-justeringen symmetriskt i Python och TypeScript:

1. Validera postens egen payload som en sluten struktur med exakt
   `type/rate/unit/months`; `unit="SEK/m3"`, ändlig positiv sats samt en
   icke-tom lista av unika heltal 1–12. Extra/saknad nyckel, bool som tal,
   dubblett eller månad utanför intervallet blockerar.
2. Utöka `kontrollera_volymbindning` så en kontraktsstyrd tariff har exakt
   en `volume`-post och exakt ett matchande policyfält.
3. När postens månader är exakt `{1..12}` ska det befintliga skalära
   kontraktet bestå: `vardetyp="number"`, annual, endast
   `supplier_value`, `minvarde=0`.
4. När postens månader är en riktig delmängd av `{1..12}` ska policyn i
   stället kräva `vardetyp="number_series"`, `antal_varden=12`, annual,
   endast `supplier_value`, `minvarde=0`, `rullande=False` och
   `takad_till_snapshot=True`.
5. Årsfasaden transporterar serien via befintliga `falt_serier`. Motorn
   summerar `falt_serier["flode_m3"][m]` för exakt postens egna månader
   och multiplicerar med `rate`. Ingen annan månad får bidra.
6. Saknad/feltypad serie ska kasta även vid direkt motoranrop. En
   säsongspost får aldrig falla tillbaka på `MWh/(1,163×45)`.

Ändra inte Mölndals icke-kontraktsstyrda helårsreserv. Ändra inte Batch
5b:s eller VänerEnergis policyer från skalär till serie. Dessa regressioner
är en del av acceptansgrinden.

## 5. UI och produktbyte

Återanvänd den befintliga generiska renderingen av 12-elements
`number_series`, som redan visar Jan–Dec. Lägg ingen tariffspecifik
hardkodning i `KalkylatorPage.tsx`.

Hjälptexten ska namnge varje produkts debiterade period. Resultattexten ska
göra klart att årskostnaden är uppskattad och att effekt-/bandvärden kommer
från leverantör/faktura. Okänd månadsperiodisering av årsavgifter får inte
visas som fakturaexakt månadskostnad.

Produktbyte ska rensa tariffspecifik effekt, band och flödesserie. Växling
mellan en 9-, 5-, 6- eller 7-månadersprodukt får inte återanvända gamla
värden tyst. Växling till/från Mälarenergi ska dessutom ta bort/lägga till
effekt- och bandfälten korrekt.

Kronor, schablon och besparing ska fortsätta blockeras för samtliga åtta.

## 6. Oberoende och speglade tester

Lägg permanenta Python-/TypeScript-prov genom verklig katalog, policy,
kontraktsfasad och motor. Fixturer mellan språk ska härledas från samma
genererade källa där det är möjligt; golden-förväntningar ska vara
oberoende handräknade statiska tal.

Minimikrav:

- ett golden-facit per tariff som inkluderar tolv månaders energi,
  kapacitetsbandets `fixed + variable × effekt` för de sju relevanta,
  Mälarenergis fasta årsavgift, säsongsflöde och moms;
- Nevels publicerade referensfall: 120 kW/band 2, 520 MWh med källans
  82,2-procentsandel, alltså oavrundat 427,44 vinter + 92,56 sommar, och
  8 320 m³ okt–apr = 613 622,50 kr exkl. moms efter avrundning. Källans
  visade deltal 427,4 + 92,6 ger bokstavligt 613 608,76 kr; testet måste
  dokumentera och välja rätt precision, inte blanda totalen med de
  presentationsavrundade delarna;
- exakt postlista per tariff och separata prov för 5, 6, 7 och 9 månader;
- `+100 m³` i inkluderad månad ändrar exkl.-momsfacit med
  `100 × tariffens rate`; samma ändring i exkluderad månad ändrar exakt
  0;
- samtliga band-ID:n för var och en av de sju kapacitetstarifferna, plus
  saknat/tomt/okänt band och saknad/ogiltig effekt;
- seriefelet saknad, skalär, 11/13 värden, tomt element, sträng, negativt,
  NaN/oändlighet och över max;
- preflightmutationer för saknad/dubblerad/malformed `volume`-post,
  fel `months`, fel policyvärdetyp/källa/omfattning/min/kardinalitet;
- Mälarenergi renderas och räknas utan kapacitetsfält;
- R03 blockerar fortsatt exakt de två tariff-ID:na och inte 2–4
  lägenheter i den isolerade kandidatuppsättningen;
- Batch 5b/VänerEnergi behåller skalärt helårsflöde; Mölndal behåller sin
  legacyreserv; Batch 3, 4, 5a, 5b och Lidköping förblir gröna;
- renderad React-testväg från isolerat genererad policy, inte en
  handskriven policydublett;
- minst två isolerade omockade E2E-flöden: Luleå med effekt/band/serie och
  Mälarenergi utan kapacitet;
- isolerad E2E-harness ska skapa egen temporär arbetskopia, välja unik port,
  verifiera att den egna serverprocessen lever och städa utan att röra
  arbetskopians `dist/` eller genererade skarpa filer.

Golden-facit får inte genereras av `calcResult`, `beraknaArsprodukt`,
`arskostnad` eller en kopia av produktionsalgoritmen.

## 7. Räkningsgrind och leverans

Under implementationen ska följande bestå:

- disposition `51/13/28 av 92`;
- 51 godkända katalograder;
- 53 skarpa produkter;
- inga Batch 5c-ID:n i skarp genererad payload.

En isolerad katalogkopia där exakt kandidaternas `investigation` rensas
ska ge:

- disposition `59/5/28 av 92`;
- 59 godkända katalograder;
- 61 produkter inklusive två leverantörsfilsprodukter;
- exakt åtta nya produkt-ID:n, inga borttagna, och av de 53 äldre
  produkterna: 52 helt oförändrade och en (Öresundskraft Helsingborg
  Totalvärme, central installerad före 2024) med enbart ett avsiktligt
  disambiguerat visningsnamn — ID, prisdata och policy oförändrade
  (rättat 2026-09-16 efter granskning 2026-09-16-009 P2.2; se
  sessionsloggen för den daterade rättelsen).

Kör minst full Python-svit, full TypeScript-svit, `tsc --noEmit`, isolerat
bygge, ordinarie E2E samt den nya isolerade kandidat-E2E:n. Kör
`git diff --check` i alla tre repon.

Commitera bara avsedda filer i respektive repo. Rör inte orelaterad
arbetskopiedata eller `neptune-marketing/dist/`. Sessionsloggen ska ange
exakta commit-hashar, testantal, disposition, produktantal och bekräfta:

> Batch 5c är implementerad bakom spärr. Ingen tariff är aktiverad och
> inget är pushat. Väntar på Codex kodgranskning.

Stanna sedan. Aktivering och push är separata framtida beslut.
