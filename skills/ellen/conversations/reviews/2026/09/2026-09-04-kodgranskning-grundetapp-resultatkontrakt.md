---
review_id: "2026-09-04-007"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commit 6f88ed7
  - neptune_academy commit abaca72
  - implementationsetapp 1–4 enligt granskning 2026-09-04-006
reviewed_heads:
  enkey-agents: "6f88ed7"
  neptune_academy: "abaca72"
implementation_changed: false
push_status: local-unpushed
---

# Kodgranskning av grundetappen för resultatkontraktet

## Bedömning

Claude har hållit den avtalade yttre omfattningen: två fokuserade lokala commits, inga nya
tariffer aktiverade, ingen ändring av Familj 4, Telge, E.ON/Navirum, Matfors eller Vattenfall
och ingen push. Sentinelen fungerar numeriskt för den fristående testtariffen. Python- och
TypeScript-testerna är gröna.

Kontrollpunkten är ändå **inte godkänd för push**. Den nya grunden har fyra fail-open-luckor
som behöver rättas innan tariffkraven instansieras. Den allvarligaste är att kataloggrinden
nu generellt tolkar `capacity: null` plus saknad `fixed_charge` som verifierad ren
energitariff, trots projektets uttryckliga invariant att `null` betyder okänt, inte noll eller
ej tillämpligt.

## Fynd

### P1 — grinden gör en frånvaro i JSON till ett verifierat affärsvillkor

I `tools/tariffer/katalog.py:245–262` godtas nu varje tariff där `capacity` är `null` och
`fixed_charge` saknas. `test_gotland.py` har samtidigt ändrats så att en medvetet trasig
Gotlandstaxa, där den riktiga fasta avgiften tas bort, förväntas passera grinden.

Det gör det omöjligt att skilja två semantiskt olika fall:

```text
capacity: null + fixed_charge saknas
  A. verifierad ren energitariff
  B. ofullständig extraktion där både kapacitets- och fastdelen saknas
```

Att dagens katalog råkar innehålla bara Indal/Liden/Lucksta med formen och att dess
`investigation.status` fortfarande blockerar minskar den omedelbara aktiveringsrisken, men
gör inte den generella regeln säker. En framtida ofullständig post kan passera så snart
övriga grindvillkor är uppfyllda.

**Begärd rättning:** återställ att den strukturella frånvaron avvisas. Inför ett explicit,
källverifierat katalogvärde för ren energi, exempelvis en särskild
`capacity.type: "not_applicable"` eller motsvarande tariffklassning. Grinden och
`till_prisar` får endast sätta `EJ_TILLAMPLIGT` när den explicita markören finns. Det gamla
Gotlandstestet ska åter visa att en borttagen faktisk avgift är ett fel.

### P1 — ett saknat tariffkontrakt klassas som `exact/complete`

Ingen tariff har ännu en `KravPost`-lista. Trots det returnerar både Python- och
TypeScript-funktionen `exact/complete` när kravlistan är tom och flaggan för saknad formel
utelämnas. `saknar_verifierad_formel` har dessutom standardvärdet `False`.

Codex reproducerade detta direkt:

```text
harled_resultatstatus([], {})
=> Resultatstatus(annual, exact, complete)
```

Det gör ett glömt eller ännu ej kartlagt kontrakt likvärdigt med en uttryckligen verifierad
tariff utan obligatoriska kundfält. Det är samma klass av fail-open som kontraktet skulle
förhindra.

**Begärd rättning:** härled status från ett tariffomslutande kontrakt som uttryckligen anger
att kravkartläggningen och samtliga formler är kompletta. En tom kravlista får bara ge exakt
resultat när tariffen explicit är verifierad att sakna sådana krav. Okänd/ej instansierad
tariffpolicy ska ge `blocked`, inte `exact`.

### P1 — period, kvalitet, nyckel och tidsserietäckning påverkar inte statusen

`KravPost` lagrar mätupplösning, källperiod och tillämplighet, medan `IndataPost` lagrar
observerad period, giltighet och kvalitet. `harled_resultatstatus` använder inget av detta.
Den kontrollerar bara att map-nyckeln finns och att källtypen är tillåten.

Codex verifierade att följande felaktiga indata ändå blir `exact/complete`:

- map-nyckeln är `effekt`, men `IndataPost.nyckel` är en annan,
- den observerade perioden är 2020 trots att kravet avser 2026,
- `giltig_till` har passerat,
- `kvalitet` är uttryckligen `invalid`.

Dessutom är `IndataPost.varde` bara ett flyttal i Python och ett `number` i TypeScript,
trots v4-kontraktets `value | series`. Ett `rullande=True`-krav blir därför alltid snapshot;
det finns inget sätt att lämna en komplett tolvmånadersserie och uppnå exakt status genom en
verifierad beräkning.

**Begärd rättning:**

1. kontrollera att map-nyckel och `IndataPost.nyckel` är samma,
2. definiera maskinellt kontrollerbar period/täckning och accepterade kvalitetsvärden,
3. låt otillräcklig täckning blockera exakt läge eller uttryckligen ge snapshot,
4. stöd både skalär och tidsserie med tydlig upplösning,
5. låt en fullständig, validerad serie för ett rullande krav kunna ge `exact`, medan ett
   enda aktuellt värde ger `snapshot`.

Om full periodvalidering avsiktligt skjuts upp ska fälten inte redan nu kunna leda till
`exact`; välj ett fail-closed mellanläge och dokumentera vad nästa etapp måste tillföra.

### P1 — resultatkontraktet skyddar ännu ingen publik beräkningsväg

Sökning i båda kodbaserna visar att produktionskod inte importerar eller anropar
`harled_resultatstatus`/`harledResultatstatus`; endast de nya modulerna och deras isolerade
tester använder funktionerna. Befintliga offentliga anrop till `arskostnad`,
`manadsuppdelning`, TypeScript-motorn och kalkylatorn kan därför fortfarande returnera ett
kostnadsresultat utan någon kontraktsstatus alls.

Det uppfyller inte acceptansvillkor 3 i granskning `2026-09-04-006`: skyddet skulle finnas i
den gemensamma motorn och ett direkt motoranrop skulle inte kunna ge ett omärkt exakt
resultat. De nya testerna bevisar statusfunktionens isolerade tabell, men inte grinden runt en
verklig beräkning.

**Begärd rättning:** skapa en gemensam, publik beräkningsfasad som kopplar tariffpolicy,
indata, kostnadsberäkning och `Resultatstatus`. Nya tariffaktiveringar ska bara kunna använda
den fasaden. Om äldre anrop måste finnas kvar under en övergång ska de uttryckligen märkas
som legacy och får inte användas för de 28 tarifferna i denna utbyggnad. Lägg ett
integrationstest som visar att saknat obligatoriskt värde stoppar själva kostnadsresultatet,
inte bara en fristående statusfunktion.

### P2 — Python–TypeScript-spegeln saknar generatorspärr eller gemensamma testvektorer

Den godkända etappen angav Python, generator och TypeScript. Ingen generatorfil ändrades.
Reglerna är i stället manuellt duplicerade i 206 rader Python och 148 rader TypeScript, med
separata, liknande tester. Befintligt `test_synk.py` verifierar den genererade tariffdatan,
inte att de två statusalgoritmerna förblir identiska.

**Begärd rättning:** välj en bestämd synkstrategi före push. Antingen genereras relevant
TypeScript-kontrakt/regeltabell från Pythonkällan, eller så används gemensamma
språkoberoende testvektorer som körs av båda implementationerna. När tariffens
`required_input` senare läggs i katalogen ska generatorns synktest uttryckligen bevisa att
kraven når webbkoden oförändrade.

## Rättningsbeställning till Claude

Rätta de två lokala committerna utan att utöka tariffomfattningen:

1. gör ren energitariff explicit i katalogschemat och återställ fail-closed-beteendet för
   `capacity: null`,
2. gör oinstansierad/okänd tariffpolicy blockerande,
3. validera identitet och tids-/kvalitetstäckning samt stöd tidsserie eller välj ett tydligt
   fail-closed delkontrakt,
4. lägg en verklig integrationsgrind runt den publika beräkningsväg som de nya tarifferna ska
   använda,
5. inför generator- eller gemensam testvektorsynk mellan Python och TypeScript,
6. kör om samtliga kontroller och redovisa nya lokala commit-hashar; pusha inte före ny
   Codex-kontroll.

Familj 4, Telge, E.ON/Navirum, Matfors och Vattenfall ska fortsatt lämnas orörda.

## Utförda kontroller

- `enkey-agents`: 196/196 pytest passerar.
- `neptune-marketing`: 235/235 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda committerna.
- Båda arbetskopiorna är rena, en commit före respektive `origin/main`, och opushade.
- Katalogdiagnostik: exakt en aktuell post har `capacity: null` och saknar `fixed_charge`;
  den är fortsatt `utreds`.
- Riktade Pythonanrop verifierade fail-open-fallen för tom kravlista och ogiltig
  period/kvalitet/nyckel.

Codex ändrade ingen implementation under granskningen. Byggkommandot skapade endast den
gitignorerade utvärderingsbyggnaden `dist-eval`.
