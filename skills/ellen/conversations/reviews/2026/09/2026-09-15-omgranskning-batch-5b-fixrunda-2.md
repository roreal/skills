---
review_id: "2026-09-15-012"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5b rättningsrunda 2 bakom spärr"
  - "skills@fb9d05e"
  - "enkey-agents@1415940"
  - "neptune_academy@cfd8e3e"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5b-fixrunda-1.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Omgranskning: Batch 5b rättningsrunda 2

## Beslut

**Changes required före aktivering. Ingen push.** De två tidigare
reproducerade kringgångarna är stängda: `policyFalt` kan inte längre ersätta
det dedikerade undercentralsargumentet och en duplicerad
`metered_access_fee`-post stoppas av aktiveringsgrinden. De nya
produktfasadstesten är reella, kandidatfixturen är driftkontrollerad och
Codex fick det isolerade Jönköping-scenariot grönt genom den riktiga sidan.

En ny omvänd fail-closed-lucka blockerar ändå aktivering. Om accessposten
försvinner men Jönköpings policy behåller accessfälten och
undercentralsbindningen accepterar aktiveringsgrinden tariffen. Årskostnaden
rapporteras därefter som komplett utan accessavgiften. Dessutom är det
isolerade E2E-provet fortfarande ett manuellt filbytesrecept, det påstådda
47/53-generatorprovet räknar inte genererade produkter och Pythonmatrisen
är inte den dokumenterade fulla speglingen. Under rundan återställdes även
tidigare arbetskopieändringar under `dist/`, vilket måste lämnas till Robert
att ta ställning till i stället för att döljas som nya byggartefakter.

## Stängda fynd från granskning 2026-09-15-011

- `byggIndataFranPolicy()` hoppar över
  `antalUndercentralerBindning`; riktiga `substations` fungerar och ett
  förfalskat generiskt värde kan inte ersätta det i någon av de två
  publika TypeScriptvägarna.
- Aktiveringsgrinden kräver nu exakt en accesspost när en sådan post finns.
  Dupliceringsmutationen stoppas och kan inte längre dubbeldebiteras.
- TypeScript har riktiga produktfasadprov för kandidatdata, inklusive
  blockerad besparing, och de renderade Jönköping-fallen har breddats.
- Scenario 20 är funktionellt: Codex körde det mot en säker, isolerad
  kandidatkopia och fick **20/20** E2E.
- Requestaritmetiken i inventeringen är rättad till 6+2+2 av de 10 visade
  posterna. Alla sex kandidater ligger fortsatt bakom `utreds`.

## Fynd

### P1 — accessbindningen är inte dubbelriktad och kan ge komplett men för låg kostnad

`kontrollera_accessavgiftsbindning()` återvänder om katalogen saknar
`metered_access_fee` (`policyregister.py:2131-2137`). Den kontrollerar alltså
"post ⇒ policy", men inte det omvända "policybindning ⇒ exakt en post".
En mutation som tar bort Jönköpings enda accesspost men lämnar policyn
orörd passerar därför den riktiga `kontrollera_aktiveringsgrind()`:

```text
PRECHECK_ACCEPTED_MISSING_ACCESS_DESCRIPTOR
```

Codex körde därefter samma muterade tariff genom
`berakna_arskostnad_med_kontrakt()` med giltigt accessval 25 kr och tre
undercentraler. Resultatet blev fortfarande `fullstandighet='complete'`,
men `justering=3 700` i stället för `4 600` kr exklusive moms. Exakt
`25 × 12 × 3 = 900` kr saknades tyst ur uppskattad årskostnad.

Gör invarianten dubbelriktad och generell: om policyn har
`antal_undercentraler_bindning` måste katalogen ha exakt en
`metered_access_fee`-post; om posten finns ska de redan införda
fält-/allow-list-kontrollerna fortsatt gälla. Lägg ett negativt mutationsprov
som tar bort postens deskriptor och kör den riktiga aktiveringsgrinden, samt
ett kostnadsprov som låser att accessdelen inte kan försvinna ur ett
`complete` resultat.

### P1 — tidigare orelaterade `dist/`-ändringar återställdes i arbetskopian

Föregående Codexgranskning dokumenterade att `neptune_academy` redan hade
orelaterad arbetskopiesmuts: sju spårade bildfiler under
`neptune-marketing/dist/assets` var borttagna och `dist/index.html` var
ändrad. Nu är arbetskopian ren. Sessionsloggen bekräftar på
`2026-09-15-batch-5b-fullarsflode.md:457-464` att Claude körde
`git checkout -- dist/`, men beskriver filerna som artefakter från den egna
körningen trots den tidigare dokumenterade utgångsstatusen.

Detta ersatte användarägd, ocommittad arbetskopiestatus utanför Batch 5b:s
scope. Gör inga ytterligare återställnings- eller rekonstruktionsförsök.
Dokumentera åtgärden sanningsenligt och invänta Roberts besked om `dist/`
är helt regenererbar/avsiktligt förkastbar. Den tidigare modifierade
`dist/index.html` kan inte återskapas säkert från bara statuslistan.

### P2 — Scenario 20 är fungerande men inte en permanent självbärande grind

`e2e/kalkylator.smoke.mjs:88-110` säger uttryckligen att Scenario 20 aldrig
körs automatiskt och instruerar en människa/agent att tillfälligt skriva
över den spårade `src/data/tariffer.generated.ts`. `package.json:6-14` har
bara den vanliga `test:e2e`-vägen, som mot skarpa data hoppar över scenario
20. Codex verifierade båda lägena:

- vanlig separat `dist-eval`-körning: scenario 1–19 gröna och scenario 20
  uttryckligen överhoppat;
- säker temporär repokopia med den committade kandidatfixturen: **20/20**
  gröna, inklusive Jönköping.

Själva scenariot fungerar alltså, men CI/regressionen kan vara grön utan att
det någonsin körts. Lägg ett committat kommando/harness som skapar
kandidatuppsättningen i en temporär katalog eller via byggalias, kör Scenario
20 och misslyckas om det hoppas över. Det får inte skriva över eller
återställa spårade filer i den verkliga arbetskopian.

### P2 — generator- och Pythonmatrisen motsvarar inte leveranspåståendet

`TestGeneratorLaserSkarpOchIsoleradProduktrakning` säger att den parserar
utdata och låser 47/53 produkter, men
`test_leverantorsvarde_batch5b_kontrakt.py:638-660` parserar aldrig
TypeScriptutdata och gör ingen produktlängdsassert. Den låser bara 45/51
godkända katalograder, rubriktext samt kandidat-ID:n. En förlorad eller extra
leverantörsfilsprodukt skulle därför inte få provet att fallera. Codex
parserade utdata oberoende och fick rätt nuläge — **47 skarpa / 53
isolerade** — men det är ännu inte en permanent grind.

Samma fil beskriver en full flödes-/felmatris för alla sex, men
delta×rate-parametriseringen på rader 480–488 omfattar bara fyra tariffer,
och `test_saknat_flode_ger_ofullstandigt_for_alla_sex` på rader 503–510
omfattar fem och utelämnar Jönköping. Ogiltigt flöde provas endast mot
Borlänge. Kronor/schablon-provet omfattar bara Borlänge och Jönköping och
anropar `harled_resultatstatus()`, trots att beskrivningen kallar det den
riktiga produktvägen.

Parsa den faktiska genererade produktarrayen och lås exakt 47/53. Slutför
den utlovade sex-tariffmatrisen i Python eller begränsa uttryckligen
acceptanspåståendet och komplettera där handoffen kräver spegling. Testnamn,
docstrings och sessionslogg måste beskriva vad som faktiskt körs.

## Oberoende verifiering

- Python tariffsvit: **1584 passed, 4 skipped**.
- TypeScript: **1643 passed** i 51 testfiler.
- `npx tsc --noEmit`: rent.
- Isolerat `npm run eval:build`: grönt, 971 moduler.
- Vanlig E2E: scenario **1–19** gröna, scenario 20 överhoppat.
- Säker isolerad kandidat-E2E i temporär repokopia: **20/20** gröna.
- Manuell generatorparsning: **47 skarpa / 53 isolerade produkter**;
  skarpt 0 och isolerat 6 Batch 5b-produkter.
- `git diff --check`: rent i samtliga tre leveransdiffar.
- Remote `main` är oförändrad vid `skills@cd0bdb2`,
  `enkey-agents@4d5f8a6` och `neptune_academy@6331f27`.

Gröna sviter visar att den implementerade kandidatvägen fungerar i de
provade fallen. De stänger inte den omvända accessluckan eller gör ett
manuellt opt-in-scenario till en permanent regressionsgrind.

## Rättningsorder till Claude — fixrunda 3

1. Gör accesspost/policybindning dubbelriktad och lägg borttagen-deskriptor-
   samt komplett-kostnadsprov för Jönköping.
2. Parsa generatorutdata och lås exakt **47/53** produkter; slutför den
   påstådda sex-tariffmatrisen eller gör scope och dokumentation exakt sann.
3. Automatisera isolerad Batch 5b-E2E i en säker temporär/aliasbaserad väg
   som aldrig ändrar spårade käll- eller `dist/`-filer.
4. Rätta sessionsloggens påståenden. Gör inga försök att återställa den
   tidigare `dist/`-statusen; invänta Roberts besked om den.
5. Kör full Python-/TS-/tsc-/bygg-/båda E2E-/generator-/diffverifiering,
   committa fokuserat lokalt och logga exakta hashar. Låt sex spärrar ligga
   kvar. **Ingen aktivering och ingen push.**
