---
review_id: "2026-09-25-009"
date: "2026-09-25"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-25-008"
skills_reviewed_head: "3e8e9fb17e8580636605c671d1cb7c94525ae78e"
neptune_reviewed_branch: "optimate-vag1-ren-energi"
neptune_reviewed_base: "1bfe1037063e1713dfbb54bfcc62d94b848b24f8"
neptune_reviewed_head: "2b57bd859abf3e80c63ca43539b70699da5a9ad0"
activation_allowed: false
push_allowed: false
approved_by: "Codex"
---

# Granskning av Optimate våg 1, signal 008

## Beslut

Leveransen behöver rättas innan våg 1 kan godkännas. De oberoende
kostnadsfaciten och den tomma publika allowlisten är korrekta, men den
valda inkopplingen ändrar en redan publik Gotlandsfunktion, redigerar en
genererad tariffil för hand och lämnar den beställda sidkopplingen
ofärdig.

Rätta append-only ovanpå den befintliga våg-1-branchen. Skriv inte om
historiken, aktivera ingen tariff, mergea inte och pusha inte.

## Fynd

### P1 — den manuella katalogpatchen slår ut Gotlands befintliga väg

`neptune-marketing/src/data/tariffer.generated.ts` säger själv
`GENERERAD FIL — redigera inte`, men commit `6c78871` lägger in en
handskriven `_kraver_kontrakt`-policy för Gotland taxa 17. Policyn sätter
`stodjer_besparing: false`. Därmed går det befintliga publika anropet
från ett faktiskt resultat till
`Produktbegransning('besparing_ej_stodd')`.

Det strider mot handoffens krav att de äldre resultaten ska bevaras och
mot avgränsningen att Enkey inte ska ändras. Påståendet i kommentaren att
kontraktsgatning är den enda möjliga arkitekturen godtas inte.

Rättning:

1. Återställ innehållet från `6c78871` i en ny commit: den genererade
   filen ska åter motsvara generatorns utdata; ta bort den nya
   `_manadsuppdelningForKontraktfasad`, katalogaktiveringstestet och de
   parityändringar som bara kompenserar för kontraktsgatningen.
2. Bevara och bind regressionstest för Gotlands befintliga publika facit:
   40 MWh totalvärme, 20 MWh påverkbar värme och 50 procent ska fortsatt
   ge 50 570 kr före, 38 020 kr efter och 12 550 kr besparing.
3. Ge scenariomotorn två smala kostnadsbackendar bakom samma fail-closed
   produktregister: Sundsvall använder fortsatt
   `beraknaArsproduktMedKostnadsled`; Gotland använder den befintliga
   legacy-/årskostnadsmotorn med explicita månadsserier. Duplicera ingen
   prisformel och byt aldrig taxa 17 mot taxa 21 mellan före och efter.
4. Ett oregistrerat legacy-ID och en kontraktsprodukt på fel backend ska
   avvisas. Skapa ingen allmän genväg runt kontraktsgrinden.

### P1 — beställd verklig UI-koppling saknas

`OptimateScenarioCard` och adaptern används inte av
`KalkylatorPage.tsx`. Fristående komponentprov visar därför inte att
användarens formulärdata når motorn eller att resultatet kan visas efter
de två befintliga resultatvägarna.

Koppla in den gemensamma scenariovyn på kalkylatorsidan för både
Gotland/legacy-resultatet och Sundsvall/årskostnadsresultatet. Den
auktoritativa publika allowlisten ska förbli tom, så ingen ny vy syns i
den normala byggnaden. Lägg sid-/Reactprov som med en testlokal
modulmock öppnar exakt respektive produkt samt ett ordinarie negativt
browserprov mot verklig tom allowlist.

### P1 — produktionskomponenten har en publik spärrbypass

`OptimateScenarioCardProps.stodjerPubliktAktiverad` låter varje anropare
ersätta den auktoritativa grinden med en funktion som returnerar `true`.
Att kommentaren säger att produktionskod inte ska använda propen är
inte ett tekniskt skydd.

Ta bort propen ur produktionsgränssnittet. Öppna grinden i prov genom en
testlokal modulmock eller prova en ren presentationsdel som inte själv
äger aktiveringsbeslutet.

### P1 — rumsvärmeskattningen är varken synlig, ändringsbar eller rätt beskriven

Adaptern returnerar `skattningsAntaganden`, men kortet tar bara emot
motorresultatet och visar aldrig denna metadata. Det finns heller inget
fält på sidan där användaren kan ändra den skattade rumsvärmen eller
baslasten. Texten säger dessutom att rumsvärmen är 82 procent av totalen,
trots att formeln drar av en flat 18-procents årsbaslast per månad och
klipper negativa månader till noll; då behöver årssumman inte bli
82 procent.

Gör den styrbara rumsvärmen till faktisk, synlig och validerad indata.
Om fallbacken behålls ska exakt antagande visas som exempelvis ”upp till
18 procent av årsenergin som jämn baslast” och användaren ska kunna ändra
värdet/serien innan beräkning. För vidare skattningsmetadata till
resultatkortet. Tolv totalmånader och tolv rumsvärmemånader ska summera
mot sina visade årsbelopp och rumsvärme får aldrig överstiga totalvärmen
i någon månad. En användarredigerad skattning ska kunna behålla korrekt
`estimated_mwh`-proveniens; typen får inte tvinga allt användarangivet
till `confirmed_mwh`.

### P2 — full verifieringsgrind saknas

Signal 008 redovisar 2 444/2 445 Vitest och inget bygge eller E2E.
Härnösandsprovet är miljöberoende men ska inte lämnas rött: kör mot exakt
`/private/tmp/enkey-agents-harnosand-2026` i en isolerad syskonlayout,
samma låsta källa som portföljgrunden.

Rättningsleveransen ska redovisa:

- full Vitest helt grön mot den låsta Enkey-snapshoten;
- `npx tsc --noEmit`;
- isolerat bygge med spårad `dist/` ren efteråt;
- ordinarie browser-E2E, inklusive det negativa våg-1-provet;
- `git diff --check` och ren worktree;
- exakta nya commit-hashar och `REVIEW_READY: Codex`.

## Oberoende kontroll

- Codex: 146/146 riktade TypeScript-prov gröna över motor, Gotlandsfacit,
  adapter, kort, legacyaktivering och fjärrvärmemotor.
- Codex: `npx tsc --noEmit` rent.
- Codex: 17/17 matrisprov, generatorns `--check` och båda repornas
  diffkontroll gröna.
- Publik scenarioallowlist är fortsatt tom.

Matrisens interna pilotstatus för Gotland får ligga kvar endast om den
rättade implementationen klarar hela grinden. Annars ska Gotland
återställas till `not_reviewed` i matrisen.
