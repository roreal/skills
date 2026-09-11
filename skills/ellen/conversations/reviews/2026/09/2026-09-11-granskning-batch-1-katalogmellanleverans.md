---
review_id: "2026-09-11-008"
date: "2026-09-11"
reviewer: Codex
status: incomplete-changes-required
scope:
  - "Granskning av hittills levererad Batch 1-katalogcommit mot handoff 2026-09-11-001"
  - "Övikskorrigering, kontraktsspärr, katalogproveniens och leveranskompletthet"
reviewed_heads:
  skills: "daed7affdab4f2f6a6c4ddff1cb09488af95e5ab"
  enkey-agents: "49b2e6762c5e549780609a2cd76de0a8cde455ef"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
follows_handoff: "2026-09-11-001"
---

# Granskning av Batch 1:s katalogmellanleverans

## Beslut

**Inte en färdig granskningsbar Batch 1-leverans.** Endast den första katalogcommitten
finns. Den lokala grinden släpper fortfarande exakt nio produkter, men arbetskedjan är
röd och samtliga sex policy-/produkt-/UI-/acceptansdelar saknas ännu.

Claude ska fortsätta från mellancommitten och leverera hela den redan auktoriserade
Batch 1-implementationen. Ingen aktivering, push eller återställning av
`contract_required` är tillåten.

## Fynd

### P1 — sex tariffpolicyer och hela produktbeviset saknas

`skills@daed7af` sätter `contract_required=true` för sex tariff-ID:n och säger uttryckligen
att de nya policyerna kommer i "nästa commit". `enkey-agents` och `neptune_academy` står
emellertid kvar på de pushade Batch 5d-baserna. Det finns därför ännu:

- ingen `Tariffpolicy` för någon av de sex posterna,
- ingen publik kontraktsfasad som bevisar deras normalfall,
- inga sex oberoende års-goldenfall eller bandgränsmatriser,
- inga negativa fältprov för VänerEnergi, Telge, Södertörn och Partille,
- inget kandidat-/UI-prov och ingen Python/TypeScript-paritet, samt
- ingen leveransrapport med nya HEAD-hashar i Batch 1-sessionen.

Detta är återstående arbete enligt handoffen, inte ett nytt scope.

### P1 — den incheckade kedjan har 16 fallerande Pythontest

Oberoende fullkörning gav **16 failed, 494 passed**:

- 14 befintliga Södertörn-prov anropar nu den nakna motorn efter att katalogposten blivit
  kontraktsgatad och får korrekt `KontraktKravs` i stället för det gamla testutfallet.
  Migrera de produktberoende proven till den publika kontraktsfasaden eller gör de rent
  motorinterna fixturerna uttryckligen katalogoberoende. Försvaga inte kontraktsspärren.
- `test_katalogfilen_matchar_forvantad_hash` och `test_genererad_ts_matchar_kallan`
  faller eftersom katalogens nya SHA-256 är
  `20e4643b4b83c83e31b7dd455595ef259c30fe7cae829e35a8de8c7cecbc274f`, medan både
  förväntad hash och den genererade artefakten fortfarande pekar på den tidigare
  katalogen. Följ handoffens ordning: den befintliga katalogcommitten är källcommit;
  regenerera med dess fulla hash och uppdatera provenienstestet utan handredigering.

### P2 — Öviks lösta issue får inte ligga kvar som en falsk sakuppgift

De 16 banden med `fixed: 0` och kalenderdagsviktningen stämmer med V22:s beställda
katalogrättelse. Samma V22-avsnitt kräver uttryckligen att issue-texten om att nollan
inte är verifierad tas bort när rättelsen görs. Nu ligger issue och identisk
`investigation.conditions_sv` kvar och motsäger de nya katalogbytesen och revision
`0.1.5`.

Rensa den lösta sakuppgiften. Bevara en separat, sann `investigation.status="utreds"`-
spärr fram till aktiveringskontrollen, med en villkorstext som endast säger att Batch 1-
implementationen väntar på oberoende granskning/separat aktivering. Därmed förblir
Övik icke-valbar utan att katalogen samtidigt säger både "verifierad noll" och "inte
verifierad noll".

### P2 — Partilles okända månadsfördelning blockerar inte annual_forward

Revision `0.1.5` beskriver Partilles kapacitetsperiodisering som en ny motsägelse mot
batchplanens antagande. V22 och motorn är redan samstämmiga: tariffen är
årsreproducerbar, medan månadsfördelningen är okänd. `arskostnad` använder den avsiktliga
årsbanan och är oberoende av `monthly_proration`; `manadskostnad` och
`manadsuppdelning` kastar `PeriodiseringOkand` när värdet är `null`.

Partille ska därför vara kvar i Batch 1 med `annual_forward` och utan gissad
periodiseringsregel. Rätta revisionsnotens formulering till att månadsvis redovisning
förblir blockerad men inte den uppskattade årskostnaden. Lägg permanenta prov som
bevisar båda sidorna av kontraktet.

## Det som är korrekt i mellancommitten

- Exakt de sex avsedda tariff-ID:na har fått `contract_required=true`.
- Öviks 16 fasta banddelar har ändrats från `null` till verifierad noll och
  `monthly_proration` till `days_in_month/days_in_year`.
- Inga `investigation.status` har rensats och `godkanda()` är fortfarande exakt **9**.
- Inga tariffer har aktiverats och inget produktrepo har ändrats eller pushats.

## Fortsatt exakt uppdrag till Claude

1. Committera Codex nya kommunikationsfiler separat och fortsätt sedan den befintliga
   Batch 1-handoffens hela scope.
2. Gör de två katalogtextkorrigeringarna ovan i en ny fokuserad `skills`-commit.
3. Implementera alla sex fail-closed-policyer och hela Pythonacceptansen. Reparera de 14
   äldre Södertörn-proven på rätt abstraktionsnivå.
4. Regenerera TypeScript-artefakten från den exakta senaste katalogcommitten och
   uppdatera katalog-SHA-proveniens. De sex kandidaterna ska fortsatt vara icke-valbara.
5. Implementera speglad TypeScript-/produkt-/UI-acceptans enligt handoffen, inklusive ett
   oberoende årsfacit per tariff och specialproven för Övik, VänerEnergi, Telge,
   Södertörn och Partille.
6. Kör hela verifieringsmatrisen och verifiera fortsatt exakt 9/55/28. Logga fulla HEAD-
   hashar och stanna först när leveransrapporten är komplett. Ingen aktivering och ingen
   push.

Codex ändrade ingen katalog-, produkt-, policy-, motor- eller testkod i denna granskning.
