# Rekommenderad justering av prismodell och kalkyllogik för små fastigheter

**Syfte:** Underlag för att justera Enkeys energipotential-kalkylator så att små föreningar och fastigheter inte överprissätts, samtidigt som större och starkare case fortfarande kan bära en värdebaserad prismodell.

**Bakgrund:** I version 1.1 används ett abonnemangstak där abonnemanget begränsas till maximalt 45 % av beräknad bruttobesparing. Det är ett bra skydd mot överprissättning, men för små fastigheter behövs en mer segmenterad modell.

---

## 1. Grundproblem

Nuvarande logik:

```text
abonnemang = min(
  max(6 000, påverkbar MWh × kr/MWh),
  bruttobesparing × 0,45
)
```

Denna modell har två konsekvenser:

1. Den skyddar mot att Enkey blir för dyrt jämfört med konkurrenter.
2. Den gör samtidigt att abonnemanget i praktiken ofta blir en value-share-modell, där priset hamnar nära en andel av bruttobesparingen.

Det är inte nödvändigtvis fel. Men för små föreningar och fastigheter bör kalkylatorn ha en särskild kommersiell logik, så att priset blir konkurrenskraftigt och lättare att motivera.

---

## 2. Rekommenderad segmentering

Inför tre kommersiella segment:

| Segment | Villkor | Rekommenderad prismodell |
|---|---|---|
| **Small BRF / Small Fastighet** | 1 UC och <500 MWh påverkbar energi | Paketpris + lägre value-share-tak |
| **Medium** | 1–2 UC och 500–1 500 MWh påverkbar energi | MWh-pris med value-share-tak |
| **Large** | >1 500 MWh påverkbar energi eller flera UC | Nuvarande MWh-modell fungerar bra |

Syftet är att inte sänka prislogiken för stora starka case, men samtidigt göra små case konkurrenskraftiga.

---

## 3. Föreslagen Small BRF-modell

För små föreningar och fastigheter rekommenderas ett särskilt paket.

| Parameter | Rekommendation |
|---|---:|
| Villkor | 1 UC och <500 MWh påverkbar energi |
| Årsabonnemang, riktvärde | 12 000–18 000 kr/år |
| MWh-pris | 40–60 kr/MWh |
| Value-share-tak | 30–35 % av bruttobesparing |
| Absolut tak | 18 000 kr/år |
| Golv | 9 000 kr/år, alternativt 6 000 kr vid mycket små case |
| Mål-payback | 3,5–4 år |

### Rekommenderad formel

```text
if affectable_mwh < 500 and substations == 1:
    subscription = min(
        max(9 000, affectable_mwh × 50),
        gross_saving × 0.35,
        18 000
    )
else:
    subscription = min(
        max(6 000, affectable_mwh × score_price_per_mwh),
        gross_saving × 0.45
    )
```

### Kommentar

Detta gör att små fastigheter inte får ett för högt abonnemang baserat på score och MWh, samtidigt som Enkey behåller en tydlig intäktsmodell.

---

## 4. Payback-baserat abonnemangstak

För små fastigheter kan abonnemanget också begränsas utifrån önskad återbetalningstid.

### Formel

```text
max_abonnemang = bruttobesparing − installationskostnad / mål_payback
```

Exempel:

| Parameter | Värde |
|---|---:|
| Bruttobesparing | 36 000 kr/år |
| Installation | 67 500 kr |
| Mål-payback | 4 år |

```text
max_abonnemang = 36 000 − 67 500 / 4
max_abonnemang = 19 125 kr/år
```

Vid mål-payback 3 år:

```text
max_abonnemang = 36 000 − 67 500 / 3
max_abonnemang = 13 500 kr/år
```

Detta hamnar nära prisnivåer som kan vara konkurrenskraftiga mot enklare marknadserbjudanden.

### Rekommenderad användning

Payback-taket bör inte vara den enda prismekanismen, men kan användas som en extra spärr.

---

## 5. Rekommenderad komplett abonnemangslogik

För små fastigheter:

```text
subscription_raw = affectable_mwh × small_price_per_mwh

subscription_value_cap = gross_saving × 0.35

subscription_payback_cap = gross_saving − installation / target_payback

subscription_package_cap = 18 000

subscription = min(
    subscription_raw,
    subscription_value_cap,
    subscription_payback_cap,
    subscription_package_cap
)

subscription = max(subscription, small_minimum)
```

Där:

| Parameter | Rekommenderat värde |
|---|---:|
| small_price_per_mwh | 50 kr/MWh |
| value_share_cap | 35 % |
| target_payback | 3,5–4 år |
| package_cap | 18 000 kr/år |
| small_minimum | 9 000 kr/år, alternativt 6 000 kr i undantagsfall |

### Viktig regel

Om formeln ger ett abonnemang som gör att caset får negativ nettobesparing eller orimlig payback, bör kalkylatorn inte visa ett exakt årtal.

Visa i stället:

> Detta case kräver separat analys.

---

## 6. Medium och Large

### 6.1 Medium

| Parameter | Rekommendation |
|---|---:|
| Villkor | 1–2 UC och 500–1 500 MWh påverkbar energi |
| Value-share-tak | 40 % |
| MWh-pris | Scorebaserat |
| Package cap | Normalt inget |
| Minimiabonnemang | 6 000 kr/år |

Exempel:

```text
if affectable_mwh >= 500 and affectable_mwh <= 1500:
    subscription = min(
        max(6 000, affectable_mwh × score_price_per_mwh),
        gross_saving × 0.40
    )
```

### 6.2 Large

| Parameter | Rekommendation |
|---|---:|
| Villkor | >1 500 MWh påverkbar energi eller flera UC |
| Value-share-tak | 45 % |
| MWh-pris | Scorebaserat |
| Package cap | Inget |
| Minimiabonnemang | 6 000 kr/år |

Exempel:

```text
if affectable_mwh > 1500 or substations > 2:
    subscription = min(
        max(6 000, affectable_mwh × score_price_per_mwh),
        gross_saving × 0.45
    )
```

---

## 7. Föreslagen segmenteringslogik

```pseudo
if substations == 1 and affectable_mwh < 500:
    commercial_segment = "small"

elif affectable_mwh < 1500 and substations <= 2:
    commercial_segment = "medium"

else:
    commercial_segment = "large"
```

Rekommenderade kommersiella parametrar:

| Segment | Value-share cap | MWh-pris | Tak | Kommentar |
|---|---:|---:|---:|---|
| Small | 30–35 % | 40–60 kr/MWh | 18 000 kr/år | Konkurrensskydd |
| Medium | 40 % | Scorebaserat | Inget eller mjukt tak | Normal BRF |
| Large | 45 % | Scorebaserat | Inget | Stora energivolymer |

---

# Del 2 — Rekommenderade förbättringar av kalkyllogiken

## 8. Förtydliga minimiabonnemanget

### Problem

Om formeln skrivs så här:

```text
abonnemang = min(max(6 000, raw), bruttobesparing × 0.45)
```

kan abonnemanget bli lägre än 6 000 kr om value-share-taket är lägre än 6 000 kr.

Exempel:

```text
max(6 000, 3 000) = 6 000
min(6 000, 4 500) = 4 500
```

Det innebär att 6 000 kr inte är ett absolut minimiabonnemang.

### Rekommendation

Bestäm vilken princip som ska gälla.

#### Alternativ A — absolut minimiabonnemang

```text
abonnemang = max(
  6 000,
  min(raw_abonnemang, bruttobesparing × value_share_cap)
)
```

Effekt:

- abonnemang går aldrig under 6 000 kr,
- små svaga case kan få lång payback,
- kalkylatorn bör då ibland visa “kräver separat analys”.

#### Alternativ B — value-share går före minimum

```text
abonnemang = min(
  max(6 000, raw_abonnemang),
  bruttobesparing × value_share_cap
)
```

Effekt:

- abonnemang kan bli lägre än 6 000 kr,
- caset ser bättre ut i kalkylen,
- men “minimiabonnemang” blir inte längre en korrekt formulering.

### Rekommenderat val

För Enkey rekommenderas:

- **Absolut minimum för Medium och Large**
- **Flexibelt minimum för Small**

Exempel:

```text
if segment == "small":
    minimum = 6 000–9 000
    value_share_cap may override in exceptional cases

if segment in ["medium", "large"]:
    minimum = 6 000 absolute
```

---

## 9. Byt namn på energifältet

### Problem

Fältet “Köpt energi” är missvisande när användaren kan ange olika energyscope:

- total värme inklusive tappvarmvatten,
- rumsvärme exklusive tappvarmvatten,
- köpt el till värmepump,
- levererad värme från värmepump.

Särskilt `delivered_heat_from_hp` är inte köpt energi.

### Rekommendation

Byt UI-label från:

> Köpt energi (MWh/år)

till:

> **Årsenergi för värme (MWh/år)**

Föreslagen hjälptext:

> Ange den årsenergi du har tillgång till. I nästa steg väljer du vad värdet avser.

Alternativt:

> Om du inte vet årsenergin kan kalkylatorn uppskatta den från byggnadens area och byggår.

---

## 10. Förtydliga energyscope `space_heat_excl_dhw`

### Problem

Nuvarande scope:

> Endast uppvärmning/rumsvärme exklusive varmvatten

är bättre än tidigare, men kan fortfarande feltolkas.

I vissa underlag kan “uppvärmning exklusive varmvatten” fortfarande inkludera separat ventilationsvärme eller eftervärme.

### Rekommenderad UI-text

Byt från:

> Endast uppvärmning/rumsvärme exklusive varmvatten

till:

> **Endast rumsvärme/radiatorvärme exklusive varmvatten och separat ventilationsvärme**

### Enkel teknisk logik

```text
if energy_scope == "space_heat_excl_dhw":
    affectable_energy = base_energy × 1.0
```

Det är acceptabelt om UI-texten är tydlig.

### Mer försiktig teknisk logik

Om ni vill vara mer konservativa:

| Ventilation | Faktor vid `space_heat_excl_dhw` |
|---|---:|
| S/F | 1,00 |
| FT | 0,90–0,95 |
| FTX | 0,90–1,00 |

Detta är inte nödvändigt i första versionen, men kan övervägas senare.

---

## 11. Hantera värmeåtervinning mer konservativt vid schablonenergi

### Problem

I version 1.1 påverkar värmeåtervinning främst confidence och varning. Men om faktisk energi saknas används fortfarande schablonenergi.

Det kan överskatta köpt värme i fastigheter som redan har:

- FTX,
- frånluftsvärmepump,
- återvinningsvärme till värmesystem,
- spillvärmeåtervinning,
- modern styrning som redan minskat energianvändningen.

### Rekommendation

Om faktisk energi saknas och fastigheten har återvinningssystem bör schablonen reduceras.

### Föreslagen regel

```text
if known_energy_missing and has_heat_recovery == true:
    total_energy = total_energy × 0.85
    confidence = "låg"
    show_warning = true
```

### Mer differentierad regel

| Fall | Rekommenderad åtgärd |
|---|---|
| FTX valt, ingen faktisk energi | Låg confidence + varning |
| Annan återvinning, ingen faktisk energi | Sänk schablon med 15–20 % |
| Frånluftsvärmepump, ingen faktisk energi | Sänk schablon med 20–25 % |
| Faktisk energi angiven | Ingen schablonsänkning |

### Föreslagen UI-text

> Fastigheter med värmeåtervinning kan ha betydligt lägre köpt värme än schablonen. Ange gärna faktisk årsenergi för värme för en säkrare kalkyl.

---

## 12. Förtydliga frågan om värmeåtervinning

### Problem

Ventilationstypen kan redan vara FTX. Då kan frågan “Har värmeåtervinning?” upplevas dubbel.

### Rekommendation

Byt fråga från:

> Har fastigheten värmeåtervinning?

till:

> **Har fastigheten annan värmeåtervinning eller frånluftsvärmepump utöver ventilationsvalet?**

Exempel i hjälptext:

> Exempel är frånluftsvärmepump, återvinningsvärme från ventilation till värmesystem, spillvärmeåtervinning eller annat system som redan minskar köpt värme.

---

## 13. Prioriterad ändringslista

| Prio | Ändring | Varför |
|---:|---|---|
| 1 | Inför segmenten Small / Medium / Large | Skyddar små case utan att sänka stora case |
| 1 | Inför Small BRF-prislogik | Gör Enkey konkurrenskraftigt mot lågprisalternativ |
| 1 | Förtydliga minimiabonnemang | Undviker intern otydlighet i formeln |
| 1 | Byt “Köpt energi” till “Årsenergi för värme” | Minskar felinmatning |
| 1 | Förtydliga `space_heat_excl_dhw` | Undviker dubbel- eller felreduktion |
| 2 | Reducera schablon vid återvinning utan faktisk energi | Minskar överskattad payback |
| 2 | Förtydliga frågan om värmeåtervinning | Undviker dubbelhet mot FTX |
| 2 | Lägg till payback-cap i Small-segmentet | Säkrar konkurrenskraftig återbetalningstid |
| 3 | Inför mer detaljerad logik för FT/FTX vid space heat-scope | Mer precision i v2 |
| 3 | Separat prissida/paket för Small BRF | Gör försäljning enklare |

---

## 14. Rekommenderad slutmodell

### Segment

```pseudo
if substations == 1 and affectable_mwh < 500:
    segment = "small"
elif affectable_mwh < 1500 and substations <= 2:
    segment = "medium"
else:
    segment = "large"
```

### Abonnemang

```pseudo
if segment == "small":
    subscription = min(
        max(9_000, affectable_mwh * 50),
        gross_saving * 0.35,
        18_000
    )

elif segment == "medium":
    subscription = min(
        max(6_000, affectable_mwh * score_price),
        gross_saving * 0.40
    )

else:
    subscription = min(
        max(6_000, affectable_mwh * score_price),
        gross_saving * 0.45
    )
```

### Energifält

```text
Label: Årsenergi för värme (MWh/år)

Hjälptext:
Ange den årsenergi du har tillgång till. I nästa steg väljer du vad värdet avser.
```

### Energyscope

```text
total_incl_dhw:
  Total värme inklusive varmvatten

space_heat_excl_dhw:
  Endast rumsvärme/radiatorvärme exklusive varmvatten och separat ventilationsvärme

purchased_hp_electricity:
  Köpt el till värmepump

delivered_heat_from_hp:
  Levererad värme från värmepump
```

### Återvinning

```pseudo
if known_energy_missing and has_heat_recovery:
    total_energy = total_energy * 0.85
    confidence = "låg"
    show_warning = true
```

---

## 15. Slutsats

Rekommendationen är att inte ta bort abonnemangstaket, utan att göra det mer segmenterat.

För små föreningar och fastigheter bör Enkey använda:

```text
Optimate Small:
1 UC och <500 MWh påverkbar energi
abonnemang = min(
  max(9 000, MWh × 50 kr),
  bruttobesparing × 35 %,
  18 000 kr/år
)
```

För medium och large kan den nuvarande MWh- och value-share-modellen i huvudsak behållas, men med olika value-share-tak:

| Segment | Value-share-tak |
|---|---:|
| Small | 30–35 % |
| Medium | 40 % |
| Large | 45 % |

Detta ger en modell som:

- skyddar små föreningar från överprissättning,
- behåller lönsamhet i större case,
- gör kalkylen mer konkurrenskraftig,
- minskar risken för att tappa affärer till lågprisalternativ,
- och ger säljorganisationen en tydligare kommersiell struktur.
