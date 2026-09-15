---
review_id: "2026-09-15-014"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5b rättningsrunda 4 bakom spärr"
  - "skills@7043143"
  - "enkey-agents@18022c1"
  - "neptune_academy@b54329b"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5b-fixrunda-3.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Omgranskning: Batch 5b rättningsrunda 4

## Beslut

**Changes required före aktivering. Ingen push.** Pythonvalet är nu
självbärande på Roberts maskin, Falu ytterorter ingår i delta×rate-matrisen
och smoke-drivern körs ur den arkiverade tempkopian. Med fri port passerar
det exakt dokumenterade kommandot **20/20**, och samtliga produkt-, motor-,
generator- och UI-sviter är gröna.

En av den föregående granskningens fail-closed-delar är dock inte faktiskt
stängd. Vid en upptagen port hinner HTTP-kontrollen godta den redan
lyssnande gamla servern innan den nya previewprocessens asynkrona
`exit`-handler sätter avbrottsflaggan. Harnesset kör då smoke-sviten mot fel
build. Codex reproducerade detta direkt. Den gamla manuella filbytesguiden
i smoke-filens huvud motsäger dessutom den nya säkra vägen och bör tas bort
i samma lilla sluträttning.

Ingen tariff- eller produktlogik behöver ändras i fixrunda 5.

## Stängda fynd från granskning 2026-09-15-013

- `valjPython()` prioriterar dokumenterad `ELLEN_PYTHON`, därefter
  `enkey-agents/.venv/bin/python`, och kräver Python ≥3.10 innan
  generatorn körs. Exakt `npm run test:e2e:batch5b-isolated` väljer nu
  projektets Python 3.14 och passerar normalfallet.
- Falu ytterorter finns i delta×rate-parametriseringen med katalogens
  3,5 kr/m³. Klassen lovar inte längre ett källgrundat över-max-fall.
- Smoke-drivern tas från `tempMarketing/e2e`, inte från den verkliga
  arbetskopian.
- `dist/` har rensats till HEAD enligt Roberts beslut och är rent. Ingen
  byggoutput har committats; utvärderingen använder `dist-eval/` och
  temporär katalog.
- Accessgrind, Jönköpings 900-kronorslås och 47/53-generatorgrind är
  oförändrat gröna.

## Fynd

### P2 — portkonfliktsspärren har fortfarande en readiness/exit-race

`batch5b-isolated-e2e.mjs:186-200` startar previewprocessen och sätter
`serverAvbruten` först när Node levererar dess asynkrona `exit`-event.
`vantaPaServer()` provar samtidigt URL:en direkt. Om port 4174 redan
används kan den gamla servern svara innan den nya processens portfel hunnit
sätta flaggan.

Codex reproducerade exakt detta:

1. startade skarp `dist-eval` på port 4174;
2. körde `npm run test:e2e:batch5b-isolated`;
3. den nya `vite preview --strictPort` kunde inte äga porten, men harnesset
   började ändå köra scenario 1–19 mot den gamla servern;
4. körningen föll först i scenario 20 med "Jönköping Energi saknas" — inte
   vid serverstarten.

Det är fail-open mot fel server och kan bli falskt grönt om den gamla
servern råkar innehålla en tidigare Batch 5b-kandidat. Vänta på en
processunik readiness-signal från den startade Viteprocessen innan HTTP-
polling, använd Vites program-API med en OS-tilldelad port eller inför en
annan lösning som bevisar att just den startade child-processen äger
adressen. Lägg ett regressionstest som avsiktligt blockerar vald port och
kräver ett serverstarts-/portfel **innan** smoke-sviten körs.

### P2 — smoke-filens huvud instruerar fortfarande ett osäkert manuellt filbyte

`e2e/kalkylator.smoke.mjs:88-110` säger att Scenario 20 aldrig körs
automatiskt och instruerar användaren att skriva över den spårade
`src/data/tariffer.generated.ts`, köra ett build som skriver `dist/` och
sedan återställa filen manuellt. Detta är nu både inaktuellt och motsatsen
till den nya säkra permanenta grinden.

Ersätt receptet med att vanlig `npm run test:e2e` avsiktligt hoppar över
den spärrade kandidaten och att
`npm run test:e2e:batch5b-isolated` är den enda dokumenterade vägen för
Scenario 20. Ingen instruktion ska längre rekommendera temporär skrivning
till en spårad fil i den riktiga arbetskopian.

## Oberoende verifiering

- Python tariffsvit: **1608 passed, 4 skipped**.
- TypeScript: **1643 passed** i 51 testfiler.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt, 971 moduler, endast `dist-eval/`.
- Vanlig E2E mot separat `dist-eval`: scenario **1–19** gröna och scenario
  20 korrekt överhoppat.
- Exakt `npm run test:e2e:batch5b-isolated`, fri port: **20/20** gröna,
  projektets Python 3.14 valdes automatiskt.
- Samma kommando med port 4174 avsiktligt upptagen: **föll först i scenario
  20 efter att 1–19 körts mot den gamla servern**, vilket reproducerar
  kvarvarande race.
- `git diff --check`: rent i samtliga tre leveransdiffar.
- Arbetskopiorna för `enkey-agents` och `neptune_academy` är rena;
  `skills` har endast sedan tidigare dokumenterade orelaterade filer.
- Dispositionen är fortsatt **45/19/28**, produktmängden **47/53** och alla
  sex kandidater ligger kvar bakom `utreds`.
- Remote `main` är oförändrad vid `skills@cd0bdb2`,
  `enkey-agents@4d5f8a6` och `neptune_academy@6331f27`.

## Rättningsorder till Claude — fixrunda 5

1. Gör serverstarten processunik och verkligt fail-closed. Ett avsiktligt
   upptaget portnummer ska stoppa före smoke och ge ett tydligt port-/
   serverstartsfel; lägg ett permanent negativt prov för detta.
2. Ersätt smoke-filens manuella filbytesguide med hänvisning till
   `npm run test:e2e:batch5b-isolated`.
3. Ändra ingen tariff-, motor-, produkt- eller kandidatdata. Kör riktade
   portkonflikt-/normalfallsprov samt full Python-/TS-/tsc-/bygg-/standard-
   E2E-/isolerad E2E-/generator-/diffverifiering. Committa fokuserat lokalt,
   logga exakta hashar och lämna sex spärrar kvar. **Ingen aktivering och
   ingen push.**
