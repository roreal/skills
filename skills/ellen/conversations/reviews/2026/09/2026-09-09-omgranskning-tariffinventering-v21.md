---
review_id: "2026-09-09-015"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v21.md
  - Fjarrvarmetariffer/batchplan-v21.md
  - skills commits bfbf4327334423519e91e46e6d540a63ac9d94c6 and 6a138824a9cc9ac4578b653ffaa0387bfc2e8e0b
reviewed_heads:
  skills: "6a138824a9cc9ac4578b653ffaa0387bfc2e8e0b"
  enkey-agents: "17c859908f938e419bf3ce92a8daf11282f63878"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-014"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v21 och batchplan v21

## Bedömning

V21 löser konstruktionsfyndet från granskning 014. Den planerade
`TariffpolicyOptions` är namngiven och exporterad, flödesvarianten är den slutna unionen
`'golvfri' | 'golvbegransad'`, och samtliga sju nyckelbärande bindningar valideras både
för existens och avsedd `vardetyp`. Normaliseringen `krav.vardetyp ?? 'number'` bevarar
bakåtkompatibiliteten för befintliga skalära krav. De negativa direkt- och
genereringstesten är också tillräckligt specificerade.

Attesteringskedjan är förbättrad i Batch 0:s punkter 5–8 och testplanen täcker nu de fem
begärda gränserna. Men batchplanen inför samtidigt en andra attesteringskälla i
förkontrollen, i direkt konflikt med inventeringens gällande fyrparameterskontrakt och
dess konkreta anropsskisser. Dessutom är själva `tariffinventering-v21.md` fortfarande
identifierad som V20 och flera aktiva batchreferenser pekar på V20. Planen är därför inte
implementeringsklar. V22 krävs innan produktkod, tariffdata, aktivering eller push.

## P1-fynd

### P1 — förkontrollen har två konkurrerande attesteringskällor

Inventeringen anger ett sammanhängande kontrakt:

- `byggIndataFranPolicy(policy, policyFalt, policyFaltAttestering)` skriver
  `IndataPost.attesterad` (`tariffinventering-v21.md:2728–2744`);
- `forkontrolleraPolicyIndata(policy, prisar, indata, omfattning)` tar fyra parametrar och
  läser den färdigbyggda `ReadonlyMap<string, IndataPost>`
  (`tariffinventering-v21.md:2831–2837`); och
- båda utskrivna produktanropen använder just den fyrparametriga formen
  (`tariffinventering-v21.md:3772–3778` och `4016–4021`).

Batchplanens punkt 8 byter däremot till
`forkontrolleraPolicyIndata(policy, prisar, indata, indataAttestering, omfattning)` och
läser `indataAttestering[f.nyckel]` (`batchplan-v21.md:304–332`). Punkt 12 hänvisar sedan
till denna ”femte parameter” (`batchplan-v21.md:487–494`), trots att inledningen säger att
punkt 12 är borttagen och att punkterna 5–8 är det enda gällande kontraktet.

Det ger två sanningskällor efter byggsteget: `IndataPost.attesterad` och en separat karta.
De kan motsäga varandra, och batchplanen anger inte vilken av dem som ett direkt
produktanrop ska skicka till förkontrollen. Den separata kartan behövs bara fram till
byggaren; därefter ska både förkontrollen och den auktoritativa statusvalidatorn läsa
samma `IndataPost.attesterad`. Då ger ett uteblivet `policyFaltAttestering` automatiskt
`attesterad: false`, ett fältnära `ej_attesterat` i produktvägen och `blocked` i den
direkta fasadvägen utan parallella kontrollkanaler.

**Begärd rättning:** behåll fem argument på `byggKontraktIndata` och tre på
`byggIndataFranPolicy`, men behåll exakt fyra argument på
`forkontrolleraPolicyIndata(policy, prisar, indata, omfattning)`. Punkt 8 ska kontrollera
`post.attesterad === true` för krav med `kravAttestering === true`. Stryk punkt 12 helt;
den ligger sist och kräver därför ingen omnumrering. Behåll de fem redan specificerade
attesteringstesten, men låt produkt- och förkontrolltesten bevisa att de läser
`IndataPost.attesterad`, inte den råa DTO-kartan.

### P1 — V21 saknar egen dokumentidentitet och använder V20 som aktiv normkälla

Den mekaniska V20→V21-jämförelsen visar att inventeringens enda sakändring ligger kring
policykonstruktorn. Filens rubrik är fortfarande ”Tariffinventering v20.0”, inledningen
säger att den ersätter V19 och svarar på granskning 013, och sammanfattningen heter ”Vad
som är nytt i v20” (`tariffinventering-v21.md:1–56`). Den pekar dessutom ut
`batchplan-v20.md` som det aktuella dokumentet vid rad 46.

Batchplanen har rätt V21-rubrik, men flera normativa eller aktuella arbetsstycken pekar
fortfarande på `tariffinventering-v20.md`, bland annat den gällande förmågedefinitionen,
Batch 5d:s motorkedja och fillista, dess test-/dokumentationsscope, Batch 7:s
produktbegränsning och slutsummeringen (`batchplan-v21.md:375–376`, `560–564`, `589–600`,
`656–663`, `1120–1125`, `1277–1281`). Detta motsäger både granskning 014:s uttryckliga
krav och leveransloggens påstående att aktiva referenser är uppdaterade.

**Begärd rättning:** ge V22 en verklig V22-rubrik och inledning: den ersätter V21, svarar
på granskning 015 och har ett kort eget ”Vad som är nytt i v22”-avsnitt. Uppdatera alla
normativa och aktuella korsreferenser till V22. Äldre versioner får bara förekomma när
texten uttryckligen beskriver historik eller en äldre gransknings leverans.

## Godkända delar och verifieringar

- `TariffpolicyOptions` och de sju bindningarnas existens-/typvalidering löser P1 #2 i
  granskning 014 och ska bevaras oförändrade i sak.
- Batch 0:s punkt 5 bär attestkartan genom produkt-DTO:er och båda byggarna till
  `IndataPost.attesterad`; metadataformen och orsaksunionen har rätt fält.
- Testplanen anger metadata, UI-default, byggare, direkt produktentry och direkt fasad,
  med både negativ och positiv attesteringsväg.
- Den verkliga femparametersguarden för `beraknaBesparingsvardeKontrakt`, fail-closed
  besparingsförmåga, `vardefelForKrav`-ägarskap, Tm-modell, motortransport och Batch 5d:s
  verkliga katalogfil ska bevaras.
- Lidköpings två produkter förblir källgodkända och `ready_to_implement`. Dispositionen
  förblir 7 implementerade, 57 redo och 28 externt blockerade av totalt 92.
- V21:s lokala Markdownlänkar är hela; den enda naiva regexträffen var koduttrycket
  `JUSTERING_BERAKNING[post.type](...)`, inte en länk. `git diff --check
  c732bd4..6a13882` är rent.
- Produktrepoerna står oförändrade på `enkey-agents@17c8599` och
  `neptune_academy@f1df177`; V21-committarna ändrar bara dokumentation och logg.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v22.md` och `batchplan-v22.md`; ändra inte V21 i efterhand.
2. Använd en enda attesteringskälla efter byggsteget: `IndataPost.attesterad`.
   `forkontrolleraPolicyIndata` ska ha fyra parametrar och läsa posten; den råa
   attesteringskartan slutar vid byggaren.
3. Stryk Batch 0 punkt 12 helt. Punkterna 5–8 och deras tester ska ensamma beskriva den
   fullständiga modellen.
4. Ge inventeringen korrekt V22-identitet och byt samtliga aktiva/normativa V20-/V21-
   korsreferenser till V22. Bevara äldre referenser endast i uttrycklig historik.
5. Bevara den godkända strikta `TariffpolicyOptions`, samtliga tidigare godkända delar,
   Lidköpings källstatus, Åkermannen-underlaget och räkningen 7/57/28.
6. Lägg granskning 015 och loggändringarna i en fokuserad lokal dokumentationscommit,
   logga verklig hash/tid och stanna för omgranskning. Ändra ingen produktkod, tariffdata,
   genererad fil, aktivering eller push.
