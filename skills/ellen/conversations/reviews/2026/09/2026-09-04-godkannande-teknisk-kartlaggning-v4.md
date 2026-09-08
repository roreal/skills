---
review_id: "2026-09-04-006"
date: "2026-09-04"
reviewer: Codex
status: approved-with-conditions
scope:
  - teknisk-kartlaggning-28-tariffer.md version 4
  - omgranskning 2026-09-04-005
  - aktuell tariffkatalog
implementation_changed: false
---

# Godkännande av teknisk kartläggning v4

## Bedömning

V4 stänger samtliga sex uttryckliga fynd i granskning `2026-09-04-005`:

- tariffkrav, körningsindata och resultatmetadata är separata objekt,
- snapshot är en resultategenskap och inte en påhittad fjärde indatakälla,
- E.ON/Navirum med ett enda effektvärde klassas inte längre som exakt,
- hela Vattenfalltariffen blockeras medan flödesposten saknas,
- Södertörns och Telges temperaturunderlag behandlas inte längre som verifierad noll,
- byggbara och blockerade justeringar hålls isär,
- matrisen har ersatts med familjealgoritmer plus ett verkligt tariff-ID-register,
- Vattenfalls årliga uppdatering har fått en avgränsad källbedömning.

Codex kontrollerade maskinellt att matrisen innehåller exakt 27 tariff-ID:n, att inga är
dubbletter och att samtliga 27 finns i `optimate-fjarrvarme-2026.json`.

Arkitekturen är därmed **godkänd med villkor för en avgränsad grundimplementation**. Det
behövs inte en ny dokumentversion före kodstart. Villkoren nedan ska däremot vara uppfyllda
och testade innan någon av de nya tarifferna blir valbar eller kallas produktionsklar.

## Acceptansvillkor för implementationen

### 1. Exakt läge och uppskattningsläge måste vara två uttryckliga körningar

V4 rad 79–82 säger korrekt att ett saknat obligatoriskt `supplied_input` blockerar hela
resultatet. Rad 138–141 säger samtidigt att ett saknat temperaturvärde ger
`accuracy: estimated`. Båda beteendena kan finnas, men inte i samma implicita körning.

Motorn ska tillämpa följande regel:

```text
Begärt exakt resultat + obligatorisk indata saknas
  => completeness: blocked

Uttryckligen valt uppskattningsläge + en dokumenterad schablon skapas
  => supplied_input.basis_type: estimated
  => accuracy: estimated
  => schablonens värde, källa och antagande redovisas
```

Ett saknat värde får alltså inte automatiskt bli ett giltigt nollvärde. Om ett estimat är
tillåtet måste även det existera som en spårbar `supplied_input`, inte bara uppstå inne i en
formel.

### 2. Resultatstatus ska härledas deterministiskt och testas

Implementationen behöver en gemensam statusfunktion, inte separata UI-bedömningar. Minst
följande fall ska ha tester:

| Situation | Förväntad status |
|---|---|
| Alla obligatoriska årsindata har rätt täckning och är `supplier_value` eller verifierat `calculated` | `accuracy: exact`, `completeness: complete` |
| Minst en uttryckligen tillåten indata är `estimated` | `accuracy: estimated` |
| Rullande månadsfält representeras av ett enda aktuellt värde | `accuracy: snapshot` |
| Obligatorisk indata eller verifierad formel saknas i exakt läge | `completeness: blocked` |
| En hel kostnadskomponent utelämnas | Aldrig `complete` eller `exact` |

`partial` bör antingen få en tydlig, testad betydelse eller tas bort tills ett faktiskt
användningsfall finns.

### 3. Skyddet måste finnas i den gemensamma motorn, inte bara i React

V4 rad 145–148 vill behålla temperaturdefaultar i låg nivå för direkta motoranrop. Det är
acceptabelt endast om dessa hjälpfunktioner inte kan nå ett publikt kostnadsresultat utan att
resultatkontraktet känner till att defaulten användes.

Alla publika beräkningsvägar — Python, generator, TypeScript-wrapper och React — ska gå
genom samma krav- och statuskontroll. Ett direkt motoranrop med saknad temperatur eller
volym får aldrig ge ett omärkt exakt resultat. Bakåtkompatibla låg-nivådefaultar ska antingen
vara interna eller automatiskt skapa `basis_type: estimated`.

### 4. De statiska tariffkraven ska instansieras per tariff

V4 definierar schemat för `required_input`, men implementationen måste också lägga in de
faktiska posterna per tariff. Varje post ska bära enhet, tillämpning, tidsupplösning,
täckningsperiod och källreferens. Särskilt viktigt:

- Karlstads effekt kan uppdateras november–mars. Ett enda värde är därför bara exakt för den
  period där det gällde; historisk årssumma kräver rätt värde per giltighetsperiod.
- E.ON/Navirums årsberäkning kräver faktisk årsvolym och volymvägd framledningstemperatur,
  eller motsvarande månadsserie, utöver effektvärdet.
- Södertörn kräver verkligt temperatur-/avvikelseunderlag.
- Telge kräver returtemperaturunderlag och normalårskorrigerad energi för rätt period.
- VänerEnergi kräver verklig volym.
- leverantörsbekräftat band eller produktval ska vara ett eget krav där formeln inte får
  välja det automatiskt.

Matrisens generella källtexter som “Katalog + verifieringslista” ska vid implementationen
lösas till befintliga `source_refs` eller en konkret verifieringspost.

### 5. Månadsvis redovisningsfördelning får inte kallas fakturarekonstruktion

Denna batch är godkänd för årsnivå. Om befintlig `manadsuppdelning` visas ska den fortsatt
märkas som redovisningsmässig fördelning av årsbeloppet. `scope: monthly` eller
`accuracy: exact` får inte användas för den visningen innan varje månads tariffposter räknas
om med månadens egna indata.

### 6. Blockerade tariffer ska förbli inaktiva

- Sundsvall Matfors/Kvissleby förblir inaktiv tills nätvärdet har en verifierad källa och
  motorn kan ta emot rätt månadsdata.
- Samtliga tolv Vattenfalltariffer förblir inaktiva även om delreglerna 3.1, 3.2 och 3.4
  implementeras och testas.
- `production_ready: false` får inte kringgås av UI eller wrapper.

## Godkänd första implementationsetapp

Claude kan nu börja med följande avgränsade etapp:

1. Implementera de tre kontraktsobjekten och den gemensamma statusfunktionen.
2. Spegla samma typade kontrakt genom Python, generator och TypeScript.
3. Lägg till testerna i acceptansvillkor 1–3 utan att aktivera nya tariffer.
4. Implementera Indal/Liden/Luckstas `ej_tillämpligt`-sentinel som första tariffändring.
5. Lämna en kontrollpunkt till Codex innan Familj 4, Telge eller E.ON/Navirum aktiveras.

Detta ger en liten och verifierbar grund. Familj 4 och Telge kan därefter tas en i taget;
E.ON/Navirum efter att snapshot- och täckningsreglerna är testade. Vattenfalls byggbara
delar kan utvecklas internt men gruppen får inte exponeras.

## Slutsats

Kartläggningens arkitektur är godkänd. Godkännandet gäller kontrakts- och grundarbetet ovan,
inte att de 28 tarifferna redan är produktionsgodkända. Det slutliga tariffgodkännandet sker
först mot körd kod, tester och fullständiga `required_input`-poster.

Ingen implementation eller tariffdata ändrades i denna granskning.

## Kontrollerade underlag

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md` (v4)
- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json`
- `Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`
- `SKILL.md`, särskilt invarianten att `null` betyder okänt, inte noll
- `conversations/reviews/2026/09/2026-09-04-omgranskning-teknisk-kartlaggning-v3.md`

## Utförda kontroller

- räknat tariff-ID-rader i v4: 27,
- kontrollerat dubbletter: inga,
- verifierat varje ID mot tariffkatalogen: samtliga finns,
- läst hela v4 och jämfört varje rättning mot fynden i `2026-09-04-005`.

Inga kodtester kördes eftersom v4 uttryckligen inte innehåller någon implementation.
