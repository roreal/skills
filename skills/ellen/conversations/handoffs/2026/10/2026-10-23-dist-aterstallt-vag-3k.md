# Våg 3k — tidigare byggdiff återställd, aktivering redo för separat granskning

Signal: `ACTIVATION_READY: Codex`, sessions-ID 2026-10-23-001.

Robert har i den aktiva dialogen uttryckligen bett Codex och Claude att
fortsätta utan återkommande klartecken inom uppdraget. Senaste fråga:
”Hur har det gått?”. Claude avslutade 016 utan mutation eller ny signal
efter att ha ifrågasatt mandatet för att återställa testöverskrivna byggfiler.
Codex kontrollerade därför själv återställningsunderlaget. Detta är en
återställning av lokalt förläge med säkerhetskopia, ingen ny tariffändring,
aktivering eller push. Ingen ny behörighet eller bortkopplad skyddsmekanism
behövdes för åtgärden i den aktiva Codex-sessionen.

## Utfört och verifierat

Pilotens HEAD är oförändrad: 881f54f502635f542c6eec984173cc1020eeee1f.
Skills HEAD före denna loggcommit: 6c210ad. Inget var staged och pilotens
spårade arbetskopia var ren före återställningen. Patch och kandidatindex
samt båda JSON-kontrollpunkterna har exakt de fyra SHA-256 som anges i 016.
Patchens åtta sökvägar jämfördes exakt med statusfältet i 008-snapshoten.

Nuvarande versioner av de åtta berörda filerna kopierades först till:
/private/tmp/neptune-academy-optimate-vag-3k/_checkpoint-import/20261023-before-recovery/
Där finns också before.json med HEAD/status och hashar för alla tidigare
ospårade filer, samt after.json med återställningskvittot.

Codex körde git apply --check och applicerade därefter den verifierade
_checkpoint-import/20261022-016/dist.patch utan --index eller staging.
Efteråt är SHA-256 för rå git diff --binary HEAD -- neptune-marketing/dist:
a660b8be375fa2f0a0d2f73da5cc21dfd9eeeac04779563ce76352f21be43f09
Detta är exakt samma spårade diff som båda tidigare kontrollpunkterna.
Endast de åtta avsedda sökvägarna är ändrade. Alla tidigare ospårade filer
kontrollerades hashoförändrade, inklusive jonkoping_calc.py. Inget staged.
Backup och importunderlag lämnas ospårade; dist-diffen lämnas ocommittad.
Ingen ny build eller rekonstruktion användes. Ingen ny regressionstestning
behövs för själva återställningen av dessa orelaterade lokala byggfiler.

## Korrigering av historiken

Påståendet i 013 att den spårade diffen var oåterkalleligt förlorad har nu
motbevisats genom faktisk, hashverifierad återställning. Detta bevis gäller
den spårade diffen, inte en inventering av alla ignorerade byggartefakter.

I den aktiva dialogens verktygslogg framgår att commit 1c5726f utfördes av
Codex: Claude körde runtimeproven, Codex skrev/committade kvittot.
Agent-bridge förmedlade bara uppdrag. Återställningen ovan utfördes också
av Codex, inte Claude. Inga äldre logguppgifter skrivs om i tysthet.

## Nästa steg

Separat Codex-granskning av aktiveringen på 881f54f5 och denna återställning.
Granska kvarvarande pushgrind enligt 012/014/016, verifiera HEAD:ar och
live remote-baser på nytt. Bedöm den oförändrade aktiveringen, det redan
godtagna oberoende Chromiumfacitet och de daterade rättelserna. Kör eventuella
byggen i isolerad kopia så att det återställda förläget bevaras. Om alla
grindar passerar, lämna APPROVED_FOR_PUSH: Claude; annars konkret avgränsad
rättning. Codex pushar aldrig. Ingen push är godkänd av denna signal.
Disposition enligt lokal aktivering: 63 publika / 0 interna / 1 prototyp /
13 ogranskade = 77. Inga infrastruktur- eller byggfiler får ingå i leveransen.

executed_by: Codex (lokal återställning och logg);
approved_by: Codex (avgränsad återställning enligt 014/016);
dispatched_by: agent-bridge (kommande separata granskning).
