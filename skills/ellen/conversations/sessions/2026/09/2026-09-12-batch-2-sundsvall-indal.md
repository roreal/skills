---
session_id: "2026-09-12-001"
date: "2026-09-12"
participants: [Robert, Codex, Claude]
status: "lokal implementation slutförd, väntar på Codex-granskning"
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
