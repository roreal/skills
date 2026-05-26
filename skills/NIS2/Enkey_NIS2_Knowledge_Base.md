# Enkey Building Insight® — NIS2, OT, IoT och Secure Architecture Knowledge Base

## Syfte

Detta dokument sammanfattar kunskap, resonemang och arkitekturprinciper kring:
- NIS2
- OT/IoT-säkerhet
- M-Bus
- Modbus
- LoRaWAN
- Edge-arkitektur
- Enkey Building Insight®

Dokumentet är strukturerat för att kunna användas som:
- AI-kunskapsbas
- RAG-underlag
- intern teknisk referens
- workshopmaterial
- kravspecifikation
- presentationsunderlag

---

# 1. Övergripande slutsats

M-Bus och Modbus är inte i sig NIS2-kompatibla protokoll.

De är däremot fullt användbara i en NIS2-kompatibel arkitektur om de:
- isoleras
- termineras säkert
- kapslas bakom moderna säkerhetslager
- övervakas
- valideras

LoRaWAN skiljer sig tydligt från klassiska OT-protokoll eftersom LoRaWAN innehåller:
- AES-128 kryptering
- autentisering
- replay-skydd
- message integrity
- session keys

Det gör LoRaWAN till ett modernare “secure-by-design”-protokoll.

---

# 2. NIS2 — centrala säkerhetsprinciper

NIS2 fokuserar på:

- Riskbaserad säkerhet
- Zero Trust
- Least privilege
- Segmentering
- Incidentdetektion
- Incidentrapportering
- Kontinuitet och resiliens
- Leverantörskedjesäkerhet
- Logging och spårbarhet
- Återställningsförmåga

---

# 3. Problem med M-Bus och Modbus ur NIS2-perspektiv

## 3.1 Trusted network-antagande

Både M-Bus och Modbus designades för:
- slutna nät
- betrodda miljöer
- frånvaro av angripare

Detta bryter mot moderna Zero Trust-principer.

---

## 3.2 Ingen autentisering

M-Bus och Modbus saknar inbyggd:
- användarautentisering
- enhetsautentisering
- sessionskontroll

Konsekvens:
- vem som helst på nätet kan potentiellt läsa eller skriva data

---

## 3.3 Ingen kryptering

Trafiken är normalt okrypterad.

Risker:
- sniffning
- dataläckage
- replay-attacker
- manipulering

---

## 3.4 Ingen kryptografisk integritet

CRC skyddar endast mot transmissionsfel.

Det finns normalt inget:
- MAC-skydd
- signering
- kryptografisk integritetskontroll

---

## 3.5 Ingen rollbaserad accesskontroll

Ingen separation mellan:
- read
- write
- admin
- operator

---

## 3.6 Ingen säker sessionshantering

Saknar:
- sessioner
- tokens
- timeout
- replay protection

---

## 3.7 Bristande logging och audit trail

Protokollen innehåller normalt inte:
- audit trail
- säker loggning
- användarspårning

---

## 3.8 Ingen säker device identity

Enheter identifieras typiskt via:
- adress
- ID
- slave address

Inte via:
- certifikat
- PKI
- kryptografisk identitet

---

## 3.9 Risk för lateral movement

När M-Bus eller Modbus kopplas till IP-nät skapas nya attackytor.

Exempel:
- OT → IT
- IT → OT
- gateway pivoting

---

## 3.10 Ingen DoS-säkerhet

Protokollen saknar normalt:
- rate limiting
- flood protection
- DoS-skydd

---

# 4. LoRaWAN — säkerhetsmässig skillnad

LoRaWAN är betydligt modernare än M-Bus och Modbus.

## Inbyggda säkerhetsfunktioner

- AES-128 kryptering
- MIC (Message Integrity Code)
- OTAA-authentication
- Session keys
- Replay protection
- Device keys

---

# 5. Viktig skillnad — LoRa vs LoRaWAN

## LoRa
Är endast radio/modulation.

## LoRaWAN
Är nätverks- och säkerhetsprotokollet ovanpå LoRa.

Det är LoRaWAN som innehåller:
- kryptering
- autentisering
- frame counters
- säkerhetsmodellen

---

# 6. Varför LoRaWAN ändå inte automatiskt är NIS2-säkert

## 6.1 Nyckelhantering

Säkerheten beror på:
- AppKey
- NwkKey
- session keys

Problem uppstår om:
- nycklar återanvänds
- lagras osäkert
- delas mellan system

---

## 6.2 Svaga implementationer

Vanliga problem:
- ABP istället för OTAA
- statiska nycklar
- dålig rotation
- ingen secure element

---

## 6.3 Gatewayn är ofta svagaste länken

LoRaWAN skyddar främst:
- sensor ↔ network server

Men:
- gateway ↔ backend
är ofta svagare skyddad.

Exempel:
- osäker MQTT
- dåliga API-nycklar
- ingen mTLS

---

## 6.4 Metadata är inte krypterad

Payload är krypterad men metadata kan avslöja:
- trafikmönster
- närvaro
- aktivitet

---

## 6.5 Tillgänglighet och störning

LoRaWAN är fortfarande radiobaserat och kan:
- störas
- jammas

NIS2 fokuserar starkt på:
- availability
- resiliency

---

# 7. Rekommenderad säkerhetsmodell för Enkey

## Grundprincip

Legacy OT skall aldrig exponeras direkt.

---

# 8. Rekommenderad zonindelning

## Zon 1 — Legacy OT

Exempel:
- M-Bus
- Modbus RTU
- äldre BACnet
- RS485

Dessa skall betraktas som:
“Implicit insecure”.

---

## Zon 2 — Secure IoT / Edge

Exempel:
- LoRaWAN
- MQTT/TLS
- OPC UA
- BACnet/SC
- HTTPS API

Dessa är:
“Secure-by-design”.

---

## Zon 3 — Gateway / Edge

Funktion:
- terminering
- normalisering
- protokollöversättning
- säkerhetskontroll

Exempel:
- PiiGAB 900
- EG71
- Docker Edge

---

## Zon 4 — Kommunikation

Rekommendation:
- TLS 1.3
- mTLS
- VPN/IPsec
- segmentering
- IDS/IPS

---

## Zon 5 — Core / EBI

Funktioner:
- datalake
- analys
- anomaly detection
- command & control
- API integration
- audit trail

---

# 9. Enkey-specifika säkerhetsrekommendationer

## 9.1 Isolera legacy OT

- VLAN
- separata nät
- inga transparenta routningar

---

## 9.2 Använd gateway som trust boundary

Gateway skall:
- terminera osäkra protokoll
- autentisera uppströms
- använda TLS/mTLS

---

## 9.3 Zero Trust ovanför OT

All logik skall:
- verifiera data
- aldrig implicit lita på OT-data

---

## 9.4 Datavalidering

Valida-konceptet är strategiskt viktigt.

Exempel:
- sanity checks
- anomaly detection
- AI/ML-validering

---

## 9.5 Command hardening

Särskilt viktigt för Demand Response.

Rekommendationer:
- whitelist
- tidsbegränsningar
- rollback
- fallback-lägen

---

# 10. Edge-arkitektur

## Koncept

Edge används för:
- lokal intelligens
- resiliency
- buffring
- lokal reglering

---

## Exempel — EG71 + Docker

Möjliga funktioner:
- lokal datalagring
- watchdog
- lokal reglerlogik
- protokollöversättning
- fallback drift

---

# 11. MQTT och säker kommunikation

Rekommendation:
- MQTT över TLS 1.3
- mTLS
- certifikatbaserad auth

---

# 12. Rekommenderade säkerhetsfunktioner

## Gateway / Edge

- Secure boot
- Certifikat
- Watchdog
- Lokal buffer
- Fail-safe mode
- Rate limiting

---

## Core / EBI

- RBAC
- MFA
- SIEM integration
- Audit trail
- Backup
- DR-plan

---

# 13. Strategisk positionering för Enkey

En stark positionering är:

“Enkey möjliggör modernisering av legacy OT genom att kombinera äldre fältbussar med moderna secure-by-design IoT-lager.”

---

# 14. Viktiga budskap mot marknaden

## Enkey kan positioneras mot:

- NIS2
- EPBD
- ISO27001
- cybersäkerhet
- ESG
- GRESB
- kommuner
- kritisk infrastruktur
- större fastighetsägare

---

# 15. Viktiga begrepp

## Legacy OT
Äldre protokoll utan inbyggd säkerhet.

## Secure IoT Overlay
Modernt säkerhetslager ovanpå äldre OT.

## Trust Boundary
Punkt där säkerhetsmodell förändras.

## Zero Trust
Ingen implicit tillit.

## Secure-by-design
Säkerhet inbyggd från början.

---

# 16. Rekommenderad arkitektur för Enkey Building Insight®

## Dataflöde

Legacy OT:
M-Bus / Modbus

↓

Gateway / Edge:
PiiGAB / EG71

↓

Säker transport:
MQTT TLS / VPN

↓

Core:
Enkey Building Insight®

↓

Integration:
BI / API / Fastighetssystem

---

# 17. Sammanfattning

## M-Bus och Modbus

Är:
- osäkra protokoll
- men användbara i säker arkitektur

## LoRaWAN

Är:
- modernt
- secure-by-design
- betydligt bättre säkerhetsmässigt

## Enkeys strategi

Bör vara:
- secure overlay
- segmentering
- edge intelligence
- zero trust
- datavalidering
- säker gateway-arkitektur

