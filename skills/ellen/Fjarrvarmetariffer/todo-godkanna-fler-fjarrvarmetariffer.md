# To-do: godkänna och införa fler fjärrvärmetariffer

Upprättad 2026-09-04 utifrån [verifieringslistan](verifieringslista-fjarrvarmebolag.md).

## Nuläge

- 28 tariffer har fullständigt källunderlag och kan gå vidare till teknisk beredning utan fler prisfrågor till leverantören.
- 31 tariffer är villkorat godkända eller godkända endast för årsberäkning.
- 12 tariffer är underkända i väntan på entydiga leverantörsbesked.
- Stockholm Exergi är separat implementerad och fakturavaliderad men katalogposten kräver fortfarande motorarbete.
- Källgodkännande betyder inte att tariffen redan är implementerad, testad eller synlig i kalkylatorn.

## Ansvar

| Ansvarig | Uppgift |
|---|---|
| Robert | Bestäm produktnivå och prioriteringsordning, kontakta leverantörer, ordna anonymiserade fakturor och lämna slutligt verksamhetsgodkännande. |
| Claude | Kartlägg motorstöd, rätta katalogdata, implementera tariff och användargränssnitt, skriva tester samt lämna en ändrings- och testrapport. |
| Codex | Oberoende kontroll av källa mot katalog och kod, gränsvärdes- och webbläsartestning, fakturajämförelse samt dokumenterat godkännande eller fynd. |
| Fjärrvärmebolaget | Besvara sådant som inte framgår entydigt av publicerade villkor och vid behov bekräfta kundens prisgrupp, effekt eller andra avtalsvärden. |

## 1. Robert beslutar godkännandenivå

- [ ] Bestäm om kalkylatorn tills vidare bara ska visa tariffer med komplett månadsmodell. **Rekommendation:** börja så; hantera årsberäkning som en senare, tydligt märkt funktion.
- [ ] Bestäm om kundspecifika värden från faktura eller leverantör, exempelvis debiterbar effekt, får vara obligatoriska indata. De får aldrig ersättas med ett dolt standardvärde.
- [ ] Bestäm miniminivå för fakturavalidering. **Rekommendation:** minst en anonymiserad verklig faktura per prismodell och, när priset är säsongsberoende, helst en vinter- och en sommarfaktura.
- [ ] Godkänn första införandebatchen efter Claudes tekniska kartläggning i steg 2.

## 2. Claude kartlägger de 28 källgodkända tarifferna

- [ ] Jämför varje tariff med befintligt stöd i Python-, TypeScript- och gränssnittslagret.
- [ ] Klassificera varje tariff som `enbart katalogändring`, `mindre motorändring`, `ny gemensam prismodell` eller `ny obligatorisk kundindata`.
- [ ] Lista exakt vilka fält, formler, spärrar och gränssnittskomponenter som behöver ändras.
- [ ] Bekräfta att samma beräkning kan användas i både MWh- och kronorflödet.
- [ ] Lämna kartläggningen till Codex för oberoende granskning innan flera modeller byggs samtidigt.

Föreslagen granskningsordning:

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
- [ ] Testa både direkt MWh-beräkning och inversen från kronor till MWh.
- [ ] Testa kronor → MWh → kronor som rimlighetskontroll där modellen tillåter det.
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

- [ ] Robert beslutar om en separat, tydligt märkt årsberäkning ska stödjas. Om svaret är nej ligger tariffer utan verifierad månadsfördelning kvar avstängda.
- [ ] Robert begär vid behov exakt månadsfördelning från berörda leverantörer.
- [ ] Robert eller användaren tillhandahåller avtals-/fakturavärden när tariffen kräver exempelvis effektgrupp, P, Wn, Q, A, B eller U.
- [ ] Claude gör sådana värden obligatoriska och synliga; inga automatiska antaganden får göras.
- [ ] Codex verifierar att årsresultat aldrig presenteras som månadsresultat och att villkoren följer med genom hela användarflödet.

## Definition av klar för produktion

En tariff får markeras som produktionsgodkänd först när allt nedan är uppfyllt:

- [ ] Aktuell officiell primärkälla är länkad och alla priskomponenter är spårbara.
- [ ] Det finns ingen olöst motsägelse eller dold standardtolkning.
- [ ] Katalog, motor och gränssnitt stöder hela den avsedda omfattningen eller blockerar resten uttryckligen.
- [ ] Automatiska normal-, gräns-, fel- och regressionstester är gröna.
- [ ] Resultatet har jämförts med faktura eller ett tillräckligt komplett officiellt räkneexempel.
- [ ] Codex oberoende granskning är godkänd och eventuella fynd är stängda.
- [ ] Robert har godkänt funktion och presentation i testmiljön.
- [ ] Ändringen, källorna och godkännandet finns i konversations-/granskningsloggen.
