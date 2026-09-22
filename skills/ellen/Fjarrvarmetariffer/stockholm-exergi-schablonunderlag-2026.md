# Stockholm Exergi – schablonunderlag för snabb kalkyl 2026

## Syfte och avgränsning

Underlaget gör det möjligt att fylla Stockholm Exergis kalkyl med preliminära värden när kunden saknar fullständiga fakturauppgifter. Schablonen uppskattar:

- årsenergi, om användaren inte redan har angett känd MWh/år,
- månadsenergi med samma omfattning som vald årsenergi: total köpt värme eller enbart rumsvärme,
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
summan blir exakt vald årsenergi. Vid totalvärme prissätter tariffmotorn
den synliga serien. Vid enbart rumsvärme prissätter den den synliga
rumsvärmeserien **plus samma uppskattade baslast varje månad**, inte en
annan generisk förbrukningsprofil.

Kunden anger eller justerar i formuläret månadsenergi med **samma omfattning
som vald årsenergi**. För total köpt värme summerar fälten till tariffens
årsenergi. För valet enbart rumsvärme summerar de till angiven rumsvärme;
schablonen visar då nära noll rumsvärme under sommaren. För tariffpriset
läggs ett separat, jämnt fördelat och uttryckligen uppskattat tappvarmvatten
till varje rumsvärmemånad. Den köpta månadsserien finns internt och summerar
till `rumsvärme / (1 − 0,18)`. Uppskattningen inkluderar **inte separat
ventilationsvärme**; sådan behöver verifieras från faktura eller annan mätning,
och kunden bör då använda valet total köpt värme.
Tariffmotorns separata, obligatoriska serie för överskjutande energi fylls
automatiskt med källtypen `estimated`. För varje månad multipliceras kundens
totala månadsenergi med normalårsmodellens skattade andel överskjutande
energi just den månaden. Approximationen fångar inte kundens verkliga
dygnsvärden eller avtalade effektgräns och får inte utges för
fakturareproduktion. Formuläret frågar inte kunden efter den interna serien.

Om användaren uttryckligen anger **enbart rumsvärme** behålls den uppgiften
och dess omfattning. För att uppskatta total köpt värme inklusive tappvarmvatten
dividerar modellen då rumsvärmen med `1 − 0,18`. Talet 18 procent kommer från
projektets verifierade kundexempel, inte från SMHI och inte från en generell
regel för alla byggnader. SMHI:s guide stödjer uppdelningen i väderberoende
värme och väderoberoende baslast, men anger ingen generell baslastandel.
Om användaren anger **total köpt värme inklusive varmvatten** används talet
oförändrat. Ett byte av energins omfattning rensar tidigare månadsserie för att
förhindra att samma tal tolkas som ett annat energislag.

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

## Utforskande Optimate-potential (lokal prototyp 2026-09-21)

Den befintliga `annual_forward`-produkten och dess spärr
`stodjer_besparing=false` är oförändrade. En separat, uttryckligen
**preliminär scenariovy** under Stockholms årskostnad prövar Roberts antagande
om 15, 20 och 25 procent mindre styrbar rumsvärme. Dessa procenttal är inte
fakturaverifierade eller garanterade utfall. För varje kalendermånad gäller:

`köpt värme efter = köpt värme före − styrbar rumsvärme före × scenarioandel`.

Om kunden anger enbart rumsvärme används den uttryckligen angivna
månadsserien. Om kunden anger total köpt värme skattas styrbar rumsvärme
som `max(0, köpt månadsenergi − 18 % av total årsenergi / 12)`; resultatet
märks som uppskattat. Den opåverkade delen — huvudsakligen schablonens
tappvarmvatten — minskas aldrig. Separat ventilationsvärme är inte
identifierbar från dessa uppgifter.

Samma 2026-tariffmotor och prisår körs före och efter. **Debiterbar effekt,
returtemperatur och den skattade kölddygnsvolymen hålls oförändrade** i
huvudscenarierna. Tariffens redan energiviktade returavgift kan därmed
ändras när månadsenergin ändras, men ingen förbättrad temperatur antas.
Om den fasta kölddygnsvolymen inte längre ryms inom någon eftermånad
avvisas scenariot, i stället för att skapa en ogiltig efterkostnad.
Resultatet är en skattad *kostnadsskillnad för energiscenariot*, inklusive
moms — inte en fullständig prognos för Optimate och inte en godkänd
besparingsprodukt.

En separat, hopfälld känslighet visar tariffkostnadens skillnad om
**leverantören senare skulle fastställa 20 % lägre debiterbar kW** i
20-procentsscenariot. Hypotetiskt eftervärde avrundas till heltal och
begränsas av Stockholms 10 kW-golv. Detta är inte samma sak som 20 % lägre
fysisk toppeffekt. Stockholm Exergi härleder debiterbar effekt ur tidigare
vardagars energisignatur och reviderar den den 1 januari; en verklig
effektbesparing kan därför komma senare eller utebli. Den eventuellt ändrade
`Effektgräns −3 °C` kan inte räknas fram ur tolv månadsbelopp och hålls
oförändrad även i denna känslighet. Beloppet adderas **inte** till
huvudscenarierna.

Innan en verifierad besparingsprodukt kan öppnas behövs minst en separat
granskning av styrbar last, dygnsvärden/effektsignatur, avtalad effektgräns,
tariffens omräkningsdatum och komfortutfall. Jämför verklig drift med
likvärdigt väder och bevarat inomhusklimat; schablonens procenttal är bara
en start för diskussion.

## Produktkrav

- Hjälpen ska vara frivillig och synligt märkt som preliminär uppskattning.
- Användaren ska kunna ersätta alla schablonvärden med fakturavärden.
- Känd, manuellt angiven årsenergi ska behålla sin proveniens; bara de framräknade fälten märks `estimated`.
- Kunden ska se och kunna ändra tolv värden för vald energiomfattning. Enbart rumsvärme summerar till angiven rumsvärme, totalvärme till tariffens årsenergi. Tariffmotorn får alltid en separat serie för uppskattat totalt fjärrvärmeköp. Överskjutande energi är ett internt uppskattat tariffunderlag, inte ett eget kundfält.
- Om byggnadsindata ändras ska gamla modellvärden ogiltigförklaras och rensas.
- Den ordinarie, kontraktsstyrda tariffprodukten får endast ge en uppskattad aktuell årskostnad och ska fortsatt ange att den inte är en godkänd besparingsberäkning. Den separata Optimate-vyn ovan är uttryckligen en utforskande scenariokalkyl, inte ett upplåst produktlöfte.
