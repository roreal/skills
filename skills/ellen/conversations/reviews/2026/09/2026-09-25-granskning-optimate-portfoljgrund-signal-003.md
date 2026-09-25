---
review_id: "2026-09-25-004"
date: "2026-09-25"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-25-003"
skills_reviewed_head: "bbbdf9bf33ea1e21994fa6d2b0d2dc88b6bf781e"
neptune_reviewed_branch: "optimate-portfoljgrund-10-15-20"
neptune_reviewed_head: "1bfe1037063e1713dfbb54bfcc62d94b848b24f8"
activation_allowed: false
push_allowed: false
approved_by: "Codex"
---

# Granskning av Optimate-portföljgrund, signal 003

## Beslut

Den gemensamma scenariomotorns byte till 10/15/20 godtas i sak. Den
aktuella portföljräkningen och vågindelningen är också rätt: **77 val =
76 verkliga + 1 syntetiskt**, 8 befintliga besparingsvägar, 69
årskostnadsvägar och vågor `1:2`, `2:15`, `3:48`, `4:12`.

Matrisdelen behöver en avgränsad rättningsrunda innan våg 1 får starta.
Ingen publik aktivering eller push ingår.

## Fynd

### P1 — katalogcommitens 7–40-grind är inte fullständigt bunden

`parse_snapshot()` söker
`commit=([0-9a-f]{7,40})` utan att binda tokenens högra kant. Därför
godtas ogiltig proveniens genom att parsern tyst kapar den:

- 41 hextecken accepteras som de första 40;
- 40 hextecken följt av `g` accepteras också som de första 40.

Codex reproducerade båda fallen direkt mot den granskade generatorn. Det
bryter handoffens krav att endast ett verkligt commitformat om 7–40
hextecken ska accepteras och att icke-hex proveniens ska avvisas.

Bind hela commitvärdet mot radslut, med eventuellt endast blanktecken
före radslutet, och lägg negativa prov för minst 41 hextecken samt
efterföljande icke-hextecken. Behåll positiva prov för 7 och 40 tecken.

### P1 — ”status-ID finns exakt en gång” är fortfarande fail-open

`json.loads(payload)` accepterar dubbla objektnycklar och behåller den
sista. Kontrollen efter parsning kan därför inte upptäcka att exempelvis
`stockholm-exergi` förekommer två gånger i snapshottexten. Den bevisar
bara att det återstår ett ID efter att en eventuell dublett redan har
skrivits över.

Gör snapshotparsningen fail-closed för dubbla JSON-nycklar och lägg ett
negativt prov som duplicerar ett registrerat produkt-ID. Lägg dessutom
ett faktiskt negativt prov där statusregistret innehåller ett okänt ID;
det nuvarande testet kontrollerar bara de två positiva värdena trots
handoffens uttryckliga negativa krav.

### P2 — statusvärdena saknar sluten vokabulär och den mänskliga matrisen döljer dem

Registret är typat som fri `str`, så ett stavfel skapar en ny status utan
fel. Definiera en sluten mängd tillåtna statusvärden, validera registret
mot den och prova ett ogiltigt värde. Rätta samtidigt den nya sluggen
`synlig_saerskild_preliminar_prototyp` till det konsekventa svenska
ASCII-formatet `synlig_sarskild_preliminar_prototyp` innan värdet sprids
vidare.

Markdownfilen beskriver specialfallen i ingressen men visar inte
`scenario_review_status` på respektive produktrad. Lägg till en
`Scenariostatus`-kolumn och statusräkning i sammanfattningen; bind båda i
test så JSON och den mänskliga arbetsmatrisen inte kan ge olika bild.

## Oberoende verifiering

- Neptune-diffen är exakt två avsedda filer; Sundsvalls interna
  allowlist är oförändrad och den publika allowlisten är fortsatt tom.
- Det riktade 96-MWh-facitet är korrekt: sparad rumsvärme
  `[9,6; 14,4; 19,2]` MWh och köpt totalvärme
  `[110,4; 105,6; 100,8]` MWh.
- Matrisgeneratorns 10 Pythonprov och `--check` är gröna; käll-SHA:n
  matchar den använda tariff-snapshoten.
- Codex körde hela Vitest i en isolerad syskonlayout med exakt
  `/private/tmp/enkey-agents-harnosand-2026` och Python 3.14.4:
  **75 testfiler / 2 410 test gröna**. De fem äldre driftproven ignorerar
  `ELLEN_ENKEY_AGENTS_SOKVAG`, så rätt snapshot måste ligga på deras
  hårdkodade syskonplats; ingen ändring av de äldre proven krävs i denna
  rättningsrunda.

## Rättningsuppdrag

1. Rätta endast matrisgeneratorn, dess test och de två regenererade
   matrisartefakterna samt append-only sessions-/indexlogg.
2. Ändra inte Neptune-committen `1bfe103`; den godtas oförändrad.
3. Kör Python-unittest, `--check`, deterministisk omgenerering och
   `git diff --check`.
4. Kör om hela Vitest mot den exakt låsta Enkey-snapshoten i en isolerad
   syskonlayout; rapportera verkligt kommando och exakt snapshot.
5. Lämna en unik, committad `REVIEW_READY: Codex` med exakta fillistor
   och HEAD:ar. Ingen våg 1, aktivering, merge, rebase eller push.
