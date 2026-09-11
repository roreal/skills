# Verifieringslista: fjärrvärmebolag att gå igenom

Genererad 2026-09-04 ur `optimate-fjarrvarme-2026.json`, körd genom `grind()` i `enkey-agents/tools/tariffer/katalog.py`.

**Läge just nu:** 6 av 78 utdragna tariffer (5 av 53 bolag) är godkända och syns i kalkylatorn. Den här listan är de återstående 72.

## Så här används listan

- **Del A** (65 tariffer) är avvisade för att källdatan själv är märkt `utreds` — inte för att motorn saknar stöd. Varje rad har de konkreta villkor som måste bekräftas mot bolagets faktiska, aktuella prislista innan tariffen kan läggas till i katalogen som verifierad.
- **Del B** (7 tariffer) är avvisade för att prisformen eller kapacitetsformeln inte är en av de motorn stödjer ännu ("Fas 2"). Dessa kräver motorarbete innan de ens är värda att verifiera mot en faktura.
- Källhänvisningen (`source_id`, sida) pekar mot underlaget — bekräfta alltid mot bolagets egen, aktuella prislista, inte bara mot det redan utdragna talet.
- Kryssa i varje villkor när det är bekräftat. När alla villkor för en tariff är bekräftade och periodiseringen/kapacitetsmappningen är inlagd i motorn, ta bort `investigation`-blocket (eller sätt `status` till något annat än `utreds`) i katalogen och kör om `grind()`.

### Status för den externa källgranskningen

Codex granskar här **källdatan**, inte om tariffen redan är produktionsklar i kalkylatorn. Statusarna betyder:

- **✅ Källunderlag godkänt** — priser, enheter, intervall, beräkningsgrund och periodisering har stöd i en aktuell primärkälla. Fortfarande krävs implementation, testfall och helst fakturavalidering.
- **🟡 Villkorat godkänt / godkänt för årsberäkning** — antingen saknas en entydig publicerad månadsfördelning, eller så är beräkningen bara entydig med ett leverantörsvärde som effekt, effektgrupp eller uttagsfaktor. Det uttryckliga villkoret på tariffens rad måste bevaras; okända värden får inte härledas eller ges ett standardvärde.
- **⛔ Ej godkänt** — minst en materiell uppgift saknas eller motsägs av källorna.
- **ℹ️ Redan verifierad utanför katalogspåret** — tariffen har en separat implementation och validering; katalogposten hålls ändå avstängd tills dess motorarbete är klart.
- En ikryssad huvudrad betyder att samtliga ursprungliga verifieringsvillkor i den här listan är lösta. En huvudrad kan därför vara okryssad trots att årsunderlaget är godkänt.

**Verifieringsomgång 2026-09-04:** Samtliga 72 poster är nu hanterade. Av de 71 katalogtariffer som källgranskats mot leverantörernas egna aktuella 2026-underlag har 28 fullständigt källunderlag även för månadsmodell, 31 är villkorat godkända eller godkända endast för årsberäkning och 12 är fortsatt underkända. Den återstående posten, Stockholm Exergi, är redan separat implementerad och fakturavaliderad enligt undantaget nedan. Antalen i sammanfattningen nedan beskriver fortfarande vad som faktiskt finns i kalkylatorn och ändras inte av denna källgranskning.

**Fortsatt arbete:** se [to-do-listan med ansvar för Robert, Claude, Codex och leverantörerna](todo-godkanna-fler-fjarrvarmetariffer.md).

**Viktigt undantag — Stockholm Exergi:** bolaget listas nedan i Del B (dess katalogpost `stockholm-exergi-stockholm-exergi-normal-2026` avvisas för `energiform`), men Stockholm Exergi är redan den mest rigoröst verifierade leverantören i kalkylatorn — inte via katalogen, utan via en fristående, handbyggd leverantörsfil (`enkey-agents/skills/ellen/leverantor-stockholm-exergi.md`) verifierad mot 18 riktiga fakturor för Brf Åkermannen 33. Samma sak gäller riksgenomsnittet (`leverantor-riksgenomsnitt.md`), som inte har någon katalogpost alls. Ingen av dessa två behöver arbete från den här listan — ta bara med det om katalogens egen extraktion av Stockholm Exergi någon gång ska ersätta eller komplettera leverantörsfilen.

## Sammanfattning

| | Antal tariffer | Antal bolag |
|---|---:|---:|
| Godkända (i kalkylatorn i dag) | 6 | 5 |
| Del A — utreds, data att verifiera | 65 | 44 |
| Del B — kräver motorstöd (Fas 2) | 7 | 6 |
| **Totalt i katalogen** | **78** | **53** |

---

## Del A — Data att verifiera (65 tariffer, 44 bolag)

### Borlänge Energi

- [ ] **Borlänge** (`borlange-energi-borlange-2026`)
  - Källa: [officiell prislista för näringsidkare 2026](https://www.borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare) (`borlange-web`)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast med leverantörens effektgrupp.** Aktuell prislista bekräftar 559 SEK/MWh även september–oktober, övriga energimånader, effektbelopp, effektgrund och flödespris. Automatisk gruppindelning får inte användas vid 501 kW eller i luckan direkt ovanför.
  - [x] Energipriset 559 SEK/MWh för september–oktober är bekräftat i aktuell officiell 2026-tabell.
  - [ ] Effektgränsen är fortfarande motsägelsefull: föregående grupp slutar vid 500 kW och nästa anges som ”mer än 501 kW”. Be leverantören bekräfta hur exakt 501 kW och intervallet upp till men inte över 501 ska hanteras.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### C4 Energi

- [ ] **Kristianstad** (`c4-energi-kristianstad-2026`)
  - Källor: [officiell prislista och villkor 2026](https://www.c4energi.se/foretag/fjarrvarme/priser-och-villkor/), [Prisdialogens prisändringsmodell 2026 (PDF)](https://www.prisdialogen.se/wp-content/uploads/2025/08/Prisandringsmodell-2026-C4-Energi.pdf) (`02_0` s.8)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast med leverantörens effektgrupp.** Energiperioder, årsformler, effektbelopp och effektgrund stämmer med katalogen. Automatisk gruppindelning vid 500 kW är inte godkänd.
  - [ ] Exakt 500 kW saknar entydig grupp i publicerad tabell. Energienheten har verifierats på aktuell webbplats.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### E.ON - Järfälla

- Gemensamma källor: [E.ON:s aktuella prissida för företag](https://www.eon.se/foeretag/vaerme-och-kyla/fjarrvarme/fjarrvarmepriser) och [officiell prislista och fullständiga prisvillkor 2026 för Bro, Bålsta, Järfälla och Kungsängen (PDF)](https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) (`03_0` s.4 och den aktuella tvåsidiga prislistan)
- **Gemensamt verifierat 2026-09-04:** Alla katalogpriser stämmer. Effektpriset är per kW och månad. För fullvärmekunder beräknas månadens effekt genom linjär regression av vardagarnas dygnsmedeleffekt vid utetemperatur under 15 °C, vid −15 °C, under den rullande perioden från månad 13 till månad 2 före fakturamånaden. Om underlaget inte uppfyller villkoren används medel av de tre högsta dygnsmedeleffekterna november–mars. För kunder där en annan värmekälla levererar bas- eller delvärme används i stället medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste 36 månaderna, inklusive fakturamånaden. Flödeskorrigeringen är månadens volym × grundpris × `0,02 × (månadens medelframledningstemperatur − 60) + 0,2`. Prisvillkoren anger endast tre kostnadsdelar — effekt, energi och flöde — så separat fast avgift är verifierad noll.
- [x] **Järfälla och Upplands-Bro – Bostäder** (`e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`)
  - **✅ Källunderlag godkänt.** Månadsdebitering och samtliga ursprungliga verifieringsvillkor är lösta. Katalogen behöver mappa `capacity.rate_period: "month"`, båda effektmetoderna och den fullständiga flödeskorrigeringen före aktivering, eller uttryckligen begränsa posten till fullvärmekunder.
- [x] **Järfälla och Upplands-Bro – Övriga fastigheter** (`e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`)
  - **✅ Källunderlag godkänt.** Samma verifierade månadsmodell och beräkningsregler som för bostäder, med prislistans belopp för övriga fastigheter.

### E.ON - Malmö

- Gemensamma källor: [E.ON:s aktuella prissida för företag](https://www.eon.se/foeretag/vaerme-och-kyla/fjarrvarme/fjarrvarmepriser) och [officiell prislista och fullständiga prisvillkor 2026 för Malmö och Burlöv (PDF)](https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) (`04_0` s.4 och den aktuella tvåsidiga prislistan)
- **Gemensamt verifierat 2026-09-04:** Alla publicerade priser stämmer. Effektpris, rullande månadsberäkning, reservregel, flödeskorrigering och avsaknad av separat fast avgift följer samma regler som i Järfälla ovan. Ortens beräkningstemperatur är dock −8 °C.
- [x] **Malmö och Burlöv – Bostäder** (`e-on-malmo-malmo-och-burlov-bostader-2026`)
  - **✅ Källunderlag godkänt, men katalogrättelse krävs.** Katalogens `billing_basis_temperature_c: -15` ska ändras till `-8`. Månadsenheten, båda effektmetoderna och flödesformeln måste samtidigt mappas före aktivering, alternativt ska posten begränsas till fullvärmekunder.
- [x] **Malmö och Burlöv – Övriga fastigheter** (`e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`)
  - **✅ Källunderlag godkänt, men katalogrättelse krävs.** Samma temperaturkorrigering från −15 till −8 °C och samma verifierade månadsmodell gäller som för bostäder.

### Eskilstuna Energi och Miljö

- [ ] **Eskilstuna** (`eskilstuna-energi-och-miljo-eskilstuna-2026`)
  - Källor: [officiell prislista 2026](https://www.eem.se/foretag/fjarrvarme/priser), [officiell prismodell](https://www.eem.se/foretag/fjarrvarme/priser/prismodell), [officiell flödestaxa](https://www.eem.se/foretag/fjarrvarme/redan-fjarrvarmekund/flodestaxa) (`05_1` s.1 samt webbkällorna i katalogen)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Energipris, samtliga effektintervall, årsavgifter och flödeskomponent överensstämmer med katalogen. Använd leverantörens prisgrundande effekt/band.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Falu Energi & Vatten

- [ ] **Falun** (`falu-energi-vatten-falun-2026`)
  - Källor: [officiell pris- och avtalssida](https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html), [officiell prisändringsmodell 2026 (PDF)](https://fev.se/download/18.2d00c01419a0a2a583253004/1762859522143/Pris%C3%A4ndringsmodell%202026.pdf) (`06_0` s.6)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Säsongsenergi, effektgrupper, årsformel, effektgrund och flödespris stämmer med katalogen.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Bjursås, Grycksbo, Sundborn, Svärdsjö** (`falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`)
  - Källor: [officiell pris- och avtalssida för ytterorterna](https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html), [officiell prisändringsmodell 2026 (PDF)](https://fev.se/download/18.2d00c01419a0a2a583253004/1762859522143/Pris%C3%A4ndringsmodell%202026.pdf) (`06_0` s.7)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast för 0–500 kW.** Samtliga publicerade priser, effektgrunden och flödeskomponenten stämmer med katalogen. Motorn måste stoppa eller kräva särskilt avtal över 500 kW.
  - [ ] Publicerad prislista för ytterorterna innehåller endast effektgrupper till och med 500 kW.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Gävle Energi

- [ ] **Gävle** (`gavle-energi-gavle-2026`)
  - Källor: [officiell prislista 2026](https://www.gavleenergi.se/foretag/fjarrvarme/fjarrvarmeavgifter/), [officiella prisvillkor](https://www.gavleenergi.se/dokument/prisvillkor-fjarrvarme-naringsverksamhet/) (`08_0` s.4,5)
  - **⛔ Ej godkänt 2026-09-04.** Kapacitetspris, energisäsonger, dygnsperiodisering och att separat fast avgift saknas är verifierade. Däremot anger katalogen ett *marginalt* volymavdrag, medan de officiella villkoren bara säger att avdraget baseras på ackumulerad kalenderårsvolym och erhålls månadsvis. Det framgår inte om tabellens avdrag gäller endast marginalvolymen eller hela månadens volym efter uppnådd nivå.
  - [x] Kapacitetskostnaden periodiseras lika per kalenderdygn och debiteras för antal dygn på respektive månads faktura.
  - [x] `null` i fast avgift kan ersättas med verifierad noll: den officiella formeln är enbart `kapacitetsbehov × kapacitetspris`.
  - [ ] Begär leverantörsbesked eller faktura som visar exakt hur volymavdragets nivåskiften beräknas.

### Habo Energi

- [ ] **Habo** (`habo-energi-habo-2026`)
  - Källor: [officiell prislista för företag 2026](https://www.haboenergi.se/varme-miljo-foretag/), [officiellt besked om prisändring 2026](https://www.haboenergi.se/2025/10/28/prisandring-fjarrvarme-2026/) (`11_0` s.14)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Fast årsavgift, effektpris per kW och år, tre energisäsonger samt flödespris överensstämmer med katalogen.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Härnösand Energi & Miljö

- [ ] **Härnösand** (`harnosand-energi-miljo-harnosand-2026`)
  - Källa: [officiell prislista för flerbostadshus och lokaler 2026 (PDF)](https://www.hemab.se/download/18.727ad6af19ac23cdb98120ae/1764247260203/Prislista%2520flerbostadshus%25202026.pdf) (`13_1` s.1,2)
  - **⛔ Ej godkänt 2026-09-04.** Den aktuella officiella prislistan innehåller samma interna motsägelse som tidigare underlag. För 1 750 MWh använder exemplet 750 MWh × 42,90 och inget på 65,00-nivån, medan tabellen anger 42,90 endast för 1 001–1 500 MWh och 65,00 för 1 501–2 000 MWh. Övriga priser, 1/12-periodisering och avräkning av rabatten på årets sista faktura är tydliga.
  - [ ] Begär ett skriftligt leverantörsbesked om korrekt intervallformel eller ett korrigerat räkneexempel innan volymrabatten implementeras.

### Hässleholm Miljö

- [ ] **Hässleholm** (`hassleholm-miljo-hassleholm-2026`)
  - Källor: [officiell prislista Hässleholm 2026](https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-hassleholm), [officiell beskrivning av prismodellen](https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell) (`14_0` s.11)
  - **⛔ Ej godkänt 2026-09-04.** Effekt-, energi- och flödespriser samt månadsenheter stämmer med katalogen. De officiella sidorna beskriver dock bara rabatten per effektintervall och säger inte om rabattpriset multipliceras med hela effekten eller enbart effekten inom respektive intervall.
  - [ ] Bekräfta om effektrabatten gäller hela effekten eller intervallvis.
- [ ] **Tyringe** (`hassleholm-miljo-tyringe-2026`)
  - Källor: [officiell prislista Tyringe 2026](https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-tyringe), [officiell beskrivning av prismodellen](https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell) (`14_0` s.11)
  - **⛔ Ej godkänt 2026-09-04.** Effekt-, energi- och flödespriser samt månadsenheter stämmer med katalogen. De officiella sidorna beskriver dock bara rabatten per effektintervall och säger inte om rabattpriset multipliceras med hela effekten eller enbart effekten inom respektive intervall.
  - [ ] Bekräfta om effektrabatten gäller hela effekten eller intervallvis.

### Jämtkraft

- [ ] **Östersund, Frösön, Ås** (`jamtkraft-ostersund-froson-as-2026`)
  - Källor: [officiell prismodell](https://www.jamtkraft.se/foretag/fjarrvarme/priser/prismodell/), [officiell prisändringsmodell och prislista 2026–2028](https://www.jamtkraft.se/wt/documents/519/Pris%C3%A4ndringsmodellen_2026-2028.pdf) (`15_0` s.18–19)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Alla katalogpriser, effektintervall, säsonger och flödesformeln stämmer. Debiteringseffekten är medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste tolv månaderna; ett fastställt värde gäller tills ett högre värde mäts, dock längst tolv månader. Detta måste mappas i katalogen före implementation.
  - [x] Metod för debiterbar effekt/kapacitet verifierad; uppdatera `billing_basis_method` från `null` enligt beskrivningen ovan.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Brunflo och Opevägen** (`jamtkraft-brunflo-och-opevagen-2026`)
  - Källor: [officiell prismodell](https://www.jamtkraft.se/foretag/fjarrvarme/priser/prismodell/), [officiell prisändringsmodell och prislista 2026–2028](https://www.jamtkraft.se/wt/documents/519/Pris%C3%A4ndringsmodellen_2026-2028.pdf) (`15_0` s.18–19)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Alla katalogpriser, effektintervall, säsonger och flödesformeln stämmer. Debiteringseffekten är medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste tolv månaderna; ett fastställt värde gäller tills ett högre värde mäts, dock längst tolv månader. Detta måste mappas i katalogen före implementation.
  - [x] Metod för debiterbar effekt/kapacitet verifierad; uppdatera `billing_basis_method` från `null` enligt beskrivningen ovan.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Åre, Järpen, Mörsil, Duved, Kall, Hallen, Krokom, Nälden, Föllinge** (`jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`)
  - Källor: [officiell prismodell](https://www.jamtkraft.se/foretag/fjarrvarme/priser/prismodell/), [officiell prisändringsmodell och prislista 2026–2028](https://www.jamtkraft.se/wt/documents/519/Pris%C3%A4ndringsmodellen_2026-2028.pdf) (`15_0` s.18–19)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Alla katalogpriser, effektintervall, säsonger och flödesformeln stämmer. Debiteringseffekten är medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste tolv månaderna; ett fastställt värde gäller tills ett högre värde mäts, dock längst tolv månader. Detta måste mappas i katalogen före implementation.
  - [x] Metod för debiterbar effekt/kapacitet verifierad; uppdatera `billing_basis_method` från `null` enligt beskrivningen ovan.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Jönköping Energi

- [ ] **Jönköping och Gränna** (`jonkoping-energi-jonkoping-och-granna-2026`)
  - Källor: [officiell prislista 2026](https://jonkopingenergi.se/foretag/fjarrvarme/fjarrvarme/priser), [officiell förklaring av fjärrvärmekostnaden](https://jonkopingenergi.se/foretag/kundcenter/guider/vad-bestar-fjarrvarmekostnaden-av) (`16_0` s.36–37)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Energi-, effekt- och flödespriser samt intervall stämmer. Debiteringseffekten är medelvärdet av de tre högsta värdena bland de fem högsta dygnsmedeleffekterna under de senaste tolv månaderna; detta måste mappas i katalogen. Prislistan nämner dessutom en accessavgift om 0, 10, 25 eller 50 kr/månad för avtal tecknade från 2024, beroende på avtalad åtkomst. Den är avtalsspecifik och ingår inte i den här godkända kärntariffen.
  - [x] Metod för debiterbar effekt/kapacitet verifierad; uppdatera `billing_basis_method` från `null` enligt beskrivningen ovan.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Karlstads Energi

- [x] **Karlstad** (`karlstads-energi-karlstad-2026`)
  - Källa: [officiell prislista 2026](https://karlstadsenergi.se/foretag/fjarrvarme/priser) (`17_1` s.1)
  - **✅ Källunderlag godkänt 2026-09-04.** Tabellen anger fast pris i `kr/mån`; leverantörens årsexempel bekräftar att både fast del och effektpris tas ut varje månad. Energimånader, effektintervall och belopp stämmer med katalogen. `capacity.rate_period: month` är rätt representation; ingen årsavgift ska först divideras med 12.
  - [x] Månadsperiodisering verifierad genom månadsenheten och leverantörens publicerade årsexempel.

### Kils Energi

- [ ] **Kil** (`kils-energi-kil-2026`)
  - Källor: [officiell pris- och informationssida](https://kilsenergi.kil.se/kils-energi/fjarrvarme/varme-och-varmvatten-till-konkurrenskraftiga-priser), [officiell normalprislista 2026 (PDF)](https://bolag.kil.se/download/18.1b9e2707199c916c9d91010c/1761112730710/Fj%C3%A4rrv%C3%A4rmeavgifter%202026%20normalprislista.pdf) (`18_0` s.17, `web-review-kil-vat` s.4–5 och `kil-user-supplied-pricelist`)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast med avtalets kategorital eller leverantörens effektvärde.** Energipris, effektpriser och momsgrund stämmer. Effektbehovet beräknas som årsförbrukning `W` dividerad med avtalat kategorital `n`; källan anger 2 500 som normalt värde för hyres- och mindre affärslokaler men detta får inte antas för alla kunder. Publicerade årsexempel verifierar att ingen separat fast avgift tillkommer.
  - [x] Metod för debiterbar effekt är verifierad men kräver kundens avtalade kategorital; uppdatera `billing_basis_method` och använd leverantörsvärdet när kategoritalet saknas.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
  - [x] `null` i fast avgift kan ersättas med verifierad noll.

### Kraftringen

- [ ] **Kraftringen** (`kraftringen-kraftringen-2026`)
  - Källa: [officiell prislista och prismodell för företag 2026](https://www.kraftringen.se/brf/varme-och-kylalosningar/fjarrvarme/fjarrvarmepriser/) (`19_0` s.6 och `web-review-kraftringen-model`)
  - **🟡 Godkänt för årsberäkning 2026-09-04 för Kraftringens ordinarie nät, inte lågtemperaturnätet Brunnshög.** Energiperioder, årsvis effektpris, kumulativa effektgränser, effektgrund och flödesformel stämmer. Den officiella sidan beskriver endast tre kostnadsdelar och årsjämförelserna bekräftar att ingen separat fast avgift finns.
  - [x] Sätt `capacity.rate_period: year`, `fixed: 0` och mappa flödespriset som `flöde_m3 × 10,40 × max(0,2; 0,2 + (Tf − 60) × 0,02)`, där `Tf` är förbrukningsvägt månadsmedel för framledningstemperaturen.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Lidköping Energi

**Externt källunderlag GODKÄNT 2026-09-09** (bedömning
[`2026-09-09-006`](../conversations/reviews/2026/09/2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md),
gäller BÅDA raderna nedan). Lidköping Energis värmenätschef svarade skriftligt 2026-09-09
10:07 på de öppna frågorna nedan. Lokalt arkiverad källa:
`Fjarrvarmetariffer/Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf`
(tre sidor, sida 3 hänvisar bara till en separat, inte inbäddad bilaga
`prismodell komersiella.pdf`), `source_sha256:
93b47766933ba2cd6c841db982cc0981a4b44ec39fe08ff543b3c707746e8f34`. **Råfilen innehåller
kontaktuppgifter och är INTE tillagd i git eller pushad — kräver Roberts separata beslut.**
Bekräftade svar:
1. Publicerade företagspriser läses exklusive moms (webbsidans "inklusive moms" är fel);
   katalogens `vat_basis: "excluded"` är korrekt.
2. Flödesavgift/-premie gäller samtliga kommersiella kunder i prisgrupp 2–5.
3. Flödesprisfaktorn är `N = 5 kr/m³`.
4. Formeln är `N × Q × (1 − T/Tm)`.
5. `Tm` är nätets månadsvisa medel av samtliga anläggningars `T_in − T_ut`.
6. Komponenten gäller alla månader, debiteras/krediteras månadsvis.
7. Debiterbar effekt: i första hand effektsignatur vid −10 °C (dygnsvärden december–februari,
   två senaste vintrarna); i andra hand högsta uppmätta dygnsmedeleffekt. Den redan beslutade
   säkra produktvägen kan fortsatt kräva leverantörens fastställda effekt i stället för att
   återskapa signaturen.
8. Fasta års-/effektavgifter periodiseras 1/12 per månad.

**Källgodkännande ≠ implementation/fakturavalidering.** `Tm`s tolv faktiska månadsutfall är
INTE angivna i svaret (metoden är källbelagd, inte de tolv talen) — det är ett runtimekrav
per kundfall, inte ett statiskt katalogvärde. Se
[`tariffinventering-v16.md`](tariffinventering-v16.md) §6a.7 och `batchplan-v16.md` batch 5d
för den planerade, ännu ej genomförda implementationen.

- [x] **Lidköping 0–41 kW** (`lidkoping-energi-lidkoping-041-kw-2026`)
  - Källor: [officiell företagsprislista 2026](https://lidkopingenergi.se/foretag/), [officiell prisändringsmodell 2026](https://lidkopingenergi.se/wp-content/uploads/2025/10/Prisandringsmodell-Fjarrvarme-2026.pdf), [officiellt länkad detaljerad modell för kommersiella kunder](https://2023.lidkopingsenergi.se/wp-content/uploads/2022/11/prismodell-komersiella.pdf) (`20_1` s.1), samt leverantörssvaret 2026-09-09 ovan
  - **🟢 Källunderlag godkänt 2026-09-09.** Energi-, effekt- och fasta priser, intervall och minimieffekt stämde redan. Flödesavgiften/-premien som 2026-modellen anger för kommersiella kunder är nu källbelagd i sin helhet (`N`, formel, `Tm`-metod) genom leverantörssvaret ovan.
  - [x] Effektmetoden är källbelagd: i första hand effektsignatur vid −10 °C från dygnsvärden december–februari för de två senaste vintrarna; i andra hand högsta dygnsmedeleffekt under samma period. Leverantörens fastställda effekt bör användas tills hela metoden implementerats.
  - [x] Flödesjusteringens `N` och hur `Tm` tillhandahålls är källbelagda (leverantörssvar 2026-09-09). Kvarstår: implementation (batch 5d) och att `Tm`s tolv faktiska månadsvärden hämtas per kundfall (runtime, inte katalogstatiskt).
  - [ ] Månadsperiodisering (1/12 för fasta avgifter) är källbelagd men behöver verifieras i implementationen; årsbelopp får inte automatiskt delas med 12 utan kontroll.
- [x] **Lidköping 42+ kW** (`lidkoping-energi-lidkoping-42-kw-2026`)
  - Källor: [officiell företagsprislista 2026](https://lidkopingenergi.se/foretag/), [officiell prisändringsmodell 2026](https://lidkopingenergi.se/wp-content/uploads/2025/10/Prisandringsmodell-Fjarrvarme-2026.pdf), [officiellt länkad detaljerad modell för kommersiella kunder](https://2023.lidkopingsenergi.se/wp-content/uploads/2022/11/prismodell-komersiella.pdf) (`20_1` s.1), samt leverantörssvaret 2026-09-09 ovan
  - **🟢 Källunderlag godkänt 2026-09-09.** Samma godkännande som Lidköping 0–41 kW ovan (samma leverantörssvar, samma `N`/formel/`Tm`-metod).
  - [x] Effektmetoden är källbelagd: i första hand effektsignatur vid −10 °C från dygnsvärden december–februari för de två senaste vintrarna; i andra hand högsta dygnsmedeleffekt under samma period. Leverantörens fastställda effekt bör användas tills hela metoden implementerats.
  - [x] Flödesjusteringens `N` och hur `Tm` tillhandahålls är källbelagda (leverantörssvar 2026-09-09). Kvarstår: implementation (batch 5d) och att `Tm`s tolv faktiska månadsvärden hämtas per kundfall (runtime, inte katalogstatiskt).
  - [ ] Månadsperiodisering (1/12 för fasta avgifter) är källbelagd men behöver verifieras i implementationen; årsbelopp får inte automatiskt delas med 12 utan kontroll.

### Luleå Energi

- [ ] **Luleå** (`lulea-energi-lulea-2026`)
  - Källa: [officiell företagsprislista och prismodell 2026](https://www.luleaenergi.se/produktion-och-infrastruktur/fjarrvarme/priser-och-avtalsvillkor/lulea-foretag-2026/) (`21_0` s.8–9)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast med leverantörens effektvärde eller bekräftade effektgrupp.** Energi-, effekt- och flödespriser, säsonger och intervall stämmer med katalogen. Den publika beskrivningen definierar dygnsmedeleffekt som dygnets energianvändning dividerad med 24, men anger inte hur många värden som väljs, deras tidsfönster eller hur de sammanvägs.
  - [ ] Fullständig regel för debiterbar effekt behöver bekräftas av Luleå Energi och mappas.
  - [ ] Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd leverantörens fakturavärde tills villkoren implementerats.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Mjölby Svartådalen Energi

- [ ] **Mjölby** (`mjolby-svartadalen-energi-mjolby-2026`)
  - Källa: [officiell prislista för företag 2026](https://www.mse.se/foretag/fjarrvarme/priser) (`23_0` s.3)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Energiperioder, effektgrupper, årsformel, effektsignatur och flödespris stämmer med katalogen.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Mälarenergi

- [ ] **Västerås och Hallstahammar, 2–4 lägenheter** (`malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`)
  - Källor: [officiell prislista för mindre flerbostadshus 2026](https://www.malarenergi.se/fjarrvarme/pris-for-fjarrvarme/), [officiell tabell för flödespremie](https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/) (`22_0` s.5, `web-review-malar-price` och `web-review-malar-flow`)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Den momsexkluderade katalogposten motsvarar exakt den officiella prislistans energipriser 985/780/295, flödespris 2 kr/m³ och fast årsavgift 9 855 kr inklusive moms efter division med 1,25.
  - [ ] Månadsperiodisering av den fasta årsavgiften saknas; årsbeloppet får inte automatiskt delas med 12.

### Navirum Energi - Norrköping och Söderköping

- Gemensam källa: [officiell prislista och fullständiga prisvillkor 2026 för Norrköping och Söderköping (PDF)](https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) (`25_0` s.4 och den aktuella tvåsidiga prislistan)
- **Gemensamt verifierat 2026-09-04:** Alla katalogpriser stämmer. Effektpriset är per kW och månad. Fullvärmekundens effekt regressionsberäknas vid −15 °C med samma rullande mätperiod, kvalitetskrav och reservregel som i E.ON-villkoren ovan. För bas- eller delvärme från en annan värmekälla gäller i stället tre högsta dygnsmedeleffekter under 36 månader, inklusive fakturamånaden. Flödeskorrigeringen följer `månadens volym × grundpris × (0,02 × (medelframledningstemperatur − 60) + 0,2)`. Separat fast avgift saknas och är verifierad noll.
- [x] **Norrköping och Söderköping – Bostäder** (`navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`)
  - **✅ Källunderlag godkänt.** Månadsdebitering och samtliga ursprungliga verifieringsvillkor är lösta. Katalogen måste mappa månadsenheten, båda effektmetoderna och flödesformeln före aktivering, eller uttryckligen begränsa posten till fullvärmekunder.
- [x] **Norrköping och Söderköping – Övriga fastigheter** (`navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`)
  - **✅ Källunderlag godkänt.** Samma verifierade månadsmodell som för bostäder, med prislistans belopp för övriga fastigheter.

### Navirum Energi - Örebro, Kumla och Hallsberg

- Gemensam källa: [officiell prislista och fullständiga prisvillkor 2026 för Hallsberg, Kumla och Örebro (PDF)](https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) (`26_0` s.4 och den aktuella tvåsidiga prislistan)
- **Gemensamt verifierat 2026-09-04:** Alla katalogpriser stämmer. Effektpriset är per kW och månad. Fullvärmekundens effekt regressionsberäknas vid −15 °C med samma rullande mätperiod, kvalitetskrav och reservregel som ovan; samma alternativa 36-månadersmetod gäller för bas- eller delvärme från annan värmekälla. Samma fullständiga flödeskorrigering gäller. Separat fast avgift saknas och är verifierad noll.
- [x] **Örebro, Kumla och Hallsberg – Bostäder** (`navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`)
  - **✅ Källunderlag godkänt.** Månadsdebitering och samtliga ursprungliga verifieringsvillkor är lösta. Katalogen måste mappa månadsenheten, båda effektmetoderna och flödesformeln före aktivering, eller uttryckligen begränsa posten till fullvärmekunder.
- [x] **Örebro, Kumla och Hallsberg – Övriga fastigheter** (`navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`)
  - **✅ Källunderlag godkänt.** Samma verifierade månadsmodell som för bostäder, med prislistans belopp för övriga fastigheter.

### Nevel

- [ ] **Gimo, Österbybruk och Östhammar** (`nevel-gimo-osterbybruk-och-osthammar-2026`)
  - Källa: [officiell lokal prislista och prismodell 2026](https://nevel.com/sv/fjarrvarme/gimo/) (`27_0` s.5)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Samtliga energi-, effekt-, grund- och flödespriser, intervall och minimieffekt stämmer. Debiteringseffekten är medelvärdet av de två senaste årens medeleffektuttag baserat på normalårskorrigerad värmeanvändning januari–februari och revideras den 1 juli; använd fakturans E-värde tills metoden implementerats.
  - [x] Metod för debiterbar effekt verifierad; uppdatera `billing_basis_method` från `null` enligt beskrivningen ovan.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Partille Energi

- [ ] **Partille** (`partille-energi-partille-2026`)
  - Källa: [officiell prislista Fjärrvärme Grund 2026](https://partilleenergi.se/foretag/fjarrvarme-for-foretag/) (`31_0` s.9,10)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Energisäsonger, fasta årsdelar, rörliga effektpriser, effektgrund och returtemperaturkomponent stämmer. Välj leverantörens band vid gränsen 2 500 kW eftersom webbrubriken inte visar ett entydigt större-än-tecken.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### PiteEnergi

- [ ] **Piteå centrala nätet** (`piteenergi-pitea-centrala-natet-2026`)
  - Källa: [officiell prislista för centrala nätet 2026](https://www.piteenergi.se/fjarrvarme/priser-foretag/) (`pite-central`)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Effektgruppernas fasta och rörliga årsdelar, två energisäsonger och vinterflöde stämmer med katalogen. Använd leverantörens uppmätta effekt/band.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Norrfjärden och Sjulnäs** (`piteenergi-norrfjarden-och-sjulnas-2026`)
  - Källa: [officiell prislista för Norrfjärden och Sjulnäs 2026](https://www.piteenergi.se/fjarrvarme/priser-2-foretag/) (`pite-small`)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Effektgruppernas fasta och rörliga årsdelar, två energisäsonger och vinterflöde stämmer med katalogen. Använd leverantörens uppmätta effekt/band.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Sandviken Energi

- [x] **Sandviken normal** (`sandviken-energi-sandviken-normal-2026`)
  - Källor: [officiell prislista för näringsidkare 2026](https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme.7681.html), [officiell effektmodell](https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme/saberaknasdineffekt.7682.html) (`33_0` s.8)
  - **✅ Källunderlag godkänt 2026-09-04 för helleverans.** Energipris, effektgrupper, fasta årsdelar och effektpriser stämmer. Effektbehovet beräknas normalt med effektsignatur vid −16 °C från föregående vinters dygnsvärden oktober–april; utan tillräckligt temperatursamband används medelvärdet av de två senaste årens högsta dygnsmedeleffekt. Använd leverantörens effektvärde tills metoden implementerats.
  - [x] Månadsperiodisering verifierad: effekt- och fast avgift fördelas jämnt per kalenderdygn och debiteras månadsvis; energi baseras på månadens uppmätta förbrukning.

### Skellefteå Kraft

- [ ] **Skellefteå, Skelleftehamn, Ursviken, Lycksele, Malå** (`skelleftea-kraft-skelleftea-skelleftehamn-ursviken-lycksele-mala-2026`)
  - Källor: [officiell pris- och modellsida 2026](https://www.skekraft.se/foretag/fjarrvarme/pris-pa-fjarrvarme-till-foretag/), [officiell prislista för kraftvärmeorter 2026 (PDF)](https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_kraftvarmeort_2026.pdf) (`34_1` s.1 och `web-review-skelleftea-final` s.1–2)
  - **⛔ Ej godkänt 2026-09-04.** Energi-, kapacitets-, övertrasserings- och avkylningspriser samt kalenderdagsperiodisering stämmer. Prislistan anger dock ingen valutaenhet för resultatet av energirabatten `Qnorm × A + B`. Talområdet gör öre/kWh sannolikt, men detta får inte antas. Ursviken saknar dessutom uttrycklig dimensionerande temperatur i ortstabellen.
  - [x] `null` i fast avgift kan ersättas med verifierad noll; prislistan anger ingen separat fast avgift.
  - [ ] Be Skellefteå Kraft bekräfta att rabattresultatet är öre/kWh och ange dimensionerande temperatur för Ursviken, alternativt använd leverantörens kapacitetsvärde.
- [ ] **Boliden, Bureå, Burträsk, Byske, Jörn, Kåge, Lövånger, Norsjö, Robertsfors, Stensele, Storuman, Vindeln, Ånäset** (`skelleftea-kraft-boliden-burea-burtrask-byske-jorn-kage-lovanger-norsjo-robertsfors-stensele-storuman-vindeln-anaset-2026`)
  - Källor: [officiell pris- och modellsida 2026](https://www.skekraft.se/foretag/fjarrvarme/pris-pa-fjarrvarme-till-foretag/), [officiell prislista för pelletsorter 2026 (PDF)](https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_pelletsort_2026.pdf) (`34_2` s.1 och `web-review-skelleftea-final` s.1–2)
  - **⛔ Ej godkänt 2026-09-04.** Energi-, kapacitets-, övertrasserings- och avkylningspriser samt kalenderdagsperiodisering stämmer. Prislistan anger dock ingen valutaenhet för resultatet av energirabatten `Qnorm × A + B`. Talområdet gör öre/kWh sannolikt, men detta får inte antas. Stensele saknar dessutom uttrycklig dimensionerande temperatur i ortstabellen.
  - [x] `null` i fast avgift kan ersättas med verifierad noll; prislistan anger ingen separat fast avgift.
  - [ ] Be Skellefteå Kraft bekräfta att rabattresultatet är öre/kWh och ange dimensionerande temperatur för Stensele, alternativt använd leverantörens kapacitetsvärde.

### Skövde Energi

- [ ] **Skövde** (`skovde-energi-skovde-2026`)
  - Källa: [officiell fjärrvärmetaxa 2026 inklusive moms](https://skovdeenergi.se/fjarrvarme/priser-avgifter/taxa-fjarrvarme-2026-inklusive-moms/) (`35_0` s.13)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Katalogens momsexkluderade energipriser och effektpris motsvarar exakt de officiella beloppen dividerade med 1,25. Effektgrunden och månadsvis debitering är bekräftade, men källan anger inte uttryckligen hur årsavgiften fördelas mellan månaderna.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Sundsvall Energi

- [ ] **Sundsvall normal** (`sundsvall-energi-sundsvall-normal-2026`)
  - Källor: [officiell prislista och fullständiga prisvillkor 2026](https://sundsvallenergi.se/foretag-och-brf/fjarrvarme/fjarrvarme-for-verksamheten/fjarrvarmepriser), [officiell formelbild för flödespremie/-avgift](https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG) (`39_0` s.2 och `web-review-sundsvall-flow`)
  - **⛔ Ej godkänt 2026-09-04.** Alla priser till och med 1 999 kW, effektmetod och 1/12-periodisering är verifierade; 2 000 kW och högre har uttryckligen individuella villkor. Katalogposten saknar däremot hela den obligatoriska flödespremien/-avgiften. Formeln är `(Qkund/Wkund − Qalla/Walla) × 5 kr/m³ × Wkund` för januari–april och oktober–december.
  - [ ] Lägg till flödesjusteringen och kräv månadens nätvärde `Qalla/Walla`; blockera automatisk prissättning från 2 000 kW.
- [x] **Matfors och Kvissleby normal** (`sundsvall-energi-matfors-och-kvissleby-normal-2026`)
  - Källor: [officiell lokal prislista och prisvillkor 2026](https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-kvissleby-njurunda), [officiell formelbild för flödespremie/-avgift](https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG) (`39_0` s.4, `web-review-matfors-final` och `web-review-sundsvall-flow`)
  - **✅ Källunderlag godkänt 2026-09-04 för normalleverans under 2 000 kW.** Energi- och effektpriser, fasta årsdelar, flödesformel, urvalsregel och effektkalibrering stämmer. Normalleverans kräver över 2 000 utnyttjningstimmar; använd leverantörens kalibrerade effekt.
  - [x] Effektkostnaden faktureras med 1/12 per månad. Flödesjusteringen beräknas månadsvis januari–april och oktober–december. Från 2 000 kW gäller individuella villkor och motorn ska stoppa.

### Söderhamn Nära

- [ ] **Söderhamn företag, taxa 10–13** (`soderhamn-nara-soderhamn-taxa-11-och-12-2026`)
  - Källa: [officiell prislista för företag 2026](https://www.soderhamnnara.se/sidor/fjarrvarme/foretagskunder/priser-foretag.html) (`36_1` s.1)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Taxa 10–13, fasta årsavgifter, effektformler och energipris stämmer med katalogen. Sidan bekräftar månadsdebitering men inte explicit fördelning av årsbeloppen; använd leverantörens anslutningseffekt.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Södertörns Fjärrvärme

- [x] **Södertörns Fjärrvärme** (`sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`)
  - Källor: [officiell prislista Normal 2026 med prisvillkor (PDF)](https://sfab.se/media/33mnnexa/prislista-normal-2026.pdf), [officiell prisändringsmodell 2026 (PDF)](https://sfab.se/media/uwschiaj/prisandringsmodell-2026.pdf) (`37_0` s.11,12)
  - **✅ Källunderlag godkänt 2026-09-04 för Normal med SFAB:s rekommenderade effekt.** Prislistan verifierar energisäsonger, effektgrupper, returtemperatur och effektgrund. Prisvillkoret anger att effektkostnaden fördelas lika över 12 månader. Kundvald effekt har därutöver en överuttagsavgift om 1 032 kr/kW och ska inte aktiveras innan den regeln stöds.
  - [x] Månadsperiodisering verifierad: effektkostnaden fördelas lika över 12 månader och förbrukningsdelarna faktureras månadsvis i efterskott.

### TEMAB Fjärrvärme

- [ ] **Tierp, Karlholmsbruk och Örbyhus** (`temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`)
  - Källa: [officiell styrelsefastställd taxa för fjärrvärmeleveranser 2026 (PDF)](https://temab.tierp.se/download/18.7fa3d20319a7bbd966d1fe/1763023016779/Taxa%20f%C3%B6r%20Fj%C3%A4rrv%C3%A4rmeleveranser%202026.pdf) (`43_0` s.18 och `web-review-temab-final` s.3–4)
  - **🟡 Villkorat godkänt 2026-09-04 endast med TEMAB:s fastställda debiteringseffekt eller anslutningsvärde.** Alla prisbelopp, intervall, momsgrund och kalenderdagsperiodisering stämmer. Taxan säger att kategoritalsmetoden används men publicerar varken kategorital eller vilken energihistorik som ingår; vid nyanslutning eller när metoden inte passar används anslutningsvärdet.
  - [x] Fast avgift periodiseras efter `days_in_month/365` under 2026 och energi efter uppmätt månadsförbrukning.
  - [ ] Beräkna inte debiteringseffekten automatiskt utan bolagets värde; begär kategorital och historikperiod om metoden ska implementeras.

### Tekniska Verken - Katrineholm

- [ ] **Katrineholm** (`tekniska-verken-katrineholm-katrineholm-2026`)
  - Källa: [officiell prislista och prismodell för företag 2026](https://tekniskaverken.se/foretag/fjarrvarme/priser) (`40_0` s.3 och `web-review-tekniska-verken-2026`)
  - **🟡 Godkänt för årsberäkning 2026-09-04 med leverantörens effektsignatur och effektgrupp.** Den aktuella sidan bekräftar årsavgifter, effektpriser och energipriset 609 kr/MWh. Effektsignaturen är dygnsenergi/24, regressionsberäknad från 1 november–31 mars vid −17,7 °C och debiteringen använder medelvärdet av de två senaste årens signaturer. Effektpriset kalenderdagsfördelas, men sidan säger bara att den separata årsavgiften faktureras månadsvis; dess exakta månadsfördelning framgår inte. Intervallen 5–50, 51–250 osv. lämnar dessutom luckor om signaturen inte är heltalsavrundad.
  - [x] Metod för debiterbar effekt är verifierad; använd ändå leverantörens effektsignatur och effektgrupp tills avrundnings-/intervallregeln är bekräftad.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Tekniska Verken - Linköping

- [ ] **Linköping** (`tekniska-verken-linkoping-linkoping-2026`)
  - Källa: [officiell prislista och prismodell för företag 2026](https://tekniskaverken.se/foretag/fjarrvarme/priser) (`41_0` s.3 och `web-review-tekniska-verken-2026`)
  - **🟡 Godkänt för årsberäkning 2026-09-04 med leverantörens effektsignatur och effektgrupp.** Årsavgifter, effektpriser, tre energisäsonger och flödespriset 5,35 kr/m³ oktober–april stämmer. Effektsignaturen är dygnsenergi/24, regressionsberäknad från 1 november–31 mars vid −17,6 °C och debiteringen använder medelvärdet av de två senaste årens signaturer. Effektpriset kalenderdagsfördelas, men den separata årsavgiftens exakta månadsfördelning saknas. Intervallen 5–50, 51–250 osv. lämnar också luckor om signaturen inte är heltalsavrundad. Prislistan har dessutom ett separat halverat flödespris för lågtemperaturvärme; katalogposten gäller bara normal leverans.
  - [x] Metod för debiterbar effekt är verifierad; använd ändå leverantörens effektsignatur och effektgrupp tills avrundnings-/intervallregeln är bekräftad.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Telge Nät

- [x] **Telge företag och bostadsrättsföreningar** (`telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`)
  - Källa: [officiell prislista för företag och bostadsrättsföreningar 2026](https://www.telge.se/foretag/fjarrvarme-energi/kundservice/fjarrvarmepris/) och [Telge Näts prisvillkor, giltiga tills vidare från 2021-01-01](https://www.prisdialogen.se/wp-content/uploads/2020/11/TN-prislista-fjarrvarme-2025_Foretag.pdf) (`telge-attachment` s.1–2 och `telge-terms` s.3–5)
  - **✅ Källunderlag godkänt 2026-09-04.** 2026-sidan bekräftar alla belopp och säsonger. Tillsvidarevillkoren verifierar effektsignatur vid −11 °C från vardagsdygn under föregående 1 juli–30 juni, heltalsavrundning, alternativa historik-/toppregler, kalenderdagsfördelning, nyttjandetidstillägg och den stegvisa returtemperaturavgiften oktober–april. Prislistans formeltext för effekttillägg säger felaktigt ”effektpris” där enheten och villkoren visar att `effektbehov` ska användas; katalogens formel är den dimensionsriktiga tolkningen och bör fakturatestas.
  - [x] Villkoren är uttryckligen giltiga tills vidare och beskriver samma prismodell som den aktuella 2026-sidan; periodisering och beräkningsmetod är verifierade.

### Trollhättan Energi

- [ ] **Trollhättan** (`trollhattan-energi-trollhattan-2026`)
  - Källa: [officiell prislista och prismodell för företag 2026](https://www.trollhattanenergi.se/foretag/fjarrvarme/) (`44_0` s.7)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Tre energisäsonger, effektgruppernas fasta och rörliga årsdelar samt regeln för prisgrundande effekt stämmer med katalogen.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Umeå Energi

- [ ] **Umeå Enkel** (`umea-energi-umea-enkel-2026`)
  - Källa: [officiell prislista Enkel 2026](https://www.umeaenergi.se/foretag/varme/priser/prisavtal-enkel), [officiell förklaring av prismodellen](https://www.umeaenergi.se/foretag/varme/priser/prismodell) och [gällande särskilda prisvillkor (PDF)](https://a.storyblok.com/f/162274/x/bed500e2ec/prisvillkor-fjarrvarme.pdf) (`45_0` s.14, `web-review-umea-terms` s.1–2 och `web-review-umea-enkel`)
  - **🟡 Villkorat godkänt 2026-09-04 med Umeå Energis abonnerade effekt och uttagsfaktor.** Samtliga 2026-priser, intervall, energisäsonger och flödesformeln är verifierade. Årseffekten är medel av årets tre högsta fasta 12-timmarsblock (06–18/18–06), abonnerad effekt är medel av de tre föregående årseffekterna och hela `(k × A + m)` multipliceras med B. Effektpriset kalenderdagsfördelas. U beräknas av normalårskorrigerad energi december–februari dividerad med september–april, men bolaget publicerar inte metoden för själva normalårskorrigeringen; räkna därför inte fram B från råa mätvärden utan bolagets värde eller en separat verifierad normalårsmodell.
  - [x] Gränserna och B-formlerna är verifierade: 0–0,299 → 0,93; 0,300–0,499 → `0,35U+0,825`; 0,500–0,799 → `1,34U+0,330`; ≥0,800 → 1,40.
  - [ ] Normalårskorrigeringen är inte publicerad. Tariffen får bara aktiveras med leverantörens A och B/U tills denna metod är verifierad. Andra avtalsalternativ ingår inte.

### Vattenfall - Haninge, Tyresö, Älta och Gustavsberg

- Gemensamma källor: [Vattenfalls aktuella prislistor och beräknare 2026](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/), [officiell beskrivning av prismodellen](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/) och [prisändringsmodell med 2026-priser (PDF)](https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf) (`47_0` s.7–8 och de aktuella tvåsidiga 2026-prislistorna)
- **Gemensamt verifierat 2026-09-04:** Volymgruppen baseras på uppmätt energi föregående 1 maj–30 april och rabatten dras per köpt MWh endast oktober–april. Rekommenderad effekt regressionsberäknas från vardagarnas dygnsmedeleffekt oktober–april vid −14 °C; alternativet är medel av tre högsta dygnsmedeleffekter under de tre senaste fullständiga kalenderåren. Effektavgiften kalenderdagsfördelas. Flödespremie/-avgift gäller oktober–april. Ingen separat fast avgift finns (`fixed` ska vara 0). Egen vald effekt utlöser de publicerade överuttagsreglerna.
- [x] **Haninge, Tyresö och Älta – Standard** (`vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-standard-2026`)
  - **✅ Källunderlag godkänt.** Standard gäller när energi/effekt-kvoten inte är under 1,2; använd Vattenfalls rekommenderade effekt tills effektsignaturen implementerats och testats.
- [x] **Haninge, Tyresö och Älta – Spetsig** (`vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Spetsig får bara väljas när energi/effekt-kvoten är under 1,2. Kvoten använder energi och medel av de tre högsta timmedeleffekterna föregående 1 maj–30 april.
- [x] **Gustavsberg – Standard** (`vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-standard-2026`)
  - **✅ Källunderlag godkänt.** Samma verifierade modell, med Gustavsbergs egna publicerade priser och nätmedelvärde för flöde.
- [x] **Gustavsberg – Spetsig** (`vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Samma villkor under 1,2 som ovan, med Gustavsbergs prislista.

### Vattenfall - Motala och Askersund

- Gemensamma källor: [Vattenfalls aktuella prislistor och beräknare 2026](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/), [officiell prismodell](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/) och [prisändringsmodell med 2026-priser (PDF)](https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Motala-och-Askersund-2025.pdf) (`48_0` s.7 och separata aktuella 2026-prislistor för Motala och Askersund)
- **Gemensamt verifierat 2026-09-04:** Samma volym-, rabatt-, flödes-, överuttags- och kalenderdagsregler som ovan. Rekommenderad effekt beräknas vid −15 °C i både Motala och Askersund. Ingen separat fast avgift finns.
- [x] **Motala och Askersund – Standard** (`vattenfall-motala-och-askersund-motala-och-askersund-standard-2026`)
  - **✅ Källunderlag godkänt.** Använd Vattenfalls rekommenderade effekt tills effektsignaturen implementerats och testats.
- [x] **Motala och Askersund – Spetsig** (`vattenfall-motala-och-askersund-motala-och-askersund-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Får bara väljas när energi/effekt-kvoten föregående 1 maj–30 april är under 1,2.

### Vattenfall - Nyköping

- Gemensamma källor: [Vattenfalls aktuella prislistor och beräknare 2026](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/), [officiell prismodell](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/) och [prisändringsmodell med 2026-priser (PDF)](https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Nykoping-2025.pdf) (`49_0` s.7 och aktuell tvåsidig 2026-prislista)
- **Gemensamt verifierat 2026-09-04:** Samma volym-, rabatt-, flödes-, överuttags- och kalenderdagsregler som ovan. Rekommenderad effekt beräknas vid −14 °C. Ingen separat fast avgift finns.
- [x] **Nyköping – Standard** (`vattenfall-nykoping-nykoping-standard-2026`)
  - **✅ Källunderlag godkänt.** Använd Vattenfalls rekommenderade effekt tills effektsignaturen implementerats och testats.
- [x] **Nyköping – Spetsig** (`vattenfall-nykoping-nykoping-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Får bara väljas när energi/effekt-kvoten föregående 1 maj–30 april är under 1,2.

### Vattenfall - Uppsala

- Gemensamma källor: [Vattenfalls aktuella prislistor och beräknare 2026](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/), [officiell prismodell](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/) och [prisändringsmodell med 2026-priser (PDF)](https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Uppsala-2025.pdf) (`50_0` s.7 och aktuell tvåsidig 2026-prislista)
- **Gemensamt verifierat 2026-09-04:** Samma volym-, rabatt-, flödes-, överuttags- och kalenderdagsregler som ovan. Rekommenderad effekt beräknas vid −15 °C. Ingen separat fast avgift finns.
- [x] **Uppsala – Standard** (`vattenfall-uppsala-uppsala-standard-2026`)
  - **✅ Källunderlag godkänt.** Använd Vattenfalls rekommenderade effekt tills effektsignaturen implementerats och testats.
- [x] **Uppsala – Spetsig** (`vattenfall-uppsala-uppsala-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Får bara väljas när energi/effekt-kvoten föregående 1 maj–30 april är under 1,2.

### Vattenfall - Vänersborg

- Gemensamma källor: [Vattenfalls aktuella prislistor och beräknare 2026](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/berakna-ditt-pris/), [officiell prismodell](https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/) och [prisändringsmodell med 2026-priser (PDF)](https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Vanersborg-2025.pdf) (`51_0` s.7 och aktuell tvåsidig 2026-prislista)
- **Gemensamt verifierat 2026-09-04:** Samma volym-, rabatt-, flödes-, överuttags- och kalenderdagsregler som ovan. Rekommenderad effekt beräknas vid −12,5 °C. Ingen separat fast avgift finns.
- [x] **Vänersborg – Standard** (`vattenfall-vanersborg-vanersborg-standard-2026`)
  - **✅ Källunderlag godkänt.** Använd Vattenfalls rekommenderade effekt tills effektsignaturen implementerats och testats.
- [x] **Vänersborg – Spetsig** (`vattenfall-vanersborg-vanersborg-spetsig-2026`)
  - **✅ Källunderlag godkänt.** Får bara väljas när energi/effekt-kvoten föregående 1 maj–30 april är under 1,2.

### VänerEnergi

- [x] **Mariestad och Töreboda** (`vanerenergi-mariestad-och-toreboda-2026`)
  - Källor: [officiell prisöversikt för företag 2026](https://vanerenergi.se/fjarrvarme/priser-fjarrvarme-foretag-2026), [officiell prisändringsmodell 2026–2028 (PDF)](https://vanerenergi.se/download/18.76bfc4fd19a0f6d5c0785f/1761289418005/Pris%C3%A4ndringsmodellen%20Mariestad%20T%C3%B6reboda%20%202026-2028.pdf) (`46_0` s.11,12)
  - **✅ Källunderlag godkänt 2026-09-04.** Effektgrupper, energi- och flödespriser, effektsignatur/alternativregel samt månadsdebitering stämmer med katalogen. Officiella villkor anger att effekt- och fast avgift fördelas jämnt över året.
  - [x] Månadsperiodisering verifierad: 1/12 av den årliga effekt- och fasta avgiften per månad; energi och flöde beräknas på månadens avlästa mängd.

### Öresundskraft

- [ ] **Helsingborg normal** (`oresundskraft-helsingborg-normal-2026`)
  - Källa: [officiell prislista för företagskund 2026](https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/) (`29_0` s.19)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Effektformel och -grupper, energisäsonger och vinterflöde överensstämmer med katalogen. Använd effektvärdet från leverantörens faktura och leverantörens band vid exakta tabellgränser.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Helsingborg Totalvärme, central installerad före 2024** (`oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`)
  - Källa: [officiell prislista för företagskund 2026](https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/) (`29_0` s.20)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Målgruppen, effektformeln, vinterenergipriset och övriga energisäsonger överensstämmer med katalogen. Använd fakturans effektvärde och leverantörens band.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.
- [ ] **Ängelholm normal** (`oresundskraft-angelholm-normal-2026`)
  - Källa: [officiell prislista för företagskund 2026](https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/) (`29_0` s.21)
  - **🟡 Godkänt för årsberäkning 2026-09-04.** Effektformel och -grupper, energisäsonger och vinterflöde överensstämmer med katalogen. Använd effektvärdet från leverantörens faktura och leverantörens band vid exakta tabellgränser.
  - [ ] Månadsperiodisering saknas eller behöver verifieras; årsbelopp får inte automatiskt delas med 12.

### Övik Energi

- [x] **Örnsköldsvik** (`ovik-energi-ornskoldsvik-2026`)
  - Källor: [officiell pris- och villkorssida 2026](https://www.ovikenergi.se/foretag-brf/fjarrvarme/priser-och-villkor), [officiell prislista för Örnsköldsviks tätort 2026 (PDF)](https://www.ovikenergi.se/download/18.22c9a27819936f83d5c305b2/1758525271448/Prislista%20giltig%20fr%C3%A5n%201%20jan%202026%20-%20n%C3%A4ringsidkare%20%C3%96rnsk%C3%B6ldsvik%20t%C3%A4tort.pdf) (`30_1` s.1,2 — rättat efter granskning 2026-09-11-010; `30_0` var Prisdialogens 2025-dokument, inte samma källa)
  - **✅ Källunderlag godkänt 2026-09-04, men katalogrättelse krävs.** Prislistan visar att tariffen enbart består av energi och kapacitet; `fixed: null` ska därför bli verifierad noll. Samtliga kapacitetsband, energipriser och metoder för kapacitetsbehov är publicerade.
  - **⚠️ Katalogfel:** `monthly_proration: "1/12"` ska ersättas med kalenderdagsviktning: årskostnaden delas med årets antal dygn och varje månadsfaktura belastas efter månadens antal dygn.
  - [x] `null` i fast avgift är verifierad noll; någon separat fast avgift finns inte.

---

## Del B — Kräver motorstöd innan verifiering (7 tariffer, 6 bolag)

### Borås Energi och Miljö

- [ ] **Borås, Sjömarken, Sandared, Dalsjöfors, Fristad** (`boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`) — avvisad: `kapacitetsform`
  - Källa: [officiella priser och villkor för företag 2026](https://borasem.se/webb/foretag/fjarrvarme/priserochvillkor2026.4.3b2618bc1976272a99c471fd.html) (`00_0` s.6 och den aktuella webbsidan)
  - **🟡 Godkänt för årsberäkning 2026-09-04 endast med leverantörens prisgrupp, Wn och Q.** Energipriset 609 kr/MWh samt alla sex publicerade årsformler stämmer med katalogen. Grupp 1–2 använder normalårskorrigerad energi `Wn` som beräkningsgrund, medan grupp 3–6 använder kundens maximala erforderliga flöde `Q` i m³/h. `Q` väljs av kunden och ställs in i en installerad flödesbegränsare. Leveransområdet omfattar även Gånghester, som saknas i katalogpostens namn.
  - [ ] Prisintervallen överlappar vid exakt 40, 150, 600, 2 000 och 7 000 MWh. Välj därför prisgrupp från avtal eller leverantörsbesked; automatisk gruppindelning är inte godkänd.
  - [ ] Månadsperiodisering av årsbeloppen är inte publicerad; behåll `monthly_proration: null` och använd inte tariffen för månadsresultat.

### Finspångs Tekniska Verk

- [ ] **Finspång** (`finspangs-tekniska-verk-finspang-2026`) — avvisad: `kapacitetsform`
  - Källor: [Finspångs Tekniska Verks officiella sida för taxor och avtalsvillkor](https://www.finspangstekniska.se/vara-tjanster/fjarrvarme/taxor-avtalsvillkor), [officiell prislista för näringsidkare 2026 (PDF)](https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf), [officiella frågor och svar](https://www.finspangstekniska.se/kundservice/vanliga-fragor-svar/fjarrvarme) och [Prisdialogens prisändringsmodell](https://www.prisdialogen.se/wp-content/uploads/2025/10/Prisandringsmodell-Finspang-2025.pdf) (`07_1` s.1 och webbkällorna)
  - **🟡 Villkorat godkänt 2026-09-04 med Finspångs Tekniska Verks effektvärde P.** Energipriserna 70,86 öre/kWh november–mars, 35,50 öre/kWh april–maj och september–oktober samt 21,22 öre/kWh juni–augusti stämmer. Kapacitetsårskostnaden är `(-0,204 × P + 1 093) × P` till och med 2 600 kW och `98,45 × P + 1 206 554` över 2 600 kW. Årskostnaden kalenderdagsfördelas. Flödesavgiften är 20 kr/m³ när månadens medelreturtemperatur överstiger 55 °C.
  - [ ] Leverantören kan lämna kundens P-värde, men den publika källan beskriver inte en fullständig reproducerbar metod för hur P fastställs. Automatisk effektberäkning är därför inte godkänd.
  - [ ] Katalogposten får endast användas för ordinarie fullvärmeleverans tills motorn stöder prislistans 20-procentiga tillägg när fjärrvärme används som spetsvärme.

### Mälarenergi

- [ ] **Västerås och Hallstahammar, större fastigheter** (`malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026`) — avvisad: `energiform`
  - Källor: [officiell företagsprislista och prismodell 2026](https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/), [officiell flödespremiemodell](https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/) (`22_0` s.5, `web-review-malar-price` och `web-review-malar-flow`)
  - **⛔ Ej godkänt 2026-09-04.** Katalogens första tabell är den aktuella taxan för Västerås/Hallstahammar; den andra, felrubricerade tabellen på webbsidan avser Surahammar, vilket framgår av efterföljande rubrik. Alla listade priser och effektdefinitioner stämmer. Offentligt underlag saknar dock exakt avgränsning för sommarenergin, när och hur överuttagsavgiften debiteras samt debetsatsen när kundens flöde ligger över nätmedlet. Endast premiesatsen 2,50 kr/m³ är publicerad.
  - [ ] Begär fullständiga 2026-villkor för sommarperiod, överuttag och flödesavgift innan taxan implementeras.
- [ ] **Västerås och Hallstahammar, gruppanslutna småhus** (`malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026`) — avvisad: `energiform`
  - Källor: [officiell företagsprislista och prismodell 2026](https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/), [officiell flödespremiemodell](https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/) (`22_0` s.5, `web-review-malar-price` och `web-review-malar-flow`)
  - **⛔ Ej godkänt 2026-09-04.** Katalogens första tabell är den aktuella taxan för Västerås/Hallstahammar; den andra, felrubricerade tabellen på webbsidan avser Surahammar. Alla listade priser och effektdefinitioner stämmer. Offentligt underlag saknar dock exakt avgränsning för sommarenergin, när och hur överuttagsavgiften debiteras samt debetsatsen när kundens flöde ligger över nätmedlet. Dessutom anger flödespremiesidan att systemet gäller stora fastigheter, medan katalogposten lägger det även på gruppanslutna småhus med villkoret `customer_contract_required`.
  - [ ] Bekräfta om flödespremien alls gäller gruppanslutna småhus och begär fullständiga villkor för sommarperiod och överuttag.

### Stockholm Exergi

- [ ] **Stockholm Exergi normal** (`stockholm-exergi-stockholm-exergi-normal-2026`) — avvisad: `energiform`
  - Källor: [lokalt arkiverad officiell prislista 2026 (PDF)](prislistor/stockholm-exergi-2026.pdf), `stockholm-2026` s.1–2 och `web-review-stockholm-clarification` s.1–4
  - **ℹ️ Redan verifierad utanför katalogspåret.** Förtydligade prisvillkor och 18 verkliga fakturor har validerats i den separata handbyggda leverantörsmodellen. Katalogposten hålls ändå avstängd: tvådelad prognos och alternativa vinterregler återstår att mappa i katalogmotorn. Leverantörens effektvärde och −3 °C-gräns kan användas som kundindata. Detta är motorarbete, inte en återstående extern källgranskning.

### Sundsvall Energi

- [x] **Indal, Liden och Lucksta** (`sundsvall-energi-indal-liden-och-lucksta-2026`) — avvisad: `kapacitetsform`
  - Källa: [officiell prislista och prisvillkor 2026](https://sundsvallenergi.se/foretag-och-brf/fjarrvarme/fjarrvarme-for-verksamheten/fjarrvarmepriser) (`39_0` s.5, `web-review-matfors-final` och `web-review-sundsvall-flow`)
  - **✅ Källunderlag godkänt 2026-09-04.** Tariffen består uttryckligen endast av energipriset 100,8 öre/kWh exklusive moms; inga fasta, effekt- eller flödesavgifter tillkommer. Motoravvisningen gäller stöd för en tariff utan kapacitetsdel, inte en källbrist.

### VB Energi

- [ ] **Ludvika, Björnmossen, Grängesberg, Fagersta och Norberg** (`vb-energi-normal-2026`) — avvisad: `energiform`
  - Källa: [officiella prisvillkor för företagskunder 2026](https://www.vbenergi.se/foretag/fjarrvarme/priser/nya-prisvillkor-20222222/), [officiellt samrådsunderlag med 2026-tabellen (PDF)](https://www.vbenergi.se/globalassets/bilagor/fjarrvarme/prisinformation/prisdialogen/presentation--samradsmote-nr-2-2025-09-09.pdf) och [bolagets beskrivning av Björnmossens nät](https://www.vbenergi.se/fjarrvarme/pagaende-projekt/) (`52_0` s.5 och `web-review-vb-2026`)
  - **⛔ Ej godkänt 2026-09-04.** Priserna i katalogen stämmer, och Björnmossen bekräftas vara ett fristående nät i Ludvikaområdet. Däremot motsäger två officiella 2026-källor varandra: prissidan anger att de fem högsta dygnsmedeleffekterna tas under november–mars, medan samrådspresentationen anger december–mars. Källorna anger inte heller vilken årsvolym som väljer energigrupp eller hur den årliga effektavgiften fördelas per månad.
  - [ ] Begär besked om effektperioden är november–mars eller december–mars.
  - [ ] Prisgrupp styrs av årsenergi; bekräfta vilket mät-/normalår och vilken omprövningsdag som väljer grupp.
  - [ ] Månadsperiodisering saknas; årsbelopp får inte automatiskt delas med 12.
  - [x] Ingen separat fast avgift publiceras; katalogens `fixed: null` ska mappas till 0, inte behandlas som ett okänt belopp.
