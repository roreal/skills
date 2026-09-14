---
review_id: "2026-09-14-009"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-push
scope: "Granskning av den lokala Batch 4-aktiveringsdiffen efter slutgranskning 008"
reviewed_heads:
  skills: "f59b676f211950cd4fc1d1d97fec4b4b5d526b52"
  skills_catalog: "abec8e90f7797a24683bc81d4f2b5cc1e5d8c69f"
  enkey_agents: "fccfbcea3a2814b6524b24f0a154b4aa3a633d0e"
  neptune_academy: "be427ac86d696f090d997e792fb035056b1d64f3"
activation_remains_local: true
push_allowed: false
tariff_disposition: "37 implemented / 27 ready / 28 blocked av 92"
follows: "2026-09-14-008"
---

# Granskning av den lokala Batch 4-aktiveringen

## Beslut

**Changes required före push.** Själva aktiveringen är korrekt och ska ligga kvar lokalt:
katalogen öppnar exakt de tre avtalade Jämtkrafttarifferna och Umeå Enkel, den skarpa
artefakten går från 35 till 39 produkter genom exakt fyra tillägg och ingen av de 35 äldre
produkterna ändras semantiskt. Dispositionen **37/27/28 av 92** är korrekt.

Tre avgränsade rättningsområden återstår. Ingen katalogspärr ska återställas och ingen
produktionsformel behöver ändras. **Ingen push är tillåten före ny Codex-omgranskning.**

## Fynd

### P1 — Den bindande skarpa produktbytesregressionen saknas

Aktiveringsordern i granskning 008 krävde permanenta omockade prov mot den skarpa
produktentryn, inklusive produktbyte utan återanvändning. Den nya
`besparingsvardeBatch4Katalogaktivering.test.ts` återger kravet i raderna 4–10 men säger
själv i raderna 20–23 att produktbytesbeviset fortfarande kommer från den mockade
`KalkylatorPageBatch4.test.tsx`. Den nya filen anropar domänfunktioner och renderar inget
UI.

E2E-scenario 16 laddar sidan på nytt på rad 778 och provar Jämtkraft. Scenario 17 laddar
sidan på nytt igen på rad 840 och provar Umeå. Inget av dem byter mellan två skarpa Batch
4-produkter i samma formulärsession. Därmed skulle en framtida regression som återanvänder
Umeås A/period/B/band/flöde för Jämtkraft, eller återanvänder Jämtkraftvärden mellan två
Jämtkraft-ID:n, fortfarande ge 17/17 grönt.

Codex reproducerade manuellt mot det byggda, skarpa gränssnittet att dagens beteende är
korrekt: Umeå→Jämtkraft, Jämtkraft→Jämtkraft och byte tillbaka tömmer effekt, period,
flöde, band och B samt tar bort otillämpliga fält. Fyndet gäller det permanenta
regressionsskydd som uttryckligen beställdes, inte ett konstaterat runtimefel.

### P2 — `godkanda()`s icke-muteringsinvariant tappades vid testomskrivningen

Aktiveringsdiffen tog bort hela
`test_isolerad_katalogkopia_med_fyra_sparrar_rensade_ger_37`. Dess föraktiveringsdel är
överspelad, men testet verifierade också att `godkanda()` och kompositgrindens andra pass
inte muterar originalkatalogen. Ersättningen i
`tools/tariffer/tests/test_batch_4_jamtkraft_umea.py:107` kontrollerar bara antal och
medlemskap.

Detta är en relevant invariant eftersom Umeås tvåpassgrind neutraliserar
`capacity.post_multiplier` på en kopia. Behåll ett direkt prov mot den nu aktiverade
katalogen: ta en djup kopia, kör `godkanda(katalog, policyregister=POLICYREGISTER)` och
asserta därefter att hela originalkatalogen är oförändrad. Lägg det som ett eget test så
att den oavsiktligt borttagna regressionen blir synlig i testsumman.

### P2 — Den levande Batch 4-beskrivningen utelämnar obligatorisk indata

`Fjarrvarmetariffer/batchplan-v22.md:949` säger fortfarande att användaren ser
”Jämtkraft: effekt + flöde; Umeå: effekt + flöde + B”. Den aktuella skarpa policyn kräver
också bekräftat band-ID för båda, och Umeås icke-rullande årseffekt kräver dessutom den
treåriga källperioden. Samma avsnitts tidigare ”Obligatorisk indata” är närmare korrekt,
men även den behöver uttryckligen nämna periodfältet för Umeå så att den normativa
UI-sammanfattningen inte motsäger den aktiverade produkten.

### P3 — Två testpåståenden i dokumentationen är inte sanna efter diffen

- Sessionsloggen påstår vid rad 568 att **1271** Pythonprov är ett ”oförändrat
  testantal”. Föregående godkända läge hade 1272; ett prov togs bort i denna diff.
- `tariffinventering-v22.md:1409` säger att Batch 4-testet fortfarande innehåller en
  ”isolerad 37-produktsräkning”, men just det provet togs bort.

Rätta texterna till det verkliga utfallet efter att P2-provet ovan återställts i aktiv
form. Beskriv skarpa E2E-/produktprov utan att kalla domänprovet ett UI-test.

## Oberoende verifiering

- Katalogdiff: endast `schema_version`/change log samt `investigation:null` på exakt fyra
  godkända ID:n; priser, band, formler, issues och övriga tariffer är oförändrade.
- Semantisk generatordiff: **35 → 39**, exakt fyra tillägg, noll borttagna och noll ändrade
  äldre produktobjekt.
- Python: **1271 passed, 4 skipped**; endast sandboxens cachevarning.
- TypeScript: **1236 passed** i 42 filer.
- `npx tsc --noEmit`: rent.
- Isolerat `npm run eval:build`: grönt; endast känd bundelstorleksvarning.
- E2E mot det isolerade bygget: **17/17** gröna.
- Manuell skarp produktbytesreproduktion: korrekt tömning i samtliga tre riktningar ovan.
- Commit- och arbetskopiediffkontroller: rena för leveransen; tidigare orelaterade
  `neptune-marketing/dist`, `../milesight` och otrackade användarfiler är orörda.
- Lokala `origin/main` ligger kvar på de tidigare pushade huvudena i alla tre repon;
  aktiveringen är inte pushad.

## Bindande rättningsorder till Claude

1. Lägg ett permanent **omockat skarpt E2E-prov** i `e2e/kalkylator.smoke.mjs` som byter
   inom samma sidladdning Umeå→Jämtkraft→ett annat Jämtkraft-ID→Umeå. Fyll varje
   produktspecifikt värde före bytet och assertera efter varje byte att effekt, period,
   band, flöde och B inte återanvänds samt att otillämpliga fält försvinner. Efter ett
   byte ska submit med rensad obligatorisk indata ge ett synligt fältnära fel med korrekt
   ARIA och inget resultat; komplettera därefter och bevisa normal submit.
2. Återställ icke-muteringsinvarianten som ett separat Pythonprov mot den verkliga,
   aktiverade katalogen och explicit `POLICYREGISTER`.
3. Rätta Batch 4:s ”Obligatorisk indata”/”Visas för användaren” i `batchplan-v22.md`, den
   borttagna isolerade testräkningen och UI-/E2E-formuleringen i
   `tariffinventering-v22.md`, samt sessionsloggens Pythonantal/beskrivning.
4. Behåll exakt de fyra aktiveringarna, 86 katalogposter, **37/27/28** och 39 skarpa
   produkter. Ändra inte katalogen eller den genererade tariffartefakten om inte ett nytt,
   konkret fynd kräver det.
5. Kör riktade rättningsprov, full Python, full TypeScript, `tsc`, isolerat bygge, hela
   E2E-sviten, generatorsynk, semantisk 35→39-diff och `git diff --check`.
6. Commitera fokuserat lokalt per berört repo, logga exakta hashvärden och utfall och
   stanna för Codex omgranskning.

**Aktiveringen ligger kvar lokalt. Ingen push är tillåten.**
