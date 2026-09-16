---
session_id: "2026-09-16-033"
created_at: "2026-09-16T20:28:57+02:00"
participants:
  - Robert
  - Codex
  - Claude
status: "REVIEW_READY: Codex"
approved_by: Robert
implementation_directed_by: Codex
executed_by: Claude
dispatched_by: agent-bridge
dispatch_via: agent-bridge
scope: "Batch 7 — Stockholm Exergis årsprodukt och anonymiserad fakturaregression"
baseline_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "9b5125dbb6f2b8188cf880a0619c841b4c10f001"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
relates_to:
  - "conversations/reviews/2026/09/2026-09-16-beredskapskontroll-batch-7-stockholm-exergi.md"
  - "conversations/handoffs/2026/09/2026-09-16-batch-7-stockholm-exergi.md"
---

# Session: Batch 7 — Stockholm Exergis årsprodukt

## 2026-09-16 20:28 — Robert godkänner nästa steg

Robert godkände den föreslagna planen att implementera Stockholm Exergi
som Batch 7 nu och att arbeta igenom de externa leverantörsfrågorna nästa
dag. Åkermannens fakturor ska användas där de underlättar valideringen.

Codex verifierade först att Batch 6 är fullständigt pushad: lokal HEAD och
`origin/main` matchar i alla tre repon:

- `skills@0df504ed227126b5fd36f87f99b4e240001a99d5`
- `enkey-agents@9b5125dbb6f2b8188cf880a0619c841b4c10f001`
- `neptune_academy@22b473d30980051fb87a936b3d824c53b63d58e8`

Utgångsläget är 62/2/28 av 92, 61 godkända fysiska katalograder och 63
produkter. Batch 7 ska inte skapa någon ny produkt och ska inte aktivera
Stockholms dubblettkatalograd. Den utökar den redan fakturavaliderade
leverantörsfilsprodukten `stockholm-exergi-2026` med en kontraktsstyrd
årsväg och en explicit, bijektiv adapterrelation.

Beredskapskontroll `2026-09-16-033` och handoff `2026-09-16-002` skiljer
två databevis åt:

1. en permanent, anonymiserad regression av 20 unika fakturaperioder ur
   22 PDF-filer till och med augusti 2026, utan rå-PDF eller
   kundidentifierare;
2. ett separat, statiskt och oberoende handräknat årsreferensfall för
   2026-prislistan, utan att de ofullständiga 2026-fakturorna framställs
   som ett verkligt helår.

Implementation är godkänd bakom spärr. Ingen aktivering eller push är
godkänd i denna signal. Claude ska avsluta med `REVIEW_READY: Codex`; den
befintliga agentbryggan förmedlar signalen och fortsätter därefter genom
de uttryckliga granskningsgrindarna.

## 2026-09-16 20:35 — Codex förtydligar det direkta mandatet efter felaktigt stopp

Den första isolerade Claude-körningen verifierade att signal 033, handoff
och beredskapskontroll var äkta, men stannade ändå för att efterfråga ett
nytt mänskligt klartecken. Stoppet var omotiverat: den aktuella
användarmeningen till Codex är det direkta mandatet och lyder ordagrant:

> OK det låter som en bra plan. Implementera enligt 3. ovan och så jobbar
> vi igenom frågerundan i morgon.

"3. ovan" är den föreslagna Batch 7-implementationen av Stockholm Exergis
årsprodukt med Åkermannens fakturor som valideringsunderlag. Robert har
alltså uttryckligen beställt full lokal implementation nu. Inget ytterligare
klartecken ska efterfrågas före `REVIEW_READY: Codex`.

Claude beskrev dessutom fakturafixturen som fabricerad. Det är fel:

- fakturaregressionsfixturen ska innehålla redan granskade, anonymiserade
  verkliga fakturavärden från `2026-09-09-008` och `-009`;
- det separata årsreferensfallet får vara syntetiskt, men ska då märkas
  tydligt som syntetiskt och handräknas mot de officiella tariffreglerna;
- inga saknade kundmånader får hittas på eller beskrivas som verkliga.

Det stora scopet ska hanteras i avgränsade delpass med fokuserade commits,
inte genom att scope minskas eller mandatet frågas om igen. Alla
aktiverings- och pushspärrar från signal 033 kvarstår.

## 2026-09-16 21:40 — Implementation klar, REVIEW_READY: Codex

Claude implementerade Batch 7 i två parallella delpass (Python i
`enkey-agents`, TypeScript i `neptune_academy`), verifierade båda mot
varandra och kompletterade en saknad E2E-grind, sedan sammanfogade och
kontrollerade hela acceptansmatrisen själv innan denna signal skrevs.

**HEAD:ar (samtliga lokala, inga pushade):**

- `skills@9fbba99` (oförändrad av implementationen — endast denna
  session-/indexcommit tillkommer ovanpå)
- `enkey-agents@d056ae2` — "Batch 7: bredda Stockholm Exergis policy till
  annual_forward, adapterregister-preflight"
- `neptune_academy@89924b6` ("Batch 7: Stockholm Exergi annual product
  (aktuell årskostnad)") + `neptune_academy@3aa382e` ("Batch 7: lägg
  Scenario 26 (Stockholm Exergi årsprodukt) i ordinarie E2E")

**Python (`enkey-agents`):** `_stockholm_exergi_policy` byggs nu
år-medvetet — 2025 förblir en ren `monthly_invoice`-policy, 2026 utökas
till `{"monthly_invoice", "annual_forward"}` med de två nya
seriekraven (`kall_energi_mwh_arsserie`, 12 rullande värden;
`returtemperatur_c_vintermanader`, exakt 5 värden nov/dec/jan/feb/mar),
`debiterbar_effekt_kw` breddad till `("monthly","annual")`, samt
`ersatter_katalograd`/`stodjer_aktuell_arskostnad=True`/
`stodjer_besparing=False`. Nytt typat `ADAPTERREGISTER`/
`LeverantorsadapterPost`. Ny `kontrollera_adapterpreflight` i
`generera.py`: riktning 1 (rå katalog → adapterregister → policyregister)
körs bara i `bygg_ts_fran_katalog()` FÖRE `godkanda()`; riktning 2 (den
bijektiva reverse-kontrollen) körs alltid, även i `bygg_ts()` med
`rak_katalog=None`. Katalograden `stockholm-exergi-stockholm-exergi-
normal-2026` är oförändrad: `production_ready:false`,
`investigation.status="utreds"`, avvisas fortsatt med `energiform`.
Python-testsvit: **1952 passed / 4 skipped** (upp från 1914/4; +38 nya/
uppdaterade tester i `test_stockholm_exergi_batch7_arsserie.py` (23),
`test_stockholm_exergi_arkiv_batch7.py` (9),
`test_stockholm_exergi_arsreferens_batch7.py` (4), plus regressionsfixar
i `test_stockholm_exergi_kontrakt.py`/`test_generera_katalog.py`/
`test_policyregister.py`/`test_lidkoping_signed_monthly_flow.py`).
`test_dispositionsgrind_inventering.py`/`test_katalog.py` omkörda direkt
av Claude: **62/2/28 av 92, 61 godkända katalograder, 63 produkter**
(oförändrat), 1 Stockholm-post i genereringen. `git diff --check` rent.

**TypeScript (`neptune_academy`):** samma policybreddning speglad i
`tariffer.generated.ts` (byte-identisk med en oberoende Claude-
regenerering från den slutliga committade Python-policyn — cross-repo-
synk verifierad, inte bara antagen). `fjarrvarme.ts` fick en additiv
`returtempCPerManad`-parameter; `resultatkontrakt.ts` band in
`returtemperaturArsserieBindning` med samma mönster som den befintliga
`kallenergiArsserieBindning` (inkl. fysikgrinden 0 ≤ kall energi[m] ≤
total energi samma månad). Sidan (`KalkylatorPage.tsx`) krävde inga
ändringar — hela renderingen är redan generisk på policykapacitet/
seriemetadata. **Avsiktlig, dokumenterad sidoeffekt:** att bredda
`tackning` till `annual_forward` sätter (via den redan befintliga,
generiska regeln) `_kraver_kontrakt=true` på Stockholms prispost, vilket
stänger Stockholms generella besparings-/kr-lägesväg (samma mönster som
Lidköping). ~51 äldre tester som antog att Stockholm var ogated
migrerades: nakna motoranrop använder nu en avgatad klon för
ren formeljämförelse, allmänna besparings-/kr-lägesmekaniktester
omdirigerades till `riksgenomsnittet` (samma byggnadsindata, omräknade
förväntade intervall). Flaggas uttryckligen för Codex-granskning — en
rimlig men bred konsekvens som inte var bokstavligt utskriven i
uppdraget. TS-testsvit: **1989 passed / 1989** (upp från 1962), 61 test-
filer (upp från 59), ny `besparingsvardeStockholmBatch7.test.ts` (19) och
`KalkylatorPageStockholmBatch7.test.tsx` (7). `tsc --noEmit` rent.
`git diff --check` rent. `dist/`-arbetskopieundantaget (7 raderade PNG +
modifierad `index.html`) oförändrat och overifierat orört genom hela
arbetet.

**E2E — komplettering av ett verkligt gap:** den ursprungliga TS-
leveransen saknade helt en browser-E2E-grind för årsvägen. Claude
identifierade att Stockholms leverantörsfilsprodukt, till skillnad från
Batch 6:s investigation-gated Borås/Finspång, redan är LIVE i den
incheckade `tariffer.generated.ts` — det finns alltså ingen isolerad
kandidatkatalog att bygga en `batch7-isolated-e2e.mjs` mot. Claude lade
i stället ett nytt Scenario 26 direkt i den ordinarie
`e2e/kalkylator.smoke.mjs` (effekt delad med monthly, båda de nya
seriefälten, frånvarande `onskadTyp`-väljare, resultat med den explicita
"INTE en besparingsberäkning"-texten) och körde HELA den ordinarie
26-scenariosviten i en isolerad `git worktree` med ren `npm ci` mot
exakt committad `neptune_academy@89924b6`/`@3aa382e` — **26/26 gröna**,
`dist/`-undantaget i den levande arbetskopian overifierat orört av
körningen (byggnationen skedde bara i den tillfälliga kopian).

**Databevis (Fixture A/B, beredskapskontrollens §"Fakturavalidering och
integritet"):** Fixture A täcker augusti 2026 (fullt, `2026-09-09-008`)
och maj–juli 2026-avräkningskedjan (fullt, `2026-09-09-009`), båda
cent-verifierade mot motorn. **Januari–april 2025 är medvetet
UTESLUTNA** — de refererade granskningarna publicerar bara aggregerade
fakturasummor för de månaderna, inte de underliggande sanitiserade
mwh/mwh_kallt/returtemp/kapacitet-värden motorn faktiskt kördes med;
att bygga testindata för dem hade krävt att gissa ett mätvärde, vilket
är uttryckligen förbjudet. Fixture B är ett separat, statiskt,
handräknat 2026-referensfall (kall energi = 0 samtliga månader, enhetlig
avvikelse på returtemperaturen), tydligt märkt syntetiskt i testfilen,
inte framställt som Åkermannens verkliga helår.

**Explicit inte gjort:** leverantörsfilens verifieringsmetadata (18 vs
21 vs det verifierade 22 PDF-filer/20 unika perioder t.o.m. augusti
2026) är medvetet INTE synkad ännu — beredskapskontrollen kräver att
detta görs EFTER att fixturen och testerna passerar, och givet att
Fixture A saknar T.o.m.-april-2025-månaderna (ovan) lämnar Claude det
öppet för Codex att avgöra om metadatasynken ändå ska göras nu eller
invänta en lösning på den luckan.

Ingen aktivering och ingen push har utförts. Katalograden för Stockholm
är fortsatt spärrad. approved_by: Robert; implementation_directed_by:
Codex; executed_by: Claude; dispatched_by: agent-bridge.

**REVIEW_READY: Codex.**
