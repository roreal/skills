---
session_id: "2026-10-22-013"
signal: "BLOCKED: Codex"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Claude
---

# Optimate våg 3k — blockerad på dist-bevarande (signal 013)

Beslut: `BLOCKED: Codex`. Ingen push, ingen mainflytt, ingen ny
tariffaktivering. Utfört exakt de tre avgränsade punkterna från
`CHANGES_REQUIRED: Claude` (signal 012), se
[granskningsutlåtandet](../../../reviews/2026/10/2026-10-22-aktiveringsgranskning-011-vag-3k.md).

## Kontrollpunkt före arbetet

- Skills HEAD oförändrad: `41e1125cd05f51652c5ee6a64e0c1d686a254255`.
- Neptune-pilot HEAD oförändrad vid start: `e844ed6cb16879a5ddec9cc640463d6c5bbc0cee`.
- Index: `2026-10-22-012` var fortfarande överst och unik; `013` oanvänt.

## Punkt 1 — Bevarandekravet: BLOCKERAT, konkret evidens

`neptune-marketing/dist/` är faktiskt git-spårad (inte endast en bygg-artefakt
— `.gitignore` tillkom efter att filerna redan committades, vilket inte
avspårar dem). Senaste faktiska commit som rör `dist/` är
`5e6b2bed6c52218aa0c223357f92ac350f9dee68` ("Commit for Marketing Docker
Image build", 2026-05-25) — ingen av våg 3k:s commits (3847b4ba…e844ed6c)
har rört `dist/`.

Tidigare utlåtanden (`2026-10-22-slutgranskning-004-optimate-vag-3k.md`,
`2026-10-22-omgranskning-002-optimate-vag-3k.md`,
`2026-10-22-blockergranskning-006-optimate-vag-3k.md`,
`2026-10-22-blockergranskning-008-optimate-vag-3k.md`) bekräftar upprepade
gånger att piloten hade **åtta spårade, ocommittade dist-ändringar** som låg
kvar oförändrade genom hela vågens tidigare körningar (byggen före/efter
jämförda och funna identiska bortsett från dessa åtta filer).

Nuvarande kontroll: `git status --short -- neptune-marketing/dist` i
piloten ger **inget resultat** — arbetskopian är fullständigt ren mot HEAD,
dvs. de åtta tidigare ocommittade filändringarna finns inte längre. De kan
inte återskapas ur git (de var aldrig committade eller stashade), och ingen
backup/patch/snapshot av dem hittades:

- `find` i pilotens arbetskopia och i `/Users/robertrennel/Code/neptune_academy`
  efter `*dist*backup*`, `*dist*.patch`, `*dist*.tar*`, `*dist*.zip`,
  `*dist*snapshot*`: inga träffar.
- `git log --all -- neptune-marketing/dist`: inga commits efter 2026-05-25.
- Ingen stash-post, ingen reflog-post kan återställa en ocommitterad
  arbetskopieändring som redan skrivits över.

**Slutsats:** de åtta filernas tidigare, ocommittade innehåll är sannolikt
oåterkalleligt förlorat genom `git restore --source=HEAD -- dist` i signal
011:s byggsteg. Detta kan inte likställas med bevarande, i linje med
granskningens punkt 1. Inga ytterligare bygg- eller återställningsåtgärder
har vidtagits i detta steg för att inte riskera ytterligare skrivning över
eventuella kvarvarande spår.

### Återstående alternativ (för Codex att väga)

1. Acceptera förlusten som fullbordad: de åtta filerna var sedan 2026-05-25
   ocommitterade byggrester av ett annat syfte (Docker-imagebygget) och inte
   en del av det granskade tariffscopet; fortsätt kedjan utan dem, med denna
   logg som permanent dokumentation av förlusten.
2. Fråga Robert specifikt om han har en lokal kopia (t.ex. en annan
   checkout, ett CI-artefaktlager eller en tidigare Docker-image) som
   innehåller det exakta dist-läget före 2026-10-22 — detta är en konkret,
   avgränsad fråga, inte ett generellt tariffklartecken.
3. Om varken 1 eller 2 godtas: hela vågens aktivering förblir blockerad
   tills frågan är löst.

Denna logg tar inte ställning till vilket alternativ som väljs — det kräver
Codex/Roberts sakbeslut enligt kedjans rollfördelning.

## Punkt 2 — Oberoende beräkningsunderlag: KLART

Nytt, körbart Vitest-engångsprov tillagt och grönt:
`neptune-marketing/src/utils/optimateScenario51.engangsprov.test.ts`
(pilot-commit `881f54f502635f542c6eec984173cc1020eeee1f`, förälder `e844ed6c`,
1 ny fil, inget annat ändrat).

Provet importerar bara den riktiga, oförändrade `fordelaEnergi()`/
`RUMSVARME_ANDEL_PER_MANAD`/`VARMVATTEN_ANDEL` ur `varmeprofil.ts` och
Jönköping Energis riktiga `manadspriser` ur `tariffer.generated.ts`.
Kapacitet (99 300), flödesavgift (3 700) och accessavgift (900) är
hårdkodade LÅSTA literaler (identiska med `optimateScenarioVag3k.test.ts`
rad 56–58, oberoende av månadsserien). Ingen produktionsberäkningsfunktion
(`beraknaOptimateScenario`, `beraknaArsprodukt*`, `arskostnadKapacitet`,
`flodesavgift`, `accessavgift`) anropas för kalkylen själv — bara ren,
handskriven aritmetik, skild från komponentfixturen.

Resultat (verifierat grönt, `npx vitest run
src/utils/optimateScenario51.engangsprov.test.ts`, 2/2 prov):

- `fordelaEnergi(120)` summerar till 120 MWh; andelarna i
  `RUMSVARME_ANDEL_PER_MANAD` summerar till 1; `VARMVATTEN_ANDEL=0,18`.
- energi_före (exkl. moms, hela 120 MWh-serien, oskalad) = **60 208,66176 kr**.
- referens (inkl. moms) = **205 135,8272 kr**.
- besparing vid andel 10/15/20 % = **6 020,866176 / 9 031,299264 /
  12 041,732352 kr** — exakt smoke-testets (`kalkylator.smoke.mjs`,
  Scenario 51) facit.

Viktig precisering mot tidigare kommentartext: referensen (energi_före)
räknas på HELA, oskalade 120 MWh-serien. Den angivna rumsvärmen (96 av
120 MWh) ger andelen 0,8 som bara används i besparingsformeln
(`energiFore × (1 − 0,8 × andel)`) — den skalar INTE själva referensen.
Detta skiljer sig från komponentfixturens 205 290 kr-facit uteslutande
genom den riktiga produktionsschablonens månadsserie (82/18
rumsvärme/varmvatten-vägning × `RUMSVARME_ANDEL_PER_MANAD`) mot
testfilens handplockade litterala serie — inget UI, ingen motor och
inget tariffdata är ändrat.

## Punkt 3 — Daterade protokoll-/rollrättelser: KLART

Daterad rättelse tillagd i
[`2026-10-22-aktivering-010-jonkoping-vag-3k.md`](../../../reviews/2026/10/2026-10-22-aktivering-010-jonkoping-vag-3k.md)
(ändringslogg, äldre text oförändrad, se README punkt 5):

1. Klargör att filen är Claudes leveransunderlag, inte ett Codexutlåtande
   (README punkt 9); framtida leveranser av detta slag går i `sessions/`.
2. Rättar påståendet att `agent-bridge` "committade" signal 010:s loggpost
   — bryggan gör aldrig repoändringar (README punkt 12); det var Claude.
3. Rättar påståendet att ingen skills-implementationscommit gjordes —
   `2853e87983c58b7994b1bb1ff1621bf9bfb6dc72` innehåller själva
   implementationen (generatorkörning mot båda matriserna + pytest).

## Verifiering i detta steg

- `npx vitest run src/utils/optimateScenario51.engangsprov.test.ts`:
  **2/2 gröna** (se ovan). Ingen annan testfil, UI, motor eller tariffdata
  rörd i detta steg — full regressionskörning är inte relevant för en
  avgränsad, append-only loggrättelse/beräkningsunderlag och har inte
  körts om.
- Pilot-status efter arbetet: endast `jonkoping_calc.py` (sedan tidigare
  ospårad, bevarad orörd) kvarstår som avvikelse; `dist` fortsatt rent mot
  HEAD (ingen ytterligare bygg-/återställningsåtgärd har körts).
- Skills-repot: endast denna sessionsfil, denna indexrad och rättelsen i
  granskningsfilen för 011 ändrade/tillagda. Inga orelaterade filer
  (automation/, milesight, Fjarrvarmetariffer-underlag, Enkeys lokala
  ändringar, ordinarie Neptunes ospårade worktrees) rörda.

## Nästa steg

Codex tar sakbeslut om alternativen i punkt 1 ovan (acceptera förlusten,
fråga Robert en avgränsad fråga om en existerande backup, eller hålla
blockeringen). Inom befintligt scope: om Codex accepterar förlusten eller
löser den med en verifierad backup, skriv ny unik
`ACTIVATION_READY: Codex`. Annars kvarstår `BLOCKED: Codex`. Ingen push,
mainflytt eller ny tariffaktivering är tillåten förrän bevarandefrågan är
löst.

approved_by: Codex (signal 2026-10-22-012); dispatched_by: agent-bridge;
executed_by: Claude.
