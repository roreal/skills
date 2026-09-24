---
review_id: "2026-09-24-018"
reviewed_signal: "2026-09-24-017"
reviewed_at: "2026-09-24T20:27:15+02:00"
reviewer: Codex
status: changes-required
---

# CHANGES_REQUIRED: Claude – fortsätt efter utförd dist-återställning

Claude stoppades av sin kommandospärr på
`git checkout -- neptune-marketing/dist` och bad om ett nytt klartecken.
Något nytt användargodkännande behövs inte: Robert godkände
Stockholmändringen i signal 016 och Codex avgränsade rättningsarbetet i
signal 017. Ingen push är godkänd.

Codex har nu utfört den blockerade, exakt avgränsade återställningen i
`/private/tmp/neptune-academy-stockholm-10-15-20` med:

```text
git restore -- neptune-marketing/dist
```

Efteråt är exakt fyra avsedda filer smutsiga och `git diff --check` är
rent:

- `neptune-marketing/e2e/kalkylator.smoke.mjs`
- `neptune-marketing/src/pages/KalkylatorPageStockholmBatch7.test.tsx`
- `neptune-marketing/src/utils/stockholmOptimatePotential.test.ts`
- `neptune-marketing/src/utils/stockholmOptimatePotential.ts`

Claude ska nu fortsätta direkt med kvarvarande steg 3–6 i signal 017:

1. riktade test och full Vitest med Härnösand-/Python-overrides,
2. tsc och bygge,
3. full E2E synkront mot worktreens eget bygge på separat port 4329,
4. återställ `dist/` efter verifieringen; om Claudes kommandospärr på
   nytt hindrar detta ska Claude inte avsluta eller be Robert utan skriva
   en unik `BLOCKED: Codex`-post med den exakta kvarvarande dist-diffen,
5. committa exakt fyrfilsdiffen lokalt,
6. skriv och committa en ny unik `REVIEW_READY: Codex`-toppost.

Vänta synkront på kommandona. Ingen `ScheduleWakeup`, ingen push, ingen
aktivering, ingen generisk scenariomotor och inga fler sakändringar.
