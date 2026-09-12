---
review_id: "2026-09-12-028"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope: "Batch 3 rättningsrunda 4 efter granskning 027"
reviewed_heads:
  skills: "008c67c8a70a466151410c7ad52580fd01be3635"
  enkey_agents: "f0a030f4b6d2b03f30f13c09f9b8d85c9ce886ac"
  neptune_academy: "c1741801f1a2a43c9a8bdf1d539bcde7f88daa87"
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
---

# Omgranskning av Batch 3 — rättningsrunda 4

## Beslut

**Changes required före lokal aktivering.** Det enda fyndet i granskning 027 är rättat
i den publika TypeScript-produktfasaden: saknad, trunkerad och omvänd källperiod
blockeras typat före kostnad, hela januari–februari-intervallet ger
`snapshot/complete` och exakt värde når `IndataPost`.

Rättningen lade samtidigt samma nya ISO-intervallregel i det delade
`harledResultatstatus`, men lämnade Python-spegeln oförändrad enligt den tidigare
arbetsordern. Därmed ger de två språkversionerna nu olika beslut för identisk annual-
indata. Detta måste återställas före aktivering. Den minsta rättningen är att behålla
den nya produktgrinden men ta bort överimplementeringen ur den delade TypeScript-
statusvalidatorn.

## Fynd

### P1 — TypeScript och Python har nu olika auktoritativt resultatkontrakt

`resultatkontrakt.ts::harledResultatstatus` har fått en ny annual-gren som kräver
`ÅÅÅÅ-MM-DD/ÅÅÅÅ-MM-DD` för varje `kalperiodDefinition`. Motsvarande
`resultatkontrakt.py::harled_resultatstatus` kräver fortfarande, enligt det etablerade
gemensamma kontraktet, bara en icke-tom `observerad_period` när källperioden inte kan
verifieras maskinellt.

Codex reproducerade samma Kraftringen-liknande krav och
`observeradPeriod='2026-01'` direkt mot båda statusvalidatorerna:

```text
Python:     Resultatstatus(omfattning='annual', noggrannhet='snapshot',
            fullstandighet='complete')
TypeScript: Error: effekt.observeradPeriod: "2026-01" är inte ett giltigt
            källperiodintervall
```

De befintliga delade testvektorerna finns uttryckligen för att hindra denna typ av
språkdrift, men de saknar en ogiltig annual-källperiod och fångar därför inte
regressionen. Fullsviterna blir gröna trots olika kontrakt. Python-Batch 3-fixturen
förstärker motsägelsen genom att fortfarande skapa Kraftringens period som `2026-01`.

### Minsta föredragna rättning

1. Behåll den nya periodkontrollen i `forkontrolleraPolicyIndata`. Det är
   TypeScript-produktlagrets grind och gör `beraknaArsprodukt` fail-closed precis som
   granskning 027 krävde.
2. Ta bort endast den nytillagda annual-formatgrenen ur
   `harledResultatstatus`. Den gemensamma statusvalidatorn ska åter ha samma semantik
   som Python: en fri, icke-maskinellt verifierbar `kalperiodDefinition` kräver en
   icke-tom källperiod och takar resultatet på `snapshot`; produktlagret får tillämpa
   den striktare UI-/produktkonventionen för ISO-intervall.
3. Lägg ett regressionsprov som tydliggör lagergränsen: produktfasaden avvisar
   `2026-01`, medan den delade statusvalidatorns befintliga språkneutrala semantik inte
   ändras av produktformatet.
4. Rätta den test-only Python-fixturen `_indata_for` för Kraftringen från `2026-01` till
   `2026-01-01/2026-02-28` och uppdatera kommentaren. Ingen Python-produktionskod ska
   ändras.

Om ISO-intervall i stället avsiktligt ska bli en ny regel i det **delade**
resultatkontraktet krävs den större alternativa vägen: samma validering i Python,
gemensamma positiva/negativa testvektorer och uppdaterade hashgrindar i båda repon.
Gör inte halva denna variant. Den föredragna minsta rättningen ovan räcker för Batch 3.

## Stängt från granskning 027

- `forkontrolleraPolicyIndata` ger typad `invalid_policy_fields` med orsaken `period`.
- Publik `beraknaArsprodukt` blockerar saknad period, `2026-01` och omvänd ordning.
- Kraftringens publika happy-path använder `2026-01-01/2026-02-28` och ger
  `snapshot/complete`.
- Ett direkt byggarprov visar bokstavligen oförändrad forwarding till den bundna
  `IndataPost.observeradPeriod`.
- UI:s `policyFelText` täcker den nya typade periodorsaken.
- Ingen katalog-, pris-, generator-, spärr- eller dispositionsändring gjordes.

## Oberoende verifiering utförd av Codex

- full TypeScript-svit: **1004 passed i 36 filer**;
- full Python-svit: **1009 passed, 4 skipped**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- E2E mot isolerat `dist-eval`: **10/10 scenarier godkända**;
- `git diff --check`: rent i samtliga granskade intervall;
- generatorfilen är oförändrad i rättningsrunda 4;
- `neptune-marketing/dist` är fortsatt orört.

Ett nytt oincheckat testartefakt finns som
`neptune-marketing/test-results/.last-run.json`. Det ska tas bort eller uttryckligen
ignoreras före en framtida push och får inte följa med i aktiveringscommitten.

## Nästa steg för Claude

1. Återställ språkparitet med den minsta lageravgränsade rättningen ovan.
2. Rätta Python-fixturens period, men inte Python-produktionskontraktet.
3. Ta hand om det oincheckade `test-results`-artefaktet utan att röra de sedan tidigare
   användarägda `dist`-ändringarna.
4. Kör berörda riktade prov, full Python/TypeScript, `tsc`, isolerat bygge, E2E och
   `git diff --check`; stanna för Codex slutgranskning.

**Ingen tariffaktivering, ingen borttagning av R06/R10 och ingen push.**
