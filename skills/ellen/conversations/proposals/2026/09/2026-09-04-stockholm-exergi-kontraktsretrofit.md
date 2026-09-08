---
proposal_id: "2026-09-04-002"
version: 3
date: "2026-09-05"
author: Claude
status: v3 — inväntar utvärdering av Codex innan kodning
relates_to: "Granskning 2026-09-05-002 (changes-required på v2); Granskning 2026-09-05-001 (changes-required på v1); Slutgodkännande 2026-09-04-013 (resultatkontraktets grundetapp)"
---

# Förslag v3: koppla Stockholm Exergis leverantörsfil till resultatkontrakt/policyregister

Ersätter v2 i sin helhet. Svarar på de tre P1- och två P2-fynden i granskning
`2026-09-05-002`. Fortfarande ingen kod — det här är en modellutvidgning som måste granskas
innan den kodas, eftersom den rör den redan godkända grundetappens kärnkontrakt
(`harled_resultatstatus`, `Tariffpolicy`). Stockholm Exergis nuvarande produktionsbeteende,
prisdata och (frånvaro av) kontraktsmarkör är fortfarande oförändrade.

## Vad som var fel i v2, i klartext

v2 satte `debiterbar_effekt_kw` till `kravs_for=("annual",)` och de två andra dynamiska
fälten till `kravs_for=("monthly",)`, men `harled_resultatstatus(..., omfattning="annual")`
filtrerar bort ALLA `monthly`-krav — en policy med bara effekten inrapporterad gav alltså
`annual/exact/complete` trots att kall energi och returtemperatur aldrig validerades. v2
uppfann också ett `kalla_typ`-värde som inte finns (`"fakturerad"`), föreslog ett
motorfält (en månadsmappning) som varken `IndataPost.varde` eller årsfasadens
`kapacitet_bindning`-mekanism kan representera, och blandade ihop tre olika beräkningsändamål
under en enda policy och en enda regressionsplan. Codex mätte konkret att ett årsanrop med
bara en del av fixturens månader ger en HELT annan fast kostnad (139 476 kr för 2025-delen mot
93 620,88 kr av de verkliga månadsanropen) — årsfasaden kan strukturellt inte återspela ett
delår.

## 1. Tre separata beräkningsändamål, med egna krav

| Ändamål | Använder | Publik konsument i dag | Vad v3 kräver för `exact` |
|---|---|---|---|
| **A. Fakturaexakt månadsåterspelning** (regressionstestning, ny intern kontraktsfasad) | `manadskostnad` | Ingen — internt regressionsverktyg, inte en produktväg | Alla tre dynamiska fält rapporterade för EXAKT den månaden, `kalla_typ="supplier_value"`, `kvalitet="verified"` |
| **B. Framåtriktad årsprognos** (det befintliga produktflödet) | `arskostnad`, via `beraknaBesparingsvarde` i `besparingsvarde.ts` | `KalkylatorPage.tsx` — kalkylatorns huvudflöde | Kunden har normalt INTE dessa månadsuppgifter — se punkt 2 nedan för hur `estimated`/`blocked` hanteras utan att blockera hela kalkylatorn |
| **C. Kronor → MWh** (inversen) | `mwhFranArskostnad`, via samma fil | Formulärets "jag vet bara min kostnad"-läge | Se punkt 3 — underbestämt utan samma tre fält, blockeras som `exact` i denna pilot |

Detta ersätter v2:s enda, delade policy och enda regressionsplan. Ändamål A och C bygger på
samma `Tariffpolicy`-definition (samma `KravPost`-uppsättning), men A anropas en gång per
kalendermånad medan B och C förblir årsbaserade — se punkt 2 för hur en årsomfattning ändå kan
uttrycka krav på månadsdata utan att C förväxlas med A.

## 2. Modellutvidgningen: validerat månadsobjekt + tre statiska motorbindningar

**A. Ny, generell periodicitet i `IndataPost`, inte en Stockholm-specifik månadsmappning.**
I stället för v2:s fria `dict`-idé läggs ett formellt, delat begrepp till i
`resultatkontrakt.py`/`.ts`, användbart av vilken framtida tariff som helst med
månadsupplösta fakturafält:

```python
# Ny periodicitet, vid sidan av dagens skalär/serie:
# IndataPost.varde förblir float | Sequence[float] (oförändrat, ingen breaking change).
# NYTT: ett fälts KRAV kan nu deklarera vilka kalendermånader det är tillämpligt för.
tillampliga_manader: frozenset[int] | None = None   # None = alla 12; annars t.ex. frozenset({11,12,1,2,3})
```

`KravPost` får detta nya, valfria fält. Det ersätter den ostrukturerade fritexten i
`tillamplighet` för fält som faktiskt behöver en maskinläsbar månadsregel (returtemperaturen
gäller bara nov–mars) utan att röra `tillamplighet` för andra tariffer.

**B. `harled_resultatstatus` får ett nytt `omfattning="monthly"`**, som INTE filtrerar bort
`monthly`-krav (bugfixen v2 saknade) och som, när ett anrop gäller en specifik `manad`,
kontrollerar `tillampliga_manader` innan ett fält räknas som obligatoriskt: en returtemperatur
för juli är inte `blocked` av att saknas (fältet är inte tillämpligt då), men en returtemperatur
för januari är `blocked` om den saknas eller inte är explicit rapporterad. `omfattning="annual"`
förblir oförändrad — Stockholm Exergis Ändamål A använder INTE årsomfattningen alls, precis
för att undvika den bugg v2 hade.

**C. `Tariffpolicy` får två nya, valfria statiska bindningar, vid sidan av
`kapacitet_bindning`:**

```python
kallenergi_bindning: str | None = None
returtemperatur_bindning: str | None = None
```

Validerade i `__post_init__` på samma sätt som `kapacitet_bindning` redan är (måste finnas i
`kravda_falt`, måste ha rätt `kravs_for`) — men bundna till `"monthly"` i stället för
`"annual"`, eftersom de bara ger mening för Ändamål A.

**D. Ny fasad `berakna_manadskostnad_med_kontrakt`/`beraknaManadskostnadMedKontrakt`**, en
egen fasad vid sidan av (inte en ersättning för) den befintliga
`berakna_arskostnad_med_kontrakt`:

```python
def berakna_manadskostnad_med_kontrakt(
    prisar: dict, policy: Tariffpolicy,
    inrapporterad_indata: Mapping[str, IndataPost],
    ar: int, manad: int, mwh: float, moms: str | None = None,
    saknar_verifierad_formel: bool = False, berakningsdatum: str | None = None,
) -> KontraktResultat:
```

Härleder `Forbrukning(mwh=mwh, mwh_kallt=<kallenergi_bindning>, returtemp_c=<returtemperatur_bindning>,
kapacitet=<kapacitet_bindning>)` ur de validerade `IndataPost`-skalärvärdena (alla tre
bindningar är skalärer för EN månad, ingen serie/mappning behövs eftersom varje anrop redan är
för exakt en månad — detta är den centrala förenklingen jämfört med v2:s månadsmappningsidé)
och anropar den befintliga, redan kontraktsskyddade `manadskostnad(..., _kontraktpassersedel=...)`
via samma mönster som `_arskostnad_for_kontraktfasad`. `kalla_typ` för samtliga tre fält är
`"supplier_value"` (rättat från v2:s uppfunna `"fakturerad"`), aldrig `"calculated"` eller
`"estimated"` i Ändamål A — den fakturaexakta återspelningen kräver leverantörens egna,
fakturerade tal.

**Vad som INTE byggs i den här etappen:** ingen generell "en policy täcker både
årsomfattning och månadsomfattning automatiskt"-mekanism. Ändamål A och B förblir uttryckligen
separata anrop mot samma statiska `Tariffpolicy`-definition men olika `omfattning`-värden —
enklare att resonera om och granska än en enda, allomfattande regel.

## 3. Ändamål B (årsprognosen) och Ändamål C (inversen): explicit hantering utan att blockera kalkylatorn

**Ändamål B — `beraknaBesparingsvarde`/`arskostnad`:** kunden anger normalt bara total-MWh,
påverkbar MWh och besparingsgrad — INTE månadsvis kall energi eller returtemperatur. Den
här piloten ändrar INTE detta produktflöde till att kräva dem. I stället: `arskostnad`s
befintliga defaultbeteende (kall energi = 0, en enda `returtemp_c` eller `None`) fortsätter
gälla OFÖRÄNDRAT för Stockholm Exergi i Ändamål B, precis som för alla andra tariffer —
Ändamål B får ALDRIG `_kraver_kontrakt`/`KontraktKravs` eftersom det aldrig anropar
kontraktsfasaden. Det är en medveten, dokumenterad avgränsning: kontraktsmekanismen skyddar i
den här piloten bara Ändamål A (regressionstestningen), inte det befintliga
årsprognosflödet, som fortsätter fungera som i dag för alla tariffer inklusive Stockholm
Exergi.

**Ändamål C — `mwhFranArskostnad`-inversen:** Codex har rätt att den är strukturellt
underbestämd för Stockholm Exergi (olika kombinationer av kall energi/returtemp kan ge samma
totalbelopp). För den här piloten byggs INGEN ny, uppskattningsbaserad inversmekanism —
det skulle kräva ett separat produktbeslut av Robert om vilka antaganden som är acceptabla att
visa för en kund, och det ligger utanför den tekniska kontraktsomfattningen. Ändamål C:s
befintliga beteende för Stockholm Exergi lämnas därför OFÖRÄNDRAT i den här piloten, precis
som Ändamål B — samma avgränsning, samma skäl.

**Konsekvens:** i Fas A (se punkt 5) berörs `besparingsvarde.ts` INTE alls. Kontraktsfasaden
och dess statuspropagering byggs och testas uteslutande i Python/TypeScript-motorlagret
(`resultatkontrakt.py`/`.ts`) mot Ändamål A:s regressionsfixtur. Det finns därför inget nytt
UI-tillstånd att rendera i `KalkylatorPage.tsx` i den här etappen — `kapacitetUppskattad`
(`KalkylatorPage.tsx:945`) är den befintliga, redan granskade förlagan för hur en framtida
status-badge SKULLE kunna se ut, om/när Ändamål B eller C någon gång faktiskt kontraktsbinds
i en senare, separat etapp. Det håller den här piloten till motorlagret, i linje med hur
grundetappen (resultatkontrakt.py/.ts) redan är byggd och granskad utan att röra
produktionens UI.

## 4. Aktiveringsläge: strikt allow-list, och `shadow` byter namn

Ingen runtime-jämförelse eller loggning byggs i webbappen (se punkt 3 — Ändamål B/C rörs
inte). Fältet är alltså en bygg-/testgrind, inte ett observerbart shadow-läge, och byter namn
därefter:

```python
AKTIVERINGSLAGEN = frozenset({"off", "validated", "enforced"})
```

- `"off"` (default, fältet får saknas): leverantörsfilen beter sig exakt som i dag.
- `"validated"`: genererar och testar `Tariffpolicy`/kontraktsfasaden (Ändamål A) men sätter
  INTE `_kraver_kontrakt` — den genererade tariffen förblir exekverbar via de befintliga,
  direkta motorfunktionerna precis som i dag.
- `"enforced"`: sätter `_kraver_kontrakt` — egen, separat commit, egen Codex-kontrollpunkt,
  kodas INTE i den här leveransen.

Generatorn validerar värdet mot EXAKT denna mängd (`frozenset`-medlemskap, inte `bool()` eller
`!= "off"`) och kastar för varje annat värde, inklusive felstavningar och fel typ.

## 5. `effektgrans_kw` och den semantiska diffen — motsägelsen upplöst

v2 sa både "flytta ut `effektgrans_kw: 96` ur prisdatan" och "alla prisfält ska vara
identiska". v3 väljer: flytten är en EXPLICIT, uttryckligen tillåten dataändring, avgränsad
till just det fältet:

- `effektgrans_kw: 96` flyttas från `energi.tillagg[].effektgrans_kw` till en ny, tydligt
  namngiven `_akermannen_fixture_specifik`-sektion i `akermannen-baslinje.json` (fixturen,
  INTE leverantörsfilens generella prisdata) — den är Åkermannens egen, kundspecifika
  effektgräns, inte en Stockholm Exergi-generell konstant (se v1-kritikens P1).
- Den semantiska diffen jämför den genererade TS-filen FÖRE/EFTER och kräver byte-identitet
  för ALLA fält UTOM: den nya `policy`-nyckeln, `aktiveringslage`/`tariff_id`, och
  `energi.tillagg[].effektgrans_kw` (uttryckligen namngiven i testet som den enda tillåtna
  prisfältsändringen, med en kommentar som pekar på den här sektionen).

## 6. Reviderad regressionsplan (ersätter v2:s delårs-årstest helt)

- Den befintliga fakturaverifierande månadsregressionen (mot leverantörsfilens direkta
  `manadskostnad`) förblir OFÖRÄNDRAD och auktoritativ.
- **Ny testtäckning:** ett anrop av `berakna_manadskostnad_med_kontrakt` per fixture-rad — alla
  tolv, var och en jämförd krontal för krontal mot samma rads resultat ur den befintliga
  direkta `manadskostnad`-vägen. Inga syntetiska helårstester i den här etappen; om sådana
  läggs till senare ska de uttryckligen märkas som just syntetiska, aldrig kallas
  fakturaverifiering.
- Täcker därmed automatiskt `tillampliga_manader`-logiken (punkt 2B): novembers och januaris
  rader måste ge `exact` med returtemperaturen bunden, medan en sommarmånad (utan tillämplig
  returtemperatur) inte blockeras av att fältet saknas.
- En explicit negativ testrad: en fixture-rad med en kallmånad (`mwh_kallt > 0`) där
  `kallenergi_bindning`-fältet UTELÄMNAS ur `inrapporterad_indata` ska ge `blocked`, aldrig
  tyst falla tillbaka till noll — det bevisar att avsaknad inte kan ge `exact`.

## 7. 12/18/21 — tre separata, oattribuerade fakta (ingen hypotes)

Per Codex begäran, utan tolkning:

- Testfixturen (`akermannen-baslinje.json`) innehåller **12** konsoliderade månadsrader (maj
  2025–april 2026).
- Leverantörsfilens fria textrad uppger **18** fakturor (jan 2025–juli 2026).
- Leverantörsfilens JSON-metadata (`verifierad.mot`) uppger **21** fakturor (maj 2025–juli
  2026).
- Relationen mellan de tre talen är INTE verifierad i det här repot. Min tidigare förklaring
  (preliminära/avräknade fakturor enligt Roberts kommentar i chatten) är en rimlig HYPOTES,
  inte ett bekräftat facit — den lämnas här som kontext men påstås inte längre vara löst.
  Om en enda, exakt siffra önskas i dokumentationen krävs en genomgång av de faktiska
  fakturadokumenten (datum, vilka som är `(P)`-preliminära och vilka som är efterföljande
  avräkningar) av Robert eller Claude med tillgång till dem — inget antal härleds ur
  antaganden. Detta blockerar inte kontraktsarkitekturen i punkterna 1–6.

## Oförändrat till nästa Codex-kontrollpunkt

Stockholm Exergis nuvarande produktionsbeteende (Ändamål B och C, alltså allt kunder faktiskt
möter i kalkylatorn), prisdata i `leverantor-stockholm-exergi.md` och avsaknad av
kontraktsmarkör förblir precis som i dag tills en `"validated"`-leverans av Ändamål A (punkt
2, 4, 6) är kodad, testad och godkänd. Ingen annan leverantörsfil eller katalogtariff rörs.
