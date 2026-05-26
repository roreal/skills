# Kalkylator — Påverkbar Energi: Parametrar och Matriser

**Version:** 2026-05-26
**Status:** Implementerad i production (marketing-v26.5.699)

---

## Syfte

Detta dokument specificerar de schablonvärden som styr beräkningen av **påverkbar energi** i Enkeys energipotential-kalkylator på enkey.io/kalkylator.

> **Påverkbar energi** = den del av byggnadens värmeanvändning som avser rumsvärme/transmission och som kan påverkas genom optimerad styrning. Tappvarmvatten och separat ventilationsvärme ingår inte.

---

## Formel

```
påverkbar energi (MWh) = total energi (MWh) × påverkbar_andel
```

För värmepumpar tillkommer ett COP-steg efter grundformeln (se avsnitt 3).

---

## 1. Flerbostadshus & Radhus

Påverkbar andel beror på **ventilationstyp** och **åldersgrupp**. Byggår ger åldersgrupp:

| Åldersgrupp | Byggår |
|---|---|
| Äldre | Före 1950, 1950–1975 |
| Normal | 1975–1995 |
| Nyare | 1995–2010, 2010+ |

### Påverkbar andel (%) — implementerad matris

| Ventilationstyp | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| S – Självdrag | 80 % | 75 % | 68 % |
| F – Frånluft | 80 % | 75 % | 68 % |
| FT – Från- och tilluft (utan återvinning) | 60 % | 57 % | 54 % |
| FTX – Med värmeåtervinning | 65 % | 60 % | 54 % |

**Kommentarer:**

- **S/F:** Ingen separat ventilationsvärme. Ventilationsförluster ingår i rumsuppvärmningen. VV ökar som andel i nyare byggnader eftersom total energiförbrukning sjunker.
- **FT:** Konservativ publik schablon. Tilluften värms via separat ventilationsbatteri som Optimate ej styr.
- **FTX:** Äldre/sämre injusterade FTX har högre påverkbar andel. Nyare energieffektiva FTX-hus har relativt sett högre VV-andel och lägre rumsvärmeandel.

### Energifördelning bakom matrisen (referens)

| System | Åldersgrupp | VV% | Ventilation% | Rumsvärme (påverkbar)% |
|---|---|---:|---:|---:|
| S/F | Äldre | 20 % | 0 % | **80 %** |
| S/F | Normal | 25 % | 0 % | **75 %** |
| S/F | Nyare | 32 % | 0 % | **68 %** |
| FT | Äldre | 22 % | 18 % | **60 %** |
| FT | Normal | 27 % | 16 % | **57 %** |
| FT | Nyare | 33 % | 13 % | **54 %** |
| FTX | Äldre | 25 % | 10 % | **65 %** |
| FTX | Normal | 30 % | 10 % | **60 %** |
| FTX | Nyare | 38 % | 8 % | **54 %** |

---

## 2. Lokaler

Lokaler varierar mer med **verksamhetstyp** än med byggår. Åldersvariation används ej i version 1.

Användaren väljer lokaltyp i en dropdown. Påverkbar andel är en konservativ publik schablon.

### Implementerade lokaltyper

| Lokaltyp (UI-val) | Påverkbar andel | VV% | Ventilation% | Kommentar |
|---|---:|---:|---:|---|
| Kontor / butik / lätt lokal | **60 %** | 5 % | 35 % | Normalt kontor med FTX |
| Kontor utan duschar eller kök | **70 %** | 2,5 % | 27,5 % | Minimal VV-användning |
| Skola / vård / gym (hög personbelastning) | **52,5 %** | 10 % | 37,5 % | Lång drifttid, höga luftflöden |
| Restaurang / storkök / bad | **Ej beräkningsbar** | — | — | Separat bedömning krävs |

**Restaurang/storkök/bad:** Visas ej som kalkylerbar lokaltyp. Kalkylatorn visar ett kontaktformulär direkt med texten *"Denna lokaltyp kräver separat bedömning."*

---

## 3. Värmepumpsjustering (COP ≈ 3)

Schablonvärdena representerar **total värmeleverans** (inkl. gratisenergi från mark/luft). Optimate kan bara påverka el-delen (kompressorn) = 1/3 av värmeleveransen.

```
påverkbar (VP) = total × påverkbar_andel × (1/3)
```

| Energisystem | COP-faktor | Formel |
|---|---:|---|
| Fjärrvärme | × 1,0 | total × andel |
| Elpanna | × 1,0 | total × andel |
| VP äldre | × 0,333 | total × andel × 1/3 |
| VP modern | × 0,333 | total × andel × 1/3 |
| VP + FV hybrid | × 0,567 | total × andel × (0,65 × 1/3 + 0,35 × 1,0) |

**VP + FV hybrid:** ~65 % baslast på VP (×1/3) + ~35 % spets på fjärrvärme (×1,0).

**Viktigt om energiinmatning:** VP-faktorn ×1/3 gäller när inmatat energivärde är **levererad värme** eller beräknat värmebehov. Användaren instrueras i UI:t att ange levererad värme (MWh/år), *inte* köpt el till värmepump.

---

## 4. Energiinmatning och validering

Kalkylatorn erbjuder ett valfritt fält för känd energiförbrukning. Om fältet lämnas tomt används schablon baserat på byggnadstyp och byggår.

### Schablonvärden (kWh/m²/år)

| Byggnadstyp | Före 1950 | 1950–1975 | 1975–1995 | 1995–2010 | 2010+ |
|---|---:|---:|---:|---:|---:|
| Flerbostadshus | 185 | 165 | 130 | 100 | 70 |
| Lokaler | 150 | 150 | 150 | 150 | 150 |
| Radhus / Småhus | 130 | 130 | 130 | 130 | 130 |

### Valideringsregel

Om inmatat MWh < area × 10 / 1 000 (dvs. under 10 kWh/m²) visas ett felmeddelande och beräkningen stoppas. Gränsen skyddar mot oavsiktliga inmatningar (t.ex. kWh istället för MWh, eller el till VP istället för levererad värme).

---

## 5. Abonnemangsprissättning

Årsabonnemang beräknas som **påverkbar energi (MWh) × kr/MWh**, baserat på Optimate Score.

Lowerbound används i kalkylen (konservativ). Abonnemanget visas **ej publikt** — används enbart internt i återbetalningstidsberäkningen.

| Optimate Score | Nivå | kr/MWh (lowerbound i kalkyl) | Intervall |
|---|---|---:|---|
| ≥ 75 | Mycket hög | 140 kr | 140–180 kr |
| ≥ 55 | Hög | 100 kr | 100–140 kr |
| ≥ 35 | Medium | 70 kr | 70–100 kr |
| ≥ 15 | Låg | 40 kr | 40–70 kr |
| < 15 | Mycket låg | 0 kr | Ej rekommenderat |

**Miniminivå:** 6 000 kr/år, oavsett beräknat värde (skyddar mot extremt små fastigheter).

---

## 6. ROI-beräkning

```
Besparing/år    = påverkbar energi × 1 100 kr/MWh × besparingsprocent (mid)
Abonnemang/år   = max(6 000, påverkbar energi × kr/MWh)
Nettobesparing  = Besparing − Abonnemang
Installationskostnad = 29 000 kr (fast) + antal undercentraler × 38 500 kr
Återbetalningstid    = Installationskostnad / Nettobesparing
```

Om nettobesparing ≤ 0 visas **"—"** med texten *"Besparingen täcker ej abonnemanget — kontakta oss för analys"* istället för ett årstal.

### Besparingsprocent per Score-nivå (mid används i kalkylen)

| Optimate Score | Besparing min | Besparing max | Mid (används) |
|---|---:|---:|---:|
| ≥ 75 | 15 % | 22 % | 18,5 % |
| ≥ 50 | 10 % | 16 % | 13,0 % |
| ≥ 25 | 5 % | 10 % | 7,5 % |
| < 25 | 2 % | 5 % | 3,5 % |

---

## 7. Övriga konstanter

| Parameter | Värde |
|---|---|
| Energipris (besparingsberäkning) | 1 100 kr/MWh |
| Fast installationskostnad | 29 000 kr |
| Kostnad per undercentral | 38 500 kr |
| Årsabonnemang minimum | 6 000 kr/år |
| Valideringströskel energiinmatning | 10 kWh/m² (area × 10 / 1 000 MWh) |

---

## 8. Optimate Score-formel

Score beräknas som viktat medelvärde av tre faktorer:

| Faktor | Vikt |
|---|---:|
| Ventilationstyp | 40 % |
| Energisystem | 35 % |
| Byggår | 25 % |

### Poäng per faktor

**Ventilationstyp:**
| Typ | Poäng |
|---|---:|
| S – Självdrag | 95 |
| F – Frånluft | 80 |
| FT – Från- och tilluft | 55 |
| FTX – Med värmeåtervinning | 30 |

**Energisystem:**
| System | Poäng |
|---|---:|
| Fjärrvärme | 80 |
| Elpanna | 75 |
| VP + FV hybrid | 65 |
| VP äldre | 55 |
| VP modern | 25 |

**Byggår:**
| Ålder | Poäng |
|---|---:|
| Före 1950 | 90 |
| 1950–1975 | 85 |
| 1975–1995 | 75 |
| 1995–2010 | 50 |
| 2010+ | 25 |

---

## 9. Öppna frågor / framtida versioner

| Fråga | Status |
|---|---|
| Lokaler × byggår | Ej implementerat i v1 — verksamhetstyp viktigare än byggår |
| Restaurang/storkök/bad som beräkningsbar lokaltyp | Ej implementerat — kräver separat kalkylmodell |
| Visa abonnemangspris publikt | Beslutat: visas ej, används endast internt |
| VP: skilja på köpt el vs. levererad värme | Hanteras via UI-text; ×1/3 alltid för VP i nuvarande version |
