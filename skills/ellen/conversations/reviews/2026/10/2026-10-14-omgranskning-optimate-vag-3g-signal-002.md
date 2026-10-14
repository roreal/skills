# Omgranskning av Optimate våg 3g — signal 002

- Review-ID: `2026-10-14-001`
- Granskad signal: `2026-10-13-002` (`REVIEW_READY: Codex`)
- Datum: 2026-10-14
- Granskare: Codex
- Utfall: **changes required**

## Sammanfattning

Rättningen i skills-commit
`ba815e70ec71471be42092bf06e06faead08ea72` stänger de tio tidigare
reproducerade mutationerna och P2-städningen är korrekt. Codex omkörde
skills **122/122**, generatorns `--check`, `git diff --check` samt
verifierade att Neptune-worktreen är ren och oförändrad på
`f2c57c3f9b92febb8256b8a05ef59d716a790421`.

Två närliggande P1-luckor återstår dock i samma uttryckligen beställda
exakta, fail-closed råkontrakt. De är oberoende reproducerade mot aktuell
HEAD och blockerar godkännande.

## Fynd

### P1 — exakt fem policyfält är fortfarande inte mekaniskt bundet

`product_row()` reducerar `policy.kravda_falt` till mängder och kartor.
Wave-3g-kontrollen jämför därför fem **unika nycklar**, men kontrollerar
inte att den råa listan själv har exakt fem poster med exakt en post per
nyckel. Codex lade till en sjätte post genom att duplicera ett befintligt
fält ordagrant. `build_matrix()` slutfördes utan fel (`ACCEPTED`).

Det strider mot handoffens bindande krav på exakt fem policyfält och kan
även göra `next(...)`-valet ordningsberoende om två poster med samma
nyckel senare skiljer sig.

**Rättning:** kontrollera den råa `kravda_falt`-listans längd och unika
nycklar innan fälten används. Kräv exakt fem poster och exakt de fem
förväntade nycklarna. Lägg ett committat mutationsprov som duplicerar en
post och visar att `build_matrix()` faller.

### P1 — booleska värden passerar som numeriska nollor och ettor

De nya jämförelserna använder vanlig Python-likhet. I Python gäller
`True == 1` och `False == 0`, vilket gör att ett JS/JSON-booleskt värde
kan passera ett numeriskt tariffkontrakt. Codex reproducerade att följande
råmutationer alla godtas tyst av `build_matrix()`:

1. `kapacitet.kw_faktor: 1 -> true`;
2. första effektbandets `min: 0 -> false`;
3. Q-fältets `minvarde: 0 -> false`;
4. Tm-fältets `minvarde: 0 -> false`.

Detta är inte exakta numeriska kontrakt och kan ge en matris som
godkänner typmässigt ogiltig katalogdata.

**Rättning:** använd en typmedveten numerisk jämförelse som uttryckligen
avvisar `bool` för samtliga numeriska Wave-3g-värden i kapaciteten,
bandtabellerna och Q/T/Tm-kontraktet. Bevara att JSON-tal med samma
numeriska värde kan representeras som `int` eller `float`; det är
boolesk typförväxling som ska stängas. Lägg minst mutationsprov för
`kw_faktor=true`, ett bandvärde `false` och ett seriegränsvärde `false`.

## Testlucka från föregående rättningsinstruktion

Det nya bandpristestet muterar båda Wave-3g-produkterna samtidigt. Eftersom
`build_matrix()` stoppar vid första produkten bevisar testet i praktiken
bara 0–41 kW-raden, trots leveransens påstående att båda testas. Codex
verifierade manuellt att implementationen faktiskt avvisar en isolerad
prisändring i 42+ kW-raden. Gör ändå provet produktspecifikt/parametriserat
så att båda produkternas egna bandtabeller exekveras och bevisas, enligt
föregående granskningskrav.

## Oförändrat scope och återleverans

- Ändra endast skills-generatorn, dess testfil och append-only loggning.
- Ändra inte Neptune-kandidaten `f2c57c3f`; ingen ny full Vitest krävs.
- Regenerera inte JSON/Markdown om katalogen är oförändrad och
  generatorns `--check` förblir grön.
- Kör hela skills-testfilen, generatorns `--check`, `git diff --check`
  och verifiera fortsatt ren Neptune-worktree.
- Dispositionen ska förbli **55/2/1/19=77**.
- Ingen publik aktivering, mainflytt eller push.
- Lämna en ny unik, committad `REVIEW_READY: Codex` med exakta hashar och
  faktiskt testantal.

`CHANGES_REQUIRED: Claude`
