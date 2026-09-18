# Variantfrågor för ej materialiserade tilläggsfunktioner (2026)

Version 2 — 2026-09-18. Skapad av Codex beslut i granskning
[2026-09-17, källnormalisering 002](../conversations/reviews/2026/09/2026-09-17-granskning-kallnormalisering-002.md)
(session `2026-09-17-003`, `CHANGES_REQUIRED: Claude`), rättad av Claude i session
`2026-09-17-004`. Uppdaterad av Claude i session `2026-09-18-045` efter Codex
rättningskrav i granskning
[2026-09-18, källnormalisering 044](../conversations/reviews/2026/09/2026-09-18-granskning-finspang-kallnormalisering-043.md)
för att spegla att Finspångs post stängdes 2026-09-18. Länkad från
`tariffinventering-v22.md` §8a.

## Syfte

De fyra raderna i §8a:s dispositionsmatris (rad 20–22, 28) och i §5:s varianttabell som
är märkta "ej materialiserad variantrad" saknar egen post i
`optimate-fjarrvarme-2026.json:tariffs[]`. De är tilläggsfunktioner eller alternativa
kundval på redan existerande basrader, inte fristående tariffer. Tre av dem —
Södertörns kundvalda effekt, Kraftringen Brunnshög och Tekniska Verken
lågtemperatur — har publicerade 2026-källor och väntar bara på intern modellering
(`source_resolved_implementation_pending`). Den fjärde — Finspångs
spetsvärmetillägg — är stängd och klassad `not_applicable` för 2026: leverantören
bekräftar att prislistans text finns kvar men att inget sådant tillägg debiteras
2026. Den representeras inte som en fysisk `remaining_information_requests`-post,
eftersom dess `tariff_ids` skulle peka på den redan aktiva
`finspangs-tekniska-verk-finspang-2026`-basraden och därmed felaktigt spärra den
för `enkey-agents/tools/tariffer/katalog.py`s kataloggrind.

Detta dokument är den auktoritativa, versionsstyrda platsen för status på dessa fyra
variantfrågor tills de tre öppna eventuellt materialiseras som egna katalograder.

## Dispositionsmatris (4 rader, motsvarar §8a rad 20–22 och 28)

| # | Variant (ej egen katalograd) | Basrad (`tariffs[].id`) | Klassning | Öppen fråga |
|---:|---|---|---|---|
| 1 | Södertörns kundvalda effekt (`sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026--kundvald-effekt`) | `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | `source_resolved_implementation_pending` | Ingen — SFAB 2026-villkoren (överuttag 1032 kr/kW) är publicerade; kräver bara intern modellering. |
| 2 | Kraftringen Brunnshög (`kraftringen-kraftringen-2026--brunnshog`) | `kraftringen-kraftringen-2026` | `source_resolved_implementation_pending` | Ingen — 647 kr/MWh + styckvis returtemperaturdel publicerad; kräver bara intern modellering. |
| 3 | Tekniska Verken lågtemperatur (`tekniska-verken-linkoping-linkoping-2026--lagtemperatur`) | `tekniska-verken-linkoping-linkoping-2026` | `source_resolved_implementation_pending` | Ingen — flödespris okt–apr 2,67 kr/m³ publicerat; kräver bara intern modellering. |
| 4 | Finspångs spetsvärmetillägg (`finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg`) | `finspangs-tekniska-verk-finspang-2026` | `not_applicable` | **Stängd 2026-09-18 (A5 besvarad).** Se rättelse nedan. |

Rad 1–3 kräver inget bolagssvar för att gå vidare till en separat, granskad
aktiveringsrunda. Rad 4 är stängd — inget nytt leverantörssvar behövs för 2026.

## Stängd fråga (2026-09-18): Finspångs spetsvärmetillägg

Historiskt spårad som `R17` i `optimate-fjarrvarme-2026.json` fram till
2026-09-17-rättningen (revision `0.1.27`), då `R17` togs bort ur den fysiska
`remaining_information_requests`-listan eftersom dess `tariff_ids` pekade på den redan
aktiva `finspangs-tekniska-verk-finspang-2026`-basraden och därmed felaktigt fick
kataloggrinden att räkna en rad färre godkänd (60 i stället för 61). Den aktiva basradens
energi-, effekt- och `conditional_flow`-delar påverkas inte av denna fråga eller av att
`R17` togs bort ur den fysiska listan.

**Fråga (oförändrad, ordagrant identisk med tidigare `R17.question_sv` och med brevet
nedan):** Omfattar spetsvärmekunders 20-procentiga prispåslag hela summan av energi-,
effekt- och flödesavgift eller bara vissa prisdelar? Hur klassas en kund som
spetsvärmekund, och gäller klassningen hela avtals-/kalenderåret eller kan den
börja/sluta en viss månad?

**Frågedokument (återanvänt, inte duplicerat):**
[A5 i `leverantorsfragor-blockerade-tariffer-2026.md`](leverantorsfragor-blockerade-tariffer-2026.md#a5-finspångs-tekniska--omfattningen-av-20-procents-spetsvärmetillägg)
innehåller det fullständiga, skickbara mejlet till Finspångs Tekniska Verk.

**Status (t.o.m. 2026-09-17):** `utreds`, öppen sedan 2026-09-17 (`created_on` i den
tidigare `R17`-posten).

**Svar mottaget 2026-09-17, bedömt 2026-09-18:** Finspångs Tekniska Verk bekräftar att
prislistans text om spetsvärmetillägg finns kvar, men att inget sådant tillägg har
debiterats kunder 2026 och att bolaget saknar en tillämpad debiteringsmodell. Den
sanitiserade bedömningen finns i
[`2026-09-18-bedomning-finspang-spetsvarmetillagg.md`](Svar%20på%20frågor/2026-09-18-bedomning-finspang-spetsvarmetillagg.md)
(originalmejlet innehåller personuppgifter och committas inte).

**Beslut:** variantposten klassas `not_applicable` för 2026 — det finns ingen faktisk
debiteringsregel att modellera, och kalkylatorn ska inte konstruera ett 20-procentigt
påslag från prislistans oklara formulering. Detta är en käll- och
dispositionsnormalisering, inte en implementation eller aktivering. Finspångs redan
implementerade bastariff `finspangs-tekniska-verk-finspang-2026` är oförändrad. Ingen
ny katalograd, produktkod eller prisändring följer av detta.

**Nästa steg om läget ändras:** om en senare prislista eller ett kundavtal inför ett
faktiskt spetsvärmetillägg måste den nya debiteringsmodellen källgranskas från början
innan en variant får byggas eller aktiveras — samma krav som tidigare, oförändrat av
denna stängning.
