---
review_id: "2026-09-09-016"
date: "2026-09-09"
reviewer: Codex
status: approved-with-conditions
scope:
  - Fjarrvarmetariffer/tariffinventering-v22.md
  - Fjarrvarmetariffer/batchplan-v22.md
  - skills commits a5729cbd93ec19111399c4dd0368687b1e36ff31 and ea917d7bf53d38ddf20c7c4149bc9aa967bbb84e
reviewed_heads:
  skills: "ea917d7bf53d38ddf20c7c4149bc9aa967bbb84e"
  enkey-agents: "17c859908f938e419bf3ce92a8daf11282f63878"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
approved_implementation_scope: batch-0-infrastructure-only
implementation_start_authorized: false
tariff_activation_allowed: false
push_allowed: false
implementation_changed: false
supersedes_review: "2026-09-09-015"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Godkännande av tariffinventering v22 och batchplan v22

## Beslut

V22 stänger båda P1-fynden i granskning `2026-09-09-015` och godkänns med villkor som
implementationsplan för **Batch 0:s grundinfrastruktur**. Ingen V23-plan krävs före denna
avgränsade kodetapp.

Godkännandet betyder inte att de 57 planerade tarifferna är implementerade eller
produktionsgodkända. Det omfattar inte tariffaktivering, ändrad status i katalogen, push
eller någon efterföljande tariffbatch. Själva kodstarten inväntar Roberts uttryckliga
klartecken; denna kontrollpunkt var en granskning, inte en beställning av produktändringar.

## Stängda fynd

### En attesteringskälla efter byggsteget

Batch 0 anger nu en sammanhängande kedja:

1. `policyFaltAttestering` transporteras genom UI- och produkt-DTO:erna.
2. `byggIndataFranPolicy(policy, policyFalt, policyFaltAttestering)` skriver värdet till
   `IndataPost.attesterad`.
3. `byggKontraktIndata` tar sina fem planerade argument och returnerar den byggda kartan.
4. `forkontrolleraPolicyIndata(policy, prisar, indata, omfattning)` har fyra parametrar
   och läser `post.attesterad` ur kartan.
5. `harledResultatstatus`/Pythonmotsvarigheten läser samma `IndataPost.attesterad` som
   oberoende, auktoritativ spärr för direkta fasadanrop.

Det finns därmed inte längre en separat attesteringskarta efter bygggränsen. Direkta
produktanrop utan `policyFaltAttestering` får fail-closed `attesterad: false` och ett
fältnära `ej_attesterat`; direkta fasadanrop utan attestering blir `blocked`.

### Korrekt V22-identitet och normkälla

Båda dokumenten har nu V22-rubrik, ersätter V21, refererar granskning 015 och innehåller
ett eget V22-avsnitt. Den mekaniska V21→V22-diffen visar att aktiva Batch 0-, Batch 5d-,
Batch 7- och summeringsreferenser har flyttats till `tariffinventering-v22.md`/
`batchplan-v22.md`. Återstående V20/V21-förekomster hör till inledande proveniens eller
uttryckligt märkta historikavsnitt.

## Godkända delar som ska bevaras

- Den namngivna, exporterade `TariffpolicyOptions` med samtliga åtta planerade fält.
- Den slutna unionen `'golvfri' | 'golvbegransad'` och runtimegrinden för genererad rådata.
- Existens- och `vardetyp`-validering av samtliga sju nyckelbärande bindningar, inklusive
  bakåtkompatibelt `vardetyp ?? 'number'` för befintliga skalära krav.
- Den fullständiga testmatrisen för attestering: metadata, UI-default, byggare, direkt
  produktentry och direkt fasad, med både positiv och negativ väg.
- Fail-closed produktförmågor, `vardefelForKrav` som delad validator, Tm:s
  `supplier_value`-/`snapshot`-modell, motortransporten och den verkliga katalogfilen.
- Lidköpings två källgodkända `ready_to_implement`-produkter och dispositionen
  7 implementerade / 57 redo / 28 blockerade av 92.

## Icke-blockerande redaktionella noteringar

- `batchplan-v22.md:515–518` har kvar en parentes som säger att punkt 12 är borttagen.
  Den är inte längre en numrerad punkt och innehåller inget alternativt kontrakt, men kan
  strykas redaktionellt.
- Fillistan vid `batchplan-v22.md:524` säger fortfarande ”punkt 11/12 ovan”. Den
  auktoritativa hänvisningen är punkt 11 för policykonstruktionen och punkterna 5–8 för
  attesteringen. Detta är ett hänvisningsfel, inte ett eget API. Samma parentes innehåller
  språkfelet ”är därför strukits”.

Dessa rester kräver ingen V23. Om V22 rättas redaktionellt ska ändringen vara en liten,
separat dokumentationsdiff utan nya designbeslut och nämnas i nästa leveranslogg.

## Villkor för Batch 0-implementationen

När Robert ger klartecken får Claude genomföra endast Batch 0:

1. Implementera de typade kontrakten och valideringarna i Python och TypeScript enligt
   V22, med en enda attesteringskälla efter byggsteget.
2. Trä `policyFalt` och `policyFaltAttestering` genom den verkliga produktkedjan och UI:t;
   legacyfältet `falt` och legacytariffernas beteende ska förbli oförändrade.
3. Implementera den namngivna årskostnadsentryn, fail-closed förmågegrindarna och de
   typade användar-/produktbegränsningsfelen som Batch 0 specificerar.
4. Uppdatera generatortransport och deterministiskt genererade artefakter endast i den
   utsträckning grundkontraktet kräver. Ingen tariff får aktiveras eller flyttas mellan
   dispositioner i denna etapp.
5. Kör relevanta Python- och TypeScripttester, de fem attesteringsgränserna,
   direkt-/genererad policykonstruktion, typkontroll, produktionsbygge,
   generator-/fixture-synk och `git diff --check`.
6. Skapa fokuserade lokala commits per berört repo, redovisa bas- och slut-HEAD,
   ändrade filer och exakta testkommandon/resultat och stanna för Codex kodgranskning.
   Ingen push.

## Verifierat nuläge

- V21→V22 ändrar endast den beställda dokumentidentiteten och attestmodellens beskrivning;
  tariffmatrisen och dispositionerna är oförändrade.
- `git diff --check 6a13882..ea917d7` är rent.
- Inga brutna lokala Markdownlänkar hittades efter att kodblock och inlinekod
  exkluderats från kontrollen.
- Produktrepoerna är oförändrade och rena på `enkey-agents@17c8599` och
  `neptune_academy@f1df177`.
- Inga kodtester kördes eftersom V22 är en dokumentationsleverans utan produktändringar.
