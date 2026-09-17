---
review_id: "2026-09-17-035"
date: "2026-09-17"
reviewer: Codex
status: blocked
signal: "BLOCKED: Robert"
reviewed_signal: "2026-09-17-034"
approved_by: Codex
dispatched_by: agent-bridge
executed_by: Codex
executed_action: "oberoende granskning av isolerad sanerad Neptune-kandidat"
candidate_approved: true
branch_replacement_allowed: false
push_allowed: false
force_push_allowed: false
tariff_activation_allowed: false
reviewed_heads:
  skills: "09f9b1e0aec5650fab9090984b33d1bd397ce835"
  enkey_agents: "47fdc67386b9db990d63c910069700b75301f743"
  neptune_main: "bb28095cdd97d97bea615849bb132bdfbe4a4897"
  neptune_candidate: "92226dbf16d705365cf9d9d3b52e763dadfad1b5"
live_origin_main_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Granskning av signal 034 — isolerad Neptune-historiksanering

**Kandidaten godkänns tekniskt. BLOCKED: Robert före lokal
branchersättning. Ingen push är godkänd.**

## Oberoende verifierat resultat

Signal 034 är en unik, committad toppost. Skills-commit `09f9b1e` ändrar
endast session/index. Enkey står rent på `47fdc67`. Neptune står rent på
`main@bb28095`; kandidaten finns endast som lokal branchref
`neptune-batch7-history-sanitized-candidate@92226db` och finns inte på
`origin` eller `upstream`. Live `origin/main` matchar värdena ovan;
Neptune `upstream/main` är `fa177e9` och saknar också kandidatrefen.

Kandidaten är en linjär kedja om exakt 13 commits från den verifierade
remotebasen `22b473d`. Följande kontroller passerar:

- kandidatens steg 4 (`a2919a6`) har exakt samma träd som originalets
  sanerade steg `0bdb675`; den utelämnade commiten är därför fullständigt
  absorberad;
- vart och ett av de nio senare kandidatträden är byte-identiskt med
  motsvarande originalträd, inklusive slutträdet
  `7f6e7ecae25fb7f032f387a20e2b94dad0f941ca` för både `92226db` och
  `bb28095`;
- före absorptionspunkten skiljer sig original och kandidat endast i de två
  avsedda testfilerna, och samtliga ändrade rader är kommentarer — ingen
  exekverbar kod eller något facit skiljer sig;
- en konservativ kontroll av alla fyra borttagna kommentarformerna från de
  två rättningspatcharna (inklusive de tre identifierande kommentarerna)
  ger noll träffar i varje kandidatsnapshot och kandidatens
  commitmeddelanden;
- hela kandidatintervallets `git diff --check` är rent och huvudworktreet
  har inte bytts till kandidaten.

Codex körde dessutom om slutträdet oberoende. Eftersom kandidat och
`main@bb28095` har exakt samma träd är huvudworktreet en byte-identisk
testyta:

- Vitest: **2245 passed** i 66 filer;
- `npx tsc --noEmit`: rent;
- isolerat produktionsbygge till `/tmp`: **971 moduler**, grönt;
- ordinarie browsergrind: **Scenario 1–29 gröna**, inklusive Stockholm
  Exergi Scenario 26 och Vattenfall Scenario 27–29.

Första Chromium-starten blockerades av macOS sandboxens Mach-portregel;
omkörning med avgränsad körbehörighet passerade hela sviten. Det var inget
produktfel. Ingen byggartefakt skrevs i repot och produktarbetskopian är
fortsatt ren.

Dispositionen `74 implemented / 2 ready / 16 blocked av 92`, katalogen och
alla tariffaktiveringar är oförändrade: kandidaten ändrar endast
föräldrahistoriken mellan samma bas- och slutträd. Inga råa mejl/PDF:er,
kontaktuppgifter eller bryggfiler har tillförts.

## Nästa separata beslut

Signal 033 tillät uttryckligen bara kandidatframtagning och förbjöd
branchersättning. Robert behöver därför godkänna följande avgränsade lokala
steg innan Claude får fortsätta:

1. verifiera samma HEAD:ar och live-remoter på nytt;
2. skapa en lokal säkerhetsref
   `neptune-batch7-history-original-backup` vid `bb28095`;
3. flytta endast lokala `refs/heads/main` atomiskt från exakt `bb28095` till
   exakt `92226db`; slutträdet och arbetskopian ska därmed förbli identiska;
4. bevara både säkerhetsrefen och kandidatrefen, verifiera ren arbetskopia
   och leverera en ny `REVIEW_READY: Codex`.

Detta beslut omfattar **ingen push**, ingen force-push, ingen ändring av
publicerad historik, ingen tariffaktivering och ingen ändring i Enkey eller
skills produkthistorik. Efter lokal branchersättning krävs en ny Codex-
granskning innan ett eventuellt separat `APPROVED_FOR_PUSH: Claude` kan
övervägas.
