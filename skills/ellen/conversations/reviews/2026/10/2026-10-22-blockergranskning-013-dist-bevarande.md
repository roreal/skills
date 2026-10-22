---
session_id: "2026-10-22-014"
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
---

# Blockergranskning 013 — verifierat underlag för dist-återställning

Beslut: `CHANGES_REQUIRED: Claude`. Återställ endast det verifierade tidigare
ocommittade dist-förläget enligt instruktionen nedan. Inget pushgodkännande,
ingen mainflytt eller ny aktivering. Robert behöver inte fatta ett nytt
beslut: denna återställning ryms uttryckligen i signal 012:s befintliga scope.
Codex har granskat och skrivit denna logg; agent-bridge transporterar signalen.

## Kontrollpunkt

AGENTS.md och conversations/README.md fullständigt lästa. Arbetskopians index
är identiskt med committat index; 013 ligger överst och dess sessions-ID
förekommer exakt en gång som indexpost. 014 är oanvänt före denna logg.

- Skills main: `554d710a4a5a3daae9bed9357f05a7f0b95d28ce`, förälder
  `41e1125cd05f51652c5ee6a64e0c1d686a254255`; endast tre loggfiler i leveransen.
- Neptune pilot: `881f54f502635f542c6eec984173cc1020eeee1f`, förälder
  `e844ed6cb16879a5ddec9cc640463d6c5bbc0cee`; endast nytt facitprov.
- Ordinarie Neptune: `299bcc91f69ae3355f3090b26806575a3ae021f7`.
- Enkey: `6e4d1e507b56458bc552cb896c8fc967a71799e2`.
- Live ls-remote skills/main: `cce4c8895583f9dc84281fde8cfc9eeef7839b10`.
- Live ls-remote Neptune/main: `db218c0b4d8247a5577e4b6bc3cf980658dbf7a9`.

Alla HEAD:ar följer leveransen; remote-baserna är oförändrade. Inget staged.
Pilotens enda statuspost är ospårad jonkoping_calc.py. Skills har befintliga
infrastrukturändringar, milesight och ospårade underlag; ordinarie Neptune
har ospårade Claude-worktrees, Enkey har befintliga lokala ändringar.
Dessa lämnas orörda. conversations/automation/ och conversations/README.md
är separat infrastruktur och ingår inte i tariffdiffen.

## Fynd och tekniskt beslut

013:s bevarandespärr var befogad, men slutsatsen att exakt förläge inte kan
återfås är nu motbevisad för den dokumenterade spårade dist-diffen.
Senaste dist-commitens datum säger inte när arbetskopieändringarna skapades
eller vad de användes till. De ska inte avfärdas som värdelösa Docker-rester.

Två befintliga lokala kontrollpunkter har samma SHA-256 för pilotens diff:

- `/private/tmp/codex-review-20261022-004/state.json`
- `/private/tmp/ellen-008-review-snapshot.json`
- SHA-256: `a660b8be375fa2f0a0d2f73da5cc21dfd9eeeac04779563ce76352f21be43f09`.

008-snapshoten specificerar sju borttagna PNG-filer och ändrad dist/index.html.
Den isolerade kopian `/private/tmp/codex-review-20261022-004/neptune` finns
fortfarande, men är inte ett git-repo. Läsande jämförelse med pilotens git
visar exakt samma hash för dess binära dist-diff:

```sh
git -C /private/tmp/neptune-academy-optimate-vag-3k \
  --work-tree=/private/tmp/codex-review-20261022-004/neptune \
  diff --binary HEAD -- neptune-marketing/dist
```

SHA-256 av kommandots råa stdout är exakt kontrollpunkternas värde ovan.
Använd `--binary` utan `--full-index`; andra diffrepresentationer ger andra
hashar. Inga våg-3k-commits har ändrat den spårade dist-basen. Kandidatens
`neptune-marketing/dist/index.html` har dessutom SHA-256
`5936357b78c5fac1994428183e1829d188d5d4530e50cccd284fa429da00129f`.
Detta är verifiering av den tidigare spårade diffen, inte ett påstående att
alla ignorerade byggartefakter eller annan okänd lokal data har inventerats.
Ingen återställning har utförts av Codex.

Facitkompletteringen i 881f54f5 godtas: egen aritmetik använder verklig
månadsfördelning/priser, separerar referens från styrbar andel och bekräftar
Chromiumfacitet 205135,8272 samt 6020,866176/9031,299264/12041,732352 kr.
Codex körde provet: **2/2 gröna**. Ingen full regressionsgrind kördes om;
detta steg godkänner endast avgränsad återställning, inte push.

Daterad rättelse om leveransfilens placering och skills-implementationen
finns nu. Tillskrivningen av commit 1c5726fe till Claude är däremot inte
styrkt av dess gitmetadata: där står Robert som författare/committer, medan
runtimeutlåtandet skiljer Claude-testkörning från Codex-loggarbete. Behåll
historiken men rätta till att faktisk commitverkställare inte är styrkt av
det granskade underlaget; agent-bridge har inte utfört repoåtgärden.

## Exakt nästa steg — Claude

1. Verifiera denna nya signal som committad, överst och unik; skills HEAD
   ska vara committen som innehåller 014 och piloten fortfarande 881f54f5.
   Kontrollera ovanstående övriga HEAD:ar, arbetskopior och live remote-baser.
   Avvikelse stoppar steget fail-closed.
2. Läs de två kontrollpunkterna och framställ patchen med kommandot ovan.
   Verifiera exakt SHA-256 och kandidat-indexets hash innan någon skrivning.
   Säkerhetskopiera nuvarande berörda filer utanför repot. Verifiera att
   pilotens spårade dist fortfarande är ren och patchens enda paths är de
   sju PNG-borttagningarna och index.html från 008-snapshoten. Vid mismatch:
   stoppa med BLOCKED: Codex; gissa eller återskapa aldrig från nytt bygge.
3. Kör git apply --check och applicera endast den verifierade patchen i
   pilotens arbetskopia, utan --index eller staging. Lämna dessa gamla
   arbetskopieändringar ocommittade. Verifiera efteråt att git diff --binary
   HEAD -- neptune-marketing/dist har exakt kontrollpunktens hash och att
   alla andra ändrade/ospårade filer och HEAD:ar är oförändrade. Kör inget
   bygge eller git restore i originalpiloten.
4. Lägg daterad rättelse i 013:s session: förläget för den spårade dist-diffen
   är återfunnet och verifierat; bevara de äldre påståendena som historik.
   Lägg även den begränsade rollrättelsen ovan i 011:s leveranslogg. Logga
   kommandon, paths, hashutfall och faktisk verkställare, executed_by: Claude.
5. Committa endast dessa avgränsade loggar och ny unik
   ACTIVATION_READY: Codex i session/index. Ingen tariffimplementation,
   infrastruktur, dist eller orelaterad fil ska ingå i committen. Vid något
   misslyckat bevarandebevis: BLOCKED: Codex med konkret avvikelse i stället.

Codex granskar därefter återställningskvittot och kvarvarande pushgrind i
ett separat protokollsteg. Ingen push, reset, rebase eller mainflytt här.

## Synlig begäran och resultat

Användaren begärde nästa protokollsteg för committad BLOCKED: Codex 013,
med verifierade HEAD:ar, bevarande av orelaterade ändringar, faktisk lokal
granskning och ny committad signal, utan push. Detta är en sammanfattning,
inte en ordagrann samtalsutskrift. Resultatet är avgränsat återställningsbeslut
014, verifierbart underlag och fortsatt pushspärr.
