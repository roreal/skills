# Provtryckning av Enkeys energikalkylator — findings och justeringsförslag

**Datum:** 2026-05-26  
**Syfte:** Underlag för justering av Enkeys kalkylator för påverkbar energi och återbetalningstid.  
**Kalkylversion:** Implementerad modell enligt `Kalkylator — Påverkbar Energi: Parametrar och Matriser`, version 2026-05-26, production `marketing-v26.5.699`.

---

## 1. Sammanfattning

Den implementerade kalkylmodellen fungerar i huvudsak bra för sitt syfte: att ge en snabb uppskattning av energipotential och återbetalningstid för Optimate®.

Provtryckningen visar dock att modellen bör justeras på några punkter innan den används fullt ut i sälj- och marknadsföringsflödet.

### Viktigaste findings

1. **Modellen fungerar mycket bra för stora äldre flerbostadshus med fjärrvärme och självdrag/frånluft.**
2. **Modellen blir känslig i små 1-UC-fastigheter**, särskilt när abonnemang beräknas med hög kr/MWh-nivå.
3. **Kalkylatorn behöver fråga vad den inmatade energin avser**, annars riskerar den att dubbelreducera värmeenergin.
4. **Fastigheter med återvinningsvärme, FTX, frånluftsvärmepump eller redan modern styrning bör flaggas för separat analys.**
5. **Schablonenergi kan bli för hög för byggnader med återvinning eller redan energieffektiv drift.**
6. **NrLyze-caset visar att Enkeys interna abonnemangslogik kan bli hög i små objekt jämfört med konkurrentens abonnemang.**
7. **Kalkylatorn bör hellre visa intervall eller försiktigare caseklassning än ett alltför exakt återbetalningstal.**

---

## 2. Nuvarande beräkningsmodell

Den implementerade modellen bygger på:

```text
påverkbar energi = total energi × påverkbar andel
```

För värmepumpar:

```text
påverkbar energi VP = total energi × påverkbar andel × 1/3
```

ROI-beräkning:

```text
Besparing/år = påverkbar energi × 1 100 kr/MWh × besparingsprocent
Abonnemang/år = max(6 000 kr, påverkbar energi × kr/MWh)
Nettobesparing = Besparing/år − Abonnemang/år
Installationskostnad = 29 000 kr + antal undercentraler × 38 500 kr
Återbetalningstid = Installationskostnad / Nettobesparing
```

---

## 3. Viktig ekonomisk konsekvens av score-modellen

Optimate Score styr både:

1. antagen besparingsprocent,
2. abonnemang i kr/MWh.

Det gör att nettovärdet per påverkbar MWh blir avgörande.

### Nettovärde per påverkbar MWh

| Score-nivå | Besparing mid | Abonnemang | Bruttovärde vid 1 100 kr/MWh | Nettovärde per MWh |
|---|---:|---:|---:|---:|
| Mycket hög | 18,5 % | 140 kr/MWh | 203,50 kr/MWh | **63,50 kr/MWh** |
| Hög | 13,0 % | 100 kr/MWh | 143,00 kr/MWh | **43,00 kr/MWh** |
| Medium | 7,5 % | 70 kr/MWh | 82,50 kr/MWh | **12,50 kr/MWh** |
| Låg | 3,5 % | 40 kr/MWh | 38,50 kr/MWh | **−1,50 kr/MWh** |

### Slutsats

- I **Mycket hög** och **Hög** nivå fungerar modellen.
- I **Medium** blir nettoeffekten mycket svag.
- I **Låg** blir nettobesparingen negativ om abonnemanget räknas fullt ut.

### Rekommendation

Kalkylatorn bör ha en tydlig intern regel:

| Nivå | Rekommenderad hantering |
|---|---|
| Mycket hög | Visa normal ROI |
| Hög | Visa normal ROI |
| Medium | Visa försiktig ROI eller uppmana till analys |
| Låg | Visa inte payback som huvudbudskap |
| Mycket låg | Rekommendera inte automatiskt |

---

## 4. Casebedömningar efter provtryckning

## 4.1 Brf Sjötungan

### Antaganden

- Flerbostadshus
- Äldre byggnadskategori
- Fjärrvärme
- Frånluft/självdrag antaget i kalkyl
- 5 undercentraler
- Stor energivolym

### Bedömning

Sjötungan är ett mycket starkt Optimate-case.

Den stora energivolymen gör att installationskostnaden för fem undercentraler får relativt liten betydelse. Modellen bör visa kort återbetalningstid och hög potential.

### Finding

Detta är ett bra referenscase för kalkylatorn.

### Rekommendation

Behåll nuvarande logik för denna typ av case.

Dock bör kalkylatorn undvika att lova för exakt återbetalning om det saknas faktisk energidata. Visa gärna:

> “Indikerad återbetalningstid: under 1–2 år, beroende på faktisk drift och injusteringsläge.”

---

## 4.2 HSB Brf Pluto

### Antaganden

- Flerbostadshus
- Byggt omkring 1970–1971
- Fjärrvärme
- Frånluft antaget
- 1 undercentral
- Hög score

### Bedömning

Pluto blir ett starkt 1-UC-case i den implementerade modellen.

Eftersom byggår, energisystem och ventilation ger hög score blir både påverkbar andel och antagen besparingsprocent höga.

### Finding

Modellen ger ett rimligt positivt utfall.

### Risk

Om föreningen redan har modern styrning, låg framledningstemperatur, god injustering eller tidigare optimering kan 18,5 % besparingsantagande vara offensivt.

### Rekommendation

Behåll modellen men lägg till en kvalificerande fråga:

> “Har värmesystemet injusterats eller optimerats de senaste 3 åren?”

Om ja: sänk besparingsantagandet en nivå eller visa bredare intervall.

---

## 4.3 HSB Brf Delfinen

### Antaganden

- Flerbostadshus
- Byggt 1980-tal
- Återvinning/FTX eller tekniskt återvinningssystem
- Fjärrvärme och/eller elintensiva system
- 1 undercentral
- Pågående eller genomförda styr-/regler- och återvinningsåtgärder

### Bedömning

Delfinen är inte ett rent standardcase för radiatoroptimering.

Den verkliga energipotentialen verkar i hög grad kunna ligga i:

- fläktar,
- återvinningsvärme,
- varmvatten,
- styr- och reglersystem,
- el,
- och samspel mellan värme och ventilation.

### Finding

Kalkylatorn riskerar att underskatta eller feltolka caset om den bara hanterar värme som radiator-/rumsvärme.

### Rekommendation

Inför en specialflagga:

> “Har fastigheten värmeåtervinning, frånluftsvärmepump, FTX eller större ventilationsåtgärder?”

Om ja:

- visa resultatet som preliminärt,
- uppmana till separat analys,
- eller låt kunden välja “värmeåtervinning/komplext system”.

### Föreslagen UI-text

> “Denna typ av fastighet kan ha stor potential, men energiflödena behöver delas upp mellan rumsvärme, varmvatten, ventilation och el. Kontakta Enkey för en mer träffsäker analys.”

---

## 4.4 Brf Laken

### Antaganden

- Flerbostadshus
- Äldre byggnadskategori
- Fjärrvärme
- Frånluft antaget
- 5 undercentraler
- Schablonenergi använd om faktisk energi saknas

### Bedömning

Laken ser starkt ut i kalkylatorn, men resultatet är beroende av faktisk energiförbrukning.

Med schablonenergi ger modellen ett attraktivt utfall trots fem undercentraler. Om faktisk energianvändning är betydligt lägre än schablonen kan återbetalningstiden bli längre.

### Finding

Laken är ett bra stresstest för relationen mellan energivolym och antal undercentraler.

### Rekommendation

För fastigheter med fler än 3 undercentraler bör kalkylatorn helst efterfråga faktisk värmeenergi eller värmekostnad.

Föreslagen regel:

```text
Om antal UC ≥ 3 och energifältet är tomt:
  visa uppmaning att ange faktisk energianvändning för säkrare kalkyl.
```

### Föreslagen UI-text

> “Eftersom fastigheten har flera undercentraler blir resultatet mer känsligt för faktisk energianvändning. Ange gärna årsenergi eller fjärrvärmekostnad för bättre precision.”

---

## 4.5 HSB Brf Siken

### Antaganden

- Flerbostadshus
- Byggt 1960-tal
- Fjärrvärme
- Återvinningsvärme installerad
- 1 undercentral

### Bedömning

Siken är ett bra men känsligt case.

Om faktisk uppvärmningsenergi används blir resultatet rimligt. Om kalkylatorn använder schablonenergi baserat på area och byggår riskerar den att överskatta potentialen, eftersom återvinningsvärme redan minskat köpt värme.

### Finding

Schablonenergin är för grov för byggnader med redan installerad återvinningsvärme.

### Rekommendation

Lägg till en följdfråga vid FTX/återvinningssystem:

> “Vet du fastighetens faktiska årsenergi för värme?”

Om nej, visa en varning:

> “Schablonvärdet kan överskatta energipotentialen i fastigheter med värmeåtervinning.”

### Möjlig regel

```text
Om ventilationstyp = FTX eller återvinning:
  och användaren inte anger faktisk energi:
    sänk schablonenergin med exempelvis 15–25 %
    eller visa resultat som preliminärt.
```

---

## 4.6 NrLyze / Brf Vapensmeden 5

### Underlag från offert

NrLyze-offerten anger:

- A-temp: 3 312 m²
- BOA: 2 760 m²
- Energiprestanda: 118 kWh/m²
- Energi för uppvärmning: 322 MWh/år
- Energipris: 1,125 kr/kWh
- Besparing: 10 %
- Besparing per år: 36 204 kr
- Grundinvestering inkl. moms: 78 306 kr
- Återbetalningstid: 2,9 år

Offerten anger också att varmvatten uppskattats till 25 kWh/m² BOA och dragits bort från den totala energianvändningen.

### Viktig finding

NrLyze-casets 322 MWh är redan **uppvärmning exklusive varmvatten**.

Om Enkeys kalkylator behandlar 322 MWh som total värme inklusive varmvatten och därefter multiplicerar med exempelvis 80 %, reduceras energin en gång för mycket.

### Rekommendation

Kalkylatorn måste fråga vad inmatad energi avser.

Föreslagen dropdown:

| Alternativ | Kalkylatorns hantering |
|---|---|
| Total värme inkl. varmvatten | Använd påverkbar andel enligt matris |
| Endast uppvärmning/rumsvärme exkl. varmvatten | Använd 100 % som påverkbar bas, alternativt annan justerad faktor |
| Köpt el till värmepump | Använd ej COP-avdrag |
| Levererad värme från värmepump | Använd COP-avdrag |

### Konkurrensobservation

NrLyze har i offerten ett abonnemang på 13 440 kr/år exkl. moms.

Enkeys interna abonnemang kan i ett litet högscore-case bli betydligt högre om det räknas som:

```text
påverkbar energi × 140 kr/MWh
```

Exempel:

```text
322 MWh × 140 kr/MWh = 45 080 kr/år
```

Det är väsentligt högre än NrLyze-abonnemanget.

### Rekommendation

Inför särskild abonnemangslogik för små 1-UC-case.

---

## 5. Rekommenderade modelljusteringar

## 5.1 Lägg till “vad avser energin?” som obligatorisk fråga vid känd energi

### Problem

Kalkylatorn antar i praktiken att angiven energi är total värmeleverans inklusive tappvarmvatten och eventuell ventilationsvärme.

Det stämmer inte alltid.

### Rekommenderad fråga

> **Vad avser den angivna energin?**

### Föreslagna val

| UI-val | Intern behandling |
|---|---|
| Total värme inklusive varmvatten | Multiplicera med påverkbar andel |
| Endast uppvärmning/rumsvärme exklusive varmvatten | Multiplicera ej med VV-reducerande andel, eller använd särskild faktor |
| Köpt fjärrvärme enligt faktura | Multiplicera med påverkbar andel |
| Köpt el till värmepump | Multiplicera med påverkbar andel men ej med COP-avdrag |
| Levererad värme från värmepump | Multiplicera med påverkbar andel och COP-faktor |

### Rekommenderad intern logik

```text
if energy_scope == "total_heat_incl_dhw":
    affectable_energy = total_energy * affectable_share

if energy_scope == "space_heating_excl_dhw":
    affectable_energy = total_energy * space_heat_adjustment
```

Där `space_heat_adjustment` kan sättas till 1,0 i enkel version, eller 0,9–1,0 om separat ventilationsvärme fortfarande kan ingå.

---

## 5.2 Undvik dubbelreduktion

### Problem

Om användaren matar in energi som redan är rumsuppvärmning exklusive varmvatten, ska kalkylatorn inte återigen räkna bort varmvatten.

### Exempel

NrLyze anger 322 MWh som energi för uppvärmning efter att varmvatten dragits bort.

Fel behandling:

```text
322 MWh × 80 % = 258 MWh påverkbar energi
```

Möjligt korrektare behandling:

```text
322 MWh × 100 % = 322 MWh påverkbar energi
```

eller:

```text
322 MWh × 90–100 % = 290–322 MWh påverkbar energi
```

beroende på om uppvärmningsenergin även innehåller separat ventilationsvärme.

### Rekommendation

Inför energiscope.

---

## 5.3 Hantera värmepumpsenergi tydligare

### Problem

Nuvarande modell använder alltid COP-faktor ×1/3 för värmepumpar, men detta förutsätter att användaren anger levererad värme eller beräknat värmebehov.

Om användaren anger köpt el till värmepump blir resultatet fel.

### Rekommendation

Lägg in ett val:

> **Är värmepumpsenergin angiven som köpt el eller levererad värme?**

### Rekommenderad logik

| Angiven VP-energi | COP-faktor |
|---|---:|
| Köpt el till värmepump | × 1,0 |
| Levererad värme från värmepump | × 1/3 |
| Vet ej | Visa hjälptext eller separat analys |

---

## 5.4 Inför specialflagga för återvinningssystem

### Problem

Byggnader med FTX, återvinningsvärme eller frånluftsvärmepump kan få för hög schablonenergi om kunden lämnar energifältet tomt.

### Rekommendation

Lägg till fråga:

> **Har byggnaden värmeåtervinning eller frånluftsvärmepump?**

Om ja och energifältet är tomt:

- visa varning,
- sänk schablonenergi,
- eller be kunden ange faktisk energi.

### Föreslagen regel

```text
if has_heat_recovery == true and known_energy_missing == true:
    result_confidence = "low"
    show_warning = true
```

### Föreslagen UI-text

> “Fastigheter med värmeåtervinning kan ha betydligt lägre köpt värme än schablonen. Ange gärna faktisk årsenergi för värme för en säkrare kalkyl.”

---

## 5.5 Justera abonnemangslogik för små objekt

### Problem

För små 1-UC-case kan abonnemang per MWh ge ett högt årsabonnemang relativt konkurrenter och relativt faktisk bruttobesparing.

### Rekommenderade alternativ

## Alternativ A — Tak för små case

```text
if number_of_substations == 1 and affectable_energy < 500:
    subscription = min(subscription, 15000–25000 kr/year)
```

## Alternativ B — Lägre prisnivå för små case

```text
if affectable_energy < 500:
    use one score tier lower for subscription only
```

## Alternativ C — Abonnemang som procent av bruttobesparing

```text
subscription = min(calculated_subscription, gross_saving * 0.35–0.50)
```

## Alternativ D — Fast paketpris för små BRF:er

Exempel:

| Paket | Villkor | Årsabonnemang |
|---|---|---:|
| Small BRF | 1 UC, <500 MWh påverkbar energi | 12 000–18 000 kr/år |
| Medium BRF | 1–2 UC, 500–1 500 MWh | 20 000–60 000 kr/år |
| Large BRF | >1 500 MWh | MWh-baserat |

### Rekommendation

För CTA-kalkylatorn är Alternativ C mest robust:

```text
subscription = min(
    max(6000, affectable_energy * price_per_mwh),
    gross_saving * 0.45
)
```

Det gör att abonnemanget inte äter upp för stor del av bruttobesparingen.

---

## 5.6 Visa intervall i stället för exakt återbetalningstid

### Problem

Ett exakt årtal kan ge falsk precision.

Exempel:

```text
Återbetalningstid: 0,6 år
```

kan upplevas som för aggressivt, särskilt om energin är schablonbaserad.

### Rekommendation

Visa intervall:

| Beräknad payback | Publik visning |
|---:|---|
| <1 år | “under 1–2 år” |
| 1–2 år | “cirka 1–3 år” |
| 2–4 år | “cirka 2–4 år” |
| 4–6 år | “cirka 4–6 år” |
| >6 år | “kräver separat analys” |

### Föreslagen komplettering

Visa även en konfidensnivå:

| Datakvalitet | Visning |
|---|---|
| Faktisk energi angiven | Hög precision |
| Schablonenergi | Preliminär uppskattning |
| Schablon + FTX/återvinning | Låg precision |
| Speciallokal | Separat analys |

---

## 6. Rekommenderad caseklassning

Kalkylatorn kan med fördel inte bara visa återbetalningstid, utan även klassificera caset.

### Föreslagen klassning

| Klass | Kriterium | Budskap |
|---|---|---|
| A — Mycket starkt case | Payback <2 år, hög score, faktisk energi | “Mycket god potential” |
| B — Bra case | Payback 2–4 år | “God potential” |
| C — Osäkert case | Schablondata + återvinning/FTX | “Potential finns, men kräver verifiering” |
| D — Svagt case | Nettobesparing låg eller negativ | “Kontakta oss för analys” |
| E — Specialcase | Restaurang, bad, storkök, komplex återvinning | “Separat bedömning krävs” |

---

## 7. Ny rangordning av testade case

| Rang | Case | Bedömning | Kommentar |
|---:|---|---|---|
| 1 | Brf Sjötungan | Mycket starkt | Stor energivolym bär 5 UC |
| 2 | HSB Brf Pluto | Mycket starkt | Bra 1-UC-case i äldre FV-hus |
| 3 | Brf Laken | Starkt men datakänsligt | 5 UC kräver faktisk energi för bättre precision |
| 4 | HSB Brf Siken | Bra men osäkert | Återvinningsvärme gör schablon riskabel |
| 5 | HSB Brf Delfinen | Specialcase | Stor potential men inte ren radiatoroptimering |
| 6 | Brf Vapensmeden 5 / NrLyze | Konkurrenscase | Viktigt att undvika dubbelreduktion och för högt småcase-abonnemang |

---

## 8. Prioriterad åtgärdslista

## Prio 1 — bör göras före bred lansering

1. Lägg till fråga: **Vad avser angiven energi?**
2. Förhindra dubbelreduktion när energi redan avser uppvärmning exklusive varmvatten.
3. Lägg till särskild hantering av köpt el kontra levererad värme för värmepumpar.
4. Lägg till varning vid FTX/återvinningsvärme om faktisk energi saknas.

## Prio 2 — bör göras för bättre säljprecision

5. Justera abonnemangslogik för små 1-UC-case.
6. Visa återbetalningstid som intervall.
7. Visa konfidensnivå baserat på datakvalitet.
8. Lägg till caseklassning A–E.
9. Förtydliga label och hint för energifältet: label ska vara "Totalt köpt energi (MWh/år)", hint ska vara "Valfritt — ange köpt fjärrvärme och/eller el till värmepump".

## Prio 3 — framtida version

9. Mer detaljerad modell för lokaler.
10. Separat modell för bad, restaurang, storkök och vård.
11. Möjlighet att ange faktisk fjärrvärmekostnad i stället för MWh.
12. Möjlighet att ange både värmeenergi, elenergi och varmvatten separat.

---

## 9. Rekommenderad uppdaterad kalkyllogik

Nedan är ett förenklat förslag till förbättrad logik.

```pseudo
input:
  building_type
  area
  build_year
  ventilation_type
  energy_system
  substations
  known_energy
  energy_scope
  has_heat_recovery
  recent_optimization

if known_energy exists:
    base_energy = known_energy
else:
    base_energy = area * benchmark_kwh_per_m2 / 1000
    data_quality = "schablon"

if energy_scope == "total_heat_incl_dhw":
    affectable_energy = base_energy * affectable_share

if energy_scope == "space_heating_excl_dhw":
    affectable_energy = base_energy * 1.0

if energy_scope == "purchased_heat_invoice":
    affectable_energy = base_energy * affectable_share

if energy_system == "heat_pump":
    if energy_scope == "delivered_heat":
        affectable_energy = affectable_energy / COP
    if energy_scope == "purchased_hp_electricity":
        affectable_energy = affectable_energy

if has_heat_recovery and known_energy missing:
    confidence = "low"
    show_warning = true

if recent_optimization:
    reduce_saving_tier_by_one_step = true

score = weighted_score(ventilation, energy_system, build_year)

saving_percent = saving_mid_from_score(score)
gross_saving = affectable_energy * 1100 * saving_percent

subscription_raw = max(6000, affectable_energy * price_per_mwh_from_score(score))

subscription = min(subscription_raw, gross_saving * 0.45)

net_saving = gross_saving - subscription

installation = 29000 + substations * 38500

if net_saving <= 0:
    show "Kontakta oss för analys"
else:
    payback = installation / net_saving
    show payback_interval(payback)
```

---

## 10. Förslag på nya UI-frågor

### 10.1 Energi

> **Vet du fastighetens årliga energi för värme?**

Val:

- Ja, total värme inklusive varmvatten
- Ja, endast uppvärmning/rumsvärme exklusive varmvatten
- Ja, köpt el till värmepump
- Ja, levererad värme från värmepump
- Nej, uppskatta från byggnadens area och byggår

### 10.2 Återvinning

> **Har fastigheten värmeåtervinning eller frånluftsvärmepump?**

Val:

- Nej / vet ej
- Ja, FTX
- Ja, frånluftsvärmepump
- Ja, annat återvinningssystem

### 10.3 Tidigare optimering

> **Har värmesystemet injusterats eller optimerats de senaste 3 åren?**

Val:

- Nej / vet ej
- Ja

Om ja, sänk besparingsantagandet eller visa försiktigare intervall.

---

## 11. Slutsats

Den implementerade kalkylatorn är en bra version 1 och ger rimliga utslag för klassiska Optimate-case: äldre flerbostadshus med fjärrvärme, frånluft/självdrag och stor energivolym.

De viktigaste justeringarna för version 1.1 är:

1. **Förstå vad användarens energiinmatning avser.**
2. **Undvika dubbelreduktion av varmvatten.**
3. **Hantera köpt värmepumpsel och levererad värmepumpsvärme olika.**
4. **Flagga återvinningssystem och FTX som lägre konfidens vid schablonenergi.**
5. **Justera abonnemang för små 1-UC-case så att kalkylen inte blir svag relativt konkurrenter.**
6. **Visa payback som intervall och med konfidensnivå.**

Med dessa justeringar blir kalkylatorn både mer trovärdig och mer användbar som CTA-verktyg.
