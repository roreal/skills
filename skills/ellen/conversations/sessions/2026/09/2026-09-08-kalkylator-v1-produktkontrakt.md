---
session_id: "2026-09-08-001"
started_at: "2026-09-08T09:21:35+02:00"
last_updated: "2026-09-08T09:36:59+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: coverage-decided
topics:
  - kalkylator-v1
  - produktdirektiv
  - verifieringsnivaer
  - leverantorstackning
  - tariffprioritering
source: visible-conversation
transcript_fidelity: summarized
---

# Session: produktkontrakt för kalkylator v1

## Sammanfattning

Efter att Claudes Sandviken-push hade verifierats bad Robert Codex fortsätta. Codex
genomförde den avgränsade dokumentationsetapp som tidigare rekommenderats: ett första
produktdirektiv för kalkylator v1 skapades, den inaktuella tariff-to-do-listan synkades
med Roberts beslut om års- och fakturaverifiering och två tekniska underlag fick
förtydliganden om verifieringsmetod och ordet `exact`.

Ingen kalkylatorkod, tariffdata, adapter, genererad fil eller tariffaktivering ändrades.

## Levererade dokument

- `PROJECT_CHARTER.md` — målprioritering, kalkylatorns v1-scope, verifieringsnivåer,
  redovisningsspråk, leverantörsprioritering, Definition of Done och icke-mål.
- `Fjarrvarmetariffer/todo-godkanna-fler-fjarrvarmetariffer.md` — äldre krav på generell
  månadsmodell och faktura per prismodell ersatta med den beslutade årsmodellen;
  Sandviken och grundkartläggningen markerade klara.
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md` — not om att intern status
  `exact` inte betyder fakturaverifierad och inte ska användas som kundlöfte.
- `Fjarrvarmetariffer/optimate-agentfundament-bebo-fjarrvarme.md` — tariffadapter kan
  årsverifieras mot leverantörsexempel eller oberoende referensberäkning; fakturor används
  för Enkeys kunder eller när kontroll uttryckligen efterfrågas.

## Beslut som dokumenten återger

- Kalkylatorn är projektets primära produktmål; Ellens mätdata- och
  kostnadsoptimeringsförmåga är sekundär.
- Kalkylator v1 är i första hand en leverantörsspecifik årsberäkning.
- Modellstatus och resultatstatus hålls isär. En källverifierad tariff gör inte ett
  enskilt kundresultat fakturaverifierat.
- Kundgränssnittet skiljer `beräknat`, `uppskattat` och `fakturaverifierat`; det
  fristående ordet "exakt" används inte som kvalitetslöfte.
- MWh-, kronor- och schablonläge är separata tarifförmågor. Ett icke verifierat läge
  blockeras i stället för att gissas.
- Samtliga möjliga tariffprodukter i en fryst inventering ska implementeras. Varje
  återstående post ska vara explicit blockerad av extern information eller motiverat ej
  tillämplig; ingen oklassificerad rest tillåts.

## Öppet beslut för Robert

1. Ska en saknad leverantör ge ett separat val med tydligt märkt generell uppskattning och
   möjlighet att efterfråga bolaget? Codex rekommenderar ja; ett riksgenomsnitt får aldrig
   framstå som den namngivna leverantörens tariff.

## Nästa kontrollpunkt

Claude har fått överlämning `2026-09-08-001`: bygg först en fullständig, deduplicerad och
versionssatt tariffinventering över både katalogen och separat förvaltade leverantörsfiler.
Varje post ska klassas som implementerad, redo att implementera, externt blockerad eller
ej tillämplig, med obligatoriska indata och stödda inmatningslägen. Claude ska även lämna
en batchplan men inte ändra kod eller tariffdata före Codex granskning.

Beslutet om UI-beteendet för saknad leverantör kan fattas parallellt. Därefter kan
produktdirektivet få status `approved` och ett separat språk-/metadataförslag tas fram.

## Konversation

### Robert — användare

> Du kan fortsätta nu

### Codex — assistent

Codex fortsatte med dokumentationsetappen enligt den tidigare beslutade arbetsordningen.
Produktdirektivet och de synkade arbetsdokumenten levererades utan ändring av produktkod
eller tariffdata. Två produktbeslut återstår för Robert: v1:s minsta leverantörstäckning
och beteendet när användarens leverantör saknas.

### Robert — användare

> Jag ser de sju befintliga tarifferna som en utvärdering, jag vill att vi tar oss igenom samtliga som är möjliga. Om energibolagen kan fakturera på dessas uppgifter så ska vi kunna bygga en kalkyl som skapar motsvarande uppskattade årskostnad.

### Codex — assistent

Codex uppdaterade produktdirektivet till version 0.2. De sju aktiva tarifferna är nu
uttryckligen en utvärderingsbas, inte v1:s slutliga omfattning. Täckningsmålet är samtliga
tariffer i en fryst tariffinventering som kan återskapas som källverifierad uppskattad
årskostnad. Inventeringen omfattar både JSON-katalogen och separat förvaltade
leverantörsfiler, så exempelvis Stockholm Exergi inte faller utanför kontrollmängden.

"Möjlig" definieras tekniskt: alla nödvändiga prisdelar, formler och villkor ska vara
kända, och dynamiska värden ska kunna anges synligt, hämtas från verifierad källa eller
beräknas från uttryckligt underlag. En leverantörs internt dolda formel eller nätreferens
ersätts inte med en gissning; tariffen får då `blocked_external_info` och en konkret fråga
tills besked finns. Varje tariff ska till slut vara implementerad, externt blockerad eller
motiverat ej tillämplig — ingen oklassificerad restlista.

### Claude — assistent

Claude genomförde överlämning `2026-09-08-001`: en fullständig, deduplicerad
tariffinventering och batchplan, ingen kod eller tariffdata ändrad.

[`tariffinventering-v1.md`](../../../Fjarrvarmetariffer/tariffinventering-v1.md) täcker
samtliga 78 katalograder plus de två separat förvaltade leverantörsfilerna (Stockholm
Exergi, Riksgenomsnittet) — 80 enheter, deduplicerat till 79 unika produkter. Byggd på
den redan granskade [verifieringslistan](../../../Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md)
och [teknisk-kartläggning v4](../../../Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md)
i stället för att omgranska källorna på nytt, plus en direkt läsning av
`katalog.py`/`policyregister.py`/`tariffer.generated.ts` för faktisk motor-/kontrakts-/
UI-status. Disposition: 8 `implemented_source_verified_annual` (de sju katalogtarifferna +
Stockholm Exergi), 43 `ready_to_implement`, 27 `blocked_external_info` (varje rad med den
exakta leverantörsfrågan), 2 `not_applicable` (Riksgenomsnittet, Stockholm Exergis
katalogduplikat). Summan stämmer mot kontrollmängden (78 katalog + 2 leverantörsfiler = 80).
`optimate-fjarrvarme-2027.json` (en annan sessions redan pushade commit `62181a1`, prisår
2027, bara 2 av 53 medlemmar ifyllda) är uttryckligen utanför denna frusna 2026-version.

[`batchplan-v1.md`](../../../Fjarrvarmetariffer/batchplan-v1.md) föreslår sju batcher (43
tariffer) i stigande risk-/motorarbetesordning: (1) Sundsvall Indal/Liden/Lucksta —
ren energitariff, ren aktivering; (2) Familj 4-resten + Telge, Sandviken-mönstret rakt av;
(3) E.ON/Navirum, delad ny flödesformel; (4a–4c) 26 fristående leverantörsvärde-tariffer i
tre delbatcher efter hur mycket särvillkor de bär; (5) Borås + Finspång, två nya
kapacitetsformer i motorn; (6) Vattenfalls tolv tariffer, kontingent på ett öppet beslut om
3.3 (asymmetrisk flödesjustering). De 27 blockerade tarifferna batchas inte — de väntar på
leverantörssvar via den befintliga processen i tariff-to-do:ns §7.

Fyra öppna frågor lämnade till Codex i inventeringens §8: Vattenfalls delnings-/väntebeslut,
en motsägelse mellan verifieringslistan och teknisk-kartläggningen om Sundsvall Matfors
(löst genom att följa den senare, mer detaljerade, redan granskade källan som auktoritativ),
om "leverantörsvärde-mönstret" som generell policy för ~26 produkter behöver granskas
tariff för tariff, och om de föreslagna `not_applicable`-undantagen inom vissa batcher
(kundvald effekt hos Södertörn, lågtemperaturvärme hos Tekniska Verken Linköping,
Brunnshög hos Kraftringen, spetsvärme hos Finspång) är rätt avvägning.

Ingen produktkod, tariffdata, genererad fil eller produktionsgrind ändrad. Ingen ny tariff
aktiverad.

## Ändringslogg

- `2026-09-08T10:15:00+02:00` – Claude levererade tariffinventering v1.0 och batchplan v1.0 enligt överlämning `2026-09-08-001`: 80 enheter klassade (8 implementerade, 43 redo, 27 externt blockerade, 2 ej tillämpliga), sju föreslagna implementationsbatcher, fyra öppna frågor till Codex. Ingen kod, tariffdata eller aktivering ändrad.
- `2026-09-08T09:36:59+02:00` – Codex skapade överlämning `2026-09-08-001` till Claude för en fullständig, deduplicerad v1-inventering och batchplan. Kontrollmängden ska omfatta både JSON-katalogen och separat förvaltade leverantörsfiler; ingen kod, tariffdata eller aktivering får ändras före Codex granskning.
- `2026-09-08T09:31:03+02:00` – Robert beslutade att de sju aktiva tarifferna endast är en utvärdering och att alla möjliga tariffer ska implementeras. Produktdirektiv v0.2 och tariff-to-do uppdaterades med ett versionssatt slutkriterium och dispositionerna `implemented_source_verified_annual`, `blocked_external_info` och `not_applicable`. Ingen implementation eller tariffdata ändrad.
- `2026-09-08T09:21:35+02:00` – Produktdirektiv v0.1 skapat och tariffens to-do,
  tekniska kartläggning samt agentfundament synkade med Roberts beslut. Ingen
  implementation eller tariffaktivering ändrad.
