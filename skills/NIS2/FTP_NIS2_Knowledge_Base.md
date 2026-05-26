# FTP och NIS2 — Knowledge Base

## Syfte

Detta dokument beskriver:
- FTP ur ett NIS2-perspektiv
- skillnader mellan FTP, FTPS och SFTP
- risker
- rekommendationer
- relevans för OT/IoT och Enkey Building Insight®

Dokumentet är strukturerat för:
- AI-kunskapsbas
- RAG
- cybersäkerhetsworkshops
- OT/IoT-arkitektur
- NIS2-positionering

---

# 1. Övergripande slutsats

Klassisk FTP är i princip oförenligt med moderna NIS2-principer.

FTP bör betraktas som:
- legacy insecure protocol
- pre-zero-trust
- okrypterad transport

Det kan jämföras med:
- Telnet
- HTTP utan TLS
- okrypterad Modbus TCP

---

# 2. Vad är FTP?

FTP = File Transfer Protocol

Designat:
- 1971
- långt före moderna cybersäkerhetskrav

FTP utvecklades för:
- betrodda nätverk
- slutna miljöer
- låg hotbild

---

# 3. NIS2-perspektiv på FTP

NIS2 fokuserar på:
- konfidentialitet
- integritet
- autenticitet
- resiliency
- incidentdetektion
- säker åtkomst
- state-of-the-art security

Klassisk FTP uppfyller inte dessa krav.

---

# 4. Problem med FTP ur NIS2-perspektiv

## 4.1 Klartextlösenord

FTP skickar:
- användarnamn
- lösenord

i klartext.

Risk:
- credential theft
- sniffning
- lateral movement

---

## 4.2 Okrypterad data

All data skickas okrypterat.

Exempel:
- konfigurationer
- firmware
- loggar
- backupdata

Risk:
- dataläckage
- MITM-attacker

---

## 4.3 Ingen integritetssäkring

FTP verifierar normalt inte:
- om filer manipulerats
- om data modifierats

Risk:
- filmanipulation
- falska firmwarefiler
- sabotage

---

## 4.4 Ingen modern autentisering

FTP saknar normalt stöd för:
- MFA
- certifikat
- SSO
- federerad identitet

---

## 4.5 Komplex portmodell

FTP använder:
- kontrollkanal
- dynamiska dataportar

Konsekvenser:
- svår segmentering
- svårare brandväggsregler
- svårare IDS/IPS

---

## 4.6 Bristande auditability

Många FTP-servrar saknar:
- central logging
- SIEM-integration
- detaljerad audit trail

NIS2 kräver:
- incidentspårning
- forensik
- auditability

---

## 4.7 Hög ransomware-risk

FTP används ofta för:
- backup
- filutbyte
- automation

Det gör FTP-servrar till attraktiva mål.

---

# 5. Skillnad mellan FTP, FTPS och SFTP

## 5.1 Klassisk FTP

### Egenskaper

- ingen kryptering
- klartextlösenord
- ingen integritetssäkring

### NIS2-bedömning

Ej rekommenderat.
Bör fasas ut.

---

## 5.2 FTPS

### Vad är FTPS?

FTP + TLS.

### Fördelar

- TLS-kryptering
- certifikat
- bättre säkerhet

### Problem kvarstår

- komplex portmodell
- svår segmentering
- komplicerade brandväggsregler

### NIS2-bedömning

Acceptabelt men legacy-orienterat.

---

## 5.3 SFTP

### Viktig skillnad

SFTP är inte FTP.

SFTP = SSH File Transfer Protocol

### Säkerhetsfördelar

- kryptering
- stark autentisering
- integritetsskydd
- en enda port
- stöd för nyckelbaserad auth
- bra logging

### NIS2-bedömning

SFTP är normalt fullt acceptabelt i moderna miljöer.

---

# 6. FTP i OT- och IoT-miljöer

FTP förekommer fortfarande i:
- PLC-system
- BMS-system
- gateways
- SCADA
- energisystem
- äldre fastighetssystem

Vanliga användningsområden:
- firmwareuppladdning
- loggexport
- backup
- konfigurationsfiler

---

# 7. Relevans för Enkey

## Rekommenderad policy

Undvik:
- FTP
- anonym FTP
- okrypterade filöverföringar

## Rekommenderade alternativ

### Säker filöverföring

- SFTP
- SCP
- HTTPS upload
- HTTPS API

### Säker kommunikation

- MQTT TLS 1.3
- mTLS
- VPN
- WireGuard
- IPsec

---

# 8. Rekommenderad säkerhetsarkitektur

## Fältnivå

Legacy:
- M-Bus
- Modbus
- äldre OT

## Edge/Gateway

- Docker
- lokal buffring
- certifikat
- secure boot
- watchdog

## Transport

- MQTT TLS
- HTTPS
- VPN

## Filöverföring

Tillåt:
- SFTP
- SCP
- HTTPS API

Undvik:
- FTP

---

# 9. Strategisk slutsats

FTP tillhör samma kategori som:
- Telnet
- okrypterad Modbus
- äldre BACnet/IP
- HTTP utan TLS

Alltså:
“Historiskt funktionella protokoll utan modern säkerhetsmodell.”

---

# 10. Rekommenderad säkerhetsprincip

Legacy-protokoll får:

✅ existera lokalt  
✅ isoleras  
✅ termineras säkert  

Men de får inte:

❌ exponeras direkt mot Internet  
❌ routas transparent mellan zoner  
❌ användas utan kompensatoriska skydd  

---

# 11. Rekommenderad Enkey-positionering

“Enkey moderniserar legacy OT genom att kombinera äldre fastighetsprotokoll med moderna secure-by-design kommunikationslager och NIS2-anpassad arkitektur.”

---

# 12. Sammanfattning

| Protokoll | Säkerhetsnivå | NIS2-lämplighet |
|---|---|---|
| FTP | Låg | ❌ Dålig |
| FTPS | Medel | ⚠️ Acceptabel |
| SFTP | Hög | ✅ Bra |
| HTTPS API | Hög | ✅ Mycket bra |
| MQTT/TLS | Hög | ✅ Mycket bra |

---

# 13. Viktiga begrepp

## Legacy insecure protocol
Äldre protokoll utan modern säkerhetsmodell.

## Secure-by-design
Säkerhet integrerad från början.

## Zero Trust
Ingen implicit tillit mellan system.

## Trust boundary
Punkt där säkerhetsmodell förändras.

## Compensating controls
Kompenserande säkerhetsåtgärder runt osäkra protokoll.
