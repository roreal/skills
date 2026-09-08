---
proposal_id: "2026-09-04-001"
date: "2026-09-04"
author: Claude
status: draft — inväntar utvärdering av Robert och Codex
relates_to: "Utvärderingsfynd P2, 2026-09-04-utvardering-av-kalkylatorn.md (\"Motstridig Gotlandstaxa och årsenergi accepteras utan varning\")"
---

# Förslag: strukturerad giltighetsmetadata för tariffer med årsenergigräns

## Problemet, kort

Kalkylatorn lät ett scenario med 500 MWh/år räkna på "Gotland taxa 17,
under 50 MWh/år" utan varning. Tariffnamnet gör gränsen synlig för en
människa som läser dropdownen, men inget i koden kontrollerar den. En
kund kan därför få ett trovärdigt resultat från en tariff som motsäger
den egna inmatningen.

Codex rekommendation (utvärderingen): "lägg tariffens giltighetsvillkor i
strukturerad metadata och visa en blockerande kontroll eller tydlig
varning. Undvik leverantörsspecifik strängtolkning i UI:t." Det här
förslaget är en konkret utformning av det.

## Vad som finns i källan i dag

Jag har läst båda Gotland-posterna i katalogen i sin helhet. Ingen
strukturerad gräns finns — "under 50 MWh/år" och "över 50 MWh/år" står
bara i det fria textfältet `network_or_product`:

```json
{
  "id": "gotlands-energi-gotland-taxa-17-under-50-mwh-ar-2026",
  "network_or_product": "Gotland taxa 17, under 50 MWh/år",
  ...
}
{
  "id": "gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026",
  "network_or_product": "Gotland taxa 21, över 50 MWh/år",
  "adjustments": [
    { "type": "volume_discount", "basis": "previous_calendar_year_MWh", ... }
  ],
  ...
}
```

Två saker är värda att notera:

1. **Taxa 21 har redan ett besläktat begrepp**: `volume_discount`-posten
   anger uttryckligen `basis: "previous_calendar_year_MWh"` — samma
   affärsvariabel (föregående kalenderårs energi) som styr vilken av de
   två taxorna en kund överhuvudtaget hör hemma i. Det här förslaget
   återanvänder samma variabel och samma UI-fält
   (`falt.foregaende_ars_mwh`, redan byggt för granskningsfynd P1) i
   stället för att uppfinna ett nytt.
2. **Gränsens exakta sida vid 50,000 MWh är inte verifierad.** "Under"
   respektive "över" i namnen antyder att 50 MWh hör till taxa 21
   (`>= 50`), men det är inte bekräftat mot en primärkälla. Det här
   förslaget flaggar det som en öppen punkt för verifieringslistan
   (`Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`) snarare än
   att gissa.

## Föreslagen katalogschema-utökning

Ett nytt, valfritt fält `eligibility` på tariffnivå, generellt formulerat
— inte Gotland-specifikt, så att nästa leverantör med en liknande
volymstyrd produktuppdelning (t.ex. VB Energi, som redan är flaggad i
verifieringslistan med "Prisgrupp styrs av årsenergi") kan använda samma
mekanism utan kodändring:

```json
"eligibility": {
  "basis": "previous_calendar_year_MWh",
  "min_mwh": 50,
  "max_mwh": null,
  "note_sv": "Gäller kunder med en årsförbrukning på minst 50 MWh."
}
```

för taxa 21, och

```json
"eligibility": {
  "basis": "previous_calendar_year_MWh",
  "min_mwh": 0,
  "max_mwh": 50,
  "note_sv": "Gäller kunder med en årsförbrukning under 50 MWh."
}
```

för taxa 17. `min_mwh`/`max_mwh` är `null` när det hållet är obegränsat.
`basis` speglar samma litterala värde som `volume_discount.basis` redan
använder — bara `"previous_calendar_year_MWh"` behöver stödjas i det här
steget, men fältet är öppet för framtida baser (t.ex. `"contract_MWh"`)
utan att strukturen behöver ändras.

Fältet saknas helt för tariffer utan en sådan gräns (de allra flesta) —
en godkännandelista igen, inte en avvisningslista: motorn kontrollerar
bara när `eligibility` faktiskt finns.

## Vad som behöver ändras, och var

| Steg | Fil | Ändring |
|---|---|---|
| 1 | `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` | Lägg `eligibility` på Gotlands två poster (källdata — kräver Roberts/Codex godkännande av gränsens sida, se ovan) |
| 2 | `enkey-agents/tools/tariffer/katalog.py` (`till_prisar`) | Passera `eligibility` oförändrat till prisårsposten, som `indatafalt` redan görs — ingen tolkning i motorn |
| 3 | `enkey-agents/tools/tariffer/generera.py` | Ingen ändring — dumpar redan `till_prisar(t)` rakt av (samma mönster som uppgift 6 etablerade) |
| 4 | `neptune-marketing/src/utils/besparingsvarde.ts` | Ny, ren funktion `eligibilityWarning(prisar, energiMwh): string \| null`. `beraknaBesparingsvarde` anropar den med samma bas som redan resolveras för volymrabatten (`falt.foregaende_ars_mwh ?? totalMwh`) och lägger resultatet i `Besparingsvarde.eligibilityWarning` |
| 5 | `neptune-marketing/src/pages/KalkylatorPage.tsx` | Visa `result.besparingsvarde?.eligibilityWarning` som ett `warningMsg`-block under resultatet, samma mönster som Mölndal-upplysningen och `hasHeatRecoveryWarning` redan använder |
| 6 | Pythons motsvarighet (`faktura.py`) | Ingen ändring föreslås i det här steget — se "Avgränsning" nedan |

Steg 4 är den enda nya logiken. Ett förslag på funktionen:

```typescript
export interface EligibilityInfo {
  basis: string;
  min_mwh: number | null;
  max_mwh: number | null;
  note_sv?: string;
}

export function eligibilityWarning(prisar: any, energiMwh: number): string | null {
  const e: EligibilityInfo | undefined = prisar.eligibility;
  if (!e) return null;
  const under = e.min_mwh != null && energiMwh < e.min_mwh;
  const over = e.max_mwh != null && energiMwh > e.max_mwh;
  if (!under && !over) return null;
  return `Den valda tariffen ${e.note_sv ? `(${e.note_sv.toLowerCase()}) ` : ''}` +
    `stämmer inte med den angivna/uppskattade årsenergin (${Math.round(energiMwh)} MWh). ` +
    `Kontrollera att rätt tariff är vald.`;
}
```

Namnet på källan till `energiMwh` (angiven, uppskattad eller löst ur
kronbelopp) skiljs redan ut av `confidenceLabel` (dagens fix) — samma
värde kan återanvändas här utan ny plumbing.

## Varning eller blockering?

**Rekommendation: varning, inte blockering.**

Skälen:

- Gränsen avser *föregående kalenderårs* energi, som kalkylatorn sällan
  känner med säkerhet (bara om `falt.foregaende_ars_mwh` är ifyllt).
  Fallbacken (`totalMwh`, årets egen uppskattning) är en approximation —
  att hårdblockera på en approximation är för strängt, jämfört med
  kronor-lägets P1-fynd där själva TALET blev odefinierbart utan fältet.
  Här är talet fortfarande korrekt räknat för den valda tariffen; det är
  bara valet av tariff som kan vara fel.
- Samma varningsmönster (`warningMsg`, gul/orange banner under
  resultatet) används redan för Mölndals dygnstopp och för
  värmeåtervinning — konsekvent med hur kalkylatorn redan kommunicerar
  "resultatet är korrekt räknat, men var uppmärksam på X".
- En hård blockering riskerar att stänga ute legitima kunder nära
  gränsen (t.ex. en kund vars faktiska förbrukning ligger på 49 MWh men
  vars schablonuppskattning råkar hamna på 51).

Om Robert eller Codex bedömer att blockering ändå är rätt (t.ex. om
riskaptiten för att en kund agerar på fel tariff är låg), är det en
liten ändring: byt `warningMsg` mot samma `setFormError`-mönster som
Gotlands kr-läges P1-spärr redan använder, och stoppa beräkningen
i stället för att bara visa resultatet med en varning.

## Avgränsning: bara TypeScript-sidan i det här steget

Precis som med `foregaende_ars_mwh`-kravet i granskning 003/004 föreslår
jag att kontrollen läggs i webbkalkylatorns kod
(`besparingsvarde.ts`/`KalkylatorPage.tsx`), inte i den delade
Python-motorn (`faktura.py`). Skälen är desamma som då: Python-motorn är
en generisk, redan hårt testad beräkningskärna som andra sammanhang
(en framtida Ellen-integration) kan vilja anropa utan att nödvändigtvis
vilja ha kalkylatorns UI-varningar. Om `eligibility`-fältet visar sig
användbart för fler leverantörer och Ellen-integrationen blir konkret,
är nästa steg att göra samma kontroll tillgänglig därifrån också — inte
att bygga den i förväg för ett scenario som inte finns än.

## Öppna frågor för Robert och Codex

1. **Gränsens sida vid exakt 50,000 MWh** — hör till taxa 17 eller
   taxa 21? Behöver verifieras mot primärkällan (samma källa som redan
   ligger i verifieringslistan för dessa två poster, `source_id: 10_0`).
   Föreslår att lägga till som ett villkor där, inte gissa här.
2. **Varning kontra blockering** — håller ni med om varning som
   standardval, eller ska det vara en hård spärr?
3. **Ska `eligibility` gälla fler leverantörer redan nu?** VB Energi
   ("Prisgrupp styrs av årsenergi") är ett kandidattillfälle i Del B av
   verifieringslistan — om ni redan vet om fler liknande fall bland de
   65 utreds-tarifferna är det billigare att bygga in dem i samma svep
   än att komma tillbaka till mekanismen senare.
4. **Meddelandetext** — är ovanstående svenska text tillräckligt tydlig,
   eller ska den vara mer specifik (t.ex. namnge den tariff som troligen
   är rätt i stället)? Att föreslå en konkret ALTERNATIV tariff kräver
   mer logik (matcha mot andra tariffer hos samma `member_id` vars
   `eligibility`-spann täcker energin) — görbart som en uppföljning om
   ni vill ha det, men inte i förslagets första version.

Jag implementerar inget av detta förrän ni har tagit ställning till
punkterna ovan.
