---
session_id: "2026-09-21-001"
started_at: "2026-09-21T09:45:33+02:00"
last_updated: "2026-09-21T09:47:44+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: completed
topics:
  - Stockholm Exergi
  - kalkylator
  - månadsförbrukning
source: visible-conversation
transcript_fidelity: summarized
---

# Session: Stockholm Exergis månadsvärden i kalkylatorn

## Sammanfattning

Efter Roberts observation att 1 000 MWh årsenergi verkade bli 17,35 MWh i
de tolv rutorna kontrollerades Stockholm Exergis normalprislista 2026.
Prislistan har ett verkligt dygnsvis tillägg för överskjutande energi när
dygnsmedeltemperaturen understiger −3 °C, men ordet ”kallprisvolym” var
vår etikett och den volymen är inte total månadsförbrukning. Med endast
månadsdata kan tillägget inte fakturaberäknas exakt.

Stockholms formulär visar nu tolv redigerbara värden för **total köpt
fjärrvärme per månad**. De valideras mot årsenergin och används i
årskostnaden. Det dygnsberoende tillägget skattas internt, markeras
`estimated` och exponeras inte som ett kundfält. För 1 000 MWh/år ger
normalårsschablonen 156,389 MWh i januari och 1 000 MWh sammanlagt.
Metod och begränsningar finns i
`Fjarrvarmetariffer/stockholm-exergi-schablonunderlag-2026.md`.

## Leverans och verifiering

- `enkey-agents@716d2e8`: Stockholms krav accepterar `estimated` för
  årsproduktens schablonfält; 28 riktade Python-test passerade.
- `neptune_academy@a4eb519`: månadsvärden och intern tilläggsskattning,
  UI, tester och byggd sida; 2 262 TypeScript-test, ren `tsc`, isolerat
  bygge och alla E2E-scenarier passerade. Mobilvyn hade ingen horisontell
  overflow. Ett ändrat månadsbelopp ändrar den beräknade årskostnaden.
- `skills@e9d7353`: metodunderlaget och källan till prisvillkoret.
- Alla tre `origin/main` verifierades med `git ls-remote` efter normal
  fast-forward-push. Ingen force-push eller tariffaktivering gjordes.
- Lokala `enkey-agents/main@2e30bb2` med separat, opushad Milesight-commit
  lämnades orörd. Stockholm-ändringen lades isolerat på dåvarande
  `origin/main@3762066`; ingen merge eller rebase av Milesight-grenen.

## Öppna frågor

- Exakt fakturareproduktion av tillägget kräver kundens dygnsvärden och
  faktiska Effektgräns −3 °C. Månadsbeloppen ger en uppskattad årskostnad.

## Konversation

### Robert — användare

> Vad är kallpris volym? Är det något som används i prissättning av fjärrvärme? Om det är ett internt begrepp i kalylatorn skall det tas bort och ersättas av total värmeförbrukning för uppvärming per månad. Därefter committ och push så jag kan testa igen.

### Codex — assistent (sammanfattat, inte ordagrant)

Prisledet för överskjutande energi under kalla dygn är verkligt, men
”kallprisvolym” ska inte begäras som användarindata. Formuläret har ändrats
till total köpt fjärrvärme per månad. Beräkningen, testerna och normal
fast-forward-push är klara; den dygnsberoende delen är fortfarande en
uttryckligen osäker uppskattning.

## Ändringslogg

- `2026-09-21T09:47:44+02:00` – Session och pushkvitto skapade efter
  verifierade remoter.
