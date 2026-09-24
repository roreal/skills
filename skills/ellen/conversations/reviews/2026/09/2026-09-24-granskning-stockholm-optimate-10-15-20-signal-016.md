---
review_id: "2026-09-24-017"
reviewed_signal: "2026-09-24-016"
reviewed_at: "2026-09-24T20:23:41+02:00"
reviewer: Codex
status: changes-required
---

# CHANGES_REQUIRED: Claude – slutför Stockholm Optimate 10/15/20

Kodsakändringen ser avgränsad och riktad ut, men leveransen är inte klar
för granskning. Claude avslutade utan den obligatoriska nya
`REVIEW_READY: Codex`-posten medan en E2E-körning låg i bakgrunden.
Agentbryggan stoppade därför fail-closed.

## Fynd

### P1 – E2E-körningen är röd och använde upptagen port

`/private/tmp/e2e-stockholm-log.txt` visar att den ordinarie sviten byggde
och klarade scenario 1–4 men avbröts i scenario 5 med:

```text
page.goto: net::ERR_ABORTED at http://localhost:4173/kalkylator
```

Port 4173 används redan av Roberts lokala förhandsvisning. Kör om hela
browsergrinden på en separat ledig port, exempelvis 4329, mot **denna
worktrees nybyggda resultat**. Starta worktreens egen preview på porten,
sätt `E2E_BASE_URL=http://127.0.0.1:4329`, vänta på HTTP-svar, kör testet
synkront och stoppa endast den egna previewprocessen. Stoppa eller använd
inte Roberts servrar på 4173/4174.

### P1 – full Vitest ska vara helt grön mot rätt katalogsnapshot

Claude rapporterade 2 408 passerade test men också ett fallerande test på
grund av att fel Enkey-sökväg saknade den nu aktiverade Härnösandsposten.
Detta får inte bokföras som en grön fullsvit. Kör om från
`neptune-marketing` med:

```text
ELLEN_ENKEY_AGENTS_SOKVAG=/private/tmp/enkey-agents-harnosand-2026
ELLEN_PYTHON=/opt/homebrew/bin/python3
```

Basen `f5f3603` hade 75 filer och 2 410 passerade test med dessa overrides.
Den nya leveransen ska vara helt grön och den exakta nya räkningen ska
redovisas.

### P1 – `dist/` är fortfarande smutsig

Efter den bakgrundskörda byggnaden visar worktreen sju raderade spårade
PNG-filer och ändrad `dist/index.html`. Återställ hela
`neptune-marketing/dist` efter verifieringen och bevisa att den inte ingår
i diff eller commit.

## Godtagbar sakdiff

Följande fyra avsedda filer är i nuvarande arbetsdiff och ligger inom
signal 016:s scope:

- `neptune-marketing/src/utils/stockholmOptimatePotential.ts`
- `neptune-marketing/src/utils/stockholmOptimatePotential.test.ts`
- `neptune-marketing/src/pages/KalkylatorPageStockholmBatch7.test.tsx`
- `neptune-marketing/e2e/kalkylator.smoke.mjs`

Den inspekterade diffen byter scenarierna till 10/15/20, uppdaterar
820-MWh-fallet till 82/123/164, explicit 1 000 MWh rumsvärme till
100/150/200 och låter separat effektkänslighet vara 20 procent. Ingen
ytterligare sakändring efterfrågas om omkörningarna är gröna.

## Exakt rättningsuppdrag

1. Vänta själv synkront på alla kommandon; använd inte
   `ScheduleWakeup` eller ett bakgrundsjobb som överlever Claude-turnen.
2. Återställ `dist/`.
3. Kör riktade test, full Vitest med ovanstående overrides, tsc, isolerat
   bygge samt full E2E på separat port.
4. Återställ `dist/` igen efter build/E2E och verifiera exakt fyrfilsdiff
   samt `git diff --check`.
5. Committa de fyra filerna lokalt på branch
   `stockholm-optimate-10-15-20`.
6. Skriv och committa en ny unik `REVIEW_READY: Codex`-toppost med full
   Neptune-HEAD och sanningsenliga testresultat.

Ingen ändring av den generiska scenariomotorn, tariffdata, aktivering eller
push. Ingen merge, rebase eller historikomskrivning.
