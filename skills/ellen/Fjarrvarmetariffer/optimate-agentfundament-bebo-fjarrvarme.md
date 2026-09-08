---
title: "Agentfundament för temperatur- och kostnadsoptimering av fjärrvärme"
document_id: "optimate-agentfundament-bebo-fjarrvarme"
version: "1.0.0"
created: "2026-09-03"
language: "sv-SE"
purpose: "Kunskapsunderlag och föreslagen agentinstruktion för Optimate"
document_type: "Källförankrad syntes med egen teknisk tillämpning"
source_report_date: "2024-11-30"
operational_authorization: false
---

# Agentfundament för temperatur- och kostnadsoptimering av fjärrvärme

## 1. Användning och källstatus

Dokumentet är ett agentanpassat underlag med BeBo/Beloks förstudie som utgångspunkt. Det är inte en fullständig avskrift av rapporten eller en av BeBo fastställd styrstandard.

**Källgrund:** Markus Lindahl, RISE; Mette Lager, CIT Renergy; Magnus Önnheim, Fraunhofer Chalmers Centre: *Maskinläsbara prismodeller för fjärrvärme*, förstudie, version 1.0, projektnummer 2024:04, 2024-11-30. [Originalrapport, PDF](https://www.bebostad.se/media/7182/bebo-maskinl%C3%A4sbara-prismodeller-f%C3%B6r-fj%C3%A4rrv%C3%A4rme.pdf).

- **Avsnitt 2:** kort sammanfattning av rapportens bidrag.
- **Avsnitt 3–15:** egna förslag till agentbeteende, beräkningsstruktur och teknisk tillämpning för Optimate. Dessa ska inte tillskrivas rapportförfattarna.
- **Anläggningsspecifika värden:** hämtas från aktuellt avtal, driftkort, driftsättning och verifierade mätdata. Detta dokument fastställer inga generella temperaturgränser eller besparingsprocent.

Förslagen kan användas som kunskapsfil eller som grund för en agentinstruktion. De ersätter inte agentens överordnade instruktioner, befintliga driftmandat eller lokala skyddsfunktioner. Att läsa denna fil ger ingen behörighet att skriva till en anläggning.

## 2. Rapportens bidrag i korthet

Förstudien behandlar hur svenska fjärrvärmebolags företagsmodeller kan beskrivas digitalt för analys och styrning. Den grupperar debiteringen i fast avgift, kapacitet, energi och effektivitet. Skillnaderna gäller både beräkningar och villkor.

Kapacitet kan exempelvis grundas på kategorital, distributionstal, dygnsmedel, temperaturvillkor, effektsignatur, abonnerad effekt eller medelvärden över timmar och halva dygn. Rapporten skiljer också mellan mätvärden från debiteringsmätaren och andra parametrar, samt mellan uppgifter som är tillgängliga i förväg och sådana som blir kända senare.

Tre digitaliseringsalternativ diskuteras: en beräkningsfunktion som svart låda, gemensamma API:er och ontologisk modellering. Författarna föredrar det sistnämnda: gemensam betydelse för begrepp och samband, med utrymme för olika leverantörsmodeller. De föreslår harmoniserad terminologi och pilotprojekt.

Förstudien ger ett metodiskt underlag, inte en färdig produktionsmodell. Prisexemplen och marknadsandelarna är historiska.

**Läsanvisning:** kapitel 4 för kartläggning och parametrar, kapitel 5 för digital struktur, kapitel 6–7 för diskussion och slutsatser, bilaga 1 för leverantörsexempel. Sidnummer i rapportens huvuddel skiljer sig från PDF-läsarens sidnummer. [Källa: originalrapporten](https://www.bebostad.se/media/7182/bebo-maskinl%C3%A4sbara-prismodeller-f%C3%B6r-fj%C3%A4rrv%C3%A4rme.pdf).

## 3. Föreslaget uppdrag till agenten

Du analyserar och, inom tilldelat driftmandat, optimerar en fjärrvärmeanläggnings värmetillförsel. Målet är att minska kundens relevanta kostnad och undvika onödig energianvändning, med bibehållen avtalad komfort och tillåtna driftförhållanden.

Arbeta i följande ordning:

1. Fastställ anläggning, kundavtal, mätpunkter och tillåtna styrvariabler.
2. Kontrollera mätkvalitet och identifiera aktuell driftstatus.
3. Beräkna vad oförändrad styrning väntas ge för temperaturer, energianvändning och kostnader.
4. Simulera genomförbara styralternativ med samma väder, användningsantaganden och starttillstånd.
5. Välj ett alternativ som klarar driftgränser även med rimlig prognososäkerhet.
6. Redovisa åtgärd, förväntad nytta, osäkerhet och återgångsvillkor.
7. Utför endast den första tillåtna styrändringen och följ upp utfallet innan planen räknas om.

Håll isär fyra resultat: **sparad energi, förändrat effektuttag, förändrad fakturakostnad och förändrad komfort**. Ett positivt resultat inom ett område bevisar inte automatiskt ett positivt resultat inom de andra.

Kunden kan ange kostnad, energianvändning eller en kombination som mål. Dokumentera målvikterna. Miljöoptimering kräver en separat, tidsupplöst och relevant miljösignal; använd inte pris som automatiskt mått på utsläpp.

## 4. Systemgräns och temperaturer

Definiera primärsidan som fjärrvärmenätets sida av värmeväxlaren och sekundärsidan som byggnadens distributionssystem. Ange krets för varje givare och styrpunkt.

| Beteckning | Betydelse | Användning i agenten |
| --- | --- | --- |
| `T_primary_supply` | Primär framledning | Driftanalys och eventuella tariffvillkor; normalt inte kundens styrvariabel |
| `T_primary_return` | Primär retur | Avkylning och eventuell temperaturdebitering |
| `T_secondary_supply` | Sekundär framledning | Möjlig styrvariabel om regulator och mandat tillåter |
| `T_secondary_return` | Sekundär retur | Diagnostik och byggnadsmodell |
| `T_indoor_zone` | Inomhustemperatur per representativ zon | Komfortåterföring och prognoskontroll |
| `T_outdoor_actual` | Verklig utetemperatur | Byggnadsmodell och felsökning |
| `T_outdoor_forecast` | Prognostiserad utetemperatur | Framåtblickande planering |
| `T_outdoor_emulated` | Temperatur som Optimate skickar till befintlig regulator | Styrsignal, inte väderobservation |
| `T_outdoor_billing` | Den väderkälla som avtalet använder | Debiteringsberäkning när avtalet kräver det |

**Blanda aldrig emulerad temperatur med verklig utetemperatur i inlärning, normalårskorrigering eller tariffberäkning.** Logga båda med separata identiteter.

Utred vad en emulerad utetemperatur faktiskt påverkar: värmekurva, pumpstopp, frostfunktion, tidsprogram och eventuella andra kretsar. Verifiera tecken, skalning, begränsningar och återgång till ordinarie givare. Anta inte att en hög emulerad temperatur alltid stoppar en pump.

Skilj värme, tappvarmvatten, VVC och andra laster åt. Huvudmätaren kan omfatta allt, även om agenten endast styr uppvärmningen. Tariffmotorn använder avtalets mätgräns; optimeraren modellerar endast den del som faktiskt kan påverkas.

## 5. Indata och tillstånd

### 5.1 Obligatoriskt innan automatisk temperaturstyrning

| Indata | Vad som måste vara bestämt |
| --- | --- |
| Anläggningsidentitet | Nät, kund, mätare, central och styrd krets |
| Driftmandat | Tillåtna skrivpunkter, intervall, ändringshastighet och kommandots livslängd |
| Komfortprofil | Börvärde och tillåtet intervall per zon och tid; hur avvikande rum hanteras |
| Lokala skydd | Vilka spärrar och skydd som alltid har företräde |
| Återgång | Vad lokal regulator gör vid kommunikationsfel, felaktiga givare eller utgånget kommando |
| Mätdata | Tidsstämplar, enheter, sensorplacering, kvalitetsflaggor och dataluckor |
| Byggnadsmodell | Validerat giltighetsområde och osäkerhet; annars endast begränsad analys |

Skydd och gränser för tappvarmvatten/VVC, frost, ventilation och utrustning ska komma från fastställda anläggningskrav. Saknas dessa för en krets, får agenten inte använda kretsen för ekonomisk optimering.

### 5.2 Ytterligare indata för kostnadsoptimering

- Tariff-ID, giltighetsperiod, nät, kundkategori och källa.
- Momsgrund för varje belopp samt kundens avtalade beräkningsperspektiv. Anta inte full avdragsrätt för en BRF.
- Alla prisled och tillämpningsvillkor, inklusive rabatt, tillägg, effektgrupp och periodisering.
- Historik som fortfarande påverkar debiteringen, inte enbart senaste mätvärdet.
- Aktuell debiterbar kapacitet, abonnemang, tidigare toppar och nästa omräkningsdatum.
- Parametrar från leverantören, med publiceringstid och giltig mätperiod.
- Elektricitet och andra rörliga kostnader som styråtgärden påverkar, när dessa är materiella.

Lagra ett ekonomiskt tillstånd `billing_state` separat från byggnadens termiska tillstånd. En historisk topp kan fortsätta påverka fakturan efter att temperaturerna ändrats.

## 6. Koppling till Optimates tariff-JSON

Följande är ett föreslaget integrationskontrakt för katalogen `optimate-fjarrvarme-2026.json`. Filnamnet är en referens; ingen fil behöver finnas på en viss sökväg hos mottagaren.

| Befintligt fält | Agentens tolkning |
| --- | --- |
| `member_id`, `network_or_product` | Kräver säker kundkoppling; leverantörsnamn ensamt räcker inte |
| `price_status`, `valid_from`, `valid_to` | Prisets status och giltighet, inte godkännande av beräkningsmotorn |
| `vat_basis` | Beloppen ska tolkas enligt denna grund; konvertera högst en gång |
| `capacity.basis_unit` | Bevara skillnaden mellan exempelvis kW, kWh/dygn och MWh |
| `capacity.rate_period` | Prisets tidsenhet; får inte härledas från faktureringsfrekvens |
| `capacity.monthly_proration` | Hur kostnaden periodiseras; `null` är inte automatiskt 1/12 |
| `source_refs` | Spårbarhet till dokument och, där tillgängligt, sida |
| `issues`, `investigation.conditions_sv` | Kvarstående begränsningar för beräkning och användning |
| `remaining_information_requests` | Öppna frågor; `status: utreds` betyder olöst uppgift |
| `resolved_information_requests` | Enskilda lösta frågor, inte godkännande av hela tariffen |
| `production_ready` | Tekniskt beredskapsfält; får inte ignoreras av agenten |

Katalogversionen från föregående arbete markerar Kils publicerade belopp inklusive moms. Behåll den momsgrunden om den versionen används. Bekräftelsen löser momsfrågan, inte andra öppna villkor.

**Hantering av `utreds`:** Bevara frågetext, villkor, källor och alternativ. Använd inte ett gissat värde som faktureringsregel. Om en parameter påverkar styrvalet, redovisa alternativa scenarier och avstå från tariffberoende automatisk styrning tills nödvändiga delar är verifierade. Oberoende, redan godkänd komfortstyrning kan fortsätta.

Låt `null` betyda okänt. Lägg vid behov till en uttrycklig status för ”ej tillämpligt”. Använd noll endast när frånvaro av avgift eller mätstorhet faktiskt är fastställd.

## 7. Beräkningsmotor: generiska matematiska byggstenar

Detta avsnitt är en egen teknisk specifikation. Formlerna är mallar och grundläggande samband, inte leverantörsvillkor. Använd endast en mall när det aktuella avtalet överensstämmer med den.

Låt språkmodellen tolka och förklara underlag. Låt en separat deterministisk beräkningsmotor räkna kostnader. Kör aldrig fri text från PDF eller JSON med `eval`.

### 7.1 Tid och enheter

```text
E_kWh = 1000 * E_MWh
P_mean_kW = E_kWh / duration_hours
E_MWh = sum(P_mean_kW[t] * duration_hours[t]) / 1000
1 öre/kWh = 10 SEK/MWh
```

Beräkna energi från differensen mellan giltiga kumulativa mätarställningar. Hantera mätarbyte och återställning innan differensbildning. Interpolerade toppar är skattningar och ska flaggas.

Lagra tidsstämplar entydigt, gärna i UTC, och tillämpa tariffens lokala kalender. Sommartidsdygn kan ha annan faktisk längd än 24 timmar. Fastställ om avtalet använder faktiska timmar, fasta block eller särskild normalisering. Använd samma regel i historik och prognos.

### 7.2 Energi och total kostnad

```text
C_energy = sum(E_MWh[t] * price_SEK_per_MWh[t])
C_heat = C_fixed + C_capacity + C_energy + C_other_charges - C_discounts
```

En signerad bonus/avgift ska läggas till en gång, med rätt tecken. Den får inte samtidigt tas upp som separat rabatt.

För en tariff som faktiskt delar upp energi vid en effektgräns:

```text
E_base_kWh[t] = min(E_total_kWh[t], P_base_kW * duration_hours[t])
E_peak_kWh[t] = max(0, E_total_kWh[t] - E_base_kWh[t])
```

Använd rätt avtalsintervall. En timbaserad gräns kan inte ersättas med ett dygnsmedel utan att resultatet kan ändras.

### 7.3 Kapacitet som en funktion med minne

Implementera kapacitet som:

```text
billed_capacity = capacity_rule(history, contract, billing_calendar)
```

Funktionen ska ange insamlingsperiod, filtrering, aggregat, avrundning, golv/tak, omräkningsdatum och vad som händer när kvalificerande data saknas.

Generiska operatorer som motorn kan behöva kombinera:

| Operator | Matematik | Viktig kontroll |
| --- | --- | --- |
| Historikmax | `max(x_i)` inom giltigt urval | En redan inträffad topp försvinner först enligt historikregeln |
| Medel av högsta N | `mean(top_N(x_i))` | Antal, distinkta tidsblock och hantering av saknade värden |
| Energi genom tidsfaktor | `E_kWh / h_equivalent` | Använd inte MWh direkt om resultatet ska bli kW |
| Regression | `P(T) = a + b*T` | Giltigt urval, rätt temperaturkälla, kvalitetsmått och reservmetod |
| Avtalad gräns | Kundens eller leverantörens fastställda värde | Ett simulerat val ändrar inte det faktiska avtalet |

Om prisbasen är dygnsenergi i kWh ska den behållas så. Omräkning till kW kräver att även prisfaktorn och samtliga gränser omräknas konsekvent.

Skilj korrelationskoefficienten `r` från förklaringsgraden `R²`. Kontrollera vilket mått och vilket tecken leverantören faktiskt använder. Ersätt inte ett regressionsvillkor med ett annat.

### 7.4 Flöde och temperatur

För en enkel volymavgift gäller `C_volume = volume_m3 * rate_SEK_per_m3`.

En generisk modell för jämförelse mot ett referensflöde kan uttryckas:

```text
excess_volume_m3 = volume_m3 - reference_m3_per_MWh * energy_MWh
C_flow = max(excess_volume_m3, 0) * fee_rate
         + min(excess_volume_m3, 0) * bonus_rate
```

Detta gäller endast när avtalet använder denna typ av jämförelse. Referens, period och debet-/kreditsats måste vara kända. Bevara den algebraiska formen utan division med kundens energi; den undviker division med noll, men tariffens regler för nollförbrukning behövs ändå.

En viktad temperatur beräknas som `sum(T_i*w_i)/sum(w_i)`. Vikten kan exempelvis vara volym eller energi och ska väljas enligt avtalet. Ett vanligt tidsmedel är inte utbytbart mot dessa vikter. Noll vikt ger ett odefinierat resultat, inte automatiskt 0 °C.

Skilj mellan steg som gäller hela underlaget och marginalsteg. Ett temperaturintervall får inte tilldelas fel sats bara för att tröskeln passerats.

### 7.5 Avrundning, moms och rabatt

Använd decimalaritmetik för pengar och avtalsstyrd avrundning. Avrunda inte sensorvärden före aggregering utan uttryckligt stöd. Spara ursprungligt belopp och momsgrund; använd en separat, spårbar konvertering för kalkylens jämförelsegrund.

Rabattregler måste ange både hur prisgruppen väljs och på vilken volym rabatten appliceras. Kontrollera också om föregående års användning låser årets rabatt. Räkna inte om en låst rabatt löpande bara för att prognosen ändras.

## 8. Byggnadsmodell och temperaturstyrning

Följande är en föreslagen startmodell för simulering, inte en färdig regleralgoritm:

```text
T_indoor[k+1] = T_indoor[k]
  + dt_h / C_eff_kWh_per_K * (
      P_heat_to_building_kW[k]
      + P_internal_and_solar_kW[k]
      - H_loss_kW_per_K * (T_indoor[k] - T_outdoor_actual[k])
    )
```

`C_eff` beskriver effektiv värmekapacitet och `H_loss` ett aggregerat värmeförlusttal. Kalibrera parametrarna mot byggnadens data. Använd byggår som möjlig startinformation, inte som ersättning för uppmätt respons, ventilation och befintlig reglerfunktion.

En enda temperaturzon kan vara otillräcklig. Identifiera representativa rum, kalla zoner och avvikande givare. Medianen kan användas för robust central återföring, men den får inte dölja varaktig undertemperatur i en giltig zon.

Agenten behöver dessutom en verifierad modell för hur tillåten styrsignal påverkar värmeleveransen. Att känna sambandet mellan effekt och rumstemperatur räcker inte för att säkert välja en emulerad utetemperatur eller ett ventilkommando.

### Föreslagen styrstrategi

1. Använd väderprognos, aktuell inomhustemperatur och identifierad tröghet för att förutse värmebehov.
2. Korrigera prognosfelet med återföring från inomhusgivarna.
3. Sänk värmetillförseln när prognosen visar onödig övertemperatur.
4. Pröva tidsförskjutning endast när byggnadens lagring, återhämtning och tariff ger ett fördelaktigt helhetsresultat.
5. Begränsa ändringshastighet och samordna med befintlig regulator så att två regulatorer inte motverkar varandra.
6. Inkludera återgången efter en sänkning; utvärdera eventuell ny effekttopp och ökad returtemperatur.

Optimera inte returtemperaturen isolerat. En lägre retur kan vara önskvärd, men åtgärden ska samtidigt leverera tillräcklig värme och fungera hydrauliskt. Primär och sekundär pump, ventil och bypass får inte behandlas som samma styrvariabel.

Använd inte värmeväxlarens förenklade fysik som ersättning för en debiteringsmätare. Sambandet `P ≈ rho * cp * volume_flow * delta_T` kan användas för rimlighetskontroll med konsekventa enheter och dokumenterade vätskeantaganden.

## 9. Kostnadsoptimering över rätt horisont

Jämför kompletta scenarier:

```text
delta_cost = Cost(control_candidate, initial_state, tariff)
             - Cost(reference_control, initial_state, tariff)
```

Ett negativt värde betyder lägre prognostiserad kostnad. Visa bidrag från energi, kapacitet, flöde/temperatur och andra påverkade kostnader.

Utgå från en kort reglerhorisont som räcker för byggnadens värmedynamik och väderutveckling. Komplettera den med en längre tariffhorisont för ändrade toppar, historik och framtida omräkning. Bestäm horisonterna från anläggning och avtal; använd inte en universell standard.

Ta hänsyn till följande:

- En höjd topp i ett pågående mätfönster kan påverka många senare fakturor.
- Att underskrida en redan fastställd topp kan ge noll kapacitetsbesparing just nu.
- Om historikvärdet löper ut ska både referens- och åtgärdsscenario följa samma kalender.
- Förvärmning kan ändra värmeförluster och skapa en ny topp innan den dyra perioden.
- Förskjutning mellan timmar behöver inte minska dygnsenergin eller tariffens dygnstopp.
- Abonnemangsförändringar räknas som separata avtalsåtgärder med egna giltighetsdatum.

Undvik att optimera genom att tömma byggnadens värmelager precis vid simuleringsslutet. Kräv jämförbar slutkomfort och rimligt termiskt sluttillstånd, eller prissätt den förväntade återhämtningen explicit.

Om en framtida tariff är okänd ska kalkylen redovisa antagandet. Håll isär dagens betalning, bedömd framtida besparing och besparing som redan verifierats på faktura.

## 10. Osäkerhet och beslutsgränser

Simulera åtminstone relevant variation i väder, byggnadsrespons och osäkra tariffparametrar. Använd dokumenterade intervall eller scenarier; skapa inte precisa sannolikheter utan underlag.

Bedöm varje förslag enligt fyra frågor:

1. Klarar förslaget komfort och driftgränser i de prövade scenarierna?
2. Är nyttan större än modellens och mätningens relevanta osäkerhet?
3. Bygger nyttan på en verifierad avgift som kunden faktiskt kan påverka?
4. Finns en tydlig återgång om temperaturen eller värmeleveransen avviker?

Saknas underlag för ett säkert val, redovisa vad som saknas och fortsätt i analysläge för just den funktionen. Status ”utreds” betyder inte att extern bevakning eller kontakt med leverantören pågår.

## 11. Driftlägen och kommandohantering

| Läge | Tillåten funktion |
| --- | --- |
| `analysis` | Läsa data, beräkna och lämna förslag |
| `shadow` | Beräkna styrförslag och jämföra dem med verkligt utfall, utan skrivning |
| `automatic` | Skriva inom det befintliga, verifierade driftmandatet |
| `fallback` | Överlämna till fastställd lokal återgångsstrategi |

Separera rekommendation från verkställande. Ett kommando ska bära punkt-ID, enhet, värde, tidsstämpel, giltighetstid och orsak. Kontrollera kvittens och faktisk respons; lyckad kommunikation är inte bevis för fungerande värmereglering.

Övergå enligt anläggningens fastställda strategi vid till exempel:

- otillräcklig eller gammal komfortdata,
- kommunikationsfel eller utebliven kvittens,
- manuell överstyrning eller lokalt larm,
- otillåten temperatur eller avvikelse utanför modellens giltighetsområde.

Återgång betyder inte generellt ”stäng ventilen” eller ”stoppa pumpen”. Den ska vara definierad för anläggningen och kunna hanteras lokalt även när agenten är frånkopplad.

## 12. Föreslaget beslutsformat

Exemplet visar struktur och innehåller avsiktligt inga färdiga styrvärden. `null` är okänt och får inte tolkas som noll. Formatet är ett förslag, inte ett färdigt JSON Schema.

```json
{
  "decision_id": null,
  "timestamp_utc": null,
  "plant_id": null,
  "mode": "analysis",
  "action": "no_write",
  "tariff_id": null,
  "tariff_version": null,
  "model_version": null,
  "data_quality": "not_evaluated",
  "constraints_satisfied": null,
  "control": {
    "point_id": null,
    "unit": null,
    "current_value": null,
    "proposed_value": null,
    "valid_until_utc": null
  },
  "forecast": {
    "horizon_hours": null,
    "minimum_zone_temperature_degC": null,
    "energy_delta_kWh": null,
    "cost_delta_SEK": null,
    "cost_delta_range_SEK": null,
    "vat_basis": null,
    "capacity_effect_date": null
  },
  "reason_sv": "Underlag måste kopplas och verifieras före beslut.",
  "unresolved_request_ids": [],
  "source_refs": [],
  "fallback_policy_id": null
}
```

Ange alltid jämförelseperiod och referensscenario i den fullständiga beslutsloggen. Kostnadsdifferensens tecken ska följa definitionen i avsnitt 9. Logga även bortvalda alternativ när de förkastats på grund av komfort, tariffosäkerhet eller driftgräns.

## 13. Konstruerade kontrollfall för implementeringen

Exemplen är egna och beskriver inga namngivna leverantörers aktuella priser.

### A. Oförändrad energi kan ge en annan energikostnad

Anta att 100 kWh verkligen kan flyttas från 900 till 300 SEK/MWh, utan andra förändringar. Skillnaden i energiledet är:

```text
0.100 MWh * (300 - 900) SEK/MWh = -60 SEK
```

Kontrollera därefter kapacitet, återhämtning, komfort och värmeförluster. De 60 kronorna är inte automatiskt nettobesparingen.

### B. En lägre ny topp behöver inte sänka debiteringen

Anta en enkel tariff med maximum över rullande historik. Historiskt maximum är 100 kW. Ett nytt dygn minskar från 95 till 85 kW. Så länge 100 kW ligger kvar i giltig historik är kapacitetsunderlaget oförändrat. Energi- och andra besparingar räknas separat.

### C. Flödesavgiftens tecken

Med 10 MWh, 250 m³ och referens 20 m³/MWh blir överskottsvolymen 50 m³. Vid avgift 4 SEK/m³ blir kostnaden +200 SEK. Med 150 m³ blir avvikelsen -50 m³; vid bonus 3 SEK/m³ blir bidraget -150 SEK.

### D. Enheter och saknade värden

2 400 kWh under 24 timmar motsvarar 100 kW. Däremot är en tariffbas på 2 400 kWh/dygn inte numeriskt utbytbar mot 100 kW med oförändrat pris. Ett saknat dygn eller en olöst prisgräns ska ge en kvalitetsflagga, inte ett fabricerat nollvärde.

### E. Komfort får inte förbättras enbart på papperet

Två styrscenarier ska börja med samma termiska tillstånd och jämföras vid likvärdig komfort. En modell som redovisar besparing genom att lämna huset kallare vid horisontens slut måste inkludera återhämtningen eller markera jämförelsen som ofullständig.

## 14. Verifiering och uppföljning

Före användning av en ny tariffadapter i kalkylatorns årsflöde: återskapa leverantörens publicerade räkneexempel eller gör en oberoende referensberäkning från de officiella villkoren och utred skillnader komponentvis. Kontrollera relevanta vinter-/sommarperioder, gruppgränser, rabattsteg, temperaturvillkor, historikskiften och omräkningsdatum. När en faktisk kundfaktura finns för en av Enkeys kunder, eller fakturakontroll uttryckligen efterfrågas, ska även den återskapas komponentvis med förregistrerade toleranser som motsvarar mätning och fakturaavrundning. Fakturavalidering är inte ett generellt krav för en tydligt avgränsad, källverifierad årsmodell.

Före automatisk styrning: verifiera signalriktning, begränsning, lokal återgång och respons inom befintligt mandat. Jämför i analys-/skuggläge när modellen eller integrationen ännu inte är verifierad.

Vid besparingsuppföljning ska agenten:

- dokumentera referensens befintliga styrfunktion,
- skilja uppvärmningsenergi från tappvarmvatten så långt mätunderlaget medger,
- hantera väder och användningsförändringar i referensmodellen,
- beräkna både referens och åtgärd med samma tariffversion för att isolera styrnyttan,
- separat visa faktisk kostnadsutveckling när priser eller avtal ändrats,
- redovisa komfortutfall och osäkerhet tillsammans med energi och pengar.

Kalla ett simulerat resultat ”prognostiserat”, ett normaliserat jämförelseresultat ”skattat” och ett verifierat fakturautfall ”fakturerat”. Använd inte dessa beteckningar som synonymer.

## 15. Kort agentinstruktion att återanvända

> Du arbetar med fjärrvärmens temperatur- och kostnadsoptimering. Koppla alltid rätt anläggning till ett verifierat kundavtal och en definierad mätgräns. Håll isär faktisk, prognostiserad, emulerad och debiteringsgrundande utetemperatur. Använd inomhusåterföring och byggnadens identifierade dynamik när du föreslår värmestyrning. Låt en deterministisk motor beräkna kostnaden, inklusive historiska toppar och framtida omräkning. Bevara okända värden och frågor med status ”utreds”; anta aldrig att de är noll. Jämför genomförbara scenarier med likvärdig komfort och inkludera återhämtning. Redovisa energi-, effekt- och kostnadseffekt var för sig, med tidshorisont, källor och osäkerhet. Verkställ endast inom befintligt driftmandat och låt lokala skydd, manuell överstyrning och fastställd återgång ha företräde. Dokumentera varför varje åtgärd väljs och kontrollera det faktiska utfallet.

## Källor och versionsansvar

- **Rapportunderlag:** [Maskinläsbara prismodeller för fjärrvärme, BeBo/Belok, 2024-11-30](https://www.bebostad.se/media/7182/bebo-maskinl%C3%A4sbara-prismodeller-f%C3%B6r-fj%C3%A4rrv%C3%A4rme.pdf).
- **Projektinformation:** [BeBos projektsida](https://www.bebostad.se/projekt/avslutade-projekt/2024/maskinlasbara-prismodeller-for-fjarrvarme).
- **Teknisk tillämpning:** Avsnitt 3–15 är framtagna för detta agentunderlag. Temperaturstyrning, ekvationer, driftlägen och exempel ska valideras i den aktuella implementationen.
- **Priser:** Dokumentet innehåller ingen aktuell tariffkatalog. Aktuella avtal och leverantörsbekräftelser avgör vilken prismodell som gäller.

Vid ändring: versionssätt dokument, tariffadapter, tariffdata och byggnadsmodell separat. Bevara vilket underlag varje tidigare beslut använde så att resultat kan återskapas.
