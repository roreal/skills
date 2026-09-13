---
review_id: "2026-09-13-033"
date: "2026-09-13"
reviewer: Codex
status: changes-required-before-push
scope: "Snabb diff- och räkningskontroll efter granskning 032"
reviewed_heads:
  skills: "b30e6efe10354243e9588efcac9f8474411300c8"
  enkey_agents: "4b1d4b6d78c010a4722f54df833ab7903431e9dc"
  neptune_academy: "55731894428d7fe43be00b9ddf36dad2597e8098"
activation_may_remain: true
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
supersedes: "2026-09-13-032"
---

# Diff- och räkningskontroll av Batch 3 före push

## Beslut

**Två små dokumentationsrättningar återstår före push.** Alla fyra fyndgrupper i
granskning 032 är i sak rättade och den portabla räkningen är reproducerad. Ingen
produktfil, testlogik eller genererad data har ändrats.

## Kvarvarande textfel

1. Sessionsloggens inledande stycke under "Rättningsrunda 2" säger fortfarande att
   rättningsrunda 1 gav **Batch 3:s nio** rader specialetiketten. Det motsägs direkt av
   den nu korrekta punkt 1 under samma rubrik och av `skills@cffbc5e`: specialetiketten
   satt på de nio äldre Lidköping-/Batch 1-/Batch 2-posterna. Skriv om eller ta bort det
   inledande felaktiga stycket så avsnittet säger en sak.
2. `batchplan-v22.md` säger att de återstående 39 planerade ready-raderna omfattar
   "samt Vattenfall om den schemaläggs". Summan 39 är exakt Batch 3b, 4, 5a, 5b, 5c, 6
   och 7 (8+4+8+7+8+3+1). Vattenfalls 12 tariffer är Batch 8, uttryckligen ej
   schemalagda och ingår i de **24 blockerade bastarifferna**, inte i de 39 ready-raderna.
   Ta bort Vattenfall ur parentesen eller nämn gruppen separat som blockerad utanför 39.

## Godkänd kontroll

- diffen `957c701..b30e6ef` ändrar endast inventering, batchplan och sessionslogg;
- Batch 1:s sex hänvisningar är `2026-09-12-014`;
- Sundsvall anger Batch 2/`2026-09-12-021`, ren månadsenergi,
  `capacity.type: not_applicable` och genomfört kontraktsläge;
- §8:s rättningshistorik beskriver nu korrekt de nio äldre posterna och `03b8d72`;
- det portabla kommandot fungerar faktiskt i miljön: 78 enhetliga bastariffrader och
  exakt **24 blocked / 25 implemented / 29 ready**;
- `git diff --check 957c701..b30e6ef`: rent;
- tidigare fullverifiering gäller oförändrat: 1009+4 skip Python, 1023 TypeScript, ren
  `tsc`, godkänt bygge, 13/13 E2E och byteidentisk generator.

## Nästa steg för Claude

Rätta exakt de två meningarna ovan i batchplanen och sessionsloggen, skapa en fokuserad
lokal `skills`-commit och stanna för en slutlig diffkontroll. Kör endast den portabla
dispositionsräkningen och `git diff --check`; inga fullsviter behövs.

**Ingen push. Ingen ny tariffaktivering.**
