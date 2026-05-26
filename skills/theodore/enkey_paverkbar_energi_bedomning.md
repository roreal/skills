# Bedömning av antaganden för påverkbar energi i Enkeys kalkylator

## Syfte

Detta dokument sammanfattar bedömning, slutsatser och förbättringsförslag för matrisen:

**Kalkylator — Påverkbar Energi: Parametrar och Matriser**

Målet är att göra kalkylmodellen tillräckligt robust för en publik CTA-kalkylator på Enkeys webbplats, utan att ge en falsk precision eller systematiskt överskatta den energi som Optimate® faktiskt kan påverka.

---

## 1. Samlad bedömning

Matrisen är i huvudsak en bra första version. Grundprincipen är korrekt:

> **Påverkbar energi = den del av fastighetens energianvändning som Optimate® faktiskt kan påverka, främst rumsvärme/transmission/radiatorvärme.**

Tappvarmvatten och separat ventilationsvärme bör normalt exkluderas.

Den viktigaste slutsatsen är dock att modellen behöver förtydligas på tre punkter innan den används publikt:

1. **Terminologi för ventilationssystem**
2. **Logik för värmepumpar**
3. **Försiktigare standardvärden i vissa fall, särskilt lokaler och FT-system**

---

## 2. Övergripande styrkor i modellen

### 2.1 Rätt angreppssätt

Det är korrekt att inte räkna hela energianvändningen som påverkbar. En Optimate-kalkyl bör inte baseras på total fjärrvärme, total el eller total köpt energi utan på den del som faktiskt påverkas av styrning av värmesystemet.

### 2.2 Bra uppdelning mellan bostäder och lokaler

Flerbostadshus och lokaler bör separeras. De har olika energiprofil:

- Flerbostadshus har ofta betydande tappvarmvattenandel.
- Lokaler har ofta låg tappvarmvattenandel men högre ventilationsandel.
- Lokaler varierar mer med verksamhetstyp än med byggår.

### 2.3 FTX-antagandena för flerbostadshus är rimliga

FTX-tabellen i underlaget är väl avvägd och kan i princip behållas.

---

## 3. Viktigaste riskerna

## 3.1 Risk 1 — Begreppet “påverkbar energi” kan feltolkas

Det måste vara tydligt att påverkbar energi inte är samma sak som:

- total energianvändning,
- köpt energi,
- levererad värme,
- energiprestanda enligt energideklaration,
- eller total värmekostnad.

I kalkylatorn bör definitionen vara konsekvent:

> **Påverkbar energi är den del av värmeenergin som avser rumsvärme och som kan påverkas genom optimerad styrning.**

---

## 3.2 Risk 2 — Värmepumpsjusteringen kan bli fel

Detta är den största metodrisken.

I nuvarande modell multipliceras påverkbar energi för värmepumpar med cirka 1/3, baserat på COP ≈ 3.

Det är bara korrekt om användaren matar in **levererad värmeenergi** eller ett uppskattat värmebehov före värmepumpens COP.

Om användaren däremot matar in **köpt el till värmepumpen**, är energin redan reducerad av COP. Då ska man inte multiplicera med 1/3 igen.

### Rekommenderad princip

| Inmatad energi | Exempel | Rekommenderad faktor |
|---|---|---:|
| Köpt fjärrvärme | Faktura fjärrvärme | × 1,0 |
| Köpt el till elpanna | Elmätning elpanna | × 1,0 |
| Köpt el till värmepump | Elmätning VP | × 1,0 |
| Levererad värme från värmepump | Värmemängdsmätare efter VP | × 1/COP |
| Uppskattat värmebehov före energisystem | Schablon eller beräkning | × 1/COP |

### Rekommendation

Kalkylatorn bör fråga:

> **Vilken typ av energi anger du?**

Förslag på val:

1. Köpt energi från faktura
2. Levererad värmeenergi
3. Vet ej — uppskatta från byggnadstyp och area

För en första publik version är det enklast att styra användaren mot:

> **Ange årlig köpt energi för värme och varmvatten. Ange inte hushållsel eller verksamhetsel.**

Då måste värmepumpslogiken hanteras försiktigt.

---

## 3.3 Risk 3 — FX används sannolikt fel

I underlaget används begreppet:

> FX — tilluft utan värmeåtervinning

Det bör sannolikt bytas till:

> **FT — från- och tilluft utan värmeåtervinning**

Vanlig svensk terminologi:

| Beteckning | Betydelse |
|---|---|
| S | Självdrag |
| F | Frånluft |
| FT | Från- och tilluft utan värmeåtervinning |
| FTX | Från- och tilluft med värmeåtervinning |
| FX | Används ofta för frånluft med värmeåtervinning, exempelvis frånluftsvärmepump |

### Rekommendation

Byt rubriken **FX** till **FT utan värmeåtervinning**, om det är det som avses.

---

## 4. Bedömning av flerbostadshus och radhus

## 4.1 Självdrag och frånluft

Nuvarande antaganden:

| Åldersgrupp | VV | Ventilation | Påverkbar rumsvärme |
|---|---:|---:|---:|
| Äldre | 20 % | 0 % | 80 % |
| Normal | 25 % | 0 % | 75 % |
| Nyare | 32 % | 0 % | 68 % |

### Bedömning

Värdena är rimliga, men kommentaren bör ändras.

Det är inte korrekt att säga att ventilationen inte har någon värmepåverkan. Självdrag och frånluft kan ge stora värmeförluster. Däremot finns normalt ingen separat ventilationsvärme som ska exkluderas.

Ventilationsförlusterna täcks i stället av byggnadens vanliga värmesystem och ingår därför praktiskt i rumsuppvärmningen.

### Rekommenderad kommentar

> **Ingen separat ventilationsvärme antas. Ventilationsförluster ingår i rumsuppvärmningen.**

### Rekommendation

Behåll värdena:

| Ventilation | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| S/F | 80 % | 75 % | 68 % |

---

## 4.2 FT utan värmeåtervinning

Nuvarande antaganden:

| Åldersgrupp | VV | Ventilation | Påverkbar rumsvärme |
|---|---:|---:|---:|
| Äldre | 22 % | 15 % | 63 % |
| Normal | 27 % | 13 % | 60 % |
| Nyare | 33 % | 10 % | 57 % |

### Bedömning

Antagandena är inte orimliga, men något optimistiska om tilluften värms med separat ventilationsbatteri som Optimate inte styr.

För en publik kalkylator bör modellen hellre vara något konservativ än för offensiv.

### Rekommenderad försiktig version

| System | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| FT utan värmeåtervinning | 60 % | 57 % | 54 % |

### Alternativ intern version

Om ventilationen inte är separat debiterbar eller om ventilationsvärmen i praktiken belastar samma värmesystem som Optimate påverkar kan ursprungliga värden användas internt:

| System | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| FT utan värmeåtervinning, intern kalkyl | 63 % | 60 % | 57 % |

---

## 4.3 FTX med värmeåtervinning

Nuvarande antaganden:

| Åldersgrupp | VV | Ventilation | Påverkbar rumsvärme |
|---|---:|---:|---:|
| Äldre | 25 % | 10 % | 65 % |
| Normal | 30 % | 10 % | 60 % |
| Nyare | 38 % | 8 % | 54 % |

### Bedömning

Detta är den starkaste delen av matrisen.

Antagandena är väl avvägda:

- Äldre eller sämre injusterade FTX-hus får högre påverkbar rumsvärmeandel.
- Normal FTX-drift hamnar kring 60 % påverkbar rumsvärme.
- Nyare energieffektiva FTX-hus får högre relativ andel tappvarmvatten och lägre påverkbar rumsvärmeandel.

### Rekommendation

Behåll tabellen:

| System | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| FTX | 65 % | 60 % | 54 % |

---

## 5. Bedömning av lokaler

Nuvarande antaganden:

| Lokaltyp | VV | Ventilation | Påverkbar rumsvärme |
|---|---:|---:|---:|
| Kontor standard | 5 % | 30 % | 65 % |
| Kontor minimal VV | 2,5 % | 27,5 % | 70 % |
| Skola / vård / gym | 10 % | 37 % | 53 % |
| Restaurang / storkök / bad | — | — | Ej implementerad |

### Bedömning

Strukturen är bra. Lokaler bör delas upp efter verksamhetstyp snarare än byggår i första versionen.

I lokaler är varmvatten ofta en liten post, särskilt i kontor. Ventilationen kan däremot vara en stor post, särskilt vid hög personbelastning, långa drifttider eller höga luftflöden.

### Rekommendation

Inför en **lokaltyp-dropdown** i kalkylatorn.

Föreslagna val:

1. Kontor / butik / lätt lokal
2. Kontor med låg varmvattenanvändning
3. Skola / vård / gym / hög personbelastning
4. Varmvattenintensiv lokal — kräver separat bedömning

### Rekommenderad publik matris

| Lokaltyp | Påverkbar andel | Kommentar |
|---|---:|---|
| Kontor standard | 60 % | Försiktig publik schablon |
| Kontor minimal VV | 70 % | Rimligt om ingen dusch/storkök finns |
| Skola / vård / gym | 50–55 % | Beror mycket på luftflöde och drifttid |
| Restaurang / bad / storkök | Ej standard | Bör inte schablonberäknas i första version |

### Intern matris

| Lokaltyp | Påverkbar andel | Kommentar |
|---|---:|---|
| Kontor standard | 65 % | Kan användas internt vid kvalificerad dialog |
| Kontor minimal VV | 70 % | Rimligt |
| Skola / vård / gym | 53 % | Rimligt |
| Restaurang / bad / storkök | Separat kalkyl | VV och processvärme kan dominera |

---

## 6. Ska lokaler variera med byggår?

### Bedömning

Inte i första versionen.

För lokaler påverkas energianvändningen ofta mer av:

- verksamhetstyp,
- ventilationsflöden,
- drifttider,
- internlaster,
- krav på luftkvalitet,
- duschar/kök/processer,
- och styrstrategi,

än av byggår.

Byggår kan ge viss information om klimatskal och teknisk standard, men i en enkel CTA-kalkylator riskerar det att skapa falsk precision.

### Rekommendation

Håll lokaler enkla i version 1:

> **Lokaltyp är viktigare än byggår.**

Byggår kan eventuellt införas i en senare, mer avancerad version.

---

## 7. Ska restaurang, storkök och bad implementeras?

### Bedömning

Inte som vanlig schablon i första versionen.

Dessa verksamheter kan ha:

- mycket hög tappvarmvattenanvändning,
- processvärme,
- hög ventilation,
- frånluft med särskilda krav,
- kyl- och värmeprocesser,
- och energiflöden som inte liknar kontor eller normala lokaler.

### Rekommendation

Visa hellre ett särskilt meddelande:

> **Denna lokaltyp kräver separat bedömning. Kontakta Enkey för en anpassad analys.**

Det kan fungera bra som CTA i stället för att ge en osäker schablon.

---

## 8. Rekommenderad justerad huvudmatris

## 8.1 Flerbostadshus och radhus

| Ventilationssystem | Äldre | Normal | Nyare | Kommentar |
|---|---:|---:|---:|---|
| S/F | 80 % | 75 % | 68 % | Ventilationsförluster ingår i rumsuppvärmning |
| FT utan återvinning | 60 % | 57 % | 54 % | Försiktig publik schablon |
| FTX | 65 % | 60 % | 54 % | Rimlig schablon |

---

## 8.2 Lokaler

| Lokaltyp | Publik schablon | Intern schablon | Kommentar |
|---|---:|---:|---|
| Kontor standard | 60 % | 65 % | Normal kontorslokal |
| Kontor minimal VV | 70 % | 70 % | Låg varmvattenanvändning |
| Skola / vård / gym | 50–55 % | 53 % | Hög personbelastning och ventilation |
| Restaurang / bad / storkök | Ej standard | Separat kalkyl | Bör inte schablonberäknas |

---

## 9. Rekommenderade formuleringar i kalkylatorn

### 9.1 Definition av påverkbar energi

> **Påverkbar energi är den del av byggnadens värmeanvändning som avser rumsvärme och som kan påverkas genom optimerad styrning. Tappvarmvatten, verksamhetsel och separat ventilationsvärme ingår normalt inte.**

### 9.2 För användarens energiinmatning

> **Ange årlig köpt energi för värme och varmvatten. Ange inte hushållsel eller verksamhetsel.**

### 9.3 För värmepump

> **Om energin avser levererad värme från värmepumpen justeras kalkylen med antagen COP. Om energin avser köpt el till värmepumpen görs ingen extra COP-justering.**

### 9.4 För lokaler med hög varmvatten- eller processenergi

> **Denna lokaltyp kräver separat bedömning eftersom tappvarmvatten, processvärme och ventilation kan dominera energibalansen.**

---

## 10. Rekommenderade beslut

| Fråga | Rekommendation |
|---|---|
| Ska S/F-värdena 80/75/68 % behållas? | Ja, men ändra kommentaren |
| Ska FX-kolumnen behållas? | Nej, byt till FT om det är tilluft utan återvinning |
| Ska FT-värdena justeras? | Ja, använd 60/57/54 % publikt |
| Ska FTX-värdena behållas? | Ja |
| Ska lokaltyp-dropdown införas? | Ja |
| Ska lokaler variera med byggår? | Nej, inte i version 1 |
| Ska restaurang/storkök/bad implementeras? | Inte som vanlig schablon; använd separat bedömning |
| Ska VP-faktorn ×1/3 användas generellt? | Nej, bara när inmatad energi är levererad värme eller uppskattat värmebehov före COP |
| Ska publika värden vara konservativa? | Ja |

---

## 11. Slutsats

Matrisen är tillräckligt bra för att ligga till grund för en första version av Enkeys kalkylator, men bör justeras innan publicering.

De viktigaste ändringarna är:

1. Byt **FX** till **FT**, om systemet avser från- och tilluft utan värmeåtervinning.
2. Förtydliga att S/F-systemens ventilationsförluster ingår i rumsuppvärmningen.
3. Inför lokaltyp som dropdown för lokaler.
4. Använd inte byggår för lokaler i första versionen.
5. Hantera värmepumpar beroende på om användaren matar in köpt el eller levererad värme.
6. Använd försiktigare publika schabloner än interna säljkalkyler.

Min rekommenderade huvudmodell för version 1 är:

### Flerbostadshus

| System | Äldre | Normal | Nyare |
|---|---:|---:|---:|
| S/F | 80 % | 75 % | 68 % |
| FT utan återvinning | 60 % | 57 % | 54 % |
| FTX | 65 % | 60 % | 54 % |

### Lokaler

| Lokaltyp | Påverkbar andel |
|---|---:|
| Kontor standard | 60 % |
| Kontor minimal VV | 70 % |
| Skola / vård / gym | 50–55 % |
| Restaurang / bad / storkök | Separat bedömning |

Detta ger en kalkylator som är enkel nog för en CTA, men tillräckligt försiktig för att inte översälja Optimate®s påverkbara energibas.
