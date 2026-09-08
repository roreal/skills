---
review_id: "2026-09-06-003"
date: "2026-09-06"
reviewer: Codex
status: approved
scope:
  - enkey-agents commits 670efa7, 0c5c81e och 2dd62a2
  - neptune_academy commits 68543a4, f4f04f6 och e64c3de
  - Stockholm Exergi validated månadsvis resultatkontrakt
reviewed_heads:
  enkey-agents: "2dd62a2"
  neptune_academy: "e64c3de"
implementation_changed: false
push_status: approved-for-push
---

# Slutgodkännande av Stockholm Exergis månadsvisa resultatkontrakt

## Bedömning

**Kontrollpunkten är godkänd för push.** Claudes sista rättningar stänger det kvarstående
P1-fyndet i granskning `2026-09-06-002`: kapacitets-, kallenergi- och
returtemperaturbindningarna går nu genom samma fail-closed-kontroll före statusberäkning
och före indexering av indata. När tariffstrukturen kräver en post måste bindningen finnas,
gälla månadsomfattningen och omfatta målmånaden enligt sitt eget
`tillampliga_manader`/`tillampligaManader`.

Det saknade regressionstestet för aktiveringsgrinden finns också. Dagens Stockholm-policy,
som bara täcker `monthly_invoice`, avvisar `enforced`; läget `validated` sätter fortfarande
inte `_kraver_kontrakt`.

Inga nya blockerande eller övriga kodfynd återstår inom den godkända avgränsningen.

## Bekräftade egenskaper

- Samma bindningsregel används i Python och TypeScript för kapacitet, kall energi och
  returtemperatur.
- En strukturmässigt nödvändig bindning som saknas stoppas med ett tydligt domänfel.
- En kapacitets- eller kallenergibindning vars policyfält inte omfattar målmånaden stoppas
  före status och före motoranrop; inget falskt `exact/complete`, ingen felaktig kostnad och
  ingen rå `KeyError`/`TypeError` återstår i de reproducerade fallen.
- Kapacitetspostens giltighetsintervall måste fortsatt täcka hela kalendermånaden,
  inklusive skottårsdag.
- Tolv Åkermannen-rader återspelas månadsvis genom kontraktsfasaden och jämförs med den
  befintliga direkta månadsvägen.
- `off`/`validated`/`enforced` är fortsatt en strikt allow-list; felstavningar och fel typer
  avvisas.
- `enforced` för Stockholm Exergi är uttryckligen spärrat eftersom årsprognos och invers
  saknar kontraktstäckning.
- Ingen global kontraktsmarkör, produktväg eller annan tariff aktiveras av dessa commits.

## Utförda kontroller

- `enkey-agents@2dd62a2`: 345/345 tester under `tools/tariffer/tests` passerar.
- `neptune_academy@e64c3de`: 360/360 Vitest passerar.
- `npx tsc --noEmit`: passerar utan fel.
- `npm run build`: passerar; endast den sedan tidigare kända varningen om stor bundle.
- `git diff --check`: rent i båda implementationsrepona.
- Båda arbetskopiorna är rena efter kontrollen.
- `enkey-agents` är tre commits före `origin/main`.
- `neptune_academy` är tre commits före `origin/main`; lokal `main` spårar fortsatt
  `upstream/main` och visas därför som 38 commits före den remoten.

Pytest gav en lokal varning om att sandboxen inte kunde skriva `.pytest_cache`; alla 345
tester kördes och passerade, så varningen påverkar inte bedömningen.

## Godkännandets gräns

Godkännandet omfattar hela den lokala trecommitskedjan för Stockholm Exergis
**`validated` månadsvisa fakturaåterspelning**:

- `enkey-agents`: `670efa7`, `0c5c81e`, `2dd62a2`;
- `neptune_academy`: `68543a4`, `f4f04f6`, `e64c3de`.

Det är inte ett godkännande av `enforced`, kalkylatorns framåtriktade årsprognos,
kronor-till-MWh-inversen, UI-ändringar eller aktivering av andra bolag och tariffer. Varje
sådan utvidgning kräver en ny avgränsad specifikation och kontrollpunkt.

## Nästa steg

Robert kan nu be Claude att pusha exakt de granskade HEAD-versionerna till `origin/main` i
båda implementationsrepona. Efter push bör remote-heads verifieras mot `2dd62a2` respektive
`e64c3de`. Ingen push utfördes av Codex under granskningen.
