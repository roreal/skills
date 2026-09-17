---
handoff_id: "2026-09-17-001"
created_at: "2026-09-17T08:43:27+02:00"
from: Codex
to: Claude
status: ready-for-implementation
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "skills-only-source-and-blocker-normalization-for-28-dispositions"
tariff_activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
review_required_before_product_implementation: true
review_required_before_activation: true
review_required_before_push: true
required_parent_heads:
  skills: "2536c401b77f072d1f524dddb0807de194e4ea5f"
  enkey_agents: "13effb1d1901379826059939c2c80ba03114f474"
  neptune_academy: "0bdb6759bdbbb8785d0b716976b0483214282141"
tariff_disposition_before: "62 implemented / 2 ready / 28 blocked av 92"
tariff_disposition_after: "62 implemented / 2 ready / 28 blocked av 92"
relates_to:
  - "conversations/proposals/2026/09/2026-09-17-blockerade-tariffer-kallrevision.md"
  - "Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
  - "Fjarrvarmetariffer/batchplan-v22.md"
  - "Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md"
  - "Fjarrvarmetariffer/optimate-fjarrvarme-2026.json"
---

# Uppdrag till Claude: normalisera käll- och blockeringsläget för 28 dispositioner

## Mandat och stoppunkt

Robert har gett fria händer att lösa de blockerade energibolagen. Codex har därefter
genomfört en ny officiell källrevision och fastställt att 22 av 28 dispositioner kan
lösas internt, medan sex dispositioner fortfarande kräver fem externa svar.

Gör **endast en fokuserad skills-repo-leverans** som gör denna klassning maskinellt och
dokumentärt konsekvent. Ändra inte produktkod i `enkey-agents` eller
`neptune_academy`. Aktivera ingen tariff, pusha inte, skriv inte om historik och ändra
inte `conversations/automation/`. Avsluta med en unik committad
`REVIEW_READY: Codex`-post och stanna.

Batch 7:s opushade produktcommits och separat granskade historikförslag är uttryckligen
utanför scope. `neptune-marketing/dist/` och alla andra dokumenterade
arbetskopieundantag ska bevaras byte-för-byte.

## Bindande sakbeslut

Läs källrevisionen fullständigt. Följande totalsumma ska vara 1:1 spårbar:

- 22 `source_resolved_implementation_pending`;
- 6 `external_answer_required`;
- totalt 28 oförändrade blockerade dispositioner.

De 22 är: Vattenfall 12, Skellefteå 2, Sundsvall 2, EEM 1, Mälarenergi större
fastigheter 1, VB Energi 1, SFAB kundvald effekt 1, Kraftringen Brunnshög 1 och
Tekniska Verken Linköping lågtemperatur 1.

De sex är: Hässleholm 2, HEMAB 1, Gävle 1, Mälarenergi gruppanslutna småhus 1 och
Finspång spetsvärme 1.

## Ändringar som ska göras

1. Revidera `tariffinventering-v22.md`, `batchplan-v22.md` och
   `teknisk-kartlaggning-28-tariffer.md` så att gamla påståenden om att alla 28 väntar
   på leverantörssvar ersätts med den nya 22/6-klassningen. Bevara historiska noter som
   historik, men lägg daterade rättelser där de annars motsäger den nya baslinjen.
2. Normalisera `optimate-fjarrvarme-2026.json` utan att öppna aktiveringsgrinden:
   - bind aktuella officiella källor till berörda medlem-/tariffposter;
   - ersätt stale blockeringsvillkor med exakt återstående internt arbete eller extern
     fråga;
   - flytta R07, R09 och R14 från `remaining_information_requests` när deras gamla
     fråga inte längre är produktblockerande; bevara vad som lösts och hur i
     `resolved_information_requests`;
   - smalna av R03 till endast Mälarenergis gruppanslutna småhus;
   - behåll R02 och R08 med korrekt dispositionstäckning;
   - skapa entydiga requestposter för Gävles brytmånad och Finspångs 20-procentiga
     spetsvärmetillägg;
   - säkerställ att varje externt blockerad fysisk tariffrad täcks av exakt relevant
     request och att källösta rader förblir blockerade enbart av lokal
     implementationsstatus, inte en falsk extern fråga.
3. Lägg en mekaniskt kontrollerbar 28-raders dispositionsmatris i inventeringen eller
   ett direkt länkat, versionsstyrt underlag. Den ska även omfatta de fyra varianterna,
   som inte nödvändigtvis är fysiska katalograder.
4. Bevara prisdata om inte källrevisionen uttryckligen anger en verifierad rättelse.
   Ingen implicit standard för effekt, band, flöde, temperatur, nätmedel, profil eller
   avtalsklass får införas.
5. Lägg Vattenfalls officiella kalkylator och FAQ som normerande aktuella källor med
   retrieval-datum 2026-09-17. Om maskinläsbar komponent-URL är instabil ska sid-URL,
   hash och extraherad konfiguration dokumenteras; skapa inte en falsk permanent URL.
6. Dokumentera att VB-produkten bara omfattar Ludvika, Grängesberg, Fagersta och
   Norberg tills Björnmossen har bekräftats. Dokumentera hård 1 999-kW-gräns för de
   två Sundsvallsposterna; 2 000+ är individuellt och får fail-closed.

## Verifiering

Minst följande ska redovisas:

- JSON-parse och befintliga katalog-/inventerings-/dispositionsgrindar;
- mekaniskt bevis för exakt `22 + 6 = 28`, inklusive fyra varianter;
- exakt vilka `remaining_information_requests` som återstår och vilka dispositioner
  varje request täcker;
- oförändrad skarp disposition `62/2/28` och oförändrat antal katalograder/produkter;
- `git diff --check` på leveransens filer;
- inga ändringar i produktrepon, automation, Batch 7-historik eller orelaterade filer.

Commitera fokuserat i skills-repot. Lägg sedan en unik toppost i `conversations/index.md`
med:

`REVIEW_READY: Codex`

Sammanfatta att detta bara är käll-/blockeringsnormalisering, att alla 28 fortfarande
är tekniskt spärrade, att ingen produktkod/aktivering/push/historikomskrivning skett,
och att nästa planerade produktetapp efter godkänd granskning är Vattenfall 12.
