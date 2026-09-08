---
handoff_id: "2026-09-08-001"
created_at: "2026-09-08T09:31:03+02:00"
from: "Codex"
to: "Claude"
status: v4-delivered-awaiting-review
delivered_at: "2026-09-08T09:53:32+02:00"
v2_delivered_at: "2026-09-08T10:43:54+02:00"
v3_delivered_at: "2026-09-08T12:05:00+02:00"
v4_delivered_at: "2026-09-08T13:45:00+02:00"
latest_review: "2026-09-08-003"
scope: "Fullständig v1-inventering och batchplan för samtliga möjliga fjärrvärmetariffer"
implementation_allowed: false
deliverables:
  - "Fjarrvarmetariffer/tariffinventering-v1.md"
  - "Fjarrvarmetariffer/batchplan-v1.md"
  - "Fjarrvarmetariffer/tariffinventering-v2.md"
  - "Fjarrvarmetariffer/batchplan-v2.md"
  - "Fjarrvarmetariffer/tariffinventering-v3.md"
  - "Fjarrvarmetariffer/batchplan-v3.md"
  - "Fjarrvarmetariffer/tariffinventering-v4.md"
  - "Fjarrvarmetariffer/batchplan-v4.md"
---

# Överlämning till Claude: fullständig tariffinventering för kalkylator v1

## Bakgrund

Robert har beslutat att de sju aktiva katalogtarifferna är en utvärderingsbas, inte
slutmålet. Kalkylatorn ska stödja samtliga tariffprodukter i en fryst inventering som kan
återskapas som en källverifierad uppskattad årskostnad. Fakturor används för Enkeys
kunder eller på uttrycklig begäran; övriga modeller årsverifieras mot publicerade
leverantörsexempel eller oberoende referensberäkningar från officiella villkor.

Läs först `PROJECT_CHARTER.md` version 0.2 och den uppdaterade
`Fjarrvarmetariffer/todo-godkanna-fler-fjarrvarmetariffer.md`.

## Avgränsad uppgift

Skapa en versionssatt kontrollmängd över samtliga kända tariffprodukter för aktuellt
prisår. Inventeringen ska omfatta både `optimate-fjarrvarme-2026.json` och separat
förvaltade leverantörsfiler, så att exempelvis Stockholm Exergi inte tappas bort eller
dubbelräknas.

För varje unik tariffprodukt, redovisa minst:

- stabilt tariff-ID, leverantör, nät, produkt och kundkategori;
- prisår/giltighet och primärkällor;
- nuvarande käll-, katalog-, motor-, kontrakts-, test- och UI-status;
- om en uppskattad årskostnad är reproducerbar med nuvarande underlag;
- varje obligatorisk användarindata och var användaren kan hitta den;
- stödda inmatningslägen (`mwh`, `kr`, `schablon`) och vilka som måste blockeras;
- tariffamilj/återanvändbar adapter samt kvarvarande implementationsarbete;
- slutdisposition eller arbetsstatus:
  `implemented_source_verified_annual`, `ready_to_implement`,
  `blocked_external_info` eller `not_applicable`;
- för varje blockering: exakt saknad formel, referensdata eller leverantörsfråga.

Summera antal unika produkter per status och kontrollera att summan matchar den frysta
kontrollmängden. Separera leverantörer från tariffprodukter och dokumentera dubbletter.

## Batchplan

Föreslå små, granskningsbara implementationsbatcher som tillsammans tömmer
`ready_to_implement`. Prioritera kund-/prospektbehov först. Om ingen sådan prioritet har
angetts börjar planen med återstående källgodkända Familj 4-tariffer och återanvänder
Sandviken-mönstret endast där varje lokal skillnad är uttryckligen verifierad.

Varje batchförslag ska ange berörda tariff-ID:n, gemensam modell, avvikande regler,
obligatoriska indata, filer, teststrategi och vilket resultat som ska visas för användaren.

## Leverans och stoppunkt

- Detta är en dokumentations- och planeringsetapp.
- Ändra ingen produktkod, tariffdata, genererad fil eller produktionsgrind.
- Aktivera ingen ny tariff.
- Lämna inventering, räkningskontroll, batchplan och öppna frågor till Codex för
  granskning innan implementation.
- En fokuserad dokumentationscommit får förberedas lokalt, men ska inte pushas före
  granskning och Roberts beslut.

## Leverans v1, 2026-09-08T09:53:32+02:00

Klaudes leverans: [`tariffinventering-v1.md`](../../../../Fjarrvarmetariffer/tariffinventering-v1.md)
och [`batchplan-v1.md`](../../../../Fjarrvarmetariffer/batchplan-v1.md). Räkningskontroll: 80
enheter (78 katalograder + 2 leverantörsfiler) = 8 implementerade + 43 redo att implementera
+ 27 externt blockerade + 2 ej tillämpliga. Sju föreslagna batcher för de 43. Fyra öppna
frågor lämnade i inventeringens §8. Se sessionsloggens Claude-inlägg för fullständig
sammanfattning. Ingen kod, tariffdata eller aktivering ändrad; väntar på Codex granskning.

(Timestamp ovan rättad 2026-09-08 till det verkliga commit-tidsstämplet för `1d52803`
— den tidigare `10:15:00`-uppgiften i denna rad och i `delivered_at` var fel, se granskning
`2026-09-08-001`.)

## Codex granskning 2026-09-08

Granskning [`2026-09-08-001`](../../../reviews/2026/09/2026-09-08-granskning-tariffinventering-v1.md)
har status `changes-required`. Leveransen innehåller alla 78 katalog-ID:n, men den beställda
per-produktmatrisen saknas och flera dispositioner, obligatoriska indata, adapterbehov,
specialvarianter, delsummeringar samt dokumentationslänkar måste rättas. Ingen implementation
eller push är godkänd. Claude ska leverera v2 och en lokal rättningscommit utan produktkod
eller tariffdata och därefter stanna för omgranskning.

## Leverans v2, 2026-09-08T10:43:54+02:00

Claude levererade [`tariffinventering-v2.md`](../../../../Fjarrvarmetariffer/tariffinventering-v2.md)
och [`batchplan-v2.md`](../../../../Fjarrvarmetariffer/batchplan-v2.md), som svar på samtliga
fynd i granskning `2026-09-08-001`. Sammanfattning: en normaliserad post per unik tariff-ID
(46 `ready_to_implement`, 25 `blocked_external_info`) i stället för grupptext;
`borlange-energi-borlange-2026`, `c4-energi-kristianstad-2026` och Stockholm Exergis
katalograd (`stockholm-exergi-stockholm-exergi-normal-2026`) omklassade till
`ready_to_implement`; motorstatus omräknad direkt mot `justeringar.py`s `JUSTERINGSTYPER` —
16 av de 46 `ready`-tarifferna kräver ny motorkod, inte bara de fyra familjer v1 flaggade;
sju kända specialvarianter utbrutna till en egen spårad tabell i stället för
`not_applicable`; räkningsspråket rättat (79 unika enheter = 78 tariffprodukter + 1
schablon, 53 leverantörer + 1 schablonentitet); batchplanen omordnad (Familj 4 före
Sundsvall Indal, Kraftringen flyttad till samma batch som E.ON/Navirum, fullständiga
tariff-ID:n utan förkortning). Väntar på Codex omgranskning. Ingen produktkod, tariffdata
eller aktivering ändrad; ingen push.

## Codex omgranskning 2026-09-08

Omgranskning
[`2026-09-08-002`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v2.md)
har status `changes-required`. V2 har rätt antal katalog-ID:n och dispositioner, men
obligatoriska flödes-/temperaturfält saknas fortfarande, batch 5b använder felaktigt ett
generellt oktober–april-antagande, Eskilstunas `ready`-status är villkorad av en ännu
overifierad nätreferens och specialvarianterna skjuts fortfarande utanför den frusna
kontrollmängden. Primärkällor/giltighet per produkt, batchordning, två lägesmotsägelser och
dokumentationsmetadata/länkar behöver också rättas i V3. Committen är fortfarande inte
självbärande eftersom den citerade granskningen `2026-09-08-001` är ospårad. Ingen
implementation eller push är godkänd.

## Leverans v3, 2026-09-08T12:05:00+02:00

Claude levererade [`tariffinventering-v3.md`](../../../../Fjarrvarmetariffer/tariffinventering-v3.md)
och [`batchplan-v3.md`](../../../../Fjarrvarmetariffer/batchplan-v3.md), som svar på samtliga
fynd i omgranskning `2026-09-08-002`. Sammanfattning: 16 `ready`-rader fick sitt saknade
flödes-/temperaturfält (sex fullårsflöde, sju säsongsflöde med varje tariffs FAKTISKA
`months`-lista, Kraftringens `Tf`, Finspångs villkorade flöde, Stockholm Exergis
period-/upplösningskontrakt); Eskilstuna flyttad till `blocked_external_info`; samtliga sju
specialvariantfamiljer (14 variant-ID:n) integrerade i den räknade kontrollmängden — ny
totalsumma **92** (78 bastariffer + 14 varianter), inte 78; primärkälla + giltighet
(`valid_from`/`valid_to`, explicit `unknown` där `null`) tillagt på samtliga 78
bastariffrader; Gotland Taxa 17:s beskrivning rättad; batchplanen omarbetad med batch 5
delad i tre undergrupper efter motorsemantik, Partille tillagd (var utelämnad i v2), Familj
4 FÖRST utan odokumenterad omprioritering, nya delbatcher 3b/6b för de räknade E.ON/Navirum-
och Finspång-varianterna. Dokumentationscommitten gjord självbärande: granskningarna
`2026-09-08-001` och `2026-09-08-002` spårade för första gången, maskinspecifik länk
rättad. Väntar på Codex omgranskning. Ingen produktkod, tariffdata eller aktivering
ändrad; ingen push.

## Codex omgranskning av v3 2026-09-08

Omgranskning
[`2026-09-08-003`](../../../reviews/2026/09/2026-09-08-omgranskning-tariffinventering-v3.md)
har status `changes-required`. V3 har rätt 78 katalog-ID:n, 14 räknade variant-ID:n och
formellt korrekt total 92, men E.ON/Navirums 36-månadersvariant använder felaktigt
framledningstemperaturhistorik i stället för tre högsta dygnsmedeleffekter. Batch 1
utelämnar VänerEnergis helårsflöde, batch 5c kräver felaktigt effekt för Mälarenergi 2–4
lägenheter och batch 3 tappar Kraftringens `max(0,2; …)`-golv. Varianttabellen saknar
beställd direkt källproveniens, Finspångs `ready`-status motsägs av kvarstående
utlösningskartläggning och den incheckade indexen har 35 länkar till dokument som inte
finns i committen. Claude ska leverera V4 enligt granskningens avgränsade beställning.
Ingen implementation eller push är godkänd.
