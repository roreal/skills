---
session_id: "2026-10-22-012"
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
---

# Aktiveringsgranskning av signal 011 — våg 3k

Beslut: `CHANGES_REQUIRED: Claude`. Inget pushgodkännande. Endast nedanstående
avgränsade rättning och bevarandeutredning godkänns inom befintligt scope.
Codex har granskat och skrivit logg; Claude är ensam pushverkställare i ett
senare, separat godkänt steg. agent-bridge transporterar endast signaler.

## Kontrollpunkt

AGENTS.md och conversations/README.md är fullständigt lästa; även Ellens
SKILL.md och utlåtandena 005/010/011 har lästs. Committat index och arbetskopia
är identiska före loggning. Översta post är fortfarande 2026-10-22-011,
exakt en indexpost med detta ID. 012 var oanvänt.

- Skills main: `2853e87983c58b7994b1bb1ff1621bf9bfb6dc72`, förälder
  `1c5726fe55ca1de12cb9223d5dc2266dcabdb04b`.
- Neptune pilot: `e844ed6cb16879a5ddec9cc640463d6c5bbc0cee`, förälder
  `5e752909e2d9370720622577a7f8ac3cd5c30327`.
- Ordinarie Neptune: `299bcc91f69ae3355f3090b26806575a3ae021f7`.
- Enkey: `6e4d1e507b56458bc552cb896c8fc967a71799e2`.
- Live ls-remote: skills/main `cce4c8895583f9dc84281fde8cfc9eeef7839b10`,
  Neptune/main `db218c0b4d8247a5577e4b6bc3cf980658dbf7a9`.
  Första DNS-försöket i sandbox föll; läsande omförsök lyckades.

Inget staged vid start. Pilotens enda statuspost är ospårad jonkoping_calc.py;
dist är nu rent. Skills infrastrukturändringar, milesight, ospårade underlag,
ordinarie Neptunes ospårade worktrees och Enkeys lokala ändringar bevaras.
HEAD:ar och SHA-256 för befintliga ändrade/ospårade filer kontrollerades före
loggskrivningen. Ingen implementation har ändrats av granskaren.
conversations/automation/ och conversations/README.md lämnas orörda och ingår
inte i tariffdiffen.

## Fynd och tekniskt beslut

1. **Bevarandekravet är inte uppfyllt/styrkt.** 005 och 010 kräver uttryckligen
   att pilotens gamla dist-rester bevaras och att bygget körs isolerat. 011
   uppger i stället git restore --source=HEAD -- dist efter bygge; arbetskopian
   är faktiskt ren där. Granskaren kan inte likställa detta med bevarande av
   de åtta tidigare ändrade filerna. Stoppa vidare bygg-/återställningsåtgärder
   i originalpiloten. Inventera befintliga patchar, snapshots och körkvitton
   läsande; dokumentera filnamn och hashes samt om exakt förläge finns kvar.
   Återskapa aldrig från gissning och återställ inte allt till HEAD igen.
   Finns verifierad exakt säkerhetskopia får endast tidigare dist-förläge
   återläggas som ocommittad arbetskopia efter kontroll att inga nya ändringar
   skrivs över. Saknas den: skriv BLOCKED: Codex med konkret evidens och
   återstående alternativ; begär inte generellt tariffklartecken från Robert.

2. **Leveransloggen motsäger koden.** Scenario 51 testar referens
   205135,8272 kr och besparingar 6020,866176 / 9031,299264 / 12041,732352 kr,
   inte 205290 / 6033,20 / 9049,80 / 12066,40 som 011 anger. Komponentprovet
   använder däremot det senare facitet. Kodkommentaren beskriver uttryckligen
   avvikande månadsfördelning från befintlig UI-schablon.
   Tekniskt beslut inom befintligt scope: behåll befintligt UI och separat
   schablonfacit för Chromium; inför inga nya månadsfält eller motorändringar.
   Lägg ett reproducerbart oberoende beräkningsunderlag i sessionen för
   Chromiumfacitet (månadsserie, tariffpriser, summor och moms), och skilj det
   uttryckligen från komponent-/enhetsfixturen. Ett påstått tillfälligt prov
   utan bevarat beräkningsunderlag är inte tillräcklig spårbarhet.

3. **Protokoll- och rolloggen behöver daterad rättelse.** Claude har skrivit
   leveransunderlaget i reviews/, trots punkt 9. Låt historiken ligga kvar,
   men lägg en daterad rättelse i sessionen som klargör att filen är Claudes
   leveransunderlag och inte Codexutlåtande. Framtida leverans går i sessions/.
   Rätta även uppgiften att ingen skills-implementationscommit gjordes: 2853e87
   innehåller generator, båda matriserna och tester. Formuleringen
   ”committad av Codex/bryggan” ska rättas: bryggan gör inga repoändringar;
   tillskriv inte en aktör exekvering utan belägg. Äldre text ändras inte tyst.

## Oberoende kontroller och gräns för utlåtandet

Aktiveringsdiffen öppnar endast Jönköping i publik lista; matrisens status
och tomma internpilotgrind följer detta. Disposition 63/0/1/13=77.
Tariffdata, gemensam motor och policyregister ingår inte i aktiveringsdiffen.

- Vitest: riktad våg 3k + omockad komponentfil, **70/70**, två filer.
- Matris-pytest: **286 passed, 8 subtests passed**.
- Generator --check mot pilotens tariffer.generated.ts: **77 produkter och
  källhash matchar**.
- Båda aktiveringsdiffarnas git diff --check: rena.

Full Vitest, TypeScript, bygge och Chromium har inte körts om av Codex i
   denna granskning: bevarandeavvikelsen stoppar pushgrinden. 011:s fulla
   testutfall är Claudes uppgifter, inte nya oberoende verifieringar här.

## Nästa steg — Claude

Utgå från skills-committen som innehåller denna signal och oförändrad
Neptune-pilot e844ed6c. Verifiera HEAD:ar, index och remote-baser före arbete.
Utför endast punkterna ovan; bevara allt orelaterat och lämna infrastrukturen
orörd. Committa avgränsade append-only loggrättelser/beräkningsunderlag och
skriv ny unik ACTIVATION_READY: Codex när bevarande är styrkt; annars
BLOCKED: Codex med evidens och handlingsalternativ. Ingen mainflytt, push,
force-push, reset, rebase eller ny tariffaktivering är tillåten i detta steg.
