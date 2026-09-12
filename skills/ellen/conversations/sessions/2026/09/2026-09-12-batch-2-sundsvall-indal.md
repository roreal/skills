---
session_id: "2026-09-12-001"
date: "2026-09-12"
participants: [Robert, Codex, Claude]
status: "changes required i rättningsrunda 1 före aktivering"
topic: "Batch 2: Sundsvall Energi — Indal, Liden och Lucksta"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-12-batch-2-sundsvall-indal.md"
  - "conversations/reviews/2026/09/2026-09-12-beredskapskontroll-batch-2.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 2"
---

# Session: Batch 2 — Sundsvall Energi Indal, Liden och Lucksta

## Uppdrag

Robert gav explicit klartecken ("Batch 2 är startklar för lokal implementation")
för att starta implementationen enligt Codex auktoritativa handoff
`2026-09-12-001` och beredskapskontroll `2026-09-12-018`. Ingen aktivering och
ingen push i denna etapp — tariffen ligger fortsatt bakom
`investigation.status="utreds"`.

## Implementation

1. **Katalog** (`skills`): satte `capacity: {"type": "not_applicable"}` och
   `contract_required: true` på `sundsvall-energi-indal-liden-och-lucksta-2026`.
   `investigation` ombildad till en ren implementationsspärr
   (`request_ids: []`, ny `conditions_sv`-text) — samma mönster Batch 1 använde
   före sin aktivering. R14 (Sundsvall Energi) fick explicit `tariff_ids` för de
   två fortsatt blockerade tarifferna (Sundsvall normal, Matfors/Kvissleby) i
   stället för sitt tidigare medlemsomfattande `member_ids`. Rättade en
   kvarlämnad, felaktig legacytext i `tariffinventering-v22.md:489–492` som
   motsade den redan styrande, rättade modellen.
2. **Policy** (`enkey-agents`): registrerade en helt fältlös `Tariffpolicy`
   (`kravda_falt=()`, ingen bindning, `tackning={"annual_forward"}`,
   `stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False`).
3. **Tariffscopad informationsförfrågan**: byggde den i V22 beslutade generiska
   funktionen `blockerade_tariff_ider(katalog) -> set[str]` och kopplade den in
   i `grind()`/`godkanda()` i stället för den tidigare medlemsbaserade
   `utredda_medlemmar()`-kopplingen. En request med `tariff_ids` blockerar
   exakt de namngivna tariff-ID:na; en äldre request utan `tariff_ids`
   expanderar sina `member_ids` till medlemmens samtliga tariff-ID:n
   (bakåtkompatibelt, verifierat mot R09/Vattenfall). Fail-closed: ett okänt
   `member_id` eller ett dubblerat request-`id` kastar i stället för att tyst
   bidra med noll blockering.
4. **Verklig bugg upptäckt och rättad** (`neptune_academy`): `beraknaArsprodukt`
   krävde tidigare ovillkorligen `kapacitetKw` (kastade `KontraktBlockerat/
   missing_capacity`) även för en policy helt utan `kapacitetBindning` — ingen
   tidigare kontraktsgated tariff hade saknat kapacitetsdel helt, så gapet
   syntes först nu. Kapacitetskontrollen körs numera bara när
   `policy.kapacitetBindning` faktiskt är satt; `ArsprodukResultat.kapacitetKw`
   är nu valfritt. `KalkylatorPage.tsx`s dedikerade kapacitetsfält
   (`#kapacitetKw`) renderas inte längre för en sådan tariff (det var tidigare
   oavsiktligt `required` trots att fältet saknar motsvarighet i policyn), och
   resultattexten samt den statiska MWh-hjälptexten rättades att inte nämna
   kapacitet/debiterbar effekt när tariffen inte har någon sådan del.
5. **Generator/proveniens**: regenererade `tariffer.generated.ts` med ny
   sha256/commit-proveniens mot `skills@08a8d6a` (katalogfilens bytes ändrades,
   trots att `godkanda()`-utfallet är oförändrat — tariffen är ännu inte
   genererad). Uppdaterade `test_katalog_proveniens.py`s förväntade hash i
   samma commit.

## Verifiering

- **Python**: 718 passed, 4 skipped (700+4 baslinje + 18 nya Batch 2-tester),
  0 failed. `git diff --check` rent.
- **TypeScript**: 942 passed i 31 filer (934 baslinje + 8 nya: 2 golden,
  3 besparingsvarde-buggfix, 3 UI), 0 failed/0 skippade.
- `npx tsc --noEmit`: godkänt.
- `npm run build`: godkänt.
- `npm run test:e2e`: samtliga 9 befintliga scenarier godkända (scenario för
  Sundsvall Indal hör till den senare aktiveringsrunden, eftersom tariffen
  ännu är spärrad i den riktiga katalogen).
- Dispositionen är oförändrad: `godkanda(katalog)` ger fortsatt exakt 15
  tariffer; Sundsvall Indal ingår inte.
- Golden: 100 MWh → 100 800 SEK exkl. moms / 126 000 SEK inkl. moms,
  fast/kapacitet/justering noll — verifierat identiskt i Python och
  TypeScript, genom respektive kontraktsfasad.

## Commits (lokalt, ingen push)

- `skills@08a8d6a` — katalog- och dokumentationsrättning.
- `enkey-agents@a30c876` — policy, tariffscopad grind, testuppdateringar.
- `neptune_academy@ab57d02` — buggfix i `beraknaArsprodukt`, UI-rättningar,
  regenererad `tariffer.generated.ts`, nya tester.

Ingen aktivering, ingen push. Stannar för Codex granskning av hela
implementationen.

## Codex-granskning 2026-09-12-019

Codex verifierade tariffmodellen, goldenfacit, 718+4 skip Python, 942 TypeScript,
ren tsc och fortsatt 15/49/28. Leveransen behöver en avgränsad rättningsrunda innan
aktivering: `blockerade_tariff_ider()` accepterar okända/dubblerade `tariff_ids`
och validerar inte `investigation.request_ids` fullt fail-closed. Ett Pythonprov
som påstår att irrelevant kapacitetsindata inte påverkar kostnaden gör dessutom
bara anropet utan sådan indata, och den incheckade handoffen ger ett
`git diff --check`-fel trots loggens uppgift om ren diff.

Auktoritativ instruktion och reproduktion finns i
`conversations/reviews/2026/09/2026-09-12-granskning-batch-2-implementation.md`.
Ingen tariffmodell eller aktiveringsstatus ska ändras. Ingen push.

## Rättningsrunda 1 — svar på granskning 2026-09-12-019

Alla tre fynd rättade ovanpå de tidigare lokala commits. Ingen tariffmodell,
aktiveringsstatus, prisdata eller disposition ändrad; produktkatalogen
regenererades inte (katalogbytes oförändrade sedan förra rundan).

1. **P1 — `blockerade_tariff_ider()` är nu fullt fail-closed**
   (`enkey-agents/tools/tariffer/katalog.py`). Funktionen validerar nu:
   unika, icke-tomma request-ID:n; exakt en scopeform per request
   (`tariff_ids` XOR `member_ids`, aldrig båda eller ingen); för
   `tariff_ids` — icke-tom lista, unika icke-tomma strängar, varje ID
   måste existera exakt en gång i katalogens tariffer; för `member_ids`
   — samma tomhets-/dubblettvalidering som tidigare bevarad; för varje
   tariffs `investigation.request_ids` — unik referens, requesten måste
   finnas, och dess upplösta omfattning måste faktiskt täcka tariffen som
   bär referensen. Åtta nya negativa test lagts i
   `test_batch_2_sundsvall_indal.py`: okänt/dubblerat `tariff_ids`, båda
   scopeformerna samtidigt, ingen scopeform, tom `tariff_ids`-lista,
   okänt/dubblerat `investigation.request_ids`, samt en referens utanför
   requestens upplösta omfattning. Den riktiga katalogen och R14 validerar
   fortsatt rent (ingen falsk positiv mot legitim data).
2. **P2 — kapacitetsindata-provet jämför nu faktiskt två anrop.**
   `test_ingen_kapacitetsindata_behovs_eller_paverkar_kostnaden` gör ett
   riktigt `res_med`-anrop med ett irrelevant `kapacitet_kw`-fält
   (`IndataPost`) och jämför kostnad/status mot `res_utan`, i stället för
   att bara beräkna och kontrollera `res_utan` ensamt. Goldenprovet i
   samma fil samt `resultatkontrakt.batch2.test.ts` och
   `besparingsvardeBatch2.test.ts` (`neptune_academy`) stärktes till
   uttrycklig `omfattning`/`noggrannhet`/`fullstandighet`-paritet
   respektive en explicit jämförelse mot anropet utan `kapacitetKw`.
3. **P2 — whitespacefelet i handoffen.** Den incheckade Batch 2-handoffen
   (`skills@fa68890`) hade en extra tomrad vid EOF; `git diff --check
   ca99492..fa68890` visade felet. Den nuvarande arbetskopian av handoffen
   (efter Codex egen uppdatering till `status: changes-required-fix-1`)
   har redan korrekt radslut utan tomrad vid EOF — verifierat med
   `git diff --check` mot arbetskopian innan denna commit (rent, ingen
   utskrift). Ingen ytterligare ändring behövdes i den filen utöver att
   committa Codex redan gjorda uppdatering tillsammans med denna rättning.

### Verifiering

- **Python** (`enkey-agents`): `python3 -m pytest tools/tariffer/` →
  **726 passed, 4 skipped** (718+4 baslinje + 8 nya negativa test), 0
  failed.
- **TypeScript** (`neptune_academy`): `npx vitest run` → **942 passed**
  i 31 filer (oförändrat antal — befintliga `it`-block stärktes med fler
  assertions, inga nya block), 0 failed/0 skippade.
- `npx tsc --noEmit`: godkänt, ingen utskrift.
- `git diff --check a30c876..d81831a` (enkey-agents): rent, exit 0.
- `git diff --check ab57d02..fbc925f` (neptune_academy): rent, exit 0.
- Dispositionen mekaniskt verifierad: `godkanda(katalog)` ger exakt **15**
  tariffer; `sundsvall-energi-indal-liden-och-lucksta-2026` ingår inte.
- Katalogfilen `optimate-fjarrvarme-2026.json` oförändrad (`git status
  --porcelain` rent för filen); ingen regenerering av produktkatalogen.

### Commits (lokalt, ingen push)

- `enkey-agents@d81831a` — fail-closed requestgrind, åtta nya negativa
  test, stärkt kapacitetsindata-jämförelse.
- `neptune_academy@fbc925f` — stärkt statusparitet i golden- och
  kapacitets-ignoreringsproven.
- `skills` — denna sessionslogg-uppdatering, tillsammans med Codex egna
  uppdateringar av handoff (`status: changes-required-fix-1`), index.md
  och den nya granskningsfilen `2026-09-12-019`.

Ingen aktivering, ingen push. Stannar för Codex omgranskning.
