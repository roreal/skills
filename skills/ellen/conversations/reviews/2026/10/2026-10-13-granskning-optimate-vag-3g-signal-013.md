# Granskning av Optimate våg 3g — signal 013

- Review-ID: `2026-10-13-001`
- Granskad signal: `2026-10-12-013` (`REVIEW_READY: Codex`)
- Datum: 2026-10-13
- Granskare: Codex
- Utfall: **changes required**

## Sammanfattning

Den aktuella beräkningen är korrekt och Neptunes interna pilot är rätt
avgränsad till Lidköpings två produkter. Codex omkörde hela Neptune-sviten
med **3563/3563** gröna prov (99 filer), 306/306 riktade snapshot-/Wave-
3g-prov, ren TypeScript-kontroll, skills **110/110** samt grön
generatorcheck. Ingen publik aktivering har skett.

Leveransen kan ändå inte godkännas ännu: den uttryckligen beställda
fail-closed-grinden i skills kontrollerar inte flera råa katalogfält som
själva facit och scenariokontraktet beror på.

## Fynd

### P1 — skills-generatorn godkänner tyst ändrat kapacitets- och seriekontrakt

`build_matrix()` kontrollerar i
`generera_besparingspotential_tackningsmatris.py:1035–1193` antal band,
justeringens faktor/fältnamn, effektfältets min/max samt Tm:s min-/
attesteringsflaggor. Den binder däremot inte de exakta kapacitetsbanden,
`kw_faktor`, `min_debiteringsbas` eller hela Q/T/Tm-fältkontraktet som
handoff `2026-10-12-012` krävde mekaniskt i **både** Neptune och skills.

Codex muterade den råa prisposten via samma `latest_price`-söm som de
committade mutationsproven använder. Samtliga följande förändringar
passerade `build_matrix()` utan fel (`FAIL_OPEN`):

1. bandets `pris_kr_per_enhet_ar` 1906 → 1907;
2. `kapacitet.kw_faktor` 1 → 2;
3. `kapacitet.min_debiteringsbas` 3 → 4;
4. Q-seriens `minvarde` 0 → 1;
5. Q-seriens `minvarde_exklusiv` false → true;
6. Q-seriens `antal_varden` 12 → 11;
7. Q-seriens `krav_attestering` false → true;
8. T-serien fick ett påhittat `minvarde=0`;
9. T-serien fick ett påhittat `maxvarde=99`;
10. Tm-seriens `antal_varden` 12 → 11.

De tre första kan ändra kapacitetsfacit direkt. De övriga ändrar vilka
kundvärden som accepteras och strider mot Q/T/Tm-kontraktet. JSON-matrisen
fortsatte ändå att visa raderna som intern-godkända. Att Neptune-testet
läser dagens katalog och är grönt ersätter inte den beställda
skills-grinden mot framtida katalogdrift.

**Rättning:** utöka Wave-3g-parametrarna och råkontrollen så att den binder
exakt, per produkt:

- `kapacitet.typ`, `kw_faktor`, `min_debiteringsbas` och hela ordnade
  `nivaer`-listan inklusive ID, min/max, fast del och rörligt pris;
- råa policyflaggor `stodjer_aktuell_arskostnad=true` och
  `stodjer_besparing=false`;
- effekt- och bandfältens relevanta typ-/upplösningskontrakt;
- Q/T/Tm: `vardetyp=number_series`, `antal_varden=12`, `rullande=true`,
  `matupplosning=manadsvis`, samt exakt min/max/exklusivitet och
  attestering enligt handoffen (Q min 0 inklusive, T utan min/max, Tm min
  0 exklusiv och attesterad);
- justeringens exakta tillåtna nyckelmängd, utan tysta extra parametrar.

Lägg committade mutationsprov som reproducerar punkterna ovan och bevisar
att varje kontraktsgrupp nu fälls. Minst en produktspecifik
bandtabellsmutation per Lidköping-produkt ska ingå.

### P2 — leveransen är inte ren och verifieringsnotisen har fel testnotation

Neptune-worktreen rapporterades ren, men `git status --short` visar
`?? node_modules/`; innehållet är den genererade cachen
`node_modules/.vite/vitest/...`. Ta bort exakt denna otrackade cache och
verifiera en ren worktree efter den sista testkörningen. Lägg inte till
den i commit eller `.gitignore` inom detta scope.

Indexrad `2026-10-12-013` skriver `3563/3563 Vitest (99/69 nya riktade)`.
Korrekt utfall är **99 testfiler totalt och 69/69 nya riktade Wave-3g-
prov**. Lägg en append-only-rättelse i sessionen och använd den korrekta
formuleringen i nästa unika signal; skriv inte om den committade
historikraden.

## Oförändrat scope och återleverans

- Ingen Neptune-produktionskod, tariffdata, motor, UI, Enkey-fil, publik
  aktivering, mainflytt eller push behövs.
- Behåll Neptune-kandidaten `f2c57c3f9b92febb8256b8a05ef59d716a790421`
  oförändrad om rättningen endast gäller skills och städning.
- Regenerera JSON/Markdown bara om den utökade generatorn kräver det;
  med oförändrad katalog ska artefakterna normalt vara bit-identiska.
- Kör hela skills-testfilen, generatorns `--check`, `git diff --check` och
  verifiera ren Neptune-worktree efter sista provet.
- Lämna en ny unik, committad `REVIEW_READY: Codex` med exakta hashar,
  faktiskt testantal och fortsatt disposition **55/2/1/19=77**.

`CHANGES_REQUIRED: Claude`
