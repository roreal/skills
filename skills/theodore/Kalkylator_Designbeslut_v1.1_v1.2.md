# Enkey Energipotential-kalkylator — Designbeslut v1.1 och v1.2

**Session:** 2026-05-26  
**Baserad på:** provtryckning mot 6 verkliga BRF-fall + prismodell Small BRF  
**Resultat:** marketing-v26.5.722 (live på enkey.io/kalkylator)

---

## Bakgrund

Kalkylatorn provtrycktes mot verkliga fall (bl.a. NrLyze-jämförelse). Två problembilder identifierades:

1. **Teknisk precision** — schablonenergin överskattar i vissa fall; DHW-dubbelreduktion om användaren anger enbart rumsvärme; VP-systemet hanterade inte skillnaden mellan köpt el och levererad värme.
2. **Kommersiell kalibrering** — abonnemangsformeln gav orimligt höga priser för Small BRF (<500 MWh påverkbar). Konkurrens med NrLyze: Enkey-formeln gav ~45 000 kr/år, NrLyze ~13 440 kr/år för samma fastighet.

---

## v1.1 — Teknisk precision

### 1. EnergyScope (vad avser angiven energi?)

**Problem:** Om användaren anger "322 MWh enbart rumsvärme" och kalkylen sedan tar 80 % av det, räknas VV bort två gånger.

**Beslut:** Nytt fält `energyScope` visas när faktisk energi anges.

| Scope | Effekt |
|---|---|
| `total_incl_dhw` | Multiplicerar med basandel (default FV) |
| `space_heat_excl_dhw` | Multiplicerar med **1,0** — ingen dubbelreduktion |
| `purchased_hp_electricity` | Multiplicerar med basandel, **ingen** COP-division |
| `delivered_heat_from_hp` | Multiplicerar med basandel × 1/3 (COP-faktor) |

Auto-reset: När energisystem byter mellan VP och icke-VP nollställs scope-valet.

---

### 2. VP-schablon använder alltid COP/3

**Problem:** Schablonvärden = levererad värme (kWh/m²). Optimate styr kompressorn ≈ 1/3 av levererad värme.

**Beslut:** Vid schablon för VP-system appliceras alltid ×1/3, oavsett scope (scope är inte relevant om energin är okänd).

---

### 3. Confidence-indikator

Visas som färgad badge i resultatkort.

| Confidence | Utlösare |
|---|---|
| **Hög** | Faktisk energi angiven |
| **Medium** | Schablonenergi, ingen känd återvinning |
| **Låg** | Schablonenergi + FTX-ventilation, eller `hasHeatRecovery = true` |

---

### 4. Payback visas som intervall

Exakt payback-år är missvisande givet beräkningens osäkerhet. Ersattes med intervall:

| Beräknad paybackMid | Visas som |
|---|---|
| < 1 år | under 1–2 år |
| 1–2 år | cirka 1–3 år |
| 2–4 år | cirka 2–4 år |
| 4–6 år | cirka 4–6 år |
| ≥ 6 år | kräver separat analys |

---

### 5. Caseklassning A–E

| Klass | Kriterium |
|---|---|
| **A** | Payback < 2 år, score ≥ 75, faktisk energi angiven |
| **B** | Payback < 4 år |
| **C** | Payback 4–6 år, eller låg confidence |
| **D** | Payback ≥ 6 år, eller nettobesparing negativ |
| **E** | Restaurang / speciallokal — separat bedömning |

---

## v1.2 — Kommersiell kalibrering

### 6. Segmentering Small / Medium / Large

**Problem:** En formel passar inte alla fastigheter. Small BRF är priskänsligt och konkurrensexponerat.

**Beslut:** Tre segment med olika formler.

| Segment | Villkor | Formel |
|---|---|---|
| **Small** | 1 UC och <500 MWh påverkbar | `min(max(9 000, MWh×50), gross×35%, 18 000)` |
| **Medium** | 1–2 UC och 500–1 500 MWh | `max(6 000, min(score-raw, gross×40%))` |
| **Large** | >1 500 MWh eller >2 UC | `max(6 000, min(score-raw, gross×45%))` |

**Rationale Small:**
- 50 kr/MWh ger jämförbart pris med NrLyze-nivå.
- 9 000 kr/år nedre golv — täcker driftkostnad.
- 18 000 kr/år tak — begränsar risk för kund i litet case.
- 35 % value-share cap — säkrar att abonnemanget aldrig överstiger värdet.

**Rationale Medium/Large:**
- Behåller befintlig score-baserad prissättning.
- Absolut minimum 6 000 kr — kan inte underskridas av value-share.
- Value-share 40 % (Medium) / 45 % (Large) skyddar Enkeys marginaler.

---

### 7. Schablonsänkning vid värmeåtervinning (Prio 2, del 1)

**Problem:** Standardschabloner antar byggnader utan frånluftsvärmepump. Fastigheter med extra återvinning köper väsentligt mindre fjärrvärme — schablonen överskattar.

**Beslut:** Om `hasHeatRecovery = true` och ingen faktisk energi angetts:

```
totalMwh = schablon × 0,85
```

Kombineras alltid med `confidence = 'low'` och varningsruta i resultatet.

---

### 8. Etikettjusteringar

| Fält | Gammalt | Nytt |
|---|---|---|
| Energifält | "Totalt köpt energi (MWh/år)" | "Årsenergi för värme (MWh/år)" |
| EnergyScope `space_heat_excl_dhw` | "Enbart rumsvärme" | "Enbart rumsvärme/radiatorvärme (exkl. varmvatten och ventilationsvärme)" |

---

## Testsvit

43 tester i `energiPotential.test.ts`, alla godkända. Täcker:

- Optimate Score (3 konfigurationer)
- Schablonenergi inkl. hasHeatRecovery-reduktion (3)
- Besparingsprocent per score-band (4)
- Confidence + hasHeatRecoveryWarning (4)
- Payback-intervall och caseklassning (3)
- EnergyScope (5 scenarier inkl. VP COP-logik)
- Segmentering Small/Medium/Large (4)
- Rekommenderade tjänster (4)
- Övriga calcResult-egenskaper (13)

---

## Öppna punkter efter v1.2

| Prio | Punkt |
|---|---|
| 2 | Förtydliga `hasHeatRecovery`-frågan med "(utöver ventilationsvalet)" |
| 2 | Payback-cap i Small-segment (om net < installationskostnad / 10 år) |
| 3 | Lokaler × byggår (verksamhetstyp är mer avgörande — planerat v2) |
| 3 | Restaurang/bad som beräkningsbar typ med separat modell |
| 3 | Fjärrvärmekostnad i kr som alternativ inmatning |
| 3 | Separat sida med Small BRF-prissättning för säljstöd |
