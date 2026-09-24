---
handoff_id: "2026-09-24-016"
created_at: "2026-09-24T20:14:27+02:00"
from: Codex
to: Claude
status: approved-for-implementation
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_IMPLEMENTATION: Claude – Stockholm Optimate 10/15/20

## Mål

Byt Stockholm Exergis synliga, preliminära energiscenarier från
15/20/25 procent till 10/15/20 procent. Detta är Fas A och ska bli ett
visuellt och beräkningsmässigt acceptanstest innan den gemensamma motorn och
fler tariffprodukter ändras.

## Verifierade baser

- skills `origin/main@775bd66acc339f006fc722b6fb17c812b7fdee4e`
- enkey-agents `origin/main@26eb133ec14a02ca956e9a87d8467a7f9f0860ea`
- neptune_academy `origin/main@f5f3603202c7c4377484f37f9719f4cad760c9fb`

Utgå från Neptunes exakta remote-main i en ny isolerad branch/worktree.
Den befintliga rena worktreen
`/private/tmp/neptune-academy-harnosand-2026` pekar på samma commit men dess
branch ska inte återanvändas som namn för det nya arbetet. Enkeys lokala
`main@5150d0b` innehåller orelaterat Milesight-arbete och får inte användas.

## Tillåtet implementationsscope

Primära filer:

- `neptune-marketing/src/utils/stockholmOptimatePotential.ts`
- `neptune-marketing/src/utils/stockholmOptimatePotential.test.ts`
- `neptune-marketing/e2e/kalkylator.smoke.mjs`

`KalkylatorPage.tsx` eller dess befintliga test får endast ändras om en
Stockholmsspecifik statisk text eller assertion annars blir fel. Gör ingen
layoutombyggnad och ingen tariffaktivering.

## Exakta regler

1. Stockholm-konstanten blir `[0.10, 0.15, 0.20]`.
2. Minskningen appliceras endast på styrbar rumsvärme. Varmvatten/övrig
   last förblir oförändrad.
3. Huvudscenarierna fryser debiterbar effekt, returtemperatur och
   kölddygnsvolym precis som idag.
4. Separat effektkänslighet behåller antagandet 20 procent lägre
   debiterbar effekt. Efter ändringen jämförs den mot det mittersta
   **15-procentiga energiscenariot**. Den får inte bakas in i huvudtalen.
5. Dynamiska test-ID:n och synlig text ska följa 10/15/20.
6. Fortsätt märka potentialen som preliminär, uppskattad och inte
   garanterad; bevarad komfort verifieras separat.

Minsta numeriska regressioner:

- 1 000 MWh total köpt värme med skattad rumsvärme 820 MWh ger sparad
  rumsvärme `[82, 123, 164]` MWh.
- 1 000 MWh explicit rumsvärme ger `[100, 150, 200]` MWh.
- Handräkning och effektkänslighet som tidigare använde mittenscenariot
  20 procent ska uppdateras till mittenscenariot 15 procent utan att
  ändra den separata effektandelen 20 procent.

## Uttryckligen utanför scope

- `src/utils/optimateScenario.ts` och dess interna Sundsvall-pilot,
- den publika scenario-allowlisten,
- `stodjer_besparing`, tariffkatalog, priser eller leverantörsaktivering,
- andra energibolag,
- Enkey/skills domändata,
- push, merge, rebase eller historikomskrivning.

Träffar på 15/20/25 i den generiska motorn är alltså avsiktligt kvar
efter Fas A och ska redovisas som sådana, inte ”rättas” i denna leverans.

## Verifiering

- Riktade Stockholm-enhetstest.
- Full Vitest-svit och `npx tsc --noEmit`.
- Isolerat bygge utan att lämna spårad `dist/` ändrad.
- Ordinarie Chromium-E2E; Scenario 26 ska kontrollera 10/15/20 och
  100/150/200 MWh för explicit rumsvärme.
- `git diff --check` och exakt fillista.

Committa lokalt och skriv en ny unik toppost
`REVIEW_READY: Codex` med full Neptune-HEAD, tester, fillista och uttrycklig
bekräftelse att generisk motor, aktivering och push är orörda.
