---
session_id: "2026-09-21-002"
started_at: "2026-09-21T13:00:00+02:00"
last_updated: "2026-09-21T13:11:49+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: locally-verified-not-pushed
topics:
  - Stockholm Exergi
  - rumsvärme
  - månadsfördelning
source: visible-conversation
transcript_fidelity: summarized
---

# Stockholm Exergi: rumsvärme skild från köpt totalvärme

## Roberts frågor

> Stämmer verkligen värmefördelningen över månaderna? Det borde vara noll eller väldigt nära noll under juni, juli och augusti? Det är inte så att det är med varmvattenförbrukning i schablonvärdena?

> om jag bockar i "Enbart rumsvärme/radiatorvärme (exkl. varmvatten och ventilationsvärme)" så måste kalkylen hantera ovanstående.

## Svar och lokal ändring

Ja, den tidigare visade totalserien innehöll en jämn, antagen 18-procentig
tappvarmvattenlast även när användaren hade valt enbart rumsvärme. För den
omfattningen visar de tolv redigerbara rutorna nu i stället bara rumsvärme,
och de summerar till den angivna rumsvärmens årsenergi. Med flerbostadshus
1975–1995 och 1 000 MWh rumsvärme blir juni <10, juli <1 och augusti <3
MWh enligt normalårsmodellen. För tariffpriset läggs separat en uppskattad,
jämn tappvarmvattenlast på den interna totalserien. Byte mellan totalvärme
och rumsvärme rensar den tidigare månadsserien, även om den var manuellt
redigerad.

18 procent är härlett ur ett verifierat kundexempel, inte en generell
SMHI-faktor. SMHI:s [guide för normalårskorrigering](https://www.smhi.se/download/18.1cdddc041958439e87f232/1741699305087/Guide%20Normal%C3%A5rskorrigering%20v%C3%A4rme.pdf)
skiljer på väderberoende värme och väderoberoende baslast, men ger inte denna
andel. Separat ventilationsvärme kan inte härledas ur rumsvärmen och ingår
inte i den uppskattade totalen. Detta framgår nu i formuläret; för sådan
last bör användaren välja total köpt värme och använda fakturavärden.

## Verifiering och handoff

- Neptune: 2 266/2 266 TypeScript-test, ren `tsc`, produktionsbygge och
  samtliga E2E-scenarier gröna, inklusive riktig Chromium för båda
  omfattningarna och kostnadsberäkning för rumsvärme.
- Ny lokal förhandsvisning: `http://127.0.0.1:4174/kalkylator`. Den
  befintliga servern på port 4173 visar fortfarande en äldre byggversion.
  Förhandsvisningen använder den git-ignorerade `dist-eval/`-byggnaden;
  spårade `dist/`-filer som det vanliga bygget först ändrade är återställda
  från oförändrat HEAD utan att röra källkod eller andra arbetskopieändringar.
- Metodunderlaget `Fjarrvarmetariffer/stockholm-exergi-schablonunderlag-2026.md`
  har uppdaterats. Orelaterade arbetskopieändringar har inte berörts.
- Ingen commit, push eller tariffaktivering gjord i denna uppföljning.
