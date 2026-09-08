---
review_id: "2026-09-06-002"
date: "2026-09-06"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit 0c5c81e
  - neptune_academy commit f4f04f6
  - rättningar efter granskning 2026-09-06-001
reviewed_heads:
  enkey-agents: "0c5c81e"
  neptune_academy: "f4f04f6"
implementation_changed: false
push_status: local-unpushed-not-approved
---

# Omgranskning av Stockholm Exergis månadsvisa resultatkontrakt

## Bedömning

Rättningarna stänger de två konkreta P1-reproduktionerna från granskning
`2026-09-06-001`: saknade kallenergi-/returtemperaturbindningar stoppas nu mot tariffens
struktur, och kapacitetens giltighetsintervall måste täcka hela målmånaden. TypeScripts
dubblettkontroll, de nya allow-list-testerna och dokumentationsrättningarna fungerar också.
Samtliga 342 Python- och 358 TypeScript-tester, typkontrollen, produktionsbygget och
diffkontrollerna passerar.

Kontrollpunkten behåller ändå **`changes-required` före push** på ett enda närliggande
P1-fynd. Den generiska bindningsregeln kontrollerar fortfarande bara
`returtemperatur_bindning` mot fältets `tillampliga_manader`. Samma kontroll saknas för
kapacitet och kall energi, trots att det ursprungliga villkoret kräver att alla tre
bindningarna är relevanta och obligatoriska för den aktuella månaden.

## Fynd

### P1 — kapacitets- och kallenergibindningar kan vara otillämpliga för målmånaden

Den nya korskontrollen verifierar korrekt att `energi.tillagg` har en
`kallenergi_bindning`, men inte att bindningens `KravPost.tillampliga_manader` omfattar
målmånaden. Den generella loopen kontrollerar bara `"monthly" in kravs_for`
(`resultatkontrakt.py:666–716`, `resultatkontrakt.ts:634–681`).

Codex reproducerade därför följande för januari 2026:

1. Behåll `kallenergi_bindning`, men ändra dess policyfält till
   `tillampliga_manader={2}` och utelämna januari månads kallenergi.
2. Fasaden klassar då bort fältet som irrelevant i statuskontrollen.
3. Resultatet blir ändå `monthly/exact/complete`; motorn får standardvärdet noll.
4. Energikostnaden blir 64 608,486 kr i stället för 65 580,451 kr.

Motsvarande felkonfiguration för `kapacitet_bindning` passerar också statuskontrollen. Om
kapacitetsposten utelämnas kraschar Python därefter med rå
`KeyError('debiterbar_effekt_kw')`; TypeScript försöker på motsvarande sätt läsa
`giltigFran` från en saknad post (`resultatkontrakt.py:718–751`,
`resultatkontrakt.ts:683–709`).

Detta bryter fortfarande mot villkor 2 i `2026-09-05-003`: ett kallenergitillägg kräver
ett explicit verifierat värde varje månad, även när värdet är noll, och varje deklarerad
bindning måste peka på ett policyfält som verkligen är relevant för månadens
beräkningsändamål. En rå `KeyError`/`TypeError` efter en intern `complete`-status är inte en
godkänd fail-closed-gräns.

**Begärd rättning:** centralisera bindningskontrollen i båda språken så att varje
strukturmässigt nödvändig bindning kontrolleras mot:

- att bindningen finns;
- att dess `KravPost` gäller `monthly`;
- att `tillampliga_manader` är `None`/`undefined` eller innehåller målmånaden.

Applicera detta på kapacitet och kall energi varje månad när motsvarande tariffstruktur
finns, och på returtemperatur när månaden ingår i tariffens returtemperaturpost. Kör denna
kontroll före statusen och före varje indexering av indata. Lägg speglade negativtester för
en befintlig kallenergi- respektive kapacitetsbindning vars policyfält inte omfattar
målmånaden; inget fall får ge kostnad eller rå nyckel-/typkrasch.

### P2 — `enforced`-spärren fungerar men saknar den begärda regressionen

De nya allow-list-testerna täcker felskrivning och fel datatyper, och koden avvisar också
`enforced` för Stockholm Exergis endast-`monthly_invoice`-policy. Codex verifierade det
direkt: grinden kastar eftersom `annual_forward` och `annual_inverse` saknas. Det
uttryckliga regressionstestet som beställdes i granskning 001 lades dock inte till.

**Begärd rättning:** lägg ett litet test som anropar leverantörsfilsgrinden med Stockholm
Exergi och `enforced`, förväntar fel på saknad års-/inverstäckning och fortsatt bevisar att
`validated` aldrig skapar `_kraver_kontrakt`.

## Bekräftat rättat

- Saknad `kallenergi_bindning` stoppas när tariffen har `energi.tillagg`.
- Saknad `returtemperatur_bindning` stoppas under tariffens tillämpliga månader.
- Returtemperaturfältets egen månadstillämplighet korskontrolleras mot tariffen.
- Kapacitet utan giltighetsintervall, med endagsintervall eller med delvis månadstäckning
  blockeras.
- Exakt månadstäckning och skottårets februari fungerar i båda språken.
- TypeScript avvisar dubblerade `tillampligaManader`.
- Leverantörsfilsgrinden avvisar felstavat läge, `None`, tal, lista och objekt.
- Modulkommentarerna beskriver nu `tackning`, tre bindningar, månadsfasaden och
  `validated`-piloten.
- Ingen `enforced`-aktivering, global kontraktsmarkör, produktväg eller annan tariff har
  ändrats.

## Sista avgränsade rättningsbeställning till Claude

1. Gör månadstillämplighetskontrollen gemensam för alla tre strukturkrävda bindningar.
2. Lägg två speglade negativtester: otillämplig kallenergi- och kapacitetsbindning.
3. Lägg regressionstestet för att dagens Stockholm-policy avvisar `enforced`.
4. Kör tariffsviten, Vitest, `tsc --noEmit`, produktionsbygget och `git diff --check`.
5. Skapa fokuserade lokala rättningscommits och stanna för slutomgranskning.

Ändra ingen tariffdata, produktväg, `validated`-status eller enforcementmarkör och pusha
inte före nästa Codex-kontroll.

## Utförda kontroller

- `enkey-agents@0c5c81e`: 342/342 tester under `tools/tariffer/tests` passerar.
- `neptune_academy@f4f04f6`: 358/358 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda rättningscommitterna.
- Båda implementationsarbetskopiorna är rena och fortfarande opushade.
- Codex reproducerade falskt `exact/complete` och fel energikostnad när
  kallenergibindningens policyfält inte omfattar målmånaden samt en rå `KeyError` för
  motsvarande kapacitetsfall.
- Codex verifierade separat att grinden redan avvisar `enforced` för dagens
  Stockholm-policy; endast regressionstestet saknas.

Codex ändrade ingen implementation, tariffdata, commit eller push under omgranskningen.
