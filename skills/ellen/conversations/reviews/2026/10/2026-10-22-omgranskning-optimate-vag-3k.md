# Optimate våg 3k — omgranskning av signal 2026-10-21-002

Beslut: `CHANGES_REQUIRED: Claude`. Inte slutgodkänd för aktivering eller push.

Granskat Neptune `8db511042600e04dcbd8f30313da6cecd67712ba` och skills `97f41e3bb219be4076e4aaf7a42f743a2a2a3161` med logg-HEAD `d9f7f9f`. Robert bad: ”Kontrollera om du kan slutgodkänna”.

## Stängda fynd

De två Python-fynden från 2026-10-21-001 är stängda inom granskat scope. Energi-, kapacitets- och policyobjekten jämförs nu strikt, och hela accessavgiftsfamiljen binds mot Wave-3k-listan. De nya negativa proven omfattar tidigare reproducerade kontraktsmutationer.

Neptunes fyra bandgränser körs nu genom produktionsvägen. Besparingarna pinnas mot handoffens literaler, och icke-numerisk kapacitet blockeras typat. Dessa delar av fynd 3 är stängda.

## Kvarstående fynd

1. **P2 — negativt felbandskrav har ersatts med ett accepterande test utan beslutad kravändring.** `neptune-marketing/src/utils/optimateScenarioVag3k.test.ts:578` kräver att band 1 vid 100 kW accepteras och ger 106 050 kr i kapacitetsled, jämfört med band 2:s 99 300 kr. Skillnaden i total årskostnad är 8 437,50 kr inklusive moms för samma övriga indata. Testet beskriver befintligt beteende, men uppfyller inte handoff 2026-10-18-009 rad 103: ”fel band för angiven effekt, okänt band eller saknat band blockerar”. Det anropar dessutom årsproduktvägen, inte scenariovägen som uppdraget gäller.

   Hänvisningen till `resultatkontrakt.ts: "VALIDERAS INTE här"` är missvisande. Texten finns i `besparingsvarde.ts:332` och förklarar att byggaren överlåter kontroll av okända ID:n till förkontrollen för rätt typat fel. Den ger inget stöd för ett beslut om numeriskt motsägande band/effekt. Befintlig motor slår upp ett bekräftat band efter ID; detta är inte en regression som introducerats i denna rättning. Krav och befintlig arkitektur behöver dock förenas uttryckligen innan slutgodkännande. Ändra inte den gemensamma motorn inom nuvarande test-/matrisscope. Redovisa relevant tidigare beslut/leverantörsunderlag och ett avgränsat förslag: antingen en motiverad rättelse av handoffens krav eller en separat godkänd valideringsändring. Godta inte bara det observerade utfallet som bevis för avsett beteende.

2. **P2 — beställt bevis för oförändrade indata saknas fortfarande.** Testet vid rad 599 och de nya bandgränsproven jämför utdata och summerade prisled. De fångar inte mutation av input eller ändrad proveniens/attestering som lämnar samma pris. Lägg ett Jönköping-prov som fryser eller jämför hela indataobjektet före/efter och kontrollerar att låsta kontraktsfält samt proveniens/attestering återanvänds i referens och alla tre backendanrop. Den befintliga scenariokoden sprider underlaget och ersätter energi, men det efterfrågade regressionsbeviset finns inte i leveransen. Ingen faktisk mutation har påvisats.

## Oberoende verifiering

- Full Vitest: **3 793/3 793 i 108/108 filer**. De åtta tidigare miljöblockerade filerna passerar också.
- Full matris-pytest: **286/286 + 8 subtest**.
- `tsc --noEmit`: grön; produktionsbygge: grönt.
- Matrisgenerator `--check` mot granskad snapshot: grön för 77 produkter och källhash.
- Båda rättningsdiffarnas `git diff --check`: rena.
- Disposition oförändrad: **62 publika / 1 intern / 1 prototyp / 13 ogranskade**.

Verifieringen kördes i granskarens isolerade `/Users/robertrennel/Code/neptune-review-vag-3k` på exakt Neptune-commit ovan. Den placeringen ger de äldre proven deras förväntade syskonrepo. `ELLEN_ENKEY_AGENTS_SOKVAG=/Users/robertrennel/Code/enkey-agents` och `ELLEN_PYTHON=/Users/robertrennel/Code/enkey-agents/.venv/bin/python` sattes också för proven som stöder dem. Problemet var alltså inte en kvarstående testregression. Byggändringarna i spårad `dist` återställdes; granskarens arbetskopia är ren.

## Nästa avgränsade steg

Claude kompletterar icke-muterings-/anropsprovet och rättar den felaktiga källhänvisningen. Bandfrågan ska lämnas till Codex med konkret underlag och förslag innan en ändring av beteende eller krav genomförs. Ingen tariffdata, gemensam motor, kund-UI, publik aktivering, mainflytt eller push ingår. Denna omgranskning har inte startat en ny Claude-körning.
