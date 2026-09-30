---
handoff_id: "2026-09-30-002"
created_at: "2026-09-30T18:43:42+02:00"
from: Codex
to: Claude
status: approved-for-activation
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_ACTIVATION: Claude – kör våg 2 direkt i huvudsessionen

## Beslut

Signal `2026-09-30-001` stoppades utan kodändring när Claudes interna
underagentsanrop nekades av körmiljön. Det ändrar inte Roberts och Codex
tidigare godkännande. Robert har redan sagt "Då kan du köra på" och behöver
inte ge ett nytt klartecken eller en bredare Bash-behörighet.

Utför därför aktiveringen **direkt i denna Claude-huvudsession**. Starta
ingen underagent och delegera inte arbetet. Använd de vanliga filverktygen
och avgränsade testkommandona själv, vänta in alla verifieringar och skriv
nästa committade signal innan sessionen avslutas.

Verifierat nuläge efter det avbrutna försöket:

- inga kod-, matris- eller dokumentationsändringar gjordes av Claude;
- skills `main@b73a19f7bedda6b909b35bedbed63851bc06905d` är en ren
  efterföljare till den granskade skills-basen `b742565`;
- Neptune `main` och `origin/main` är fortsatt
  `f3ce263c532bdc9733acbe6e59a373ac90bc0336`;
- den rena isolerade grenen `worktree-agent-ae46c6f3096412378` finns kvar
  vid den granskade kandidaten
  `5d91de6feec313f2f5d0f802d198e40d41cf2c15`;
- Neptune-main är kandidatens rena förfader; ingen merge eller rebase krävs
  för den lokala aktiveringsdiffen.

## Bindande aktiveringsscope

Följ exakt den redan slutgodkända specifikationen i
[`2026-09-30-slutgodkannande-optimate-vag-2-signal-004.md`](../../../reviews/2026/09/2026-09-30-slutgodkannande-optimate-vag-2-signal-004.md):

1. Publik lista ska vara mekaniskt härledd som våg 1 + samtliga 15
   `WAVE_2_PRODUCT_IDS`, exakt 17 unika produkter.
2. Bind exakt lista, frysning, unikhet och ID→backend mot pilotsnapshoten i
   test.
3. Behåll negativa prov för minst ett våg-3-ID, okänt ID och `undefined`;
   Stockholm förblir separat prototyp.
4. Ändra inte tariffdata, prisformler, backendval, capability-flaggor,
   Enkey eller 10/15/20-logik.
5. Bevisa synligt scenario i React-/sidprov för Halmstad, Sandviken och en
   vanlig `kontraktsgatad_kostnadsled`.
6. Lägg positiva Chromium/E2E-kontroller för alla tre backendfamiljer och
   en negativ våg-3-kontroll; bind kostnadsfacit.
7. Regenerera matrisen endast via generatorn till 17 publika, 0 interna,
   1 prototyp och 59 ej granskade.

Kör hela verifieringsgrinden från signal 001. Committa fokuserat i den
isolerade Neptune-worktreen och skills-repot och lämna en unik
`ACTIVATION_READY: Codex`. Ingen mainflytt, merge, rebase, push, force
eller historikomskrivning ingår.

Om ett verkligt tekniskt hinder ändå återstår ska Claude själv skriva och
committa en unik `BLOCKED: Codex` med exakt reproduktion. Avsluta inte på
nytt enbart för att underagentsanrop inte används — direkt körning är den
uttryckliga instruktionen för denna signal.
