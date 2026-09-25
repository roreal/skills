---
handoff_id: "2026-09-25-007"
created_at: "2026-09-25T09:29:55+02:00"
from: Codex
to: Claude
status: approved-for-implementation
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_IMPLEMENTATION: Claude – Optimate våg 1, ren energi

## Mandat och avgränsning

Robert har godkänt hela utrullningsplanens steg 1–5. Portföljgrunden är
nu slutgranskad i signal 006. Implementera nästa lokala kontrollpunkt för
exakt dessa två verkliga våg-1-produkter:

1. `gotlands-energi-gotland-taxa-17-under-50-mwh-ar`
2. `sundsvall-energi-indal-liden-och-lucksta`

Detta är en implementation bakom två separata spärrar. Lägg Gotland till
den interna scenariomotorns pilot-/stödmängd tillsammans med Sundsvall,
men behåll den publika allowlisten **helt tom**. Ingen kund ska se den nya
generiska vyn före en separat aktiveringsdiff och Codexgranskning.

Utgå i en ny isolerad Neptune-worktree/branch från exakt den godkända
committen `1bfe1037063e1713dfbb54bfcc62d94b848b24f8`. Ändra inte Enkey.
Skills-bas är `be8ef4d010debdb9867941ccb1021d37787e15a2`.

## A. Tariffneutral våg-1-motor

1. Den interna stödmängden ska innehålla exakt de två ID:na ovan. Den
   publika mängden förblir tom och ska ha negativa test för båda ID:na.
2. Samma `beraknaArsproduktMedKostnadsled` ska användas för referens och
   alla efterfall. Endast den explicita styrbara rumsvärmeserien minskas
   10/15/20 procent. Fast avgift, kapacitet, flöde, retur, historik,
   policyfält och vald tariffprodukt hålls oförändrade.
3. Gotlands valda taxa får inte bytas mitt i scenariot. Taxa 17/21 väljs
   av föregående kalenderårs tariffgrund, inte av att efterfallet råkar
   passera en energigräns. Våg 1 omfattar endast taxa 17; taxa 21 ligger
   kvar i våg 3 på grund av volymrabatt och avkylningsregel.
4. Bind oberoende facit, inte facit genererat av funktionen under test:
   - Sundsvall: 120 MWh total, 96 MWh rumsvärme, referens
     151 200 kr inkl. moms; besparing 12 096 / 18 144 / 24 192 kr och
     efterkostnad 139 104 / 133 056 / 127 008 kr.
   - Gotland taxa 17: 40 MWh total, 32 MWh rumsvärme, referens
     50 570 kr inkl. moms; fast avgift ska ligga kvar 370 kr inkl. moms;
     besparing 4 016 / 6 024 / 8 032 kr och efterkostnad
     46 554 / 44 546 / 42 538 kr.
5. Prova noll/nära-noll sommarvärme, ogiltiga serier, negativ/noll
   besparing och att prisledssumman stämmer före/efter. Inga dolda
   effekt-, flödes- eller temperaturvinster får uppstå.

## B. Återanvändbar, men fortfarande spärrad UI-väg

Bygg den generiska kopplingen nu så att en senare aktiveringsdiff bara
behöver öppna den publika produktgrinden, inte lägga ny prislogik i
React.

1. Skapa en tariffneutral indataadapter och resultatvy för
   `OptimateScenarioResultat`. Den ska kunna användas efter både den äldre
   `fullstandig`-vägen (Gotland) och `arsprodukt`-vägen (Sundsvall), utan
   att ändra deras befintliga resultat.
2. UI-lagret måste kontrollera
   `stodjerOptimateScenarioPubliktAktiverad`, aldrig bara den interna
   stödmängden. När den publika mängden är tom ska inget generiskt
   scenariofält, kort eller felmeddelande synas i den skarpa sidan.
3. Den styrbara rumsvärmen ska vara en explicit, validerad storhet. Om
   total köpt värme anges får 18 procent tappvarmvatten/övrig last endast
   användas som en **synlig och ändringsbar preliminär uppskattning**, med
   källa/antagande i resultatet; den får inte vara en dold universell
   leverantörsregel. Om användaren anger enbart rumsvärme ska den angivna
   årssumman bevaras som rumsvärme.
4. En skattad månadsprofil ska märkas `estimated_mwh` och visa att den är
   en schablon. En uttryckligen ifylld giltig rumsvärmeserie får märkas
   enligt sin verkliga källa. Tolv totalmånader och tolv rumsvärmemånader
   ska summera mot sina årsbelopp och rumsvärme får aldrig överstiga köpt
   värme en månad.
5. Resultatkortet ska visa 10/15/20, sparad MWh, kostnadsskillnad,
   årskostnad efter, prisår/moms samt att fasta och andra låsta prisled
   inte antagits minska. Visa noll eller negativ skillnad ärligt.
6. Lägg komponent-/Reactprov som genom en testlokal mock/injektion öppnar
   den publika grinden och bevisar hela kopplingen för båda produkterna.
   Produktionskoden och den byggda standardartefakten ska fortsatt ha tom
   publik allowlist. Lägg även ett ordinarie negativt browserprov att
   inget generiskt våg-1-kort syns före aktivering.

Om en säker, ändringsbar rumsvärmeinmatning inte ryms utan att bryta den
befintliga formulärsemantiken: skriv `BLOCKED: Codex` med konkret
komponent-/datakontrakt i stället för att gömma ett 18-procentsantagande.

## C. Matris och dokumentation

1. Sätt Gotland taxa 17 till `godkand_intern_pilot_ej_publik`, samma
   status som Sundsvall. Förväntad statusfördelning blir då 74
   `not_reviewed`, 2 interna piloter och 1 synlig särskild
   Stockholm-prototyp.
2. Lägg en mekanisk, fail-closed lista över exakt våg-1-ID:na och test att
   matrisens `review_wave == 1` är identisk med listan. Ingen framtida
   katalogändring får tyst ändra våg-1-scope.
3. Uppdatera planens daterade status append-only till 10/15/20 och dagens
   mål 76 verkliga produkter; skriv inte om den historiska originaltexten.
4. Bevara Gävle/Härnösand och alla övriga 74 produkters teknik- och
   granskningsstatus oförändrad.

## Verifieringsgrind

- riktade motor-, adapter-, React- och matrisprov för båda produkterna;
- full Vitest mot exakt
  `/private/tmp/enkey-agents-harnosand-2026` i isolerad syskonlayout och
  Python 3.14.4 — använd inte den divergerade
  `/Users/robertrennel/Code/enkey-agents` som bevis;
- `npx tsc --noEmit`, isolerat bygge och ordinarie negativt E2E;
- Python-unittest, matris `--check`, deterministisk omgenerering och
  `git diff --check`;
- exakta fillistor och rena isolerade worktrees efter test.

Committa Neptune- och skills-delarna fokuserat och lämna en ny unik
`REVIEW_READY: Codex`. Ingen publik aktivering, merge till main, rebase,
push eller historikomskrivning.
