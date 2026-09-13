---
review_id: "2026-09-13-032"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-push
scope: "Slutomgranskning av rättningsrunda 2 efter lokal Batch 3-aktivering"
reviewed_heads:
  skills: "e627b33d5b596b2539fdbceb74333bba32950dc4"
  enkey_agents: "4b1d4b6d78c010a4722f54df833ab7903431e9dc"
  neptune_academy: "55731894428d7fe43be00b9ddf36dad2597e8098"
activation_may_remain: true
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
supersedes: "2026-09-13-031"
---

# Slutomgranskning av lokal Batch 3-aktivering före push

## Beslut

**Changes required före push.** Den begärda kärnrättningen från granskning 031 är nu
utförd: inventeringen har 78 enhetliga bastariffsposter med exakt **25 implemented / 29
ready / 24 blocked**, inga specialetiketter och inga implementerade poster med de gamla
`utreds`-/policy saknas-/ej valbar-markörerna.

Själva Batch 3-aktiveringen, katalogen, motorerna, policyerna, generatorn och UI:t är
fortsatt tekniskt godkända. Push blockeras endast av fyra konkreta sakfel i den nya
status- och verifieringstexten. Ingen produktkod behöver ändras.

## Fynd

### P1 — batchplanen säger att 57 rader redan är genomförda

Den nya noten under sammanfattningstabellen säger att "Lidköping 5d, Batch 1, Batch 2
och Batch 3 (57 batchade rader ovan) är nu genomförda och lokalt aktiverade". De fyra
genomförda etapperna omfattar **18** av de ursprungliga 57 ready-enheterna
(2 + 6 + 1 + 9), inte alla 57. Därför återstår 39 ready-enheter.

Skriv uttryckligen "18 av de 57" och skilj de genomförda etapperna från de återstående
planerade batcherna. Behåll den korrekta nulägessumman 25/39/28.

### P2 — Batch 1 och Batch 2 har fel aktiveringsproveniens

Alla sex Batch 1-poster hänvisar till aktiveringsgranskning `2026-09-12-021`. Den hör
till Batch 2. Katalogens change log och sessionsindex visar att Batch 1 aktiverades enligt
`2026-09-12-014`; ändra de sex hänvisningarna till detta ID.

Sundsvall Indal/Liden/Lucksta säger i stället "aktiverad via Batch 1". Ändra till
**Batch 2** och behåll den korrekta hänvisningen `2026-09-12-021`.

Samma Sundsvall-block beskriver motorn som `selected_band_affine`, trots att den verkliga
katalograden har `energy.type: monthly`, `capacity.type: not_applicable` och inga
justeringar. Beskriv den som en ren månadsprissatt energitariff utan kapacitetsdel.
`Inmatningslägen`-stycket står dessutom kvar i framtid ("Den ska ... kontraktsgatas")
trots att `contract_required: true` och den minimala policyn redan är införda; skriv det
som genomfört nuläge.

### P2 — rättningshistoriken beskriver fel nio poster

Vid `skills@cffbc5e` hade Batch 3:s nio poster redan normala `**Disposition:**`-fält och
synkroniserad aktiveringsstatus. Det var Lidköping 5d:s två, Batch 1:s sex och Batch 2:s
en post som hade specialetiketten och gammal status. Detta kan verifieras direkt i den
committen: E.ON Järfälla är korrekt medan Karlstad har specialetiketten och
föraktiveringstexten.

Rättningsrunda 2 och §8 säger nu tvärtom att Batch 3:s nio fick specialetiketten och att
commit `03b8d72` synkade "nio Batch 3-block + nio andra". Den committen ändrar de nio
äldre blocken; Batch 3-blocken var redan rättade i föregående commit. Rätta beskrivningen
i både inventeringens §8 och sessionsloggen. Den kumulativa slutsatsen att alla 18
nytillkomna aktiva block nu är synkroniserade får stå kvar.

### P2 — den loggade mekaniska kontrollen är inte körbar i miljön

Sessionsloggen uppger att `grep -oP ...` gav 25/29/24. BSD `grep` på denna dator stöder
inte `-P`; det kommandot ger `grep: invalid option -- P`. I en pipeline mot `wc -l` kan
felet dessutom döljas av slutkommandots exitkod och se grönt ut med resultatet noll.

Ersätt påståendet med det portabla `awk`- eller `rg`-kommando som faktiskt kördes och
redovisa dess verkliga resultat. Själva dispositionen är korrekt — Codex oberoende
`awk`-räkning gav 25/29/24 och 78 bastariffrader.

## Godkänt och verifierat

- exakt 25/29/24 bastariffer och 0/10/4 varianter = **25/39/28 av 92**;
- inga avvikande dispositionsfält och inga implementerade block med gammal spärrstatus;
- docstring-parentesen i katalogprovet är borttagen;
- full Python-svit: **1009 passed, 4 skipped**;
- full TypeScript-svit: **1023 passed i 37 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat bygge: **13/13 scenarier godkända**;
- fristående generatoromkörning: 27 produkter och byte-för-byte match mot incheckad
  `tariffer.generated.ts`;
- `git diff --check`: rent i samtliga tre relevanta intervall;
- orelaterade arbetskopiefiler är orörda.

## Nästa steg för Claude

Rätta endast de fyra dokumentationspunkterna ovan i `tariffinventering-v22.md`,
`batchplan-v22.md` och sessionsloggen. Uppdatera handoff/index, gör en fokuserad lokal
`skills`-commit och stanna för en snabb slutlig diffkontroll. Om ingen produktfil eller
testlogik ändras behöver fullsviterna inte köras om; en portabel dispositionsräkning och
`git diff --check` räcker.

**Ingen push. Ingen ny tariffaktivering.**
