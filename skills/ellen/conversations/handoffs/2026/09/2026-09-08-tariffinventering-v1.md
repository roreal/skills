---
handoff_id: "2026-09-08-001"
created_at: "2026-09-08T09:31:03+02:00"
from: "Codex"
to: "Claude"
status: delivered
delivered_at: "2026-09-08T10:15:00+02:00"
scope: "Fullständig v1-inventering och batchplan för samtliga möjliga fjärrvärmetariffer"
implementation_allowed: false
deliverables:
  - "Fjarrvarmetariffer/tariffinventering-v1.md"
  - "Fjarrvarmetariffer/batchplan-v1.md"
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

## Leverans 2026-09-08T10:15:00+02:00

Klaudes leverans: [`tariffinventering-v1.md`](../../../Fjarrvarmetariffer/tariffinventering-v1.md)
och [`batchplan-v1.md`](../../../Fjarrvarmetariffer/batchplan-v1.md). Räkningskontroll: 80
enheter (78 katalograder + 2 leverantörsfiler) = 8 implementerade + 43 redo att implementera
+ 27 externt blockerade + 2 ej tillämpliga. Sju föreslagna batcher för de 43. Fyra öppna
frågor lämnade i inventeringens §8. Se sessionsloggens Claude-inlägg för fullständig
sammanfattning. Ingen kod, tariffdata eller aktivering ändrad; väntar på Codex granskning.

