# Stockholm Exergi – schablonunderlag för snabb kalkyl 2026

## Syfte och avgränsning

Underlaget gör det möjligt att fylla Stockholm Exergis kalkyl med preliminära värden när kunden saknar fullständiga fakturauppgifter. Schablonen uppskattar:

- årsenergi, om användaren inte redan har angett känd MWh/år,
- total köpt värme per kalendermånad, som tillsammans summerar till årsenergin och kan ersättas med fakturans månadsvärden,
- debiterbar effekt,
- internt skattad överskjutande energivolym under kalla dygn, som bara är en del av månadsenergin,
- energiviktad returtemperatur för november–mars.

Värdena är **uppskattningar**, inte leverantörs- eller fakturavärden. De får användas för en uppskattad aktuell årskostnad, men inte presenteras som fakturaverifierade och inte användas som bevis för en besparing. Fakturans värden har alltid företräde.

## Källor

Hämtade och kontrollerade 2026-09-19–21:

1. [Stockholm Exergi – pris och avtal för företag](https://www.stockholmexergi.se/foretag/fjarrvarme-for-foretag/pris-och-avtal-foretag/)
   Beskriver kostnadskomponenterna energi, effekt och returtemperatur, rekommenderad effekt vid −10 °C samt nätets referens för returtemperatur, 37,5 °C.
2. [Stockholm Exergi – normalprislista fjärrvärme 2026](https://www.stockholmexergi.se/wp-content/uploads/2026/04/Normalprislista_fjarrvarme_2026-1.pdf)
   Punkt 3 definierar tillägget per kallt dygn: endast energi över kundens Effektgräns −3 °C får det högre priset. Detta kan inte återskapas exakt från tolv månadsvärden.
3. [SMHI – dygnsmedeltemperatur, öppna data](https://www.smhi.se/data/sok-oppna-data-i-utforskaren/se-acmf-meteorologiska-observationer-lufttemperatur-medelvarde-1-dygn)
   Kvalitetskontrollerade dygnsvärden från Stockholm-Observatoriekullen, station 98210. Normalperiod 1991–2020 användes.
4. [SMHI – Guide normalårskorrigering värme](https://www.smhi.se/download/18.1cdddc041958439e87f232/1741699305087/Guide%20Normal%C3%A5rskorrigering%20v%C3%A4rme.pdf)
   Publicerade balanstemperaturer för typhus: 17, 15, 13, 11 och 7 °C beroende på byggnadstyp och ålder.
5. [Energiforsk – Samband mellan flödespremie och returtemperatur](https://energiforsk.se/media/18653/2013-25-samband-mellan-floedespremie-och-returtemperatur.pdf)
   Kategorimedel för returtemperatur: flerbostadshus 39,6 °C, offentliga byggnader 41,0 °C och övriga byggnader 42,6 °C.
6. `leverantor-stockholm-exergi.md` i Ellen-underlaget
   Källverifierat tariffkontrakt och kundexempel för 2026. Kundexemplet visar en kallenergigräns omkring 77 procent av debiterbar effekt. Detta är ett exempel, inte ett generellt publicerat leverantörsvillkor.

## Beräkningsmodell

Modellen använder en linjär värmesignatur, 18 procent jämnt fördelad baslast och SMHI:s dygnsmedeltemperaturer. Värmeeffekten antas vara noll över byggnadens balanstemperatur och öka linjärt när utetemperaturen sjunker.

Den totala månadsenergin är separat från den överskjutande energivolymen. För varje typhus
fördelas 82 procent av årsenergin mellan månaderna efter summan av positiva
dygnsgradskillnader `max(0, balanstemperatur − dygnsmedeltemperatur)` för
1991–2020. Resterande 18 procent fördelas lika på årets tolv månader.
Månadsandelarna avrundas för visning och sista månaden får differensen, så
summan blir exakt det årsbelopp som används av tariffmotorn. När schablonen
används prissätter motorn just denna synliga månadsserie, inte en annan
generisk förbrukningsprofil.

Kunden anger eller justerar i formuläret **total köpt fjärrvärme per månad**;
den ska summera till årsenergin för tariffen. När årsenergin anges som enbart
rumsvärme ingår modellens uppskattade tappvarmvatten i tariffens månadsbelopp.
Tariffmotorns separata, obligatoriska serie för överskjutande energi fylls
automatiskt med källtypen `estimated`. För varje månad multipliceras kundens
totala månadsenergi med normalårsmodellens skattade andel överskjutande
energi just den månaden. Approximationen fångar inte kundens verkliga
dygnsvärden eller avtalade effektgräns och får inte utges för
fakturareproduktion. Formuläret frågar inte kunden efter den interna serien.

Om användaren uttryckligen anger **enbart rumsvärme** behålls den uppgiften
och dess omfattning. För att uppskatta total köpt värme inklusive varmvatten
dividerar modellen då rumsvärmen med `1 − 0,18`; den antagna tillkommande
varmvattendelen redovisas som en osäkerhet. Om användaren anger **total köpt
värme inklusive varmvatten** används talet oförändrat.

Byggnadens balanstemperatur väljs så här:

| Byggnad | Ålder | Balanstemperatur |
|---|---:|---:|
| Flerbostadshus/radhus | före 1975 | 17 °C |
| Flerbostadshus/radhus | 1975–1995 | 15 °C |
| Flerbostadshus/radhus | efter 1995 | 13 °C |
| Lokal | före 1975 | 17 °C |
| Lokal | 1975–2010 | 11 °C |
| Lokal | efter 2010 | 7 °C |

För varje profil har följande faktorer räknats fram per MWh årsenergi:

| Balanstemperatur | Effekt vid −10 °C, kW/MWh | Kallenergi jan | feb | mar | nov | dec |
|---:|---:|---:|---:|---:|---:|---:|
| 7 °C | 0,6051 | 0,00807 | 0,00744 | 0,00103 | 0,00016 | 0,00437 |
| 11 °C | 0,4137 | 0,00670 | 0,00633 | 0,00112 | 0,00021 | 0,00379 |
| 13 °C | 0,3609 | 0,00642 | 0,00605 | 0,00122 | 0,00024 | 0,00369 |
| 15 °C | 0,3207 | 0,00625 | 0,00589 | 0,00132 | 0,00026 | 0,00363 |
| 17 °C | 0,2887 | 0,00616 | 0,00584 | 0,00142 | 0,00030 | 0,00358 |

Kallenergin är noll i april–oktober i normalårsprofilen. För kalla dagar under −3 °C räknas endast den energidel som ligger över 77 procent av uppskattad effekt vid −10 °C. Eftersom 77-procentsnivån kommer från ett enskilt verifierat kundexempel ska resultatet alltid märkas `estimated`.

Exempel: 1 000 MWh/år total köpt värme i ett flerbostadshus från 1975–1995
ger **1 000 MWh** när de tolv totala månadsvärdena summeras. Januari är
156,389 MWh total värme. De tolv internt beräknade överskjutande
energimängderna summerar i modellen bara till **17,35 MWh**; januari utgör
6,25 MWh. Den serien ska varken visas som ett kundfält eller tolkas som
hela månadens förbrukning.

Returtemperaturen fylls med samma kategorivärde för november, december, januari, februari och mars:

| Kategori | Schablon |
|---|---:|
| Flerbostadshus | 39,6 °C |
| Skola, vård eller gym | 41,0 °C |
| Övrig lokal | 42,6 °C |
| Radhus | 37,5 °C |

Energiforsks kategoridata i denna studie omfattar inte småhus. För radhus används därför Stockholm Exergis publicerade nätreferens 37,5 °C, tydligt märkt som schablon.

## Rimlighetskontroll

Profilen 17 °C ger cirka 122 kW vid 423 MWh/år. Det ligger nära det verifierade kundexemplets 123–125 kW och används som rimlighetskontroll, inte som kalibrering eller facit för andra fastigheter.

## Osäkerheter

- En verklig byggnads värmesignatur påverkas av internlaster, ventilation, varmvattendel, verksamhetstider, klimatskal och styrning.
- Returtemperaturen kan variera mycket mellan anläggningar och månader. Kategorimedlen ersätter inte mätvärden.
- Normalårets kallenergi är inte en prognos för ett visst kalenderårs väder.
- 77-procentsgränsen är härledd ur ett kundexempel och kan avvika från den effektgräns Stockholm Exergi fastställer för en annan kund.
- Industriprocesser och andra avvikande värmelaster kräver manuell bedömning.

## Produktkrav

- Hjälpen ska vara frivillig och synligt märkt som preliminär uppskattning.
- Användaren ska kunna ersätta alla schablonvärden med fakturavärden.
- Känd, manuellt angiven årsenergi ska behålla sin proveniens; bara de framräknade fälten märks `estimated`.
- Kunden ska se och kunna ändra tolv värden för total månadsenergi. De ska summera till den årsenergi som tariffmotorn använder. Överskjutande energi är ett internt uppskattat tariffunderlag, inte ett eget kundfält.
- Om byggnadsindata ändras ska gamla modellvärden ogiltigförklaras och rensas.
- Resultatet får endast vara en uppskattad aktuell årskostnad och ska visa att det inte är en besparingsberäkning.
