---
review_id: "2026-09-15-013"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5b rättningsrunda 3 bakom spärr"
  - "skills@e2e4e2f"
  - "enkey-agents@30ffc74"
  - "neptune_academy@3f49941"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "45 implemented / 19 ready / 28 blocked av 92"
generated_products: "47 skarpa; isolerad aktiveringskopia 53"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5b-fixrunda-2.md"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Omgranskning: Batch 5b rättningsrunda 3

## Beslut

**Changes required före aktivering. Ingen push.** Själva tariff- och
produktlogiken som blockerade föregående runda är nu rättad. Den omvända
accessbindningen stoppar en borttagen deskriptor, den oförändrade
Jönköpingsraden låser de fulla 900 kronorna, generatorprovet parserar nu den
verkliga produktordboken och verifierar exakt 47/53 produkter. Den nya
isolerade E2E-vägen kan också köra och godkänna alla 20 scenarier utan att
röra den riktiga arbetskopians käll- eller `dist/`-filer.

Två delar av den bindande verifieringsleveransen återstår. Det nya
standardkommandot är inte självbärande i repots normala arbetskatalog,
eftersom Node-processen hårdkodar ett inkompatibelt system-`python3`.
Dessutom saknas fortfarande Falu ytterorter i delta×flödesprisprovet trots
leveranspåståendet att den matrisen omfattar alla sex. E2E-harnesset bör i
samma lilla rättning göras fail-closed mot en upptagen port och köra den
arkiverade smoke-filen, inte en möjlig ocommittad arbetskopieversion.

## Stängda fynd från granskning 2026-09-15-012

- `kontrollera_accessavgiftsbindning()` kräver nu
  `metered_access_fee` när policyn deklarerar
  `antal_undercentraler_bindning`. Borttagen-deskriptor-mutationen stoppas
  i den riktiga aktiveringsgrinden.
- Kostnadsprovet låser Jönköpings accessdel till `25 × 12 × 3 = 900` kr
  exklusive moms och den kompletta exempelårskostnaden till 62 500 kr.
- Generatorprovet parserar den genererade `TARIFFER`-ordboken och låser
  47 skarpa respektive 53 isolerade produkter samt kandidat-ID:na.
- Saknat och ogiltigt flöde samt kronor/schablon omfattar nu alla sex
  kandidater. Det avsedda isolerade Scenario 20 fungerar genom den riktiga
  sidan.
- Roberts/Codex beslut om `neptune-marketing/dist/` är nu fastställt:
  katalogen är regenererbar byggoutput, inte källans sanningskälla. Den
  nuvarande deterministiskt återskapade diffen är förkastbar, ska inte
  committas och behöver inte rekonstrueras. Framtida utvärdering ska använda
  `dist-eval/` eller temporär katalog.

## Fynd

### P1 — det nya npm-kommandot väljer inkompatibel Python och faller före E2E

`e2e/batch5b-isolated-e2e.mjs:103-109` anropar det generiska kommandot
`python3`. Från `neptune-marketing` löser en Node-underprocess detta på
Roberts maskin till `/usr/bin/python3`, Python 3.9.6. Tariffmotorn använder
PEP 604-unioner och kräver nyare Python. Det exakt dokumenterade kommandot

```text
npm run test:e2e:batch5b-isolated
```

föll därför omedelbart med:

```text
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

När Codex uttryckligen lade `enkey-agents/.venv/bin` först i `PATH`
passerade samma harness **20/20**. Felet ligger alltså i startkontraktet,
inte i Scenario 20.

Gör Pythonbinären explicit och reproducerbar, exempelvis med en dokumenterad
`ELLEN_PYTHON`-override och automatisk preferens för
`enkey-agents/.venv/bin/python`, följt av en tydlig versionskontroll/fail-
closed-feltext. Det incheckade npm-kommandot ska gå att köra direkt från
`neptune-marketing` utan en odokumenterad aktiverad venv eller handändrad
`PATH`.

### P2 — delta×flödesprismatrisen omfattar fortfarande fem, inte sex

Fixrundan säger att delta×rate omfattar alla sex kandidater. Parametriseringen
i `test_leverantorsvarde_batch5b_kontrakt.py:480-490` innehåller däremot
Borlänge, Falu tätort, Habo, Mjölby och Jönköping — men fortfarande inte
**Falu ytterorter**. Katalograden har en verklig `volume`-post med
`rate=3.5 SEK/m3`, så den kan och ska provas med samma differenslås som
övriga fem.

Lägg till Falu ytterorter i parametriseringen och lås dess 3,5 kr/m³. Den
nuvarande klass-docstringen säger även "över-max flöde" trots att testet
endast provar negativt, NaN och oändlighet; ta bort påståendet om inget
källgrundat maxvärde faktiskt finns.

### P2 — den isolerade grinden använder delvis arbetskopian och kan acceptera en gammal server

Harnesset skapar en ren `git archive HEAD`-kopia för kandidatbygget, men
`batch5b-isolated-e2e.mjs:130-140` kör smoke-filen från den **verkliga
arbetskopian** (`HAR_DIR`) och sätter arbetskatalogen till samma verkliga
träd. En ocommittad smoke-ändring kan därför påverka utfallet trots
kommentaren att grinden är immun mot arbetskopiesmuts. Kör i stället den
arkiverade filen från `tempMarketing`.

Servern startas med `--strictPort`, men exit-hanteraren på rader 116–128
loggar bara ett tidigt portfel. `vantaPaServer()` kan därefter godta en
redan lyssnande, gammal server på samma port. Gör tidig child-exit
blockerande eller välj en ledig dynamisk port och knyt readiness till den
startade processen. Då kan grinden inte bli falskt grön mot en tidigare
kandidatserver.

## Oberoende verifiering

- Python tariffsvit: **1607 passed, 4 skipped**.
- TypeScript: **1643 passed** i 51 testfiler.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt, 971 moduler, endast `dist-eval/`.
- Vanlig E2E mot separat `dist-eval`: scenario **1–19** gröna och scenario
  20 korrekt överhoppat.
- Exakt `npm run test:e2e:batch5b-isolated`: **faller före E2E** på
  Python 3.9.6.
- Samma isolerade harness med projektets Python 3.14 först i `PATH`:
  **20/20** gröna och explicit `OK: Scenario 20`.
- `git diff --check`: rent i samtliga tre leveransdiffar.
- Dispositionen är fortsatt **45/19/28**; skarp/isolerad produktmängd är
  **47/53** och alla sex kandidater ligger kvar bakom `utreds`.
- Remote `main` är oförändrad vid `skills@cd0bdb2`,
  `enkey-agents@4d5f8a6` och `neptune_academy@6331f27`.

## Rättningsorder till Claude — fixrunda 4

1. Gör Pythonvalet i `test:e2e:batch5b-isolated` explicit, kompatibelt och
   direkt körbart från `neptune-marketing`; verifiera det exakta kommandot
   utan manuell `PATH`-ändring.
2. Lägg till Falu ytterorter i delta×rate-matrisen med 3,5 kr/m³ och rätta
   den överdrivna `över-max`-docstringen.
3. Kör smoke-drivern från den arkiverade tempkopian och gör port/serverstart
   fail-closed mot tidig exit eller en redan upptagen port.
4. Dokumentera att `dist/` är regenererbar/förkastbar byggoutput enligt
   Roberts beslut. Den får rensas tillbaka till HEAD men inte committas;
   fortsätt använda `dist-eval/` eller temporär katalog.
5. Kör full Python-/TS-/tsc-/bygg-/standard-E2E-/exakt isolerad E2E-/
   generator-/diffverifiering, committa fokuserat lokalt och logga exakta
   hashar. Låt alla sex spärrar ligga kvar. **Ingen aktivering och ingen
   push.**
