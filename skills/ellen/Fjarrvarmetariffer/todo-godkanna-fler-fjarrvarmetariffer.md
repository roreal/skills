# To-do: godkänna och införa fler fjärrvärmetariffer

Upprättad 2026-09-04 utifrån [verifieringslistan](verifieringslista-fjarrvarmebolag.md).
Uppdaterad 2026-09-08 enligt [produktdirektivet](../PROJECT_CHARTER.md).

## Nuläge

- 28 tariffer har fullständigt källunderlag och kan gå vidare till teknisk beredning utan fler prisfrågor till leverantören.
- 31 tariffer är villkorat godkända eller godkända endast för årsberäkning.
- 12 tariffer är underkända i väntan på entydiga leverantörsbesked.
- Stockholm Exergi är separat implementerad och fakturavaliderad men katalogposten kräver fortfarande motorarbete.
- Sju katalogtariffer från sex leverantörer är nu aktiva efter den godkända och pushade Sandviken-etappen. De är en utvärderingsbas, inte slutlig v1-täckning.
- Källgodkännande betyder inte att tariffen redan är implementerad, testad eller synlig i kalkylatorn.

## Slutmål för tariffarbetet

Samtliga tariffer som kan återskapas som en källverifierad, uppskattad årskostnad ska
implementeras. För en fryst tariffinventering och ett angivet prisår ska varje
tariffprodukt — både i JSON-katalogen och i separat förvaltade leverantörsfiler — till
slut vara antingen:

- `implemented_source_verified_annual`;
- `blocked_external_info`, med exakt saknat leverantörsbesked eller datakrav;
- `not_applicable`, med dokumenterad motivering.

"Möjlig" betyder att alla prisdelar och regler är kända och att varje dynamiskt värde kan
anges av användaren, hämtas från verifierad källa eller beräknas från uttryckligt underlag.
Att bolaget kan fakturera räcker inte ensamt om en nödvändig intern formel eller
nätreferens inte går att reproducera externt. Prioritering efter kundnytta styr ordningen,
inte vilka möjliga tariffer som till slut ska omfattas.

## Ansvar

| Ansvarig | Uppgift |
|---|---|
| Robert | Bestäm v1-täckning och prioriteringsordning, kontakta leverantörer, ordna fakturor för egna kunder eller uttrycklig fakturakontroll och lämna slutligt verksamhetsgodkännande. |
| Claude | Kartlägg motorstöd, rätta katalogdata, implementera tariff och användargränssnitt, skriva tester samt lämna en ändrings- och testrapport. |
| Codex | Oberoende kontroll av källa mot katalog och kod, gränsvärdes- och webbläsartestning, fakturajämförelse samt dokumenterat godkännande eller fynd. |
| Fjärrvärmebolaget | Besvara sådant som inte framgår entydigt av publicerade villkor och vid behov bekräfta kundens prisgrupp, effekt eller andra avtalsvärden. |

## 1. Robert beslutar godkännandenivå

- [x] Årsberäkning är kalkylatorns primära scope. Månadsresultat kräver separat verifierad periodisering och får inte antydas generellt.
- [x] Kund-/leverantörsspecifika värden, exempelvis debiterbar effekt, får vara obligatoriska. De får aldrig ersättas med ett dolt standardvärde.
- [x] Fakturor krävs för Enkeys kunder eller när fakturakontroll uttryckligen efterfrågas. Övriga årsmodeller verifieras mot ett tillräckligt komplett officiellt räkneexempel eller en oberoende referensberäkning från leverantörens publicerade villkor.
- [x] Första införandebatchen Sandviken Energi — Helleverans är godkänd och pushad.
- [x] Täckningsmål beslutat: implementera samtliga möjliga tariffer i den frysta v1-inventeringen, inklusive separat förvaltade leverantörsfiler; klassificera resten explicit som blockerade eller ej tillämpliga.
- [ ] Bestäm om saknad leverantör ska ge ett separat, tydligt märkt generellt resultat enligt rekommendationen i produktdirektivet.

## 2. Claude kartlägger de 28 källgodkända tarifferna — slutförd grundkartläggning

- [x] Jämför varje tariff med befintligt stöd i Python-, TypeScript- och gränssnittslagret.
- [x] Klassificera varje tariff som `enbart katalogändring`, `mindre motorändring`, `ny gemensam prismodell` eller `ny obligatorisk kundindata`.
- [x] Lista exakt vilka fält, formler, spärrar och gränssnittskomponenter som behöver ändras.
- [x] Klassificera MWh-, kronor- och schablonflödet separat; ett läge som inte kan stödjas entydigt ska blockeras.
- [x] Lämna kartläggningen till Codex för oberoende granskning innan flera modeller byggs samtidigt.

Föreslagen granskningsordning om inget konkret kund-/prospektbehov ger en annan prioritet:

1. **Första gruppen att tekniskt bedöma:** Karlstad, Sandviken, Matfors/Kvissleby, Södertörns Fjärrvärme, VänerEnergi och Övik Energi.
2. **Gemensam högutväxlingsmodell:** E.ON och Navirum, totalt åtta tariffer. Samma rullande effekt- och flödesmodell kan återanvändas. Malmö/Burlöv måste samtidigt rättas från −15 till −8 °C.
3. **Vattenfalls gemensamma modell:** tolv tariffer för Standard och Spetsig i fem tariffamiljer.
4. **Specialfallen:** Telge samt Sundsvall Indal/Liden/Lucksta, där den senare kräver motorstöd för en ren energitariff utan kapacitetsdel.

Ordningen ovan är en bedömningsordning, inte ett påstående om att första gruppen kan lanseras utan kodändringar.

## 3. Claude implementerar en godkänd batch

För varje tariff:

- [ ] Rätta katalogens kända fel och fyll alla verifierade värden, enheter, giltighetsperioder och källänkar.
- [ ] Mappa energi, fast avgift, effekt/kapacitet, flöde, rabatter, säsonger och månadsperiodisering uttryckligen.
- [ ] Lägg in obligatoriska kund- eller leverantörsvärden som synliga, validerade indata.
- [ ] Lägg in spärrar för fel kundtyp, fel nät, fel effektintervall och saknade värden. Motorn ska stoppa i stället för att gissa.
- [ ] Begränsa tariffens omfattning när källgodkännandet har villkor, exempelvis fullvärme, normalleverans eller högsta tillåtna effekt.
- [ ] Säkerställ likvärdigt beteende i Python och TypeScript där båda motorerna används.
- [ ] Ta inte bort `investigation` eller aktivera tariffen förrän implementation, tester och oberoende granskning är klara.
- [ ] Dokumentera ändrade filer, antaganden, källor och avsiktligt uppskjutna delar i slutrapporten.

## 4. Claude skriver verifierbara tester

- [ ] Testa ett normalfall med manuellt uträknat referensvärde från prislistan.
- [ ] Testa varje prisgräns precis under, exakt på och precis över gränsen.
- [ ] Testa alla säsongsbyten och månadsperiodiseringar.
- [ ] Testa noll, negativa värden, saknade obligatoriska värden och otillåten kundtyp.
- [ ] Testa eventuella rabatt-, flödes-, returtemperatur- och överuttagsregler.
- [ ] Testa varje inmatningsläge som tariffen deklarerar stöd för och testa att övriga lägen blockeras.
- [ ] Testa kronor → MWh → kronor som rimlighetskontroll endast där inversen är entydig och verifierad.
- [ ] Lägg till regressionsfall för Malmö/Burlövs −8 °C och Öviks kalenderdagsfördelning.
- [ ] Kör relevanta Python- och TypeScript-tester, typkontroll och produktionsbygge.

## 5. Codex gör oberoende godkännande

- [ ] Jämför varje implementerat tal och regel med den länkade primärkällan.
- [ ] Kontrollera att katalogen inte innehåller kvarvarande `null`, standardvärden eller intervalltolkningar som saknar källstöd.
- [ ] Granska att gemensam motorkod verkligen passar alla nät som återanvänder modellen.
- [ ] Kör om automatiska tester och egna gränsvärdesfall.
- [ ] Testa kalkylatorn i webbläsare, inklusive begripliga fel när indata saknas.
- [ ] Jämför mot anonymiserad faktura eller leverantörens publicerade räkneexempel.
- [ ] Skriv ett separat resultat: `godkänd`, `godkänd med dokumenterat villkor` eller `ej godkänd`.
- [ ] Låt Claude rätta fynd och gör därefter en slutlig omtestning.

## 6. Robert gör verksamhets- och lanseringsgodkännande

- [ ] Prova varje nytt leverantörsalternativ i testmiljön med realistiska indata.
- [ ] Kontrollera att namn, nätområde, kundtyp och krav på extra indata är begripliga.
- [ ] Bekräfta att begränsningar och varningar är acceptabla för användaren.
- [ ] Lämna uttryckligt godkännande för den färdiga batchen.
- [ ] Först därefter: versionera, tagga, bygga och driftsätta enligt projektets releaseprocess.

## 7. Robert och leverantörerna löser de 12 underkända tarifferna

Codex kan formulera varje fråga. Robert skickar den från lämplig avsändare och sparar svaret i projektet. Claude ska inte implementera den oklara delen innan svaret har verifierats.

| Bolag | Tariffer | Besked som krävs |
|---|---:|---|
| Gävle Energi | 1 | Om volymavdraget är marginalt eller gäller hela månadens volym efter uppnådd nivå. |
| Härnösand Energi & Miljö | 1 | Korrekt intervallformel eftersom officiell tabell och räkneexempel motsäger varandra. |
| Hässleholm Miljö | 2 | Om effektrabatten beräknas intervallvis eller på hela effekten. |
| Lidköping Energi | 2 | Flödesjusteringens exakta värden/formel samt vilken momsangivelse som är korrekt. |
| Skellefteå Kraft | 2 | Rabattens enhet/beräkning och saknade lokala beräkningstemperaturer. |
| Sundsvall Energi | 1 | Fullständig flödesjustering, nätvärdet `Qalla/Walla` och hantering från 2 000 kW. |
| Mälarenergi | 2 | Sommarperiod, överuttagsregler, flödesavgift och om flödesmodellen gäller gruppanslutna småhus. |
| VB Energi | 1 | Effektperiod november–mars eller december–mars, volymgruppens mätår/omprövningsdag och månadsperiodisering. |

Efter varje svar:

- [ ] Robert sparar originalsvaret med datum, avsändare och eventuella bilagor.
- [ ] Codex kontrollerar att svaret löser hela frågan och uppdaterar verifieringsstatusen.
- [ ] Claude uppdaterar katalog och implementation först när statusen tillåter det.
- [ ] Codex testar och godkänner ändringen enligt steg 5.

## 8. Hantera de 31 villkorade tarifferna

- [x] En separat, tydligt märkt årsberäkning ska stödjas när årsmodellen är källverifierad. Avsaknad av generell månadsmodell blockerar inte i sig detta scope.
- [ ] Robert begär vid behov exakt månadsfördelning från berörda leverantörer när ett månadsresultat eller en fakturakontroll faktiskt efterfrågas.
- [ ] Robert eller användaren tillhandahåller avtals-/fakturavärden när tariffen kräver exempelvis effektgrupp, P, Wn, Q, A, B eller U.
- [ ] Claude gör sådana värden obligatoriska och synliga; inga automatiska antaganden får göras.
- [ ] Codex verifierar att årsresultat aldrig presenteras som månadsresultat och att villkoren följer med genom hela användarflödet.

## Definition av klar för produktion

En tariff får markeras som produktionsgodkänd först när allt nedan är uppfyllt:

- [ ] Aktuell officiell primärkälla är länkad och alla priskomponenter är spårbara.
- [ ] Det finns ingen olöst motsägelse eller dold standardtolkning.
- [ ] Katalog, motor och gränssnitt stöder hela den avsedda omfattningen eller blockerar resten uttryckligen.
- [ ] Automatiska normal-, gräns-, fel- och regressionstester är gröna.
- [ ] Årsmodellen har jämförts med ett tillräckligt komplett officiellt räkneexempel eller en oberoende referensberäkning från publicerade villkor. Faktura används för egna kunder eller uttrycklig fakturakontroll.
- [ ] Kundtexten skiljer beräknad årskostnad, uppskattning och fakturaverifierat utfall och använder inte ordet "exakt" som synonym för någon av dem.
- [ ] Codex oberoende granskning är godkänd och eventuella fynd är stängda.
- [ ] Robert har godkänt funktion och presentation i testmiljön.
- [ ] Ändringen, källorna och godkännandet finns i konversations-/granskningsloggen.

Kalkylatorns tariffetapp som helhet är klar först när ingen tariff i den frysta
kontrollmängden är oklassificerad och samtliga genomförbara tariffer har godkänts enligt
listan ovan.
