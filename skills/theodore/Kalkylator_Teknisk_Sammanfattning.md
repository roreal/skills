# Enkey Energipotential-kalkylator — teknisk sammanfattning

**Version:** 1.2 (marketing-v26.5.722, 2026-05-27)  
**URL:** https://enkey.io/kalkylator  
**Kod:** `neptune-marketing/src/utils/energiPotential.ts` + `KalkylatorPage.tsx`

---

## Syfte

CTA-verktyg som ger en snabb uppskattning av en fastighets energipotential för Optimate®. Räknar ut Optimate Score, möjlig besparing, abonnemangsnivå och återbetalningstid — utan att lova exakta siffror.

---

## Flöde steg för steg

```
1. Indata → 2. Optimate Score → 3. Total energi (MWh) → 4. Påverkbar energi →
5. Bruttobesparing → 6. Abonnemang → 7. Nettobesparing → 8. Payback → 9. Caseklassning
```

---

## 1. Indata

| Fält | Typ | Notering |
|---|---|---|
| Byggnadstyp | flerbostadshus / lokaler / radhus | |
| Byggår | 5 intervall (pre1950 → 2010+) | |
| Energisystem | fjärrvärme / elpanna / vp-fjarrvarme / vp-aldre / vp-modern | |
| Ventilationstyp | S / F / FT / FTX | Starkaste drivaren |
| Lokaltyp | kontor / kontor-minimal-vv / skola-vard-gym / restaurang | Bara för lokaler |
| Area | m² | |
| Antal undercentraler | 1–20 | Styr installationskostnad |
| Köpt energi (MWh/år) | valfritt | Lämna tomt = schablon |
| **Energyscope** | total_incl_dhw / space_heat_excl_dhw / purchased_hp_electricity / delivered_heat_from_hp | Visas när energi anges |
| **Har värmeåtervinning** | ja / nej | Påverkar confidence |

---

## 2. Optimate Score (0–100)

Viktat medelvärde:

| Faktor | Vikt | Poäng (högt = mer potential) |
|---|---:|---|
| Ventilationstyp | 40 % | S=95, F=80, FT=55, FTX=30 |
| Energisystem | 35 % | FV=80, elpanna=75, VP+FV=65, VP äldre=55, VP modern=25 |
| Byggår | 25 % | pre1950=90, 1950-75=85, 1975-95=75, 1995-2010=50, 2010+=25 |

FTX och modern VP ger lågt score eftersom de redan optimerar passivt.

---

## 3. Total energi (MWh)

- **Om energiMwh angiven:** används direkt.
- **Annars schablon:** `area × kWh/m² / 1000`

### Schablonvärden (kWh/m²/år)

| Byggnadstyp | pre1950 | 1950–75 | 1975–95 | 1995–2010 | 2010+ |
|---|---:|---:|---:|---:|---:|
| Flerbostadshus | 185 | 165 | 130 | 100 | 70 |
| Lokaler | 150 | 150 | 150 | 150 | 150 |
| Radhus | 130 | 130 | 130 | 130 | 130 |

**Validering:** Om angiven energi < `area × 10 / 1000` MWh stoppas beräkningen med felmeddelande.

---

## 4. Påverkbar energi

> Den del av energin som Optimate kan påverka = rumsvärme/transmission. VV och ventilationsvärme räknas bort.

### 4a. Basandel (flerbostadshus & radhus)

| Ventilation | Äldre (pre–75) | Normal (1975–95) | Nyare (1995–) |
|---|---:|---:|---:|
| S – Självdrag | 80 % | 75 % | 68 % |
| F – Frånluft | 80 % | 75 % | 68 % |
| FT – Från/tilluft | 60 % | 57 % | 54 % |
| FTX – Återvinning | 65 % | 60 % | 54 % |

### 4b. Lokaler (åldersvariation används ej i v1)

| Lokaltyp | Påverkbar andel |
|---|---:|
| Kontor / butik | 60 % |
| Kontor utan VV | 70 % |
| Skola / vård / gym | 52,5 % |
| Restaurang / bad | **Separat bedömning** |

### 4c. Energyscope-justering (v1.1)

Gäller bara när användaren angett faktisk energi.

| Energyscope | Effekt |
|---|---|
| `total_incl_dhw` (default FV) | Multiplicerar med basandel |
| `space_heat_excl_dhw` | Multiplicerar med **1,0** — VV redan borträknat, ingen dubbelreduktion |
| `purchased_hp_electricity` (default VP) | Multiplicerar med basandel, **ingen** COP-division |
| `delivered_heat_from_hp` | Multiplicerar med basandel × **1/3** (COP-faktor) |

### 4d. VP-justering vid schablon

Schabloner = levererad värme. Optimate styr bara el-delen (kompressorn ≈ 1/3 av levererad värme).

| Energisystem | Schablon-COP-faktor |
|---|---:|
| Fjärrvärme / elpanna | × 1,0 |
| VP äldre / modern (schablon) | × 0,333 |
| VP + FV hybrid (schablon) | × 0,567 (0,65 × 1/3 + 0,35 × 1,0) |

---

## 5. Besparingsprocent

| Optimate Score | Min | Max | Mid (används i kalkyl) |
|---|---:|---:|---:|
| ≥ 75 | 15 % | 22 % | 18,5 % |
| ≥ 50 | 10 % | 16 % | 13,0 % |
| ≥ 25 | 5 % | 10 % | 7,5 % |
| < 25 | 2 % | 5 % | 3,5 % |

```
bruttobesparing/år = påverkbar energi (MWh) × 1 100 kr/MWh × besparingsprocent (mid)
```

---

## 6. Abonnemang (internt, visas ej publikt)

Tre kommersiella segment med olika formler:

| Segment | Villkor | Formel |
|---|---|---|
| **Small** | 1 UC och <500 MWh påverkbar | `min(max(9 000, MWh×50), gross×35%, 18 000)` |
| **Medium** | 1–2 UC och 500–1 500 MWh | `max(6 000, min(score-raw, gross×40%))` |
| **Large** | >1 500 MWh eller >2 UC | `max(6 000, min(score-raw, gross×45%))` |

Small har flexibelt minimum (value-share kan gå under 9 000 kr i extremfall).  
Medium/Large har **absolut minimum 6 000 kr** — value-share-cap kan inte underskridas.

### Score-baserat kr/MWh-pris (Medium & Large)

| Optimate Score | kr/MWh (lowerbound) |
|---|---:|
| ≥ 75 | 140 kr |
| ≥ 55 | 100 kr |
| ≥ 35 | 70 kr |
| ≥ 15 | 40 kr |
| < 15 | 0 kr |

---

## 7. ROI och payback

```
installationskostnad = 29 000 kr + antal UC × 38 500 kr
nettobesparing/år    = bruttobesparing − abonnemang
payback (mid)        = installationskostnad / nettobesparing
paybackMin = paybackMid × 0,8
paybackMax = paybackMid × 1,2
```

Om nettobesparing ≤ 0 visas "—" och kontaktuppmaning, inget payback-tal.

### Payback visas som intervall (v1.1)

| Beräknad paybackMid | Visas som |
|---|---|
| < 1 år | under 1–2 år |
| 1–2 år | cirka 1–3 år |
| 2–4 år | cirka 2–4 år |
| 4–6 år | cirka 4–6 år |
| ≥ 6 år | kräver separat analys |

---

## 8. Caseklassning (v1.1)

| Klass | Kriterium |
|---|---|
| **A** | Payback < 2 år, score ≥ 75, faktisk energi angiven |
| **B** | Payback < 4 år |
| **C** | Payback 4–6 år, eller låg confidence |
| **D** | Payback ≥ 6 år, eller nettobesparing negativ |
| **E** | Restaurang / speciallokal — separat bedömning |

---

## 9. Confidence-indikator (v1.1)

Visas i resultatkort som en färgad badge.

| Confidence | Utlösare |
|---|---|
| **Hög** | Faktisk energi angiven |
| **Medium** | Schablonenergi, ingen känd återvinning |
| **Låg** | Schablonenergi + FTX-ventilation eller `hasHeatRecovery = ja` |

**Varning** visas i resultatkort om `hasHeatRecovery = ja` och ingen faktisk energi angetts: schablonen kan överskatta köpt värme.

---

## 10. Rekommenderade tjänster (logik)

| Score | Energisystem | Rekommendation |
|---|---|---|
| ≥ 50 | VP + FV hybrid | Optimate® + Demand Response + Building Insight® |
| ≥ 50 | Fjärrvärme / elpanna | Optimate® + Building Insight® |
| ≥ 50 | VP äldre/modern | Demand Response + Building Insight® |
| < 50 | alla | Building Insight® |

---

## 11. Kontaktformulär

Visas alltid under resultatet. Skickar e-post med alla beräkningsparametrar och resultat till hello@enkey.io.

---

## 11b. Schablonsänkning vid värmeåtervinning

Om `hasHeatRecovery = true` och ingen faktisk energi angetts reduceras schablonen med 15 %:

```
totalMwh = schablon × 0,85
```

Kombineras med `confidence = 'low'` och varningsruta i resultatet.

---

## 12. Vad kalkylatorn inte kan hantera

- Restaurang / storkök / bad (för komplex energibalans)
- Lokaler med åldersvariation (verksamhetstyp viktigare — planerat för v2)
- Separat fjärrvärmekostnad i kr (MWh-ingång krävs)
- Fastigheter där VV, el och värme redovisas separat i energistatistiken
- Modbus/BACnet-data eller faktisk driftstatistik — kräver EBI

---

## 13. Öppna förbättringar (framtida versioner)

| Prio | Förbättring |
|---|---|
| 3 | Lokaler × byggår |
| 3 | Restaurang/bad som beräkningsbar typ med separat modell |
| 3 | Fjärrvärmekostnad (kr) som alternativ inmatning till MWh |
| 3 | Separat inmatning av värme + el + VV |
