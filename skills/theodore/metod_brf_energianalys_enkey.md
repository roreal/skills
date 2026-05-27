# Metod för analys av bostadsrättsföreningars energianvändning
## Enkey – Schablonmodell för fjärrvärme, varmvatten och optimeringspotential

## Syfte

Denna metod används för att snabbt uppskatta:
- fjärrvärmeanvändning
- energikostnader
- effektprofil
- varmvattenandel
- möjlig besparingspotential
- ekonomisk potential för Enkeys tjänster

Modellen är avsedd som:
- säljkalkyl
- benchmark
- CTA-underlag på webbsida
- första energibedömning innan platsbesök eller förstudie

---

# 1. Grundläggande indata

Följande information används i första hand:

| Parameter | Källa |
|---|---|
| BOA (bostadsarea) | Booli / årsredovisning |
| LOA (lokalarea) | Booli / årsredovisning |
| Energideklaration | Energiprestanda kWh/m² |
| Uppvärmningssystem | Fjärrvärme / värmepump |
| Antal lägenheter | Årsredovisning |
| Byggår | Årsredovisning |
| Eventuell lokalandel | Årsredovisning |

---

# 2. Schablon för energianvändning

Om faktisk energistatistik saknas används schablonvärden.

## Typiska nivåer för BRF i Stockholm

| Byggnadstyp | Total energianvändning |
|---|---:|
| Nyproducerad BRF | 70–100 kWh/m² |
| Moderniserad BRF | 100–140 kWh/m² |
| Normal äldre BRF | 140–180 kWh/m² |
| Äldre ineffektiv BRF | 180–240 kWh/m² |

---

# 3. Uppdelning mellan varmvatten och rumsvärme

Standardantagande:

\[
30\% = tappvarmvatten
\]

\[
70\% = rumsvärme
\]

Detta används eftersom:
- varmvatten är relativt konstant över året
- rumsvärme är starkt vinterberoende
- effektavgifter främst drivs av rumsvärme

---

# 4. Beräkning av fjärrvärme

## Formel

\[
\text{Årsenergi} =
\text{Area} \times \text{kWh/m²}
\]

Exempel:

- BOA = 2 500 m²
- Energiprestanda = 150 kWh/m²

\[
2\,500 \times 150 =
375\,000\ \text{kWh}
\]

\[
=
375\ \text{MWh/år}
\]

---

# 5. Fördelning VV / rumsvärme

## Exempel

Total energi:

\[
375\ \text{MWh}
\]

### Varmvatten

\[
375 \times 0.30 =
112.5\ \text{MWh}
\]

### Rumsvärme

\[
375 \times 0.70 =
262.5\ \text{MWh}
\]

---

# 6. Genomsnittligt fjärrvärmepris

## Stockholm Exergi – schablon

| Fastighetstyp | Typiskt totalpris |
|---|---:|
| Stor effektiv BRF | 0,85–0,95 kr/kWh |
| Normal BRF | 0,95–1,10 kr/kWh |
| Liten / effekttung BRF | 1,10–1,35 kr/kWh |

## Rekommenderat kalkylvärde

\[
1.0\ \text{kr/kWh}
\]

inklusive:
- energi
- effekt
- fasta avgifter

---

# 7. Beräkning av årlig fjärrvärmekostnad

## Formel

\[
\text{Årskostnad} =
\text{Årsenergi} \times \text{kr/kWh}
\]

Exempel:

\[
375\,000 \times 1.0 =
375\,000\ \text{kr/år}
\]

---

# 8. Klassificering av BRF-storlek

| Klass | Fjärrvärme |
|---|---:|
| Liten | < 300 MWh |
| Medelstor | 300–1 000 MWh |
| Stor | 1 000–3 000 MWh |
| Mycket stor | > 3 000 MWh |

Alternativt:

| Klass | Lägenheter |
|---|---:|
| Liten | < 40 |
| Medelstor | 40–120 |
| Stor | 120–350 |
| Mycket stor | > 350 |

---

# 9. Identifiering av Optimate-potential

## Hög potential

Indikationer:
- hög energianvändning
- äldre byggnad
- klagomål på värme
- hög returtemperatur
- stora effekttoppar
- övertemperatur vintertid
- ojämn temperatur mellan lägenheter

## Typisk möjlig besparing

| Åtgärd | Besparing |
|---|---:|
| Framledningsoptimering | 5–15 % |
| Pumpstopp | 2–8 % |
| Temperaturreduktion | 3–10 % |
| Demand/Response | 2–15 % effektkostnad |

---

# 10. Viktig observation kring varmvatten

En hög varmvattenandel:
- ger jämnare energiprofil
- minskar effektproblematik
- förbättrar fjärrvärmeekonomi per kWh

Detta innebär att:
- stora BRF:er ofta får lägre verkligt genomsnittspris
- små BRF:er ofta har högre kostnad per kWh

---

# 11. Rekommenderad analysprocess

## Steg 1

Hämta:
- BOA
- LOA
- antal lägenheter
- byggår

från:
- Booli
- årsredovisning
- energideklaration

## Steg 2

Identifiera:
- fjärrvärme eller värmepump
- energiprestanda
- eventuella lokaler

## Steg 3

Beräkna:
- total energi
- varmvattenandel
- rumsvärmeandel

## Steg 4

Applicera:
- schablonpris fjärrvärme
- möjlig besparing
- uppskattad payback

## Steg 5

Bedöm:
- potential för Optimate
- potential för Demand/Response
- behov av mätning/sensorik

---

# 12. Exempel – Typisk BRF

| Parameter | Värde |
|---|---:|
| BOA | 2 500 m² |
| Energiprestanda | 150 kWh/m² |
| Årsenergi | 375 MWh |
| VV-andel | 112 MWh |
| Rumsvärme | 263 MWh |
| Fjärrvärmekostnad | 375 000 kr/år |

## Möjlig besparing

Vid 10 % reduktion:

\[
37\,500\ \text{kr/år}
\]

---

# 13. Rekommendation för Enkeys kalkylator

Låt användaren ange:

- byggnadstyp
- area
- energiförbrukning (om känd)
- fjärrvärme eller värmepump
- antal lägenheter

Om energianvändning saknas:
- uppskatta automatiskt med schabloner

Målet är:
- låg tröskel
- snabb CTA
- enkel uppskattning
- försäljningsdrivande resultat

